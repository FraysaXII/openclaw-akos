# I99 P1 — MCP / CLI inventory reconcile (2026-06-13)

**Initiative:** I99 Supabase Platform EG-5 Tranche (`INIT-OPENCLAW_AKOS-99`)  
**Probe method:** Supabase CLI against **linked** MasterData project (MCP server unavailable in agent session; CLI equivalent per holistika-ops doctrine)  
**Evidence artifacts:** `artifacts/i99-migration-list-2026-06-13-full.txt`, `artifacts/i99-extensions-2026-06-13.json`, `artifacts/i99-advisors-security-2026-06-13.json`

---

## Executive outcome

Git and hosted MasterData are **almost aligned** on schema (95/98 migration versions matched). **Two git migrations are pending prod apply** — including the **I96 auth/RPC fix** that unblocks Research Center role resolution. **One remote-only ledger row** (`20260611230847`) has no git file and needs reverse-import or repair before the next `db push`.

Hosted extensions match the I95 extension manifest (including **`vector` enabled** — updates KiRBe/AKOS boundary signal). Security Advisor ran successfully: **237 findings** (41 ERROR / 157 WARN / 39 INFO); **39 `rls_enabled_no_policy`** on compliance mirrors feed **EG-4**; **Auth remains the only critical-priority ungoverned module** (`SUPA-MOD-22`).

---

## 1. Migration ledger parity

| Metric | Count |
|:---|---:|
| Local + remote matched | **95** |
| Local-only (pending prod) | **2** |
| Remote-only (no git file) | **1** |

### Local-only — **operator SQL gate required**

| Version | Git file | Consumer | Why it matters |
|:---|:---|:---|:---|
| `20260612093000` | `20260612093000_i96_current_user_role_mapping_rpc.sql` | **I96** Research Center | Fixes `user_role_mapping` RLS recursion; adds `current_user_role_mapping()` RPC for hlk-erp auth path |
| `20260613120000` | `20260613120000_i97_p6b_infonomics_register_columns.sql` | I97 (closed) | Infonomics economic columns on compliance mirrors — P6b-CSV follow-through |

