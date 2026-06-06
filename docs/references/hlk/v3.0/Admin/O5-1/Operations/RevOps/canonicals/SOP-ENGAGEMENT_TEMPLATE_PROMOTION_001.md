---
language: en
status: review
canonical: true
role_owner: PMO + RevOps Manager (forward; activates at P4 per D-IH-72-AC)
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-A
methodology_version_at_review: v3.0
companion_to:
  - dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv
  - REVOPS_AREA_CHARTER.md
  - ../../../People/Compliance/canonicals/process_list.csv
---

# SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001 — Engagement template promotion lifecycle

> Authored I72 P3 per `D-IH-72-A` (P0 charter) + `D-IH-72-F` (sibling registry pattern) + `D-IH-72-AH` (Round 8 Operations/RevOps area charter at P1). Codifies the **scaffold → active** promotion gate for rows in `ENGAGEMENT_TEMPLATE_REGISTRY.csv`. Until a template is `lifecycle_status=active` (with a valid `promotion_decision_id`), it cannot be assigned to a new engagement instance in `ENGAGEMENT_REGISTRY.csv`. This SOP is the **operator-facing canonical**; paired runbook is `scripts/validate_engagement_template_promotion.py` per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1.

## 1. Purpose

Provide a deterministic, evidence-backed promotion gate that prevents `scaffold` templates from being applied to active engagements without operator review. Templates carry contract patterns (billing cadence + value band + duration target + discipline mix) that bind future engagement-instance behavior; promoting a template prematurely propagates downstream errors into engagement contracts.

## 2. Scope

In scope:
- Every row in `ENGAGEMENT_TEMPLATE_REGISTRY.csv` with `lifecycle_status` in `{scaffold, active, deprecated}`.
- Promotion transitions: `scaffold → active`, `active → deprecated`, `deprecated → archived` (latter is canonical-CSV row removal + audit-trail decision id).
- Process row: `tbi_mkt_dtp_revops_template_promotion_001` in `process_list.csv` (operator-gated cadence per `D-IH-72-Q`).

Out of scope:
- Authoring net-new templates (separate SOP at P8 process catalog mint; until then, operator + RevOps Manager author directly into the registry CSV with `lifecycle_status=scaffold`).
- Per-engagement instance lifecycle (governed by `ENGAGEMENT_REGISTRY.csv` + future `SOP-ENGAGEMENT_INSTANCE_LIFECYCLE_001.md` at P10 closing UAT).

## 3. Inputs

- A scaffold template row in `ENGAGEMENT_TEMPLATE_REGISTRY.csv` (current state: `lifecycle_status=scaffold`, `promotion_decision_id=D-IH-72-F` or similar bootstrap pointer).
- At least one active engagement instance in `ENGAGEMENT_REGISTRY.csv` whose shape matches the template (used as the reference instance for promotion evidence).
- Operator availability for the canonical-CSV gate (per `akos-governance-remediation.mdc`).

## 4. Steps

### 4.1 Pre-promotion evidence pack

The role_owner (PMO interim until P4; RevOps Manager post-P4) assembles:

1. **Reference engagement instance(s)**: cite at least one `engagement_id` in `ENGAGEMENT_REGISTRY.csv` whose actual shape (engagement_class + value_band + duration + discipline_mix) matched the template's contract.
2. **Variance report**: any deviation between the template's prescribed shape and the reference instance's actual shape; rationale per deviation.
3. **Risk register entry**: per-template risks (e.g., billing-cadence collisions, contract-kind mismatches) with mitigation posture.
4. **DAMA-DMBOK 2.0 alignment check**: confirm the template's `supabase_mirror` + `panel_slot` + `artifact_path_pattern` cells are wired through the engagement-revenue spine (P7 deliverable; per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 4).

### 4.2 Operator review gate (canonical-CSV gate)

Per `akos-governance-remediation.mdc` HLK governance + canonical-CSV gates:

