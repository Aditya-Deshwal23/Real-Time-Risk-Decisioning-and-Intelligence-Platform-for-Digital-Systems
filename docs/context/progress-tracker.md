# VERDICT — Progress Tracker

**Format version:** 1.0.0
**Last updated:** 2026-11-15, by Claude (initial draft). Owner review pending.
**Companions:** `project-overview.md`, `architecture.md`, `code-standards.md`, `ui-context.md`, `ai-workflow-rules.md`. Updates to this file are governed by AW-41 to AW-44.

## 1. How to use this file

- This file is the single record of state. The specifications live in the other five files; this file links to them and never copies a requirement (AW-35).
- The assistant updates it in the same change as every unit and may set a task to IN REVIEW. Only the owner sets DONE, after the owner review gate (AW-37).
- Task and phase statuses: NOT STARTED, IN PROGRESS, IN REVIEW, DONE, BLOCKED, DEFERRED. Test statuses: PASSED, FAILED or NOT EXECUTED (AW-31), each with a date.
- ID schemes: tasks `T-nnn`, decisions `D-nn`, blockers `B-nn`, open questions `OQ-nn`, assumptions `A-nn`, risks `R-nn`, proposed decisions `PD-n`, architecture decisions `ADR-nnn`, Copilot prompts `CP-&lt;phase&gt;.&lt;n&gt;`, Claude review prompts `RV-&lt;phase&gt;`, features `F01` to `F28`, acceptance criteria `AC-01` to `AC-24`.
- No performance, accuracy or cost number appears here unless it is in `docs/claims-ledger.md` with its measurement conditions (AW-32).
- Dates are ISO dates in the owner's calendar.

## 2. Current phase and objective

| Field | Value |
|---|---|
| Phase | 1, Repository foundation and toolchains; roadmap Week 1–2, milestone P01 |
| Status | IN PROGRESS. Repository skeleton, JVM build and Python workspace are present; CP-01.4 console skeleton is underway |
| Objective | Establish reproducible repository and ecosystem foundations before feature implementation |
| Implementation | Repository documentation, JVM and Python skeletons are present. No decisioning business implementation has started |
| Exit criteria | Complete the Phase 1 tasks T-012 through T-016 in section 7 and pass the owner review gate; each task's checks and state are recorded here |
| Schedule | Roadmap Week 1 starts on Monday 2026-11-16. The roadmap is the only place that maps phases to weeks |

## 3. Phase map

| Phase | Name | Status |
|---|---|---|
| 0 | Product specification and architecture lock | IN PROGRESS |
| 1 | Empty repository to professional monorepo | NOT STARTED |
| 2 | Development environment and containers | NOT STARTED |
| 3 | Frontend foundations and design system | NOT STARTED |
| 4 | Authentication, authorization and tenancy | NOT STARTED |
| 5 | Java domain and decision core | NOT STARTED |
| 6 | Outbox and event contracts | NOT STARTED |
| 7 | Kafka and streaming feature engine | NOT STARTED |
| 8 | Online and offline feature consistency | NOT STARTED |
| 9 | Python data engineering and ML pipelines | NOT STARTED |
| 10 | Applied machine learning | NOT STARTED |
| 11 | Model serving and reliable inference | NOT STARTED |
| 12 | Decision governance | NOT STARTED |
| 13 | Delayed outcomes and model monitoring | NOT STARTED |
| 14 | Champion / challenger governance | NOT STARTED |
| 15 | Case management and analyst workbench | NOT STARTED |
| 16 | Complete frontend product | NOT STARTED |
| 17 | Optional AI extensions | NOT STARTED |
| 18 | Observability and operations | NOT STARTED |
| 19 | CI/CD and security automation | NOT STARTED |
| 20 | AWS and Terraform | NOT STARTED |
| 21 | Integration, load and chaos testing | NOT STARTED |
| 22 | Benchmark and technical evidence | NOT STARTED |
| 23 | Final product polish | NOT STARTED |

## 4. Completed decisions

State "Accepted" means the owner decided it. "Drafted" means it is in a delivered draft and becomes accepted at the approval gate. "Proposed" means it needs the owner's confirmation.

