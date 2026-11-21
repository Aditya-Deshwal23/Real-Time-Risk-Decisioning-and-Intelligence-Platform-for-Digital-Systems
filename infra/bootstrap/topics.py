import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

COMPOSE_DIR = Path(__file__).resolve().parents[1] / "compose"
ROOT = COMPOSE_DIR.parents[1]
COMPOSE_FILE = COMPOSE_DIR / "compose.yaml"
ENV_FILE = COMPOSE_DIR / ".env"
TOPICS_FILE = Path(__file__).resolve().with_name("topics.json")


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


def kafka_topics(*args: str) -> subprocess.CompletedProcess[str]:
    return compose(
        "exec",
        "-T",
        "kafka",
        "/opt/kafka/bin/kafka-topics.sh",
        "--bootstrap-server",
        "kafka:9092",
        *args,
    )


def load_topics(definitions_file: Path | None = None) -> dict[str, object]:
    source = definitions_file or TOPICS_FILE
    return json.loads(source.read_text(encoding="utf-8"))


def list_topics() -> set[str]:
    result = kafka_topics("--list")
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        raise SystemExit(result.returncode)
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def describe_topic(name: str) -> dict[str, object]:
    result = kafka_topics("--describe", "--topic", name)
    if result.returncode != 0:
        return {}
    partition_count = 0
    configs: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if line.startswith("Topic:"):
            match = re.search(r"\bPartitionCount:\s*(\d+)", line)
            if match:
                partition_count = int(match.group(1))
        if line.strip().startswith("Configs:"):
            raw = line.split("Configs:", 1)[1].strip()
            if raw:
                for item in raw.split(","):
                    if "=" in item:
                        key, value = item.strip().split("=", 1)
                        configs[key] = value
    return {"partitions": partition_count, "configs": configs}


def bootstrap(definitions_file: Path | None = None) -> int:
    definitions = load_topics(definitions_file)
    existing = list_topics()
    failures: list[str] = []

    for topic in definitions["topics"]:
        name = str(topic["name"])
        desired_partitions = int(topic["partitions"])
        desired_replication = int(topic["replication_factor"])
        if name not in existing:
            create = kafka_topics(
                "--create",
                "--topic",
                name,
                "--partitions",
                str(desired_partitions),
                "--replication-factor",
                str(desired_replication),
                "--config",
                f"cleanup.policy={topic['cleanup_policy']}",
                "--config",
                "retention.ms=" + str(topic["configs"]["retention.ms"]),
                "--config",
                "segment.ms=" + str(topic["configs"]["segment.ms"]),
                "--config",
                "min.insync.replicas=" + str(topic["configs"]["min.insync.replicas"]),
            )
            if create.returncode != 0:
                failures.append(f"{name}: create failed: {create.stderr.strip()}")
            continue

        described = describe_topic(name)
        actual_partitions = int(described.get("partitions", 0))
        if actual_partitions != desired_partitions:
            failures.append(
                f"{name}: partition drift: expected {desired_partitions}, "
                f"found {actual_partitions}"
            )

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("Kafka topics match the declarative definitions")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("bootstrap", "list"))
    parser.add_argument("--definitions", type=Path)
    args = parser.parse_args()
    if args.action == "list":
        print("\n".join(sorted(list_topics())))
        return 0
    return bootstrap(args.definitions)


if __name__ == "__main__":
    raise SystemExit(main())
