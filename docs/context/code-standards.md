# VERDICT — Code Standards

**Standards version:** 1.0.0 (draft until the approval gate, then frozen with spec baseline V1.0)
**Applies to:** all code, SQL, configuration, infrastructure and tests in the repository, whether written by a person, GitHub Copilot or any other assistant.
**Companions:** `project-overview.md` (what and why), `architecture.md` (how it is built), `ui-context.md` (console design), `ai-workflow-rules.md` (how assistants work), `progress-tracker.md` (state).

## 0. How to use this file

- **Keywords.** MUST and MUST NOT block a merge. SHOULD and SHOULD NOT need a written reason in the PR when not followed. MAY is a permission.
- **Rule IDs.** `CS-U-nn` universal, `CS-J-nn` Java, `CS-P-nn` Python, `CS-T-nn` TypeScript, `CS-D-nn` data stores, `CS-X-nn` process. Cite IDs instead of paraphrasing.
- **Enforced by.** `tool` is a failing check in CI or a hook. `test` is a named automated test. `review` is a check against the PR checklist (section 9). A rule enforced only by `review` is a gap; list it in `progress-tracker.md` and close it when a tool becomes feasible.
- **Precedence.** Security and data-integrity rules and the invariants in `architecture.md` outrank style rules. If this file conflicts with `architecture.md`, `architecture.md` wins and this file is corrected in the same PR.
- **Exceptions.** Only in place, written as `VERDICT-EXCEPTION(CS-x-nn, #issue, YYYY-MM-DD): reason` where the date is an expiry. `tools/ci/check_exceptions.py` lists them and fails the build on an expired one. Rules that protect an invariant need an ADR instead.
- **Versions.** Each ecosystem pins versions in one place: `gradle/libs.versions.toml` plus dependency lockfiles (JVM), `pyproject.toml` plus `uv.lock` (Python), `package.json` plus `package-lock.json` (web). `docs/compatibility-matrix.md` records the verified combination and changes in the same PR as any version change.
- **No API from memory.** Never write an API, annotation, configuration key, package name or CLI flag for a library the repository uses without reading the installed version's documentation or source first (CS-X-01).

## 1. Universal rules

| ID | Rule | Enforced by |
|---|---|---|
| CS-U-01 | **Smallest correct change.** One logical change per pull request. No drive-by refactors, renames or reformatting outside touched lines unless the PR is that refactor | review |
| CS-U-02 | **One concept, one name.** Canonical terms: organization, project, environment, API client, API credential, subject, event, decision, decision evidence, outcome, case file, shadow score, policy set, policy version, model, model version, deployment, replay job, simulation run, approval request, audit record. `tenant` is the technical name of the organization boundary (`tenant_id` is the organization id) and appears only in code, SQL and logs. No synonyms, and no `workspace` entity (ADR-019) | review |
| CS-U-03 | **Time.** UTC everywhere, `timestamptz` in SQL, ISO 8601 with `Z` on the wire, time from an injected clock (invariant 21). Event time (when it happened at the client) and processing time (when VERDICT handled it) are separate fields whose names say which; never substitute one for the other. No naive date-times | tool (banned APIs, ruff `DTZ`), test |
| CS-U-04 | **Money.** Integer minor units plus the environment's single currency code. No floating point for money anywhere. Formatting happens only in the console | test, review |
| CS-U-05 | **Identity and tenancy.** Tenant and environment come only from a verified identity or API credential, never from a body, query, header or frontend value (invariant 1) | test (cross-tenant tests, section 6) |
| CS-U-06 | **Configuration.** Typed, validated at start-up, failing fast with a message that names the key. Own settings use the prefix `VERDICT_` (environment) or `verdict.` (JVM properties). No defaults for secrets. `.env.example` holds fake values only | test (start-up test with a missing key) |
| CS-U-07 | **Logging.** Structured JSON to stdout with the fields in `architecture.md` section 21. Never log credentials, tokens, secrets, request or response bodies at INFO, or raw subject identifiers; log the decision id instead | test (log-scrubbing test), review |
| CS-U-08 | **Errors.** No swallowed exceptions: catch only to handle, to map to a stable error code, or to rethrow with the cause. Responses never carry stack traces or internal class names. Every 5xx is logged once with the trace id | test, review |
| CS-U-09 | **Bounded everything.** Every outbound call has a timeout derived from the remaining request deadline. Retries only for idempotent operations, with capped exponential backoff and jitter. Every queue, pool, cache, batch and page size fed by external input has an explicit bound | test, review |
| CS-U-10 | **Safe under repetition.** Anything that can be retried or redelivered (HTTP with an Idempotency-Key, Kafka consumers, the outbox relay, the materializer, jobs) is idempotent by construction and has a test that delivers twice and asserts identical state | test |
| CS-U-11 | **Determinism.** Decision-path, feature and policy code takes time, randomness and identifiers from injected providers so replay reproduces results from the same inputs | tool (banned APIs), test (replay determinism) |
| CS-U-12 | **Untrusted input.** Validate at every boundary (HTTP, Kafka, files, environment, artifacts) with allow-lists and size limits before use | test, review |
| CS-U-13 | **No code from data.** No `eval`, `exec`, `Runtime.exec`, `subprocess` with a shell, reflection on external class names, or unsafe deserialization (Java serialization, `pickle`, `yaml.load`). Policies are data (VPL, invariant 7) | tool, review |
| CS-U-14 | **Cryptography.** Platform or well-known library primitives only, never a custom scheme. Constant-time comparison for secrets, a CSPRNG for tokens, credential hashing exactly as `architecture.md` specifies | test, review |
| CS-U-15 | **Dependencies.** A new dependency needs a PR section with purpose, alternatives, licence, maintenance signal and the version verified on its registry that day. GPL, AGPL, SSPL and BUSL licences need an ADR. Prefer the platform or an existing dependency | tool (dependency review), review |
| CS-U-16 | **Generated code** (Protobuf classes, OpenAPI types) is never edited by hand, carries a generated-file header, and CI regenerates it and fails on any diff | tool |
| CS-U-17 | **Comments** explain why, invariants and trade-offs, not what. No commented-out code. A TODO must read `TODO(#issue): text` | tool (regex check) |
| CS-U-18 | **Secrets** never appear in Git, images, logs or fixtures. A secret scanner runs in a pre-commit hook and in CI | tool |
| CS-U-19 | **No large or binary artefacts in Git:** no datasets, model binaries, build output or notebook outputs. Commit manifests with SHA-256 instead | tool (size check) |

