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

## Contact leads (`holistika_ops.lead_intake`)

**Spec:** [`contact-lead-ingest-spec.md`](../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md)

1. **`20260418_holistika_ops_lead_intake_up.sql`** — marketing contact / lead rows; RLS deny `anon`/`authenticated`; `service_role` insert from Next API.
2. **`20260418_holistika_ops_lead_intake_rollback.sql`** — drop table (destructive).
3. **`20260419_holistika_ops_lead_intake_captcha_columns_up.sql`** — optional **Phase B** nullable `captcha_provider` / `captcha_verified_at` + partial index (MAROPS); apply before prod Turnstile + column inserts.
4. **`20260419_holistika_ops_lead_intake_captcha_columns_rollback.sql`** — drop captcha columns + index only.

## Related: FINOPS mirror (Initiative 16 → 18)

**Historical:** [`../i16_phase3_staging/README.md`](../i16_phase3_staging/README.md). **Current:** [`../i18_phase1_staging/README.md`](../i18_phase1_staging/README.md) — `compliance.finops_counterparty_register_mirror`; sync via `sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only` or **`py scripts/verify.py compliance_mirror_emit`**.
