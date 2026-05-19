---
language: en
sop_id: SOP-EXTERNAL_RENDER_GATE_PROMOTION_001
title: External-render trail gate promotion and demotion runbook
area: Tech
role_owner: System Owner
co_owner_role: Brand & Narrative Manager
status: active
version: 1.0
inception: 2026-05-19
last_review: 2026-05-19
linked_initiative: INIT-OPENCLAW_AKOS-86
linked_decisions:
  - D-IH-86-P (external-render discipline canonization)
  - D-IH-86-Q (Wave F INFO-to-FAIL gate promotion; ratified at this SOP mint)
canonical_dependencies:
  - .cursor/rules/akos-external-render-discipline.mdc
  - .cursor/skills/external-render-craft/SKILL.md
  - scripts/validate_external_render_trail.py
  - scripts/validate_locale_orthography.py
  - docs/wip/planning/_trackers/external-render-pending-tracker.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
governance_rules:
  - ".cursor/rules/akos-executable-process-catalog.mdc (Rule 1: SOP+runbook pairing — this SOP is the human-readable contract; scripts/validate_external_render_trail.py is the executable runbook)"
  - ".cursor/rules/akos-external-render-discipline.mdc (RULE 6 INFO-to-FAIL ramp + RULE 7 channel-touchpoint axis; this SOP operationalises both promotions)"
  - ".cursor/rules/akos-governance-remediation.mdc (HLK compliance governance — this SOP touches no canonical CSV; process_list.csv row deferred to a follow-up tranche per SOP-META order)"
  - ".cursor/rules/akos-planning-traceability.mdc (per-initiative file-changes CSV must record additions or changes when promote/demote is exercised)"
methodology_version: v3.0
paired_runbook: scripts/validate_external_render_trail.py
---

# SOP-EXTERNAL_RENDER_GATE_PROMOTION_001 — External-render trail gate promotion and demotion runbook

## 1 — Purpose

The external-render trail validator [`scripts/validate_external_render_trail.py`](../../../../../../../../scripts/validate_external_render_trail.py) is the mechanical drift gate that enforces [`akos-external-render-discipline.mdc`](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) — every external-tagged surface (J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO) must carry a paired render artifact (PDF / Web / ERP / Mail / Slide / Broadcast) or an entry in the render-pending tracker.

The validator runs at one of two postures:

- **INFO (advisory)**: emits findings but never fails the release gate. This is the rule-mint default per RULE 6 backfill posture — the validator surfaces gaps without blocking CI while the operator + agents work through the backfill.
- **FAIL (strict)**: missing render trails fail the release gate. Promotion to strict happens once the pending tracker reaches zero entries (or operator explicitly ratifies the promotion via a `D-IH-86-*` decision row).

This SOP is the operator-facing canonical for **promoting** the gate from INFO to FAIL, **demoting** it back to INFO when a regression blocks an urgent commit, and the **pre-flight + rollback** procedures around both transitions. The paired runbook is the validator script itself — running it with `--strict` is the mechanical promotion action; the surrounding ratification + commit hygiene is what this SOP codifies.

> Codifies decision **D-IH-86-Q** (Wave F INFO-to-FAIL gate promotion; ratified at second axis-2 ratify gate 2026-05-19): the validator passed in strict + strict-freshness modes at the rule-mint commit (Wave E) + the Tier-1 paired-runbook commit (665a077). Wave F's promotion is the formal close-out of the backfill ramp.

## 2 — Scope

In scope:

- Flipping `validate_external_render_trail` between INFO and FAIL in [`scripts/release-gate.py`](../../../../../../../../scripts/release-gate.py) and [`config/verification-profiles.json`](../../../../../../../../config/verification-profiles.json).
- Authoring the decision register row that records the promotion or demotion in [`DECISION_REGISTER.csv`](../../../../People/Compliance/canonicals/DECISION_REGISTER.csv).
- Updating [`akos-external-render-discipline.mdc`](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) RULE 6 to record the closure date when the promotion happens.
- Adding a closure preamble to [`external-render-pending-tracker.md`](../../../../../../../../docs/wip/planning/_trackers/external-render-pending-tracker.md) so future readers see the promotion lineage.
- Running the verification matrix (validator strict, full test suite, release-gate end-to-end) and recording outcomes before commit.

Out of scope:

