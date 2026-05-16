---
language: en
status: active
canonical: true
role_owner: People Operations Lead
area: People
entity: Holistika
intellectual_kind: sop
authored: 2026-05-15
last_review: 2026-05-16
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
process_list_id: tbi_peopl_dtp_engagement_model_registry_mtnce_001
paired_runbook: scripts/peopl_engagement_engagement_model_registry_mtnce.py
companion_to:
  - SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.addendum.md
---

# SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001 — Engagement Model Registry maintenance

## 1. Purpose

Keep [`ENGAGEMENT_MODEL_REGISTRY.csv`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) aligned with the ratified 7-class taxonomy (`D-IH-73-D`) and with sibling [`ENGAGEMENT_REGISTRY.csv`](../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) via `engagement_model_id` FK posture (`D-IH-73-N`). **People Operations Lead** is Data Owner; PMO retains Operations/PMO ownership of engagement instances.

## 2. Scope

In scope: quarterly row review, enum drift detection, historical_examples hygiene, preparing canonical-CSV gate packets when adding a class. Out of scope: inventing new `eng_model_*` slugs without operator-approved `process_list.csv` tranche + pause record.

## 3. Inputs

- [`ENGAGEMENT_MODEL_REGISTRY.md`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.md) — schema + FK rules.
- [`ENGAGEMENT_REGISTRY.md`](../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md) — instance registry spec.
- [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) — payout-side counterparty SSOT (cross-link only; no duplicate counterparty rows here).

## 4. Steps

1. Run `py scripts/validate_engagement_model_registry.py` and confirm PASS.
2. Scan each registry row for stale `historical_examples` prose vs [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) internal codex (do **not** paste restricted prose into external-register surfaces).
3. Verify optional `engagement_model_id` cells in `ENGAGEMENT_REGISTRY.csv` either empty (legacy) or FK-valid against registry slugs.
4. If a net-new class is needed: pause per [`akos-governance-remediation.mdc`](../../../../../../../../.cursor/rules/akos-governance-remediation.mdc); obtain explicit operator approval before CSV edit.

## 5. Outputs

- Validator PASS retained; initiative/decision notes updated when classification changes.
- Optional OPS_REGISTER row when remediation work is tracked.

## 6. Failure modes

- Validator FAIL — stop; file opt-stop-report per governance rule; no prod mirror resync until fixed.
- Mirror drift — canonical CSV wins; investigate sync path.

## 7. Cross-references

- Runbook: [`scripts/peopl_engagement_engagement_model_registry_mtnce.py`](../../../../../../../../scripts/peopl_engagement_engagement_model_registry_mtnce.py).
- Workspace doctrine (customer engagement folder shape reused for People engagements): [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §1 (four-channel persistence), §3–§4 (skeleton + `_engagement-template/` copy targets).
