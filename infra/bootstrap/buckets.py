import json
import subprocess
import sys
from pathlib import Path

COMPOSE_DIR = Path(__file__).resolve().parents[1] / "compose"
ROOT = COMPOSE_DIR.parents[1]
COMPOSE_FILE = COMPOSE_DIR / "compose.yaml"
ENV_FILE = COMPOSE_DIR / ".env"
BUCKETS_FILE = Path(__file__).resolve().with_name("buckets.json")


def compose(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "--env-file",
            str(ENV_FILE),
            *args,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    buckets = json.loads(BUCKETS_FILE.read_text(encoding="utf-8"))["buckets"]
    for bucket in buckets:
        result = compose(
            "run",
            "--rm",
            "--entrypoint",
            "sh",
            "object-bootstrap",
            "-c",
            f"mc mb --ignore-existing local/{bucket}",
        )
        if result.returncode != 0:
            print(
                f"Bucket bootstrap failed for {bucket}: {result.stderr.strip()}",
                file=sys.stderr,
            )
            return result.returncode
    print("MinIO buckets match the declarative definitions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
