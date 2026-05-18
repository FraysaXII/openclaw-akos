# I89 — Decision Log

> Decision rows for I89 (HLK-ERP persona-rollup panel implementation). Canonical records live in [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv). This log carries narrative + operator-citation per row.

## Round 1 — I86 P3 closure inline-ratify batch (2026-05-17)

Forward-charter from I86 P3 closure (D-IH-86-K + D-IH-86-N) surfaced five architectural decisions via `AskQuestion` batch in the I86 P3 close chat. All five ratified same chat — operator answers `i89-q1-now` + `i89-q2-all-six` + `i89-q3-cross-cutting-phases` + `i89-q4-tri-co-own` + `i89-q5-flip-now`.

### D-IH-89-A — Promote candidate to active NOW

- **Question**: Promote I89 candidate to `status:active` immediately, or hold until I86 cluster-burndown closes (when all ten siblings reach `status:closed`)?
- **Options evaluated**:
 - (A) NOW — establish operator-surface visibility ASAP; do not let I86 P3 close in a state where the implementation is unscheduled. **Operator picked.**
 - (B) HOLD until I86 closes — reduces concurrent in-flight initiatives. Operator declined because I86 cluster-burndown is multi-week and the operator-surface gap (PMO has no rollup view today) is felt now.
- **Operator citation**: I86 P3 close chat 2026-05-17, answer `i89-q1-now`.
- **Status**: RATIFIED.
- **Close-out**: P0 (this commit).
- **Reversibility**: low (once minted, INIT row demands attention until closure).

### D-IH-89-B — Scope = all six routes including Adviser-external

- **Question**: I89 scope = all six routes (PMO + Marketing + Research + People + Founder + Adviser-external), or carve Adviser-external into I90 (separate initiative because public-prose MANDATORY pause)?
- **Options evaluated**:
 - (A) All six — keep the panel-family coherent; the operator-surface story is six routes or it isn't a rollup. **Operator picked.**
 - (B) Defer Adviser-external to I90 — reduces I89 MANDATORY pause-point count from 2 to 0. Operator declined because the BBR drift-gate scope extension in I86 P3 already targeted Adviser-external; carving it out would re-orphan it.
- **Operator citation**: I86 P3 close chat 2026-05-17, answer `i89-q2-all-six`.
- **Status**: RATIFIED.
- **Close-out**: P3 (Adviser-external panel ships).
- **Reversibility**: medium (could split P3+P4 into I90 if BBR triage stalls beyond P3 entry; documented in risk-register as R-IH-89-1 mitigation lane).

### D-IH-89-C — Phase shape = cross-cutting (P0-P5 across all 6 routes)

- **Question**: Phase shape — cross-cutting (P0 charter + P1 RLS for all 6 + P2 TSX for 5 internal + P3 redaction + Adviser + P4 PDF + P5 closure), or sequential per-route (P0 PMO route, P1 Marketing route, ...)?
- **Options evaluated**:
 - (A) Cross-cutting — RLS policies, JWT claims, and the shared RollupTable component fan out best when minted together. **Operator picked.**
 - (B) Per-route sequential — easier blast radius isolation but produces five duplicated component shapes; rejected as failing the "no copy-paste" bar.
- **Operator citation**: I86 P3 close chat 2026-05-17, answer `i89-q3-cross-cutting-phases`.
- **Status**: RATIFIED.
- **Close-out**: P5 (closure validates phase shape worked).
- **Reversibility**: low (phase shape baked into the plan; revising mid-execution is a re-plan).

### D-IH-89-D — Tri-co-ownership (System Owner + PMO + Brand & Narrative Manager)

- **Question**: Ownership — single primary owner (System Owner because TSX) vs tri-co-owned (System Owner + PMO + Brand & Narrative Manager)?
- **Options evaluated**:
 - (A) Tri-co-owned — Tech (System Owner — TSX + RLS + browser smoke in sibling hlk-erp repo) + Operations/PMO (cross-area persona contract coherence + INIT row + AskQuestion hub) + Marketing (Brand & Narrative Manager — BBR doctrine + redaction matrix translation table). Each persona reviewer carries the deliverable that requires their role's expertise. **Operator picked.**
 - (B) Single System Owner — simpler accountability but underweights BBR doctrine review (the I66 BBR matrix author should sign off on the TS translation table).
