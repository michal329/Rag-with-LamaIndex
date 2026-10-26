---
title: Event-Driven RAG System
emoji: 📚
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 6.29.0
python_version: "3.12"
app_file: app.py
pinned: false
short_description: Event-driven RAG over Markdown with LlamaIndex and Cohere
---

# Event-Driven RAG with LlamaIndex

A small question-answering app over a folder of Markdown files. Questions are routed to one of two paths:

- **Semantic path (RAG):** a LlamaIndex `Workflow` retrieves the most similar chunks using Cohere embeddings and asks a Cohere LLM to answer from them only.
- **Structured path:** questions that ask for decisions, rules, warnings, or "what changed in the last week/month/today" are answered directly from `data/structured_data.json`, with no LLM or API call.

The knowledge base (`data/md_files/*.md`) and the user-facing prompts and answers are in **Hebrew**; the embedding model is multilingual. The UI is a Gradio `Interface`.

## Architecture

```
Gradio textbox
      |
run_rag_workflow(query)                       src/main.py
      |
is_structured_query(query)?  --yes-->  build_structured_response(query)   src/structured_data.py
      |no                                      reads data/structured_data.json
      v
RAGWorkflow (llama_index.core.workflow.Workflow)
  StartEvent
    -> validate_input      trims; rejects empty / <3 chars          -> InputValidatedEvent
    -> retrieve_context    top-5 vector search (also on retry)      -> RetrievalDoneEvent
    -> validate_results    best score < 0.35 or no hits?
                             first time: rewrite query              -> RetrySearchEvent (back to retrieve_context)
                             second time: give up                   -> StopEvent("no relevant results")
                           otherwise                                -> SynthesisReadyEvent
    -> generate_answer     Cohere chat, prompt says "answer from the context only,
                           otherwise say you don't know"            -> AnswerReadyEvent
    -> finish                                                       -> StopEvent(answer)
```

`workflow_flowchart.html` is a Mermaid diagram of the routing (open it in a browser; it loads Mermaid from a CDN).

Components, as implemented:

| Piece | What the code uses |
|---|---|
| Orchestration | LlamaIndex `Workflow`, typed `Event`s, `@step` (`src/main.py`) |
| Embeddings | Cohere `embed-multilingual-v3.0` via `llama-index-embeddings-cohere` |
| LLM | Cohere `command-r-08-2024` via `llama-index-llms-cohere` |
| Vector index | LlamaIndex `VectorStoreIndex` held **in memory**, built from `data/md_files` on the first semantic question and cached for the process lifetime |
| UI | Gradio `Interface` (`app.py` for Spaces, `python src/main.py` also works) |
| Structured data | `src/structured_data.py` + `data/structured_data.json` (keyword routing, optional time filter) |

**No Pinecone.** Earlier versions of this project planned a Pinecone vector store; the current code does not import or use it, and no Pinecone key is needed.

### Structured path details

- Routing is keyword-based (Hebrew trigger words such as החלטות, הנחיות, אזהרה, שבוע האחרון, היום).
- The JSON holds three categories: `decisions`, `rules`, `warnings`. The shipped file contains 8 items in total (3 decisions, 3 rules, 2 warnings), written by hand in `generate_structured_dataset()`. The function can also extract items from Markdown paragraphs by keyword, but the three sample documents currently yield none.
- Time filters ("last week", "last month", "today") compare each item's `observed_at` with now. In the shipped JSON, `observed_at` is the generation time, so these filters return items only while the file is recent; regenerate with `python -c "from src.structured_data import save_structured_dataset; save_structured_dataset()"`.

## Setup

Requirements: Python 3.10 or newer (the packages declare `>=3.10`; developed and tested on 3.12, which is also what the Space config uses). Pinned versions are in `requirements.txt`:

| Package | Version |
|---|---|
| llama-index-core | 0.14.25 |
| llama-index-embeddings-cohere | 0.9.0 |
| llama-index-llms-cohere | 0.9.0 |
| gradio | 6.29.0 |
| python-dotenv | 1.2.4 |

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root (it is git-ignored) with your key. Never put keys in code.

```
COHERE_API_KEY=your-cohere-key
```

Only `COHERE_API_KEY` is read. Structured questions work without it; semantic questions fail with `COHERE_API_KEY Missing`.

## Run

```powershell
python app.py
```

Gradio serves on `http://127.0.0.1:7860`. The first semantic question builds the index (embedding the three Markdown files), so it is slower; later ones reuse it. `python src/main.py` does the same but builds the index at startup and exits with a clear message if the key is missing.

Deployment to Hugging Face Spaces is described in [DEPLOY_HF.md](DEPLOY_HF.md).

## Tests

```powershell
pip install pytest
python -m pytest -q
```

The 14 tests need no API keys. They cover query validation and retry logic, context/prompt building, structured-data routing and responses, and that the modules import without keys. The live Cohere calls and the full workflow run are not covered by tests.

## Retrieval evaluation

`eval/eval_retrieval.py` runs 10 Hebrew questions from `eval/questions.json` (each with the Markdown file that should answer it) through the same index and reports hit@1 and hit@5 for the expected source file. It calls the Cohere embedding API, so it needs `COHERE_API_KEY`:

```powershell
python eval/eval_retrieval.py
```

No results are published here because the script has not been run with a key yet. Note that the corpus is only three short files, so this checks basic sanity, not retrieval quality at scale.

## Example

Structured path (runs offline). Question: `תן לי רשימה של כל ההחלטות הטכניות שהתקבלו בפרויקט` ("list all technical decisions made in the project"). Actual output:

```
החלטות:

1. הפרויקט משתמש ב-LlamaIndex, Cohere ו-Gradio
   הזרימה מבוססת LlamaIndex עם embeddings מ-Cohere, אינדקס וקטורי בזיכרון (VectorStoreIndex), והצגת התוצאות דרך Gradio.
   מקור: data/md_files/rag_guide.md
2. Agentic Coding משתמש בכלי AI שונים לפיתוח
   במסמך Agentic Coding נזכרים Cursor, Claude Code, Kiro, GitHub Copilot ו-Cody ככלים זמינים לפיתוח.
   מקור: data/md_files/agentic_coding.md
3. Gradio משמש לממשק משתמש מקומי ל-LLM
   הפרויקט מציג ממשק Gradio מקומי, והפעולה המרכזית היא launch() שמפעילה את הממשק על localhost.
   מקור: data/md_files/gradio_intro.md
```

A semantic question such as `מה זה RAG?` goes through `RAGWorkflow` and needs the Cohere key. Its answer is not shown here because it was not run for this README.

## Limitations

- The vector index lives in memory and is rebuilt on every process start (each start spends Cohere quota); there is no persistent vector database.
- The knowledge base is three short Hebrew Markdown files; there is no document upload or chunking configuration (LlamaIndex defaults are used).
- The structured dataset is tiny and mostly hand-written; the routing is keyword-based, so some questions containing words like `אילו` or `היום` take the structured path even when a semantic answer would fit better, and only Hebrew trigger words are recognised.
- The retry only prepends a short Hebrew phrase to the query; it is not a real query rewrite.
- The retry threshold (0.35) is a fixed constant and has not been tuned.
- A semantic question blocks the Workflow with a 30-second timeout; there is no streaming, conversation memory, or citation display in the UI (sources are passed to the LLM in the prompt but not shown separately).
- `command-r-08-2024` is a fixed model id; if Cohere retires it, change it in `build_runtime()`.
- The runtime cache is a module-level global, shared by all users of the process.