## 2. Java (`platform`, `stream`, `simulator`, shared libraries)

### 2.1 Build, toolchain and static checks

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-01 | Gradle with Kotlin DSL, the committed wrapper (`./gradlew`, never a system Gradle), a version catalog at `gradle/libs.versions.toml`, and convention plugins in the included build `build-logic/`. No version literals in module build files. Dependency locking is on and lockfiles are committed | tool |
| CS-J-02 | The Java release comes from the Gradle toolchain pinned in `build-logic` and recorded in the compatibility matrix. Compile with `-Xlint:all -Werror`. No preview features. Every `@SuppressWarnings` has a reason comment | tool |
| CS-J-03 | Formatting by Spotless with google-java-format. `spotlessCheck` fails the build and formatting is never debated in review | tool |
| CS-J-04 | Null safety uses JSpecify annotations: `@NullMarked` in every `package-info.java`, `@Nullable` only where null is a legitimate value, checked by NullAway through Error Prone, with SpotBugs alongside. If Error Prone or NullAway does not support the pinned JDK at scaffold time, record that in an ADR and keep SpotBugs plus the annotation convention | tool |
| CS-J-05 | Banned APIs, signatures in `build-logic/forbidden-apis.txt` (forbidden-apis plugin) plus ArchUnit: `Instant.now()`, `System.currentTimeMillis()`, `LocalDateTime.now()` and `new Date()` outside the kernel clock adapter; `UUID.randomUUID()` outside the kernel `IdGenerator`; `Math.random()` and unseeded `new Random()`; `System.out` and `System.err`; `Throwable.printStackTrace()`; `Thread.sleep()` in main code; `ProcessBuilder` and `Runtime.exec`; Java serialization; constructing a JSON mapper outside the single configuration class | tool |
| CS-J-06 | Checkstyle (config under `build-logic/config/`): method length at most 50 lines, cyclomatic complexity at most 10, at most 7 parameters, no wildcard imports. Exceeding a limit needs a marked exception | tool |

### 2.2 Structure and module boundaries

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-07 | Root package `io.verdict` (a project namespace, not a domain claim). In `platform`, each module is `io.verdict.platform.&lt;module&gt;` where the root package holds only the published API (interfaces, command and result records, domain events) and `internal` holds everything else. `io.verdict.platform.web` is the API layer and `io.verdict.platform.kernel` the shared kernel (ids, clock, errors, tenant context). Public types in a module root have Javadoc stating nullability, thread-safety and failure modes | tool (ArchUnit), review |
| CS-J-08 | `PlatformArchitectureTest` (ArchUnit) asserts: (a) nothing outside module M touches `M.internal`; (b) module dependencies equal exactly the map in the architecture module diagram, kept in the test as data; (c) no package cycles; (d) `kernel` depends on no module; (e) `web` uses module root packages only; (f) `internal.domain` packages do not depend on Spring, JDBC, JPA or Jackson; (g) controllers never touch repositories; (h) `decision` depends on neither Kafka client classes (invariant 5) nor JPA | test |
| CS-J-09 | Dependencies point inward: web, then application services, then domain. Adapters (JDBC, Redis, HTTP clients, Kafka) implement interfaces owned by the application layer | test (ArchUnit) |
| CS-J-10 | `stream` and `simulator` use `io.verdict.stream` and `io.verdict.simulator` with the same internal convention and depend only on `libs/*`, never on `platform`. `libs/*` are framework-free JVM libraries (generated contracts, shared feature definitions) with no Spring dependency | tool (dependency rules, ArchUnit) |

### 2.3 Language usage

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-11 | Records for DTOs, commands, events and value objects, validated in compact constructors. Closed sets (decision outcomes, failure modes, VPL nodes) are sealed interfaces handled by exhaustive pattern-matching `switch` with **no `default` branch**, so adding a variant breaks compilation until handled | review, test |
| CS-J-12 | Immutable by default: `final` fields, defensive copies (`List.copyOf`), no setters on domain types, classes `final` unless designed for extension | review |
| CS-J-13 | No Lombok and no reflection-based mapping libraries. Mapping between layers is explicit code | tool (banned dependencies in `build-logic`) |
| CS-J-14 | Never return null for a collection or string. `Optional` only as a return type, never as a field or parameter | tool (Error Prone), review |
| CS-J-15 | Application and domain errors extend one kernel `VerdictException` carrying a stable `ErrorCode`. HTTP mapping happens in exactly one `@RestControllerAdvice` in `web`. `ResponseStatusException` and hand-set status codes elsewhere are banned | tool (ArchUnit) |
| CS-J-16 | `var` only when the right-hand side states the type. No wildcard imports. Static imports only for test assertions and constants | tool |
### 2.4 Concurrency and resilience

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-17 | Blocking I/O runs on virtual threads. No `synchronized` around blocking calls (use `ReentrantLock`). Business logic never reads a `ThreadLocal`; request context is passed explicitly (MDC for log fields is allowed). No `parallelStream()` on request paths | tool (ArchUnit, banned APIs), review |
| CS-J-18 | Each outbound dependency (PostgreSQL, Redis, model service) has a bounded concurrency limit, a timeout taken from the remaining deadline, and a failure policy that matches the failure matrix in `architecture.md`. One resilience library only, the one in the version catalog; a second needs an ADR | test (failure injection: slow, erroring, down) |
| CS-J-19 | Background work (outbox relay, retention, rebuilds) is safe on every instance: a single active worker via PostgreSQL advisory lock, idempotent steps, bounded batches, a lag metric | test (two instances, exactly one active) |

