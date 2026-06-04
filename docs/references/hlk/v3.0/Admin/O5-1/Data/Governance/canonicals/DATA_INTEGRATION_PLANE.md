---
title: Data Integration Plane
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Architect
co_authors:
  - System Owner
  - Data Governance Lead
last_review: 2026-06-04
last_review_by: Data Architect
last_review_decision_id: D-IH-93-I
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-I
  - D-IH-93-D
status: active
register: internal
linked_canonicals:
  - DATA_BI_GOVERNANCE.md
  - dimensions/RPA_ADAPTER_REGISTRY.csv
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - ../../../People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv
linked_runbooks:
  - scripts/bi_integration_readiness_check.py
  - supabase/functions/stripe-webhook-handler/
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
---

# Data Integration Plane — Supabase-native patterns

> Names **how data enters and leaves** the T2 warehouse: Edge Functions, pgmq workers,
> database webhooks, cron, FDW, Realtime, and governed low-code RPA adapters.

## 1. Purpose

Provide one integration doctrine so engagements do not default to ad-hoc Power Automate
when Holistika-owned surfaces should use the **proven internal pattern** (I81 Stripe).

## 2. Holistika-internal pattern (Stream B — binding template)

```
External webhook → Edge Function → holistika_ops.* (idempotent store)
                → pgmq.enqueue → worker Edge Function → finops.* / mirror emit
```

**Evidence:** `supabase/functions/stripe-webhook-handler/`,
`supabase/migrations/20260524000000_i81_p2_b2_finops_writer_substrate.sql`.

**When to use:** Holistika owns ingress, secrets, and retry semantics.

## 3. Supabase capability modules

| Module | Role | Governance |
|:---|:---|:---|
| **Edge Functions** | HTTP ingress, auth, fan-out | `holistika_edge` RPA adapter |
| **pgmq** | Durable async queue | Pair worker function + DLQ |
| **pg_net / Database Webhooks** | Postgres-triggered HTTP | `pg_net_webhook` adapter |
| **pg_cron** | Scheduled refresh / exports | Contract SLA + runbook |
| **Realtime** | Push mirror freshness to ERP | Optional; not SSOT |
| **Wrappers FDW** | External read planes (Stripe) | `fdw_projection` contracts |
| **Vault** | Secret storage | Never log secret values |

See `DATA_ARCHITECTURE.md` §9 for condensed module table.

## 4. RPA / low-code tier (Stream A / C)

Governed by `RPA_ADAPTER_REGISTRY.csv` (Normalized Adapter Pattern per `D-IH-72-O`):

| Adapter | Stream | Status posture |
|:---|:---|:---|
| `holistika_edge` | B | **active** — default internal |
| `pg_net_webhook` | B | **active** |
| `power_platform` | A | **planned** until engagement scaffold complete |
| `make` / `n8n` | C | **active** where already in matrix |

**Non-goal:** Building client-tenant Power Automate flows inside AKOS repo.

## 5. Adapter composition rules

1. Every external ingress declares a **data contract** (`DATA_CONTRACT_REGISTRY.csv`).
2. RPA adapters link **paired SOP + runbook** (or TODO marker per `D-IH-72-W`).
3. `integration_pattern` on matrix rows must reflect actual mechanism
   (`event`, `edge_webhook`, `pgmq_worker`, `fdw_read`, `low_code_rpa`).
4. Feature flags: `gated_operator` for client-tenant flows; `always_on` for Edge.

## 6. Security invariants

- Idempotent webhook stores before side effects.
- No secrets in git; Vault / Supabase secrets only.
- Client-tenant tools run in **client Azure** — Holistika supplies contracts + export
  views, not DSI credentials in AKOS.
- Classification from `DATA_PRIVACY_RETENTION_POLICY.md` on all integration payloads.

## 7. SUEZ worked example (Stream B alternative)

When client Power Automate is blocked, Holistika delivers Stream B:

| Demo spec element | Stream B substitute |
|:---|:---|
| Excel referential on SharePoint | Git-seeded CSV + optional mirror table |
| Power Automate email trigger | Edge Function webhook or pg_net trigger |
| Power Apps validation form | HLK-ERP customer panel |
| Power BI report | ERP Recharts + optional `erp.vw_*` export |

Full procedure: `SOP-DATA_SUEZ_LIBELLE_001.md`.

## 8. Cross-references

- BI tiers: `DATA_BI_GOVERNANCE.md`
- Engagement scaffold: `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`
- Stripe FDW runbook: `docs/wip/planning/18-hlk-finops-counterparty-stripe/reports/stripe-fdw-operator-runbook.md`

## Evidence base

- DAMA-DMBOK2 Ch.6 Data Integration — hub-and-spoke vs point-to-point; adapter registry.
- Supabase Queues, Edge Functions, Database Webhooks official docs (2026).
- I81 finops writer substrate (repo migrations).
