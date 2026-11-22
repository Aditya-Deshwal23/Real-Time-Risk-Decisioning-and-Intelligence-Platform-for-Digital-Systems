#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, required=True)
    args = parser.parse_args()
    dist = args.dist.resolve()
    index = dist / "index.html"
    failures: list[str] = []

    if not index.is_file():
        return 1

    html = index.read_text(encoding="utf-8")
    inline_script = re.search(r"<script(?![^>]*\bsrc\s*=)[^>]*>", html, re.I)
    if inline_script:
        failures.append("dist/index.html contains an inline script")

    theme_init = dist / "theme-init.js"
    if not theme_init.is_file():
        failures.append("dist/theme-init.js is missing")
    if 'src="/theme-init.js"' not in html:
        failures.append("dist/index.html does not load /theme-init.js")

    required_fonts = (
        "ibm-plex-sans-latin-400-normal.woff2",
        "ibm-plex-mono-latin-400-normal.woff2",
    )
    for font in required_fonts:
        if not (dist / "fonts" / font).is_file():
            failures.append(f"dist/fonts/{font} is missing")

    forbidden_hosts = (
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "cdn.jsdelivr.net",
        "unpkg.com",
    )
    for path in dist.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".html", ".css", ".js"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for host in forbidden_hosts:
            if host in text:
                failures.append(f"{path.relative_to(dist)} requests {host}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("Theme build assets are separate, same-origin, and non-inline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
