# VERDICT — UI Context

**Version:** 1.0.0 (draft until the approval gate, then frozen with spec baseline V1.0)
**Scope:** the complete visual and interaction specification of the VERDICT console (`console/`).
**Companions:** `project-overview.md` (workflows, personas), `architecture.md` (services, roles, APIs), `code-standards.md` (how UI code is written, rule IDs `CS-T-nn`), `ai-workflow-rules.md`, `progress-tracker.md`.

## 1. Purpose and status

- This file decides how the console looks and behaves. `architecture.md` decides what exists. A page, control, filter, chart or notification exists only if the API behind it exists in `architecture.md` and is implemented. Otherwise it is cut, never mocked (**UX-01**).
- Demo data and realistic fixtures appear only in tests, Storybook and environments flagged as demo, and are labelled "Demo data" on screen wherever they appear (**UX-02**).
- Section 7 is the single source of token values. `console/src/styles/tokens.css` implements it. `tools/ci/check_tokens.py` (no literal colors or arbitrary sizes outside tokens) and `tools/ci/check_contrast.py` (every pair listed in section 7.3 meets its ratio) fail the build when code and this file disagree.
- Rules in this file are numbered `UX-nn`. Reviews and Copilot reports cite them the way they cite `CS-` rules.
- Role names live in the RBAC matrix of `architecture.md`. The console keys on the permission set returned by the session endpoint, never on role names (CS-T-15). Where this file mentions a persona, it uses the persona names from the system context: integration engineer, risk analyst, model manager, administrator, auditor.

## 2. Design philosophy

1. **Evidence before decoration.** Every pixel carries information or structure. There is no chart without a question it answers and no tile without a number someone acts on.
2. **The decision record is the unit.** Every metric drills down to the decisions behind it in at most two clicks, and every decision links to its evidence, policy version, model version and audit trail.
3. **State honesty.** Data always shows its age and its source. Degraded, stale, demo and read-only conditions are visible, never implied.
4. **Dense but calm.** High information density on a strict grid with quiet neutrals. Color is reserved for meaning: status, selection, focus and data series.
5. **Governance is visible.** Environment mode, approvals, who requested and who approved, and links to audit records are first-class interface elements.
6. **Keyboard first, mouse friendly.** Every action is reachable from the keyboard. Shortcuts accelerate; they are never required.
7. **Consequence sets the friction.** Reading is free, reversible actions are one step, consequential actions confirm, and actions in a `LIVE` environment require typed confirmation.
8. **Engineered, not decorated.** The identity comes from thresholds, rules, grids and measured type, not from gradients, illustration or oversized rounded cards.

## 3. Design research

General knowledge of these products and their public documentation; nothing was re-fetched for this file, and no logo, styling, asset or pixel layout was copied.

| Reference | What was studied | What VERDICT takes | What VERDICT avoids |
|---|---|---|---|
| Datadog | Dashboard density, one time and facet filter row scoping everything below it | A single filter row above content; dense panels on a strict grid | Widget-gallery sprawl; decorative sparklines |
| Postman | Request playground, environment selector, collections | An environment selector that changes the whole console scope; a playground that calls the real API | Multi-pane complexity in the first-run experience |
| Linear | Keyboard-first flows, command menu, restrained palette, list and detail | Keyboard shortcuts, a command palette, calm neutrals, list and detail layouts | Marketing-style gradients and motion |
| Notion | Workspace switcher, guided empty states | A workspace switcher; empty states that say what to do next | Free-form blocks |
| GitHub Primer | Role-named tokens, status labels, focus treatment, density options | Tokens named by role; two density modes; strong focus rings | Copying component styling |
| Stripe | Test and live mode prominence, docs-integrated dashboard | Unmistakable environment mode treatment; copy-once credentials; docs beside the playground | Ornamental gradients |
| Atlassian Design System | Content design, error and empty-state guidance, accessibility | Error and empty-state microcopy structure | Its visual identity |
| IBM Carbon | Data visualization guidance, density, accessibility, an open-source type family | IBM Plex as the typeface (open licence); two densities; accessible chart practice | Carbon's component look |
| Storybook and TanStack Table docs | Writing tests for stories; virtualization guidance | Stories as the component contract; virtualization above a measured threshold | Virtualizing short lists |

## 4. Brand identity

**Name and idea.** VERDICT is the moment a decision is made. The identity is built from three things in every decision: a space, a threshold and a score.

**Mark.** A square (the decision space), a horizontal line two thirds of the way down (the threshold) and a small filled square above it (the score). Monochrome only, drawn with `currentColor`:

```svg
&lt;svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"&gt;
  &lt;rect x="3" y="3" width="18" height="18" stroke="currentColor" stroke-width="2"/&gt;
  &lt;path d="M3 15h18" stroke="currentColor" stroke-width="2"/&gt;
  &lt;rect x="13" y="8" width="4" height="4" fill="currentColor"/&gt;
&lt;/svg&gt;
```

**Wordmark and lockup.** "VERDICT" in IBM Plex Sans SemiBold (600), 16 px, letter-spacing 0.08 em, set in capitals as a wordmark only (never as a text style). Horizontal lockup: 24 px mark, 8 px gap, wordmark vertically centered on the mark. The mark alone is used in the collapsed sidebar and as the favicon (SVG favicon with an internal `prefers-color-scheme` rule so it follows the OS).

**Usage rules (UX-03).**

| Rule | Value |
|---|---|
| Clear space | One sixth of the mark's width (4 px at 24 px) on every side |
| Minimum size | Mark 16 px; lockup with a 20 px mark |
| Color | `--color-text-primary` only. Never an accent or status color, never a gradient or shadow |
| Never | Stretch, rotate, outline, animate or place on a busy image; recolor the marker; add a tagline in the lockup |

**Brand color.** Ink (`--color-text-primary`) is the brand. Signal blue (`--color-accent`) marks interactive state only: the primary action, links, selection and focus. Status colors mean status and nothing else. No other hue appears in the chrome.

**Imagery.** No stock photography, mascots or decorative illustration. Empty and onboarding states use typography, the Verdict strip (section 9.9) and real structure from the product.

**Voice.** Plain and exact. Sentence case. No exclamation marks, no emoji, no apologies in errors, no jokes in failure states. Say what happened and what to do.

## 5. Vocabulary and copy

### 5.1 Terms

| UI term | Meaning | Not used |
|---|---|---|
| Organization | The tenant boundary (the API says organization) | account, company, tenant |
| Workspace | A UI label only for the current organization and project pair. It is not an entity, API field or route segment (ADR-019) | |
| Project | Groups environments, policies and models | app, product |
| Environment | An isolated data and credential scope with a mode badge | stage, tier |
| API credential | What a client sends to authenticate. The identifier prefix `vk_` is shown; the secret is shown once | API key (docs may say "key" in code identifiers only) |
| Subject | The account, card or customer a decision is about | user, customer |
| Event | The input record sent for a decision | transaction (except in the demo story) |
| Decision | The result of evaluating an event: Approve, Review or Decline | verdict, assessment |
| Outcome label | The later-known truth about a decision, such as confirmed fraud | outcome (alone), feedback |
| Case | A human review item created by a Review decision | ticket, alert |
| Policy, rule | Versioned rules that decide. "VPL" appears only in developer documentation | script, ruleset |
| Model, model version | A trained scorer and its immutable versions. The deployed version is the champion; a candidate under evaluation runs in shadow | |
| Replay | Re-deciding a stored event under another policy or model in isolation | re-run, backtest |

Area names are proper nouns and keep their spelling: Decision Explorer, Policy Studio, Model Centre, Feature Platform, Replay Studio, Simulation Lab, Developer Portal, Audit Centre. All other UI copy uses the `z` spellings of the canonical domain terms.

### 5.2 Copy rules

| ID | Rule |
|---|---|
| UX-04 | Sentence case everywhere. All-caps appears only in the wordmark and in raw enum values inside code and JSON views. Statuses display as "Approve", "Review", "Decline" |
| UX-05 | A button names its action with a verb and object ("Revoke credential"). The same word is used in the dialog title, the button, the toast and the audit entry. "Submit" and "OK" are not used |
| UX-06 | An error says what happened, why if known, and what to do next, and shows the API's reference identifier when one is returned. No apology, no blame, no stack text |
| UX-07 | An empty state says what the area shows, then offers one primary action. "No results" for an active filter offers "Clear filters" |
| UX-08 | Numbers use one locale constant (`en-US` grouping) in `lib/format`. Amounts always show the environment's ISO currency code and minor-unit precision. Latencies show a unit ("42 ms"). Rates and percentages state their window ("last 15 min") |
| UX-09 | Times are shown in UTC with the suffix "UTC" by default; a personal setting switches to local time and then shows the offset. Relative times ("3 min ago") always carry the absolute time in a tooltip |
| UX-10 | Helper text and descriptions stay under 80 characters per line and under 140 characters in total; anything longer links to documentation |
## 6. Information architecture

### 6.1 Sitemap

