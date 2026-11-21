# platform/

**Responsibility:** Spring Boot modular monolith for the control plane and decision API.

**Must never contain:** Kafka Streams topologies, model training, or code owned by another deployable.

**First implementation phase:** Phase 4 — Authentication, authorization and tenancy.

## Package boundaries

Platform packages follow `dev.verdict.platform`, as defined by [`architecture.md`](../docs/context/architecture.md). The root package contains the application entry point and published platform API.

| Package | Responsibility |
|---|---|
| `shared` | Shared identifiers, injected clock, error model, and tenant context |
| `web` | HTTP API adapters and security filters |
| `identity` | Organizations, users, memberships, projects, environments, credentials, sessions, and RBAC |
| `decision` | Request orchestration, decision evidence, and idempotency |
| `policy` | Policy versioning, VPL parsing, validation, and evaluation |
| `features` | Feature catalog, online-store reads, and freshness evaluation |
| `scoring` | Model-service client, circuit breaker, fallback, and shadow scoring |
| `governance` | Models, deployments, evaluations, and approval requests |
| `cases` | Cases, case events, and outcomes |
| `replay` | Replay jobs and results |
| `simulation` | Simulation runs and simulator worker control |
| `audit` | Append-only, hash-chained audit records |
| `outbox` | Outbox events and the single-active relay |
| `insights` | Read models for overview and exploration |

Modules interact only through their published interfaces and events, following the dependency map in [`architecture.md`](../docs/context/architecture.md). `shared` depends on no module; `web` uses module root APIs rather than internal packages. The platform may depend on `libs/contracts` and `libs/features`; `stream` and `simulator` must never depend on the platform.