- Authoring new render scripts (covered by [`SOP-RENDERING_PIPELINE_GOVERNANCE_001`](SOP-RENDERING_PIPELINE_GOVERNANCE_001.md)).
- Authoring new external-tagged surfaces (covered by `.cursor/skills/external-render-craft/SKILL.md` Surface 0 lookup).
- Channel-touchpoint registry mint or promotion (covered by [`SOP-CHANNEL_TOUCHPOINT_MAINTENANCE_001`](../../../../People/People%20Operations/canonicals/SOP-CHANNEL_TOUCHPOINT_MAINTENANCE_001.md) when minted).

## 3 — When to promote (INFO → FAIL)

Promote when **all** of the following are true:

1. **Mechanical readiness**: `py scripts/validate_external_render_trail.py --strict --strict-freshness` exits 0. Re-run after a fresh `git status` to confirm no recently-edited surfaces tip the count.
2. **Tracker emptiness OR operator override**: either [`external-render-pending-tracker.md`](../../../../../../../../docs/wip/planning/_trackers/external-render-pending-tracker.md) carries zero open entries, OR the operator explicitly ratifies an exceptional promotion (e.g., "promote now even with N tracker entries; downgrade lane via env var").
3. **Operator ratification**: a fresh `D-IH-86-*` decision row exists in [`DECISION_REGISTER.csv`](../../../../People/Compliance/canonicals/DECISION_REGISTER.csv) capturing the promotion decision + the ratifying evidence sha (latest commit + validator output).
4. **No active regression on a sister validator**: pre-existing FAILs on unrelated validators (e.g., [`validate_brand_voice_register.py`](../../../../../../../../scripts/validate_brand_voice_register.py) per I71 P1) do not block this promotion. Note them as out-of-scope in the decision row.

Promote when these are true; defer when any is false.

## 4 — Promotion procedure (5 steps)

### 4.1 — Pre-flight

Run, in order, from repo root:

```powershell
py scripts/validate_external_render_trail.py --strict --strict-freshness
py scripts/validate_locale_orthography.py
py scripts/validate_hlk.py
py -m pytest tests/test_external_render_trail.py tests/test_validate_locale_orthography.py -v
```

Every command must exit 0 (except `validate_locale_orthography.py` which is advisory by design — INFO output is acceptable as long as exit is 0).

### 4.2 — Ratify the decision

Append a row to [`DECISION_REGISTER.csv`](../../../../People/Compliance/canonicals/DECISION_REGISTER.csv) with `decision_id=D-IH-86-Q` (or next available `D-IH-86-*`), `decision_kind=ratification`, `links` citing this SOP + the validator + the latest commit sha as ratifying evidence. The decision row is the SSOT signal that the rule's RULE 6 ramp has closed.

### 4.3 — Flip the gate

Two edits, atomic in the same commit:

(a) In [`config/verification-profiles.json`](../../../../../../../../config/verification-profiles.json), modify the `validate_external_render_trail` step's `argv` to include `--strict` (and optionally `--strict-freshness`):

```json
{
  "id": "validate_external_render_trail",
  "description": "<updated to record the closure date + decision ID>",
  "argv": ["scripts/validate_external_render_trail.py", "--strict", "--strict-freshness"]
}
```

(b) In [`scripts/release-gate.py`](../../../../../../../../scripts/release-gate.py), modify `run_external_render_trail_validation()` to invoke the validator with `--strict` (and optionally `--strict-freshness`), and change the row severity from `INFO` to `PASS / FAIL` (based on `result.success`). The pattern mirrors [`run_brand_voice_register_validation()`](../../../../../../../../scripts/release-gate.py) which promoted from INFO to strict-default at I66 P5 increment 3.

### 4.4 — Update the rule + tracker

(c) In [`.cursor/rules/akos-external-render-discipline.mdc`](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) RULE 6, append a one-line closure note citing the decision row + closure date:

```text
Closure: Promoted to FAIL at 2026-05-19 per D-IH-86-Q (Wave F closure of RULE 6 backfill ramp).
```

(d) In [`external-render-pending-tracker.md`](../../../../../../../../docs/wip/planning/_trackers/external-render-pending-tracker.md), add a closure preamble at the top of the file recording the date + decision ID + verification matrix outcomes. The tracker stays in repo for historical reference even at zero entries.

### 4.5 — Verify + commit