```mermaid
flowchart LR
    root["App root"] --&gt; auth{"Session?"}
    auth --&gt;|"no"| signin["Sign in with Keycloak"]
    auth --&gt;|"yes, no project yet"| welcome["Welcome and onboarding"]
    auth --&gt;|"yes"| env["Environment scope: /e/:environmentId"]
    env --&gt; monitor["Monitor"]
    env --&gt; configure["Configure"]
    env --&gt; test["Test"]
    env --&gt; integrate["Integrate"]
    monitor --&gt; overview["Overview"]
    monitor --&gt; decisions["Decisions"] --&gt; decision["Decision detail"]
    monitor --&gt; cases["Cases"] --&gt; casedetail["Case detail"]
    configure --&gt; policies["Policies"] --&gt; policy["Policy version"]
    configure --&gt; models["Models"] --&gt; model["Model version"]
    configure --&gt; features["Features"]
    test --&gt; replay["Replay"] --&gt; replayjob["Replay job"]
    test --&gt; simulator["Simulator"] --&gt; run["Simulation run"]
    integrate --&gt; developers["Developers"] --&gt; keys["API credentials"]
    auth --&gt;|"yes"| orgscope["Organization scope"]
    orgscope --&gt; audit["Audit"]
    orgscope --&gt; settings["Settings"]
```

### 6.2 Areas

| Area | Sidebar label | Primary persona | Backing modules (`architecture.md`) |
|---|---|---|---|
| Overview | Overview | Everyone | `insights`, `features`, `decision` |
| Decision Explorer and detail | Decisions | Risk analyst, auditor | `decision`, `insights` |
| Case management | Cases | Risk analyst | `cases` |
| Policy Studio | Policies | Risk analyst | `policy`, `governance` |
| Model Centre | Models | Model manager | `governance`, `scoring` |
| Feature Platform | Features | Model manager, integration engineer | `features` |
| Replay Studio | Replay | Risk analyst, model manager | `replay` |
| Simulation Lab | Simulator | Integration engineer, risk analyst | `simctl` |
| Developer Portal | Developers | Integration engineer | `identity` (credentials), `decision` (playground) |
| Audit Centre | Audit | Auditor, administrator | `audit` |
| Administration | Settings | Administrator | `identity` |

### 6.3 Routes

SPA paths never start with `/console` or `/v1`; the load balancer routes those to the platform. CloudFront returns `index.html` for unknown SPA paths so deep links work (configured in `infra/`).

| Path | Page |
|---|---|
| `/` | Redirects to the viewer's last environment Overview, or to `/welcome` when the organization has no environment |
| `/welcome` | Onboarding checklist and first-run flow (also reachable from the help menu) |
| `/e/:environmentId/overview` | Overview |
| `/e/:environmentId/decisions` | Decision Explorer. `?peek=:decisionId` opens the peek drawer |
| `/e/:environmentId/decisions/:decisionId` | Decision detail. `?tab=` selects Summary, Evidence, Timeline, Outcome |
| `/e/:environmentId/cases` and `/cases/:caseId` | Case queue and case workbench |
| `/e/:environmentId/policies`, `/policies/:policySetId`, `/policies/:policySetId/versions/:versionId` | Policy sets, one policy set with its versions, one version (editor or read-only) |
| `/e/:environmentId/models` and `/models/:modelId/versions/:versionId` | Model registry and one model version |
| `/e/:environmentId/features` | Feature Platform |
| `/e/:environmentId/replay` and `/replay/:replayJobId` | Replay jobs and one job's result |
| `/e/:environmentId/simulator` and `/simulator/:runId` | Simulation runs and one live run |
| `/e/:environmentId/developers` and `/developers/credentials` | Quickstart, playground, schemas and limits (tabs); API credentials |
| `/audit` | Audit Centre (organization scope, environment is a filter) |
| `/settings/organization`, `/settings/members`, `/settings/projects`, `/settings/security` | Administration |
| `/account` | Profile, sessions, theme, density, time zone, shortcuts |
| `/forbidden`, `/session-expired`, `*` | Full-page error states |

| ID | URL rule |
|---|---|
| UX-11 | The environment is always a path segment. Filters, sort, pagination, time range and tab live in validated query parameters (Zod). An invalid parameter falls back to its default and shows a one-line notice naming the parameter. Every view is a shareable link |
| UX-12 | Identifiers render in the monospace face as the first 8 characters with an ellipsis, the full value in a tooltip, and a copy button. The copy action confirms with a polite live-region message |

### 6.4 Application shell

| Region | Specification |
|---|---|
| Skip link | First focusable element, visible on focus: "Skip to main content" |
| Sidebar | Full height, left. Expanded 232 px, collapsed rail 56 px. `--color-bg-surface` with a 1 px right border. Top 48 px holds the lockup (the mark alone when collapsed). Below it the workspace switcher, then the navigation groups. The collapse toggle sits at the bottom and `[` toggles it. Collapsed state persists per viewer |
| Top bar | 48 px high, the width of the content area. Left to right: environment selector, search button (240 to 320 px, label "Search or jump to", shows the shortcut), flexible space, help menu, account menu. A `LIVE` environment adds a 2 px top rule in `--color-text-primary` across the full width |
| Banner slot | Between the top bar and the page header. Stacked banners for platform degradation, demo environment, session warnings and stale data. Informational banners can be dismissed; degradation banners cannot |
| Page header | Breadcrumb (12/16, secondary), title as `h1` (20/28), status chips, primary actions right-aligned. Minimum height 56 px, not sticky |
| Content | Padding 24 px (16 px below 768 px). 12-column grid with 16 px gutters. Data pages use the full width; reading pages (documentation, onboarding) cap at 1120 px and prose at 72 characters |
| Drawer | Right overlay, 480 px (720 px wide variant), focus trapped, scrim behind |
| Toasts | Bottom right, 16 px from the edges, at most three visible |
| Sticky layers | Top bar (z 40) and a table toolbar that sticks at 48 px. `scroll-padding-top` equals both combined so a focused element is never hidden behind them (WCAG 2.2, 2.4.11) |

**Navigation groups.** Group headings are 12/16 text in `--color-text-tertiary`, sentence case. Items are 32 px high with a 20 px icon (icon concepts below; exact Lucide names are verified at scaffold, CS-X-01).

| Group | Items (icon concept) |
|---|---|
| Monitor | Overview (gauge), Decisions (list), Cases (inbox) |
| Configure | Policies (sliders), Models (box), Features (activity) |
| Test | Replay (rewind), Simulator (flask) |
| Integrate | Developers (terminal) |
| Govern | Audit (scroll), Settings (gear) |

| ID | Rule |
|---|---|
| UX-13 | An item or page the user can never use is hidden. An action the user could perform in another state or with a grant is shown disabled with a visible reason next to it (not only a tooltip) |
| UX-14 | A navigation item ships only with a page that works end to end. No placeholder pages |
| UX-15 | The active item uses `--color-bg-selected`, a 2 px accent bar on the inline start, and `aria-current="page"` |

### 6.5 Workspace and environment selectors

**Workspace switcher** (sidebar, under the lockup). Shows the organization name (13/20) over the project name (12/16, secondary) with a chevron. It opens a popover with a search field when there are more than seven entries, organizations first when the user belongs to several, then the projects of the selected organization. Choosing a project opens its last-used environment's Overview, or `/welcome` if it has none. "Create project" appears at the bottom only with permission.

**Environment selector** (top bar, left). Shows the environment name and a mode badge. The popover lists the project's environments with their badges. The badge text is the API's mode value; the visual treatment depends on three categories:

| Category | Treatment |
|---|---|
| `LIVE` governance mode | Inverted ink badge ("Live") and the 2 px top rule across the app |
| Flagged as demo data | Outline badge "Demo data" in info colors, plus the "Demo data" label on every panel that shows demo content (UX-02) |
| Any other mode | Neutral outline badge with the mode text |

| ID | Rule |
|---|---|
| UX-16 | Switching environment keeps the same page when it exists in the target (new `:environmentId`), otherwise goes to Overview. Detail pages go to their list because identifiers do not carry across. Unsaved form changes ask before leaving |
| UX-17 | In a `LIVE` environment, governance and destructive actions (policy activation, model promotion, credential revocation, settings changes) require typing the environment name in the confirmation dialog |

### 6.6 Search and command palette

`Ctrl/Cmd+K` or the search button opens a modal command palette (Radix Dialog with an ARIA combobox and listbox). It contains only commands with real behavior:

- Navigate to any page the user may open.
- Jump to a decision or case by identifier, using the lookup endpoints. An unknown identifier shows "Not found" with no fallback.
- Switch project or environment.
- Toggle theme and density, and show the keyboard shortcut list.
- Recent items: the last eight detail pages visited, stored in the viewer's browser.

**UX-18.** The palette does not search decision content. Searching decisions is done with Decision Explorer filters, which are server-side. The palette and shortcut layer are Extended scope, cut first if the schedule slips, and their controls ship only with them (UX-01).

**Breadcrumbs.** In the page header: "Policies / Card-not-present baseline / Version 7", with the current page as plain text carrying `aria-current`. Below 768 px the middle items collapse into a menu.

## 7. Design tokens

### 7.1 Principles

- Tokens are CSS custom properties defined in `console/src/styles/tokens.css`, named by role, never by value (`--color-bg-surface`, not `--color-gray-900`). Tailwind v4 utilities are generated from them through its theme variables; the exact directive syntax is verified against the installed Tailwind documentation at scaffold (CS-X-01).
- Dark is the default theme (section 16). The `:root` block holds dark values and `:root[data-theme="light"]` overrides them. `color-scheme` is set to match.
- Components use tokens only (CS-T-17). A new token needs an entry in this file first.

### 7.2 Color tokens

