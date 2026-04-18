# Initiative 14 — Phase 3 staging DDL (Supabase / Postgres)

**Authority:** [`sql-proposal-stack-20260417.md`](../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md)  
**Gate:** [`operator-sql-gate.md`](../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) — **staging only** until operator approval; never ad-hoc production DDL.

## Apply (staging)

1. Backup the staging project.
2. Run **`20260417_i14_phase3_up.sql`** in order (single file, idempotent `IF NOT EXISTS` / `DROP POLICY IF EXISTS` where applicable).
3. Load mirror data: [`sync_compliance_mirrors_from_csv.py`](../../sync_compliance_mirrors_from_csv.py) → review SQL → execute in SQL editor or `psql`.
4. Run verification: **`verify_staging.sql`** or `py scripts/verify_phase3_mirror_schema.py` from the repo root (requires `DATABASE_URL` or `SUPABASE_DB_URL`, and `psql` on `PATH`).

## Optional legacy rename (Wave B2)

Run **`20260417_deprecate_legacy_public_optional.sql`** only after inventory confirms object names and a maintenance window. Adjust quoted identifiers to match the target database.

## Rollback

**`20260417_i14_phase3_rollback.sql`** drops policies and tables created by the up migration (destructive). Review before executing.
