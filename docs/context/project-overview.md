# VERDICT

**Real-Time Risk Decisioning and Intelligence Platform for Digital Systems**

Specification baseline: V1.0 (draft, pending owner approval) · Status: specification phase, no code written · Owner: project owner (sole developer)

## Overview

VERDICT is a programmable, event-driven platform that receives digital events (v1: simulated payment transactions), computes real-time behavioural features from event streams, combines deterministic policies with a machine-learning risk score, returns an explainable `APPROVE`, `REVIEW` or `DECLINE` decision within a latency budget, routes uncertain cases to human review, learns from outcomes that arrive days later, and governs every policy and model change through replay, shadow evaluation, approval and rollback. It is built for engineering teams that must make fast, auditable risk decisions on high-volume, duplicated, delayed and out-of-order data. It uses public and synthetic datasets only. It never moves money and makes no regulatory or PCI DSS claims.

## Product identity

| Item | Decision |
|---|---|
| Name | VERDICT |
| Positioning | Programmable risk decisioning with built-in model and policy governance |
| v1 use case | Real-time transaction risk (simulated): one use case done completely, on a reusable core |
| Decisions | `APPROVE`, `REVIEW`, `DECLINE`, each with reason codes, versions and evidence |
| Data policy | Public datasets used within their licences, plus synthetic streams. Every simulated outcome is labelled simulated |
| Environments | `SANDBOX` (demo data allowed) and `LIVE` (stricter governance, demo generators off). Even `LIVE` handles synthetic or permitted data only |
| Tenancy model | Organization (the tenant) → Project → Environment. "Workspace" in the UI means the organization a user is currently working in; there is no separate workspace table |

## Problem statement

Digital platforms must decide, within a few hundred milliseconds, whether to allow an event (for example a card-not-present payment) using information that is high volume, time sensitive, incomplete, duplicated, delayed, out of order, inconsistent between systems, and hard to label immediately. The decision must stay reliable when a dependency fails, must be explainable afterwards, and must change safely when a rule or model is updated.

Most portfolio projects stop at "call a model". The hard engineering is everything around it: retry-safe APIs, features that are fresh and identical in training and serving, labels that mature late, and promotion without regressions. VERDICT's engineering problem is to deliver reliable, reproducible, governed decisions despite those conditions.

## Goals

1. Return a decision for every valid request within the configured deadline, including during dependency failure, with degraded decisions clearly marked.
2. Guarantee that concurrent and repeated requests with the same idempotency key yield exactly one decision.
3. Publish every committed decision as an event without loss (at-least-once delivery with consumer-side deduplication).
4. Compute behavioural features from event time, tolerate late, duplicate and out-of-order events, and prove that the streaming (Java) and offline (Python) implementations agree on golden fixtures.
5. Evaluate models scientifically: time-ordered splits, imbalance-aware metrics, calibration, leakage controls and delayed-label cohorts, with every claim backed by a stored report.
6. Allow any past decision to be explained and re-run against a new policy or model without touching live traffic.
7. Make model and policy promotion safe: gates, approval by a second person, shadow evidence, one-action rollback.
8. Provide an enterprise-grade developer console and analyst workbench, designed before it is built and tested in a real browser.
9. Run locally with documented commands and on AWS through Terraform and CI/CD, with reproducible benchmarks.
10. Tie every performance, accuracy or cost claim to a measured, reproducible result.

## Target users and personas

| Persona | RBAC role | Goal | Main modules |
|---|---|---|---|
| Platform operator | `PLATFORM_ADMIN` | Create tenants and watch platform health; has no access to tenant decision data | Administration, platform health |
| Organization owner | `ORG_ADMIN` | Manage members, projects, environments and security settings; approve promotions | Administration, Audit, approvals |
| Risk analyst | `RISK_ANALYST` | Resolve review cases, tune policies, label outcomes | Cases, Decisions, Policy Studio, Replay Studio |
| Model manager | `MODEL_MANAGER` | Register, evaluate and shadow models; propose promotion | Model Centre, Feature Platform, Replay Studio |
| Integration engineer | `DEVELOPER` | Integrate the API, manage credentials, debug requests | Developer Portal, Decisions (sandbox), Simulation Lab |
| Auditor | `AUDITOR` | Read everything, change nothing, export evidence | Audit Centre, Decisions, policy and model history |

