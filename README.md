# VERDICT

VERDICT is a specification-first project for a real-time risk decisioning and intelligence platform using simulated transactions and permitted public data; it never moves money. **Status: specification baseline V1.0; repository, JVM and Python toolchain skeletons are present, with no business implementation yet.**

## JVM build

The JVM projects use the committed Gradle wrapper and Java 25 toolchain. With JDK 25 installed, run `./gradlew clean build` from the repository root to build and test the platform, stream, simulator, and shared JVM libraries.

## Python workspace

The Python workspace uses uv with Python 3.13 and one committed `uv.lock`. Run `uv sync --locked` from the repository root, then use the project READMEs for lint, format, type-check, and test commands.

## Console

The React and TypeScript console toolchain is in `console/`. With the pinned Node and npm versions, run `npm ci` there, followed by `npm run lint`, `npm run format:check`, `npm run typecheck`, `npm run test`, or `npm run build`.

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
