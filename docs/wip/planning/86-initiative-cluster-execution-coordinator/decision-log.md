---
language: en
status: active
canonical: false
classification: way_of_working
intellectual_kind: decision_log
phase: P0
initiative: INIT-OPENCLAW_AKOS-86
authored: 2026-05-16
last_review: 2026-05-17
role_owner: PMO
ssot: false
companion_to:
  - master-roadmap.md
  - risk-register.md
---

# I86 — Decision Log

> Workspace mirror of I86 charter-time decisions. Canonical rows land in [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) at the same commit.

## Round 1 — P0 charter (2026-05-16)

### D-IH-86-A — Ownership posture: PMO + System Owner co-own + wave spotlight facilitator per wave

**Context.** Cluster spans vault integrity, substrate doctrine, capability doctrine, ingestor productization, TRIGGER-watch brand tooling, research governance, Madeira elevation, and OpenClaw runtime hardening. Ownership ambiguity produces dropped handoffs.

**Decision.** **PMO + System Owner co-own** INIT-OPENCLAW_AKOS-86. Each Wave names a **wave spotlight** role_owner who facilitates that wave's coordination narrative and standup-style status — spotlight does **not** co-sign cluster closure or replace sibling initiative owners.

**Operator selection.** AskQuestion `c86-1-ownership` — **Option D** (`pmo-systemowner-with-wave-spotlight`).

**Rationale.** Mirrors I64 + I65 coordination-initiative shape while distributing wave-level facilitation to subject-matter experts without fragmenting closure authority.

**Reversibility.** Medium.

**Decision_source.** `operator_inline_explicit_via_askquestion`.

**Closes.** Opens OPS-86-1.

---

### D-IH-86-B — Coordination cadence: event-driven burndown pulse + 14-day quiet floor

**Context.** Fixed weekly checkpoints create ceremony on quiet weeks; wave-only checkpoints miss mid-wave drift.

**Decision.** **Event-driven pulse**: checkpoint fires when **any** coordinated sibling changes material state (candidate→active, phase ship, blocker surfaced, closure imminent). **Plus** a **14-day quiet-period floor**: if no sibling event fires in 14 days, agent files a one-paragraph `reports/cluster-quiet-pulse-<YYYY-MM-DD>.md` summarizing last-known sibling states from INITIATIVE_REGISTRY + dep map.

**Operator selection.** AskQuestion `c86-2-cadence` — **Option E** (`event-driven-burndown-pulse`).

**Rationale.** Cadence tracks cluster activity; avoids calendar noise while preventing indefinite silence.

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion`.

---

### D-IH-86-C — AskQuestion batching: wave-boundary default + blocker-overflow lane

**Context.** Per-blocker batches fatigue operators; per-promotion batches lose coupling between sibling gates in the same wave.

**Decision.** **Default**: batch inline-ratify gates at **wave-coordination points** (mega-batch every 1-2 weeks aligned with Wave boundaries). **Escape hatch**: if a cross-cluster blocker cannot wait (example — I87 P1 health-monitor escalation needed before I84 P4 substrate comparison), open a **blocker-overflow** mini-batch immediately.

**Operator selection.** AskQuestion `c86-3-askquestion-batching` — **Option D** (`wave-batches-plus-blocker-overflow`).

**Rationale.** Aligns with inline-ratify-craft Principle 5 for coupled decisions while preserving interruptibility for genuine emergencies.

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion`.

---

### D-IH-86-D — Closure delegation: sibling closes itself + I86 gated cross-check

**Context.** Centralizing closure in I86 raises blast radius if I86 slips; fully autonomous siblings risk dangling cluster deps.

**Decision.** Each sibling mints its own **closure_decision_id** and flips its INIT row per existing governance. **Before** that closure decision finalizes, I86 agent runs a **mechanical cross-check** (~5 min): scan [`INITIATIVE_DEPENDENCIES.md`](../_templates/INITIATIVE_DEPENDENCIES.md) for **solid edges** pointing at the closing sibling + blocker table rows — confirm no open dependent initiative is left inconsistent with the closure narrative.

**Operator selection.** AskQuestion `c86-4-closure-delegation` — **Option C** (`gated-closure-cross-check`).

