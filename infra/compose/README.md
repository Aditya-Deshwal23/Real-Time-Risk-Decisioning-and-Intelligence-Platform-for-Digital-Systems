# infra/compose/

**Responsibility:** Local Docker Compose definitions for the documented development stack.

**Must never contain:** Application logic, secrets, or hand-managed production resources.

**First implementation phase:** Phase 2 — Development environment and containers.

## Local services

| Service | Host | Purpose |
|---|---|---|
| PostgreSQL | `127.0.0.1:5432` | VERDICT system of record |
| Redis | `127.0.0.1:6379` | Rebuildable feature materialization and rate limiting |

PostgreSQL databases and roles:

- `verdict` database owned by `verdict_owner`
- `verdict_owner`: migration/DDL role
- `verdict_app`: runtime DML role, not a superuser, no `BYPASSRLS`
- `verdict_worker`: outbox/cleanup role
- `keycloak` database owned by `keycloak`

Copy-safe local variables are defined in `.env.example`. The development scripts generate ignored `.env` values on first run. The Redis memory limit is `256mb` with `noeviction`; this is a Phase 2 first guess proposed for Week 3 measurement.

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
