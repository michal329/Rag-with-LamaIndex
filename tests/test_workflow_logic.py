import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import (
    build_context_block,
    build_prompt,
    expand_query_for_retry,
    normalize_query,
    should_retry,
)


class DummyNode:
    def __init__(self, content: str, metadata: dict, score: float):
        self.node = SimpleNamespace(
            metadata=metadata,
            get_content=lambda: content,
        )
        self.score = score


class WorkflowLogicTests(unittest.TestCase):
    def test_normalize_query_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            normalize_query("   ")

    def test_normalize_query_rejects_short_input(self):
        with self.assertRaises(ValueError):
            normalize_query("ab")

    def test_expand_query_for_retry_adds_context_prefix(self):
        self.assertEqual(
            expand_query_for_retry("איך מתקינים את המערכת", "low_confidence"),
            "תמצית והקשר: איך מתקינים את המערכת",
        )

    def test_should_retry_returns_true_for_no_results(self):
        should_retry_now, reason = should_retry([])
        self.assertTrue(should_retry_now)
        self.assertEqual(reason, "no_results")

    def test_should_retry_returns_true_for_low_confidence(self):
        node = DummyNode("קטע טקסט", {"file_name": "test.md"}, 0.1)
        should_retry_now, reason = should_retry([node])
        self.assertTrue(should_retry_now)
        self.assertEqual(reason, "low_confidence")

    def test_build_context_block_includes_source_and_score(self):
        node = DummyNode("טקסט לדוגמה", {"file_name": "guide.md", "title": "מדריך"}, 0.87)
        block = build_context_block([node])
        self.assertIn("guide.md", block)
        self.assertIn("מדריך", block)
        self.assertIn("0.870", block)
        self.assertIn("טקסט לדוגמה", block)

    def test_build_prompt_contains_query_and_context(self):
        prompt = build_prompt("מהו Gradio?", "תוכן הקשר")
        self.assertIn("מהו Gradio?", prompt)
        self.assertIn("תוכן הקשר", prompt)


if __name__ == "__main__":
    unittest.main()
