---
language: en
status: applied-partial
initiative: 62-mission-control
report_kind: migration-application
last_review: 2026-05-07
---

# I62 Supabase migration application — 2026-05-07

Operator-approved DDL run against the `MasterData` Supabase project (`swrmqpelgoblaquequzb`, eu-central-1, postgres 15.8.1). Operator approval captured by user response on 2026-05-07. Executed via the AKOS user-supabase MCP `apply_migration` tool.

## Outcome summary

| Migration | File | Applied | Notes |
|:---|:---|:---|:---|
| **P1 — RBAC** | [`supabase/migrations/20260506130000_i62_p1_holistika_ops_rbac.sql`](../../../../../supabase/migrations/20260506130000_i62_p1_holistika_ops_rbac.sql) | YES | Migration version `20260507010953`. 4 tables + 1 helper fn applied. |
| **P2 — erp.* views** | [`supabase/migrations/20260506130100_i62_p2_erp_schema_views.sql`](../../../../../supabase/migrations/20260506130100_i62_p2_erp_schema_views.sql) | **NO — dependency gap** | Blocked by missing prerequisite mirrors (see Gap below). |
| **P3 — demo.* schema** | [`supabase/migrations/20260506130200_i62_p3_demo_schema.sql`](../../../../../supabase/migrations/20260506130200_i62_p3_demo_schema.sql) | YES | Migration version `20260507011236`. 6 demo tables + permissive read policies. |

`list_migrations` confirms both new entries are now in the `supabase_migrations.schema_migrations` ledger.

## What now exists in the database

### `holistika_ops` schema (P1)

```
holistika_ops.audit_log
holistika_ops.notifications
holistika_ops.user_preferences
holistika_ops.user_role_mapping
holistika_ops.current_access_level()  -- function
```

All four tables ship with RLS enabled and policies wired:

- `user_role_mapping`: self-read + admin-read (access_level >= 6) + service_role-all
- `audit_log`: admin-read only + service_role-all (founder impersonation surface)
- `user_preferences`: self-modify + service_role-all
- `notifications`: self-or-broadcast read + self-update + service_role-all

### `demo` schema (P3)

```
demo.dossier_run
demo.eval_run
demo.initiative_registry_mirror
demo.ops_register_mirror
demo.persona_registry_mirror
demo.skill_registry_mirror
```

All six tables: RLS on, permissive read for everyone (anon + authenticated), writes restricted to `service_role`. Empty until `scripts/seed-demo.ts` runs in CI on preview deploys.

## Gap — P2 cannot apply yet (D-IH-62-Q open question)

P2 references mirror tables and column shapes that don't currently exist on the remote:

| Reference in P2 SQL | Status on remote |
|:---|:---|
| `compliance.eval_run.run_payload` (jsonb) | column missing — actual columns: `eval_run_id`, `run_started_at`, `overall_status`, `skill_id`, `judge_scores`, ... |
| `compliance.eval_run.kind` | column missing |
| `compliance.eval_run.verdict` | column missing |
| `compliance.eval_run.occurred_at` | column missing (it's `run_started_at`) |
| `compliance.dossier_run.verdict` | column missing |
| `compliance.dossier_run.run_payload` | column missing (it's `section_metrics`) |
| `compliance.skill_registry_mirror.status` | column missing (it's `lifecycle_status`) |
| `compliance.initiative_registry_mirror` | **table missing** |
| `compliance.ops_register_mirror` | **table missing** |
| `compliance.adviser_disciplines_mirror` | name mismatch — actual is `adviser_engagement_disciplines_mirror` |
| `compliance.finops_counterparty_mirror` | name mismatch — actual is `finops_counterparty_register_mirror` |

Two missing **tables** (`initiative_registry_mirror`, `ops_register_mirror`) are the hard blockers; the rest are column/name harmonisations that can be solved by adapting the view DDL.

### Resolution plan (queued as I62 P11 follow-up)

1. **Mirror DDL tranche** — create `compliance.initiative_registry_mirror` and `compliance.ops_register_mirror` with the schemas implied by `akos/hlk_initiative_registry_csv.py` and `akos/hlk_ops_register_csv.py`. Either via a new migration in `supabase/migrations/` or as `compliance_mirror_emit` upserts (per the AKOS rule on Supabase DDL vs mirror DML).
2. **Column harmonisation** — minor amendment to the P2 SQL to use `run_started_at`, `overall_status`, `lifecycle_status`, `section_metrics`, plus the corrected mirror names.
3. **Re-apply P2** — once 1 + 2 land, P2 should apply cleanly.

OPS row to file: `OPS-62-P11 — apply remaining I62 mirror DDL + adapt P2 view names`. Owner: System Owner. Class: engineering.

## hlk-erp impact

The hand-typed views in [`hlk-erp/lib/supabase/types.ts`](https://github.com/FraysaXII/hlk-erp/blob/main/lib/supabase/types.ts) for `erp.vw_*` will return 404 from Supabase until P2 applies. Until then:

- `/mission-control` Today board renders cached fixture data + the "Demo mode" banner (`demo.*` tables are populated, `erp._mode()` returns `demo` on preview).
- `/operator-inbox`, `/initiatives`, `/decisions`, `/cycle-closures` drilldowns will show empty + the "live data unavailable" banner.
- Three Lights chip on the hero defaults to AMBER until P2 lands and `vw_three_lights_status` returns rows.

## Advisors output

Both `get_advisors --type security` and `get_advisors --type performance` were captured. Zero advisories match the new `holistika_ops.*` or `demo.*` schemas — both pass clean.

(Other advisories from preexisting tables are unchanged.)

## Trace

- Operator approval: user response on 2026-05-07.
- MCP server: `user-supabase` (`apply_migration` tool).
- Project: `MasterData` (`swrmqpelgoblaquequzb`).
- Decision logged: see [`../decision-log.md`](../decision-log.md) — D-IH-62-W "P2 deferred pending mirror DDL".
