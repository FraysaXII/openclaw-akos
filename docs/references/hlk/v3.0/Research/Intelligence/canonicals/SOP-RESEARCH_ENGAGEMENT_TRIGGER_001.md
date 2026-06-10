---
language: en
status: review
canonical: true
role_owner: Lead Researcher
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-T
methodology_version_at_review: v3.0
companion_to:
  - dimensions/INTELLIGENCEOPS_REGISTER.csv
  - SOP-REGULATOR_RELATIONSHIP_001.md
  - ../../../Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md
---

# SOP-RESEARCH_ENGAGEMENT_TRIGGER_001 — Engagement signed → Research/Intelligence collection trigger

> Authored I72 P9 per `D-IH-72-T` (MarTech adapter breadth: cross-area handoff bridges) + `D-IH-72-O` (Normalized Adapter Pattern). Codifies how the engagement-signing event triggers Research/Intelligence collection updates against `INTELLIGENCEOPS_REGISTER.csv` — keeping HUMINT/OSINT/TECHINT collection contracts in sync with active engagement portfolio.

## 1. Purpose

Bridge engagement signing to research/intelligence collection so:

1. **Counterparty intelligence collection cadence** activates when an engagement with a `competitor_intelligence_target` counterparty signs.
2. **Regulator collection cadence** updates when an engagement under regulator scope (e.g., ENISA NIS2 obligations) activates.
3. **Media counterparty collection** triggers when a media row in INTELLIGENCEOPS_REGISTER becomes engagement-relevant.
4. **Recruiter collection** updates when a hiring engagement spawns recruiter cross-links (cross-link to I73 People Operations follow-up).

## 2. Scope

In scope: any engagement transitioning to `status=active` whose counterparty_org_id resolves to a row in `GOI_POI_REGISTER.csv` that is also referenced by an INTELLIGENCEOPS_REGISTER `target_id`. Out of scope: open-ended OSINT collection for non-engagement-bound targets (covered by SOP-IO_ELICITATION_DISCIPLINE_001.md).

## 3. Steps

### 3.1 Trigger

Event: `ENGAGEMENT_REGISTRY.csv` row transition to `status=active`.

### 3.2 Counterparty resolution

Resolve `counterparty_org_id` → `GOI_POI_REGISTER.ref_id` → INTELLIGENCEOPS_REGISTER `target_id` (when present).

### 3.3 Cadence reactivation

If a matching INTELLIGENCEOPS_REGISTER row exists with `lifecycle_status=dormant`, flip to `active`. If `lifecycle_status` already `active`, increment cadence pull (e.g., scheduled monthly → switch to scheduled bi-weekly while engagement is live).

### 3.4 New row scaffold (when no match)

When no INTELLIGENCEOPS_REGISTER row exists for the counterparty, Lead Researcher considers minting one per `SOP-IO_ELICITATION_DISCIPLINE_001.md` discovery flow. Optional — most engagements do not warrant a register row.

### 3.5 Logging

Log trigger + cadence change to PMO_HUB_LOG with engagement_id + register_id + before/after cadence.

## 4. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **AC-HUMAN**: Lead Researcher executes §3 manually using only this SOP body.
- **AC-AUTOMATION**: `validate_intelligenceops_register.py` PASS + `validate_adapter_registries.py` PASS on REVOPS_ADAPTER_REGISTRY (no dedicated research adapter — handoff routed through revops_dispatch.py per D-IH-72-N catalog architecture).

## 5. Cross-references

- Sister SOPs: [`SOP-REGULATOR_RELATIONSHIP_001.md`](SOP-REGULATOR_RELATIONSHIP_001.md), [`SOP-IO_ELICITATION_DISCIPLINE_001.md`](SOP-IO_ELICITATION_DISCIPLINE_001.md).
- INTELLIGENCEOPS_REGISTER row class scopes: regulator | competitor_intelligence_target | media | recruiter.
- Adapter row context: REVOPS_ADAPTER_REGISTRY.csv entries route engagement events; this SOP describes the Research-side downstream consumption pattern.
- Decisions: D-IH-72-T, D-IH-72-O, D-IH-72-H (sibling INTELLIGENCEOPS_REGISTER.csv).