### 2.5 Spring Boot

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-20 | Constructor injection only. No field or setter injection. `ApplicationContext.getBean` only inside configuration. Component scanning limited to `io.verdict.platform` | tool (ArchUnit) |
| CS-J-21 | Configuration through `@ConfigurationProperties` records with `@Validated`, prefix `verdict.`. Profiles are exactly `local`, `ci`, `staging` and `production-like`; business classes never branch on the active profile | test, review |
| CS-J-22 | Transaction boundaries sit on application-service methods. The decision hot path uses programmatic transactions (`TransactionTemplate`) so the claim commit and the final commit are visible in code. **No network call (Redis, model service, HTTP, Kafka) inside an open database transaction on the decision path.** `@Transactional` never on controllers | test (stubs assert no active transaction during the call), review |
| CS-J-23 | Controllers are thin: parse, authorize, delegate, map. Request and response DTO records are separate from domain types and validated with Bean Validation. One explicit access check per handler. Each handler has allowed and denied tests for every role in the RBAC matrix of `architecture.md` | test |
| CS-J-24 | Contract first: `contracts/openapi/*.yaml` is the source of truth. CI runs an OpenAPI breaking-change check against `main` and contract tests that validate every integration-test response against the spec. A breaking change needs a new major version and an ADR (invariant 19) | tool, test |
| CS-J-25 | Management endpoints (health, metrics) listen on a separate management port that the load balancer does not route. The load balancer routes only the public paths documented in `architecture.md` | test, review |

### 2.6 Persistence

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-26 | The hot path (decision, idempotency, outbox, audit append) uses Spring JDBC (`JdbcClient`) with explicit SQL in dedicated `*Sql` classes or `.sql` resources: explicit column lists, bind parameters only, no dynamic identifiers except from allow-lists | tool (check for `SELECT *` and concatenated SQL), review |
| CS-J-27 | JPA (Hibernate) only in control-plane CRUD modules. `spring.jpa.open-in-view=false`. Entities never cross a module boundary or reach `web`. No lazy loading outside a transaction. Cascades need a test | tool (ArchUnit), review |
| CS-J-28 | Tenant-scoped tables are accessed only inside the kernel `TenantTransaction`, which runs `set_config('app.tenant_id', ?, true)` as the first statement of the transaction (invariant 2). Their repositories are package-private in `internal.persistence`. Each repository has an integration test proving cross-tenant reads return nothing, cross-tenant writes fail, and access without a scope returns nothing | test |
| CS-J-29 | Idempotency, outbox and audit-append code lives only in its owning packages. Any change there needs the concurrency suite green: parallel claims, lease takeover, stale-attempt fencing, crash between publish and mark, duplicate publish, parallel audit appends per tenant | test |

### 2.7 Messaging

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-30 | Events are Protobuf generated from `contracts/proto/`. `buf lint` and `buf breaking` run against `main`. No JSON on topics. Each event carries `event_id`, tenant, environment, schema version and trace context as `architecture.md` specifies. Consumers are idempotent on `event_id`. Poison records go to `dlq.v1` with a reason and are never dropped or retried forever | tool, test |
| CS-J-31 | Kafka Streams topologies are deterministic and use event time only. `TopologyTestDriver` tests cover late, duplicate, out-of-order and poison records plus the golden-fixture parity test. Topic and state-store names are constants. A topology change includes a state-compatibility note in the PR | test, review |
| CS-J-32 | Producers use idempotence and `acks=all`. In `platform` only the outbox relay produces to Kafka and `org.apache.kafka` is banned elsewhere there. In `stream` only the topologies and the materializer produce | tool (ArchUnit) |

### 2.8 Java tests

| ID | Rule | Enforced by |
|---|---|---|
| CS-J-33 | JUnit Jupiter and AssertJ. Testcontainers with real PostgreSQL, Kafka and Redis; no H2 and no embedded substitutes. Awaitility for asynchronous assertions. No `Thread.sleep` | tool (banned APIs, dependency rules) |
| CS-J-34 | Names follow `should_&lt;result&gt;_when_&lt;condition&gt;`. Unit tests are pure (no Spring context). Integration tests end in `IT` and run in a separate Gradle task with one shared container setup per test JVM and one `@SpringBootTest` configuration family so context caching works | tool |
| CS-J-35 | Concurrency tests use latches or barriers and bounded waits, never sleeps. The concurrency suite also runs repeatedly in a scheduled CI job to expose flakiness | test |
| CS-J-36 | JaCoCo is a signal, not a goal. Initial gate: 80 percent line coverage on `decision`, `policy`, `features`, `scoring`, `outbox`, `audit` and `kernel`, ratcheted upward only. Tests without meaningful assertions are rejected in review. Mutation testing with PIT on `policy` and `decision` is P2 | tool |

## 3. Python (`model-service`, `ml`)

Each is an independent project with its own `pyproject.toml` and `uv.lock`. They share no Python code; shared contracts come from `contracts/`.

### 3.1 Toolchain