The permission matrix in `architecture.md` is the single source of truth for what each role may do.

## Business and engineering value

**Value to a risk or platform team (qualitative; no figures are claimed).**
- Faster, safer rule and model changes through replay and shadow evidence before promotion.
- Fewer silent failures: degraded modes are explicit, counted and alertable.
- An audit-ready history of who changed what, which version made which decision, and why.

**Engineering value (what this project demonstrates).** Idempotent concurrent APIs, transactional outbox, event-time stream processing, online/offline feature parity, time-aware ML evaluation, model lifecycle governance, multi-tenant security with row-level security, observability, AWS deployment with Terraform, and measured performance.

## Product boundaries

**Inside the boundary:** the decision API; event ingestion and streaming features; policy and model governance; case review; outcome ingestion and monitoring; replay; simulation; developer portal; identity and tenancy; audit; observability; local and AWS deployment.

**Outside the boundary (external actors, simulated):** payment processors, card networks, banks, chargeback systems, KYC providers and real customers. Their behaviour is represented by dataset replays and the simulator.

## Core workflows

**W1. Integrate and decide (the main flow).**
1. A client calls `POST /v1/decisions` with an API credential and an `Idempotency-Key`.
2. The platform validates the request, authenticates the credential, resolves tenant and environment, and applies rate limits.
3. It claims the idempotency key. Duplicates replay the stored result.
4. It reads online features and evaluates their freshness.
5. It evaluates the active policy version.
6. It requests the champion model's score and reason codes within the remaining deadline.
7. It combines policy and model outcomes according to the policy's decision strategy.
8. In one database transaction it stores the decision, the evidence snapshot, the idempotency result and an outbox event.
9. It returns the decision. A relay publishes the outbox event to Kafka.
10. If the decision is `REVIEW`, a case is created.
11. Later, outcome labels arrive and feed evaluation, monitoring and the next training run.

**W2. Review a case.** Open the queue → claim a case → inspect the decision, features, policy rules, model reasons and entity timeline → record an outcome and notes → the outcome is published and audited.

**W3. Change a policy safely.** Draft → validate → run test cases → dry-run or replay on history → submit for approval → a different user approves → activate → monitor → roll back in one action if needed.

**W4. Train, evaluate, register and promote a model.** The pipeline builds a point-in-time dataset → trains and evaluates → logs to MLflow → registers an immutable version with its artifact hash → the challenger runs in shadow → comparison and gates → a second user approves → atomic promotion → rollback stays available.

**W5. Replay history against a candidate.** Choose a time range and a candidate policy or model → an isolated replay job runs → per-decision differences and aggregate metrics appear → there are no live side effects.

**W6. Diagnose feature health.** Open the Feature Platform → view freshness, event lag, late and duplicate counts, missing values and online/offline parity → drill into one entity.

**W7. Run a simulation.** Pick a scenario and a seed → start the run → watch decisions, lag and degradation on the Overview → stop, and compare with an earlier run of the same seed.

**W8. Rotate an API credential.** Create a new credential → copy the secret once → deploy it → both work during the overlap window → revoke the old one → the audit log shows the chain.

**W9. Audit an outcome.** Search a decision → view what produced it, the versions, the evidence and later labels → export the evidence bundle (authorised and audited).
## Features

Classification: **P0** essential, **P1** differentiating, **P2** advanced extension, **P3** not built. IDs are used by the roadmap, the prompts and the tests.

