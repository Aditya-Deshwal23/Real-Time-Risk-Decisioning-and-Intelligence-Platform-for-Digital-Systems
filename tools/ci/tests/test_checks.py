import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepositoryCheckTests(unittest.TestCase):
    def test_docs_accepts_clean_markdown_and_rejects_banned_phrase(self):
        check_docs = load_module("check_docs")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = root / "README.md"
            clean.write_text("# Test\nA safe document.\n", encoding="utf-8")
            self.assertEqual(check_docs.check_markdown(root), [])

            clean.write_text("# Test\nThis is production-ready.\n", encoding="utf-8")
            failures = check_docs.check_markdown(root)
            self.assertTrue(any("banned phrase" in failure for failure in failures))

    def test_docs_backticks_and_context_are_skipped(self):
        check_docs = load_module("check_docs")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "context").mkdir()
            sample = root / "README.md"
            sample.write_text("`bank-grade` is example text.\n", encoding="utf-8")
            self.assertEqual(check_docs.check_markdown(root), [])

    def test_docs_detects_broken_relative_link(self):
        check_docs = load_module("check_docs")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[Missing](missing.md)\n", encoding="utf-8")
            failures = check_docs.check_markdown(root)
            self.assertTrue(
                any("broken relative link" in failure for failure in failures)
            )

    def test_size_accepts_small_file_and_rejects_large_and_dataset(self):
        check_size = load_module("check_size")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("small\n", encoding="utf-8")
            self.assertEqual(check_size.check_size(root), [])

            large = root / "large.bin"
            large.write_bytes(b"x" * (check_size.MAX_BYTES + 1))
            dataset = root / "data.csv"
            dataset.write_text("x\n", encoding="utf-8")
            failures = check_size.check_size(root)
            self.assertTrue(any("10 MiB limit" in failure for failure in failures))
            self.assertTrue(any("dataset-like" in failure for failure in failures))

    def test_notebook_accepts_clean_allowed_notebook_and_rejects_outputs(self):
        check_notebooks = load_module("check_notebooks")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            allowed = root / "ml" / "notebooks"
            allowed.mkdir(parents=True)
            notebook = allowed / "clean.ipynb"
            notebook.write_text(
                json.dumps({"cells": [{"outputs": [], "execution_count": None}]}),
                encoding="utf-8",
            )
            self.assertEqual(check_notebooks.check_notebooks(root), [])

            notebook.write_text(
                json.dumps(
                    {"cells": [{"outputs": [{"text": "hello"}], "execution_count": 3}]}
                ),
                encoding="utf-8",
            )
            failures = check_notebooks.check_notebooks(root)
            self.assertTrue(any("stored outputs" in failure for failure in failures))
            self.assertTrue(any("execution_count" in failure for failure in failures))

            outside = root / "README.ipynb"
            outside.write_text(json.dumps({"cells": []}), encoding="utf-8")
            failures = check_notebooks.check_notebooks(root)
            self.assertTrue(
                any("outside ml/notebooks/" in failure for failure in failures)
            )

    def test_context_refs_accepts_identical_pointers_and_missing_ref_fails(self):
        check_context_refs = load_module("check_context_refs")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github").mkdir()
            (root / "docs" / "context").mkdir(parents=True)
            (root / "docs" / "context" / "architecture.md").write_text(
                "", encoding="utf-8"
            )
            pointer = "Read docs/context/architecture.md.\n"
            (root / "AGENTS.md").write_text(pointer, encoding="utf-8")
            (root / ".github" / "copilot-instructions.md").write_text(
                pointer, encoding="utf-8"
            )
            self.assertEqual(check_context_refs.check_context_refs(root), [])

            (root / "docs" / "context" / "architecture.md").unlink()
            failures = check_context_refs.check_context_refs(root)
            self.assertTrue(any("context path" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
