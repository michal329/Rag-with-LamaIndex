"""Hugging Face Spaces entry point (the Gradio SDK runs this file).

The index is built lazily on the first question, so the Space starts even
before COHERE_API_KEY is configured; set it under Settings -> Secrets.
"""
from src.main import interface
from src.structured_data import load_structured_dataset

load_structured_dataset()

if __name__ == "__main__":
    interface.launch()