| ID | Rule | Enforced by |
|---|---|---|
| CS-P-01 | Python 3.13 pinned in `.python-version` and `requires-python`. uv manages environments and the committed `uv.lock`. CI installs with a frozen or locked sync. Docs and scripts never use a bare `pip install` | tool |
| CS-P-02 | Ruff does linting and formatting (no black, isort or flake8). Enabled families: `E`, `F`, `I`, `B`, `BLE`, `UP`, `S`, `DTZ`, `T20`, `PT`, `SIM`, `C4`, `PERF`, `RUF`, `N`, `ANN`, `ARG`, `ERA`, `TID`, with banned imports for `pickle`, `cloudpickle`, `marshal` and `shelve`. Configuration lives in `pyproject.toml` and every ignore carries a reason | tool |
| CS-P-03 | mypy in strict mode on all library code. Only `# type: ignore[code]  # reason`, never bare. `Any` only at a validated boundary, with a comment | tool |
| CS-P-04 | `src/` layout with packages `verdict_model_service` and `verdict_ml`. Dependency groups keep the serving image minimal: the `model-service` runtime group contains no training-only libraries (MLflow, notebook tooling, plotting) | tool (image dependency check), review |

### 3.2 Language and design

| ID | Rule | Enforced by |
|---|---|---|
| CS-P-05 | Full annotations on every function. Pydantic v2 models for every I/O boundary and for configuration, with `extra="forbid"` and `frozen=True` unless a reason is recorded. Dataclasses or named tuples for internal values. No loose dicts as data contracts | tool (mypy), review |
| CS-P-06 | I/O at the edges, pure functions in the core, dependencies passed explicitly. No module-level mutable state except the artifact registry built in the lifespan handler. Randomness only from a seeded `numpy.random.Generator` that is passed in, never the global generators | review, test |
| CS-P-07 | Time-zone-aware UTC `datetime` only, from an injected clock in service code | tool (ruff `DTZ`) |
| CS-P-08 | Exceptions derive from `VerdictError` carrying a stable code. No bare `except`. No `except Exception` without a re-raise or a logged mapping. No `assert` for runtime validation | tool (ruff `BLE`, `E722`, `S101`), review |
| CS-P-09 | No `print`. JSON logs with the fields from `architecture.md` section 21. Environment variables are read only in one settings module that uses Pydantic settings | tool (ruff `T20`), review |

### 3.3 `model-service`

| ID | Rule | Enforced by |
|---|---|---|
| CS-P-10 | Scoring endpoints are plain `def` (they run in the thread pool) because inference is CPU-bound; `async def` only for non-blocking I/O. Artifacts load once in the lifespan handler. Readiness stays false until every configured artifact has loaded and its SHA-256 matches the registered hash. Liveness never depends on artifacts | test |
| CS-P-11 | A score request names the model version and the expected artifact hash. A mismatch is a hard error that the platform handles through the failure matrix, never a silent fallback to another version. Responses echo model version, artifact hash and feature schema version | test |
| CS-P-12 | Artifacts use native, non-executable formats: XGBoost native model files and, for the logistic baseline, a JSON coefficient file with its preprocessing spec. `pickle`, `cloudpickle`, `joblib.load` and `torch.load` without `weights_only=True` are banned in anything the service loads. A new format needs an ADR that defines how it is verified | tool (ruff `S301`, banned imports) |
| CS-P-13 | Request size, batch size, per-request timeout and CPU thread counts are bounded by configuration. Reason codes come only from the contract's reason-code table applied to the model's native contributions; no ad-hoc text | test |
| CS-P-14 | `model-service` has no database access, no Kafka access and no write access to platform state. It reads artifacts through a read-only storage role | review |
### 3.4 ML pipelines (`ml`)

| ID | Rule | Enforced by |
|---|---|---|
| CS-P-15 | Every pipeline is a CLI entry point (a module with a typed `main`) run through `uv run`. Notebooks live in `ml/notebooks/`, are exploratory only, are committed with outputs cleared, and no reported result depends on one | tool (notebook output check), review |
| CS-P-16 | Reproducibility: every run records seeds, dataset manifest hash, `feature_schema_version`, git SHA, library versions and configuration in a run record. A run that cannot name its inputs cannot be registered | test |
| CS-P-17 | Leakage controls (invariant 15): time-ordered splits only; preprocessing fitted on training data inside one pipeline object; point-in-time features through the canonical feature implementation. Tests with deliberately leaky fixtures prove the checks detect leakage | test |
| CS-P-18 | Evaluation lives in one module, `verdict_ml.evaluation`: metric set, assumed cost matrix, calibration and block bootstrap are implemented once and reused. Every report states its data-source label (public, synthetic or simulated; invariant 16) and never claims real-world performance | test, review |
| CS-P-19 | Offline feature code lives only in `verdict_ml.features`, passes the golden fixtures in `contracts/fixtures/`, and changing a definition needs a spec change plus a new `feature_schema_version` (invariant 10) | test (parity gate) |
| CS-P-20 | Datasets and model binaries are never committed; manifests (name, source URL, licence, SHA-256, row counts, retrieval date) are. Downloads verify hashes. Licence terms and use restrictions per dataset are recorded in `docs/data-sources.md`, and restricted datasets are never redistributed or published inside artifacts | tool (size check), review |

### 3.5 Python tests

| ID | Rule | Enforced by |
|---|---|---|
| CS-P-21 | pytest with markers `unit`, `integration` and `slow`; the default run excludes `slow`. Hypothesis for property tests of feature maths, window assembly and metrics. A fixture blocks network access in unit tests. Randomness is seeded. Fixtures are small and synthetic | tool |
| CS-P-22 | Contract tests: the service's generated schema is compared with `contracts/` in CI, and the platform client contract test runs against a real `model-service` container in integration | test |
| CS-P-23 | Coverage is a signal: initial gate 85 percent on `verdict_model_service` and 80 percent on `verdict_ml` library code, ratcheted upward only | tool |

## 4. TypeScript and React (`console`)

Stack: React 19, Vite, TypeScript, TanStack (Router, Query, Table, Virtual, Form), Tailwind v4 with design tokens, Radix primitives, ECharts, Zod, Vitest, Testing Library, MSW, Playwright, Storybook, axe. Versions come from the lockfile. Design decisions live in `ui-context.md`.

### 4.1 Toolchain