| ID | Decision | Recorded in | State |
|---|---|---|---|
| D-01 | The flagship project is VERDICT, a real-time risk decisioning and intelligence platform for digital systems | Owner's charter | Accepted |
| D-02 | Deliverables are given in chat and not as downloadable files | Owner instruction | Accepted |
| D-03 | Roles: the owner decides and reviews, Copilot implements, Claude architects, reviews and writes the prompts | `ai-workflow-rules.md` section 0 | Drafted |
| D-04 | Architecture baseline: the `platform` modular monolith plus `stream`, `model-service`, `simulator`, `ml` and `console`; PostgreSQL, Kafka, Redis and Keycloak; AWS ECS Fargate with ephemeral Terraform stacks | `architecture.md`, ADR-001 to ADR-020 (section 25) | Drafted |
| D-05 | Invariants 1 to 22 are fixed inputs for all work | `architecture.md` section 24 | Drafted |
| D-06 | Stack: Java with Spring Boot, Python with `uv`, TypeScript with React. Rule families CS-, UX- and AW- | `code-standards.md`, `ui-context.md`, `ai-workflow-rules.md` | Drafted |
| D-07 | Root Java package `io.verdict`, Gradle Kotlin DSL, npm only for the console | `code-standards.md` sections 2 and 4 | Drafted |
| D-08 | Console direction: dark theme by default with a light theme, IBM Plex, token-only styling, WCAG 2.2 AA as a target with no conformance claim | `ui-context.md` | Drafted |
| D-09 | P0 and P1 scope is frozen at V1.0; Extended items start only in their roadmap week; changes use the change-request path | `project-overview.md` (spec governance), AW-20 | Drafted |
| D-10 | The six context files live in `docs/context/`, and `.github/copilot-instructions.md` and `AGENTS.md` point to them | AW-02, AW-section 12 | Proposed. Part H confirms it |
| D-11 | Prompt IDs are `CP-&lt;phase&gt;.&lt;n&gt;` and review prompt IDs are `RV-&lt;phase&gt;` | AW-49, AW-53 | Drafted |
| D-12 | Nothing is claimed beyond what is measured: no benchmarks, compliance claims or placement claims | Owner's charter, AW-32 | Accepted |
| D-13 | A dependency version is pinned only after a registry check at scaffold time. A version that could not be verified during research stays unpinned until then | CS-X-01, `docs/compatibility-matrix.md` (created in Phase 1) | Drafted |

## 5. Completed deliverables

| Deliverable | State | Notes |
|---|---|---|
| Part A: audit of the six starter files and verified version baselines | Delivered in chat | A version that could not be reached is marked "resolve at scaffold" |
| Feature catalogue F01 to F28 | Delivered in chat | Priorities live in `project-overview.md` |
| `project-overview.md` 1.0.0 | Draft delivered | Includes AC-01 to AC-24 and the spec governance section |
| `architecture.md` 1.0.0 | Draft delivered, six parts | Sections 1 to 26; invariants in section 24, ADRs in section 25 |
| `code-standards.md` 1.0.0 | Draft delivered, five parts | A correction note was issued for the form and icon library line |
| `ui-context.md` 1.0.0 | Draft delivered, seven parts | UX-01 to UX-56; palette contrast computed by script |
| `ai-workflow-rules.md` 1.0.0 | Draft delivered, five parts | AW-01 to AW-58; a correction note is in part 5 |
| `progress-tracker.md` 1.0.0 | Draft delivered | This file |
| Cross-file consistency review | Pending (T-001) | Findings and corrections are listed when it is delivered |
| Parts H to M | Pending | Repository structure, roadmap, prompt library, Student Pack matrix, risks and audit, approval gate |
## 6. Current tasks

