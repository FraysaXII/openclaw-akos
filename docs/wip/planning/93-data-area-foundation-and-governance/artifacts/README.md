# I93 operator artifacts — OPS-86-15 mirror DML

## Why the Supabase SQL Editor rejected the monolith

The combined upsert is ~3.5 MB (~2,200 single-row `INSERT`s). The Dashboard SQL Editor has a
**size limit** and a **~1 minute timeout** — it is for short DDL/DML probes, not bulk mirror sync.

That matches Holistika **two-plane** doctrine:

| Plane | What you did | Correct tool |
|:---|:---|:---|
| **DDL** (schema) | `npm run supabase db push` for `20260604120000_i93_p6_ops8615_mirror_gap_closure.sql` | Supabase CLI / migrations |
| **DML** (mirror rows) | Git CSV → upsert SQL → load into `compliance.*_mirror` | **Not** a migration file; **not** the SQL Editor for bulk |

SSOT: [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) and
[`operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md).

General compliance mirrors use:

```powershell
py scripts/verify.py compliance_mirror_emit
```

That writes `artifacts/sql/compliance_mirror_upsert.sql` (all mirrors). OPS-86-15 gap tables are
**separate** — use the commands below.

---

## Recommended: generate batches, apply with linked Supabase CLI

Repo-wide standard: [`docs/guides/holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md).

### 1. Generate five batch files

```powershell
py scripts/verify.py ops8615_mirror_emit
```

Same as `py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only --ops8615-split`.

Writes `artifacts/ops8615-batches/01-aic_registry.sql` … `05-country_work_calendar.sql` plus
`MANIFEST.md` with row counts.

### 2. Apply via linked CLI (preferred in this repo)

Requires `npx supabase link` on MasterData (same session as `db push`):

```powershell
cd c:\Users\Shadow\cd_shadow\openclaw-akos
pwsh -File scripts/apply_mirror_batches.ps1 -Preset ops8615
```

Runs `npm run supabase db query --linked -f` on each batch in order; log under `artifacts/sql/`.

### 2b. Apply via psql (alternative)

From Dashboard → **Connect** → copy the **Session pooler** URI (port **5432**), then apply each
`ops8615-batches/*.sql` with `psql -f`. See the holistika-mirror-dml-apply guide Method B.

### 3. Verify counts

```sql
SELECT 'aic_registry_mirror' AS t, count(*)::int AS n FROM compliance.aic_registry_mirror
UNION ALL SELECT 'audience_registry_mirror', count(*) FROM compliance.audience_registry_mirror
UNION ALL SELECT 'capability_registry_mirror', count(*) FROM compliance.capability_registry_mirror
UNION ALL SELECT 'capability_confidence_registry_mirror', count(*) FROM compliance.capability_confidence_registry_mirror
UNION ALL SELECT 'country_work_calendar_mirror', count(*) FROM compliance.country_work_calendar_mirror;
```

Expected: **5 / 9 / 1119 / 1119 / 2**.

Or: `py scripts/probe_compliance_mirror_drift.py` (after saving MCP probe JSON per CONTRIBUTING.md).

---

## SQL Editor–only path (small tables)

If you cannot use psql, run **only** these batch files in the Editor (in order):

1. `01-aic_registry.sql` (5 rows)
2. `02-audience_registry.sql` (9 rows)
3. `05-country_work_calendar.sql` (2 rows)

Files **03-capability_registry.sql** and **04-capability_confidence_registry.sql** (~1,119 rows each)
are still too large for the Editor — use **psql** for those two.

---

## Monolith file (optional)

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only
```

Writes `ops8615-mirror-upsert.sql` in this folder (~3.5 MB, gitignored). Use **psql** on the
monolith if you prefer one transaction; do not paste into the SQL Editor.

---

## Preflight

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only --count-only
```
