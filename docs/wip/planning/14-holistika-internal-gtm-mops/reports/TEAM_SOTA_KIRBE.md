# TEAM SOTA — KiRBe (`kirbe` repo)

**Audience:** Engineers on `c:\Users\Shadow\cd_shadow\root_cd\kirbe` (or team clone).  
**Standalone:** Operate from this file without the Initiative 14 Cursor plan.

## 1. What KiRBe is

Document ingestion, vaults, orgs, **graph sync**, **Stripe (SaaS product)**, vectors, monitoring hooks. **HLK CSV SSOT** lives in the **company governance repo** (`process_list.csv`, `baseline_organisation.csv`); KiRBe **mirrors** via ingest jobs. On conflict, **canonical git wins**—see [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md).

## 2. SQL SSOT

- Primary bundle: `supabase/sql/yy_all_in_one.sql` (+ companion migrations). **Version** every DDL change.
- **Operator approval** before applying to shared Supabase—same gate as ERP doc.

## 3. Billing — two planes (mandatory)

| Plane | Where | What |
|-------|-------|------|
| **KiRBe SaaS product** | `kirbe.subscriptions`, `invoice_items`, `payment_methods`, Stripe RPCs | **Product** customers |
| **Holistika company ops** | **`holistika_ops`** (or chosen schema) — **not** `kirbe.*` | Client accounts, partner revenue, ERP-facing money |

Never merge company CRM billing into `kirbe.*` “for convenience.”

## 4. Ingestion

- Sources: `kirbe_sources`, `kirbe_ingestion_runs`; `kirbe_source_type` may need **`api_connector` + JSONB** for ad/marketing APIs—coordinate enum extension via migration.
- **v3.0 docs:** `kirbe_documents` + provenance to vault paths; optional `item_id` FK views.

## 5. Vectors

- Canonical path: **`kirbe.data_kirbe_document_vectors_1536`** (or unified table approved by operator). Deprecate **`public`** duplicates after row migration.

## 6. Monitoring

- **`kirbe.monitoring_logs`:** enforce **retention**, **partitioning** or time purge, **indexes**, cost budget—see Initiative 14 [`monitoring-logs-governance.md`](monitoring-logs-governance.md).

## 7. Webhooks (Stripe, connectors)

- **Idempotency** keys; signature verification; no secret logging.

## 8. Release sequence

1. Governance repo CSV change + `validate_hlk.py`.
2. Ingest job updates mirrors.
3. Apply KiRBe SQL migration.
4. Deploy app.

## 9. MCP / agents (later)

- **Phase 3b:** thin MCP servers over **same** Supabase RPCs—no duplicate credentials (reuse `config/mcporter.json.example` patterns from the governance repo).

## 10. Related (optional)

- [`TEAM_SOTA_HLK_ERP.md`](TEAM_SOTA_HLK_ERP.md) — ERP shell.
- [`docs/web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md`](../../../../web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md) — public marketing site.
