# Operator SQL gate

**Mandatory workflow**

1. **Discover:** MCP `list_tables`, `execute_sql` **SELECT** only.
2. **Read:** Supabase + Postgres docs (shared responsibility, migrations, extensions).
3. **Propose:** `reports/sql-proposal-<topic>-<YYYYMMDD>.md` with DDL, rollback, RLS, indexes, PII.
4. **Operator approval** → decision log.
5. **Execute:** `apply_migration` or KiRBe repo migration — **never** ad-hoc prod DDL without a file.

**Forbidden until approval:** mutating `execute_sql`, `apply_migration`.