**Rationale.** Preserves sibling autonomy while preventing silent cluster breakage.

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion`.

---

### D-IH-86-E — Mint posture: active initiative folder + `_candidates/` redirect stub

**Context.** Candidate→active ceremony adds latency when operator already chartered work in-session.

**Decision.** Mint **`docs/wip/planning/86-initiative-cluster-execution-coordinator/`** as **active** immediately. Also mint **`docs/wip/planning/_candidates/i86-initiative-cluster-execution-coordinator.md`** as a **redirect / pointer stub** so agents scanning `_candidates/` discover I86 without treating it as dormant candidate.

**Operator selection.** AskQuestion `c86-5-mint-posture` — **Option C** (`active-with-candidate-stub`).

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion`.

---

## Runtime decisions

### D-IH-86-H — INITIATIVE_REGISTRY program anchors convention (ERP mirror join helper)

**Context.** Intertwined `continuous` / `program_line` initiatives need queryable program anchors when dashboards (including `hlk-erp`) consume mirrored registers. Operator chose convention **N**: encode anchors in `notes` rather than minting new INIT rows or schema columns in this pass.

**Decision.** Prepend affected INIT rows’ `notes` with `Program anchors: <semicolon-separated PRJ-HOL-* ids>;` each id FK-resolves to [`PROGRAM_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv). First tranche: INIT-OPENCLAW_AKOS-01, -04, -06, -08, -14, -19, -55.

**Rationale.** `REPOSITORY_REGISTRY.csv` lists `hlk-erp` as consuming both `PROGRAM_REGISTRY` and `INITIATIVE_REGISTRY` mirrors; `[HLK_ERP_ARCHITECTURE.md](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md)` positions `/operator/operations/pmo/initiatives/` as INIT mirror + roadmap linkage (partially implemented). Parsed anchors enable grep/SQL-side rollups until a dedicated FK column ships.

**Reversibility.** Medium — revise anchors or promote to a first-class column later.

**Decision_source.** Operator preference (post-dashboard relevance discussion 2026-05-17).

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-H**.

---

## Round 2 — P1 Stage A program-anchor robustness (2026-05-17)

### D-IH-86-I — Charter-scope amendment: governance-tooling exception for program-anchor robustness

**Context.** I86 P0 charter preamble (D-IH-86-A through E) declared "mints no SSOT beyond INITIATIVE_REGISTRY / DECISION_REGISTER / OPS_REGISTER". D-IH-86-H (Round 1 runtime decision) introduced the program-anchors convention, but a free-text `notes` prefix without a validator is fragile — typos and unknown anchors silently rot the join. Robustness requires Pydantic chassis + paired SOP/runbook + validator.

**Decision.** Append a **scoped exception** to I86 P0 preamble: I86 may mint the program-anchors validator and paired SOP/runbook **as long as** the surface is anchor-specific and inherits the existing `pattern_paired_sop_runbook` pattern. Tooling lives at [`akos/hlk_initiative_program_anchors.py`](../../../../akos/hlk_initiative_program_anchors.py), [`scripts/validate_initiative_program_anchors.py`](../../../../scripts/validate_initiative_program_anchors.py), [`scripts/pmo_program_anchor_backfill.py`](../../../../scripts/pmo_program_anchor_backfill.py), and [`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md).

**Reversibility.** Medium — exception is scoped to anchor robustness; future tooling needs its own decision row.

**Decision_source.** `agent_inline_default_accepted_via_explicit_continue` (operator instruction *"Don't stop until you have completed all the to-dos"* 2026-05-17). Mirrors precedent established by I81/I82/I85/I87 charter-time `agent_inline_default_accepted_via_skip` rows.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-I**.

---

### D-IH-86-J — Stage A notes-prefix validator (P1) + Stage B first-class column (P2)

**Context.** A first-class `program_anchors` column on `INITIATIVE_REGISTRY.csv` (the durable shape per `akos-holistika-operations.mdc` two-plane model) requires a Supabase DDL migration, Pydantic fieldnames extension, FK block in `validate_initiative_registry.py`, and a one-shot conversion script. That's a 3-day pause-point class commit. Stage A delivers immediate robustness (parse + FK-resolve) without that cost.