- **Operator citation**: I86 P3 close chat 2026-05-17, answer `i89-q4-tri-co-own`.
- **Status**: RATIFIED.
- **Close-out**: continuous (ownership pattern persists across all phases).
- **Reversibility**: medium.
- **Implementation note**: `INITIATIVE_REGISTRY.csv` `owner_role` column carries a single value (PMO, per schema constraint — `owner_role` must be a single role from `baseline_organisation.csv`). Tri-co-ownership is encoded in the `notes` column + the `co_owner_role` YAML frontmatter field of master-roadmap.md. The validator enforcement (`validate_hlk.py`) is satisfied by the single primary owner; the operational reality is tri-co-owned.

### D-IH-89-E — BBR drift-gate flip INFO→FAIL immediately

- **Question**: Flip `scripts/validate_brand_baseline_reality_drift.py` from `INFO` to `FAIL` in `release-gate.py` immediately at I89 P0, or wait until ADVOPS triage of OPS-86-5 closes the 7 known `PRJ-HOL-FOUNDING-2026` leaks?
- **Options evaluated**:
 - (A) Flip NOW — maximum drift protection from day one; the CI-block surfaces ADVOPS triage urgency. Cost: until OPS-86-5 closes, every CI run fails. **Operator picked.**
 - (B) Flip after OPS-86-5 — gentle landing; ADVOPS has slack. Cost: a new leak in any I89 phase could land silently because BBR gate is still INFO.
 - (C) Hybrid — flip per-directory (FAIL on `adviser-handoff/`, INFO on `founder-filed/`) — codified split between rendered prose (FAIL) and operator-internal staging prose (INFO). Operator preferred (A) over (C) because the doctrine is "FAIL everywhere external" and the staging vs render distinction muddies the doctrine.
- **Operator citation**: I86 P3 close chat 2026-05-17, answer `i89-q5-flip-now`.
- **Status**: RATIFIED.
- **Close-out**: P0 (this commit flips the gate).
- **Reversibility**: high (one-line revert in `release-gate.py` if ADVOPS slips and a blocking I89 commit is urgent — documented as R-IH-89-1 hot-fix lane).
- **Implementation note**: BBR validator currently shows 7 errors across 2 founder-filed ENISA dossier files. Until OPS-86-5 closes these, `release-gate.py` will FAIL. This is **expected behaviour** per D-IH-89-E.

## Forward decisions (TBD when phase reaches them)

### D-IH-89-F — RLS policy shape (P1)

Choice: RLS on base tables (`compliance.initiative_registry_mirror` + `compliance.program_registry_mirror`) so the view inherits — vs view-defined policies (less common Postgres pattern).

Preferred default (recommended): RLS on base tables; views inherit naturally; documented in P1 §P1.7 inline-ratify gate.

### D-IH-89-G — Adviser-external JWT claim issuance (P1)

Choice: Supabase Auth hook issues custom claim — vs separate service issues a scoped JWT.

Preferred default (recommended): Supabase Auth hook (single source of truth for JWT issuance; consistent with the five internal personas).

### D-IH-89-H — RedactedRollupTable component shape (P3)

Choice: column projection at component prop level — vs server-side projection (RPC returns only safe columns).

Preferred default (recommended): server-side projection AND component-level column whitelist (defense in depth; if either layer fails, the other catches).

### D-IH-89-I — PDF export trigger (P4)

Choice: on-demand runbook invocation by PMO operator per advisor handoff — vs scheduled cron (weekly auto-export).

Preferred default (recommended): on-demand only (`gated_operator` cadence per akos-executable-process-catalog.mdc RULE 3) — every PDF export is operator-ratified; no surprise auto-published artifact.

### D-IH-89-CLOSURE — I89 closure (P5)

Closure condition: all UAT dimensions PASS + BBR drift-gate green on rendered DOM + ADVOPS triage of OPS-86-5 closed (prerequisite for green gate).

## Cross-references

- [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — canonical SSOT.
- [`master-roadmap.md`](master-roadmap.md) §"Decisions preview (inline)" — phase-anchored summary.
- [`risk-register.md`](risk-register.md) — risk rows referencing D-IH-89-A..E.
- I86 P3 closure pause record: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/p3-closure-pause-record-2026-05-17.md`](../86-initiative-cluster-execution-coordinator/reports/p3-closure-pause-record-2026-05-17.md).
- I86 decision-log Round 3 entry noting I89 promotion: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md`](../86-initiative-cluster-execution-coordinator/decision-log.md).
