# Initiative 18 — Decision log

## D-18-1 — Counterparty register and mirror cutover

**Decision:** Replace vendor-only **`FINOPS_VENDOR_REGISTER.csv`** with **`FINOPS_COUNTERPARTY_REGISTER.csv`**. Replace **`compliance.finops_vendor_register_mirror`** with **`compliance.finops_counterparty_register_mirror`**, migrating existing rows in the same migration tranche, then **`DROP`** the vendor mirror table.

**Rationale:** Single SSOT for commercial counterparties (vendors, customers, partners) with consistent validator and mirror semantics.

## D-18-2 — Stripe FDW SOC posture

**Decision:** Treat existing **`stripe_gtm`** foreign tables (behind **`stripe_gtm_server`**) as the **mirrored Stripe read plane**. **Stripe API** remains authoritative; FDW is a read projection. **No** second parallel Wrapper server in repo migrations unless a proven gap (e.g. separate test account) is recorded here with operator approval.

**Rationale:** MCP inventory showed FDW already present; duplicate servers increase operational risk.

**Posture:** `REVOKE ALL ON SCHEMA stripe_gtm FROM PUBLIC`; `GRANT USAGE` + `SELECT` to **`service_role`** only where the schema exists. FDW schemas must not be exposed via PostgREST for browser keys.

## D-18-3 — `holistika_ops.stripe_customer_link.finops_counterparty_id`

**Decision:** Add nullable **`finops_counterparty_id TEXT`** on **`holistika_ops.stripe_customer_link`**, storing the CSV **`counterparty_id`** slug. **No** database foreign key to the mirror — git CSV is authoritative; mirror is a projection.

**Rationale:** ERP and SQL authors can join governance register ↔ bridge ↔ FDW without storing Stripe IDs in git.

## D-18-4 — No Phase C monetary DDL (superseded for schema)

**Decision (original):** Reaffirm **no** native monetary fact tables **in Initiative 18**. Phase C **`finops`** schema DDL was deferred past this tranche.

**Update (2026-04-23):** Schema creation and an empty/skeleton **`finops.registered_fact`** table are **in scope for Initiative 19** ([`docs/wip/planning/19-hlk-finops-ledger/`](../19-hlk-finops-ledger/master-roadmap.md)). **What may be inserted** into that table remains governed by Legal/CFO process (`thi_finan_dtp_306`) and Initiative 19 decision log — this initiative still does **not** add monetary **data**.

## D-18-5 — Register maintenance `process_item_id`

**Decision:** Stewardship rows in the counterparty register continue to reference **Finance** subtree processes (`thi_finan_*`), including updated **`thi_finan_dtp_303`** for register maintenance. Customer **lifecycle** processes may live elsewhere; the **register row** still points to Finance maintenance where applicable.

## D-18-6 — `stripe_customer_link.finops_counterparty_id` backfill

**Decision (2026-04-23):** No backfill on **`MasterData`** at snapshot time — **`holistika_ops.stripe_customer_link`** had **zero** rows; mapping work is **N/A** until links exist.

**Pattern for operators:** When rows exist, set **`finops_counterparty_id`** to the **`counterparty_id`** slug from **`FINOPS_COUNTERPARTY_REGISTER.csv`** (no FK to mirror). Example: `UPDATE holistika_ops.stripe_customer_link SET finops_counterparty_id = '<slug>' WHERE stripe_customer_id = '<cus_…>';` (run under **`service_role`** / controlled job; document rationale per row).
