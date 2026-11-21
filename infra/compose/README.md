# infra/compose/

**Responsibility:** Local Docker Compose definitions for the documented development stack.

**Must never contain:** Application logic, secrets, or hand-managed production resources.

**First implementation phase:** Phase 2 — Development environment and containers.

## Local services

| Service | Host | Purpose |
|---|---|---|
| PostgreSQL | `127.0.0.1:5432` | VERDICT system of record |
| Redis | `127.0.0.1:6379` | Rebuildable feature materialization and rate limiting |
| Kafka | `127.0.0.1:29092` | Local event transport |
| MinIO API | `127.0.0.1:9000` | S3-compatible object storage |
| MinIO console | `127.0.0.1:9001` | Local-only object-store console |

PostgreSQL databases and roles:

- `verdict` database owned by `verdict_owner`
- `verdict_owner`: migration/DDL role
- `verdict_app`: runtime DML role, not a superuser, no `BYPASSRLS`
- `verdict_worker`: outbox/cleanup role
- `keycloak` database owned by `keycloak`

Copy-safe local variables are defined in `.env.example`. The development scripts generate ignored `.env` values on first run. The Redis memory limit is `256mb` with `noeviction`; this is a Phase 2 first guess proposed for Week 3 measurement.

Kafka runs in combined broker/controller KRaft mode with one node. Replication factor 1 and minimum in-sync replicas 1 prove local correctness, not high availability. Topic auto-creation is disabled. `kafka` is the container listener; `127.0.0.1:29092` is the host listener. Both listeners are plaintext and local-only convenience.

Topic definitions live in `infra/bootstrap/topics.json`. Only `verdict.smoke.v1` exists in CP-02.2. Existing topics are compared with declared partitions and drift fails the bootstrap without changing the topic.

MinIO is source-built from `RELEASE.2025-10-15T17-29-55Z` under GNU AGPLv3. The source-build decision is recorded because the repository's prebuilt image is no longer available on Docker Hub. The MC helper is source-built from `RELEASE.2025-08-13T08-35-41Z`.

Buckets:

- `verdict-datasets`
- `verdict-models`
- `verdict-replay-reports`
- `verdict-exports`
- `verdict-event-archive`

## Commands

Run from the repository root:

```text
infra/compose/dev.sh start
infra/compose/dev.sh status
infra/compose/dev.sh verify
infra/compose/dev.sh logs
infra/compose/dev.sh stop
```

PowerShell:

```powershell
.\infra\compose\dev.ps1 start
.\infra\compose\dev.ps1 status
.\infra\compose\dev.ps1 verify
.\infra\compose\dev.ps1 logs
.\infra\compose\dev.ps1 stop
```

Reset is owner-only and refuses without an explicit confirmation:

```text
infra/compose/dev.sh reset --confirm RESET
```