| Area | P0 | P1 | P2 |
|---|---|---|---|
| Decisioning | F01 Decision API, idempotency, outbox · F03 Policy engine and versions · F04 Model scoring and reason codes · F05 Decision evidence store | F13 Replay Studio · F14 Policy dry-run and historical replay · F21 Entity timeline | F24 Outbound webhooks · F25 Live traffic-split experiments |
| Features | F02 Streaming features and online store | F15 Feature Consistency Lab | none |
| ML lifecycle | F07 Model governance core · F09 Outcome ingestion and label maturation | F16 Shadow and champion/challenger analytics · F17 Drift and quality monitoring | F27 Sequence-model challenger · F26 Investigation assistant (with NLP retrieval) |
| Operations | F08 Case review · F11 Simulator · F12 Observability baseline | F18 Case workbench depth · F19 Simulation Lab · F20 Command palette, search, saved views · F22 Authorised exports | none |
| Platform | F06 Identity, RBAC, tenancy, credentials, audit · F10 Developer portal | F23 Portal depth | none |
| **P3 (not built)** | Computer vision, graph or ring detection, active learning, AutoML, multi-region, real payments, chargeback integrations, any compliance claim | | |

## Functional requirements

IDs are stable and are referenced by acceptance tests.

### Decision API
- **FR-DEC-01** `POST /v1/decisions` accepts one canonical risk event and returns `decision` (`APPROVE|REVIEW|DECLINE`), `decision_id`, `risk_score` (when available), `reason_codes`, `policy_version`, `model_version`, `degraded`, `degradation_reasons` and `evaluated_at`.
- **FR-DEC-02** `Idempotency-Key` is required. The same key and payload return the original response with `Idempotent-Replayed: true`. The same key with a different payload returns `422`. Concurrent duplicates produce exactly one decision.
- **FR-DEC-03** Requests are validated against the published schema. Unknown fields, non-decimal amounts and non-UTC timestamps are rejected with a structured error.
- **FR-DEC-04** Tenant and environment are derived only from the API credential. A tenant or environment in the body is rejected.
- **FR-DEC-05** The active policy runs first, then the champion model. The policy's decision strategy defines how the two combine.
- **FR-DEC-06** The decision, evidence snapshot, idempotency result and outbox event are committed in one transaction.
- **FR-DEC-07** Dependency failures follow the failure matrix in `architecture.md`. Every degraded decision is labelled and counted.
- **FR-DEC-08** A per-request deadline is enforced, with a sub-budget per dependency.
- **FR-DEC-09** Per-client rate limits return `429` with `Retry-After`.

### Features and events
- **FR-FEA-01** Feature definitions are versioned (`feature_schema_version`) and computed from event-time bucketed aggregates.
- **FR-FEA-02** Late events within the grace period update aggregates. Later events go to a side topic and are counted.
- **FR-FEA-03** A duplicate `event_id` never changes an aggregate.
- **FR-FEA-04** Every decision stores its feature values, as-of times and freshness status.
- **FR-FEA-05** Missing, stale, invalid or outdated-schema features trigger the behaviour the policy defines (flag, review, rules only).
- **FR-FEA-06** The online store can be rebuilt from Kafka by a documented, tested procedure.
- **FR-FEA-07** Java streaming features and Python offline features agree on the golden fixtures within the declared tolerance. This is a CI gate.

### Policy
- **FR-POL-01** Policies are JSON documents in the Verdict Policy Language (VPL) v1. No code is ever executed.
- **FR-POL-02** A published version is immutable. States: `DRAFT`, `VALIDATED`, `PENDING_APPROVAL`, `ACTIVE`, `SUPERSEDED`, `ROLLED_BACK`.
- **FR-POL-03** An author cannot approve their own version.
- **FR-POL-04** Dry-runs and replays never affect live decisions.

