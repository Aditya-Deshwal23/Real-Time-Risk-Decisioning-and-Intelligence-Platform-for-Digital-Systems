# Documentation

**Responsibility:** Index the project specifications, decisions, operational references and evidence.

**Must never contain:** Application implementation, unverified claims, or content that contradicts the context files.

**First implementation phase:** Phase 1 — Empty repository to professional monorepo.

## Documentation set

| Path | Purpose | First phase | Status |
|---|---|---|---|
| [`context/project-overview.md`](context/project-overview.md) | Product scope and requirements | Phase 0 — Product specification and architecture lock | current |
| [`context/architecture.md`](context/architecture.md) | System architecture, contracts and decisions | Phase 0 — Product specification and architecture lock | current |
| [`context/code-standards.md`](context/code-standards.md) | Engineering standards and required checks | Phase 0 — Product specification and architecture lock | current |
| [`context/ui-context.md`](context/ui-context.md) | Console design and interaction rules | Phase 0 — Product specification and architecture lock | current |
| [`context/ai-workflow-rules.md`](context/ai-workflow-rules.md) | Assistant workflow and standing rules | Phase 0 — Product specification and architecture lock | current |
| [`context/progress-tracker.md`](context/progress-tracker.md) | Project state and phase tracker | Phase 0 — Product specification and architecture lock | current |
| [`adr/README.md`](adr/README.md) | Architecture decision record index and numbering | Phase 1 — Empty repository to professional monorepo | current |
| [`adr/ADR-TEMPLATE.md`](adr/ADR-TEMPLATE.md) | Template for new architecture decisions | Phase 1 — Empty repository to professional monorepo | current |
| [`.github/workflows/`](../.github/workflows/) | Change-aware CI workflows and aggregate status | Phase 1 — Empty repository to professional monorepo | current |
| `claims-ledger.md` | Evidence-backed public claims | Phase 1 — Empty repository to professional monorepo | draft |
| [`compatibility-matrix.md`](compatibility-matrix.md) | Registry-verified dependency and tool versions | Phase 1 — Empty repository to professional monorepo | current |
| `data-sources.md` | Dataset provenance, licence and use restrictions | Phase 9 — Python data engineering and ML pipelines | planned |
| `cost-model.md` | Infrastructure cost assumptions and evidence | Phase 20 — AWS and Terraform | planned |
| `slo.md` | Service-level indicators and hypothesis targets | Phase 18 — Observability and operations | planned |
| `runbooks/` | Operational procedures for alerts and incidents | Phase 18 — Observability and operations | planned |
| `design-reviews/<wave>.md` | UI design reviews at each design wave gate | Phase 3 — Frontend foundations and design system | planned |

## Directory index

| Directory | Responsibility |
|---|---|
| [`../platform/`](../platform/README.md) | Spring Boot control plane and decision API |
| [`../stream/`](../stream/README.md) | Kafka Streams feature processing |
| [`../simulator/`](../simulator/README.md) | JVM transaction and load simulator |
| [`../model-service/`](../model-service/README.md) | FastAPI model inference |
| [`../ml/`](../ml/README.md) | Offline data and ML pipelines |
| [`../console/`](../console/README.md) | React and TypeScript console |
| [`../libs/contracts/`](../libs/contracts/README.md) | Generated JVM contract types |
| [`../libs/features/`](../libs/features/README.md) | Shared JVM feature logic |
| [`../contracts/openapi/`](../contracts/openapi/README.md) | OpenAPI contracts |
| [`../contracts/proto/`](../contracts/proto/README.md) | Protobuf event contracts |
| [`../contracts/vpl/`](../contracts/vpl/README.md) | VPL policy contract |
| [`../contracts/features/`](../contracts/features/README.md) | Feature specifications and fixtures |
| [`../contracts/reason-codes/`](../contracts/reason-codes/README.md) | Decision reason-code definitions |
| [`../infra/compose/`](../infra/compose/README.md) | Local Compose environment |
| [`../infra/bootstrap/`](../infra/bootstrap/README.md) | Development environment bootstrap |
| [`../infra/keycloak/`](../infra/keycloak/README.md) | Keycloak configuration |
| [`../tools/ci/`](../tools/ci/README.md) | Cross-platform CI checks |
| [`../benchmarks/`](../benchmarks/README.md) | Benchmark harnesses and results |
