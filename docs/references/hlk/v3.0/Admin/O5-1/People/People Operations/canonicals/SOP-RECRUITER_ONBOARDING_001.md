---
language: en
status: active
canonical: true
role_owner: People Operations Manager
area: People
entity: Holistika
intellectual_kind: sop
authored: 2026-05-15
last_review: 2026-05-15
process_list_id: tbi_peopl_dtp_recruiter_onboarding_001
paired_runbook: scripts/peopl_recruiter_onboarding_checklist_stub.py
---

# SOP-RECRUITER_ONBOARDING_001 — Recruiter counterparty onboarding brief (bootstrap)

## 1. Purpose

When a **hiring window** opens and Holistika engages an external **recruiter** counterparty (cold inbound or shortlisted firm), People Operations Manager runs a **minimal onboarding brief** so sourcing scope, channels, engagement-model presets, and SOC posture are explicit **before** interviews or candidate submission loops begin. Aligns [`INTELLIGENCEOPS_REGISTER.csv`](../../../Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv) row `IO-REC-PLACEHOLDER-001` (`target_class=recruiter`) with executable People Ops doctrine per **`D-IH-72-K`**.

## 2. Scope

Bootstrap SOP for **event-triggered** recruiter engagement (`process_list.csv` **`tbi_peopl_dtp_recruiter_onboarding_001`**). Covers brainstorming + RACI mock + checklist hand-off to classification/intake (`tbi_peopl_dtp_engagement_model_classification_001`). Does **not** replace full vendor diligence or Legal template selection when contracts exceed standard contingent-search clauses.

## 3. RACI (mocked for bootstrap)

| Role | Responsibility |
|:-----|:---------------|
| **R — People Operations Manager** | Runs brief; records outputs in wip recruiter engagement record path cited on IntelligenceOps row; selects `engagement_model_id` presets. |
| **A — CPO** | Approves role slate urgency + recruiter mandate when People Ops escalates (policy-heavy searches). |
| **C — Legal Counsel** | Reviews engagement letter / fee schedule when non-standard IP or exclusivity appears. |
| **I — Founder** | Optional calibration on exec-search mandates; sole-investor context stays private-register unless recruiter contract requires disclosure. |

## 4. Brainstorming checklist (run before first candidate submission)

1. **Roles-needed** — titles, seniority bands, must-have vs nice-to-have skills (tie to backlog / roadmap hints only; no invented reqs).
2. **Urgency** — fill-window vs exploratory; hiring-manager availability for screens.
3. **Sourcing channel** — **own-site / careers inbox** vs **third-party portal** (ATS integration posture note only).
4. **engagement_model_id presets** — map contingent vs retained vs hybrid to [`ENGAGEMENT_MODEL_REGISTRY.csv`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) rows (`hourly_consultant`, `milestone_consultant`, or outsourced-helper-adjacent flows); intake row updates [`ENGAGEMENT_REGISTRY.csv`](../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) when minted.
5. **SOC for outsourced / portal-mediated recruiters** — follow **`D-IH-73-E`** posture when recruiter operates like low-trust outsourced helper (scoped artifacts; methodology tutoring off); reference [`SOP-ENGAGEMENT_PAYROLL_OPS_001.md`](SOP-ENGAGEMENT_PAYROLL_OPS_001.md) outsourced-helper clauses.

## 5. Outputs

- Engagement record markdown at path pattern from IntelligenceOps **`output_artifact`** cell (`docs/wip/research/recruiter/<slug>-engagement-record.md`).
- Updated recruiter reliability grade note (still defaults **D** until Holistika-domain signal strengthens per FM 2-22.3 scaffolding).

## 6. Failure modes

- Recruiter insists on unrestricted KB access — **deny** or escalate to Legal + Ethics; downgrade to work-product-only channels.

## 7. Cross-references

- Engagement-folder doctrine: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §1 / §3–§4 (`Think Big/Clients/_engagement-template/` inheritance).
- Hiring classification downstream: [`SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md`](SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md).
- Runbook: [`scripts/peopl_recruiter_onboarding_checklist_stub.py`](../../../../../../../../scripts/peopl_recruiter_onboarding_checklist_stub.py).
