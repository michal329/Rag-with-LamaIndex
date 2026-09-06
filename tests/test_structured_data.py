import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.structured_data import (
    build_structured_response,
    infer_structured_category,
    is_structured_query,
    load_structured_dataset,
)


class StructuredDataTests(unittest.TestCase):
    def test_load_structured_dataset_contains_expected_sections(self):
        dataset = load_structured_dataset()

        self.assertIn("schema_version", dataset)
        self.assertIn("items", dataset)
        self.assertIn("decisions", dataset["items"])
        self.assertIn("rules", dataset["items"])
        self.assertIn("warnings", dataset["items"])
        self.assertGreater(len(dataset["items"]["decisions"]), 0)

    def test_router_detects_structured_queries(self):
        self.assertTrue(is_structured_query("תן לי רשימה של כל ההחלטות הטכניות שהתקבלו בפרויקט"))
        self.assertTrue(is_structured_query("מה ההנחיה העדכנית לגבי שימוש ב-RTL בממשק"))

    def test_infer_structured_category_for_rules(self):
        self.assertEqual(
            infer_structured_category("מה ההנחיה העדכנית לגבי שימוש ב-RTL בממשק"),
            "rules",
        )

    def test_build_structured_response_lists_decisions(self):
        response = build_structured_response("תן לי רשימה של כל ההחלטות הטכניות שהתקבלו בפרויקט")

        self.assertIn("החלטות", response)
        self.assertIn("LlamaIndex", response)
        self.assertIn("Cohere", response)


if __name__ == "__main__":
    unittest.main()
