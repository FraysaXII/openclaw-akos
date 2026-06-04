---
title: SOP — Engagement Integration Scaffold
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Lead
co_authors:
  - Data Architect
  - System Owner
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_decision_id: D-IH-93-I
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-I
  - D-IH-93-D
status: active
register: internal
linked_canonicals:
  - DATA_BI_GOVERNANCE.md
  - DATA_INTEGRATION_PLANE.md
  - dimensions/RPA_ADAPTER_REGISTRY.csv
  - dimensions/BI_CONSUMER_REGISTRY.csv
  - dimensions/DATA_CONTRACT_REGISTRY.csv
linked_runbooks:
  - scripts/bi_integration_readiness_check.py
linked_processes:
  - hol_data_dtp_engagement_integration_scaffold_001
cadence: event_triggered
cadence_trigger: new engagement demo spec OR client BI/RPA ask OR Stream A/B/C ambiguity
---

# SOP — Engagement Integration Scaffold

## Purpose

Convert customer-pack **demo specs** (Power Automate / Power BI / Excel patterns) into
**governed internal artefacts** before build starts — preventing the SUEZ pain pattern
(demos exist without adapter rows, contracts, or runbooks).

## Scope

- Engagements with external-translated integration specs under `Think Big/Clients/`.
- Stream A (client tenant), Stream B (Holistika), Stream C (hybrid) declarations.
- **Out of scope:** implementing client-tenant flows inside AKOS repo.

## Workflow (7 steps)

1. **Classify streams** — per `DATA_BI_GOVERNANCE.md` §4 (A/B/C).
2. **Inventory demo surfaces** — list each trigger, store, UI, and report target.
3. **Mint or update data contract** — one row per producer × `data_surface`.
4. **Mint or update RPA adapter row** — `RPA_ADAPTER_REGISTRY.csv` with status + SOP linkage.
5. **Mint or update BI consumer row** — `BI_CONSUMER_REGISTRY.csv` with tier + `component_id`.
6. **Matrix tranche** — ensure `COMPONENT_SERVICE_MATRIX` row exists; tag `integration_pattern`.
7. **Run readiness check** — `py scripts/bi_integration_readiness_check.py --self-test`.

## Dual-path checklist (Stream A vs B)

| Demo element | Stream A (client) | Stream B (Holistika) |
|:---|:---|:---|
| Referential data | Client SharePoint/Excel | Git CSV + optional mirror |
| Trigger | Power Automate | Edge Function / pg_net |
| Validation UI | Power Apps | HLK-ERP panel |
| Reporting | Power BI | ERP Recharts + export view |

Operator must ratify which stream is **primary** for each engagement capability.

## Acceptance criteria

- AC-HUMAN: Data Governance Lead signs checklist with stream declaration documented.
- AC-AUTOMATION: `bi_integration_readiness_check.py --self-test` PASS; registry validators PASS.

## Cross-references

- SUEZ worked example: `SOP-DATA_SUEZ_STREAM_B_LIBELLE_001.md`
- Research: `docs/wip/planning/93-data-area-foundation-and-governance/reports/research-platform-component-landscape-2026-06-04.md`
