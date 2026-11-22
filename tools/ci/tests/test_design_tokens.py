import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "check_tokens",
    ROOT / "tools/ci/check_tokens.py",
)
assert SPEC and SPEC.loader
check_tokens = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_tokens)


class TokenCheckTests(unittest.TestCase):
    def copy_real_tree(self, directory: Path) -> Path:
        source = ROOT / "console/src/styles/tokens.css"
        target = directory / "console/src/styles/tokens.css"
        target.parent.mkdir(parents=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        return directory

    def test_real_tree_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_real_tree(Path(temporary))
            self.assertEqual(check_tokens.check_tree(root), [])

    def test_raw_hex_fixture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_real_tree(Path(temporary))
            fixture = root / "console/src/app/Bad.css"
            fixture.parent.mkdir(parents=True, exist_ok=True)
            fixture.write_text(".bad { color: #123456; }", encoding="utf-8")
            failures = check_tokens.check_tree(root)
            self.assertTrue(any("raw hex value" in failure for failure in failures))

    def test_off_scale_spacing_fixture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_real_tree(Path(temporary))
            fixture = root / "console/src/app/Bad.css"
            fixture.parent.mkdir(parents=True, exist_ok=True)
            fixture.write_text(".bad { padding: 7px; }", encoding="utf-8")
            failures = check_tokens.check_tree(root)
            self.assertTrue(any("off-scale spacing" in failure for failure in failures))

    def test_raw_z_index_fixture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_real_tree(Path(temporary))
            fixture = root / "console/src/app/Bad.css"
            fixture.parent.mkdir(parents=True, exist_ok=True)
            fixture.write_text(".bad { z-index: 12; }", encoding="utf-8")
            failures = check_tokens.check_tree(root)
            self.assertTrue(any("raw z-index" in failure for failure in failures))

    def test_missing_light_token_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_real_tree(Path(temporary))
            token_file = root / "console/src/styles/tokens.css"
            text = token_file.read_text(encoding="utf-8")
            text = text.replace(
                "    --color-focus-ring: #1a5fd0;",
                "    /* intentionally missing focus ring */",
            )
            token_file.write_text(text, encoding="utf-8")
            failures = check_tokens.check_token_coverage(token_file)
            self.assertTrue(
                any(
                    "missing light token --color-focus-ring" in failure
                    for failure in failures
                )
            )


if __name__ == "__main__":
    unittest.main()