| ID | Rule | Enforced by |
|---|---|---|
| CS-T-01 | TypeScript strict mode with `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch` and `verbatimModuleSyntax`. `tsc --noEmit` is a CI gate. No `any`, no non-null assertion `!` outside tests, no `@ts-ignore`; `@ts-expect-error` only with a reason and an issue number | tool |
| CS-T-02 | Several tools are recent majors (TypeScript 6, Vite 8, Vitest 5, ESLint 9, TanStack Table 9, MSW 3, Zod 4), so remembered API shapes may be stale. At the CP-01.4 scaffold, TypeScript 6.0.3 and ESLint 9.39.5 are the newest versions satisfying the required type-aware typescript-eslint and jsx-a11y peer ranges, as verified from npm on 2026-11-21; this compatibility pin preserves both lint integrations. Before writing code against any listed tool, read the installed version's documentation or type definitions (its `package.json`, `.d.ts` files, migration guide) and cite what was read in the PR. A future version change requires compatibility evidence and an updated `docs/compatibility-matrix.md` | review (CS-X-01) |
| CS-T-03 | ESLint flat config with type-aware typescript-eslint rules, react-hooks, jsx-a11y and import restrictions that enforce section 4.2. Prettier formats. `eslint --max-warnings 0` is a CI gate | tool |
| CS-T-04 | npm only: `package-lock.json` committed, `npm ci` in CI, no yarn or pnpm files. Node pinned in `.nvmrc` and `engines` | tool |

### 4.2 Structure

| ID | Rule | Enforced by |
|---|---|---|
| CS-T-05 | Layout under `console/src/`: `app/` (providers, router, shell), `features/&lt;feature&gt;/` (one folder per product area in `ui-context.md`), `components/ui/` (primitives), `components/charts/`, `lib/` (API client, auth, formatting, time), `styles/` (tokens), `test/` (setup, MSW handlers). A feature exposes only its `index.ts`; features never import another feature's internals | tool (ESLint restricted imports) |
| CS-T-06 | One module per cross-cutting concern: a single API client in `lib/api`, a single auth module in `lib/auth`, a single formatting module on `Intl` for time, number and currency display | review |
| CS-T-07 | Function components with named exports only (no default exports except tool config files). Explicit props types. One component per file, at most 200 lines, otherwise split | tool (ESLint) |

### 4.3 Data, state and routing

| ID | Rule | Enforced by |
|---|---|---|
| CS-T-08 | Server data lives in TanStack Query only: query-key factories per feature, no fetching in `useEffect`, no copying server data into component state or global stores. Mutations invalidate by key. Mutations that change governance state (policy activation, model promotion, approvals, credential actions) are never optimistic | test, review |
| CS-T-09 | TanStack Router with typed routes. Environment, filters, sort and pagination live in the URL as Zod-validated search params, so every view is linkable and tests are deterministic | test |
| CS-T-10 | API types come from `contracts/openapi/` through generated types in `lib/api/generated`, never edited by hand and never duplicated. Zod validates URL params and form input. MSW handlers in tests are built from the same OpenAPI examples | tool (regeneration diff), review |
| CS-T-11 | Forms use the single form library named in `ui-context.md` with Zod schemas. Server errors map from the stable error `code`, never from message text | test |
| CS-T-12 | Every asynchronous view implements the loading, empty, error, stale and forbidden states defined in `ui-context.md`; no spinner-only states. Error states offer retry where safe and show the API's reference identifier when one is returned | test, review |

### 4.4 Security in the browser

| ID | Rule | Enforced by |
|---|---|---|
| CS-T-13 | Authentication is the BFF session cookie only. The SPA never sees, stores or sends tokens and keeps no auth data in `localStorage` or `sessionStorage`. Requests use `credentials: 'include'` and send the CSRF token as `X-XSRF-TOKEN`, read from the CSRF cookie. This lives in `lib/api` and nowhere else | test (unit, end to end) |
| CS-T-14 | No `dangerouslySetInnerHTML`, `eval`, `new Function`, inline `&lt;script&gt;` or inline event-handler strings, so a strict Content-Security-Policy works. All server-provided strings (subject keys, reason text, case notes) render as text. External links use `rel="noopener noreferrer"` | tool (ESLint), test |
| CS-T-15 | The console never decides authorization. It hides or disables controls from the permission set the BFF returns, for usability only; the server still enforces everything. Tenant and environment identifiers come only from the URL and the BFF session, never from constants | review, test |
| CS-T-16 | No secrets in the bundle. `VITE_` variables are public by definition and hold non-secret build settings only. CI fails when a variable name contains `SECRET`, `TOKEN`, `KEY` or `PASSWORD` | tool |

### 4.5 Design system usage

| ID | Rule | Enforced by |
|---|---|---|
| CS-T-17 | Colors, spacing, radius, type scale, elevation and motion come only from design tokens in `styles/` (Tailwind v4 theme variables). `tools/ci/check_tokens.py` fails on hex, rgb or hsl literals and on arbitrary pixel values outside `styles/` | tool |
| CS-T-18 | Primitives are Radix wrapped in `components/ui/`; product code never imports Radix directly. A new primitive needs a Storybook story covering default, hover, focus-visible, active, disabled, loading, error and empty states where they apply | tool (ESLint restricted imports), review |
| CS-T-19 | Charts go through one ECharts wrapper in `components/charts/` that applies the token theme, provides a text alternative (summary plus a data-table toggle), never encodes meaning by color alone, and caps rendered points | test, review |
| CS-T-20 | Tables use TanStack Table with virtualization above the row threshold set in `ui-context.md`. Large result sets are server-paginated with a bounded page size. Every table is keyboard navigable | test |

### 4.6 Accessibility and performance