| Token | Dark | Light | Use |
|---|---|---|---|
| `--color-bg-canvas` | `#0C1014` | `#F3F5F7` | Page background behind panels |
| `--color-bg-surface` | `#12171D` | `#FFFFFF` | Panels, tables, sidebar, chart surface |
| `--color-bg-raised` | `#1A2028` | `#FFFFFF` | Popovers, menus, dialogs, drawers (with border and shadow) |
| `--color-bg-sunken` | `#090C10` | `#EBEEF2` | Code and JSON blocks, inset areas |
| `--color-bg-hover` | `#1E252E` | `#F0F3F6` | Hover wash on rows and menu items |
| `--color-bg-selected` | `#14233A` | `#E3EDFB` | Selected row and active navigation item |
| `--color-border-subtle` | `#232B35` | `#E3E7EC` | Internal dividers, table row lines |
| `--color-border-default` | `#323C49` | `#CBD2DA` | Panel and popover edges |
| `--color-border-strong` | `#6B7684` | `#7A8695` | Input and control boundaries (3:1 non-text contrast) |
| `--color-text-primary` | `#E6EAF0` | `#0F1720` | Body, headings, values |
| `--color-text-secondary` | `#AAB4C2` | `#435061` | Supporting text, labels |
| `--color-text-tertiary` | `#8591A1` | `#596677` | Hints, axis labels, timestamps |
| `--color-text-disabled` | `#5C6776` | `#98A2AF` | Disabled controls only (exempt from contrast) |
| `--color-link` | `#6AAEFF` | `#1553B8` | Links in text |
| `--color-accent` | `#5AA2FF` | `#1A5FD0` | Primary action fill, selection marks |
| `--color-accent-hover` | `#78B4FF` | `#1553B8` | Primary action hover |
| `--color-accent-active` | `#3F8CF0` | `#104596` | Primary action pressed |
| `--color-on-accent` | `#07111F` | `#FFFFFF` | Text and icons on the accent fill |
| `--color-accent-subtle` | `#12263F` | `#E6EEFC` | Quiet accent backgrounds |
| `--color-focus-ring` | `#7DB6FF` | `#1A5FD0` | Focus ring (2 px, offset 2 px) |

**Status tokens.** Each status has a fixed `mark` (icons, chart marks, dots; identical in both themes, except info which follows the accent) and themed `text` and `bg` that meet 4.5:1 for text.

| Status | Mark | Text dark | Bg dark | Text light | Bg light | Means |
|---|---|---|---|---|---|---|
| Approve (good) | `#0CA30C` | `#5FD487` | `#0F2A1A` | `#0B6B1F` | `#E3F5E7` | Approve decision, fresh, healthy |
| Review (warning) | `#FAB219` | `#F6C65B` | `#2E2410` | `#7A4B00` | `#FFF2D1` | Review decision, lagging, pending approval |
| Decline (critical) | `#D03B3B` | `#FF8F8A` | `#331519` | `#A82525` | `#FDE8E8` | Decline decision, invalid, failed |
| Degraded (serious) | `#EC835A` | `#F4A585` | `#331C12` | `#9A3F10` | `#FDEBE3` | Degraded decision or dependency, stale |
| Info | accent | `#8CBFFF` | `#10243F` | `#1553B8` | `#E6EEFC` | Neutral information, shadow, demo |
| Neutral | none | `#AAB4C2` | `#1E252E` | `#435061` | `#EBEEF2` | Retired, closed, unknown |

| ID | Rule |
|---|---|
| UX-19 | A status is always shown with an icon and a text label, never color alone. Status colors are reserved: a chart series that is only "series 4" never wears a status color, and a series that means good or bad always does (never both in one chart) |
| UX-20 | Status text sits on its own `bg` tone or on a surface, never on another status's background. Status backgrounds are tints for badges and banners, not for large areas |
### 7.3 Contrast verification

Computed by script (WCAG 2.x relative-luminance ratio) from the values in 7.2. Thresholds: text 4.5:1; control boundaries, focus indicators and graphical marks 3:1. `tools/ci/check_contrast.py` recomputes every row from `tokens.css` and fails the build below threshold.

| Pair | Dark | Light | Needs |
|---|---|---|---|
| Primary text on canvas, surface, raised, sunken, hover, selected | 12.79 to 16.23 | 15.27 to 18.05 | 4.5 |
| Secondary text on the same six | 7.37 to 9.35 | 6.95 to 8.21 | 4.5 |
| Tertiary text on the same six | 4.83 to 6.12 | 4.95 to 5.85 | 4.5 |
| Link on canvas, surface, raised, selected | 6.84 to 8.28 | 6.00 to 7.09 | 4.5 |
| On-accent text on accent, hover, pressed | 7.26, 8.81, 5.61 | 5.85, 7.09, 9.08 | 4.5 |
| Status text on its own bg: approve, review, decline, degraded, info, neutral | 8.24, 9.55, 7.57, 8.03, 8.18, 7.37 | 5.89, 6.66, 6.05, 5.88, 6.08, 7.05 | 4.5 |
| Status text on canvas, surface, raised (lowest) | 7.45 | 6.13 | 4.5 |
| Strong border on canvas, surface, raised | 4.14, 3.90, 3.55 | 3.39, 3.70, 3.70 | 3.0 |
| Focus ring on canvas, surface, raised | 9.10, 8.58, 7.81 | 5.35, 5.85, 5.85 | 3.0 |
| Accent fill on surface | 6.90 | 5.85 | 3.0 |
| Status marks on surface: approve, review, decline, degraded, info | 5.37, 9.82, 3.75, 6.83, 6.90 | 3.35, **1.83**, 4.80, **2.64**, 5.85 | 3.0 |

The two light-theme marks in bold (review amber, degraded orange) are below 3:1 by design. They never appear without an icon and a text label (UX-19), and chart series that use them carry direct labels and a table view (UX-27). Disabled text and decorative dividers (`border-subtle`, `border-default`) are exempt. Passing contrast is necessary, not proof of accessibility (section 15).

### 7.4 Typography

**Families.** IBM Plex Sans (400, 500, 600) for the interface and IBM Plex Mono (400, 500) for identifiers, hashes, JSON and code. Self-hosted WOFF2, Latin subset, `font-display: swap`, the two critical weights preloaded, and metric-adjusted fallbacks (`system-ui` and `ui-monospace`) so late font loading does not shift layout. No runtime font requests to third parties. Package names are verified at scaffold (CS-X-01).

| Style | Size / line | Weight | Use |
|---|---|---|---|
| `caption` | 12 / 16 | 400 (badges 500) | Timestamps, axis ticks, helper text, badges |
| `body-sm` | 13 / 20 | 400 | Table cells, dense lists |
| `body` | 14 / 20 | 400 | Default text |
| `label` | 13 / 16 | 500 | Form labels, buttons, tabs, navigation items |
| `title-sm` | 14 / 20 | 600 | Panel titles |
| `title-md` | 16 / 24 | 600 | Section and dialog titles |
| `title-lg` | 20 / 28 | 600 | Page title (`h1`) |
| `figure` | 24 / 28 | 500 | Stat-tile value, proportional figures |
| `code` | 13 / 20 | Mono 400 | JSON and code blocks |
| `code-sm` | 12 / 16 | Mono 400 | Identifiers and hashes in tables |

| ID | Rule |
|---|---|
| UX-21 | No text below 12 px. Prose lines stay under 80 characters (72 in documentation). Tabular figures (`font-variant-numeric: tabular-nums`) only in table columns and axis ticks, never on stat-tile values. Monospace is for identifiers, code and aligned values, never a decorative label style. Truncation is single-line with the full text in a tooltip. Letter-spacing is 0 except in the wordmark |

### 7.5 Spacing and density

Base unit 4 px. Layout dimensions prefer multiples of 8.

| Token | px | Use |
|---|---|---|
| `--space-0-5` | 2 | Hairline gaps, chart surface gaps |
| `--space-1` | 4 | Icon-to-text gap in badges |
| `--space-2` | 8 | Between related controls |
| `--space-3` | 12 | Compact panel padding |
| `--space-4` | 16 | Default panel padding, grid gutter, gap between panels |
| `--space-6` | 24 | Page padding, gap between page sections |
| `--space-8` | 32 | Reading-page section gap |
| `--space-12` | 48 | Empty-state vertical padding |
| `--space-16` | 64 | Maximum |

| Property | Default | Compact |
|---|---|---|
| Table row height | 36 | 28 |
| Control height (button, input, select) | 32 | 28 |
| Navigation item height | 32 | 28 |
| Panel padding and gap | 16 | 12 |
| Large control (onboarding and primary calls to action) | 40 | 40 |

**UX-22.** Spacing comes only from the scale. Every pointer target is at least 24 by 24 px (WCAG 2.2, 2.5.8) and icon buttons have a hit area of at least 28 px. Density is a per-viewer setting (account page and command palette), default "Default", persisted in the viewer's browser with a safe fallback when storage is unavailable.

### 7.6 Radius, borders, elevation, layers

| Token | Value | Use |
|---|---|---|
| `--radius-sm` | 2 px | Badges, chips, tags |
| `--radius-md` | 4 px | Buttons, inputs, selects, tabs, menu items |
| `--radius-lg` | 6 px | Panels, popovers, toasts, tooltips, dialogs up to 560 px |
| `--radius-xl` | 8 px | Dialogs wider than 560 px |
| `--radius-full` | 9999 px | Status dots, avatars, switch tracks only |

**UX-23.** A nested element's radius never exceeds its parent's. No radius above 8 px except `--radius-full`.

**Borders.** 1 px everywhere. Panels use `--color-border-default`, internal dividers and table row lines `--color-border-subtle`, input and control boundaries `--color-border-strong`. Focus is a 2 px `--color-focus-ring` outline with a 2 px offset on `:focus-visible`. A 2 px accent bar marks selection on the inline start.

