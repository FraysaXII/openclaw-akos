# Supabase (Holistika)

This repo tracks **DDL** under [`migrations/`](migrations/) for the Holistika MasterData / compliance / `holistika_ops` stack. Edge Functions live under [`functions/`](functions/).

## Operator quick card

| Step | Command / action |
|------|------------------|
| Authenticate | `supabase login` |
| Link repo to project | `supabase link` (select Holistika project ref) |
| New DDL change (after `operator-sql-gate` approval) | `supabase migration new <short_description>` → edit SQL → PR → `supabase db push` (or CI) |
| Inspect remote history | `supabase migration list` |
| Reconcile drift | `supabase db pull` or `supabase migration repair` per [Database Migrations](https://supabase.com/docs/guides/deployment/database-migrations) |

**Go/no-go:** Do **not** run `db push` while `migration list` shows local-only or remote-only rows—reconcile filenames or repair the ledger first ([`migrations/README.md`](migrations/README.md)).

## Two-plane reminder

- **Migrations:** schema only (`supabase/migrations/*.sql`).
- **Mirror data:** `py scripts/verify.py compliance_mirror_emit` → review `artifacts/sql/compliance_mirror_upsert.sql` → apply in batches (not via `db push` of megabyte DML).

## Break-glass

DDL through the Dashboard SQL Editor is **only** for emergencies. Afterward: pull or repair migrations so git and `schema_migrations` stay aligned—see [`docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md`](../docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md).
