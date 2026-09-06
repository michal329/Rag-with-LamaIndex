# 🔧 תיעוד טכני - RAG with LlamaIndex

## סטאק טכנולוגי

### Python 3.11
- **סיבה**: גרסות חדשות של llama-index דורשות Python 3.10+
- **מיקום**: `C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe`
- **venv**: `.venv311/`

### LlamaIndex (v0.14.22)
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
```

**ההבדל מ-v0.11**:
- מחלקות הוזזו ל-`llama_index.core`
- Embeddings ב-`llama_index.embeddings.*`
- Vector stores ב-`llama_index.vector_stores.*`

### Cohere (v0.8.0)
- **מטרה**: Embeddings (המרה של טקסט לוקטורים)
- **מודל**: `embed-english-v3.0`
- **דוגמה**:
  ```python
  from llama_index.embeddings.cohere import CohereEmbedding
  embed_model = CohereEmbedding(model_name="embed-english-v3.0")
  ```

### Pinecone (v6.0.0)
- **מטרה**: אחסון וקטורים בענן
- **דוגמה**:
  ```python
  from pinecone import Pinecone
  pc = Pinecone(api_key='YOUR_KEY')
  index = pc.Index("rag-md")
  ```

### Gradio (v6.14.0)
- **מטרה**: ממשק משתמש ווב
- **דוגמה**:
  ```python
  import gradio as gr
  iface = gr.Interface(fn=query_func, inputs="text", outputs="text")
  iface.launch()
  ```

## זרימת ה-RAG

```
┌─────────────────┐
│   קבצי MD       │
│  data/md_files/ │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SimpleDirectory │
│   Reader        │  ← טוען קבצים וממיר לـ documents
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   CohereEmbed   │
│  model          │  ← יוצר embeddings (וקטורים)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PineconeVector │
│  Store          │  ← שומר וקטורים בpinecone
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ VectorStoreIndex│  ← מהווה אינדקס לחיפוש
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Query Engine  │  ← חוקר ומחזיר תוצאות
└─────────────────┘
```

## מפתח של API Calls

### 1. טעינת מסמכים
```python
from llama_index.core import SimpleDirectoryReader
loader = SimpleDirectoryReader('data/md_files', recursive=True)
documents = loader.load_data()
```

### 2. יצירת Embeddings
```python
from llama_index.embeddings.cohere import CohereEmbedding
embed_model = CohereEmbedding(
    model_name="embed-english-v3.0",
    api_key=os.environ.get('COHERE_API_KEY')
)
```

### 3. אחסון בפיינקון
```python
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
pinecone_index = pc.Index("rag-md")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
```

### 4. אינדקסציה
```python
from llama_index.core import VectorStoreIndex, ServiceContext
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store,
    service_context=service_context
)
```

### 5. שאילתה
```python
query_engine = index.as_query_engine()
response = query_engine.query("מה זה Agentic Coding?")
```

## מבנה קבצים

```
AI008/
├── .venv311/
│   ├── Lib/site-packages/
│   │   ├── llama_index/
│   │   ├── cohere/
│   │   ├── pinecone/
│   │   └── gradio/
│   └── Scripts/
│       └── python.exe
│
├── src/
│   └── main.py           # הקוד הראשי
│
├── data/
│   └── md_files/         # קבצי MD להתיבה
│
├── setup_example_data.py  # יוצר קבצי דוגמה
├── README.md             # תיעוד בחינם
├── INSTRUCTIONS_HE.md    # הוראות בעברית
├── TECHNICAL_DOCS.md     # קובץ זה
├── pyproject.toml        # הגדרות פרויקט
└── requirements.txt      # רשימת חבילות
```

## בעיות וידועות

### בעיה 1: `llama-index-embeddings-cohere` לא מותקן בPython 3.8
**סיבה**: תלות `cohere` דורשת `tokenizers` שתלויה ב`puccinialin` שלא קיים ב-PyPI לPython 3.8.

**פתרון**: Python 3.11+ כן מותקן!

### בעיה 2: CohereEmbeddings לא נמצא
**סיבה**: ייבוא שגוי של מודול.

**פתרון**:
```python
from llama_index.embeddings.cohere import CohereEmbedding  # ✅ נכון
# לא:
from llama_index.embeddings import CohereEmbedding  # ❌ שגוי
```

### בעיה 3: PineconeVectorStore לא נמצא
**סיבה**: ייבוא שגוי או גרסה לא תוסלת.

**פתרון**:
```python
from llama_index.vector_stores.pinecone import PineconeVectorStore  # ✅ נכון
```

## טיפסים

### Document
```python
class Document:
    doc_id: str
    text: str
    metadata: Dict[str, Any]
```

### Embedding
```python
List[float]  # וקטור של מספרים, בדרך כלל 384 או 1536 מימדים
```

### VectorStoreIndex
```python
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(docs, vector_store=vs)
```

## נקודות חשובות

1. **מפתחות API**: שמור בסביבה או בקובץ `.env`
2. **Pinecone Index**: חייב להיות קיים לפני הרצה
3. **MD Files**: הנח בתיקייה `data/md_files/`
4. **Python 3.11**: חובה למטלה זו
5. **Gradio Port**: ברירת מחדל `7860`

## מידע נוסף

- [LlamaIndex Docs](https://llamaindex.readthedocs.io/)
- [Cohere API](https://cohere.com/docs)
- [Pinecone Docs](https://docs.pinecone.io/)
- [Gradio Docs](https://gradio.app/docs/)
