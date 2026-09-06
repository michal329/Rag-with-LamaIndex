import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
STRUCTURED_DATA_PATH = DATA_DIR / "structured_data.json"

SOURCE_FILES = [
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "INSTRUCTIONS_HE.md",
] + sorted((DATA_DIR / "md_files").glob("*.md"))

CATEGORY_KEYWORDS = {
    "decisions": ["החלטה", "החלטות", "נבחר", "הוחלט", "decision"],
    "rules": ["הנחיה", "הנחיות", "כלל", "כללים", "חובה", "אסור", "יש לה", "אין"],
    "warnings": ["אזהרה", "אזהרות", "רגיש", "סיכון", "סכנה", "לא לגעת"],
}

TIME_TRIGGERS = {
    "שבוע האחרון": 7,
    "בשבוע האחרון": 7,
    "חודש האחרון": 30,
    "בחודש האחרון": 30,
    "היום": 1,
}


def _line_number_for(text: str, marker: str) -> int:
    if not marker:
        return 1

    index = text.find(marker)
    if index == -1:
        return 1

    return text[:index].count("\n") + 1


def _source_for(path: Path, anchor: str, line_range: tuple[int, int]) -> dict[str, Any]:
    return {
        "tool": "doc",
        "file": path.relative_to(PROJECT_ROOT).as_posix(),
        "anchor": anchor,
        "line_range": [line_range[0], line_range[1]],
    }


def _append_item(dataset: dict[str, Any], category: str, item: dict[str, Any]) -> None:
    dataset["items"][category].append(item)


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _sentence_summary(text: str, max_chars: int = 120) -> str:
    normalized = _normalize_text(text)
    match = re.search(r"([^.?!]*[.?!])", normalized)
    if match:
        return match.group(1).strip()
    return normalized[:max_chars].rstrip() + ("..." if len(normalized) > max_chars else "")


def _infer_scope(text: str) -> str:
    normalized = text.lower()
    if any(tok in normalized for tok in ["ui", "ממשק", "מסך", "frontend"]):
        return "ui"
    if any(tok in normalized for tok in ["data", "קובץ", "נתונים", "database"]):
        return "data"
    return "general"


def _infer_severity(text: str) -> str:
    normalized = text.lower()
    if any(tok in normalized for tok in ["חמור", "גבוה", "high", "urgent"]):
        return "high"
    if any(tok in normalized for tok in ["בינוני", "medium", "warning"]):
        return "medium"
    return "low"


def _guess_category(text: str) -> str | None:
    normalized = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return None


def _line_range_for(text: str, start_line: int, end_line: int) -> tuple[int, int]:
    return start_line, end_line


def _extract_markdown_items(path: Path) -> dict[str, list[dict[str, Any]]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    current_heading = ""
    start_line = 1
    buffer: list[str] = []
    extracted = {"decisions": [], "rules": [], "warnings": []}

    def flush_paragraph(end_line: int) -> None:
        nonlocal start_line, buffer
        if not buffer:
            start_line = end_line + 1
            return

        paragraph = _normalize_text("\n".join(buffer))
        category = _guess_category(paragraph)
        if category:
            anchor = current_heading or path.stem
            observed_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).replace(microsecond=0).isoformat()
            item: dict[str, Any] = {
                "source": _source_for(path, anchor, _line_range_for(paragraph, start_line, end_line)),
                "observed_at": observed_at,
            }

            if category == "decisions":
                item.update(
                    {
                        "title": _sentence_summary(paragraph, 80),
                        "summary": paragraph,
                        "tags": [tok for tok in ["rag", "cohere", "pinecone", "gradio", "llama-index"] if tok in paragraph.lower()],
                    }
                )
            elif category == "rules":
                item.update(
                    {
                        "rule": _sentence_summary(paragraph, 100),
                        "scope": _infer_scope(paragraph),
                        "notes": paragraph,
                    }
                )
            else:
                item.update(
                    {
                        "area": _infer_scope(paragraph),
                        "message": _sentence_summary(paragraph, 100),
                        "severity": _infer_severity(paragraph),
                    }
                )

            extracted[category].append(item)

        buffer = []
        start_line = end_line + 1

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            current_heading = stripped.lstrip("# ").strip()
        if not stripped:
            flush_paragraph(idx)
            continue
        if not buffer:
            start_line = idx
        buffer.append(line)

    if buffer:
        flush_paragraph(len(lines))

    return extracted


def _incremental_id(category: str, index: int) -> str:
    prefix = {"decisions": "dec", "rules": "rule", "warnings": "warn"}.get(category, "item")
    return f"{prefix}-{index:03d}"


