#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOKEN_FILE = ROOT / "console/src/styles/tokens.css"

SEMANTIC_TOKENS = {
    "--color-bg-canvas",
    "--color-bg-surface",
    "--color-bg-raised",
    "--color-bg-sunken",
    "--color-bg-hover",
    "--color-bg-selected",
    "--color-border-subtle",
    "--color-border-default",
    "--color-border-strong",
    "--color-text-primary",
    "--color-text-secondary",
    "--color-text-tertiary",
    "--color-text-disabled",
    "--color-link",
    "--color-accent",
    "--color-accent-hover",
    "--color-accent-active",
    "--color-on-accent",
    "--color-accent-subtle",
    "--color-focus-ring",
    "--color-status-approve-mark",
    "--color-status-approve-text",
    "--color-status-approve-bg",
    "--color-status-review-mark",
    "--color-status-review-text",
    "--color-status-review-bg",
    "--color-status-decline-mark",
    "--color-status-decline-text",
    "--color-status-decline-bg",
    "--color-status-degraded-mark",
    "--color-status-degraded-text",
    "--color-status-degraded-bg",
    "--color-status-info-mark",
    "--color-status-info-text",
    "--color-status-info-bg",
    "--color-status-neutral-mark",
    "--color-status-neutral-text",
    "--color-status-neutral-bg",
}

SPACING_SCALE = {2, 4, 8, 12, 16, 24, 32, 48, 64}
RADIUS_SCALE = {2, 4, 6, 8, 9999}
Z_INDEX_SCALE = {10, 40, 50, 60, 70, 80}

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_RE = re.compile(r"(?<![-\w])([+-]?[\d.]+)px")


def declarations(text: str) -> set[str]:
    return set(re.findall(r"(--[\w-]+)\s*:", text))


def block(text: str, selector: str) -> str:
    match = re.search(
        rf"{re.escape(selector)}\s*\{{(?P<body>[^}}]*)\}}",
        text,
        re.DOTALL,
    )
    return match.group("body") if match else ""


def check_token_coverage(token_file: Path) -> list[str]:
    failures: list[str] = []
    if not token_file.is_file():
        return [f"{token_file}: missing token source"]

    text = token_file.read_text(encoding="utf-8")
    root_declarations = declarations(block(text, ":root"))
    light_declarations = declarations(block(text, ':root[data-theme="light"]'))

    for name in sorted(SEMANTIC_TOKENS):
        if name not in root_declarations:
            failures.append(f"{token_file}: missing dark token {name}")
        if name not in light_declarations:
            failures.append(f"{token_file}: missing light token {name}")
    return failures


def check_tree(root: Path) -> list[str]:
    failures: list[str] = []
    token_file = root / "console/src/styles/tokens.css"
    failures.extend(check_token_coverage(token_file))

    source_roots = [
        root / "console/src",
        root / "console/public",
    ]
    for source_root in source_roots:
        if not source_root.is_dir():
            continue
        for path in sorted(source_root.rglob("*")):
            if not path.is_file() or path in {
                token_file,
                root / "console/public/theme-init.js",
            }:
                continue
            if path.suffix not in {".css", ".tsx", ".ts"}:
                continue
            text = path.read_text(encoding="utf-8")
            for match in HEX_RE.finditer(text):
                failures.append(
                    f"{path.relative_to(root)}:{text.count(chr(10), 0, match.start()) + 1}: "
                    f"raw hex value {match.group(0)}"
                )

            for match in re.finditer(
                r"(?:padding|margin|gap|(?:row|column)-gap)\s*:\s*([^;]+)",
                text,
                re.IGNORECASE,
            ):
                value = match.group(1)
                if "var(" not in value:
                    for px in PX_RE.findall(value):
                        number = float(px)
                        if number.is_integer() and int(number) not in SPACING_SCALE:
                            failures.append(
                                f"{path.relative_to(root)}: off-scale spacing {px}px"
                            )

            for match in re.finditer(
                r"(?:border-radius|radius)\s*:\s*([^;]+)",
                text,
                re.IGNORECASE,
            ):
                value = match.group(1)
                if "var(" not in value:
                    for px in PX_RE.findall(value):
                        number = float(px)
                        if number.is_integer() and int(number) not in RADIUS_SCALE:
                            failures.append(
                                f"{path.relative_to(root)}: off-scale radius {px}px"
                            )

            for match in re.finditer(
                r"z-index\s*:\s*(-?\d+)",
                text,
                re.IGNORECASE,
            ):
                z_index = int(match.group(1))
                if z_index not in Z_INDEX_SCALE:
                    failures.append(f"{path.relative_to(root)}: raw z-index {z_index}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    failures = check_tree(args.root.resolve())
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("Token coverage and raw-value checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
