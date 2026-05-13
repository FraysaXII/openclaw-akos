---
language: en
Item Name: Initiative governance lifecycle (HLK planning workspace)
Item Number: SOP-INITIATIVE_GOVERNANCE_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Operations
Associated Workstream: Think Big Operational Excellence
Version: 0.1
Revision Date: 2026-05-06
status: review
---

## Purpose

Define the **canonical lifecycle** for every planning **initiative** under `docs/wip/planning/<NN>-<slug>/`. This SOP is the human-readable companion to the machine-readable contracts in `INITIATIVE_REGISTRY.csv`, `CYCLE_REGISTER.csv`, `OPS_REGISTER.csv`, and `DECISION_REGISTER.csv` (canonicals introduced by Initiative [59](../../../../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md)).

The five-headed problem this SOP solves:

1. **Status ambiguity.** Before I59 there were ~12 ad-hoc statuses across roadmaps (`closed`, `forwarded`, `running`, `active`, `partially closed`, `paused`, `superseded`, …). Operators could not tell at a glance which initiatives were genuinely *worked on now* vs. simply *kept open by design*.
2. **Decision trace gaps.** `D-IH-XX-Y` decisions lived only as markdown headers in `decision-log.md`; reverse-lookup ("what decisions touched policy X?") was impossible without grep.
3. **OPS-XX-Y orphans.** Action items moved between initiatives without a register; closed-out initiatives sometimes still surfaced as "open" because their forward pointers were prose only.
4. **Cycle vs. initiative confusion.** Coordinating cycles (I57, I58, I59, …) were structurally identical to single-track initiatives in `docs/wip/planning/`, even though they have different semantics (they bundle peer initiatives).
5. **Operator delegation.** No machine-readable inbox for actions the agent cannot complete autonomously (live cycles requiring keys, third-party engagement, manual review).

## Preconditions

- A new or existing initiative with at least a draft `master-roadmap.md` under `docs/wip/planning/<NN>-<slug>/`.
- Operator-approved `initiative_id` (snake_case, ≤ 64 chars; `i<NN>_<short_slug>` recommended).
- `repo_slug` resolvable in `REPOSITORY_REGISTRY.csv` (default `openclaw-akos` for AKOS-tracked work).

## Status taxonomy (SSOT)

The SSOT for initiative statuses is `akos.planning.status_taxonomy.InitiativeStatus`. Seven values, each with required companion fields enforced by both the validators and `master-roadmap.md` frontmatter parsers:

| status | Meaning | Required companion fields | Dashboard section |
|--------|---------|--------------------------|-------------------|
| `closed` | Genuinely complete, all deliverables shipped, no live obligations | `closure_decision_id`, `closed_at` | Closed |
| `archived` | Closed and superseded by a newer initiative | `closure_decision_id`, `closed_at`, `superseded_by` | Archived |
| `active` | Currently being worked (engineering, planning, or live cycle in flight) | `last_review` | Active |
| `continuous` | **By design** never closes (e.g. recurring telemetry routine, weekly metrics review). Reviewed quarterly | `last_review`, `review_cadence` | Continuous |
| `program_line` | Long-running multi-cycle program (e.g. compliance vault stewardship) | `last_review`, `review_cadence` | Program Lines |
| `gated_external` | Blocked on a non-Holistika dependency (regulator, external counsel, vendor decision) | `last_review`, `gate_reason` | Gated |
| `gated_operator` | Blocked on operator action (key rotation, manual review, finance approval) | `last_review`, `gate_reason`, **must have one or more `OPS_REGISTER` rows pointing back** | Gated |

A `master-roadmap.md` whose frontmatter `status:` does not match `InitiativeStatus` is a **validation failure** (`scripts/validate_initiative_registry_frontmatter_sync.py`).

## Steps — initiative lifecycle

### 1. Inception

1. **Create** `docs/wip/planning/<NN>-<slug>/master-roadmap.md` with frontmatter `initiative_id`, `repo_slug`, `status: active`, `inception_decision_id`, `last_review` set to today's date.
2. **Insert** an `INITIATIVE_REGISTRY.csv` row referencing the same id; status, last_review, and decision FK must match the frontmatter exactly.
3. **Open** the inception decision in `decision-log.md` (e.g. `D-IH-<NN>-A`) and **mirror** it into `DECISION_REGISTER.csv` with `decision_class=architectural`, `status=accepted`, `reversibility=…`. The CSV row must exist for the validator to pass.
4. **Run** `py scripts/validate_hlk.py` and confirm new validators (`validate_initiative_registry`, `validate_decision_register`, sync gates) all PASS before commit.

### 2. Active execution

