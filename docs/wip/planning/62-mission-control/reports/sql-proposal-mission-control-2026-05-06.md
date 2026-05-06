---
language: en
status: active
initiative: 62-mission-control
report_kind: sql-proposal
program_id: shared
plane: ops
authority: System Owner + Founder
last_review: 2026-05-06
---

# SQL proposal — I62 P1.3 + P2.3 + P3.1 (Mission Control schema bundle)

> **Operator approval gate G-62-A + G-62-B.** Per [`operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md), DDL only lands after the operator runs the migrations against the live Supabase project.
>
> All three migrations land in **one operator session** (per R-62-1 mitigation). The operator runs them in order from the AKOS-side `supabase/migrations/` folder.

## Migration set

| File | Purpose | Phase | Reversibility |
|:---|:---|:---|:---|
| [`20260506130000_i62_p1_holistika_ops_rbac.sql`](../../../../../supabase/migrations/20260506130000_i62_p1_holistika_ops_rbac.sql) | RBAC: `holistika_ops.user_role_mapping` + `audit_log` + `user_preferences` + `notifications` + `current_access_level()` helper | P1.3 | DROP TABLE … CASCADE on each table |
| [`20260506130100_i62_p2_erp_schema_views.sql`](../../../../../supabase/migrations/20260506130100_i62_p2_erp_schema_views.sql) | `erp.*` schema + `_mode()` + 6 views (`vw_three_lights_status`, `vw_mirror_health`, `vw_initiative_pulse`, `vw_operator_inbox_top`, `vw_mission_control_today`, `vw_public_health`) | P2.3 | DROP SCHEMA erp CASCADE |
| [`20260506130200_i62_p3_demo_schema.sql`](../../../../../supabase/migrations/20260506130200_i62_p3_demo_schema.sql) | `demo.*` schema with shape-matching tables for showcase mode | P3.1 | DROP SCHEMA demo CASCADE |

## How to apply

```bash
# 1) Link the local Supabase CLI to the production project (one-time):
supabase link --project-ref <project-ref>

# 2) Apply migrations:
supabase db push

# 3) Verify:
supabase db inspect schemas
# Expected: erp, demo, holistika_ops, compliance, finops, public, auth, storage, realtime
```

Or apply via the Supabase SQL editor by pasting each file in order.

## Verification queries

```sql
-- Confirm holistika_ops tables and row counts (expected: 0 rows in each)
SELECT count(*) FROM holistika_ops.user_role_mapping;
SELECT count(*) FROM holistika_ops.audit_log;
SELECT count(*) FROM holistika_ops.user_preferences;
SELECT count(*) FROM holistika_ops.notifications;

-- Confirm erp views exist
SELECT table_name FROM information_schema.views
WHERE table_schema = 'erp' ORDER BY table_name;
-- Expected: vw_initiative_pulse, vw_mirror_health, vw_mission_control_today,
--           vw_operator_inbox_top, vw_public_health, vw_three_lights_status

-- Confirm erp.vw_public_health is anon-readable
SET ROLE anon;
SELECT * FROM erp.vw_public_health;  -- should succeed
RESET ROLE;

-- Confirm demo schema is empty
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'demo' ORDER BY table_name;
-- Expected: dossier_run, eval_run, initiative_registry_mirror, ops_register_mirror,
--           persona_registry_mirror, skill_registry_mirror

-- Test the access_level helper (run as a signed-in user)
SELECT holistika_ops.current_access_level();
```

## Bootstrap data: founder + operator user_role_mapping rows

After the migrations apply and the founder + first operator have signed in via Supabase Auth (creating rows in `auth.users`), run:

```sql
-- One-shot bootstrap: insert the founder mapping (replace email + role_id)
INSERT INTO holistika_ops.user_role_mapping (user_id, email, role_id, access_level, display_name, status)
SELECT id, email, 'role_admin_founder', 6, 'Founder', 'active'
FROM auth.users
WHERE email = '<founder-email>'
ON CONFLICT (user_id) DO UPDATE
SET role_id = EXCLUDED.role_id, access_level = EXCLUDED.access_level,
    display_name = EXCLUDED.display_name, updated_at = now();
```

The ongoing daily-sync job (P1.3 follow-up) will auto-populate new rows from `compliance.baseline_organisation_mirror` for any team member whose email matches a baseline_organisation row.

## Demo-mode routing notes

The shipped views currently read **only from `compliance.*`** for live data. The session-GUC routing pattern (`SET app.data_mode = 'demo'`) is plumbed via `erp._mode()` and exposed as a column on every view, but the actual schema switching for demo mode happens via **a `search_path` rewrite** on the application's Supabase client when `DATA_MODE=demo`:

```ts
// hlk-erp side (lib/supabase/server.ts):
if (process.env.DATA_MODE === 'demo') {
  await supabase.rpc('set_config', { setting: 'search_path', value: 'demo, public' })
  await supabase.rpc('set_config', { setting: 'app.data_mode', value: 'demo' })
}
```

This is set per-request (server-rendered surfaces) and per-tab (client-side surfaces). The `demo.*` schema mirrors the canonical column set so unqualified queries resolve cleanly. View bodies in `erp.*` will be migrated to `UNION ALL`-routed bodies in P3.5 (operator-approval gate G-62-C) once the seed script is in CI; until then, the live and demo deploys are isolated by separate Supabase projects (D-IH-62-D + R-62-4 mitigation).

## Operator approval

> **G-62-A + G-62-B + G-62-C: Approve to apply migrations.**
> Approval signature: ____________________ · date: ____________________

After the operator signs and runs the migrations, append the live `list_schemas` and `list_tables` output to this report (overwriting the §1 expected outputs in `sql-discovery-2026-05-06.md`) for traceability.
