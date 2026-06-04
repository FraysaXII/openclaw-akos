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
| Re-run emit (2026-06-05, terminal 11) | ✅ Idempotent regenerate (~3 482 296 bytes) — **does not load rows**; still requires SQL Editor execution |

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

1. Supabase Dashboard → SQL Editor → paste/run `C:\tmp\ops8615-upsert.sql` (or split into batches if editor times out).
2. Re-check counts:

```sql
SELECT 'aic_registry_mirror' AS t, count(*) FROM compliance.aic_registry_mirror
UNION ALL SELECT 'audience_registry_mirror', count(*) FROM compliance.audience_registry_mirror
UNION ALL SELECT 'capability_registry_mirror', count(*) FROM compliance.capability_registry_mirror
UNION ALL SELECT 'capability_confidence_registry_mirror', count(*) FROM compliance.capability_confidence_registry_mirror
UNION ALL SELECT 'country_work_calendar_mirror', count(*) FROM compliance.country_work_calendar_mirror;
```

Expected: 5, 9, 1119, 1119, 2.

Repo-native probe `py scripts/dataops_quality_check.py --data-fam COMPLIANCE-MIRROR` remains **PASS** (DDL + emit symbols).
