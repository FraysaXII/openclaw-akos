# Initiative 18 — Execution tranche (2026-04-23)

## Repo verification

| Check | Result |
|-------|--------|
| `py scripts/validate_hlk.py` | Expected PASS after CSV + process tranche |
| `py scripts/verify.py compliance_mirror_emit` | Expected PASS; artifact includes process + baseline + counterparty upserts |
| `pytest` (i18 SQL bundle) | Expected PASS |

## Migration ledger (applied)

**Project:** `MasterData` / `swrmqpelgoblaquequzb`  
**Apply path:** Supabase MCP `apply_migration` (`i18_finops_counterparty_mirror_cutover`) on 2026-04-23 — remote ledger version **`20260423014144`** (git file renamed from `20260423184500_*` for parity per [`supabase/migrations/README.md`](../../../../../supabase/migrations/README.md) **One-time reconciliation**).

**CLI:** `npx supabase migration list` — Local and Remote both include `20260423014144` / `i18_finops_counterparty_mirror_cutover` (verified same session).

## Mirror DML (counterparty register)

**Applied (2026-04-23):** Upserts from `py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only` (git SHA `8e3a21387254e80a73f94419010950c7aacca29a`) executed via Supabase MCP `execute_sql` (`BEGIN` / `COMMIT`). **`compliance.finops_counterparty_register_mirror`** row count **2** after apply (seed CSV rows).

## Supabase MCP snapshot (post DDL + DML)

**`list_migrations` (remote):** `20260418165339` monitoring_logs_retention; `20260418183239` i14_holistika_ops_lead_intake; `20260418193915` i14_holistika_ops_lead_intake_captcha_columns; `20260420202847` i16_finops_vendor_register_mirror; **`20260423014144` i18_finops_counterparty_mirror_cutover**.

**`list_tables` (`compliance`, `holistika_ops`):** `compliance.finops_counterparty_register_mirror` present (**RLS on**, **2** rows); **`compliance.finops_vendor_register_mirror` absent** (dropped by cutover); `holistika_ops.stripe_customer_link` **0** rows; bridge column **`finops_counterparty_id`** expected present.

**`list_extensions`:** `wrappers` **0.5.3** installed (Stripe FDW posture applied inside migration when `stripe_gtm` exists).

**`get_advisors` (security):** Many **pre-existing** project findings (RLS on legacy `public`/`kirbe` tables, security definer views, `timescaledb` version, etc.). **No Initiative-18-specific new table** surfaced as ERROR beyond global backlog; re-run after **`finops`** Initiative 19 migration for delta on new objects.

## Staging parity

| Migration file | Staging source |
|----------------|----------------|
| `supabase/migrations/20260423014144_i18_finops_counterparty_mirror_cutover.sql` | `scripts/sql/i18_phase1_staging/20260423_i18_finops_counterparty_mirror_up.sql` |