**Decision.** Two-stage promotion. Stage A (this commit; I86 P1) keeps anchors as a `Program anchors:` prefix on `notes` and ships the validator + paired SOP/runbook. Stage B (I86 P2; tracked as **OPS-86-3**) promotes anchors to a first-class semicolon-list column with idempotent DDL migration + Pydantic fieldnames extension + FK block + one-shot conversion. Stage B carries a **MANDATORY** operator pause-point per `akos-agent-checkpoint-discipline.mdc` canonical-CSV-gate category.

**Reversibility.** Medium — Stage B may be deferred indefinitely if Stage A coverage stays clean (validator advisory mode keeps the cost low).

**Decision_source.** `agent_inline_default_accepted_via_explicit_continue` 2026-05-17.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-J**.

---

### D-IH-86-K — Persona-view rollup at P3 (six personas; Adviser-external as MANDATORY pause)

**Context.** Program-anchor robustness is the substrate; persona-tailored views are how PMO / Brand & Narrative Manager / IntelligenceOps / People Operations / Founder / Adviser-external consume the rollup. Each persona has a distinct slice: PMO sees full burndown; Brand sees Marketing-area initiatives; Founder sees the founding-cycle overlay; Adviser-external sees **REDACTED** counts only (no `PRJ-HOL-*` ids).

**Decision.** P3 mints a Supabase `governance.initiative_program_rollup_view` joining `compliance.initiative_registry_mirror` × `compliance.program_registry_mirror` via `string_to_array(program_anchors)`; RLS `service_role` + `authenticated` SELECT-only. Six persona contracts land at `reports/persona-view-spec-2026-05-19.md`. The Adviser-external row enforces REDACTED rendering per `akos-brand-baseline-reality.mdc` dual-register contract — `PRJ-HOL-*` ids translate to program-name aliases or counts before reaching non-cleared audiences. hlk-erp panel implementation is **out of scope** for this plan — handoff stub for follow-up initiative **i89** lands at P3 closure.

**Reversibility.** Medium — view DDL is reversible; persona contract revisions track via decision-log entries.

**Decision_source.** `agent_inline_default_accepted_via_explicit_continue` 2026-05-17.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-K**.

---

### D-IH-86-L — BBR drift-gate extension: PRJ-HOL- added to internal-token forbid list

**Context.** Adviser-external surfaces (decks, dossiers, ENISA evidence, boilerplate prose) must not carry internal program ids. The existing BBR drift gate ([`scripts/validate_brand_baseline_reality_drift.py`](../../../../scripts/validate_brand_baseline_reality_drift.py)) enforces this for HUMINT-tradecraft vocabulary; program-id leakage is structurally the same risk.

**Decision.** Append the literal `PRJ-HOL-` prefix to `DEFAULT_INTERNAL_TOKENS`. Internal canonicals (decision logs, decision-register CSV, internal SOPs, master-roadmaps, agent transcripts, `_assets/advops/**/*.counterparty-brief.md`, `_assets/advops/**/*.objections.md`) remain free to use the prefix. P3 widens the scan scope to adviser-external surfaces under `_assets/advops/**/dossier_*.md` and `boilerplate/`; P1 ships the token addition only (no scope widening).

**Reversibility.** Low — token removal trivially reverts behavior.

**Decision_source.** `agent_inline_default_accepted_via_explicit_continue` 2026-05-17. Sibling pattern to I66 P2 drift-gate extension (D-IH-66-M).

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-L**.

---

### D-IH-86-M — Quality bar for Stage A tooling: Pydantic chassis + --json-log + paired tests + Operations/PMO SOP placement

**Context.** Validator quality varies wildly across the repo. Stage A tooling must inherit the I71 P1 / I85 P1 / I77 P4.C tooling bar (Pydantic chassis + structured logging + paired tests + frontmatter-stamped SOP) or it rots.

**Decision.**

