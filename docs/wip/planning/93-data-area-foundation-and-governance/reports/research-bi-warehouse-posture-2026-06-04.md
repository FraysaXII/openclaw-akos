---
intellectual_kind: research_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-93
feeds_decision: D-IH-93-I (amendment + full doctrine tranche)
status: research-synthesis
audience: J-OP
role_owner: CDO + Data Architect + System Owner
language: en
authored: 2026-06-04
last_review: 2026-06-04
revision: 2-deep-regression
ratifying_research:
  - Supabase Metabase integration (official docs)
  - Supabase Analytics Buckets / Iceberg (public alpha)
  - Supabase Edge Functions + pgmq queue pattern (repo evidence I81)
  - DAMA-DMBOK2 Ch.4 Storage + Ch.6 Integration + Ch.9 BI
internal_evidence_sweeps: 12
---

# BI / warehouse / integration posture — deep regression (v2)

> Operator direction (2026-06-04): **not light minting**. Stack-native BI (Option A)
> **and** readiness for Metabase, Power BI, ERP-first, Make/n8n/Power Automate,
> Recharts/chart libraries, Supabase realtime/actions — because engagements like SUEZ
> expose gaps when customer-pack demos exist without internal integration playbooks.

## 0. Executive finding

Holistika **already has a warehouse**. It is **Supabase Postgres (T2)** with layered
schemas — not a missing Snowflake layer. What is missing is a **governed BI + integration
consumer model** that:

1. Names which tool serves which question (ops dashboard vs AIC traces vs client tenant).
2. Maps half-built assets (`erp.*` views, Edge Functions, Langfuse) into `COMPONENT_SERVICE_MATRIX`.
3. Prevents the **SUEZ Power Automate pain pattern**: customer-facing demo specs without
   internal adapter rows, data contracts, or paired SOP+runbook for the integration plane.

**Amend `D-IH-93-I`** from pure not-now → **full stack-native doctrine + multi-consumer readiness**.

---

## 1. Supabase as logical warehouse (T2 layers — repo evidence)

| Layer | Schema / object | Role | Maturity |
|:---|:---|:---|:---|
| **Governance facts** | `compliance.*_mirror` (16+) | T1 CSV projections; ERP + validators consume | Active sync scripts |
| **Curated analytics** | `erp.vw_*` (6 views) | Mission Control tiles; anon-safe public health | **Migrated I62** |
| **Planning analytics** | `governance.planning_*_view` | I65 atlas routes for hlk-erp | Migrated I65 |
| **Operational events** | `holistika_ops.*` (stripe_events, audit, RBAC) | Webhook idempotency + ERP auth | Migrated I62/I81 |
| **Async integration bus** | `pgmq` queues (`finops_writer_queue`, DLQ) | Stripe → finops worker pattern | **Live I81 B-2** |
| **Edge ingress** | `supabase/functions/*` | stripe-webhook-handler, finops-writer-worker, fx-rate-cache | **Deployed pattern** |
| **Finance read plane** | `stripe_gtm` FDW + `finops.*` | GTM/CRM analytics (`DC-HOL-GTM-CRM-001`) | Active I18 |
| **Eval / quality facts** | `compliance.eval_run`, `dossier_run` mirrors | Three-lights ERP tile | Mirrored |
| **Knowledge plane** | `kirbe.*` (sibling) | Document analytics views (`SOP-KIRBE_ANALYTICS_READINESS`) | Separate repo |
| **Graph index** | Neo4j (T3) | Relationship BI; explorer + MCP | Partial (NEO4J_* gated) |
| **Forward OLAP offload** | Supabase Analytics Buckets (Iceberg) | Heavy analytics without OLTP load | **Public alpha — forward only** |

**Realtime / actions (available, under-governed today):**

- Supabase **Realtime** can push mirror freshness / ERP notifications (`holistika_ops.notifications` forward-charter I62).
- **Edge Functions** already implement the **correct internal pattern** for webhooks (Stripe): receive → idempotent store → queue → worker — superior to ad-hoc Power Automate for Holistika-owned surfaces.
- **pg_graphql / pg_cron** — referenced in planning SQL; not yet a governed integration catalog entry.

---

## 2. BI consumer tiers (beyond Power BI)

