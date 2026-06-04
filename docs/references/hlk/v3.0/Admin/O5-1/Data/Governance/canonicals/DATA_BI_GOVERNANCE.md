---
title: Data BI Governance
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Governance Lead
co_authors:
  - CDO
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
  - DATA_INTEGRATION_PLANE.md
  - DATA_ARCHITECTURE.md
  - ../Architecture/canonicals/SEMANTIC_LAYER.md
  - dimensions/BI_CONSUMER_REGISTRY.csv
  - dimensions/AREA_BI_PROFILE.csv
  - dimensions/RPA_ADAPTER_REGISTRY.csv
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - DATA_PRIVACY_RETENTION_POLICY.md
  - ../../../People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv
linked_runbooks:
  - scripts/bi_integration_readiness_check.py
  - scripts/validate_bi_consumer_registry.py
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
---

# Data BI Governance — Postgres-native warehouse + tiered consumers

> **Warehouse declaration:** Holistika's logical warehouse is **Supabase Postgres (T2)** —
> layered schemas (`compliance.*_mirror`, `erp.*`, `holistika_ops`, `finops`, FDW read
> planes) — **not** a separate Snowflake/BigQuery build. BI tools are **consumers** of
> declared data surfaces, governed by `BI_CONSUMER_REGISTRY.csv` and data contracts.

Ratified by amending decision **`D-IH-93-I`** (BI and warehouse governance) from explicit
not-now to full stack-native doctrine (2026-06-04).

## 1. Purpose

Prevent three failure modes:

1. **Surprise BI work** — engagements request Power BI / Power Automate without internal
   adapter rows, contracts, or SOP pairing (SUEZ pain pattern).
2. **Tool sprawl** — half-built assets (Langfuse, `erp.vw_*`, Edge Functions) invisible
   in `COMPONENT_SERVICE_MATRIX`.
3. **SSOT confusion** — treating BI dashboards or client Excel as authoritative over git
   canonicals or mirrors.

## 2. Warehouse layers (T2 binding)

| Layer | Schema / object | Warehouse role |
|:---|:---|:---|
| Governance facts | `compliance.*_mirror` | T1 CSV projections |
| Curated analytics | `erp.vw_*` | Mission Control + export views |
| Planning analytics | `governance.planning_*_view` | Atlas routes |
| Operational events | `holistika_ops.*` | Webhook idempotency, RBAC |
| Async bus | `pgmq` queues | Stripe → finops worker (I81) |
| Finance read plane | `stripe_gtm` FDW + `finops.*` | GTM/CRM analytics |
| Graph index | Neo4j (T3) | Relationship BI (rebuildable) |
| Forward OLAP | Analytics Buckets (Iceberg) | **Operator production** on Holistika Supabase (Marketing primary); vendor Public Alpha label is not a Holistika blocker when engagement revenue funds hardening per `SOP-DATA_PRODUCTION_READINESS_001.md` |

See `DATA_ARCHITECTURE.md` §2 and §9 (Supabase capability module table).

## 3a. Multi-area BI consumption (DAMA)

Every O5-1 area **consumes** BI appropriate to its role — DATA owns the **plane**; areas
declare consumption in `AREA_BI_PROFILE.csv` (one row per area) linked to
`BI_CONSUMER_REGISTRY.csv` tool instances.

| Role | Responsibility |
|:---|:---|
| Data Governance Lead | Maintains AREA_BI_PROFILE + BI_CONSUMER registries |
| Area steward (`steward_role` column) | Ensures area charter appendix matches profile row |
| RevOps Lead | Unified RevOps umbrella — embeds Marketing Ops **execution**; MKTOPS discipline remains **quality bar** (D-IH-93-J) |

Run: `py scripts/validate_area_bi_profile.py`

## 3. BI consumer tiers (T1–T10)

Each tier maps to one or more `BI_CONSUMER_REGISTRY.csv` rows.

