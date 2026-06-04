---
intellectual_kind: verification_report
initiative: I93
phase: P6
authored: 2026-06-04
supabase_project: MasterData (swrmqpelgoblaquequzb)
---

# P6 Supabase verification — OPS-86-15 mirrors

## Operator actions observed (terminal 11)

| Step | Result |
|:---|:---|
| `npm run supabase db push` | ✅ Applied `20260604120000_i93_p6_ops8615_mirror_gap_closure.sql` |
| Policy NOTICE lines | ✅ Expected on first CREATE (`DROP POLICY IF EXISTS` pattern) |
| `sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only` | ✅ Wrote `/tmp/ops8615-upsert.sql` (~3.5 MB) |
| Re-run emit (2026-06-05) | ✅ Idempotent regenerate — writes **repo-local** `artifacts/ops8615-mirror-upsert.sql` (not `/tmp`); **does not load rows** until SQL Editor run |

## Live database check (2026-06-04)

| Check | Expected | Actual |
|:---|:---|:---|
| Five tables exist in `compliance` | Yes | ✅ All present |
| RLS enabled | Yes | ✅ All five |
| Service-role policy | 1 per table | ✅ 1 each |
| Row counts | 5 / 9 / 1119 / 1119 / 2 | **0 / 0 / 0 / 0 / 0** |

## Verdict

**DDL: PASS** — schema matches repo migration.  
**DML: PENDING** — upsert file was generated locally but **not executed** against Supabase yet.

## Operator next step (one-time)

**Do not paste the 3.5 MB monolith into the SQL Editor** — Dashboard limit. Use Holistika DML gate:

1. `py scripts/verify.py ops8615_mirror_emit` — or `py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only --ops8615-split`
2. Apply `artifacts/ops8615-batches/*.sql` via **psql** (see [`artifacts/README.md`](../artifacts/README.md)); Editor OK for 01/02/05 only.
3. Re-check counts:

```sql
SELECT 'aic_registry_mirror' AS t, count(*) FROM compliance.aic_registry_mirror
UNION ALL SELECT 'audience_registry_mirror', count(*) FROM compliance.audience_registry_mirror
UNION ALL SELECT 'capability_registry_mirror', count(*) FROM compliance.capability_registry_mirror
UNION ALL SELECT 'capability_confidence_registry_mirror', count(*) FROM compliance.capability_confidence_registry_mirror
UNION ALL SELECT 'country_work_calendar_mirror', count(*) FROM compliance.country_work_calendar_mirror;
```

Expected: 5, 9, 1119, 1119, 2.

Repo-native probe `py scripts/dataops_quality_check.py --data-fam COMPLIANCE-MIRROR` remains **PASS** (DDL + emit symbols).