**Recommended operator sequence** (per [`operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)):

```powershell
npx supabase migration list --linked   # confirm matrix unchanged
npx supabase db push --linked          # apply 2 local-only migrations
npx scripts/verify.py compliance_mirror_emit   # if mirror DML needed after I97 cols
```

### Remote-only — **reconcile before next push**

| Version | Applied (UTC) | Git SSOT | Disposition |
|:---|:---|:---|:---|
| `20260611230847` | 2026-06-11 23:08:47 | **Missing** | **Scheduled** — reverse-import body from remote `schema_migrations` or `migration repair` with written mapping (same discipline as D-IH-OPS-2/3 in `supabase/migrations/README.md`) |

---

## 2. Extensions vs manifest

Hosted query: `select extname, extversion from pg_extension order by 1` (**36 extensions**).

| Manifest extension | Module ID | Hosted | Repo DDL | Reconcile note |
|:---|:---|:---|:---|:---|
| `pgmq` | SUPA-MOD-13 | ✓ 1.4.4 | `20260524000000_i81_p2_b2_finops_writer_substrate.sql` | Aligned |
| `pg_cron` | SUPA-MOD-14 | ✓ 1.6 | Cron schedule migrations only | Partial — still no standalone `CREATE EXTENSION` migration |
| `pg_net` | SUPA-MOD-15 | ✓ 0.14.0 | Implicit via cron SQL | Partial — aligned on hosted |
| `wrappers` | SUPA-MOD-16 | ✓ 0.5.3 | I18 privilege hardening | Partial — FDW DDL live-only |
| `vector` | SUPA-MOD-17 | ✓ **0.8.0** | Column comment only in git | **Drift:** hosted enabled; registry still `ungoverned` — I99 P4/P5 or I83 boundary tranche |

Other hosted extensions (informational): `postgis`, `timescaledb`, `pgsodium`, `supabase_vault`, `pgroonga`, etc. — not in module registry; no action unless adopted.

---

## 3. Security Advisor (`get_advisors` equivalent)

Command: `npx supabase db advisors --linked --type security --level info`

| Level | Count |
|:---|---:|
| ERROR | 41 |
| WARN | 157 |
| INFO | 39 |
| **Total** | **237** |

| Lint name | Count | I99 track |
|:---|---:|:---|
| `function_search_path_mutable` | 91 | EG-4 / RPC hygiene (partial) |
| `rls_enabled_no_policy` | 39 | **EG-4** — compliance mirror adapter tables |
| `authenticated_security_definer_function_executable` | 39 | Review post-I96 RPC apply |
| `security_definer_view` | 27 | Governance views — document in RLS posture |
| `anon_security_definer_function_executable` | 20 | **Closed class for pgmq** at I81; re-scan after I96 RPC |
| `rls_disabled_in_public` | 14 | EG-2 residual baseline |
| `auth_leaked_password_protection` | 1 | **EG-5 Auth** — Dashboard Auth hardening |

Advisor probe **PASS** — read-only lint available via CLI and MCP (operator enabled MCP Advisor per D-SUP-MCP-01).

---

## 4. Module registry cross-check

Validator: `py scripts/validate_supabase_module_registry.py` — **PASS** (27 modules).

| Status | Count | Notes |
|:---|---:|:---|
| governed | 15 | Mirrors, Edge, pgmq, cron, API exposure, CLI config |
| partial | 4 | FDW, RLS, RPCs, wrappers |
| ungoverned | 8 | **Auth, Storage, Realtime**, webhooks, secrets, kirbe, seed, vectors (registry row stale on vector) |

**Critical advisory:** `SUPA-MOD-22` (Auth) — only critical-priority ungoverned module. **I99 P2** first consumer wiring targets I96 redirect + `current_user_role_mapping` path (blocked until local-only migration applied).

### config.toml vs product modules (local dev)

| Module | config.toml | Registry | Gap |
|:---|:---|:---|:---|
| Auth | `[auth] enabled = true` | SUPA-MOD-22 ungoverned | No redirect allowlist registry for erp/research-center hosts |
| Realtime | `[realtime] enabled = true` | SUPA-MOD-21 ungoverned | No publication contract |
| Storage | `[storage] enabled = true` | SUPA-MOD-23 ungoverned | No bucket/path registry |

---

## 5. Edge + cron (unchanged; sanity pass)

| Registry | Validator | Rows |
|:---|:---|---:|
| `SUPABASE_EDGE_FUNCTION_REGISTRY.csv` | PASS | 3 |
| `SUPABASE_CRON_REGISTRY.csv` | PASS | 2 |

---

## 6. Disposition summary

| Finding | Posture | Owner phase |
|:---|:---|:---|
| Apply `20260612093000` + `20260613120000` | **satisfied** — operator repair + push 2026-06-13 | D-IH-99-C |
| Reverse-import `20260611230847` | **superseded** — reverted; duplicate of I96 RPC under dashboard timestamp | D-IH-99-C |
| Mint Auth registry (SUPA-MOD-22) | **scheduled** — EG-5 P2 | I99 P2 |
| Realtime publication contract | **scheduled** — EG-5 P3 | I99 P3 |
| Storage bucket registry | **scheduled** — EG-5 P4 | I99 P4 |
| EG-4 RLS posture (39 INFO lints) | **scheduled** — P6 paired | I99 P6 |
| Update SUPA-MOD-17 for hosted `vector` | **scheduled** — registry tranche P5 | I99 P5 |

---

## 7. Verification run (this session)

```powershell
npx supabase migration list --linked
npx supabase db query --linked --agent=no -o json "select extname, extversion from pg_extension order by 1;"
npx supabase db advisors --linked --type security --level info --agent=no -o json
py scripts/validate_supabase_module_registry.py
py scripts/validate_supabase_extension_manifest.py
py scripts/validate_supabase_edge_function_registry.py
py scripts/validate_supabase_cron_registry.py
```

---

## Cross-references

- Implementation spec: [`implementation-spec-2026-06-13.md`](implementation-spec-2026-06-13.md)
- Module SSOT: [`SUPABASE_MODULE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_MODULE_REGISTRY.csv)
- Operator SQL gate: [`operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)
- I96 auth migration: [`20260612093000_i96_current_user_role_mapping_rpc.sql`](../../../../supabase/migrations/20260612093000_i96_current_user_role_mapping_rpc.sql)
