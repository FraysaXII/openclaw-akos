# Holistika mirror DML apply (operator guide)

**When:** After canonical compliance CSVs change and mirror **DDL** is already on Supabase
(`npm run supabase db push` / migration applied).

**SSOT for two-plane doctrine:** [`operator-sql-gate.md`](../wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) · [`.cursor/rules/akos-holistika-operations.mdc`](../../.cursor/rules/akos-holistika-operations.mdc)

Git CSVs are authoritative. Mirror tables are **projections**. Never author business data in the Dashboard; never put bulk `INSERT` batches in `supabase/migrations/`.

---

## Apply methods (pick one)

| Method | When to use | Requires |
|:---|:---|:---|
| **A — Linked Supabase CLI** (preferred in this repo) | Day-to-day on a linked Holistika project (MasterData) | `npx supabase login`, `npx supabase link`, repo root |
| **B — psql** | CI headless, no Management API, or very large one-off files | Connection string from Dashboard → Connect |
| **C — SQL Editor** | Single-table smoke tests only (≤ ~50 rows) | Dashboard paste |

Methods A and B are equally valid. **A** is the default here because the repo is always linked, batches are logged, and you avoid copying passwords into shell history.

---

## Method A — Emit + apply (canonical loop)

### Step 1 — Preflight + emit SQL

**Full compliance mirror bundle** (process_list, baseline, GOI/POI, adviser registers, etc.):

```powershell
cd c:\Users\Shadow\cd_shadow\openclaw-akos
py scripts/verify.py compliance_mirror_emit
```

Writes `artifacts/sql/compliance_mirror_upsert.sql` (gitignored). For large full-bundle applies, split into chunks first (see initiative 22a / `scripts/sql/mirror-batches/` pattern) or use Method B on the monolith.

**OPS-86-15 gap mirrors only** (I93 P6 — five tables):

```powershell
py scripts/verify.py ops8615_mirror_emit
```

Same as:

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only --ops8615-split
```

Output: `docs/wip/planning/93-data-area-foundation-and-governance/artifacts/ops8615-batches/*.sql`

### Step 2 — Apply batches to linked remote DB

```powershell
pwsh -File scripts/apply_mirror_batches.ps1 -Preset ops8615
```

Or any custom batch directory:

```powershell
pwsh -File scripts/apply_mirror_batches.ps1 -BatchDir "artifacts/sql/mirror-batches/20260504"
```

The script runs `npx supabase db query --linked --file <each-chunk>.sql` in sorted order, logs to `artifacts/sql/`, and stops on first non-zero exit code.

**Prerequisites:** run from repo root; project must be **linked** (`npx supabase link --project-ref <ref>`). Same auth session as `npm run supabase db push`.

### Step 3 — Verify row counts

```powershell
npm run supabase -- db query --linked "SELECT count(*) FROM compliance.<mirror_table>" --output table
```

Or initiative-specific probe, e.g.:

```powershell
py scripts/probe_compliance_mirror_drift.py --emit-sql
# paste result via MCP, then:
py scripts/probe_compliance_mirror_drift.py --verify
```

---

## Method B — psql (alternative)

1. Emit SQL (same as Step 1 above).
2. Dashboard → **Connect** → **Session pooler** URI (port 5432).
3. Apply each `.sql` file:

```powershell
psql "<connection-string>" -f path\to\batch.sql
```

Use `set statement_timeout = '30min';` for large files. See [Supabase: long-running queries](https://supabase.com/docs/guides/troubleshooting/avoiding-timeouts-in-long-running-queries-6nmbdN).

---

## Method C — SQL Editor (limited)

Do **not** paste multi-megabyte upsert bundles — the Editor rejects them.

OK for tiny batches (e.g. OPS-86-15 files `01-aic_registry.sql`, `02-audience_registry.sql`, `05-country_work_calendar.sql`). Files `03` and `04` (~1.1k rows each) still need Method A or B.

---

## Quick reference — OPS-86-15 mirrors

| Mirror | Expected rows |
|:---|---:|
| `compliance.aic_registry_mirror` | 5 |
| `compliance.audience_registry_mirror` | 9 |
| `compliance.capability_registry_mirror` | 1119 |
| `compliance.capability_confidence_registry_mirror` | 1119 |
| `compliance.country_work_calendar_mirror` | 2 |

One-shot verify:

```powershell
npm run supabase -- db query --linked "SELECT 'aic' t, count(*)::int n FROM compliance.aic_registry_mirror UNION ALL SELECT 'audience', count(*)::int FROM compliance.audience_registry_mirror UNION ALL SELECT 'capability', count(*)::int FROM compliance.capability_registry_mirror UNION ALL SELECT 'cap_conf', count(*)::int FROM compliance.capability_confidence_registry_mirror UNION ALL SELECT 'calendar', count(*)::int FROM compliance.country_work_calendar_mirror" --output table
```

---

## Related automation

| Artifact | Role |
|:---|:---|
| [`scripts/sync_compliance_mirrors_from_csv.py`](../../scripts/sync_compliance_mirrors_from_csv.py) | Emit upsert SQL from git CSVs |
| [`scripts/apply_mirror_batches.ps1`](../../scripts/apply_mirror_batches.ps1) | Apply batch directory via `db query --linked` |
| [`config/verification-profiles.json`](../config/verification-profiles.json) | `compliance_mirror_emit`, `ops8615_mirror_emit` profiles |
| [`supabase/README.md`](../../supabase/README.md) | DDL quick card |
