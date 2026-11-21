# VERDICT

VERDICT is a specification-first project for a real-time risk decisioning and intelligence platform using simulated transactions and permitted public data; it never moves money. **Status: specification baseline V1.0, no implementation yet.**

## Repository layout

| Path | Responsibility |
|---|---|
| `platform/` | Spring Boot control plane and decision API |
| `stream/` | Kafka Streams feature processing |
| `simulator/` | JVM transaction and load simulator |
| `model-service/` | FastAPI model inference |
| `ml/` | Offline data preparation, training and evaluation |
| `console/` | React and TypeScript user interface |
| `libs/` | Shared JVM contracts and feature libraries |
| `contracts/` | OpenAPI, Protobuf, VPL, feature and reason-code contracts |
| `infra/` | Local Compose, bootstrap and Keycloak infrastructure |
| `tools/ci/` | Cross-platform CI checks |
| `benchmarks/` | Reproducible benchmark harness and results |
| `docs/` | Project context, ADRs, operational references and evidence |

## Documentation map

- [Documentation index](docs/README.md)
- [Project overview](docs/context/project-overview.md)
- [Architecture](docs/context/architecture.md)
- [Code standards](docs/context/code-standards.md)
- [UI context](docs/context/ui-context.md)
- [AI workflow rules](docs/context/ai-workflow-rules.md)
- [Progress tracker](docs/context/progress-tracker.md)

## Claims

No performance, accuracy, compliance or placement claim belongs in this repository without a corresponding entry in [`docs/claims-ledger.md`](docs/claims-ledger.md).
