# Stripe Wrappers (FDW) — operator runbook (Holistika)

## Scope

This runbook supports **Initiative 18** posture: **inventory-first** use of the Supabase **Wrappers** extension and an existing foreign server (e.g. **`stripe_gtm_server`**) projecting Stripe objects into schema **`stripe_gtm`** (table names may follow `stripe_gtm_*`).

## Secrets

- Stripe API key for the Wrapper lives in **Supabase Vault** (or equivalent secret store). **Never** commit keys or Vault secret payloads to git.
- Coordinate **test vs live** keys with Finance; document which **`srvname`** maps to which Stripe account in this file’s operator appendix (internal only).

## Privileges (read-only posture)

When schema **`stripe_gtm`** exists:

```sql
REVOKE ALL ON SCHEMA stripe_gtm FROM PUBLIC;
GRANT USAGE ON SCHEMA stripe_gtm TO service_role;
GRANT SELECT ON ALL TABLES IN SCHEMA stripe_gtm TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA stripe_gtm GRANT SELECT ON TABLES TO service_role;
```

- **Do not** grant `anon` / `authenticated` SELECT on foreign tables unless explicitly approved — foreign tables **do not honor RLS**; API exposure is a **SOC** regression.
- Confirm **`stripe_gtm`** is **not** in PostgREST exposed schemas unless there is a signed exception.

## Smoke SQL

```sql
SELECT srvname FROM pg_foreign_server WHERE srvname LIKE 'stripe%';
-- Example (adjust relation names to match `information_schema.tables`):
-- SELECT count(*) FROM stripe_gtm.stripe_gtm_customers;
```

## Failure modes

- **Empty FDW rows but API has data:** wrong Stripe account key, wrong server mapping, or Wrapper misconfiguration — fix in Dashboard/ Vault, not in git DML.
- **Auth errors:** rotate Vault secret; re-test with `service_role` server-side only.
- **Linter `foreign_table_in_api`:** remove API exposure; use server-side queries only.

## References

- [Supabase Stripe Wrapper](https://supabase.com/docs/guides/database/extensions/wrappers/stripe)
- [Database linter — foreign table in API](https://supabase.com/docs/guides/database/database-linter?lint=0017_foreign_table_in_api)
