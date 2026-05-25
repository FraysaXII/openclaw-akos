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

---

## Round 5 — Wave R closure audit trail (2026-05-24)

> Round 5 captures the **25-commit Wave R** wave-close audit trail. Wave R was the **FINOPS substrate stand-up wave** — I81 P2 layout migration 5-of-5 close (Bundles A + D T2 + T3) + FINOPS counterparty inventory close-out (Bundle B-1 + B-1ext recon) + monetary-substrate stand-up (Bundle B-2 R5-triple: substrate B-2a + executable B-2b + data/governance B-2c) + Bundle C cross-area ops wiring discipline candidate amendment + Lane B drain (53 findings dispositioned). Decisions ratified across Wave R: 11 sibling-level (`D-IH-81-N`..`D-IH-81-X`) + 2 cluster-level (`D-IH-86-CR` Lane B drain closure + `D-IH-86-CS` Wave R closure). The 11 sibling decisions live in [`I81 decision-log`](../81-vault-integrity-layout-milestones-retrofit/decision-log.md); the 2 cluster decisions are documented below.

### D-IH-86-CR — Wave R Lane B drain closure (53 findings dispositioned)

**Context.** Inter-wave regression sweep at Wave Q close surfaced 53 findings (drift + gap) that fell outside Wave Q's bundle scope. Per [`akos-inter-wave-regression.mdc`](../../../.cursor/rules/akos-inter-wave-regression.mdc) RULE 2 5-option enum, each finding needed an explicit disposition. Per `akos-conflict-surfacing-and-blocker-trackers.mdc`, drain of accumulated cross-wave findings is a legitimate lane within the next wave-close.

**Decision.** Operator-ratified 7 inline-ratify gates (drain1..drain7) at 2026-05-23. Per-finding dispositions: deterministic-fix-now for trivial CSV refreshes; manual-fix-now for prose judgement calls; defer-OPS for chartered backlog (OPS-86-15..OPS-86-20 minted as forward-charter rows); accept-as-canon for ratified pre-existing drift (CHANGELOG conditional dimension); escalate-to-blocker-tracker for none. Closure commit `ce589f4`. Cross-reference: [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) rows `OPS-86-15` through `OPS-86-20`.

**Special case: drain7 cursor-rule-skill-pairing**. Operator ratified `drain7-dispatch-a` (subagent dispatch for the proposal authoring). Subagent dispatch surfaced reliability concerns; superseded by `wrd2-a` in-chat authoring 2026-05-24 (Wave R close session). Proposal authors at `reports/drain7-cursor-rule-skill-pairing-proposal-2026-05-24.md` in successor commit. Forward-charter: `OPS-86-21` placeholder until proposal lands.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-CR**.

### D-IH-86-CS — Wave R closure ratification (this wave-close commit)

