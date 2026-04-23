# Supabase MCP verification — Initiative 16 + mirror refresh

**Project:** MasterData (`swrmqpelgoblaquequzb`)  
**Git HEAD (operator):** `8e3a21387254e80a73f94419010950c7aacca29a`  
**Date:** 2026-04-20

## Preconditions

- `py scripts/validate_hlk.py` — **PASS** (65 org roles, 1083 process items, 1 FINOPS vendor row).

## Migrations (`list_migrations`)

| version | name |
|---------|------|
| 20260418165339 | monitoring_logs_retention |
| 20260418183239 | i14_holistika_ops_lead_intake |
| 20260418193915 | i14_holistika_ops_lead_intake_captcha_columns |
| 20260420202847 | **i16_finops_vendor_register_mirror** |

**Note:** i16 DDL already applied; no second `apply_migration` for this tranche.

## Before refresh (SELECT)

| Table | Row count | max(synced_at) | sample source_git_sha (first row) |
|-------|-----------|----------------|-----------------------------------|
| `compliance.process_list_mirror` | 1069 | 2026-04-18 00:49:35+00 | `576c2d4545b5f459a5d648dd9c990e466e7ecb8b` |
| `compliance.baseline_organisation_mirror` | 65 | 2026-04-18 00:49:35+00 | `576c2d4545b5f459a5d648dd9c990e466e7ecb8b` |
| `compliance.finops_vendor_register_mirror` | 1 | 2026-04-20 20:31:08+00 | *(see post-refresh)* |

**Gap:** Process list mirror **14 rows behind** CSV expectation (1083 vs 1069).

## RLS (`pg_class.relrowsecurity`)

| relation | RLS enabled |
|----------|-------------|
| `compliance.process_list_mirror` | true |
| `compliance.baseline_organisation_mirror` | true |
| `compliance.finops_vendor_register_mirror` | true |

## After refresh

*(Fill in after you run the mirror upserts in the Supabase SQL editor — see below.)*

| Table | Row count | max(synced_at) | source_git_sha (spot-check) |
|-------|-----------|----------------|----------------------------|
| `compliance.process_list_mirror` | | | |
| `compliance.baseline_organisation_mirror` | | | |
| `compliance.finops_vendor_register_mirror` | | | |

**Spot-check:** `item_id` in `process_list_mirror`: `thi_finan_ws_4`, `thi_finan_dtp_303` — run after refresh:

```sql
select item_id, item_name from compliance.process_list_mirror
where item_id in ('thi_finan_ws_4', 'thi_finan_dtp_303');
```

## Operator notes

- **Governance:** Bulk mirror upserts were **not** applied via MCP in this session (aborted to avoid payload/timeouts and repo scratch noise). **Approved venue:** Supabase Dashboard → SQL Editor (or `psql` with a direct DB URL), after you review the generated files locally.
- Repo-root scratch artifacts (`_tmp_*`, `_mcp_*`, `_sqlexec_*`, etc.) were **removed**; `.gitignore` now ignores those patterns plus `.scratch/`.
- Legacy column `public.users.supakey` observed in prior inventory — **remediate separately** (do not store or echo values in docs).

## Dashboard / SQL editor — generate files (local, no repo commit)

From repo root, after `py scripts/validate_hlk.py` passes and you have recorded `git rev-parse HEAD`:

**PowerShell (writes to your Desktop — adjust paths if you prefer):**

```powershell
cd c:\Users\Shadow\cd_shadow\openclaw-akos
$out = [Environment]::GetFolderPath('Desktop')
py scripts/sync_compliance_mirrors_from_csv.py --no-begin-commit --baseline-only --output "$out\mirror_baseline.sql"
py scripts/sync_compliance_mirrors_from_csv.py --no-begin-commit --process-list-only --output "$out\mirror_process.sql"
py scripts/sync_compliance_mirrors_from_csv.py --no-begin-commit --finops-vendor-register-only --output "$out\mirror_finops.sql"
```

**Run order in the SQL editor:** open and execute **`mirror_baseline.sql`**, then **`mirror_process.sql`**, then **`mirror_finops.sql`**. Each file is idempotent upserts (`ON CONFLICT`); still review headers and row counts before Run.

**Post-run verification (SELECT only):**

```sql
select
  (select count(*) from compliance.process_list_mirror) as process_list_mirror_ct,
  (select count(*) from compliance.baseline_organisation_mirror) as baseline_org_mirror_ct,
  (select count(*) from compliance.finops_vendor_register_mirror) as finops_mirror_ct,
  (select max(source_git_sha) from compliance.process_list_mirror) as max_process_sha,
  (select max(synced_at) from compliance.process_list_mirror) as process_synced_max;
```

Expect **1083** / **65** / **1** row counts when CSVs match `validate_hlk.py`; `max_process_sha` should equal the repo `HEAD` used when you generated the files.
