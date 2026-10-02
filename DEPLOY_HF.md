# Deploying to Hugging Face Spaces (free)

The repository is ready to run as a **Gradio Space**: `app.py` is the entry point, `requirements.txt` is pinned, and the Space settings live in the YAML header at the top of `README.md`.

## Steps

1. Sign in at <https://huggingface.co> and open **New → Space**.
2. **Space name:** e.g. `event-driven-rag` · **SDK:** Gradio · **Hardware:** CPU basic (free) · **Visibility:** Public.
3. Get the code into the Space, either:
   - **From GitHub (simplest):** in the new Space, choose *Files → Add file → Upload files* and upload the repository contents, or
   - **With git:**
     ```bash
     git remote add space https://huggingface.co/spaces/<your-username>/event-driven-rag
     git push space main
     ```
4. In the Space: **Settings → Variables and secrets → New secret**
   - `COHERE_API_KEY` = your Cohere key (free trial keys work).
5. The Space builds in a few minutes and is live at `https://huggingface.co/spaces/<your-username>/event-driven-rag`.

## Notes

- The vector index is built in memory on the first question (about 10–20 s), then cached.
- Without the secret the app still starts and answers `שגיאה: COHERE_API_KEY Missing`.
- A free Space sleeps after a period without traffic; the first visitor wakes it up.
- Every question uses your Cohere quota. Trial keys are rate-limited, which caps cost.
