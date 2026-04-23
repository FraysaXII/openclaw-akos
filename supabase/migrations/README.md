# Supabase migrations (Holistika MasterData DDL)

Git is the **SSOT** for forward DDL applied through the [Supabase CLI](https://supabase.com/docs/guides/deployment/database-migrations). Staging copies under `scripts/sql/*_staging/` remain **proposals** until promoted here.

## Parity map (staging → migration file)

Migration **filename prefixes** must match the remote ledger (`schema_migrations`) after reconciliation—see **One-time reconciliation** below.

| Migration file (this folder) | Staging source |
|-----------------------------|----------------|
| `20260418165339_i14_phase3_compliance_and_holistika_ops.sql` | `scripts/sql/i14_phase3_staging/20260417_i14_phase3_up.sql` |
| `20260418183239_holistika_ops_lead_intake.sql` | `scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql` |
| `20260418193915_holistika_ops_lead_intake_captcha_columns.sql` | `scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql` |
| `20260420202847_i16_finops_vendor_register_mirror.sql` | `scripts/sql/i16_phase3_staging/20260420_i16_finops_vendor_mirror_up.sql` |
| `20260423014144_i18_finops_counterparty_mirror_cutover.sql` | `scripts/sql/i18_phase1_staging/20260423_i18_finops_counterparty_mirror_up.sql` |
| `20260423014326_i19_finops_ledger_phase1.sql` | `scripts/sql/i19_phase1_staging/20260423_i19_finops_ledger_phase1_up.sql` |

## Pre-`db push` checklist (mandatory)

1. `supabase login` and `supabase link` to the target project.
2. Run `npx supabase migration list` (or `npm run supabase -- migration list`).
3. **Go/no-go:** Local and Remote columns must **match** for every row (no local-only or remote-only migrations). If there is drift, **do not** `db push` until reconciled—see below.

## One-time reconciliation (remote ↔ git)

When Dashboard or break-glass applied migrations, the platform records **version strings** (e.g. `20260418165339`). Git files must use the **same prefix** so `migration list` stays deterministic ([Database Migrations](https://supabase.com/docs/guides/deployment/database-migrations)).

**Decision tree**

1. Compare `migration list` to files in this folder.
2. For each divergent version, prove **content equivalence**: diff the SQL Supabase recorded (Dashboard migration detail or `db pull` workflow) against the matching Git migration body.
3. **If DDL is equivalent and remote already applied it:** **Rename** the Git file so the leading timestamp matches the remote version exactly (pattern `YYYYMMDDHHMMSS_description.sql`; remote wins the **ID**; Git keeps the **DDL**).
4. **If the ledger is wrong but schema is correct:** use **`supabase migration repair`** only with a written operator mapping and [`operator-sql-gate.md`](../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) break-glass follow-up—do not guess.
5. Re-run `migration list` until the matrix is clean, then proceed with normal `db push` for **new** migrations only.

**Large compliance mirror DML** (CSV → upserts) stays **out** of this folder—use `py scripts/verify.py compliance_mirror_emit` and operator-reviewed SQL batches (two-plane model).
