---
title: SOP — SUEZ Stream B Libellé Generator
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_SUEZ_STREAM_B_LIBELLE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Lead
co_authors:
  - System Owner
  - Data Architect
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_decision_id: D-IH-93-I
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-I
status: active
register: internal
linked_canonicals:
  - DATA_BI_GOVERNANCE.md
  - DATA_INTEGRATION_PLANE.md
  - SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - dimensions/RPA_ADAPTER_REGISTRY.csv
linked_runbooks:
  - scripts/bi_integration_readiness_check.py
linked_processes:
  - hol_data_dtp_engagement_integration_scaffold_001
cadence: event_triggered
cadence_trigger: SUEZ F-05 libellé capability build OR Stream B unblock request
---

# SOP — SUEZ Stream B Libellé Generator (F-05)

## Purpose

Deliver **Holistika-controlled proof** for SUEZ libellé generation (capability F-05)
when client Power Automate is blocked or parallel internal validation is required —
without duplicating the full client tenant build.

## Customer-pack reference

- Demo spec: `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/demo-libelle-generator.customer.fr.md`
- Engagement: `ENG-SUEZ-WEBUY-2026` / `DC-HOL-SUEZ-ENG-FACT-001`

## Stream declaration

| Path | Owner | Status |
|:---|:---|:---|
| **Stream A** — client PA + Power Apps + Power BI | SUEZ DSI / client tenant | Continues in parallel when unblocked |
| **Stream B** — Holistika Edge + ERP panel | HLK Tech Lab | **Primary internal proof** (operator ratified 2026-06-04) |

## Stream B build checklist

1. **Contract:** ensure `DC-HOL-SUEZ-LIBELLE-STAGING-001` active (mirror_table staging).
2. **Adapter:** `holistika_edge` = active; `power_platform` = planned (Stream A).
3. **Referential:** seed libellé rules CSV under engagement git path; optional mirror emit.
4. **Ingress:** Edge Function webhook or pg_net trigger (email-substitute event).
5. **Logic:** TypeScript in Edge Function with unit tests (not PA expressions).
6. **UI:** HLK-ERP `/customer/2026-suez-webuy/` validation panel.
7. **Reporting:** ERP Recharts tile; optional `erp.vw_*` export for client Power BI.
8. **Readiness:** `py scripts/bi_integration_readiness_check.py --report`.

## Explicit non-goals

- Building Power Automate flows inside AKOS repo.
- Declaring Excel/SharePoint as SSOT (engagement referential only).

## Acceptance criteria

- AC-HUMAN: Operator validates libellé output on Stream B panel matches demo spec intent.
- AC-AUTOMATION: readiness check PASS; contract + adapter FKs resolve.

## Cross-references

- Scaffold SOP: `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`
- Integration plane: `DATA_INTEGRATION_PLANE.md` §7