| ID | Rule | Enforced by |
|---|---|---|
| CS-T-21 | WCAG 2.2 AA is the target (a goal, not a compliance claim). Interactive elements are native elements or Radix primitives, every control has an accessible name, focus is visible and never trapped, `prefers-reduced-motion` is honored, and color is never the only signal | tool (jsx-a11y, axe), test |
| CS-T-22 | Every route and every story passes automated axe checks in CI with no serious or critical violations, and critical flows have keyboard-only Playwright tests. Automated checks are necessary but not sufficient, so the PR template asks for a manual keyboard pass | tool, test |
| CS-T-23 | Route-level code splitting. A bundle-size budget is checked in CI (value in `ui-context.md`) and raised only with a justification in the PR. No unbounded list is rendered without virtualization. Content that loads late reserves its space to avoid layout shift | tool, review |

### 4.7 Frontend tests

| ID | Rule | Enforced by |
|---|---|---|
| CS-T-24 | Vitest with Testing Library: query by role and accessible name, assert behavior not implementation, `user-event` for interaction, MSW for the network, fake timers for time. No DOM-tree snapshot tests | review |
| CS-T-25 | Playwright end-to-end tests run against the Docker Compose stack (real platform, Keycloak and PostgreSQL) and cover every P0 workflow in `project-overview.md`. They use role-based locators, no fixed sleeps, and create their own organization and environment so they are isolated | test |
| CS-T-26 | Visual regression runs on Storybook stories in light and dark themes with Playwright screenshots. Baselines live in `console/visual-baselines/`, the only exemption from CS-U-19, each file size-capped by the size check. A baseline update needs a reviewer note explaining the visual change | test, review |
| CS-T-27 | Coverage is a signal: initial gate 80 percent statements on `lib/` and on feature logic modules, ratcheted upward only. Components are covered by stories and behavior tests rather than coverage targets | tool |
## 5. Data stores and messaging (all languages)

### 5.1 PostgreSQL

| ID | Rule | Enforced by |
|---|---|---|
| CS-D-01 | Schema changes only through Flyway migrations named `V&lt;n&gt;__&lt;description&gt;.sql`. Applied migrations are never edited (checksums enforce it). Forward-only and expand-then-contract, so the previous release keeps working (`architecture.md` section 22). A migration mixes schema and bulk data changes only when they are inseparable | tool |
| CS-D-02 | Naming: snake_case, plural table names, singular column names. Constraints `pk_&lt;table&gt;`, `fk_&lt;table&gt;_&lt;ref&gt;`, `uq_&lt;table&gt;_&lt;cols&gt;`, `ck_&lt;table&gt;_&lt;rule&gt;`; indexes `ix_&lt;table&gt;_&lt;cols&gt;`. Timestamps are `timestamptz`, business identifiers `uuid`, money `bigint` in minor units, ordering sequences (such as the outbox) identity columns, enumerations `text` with a CHECK constraint | test (migration lint test) |
| CS-D-03 | Every tenant-scoped table has `tenant_id uuid NOT NULL` with a foreign key, row-level security enabled **and forced**, and the policy defined in `architecture.md`. A catalog test reads `pg_class` (`relrowsecurity`, `relforcerowsecurity`) and `pg_policies` and fails if any table with a `tenant_id` column lacks either. A table without `tenant_id` must be on an explicit allow-list with a reason | test |
| CS-D-04 | Three database roles: migration (DDL), application (DML only, not superuser, no `BYPASSRLS`, not the table owner) and a restricted role for replay and dry-run that cannot write live decision, outbox or topic resources (invariant 13). Tests connect as each role and assert what is denied | test |
| CS-D-05 | Decisions, decision evidence and audit records are append-only: the application role has no UPDATE or DELETE grant on them and a test asserts it. Tables with defined state transitions (idempotency records, outbox events, case files) are documented as mutable in `architecture.md`. The audit hash chain has an integrity-verification test (invariant 18) | test |
| CS-D-06 | Every foreign key is indexed. A new hot-path query ships with its `EXPLAIN (ANALYZE, BUFFERS)` output in the PR or with a test asserting the intended index is used. An index with no query that needs it is rejected | review, test |
| CS-D-07 | `jsonb` only for versioned snapshots (feature snapshot, policy document) that carry a `schema_version` and are validated against a JSON Schema in code before write. Anything queried is a real column | review, test |
| CS-D-08 | Statement and lock timeouts are set per role. Pool size times instance count stays below `max_connections` minus a reserve (`architecture.md` section 23). No long transactions; batch jobs use bounded batches | test (configuration test), review |

### 5.2 Redis, Kafka and object storage

| ID | Rule | Enforced by |
|---|---|---|
| CS-D-09 | Redis holds only rebuildable materializations (invariant 12). Every write is a version-guarded Lua script stored as a versioned resource with its own test. Keys are built in exactly one class from the format in `architecture.md`, every key has a TTL matching the retention it implements, values are size-bounded, and `KEYS` is never used | test, tool (grep) |
| CS-D-10 | Topic names, partition keys and retention come from `architecture.md` and `contracts/` and are declared once per deployable. Partition-key construction is a single function with a test. Consumers process at least once and handle redelivery idempotently | test |
| CS-D-11 | Topics, buckets, queues and database roles are created by code in `infra/` (Terraform or a bootstrap script), never by hand. The local Compose stack and AWS use the same definitions where the tooling allows | review |
| CS-D-12 | Model artifacts are stored at content-addressed keys (SHA-256), never overwritten, and read by `model-service` through a read-only role (CS-P-14). Buckets block public access and enable server-side encryption | test (policy scan), review |

## 6. Required tests by change type

A change is not done until every test listed for its type exists, fails without the change, and passes with it. A PR spanning several types satisfies all of them.

