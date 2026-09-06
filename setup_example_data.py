"""
setup_example_data.py
יוצר דוגמאות של קבצי MD להתיבה
"""

import os

def create_example_md_files():
    os.makedirs('data/md_files', exist_ok=True)
    
    # קובץ דוגמה 1: מטלות קודינג
    file1 = """# מטלות Agentic Coding

## מהו Agentic Coding?
Agentic Coding הוא שימוש בכלים כמו Cursor, Claude Code, Kiro וחברים כדי לפתח קוד במהירות על ידי שימוש ב-AI.

## יתרונות
1. מהירות פיתוח גבוהה
2. פחות שגיאות
3. טוב יותר לפרוטוטיפים
4. טוב יותר להבנת קוד

## כלים זמינים
- Cursor Editor
- Claude Code
- Kiro
- GitHub Copilot
- Cody
"""
    
    # קובץ דוגמה 2: RAG
    file2 = """# RAG - Retrieval-Augmented Generation

## מה זה RAG?
RAG הוא שיטה לשילוב חיפוש מידע עם יצירת תשובות בעזרת LLM.

## תכניות עבודה
1. טעינת מסמכים
2. יצירת embeddings
3. אינדקסציה בווקטור סטור
4. חיפוש סמנטי
5. צירוף תוצאות עם LLM

## שימוש ב-LlamaIndex
LlamaIndex הוא פרימוורק מעולה ל-RAG עם תמיכה בכמה וקטור סטורים.

## שימוש ב-Cohere
Cohere מספק מודלים לembedding ו-LLM.

## שימוש ב-Pinecone
Pinecone היא מסד נתונים וקטורי מנוהל בענן.
"""
    
    # קובץ דוגמה 3: Gradio
    file3 = """# Gradio - ממשקי משתמש ל-LLM

## מהו Gradio?
Gradio הוא ספרייה פייתון לבניית ממשקי משתמש לדגמים של ML ו-LLM.

## דוגמה פשוטה
```python
import gradio as gr

def greet(name):
    return f"Hello {name}!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()
```

## רכיבים זמינים
- Textbox
- Textarea
- Image
- Slider
- Dropdown
- Button
- ו-הרבה עוד

## שיטת launch()
`launch()` מפתחת הקובץ באתר מקומי על localhost בפורט 7860.
"""
    
    with open('data/md_files/agentic_coding.md', 'w', encoding='utf-8') as f:
        f.write(file1)
    
    with open('data/md_files/rag_guide.md', 'w', encoding='utf-8') as f:
        f.write(file2)
    
    with open('data/md_files/gradio_intro.md', 'w', encoding='utf-8') as f:
        f.write(file3)
    
    print("✅ יצרתי 3 קבצי MD דוגמה ב-data/md_files/")
    print("   - agentic_coding.md")
    print("   - rag_guide.md")
    print("   - gradio_intro.md")

if __name__ == "__main__":
    create_example_md_files()