1. **Pydantic chassis** at [`akos/hlk_initiative_program_anchors.py`](../../../../akos/hlk_initiative_program_anchors.py) — frozen module-scope regex + canonical fieldnames + `InitiativeProgramAnchorParse` model.
2. **Validator** at [`scripts/validate_initiative_program_anchors.py`](../../../../scripts/validate_initiative_program_anchors.py) with `--json-log` and `--quiet` flags, `akos.log.setup_logging` for structured output, and tests in [`tests/test_validate_initiative_program_anchors.py`](../../../../tests/test_validate_initiative_program_anchors.py) registered under `@pytest.mark.hlk`.
3. **Runbook** at [`scripts/pmo_program_anchor_backfill.py`](../../../../scripts/pmo_program_anchor_backfill.py) with `--list-unanchored`, `--coverage-report`, `--apply proposals.csv`, `--dry-run`, `--legacy-notes-parser` (Stage A→B flag), and tests in [`tests/test_pmo_program_anchor_backfill.py`](../../../../tests/test_pmo_program_anchor_backfill.py).
4. **SOP** at [`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md) — **Operations/PMO**, not People/canonicals/ (per `akos-people-discipline-of-disciplines.mdc` RULE 4 People canonicals are jargon-free + free of internal codenames; INITIATIVE_REGISTRY maintenance is PMO ops).
5. **`acceptance_criteria_human` + `acceptance_criteria_automation`** frontmatter rows per `akos-executable-process-catalog.mdc` RULE 1.

**Reversibility.** Medium — the chassis can be refactored to library form in I71-class polish.

**Decision_source.** `agent_inline_default_accepted_via_explicit_continue` 2026-05-17.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-M**.

---

## Round 3 — P3 persona-view rollup closure (2026-05-17)

### D-IH-86-N — I86 P3 persona-view rollup chassis shipped; implementation forward-chartered to I89 candidate

**Context.** I86 P3 ships the **data-layer chassis** for the cross-area persona-view rollup: the [`governance.initiative_program_rollup_view`](../../../../supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql) SQL view + the [persona-view spec](reports/persona-view-spec-2026-05-19.md) for six personas (PMO / Brand & Narrative Manager / IntelligenceOps / People / Founder / Adviser-external) + the BBR drift-gate scope extension covering founder-filed instruments and adviser-handoff exports + six new rollup-aware route slots in [`HLK_ERP_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) §4 + [UAT acceptance criteria](../../../uat/i86-p3-persona-rollup-acceptance.md) carved into self-attestable (D1-D5) + forward-chartered (E1-E4) dimensions.

The TSX panel implementation — especially the Adviser-external **REDACTED** rendering (substituting `PRJ-HOL-*` ids to `[INTERNAL-PROGRAM]` at render time) — is **MANDATORY pause-point** territory per `akos-agent-checkpoint-discipline.mdc` §"Pause-point depth heuristic" → public-prose category. That deserves a dedicated initiative with its own P0 operator ratification, not a P3 stretch of an operational coordinator.

Additionally, the TSX implementation belongs in the `hlk-erp` sibling repo (per `REPOSITORY_REGISTRY.csv`), not in `openclaw-akos`. Cross-repo bless pattern requires its own coordination per `SOP-EXTERNAL_REPO_BLESSING_001.md` + `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`.

**Decision.**

1. **Close I86 at end of P3.** No P4 or further phases under I86. The charter-scope amendment (D-IH-86-I) terminates here: no further governance tooling minted under I86.
2. **Forward-charter I89 candidate** at [`docs/wip/planning/_candidates/i89-hlk-erp-program-rollup-implementation.md`](../_candidates/i89-hlk-erp-program-rollup-implementation.md) with the implementation contract: six panel routes (TSX scaffolds under `hlk-erp/app/(operator)/...`), Adviser-external REDACTED rendering enforcement at render-time, Supabase Auth + RLS wiring per persona, Browser smoke (Cursor Browser MCP) for all six routes at `dashboard.holistikaresearch.com`, UAT acceptance per E1-E4 dimensions, Adviser-external PDF export pipeline per `akos-adviser-engagement.mdc`.
3. **Route ADVOPS triage of pre-existing BBR leaks** (7 `PRJ-HOL-FOUNDING-2026` references in `dossier_es.md` + `deck_slides.yaml`) to **OPS-86-5** for Brand & Narrative Manager + ADVOPS engagement co-owner action. Not in I86 scope; the validator's job is to *surface* the leaks; the prose fix is BBR + adviser-handoff ownership.

**Reversibility.** Low for the data-layer chassis (view ALTER reversible). Medium for the I89 charter (candidate can be re-scoped or merged into a different initiative).

**Decision_source.** `agent_inline_default_accepted_via_explicit_continue` 2026-05-17. Operator's explicit "Don't stop until you have completed all the to-dos" instruction authorises P3 closure as the I86 terminus + the forward-charter to I89. The I89 P0 operator ratification (charter-of-charters) lives outside this I86 closure.