| Tier | Consumer | Default stream | When to use |
|:---|:---|:---|:---|
| **T1** | HLK-ERP embedded (Recharts class) | B (internal) | Holistika-owned ops dashboards |
| **T2** | METRICS_REGISTRY → SQL/views | B | Define-once semantic metrics |
| **T3** | Langfuse | B | AIC quality / cost observability |
| **T4** | Metabase | B | Steward SQL BI (optional) |
| **T5** | Neo4j explorer / Graph MCP | B | Relationship / lineage questions |
| **T6** | Streamlit prototypes | B | Exploratory graph BI |
| **T7** | Power BI (+ Power Apps) | **A** (client tenant) | Customer DSI mandates Microsoft |
| **T8** | Make / n8n / Power Platform RPA | A or C | Low-code automation |
| **T9** | AKOS FastAPI control plane | B | Runtime inventory + health metrics |
| **T10** | Excel / SharePoint / Airtable | A | Engagement referentials — **never SSOT** |

**Chart standard (Holistika-owned):** embedded charts use **Recharts** (or OT-CHART-DATA
equivalent) inside HLK-ERP — not Power BI — unless engagement declares Stream A.

## 4. Engagement streams (A / B / C)

| Stream | Runs where | Governance binding |
|:---|:---|:---|
| **B — Holistika** | Supabase + Edge + ERP + Langfuse | Default for internal surfaces |
| **A — Client tenant** | Power Platform / client Azure | `RPA_ADAPTER_REGISTRY` + contract + scaffold SOP |
| **C — Hybrid bridge** | FDW, export views, webhooks | Power BI reads `erp.*`; PA writes staging tables |

Every engagement declares streams in **data contracts** + engagement scaffold — not
operator memory. See `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`.

## 5. Semantic binding

- Metrics: `METRICS_REGISTRY.csv` + `SEMANTIC_LAYER.md` (define-once).
- BI consumers **must not** redefine metrics already in the registry; they bind to SQL
  views or documented column contracts.
- New metrics require registry row **before** dashboard wiring.

## 6. Client vs internal posture

| Surface | SSOT | BI posture |
|:---|:---|:---|
| Git canonical CSV | T1 | Never bypass for dashboard convenience |
| Supabase mirror | T2 projection | Primary internal warehouse read |
| Client Power BI | Stream A | Export views or PG connector — read-only |
| Customer-pack demo specs | Reference only | Scaffold → adapter + contract before build |

## 7. Readiness matrix (operator checklist)

| Question | PASS signal |
|:---|:---|
| Is the warehouse layer named? | T2 schema in contract `schema_ref` |
| Is the BI tier declared? | Row in `BI_CONSUMER_REGISTRY.csv` |
| Is RPA governed? | Row in `RPA_ADAPTER_REGISTRY.csv` when Stream A/C |
| Is matrix current? | `component_id` FK resolves in COMPONENT_SERVICE_MATRIX |
| Are erp views present? | Migration `20260506130100_i62_p2_erp_schema_views.sql` |
| Privacy class set? | `classification` per `DATA_PRIVACY_RETENTION_POLICY.md` |

Run: `py scripts/bi_integration_readiness_check.py --self-test`

## 8. Stewardship

| Role | Responsibility |
|:---|:---|
| Data Governance Lead | BI tier assignment, Stream A/B/C declaration on engagements |
| Data Architect | Semantic binding, export view design |
| Data Steward | Metabase (T4) when activated; mirror parity |
| System Owner | Edge/ERP wiring, matrix rows for runtime components |

## 9. Cross-references

- Integration plane: `DATA_INTEGRATION_PLANE.md`
- SUEZ Stream B example: `SOP-DATA_SUEZ_LIBELLE_001.md`
- Research evidence: `docs/wip/planning/93-data-area-foundation-and-governance/reports/research-bi-warehouse-posture-2026-06-04.md`

## Evidence base

- DAMA-DMBOK2 Ch.4 Storage, Ch.9 BI — warehouse vs consumption separation.
- Supabase Metabase guide — T4 steward BI pattern.
- Internal: I81 Edge+pgmq, I62 `erp.*` views, I93 P4 semantic layer.