| Level | Used by | Treatment |
|---|---|---|
| 0 | Canvas | None |
| 1 | Panels, tables, sidebar | `--color-bg-surface`, 1 px default border, no shadow |
| 2 | Menus, popovers, tooltips, toasts | `--color-bg-raised`, default border, shadow `0 4px 12px` at 40% black (dark) or 12% ink (light) |
| 3 | Dialogs, drawers | Same surface, shadow `0 16px 40px` at 55% black (dark) or 18% ink (light), scrim at 64% near-black (dark) or 40% ink (light) |

Z-index scale: sticky 10, top bar 40, popover 50, dialog and drawer 60, toast 70, tooltip 80. Components never invent other values.

### 7.7 Motion

| Token | Value |
|---|---|
| `--duration-fast` | 100 ms (hover, focus, menu fade) |
| `--duration-base` | 150 ms (dialog and popover entry) |
| `--duration-slow` | 250 ms (drawer slide) |
| `--ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` |
| `--ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` |

**UX-24.** Motion answers a user action or explains a state change; there are no entrance animations on page load and no shimmer on skeletons. Dialogs fade and move 4 px; drawers slide; chart animation is off except tooltip movement. Under `prefers-reduced-motion: reduce` all transforms are removed and transitions are opacity-only at 100 ms or less. Nothing animates for longer than 5 seconds without a pause control.

### 7.8 Icons

Lucide through `lucide-react`, at 14 px (badges), 16 px (controls and tables), 20 px (navigation) and 24 px (empty states), stroke width 1.75, `currentColor`. Icons are imported only through one re-export file, `components/ui/icons.ts`, which is the allow-list and keeps the bundle small. Decorative icons are `aria-hidden`; an icon-only button has an accessible name and a tooltip. No emoji as icons. **UX-25.**

### 7.9 Breakpoints

| Name | Min width | Layout |
|---|---|---|
| `sm` | 640 | Single column, stacked-row lists |
| `md` | 768 | Icon rail sidebar (56 px), page padding 24 |
| `lg` | 1024 | Expanded sidebar (232 px), full tables |
| `xl` | 1280 | Wider split layouts, 720 px drawers |
| `2xl` | 1536 | Same layout with wider content; reading pages stay capped |

Below 768 px the sidebar becomes a navigation sheet opened from the top bar. Behavior per page is in section 13.

## 8. Data visualization

### 8.1 Library and wrapper

Apache ECharts through one wrapper in `components/charts/`. SVG renderer, animation off, theme colors read from the CSS tokens at render time and re-applied when the theme changes. No second charting library. Every chart is a `figure` with a caption naming the question it answers, and a "View as table" toggle that shows the same data as an accessible table (UX-27).

### 8.2 Choosing the form

| Data job in VERDICT | Form | Color job |
|---|---|---|
| Decisions over time by outcome | Stacked columns, 2 px surface gaps | Status (Approve, Review, Decline) |
| Latency p50, p95, p99 over time | Lines on one axis, with a solid labelled budget line | Categorical slots 1 to 3 |
| Feature freshness by status | Stacked columns | Status, neutral for "empty, fresh" |
| Score distribution with thresholds | Histogram, one hue, threshold lines labelled | Slot 1, status for zones |
| PR curve, calibration, ROC for model versions | Lines, at most 3 series | Entity colors (8.3) |
| Confusion matrix, replay transitions | Heatmap with counts in cells | Sequential blue |
| Per-feature drift | Small multiples, one series each | Slot 1 |
| Pipeline lag per partition | Meter list (bar, name and figure per row) | Meter ramp |
| Case age, top reason codes | Ranked horizontal bars, one hue | Slot 1 |
| One current value | Stat tile (never a one-bar chart) | None |

A donut or pie is not used. Dual-axis charts are not allowed: two measures of different scale become two charts. **UX-26.**

### 8.3 Color rules

**Categorical palette** (fixed order, never cycled; a ninth series folds into "Other", is faceted, or uses a second encoding):

| Slot | Hue | Light | Dark |
|---|---|---|---|
| 1 | Blue | `#2A78D6` | `#3987E5` |
| 2 | Orange | `#EB6834` | `#D95926` |
| 3 | Aqua | `#1BAF7A` | `#199E70` |
| 4 | Yellow | `#EDA100` | `#C98500` |
| 5 | Magenta | `#E87BA4` | `#D55181` |
| 6 | Green | `#008300` | `#008300` |
| 7 | Violet | `#6250D6` | `#9085E9` |
| 8 | Red | `#E34948` | `#E66767` |

**Entity colors (UX-26).** Color follows the entity, never its rank, so filtering never repaints survivors. Champion model is slot 1, the challenger in shadow is slot 2, the baseline is slot 3, everywhere (Model Centre, Overview, Replay Studio). Latency percentiles are slots 1, 2, 3 in order. Series that mean good or bad use status tokens, never slots.

**Sequential** (magnitude): one hue, blue ramp. Light theme runs step 100 (`#CDE2FB`) to 700 (`#0D366B`) through 150 `#B7D3F6`, 200 `#9EC5F4`, 250 `#86B6EF`, 300 `#6DA7EC`, 350 `#5598E7`, 400 `#3987E5`, 450 `#2A78D6`, 500 `#256ABF`, 550 `#1C5CAB`, 600 `#184F95`, 650 `#104281`. In the dark theme the anchor flips: near zero is the dark end so it recedes into the surface, and the maximum is the light end (about step 250). Ordinal ramps (discrete ordered marks) start no lighter than step 250 on light and no darker than step 600 on dark.

**Diverging** (signed deltas): blue and red arms with equal steps and a neutral midpoint (`#EBEEF2` light, `#2A323C` dark). Blue steps 250, 400, 600; red steps `#EA9A93`, `#D75853`, `#892B2A`, derived by script to the same perceptual lightness as the blue steps.

**Chart chrome.** Grid `#E7EAEE` light, `#1F2730` dark; axis line `#CBD2DA` light, `#323C49` dark; axis and tick text `--color-text-tertiary` (5.85:1 light, 5.63:1 dark); series labels and legends in `--color-text-secondary`. Text never wears a series color; a colored dot or key beside it carries identity.
### 8.4 Palette validation (measured)

The categorical palette was validated by script on VERDICT's own chart surfaces (light `#FFFFFF`, dark `#12171D`). Distances are Euclidean in OKLab ×100 with protanopia and deuteranopia simulated (target at least 8, floor 6, legal only with a second encoding), plus a normal-vision floor of 15. Tritanopia figures are reported, not gated.

| Check | Light | Dark |
|---|---|---|
| Lightness band (OKLCH L) | Pass, all 8 in 0.43 to 0.77 | Pass, all 8 in 0.48 to 0.67 |
| Chroma floor (C at least 0.10) | Pass | Pass |
| Colour-blind separation, adjacent pairs | Pass, worst 9.1 (yellow and aqua); tritan 5.8 | Pass, worst 8.4 (yellow and aqua); tritan 8.7 |
| Normal-vision floor, adjacent pairs | Pass, worst 19.6 | Pass, worst 19.3 |
| Contrast against the surface (3:1) | **Warn:** aqua 2.82, yellow 2.17, magenta 2.69 | Pass, all 8 |
| All-pairs check, first three slots | Pass: worst colour-blind 9.2, normal 24.0 | Pass: worst colour-blind 9.4, normal 20.9 |

Consequences: forms where any two marks can touch (scatter, categorical heatmap, small multiples) carry at most three series; with four series in adjacent forms (stacks, bars, lines) direct labels are mandatory because yellow sits beside orange; the three light-theme warnings need visible labels or the table view. The check validates colour separation only. It is not proof for every viewer or a layout check, so every chart still gets an eyes-on review (section 19).

### 8.5 Marks and anatomy

| Mark | Specification |
|---|---|
| Bar or column | At most 24 px thick, 4 px rounded data end, square at the baseline, growing from one baseline |
| Touching marks | A 2 px gap in the surface color between stacked segments and adjacent bars. No stroke around marks |
| Line | 2 px, round joins and caps |
| Marker | At least 8 px, filled with the series color, with a 2 px ring in the surface color |
| Area | The series hue at about 10% opacity, never a saturated block |
| Grid and axes | 1 px solid hairlines, recessive, never dashed. A budget or threshold line is 1 px solid in `--color-text-secondary` with a direct label such as "Budget 300 ms" |
| Container | At least 16 px of padding around the plot. The container height includes the x-axis band so there is no nested scroll |

**Legend and labels.** Two or more series always have a legend; a single series has none (the caption names it). Direct labels are selective: the endpoint, the extreme, or the series the story is about, never a number on every point. A label goes inside a mark only if it fits with padding; otherwise it goes outside the end or into the tooltip and table view, never clipped. When end labels collide, use leader lines or small multiples. Axis ticks are round numbers, written in full under 10,000 and compact above (10K), one style per axis.

### 8.6 Interaction

- **Line and area charts** have a vertical hairline that snaps to the nearest X and one tooltip listing every series at that X. **Bars and cells** carry a per-mark tooltip and the hovered mark lightens.
- In a tooltip the value leads (primary text, strong) and the series name follows (secondary). Series are keyed by a short line, not a box.
- Hover and focus areas include the surface gap and are at least 24 px; dense scatter uses a nearest-point layer.
- Filters sit in one row above everything they scope. The time range comes first with presets (last 15 minutes, last hour, last 24 hours, last 7 days) listed as rows with a check on the selection and a custom range behind a divider. Every chart, tile and table below re-renders against the same slice.
- While data refetches, charts keep their previous render at 60% opacity with `aria-busy`. There is no skeleton flash and no layout jump.
- Live views poll with TanStack Query (Overview every 15 seconds, a running simulation every 2 seconds), pause when the tab is hidden, and show "Updated 12 seconds ago" with a refresh button. There are no WebSockets in V1.0.

