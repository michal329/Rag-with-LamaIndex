# 📊 AI008 - Event-Driven RAG System with Structured Data Extraction

## 🎯 מטרת הפרויקט

**AI008** הוא מערכת **RAG (Retrieval-Augmented Generation)** מבוססת אירועים המשלבת שתי שיטות חיפוש:

1. **חיפוש סמנטי** עבור שאלות כלליות - חיפוש וקטורי באמצעות Cohere embeddings ו-Pinecone
2. **חיפוש מובנה** עבור שאלות ספציפיות - שליפה ישירה מנתונים מובנים (החלטות, כללים, אזהרות)

המערכת **לוקחת החלטה עצמאית** איזה סוג חיפוש להריץ בהתאם לסוג השאלה של המשתמש.

### מקור הנתונים
- קבצי Markdown ב-`data/md_files/`
- ניתוח אוטומטי של `README.md` ו-`INSTRUCTIONS_HE.md`
- חילוץ ודידוקציה של החלטות, כללים, אזהרות

---

## 🚀 התקנה והרצה

### 1️⃣ הפעלת הסביבה הוירטואלית

```powershell
cd C:\Users\User\Desktop\AI008
.\.venv311\Scripts\Activate
```

אם תראי `(.venv311)` בתחילת השורה - הכל טוב! ✅

### 2️⃣ ההתקנות

סביבת Python 3.11 כוללת כבר:
- `llama-index` - ליצירת RAG workflow
- `llama-index-embeddings-cohere` - Cohere embeddings
- `llama-index-vector-stores-pinecone` - אינדקס וקטורי
- `pinecone-client` - API ל-Pinecone
- `gradio` - ממשק משתמש
- `python-dotenv` - קריאת משתנים סביבתיים

### 3️⃣ קבלת API Keys

צור `.env` או עדכן את `src/main.py`:

```python
os.environ['COHERE_API_KEY'] = 'YOUR_COHERE_API_KEY'
os.environ['PINECONE_API_KEY'] = 'YOUR_PINECONE_API_KEY'
```

### 4️⃣ הפעלת האפליקציה

```powershell
python src/main.py
```

ממשק Gradio יפתח ב-`http://localhost:7860`

---

## 📋 מבנה הפרויקט

```
AI008/
├── src/
│   ├── main.py                    # Gradio UI + Workflow + Routing
│   ├── structured_data.py         # Extraction + Schema + Response Building
│   └── OldMain.py                 # רקע היסטורי
├── data/
│   ├── md_files/                  # קבצי Markdown להתיבה
│   │   ├── agentic_coding.md
│   │   ├── rag_guide.md
│   │   └── gradio_intro.md
│   └── structured_data.json       # Dataset מובנה (נוצר אוטומטית)
├── tests/
│   ├── test_main.py
│   ├── test_structured_data.py
│   └── test_workflow_logic.py
├── README.md                       # דוקומנטציה זו
├── workflow_flowchart.html         # תרשים זרימה של ה-Workflow
├── requirements.txt
├── pyproject.toml
└── .env                            # (יוצר ידנית עם API keys)
```

---

## 🔄 איך עובדת המערכת?

### תרימה זו של החלטות:

1. **קבלת שאילתה** מהמשתמש ב-Gradio
2. **בדיקה**: האם זו שאילתה מובנית או סמנטית?
   - אם **מובנית** (למשל: "תן רשימה של כל החלטות") → `build_structured_response`
   - אם **סמנטית** (למשל: "מה הוא RAG?") → `RAGWorkflow`
3. **שליפה** - מנתונים מובנים או מחיפוש וקטורי
4. **סינתזה** - בנייה של תשובה עם LLM (Cohere)
5. **החזרה** - הצגת התוצאה ל-Gradio

```
שאילתה → Is Structured? → ✓ Structured Data / ✗ Semantic Search → Response
```

---

## 💬 דוגמאות לשאלות

### ✅ שאילתות מובנות (Structured)

```
"תן לי רשימה של כל ההחלטות הטכניות שהתקבלו בפרויקט"
↓
התוצאה: רשימה של החלטות מ-structured_data.json

"מה ההנחיה העדכנית לגבי שימוש ב-RTL בממשק?"
↓
התוצאה: כללים מה-Rules category

"אילו דברים סומנו כ-רגישים/לא לגעת?"
↓
התוצאה: אזהרות מ-Warnings category
```

### ✅ שאילתות סמנטיות (Semantic)

```
"מה הוא RAG?"
↓
חיפוש וקטורי ב-Pinecone → Cohere עונה

"איך משתמשים ב-Gradio?"
↓
חיפוש וקטורי ב-rag_guide.md → Cohere עונה

"מה זה LlamaIndex?"
↓
חיפוש וקטורי → Cohere עונה
```

### ✅ שאילתות עם סינון זמן

```
"מה נשתנה בשבוע האחרון?"
↓
סינון פריטים ל-7 ימים אחרונים → Structured Response

"אילו כללים עדכנו היום?"
↓
סינון ל-1 יום אחרון → Structured Response
```

---

## 🛠️ API ו-Classes המרכזיים

### ב-`structured_data.py`:
- `generate_structured_dataset()` - חילוץ אוטומטי מ-Markdown
- `load_structured_dataset()` - טעינה מ-JSON
- `is_structured_query()` - זיהוי סוג שאילתה
- `build_structured_response()` - בנייה של תשובה מובנית
- `_filter_recent_items()` - סינון לפי `observed_at`

### ב-`main.py`:
- `RAGWorkflow` - Event-driven workflow עם LlamaIndex
- `run_rag_workflow()` - הנקודה המרכזית של הניתוב
- `gradio_interface()` - ממשק Gradio

---

## 📊 פרטי Workflow

### שלבים של RAGWorkflow:

```
StartEvent
    ↓
validate_input → InputValidatedEvent
    ↓
retrieve_context → RetrievalDoneEvent
    ↓
validate_results → (Retry/Synthesis/Stop)
    ↓
generate_answer → AnswerReadyEvent
    ↓
finish → StopEvent
```

---

## 🧪 הרצת מבחנים

```powershell
# מבחני structured_data
python -m unittest tests.test_structured_data -v

# כל המבחנים
python -m unittest discover tests -v
```

---

## 📁 נתונים מובנים - JSON Schema

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-06-07T12:00:00+02:00",
  "items": {
    "decisions": [
      {
        "id": "dec-001",
        "title": "בחירת DB",
        "summary": "נבחר Postgres...",
        "tags": ["db", "architecture"],
        "source": {
          "tool": "doc",
          "file": "README.md",
          "anchor": "#database",
          "line_range": [10, 25]
        },
        "observed_at": "2026-06-07T12:00:00+02:00"
      }
    ],
    "rules": [...],
    "warnings": [...]
  }
}
```

---

## ⚠️ הערות חשובות

1. **API Keys** - צריך למפתחות Cohere ו-Pinecone לפעולה מלאה
2. **Pinecone Index** - צריך ליצור index בשם `rag-md` ב-Pinecone
3. **MD Files** - כל קובץ ב-`data/md_files/` נטען אוטומטית
4. **Gradio Launch** - הממשק יפתח ב-`localhost:7860`

---

## 🔗 תרשים זרימה

ראה את `workflow_flowchart.html` להצגה ויזואלית של ה-workflow.

---

## 📧 צור קשר

כל שאלה או בעיה? בדוק את הלוגים של Gradio או הרץ את המבחנים כדי לאתר בעיות.

---

**🎉 AI008 - RAG System with Intelligence!**
