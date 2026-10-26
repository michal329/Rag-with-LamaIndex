"""Retrieval hit-rate evaluation over data/md_files.

Builds the same in-memory index as src/main.py (Cohere embed-multilingual-v3.0)
and checks whether the expected source file is among the top-k retrieved nodes.
Needs COHERE_API_KEY (from the environment or .env); it makes real embedding calls.

Usage: python eval/eval_retrieval.py [--top-k 5]
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)  # prepare_documents() reads the relative path data/md_files

from dotenv import load_dotenv

load_dotenv()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    if not os.environ.get("COHERE_API_KEY"):
        print("COHERE_API_KEY is not set; evaluation not run.")
        return 2

    from src.main import get_runtime_cache

    index = get_runtime_cache()["index"]
    questions = json.loads((ROOT / "eval" / "questions.json").read_text(encoding="utf-8"))
    retriever = index.as_retriever(similarity_top_k=args.top_k)

    hits_at_1 = hits_at_k = 0
    for item in questions:
        nodes = retriever.retrieve(item["question"])
        files = [(n.node.metadata or {}).get("file_name") for n in nodes]
        top1 = bool(files) and files[0] == item["expected_file"]
        topk = item["expected_file"] in files
        hits_at_1 += top1
        hits_at_k += topk
        print(f"[{'HIT ' if top1 else 'MISS'}] {item['question']} -> expected {item['expected_file']}, got {files}")

    total = len(questions)
    print(f"\nhit@1: {hits_at_1}/{total} = {hits_at_1 / total:.0%}")
    print(f"hit@{args.top_k}: {hits_at_k}/{total} = {hits_at_k / total:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