| ID | Task | Who | Status |
|---|---|---|---|
| T-001 | Cross-file consistency review of the six files, with a list of corrections | Claude | IN PROGRESS |
| T-002 | Deliver Part H (repository structure) and Part I (30-week roadmap) | Claude | NOT STARTED |
| T-003 | Deliver Part J (Copilot prompt library for Phases 0 to 23, the Claude review prompts and the index) | Claude | NOT STARTED |
| T-004 | Deliver Part K (Student Pack matrix), Part L (risk register and quality audit) and Part M (approval gate) | Claude | NOT STARTED |
| T-005 | Read the six files and the corrections, and note anything wrong, unclear or missing | Owner | NOT STARTED |

## 7. Next tasks (start only after the approval gate)

| ID | Task | Phase | Prompt |
|---|---|---|---|
| T-010 | Approve spec baseline V1.0 and answer the Part M questions | 0 | None |
| T-011 | Create the empty GitHub repository, configure branch protection for `main` (CS-X-07) and set up the Student Pack benefits as Part K describes | 1 | Owner action |
| T-012 | Repository skeleton and root documents; the six context files in `docs/context/`; the two instruction files | 1 | CP-01.1 |
| T-013 | JVM build skeleton: Gradle Kotlin DSL, version catalog, `build-logic/` | 1 | CP-01.2 |
| T-014 | Python projects `model-service/` and `ml/`, each with its own `pyproject.toml` and `uv` lock | 1 | CP-01.3 |
| T-015 | Console skeleton in `console/` with the npm scripts named in `code-standards.md` | 1 | CP-01.4 |
| T-016 | CI skeleton, pre-commit hooks, the `tools/ci/` checks and `docs/compatibility-matrix.md` | 1 | CP-01.5 |
| T-017 | Local environment: Docker Compose with PostgreSQL, Kafka, Redis and Keycloak | 2 | The Phase 2 prompts |

## 8. Blockers

| ID | Blocker | Who resolves it | Resolved when | Status |
|---|---|---|---|---|
| B-01 | Spec baseline V1.0 is not approved, so no implementation may start (AW-20) | Owner | The owner states approval and it is entered in the change log | OPEN |

## 9. Open questions

| ID | Question | Needed by | Who decides |
|---|---|---|---|
| OQ-01 | ADR-006, model serving: a remote FastAPI `model-service` against an in-JVM ONNX runtime. The draft uses the remote service; the question stays open until there are measurements | Before Phase 11 starts (proposed timing) | Owner, after Claude's recommendation |
| OQ-02 | The blocking questions for the approval gate, at most five | Part M | Owner |
| OQ-03 | The UI decisions marked open in `ui-context.md` section 20: the Keycloak theme, the code editor (CodeMirror 6), the command palette implementation and the chart patterns (ECharts decal). Each becomes an ADR numbered from ADR-021 | Before the UI wave that needs it | Owner |
| OQ-04 | Confirm `docs/context/` as the location of the six files (D-10) | Part H | Owner |
| OQ-05 | Repository visibility, public or private, and what is shown publicly. Asked in Part M | Before T-011 | Owner |

## 10. Assumptions

| ID | Assumption |
|---|---|
| A-01 | One developer, the owner, with university coursework alongside. The plan is 30 weeks: Week 1 starts on Monday 2026-11-16 and Week 30 ends on Sunday 2027-06-13 |
| A-02 | GitHub Copilot is available through the Student Developer Pack and the service chooses the model, so every prompt is model-agnostic (AW-03). Part K re-verifies this |
| A-03 | An AWS account is opened in Week 9 (Monday 2027-01-11). Until then everything runs locally with Docker Compose. Cost limits are set when the account is opened |
| A-04 | The development laptop can run the local stack (PostgreSQL, a single-node Kafka, Redis, Keycloak, MLflow) using Compose profiles. Phase 2 measures it and records the result; until then it is an assumption |
| A-05 | All data is public or synthetic and is listed in `docs/data-sources.md`. No real personal or card data is used anywhere |
| A-06 | Every latency, throughput, accuracy and cost figure in the specs is a hypothesis until it is in `docs/claims-ledger.md` with its measurement conditions |
| A-07 | Versions in the specs were verified on the dates the files state. A version marked "resolve at scaffold" is not verified yet, and every recent major is checked again before use (AW-11) |
| A-08 | Exam, lab and mini-project deadlines reduce the hours available in some weeks. The owner supplies the dates and the roadmap marks lighter weeks around them (Part I) |

