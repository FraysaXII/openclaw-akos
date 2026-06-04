# I93 operator artifacts (generated SQL)

## OPS-86-15 mirror upsert (P6)

**Default output path** (repo-local — do not use `/tmp` on Windows):

`docs/wip/planning/93-data-area-foundation-and-governance/artifacts/ops8615-mirror-upsert.sql`

Regenerate from repo root:

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only
```

Apply after migration `supabase/migrations/20260604120000_i93_p6_ops8615_mirror_gap_closure.sql`:

1. Supabase Dashboard → SQL Editor  
2. Paste/run `ops8615-mirror-upsert.sql` (batch if the editor times out)  
3. Expected row counts: **5 / 9 / 1119 / 1119 / 2**

The `.sql` file is gitignored (multi-MB); the README + command are SSOT for rediscovery.