### 8.7 Figures

- **Stat tile.** A label (sentence case, no colon), a value in the `figure` style with proportional figures, an optional delta (signed, against a named period, using status text color by direction and whether up is good, always with the sign and an icon) and an optional 12-point sparkline in neutral with the current period in the accent. Overview does not lead with one giant hero number.
- **Meter.** The fill carries severity (accent, then warning, then critical). The unfilled track is a lighter step of the same ramp. A **meter list** (name, aligned bar, figure per row) shows pipeline lag per partition against its limit.
- **Segmented bar.** One whole split into at most six parts. In tables and beside a list of figures use the thin form (8 px, 4 px when dense, fully rounded, no text). The outcome split on Overview uses the thin form beside its figures.

### 8.8 Dashboard density

At 1440 by 900 the Overview shows the posture panel, decisions by outcome, latency, pipeline health, recent decisions (8 rows) and pending cases (5 rows) without scrolling. A chart panel is at least 360 by 200 px. There is at most one row of stat tiles (five tiles maximum). Every panel title states its question and window ("Decisions by outcome, last 24 hours").

| ID | Rule |
|---|---|
| UX-26 | **Form and color.** No pie or donut. No dual axis. At most eight series, in fixed slot order, never cycled. Color follows the entity, never its rank. Status tokens only when the color means good or bad, categorical slots otherwise, never both in one chart. Series that mean good or bad always use status tokens |
| UX-27 | **Redundancy.** Every chart has a "View as table" twin with the same data. A tooltip never gates a value: every value is reachable through direct labels or the table, and the tooltip also appears on keyboard focus where marks are focusable. A color in the 8.4 warning list always has visible labels or the table view. An accessibility setting, print and `forced-colors` switch charts to 45° and 135° line patterns (ECharts decal patterns, verified at scaffold). Patterns are never on by default |
| UX-28 | **Marks** follow 8.5 exactly. Chart code contains no literal colors outside the token mapping |
| UX-29 | **Interaction** follows 8.6. Filters are never inside a chart card. Refetch never shows a skeleton over an existing chart |
| UX-30 | **Safe strings.** Tooltip and label formatters never build HTML from API strings. Every interpolated string passes through the wrapper's escape helper, which a test exercises with an HTML payload (CS-T-14) |

## 9. Components

Each component has a Storybook story for every state it has: default, hover, focus-visible, active, selected, disabled, loading, error, empty, in light and dark (CS-T-18).

### 9.1 Buttons

| Variant | Appearance | Use |
|---|---|---|
| Primary | `--color-accent` fill, `--color-on-accent` text, `label` style | The one main action in a region |
| Secondary | Surface fill, `--color-border-strong` border, primary text | Other actions |
| Tertiary | No border, primary text, hover wash | Low-emphasis and toolbar actions |
| Danger | Fill `#D03B3B`, white text (4.8:1), hover `#B83232` (5.93:1) | Confirm button of a destructive dialog only |

Sizes: small 28, medium 32, large 40 px high; an icon-only button is square at the same size. **Loading** replaces the icon with a spinner, keeps the label and width, and sets `aria-busy`. **Disabled** uses `aria-disabled="true"` and a visible reason next to the control (UX-13). One primary button per region. Buttons never wrap their label.

### 9.2 Inputs and selects

32 px high (28 compact), `--radius-md`, 1 px `--color-border-strong`. Hover darkens the border to `--color-text-tertiary`; focus shows the accent border and the 2 px ring; invalid shows a `--status-decline-mark` border, an icon and a message below; read-only uses `--color-bg-sunken`. Placeholders use tertiary text and never replace a label. Numeric inputs right-align. Identifiers and hashes use the monospace face.

Use Radix Select for lists up to 15 items. Use a combobox (popover plus listbox, type-ahead) for longer lists, and a combobox with removable chips for multi-select. The date-time range control follows 8.6 and always labels the time zone.

### 9.3 Forms

React Hook Form with Zod resolvers (CS-T-11). Single column, label above the field (`label` style), helper text below (`caption`, secondary), error below (icon, text, linked by `aria-describedby`). Related fields sit in a `fieldset` with a `legend`.

| ID | Rule |
|---|---|
| UX-31 | Fields are required by default; optional ones say "(optional)" after the label. Validation runs on blur first and on change after the first error. The submit button stays enabled; submitting validates everything, focuses the first invalid field and, for forms with more than five fields, shows an error summary whose items focus their fields |
| UX-32 | Server errors map from the stable error `code` to the field or to a form-level message, never from message text. A double submit is prevented while a request is in flight. Unsaved changes prompt before navigation. Success names what changed ("Policy version 7 saved as draft") |
| UX-33 | Use autocomplete attributes where they apply. Pasting is always allowed, including into code fields and one-time-code fields |

### 9.4 Tabs

Radix Tabs for views of the same object (Decision detail: Summary, Evidence, Timeline, Outcome). At most six tabs, labels of one or two words in sentence case, the active tab in the URL (`?tab=`). A count appears on a tab only when it is real data. Left and right arrows move between tabs.

### 9.5 Badges and chips

| Badge | Appearance |
|---|---|
| Status | 14 px icon plus label (`caption`, weight 500) on the status `bg`, `--radius-sm`, 20 px high |
| Decision (detail page) | Same, 24 px high with the `body-sm` label |
| Mode, demo data | Outline badge per 6.5 |
| Degraded | Degraded-status badge shown beside a decision's outcome badge, with the reason in its tooltip and in the detail page |
| Filter chip | Removable, with a button named "Remove filter: field value" |

Decision outcome icons by shape, so they differ without color: Approve is a check in a circle, Review is a triangle with an exclamation mark, Decline is an x in a circle (Lucide concepts; exact names are verified at scaffold). Freshness labels are Fresh, Lagging, Stale, Empty (fresh) and Invalid, mapped to approve, review, degraded, neutral and decline.

**UX-34.** API status values map to display categories (good, warning, critical, degraded, info, neutral) in one module, `lib/status.ts`, with an exhaustive `switch` over the generated enum types so a new API status breaks compilation until it is handled. Model lifecycle states map as: Champion is accent-solid, Shadow is info, Promotion requested is warning, Evaluated and Registered are neutral outline, Retired and Rolled back are neutral muted, Rejected is critical outline. Policy and case states follow the same categories from their API status values.
### 9.6 Tables and filters

Semantic `&lt;table&gt;` with a visually hidden `&lt;caption&gt;`, a sticky header (surface background, bottom border) and TanStack Table for state. Pages are cursor-paginated by the server.

| ID | Rule |
|---|---|
| UX-35 | **Structure.** The first column holds the row's primary link (identifier or name); it is the tabbable row action. Text left-aligned, numbers and amounts right-aligned with tabular figures, timestamps in UTC (`body-sm`, tabular), identifiers in `code-sm`. Single-line truncation with a tooltip that also opens on focus. Row hover uses `--color-bg-hover`, selection `--color-bg-selected` |
| UX-36 | **Sort and columns.** Sorting is server-side, one column at a time, with the header as a button carrying `aria-sort`. A column menu shows or hides columns, persisted per viewer per table with a safe fallback. No drag-to-resize or drag-to-reorder in V1.0; if added later it needs a keyboard alternative (WCAG 2.2, 2.5.7) |
| UX-37 | **Pagination.** Cursor-based "Previous" and "Next", page size 25, 50 or 100 (never above 100, CS-U-09), the visible range ("1 to 50"), and a total only when the API returns one |
| UX-38 | **Virtualization.** Above 200 rendered rows (timelines, replay results, audit lists held client-side) rows are virtualized with TanStack Virtual and `aria-rowcount` and `aria-rowindex` keep screen-reader context. Shorter lists are not virtualized |
| UX-39 | **Row actions.** In Decision Explorer, clicking a row opens the peek drawer (`?peek=`); the identifier link or Ctrl/Cmd+click opens the detail page. With shortcuts enabled, `j` and `k` move focus between row links, `Enter` opens the detail page and `Space` toggles the peek. A checkbox column and a sticky bulk-action bar appear only where a bulk API exists |
| UX-40 | **Filters.** A single row above the table with a filter builder (field, operator, value) producing removable chips, a time range first, and "Clear filters". Fields and operators come only from the list endpoint's OpenAPI parameters; the UI never offers a filter the API cannot serve. Saved views and export are Extended scope: the URL is the saved view until then |
| UX-41 | **States inside a table** keep the header and column layout. Loading shows eight skeleton rows. Empty and no-results states follow section 10 |

### 9.7 Dialogs, confirmations and one-time secrets

Radix Dialog and AlertDialog. Widths 400 (confirm), 560 (form), 720 (rare). Title in `title-md`, footer buttons right-aligned with the primary last. Escape closes unless a request is in flight. Focus returns to the trigger. Clicking the scrim closes only non-destructive dialogs.

| Level | When | Pattern |
|---|---|---|
| None | Reversible, low consequence (hiding a column) | Immediate, with an Undo toast only where the API supports undo |
| Confirm | Irreversible, or governance action outside `LIVE` | Dialog stating the consequence, a verb button, initial focus on Cancel when destructive |
| Typed confirm | Governance or destructive action in `LIVE` | The dialog also asks for the environment name; the button enables on an exact match (UX-17) |
| Maker and checker | Policy activation, model promotion | Request dialog with a required reason, then the object shows "Promotion requested" with requester and time. A different approver approves or rejects, with a reason. The requester sees the approve button disabled with the visible reason "You requested this change" (invariant 9) |

