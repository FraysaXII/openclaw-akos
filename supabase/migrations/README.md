# Supabase migrations (Holistika MasterData DDL)

Git is the **SSOT** for forward DDL applied through the [Supabase CLI](https://supabase.com/docs/guides/deployment/database-migrations). Staging copies under `scripts/sql/*_staging/` remain **proposals** until promoted here.

## Parity map (staging → migration file)

Migration **filename prefixes** must match the remote ledger (`schema_migrations`) after reconciliation—see **One-time reconciliation** below.

| Migration file (this folder) | Staging source |
|-----------------------------|----------------|
| `20260418165339_kirbe_monitoring_logs_retention.sql` | **reverse-imported 2026-05-04 (D-IH-OPS-3)** from remote `supabase_migrations.schema_migrations[20260418165339].statements`; body originally applied via Dashboard before this folder existed. Idempotent. |
| `20260418183239_holistika_ops_lead_intake.sql` | `scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql` |
| `20260418193915_holistika_ops_lead_intake_captcha_columns.sql` | `scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql` |
| `20260420202847_i16_finops_vendor_register_mirror.sql` | `scripts/sql/i16_phase3_staging/20260420_i16_finops_vendor_mirror_up.sql` |
| `20260423014144_i18_finops_counterparty_mirror_cutover.sql` | `scripts/sql/i18_phase1_staging/20260423_i18_finops_counterparty_mirror_up.sql` |
| `20260423014326_i19_finops_ledger_phase1.sql` | `scripts/sql/i19_phase1_staging/20260423_i19_finops_ledger_phase1_up.sql` |
| `20260502140000_i48_dossier_run_mirror.sql` | Initiative 48 — net-new `compliance.dossier_run` append-only trend store (no staging duplicate) |
| `20260503190000_i14_phase3_compliance_and_holistika_ops.sql` | `scripts/sql/i14_phase3_staging/20260417_i14_phase3_up.sql` — **renamed 2026-05-04 (D-IH-OPS-2)** from original `20260418165339_…`; that timestamp is now the reverse-imported kirbe-retention file. Idempotent reapply. |
| `20260523000000_i81_p2_t3_alter_filed_instruments_mirror.sql` | Initiative 81 P2 T3 (D-IH-81-S, 2026-05-23) — no staging duplicate. `ALTER TABLE compliance.founder_filed_instruments_mirror RENAME TO compliance.filed_instruments_mirror` + 4 index renames + RLS policy DROP+CREATE with aligned identifiers (the I81 P2 layout migration closure for the FOUNDER_FILED_INSTRUMENTS.csv → advops/FILED_INSTRUMENTS.csv cascade rename). Idempotent. |
| `20260524000000_i81_p2_b2_finops_writer_substrate.sql` | Initiative 81 P2 Bundle B-2a (D-IH-81-V, 2026-05-23) — no staging duplicate. `CREATE EXTENSION IF NOT EXISTS pgmq` + 2 queues (`finops_writer_queue` + `finops_writer_dlq`) + `holistika_ops.stripe_events` raw-event idempotency log (PK=`stripe_event_id`) + `holistika_ops.fx_rate_cache` ECB daily-rate cache + `finops.registered_fact` extension with 4 FX columns (`amount_minor_eur` + `fx_rate_ecb` + `fx_rate_stripe` + `fx_source`) + `service_role` grants on `compliance.ops_register_mirror`. Substrate-only; executable Edge Functions + worker land at B-2b (D-IH-81-W). All `CREATE … IF NOT EXISTS` / `ADD COLUMN IF NOT EXISTS` idempotent. |

## Pre-`db push` checklist (mandatory)

1. `npx supabase login` and `npx supabase link --project-ref <PROJECT_REF>` to the target project.
2. Run `npx supabase migration list`.
3. **Go/no-go:** Local and Remote columns must **match** for every row (no local-only or remote-only migrations). If there is drift, **do not** `npx supabase db push` until reconciled—see below.

> CLI invocation contract: every Supabase CLI command in this repo uses `npx supabase` (or the equivalent `npm run supabase -- <subcommand>`). The CLI is pinned in [`../package.json`](../../package.json); `npx` resolves the local pinned binary. See [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.1.

## One-time reconciliation (remote ↔ git)

When Dashboard or break-glass applied migrations, the platform records **version strings** (e.g. `20260418165339`). Git files must use the **same prefix** so `migration list` stays deterministic ([Database Migrations](https://supabase.com/docs/guides/deployment/database-migrations)).

**Decision tree**

1. Compare `migration list` to files in this folder.
2. For each divergent version, prove **content equivalence**: diff the SQL Supabase recorded (Dashboard migration detail or `db pull` workflow) against the matching Git migration body.
3. **If DDL is equivalent and remote already applied it:** **Rename** the Git file so the leading timestamp matches the remote version exactly (pattern `YYYYMMDDHHMMSS_description.sql`; remote wins the **ID**; Git keeps the **DDL**).
4. **If the ledger is wrong but schema is correct:** use **`npx supabase migration repair --status <reverted|applied> <version>`** only with a written operator mapping and [`operator-sql-gate.md`](../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) break-glass follow-up—do not guess.
5. Re-run `npx supabase migration list` until the matrix is clean, then proceed with normal `npx supabase db push` for **new** migrations only.

**Large compliance mirror DML** (CSV → upserts) stays **out** of this folder—use `py scripts/verify.py compliance_mirror_emit` and operator-reviewed SQL batches (two-plane model).

## Reconciliation log

| Date | Decision | Action |
|:---|:---|:---|
| 2026-05-04 | D-IH-OPS-2 | Renamed `20260418165339_i14_phase3_compliance_and_holistika_ops.sql` → `20260503190000_i14_phase3_compliance_and_holistika_ops.sql` so the original timestamp could host the reverse-imported kirbe-retention body that lived on the remote ledger only. I14-phase-3 body is fully idempotent; reapply at the new tail timestamp produces zero schema delta. See [`docs/wip/planning/22a-i22-post-closure-followups/reports/sql-proposal-supabase-parity-20260504.md`](../../docs/wip/planning/22a-i22-post-closure-followups/reports/sql-proposal-supabase-parity-20260504.md). |
| 2026-05-04 | D-IH-OPS-3 | Reverse-imported `kirbe.monitoring_logs_retention` body from remote `supabase_migrations.schema_migrations[20260418165339].statements` into new file `20260418165339_kirbe_monitoring_logs_retention.sql`. Idempotent. `supabase db push` will skip on the next push because remote already has the row at that version; git is now SSOT. |
