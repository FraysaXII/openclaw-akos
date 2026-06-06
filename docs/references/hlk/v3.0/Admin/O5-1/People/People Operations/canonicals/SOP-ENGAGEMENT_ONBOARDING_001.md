---
language: en
status: active
canonical: true
role_owner: People Operations Manager
area: People
entity: Holistika
intellectual_kind: sop
authored: 2026-05-15
last_review: 2026-05-16
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
process_list_id: tbi_peopl_dtp_engagement_lifecycle_routing_001
paired_runbook: scripts/peopl_engagement_lifecycle_routing.py
companion_to:
  - SOP-ENGAGEMENT_ONBOARDING_001.addendum.md
---

# SOP-ENGAGEMENT_ONBOARDING_001 — Onboarding + lifecycle routing (parameterized)

## 1. Purpose

Given `engagement_model_id`, execute onboarding steps (access, workspace shape, cadence hooks) and route lifecycle subprocesses (hiring intake already classified → onboarding execution here). **People Operations Manager** accountable.

## 2. Scope

Holistika engagements mirrored under Think Big engagement folders per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md):

Covers **Engagement lifecycle routing at intake** (`process_list.csv` `tbi_peopl_dtp_engagement_lifecycle_routing_001`) plus onboarding execution per `engagement_model_id`. Also references **Apprentice curriculum assignment** (`tbi_peopl_dtp_apprentice_curriculum_assignment_001`) when routing `eng_model_apprentice_learner`.

- §1 **Four-channel persistence** (git / Drive / SQL mirror / HLK-ERP) — record where authoritative artifacts live.
- §3–§4 **Skeleton + `_engagement-template/`** — copy-target discipline before filing operator artefacts.

Out of scope: RevOps revenue recognition (see RevOps spine); FINOPS fact inserts.

## 3. Inputs

- Classified engagement (`engagement_model_id`).
- [`ENGAGEMENT_MODEL_REGISTRY.csv`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) defaults (`access_level_default`, `knowledge_access_level`).
- Apprentice flows — [`LEARNING_CHARTER.md`](../../Learning/canonicals/LEARNING_CHARTER.md) + [`HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md`](../../Learning/canonicals/curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md) + [`LEARNING_OPS_BACKLOG.csv`](../../Learning/canonicals/dimensions/LEARNING_OPS_BACKLOG.csv).

## 4. Steps

1. Provision workspace folders + file-tracking markers per blueprint (internal vs customer pack separation unchanged).
2. Apply access tier from registry + [`access_levels.md`](../../Compliance/canonicals/access_levels.md).
3. Route subprocess runners:
   - Payroll-heavy monitors → [`SOP-ENGAGEMENT_PAYROLL_OPS_001.md`](SOP-ENGAGEMENT_PAYROLL_OPS_001.md).
   - Exit / round reviews → [`SOP-ENGAGEMENT_OFFBOARDING_001.md`](SOP-ENGAGEMENT_OFFBOARDING_001.md).
4. For apprentices → invoke curriculum assignment runbook [`scripts/peopl_engagement_apprentice_curriculum_assign.py`](../../../../../../../../scripts/peopl_engagement_apprentice_curriculum_assign.py).

## 5. Outputs

- Engagement README updated with model id + SOC summary (internal register wording acceptable).

## 6. Failure modes

- Missing template copy — halt until `_engagement-template/` sync completes.

## 7. Cross-references

- Runbook: [`scripts/peopl_engagement_lifecycle_routing.py`](../../../../../../../../scripts/peopl_engagement_lifecycle_routing.py).