### Models
- **FR-MOD-01** A model version records its artifact SHA-256, feature schema version, dataset manifest hash, training parameters, metrics and evaluation report.
- **FR-MOD-02** Per environment, a version is `CHAMPION`, `SHADOW` or `RETIRED`.
- **FR-MOD-03** Promotion requires passing gates, approval by a different user and an audit record. It is atomic. Rollback is one action.
- **FR-MOD-04** The platform confirms that the model service serves the expected artifact hash before routing traffic to a new champion.
- **FR-MOD-05** Shadow scores are recorded without affecting decisions and may be dropped under load (and counted).
- **FR-MOD-06** Every score returns reason codes.

### Outcomes and monitoring
- **FR-OUT-01** `POST /v1/outcomes` records a label idempotently by `outcome_id`, with its own `occurred_at` and a `source` (`ANALYST`, `DATASET`, `SIMULATED`).
- **FR-OUT-02** Labels carry a maturity state. Evaluation uses only matured cohorts.
- **FR-OUT-03** Feature and prediction drift are indicators. Accuracy degradation is reported only from matured labels.

### Cases
- **FR-CAS-01** Each `REVIEW` decision creates exactly one case.
- **FR-CAS-02** States: `OPEN`, `ASSIGNED`, `IN_REVIEW`, `RESOLVED`, `REOPENED`. Resolutions: `CONFIRMED_RISK`, `NOT_RISK`, `INCONCLUSIVE`. Every transition is audited.
- **FR-CAS-03** A resolution publishes an outcome event.

### Replay and simulation
- **FR-REP-01** Replay reads stored evidence and never writes to live decision tables or topics.
- **FR-REP-02** Replay reports per-decision differences and states where exact determinism cannot hold.
- **FR-SIM-01** Runs are seeded. The same seed and configuration produce an identical event sequence.
- **FR-SIM-02** Scenarios: baseline, spike, suspicious burst, duplicates, out-of-order, delayed events, model degradation, missing features, distribution shift, consumer lag.
- **FR-SIM-03** Simulated data and labels are labelled as simulated everywhere they appear.

### Identity, security, audit
- **FR-SEC-01** Console sign-in uses OIDC (Keycloak). Sessions are server-side. Cookies are `HttpOnly`, `Secure` and `SameSite`. CSRF protection is on. Sign-out revokes the server session.
- **FR-SEC-02** RBAC is enforced on the server. The UI hides forbidden actions but never relies on hiding.
- **FR-SEC-03** Tenant isolation is enforced in application code and by PostgreSQL row-level security.
- **FR-SEC-04** API credentials are scoped, environment-bound, stored hashed, shown once, expiring, rotatable and revocable.
- **FR-SEC-05** Security and governance actions write append-only, hash-chained audit records.
- **FR-SEC-06** Console users can enable TOTP multi-factor authentication.

### Frontend and developer experience
- **FR-UI-01** Every page implements initial, loading, empty, success, error, unauthorized, forbidden, stale and degraded states.
- **FR-UI-02** No control exists without working backend behaviour. No fake data is presented as real.
- **FR-UI-03** Tables paginate, sort and filter on the server, with filters held in the URL.
- **FR-UI-04** WCAG 2.2 AA is the engineering target, verified by automated and manual checks.
- **FR-DEV-01** A new engineer can run the full stack locally from documented commands and reach a first decision (target: under 30 minutes, measured by a fresh-clone test).

## Non-functional requirements

Numeric targets are **hypotheses** to be tested. Phase 22 publishes the measured results, including any misses.

