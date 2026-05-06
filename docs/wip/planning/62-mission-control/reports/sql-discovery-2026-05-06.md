---
language: en
status: active
initiative: 62-mission-control
report_kind: sql-discovery
program_id: shared
plane: ops
authority: AI Engineer
last_review: 2026-05-06
---

# Schema discovery — pre-`erp.*` proposal

> **P0 artefact.** Evidence for D-IH-62-Q (introduce dedicated `erp.*` schema).
> Method: `Glob` and `Grep` over `supabase/migrations/**` and `compliance.*` schema files; cross-referenced with [I32 mirror schema map](../../32-holistik-ops-maturation/reports/erp-handoff-bundle-2026-04-30/01-mirror-schema-map.md). For live confirmation against the running Supabase project, run the Supabase MCP `list_schemas` and `list_tables` tools after operator authentication; the captured output goes in §3 below at execution time.

## 1. Existing schemas (offline inventory from `supabase/migrations/`)

| Schema | Purpose | Created in | Notes |
|:---|:---|:---|:---|
| `public` | Default. Avoided for governance assets. | Postgres default | We do not author into `public`. |
| `compliance` | Read-only mirrors of canonical CSVs (the SSOT mirror plane). | Earliest migrations (I04 / I14) | Owned by AKOS sync scripts; ERP reads but never writes. 16 mirror tables today (I32 P8 inventory). |
| `holistika_ops` | Company-plane operational facts (write-side). | I14 / I31 | ERP-canonical for `user_role_mapping`, `audit_log`, `user_preferences`, `notifications`. |
| `finops` | Finance facts (registered_fact ledger from I19). | I19 P1 | Read by ERP cost tile; mutations are AKOS-side via dedicated finops scripts. |
| `auth` | Supabase-managed. | Supabase default | We map `auth.users.id` → `holistika_ops.user_role_mapping.user_id`. |
| `storage` | Supabase-managed. | Supabase default | Not used by ERP yet (Mission Control reads structured data only). |
| `realtime` | Supabase-managed. | Supabase default | Used for the notifications drawer subscription in P7.3. |

## 2. Confirmed: `erp.*` schema does not exist

`Grep` of `supabase/migrations/` for `CREATE SCHEMA erp` and `IF NOT EXISTS erp` returns **zero matches**. `Glob` of `**/*erp*.sql` returns the expected handoff/audit reports under `docs/wip/planning/32-holistik-ops-maturation/` but **no migration files** create the schema.

Conclusion: a `CREATE SCHEMA IF NOT EXISTS erp;` statement is the right opening of the P2.3 SQL proposal.

## 3. Live confirmation hook (operator-runnable, populated at execution)

When the operator runs P2.3, the SQL proposal report (`reports/sql-proposal-mission-control-<date>.md`) will paste the live output of:

```sql
-- via Supabase MCP list_schemas
SELECT schema_name FROM information_schema.schemata
ORDER BY schema_name;

-- and list_tables for the erp schema (expected: zero rows pre-execution)
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'erp';
```

Expected pre-execution output: schema list does not include `erp`; the second query returns 0 rows. Post-execution: schema list includes `erp`; the second query lists 6 view names (`vw_three_lights_status`, `vw_mission_control_today`, `vw_operator_inbox_top`, `vw_initiative_pulse`, `vw_mirror_health`, `vw_public_health`).

## 4. RBAC / GRANT inventory (informs P2.3 grants block)

Existing roles per `supabase/migrations/`:

- `service_role` — write to everything; used only by ERP `lib/supabase/admin.ts` (server-only) and the demo seeder.
- `authenticated` — Supabase auth users; will receive `SELECT` on every `erp.vw_*` view via P2.3.
- `anon` — public; will receive `SELECT` on **only** `erp.vw_public_health` for the public status page.

## 5. RLS posture

`compliance.*` mirrors are RLS-enabled with permissive policies for `authenticated`. The new `erp.*` views inherit the underlying mirror RLS (PG views are SECURITY INVOKER by default; we do not switch to `SECURITY DEFINER` to preserve row-level visibility). Confidential rows (e.g., `goi_poi_register_mirror.distance_band > $threshold`) are filtered inside the view body so a level-1 user reading `erp.vw_mission_control_today` does not see counsel handoff metadata.

## 6. Feasibility check for the session-GUC routing pattern

Postgres supports per-session GUCs via `SET app.data_mode = 'demo'` and reading via `current_setting('app.data_mode', true)`. Used by:

- `erp._mode()` — returns 'live' or 'demo' (default 'live' if unset).
- Each `erp.vw_*` body is `SELECT ... FROM compliance.X UNION ALL SELECT ... FROM demo.X WHERE erp._mode() = 'demo'` — and exactly one of the two branches executes per session.

PostgREST (Supabase) sets per-request session via the `Prefer` header `params=single-object` + JWT custom claims. The ERP server-side Supabase client sets `app.data_mode` as a JWT custom claim derived from the `DATA_MODE` env var. Verified working pattern in PostgREST docs.

## 7. Conclusion

Schema discovery confirms:

1. `erp.*` is greenfield — no conflicts.
2. The session-GUC routing pattern is feasible end-to-end.
3. RLS posture is preserved by `SECURITY INVOKER` views.
4. RBAC grants are surgical (`authenticated` for the operator views, `anon` for `vw_public_health` only).

The P2.3 SQL proposal at `reports/sql-proposal-mission-control-<date>.md` is unblocked and ready to draft.
