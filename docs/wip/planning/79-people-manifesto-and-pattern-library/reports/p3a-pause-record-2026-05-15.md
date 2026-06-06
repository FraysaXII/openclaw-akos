---
phase: P3a
date: 2026-05-15
initiative: INIT-OPENCLAW_AKOS-79
strand: C-People (AI doctrine + ops + Ethics anchor)
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-F
  - D-IH-79-L
  - D-IH-79-N
ops_action_id: OPS-79-3
gate_type: inline-ratify (closure pause point per plan)
status: PAUSE — awaiting operator acknowledgement before P3b/P4
---

# I79 P3a — Strand C-People AI doctrine + ops + Ethics anchor pause record

## Mechanical evidence

### Files created (5)

- `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md` (143 lines, `access_level: 5`, jargon-free) — People-side AI/agentic doctrine; clarity-side anchor of three-part stratified split.
- `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md` (143 lines, `access_level: 4`, jargon-free) — paired SOP with hybrid cadence ratified inline.
- `scripts/peopl_agentic_knowledge_test.py` (150 lines, zero framework deps) — paired runbook for the agentic-ops SOP per Rule 1.
- `docs/references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md` (143 lines, `access_level: 3` ratified inline, jargon-free) — Ethics-side red-lines anchor with 8 forbidden actions.
- `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/p3a-pause-record-2026-05-15.md` (this file) — pause record.

### Files modified (5)

- `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md` — 3 new rows for the three new canonicals.
- `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv` — 2 new rows: `tbi_peopl_dtp_agentic_ops_mtnce_001` (`scheduled` monthly) + `tbi_peopl_dtp_agentic_ethics_boundaries_001` (`gated_operator` annual with TODO marker).
- `scripts/validate_process_list_pairing.py` — extended runbook discovery glob with `peopl_agentic*.py`.
- `CHANGELOG.md` — Unreleased entry for P3a.
- `docs/wip/planning/79-people-manifesto-and-pattern-library/files-modified.csv` — 9 P3a rows appended.

### Validators run (all PASS)

- `py scripts/validate_hlk.py` → **OVERALL: PASS** (governs SOP frontmatter, language frontmatter, decision-register sync, all per-canonical validators).
- `py scripts/validate_design_pattern_registry.py --jargon-scan` → **PASS — no forbidden tokens in People canonicals** (5 People-area canonicals scanned including the 3 new P3a canonicals).
- `py scripts/validate_design_pattern_registry.py` (registry mode) → **PASS** (12 rows × 15 cols; no regression from P2).
- `py scripts/validate_process_list_pairing.py` → **PASS** (the two new rows pair correctly: agentic ops row paired with `peopl_agentic_knowledge_test.py` after glob extension; ethics-boundaries row paired-deferred via TODO marker per `D-IH-72-W` feature-flag pattern).

## Documentary evidence

### Decisions encoded

- **D-IH-79-F** (round 3 — AI governance refined: jargon-side to Tech Lab, clarity-side to People, red-lines to Ethics) — operationalised via the three new canonicals; the People doctrine names the *what* and *why*, the SOP names the cadence, the Ethics anchor names the *forbidden*. The Tech Lab landscape (P3b) will name the *how*.
- **D-IH-79-L** (round 3 — Strand C P3a/P3b split) — P3a closes here; P3b is the sibling phase.
- **D-IH-79-N** (anti-jargon drift gate) — mechanically enforced; the new canonicals were drafted to pass the jargon scan (not retrofitted; the pattern took on first attempt).

### Inline-ratify gate (single AskQuestion call, three batched questions)

The plan's P3a deliverable (f) called for an inline-ratify gate on Ethics canonical access level + SOP cadence + ethics review cadence. One `AskQuestion` was posted with three questions; operator answered all three in batch (per `akos-inline-ratification.mdc` pattern; not a real-stop pause). Outcomes:

| Question | Operator answer | Authored result |
|:---|:---|:---|
| Ethics canonical access level | "level-2-internal" with operator framing "red lines apply to everyone, so everyone should be able to read them" | Mapped operator intent to `access_level: 3` (Internal per `access_levels.md`) — the integer that matches "all role-owners read" semantics. The AskQuestion option label conflated levels 2 and 3; the canonical now carries an explicit ratification note explaining the mapping. |
| Knowledge-test cadence | hybrid: event_triggered + monthly ("covers high-work and idle moments") | SOP and process_list row carry primary `scheduled` monthly + secondary `event_triggered` on substantive canonical revision. SOP §1 explicitly explains the two-trigger pattern. |
| Ethics review cadence | hybrid: event_triggered + annual ("stable but not as rigid as conservative non-applicable policies") | Ethics canonical and process_list row carry primary `gated_operator` annual + secondary `event_triggered` on red-line crossing or sibling-canonical revision. Ethics §4 explicitly explains the two-trigger pattern. |