| ID | Requirement | Target (hypothesis) |
|---|---|---|
| NFR-LAT-01 | Decision latency, server side | p50 ≤ 40 ms and p99 ≤ 250 ms at 200 requests/s sustained, in the reference benchmark environment |
| NFR-LAT-02 | Overall request deadline | Default 300 ms, configurable, with sub-budgets per dependency |
| NFR-FRS-01 | Feature freshness | p99 from event publish to online-store visibility ≤ 2 s at 500 events/s |
| NFR-AVL-01 | Behaviour during a model-service outage | Every request still gets a decision (degraded) within the deadline; no 5xx except defined fail-closed cases |
| NFR-COR-01 | Idempotency | 0 duplicate decisions across 50 concurrent identical requests over 1,000 keys |
| NFR-COR-02 | Event loss | 0 committed decisions missing from Kafka after relay-restart and broker-restart tests |
| NFR-COR-03 | Feature parity | 100% of golden-fixture features equal within the declared tolerance |
| NFR-REC-01 | Backlog recovery | Documented and measured after a consumer outage |
| NFR-SEC-01 | Tenant isolation | 0 cross-tenant reads in the isolation suite, both at the app layer and with RLS enforced alone |
| NFR-A11Y-01 | Accessibility | 0 serious or critical axe violations on key screens; keyboard-complete flows |
| NFR-OPS-01 | Reproducibility | Fresh clone to running stack by documented steps; benchmarks reproducible from a commit |
| NFR-CST-01 | Cost | Every cloud session has an estimate with stated assumptions; no always-on expensive resources |

## Scope

### In Scope
All P0 and P1 features above; one complete transaction-risk use case on a reusable core; local and AWS deployment; CI/CD; benchmarks; documentation.

### MVP and advanced scope
- **Walking skeleton (earliest demonstrable slice):** authenticated API call → rules plus a stub score → persisted decision → outbox → Kafka → streaming feature → Redis → the next decision reads that feature → the decision is visible in the console.
- **MVP:** all P0 features, working end to end and deployed.
- **Advanced:** P1 features. **Extensions:** P2 features, only if the schedule allows.

### Out of Scope (non-goals)
Real money movement or settlement; PCI DSS, SOC 2 or any regulatory certification claim; real customer or cardholder data; production-grade fraud-accuracy claims; several unrelated domain applications; computer vision; a generic BI tool; a full Feast-style feature store; arbitrary code execution in policies; multi-region operation; a mobile app.

## Cross-industry applicability

The core operates on a canonical `risk event` (subject, optional counterparty, amount, attributes, event time). A new domain needs an adapter, a feature pack and a policy pack, not a new platform. Only the transaction pack is built in v1.

| Domain | Subject | Event | Typical decision | What changes |
|---|---|---|---|---|
| Transactions (v1) | Card or account | Payment | Approve, review, decline | Built in v1 |
| Account abuse | Account | Login, profile change | Allow, step-up, block | New features and policies |
| E-commerce abuse | Customer | Order, refund | Approve, review, cancel | New adapter and features |
| Marketplace risk | Seller or listing | Listing, payout | Publish, review, hold | Adapter and policies |
| Bot and automated abuse | Session or device | Request | Allow, challenge, block | Rate-based features |
| Abnormal activity | Any entity | Any event | Flag, review | Baseline-deviation features |

## AI/ML responsibilities

| Responsibility | ML does | Rules and humans do |
|---|---|---|
| Risk scoring | A gradient-boosted model scores a feature vector and returns reason codes | Policies set hard guardrails and thresholds; humans resolve reviews |
| Evaluation | Time-ordered, imbalance-aware, calibrated, with confidence intervals | Gates decide whether a candidate may be promoted; a second person approves |
| Monitoring | Drift indicators; performance from matured labels | Alerts require a human decision |
| Replay and shadow | Candidate scoring on stored evidence | Comparison informs; it never auto-promotes |
| Optional (P2) | A sequence-model challenger; a grounded assistant | The assistant can never decide or act |

## Onboarding experience and user journey

A new user must reach a first real decision, and see it explained, without a walkthrough from the developer. First run is a guided checklist, not a tour overlay: each step does real work against the real API and ends in a visible result.

