import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAX_BYTES = 10 * 1024 * 1024
SKIPPED_DIRECTORIES = {
    ".git",
    ".gradle",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    "coverage",
    "target",
}
DATASET_SUFFIXES = {
    ".csv",
    ".tsv",
    ".jsonl",
    ".ndjson",
    ".parquet",
    ".feather",
    ".arrow",
    ".avro",
    ".orc",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".pkl",
    ".joblib",
    ".model",
    ".onnx",
}


def check_size(root: Path) -> list[str]:
    failures: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIPPED_DIRECTORIES for part in path.relative_to(root).parts):
            continue

        size = path.stat().st_size
        if size > MAX_BYTES:
            failures.append(
                f"{path.relative_to(root)}:{size} bytes exceeds the 10 MiB limit"
            )
        if path.suffix.lower() in DATASET_SUFFIXES:
            failures.append(
                f"{path.relative_to(root)}: dataset-like or model file is prohibited"
            )
    return failures


def main() -> int:
    failures = check_size(ROOT)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("Repository size and dataset checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
