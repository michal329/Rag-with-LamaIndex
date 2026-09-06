# 📋 הוראות מלאות להרצת הפרויקט

## שלב 1: הפעלת הסביבה

פתח PowerShell בתיקייה `C:\Users\User\Desktop\AI008` והרץ:

```powershell
.\.venv311\Scripts\Activate
```

אתה אמור לראות משהו כמו:
```
(.venv311) C:\Users\User\Desktop\AI008>
```

## שלב 2: יצירת קבצי דוגמה (אופציונלי)

עם הסביבה מופעלת, הרץ:

```powershell
python setup_example_data.py
```

זה יוצר 3 קבצי MD בתיקייה `data/md_files/`:
- `agentic_coding.md`
- `rag_guide.md`
- `gradio_intro.md`

## שלב 3: הגדרת המפתחות

עדכן את `src/main.py` עם המפתחות שלך:

```python
os.environ['PINECONE_API_KEY'] = 'sk-...'  # החלף עם המפתח האמיתי שלך
os.environ['COHERE_API_KEY'] = '...'       # החלף עם המפתח האמיתי שלך
```

## שלב 4: בדיקת התקנות

בדוק שכל החבילות מותקנות:

```powershell
python -m pip show llama-index
python -m pip show pinecone-client
python -m pip show cohere
python -m pip show gradio
```

כל אחד צריך להיות `OK`.

## שלב 5: הרצת האפליקציה

עם הסביבה מופעלת:

```powershell
python src/main.py
```

ממשק Gradio יפתח ב-`http://localhost:7860` בדפדפן שלך.

## 📝 הערות חשובות

1. **מפתחות Cohere ו-Pinecone**: אתה צריך להירשם ל-Cohere ו-Pinecone וליצור מפתחות API.
   - Cohere: https://cohere.com
   - Pinecone: https://pinecone.io

2. **קבצי MD**: הנח קבצי MD בתיקייה `data/md_files/` לצורך התיבה.
   - ניתן להשתמש ב-`setup_example_data.py` כדי ליצור דוגמאות.

3. **Pinecone Index**: צור index בשם `rag-md` בפיינקון לפני הרצת הקוד.

## 🐛 פתרון בעיות

### בעיה: `ModuleNotFoundError: No module named 'llama_index'`
**פתרון**: בדוק שהסביבה מופעלת:
```powershell
.\.venv311\Scripts\Activate
```

### בעיה: `Pinecone index not found`
**פתרון**: צור index בשם `rag-md` בפיינקון:
```python
from pinecone import Pinecone
pc = Pinecone(api_key='YOUR_KEY')
pc.create_index('rag-md', dimension=384)
```

### בעיה: `COHERE_API_KEY not found`
**פתרון**: עדכן את `src/main.py` עם המפתח האמיתי שלך.

## 🎯 מה קרה עכשיו?

1. ✅ יצרתי Python 3.11 venv ב-`.venv311/`
2. ✅ התקנתי את כל החבילות
3. ✅ יצרתי `src/main.py` עם הקוד המלא
4. ✅ יצרתי `setup_example_data.py` ליצירת קבצי דוגמה
5. ✅ עדכנתי את `README.md`

## 🚀 הצעדים הבאים

1. הפעל את הסביבה
2. עדכן את המפתחות ב-`src/main.py`
3. הרץ `setup_example_data.py` ליצירת דוגמה
4. הרץ `python src/main.py`
5. גש ל-Gradio interface
6. שאל שאלות!