Re-run the verification matrix from §4.1, then run the full release gate end-to-end:

```powershell
py scripts/release-gate.py
```

Confirm the External-render-trail line now reports `[PASS]` or `[FAIL]` (not `[INFO]`). Commit all four files in one wave-scoped commit. Reference the decision row in the commit message body.

## 5 — Demotion procedure (FAIL → INFO; emergency only)

Demotion is the rollback path when a strict gate blocks an urgent commit (e.g., a regression in a sister rule introduced a render-trail gap on an external surface). Use sparingly.

Two paths:

### 5.1 — Soft demotion (preferred; env var only)

Set environment variable `AKOS_RENDER_TRAIL_STRICT=0` (or unset `=1` in CI). No code changes required. CI runs return to advisory mode for the duration of the env-var override. Re-flip immediately after the urgent commit lands.

Mirror precedent: [`AKOS_BRAND_BASELINE_REALITY_SOFT=1`](../../../../../../../../scripts/release-gate.py) for the BBR drift gate (per D-IH-89-E hot-fix lane).

### 5.2 — Hard demotion (commit-level revert)

Required when env-var override is insufficient (e.g., CI doesn't honour the env var for some reason, or the validator itself misbehaves under strict mode). Revert the §4.3 + §4.4 edits in a fresh commit; append a `D-IH-86-*` decision row documenting the demotion + remediation plan + ETA for re-promotion. Add a temporary entry in [`external-render-pending-tracker.md`](../../../../../../../../docs/wip/planning/_trackers/external-render-pending-tracker.md) describing the surface or class of surfaces that blocked promotion.

## 6 — Verification + acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 §"Acceptance criteria":

- **`acceptance_criteria_human` (this SOP)**: an operator (or AIC acting as System Owner) can run the §4 procedure end-to-end without invoking the runbook directly — reading this SOP front-to-back, then executing the §4.1 commands, then performing the §4.3 + §4.4 edits, then running §4.5 verification. The SOP carries enough detail to act without the script.
- **`acceptance_criteria_automation` (paired runbook)**: `scripts/validate_external_render_trail.py --strict --strict-freshness` runs unattended in CI per the [`config/verification-profiles.json`](../../../../../../../../config/verification-profiles.json) `pre_commit` profile + the [`scripts/release-gate.py`](../../../../../../../../scripts/release-gate.py) end-to-end gate. Exit code 0 = PASS; exit code 1 = FAIL. No operator interaction required at runtime.

## 7 — Process_list.csv row (deferred)

Per [`akos-governance-remediation.mdc`](../../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance — SOP-META order", this SOP does **not** mint a `process_list.csv` row at its inception commit (no `process_list.csv` tranche was operator-approved for Wave F). The row will be added in a follow-up tranche with one of the next operator-approved CSV gates. Suggested `item_id`: `env_tech_prc_extrender_gate_001`, area `Tech`, role_owner `System Owner`, cadence `gated_operator`, paired with this SOP path + the validator runbook path.

When the row lands, this SOP graduates from `partial` to `governed` governance class per the [`RENDERING_PIPELINE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/) ladder (mirroring [`SOP-RENDERING_PIPELINE_GOVERNANCE_001`](SOP-RENDERING_PIPELINE_GOVERNANCE_001.md) §4.1 definitions, adapted to the gate-promotion process).

## 8 — Cross-references

- [`akos-external-render-discipline.mdc`](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) — the *when* rule this SOP operationalises (RULE 6 ramp).
- [`.cursor/skills/external-render-craft/SKILL.md`](../../../../../../../../.cursor/skills/external-render-craft/SKILL.md) — the *how* skill for picking the right render surface per audience × channel × language × objective.
- [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 — the SOP+runbook pairing contract.
- [`SOP-RENDERING_PIPELINE_GOVERNANCE_001`](SOP-RENDERING_PIPELINE_GOVERNANCE_001.md) — sister SOP governing the full rendering-pipeline catalog.
- [`SOP-CICD_BASELINE_001`](SOP-CICD_BASELINE_001.md) — sister SOP under the same System Owner area; precedent for `--strict` env-var promotion patterns.
- D-IH-86-P + D-IH-86-Q in [`DECISION_REGISTER.csv`](../../../../People/Compliance/canonicals/DECISION_REGISTER.csv).
