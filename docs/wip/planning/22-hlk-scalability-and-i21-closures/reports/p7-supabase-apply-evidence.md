# P7 — Live Supabase mirror apply evidence

**Initiative**: 22 (Scalable HLK hierarchy + i21 closures)  
**Date**: 2026-04-29  
**Operator**: Founder (Holistika), via user-supabase MCP `apply_migration` + `execute_sql`  
**Project**: `MasterData` (`swrmqpelgoblaquequzb`, region `eu-central-1`, postgres 15.8.1.111)  
**Decision authority**: D-IH-7 (this initiative's decision log).  
**Source git sha** at the time of the seed DML: `71eb3985c58492dcea5dd8524493ab912b386a1f`.

This report records the live-apply step that closed Initiative 21's "DEFERRED — live Supabase mirror DDL apply" UAT row.

## Pre-apply discovery (read-only)

Tools: `list_projects`, `list_migrations`, `list_tables`.

- Two Supabase projects available: `MasterData` and `hlk-shopify-cart-drawer`. Initiative-21 DDL targets `MasterData`.
- Migration ledger before apply ended at `20260423014326_i19_finops_ledger_phase1`.
- `compliance` schema present with mirrors for `process_list`, `baseline_organisation`, `finops_counterparty_register`, plus the legacy taxonomy tables (`access_level`, `confidence_level`, `source_category`, `source_level`). The four Initiative-21 mirrors were absent.

## Apply step 1 — DDL via MCP `apply_migration`

Each migration was applied as its own MCP call. The MCP service stamps a fresh timestamp for the remote `schema_migrations` ledger; the local file timestamps were renamed afterwards to maintain ledger parity per [`supabase/migrations/README.md`](../../../../../supabase/migrations/README.md) and `akos-holistika-operations.mdc` §"Operator SQL gate".

| Local file (after rename) | Remote `version` | DDL summary |
|:--------------------------|:-----------------|:------------|
| `20260429081728_i21_compliance_goipoi_register_mirror.sql` | `20260429081728` | `compliance.goipoi_register_mirror` (PK `ref_id`, indexes on `synced_at`, `program_id`, `class`); RLS deny `anon`/`authenticated`; `service_role` GRANT |
| `20260429081734_i21_compliance_adviser_disciplines_mirror.sql` | `20260429081734` | `compliance.adviser_engagement_disciplines_mirror` (PK `discipline_id`, indexes on `synced_at`, `default_program_id`); RLS deny `anon`/`authenticated`; `service_role` GRANT |
| `20260429081754_i21_compliance_adviser_open_questions_mirror.sql` | `20260429081754` | `compliance.adviser_open_questions_mirror` (PK `question_id`, indexes on `synced_at`, `discipline_id`, `program_id`); RLS deny `anon`/`authenticated`; `service_role` GRANT |
| `20260429081800_i21_compliance_founder_filed_instruments_mirror.sql` | `20260429081800` | `compliance.founder_filed_instruments_mirror` (PK `instrument_id`, indexes on `synced_at`, `discipline_id`, `program_id`, `status`); RLS deny `anon`/`authenticated`; `service_role` GRANT |

All four MCP calls returned `{"success": true}`.

## Apply step 2 — Seed DML via MCP `execute_sql` (`service_role`)

Local upsert bundles generated with `py scripts/sync_compliance_mirrors_from_csv.py` and applied as multi-row `INSERT ... ON CONFLICT DO UPDATE` statements via MCP `execute_sql`. `service_role` is the implicit MCP context for `execute_sql`; `anon` and `authenticated` cannot read these tables (deny-all RLS).

| Mirror | Seed bundle (artifact) | Rows seeded | RETURNING ids verified |
|:-------|:-----------------------|:-----------:|:-----------------------|
| `compliance.goipoi_register_mirror` | `artifacts/sql/i21_goipoi_upsert.sql` | 6 | `GOI-ADV-ENTITY-2026`, `GOI-BNK-INC-2026`, `POI-BNK-DESK-LEAD-2026`, `POI-LEG-ENISA-LEAD-2026`, `POI-LEG-FISCAL-LEAD-2026`, `POI-ADV-INTAKE-LEAD-2026` |
| `compliance.adviser_engagement_disciplines_mirror` | `artifacts/sql/i21_adviser_disciplines_upsert.sql` | 6 | `legal`, `fiscal`, `ip`, `banking`, `certification`, `notary` |
| `compliance.adviser_open_questions_mirror` | `artifacts/sql/i21_adviser_questions_upsert.sql` | 12 | `Q-LEG-001..005`, `Q-FIS-001..002`, `Q-IPT-001`, `Q-BNK-001`, `Q-CRT-001..003` |
| `compliance.founder_filed_instruments_mirror` | `artifacts/sql/i21_filed_instruments_upsert.sql` | 1 | `INST-LEG-ESCRITURA-DRAFT-2026` |

## Post-apply row-count probe

```sql
SELECT 'goipoi_register_mirror' AS table_name, count(*)::text AS row_count FROM compliance.goipoi_register_mirror
UNION ALL SELECT 'adviser_engagement_disciplines_mirror', count(*)::text FROM compliance.adviser_engagement_disciplines_mirror
UNION ALL SELECT 'adviser_open_questions_mirror',         count(*)::text FROM compliance.adviser_open_questions_mirror
UNION ALL SELECT 'founder_filed_instruments_mirror',      count(*)::text FROM compliance.founder_filed_instruments_mirror
ORDER BY 1;
```

Result:

| `table_name` | `row_count` | CSV row count | Match |
|:------------|:-----------:|:-------------:|:-----:|
| `adviser_engagement_disciplines_mirror` | 6 | 6 | OK |
| `adviser_open_questions_mirror` | 12 | 12 | OK |
| `founder_filed_instruments_mirror` | 1 | 1 | OK |
| `goipoi_register_mirror` | 6 | 6 | OK |

## Security advisor

`get_advisors --type security` was run after the apply. Result: **no findings reference the four new mirrors**. Pre-existing INFO-level lints (RLS-enabled tables in other schemas without policies) are unrelated to Initiative 21/22.

## Migration ledger parity

After MCP apply, the local migration files were renamed from the original Initiative-21 file timestamps (`20260428190000..300`) to the remote ledger timestamps so `supabase migration list` reports parity for the next `supabase db push` window:

| Old local filename | New local filename (matches remote) |
|:-------------------|:------------------------------------|
| `20260428190000_i21_compliance_goipoi_register_mirror.sql` | `20260429081728_i21_compliance_goipoi_register_mirror.sql` |
| `20260428190100_i21_compliance_adviser_disciplines_mirror.sql` | `20260429081734_i21_compliance_adviser_disciplines_mirror.sql` |
| `20260428190200_i21_compliance_adviser_open_questions_mirror.sql` | `20260429081754_i21_compliance_adviser_open_questions_mirror.sql` |
| `20260428190300_i21_compliance_founder_filed_instruments_mirror.sql` | `20260429081800_i21_compliance_founder_filed_instruments_mirror.sql` |

`PRECEDENCE.md`, `CHANGELOG.md`, `ARCHITECTURE.md`, the i21 master roadmap, the i22 evidence matrix, and `FOUNDER_FILED_INSTRUMENT_REGISTER.md` were updated to reference the new filenames.

## Operator next steps (recommended)

- Refresh local CLI link: `supabase link --project-ref swrmqpelgoblaquequzb` (one-time) and `supabase migration list` to confirm both columns match for all rows.
- When canonical CSVs change, run `py scripts/verify.py compliance_mirror_emit` to regenerate the upsert bundle, then re-apply via MCP `execute_sql` (or via `psql` if the operator prefers CLI). The `ON CONFLICT (... ) DO UPDATE` clause keeps the seed idempotent.
- For drift detection: `SELECT count(*) FROM compliance.<mirror>` and compare against `py scripts/sync_compliance_mirrors_from_csv.py --count-only` output.