**Context.** Wave R accumulated 25 commits + 11 sibling decisions + 2 lane-level decisions across 3 calendar days (2026-05-22 through 2026-05-24). Per [`akos-inter-wave-regression.mdc`](../../../.cursor/rules/akos-inter-wave-regression.mdc) RULE 1 + [`akos-index-integrity.mdc`](../../../.cursor/rules/akos-index-integrity.mdc) RULE 1, wave-close mandates inter-wave regression sweep + index-integrity sweep before the UAT verdict line is filled in. Per [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT quality bar" post-2026-05-19 binding template, the Wave R closure UAT must follow [`uat-closure-template.md`](../_templates/uat-closure-template.md) v1.0 with verdict + 11-section structure + D-IH-86-D 4-signal cross-check.

**Decision.** Operator-ratified 4 inline-ratify gates (waver1..waver4) at 2026-05-24:

- **waver1-a** — PASS-WITH-FOLLOWUP verdict ratified. 11/11 closure criteria PASS; 0 SKIP; 0 FAIL. "WITH-FOLLOWUP" qualifier captures 3 named open OPS rows (OPS-81-22 Stripe live audit + OPS-86-22 DIM-02 4 true gaps + OPS-86-23 30-finding pre-existing backlog).
- **waver2-a** — Class: governance. Same shape as D-IH-86-CR + D-IH-86-CD + D-IH-86-AS.
- **waver3-b** — BOTH new OPS rows (OPS-86-22 + OPS-86-23) trigger at **Wave R+1 close** — deterministic next-wave re-fire rather than chained-to-initiative-promotion. Operator priority on visibility every wave; accepts disposition-fatigue trade-off explicitly.
- **waver4-order-abc** — Post-closure attack sequence: (1) drain7 cursor-rule-skill-pairing proposal (in-chat author per wrd2-a; closes OPS-86-21); (2) Bundle B Strand 2 ambiguous-vendor batches (~24 decisions via 4 batched inline-ratify; closes OPS-81-3); (3) Quality Fabric 12th specialty SYNTHESIS_BEFORE_TRANCHE mint (multi-session per s6-d).

**Wave-R close-out artifacts (atomic-commit binding)**:
- [`reports/regression-sweep-2026-05-24-wave-r-close.md`](reports/regression-sweep-2026-05-24-wave-r-close.md) + sidecar JSON — 46 findings dispositioned (6 clean + 1 drift accept-as-canon + 39 gap forward-chartered).
- [`reports/index-sweep-2026-05-24-wave-r-close.md`](reports/index-sweep-2026-05-24-wave-r-close.md) + sidecar JSON — 8/8 dimensions FRESH; 0 drift; 0 gap.
- [`reports/uat-wave-r-closure-2026-05-24.md`](reports/uat-wave-r-closure-2026-05-24.md) — closure UAT verdict PASS-WITH-FOLLOWUP.
- OPS-86-22 + OPS-86-23 mints in [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv).
- D-IH-86-CS appended to [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) (412 active + 2 superseded post-append).

**Mechanical evidence (Wave R)**:
- `validate_decision_register.py` PASS — 411 active + 2 superseded (412 after this row).
- `validate_ops_register.py` PASS.
- `validate_hlk.py` umbrella OVERALL PASS.
- `validate_inter_wave_regression.py --self-test` PASS + 50/50 pytest.
- `validate_index_freshness.py --self-test` PASS.
- D-IH-86-D 4-signal cross-check: ✓✓✓✓ (release-gate INFO advisory + validate_hlk OVERALL PASS + paired-runbook contract honored + UAT report present).

**Methodological enhancement landed during Wave R (post-sweep heuristic patch)**. The `_probe_dimension_2_forward_charter_carryover` probe in [`scripts/inter_wave_regression_sweep.py`](../../../../scripts/inter_wave_regression_sweep.py) was tightened during Wave R close to reduce false positives (from 10 → 4 true-gap findings). Heuristic improvements: (a) expanded evidence sweep beyond `_candidates/` + `OPS_REGISTER` to filesystem (scripts/ + akos/ + .cursor/rules/ + .cursor/skills/) + canonical CSV bodies (PRECEDENCE + process_list + baseline_organisation + dimensions/); (b) alphanumeric normalization (`_alnum` helper) for token matching across kebab-case + snake_case + path-separator variants; (c) stop-prefix filtering to strip boilerplate ("PEOPLE_DESIGN_PATTERN_REGISTRY row " etc.) from token cores. 50/50 unit tests PASS after refactor. This patch raises the regression sweep's signal-to-noise across all future waves; the methodology is now self-improving per `akos-quality-fabric.mdc` continuous-improvement framing.

**Wave R doctrine consequences**:
- I81 P2 layout migration 5-of-5 **COMPLETE** (Tranches T1..T5 all closed; P2 flipped closed at commit `1437a54`).
- FINOPS pipeline **prod-ready substrate live in MasterData**: 3 Edge Functions deployed + 2 pg_cron schedules registered + PostgREST exposed schemas operator-confirmed + 4 idempotency invariants enforced end-to-end + 1 security hardening migration (pgmq RPC wrapper role lockdown).
- FINOPS_COUNTERPARTY_REGISTER **A2 1/2 areas** (11 obvious-batch vendor rows + Stripe special row landed); ambiguous batch (~24 vendors) deferred to Bundle B Strand 2 (OPS-81-3).
- I-NN-CROSS-AREA-OPS-WIRING-REVIEW candidate **amended to every-area scope** (D-IH-81-T architecture-class; supersedes original backbone-only scope per operator novel framing); stays at `status: candidate` per operator q3-b until A2 ≥ 2/2 area coverage reached.
- Inter-wave regression sweep heuristic **self-improvement** (10 → 4 DIM-02 false positives; future waves inherit cleaner signal).

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-CS**.

### Cross-cluster note (Wave R)

Wave R was the **fifth-largest wave to date** in the I86 cluster (after Waves J, M, N, P). It consolidated **3 simultaneously-running lanes** (Lane A = FINOPS substrate / Lane B = drain / Lane D = layout migration) under a single wave-close ratification. Per `akos-conflict-surfacing-and-blocker-trackers.mdc` Option-5 default posture, the 3-lane consolidation surfaced 4 inline-ratify gates at close (waver1..waver4) — operator handled all 4 without fatigue per explicit "go all out; fully rested" framing 2026-05-24.

**Next Wave (Wave S) opens** with drain7 cursor-rule-skill-pairing proposal authoring per waver4-order-abc step 1. Wave S scope TBD; expected to include Bundle B Strand 2 ambiguous-vendor close-out + Quality Fabric 12th specialty SYNTHESIS_BEFORE_TRANCHE mint per s6-d ratification (largest pending task).

## Round 6 — drain7 cursor-rule × skill pairing audit + 10-deliverable mint (D-IH-86-CT)

**Date:** 2026-05-24 (same chat session; Wave R close-out continuation post-`855fbbf` hygiene commit).

### D-IH-86-CT — drain7 atomic-commit ratification

**Context.** Per `waver4-order-abc` ratification at Wave R close, drain7 was the first post-closure attack item — cursor-rule × skill pairing audit + mint deliverable per the Quality Fabric specialty quartet pattern (canonical doctrine + Pydantic SSOT + validator + runbook + cursor rule + skill + SOP+runbook + pattern-registry row + PRECEDENCE + QF §6 + ramp). The drain7 inventory revealed 23 `akos-*.mdc` rules × 4 paired skills (`inline-ratify-craft` + `index-integrity-craft` + `external-render-craft` + `impeccable`) → 3 paired + 20 gap + 1 orphan (`impeccable` lacks a parent rule) + 4 frontmatter-missing rules.

The proposal report at [`reports/drain7-cursor-rule-skill-pairing-proposal-2026-05-24.md`](reports/drain7-cursor-rule-skill-pairing-proposal-2026-05-24.md) was authored in-chat per `wrd2-a` (superseding the `drain7-dispatch-a` subagent dispatch from Wave Q close that surfaced reliability concerns). Proposal grounded in 5 external research citations (Anderson ACT-R declarative-vs-procedural; Alexander Pattern Language; Google SRE Runbook model; Nonaka-Takeuchi SECI tacit-vs-explicit; Anthropic Skill documentation for LLM agents) per [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc) RULE 2 novel-framing test.

**Decision.** Operator-ratified 3 sub-batch gates + 1 batch3-disposition override at 2026-05-24:

- **drain7-scope-all** — full pairing inventory (23 rules × 4 skills matrix).
- **drain7-deliverable-report-plus-mint** — proposal report + in-chat mint of top-priority skills in the same commit.
- **drain7-research-medium** — 3-5 external citations including industry-standard pattern documentation.
- **drain7-pacing-batches-of-3** — audit in 3 sub-batches, ratify each as it completes.
- **batch1-b mint-all-5** — meta-discipline batch: mint 5 new craft skills (inter-wave-regression-craft + conflict-surfacing-craft + applied-research-craft + quality-fabric-craft + planning-traceability-craft).
- **batch2-b mint-all-4-mirror-batch1** — execution-craft batch: mint 4 new craft skills (agent-checkpoint-craft + deploy-health-craft + brand-baseline-reality-craft + executable-process-catalog-craft).
- **batch3-c-instead** (override) — domain-area batch: decline 6 domain rules + backfill 4 frontmatters (akos-dataops/mktops/techops/ux-discipline.mdc) + **mint new rule `akos-frontend-design.mdc`** pairing globs against the existing `impeccable` skill. Operator declined the assistant's recommended option (f) "defer-impeccable-disposition" and the assistant's risk assessment ("scope mismatch between impeccable and akos-ux-discipline.mdc; minting a tightly-coupled new rule introduces low rework risk").

**Atomic-commit deliverable inventory**:

- 9 new craft skills (~2200 total lines across 9 SKILL.md files; 5 batch-1 + 4 batch-2).
- 1 new rule (`akos-frontend-design.mdc`) — globs frontend file extensions across boilerplate / hlk-erp / kirbe-platform / static; cross-references impeccable as paired-skill.
- 4 frontmatter backfills on prior ops-discipline rules (dataops + mktops + techops + ux).
- 9 cross-ref backfills on parent rules naming their newly-minted paired skills (inter-wave-regression + conflict-surfacing + applied-research + quality-fabric + planning-traceability + agent-checkpoint + deploy-health + brand-baseline-reality + executable-process-catalog).
- Proposal report at `reports/drain7-cursor-rule-skill-pairing-proposal-2026-05-24.md` (authored in same atomic commit per `drain7-deliverable-report-plus-mint` + `wrd2-a`).
- OPS-86-21 closed (status flipped to closed in same commit; linked_decision_ids includes D-IH-86-CT).
- D-IH-86-CT appended to DECISION_REGISTER (415 active + 2 superseded after this row).
- CHANGELOG entry + I86 files-modified +N rows + operator-scratchpad drain.

**Mechanical evidence**:
- `validate_ops_register.py` PASS (128 rows; OPS-86-21 closed cleanly).
- `validate_decision_register.py` PASS (415 active + 2 superseded).
- `validate_hlk.py` umbrella OVERALL PASS (post-commit).
- D-IH-86-D 4-signal cross-check: ✓✓✓✓ (release-gate INFO + validate_hlk PASS + paired-rule×skill cross-refs honored + proposal report present).

**Doctrine consequences**:
- Pairing inventory becomes baseline for future drift detection: future rule mints automatically inherit "paired skill expected unless declared free-standing." 4 rules explicitly declined paired skills (dataops + mktops + techops + ux — mechanical layers governed by their parent canonical SOP+runbook pair; no craft-layer surfaces meeting the codification-warrant test).
- `impeccable` orphan-skill resolved via `akos-frontend-design.mdc` mint (Option c override): paired-rule trigger surfaces now for any frontend authoring task; operator can extend later.
- Future Quality Fabric specialty mints follow the same quartet pattern + paired skill at `.cursor/skills/<rule-slug>-craft/SKILL.md` (when how-layer craft warrants codification).
- Pre-commit `validate_index_freshness.py` IDX-08 dimension (`HOLISTIKA_QUALITY_FABRIC.md §6 specialty list`) does NOT need updating (no new specialty minted; only paired-skill quartets for existing specialties + 1 new rule that is NOT a Quality Fabric specialty).

**Closes OPS-86-21**.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-CT**.

### Cross-cluster note (Round 6)

Round 6 represents the first **post-Wave-R compounding work** — the drain7 deliverable feeds back into every future agent's authoring discipline by establishing the paired rule × skill pattern as default. Per `akos-applied-research-discipline.mdc` Wave-Closure Research Enrichment subsection requirement, the proposal report's §"External research grounding" subsection captures the 5 cited sources + identifies 0 deferred enrichment items for future waves.

**Next attack**: Bundle B Strand 2 ambiguous-vendor batches (~24 counterparty decisions via 4 batched inline-ratify; closes OPS-81-3) per `waver4-order-abc` step 2.

---

## Round 7 — Bundle B Strand 2 closure + Wave R+1 P1 UAT_DISCIPLINE promotion (2026-05-24)

**Date:** 2026-05-24 (Wave R+1 entry; Bundle B Strand 2 closure landed in `c9e462b` + hygiene `15d8471`; Wave R+1 P1 UAT_DISCIPLINE promotion landed in `d0880c6` + hygiene `1898e8b`).

### D-IH-86-CW — UAT_DISCIPLINE.md promotion from charter to active (12th Quality Fabric specialty classification axis)

**Context.** UAT_DISCIPLINE.md was minted at Wave H (2026-05-19) via D-IH-86-V at `status: charter` per the convention that specialty canonicals land at charter until first exercised by a real worked example. The intervening waves H→R accumulated 4+ closure UATs authored under the new 7-class taxonomy (compose_UAT(audience, channel, scenario, brand, governance) → 7-class UAT shape), demonstrating the schema operates correctly across diverse closure contexts (single-area + multi-area + mixed-area + cluster-coordinator). The 4-class threshold from UAT_DISCIPLINE.md §10 promotion criteria was met by Wave R close.

The promotion bundle ships the full 17-surface specialty quartet contract:

- **Canonical doctrine** — UAT_DISCIPLINE.md frontmatter flipped `status: charter` → `status: active`; appended §10 promotion log + §10.4 active-status promotion narrative; appended machine-readable `field_test_window:` frontmatter block (Wave U close target; 3-wave observation window from Wave R+1 P1).
- **Paired Pydantic chassis** — `akos/hlk_uat_report.py` extended with `CanonicalFieldTestWindow` Pydantic model + frontmatter parsing + dual FTW/FTW-RT regex for field-test-code matching.
- **Paired validator** — `scripts/validate_uat_report.py` minted with strict-mode finding codes including UAT-FM-11-PWF-WITHOUT-RATIONALE which catches every PASS-WITH-FOLLOWUP UAT lacking a structural `verdict_followup_rationale:` block. The validator caught Wave R's v1 on first run as the literal field-test signal (see D-IH-86-CZ Round 8 below).
- **Paired SOP** — SOP-PEOPLE_UAT_GOVERNANCE_001.md minted as the operator-facing companion (closes OPS-86-22 sub-finding #1).
- **process_list.csv row** — `hol_peopl_dtp_uat_governance_001` appended (1179→1180; closes OPS-86-22 sub-finding #2).
- **PEOPLE_DESIGN_PATTERN_REGISTRY row** — `pattern_uat_class_taxonomy` appended (21→22; closes OPS-86-22 sub-finding #3).
- **Cursor rule update** — akos-uat-discipline.mdc RULE 2 binding the machine-readable `field_test_window:` mandate + RULE 4 INFO→FAIL ramp aligned with field-test-window lifecycle.

**Decision.** Operator-ratified the promotion at the canonical-CSV gate (Q1-a + Q2-a explicit row-content ratify per `akos-governance-remediation.mdc` § "HLK compliance governance" canonical-CSV gate discipline).

**Mechanical evidence**:
- `validate_uat_report.py --self-test` PASS (full Pydantic round-trip).
- `validate_uat_report.py --all` PASS on existing UAT reports (Wave R v1 caught as UAT-FM-11; surfaced as Commit 3 amend trigger).
- `validate_decision_register.py` PASS (418 active + 2 superseded after D-IH-86-CW append).
- `validate_ops_register.py` PASS (128 rows).
- `validate_hlk.py` umbrella OVERALL PASS.
- D-IH-86-D 4-signal cross-check: ✓✓✓✓.

**Atomic commits**: `d0880c6` (P1 Commit 1 — 17-surface mint) + `1898e8b` (hygiene SHA backfill).

**Closes OPS-86-22 sub-findings #1+#2+#3 partially** (3-of-4 UAT-side artifacts; the 4th MKTOPS-side artifact carves to OPS-86-25 per D-IH-86-CZ Round 8).

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-CW**.

### Bundle B Strand 2 closure note

In parallel with Wave R+1 P1, Bundle B Strand 2 closed at `c9e462b` (D-IH-81-Z) + `15d8471` (hygiene SHA backfill 20 rows). 15 net-new FINOPS counterparty rows + `finops_at_pymes` engagement-model amendment + banking enum extension + Spain-strategy research-area-improvement candidate + OPS-81-2 closed + D-IH-81-Z paired-closure with D-IH-81-U. Bundle B FULLY CLOSED. Not reported in detail here (lives in I81 decision-log).

---

## Round 8 — Wave R+1 P2 governance trio + Wave R UAT amendment v2 (2026-05-25)

**Date:** 2026-05-25 (Wave R+1 P2 entry; 3-commit cycle 3-a + 3-b + 3-c).

Round 8 carries the **second** Quality Fabric specialty mint of the Wave R+1 cycle + the DIM-10 probe-correctness fix + the Wave R closure UAT v2 amendment as the worked-example birth artifact for the newly-minted PWF specialty. The 4 decisions (D-IH-86-CW from Round 7 already cited + CX + CY + CZ in this Round) form a **structural trio + amendment** that together transform the UAT pipeline from prose-rationale-tolerant to machine-readable-rationale-enforcing:

- **D-IH-86-CW (Round 7)** — UAT_DISCIPLINE classification axis (the *what* of UAT class taxonomy).
- **D-IH-86-CX (this Round)** — PWF_GOVERNANCE content axis (the *what shape* of follow-up rationale).
- **D-IH-86-CY (this Round)** — DIM-10 probe-correctness fix (the *what evidence* underpins regression sweep).
- **D-IH-86-CZ (this Round)** — Wave R UAT v2 amendment (the *worked example* showing all 3 above operate end-to-end).

### Why no D-IH-86-CU / D-IH-86-CV slot mints

A pre-commit-3-c plan considered minting D-IH-86-CU (regression-sweep ratification) + D-IH-86-CV (index-sweep ratification) as a parallel "sweep-ratification quartet" alongside the structural mints. Rejected because:

1. **No new sweep-discipline ratification needed**. Wave R+1 did not change the regression-sweep or index-sweep doctrine — both were minted at Wave M (INTER_WAVE_REGRESSION_DISCIPLINE per D-IH-86-AU/BN) and Wave N (INDEX_INTEGRITY_DISCIPLINE per D-IH-86-CD/CE) respectively. The Wave R+1 sweeps were *instances* of those disciplines operating correctly, not *amendments* of them.
2. **D-IH-86-CY already covers the only sweep change**. The DIM-10 probe-correctness fix is the only sweep-side change in Wave R+1; ratifying it as CY suffices. Adding CU+CV would create empty governance shells with no semantic content.
3. **Wave R+1 has not closed yet**. Wave-close ratification (per akos-inter-wave-regression.mdc + akos-index-integrity.mdc) fires at *wave-close*, not mid-wave. Wave R+1 closes when P3 lands; the wave-close sweeps will run then and may or may not need a closure decision row depending on findings.

The trio + amendment thus carries all required governance load without inflating the decision register with structural placeholder rows.

### D-IH-86-CX — PASS-WITH-FOLLOWUP Governance Discipline mint (12th Quality Fabric specialty content axis)

**Context.** UAT_DISCIPLINE's PASS-WITH-FOLLOWUP verdict was correctly named at Wave H (2026-05-19) but the *shape* of the follow-up rationale was left under-specified. Existing PASS-WITH-FOLLOWUP UATs (including Wave R v1) carried prose-only rationale buried in §10 Verdict + Reason — readable but not machine-parseable + not classified against a taxonomy. The pre-commit-3-a inline-ratify gate surfaced 5 candidate followup classes (monitoring-obligation + deferred-work-with-tracker + convention-class-followup + mechanical-recovery-with-eta + escalation-to-blocker-tracker); operator ratified the full 5-class enum as the canonical taxonomy.

**Decision.** Operator-ratified the PWF_GOVERNANCE_DISCIPLINE mint at `status: charter` as the 12th Quality Fabric specialty. The discipline pairs with UAT_DISCIPLINE (classification axis) and composes multiplicatively per HOLISTIKA_QUALITY_FABRIC.md §3 — every PASS-WITH-FOLLOWUP UAT must satisfy BOTH the UAT_DISCIPLINE class taxonomy AND the PWF_GOVERNANCE rationale shape.

**17-surface quartet contract delivered in same commit** (per the Wave M+N specialty-mint contract pattern):

1. Canonical doctrine: `PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`.
2. Pydantic chassis: `akos/hlk_pwf_governance.py` (`PWFFollowupRationale` + `PWFGovernanceFinding` + `PWFGovernanceReport` frozen models + 5-class enum + helper frozensets `REQUIRED_CLOSURE_TARGET_CLASSES` + `REQUIRED_TRACKER_PATH_CLASSES`).
3. Validator: `scripts/validate_pwf_governance.py` (5 finding codes PWF-FM-01..05; `--self-test` + `--report` + `--all` modes).
4. Tests: 35/35 PASS in `tests/test_validate_pwf_governance.py` + `tests/test_hlk_pwf_governance.py`.
5. SOP: `SOP-PEOPLE_PWF_GOVERNANCE_001.md` (paired operator-facing companion).
6. Cursor rule: `.cursor/rules/akos-pwf-governance.mdc` (RULE 1 + RULE 2 binding).
7. Skill: `.cursor/skills/pwf-governance-craft/SKILL.md` (paired how-layer craft).
8. PRECEDENCE.md canonical + mirror rows.
9. QUALITY_FABRIC §6 specialty list row.
10. PEOPLE_DESIGN_PATTERN_REGISTRY row.
11. process_list.csv row `hol_peopl_dtp_pwf_governance_001`.
12. verification-profiles.json `validate_pwf_governance_self_test` step.
13. release-gate.py `run_pwf_governance_validation` INFO advisory.
14. CHANGELOG entry.
15. files-modified.csv +N rows.
16. operator-scratchpad drain.
17. DECISION_REGISTER D-IH-86-CX append.

**INFO→FAIL ramp** (per D-IH-86-CX rationale): gated on Wave T close at earliest + 3 consecutive clean wave-close sweeps + operator-explicit successor decision row.

**Atomic commits**: `e054208` (Commit 3-a — 17-surface mint) + `d3b1c25` (hygiene SHA backfill).

**Mechanical evidence**:
- `validate_pwf_governance.py --self-test` PASS.
- `validate_pwf_governance.py --all` PASS (no existing PASS-WITH-FOLLOWUP UAT has structural rationale yet — pre-ramp baseline).
- `validate_hlk.py` umbrella OVERALL PASS.
- 35/35 pytest PASS.
- D-IH-86-D 4-signal cross-check: ✓✓✓✓.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-CX**.

### D-IH-86-CY — DIM-10 probe-correctness fix + reality-reflecting backfill (CICD directive: no bug tolerance)

**Context.** The Wave R close regression sweep emitted 4 DIM-10-DEPLOY-EVIDENCE-COMPLETENESS findings against I68/I71/I72/I73 — each citing "sibling-repo references without deploy state tokens". On Commit 3-b entry, mechanical investigation of each cited initiative's `files-modified.csv` revealed **zero sibling-repo rows in any of the 4 initiatives' own CSVs**. The probe was checking `reports/uat-*.md` files **globally** against the cluster coordinator's `files-modified.csv` rather than **per-CSV** against each initiative's own `files-modified.csv`. The 4 findings were structural false positives induced by the probe scoping bug, not real evidence gaps.

The pre-commit-3-b inline-ratify gate surfaced 3 dispositions: (a) fix-bug-now; (b) backfill-supplement-only; (c) HYBRID combining both. Operator framed the choice as: *"option A because we must fix any bugs (make this a CICD directive no bug tolerance). but we must backfill to reflect reality as we go because we'll have better processes and metadata (also CICD for data integrity)."* This is the **HYBRID** path — both fix-the-bug AND author-the-supplement.

**Decision.** Operator-ratified the HYBRID disposition at Commit 3-b entry.

**Mechanical deliverables**:

- **Probe-correctness fix** in `scripts/inter_wave_regression_sweep.py`: `_probe_dimension_10_deploy_evidence_completeness` now uses per-CSV `this_csv_sibling_rows` counter that short-circuits the reports-dir check when the current CSV has zero sibling-repo rows; the `total_sibling_rows` global is retained only for the trailing clean-summary row.
- **Bonus fix**: `_safe_relpath` helper wraps 3 `path.relative_to(REPO_ROOT)` calls with `try/except ValueError` so the probe survives monkey-patched `PLANNING_ROOT` (tests pass on `tmp_path` layouts).
- **5 new regression tests** in `TestDimension10PerCsvScoping` class lock in the invariant on a synthetic 3-initiative fixture (zero_sibling_zero_findings + sibling_with_complete_evidence_zero_findings + sibling_without_uat_does_flag + sibling_with_uat_missing_evidence_does_flag + total_sibling_rows_counted_globally).
- **Backfill supplement** at `reports/uat-dim10-backfill-supplement-2026-05-25.md` documents per-initiative reality (each of I68/I71/I72/I73 confirmed 0 sibling-repo rows in own files-modified.csv; closure reports under non-uat-* naming patterns like `p71-closing.md` or `p7-page-spec-impeccable-*.md`).
- **Post-fix sweep** at `reports/regression-sweep-2026-05-25-commit-3-b-dim10.md` emits clean: 1 / gap: 0 with 45 sibling-repo rows across all CSVs.

**Atomic commits**: `391dd14` (Commit 3-b — probe fix + 5 tests + supplement + governance writes) + `3a0d3ea` (hygiene SHA backfill 9 rows).

**Mechanical evidence**:
- All 55 tests in `test_inter_wave_regression.py` PASS post-fix (50 prior + 5 new).
- DIM-10 sweep post-fix emits clean: 1 / gap: 0.
- `validate_hlk.py` umbrella OVERALL PASS.

**Closes OPS-86-23 DIM-10 sub-finding** (4 sibling-repo references); main OPS-86-23 row remains open for DIM-04 + DIM-05 + (carved-to-OPS-86-24) DIM-06 sub-findings.

**Doctrine consequence — CICD bug-tolerance posture**: operator's framing established CICD discipline as **zero-tolerance for probe bugs** — when a probe emits structural false positives, the probe gets fixed in the same commit window that backfills the truth-record; never one without the other. This pairs with the **HYBRID disposition** as the new default when probe-correctness fixes surface alongside reality-reflecting backfills. The pattern is reserved for transferable mint as `pattern_probe_correctness_hybrid_disposition` after third confirmed instantiation per akos-people-discipline-of-disciplines.mdc RULE 1.

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-CY**.

### D-IH-86-CZ — Wave R closure UAT v2 amendment (machine-readable verdict_followup_rationale per PWF specialty schema)

**Context.** Wave R closed 2026-05-24 with `uat-wave-r-closure-2026-05-24.md` carrying `verdict: PASS-WITH-FOLLOWUP` + prose-only rationale buried in §10. Under the pre-2026-05-19 UAT template, that shape was compliant — it correctly conveyed the wave's PASS-with-named-followups state. Two structural mints in Wave R+1 P1+P2 changed the bar:

1. **D-IH-86-CW** (Round 7) — promoted UAT_DISCIPLINE.md to `status: active`; landed paired validator `scripts/validate_uat_report.py` with finding code UAT-FM-11-PWF-WITHOUT-RATIONALE.
2. **D-IH-86-CX** (this Round) — minted PWF_GOVERNANCE_DISCIPLINE with `PWFFollowupRationale` Pydantic schema + 5-class enum.

The validator caught Wave R's v1 on first run as the literal field-test signal — this is the **closing-loop pattern** named in UAT_DISCIPLINE.md §10.4: *"mint validator → catch real gap on first run → amend offending artifact in same commit-window → cite finding as field-test signal"*. The amendment serves as the worked-example birth artifact for the 12th Quality Fabric specialty.

**Decision.** Operator-ratified the Wave R v2 amendment at Wave R+1 P2 Commit 3-c. Verdict stays PASS-WITH-FOLLOWUP — the amendment normalises the *shape* of the follow-up record, not the *substance* of the verdict.

**Mechanical delta (v1 → v2)**:

- `last_review:` 2026-05-24 → 2026-05-25.
- `verdict_history:` block added with v1 entry (legacy-string rationale) + v2 entry (monitoring-obligation rationale).
- `verdict_followup_rationale:` block added with `followup_class: monitoring-obligation` + `closure_target: Wave R+2 close` + `owner: System Owner` + `closure_decision_id_target: D-IH-86-CZ` + multi-line notes covering all 3 open OPS rows (OPS-81-22 + OPS-86-22 partial-close + OPS-86-23 backlog carve).
- `ratifying_decisions:` extended +4 (CW + CX + CY + CZ).
- `linked_canonicals:` extended +2 (UAT_DISCIPLINE.md + PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md).
- `linked_runbooks:` extended +2 (validate_uat_report.py + validate_pwf_governance.py).
- §12 Amendment log subsection added — documents v1 → v2 mechanical delta + why-no-verdict-flip + field-test-signal-closure-loop + forward-charters-surfaced.

**No body content change in §1–§11.** The 11 closure criteria + mechanical evidence + per-dimension findings + D-IH-86-D 4-signal cross-check + SOP+runbook pair + risk closures + decision close-outs + registry edits + verdict checklist all remain as authored at Wave R close.

**Why `monitoring-obligation` class (not `deferred-work-with-tracker`)**: PWF taxonomy distinguishes work that has a dedicated `_trackers/` file (deferred-work) from ongoing monitoring obligations where OPS_REGISTER rows themselves serve as the tracker. Wave R's 3 open OPS rows (OPS-81-22 Stripe MCP audit + OPS-86-22 partial-close + OPS-86-23 backlog) are wave-cadence-observable governance items — they fit `monitoring-obligation` naturally and do NOT require `tracker_path`. The decision avoids creating empty `_trackers/` files just to satisfy a stricter taxonomy class.

**OPS_REGISTER changes in same commit** (per CZ scope):

- **OPS-86-22 closed** (status: open → closed; closed_at: 2026-05-25) — 3-of-4 UAT-side artifacts closed via D-IH-86-CW; 1-of-4 MKTOPS-side carved to OPS-86-25.
- **OPS-86-23 amended** — DIM-06 10 findings carved out to OPS-86-24; DIM-10 sub-finding noted as closed via D-IH-86-CY; remaining 16 findings (DIM-04 8 + DIM-05 8).
- **OPS-86-24 minted** — DIM-06 closed-initiative UAT class completeness backfill (10 pre-2026-05-19 INIT-* rows; forward-only per migration posture; quarterly review cadence).
- **OPS-86-25 minted** — MKTOPS_DISCIPLINE forward-charter (paired runbook needs parent canonical first; closes when I-NN-MKTOPS-OPERATIONALISATION activates).

**Atomic commits**: this commit (Commit 3-c — Wave R UAT amend + 4 OPS-row deltas + D-IH-86-CZ + governance writes) + hygiene SHA backfill (to land next).

**Mechanical evidence** (pre-commit):
- `validate_uat_report.py --report uat-wave-r-closure-2026-05-24.md` expected to flip from FAIL UAT-FM-11 (v1) → PASS (v2 with structural rationale).
- `validate_pwf_governance.py --report uat-wave-r-closure-2026-05-24.md` expected PASS (PWF-FM-01..05 clean).
- `validate_ops_register.py` PASS (130 rows; OPS-86-22 closed + 23 amended + 24+25 minted).
- `validate_decision_register.py` PASS (420 active + 2 superseded after D-IH-86-CZ append; FK to OPS-86-22/23/24/25 resolvable).
- `validate_hlk.py` umbrella OVERALL PASS.
- D-IH-86-D 4-signal cross-check: ✓✓✓✓ (release-gate INFO + validate_hlk PASS + UAT-FM-11 closing-loop honored + amended UAT report present).

**Closes the closing-loop pattern**: validator → caught Wave R v1 gap on first run → amended in same wave-close window → cited finding as field-test signal. The pattern is reserved for transferable mint as `pattern_validator_field_test_closing_loop` after third confirmed instantiation per akos-people-discipline-of-disciplines.mdc RULE 1 (People owns the consulting design patterns).

Canonical row: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) **D-IH-86-CZ**.

### Cross-cluster note (Round 8)

Round 8 represents the **second compounding cycle** post-Wave-R. Where Round 6 (drain7) established the paired rule × skill pattern, Round 8 establishes the **paired UAT × PWF pattern** + the **closing-loop pattern** (validator catches gap on first run + amend offending artifact in same window). Both patterns are People-owned consulting design patterns reserved for transferable-mint after third confirmed instantiation.

The 4 decisions (D-IH-86-CW Round 7 + CX/CY/CZ Round 8) form a complete trio + amendment that operationalises:

- *What* a UAT class is (UAT_DISCIPLINE D-IH-86-CW).
- *What shape* its follow-up rationale takes (PWF_GOVERNANCE D-IH-86-CX).
- *What evidence* underpins regression sweeps (DIM-10 probe correctness D-IH-86-CY).
- *Worked example* showing all 3 operate end-to-end (Wave R UAT v2 D-IH-86-CZ).

The trio's INFO→FAIL ramps are coupled: PWF_GOVERNANCE ramp gated on Wave T close + 3 clean sweeps; UAT_DISCIPLINE field_test_window observation gated on Wave U close. The Wave R v2 amendment is the literal first instantiation that both ramps will observe in their windows.

Per `akos-applied-research-discipline.mdc` Wave-Closure Research Enrichment subsection requirement, Round 8 introduces no new external research grounding (the underlying PWF taxonomy was research-grounded at Wave R+1 P2 Commit 3-a per D-IH-86-CX rationale; the amendment is execution of that doctrine, not novel framing).

**Next attack** (post-Commit 3-c push): operator-scratchpad continuity per akos-inter-wave-regression.mdc DIM-12; CHANGELOG prepend; release-gate.py full run; atomic commit + hygiene SHA backfill + push to origin/main; Wave R+1 P3 entry decision (continue closing pre-existing backlog vs activate new initiative vs Wave R+1 close).

