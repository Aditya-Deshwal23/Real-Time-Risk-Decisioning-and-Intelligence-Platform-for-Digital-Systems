import sys
from pathlib import Path


def test_running_python_matches_workspace_pin() -> None:
    root = Path(__file__).resolve().parents[1]
    pinned = (root / ".python-version").read_text(encoding="utf-8").strip()

    assert pinned == "3.13"
    assert sys.version_info[:2] == (3, 13)