| ID | Rule |
|---|---|
| UX-42 | A dialog title names the action and object ("Revoke credential vk_live_4f9a…"). The body states what will happen and what cannot be undone. The confirm button repeats the verb |
| UX-43 | **Copy-once credentials.** After creation, a dialog shows the full credential once in `code`, with a "Copy credential" button (polite confirmation) and a checkbox "I have stored this credential". Close enables after copy or the checkbox. The secret is never shown again; lists show the prefix and bullets (`vk_staging_k123_••••••••`). The field is excluded from autofill and from client logging and telemetry |

### 9.8 Drawers, tooltips, popovers

- **Drawers** are modal Radix Dialog panels from the right (480 px, 720 px wide variant) with a title, a close button, a scrolling body and a sticky footer for actions. They show detail without leaving a list (peek, quick create). They are never used for navigation. The URL reflects open peeks. **UX-44.**
- **Tooltips** (Radix Tooltip) appear after 400 ms and on keyboard focus, hold at most two lines, are dismissible with Escape, stay open while hovered or focused (WCAG 1.4.13), and never hold essential information or controls. **UX-45.**
- **Popovers and menus** hold interactive content (selectors, menus, filter editors).

### 9.9 Notifications

| Kind | Use | Behavior |
|---|---|---|
| Toast, success and info | Confirms a completed user action after the server confirmed it | `role="status"`, polite, 5 s (info 8 s), pauses on hover and focus, one optional action link such as "View audit record", close button |
| Toast, error | Failure of a background or non-form action | `role="alert"`, stays until dismissed. Errors from forms and dialogs appear inline, not as toasts |
| Banner | Persistent system condition: degraded platform, stale data, demo environment, session | In the banner slot, stacked; degradation cannot be dismissed |

At most three toasts are visible and duplicates are merged by key. A success toast never appears before the server confirms (no fake success). **UX-46.**

### 9.10 Timelines, code and JSON

- **Latency breakdown** (Decision detail) shows each pipeline stage as a horizontal bar on one shared time axis with its duration and the budget; stage names and values also appear as text.
- **Event timeline** (cases, audit) is a vertical list: status dot with icon, title, detail, actor and UTC time. Items link to the object they describe. Virtualized above 200 items.
- **JSON viewer** is an in-house collapsible tree on `--color-bg-sunken`, in `code`, horizontal scroll with no wrapping, a "Copy JSON" button with a polite confirmation, long values truncated with "Show all". Syntax roles: keys secondary text, strings primary text, numbers `--color-link`, booleans and null tertiary text. Controls are buttons with `aria-expanded`. **UX-47.** No code-editor dependency in V1.0: JSON is viewed here and edited through structured forms; raw JSON paste is a monospace textarea validated before save. If editing proves inadequate, evaluate CodeMirror 6 through an ADR.
- **Code examples** (quickstart) use the same style with language tabs and a copy button. Payloads and request samples are generated from the examples in `contracts/openapi/`, never hand-typed (UX-01).

### 9.11 The Verdict strip

The identity's signature element: where a score sits against the decision thresholds, and what actually decided.

| Part | Specification |
|---|---|
| Track | 8 px high (6 px compact), full width of its container, at least 160 px. Three zones left to right: Approve, Review, Decline, filled with the status marks and separated by 2 px surface gaps; outer ends rounded 4 px |
| Score marker | 2 px wide, 16 px tall tick in `--color-text-primary` with a 2 px surface halo, the score value above it in `code-sm` |
| Thresholds | The two boundary values below the track in `caption`, tertiary text |
| Decided-by line | Below the strip: "Decided by Decline rule R-114", "Decided by Review rule R-203", "Decided by model thresholds: Review" or "Default: Approve". When a rule decided, the strip is shown at 60% opacity with the note "Score shown for reference" |
| Accessible name | `role="img"` and an `aria-label` such as "Risk score 0.62, in the Review zone from 0.35 to 0.80, decided by model thresholds: Review". The same values appear as text beside it, so the strip is never the only source |
| Editable form (Policy Studio) | Two-thumb Radix Slider with arrow-key steps and two numeric inputs beside it as the non-drag alternative (WCAG 2.2, 2.5.7) |

**UX-48.** Rule IDs shown here follow whatever identifiers the policy API returns; the strip's order and decided-by wording follow the VPL precedence: Decline rule, then Review rule, then model thresholds, then default Approve.

## 10. States

```mermaid
flowchart TD
    start["View mounts"] --&gt; sess{"Session valid?"}
    sess --&gt;|"401"| expired["Session expired: sign in, return to the same URL"]
    sess --&gt;|"yes"| fetch["Fetch, using cached data if present"]
    fetch --&gt; cached{"Cached data on screen?"}
    cached --&gt;|"no"| loading["Loading: skeleton in the final layout"]
    cached --&gt;|"yes"| refetch["Hold previous render at reduced opacity"]
    loading --&gt; result{"Response"}
    refetch --&gt; result
    result --&gt;|"403"| forbidden["Forbidden: name the permission"]
    result --&gt;|"error"| error["Error: retry and reference id"]
    result --&gt;|"ok, no rows, no filters"| empty["Empty: first-use guidance"]
    result --&gt;|"ok, no rows, filters set"| noresults["No results: clear filters"]
    result --&gt;|"ok, rows"| ready["Ready"]
    ready --&gt; age{"Older than stale threshold, or refetch failed?"}
    age --&gt;|"yes"| stale["Stale banner with last updated time"]
    age --&gt;|"no"| current["Current"]
```

