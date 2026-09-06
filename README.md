# 📊 AI008 - RAG with LlamaIndex

פרויקט RAG (Retrieval-Augmented Generation) המשתמש ב-LlamaIndex, Cohere, Pinecone, ו-Gradio.

## 🚀 התקנת הפרויקט

### 1. **הפעל את הסביבה הוירטואלית (Python 3.11+)**

```powershell
cd C:\Users\User\Desktop\AI008
.\.venv311\Scripts\Activate
```

אם תראי `(.venv311)` בתחילת השורה - משהו יצא טוב! ✅

### 2. **התקן את התלויות**

סביבת ה-Python 3.11 כבר מעודכנת עם כל החבילות הדרושות:
- `llama-index` (0.14.22)
- `llama-index-vector-stores-pinecone` (0.8.0)
- `llama-index-embeddings-cohere` (0.8.0)
- `pinecone-client` (6.0.0)
- `gradio` (6.14.0)

### 3. **הכן את המפתחות**

צור קובץ `.env` או עדכן את `src/main.py` עם המפתחות שלך:

```python
os.environ['PINECONE_API_KEY'] = 'YOUR_PINECONE_API_KEY'
os.environ['COHERE_API_KEY'] = 'YOUR_COHERE_API_KEY'
```

### 4. **הכן את הנתונים**

יצור תיקייה `data/md_files` והכנס בה קבצי Markdown:

```powershell
mkdir data/md_files
```

### 5. **הרץ את האפליקציה**

```powershell
python src/main.py
```

ממשק Gradio יפתח ב-`http://localhost:7860`

## 📋 מבנה הפרויקט

```
AI008/
├── .venv311/             # סביבה וירטואלית Python 3.11
├── src/
│   ├── main.py          # קוד ראשי עם Gradio UI ו-RAG
│   └── ...
├── data/
│   └── md_files/        # קבצי MD להתיבה
├── pyproject.toml       # הגדרות פרויקט
├── requirements.txt     # רשימת החבילות
└── README.md            # קובץ זה
```

## 🔧 API و Classes המשמשות

- **CohereEmbedding**: יצירת embeddings מ-Cohere
- **PineconeVectorStore**: אחסון וקטורים בפיינקון
- **VectorStoreIndex**: אינדקס וקטורי של LlamaIndex
- **Gradio Interface**: ממשק משתמש לשאילתות

## 📝 צעדי הפרויקט

1. **Loading**: טעינת קבצי MD מ-`data/md_files`
2. **Embedding**: יצירת embeddings עם Cohere
3. **Indexing**: אינדקסציה ב-Pinecone
4. **Query**: חיפוש סמנטי וצירוף תוצאות
5. **Response**: צירוף תשובה עם LLM

## ⚠️ הערות חשובות

- את צריכה למפתחות ל-Cohere ו-Pinecone
- חלק מהתלויות עדיין לא תומכות בימים אלו (cohere+tokenizers)
- אם יש בעיות, נסי להתקין קבצים בודדים בהמתנה

## 📞 תמיכה

אם יש בעיות, בדקי:
1. שה-venv מופעל: `(.venv311)` בשורה
2. שהמפתחותgit add . נשמרו בנכון
3. שקבצי MD קיימים ב-`data/md_files`