1. Add new `D-IH-<NN>-Y` decisions in lockstep (markdown header **and** `DECISION_REGISTER.csv` row).
2. When discovering an action the agent or operator must own later, file it in `OPS_REGISTER.csv` with a forward-looking `originating_initiative_id`, owner_class, and RICE score. Operator-owned and mixed rows automatically appear in `docs/wip/planning/OPERATOR_INBOX.md`.
3. Touch `last_review` whenever a phase report, decision, or material status change happens. The cycle-staleness canary (`scripts/check_active_initiative_freshness.py`, run from CI/release-gate) flags `active` initiatives whose `last_review` exceeds the configured horizon (default 14 days; tuneable per initiative via `freshness_horizon_days`).

### 3. Cycle membership

1. If the initiative joins a coordinating cycle (e.g. I58, I59), set `cycle_id` in both frontmatter and CSV; the cycle's `coordinated_initiative_ids` list must contain this initiative_id.
2. Cycles themselves have their own `INITIATIVE_REGISTRY.csv` row **and** a `CYCLE_REGISTER.csv` row; `coordinating_initiative_id` in the cycle register equals the cycle's own initiative_id.

### 4. Closure

1. Author the closure UAT report under `reports/<closure-slug>-YYYY-MM-DD.md`. UAT is mandatory — no initiative may close without dated evidence (or a recorded SKIP / N/A per row, per `.cursor/rules/akos-planning-traceability.mdc`).
2. Open `D-IH-<NN>-CLOSURE-<slug>` in `decision-log.md` and `DECISION_REGISTER.csv`. The decision register validator accepts both the standard `D-IH-XX-Y` and the closure-form pattern.
3. Flip frontmatter to `status: closed` (or `archived` if superseded), populate `closure_decision_id` and `closed_at` (ISO date), and update the `INITIATIVE_REGISTRY.csv` row in the **same commit**.
4. Forward any unfinished `OPS-<NN>-Y` items by setting `forwarded_to_initiative_id` on those rows; do **not** mutate the original initiative_id.
5. If the initiative belongs to a cycle, the cycle's `closed_count` is auto-recomputed; the cycle itself only flips to `closed` once all coordinated initiatives are closed.
6. Run `py scripts/validate_hlk.py` + `py scripts/release-gate.py` and confirm PASS before commit.

### 5. Continuous / program_line / gated initiatives

1. These statuses **never** auto-close. They require a `review_cadence` (`weekly`, `biweekly`, `monthly`, `quarterly`) and an explicit `last_review` heartbeat.
2. The dashboard (`scripts/render_wip_dashboard.py`) groups them under their dedicated sections so they cannot be confused with `active` work-in-progress.
3. Quarterly review: PMO confirms each `continuous` and `program_line` initiative still has a clear current scope; otherwise convert to `closed` or split into a fresh active initiative.

## Out of scope

- Minting new `process_list.csv` rows (see [SOP-INITIATIVE_PROCESS_HARMONISATION_001.md](SOP-INITIATIVE_PROCESS_HARMONISATION_001.md)).
- Editing the dashboard or `OPERATOR_INBOX.md` by hand — both are auto-rendered from CSVs.
- Treating `INITIATIVE_REGISTRY.csv` as the *prose* canonical — master-roadmap.md remains canonical for narrative content; the CSV is canonical only for **metadata** (status, dates, FKs, RICE).

## Registry cross-reference

- Anchor process row (planned, **not yet minted**, deferred to Initiative 60 candidate): `gtm_pm_st_initgov` "Initiative governance lifecycle" under **Think Big Operational Excellence**. Until that row exists, this SOP cites itself directly via `hlk_process` from initiative master-roadmaps.
- Related SOPs: [SOP-PMO_VAULT_PROMOTION_GATE_001.md](SOP-PMO_VAULT_PROMOTION_GATE_001.md), [SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md](SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md), [SOP-INITIATIVE_PROCESS_HARMONISATION_001.md](SOP-INITIATIVE_PROCESS_HARMONISATION_001.md).
- Canonical CSVs: `INITIATIVE_REGISTRY.csv`, `OPS_REGISTER.csv`, `CYCLE_REGISTER.csv`, `DECISION_REGISTER.csv`, `REPOSITORY_REGISTRY.csv` (all under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`).
- Status SSOT: `akos/planning/status_taxonomy.py` (`InitiativeStatus` StrEnum + companion-field rules).

## Ratification

This SOP is at **`status: review`**. It is part of Initiative 59 P9 ratification scope. Operator approval (G-59-D) ratifies this SOP and flips its frontmatter to `status: active`. Until ratification it is normative for I59-driven work and reviewed-but-non-binding elsewhere.