## 11. Technical risks

These ten are tracked here. Part L holds the full register with likelihood and impact and keeps these IDs.

| ID | Risk | Main mitigation | Where | Status |
|---|---|---|---|---|
| R-01 | Twenty-four phases are too much for one developer in 30 weeks | P0 and P1 freeze; an early vertical slice; critical path and optional work marked in the roadmap; Extended items are cut first | Part I, AW-20 | OPEN |
| R-02 | Coursework reduces the weekly hours | Lighter weeks in the roadmap, small weekly demos, buffer weeks | Part I | OPEN |
| R-03 | The local stack is too heavy for the development laptop | Compose profiles, a single-node Kafka, memory measured in Phase 2 | Phase 2 | OPEN |
| R-04 | Copilot invents APIs or relies on stale knowledge of recent majors (TypeScript 6, Vite 8, Vitest 5, ESLint 9, TanStack Table 9, MSW 3, Zod 4) | AW-09 to AW-12, AW-51, CS-T-02, CS-X-01, owner review | `ai-workflow-rules.md` | OPEN |
| R-05 | Some versions could not be verified during research | The compatibility matrix is completed in Phase 1 from real registry queries (AW-21) | Phase 1 | OPEN |
| R-06 | Online and offline feature definitions drift apart | One feature spec, golden fixtures and a CI parity gate (invariant 10) | Phase 8 | OPEN |
| R-07 | Event-time windows, grace periods and late data in Kafka Streams are hard to get right | An early spike in the vertical slice, only the two bucket sizes in the spec, replay tests | Phase 7 | OPEN |
| R-08 | AWS cost overrun | Ephemeral stacks, no NAT, budget alerts when the account opens, a cost model | Phase 20 | OPEN |
| R-09 | Mistakes in authentication, tenancy and idempotency | RLS tests per database role, ArchUnit, a Claude review of every P0-module pull request (CS-X-12) | Phases 4 to 6 | OPEN |
| R-10 | Overclaiming in the README, on the resume or in demos | Claims ledger, AW-32, the docs check, no placement or compliance claims | All phases | OPEN |

## 12. Architecture decisions

| ADR | Subject | Status | Where |
|---|---|---|---|
| ADR-001 to ADR-020, except ADR-006 | The architecture decisions of the draft | Drafted, frozen at V1.0 | `architecture.md` section 25 |
| ADR-006 | Model serving: remote FastAPI against in-JVM ONNX | OPEN (OQ-01) | `architecture.md` section 25 |
| ADR-021 and up | New decisions | None yet | `docs/adr/`, once the repository exists |
| Not yet numbered | The four UI decisions in OQ-03 | Pending | `ui-context.md` section 20 |
## 13. Test status

No code exists. Every ecosystem is NOT EXECUTED as of 2026-11-15.

