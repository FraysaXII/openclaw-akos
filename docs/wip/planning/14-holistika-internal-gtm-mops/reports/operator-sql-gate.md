# Operator SQL gate

**Mandatory workflow**

1. **Discover:** MCP `list_tables`, `execute_sql` **SELECT** only.
2. **Read:** Supabase + Postgres docs (shared responsibility, migrations, extensions).
3. **Propose:** `reports/sql-proposal-<topic>-<YYYYMMDD>.md` with DDL, rollback, RLS, indexes, PII.
4. **Operator approval** → decision log.
5. **Execute (approved DDL):** Promote exact approved `*_up.sql` into [`supabase/migrations/`](../../../../supabase/migrations/) (new `supabase migration new …` file **or** rename existing files to match remote `schema_migrations` after content-equivalence proof). **Before `db push`:** run **`supabase migration list`** on the linked project; Local and Remote must **match** (no drift). Then apply with **`supabase db push`** (or CI) per [Database Migrations](https://supabase.com/docs/guides/deployment/database-migrations). Legacy `apply_migration` / Dashboard-packaged migrations are **deprecated** for routine work once the project is linked; use them only during transition or break-glass.

**Break-glass:** Dashboard SQL Editor or MCP `apply_migration` only in emergencies. **Afterward:** run **`supabase db pull`** or **`supabase migration repair`** so [`supabase/migrations/`](../../../../supabase/migrations/) and remote `schema_migrations` match—see [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md).

**Compliance mirror DML (data plane):** Not migrations. Canonical operator guide: [`docs/guides/holistika-mirror-dml-apply.md`](../../../../docs/guides/holistika-mirror-dml-apply.md).

1. **Emit** — `py scripts/verify.py compliance_mirror_emit` (full bundle) or `py scripts/verify.py ops8615_mirror_emit` / `--ops8615-split` (five OPS-86-15 tables).
2. **Apply (preferred)** — `pwsh -File scripts/apply_mirror_batches.ps1 -Preset ops8615` or `-BatchDir <chunk-folder>` → uses **`npm run supabase db query --linked -f`** on each `.sql` (linked Holistika project; same auth as `db push`).
3. **Apply (alternative)** — `psql -f` per batch when CLI link is unavailable.
4. **Avoid** — pasting multi-megabyte SQL into the Dashboard SQL Editor (size limit); tiny smoke files only.

Prerequisites: `validate_hlk.py` when CSVs changed; `npx supabase link` on MasterData before Method A.

**Forbidden until approval:** mutating `execute_sql`, `apply_migration`.