| Tier | Consumer | Data source | Status | Matrix gap |
|:---|:---|:---|:---|:---|
| **T1 Embedded ops BI** | `hlk-erp` (Next.js + shadcn/Recharts class) | `erp.*`, `governance.*`, mirrors | Views ✅ UI mocked | **No hlk-erp row** |
| **T2 Semantic/metrics** | `METRICS_REGISTRY.csv` → SQL/views | Contracts + mirrors | P4 mint; views forward | N/A |
| **T3 AIC observability** | Langfuse saved views | `akos/telemetry.py` traces | Production | **No Langfuse row** |
| **T4 SQL steward BI** | Metabase (optional) | Supabase Postgres direct | Not deployed | Not inventoried |
| **T5 Graph BI** | Neo4j explorer / MCP | T3 graph sync | Partial | **No Neo4j row** |
| **T6 Prototype BI** | Streamlit (`hlk_graph_explorer.py`) | Graph API | Secondary | Listed as hosting only |
| **T7 Client tenant BI** | Power BI + Power Apps | Client SharePoint/Excel + PA flows | **SUEZ demos specify; not built** | Power Platform ×4 dupes |
| **T8 Low-code RPA** | Make, n8n | SaaS connectors | In matrix; **no adapter registry** | Untagged |
| **T9 Control plane** | AKOS FastAPI `/metrics`, dashboards | Langfuse + health | Active | FastAPI misclassified |
| **T10 Spreadsheet-as-DB** | Excel/SharePoint/Airtable | Engagement referentials | SUEZ demo pattern | Airtable untagged |

**Chart libraries:** `OUTPUT_TYPE_REGISTRY.csv` already names `OT-CHART-DATA` (D3/Chart.js/Recharts class). HLK-ERP stack is Next.js + shadcn — **Recharts is the native embedded chart path**, not Power BI, for Holistika-owned surfaces.

---

## 3. Integration / RPA plane (why SUEZ Power Automate hurts)

### What exists for SUEZ

- Customer-pack demos (`demo-libelle-generator`, `demo-dispute-register`) specify **Excel + Power Apps + Power Automate + Power BI** in the **client Azure tenant**.
- Capability row `CAP-HOL-DATAOPS-SUEZ-USAGE-DASHBOARD-001` names **Power BI render target Phase 3**.
- Operator scratchpad confirms Microsoft stack is **intentional for SUEZ DSI compatibility**.

### What is missing (root cause of operator struggle)

| Gap | Effect |
|:---|:---|
| No **Power Platform adapter** in any `*_ADAPTER_REGISTRY.csv` | No status, SOP, runbook, or feature flag |
| Demos are **external-translated specs**, not internal executable processes | No `process_list` row for "build PA flow from demo spec" |
| No **dual-stream engagement model** in Data doctrine | Unclear when Holistika uses Supabase Edge vs client PA |
| `COMPONENT_SERVICE_MATRIX` duplicates Power Platform 4× without `integration_pattern` | Inventory noise; no BI/RPA role |
| FlowMaker SOPs (internal automation) exist but **unpaired** (I81 partial) | Parallel automation story not wired to Data area |

### Holistika-internal integration pattern (proven — reuse)

```
External webhook → Edge Function → holistika_ops.stripe_events (idempotent)
                → pgmq.enqueue → finops-writer-worker → finops.registered_fact
```

This is the **template for Holistika-owned integrations**. Client-tenant Power Automate is a **different tier** — engagement delivery in *their* tenant, governed by adapter + contract, not by copying into Supabase.

### Recommended dual-stream model

| Stream | Where it runs | When |
|:---|:---|:---|
| **Stream B — Holistika** | Supabase + Edge Functions + ERP + Langfuse | Internal ops, governance, GTM/finops, AIC quality |
| **Stream A — Client tenant** | Power Platform / SAP / client ERP | Customer engagement (SUEZ), when DSI mandates Microsoft |
| **Stream C — Hybrid bridge** | FDW, scheduled export views, webhooks | Power BI reads `erp.*` or export views; PA writes to staging table |

Every engagement declares streams in **data contracts** + engagement scaffold — not ad-hoc per operator memory.

---

## 4. COMPONENT_SERVICE_MATRIX regression (97 rows)

