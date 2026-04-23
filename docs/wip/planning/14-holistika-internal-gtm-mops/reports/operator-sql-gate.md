# Operator SQL gate

**Mandatory workflow**

1. **Discover:** MCP `list_tables`, `execute_sql` **SELECT** only.
2. **Read:** Supabase + Postgres docs (shared responsibility, migrations, extensions).
3. **Propose:** `reports/sql-proposal-<topic>-<YYYYMMDD>.md` with DDL, rollback, RLS, indexes, PII.
4. **Operator approval** → decision log.
5. **Execute (approved DDL):** Promote exact approved `*_up.sql` into [`supabase/migrations/`](../../../../supabase/migrations/) (new `supabase migration new …` file **or** rename existing files to match remote `schema_migrations` after content-equivalence proof). **Before `db push`:** run **`supabase migration list`** on the linked project; Local and Remote must **match** (no drift). Then apply with **`supabase db push`** (or CI) per [Database Migrations](https://supabase.com/docs/guides/deployment/database-migrations). Legacy `apply_migration` / Dashboard-packaged migrations are **deprecated** for routine work once the project is linked; use them only during transition or break-glass.

**Break-glass:** Dashboard SQL Editor or MCP `apply_migration` only in emergencies. **Afterward:** run **`supabase db pull`** or **`supabase migration repair`** so [`supabase/migrations/`](../../../../supabase/migrations/) and remote `schema_migrations` match—see [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md).

**Compliance mirror DML (data plane):** Not migrations. Run **`py scripts/verify.py compliance_mirror_emit`**, review `artifacts/sql/compliance_mirror_upsert.sql`, apply in batches (`psql` / SQL Editor). Prerequisites: `validate_hlk.py` / release gate when CSVs changed.

**Forbidden until approval:** mutating `execute_sql`, `apply_migration`.
