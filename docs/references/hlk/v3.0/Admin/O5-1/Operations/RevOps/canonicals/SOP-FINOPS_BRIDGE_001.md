---
language: en
status: review
canonical: true
role_owner: RevOps Manager
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
  - dimensions/BILLING_ADAPTER_REGISTRY.csv
  - SOP-REVOPS_QBR_001.md
---

# SOP-FINOPS_BRIDGE_001 — Engagement signing → FINOPS counterparty bridge

> Authored I72 P9 per `D-IH-72-A` (P0 charter), `D-IH-72-L` (Strand D charter), `D-IH-72-T` (MarTech adapter breadth = 6 sibling registries on top of CRM+REVOPS), and `D-IH-72-O` (Normalized Adapter Pattern). Codifies how the **finops_bridge** adapter (active row in `REVOPS_ADAPTER_REGISTRY.csv`) wires engagement signing events to FINOPS counterparty registration so the engagement-revenue spine (P7) carries clean joins.

## 1. Purpose

Establish a deterministic event_triggered flow:

1. **Engagement signed** (event source: ENGAGEMENT_REGISTRY.csv row transition to `status=active`).
2. **FINOPS counterparty validation** (per FINOPS_COUNTERPARTY_REGISTER.csv): ensure a counterparty row exists for the engagement's counterparty_org_id.
3. **Stripe customer link** (when applicable; per holistika_ops.stripe_customer_link existing schema).
4. **finops.registered_fact engagement_id backfill** (per I72 P7 spine): populate engagement_id cell on subsequent revenue facts.

## 2. Scope

In scope: any engagement transitioning to `status=active`. Out of scope: Stripe API direct calls (stays in I19+I20 finops chain).

## 3. Steps

### 3.1 Engagement signed event

Trigger: `ENGAGEMENT_REGISTRY.csv` row insert OR `status` cell flip to `active`.

### 3.2 Counterparty validation

Verify FINOPS_COUNTERPARTY_REGISTER.csv row exists for engagement's counterparty_org_id. If missing, RevOps Manager authors the row + commits per CSV-as-SSOT pattern.

### 3.3 Stripe customer link (when applicable)

If counterparty has Stripe customer_id, verify holistika_ops.stripe_customer_link contains the mapping. If missing, log to operator inbox.

### 3.4 finops.registered_fact backfill

Future revenue facts for this engagement populate engagement_id cell per I72 P7 spine schema.

## 4. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **AC-HUMAN**: RevOps Manager executes §3 steps manually using only this SOP body.
- **AC-AUTOMATION**: `validate_adapter_registries.py` PASS on REVOPS_ADAPTER_REGISTRY.csv finops_bridge row + `validate_revops_spine.py` PASS.

## 5. Cross-references

- Parent: [`REVOPS_AREA_CHARTER.md`](REVOPS_AREA_CHARTER.md).
- Sister SOPs: [`SOP-REVOPS_QBR_001.md`](SOP-REVOPS_QBR_001.md), [`SOP-PEOPLE_ENGAGEMENT_HANDOFF_001.md`](SOP-PEOPLE_ENGAGEMENT_HANDOFF_001.md), [`SOP-LEGAL_TEMPLATE_FIRE_001.md`](SOP-LEGAL_TEMPLATE_FIRE_001.md), [`SOP-MADEIRA_REVOPS_HANDOFF_001.md`](SOP-MADEIRA_REVOPS_HANDOFF_001.md).
- Adapter rows: REVOPS_ADAPTER_REGISTRY.csv (finops_bridge); BILLING_ADAPTER_REGISTRY.csv (stripe).
- Decisions: D-IH-72-T, D-IH-72-O, D-IH-72-M (engagement-revenue spine).