| Change type | Required tests |
|---|---|
| REST endpoint (`/v1` or `/console/v1`) | Allowed and denied per role (CS-J-23); cross-tenant test (another tenant's resource is neither visible nor modifiable); validation tests for missing, malformed and oversized input; contract test against OpenAPI; idempotency test when the operation takes an Idempotency-Key; audit-record test for governance actions; OpenAPI breaking-change check |
| Database migration | Applied on a schema holding representative data; RLS catalog test (CS-D-03); role-privilege test (CS-D-04); expand-then-contract note in the PR |
| Tenant-scoped table or repository | Tenant isolation test and fail-closed test without scope (CS-J-28) |
| Decision path | Integration tests for success, replay of the same key, in-progress conflict and payload mismatch; failure-matrix tests for each touched dependency (slow, erroring, down); the stage latency metric exists; the concurrency suite when claim, idempotency or outbox code changes (CS-J-29); replay determinism test |
| Event or topic | `buf breaking` clean; producer test; consumer double-delivery test; DLQ path test; trace-context propagation test |
| Feature definition | Spec entry in `contracts/`; Java and Python implementations; golden fixtures covering late, duplicate, out-of-order and boundary events; parity gate green; `feature_schema_version` bump; freshness-status tests |
| VPL construct | Schema change and version; interpreter tests; property tests for determinism, absence of side effects and bounded evaluation; explanation-output tests; compatibility test against existing policy versions |
| Model or training change | Leakage and time-split tests (CS-P-17); evaluation report with data label, seeds and hashes; calibration check; artifact hash round trip through registration and loading; reason-code mapping test; lifecycle test when a state transition changes |
| Security-relevant change (authentication, authorization, credentials, sessions, CORS, RLS, audit) | The matching `ST-nn` test from `architecture.md` plus a negative test; a threat-model note in the PR; a test that secrets never reach logs |
| UI route | End-to-end test of the main workflow; axe check; keyboard-only test of the primary action; the five asynchronous states (CS-T-12); responsive check at the breakpoints in `ui-context.md` |
| UI component | Story with its states in light and dark; interaction test; axe story check; visual baseline |
| Infrastructure | `terraform fmt`, `validate` and `plan` output in the PR; Trivy configuration scan; a clean-destroy check; cost note updated |
| Dependency or version change | Lockfile diff; `docs/compatibility-matrix.md` updated; full CI green; release notes of every major bump read and cited |
| Documentation only | Mermaid parse check, link check and the banned-phrase check (CS-X-06) |

## 7. Process rules

| ID | Rule | Enforced by |
|---|---|---|
| CS-X-01 | **Verify before use.** Before using an API, annotation, configuration key, CLI flag, package name or version of anything the repository depends on, read the installed version's documentation, sources or type definitions and cite the file or URL in the PR. If it cannot be verified, stop and report instead of guessing | review (the PR must cite sources) |
| CS-X-02 | **Inspect before change.** Read the existing code and the six context files first, follow established patterns, and search for an existing implementation before writing a new one. Never create a parallel implementation of something that exists | review |
| CS-X-03 | **Docs ship with code.** A README per deployable (purpose, run, test, configuration table); an ADR for any decision that changes or extends the architecture (files in `docs/adr/`, new IDs from ADR-021); a runbook for every new alert; and `progress-tracker.md` updated in any PR that completes or changes a milestone | review |
| CS-X-04 | **Diagrams are Mermaid** inside Markdown and are parse-checked in CI. No ASCII art and no binary diagram images | tool |
| CS-X-05 | **Scripts for required checks are cross-platform.** Everything in `tools/ci/` is standard-library-only Python, never Bash-only, so it behaves the same on Windows, macOS, Linux and in CI | review |
| CS-X-06 | **Claims ledger** (invariant 22). Every number or capability stated in a README, document, demo script or résumé bullet has an entry in `docs/claims-ledger.md` that points at a test or a benchmark run (id, environment, date), or is marked "hypothesis, not measured". A docs check flags phrases that overstate: `production-ready`, `PCI compliant`, `bank-grade`, `guarantee`, `exactly-once` without the qualifier "effect", and any placement or regulatory claim | tool (docs check), review |
## 8. Git, CI and review

| ID | Rule | Enforced by |
|---|---|---|
| CS-X-07 | Trunk-based development. `main` is protected: pull request required, squash merge with linear history, required checks green, no force-push. Branches are named `&lt;type&gt;/&lt;scope&gt;-&lt;short-description&gt;` using the Conventional Commits types | tool (branch protection) |
| CS-X-08 | Conventional Commits: `type(scope): subject`. Scopes are the module or deployable: `decision`, `policy`, `features`, `scoring`, `governance`, `identity`, `cases`, `replay`, `simctl`, `insights`, `outbox`, `audit`, `kernel`, `stream`, `simulator`, `model-service`, `ml`, `console`, `contracts`, `infra`, `docs`, `ci`. Subject in the imperative, at most 72 characters; the body explains why; footer `Refs: #issue`; breaking changes carry `!` and a `BREAKING CHANGE:` footer | tool (`tools/ci/check_commit_messages.py`) |
| CS-X-09 | PR size is at most about 400 changed lines, excluding generated files, lockfiles, fixtures and visual baselines; a larger change needs a split plan or a stated reason. Every PR uses the template with these sections: Summary, Why, Linked issue and milestone, Spec and ADR references, Rule IDs touched, Invariants touched, Verification (exact commands and their results), Tests added, Security considerations, Docs updated, Risks and rollback | tool (template check), review |
| CS-X-10 | Disabling a test (`@Disabled`, `skip`, `xfail`, `it.skip`) or a lint rule (`eslint-disable`, `noqa`, `@SuppressWarnings`) needs an inline reason and an issue link. A CI script counts them and fails on any without both | tool |
| CS-X-11 | Never use `--no-verify`. Pre-commit hooks run the formatters, the secret scanner and the commit-message check, and CI repeats every check | tool |
| CS-X-12 | Merge only by a human, after required checks pass. Every PR is self-reviewed against section 9. P0 modules (`decision`, `outbox`, `identity`, `audit`, `policy`, `features`, `stream`) also get a Claude review pass using the review prompts in the prompt library. A reviewer checks pasted command output, never an assertion that tests pass | review |

### Required commands (identical locally and in CI)

| Ecosystem | Commands |
|---|---|
| JVM | `./gradlew spotlessCheck check`, `./gradlew integrationTest`, `./gradlew jacocoTestCoverageVerification` |
| Python (in `model-service/` and in `ml/`) | `uv sync --locked`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy src`, `uv run pytest -m "not slow"` |
| Web (in `console/`) | `npm ci`, `npm run lint`, `npm run format:check`, `npm run typecheck`, `npm run test`, `npm run build`, `npm run storybook:build`, `npm run test:e2e` |
| Contracts | `buf lint` and `buf breaking` against `main`; the OpenAPI breaking-change check; the feature parity gate |
| Repository | Secret scan; size check; `tools/ci/check_exceptions.py`; `tools/ci/check_tokens.py`; `tools/ci/check_commit_messages.py`; docs check (Mermaid parse, links, banned phrases) |
| Infrastructure | `terraform fmt -check`, `terraform validate`, `terraform plan`, Trivy |

Task and script names in this table are fixed by this file. If a tool's real subcommand or flag differs in the installed version, verify it (CS-X-01) and correct this table in the same PR.

## 9. Definition of done and PR checklist

A task is done only when every item is true.

- [ ] The scope is one milestone task with no unrelated changes (CS-U-01).
- [ ] Existing code and the relevant context files were read first (CS-X-02), and every new API, annotation, package and configuration key was verified against the installed version with its source cited (CS-X-01).
- [ ] The invariants the change touches are named in the PR, with how each is preserved.
- [ ] The tests required by section 6 exist and fail without the change.
- [ ] Every required command in section 8 ran locally, and the exact commands and results are pasted. No new warning, no disabled test, no weakened assertion and no widened timeout was used to hide a race.
- [ ] Security: inputs are validated, tenant scope is enforced, no secret is in code or logs, and the matching `ST-nn` tests are present.
- [ ] Migrations are expand-then-contract and RLS is verified (CS-D-03).
- [ ] Contracts are versioned and every breaking-change check is green.
- [ ] Metrics, logs and traces exist for any new path, and failure behavior is described.
- [ ] Documentation, ADR, runbook, claims ledger and `progress-tracker.md` are updated.
- [ ] UI changes had a manual keyboard pass and a look at both themes.
- [ ] Every `VERDICT-EXCEPTION` is listed in the PR with its issue and expiry.
- [ ] The acceptance criteria (`AC-nn`) from `project-overview.md` that the task serves are demonstrated by a test or a measurement, not by assertion.

## 10. Prohibited shortcuts and anti-patterns

| Shortcut | Why it is prohibited | Caught by |
|---|---|---|
| Skipping, deleting, disabling or weakening a failing test, assertion or lint rule to get green | Hides the defect the check exists to find | CS-X-10 script, review |
| Catching and ignoring errors, or returning a default value on failure in the decision path | Produces silent wrong decisions | review, failure-matrix tests |
| Raising timeouts, retries or sleeps to mask a race or a slow dependency | Moves the failure to production | review, concurrency suite |
| Mocking the unit under test, or replacing PostgreSQL, Kafka or Redis with fakes in integration tests | Proves nothing about real behavior | dependency rules (no H2), review |
| Hard-coding tenants, environments, credentials, URLs or magic numbers | Breaks isolation and configurability | secret scan, review |
| Trusting a client-supplied tenant, environment, role or amount | Breaks invariant 1 | cross-tenant tests |
| Duplicating logic that already exists (a second feature implementation, window rule or retry helper) | Creates drift and parity failures | review (CS-X-02), parity gate |
| Inventing APIs, packages, annotations, configuration keys or versions, or pasting remembered snippets for recent majors | Produces code that fails to compile or behaves differently | CS-X-01 citations, CI |
| Adding a dependency, framework, datastore, deployable or language without a CS-U-15 section or an ADR | Unreviewed cost and risk | dependency review, review |
| Editing generated code, applied migrations, lockfiles or golden fixtures by hand to make a check pass | Defeats the check | regeneration diff, Flyway checksums, review |
| Committing datasets, model binaries, secrets, `.env` files or notebooks with outputs | Leaks data and bloats history | secret scan, size check, notebook check |
| Floating-point money, naive date-times, inline `now()` or unseeded random calls | Wrong amounts and unreproducible replay | banned APIs, ruff |
| Logging bodies, credentials or raw subject identifiers, or returning stack traces | Data leakage | log-scrubbing test |
| A network call (Redis, model service, HTTP, Kafka) inside an open database transaction on the decision path | Holds locks and connections during slow I/O | CS-J-22 test |
| Putting LLM output in the decision path, or giving an LLM write access to decisions, policies or models | Breaks invariant 14 | ArchUnit, review |
| Reporting commands as passed without running them, or writing "should work" | Breaks trust in every report | review (pasted output required) |
| Fabricating benchmarks, test results, versions, screenshots, or compliance and placement claims | Destroys the project's credibility | claims ledger, docs check |
| Mixing cleanup or refactoring into feature PRs | Hides risk and blocks review | CS-U-01, review |

## 11. Governing this file

- Changes arrive as a PR labelled `standards`. Each new rule states its ID, its enforcement mechanism (or a tracked gap), and a migration plan if existing code violates it.
- Relaxing or removing a rule that protects an invariant needs an ADR. Other rule changes need a note in the PR and an entry in `progress-tracker.md`.
- Rules enforced only by review are tracked in `progress-tracker.md` under "Standards gaps" and re-examined at every phase gate.
- This version is frozen with spec baseline V1.0 at the approval gate. Later changes follow the change-request path defined in the spec governance section of `project-overview.md`.
