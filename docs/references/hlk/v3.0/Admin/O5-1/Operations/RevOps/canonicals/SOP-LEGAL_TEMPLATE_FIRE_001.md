---
language: en
status: review
canonical: true
role_owner: Legal Counsel
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
  - dimensions/CONTRACT_ADAPTER_REGISTRY.csv
---

# SOP-LEGAL_TEMPLATE_FIRE_001 — Engagement scope-locked → Legal template fire

> Authored I72 P9 per `D-IH-72-T` + `D-IH-72-O`. Codifies how the **legal_template_fire** adapter routes engagement scope-locked events to legal template instantiation (NDA / MSA / SOW per I66 P3 deliverables).

## 1. Purpose

Bridge engagement scope-lock event to legal template fire so contract artifacts get instantiated deterministically when scope is agreed (vs. blocked deals waiting on legal).

## 2. Scope

In scope: any engagement reaching `status=scope-locked` (or equivalent). Out of scope: per-contract negotiation (Legal Counsel judgment).

## 3. Steps

### 3.1 Trigger

Event: ENGAGEMENT_REGISTRY.csv row transitioning toward signed status; status enum cell signals scope-locked.

### 3.2 Template selection

Per I66 P3 brand template chain: select NDA + MSA + SOW templates appropriate to engagement_class.

### 3.3 Contract adapter dispatch

Use CONTRACT_ADAPTER_REGISTRY.csv active adapter (holistika_contracts internal seed; future docusign/pandadoc external adapters); fire instantiation.

### 3.4 Logging

Log fired template + adapter used + signing turnaround target to PMO_HUB_LOG.

## 4. Acceptance criteria

- **AC-HUMAN**: Legal Counsel reviews fired templates + monitors signing turnaround.
- **AC-AUTOMATION**: `validate_adapter_registries.py` PASS on legal_template_fire row + CONTRACT_ADAPTER_REGISTRY rows.

## 5. Cross-references

- Adapter rows: REVOPS_ADAPTER_REGISTRY.csv (legal_template_fire); CONTRACT_ADAPTER_REGISTRY.csv (3 vendor rows).
- Decisions: D-IH-72-T, D-IH-72-O.
- I66 P3 brand template chain (forward-charter source).