**Cross-references.**

- Charter: D-IH-86-K (I86 P0).
- Forward-chartered stub: [`i89-hlk-erp-program-rollup-implementation.md`](../_candidates/i89-hlk-erp-program-rollup-implementation.md).
- ADVOPS triage: OPS-86-5.
- I86 closure pause record: [`reports/p3-closure-pause-record-2026-05-17.md`](reports/p3-closure-pause-record-2026-05-17.md).

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-N**.

---

## Round 4 — I89 promotion + BBR gate flip (operator carry-forward executed 2026-05-17)

> Round 4 is **not** an I86 charter decision. It records the I89 promotion fact + the BBR drift-gate flip fact for I86 traceability, because both events were ratified in the I86 P3 close chat (same operator inline-ratify batch as D-IH-86-N) and have cascading consequences on the I86 cluster-burndown surface. The five decisions themselves (`D-IH-89-A..E`) live in **I89's** decision log; the entries below are I86's audit trail.

### D-IH-89-A — Promote I89 candidate to status:active NOW

Operator answer in I86 P3 close chat 2026-05-17: `i89-q1-now`. Implementation: [`docs/wip/planning/89-hlk-erp-program-rollup-implementation/master-roadmap.md`](../89-hlk-erp-program-rollup-implementation/master-roadmap.md) (charter-of-charters); `INIT-OPENCLAW_AKOS-89` row appended to [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv). **Consequence for I86**: `OPS-86-4` (I89 promotion trigger) transitions to `status:closed` in same commit. Cross-reference: [`I89 decision-log.md`](../89-hlk-erp-program-rollup-implementation/decision-log.md) §"D-IH-89-A".

### D-IH-89-B — I89 scope = all 6 routes including Adviser-external

Operator answer `i89-q2-all-six`. Carries the MANDATORY public-prose pause-point at I89 P3 + P4 (Adviser-external panel + PDF export per `akos-agent-checkpoint-discipline.mdc`).

### D-IH-89-C — I89 phase shape = cross-cutting P0-P5 (not sequential per-route)

Operator answer `i89-q3-cross-cutting-phases`. Shared `RollupTable.tsx` component + RLS migration mints serve all six routes; the Adviser-external panel uses isolated `RedactedRollupTable.tsx` component (security-by-component-isolation pattern).

### D-IH-89-D — I89 ownership = tri-co-owned PMO + System Owner + Brand & Narrative Manager

Operator answer `i89-q4-tri-co-own`. `INITIATIVE_REGISTRY.csv` `owner_role` column carries `PMO` (single value per schema constraint); tri-co-ownership encoded in `notes` column + `co_owner_role` YAML frontmatter of I89 master-roadmap.

### D-IH-89-E — BBR drift-gate flipped INFO → FAIL immediately at I89 P0

Operator answer `i89-q5-flip-now`. [`scripts/validate_brand_baseline_reality_drift.py`](../../../../scripts/validate_brand_baseline_reality_drift.py) wiring in [`scripts/release-gate.py`](../../../../scripts/release-gate.py) flipped from `INFO` to `FAIL` (strict by default; hot-fix lane `AKOS_BRAND_BASELINE_REALITY_SOFT=1`). Added dedicated `validate_brand_baseline_reality_drift` step to `pre_commit` profile in [`config/verification-profiles.json`](../../../../config/verification-profiles.json). **Expected CI state**: FAIL on 7 pre-existing `PRJ-HOL-FOUNDING-2026` leaks in `_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md` + `enisa_company_dossier/deck_slides.yaml` until ADVOPS triage of OPS-86-5 closes. Operator accepted this trade-off explicitly. **Consequence for I86**: the cluster-burndown of `OPS-86-5` now has a measurable CI urgency signal (every CI run fails until OPS-86-5 closes).

### Cross-cluster note

I89 is **NOT** one of the ten coordinated siblings tracked by I86's `continuous-cluster-burndown` todo (I81 / I82 / I83 / I74 / I75 / I76 / I77 / I78 / I85 / I87 per [master-roadmap.md](master-roadmap.md) §1.1 wave diagram). I89 is a **downstream forward-charter** from I86 P3, not a parallel sibling. I89's closure is independent of I86's future `D-IH-86-CLOSURE`; the cluster-burndown todo continues unchanged.

