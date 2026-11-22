# VERDICT quickstart

## Prerequisites

- Docker Engine and Docker Compose v2 or later
- Python 3.13
- Git

## Start the local infrastructure

From the repository root:

```text
infra/compose/dev.sh start
```

PowerShell:

```powershell
.\infra\compose\dev.ps1 start
```

The start command generates ignored `.env` values, starts PostgreSQL and Redis, waits for health checks, and bootstraps roles and databases. PostgreSQL listens only on `127.0.0.1:5432`; Redis listens only on `127.0.0.1:6379`.

## Check and verify

```text
infra/compose/dev.sh wait --timeout 120
infra/compose/dev.sh status
infra/compose/dev.sh verify
infra/compose/dev.sh ports
infra/compose/dev.sh logs
infra/compose/dev.sh stop
```

The verify command checks role connections and attributes, the application role's inability to create objects, Redis authentication, and loopback-only port bindings.

Kafka and MinIO are included in the same stack. The verify command produces and consumes a smoke record through the container and host listeners, rejects an undefined topic, detects a partition drift and restores it, and performs an object put/get test.

Kafka and MinIO ports are loopback-only:

```text
Kafka: 127.0.0.1:29092
MinIO API: 127.0.0.1:9000
MinIO console: 127.0.0.1:9001
```

Kafka uses combined KRaft broker/controller mode with replication factor 1. Plaintext listeners are local development convenience only. MinIO is source-built from the pinned AGPLv3 release and the access keys are generated in ignored `.env`.

## Reset

Reset is owner-only and is never run automatically:

```text
infra/compose/dev.sh reset --confirm RESET
```

Reset removes the named PostgreSQL and Redis volumes.