The `cadence_secondary` field is documented in the SOP/canonical bodies because the `process_list.csv` schema does not have a `cadence_secondary` column today; the Cursor rule `akos-executable-process-catalog.mdc` Rule 3 names this column as canonical, so a successor initiative may add it to the CSV schema. For now, primary cadence is canonical in the CSV and secondary is documented in the SOP/canonical body.

### Cross-canon link integrity

- **People doctrine** ↔ **Ethics anchor** ↔ **Tech Lab landscape (forward)**: the three canonicals form a triangle. People doctrine §6 cross-references both; Ethics anchor §2 + §5 cross-references both; the Tech Lab landscape (P3b deliverable) will cross-reference back.
- **People doctrine** ↔ **People manifesto** (P1): doctrine §1 explicitly grounds itself in `HOLISTIKA_ORGANISING_DOCTRINE.md` and frames agentic-as-DoD-recursive (the recursive pattern from `akos-people-discipline-of-disciplines.mdc` rule 2).
- **People doctrine** ↔ **design pattern library** (P2): doctrine §5 references `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` for cross-area pattern reuse.
- **SOP** ↔ **runbook**: paired per Rule 1; SOP cites runbook path; runbook docstring cites SOP path; both cite the process_list row by item_id.
- **Ethics anchor** ↔ **ETHICAL_AUTOMATION_POSTURE.md** (I70 P9): sibling Ethics anchors; the two read together (posture + per-action rules).

### CHANGELOG entry

CHANGELOG.md `[Unreleased]` section carries a comprehensive P3a entry naming all five files created, the two process_list rows, the three PRECEDENCE rows, and the verification checklist.

## Pre-next-phase self-checkpoint

### What's outstanding (not P3a; downstream)

- **P3b** — Tech Lab landscape canonical at `Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md` + `SOP-TECH_AGENTIC_INFRA_001.md`. The People canonicals already cross-reference this path. P3b will land the canonical that the cross-references point to.
- **P4** — Strand D cross-area breakthrough propagation SOP. The People doctrine and the SOP both cross-reference this future SOP path.
- **P5** — Strand E orphan inventory + housekeeping.
- **P6** — Strand F process_list 8th column `inherited_pattern_id` FK extension. The agentic ops process_list row will be eligible to declare `pattern_id` parentage at P6 (paired_sop_runbook pattern is the most likely match).
- **P7** — UAT + integration verification.
- **P8** — closure.

### What's not blocking

- The `cadence_secondary` field is documented in the SOP/canonical bodies, not the CSV schema. A successor initiative can mint the column without breaking P3a artifacts.
- The Ethics canonical points to the Tech Lab landscape (P3b deliverable) as a future cross-reference. Until P3b lands, the link will appear as a dead link in P3a → P3b interregnum. Acceptable; cross-link integrity is best-effort during phased landings.

## Operator approval checklist

Please confirm before P3b/P4:

1. **People-side AI doctrine canonical lands as expected** — read `HOLISTIKA_AGENTIC_DOCTRINE.md` §1 (operating story grounding), §3 (Agent-in-Charge frame), §6 (cross-references). Confirm the doctrine reads in the operator's voice without jargon.
2. **Ethics anchor access level is correct at level 3 (Internal — all role-owners read)** — confirm the mapping from "red lines apply to everyone" framing to integer access level 3 per `access_levels.md` is what was intended.
3. **Hybrid cadence design is correct** — knowledge-test = monthly baseline + event_triggered; ethics-review = annual baseline + event_triggered. Confirm both hybrids match the operator's idle/high-work coverage intent.
4. **Madeira role-class footnote is preserved verbatim** — `HOLISTIKA_AGENTIC_DOCTRINE.md` §4 names Madeira as a named role-class internal to People (not a product, not jargon). Confirm the framing is correct.
5. **Jargon-scan still clean** — five People-area canonicals now in scope (manifesto + pattern library + agentic doctrine + agentic-ops SOP + ethics anchor); zero forbidden tokens. Confirm the discipline holds.
6. **Process_list rows are correctly classified** — `tbi_peopl_dtp_agentic_ops_mtnce_001` is a People Operations Manager row at `hol_peopl_ws_2`; `tbi_peopl_dtp_agentic_ethics_boundaries_001` is an Ethics Advisor row at `hol_peopl_ws_6`. Confirm the routing.
7. **No new `baseline_organisation` row required** — agentic governance lands within existing People role responsibilities (People Operations Manager + Ethics Advisor + System Owner co-author the doctrine; no new role needed). Confirms `D-IH-79-K` (KB-stewardship absorbed into manifest, no new role).

## First-three-actions for P3b (next phase)

1. Author `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md` — Tech Lab framework landscape (jargon-bearing per `D-IH-79-F`; legitimate stack vocabulary scoped to Tech Lab subtree per `D-IH-79-M`). Anchor the conventional vocabulary the People doctrine deliberately avoids.
2. Author `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md` — paired SOP for the framework landscape.
3. Register both in `PRECEDENCE.md`; verify the People canonical cross-links resolve once the Tech Lab canonicals exist.

P3b does **not** apply the anti-jargon drift gate to the Tech Lab subtree (per `D-IH-79-N`; jargon scope is People-only).
