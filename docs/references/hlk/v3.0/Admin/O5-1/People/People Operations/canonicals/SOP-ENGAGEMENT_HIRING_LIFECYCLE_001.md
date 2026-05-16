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
process_list_id: tbi_peopl_dtp_engagement_model_classification_001
paired_runbook: scripts/peopl_engagement_model_classification_intake.py
companion_to:
  - SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.addendum.md
---

# SOP-ENGAGEMENT_HIRING_LIFECYCLE_001 — Hiring / intake classification by engagement_model_id

## 1. Purpose

When a new engagement instance is minted in [`ENGAGEMENT_REGISTRY.csv`](../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv), assign exactly one `engagement_model_id` slug from [`ENGAGEMENT_MODEL_REGISTRY.csv`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv). **People Operations Lead** executes with Legal/Finance handoffs as needed.

## 2. Scope

Classification + legal-template routing + SOC posture selection per registry row. Covers **Per-engagement classification at intake** (`process_list.csv` `tbi_peopl_dtp_engagement_model_classification_001`). Does **not** duplicate counterparty economics SSOT — reference [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) for payout entities.

## 3. Inputs

- Registry rows (`eng_model_*`) with `retribution_pattern`, `soc_posture`, `access_level_default`, `ip_clause_class`.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §1 / §3–§4 — engagement-folder doctrine (`Think Big/Clients/_engagement-template/` vs `Think Big/Advisers/_engagement-template/`).

## 4. Steps

1. Identify engagement shape (consultant / apprentice / investor / outsourced helper / operator_self).
2. Map to `engagement_model_id`; record rationalised note in engagement README frontmatter (internal).
3. Select templates per registry `default_legal_template` cells; attach IP + confidentiality clauses matching `ip_clause_class`.
4. For `eng_model_outsourced_helper`, enforce **work-product-only** handoff per `D-IH-73-E` — no methodology tutoring in scoped surfaces.

## 5. Outputs

- ENGAGEMENT_REGISTRY row carries non-null `engagement_model_id` when operator authorises backfill (nullable until UAT per `D-IH-73-N`).
- Engagement folder instantiated from correct `_engagement-template/` skeleton.

## 6. Failure modes

- Ambiguous multi-class pattern — escalate to PMO + Ethics if SOC posture conflicts with operator narrative.

## 7. Cross-references

- Runbook: [`scripts/peopl_engagement_model_classification_intake.py`](../../../../../../../../scripts/peopl_engagement_model_classification_intake.py).
- Pair downstream: [`SOP-ENGAGEMENT_ONBOARDING_001.md`](SOP-ENGAGEMENT_ONBOARDING_001.md).
