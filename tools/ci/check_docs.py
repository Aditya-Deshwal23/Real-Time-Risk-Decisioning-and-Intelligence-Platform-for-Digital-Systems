import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

BANNED_PHRASES = (
    "production-ready",
    "PCI compliant",
    "bank-grade",
    "guarantee",
    "exactly-once",
)

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def check_markdown(root: Path) -> list[str]:
    failures: list[str] = []
    for path in sorted(root.rglob("*.md")):
        relative_path = path.relative_to(root)
        if relative_path.parts and relative_path.parts[0] == "context":
            continue
        if relative_path.parts[:2] == ("docs", "context"):
            continue

        in_fence = False
        for line_number, original in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if original.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            text = strip_inline_code(original)
            lower = text.lower()
            for phrase in BANNED_PHRASES:
                if phrase.lower() in lower:
                    failures.append(
                        f"{relative_path}:{line_number}: banned phrase {phrase!r}"
                    )

            for target in LINK_RE.findall(text):
                target = target.strip().split()[0].strip("<>")
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                target_path = target.split("#", 1)[0]
                resolved = (path.parent / target_path).resolve()
                if not resolved.exists():
                    failures.append(
                        f"{relative_path}:{line_number}: broken relative link {target}"
                    )
    return failures


def check_docs_index() -> list[str]:
    index = DOCS / "README.md"
    failures: list[str] = []
    if not index.is_file():
        return ["docs/README.md: missing documentation index"]

    text = index.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        target = target.strip().split()[0].strip("<>")
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        resolved = (index.parent / target).resolve()
        if not resolved.exists():
            failures.append(f"docs/README.md: index link does not exist: {target}")

    required = (
        DOCS / "compatibility-matrix.md",
        DOCS / "claims-ledger.md",
        DOCS / "adr" / "README.md",
        DOCS / "adr" / "ADR-TEMPLATE.md",
    )
    for path in required:
        if not path.is_file():
            failures.append(
                f"{path.relative_to(ROOT)}: required docs index file is missing"
            )

    return failures


def main() -> int:
    failures = check_docs_index() + check_markdown(DOCS)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("Documentation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