| State | Presentation | Copy pattern |
|---|---|---|
| Initial and loading | Static skeleton in the final layout (no shimmer, no spinner-only), `aria-busy="true"` on the region | none |
| Refetching | Previous render at 60% opacity, no skeleton | none |
| Empty (first use) | Area title, one sentence on what the area shows, one primary action | "No decisions yet. Send a test decision from the Developer Portal." |
| No results | The table frame stays; message and "Clear filters" | "No decisions match these filters." |
| Error | Inline panel with a reason when known, "Try again", and the reference identifier (copyable) | "Decisions did not load. The service returned an error. Try again; if it continues, quote reference 9f2c4a1e." |
| Unauthorized (401) | Handled once by the shell: full-page "session expired" with "Sign in", returns to the same URL | "Your session has ended. Sign in to continue." |
| Forbidden (403) | Panel naming the missing permission and who can grant it | "You can't activate policies in this environment. Required permission: policy activation. Ask an administrator of your organization." |
| Not found (404, and any resource outside the viewer's organization) | Full-page state with a link to the area list | "This decision doesn't exist or you can't see it." |
| Stale | Banner with the last successful time and "Refresh". Stale means older than twice the polling interval, or a failed refetch | "Showing data from 14:02:15 UTC. The last refresh failed." |
| Offline or degraded | Global banner. Offline from failed requests and the browser's online state; degradation only from signals the API returns | "You're offline. Changes can't be saved." / "Decision service degraded: decisions use fallback rules." |
| Render failure | A route-level error boundary: reload button and reference | "This page failed to display." |

| ID | Rule |
|---|---|
| UX-49 | Every data view implements loading, empty, no results, error, forbidden and stale (CS-T-12); 401 and offline are handled by the shell |
| UX-50 | A cross-organization identifier always shows the 404 state, never 403, so existence is not revealed |
| UX-51 | Skeletons, empty states and errors reuse the real layout so nothing jumps when data arrives |
## 11. Page layouts

### 11.1 Layout rules

| Page type | Structure | Scrolling |
|---|---|---|
| Dashboard | 12-column grid of titled panels, 16 px gutters and gaps | The page scrolls as a whole |
| List | Filter row, table toolbar, table, pagination | The page scrolls; the table header sticks under the top bar |
| Detail | Page header, tabs, a main column (cols 1 to 8) and a facts column (cols 9 to 12) | The page scrolls |
| Workbench | Master-detail split: list (360 px) and detail (flexible) | Each side scrolls independently; height is the viewport minus the top bar and page header |
| Editor | Rule list (280 px), editor (flexible), side panel (360 px) | Regions scroll independently; the action footer is sticky |
| Reading | Content capped at 1120 px, prose at 72 characters | The page scrolls |

Every view has one primary scroll area, one `h1`, and a skip target on `main`. Panels are `--color-bg-surface` with a 1 px default border and `--radius-lg`. The shell dimensions are in 6.4.

### 11.2 Overview (Dashboard)

| Region | Specification |
|---|---|
| Filter row | Time range (default last 24 hours), refresh button, "Updated 12 seconds ago" |
| Checklist | While the environment is new, the onboarding checklist panel (section 12) sits above everything; dismissible after the first decision |
| Decision posture, cols 1 to 4 | What is deciding right now: active policy version, champion model version (and shadow, if any), feature schema version, count of degraded decisions in the window. Each version is a link. Beneath it the thin segmented outcome split with its figures |
| Decisions by outcome, cols 5 to 12 | Stacked columns in the status colors with a legend |
| Latency, cols 1 to 6 | p50, p95, p99 lines with a labelled budget line |
| Pipeline health, cols 7 to 12 | Meter list: feature pipeline lag per stream partition, outbox oldest pending age, circuit breaker states, each against its limit, with the freshness status counts |
| Recent decisions, cols 1 to 7 | 8 rows: time, outcome badge, score, subject, latency; header links to Decision Explorer |
| Pending cases, cols 8 to 12 | 5 rows: case, age, assignee; header links to Cases |

Responsive: 1024 to 1279 px uses two columns (6 and 6) with the posture panel full width; below 1024 px a single column in the same order.

### 11.3 Decision Explorer (List)

| Region | Specification |
|---|---|
| Filter row | Time range, filter builder with chips, "Clear filters" |
| Toolbar | Result range, column menu |
| Table | Default columns: Time (UTC), Decision (outcome badge, plus Degraded badge), Score, Reasons (first two codes and a count), Subject (short identifier), Amount, Policy version, Model version, Latency (ms), Decision ID. Default sort: time, newest first. Page size 50 |
| Peek drawer, 480 px | Outcome and Verdict strip, top reasons, facts, link "Open decision" and "Replay this decision" |
| Below 640 px | Stacked rows: identifier, outcome badge, time, amount, score |

### 11.4 Decision detail (Detail)

| Region | Specification |
|---|---|
| Header | Breadcrumb "Decisions / 9f2c4a1e". Title "Decision 9f2c4a1e". Chips: outcome, Degraded when true, environment mode. Actions: Replay this decision, Open case (when one exists), Copy link |
| Summary tab | The Verdict strip with the decided-by line, the reasons list (code, plain-language text, signed contribution), the request summary |
| Evidence tab | Feature snapshot table with a freshness badge per feature; the policy rule evaluation trace (each rule, matched or not, the values compared); the model score with signed contributions as a diverging bar chart (positive pushes toward Decline); raw request and response in JSON viewers |
| Timeline tab | The latency breakdown by stage against the budget, then the event timeline |
| Outcome tab | Outcome labels and their delayed-label status, related audit events |
| Facts column, cols 9 to 12 | Full decision ID and event ID (copy), subject, amount, policy version and model version (links, with the model artifact hash shortened), feature schema version, degraded reason, decided time (UTC) |

### 11.5 Cases (Workbench)

| Region | Specification |
|---|---|
| Queue, 360 px | Filter chips (status, assignee, age), rows of two lines: case and subject, then score, age and assignee. `j` and `k` move through the queue |
| Case header | Case ID, status badge, assignee; actions: Assign to me, Assign to someone else, Resolve with an outcome label |
| Evidence panel | Decision summary with the Verdict strip, reasons, top features |
| Event timeline | Case events and resolution history |
| Notes | A composer and the list of analyst notes with author and UTC time |

Below 1024 px the queue and the case are separate screens with a back link; the case actions stay available.

### 11.6 Policy Studio (List, then Editor)

| Region | Specification |
|---|---|
| Policy sets list | Name, active version in this environment, last published, drafts. Row opens the set |
| Policy set page | Versions table with state chips (draft, published, active, superseded), actions: New draft from this version, Compare, Request activation (maker and checker, 9.7) |
| Editor header | Tabs: Rules, Thresholds, Tests, Dry run, History. State chip and version number |
| Rule list, 280 px | Rules grouped in precedence order: Decline rules, Review rules, Model thresholds, Default |
| Editor, flexible | A structured rule form: name, conditions (feature, operator, value), outcome, reason code, stale-feature and failure behavior. The Thresholds tab holds the editable Verdict strip |
| Side panel, 360 px | Validation messages that link to the failing field, test cases with pass and fail, and Dry run: choose a sample of recent events and see outcome counts against the active policy |
| Footer (sticky) | Save draft, Validate, Publish version (immutable). Published versions open read-only with "Create draft from this version" and a read-only JSON view |

### 11.7 Model Centre (List, then Detail)

| Region | Specification |
|---|---|
| Registry | Model, family, number of versions, champion and shadow in this environment |
| Version header | Lifecycle stepper (Trained to Registered to Evaluated to Shadow to Promotion requested to Champion), the current state chip, artifact hash (short, copy) |
| Evaluation tab | Metrics table with intervals: PR-AUC, recall at fixed false-positive rate, cost under the assumed cost matrix; PR curve, calibration plot, confusion matrix at the chosen threshold. A permanent banner: "Evaluated on public or synthetic data. This is not an estimate of real-world performance" |
| Shadow tab | Agreement with the champion by outcome, score distribution comparison, latency, count of compared decisions |
| Promotion tab | Request and approval controls per 9.7, with requester, approver and times |
| Lineage tab | Training run, dataset manifest hash, feature schema version, git revision |

### 11.8 Feature Platform (List with drawer)

| Region | Specification |
|---|---|
| Header strip | Feature schema version, pipeline lag meter list, freshness status counts |
| Features table | Name, window, schema version, freshness status, lag, last update |
| Detail drawer, 720 px | The definition from the canonical spec, the window rule, current statistics, freshness history chart. Drift appears as an indicator only, with that wording. Online and offline comparison is Extended scope |

### 11.9 Replay Studio (List, then Detail)

| Region | Specification |
|---|---|
| New replay | Select events (one decision, or a time range with filters and a bounded count), choose the alternative policy version and or model version, Run replay. A permanent line: "Replay runs in isolation and never changes live decisions." |
| Jobs table | Status, requester, event count, alternative, completed time |
| Job result | Counts (replayed, changed), the transition matrix heatmap (original to replay), the changed-decisions table. A row opens a 720 px comparison drawer with original and replay side by side: same feature snapshot, rule trace differences, score difference |

### 11.10 Simulation Lab (Workbench)

| Region | Specification |
|---|---|
| Configuration, 360 px | Scenario, arrival rate (bounded), duration, toggles for duplicate events, out-of-order events, delayed labels, model slowness or outage, feature pipeline lag. "Start run" is disabled with a visible reason in environments where simulation is not allowed |
| Live panel | Throughput, decisions by outcome, latency, error rate, duplicates handled and late events as small charts, polling every 2 seconds. Stop run button |
| Runs table | Past runs with scenario, status, start, duration, link to the run |

### 11.11 Developer Portal (Reading, plus credentials List)

| Region | Specification |
|---|---|
| Tabs | Quickstart, Playground, Schemas, Limits |
| Quickstart | Three steps (create a credential, send a decision, inspect it) with language tabs for curl, Java, Python and TypeScript. Samples come from `contracts/openapi/` examples |
| Playground | A structured request form and JSON view, the environment shown prominently, and the real response with its decision link. Authentication follows the playground endpoint in `architecture.md`; the UI never stores credentials (CS-T-13) |
| Schemas, Limits | Generated from the OpenAPI document, the event schema and the configured rate limits |
| Credentials page | Table: client, prefix, created, expires, last used, status. Actions: Create (copy once, 9.7), Rotate, Revoke (typed confirmation in `LIVE`) |

### 11.12 Audit Centre (List)

| Region | Specification |
|---|---|
| Filter row | Time range, actor, action type, object type, environment |
| Table | Time (UTC), actor, action, object, environment, record hash (short), chain position |
| Detail drawer, 720 px | The full record in a JSON viewer, previous hash and hash, a "Verify integrity" action when the API offers it, with the caption "The hash chain is tamper-evident, not tamper-proof" |
| Export | Extended scope |

### 11.13 Settings and account

Settings pages are Reading-type forms. Members (list, roles), Projects and environments (create, mode, rename), Security (session information, a link to the identity provider's account page for multi-factor setup), Organization (name). Invitations that need email show their dependency on the configured mail provider in the page, as the architecture notes. Account holds theme (Dark, Light, System), density, time zone, single-key shortcuts on or off, and chart patterns.
## 12. Onboarding

The flow itself is in `project-overview.md`. This section specifies the interface. A new user must reach a real decision without anyone explaining the product.

| Step | Where | Done when (server fact, never a local click) |
|---|---|---|
| 1. Create organization and project | `/welcome`, one form on first sign-in | The organization and project exist |
| 2. Create the environment | `/welcome`, demo mode preselected and labelled "Demo data" | The environment exists |
| 3. Create an API credential | Developers, Credentials (copy once, UX-43) | A credential exists |
| 4. Read the quickstart | Developers, Quickstart | Informational, no completion state |
| 5. Send a test decision | Developers, Playground | The environment has at least one decision |
| 6. Inspect the decision | Decision detail (link from the playground response) | Same as step 5 |
| 7. Start the simulator | Simulator | A simulation run exists |
| 8. Watch Overview update | Overview | The run has produced decisions |

- **Checklist panel.** On Overview of a new environment, a panel lists the steps with status, a one-line description and an action link, plus "3 of 6 done". It collapses when complete and can be reopened from Help, "Getting started".
- **Contextual help.** Technical terms (freshness, shadow, fail mode, threshold) carry an info button that opens a popover of at most two sentences and a documentation link. The help menu holds Getting started, Keyboard shortcuts, Developer Portal and "Report an issue".
- **Demo data.** The simulator runs from a recorded seed, shown on the run, so a demo can be repeated exactly. Everything it creates is labelled "Demo data" (UX-02).
- **Error guidance.** Errors during onboarding name the specific cause and fix, for example a credential rejected because it belongs to a different environment, and say which credential to use.

## 13. Responsive behavior

"Full" means every action works. "Read-only" means views, copy and navigation work, but editing and starting actions are replaced by a visible note: "Open on a larger screen to edit." (UX-13).

| Area | 1024 px and up | 768 to 1023 px | Below 768 px |
|---|---|---|---|
| Overview | Full | Full, two columns | Read-only, one column |
| Decisions | Full | Full | Stacked rows; detail read-only |
| Cases | Full | Queue and case on separate screens | Same, actions available |
| Policies, Models | Full | Read-only | Read-only lists |
| Features, Audit | Full | Full | Read-only |
| Replay | Full | Results only | Results only |
| Simulator | Full | Observe and stop | Observe and stop |
| Developers | Full | Full | Reading and credentials list; playground read-only |
| Settings | Full | Full | Full |

| ID | Rule |
|---|---|
| UX-52 | Layouts reflow to a 320 px viewport without two-dimensional scrolling, except data tables, code and JSON blocks and chart plots, which scroll inside their panel with a visible scroll cue. Tables from 640 to 1023 px keep a sticky first column. Nothing depends on hover: every tooltip also appears on focus and on tap. Layouts survive 200% zoom and text-spacing overrides (no fixed-height text containers). Orientation is never locked |

## 14. Keyboard

| Shortcut | Action |
|---|---|
| `Ctrl` or `Cmd` + `K` | Open the command palette (always on) |
| `?` | Show this list |
| `[` | Collapse or expand the sidebar |
| `g` then `o`, `d`, `c`, `p`, `m`, `f`, `r`, `s`, `v`, `a`, `,` | Go to Overview, Decisions, Cases, Policies, Models, Features, Replay, Simulator, Developers, Audit, Settings |
| `/` | Focus the filter or search field on a list |
| `j` and `k` | Move focus to the next or previous row or queue item |
| `Enter` and `Space` | Open the focused row; toggle its peek (UX-39) |
| `Esc` | Close the top dialog, drawer or popover |

| ID | Rule |
|---|---|
| UX-53 | Single-key shortcuts can be turned off in the account page (WCAG 2.1.4). They are inactive while focus is in a text field, select, editable region or dialog. Everything they do is also reachable with the pointer and Tab |
| UX-54 | On route change focus moves to the page `h1` (`tabindex="-1"`), `document.title` becomes "Decisions - Demo - VERDICT" and a polite live region announces the page. A dialog moves focus to its first field (to Cancel when destructive) and returns it to the trigger on close. Toasts never take focus. Tab order follows visual order, no positive `tabindex`, no keyboard traps, and a skip link is first |

## 15. Accessibility

WCAG 2.2 AA is the engineering target, as in the charter. No claim of conformance is made: automated checks cover only part of the criteria, so progress is recorded in `progress-tracker.md` as verified criteria, not as compliance.

| Criterion | How the console addresses it | Verified by |
|---|---|---|
| 1.4.1, 1.4.3, 1.4.11 Color, text and non-text contrast | Status always icon plus label; contrast table in 7.3; chart relief rules | `check_contrast.py`, axe, review |
| 1.4.10, 1.4.12 Reflow, text spacing | UX-52 | Playwright at 320 px, review |
| 1.4.13 Content on hover or focus | Tooltips dismissible, hoverable, persistent | Component tests |
| 2.1.1, 2.1.2, 2.1.4 Keyboard, no trap, character keys | Section 14, UX-53 | Playwright keyboard tests |
| 2.2.1 Timing | No session timer in the UI; expiry is handled by the 401 state (section 10) | End-to-end test |
| 2.4.1, 2.4.3, 2.4.7 Bypass blocks, focus order, focus visible | Skip link, UX-54, 2 px ring | axe, Playwright |
| 2.4.11 Focus not obscured | `scroll-padding-top` equals the sticky layers (6.4) | Playwright on long tables |
| 2.5.7 Dragging | No drag-only interaction; the editable strip has inputs and arrow keys | Review |
| 2.5.8 Target size | 24 by 24 px minimum (UX-22) | Component tests |
| 3.2.6 Consistent help | The help menu is in the same place on every page | Review |
| 3.3.1, 3.3.3, 3.3.7 Errors and redundant entry | UX-06, UX-31, UX-32; entered values are kept after failures | Component tests |
| 3.3.8 Accessible authentication | Sign-in is delegated to Keycloak; paste and password managers work | Review of the Keycloak theme |
| 4.1.2, 4.1.3 Name, role, value, status messages | Radix primitives, `role="status"` and `role="alert"` (9.9) | axe, component tests |

**Manual checks** before any UI milestone: a keyboard-only pass of its workflows, a screen-reader smoke test (NVDA with Firefox or Chrome, VoiceOver with Safari), 200% and 400% zoom, and forced-colors mode.

## 16. Theme decisions

- **Dark is the default.** The console is an operations tool read for long sessions, and dark matches developer-tool convention. Light is fully supported with its own validated values; "System" follows the OS. The setting lives in the account page.
- **No flash.** A small external blocking script, `theme-init.js` (under 1 KB, served from the same origin so a strict Content-Security-Policy holds), reads the stored theme and sets `data-theme` before first paint. Storage reads are wrapped in try and catch; if storage is unavailable the theme is dark.
- **`forced-colors: active`** uses system colors for borders, focus and selection, and charts switch to patterns. **`prefers-contrast: more`** raises `--color-border-default` to the strong border. **`prefers-reduced-motion`** follows UX-24.

## 17. Storybook, testing and visual regression

| Layer | Tooling | Scope |
|---|---|---|
| Stories | Storybook, with MSW handlers built from OpenAPI examples | One story file per component and per page composition; every state in light and dark; interaction `play` functions |
| Component and interaction tests | Vitest and Testing Library; stories executed as tests through Storybook's test integration (verified at scaffold) | Behavior, states, keyboard |
| Accessibility | axe in Storybook and Playwright | Every story and every route (CS-T-22) |
| End to end | Playwright against the Compose stack | Every P0 workflow in `project-overview.md`, with real Keycloak, including the two-person approval flows |
| Responsive | Playwright viewports 1440 by 900, 1024 by 768, 768 by 1024, 390 by 844 | Section 13 behavior |
| Visual regression | Playwright screenshots of stories (both themes) and of key pages at the four viewports | Layout, spacing, color, density |

| ID | Rule |
|---|---|
| UX-55 | Visual baselines live in `console/visual-baselines/` and are generated only by the CI Linux container through a manual "update visual baselines" workflow that commits to the PR branch, because font rendering differs across machines. Captures disable animations, wait for `document.fonts.ready`, use fixed MSW or seeded data, and mask volatile regions (timestamps, identifiers). Tolerance starts at Playwright's defaults and loosens only with a written reason. A baseline change needs a reviewer note (CS-T-26) |
| UX-56 | Review screenshots live in the PR or CI artifacts, not in Git, except the baselines (CS-U-19) |

## 18. Performance

Targets are starting hypotheses, replaced by measurements as soon as builds exist.

| Item | Starting target |
|---|---|
| Initial JavaScript (shell and Overview), gzipped | 300 KB |
| Any other route chunk, gzipped | 200 KB |
| Charts | Lazy-loaded chunk; ECharts imported by module, never the full bundle |
| Core Web Vitals on staging (mid-range laptop) | Largest Contentful Paint 2.5 s, Interaction to Next Paint 200 ms, Cumulative Layout Shift 0.1 (the published "good" thresholds) |

The bundle budget lives in `console/bundle-budget.json`, is checked in CI, starts at the first measured shell build plus 10%, and rises only with a justification in the PR (CS-T-23). Route-level code splitting, error boundaries at route and app level, and virtualization per UX-38 apply.

| Query rule | Value |
|---|---|
| Stale time | Lists 15 s; polled views follow section 8.6; immutable records 5 min (outcome labels refetch on focus) |
| Cache time | 5 min |
| Retry | GET twice with backoff on network and 5xx errors, never on 4xx, never for mutations |
| Cancellation | Requests abort on unmount and on parameter change |
| Window focus | Refetch only for polled views |

## 19. Design review and acceptance

| Step | What happens |
|---|---|
| 1. Check before build | The PR states which sections of this file apply and which UX rules it touches |
| 2. Component review | Storybook shows every state in both themes with a clean accessibility panel |
| 3. Design review gate | At the end of each UI wave the real application runs in a browser. Screenshots are captured at the four viewports in both themes and checked against this file: grid alignment, type scale, token spacing, density targets, responsive behavior (13), accessibility (keyboard pass, axe, 200% zoom), every interaction exercised against the real backend, copy (UX-04 to UX-10), states (10), charts (8) |
| 4. Refinement | Each wave includes a refinement pass. Findings become issues with screenshots and are fixed before the next wave starts. The first assistant-generated design is never accepted as final |
| 5. Sign-off | The owner approves, recorded in `docs/design-reviews/&lt;wave&gt;.md` (text with links) |

**UI acceptance checklist.** No dead buttons. No inaccessible controls. No inconsistent styling. No fake production charts or hard-coded statistics presented as real. No broken routing. No unauthorized data exposure. No uncontrolled loading states. No unhandled API failures. Tablet and mobile behavior as specified in 13. No fake success notifications. Every workflow exercised in a browser before the work is called complete.

## 20. Open decisions and governance

Recorded as ADRs when decided (numbers assigned from ADR-021).

| Decision | Default until decided |
|---|---|
| Keycloak login and account theme | Standard Keycloak theme; a branded theme using these tokens is Extended scope |
| Code editor dependency | None; evaluate CodeMirror 6 only if raw JSON editing proves inadequate |
| Command palette implementation | In-house on Radix Dialog; a library only with a CS-U-15 section |
| Pattern fills for charts | ECharts decal patterns at 45° and 135° |

- Changes to this file arrive as a PR labelled `design`. A token change updates `tokens.css` and passes `check_contrast.py` in the same PR. A new component needs a story in all its states. A new page needs a row in 6.2 and 6.3, a layout in section 11, an entry in the responsive table, and a working backend (UX-01).
- This version is frozen with spec baseline V1.0 at the approval gate. Later changes follow the change-request path in the spec governance section of `project-overview.md`.
