import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def check_notebooks(root: Path) -> list[str]:
    failures: list[str] = []
    allowed_notebook_root = root / "ml" / "notebooks"
    for path in sorted(root.rglob("*.ipynb")):
        if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
            continue

        relative = path.relative_to(root)
        if not path.is_relative_to(allowed_notebook_root):
            failures.append(f"{relative}: notebook is outside ml/notebooks/")
            continue

        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            failures.append(f"{relative}: invalid notebook JSON: {error}")
            continue

        for index, cell in enumerate(notebook.get("cells", [])):
            if cell.get("outputs"):
                failures.append(f"{relative}: cell {index} contains stored outputs")
            if cell.get("execution_count") is not None:
                failures.append(f"{relative}: cell {index} has execution_count")
    return failures


def main() -> int:
    failures = check_notebooks(ROOT)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("Notebook checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