1. Operator reviews the pre-promotion evidence pack.
2. Operator surfaces a new `D-IH-72-*` (or successor) decision row in `DECISION_REGISTER.csv` codifying the promotion ratification. Decision class: `scope` or `execution` (depends on whether promotion changes the template's prescribed shape).
3. Operator approves the canonical-CSV edit.

### 4.3 CSV mutation

The role_owner (with operator approval) edits the template row:

```diff
- <template_id>,...,scaffold,D-IH-72-F,...
+ <template_id>,...,active,D-IH-72-<new>,...
```

The mutation MUST update `last_review_at`, `last_review_by`, `last_review_decision_id`, `methodology_version_at_review` to reflect the promotion review.

### 4.4 Validator gate

Run the paired runbook per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1:

```
py scripts/validate_engagement_template_promotion.py
```

Expected output: `PASS` with line counts for active / scaffold / deprecated templates. Validator FAILS if any `lifecycle_status=active` template has empty or unresolved `promotion_decision_id`.

### 4.5 Sync gate

Run the HLK aggregate validator + release-gate to confirm no cascading drift:

```
py scripts/validate_hlk.py
py scripts/release-gate.py
```

Both MUST be `PASS / OVERALL: PASS` before commit.

### 4.6 Commit + ratify

Atomic commit message format:
```
i72 promote tmpl_<template_id> to active per D-IH-72-<new> (operator-gated canonical-CSV)
```

Push to `origin/main`. The promotion is then live for any new engagement instance that wants to consume the template.

## 5. Outputs

- `ENGAGEMENT_TEMPLATE_REGISTRY.csv` row updated to `lifecycle_status=active`.
- New `D-IH-72-*` row in `DECISION_REGISTER.csv` ratifying the promotion.
- `validate_engagement_template_promotion.py` PASS.
- `validate_hlk.py` OVERALL PASS.

## 6. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **`acceptance_criteria_human`**: a human or AIC role_owner can run §4.1-§4.6 manually using only the SOP body — no scripts are strictly required for understanding (validator + release-gate are CI gates, not steps in the promotion logic).
- **`acceptance_criteria_automation`**: `validate_engagement_template_promotion.py` fires unattended in CI; release-gate flips OVERALL to FAIL if any active template lacks valid `promotion_decision_id`.

## 7. Failure modes

- **Empty `promotion_decision_id` on `active` template**: validator FAIL; revert mutation, mint decision row, retry.
- **Reference engagement instance does not exist**: cannot collect evidence; either author the instance first OR keep template `scaffold`.
- **Variance too high**: template's prescribed shape diverges materially from reference instance — author template variant (`<template_id>_v2`) instead of promoting `_v1`.
- **DAMA-DMBOK alignment gap**: template's `supabase_mirror` / `panel_slot` not wired into spine — block promotion until P7 RevOps Spine ship OR explicitly mark the template as `forward_charter` (planned future-state operator-decided).
- **Operator unavailable**: gate stays `scaffold` indefinitely. No automated promotion (gated_operator cadence per `akos-executable-process-catalog.mdc` Rule 3).

## 8. Cross-references

- Canonical: [`dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv`](dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv) — the registry this SOP governs.
- Sister canonical: [`../../../People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) — engagement-instance registry (sibling per `D-IH-72-F`; templates here, instances there).
- Parent area charter: [`REVOPS_AREA_CHARTER.md`](REVOPS_AREA_CHARTER.md).
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 1 + 3 + 4 + 5.
- Paired runbook: [`scripts/validate_engagement_template_promotion.py`](../../../../../../../scripts/validate_engagement_template_promotion.py) — agent-facing executable gate.
- Process row: `tbi_mkt_dtp_revops_template_promotion_001` in `process_list.csv` (cadence: `gated_operator`).
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-72-F` (sibling registry pattern), `D-IH-72-N` (process catalog architecture), `D-IH-72-Q` (cadence taxonomy: gated_operator), `D-IH-72-AH` (Round 8 Operations/RevOps area charter at P1).
- Cross-area handoff: Marketing/Reach (qualified-lead handoff) → RevOps template assignment → Account Management/Resonance (per-instance ownership).