| Issue | Rows / examples | Fix in tranche |
|:---|:---|:---|
| Missing production BI/ops components | Langfuse, Neo4j, Sentry, hlk-erp, AKOS serve-api | Add with `bi_consumer_tier`, `warehouse_layer`, `integration_pattern` |
| Power Platform duplication | 13, 42, 75, 81 | Consolidate → 1× Power Platform + 1× Power BI |
| Supabase duplication | 8, 9, 48, 52–54 | Consolidate roles: OLTP/mirror, Auth, Storage, Realtime |
| Untagged automation | Make (5), n8n (11), Streamlit (14) | Tag `integration_pattern=low_code_rpa` or `bi_prototype` |
| Empty governance columns | All rows lack `retention_policy_ref` / real classification | Populate from P5 privacy enum (P7 or BI tranche) |
| TBD placeholders | Forecasting Tool, Lead Tool | Resolve or mark `lifecycle_status=planned` |

---

## 5. Use-case readiness matrix

| Use case | Internal (Stream B) | Client MS (Stream A) | Blocker |
|:---|:---|:---|:---|
| Mission Control "is it safe to ship?" | `erp.vw_mission_control_today` ready | N/A | hlk-erp UI wiring |
| Mirror health / governance pulse | `erp.vw_mirror_health` ready | Power BI optional export | Matrix + ERP |
| GTM / Stripe revenue | FDW + finops pipeline **live** | Power BI via PG connector | Contract + view |
| AIC / MADEIRA quality | Langfuse dashboards **live** | N/A | Matrix row |
| SUEZ libellé generator F-05 | Not applicable internally | PA flow **spec only** | Adapter + SOP + operator runbook |
| SUEZ dispute register F-25–29 | Not applicable internally | PA + Power BI **spec only** | Same |
| Marketing attribution | CRM adapters mostly `planned/inactive` | Looker Studio possible | Adapter activation |
| KiRBe document coverage BI | `kirbe.vw_*` pattern in sibling repo | Metabase on Postgres | Cross-repo contract |

---

## 6. Proposed full doctrine tranche (not light)

### Amend `D-IH-93-I`

From "explicit not-now" → **"Postgres-native warehouse + tiered BI/integration consumers; no separate Snowflake; client-tenant tools governed via adapter + contract."**

### Mint (Data/Governance + Architecture)

| Artifact | Purpose |
|:---|:---|
| **`DATA_BI_GOVERNANCE.md`** (full) | Warehouse declaration; 10 BI tiers; chart standards; semantic binding; client vs internal; readiness matrix; engagement Stream A/B/C |
| **`DATA_INTEGRATION_PLANE.md`** | Webhook→queue→worker pattern; adapter composition; RPA tier (PA/Make/n8n); Supabase Realtime/Edge/cron; SUEZ worked example |
| **`dimensions/BI_CONSUMER_REGISTRY.csv`** | Governed rows: consumer_id, tier, tool, data_surfaces, status, paired_sop, engagement_stream |
| **`dimensions/RPA_ADAPTER_REGISTRY.csv`** (or extend RevOps) | Power Platform, Make, n8n with status + SOP linkage |
| **`SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`** | How to go from engagement demo spec → adapter row + contract + build checklist (anti-SUEZ-pain) |
| **`scripts/bi_integration_readiness_check.py`** | `--self-test`: matrix rows exist for Langfuse/Neo4j/hlk-erp; erp views reachable; registry FKs |

### COMPONENT_SERVICE_MATRIX tranche (~20 edits)

Add/dedupe/tag per §4; link `primary_process_item_id` where known; `data_classification` from privacy policy.

### Cross-amend

- `DATA_ARCHITECTURE.md` §2 — add Supabase capability layer table (Edge, pgmq, Realtime, FDW).
- `DATA_CATALOG_INTEGRATION_POSTURE.md` — BI tools as L3 projection consumers (not SSOT).

---

## 7. External sources

| Source | Confidence | Use |
|:---|:---|:---|
| [Supabase ↔ Metabase](https://supabase.com/docs/guides/database/metabase) | Safe | Tier T4 steward BI |
| [Analytics Buckets](https://supabase.com/docs/guides/storage/analytics/introduction) | Euclid (alpha) | Forward OLAP |
| DAMA Ch.4/6/9 | Safe | Warehouse + integration + BI separation |

---

## 8. Recommended operator ratification

**Ratify the full doctrine tranche (§6)** before P6 CSV work, with **SUEZ unblock** as first
`RPA_ADAPTER_REGISTRY` + scaffold SOP activation (Power Platform = `planned` → `active` for ENG-SUEZ-WEBUY-2026).

This delivers Option A **and** makes B (Metabase), C (Power BI client lane), D (ERP-first)
**declared paths** — not surprise work when the next engagement asks.