def _parse_time_filter(query: str) -> int | None:
    normalized = query.lower()
    for trigger, days in TIME_TRIGGERS.items():
        if trigger in normalized:
            return days
    return None


def _filter_recent_items(items: list[dict[str, Any]], days: int) -> list[dict[str, Any]]:
    threshold = datetime.now(timezone.utc) - timedelta(days=days)
    filtered: list[dict[str, Any]] = []
    for item in items:
        try:
            observed = datetime.fromisoformat(item.get("observed_at", ""))
            if observed.tzinfo is None:
                observed = observed.replace(tzinfo=timezone.utc)
            if observed >= threshold:
                filtered.append(item)
        except ValueError:
            continue
    return filtered


def generate_structured_dataset() -> dict[str, Any]:
    dataset = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sources": [],
        "items": {"decisions": [], "rules": [], "warnings": []},
    }

    for path in SOURCE_FILES:
        if not path.exists():
            continue

        dataset["sources"].append(
            {
                "tool": "doc",
                "root_path": path.parent.relative_to(PROJECT_ROOT).as_posix(),
                "files": [
                    {
                        "path": path.relative_to(PROJECT_ROOT).as_posix(),
                        "last_modified": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                        .replace(microsecond=0)
                        .isoformat(),
                    }
                ],
            }
        )

        extracted = _extract_markdown_items(path)
        for category in dataset["items"]:
            dataset["items"][category].extend(extracted[category])

    # השארת פריטי אבן דרך ידניים לשמירה על יציבות ודוגמאות מוכרות
    _append_item(
        dataset,
        "decisions",
        {
            "id": "dec-001",
            "title": "הפרויקט משתמש ב-LlamaIndex, Cohere ו-Pinecone",
            "summary": "הזרימה מבוססת LlamaIndex עם embeddings מ-Cohere, אינדקס וקטורי ב-Pinecone, והצגת התוצאות דרך Gradio.",
            "tags": ["rag", "llama-index", "cohere", "pinecone", "gradio"],
            "source": _source_for(
                PROJECT_ROOT / "README.md",
                "LlamaIndex / Cohere / Pinecone",
                [1, 40],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    _append_item(
        dataset,
        "decisions",
        {
            "id": "dec-002",
            "title": "Agentic Coding משתמש בכלי AI שונים לפיתוח",
            "summary": "במסמך Agentic Coding נזכרים Cursor, Claude Code, Kiro, GitHub Copilot ו-Cody ככלים זמינים לפיתוח.",
            "tags": ["agentic-coding", "tools", "cursor", "claude", "kiro", "copilot", "cody"],
            "source": _source_for(
                PROJECT_ROOT / "data" / "md_files" / "agentic_coding.md",
                "כלים זמינים",
                [1, 20],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    _append_item(
        dataset,
        "decisions",
        {
            "id": "dec-003",
            "title": "Gradio משמש לממשק משתמש מקומי ל-LLM",
            "summary": "הפרויקט מציג ממשק Gradio מקומי, והפעולה המרכזית היא launch() שמפעילה את הממשק על localhost.",
            "tags": ["gradio", "ui", "launch"],
            "source": _source_for(
                PROJECT_ROOT / "data" / "md_files" / "gradio_intro.md",
                "Gradio - ממשקי משתמש ל-LLM",
                [1, 30],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    # כללים / הנחיות
    _append_item(
        dataset,
        "rules",
        {
            "id": "rule-001",
            "rule": "שומרים את קבצי ה-Markdown בתיקייה data/md_files",
            "scope": "data",
            "notes": "המערכת בונה את ההתייחסות לתוכן דרך קבצי Markdown שנמצאים ב-data/md_files.",
            "source": _source_for(
                PROJECT_ROOT / "INSTRUCTIONS_HE.md",
                "קבצי MD",
                [20, 40],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    _append_item(
        dataset,
        "rules",
        {
            "id": "rule-002",
            "rule": "הרצת האפליקציה נעשית עם python src/main.py לאחר הפעלת הסביבה",
            "scope": "run",
            "notes": "מומלץ להשתמש ב-.venv311 ולהפעיל את הסביבה לפני הריצה.",
            "source": _source_for(
                PROJECT_ROOT / "INSTRUCTIONS_HE.md",
                "הרצת האפליקציה",
                [40, 60],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    _append_item(
        dataset,
        "rules",
        {
            "id": "rule-003",
            "rule": "Gradio צריך להיפתח דרך launch() כך שיתגלה בממשק מקומי",
            "scope": "ui",
            "notes": "המסמך מציין ש-launch() מפעיל את הממשק המקומי בפורט 7860.",
            "source": _source_for(
                PROJECT_ROOT / "data" / "md_files" / "gradio_intro.md",
                "launch()",
                [20, 30],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    # אזהרות
    _append_item(
        dataset,
        "warnings",
        {
            "id": "warn-001",
            "area": "auth",
            "message": "חוסר במפתחות COHERE_API_KEY או PINECONE_API_KEY יפגע בהרצת המערכת",
            "severity": "high",
            "source": _source_for(
                PROJECT_ROOT / "INSTRUCTIONS_HE.md",
                "מפתחות Cohere ו-Pinecone",
                [20, 40],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    _append_item(
        dataset,
        "warnings",
        {
            "id": "warn-002",
            "area": "infrastructure",
            "message": "צריך ליצור index בשם rag-md ב-Pinecone לפני הרצת הקוד",
            "severity": "high",
            "source": _source_for(
                PROJECT_ROOT / "INSTRUCTIONS_HE.md",
                "Pinecone Index",
                [26, 40],
            ),
            "observed_at": dataset["generated_at"],
        },
    )

    # assign stable ids for extracted elements if needed
    for category in dataset["items"]:
        for idx, item in enumerate(dataset["items"][category], start=1):
            item.setdefault("id", _incremental_id(category, idx))

    return dataset


def save_structured_dataset(dataset: dict[str, Any] | None = None) -> dict[str, Any]:
    dataset = dataset or generate_structured_dataset()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STRUCTURED_DATA_PATH.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    return dataset


def load_structured_dataset() -> dict[str, Any]:
    if STRUCTURED_DATA_PATH.exists():
        return json.loads(STRUCTURED_DATA_PATH.read_text(encoding="utf-8"))

    return save_structured_dataset(generate_structured_dataset())


def infer_structured_category(query: str) -> str | None:
    normalized = query.strip().lower()

    if any(token in normalized for token in ["החלטה", "החלטות", "טכני", "טכניות", "כל ההחלטות"]):
        return "decisions"

    if any(token in normalized for token in ["הנחיה", "הנחיות", "כלל", "כללים", "נוהל", "נוהלים"]):
        return "rules"

    if any(token in normalized for token in ["אזהרה", "אזהרות", "רגיש", "לא לגעת", "סיכון", "warning"]):
        return "warnings"

    return None


def is_structured_query(query: str) -> bool:
    normalized = query.strip().lower()
    triggers = [
        "רשימה",
        "החלטות",
        "החלטה",
        "הנחיה",
        "הנחיות",
        "כללים",
        "אזהרה",
        "רגיש",
        "לא לגעת",
        "אילו",
        "עדכנית",
        "שבוע האחרון",
        "חודש האחרון",
        "היום",
    ]

    return any(trigger in normalized for trigger in triggers)


def build_structured_response(query: str) -> str:
    dataset = load_structured_dataset()
    items = dataset["items"]
    category = infer_structured_category(query)
    normalized_query = query.lower()

    if category:
        selected_items = items.get(category, [])
    else:
        selected_items = items["decisions"] + items["rules"] + items["warnings"]

    if not category and "rtl" in normalized_query:
        selected_items = [
            item
            for item in items["rules"]
            if "rtl" in (item.get("rule", "") or "").lower()
            or "rtl" in (item.get("notes", "") or "").lower()
        ]
        category = "rules"

    recent_days = _parse_time_filter(query)
    if recent_days is not None:
        selected_items = _filter_recent_items(selected_items, recent_days)

    if category == "rules" and "rtl" in normalized_query and not selected_items:
        return (
            "לא נמצאה הנחיה מפורשת לגבי RTL במסמכים הנוכחיים. "
            "הנתונים הזמינים עוסקים ב-launch(), בנתיבי קבצים, בהפעלת הסביבה ובמפתחות API."
        )

    if not selected_items:
        return "לא נמצאו פריטים מובנים התואמים לשאלה הזו."

    if category == "decisions":
        header = "החלטות"
    elif category == "rules":
        header = "כללים / הנחיות"
    elif category == "warnings":
        header = "אזהרות"
    else:
        header = "פריטים מובנים"

    lines = [f"{header}:", ""]
    for index, item in enumerate(selected_items, start=1):
        if category == "decisions":
            title = item.get("title")
            summary = item.get("summary")
            lines.append(f"{index}. {title}\n   {summary}")
        elif category == "rules":
            lines.append(f"{index}. {item.get('rule')}\n   תחום: {item.get('scope')}\n   הערה: {item.get('notes')}")
        else:
            lines.append(f"{index}. {item.get('message')}\n   אזור: {item.get('area')}\n   רמת חומרה: {item.get('severity')}")

        source = item.get("source", {})
        lines.append(f"   מקור: {source.get('file')}")

    return "\n".join(lines)
