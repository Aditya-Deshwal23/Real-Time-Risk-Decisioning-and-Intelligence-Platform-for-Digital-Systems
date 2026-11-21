import re
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
ARCHITECTURE = ROOT / "docs/context/architecture.md"
PLATFORM_PACKAGES = ROOT / "platform/src/main/java/dev/verdict/platform"


def main() -> int:
    architecture = ARCHITECTURE.read_text(encoding="utf-8")
    section = architecture.split("### Platform modules", maxsplit=1)[1].split(
        "\n```", maxsplit=1
    )[0]
    architecture_modules = set(
        re.findall(r"^\|\s*`([^`]+)`\s*\|", section, flags=re.MULTILINE)
    )
    expected_packages = architecture_modules | {"web"}
    actual_packages = {
        path.name
        for path in PLATFORM_PACKAGES.iterdir()
        if path.is_dir() and (path / "package-info.java").is_file()
    }
    if expected_packages != actual_packages:
        missing = sorted(expected_packages - actual_packages)
        unexpected = sorted(actual_packages - expected_packages)
        print(f"Missing package-info.java directories: {missing}", file=sys.stderr)
        print(
            f"Unexpected package-info.java directories: {unexpected}", file=sys.stderr
        )
        return 1

    print(f"Platform packages match architecture.md: {sorted(actual_packages)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
