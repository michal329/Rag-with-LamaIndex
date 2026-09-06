# Gradio - ממשקי משתמש ל-LLM

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
