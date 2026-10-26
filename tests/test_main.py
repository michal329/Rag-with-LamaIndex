import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class ImportTests(unittest.TestCase):
    def test_modules_import_without_api_keys(self):
        import app
        import src.main

        self.assertTrue(hasattr(src.main, "RAGWorkflow"))
        self.assertIs(app.interface, src.main.interface)

    def test_runtime_requires_cohere_key(self):
        import src.main

        saved = os.environ.pop("COHERE_API_KEY", None)
        try:
            with self.assertRaises(ValueError):
                src.main.build_runtime()
        finally:
            if saved is not None:
                os.environ["COHERE_API_KEY"] = saved


if __name__ == "__main__":
    unittest.main()
