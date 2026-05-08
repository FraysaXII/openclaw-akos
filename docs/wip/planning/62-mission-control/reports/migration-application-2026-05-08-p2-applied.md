---
language: en
status: applied-full
initiative: 62-mission-control
report_kind: migration-application
last_review: 2026-05-08
---

# I62 P2 v2 + I59 mirror DDL catch-up — 2026-05-08

Operator-approved DDL run against the `MasterData` Supabase project (`swrmqpelgoblaquequzb`) via the AKOS user-supabase MCP `apply_migration` and `execute_sql` tools. Closes the P2 gap documented in [`migration-application-2026-05-07.md`](migration-application-2026-05-07.md).

## Outcome summary

| Migration | File | Applied | Notes |
|:---|:---|:---|:---|
| **I59 P1.2 — initiative_registry_mirror DDL** | [`supabase/migrations/20260506120100_i59_initiative_registry_mirror.sql`](../../../../../supabase/migrations/20260506120100_i59_initiative_registry_mirror.sql) | YES | catch-up apply, version `i59_initiative_registry_mirror` |
| **I59 P1.3 — ops_register_mirror DDL** | [`supabase/migrations/20260506120200_i59_ops_register_mirror.sql`](../../../../../supabase/migrations/20260506120200_i59_ops_register_mirror.sql) | YES | catch-up apply, version `i59_ops_register_mirror` |
| **I62 P2.5 — relax title NOT NULL on ops_register_mirror** | (inline) | YES | data-contract harmonisation; canonical CSV has empty titles for 21/22 OPS rows. Replaced with CHECK that `status='open' OR title not blank`. |
| **I62 P2 v2 — erp.* schema views (adapted)** | [`supabase/migrations/20260508000000_i62_p2_erp_schema_views_v2.sql`](../../../../../supabase/migrations/20260508000000_i62_p2_erp_schema_views_v2.sql) | YES | rewrite of original P2 to match remote column shapes |

## What changed vs the original P2

The 2026-05-06 P2 SQL referenced columns and table names that don't exist on the remote. Adaptations:

| P2 v1 (rejected) | P2 v2 (applied) |
|:---|:---|
| `compliance.eval_run.kind = 'persona_fit'` | `compliance.eval_run.mode = 'persona_fit'` |
| `(run_payload->>'persona_fit_pass')::bool` | `(overall_status = 'pass')` |
| `eval_run.verdict` | `eval_run.overall_status` |
| `eval_run.occurred_at` | `eval_run.run_started_at` |
| `eval_run.run_payload->>'skill_id'` | `eval_run.skill_id` (column) |
| `dossier_run.verdict = 'GO'` + `run_payload` | `(section_metrics->>'verdict') = 'GO'` + `section_metrics` jsonb |
| `skill_registry_mirror.status` | `skill_registry_mirror.lifecycle_status` |
| `compliance.adviser_disciplines_mirror` | `compliance.adviser_engagement_disciplines_mirror` |
| `compliance.finops_counterparty_mirror` | `compliance.finops_counterparty_register_mirror` |
| `vw_operator_inbox_top.ops_id` from `o.ops_id` | `vw_operator_inbox_top.ops_id` from `o.ops_action_id` (rename) |
| `o.initiative_id`, `o.cycle_id`, `o.last_review` | `o.originating_initiative_id` (renamed), `cycle_id` + `last_review` null-padded for backwards-compat |

Empty-fallback behavior was added to `vw_three_lights_status` so the view returns 1 row even when `compliance.dossier_run` is empty (UNION ALL fallback + LEFT JOIN in `vw_mission_control_today`).

## Mirror seeding

Two compact multi-VALUES upserts applied via `execute_sql`:

| Mirror | Rows seeded | Source |
|:---|:---|:---|
| `compliance.initiative_registry_mirror` | 51 | [`docs/references/hlk/compliance/INITIATIVE_REGISTRY.csv`](../../../../references/hlk/compliance/INITIATIVE_REGISTRY.csv) (working tree, 2026-05-08) |
| `compliance.ops_register_mirror` | 22 | [`docs/references/hlk/compliance/OPS_REGISTER.csv`](../../../../references/hlk/compliance/OPS_REGISTER.csv) (working tree, 2026-05-08) |

The default `scripts/sync_compliance_mirrors_from_csv.py` emit-format renders empty CSV cells as `''` literals, which Postgres rejects on DATE/INT/NUMERIC columns. Two helper scripts ship under `build/` (gitignored — one-shot transient artifacts):

- `build/nullify_empty_literals.py` — generic SQL string-aware substitution from `''` to NULL outside of string literals
- `build/registry_compact_upserts.py` — emits one multi-VALUES INSERT for the registry CSV (~21 KB vs ~80 KB in the legacy per-row format)

## Mission Control "Today" view — current state

`select * from erp.vw_mission_control_today` post-seeding returns:

| field | value |
|:---|:---|
| verdict | RED |
| conversational_light | AMBER |
| dossier_light | AMBER |
| skill_quality_light | RED |
| active_count | 8 |
| closed_count | 29 |
| gated_operator_count | 1 |
| closures_last_30_days | 11 days, 29 closures total |
| mirrors_total / green / red | 16 / 2 / 14 |
| operator_inbox_open | 21 |
| eval_runs_24h | 0 |
| last_dossier_verdict | unknown (empty `compliance.dossier_run`) |
| data_mode | live |

Verdict is RED because:
- Skill quality is RED (zero passing eval_runs in the last 7 days)
- 14 of 16 mirrors are stale (>48h old)

Both expected; the verdict will move once eval_runs land and the mirror sync cadence returns.

## hlk-erp impact

`/mission-control` Today board, `/operator-inbox`, `/initiatives` drilldowns now return live `compliance.*` data from PostgREST instead of empty fixtures. The "Three Lights chip" will surface the current RED verdict honestly rather than the previous AMBER "live data unavailable" fallback.

## Trace

- Operator approval: previous-session "F) Do all of the above in order" + "Skip — set placeholder values for now" path response.
- MCP server: `user-supabase` (`apply_migration`, `execute_sql`).
- Project: `MasterData` (`swrmqpelgoblaquequzb`).
- Decision: D-IH-62-W ("P2 deferred pending mirror DDL") closed with "P2 v2 applied 2026-05-08".
