#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOKEN_FILE = ROOT / "console/src/styles/tokens.css"

HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
VAR_RE = re.compile(r"var\((--[\w-]+)\)")


def srgb_channel(value: int) -> float:
    channel = value / 255
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def relative_luminance(color: str) -> float:
    match = HEX_RE.fullmatch(color.strip())
    if not match:
        raise ValueError(f"unsupported color value: {color}")
    hex_value = match.group(1)
    if len(hex_value) == 3:
        hex_value = "".join(character * 2 for character in hex_value)
    red, green, blue = (int(hex_value[index : index + 2], 16) for index in (0, 2, 4))
    return (
        0.2126 * srgb_channel(red)
        + 0.7152 * srgb_channel(green)
        + 0.0722 * srgb_channel(blue)
    )


def contrast_ratio(foreground: str, background: str) -> float:
    first = relative_luminance(foreground)
    second = relative_luminance(background)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def block(text: str, selector: str) -> str:
    match = re.search(
        rf"{re.escape(selector)}\s*\{{(?P<body>[^}}]*)\}}",
        text,
        re.DOTALL,
    )
    return match.group("body") if match else ""


def declarations(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", text):
        result[name] = value.strip()
    return result


def resolve(vars_by_theme: dict[str, str], name: str) -> str:
    value = vars_by_theme[name]
    reference = VAR_RE.fullmatch(value)
    if reference:
        return resolve(vars_by_theme, reference.group(1))
    return value


def theme_values(token_file: Path, theme: str) -> dict[str, str]:
    text = token_file.read_text(encoding="utf-8")
    root_vars = declarations(block(text, ":root"))
    if theme == "dark":
        return root_vars

    light_vars = dict(root_vars)
    light_vars.update(declarations(block(text, ':root[data-theme="light"]')))
    return light_vars


def check_theme(token_file: Path, theme: str) -> list[str]:
    failures: list[str] = []
    vars_by_theme = theme_values(token_file, theme)
    required = {
        "color-text-primary",
        "color-text-secondary",
        "color-text-tertiary",
        "color-link",
        "color-on-accent",
        "color-accent",
        "color-accent-hover",
        "color-accent-active",
        "color-bg-canvas",
        "color-bg-surface",
        "color-bg-raised",
        "color-bg-sunken",
        "color-bg-hover",
        "color-bg-selected",
        "color-border-strong",
        "color-focus-ring",
    }

    for name in sorted(required):
        full_name = f"--{name}"
        if full_name not in vars_by_theme:
            failures.append(f"{token_file}: missing {theme} token {full_name}")

    def check_pair(
        label: str,
        foreground: str,
        background: str,
        threshold: float,
        exempt: bool = False,
    ) -> None:
        try:
            foreground_color = resolve(vars_by_theme, foreground)
            background_color = resolve(vars_by_theme, background)
            ratio = contrast_ratio(foreground_color, background_color)
        except (KeyError, ValueError) as error:
            failures.append(f"{theme} {label}: {error}")
            return
        if exempt:
            return
        if ratio + 1e-9 < threshold:
            failures.append(
                f"{theme} {label}: ratio {ratio:.2f}:1 below {threshold:.1f}:1"
            )

    text_backgrounds = (
        "--color-bg-canvas",
        "--color-bg-surface",
        "--color-bg-raised",
        "--color-bg-sunken",
        "--color-bg-hover",
        "--color-bg-selected",
    )
    for background in text_backgrounds:
        check_pair(
            f"text primary on {background}",
            "--color-text-primary",
            background,
            4.5,
        )
        check_pair(
            f"text secondary on {background}",
            "--color-text-secondary",
            background,
            4.5,
        )
        check_pair(
            f"text tertiary on {background}",
            "--color-text-tertiary",
            background,
            4.5,
        )

    for background in (
        "--color-bg-canvas",
        "--color-bg-surface",
        "--color-bg-raised",
        "--color-bg-selected",
    ):
        check_pair(
            f"link on {background}",
            "--color-link",
            background,
            4.5,
        )

    for accent in (
        "--color-accent",
        "--color-accent-hover",
        "--color-accent-active",
    ):
        check_pair(
            f"on-accent text on {accent}",
            "--color-on-accent",
            accent,
            4.5,
        )

    statuses = (
        "approve",
        "review",
        "decline",
        "degraded",
        "info",
        "neutral",
    )
    for status in statuses:
        text_name = f"--color-status-{status}-text"
        background_name = f"--color-status-{status}-bg"
        if text_name in vars_by_theme and background_name in vars_by_theme:
            check_pair(
                f"status {status} text on own background",
                text_name,
                background_name,
                4.5,
            )
            for background in (
                "--color-bg-canvas",
                "--color-bg-surface",
                "--color-bg-raised",
            ):
                check_pair(
                    f"status {status} text on {background}",
                    text_name,
                    background,
                    4.5,
                )

    for background in (
        "--color-bg-canvas",
        "--color-bg-surface",
        "--color-bg-raised",
    ):
        check_pair(
            f"strong border on {background}",
            "--color-border-strong",
            background,
            3.0,
        )
        check_pair(
            f"focus ring on {background}",
            "--color-focus-ring",
            background,
            3.0,
        )

    check_pair(
        "accent fill on surface",
        "--color-accent",
        "--color-bg-surface",
        3.0,
    )

    for status in ("approve", "review", "decline", "degraded", "info"):
        mark_name = f"--color-status-{status}-mark"
        if mark_name not in vars_by_theme:
            continue
        exempt = theme == "light" and status in {"review", "degraded"}
        check_pair(
            f"status {status} mark on surface",
            mark_name,
            "--color-bg-surface",
            3.0,
            exempt=exempt,
        )
    return failures


def check_token_file(token_file: Path) -> list[str]:
    failures: list[str] = []
    if not token_file.is_file():
        return [f"{token_file}: missing token source"]
    text = token_file.read_text(encoding="utf-8")
    if not block(text, ":root"):
        failures.append(f"{token_file}: missing dark :root block")
    if not block(text, ':root[data-theme="light"]'):
        failures.append(f"{token_file}: missing light theme block")
    if not block(text, ":root") or not block(text, ':root[data-theme="light"]'):
        return failures
    for theme in ("dark", "light"):
        failures.extend(check_theme(token_file, theme))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    token_file = root / "console/src/styles/tokens.css"
    failures = check_token_file(token_file)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("Contrast checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
