import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTEXT_REF_RE = re.compile(r"docs/context/[A-Za-z0-9._/-]+")


def check_context_refs(root: Path) -> list[str]:
    failures: list[str] = []
    contents: list[str] = []
    pointers = (
        root / "AGENTS.md",
        root / ".github" / "copilot-instructions.md",
    )

    for pointer in pointers:
        if not pointer.is_file():
            failures.append(f"{pointer.relative_to(root)}: pointer file is missing")
            continue
        contents.append(pointer.read_text(encoding="utf-8"))

    if len(contents) == 2 and contents[0].encode() != contents[1].encode():
        failures.append("AGENTS.md and .github/copilot-instructions.md differ")

    if len(contents) == 2:
        cited = set(CONTEXT_REF_RE.findall("\n".join(contents)))
        for reference in sorted(reference.rstrip(".,:;)") for reference in cited):
            if not (root / reference).is_file():
                failures.append(
                    f"{reference}: context path cited by pointer is missing"
                )

    return failures


def main() -> int:
    failures = check_context_refs(ROOT)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("Context pointer checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