```mermaid
flowchart LR
    A["Sign up and verify email"] --&gt; B["Create organization"]
    B --&gt; C["Create project"]
    C --&gt; D["Create environment&lt;br/&gt;(Sandbox, demo mode)"]
    D --&gt; E["Generate scoped API credential"]
    E --&gt; F["Copy secret once"]
    F --&gt; G["Quickstart: send test transaction"]
    G --&gt; H["Receive decision"]
    H --&gt; I["Inspect features, policy, model evidence"]
    I --&gt; J["Explore the decision record"]
    J --&gt; K["Start the simulator"]
    K --&gt; L["Watch Overview update"]
```

Rules: demo data is always labelled "Demo"; empty states explain the next action; every error says what to do; documentation links sit beside the control they explain.

## Success Criteria

The product has succeeded when a reviewer who has never seen it can, from a fresh clone: run it, send a transaction, inspect the explanation, run a simulation, watch a model get promoted and rolled back, replay history against a candidate, reproduce a benchmark, and find, for every claim in the README, the test or report that supports it.

## Acceptance criteria

| ID | Criterion | Verified by |
|---|---|---|
| AC-01 | 50 concurrent identical requests produce one decision, one outbox row and identical responses | Java concurrency integration test |
| AC-02 | The same key with a different payload returns 422 | API test |
| AC-03 | Killing the process mid-request leads to correct takeover after the lease expires | Crash-recovery test |
| AC-04 | Broker outage then recovery: no committed decision is missing from Kafka | Fault test |
| AC-05 | Duplicate, late and out-of-order fixtures yield the expected aggregates | Streams topology tests |
| AC-06 | Java and Python features match on golden fixtures | CI parity job |
| AC-07 | Redis wipe and rebuild reproduces the same feature values | Rebuild test |
| AC-08 | Model-service outage yields degraded decisions within the deadline | Toxiproxy fault test |
| AC-09 | A stale or missing feature follows the policy's defined behaviour | Policy and decision tests |
| AC-10 | A tampered model artifact is rejected | Model-service contract test |
| AC-11 | Promotion needs a second approver; rollback restores the previous champion | Governance tests |
| AC-12 | Replay changes no live table or topic and reproduces the original decision for unchanged inputs | Replay tests |
| AC-13 | A user of tenant X can never read tenant Y data, with and without app-layer filters | Isolation suite |
| AC-14 | Each role can do exactly what the permission matrix allows | Authorization matrix test |
| AC-15 | Credential secrets are shown once, stored hashed, and rotation works | Security tests |
| AC-16 | CSRF, CORS and cookie attributes behave as specified | Security tests |
| AC-17 | The same seed gives the same simulated event sequence | Simulator test |
| AC-18 | Label maturity windows exclude immature outcomes from evaluation | ML tests |
| AC-19 | The training pipeline is reproducible from a manifest and seed | ML reproducibility test |
| AC-20 | Key screens pass axe checks, keyboard flows and visual regression | Playwright and Storybook |
| AC-21 | A fresh clone reaches a first decision using the documented steps | Fresh-clone test |
| AC-22 | CI deploys to AWS through OIDC and Terraform and tears down cleanly | Deployment pipeline |
| AC-23 | Every published benchmark has configuration, seed, commit and raw results | Benchmark harness |
| AC-24 | Audit-chain verification detects a modified record | Audit tests |

## Definition of completion

V1.0 is complete when: all P0 and P1 features are implemented behind real APIs; AC-01 to AC-24 pass in CI or have a documented, reproducible manual procedure; the AWS deployment has been created and destroyed from the pipeline; benchmark and ML reports are published with raw results; the README, ADRs, runbooks, threat model and model cards are current; the 10–15 minute demo runs live on the deployed system; and a claims ledger maps every public claim to its evidence.

## Specification governance

Baseline: **VERDICT Specification Baseline V1.0**. After approval, product direction, service boundaries and contracts are frozen. Feature additions need a change request (problem, rationale, impact, migration, revised acceptance tests). Architecture changes need an ADR. Security invariants cannot be bypassed. Schema changes need a migration and a compatibility analysis. UI changes follow the design system in `ui-context.md`.
