---
language: en
status: review
canonical: true
role_owner: RevOps Lead
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-T
methodology_version_at_review: v3.0
companion_to:
  - REVOPS_AREA_CHARTER.md
  - dimensions/REVOPS_ADAPTER_REGISTRY.csv
---

# SOP-PEOPLE_ENGAGEMENT_HANDOFF_001 — Engagement signed → People Operations onboarding handoff

> Authored I72 P9 per `D-IH-72-T` (MarTech adapter breadth) + `D-IH-72-O` (Normalized Adapter Pattern). Codifies how the **people_engagement_handoff** adapter routes engagement-signed events to People Operations onboarding flows. Cross-link to I73 People Operations Lead activation (forward-charter).

## 1. Purpose

Bridge engagement signing to onboarding handoff so headcount + role-mapping happens deterministically when an engagement starts (vs. ad hoc later).

## 2. Scope

In scope: any engagement transitioning to `status=active` that requires Holistika headcount allocation OR external collaborator onboarding (BD collaborator + subcontract partner + service prospect personas). Out of scope: HR systems implementation (I73 follow-up).

## 3. Steps

### 3.1 Trigger

Event: ENGAGEMENT_REGISTRY.csv row transition to `status=active`.

### 3.2 Role-allocation surface

Identify roles required from BASELINE_ORGANISATION.csv to deliver the engagement; check status=active for each.

### 3.3 Onboarding handoff

When the engagement requires gated/inactive roles or external collaborators, hand off to People Operations Lead (target I73 for full SOP); log handoff in PMO_HUB_LOG.

## 4. Acceptance criteria

- **AC-HUMAN**: RevOps Lead identifies required roles + hands off via PMO_HUB_LOG entry.
- **AC-AUTOMATION**: `validate_adapter_registries.py` PASS on people_engagement_handoff row.

## 5. Cross-references

- Adapter row: REVOPS_ADAPTER_REGISTRY.csv (people_engagement_handoff).
- Forward-link: I73 People Operations Lead activation.
- Decisions: D-IH-72-T, D-IH-72-O, D-IH-72-K.