| Ecosystem | Commands (`code-standards.md` section 8) | State | Date |
|---|---|---|---|
| JVM: `platform`, `stream`, `simulator`, `libs/*` | `./gradlew spotlessCheck check`, `./gradlew integrationTest`, `./gradlew jacocoTestCoverageVerification` | NOT EXECUTED: no code | 2026-11-15 |
| `model-service/` | `uv sync --locked`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy src`, `uv run pytest -m "not slow"` | NOT EXECUTED: no code | 2026-11-15 |
| `ml/` | The same five commands | NOT EXECUTED: no code | 2026-11-15 |
| `console/` | `npm ci`, `npm run lint`, `npm run format:check`, `npm run typecheck`, `npm run test`, `npm run build`, `npm run storybook:build`, `npm run test:e2e` | NOT EXECUTED: no code | 2026-11-15 |
| Contracts | `buf lint` and `buf breaking`, the OpenAPI breaking-change check, the feature parity gate | NOT EXECUTED: no contracts | 2026-11-15 |
| Infrastructure | `terraform fmt -check`, `terraform validate`, `terraform plan`, Trivy | NOT EXECUTED: no infrastructure | 2026-11-15 |
| Repository | Secret scan, size check, `tools/ci/check_exceptions.py`, `tools/ci/check_tokens.py`, `tools/ci/check_commit_messages.py`, docs check | NOT EXECUTED: no repository | 2026-11-15 |

Some checks were run in the research workspace during Phase 0. They are not repository tests: the colour contrast ratios and the chart palette colour-vision check in `ui-context.md`, and the parse check of the Mermaid diagrams in the architecture and UI files. The repository checks (`tools/ci/check_contrast.py`, `tools/ci/check_tokens.py` and the docs check) repeat them once they exist.

## 14. Current repository state

| Item | State |
|---|---|
| Repository | VERDICT monorepo; JVM and Python skeletons present |
| Local clone and branch | Local clone; `feature/console-skeleton` |
| Commits | Existing main baseline at `62e7b53`; current console work is uncommitted |
| Last merged milestone | CP-01.3 baseline on `main`; CP-01.4 in progress |
| `main` protection | UNVERIFIED in this session |
| GitHub Actions | None |
| Local environment | Node v26.13.0, npm 11.20.0; Java and Python toolchains were set up in prior milestones |
| Cloud | No AWS account in use (planned for Week 9) |
| Build | Gradle and uv workspaces present; console toolchain in progress |

## 15. Standards gaps

These are the rules that only review can enforce, or can enforce only in part. Each is re-examined at every phase gate (AW-40) and closed when a tool becomes feasible. The closing ideas are candidates only: confirm that the tool exists in the pinned version before adopting it (CS-X-01).

| Rule | What only review checks | Closing idea | State |
|---|---|---|---|
| CS-U-01 | One logical change per pull request, with no drive-by changes | The size check (CS-X-09) covers size only | OPEN, stays review |
| CS-U-02 | Canonical terms are used everywhere (organization, project, environment, API client, API credential and the rest of the list) | Extend the docs check with a list of banned synonyms for documents and UI strings | OPEN |
| CS-X-01 | Sources are cited for every new API, key, flag, package and version | None. The pull request template has the field and the owner checks it | OPEN, stays review |
| CS-X-02 | Existing code and the context files were read first, and no parallel implementation was written | None. The inspection summary in the report (AW-05 to AW-08) | OPEN, stays review |
| CS-X-03 | A README per deployable, an ADR per architecture decision, a runbook per alert, and the tracker updated | The docs check can find missing READMEs and broken links; the rest stays review | OPEN |
| CS-X-05 | The scripts in `tools/ci/` work on every operating system | Run the script tests on more than one OS in CI | OPEN |
| CS-X-12 | A human merges, the pull request is self-reviewed, and P0 modules get a Claude review | Branch protection enforces the pull request and the checks; the review itself stays a process | OPEN, stays process |
| CS-T-02 | The installed documentation of a recent major was read before use | None. Stays review together with AW-11 | OPEN, stays review |
| CS-T-06 | One module per cross-cutting concern (a single API client, a single auth module) | Restricted-import rules in the ESLint flat config | OPEN |
| CS-T-15 | The console never decides authorization | Tests exist; review confirms there is no permission logic beyond hiding and disabling controls | OPEN, partly tested |
| CS-T-24 | Testing Library conventions: query by role, test behavior | A Testing Library lint plugin, if one supports the installed ESLint major | OPEN |
| CS-J-11 | Records for DTOs, commands and events; closed sets | ArchUnit rules on package patterns | OPEN, partly tested |
| CS-J-12 | Immutability by default | Static-analysis or ArchUnit checks, if available for the pinned versions | OPEN |
| CS-P-06 | I/O at the edges and a pure core | Partly tested; the rest stays review | OPEN, partly tested |
| CS-P-14 | `model-service` has no database or Kafka access and no write access to platform state | An import test in `model-service/` plus network rules in `infra/` | OPEN |
| CS-D-06 | The EXPLAIN output is attached for each new hot-path query | Index existence is tested; the EXPLAIN evidence stays a pull request field | OPEN, partly tested |
| CS-D-07 | `jsonb` is used only for versioned snapshots | A catalog test that lists `jsonb` columns against an allow-list | OPEN, partly tested |
| CS-D-11 | Topics, buckets, queues and database roles are created by code in `infra/` | A CI check that compares the bootstrap lists with `infra/` and `contracts/` | OPEN |
| AW-01 to AW-58, except the tool-enforced rules named in AW-58 | Assistant behavior | The owner review gate (AW-37) and the pull request checklist | OPEN, stays review |
| UX-01 to UX-56 | The rules that `tools/ci/check_tokens.py`, `tools/ci/check_contrast.py`, axe, Playwright and the visual baselines do not reach | The design review gate of each wave (`ui-context.md` section 19) | OPEN |

## 16. Unit log

One row per implementation unit, added by the assistant in the same change (AW-41).

| Date | Prompt | Unit | Pull request | Gates | Claude review | Learning check | Status |
|---|---|---|---|---|---|---|---|
| 2026-11-21 | CP-01.4 | React/TypeScript console skeleton and compatibility pin | None | npm ci, lint, format check, typecheck, test and build PASSED; negative type/lint checks PASSED | Pending | Pending owner review | IN REVIEW |

## 17. Change log

Spec baseline changes, corrections, change requests and rule changes (AW-55, AW-56).

| Date | Change | Type | Approved by |
|---|---|---|---|
| 2026-11-21 | PD-1: pin TypeScript 6.0.3 and ESLint 9.39.5 to preserve required type-aware and jsx-a11y linting; document jsdom as test-only tooling | Approved compatibility decision | Owner |
| 2026-11-13 | `code-standards.md`: form library and icon library line corrected (note in the first part of `ui-context.md`) | Correction | Pending the approval gate |
| 2026-11-15 | `ai-workflow-rules.md` part 1: `FR-` identifiers replaced by feature and acceptance-criteria IDs | Correction | Pending the approval gate |
| 2026-11-15 | `progress-tracker.md` part 1: reference in D-10 corrected | Correction | Pending the approval gate |
| 2026-11-15 | Drafts 1.0.0 of the six context files delivered in chat | Draft | Pending the approval gate |

## 18. Prompt issues

Where an assistant misread a prompt (AW-54).

| Date | Prompt | What was misread | Fixed in library version |
|---|---|---|---|
| None yet | | | |

## 19. Recent session notes

Newest first, in the handoff format of `ai-workflow-rules.md` template 14.5.

```text
HANDOFF 2026-11-15, no repository
Done: The six context files are drafted and delivered in chat; this tracker is initialised.
In progress: The cross-file consistency review (T-001).
Uncommitted: None. There is no repository.
Resume with: T-001, then Parts H, I, J, K, L and M in that order.
Approvals awaited: The owner's review of the six files; approval of V1.0 (B-01).
Next prompt: None until approval, then CP-01.1.
```

```text
HANDOFF 2026-11-21 feature/console-skeleton
Done: CP-01.4 console skeleton, pinned npm toolchain, compatibility matrix, and docs updates.
In progress: Owner review; no commit or push made.
Uncommitted: Console source/configuration, package-lock.json, docs and root documentation changes.
Resume with: cd console && npm ci && npm run lint && npm run format:check && npm run typecheck && npm run test && npm run build
Approvals awaited: Owner review and explicit commit/push authorization.
Next prompt: CP-01.5 after review.
```

```text
HANDOFF 2026-11-14, no repository
Done: code-standards.md and ui-context.md delivered, with a correction note for the form and icon libraries.
In progress: ai-workflow-rules.md.
Next prompt: None.
```

## 20. Next implementation instruction

```text
NEXT IMPLEMENTATION INSTRUCTION
Status: IN PROGRESS.
Prompt: CP-01.4, Phase 1, milestone P01 — console skeleton.
Prerequisites to confirm: approved TypeScript/ESLint compatibility pin recorded in the active context and compatibility matrix; feature branch `feature/console-skeleton`.
Approvals still needed: none for implementation; owner review before commit or merge.
```

Update this file after every meaningful implementation unit (AW-41).
