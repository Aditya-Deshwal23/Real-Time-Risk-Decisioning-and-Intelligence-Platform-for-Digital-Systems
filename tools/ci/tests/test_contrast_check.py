import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "check_contrast",
    ROOT / "tools/ci/check_contrast.py",
)
assert SPEC and SPEC.loader
check_contrast = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_contrast)


class ContrastCheckTests(unittest.TestCase):
    def test_wcag_relative_luminance_formula(self) -> None:
        self.assertAlmostEqual(
            check_contrast.relative_luminance("#000000"),
            0.0,
            places=6,
        )
        self.assertAlmostEqual(
            check_contrast.relative_luminance("#ffffff"),
            1.0,
            places=6,
        )
        self.assertAlmostEqual(
            check_contrast.contrast_ratio("#000000", "#ffffff"),
            21.0,
            places=6,
        )

    def test_real_token_file_passes(self) -> None:
        failures = check_contrast.check_token_file(
            ROOT / "console/src/styles/tokens.css"
        )
        self.assertEqual(failures, [])

    def test_deliberately_weak_fixture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "console/src/styles/tokens.css"
            target.parent.mkdir(parents=True)
            text = (ROOT / "console/src/styles/tokens.css").read_text(encoding="utf-8")
            text = text.replace(
                ':root[data-theme="light"] {\n',
                ':root[data-theme="light"] {\n',
            )
            text = text.replace(
                "  --color-text-primary: #0f1720;",
                "  --color-text-primary: #f3f5f7;",
            )
            target.write_text(text, encoding="utf-8")
            failures = check_contrast.check_token_file(target)
            self.assertTrue(
                any(
                    "text primary" in failure and "below" in failure
                    for failure in failures
                )
            )


if __name__ == "__main__":
    unittest.main()
