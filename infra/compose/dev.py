import argparse
import json
import secrets
import subprocess
import sys
import time
from pathlib import Path

COMPOSE_DIR = Path(__file__).resolve().parent
REPO_ROOT = COMPOSE_DIR.parents[1]
COMPOSE_FILE = COMPOSE_DIR / "compose.yaml"
ENV_FILE = COMPOSE_DIR / ".env"
ENV_EXAMPLE = COMPOSE_DIR / ".env.example"


def compose(*args: str, capture: bool = True) -> subprocess.CompletedProcess[str]:
    command = [
        "docker",
        "compose",
        "-f",
        str(COMPOSE_FILE),
        "--env-file",
        str(ENV_FILE),
        *args,
    ]
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=capture,
        text=True,
    )


def ensure_env() -> None:
    if not ENV_FILE.exists():
        ENV_FILE.write_text(
            ENV_EXAMPLE.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    updated = apply_generated_passwords(lines)

    ENV_FILE.write_text("\n".join(updated) + "\n", encoding="utf-8")
    ENV_FILE.chmod(0o600)


def env_values() -> dict[str, str]:
    ensure_env()
    values: dict[str, str] = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value
    return values


def apply_generated_passwords(lines: list[str]) -> list[str]:
    generated_keys = (
        "POSTGRES_PASSWORD",
        "VERDICT_OWNER_PASSWORD",
        "VERDICT_APP_PASSWORD",
        "VERDICT_WORKER_PASSWORD",
        "KEYCLOAK_PASSWORD",
        "REDIS_PASSWORD",
    )
    updated: list[str] = []
    for line in lines:
        if "=" not in line or line.lstrip().startswith("#"):
            updated.append(line)
            continue
        key, value = line.split("=", 1)
        if key in generated_keys and (
            not value.strip()
            or value.strip() == "generate-on-first-run"
            or value.strip().startswith("CHANGE_ME")
        ):
            value = secrets.token_urlsafe(32)
            line = f"{key}={value}"
        updated.append(line)
    return updated


def print_failure(result: subprocess.CompletedProcess[str]) -> None:
    output = "\n".join(
        text.strip() for text in (result.stdout, result.stderr) if text and text.strip()
    )
    if output:
        print(output, file=sys.stderr)


def run_bootstrap() -> None:
    result = compose(
        "exec",
        "-T",
        "postgres",
        "/docker-entrypoint-initdb.d/00-verdict-bootstrap.sh",
    )
    if result.returncode != 0:
        print("PostgreSQL bootstrap failed", file=sys.stderr)
        print_failure(result)
        raise SystemExit(result.returncode)


def start(timeout: int) -> None:
    ensure_env()
    result = compose("up", "-d", "--wait", "--wait-timeout", str(timeout))
    if result.returncode != 0:
        print_failure(result)
        raise SystemExit(result.returncode)
    run_bootstrap()
    wait(timeout)


def stop() -> None:
    ensure_env()
    result = compose("down", "--remove-orphans")
    if result.returncode != 0:
        print_failure(result)
        raise SystemExit(result.returncode)


def parse_ps_output(output: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for line in output.splitlines():
        if not line.strip():
            continue
        try:
            rows = json.loads(line)
            if isinstance(rows, dict):
                rows = [rows]
        except json.JSONDecodeError:
            continue
        for row in rows:
            name = str(row.get("Service") or row.get("Name") or "")
            state = str(row.get("State") or "")
            health = str(row.get("Health") or "")
            if name:
                result[name] = {"state": state, "health": health}
    return result


def status() -> int:
    ensure_env()
    result = compose("ps", "--format", "json")
    if result.returncode != 0:
        print_failure(result)
        return result.returncode

    services = parse_ps_output(result.stdout)
    print(f"{'Service':<12} {'State':<12} {'Health':<12}")
    print("-" * 38)
    has_unhealthy = False
    for service in ("postgres", "redis"):
        info = services.get(service, {"state": "missing", "health": "missing"})
        state = info["state"] or "missing"
        health = info["health"] or "missing"
        print(f"{service:<12} {state:<12} {health:<12}")
        if state.lower() not in {"running", "up"} or health.lower() != "healthy":
            has_unhealthy = True
    return 1 if has_unhealthy else 0


def wait(timeout: int) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if status() == 0:
            print(f"Stack is healthy within {timeout} seconds.")
            return
        time.sleep(2)
    print(f"Stack did not become healthy within {timeout} seconds.", file=sys.stderr)
    raise SystemExit(1)


def logs(follow: bool, tail: int) -> None:
    ensure_env()
    args = ["logs", "--tail", str(tail)]
    if follow:
        args.append("-f")
    result = compose(*args, capture=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def reset(confirm: str | None) -> None:
    if confirm != "RESET":
        print("Reset refused: pass --confirm RESET.", file=sys.stderr)
        raise SystemExit(2)
    ensure_env()
    result = compose("down", "--volumes", "--remove-orphans")
    if result.returncode != 0:
        print_failure(result)
        raise SystemExit(result.returncode)
    print("Named PostgreSQL and Redis volumes removed.")


def port_check() -> int:
    ensure_env()
    failed = False
    for service, port in (("postgres", "5432"), ("redis", "6379")):
        result = compose("port", service, port)
        if result.returncode != 0:
            print(f"{service}: unavailable", file=sys.stderr)
            failed = True
            continue
        binding = result.stdout.strip()
        print(f"{service}: {binding}")
        if not binding.startswith("127.0.0.1:"):
            print(
                f"{service}: port is not bound to 127.0.0.1",
                file=sys.stderr,
            )
            failed = True
    return 1 if failed else 0


def verify() -> int:
    ensure_env()
    if status() != 0:
        print("Services are not healthy", file=sys.stderr)
        return 1

    run_bootstrap()
    run_bootstrap()

    values = env_values()
    postgres_checks = (
        (
            "PostgreSQL owner",
            "verdict_owner",
            values["VERDICT_OWNER_PASSWORD"],
            "verdict",
        ),
        (
            "PostgreSQL application",
            "verdict_app",
            values["VERDICT_APP_PASSWORD"],
            "verdict",
        ),
        (
            "PostgreSQL worker",
            "verdict_worker",
            values["VERDICT_WORKER_PASSWORD"],
            "verdict",
        ),
        (
            "Keycloak",
            "keycloak",
            values["KEYCLOAK_PASSWORD"],
            "keycloak",
        ),
    )
    failed = False
    for label, role, password, database in postgres_checks:
        result = compose(
            "exec",
            "-T",
            "postgres",
            "sh",
            "-ec",
            ('PGPASSWORD="$1" psql -h 127.0.0.1 -U "$2" -d "$3" -tAc "SELECT 1"'),
            "verify",
            password,
            role,
            database,
        )
        if result.returncode == 0:
            print(f"{label}: connection passed")
        else:
            print(f"{label}: connection failed", file=sys.stderr)
            failed = True

    role_result = compose(
        "exec",
        "-T",
        "postgres",
        "sh",
        "-ec",
        (
            'PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 '
            "-U postgres -d verdict -tAc "
            "\"SELECT rolsuper::text || ',' || rolbypassrls::text "
            "FROM pg_roles WHERE rolname = 'verdict_app'"
            '"'
        ),
    )
    attributes = role_result.stdout.strip() if role_result.returncode == 0 else ""
    if attributes != "false,false":
        print(
            f"Application role attributes invalid: {attributes}",
            file=sys.stderr,
        )
        failed = True
    else:
        print("Application role attributes: NOSUPERUSER, NOBYPASSRLS")

    hba_result = compose(
        "exec",
        "-T",
        "postgres",
        "sh",
        "-ec",
        (
            'PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 '
            "-U postgres -d postgres -tAc "
            "\"SELECT count(*) FROM pg_hba_file_rules WHERE auth_method = 'trust'\""
        ),
    )
    trust_rules = hba_result.stdout.strip() if hba_result.returncode == 0 else ""
    if trust_rules != "0":
        print(
            f"Runtime PostgreSQL trust authentication rules found: {trust_rules}",
            file=sys.stderr,
        )
        failed = True
    else:
        print("PostgreSQL runtime trust authentication: disabled")

    object_result = compose(
        "exec",
        "-T",
        "postgres",
        "sh",
        "-ec",
        (
            'PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 '
            "-U postgres -d postgres -tAc "
            '"SELECT (SELECT count(*) FROM pg_roles WHERE rolname IN '
            "('verdict_owner','verdict_app','verdict_worker','keycloak')) "
            "|| ',' || (SELECT count(*) FROM pg_database WHERE datname IN "
            "('verdict','keycloak'))\""
        ),
    )
    object_counts = (
        object_result.stdout.strip() if object_result.returncode == 0 else ""
    )
    if object_counts != "4,2":
        print(
            f"Idempotency object counts unexpected: {object_counts}",
            file=sys.stderr,
        )
        failed = True
    else:
        print("Idempotency object counts: 4 roles, 2 databases")

    create_result = compose(
        "exec",
        "-T",
        "postgres",
        "sh",
        "-ec",
        (
            'PGPASSWORD="$VERDICT_APP_PASSWORD" psql -h 127.0.0.1 '
            "-U verdict_app -d verdict -v ON_ERROR_STOP=1 "
            '-c "CREATE TABLE public.verdict_app_verify(id integer)"'
        ),
    )
    if create_result.returncode == 0:
        print(
            "Application role can create objects in public",
            file=sys.stderr,
        )
        failed = True
    else:
        print("Application role CREATE TABLE denied")

    unauthenticated = compose(
        "exec",
        "-T",
        "redis",
        "redis-cli",
        "ping",
    )
    if "PONG" in unauthenticated.stdout.upper():
        print("Redis accepted unauthenticated PING", file=sys.stderr)
        failed = True
    else:
        print("Redis unauthenticated PING rejected")

    authenticated = compose(
        "exec",
        "-T",
        "-e",
        f"REDISCLI_AUTH={values['REDIS_PASSWORD']}",
        "redis",
        "redis-cli",
        "--no-auth-warning",
        "ping",
    )
    if authenticated.returncode != 0 or "PONG" not in authenticated.stdout.upper():
        print("Redis authenticated PING failed", file=sys.stderr)
        failed = True
    else:
        print("Redis authenticated PING passed")

    if port_check() != 0:
        failed = True

    return 1 if failed else 0


def negative_health(service: str) -> int:
    ensure_env()
    stop_result = compose("stop", service)
    if stop_result.returncode != 0:
        print_failure(stop_result)
        return stop_result.returncode

    result = status()
    if result == 0:
        print(
            f"Negative health test failed: {service} remained healthy", file=sys.stderr
        )
        compose("start", service)
        return 1

    print(f"Negative health test passed: {service} is unhealthy")
    start_result = compose("start", service)
    if start_result.returncode != 0:
        print_failure(start_result)
        return start_result.returncode
    return status()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VERDICT local infrastructure")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("ensure-env")
    subcommands.add_parser("bootstrap")

    start_parser = subcommands.add_parser("start")
    start_parser.add_argument("--timeout", type=int, default=None)

    subcommands.add_parser("stop")
    subcommands.add_parser("status")

    wait_parser = subcommands.add_parser("wait")
    wait_parser.add_argument("--timeout", type=int, default=None)

    logs_parser = subcommands.add_parser("logs")
    logs_parser.add_argument("--follow", action="store_true")
    logs_parser.add_argument("--tail", type=int, default=100)

    reset_parser = subcommands.add_parser("reset")
    reset_parser.add_argument("--confirm")

    subcommands.add_parser("verify")
    subcommands.add_parser("ports")

    negative = subcommands.add_parser("negative-health")
    negative.add_argument("service", choices=("postgres", "redis"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    timeout = (
        args.timeout
        if hasattr(args, "timeout") and args.timeout
        else int(env_values().get("START_TIMEOUT", "120"))
    )

    if args.command == "ensure-env":
        ensure_env()
        return 0
    if args.command == "bootstrap":
        ensure_env()
        run_bootstrap()
        return 0
    if args.command == "start":
        start(timeout)
        return status()
    if args.command == "stop":
        stop()
        return 0
    if args.command == "status":
        return status()
    if args.command == "wait":
        wait(timeout)
        return 0
    if args.command == "logs":
        logs(args.follow, args.tail)
        return 0
    if args.command == "reset":
        reset(args.confirm)
        return 0
    if args.command == "verify":
        return verify()
    if args.command == "ports":
        return port_check()
    if args.command == "negative-health":
        return negative_health(args.service)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
