---
title: Supabase PostgREST API Exposure
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Architect
co_authors:
  - Data Governance Office
  - System Owner
last_review: 2026-06-09
last_review_by: Data Architect
last_review_at: 2026-06-09
last_review_decision_id: D-IH-95-G
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-95-G
status: active
register: internal
linked_canonicals:
  - SUPABASE_ECOSYSTEM_GOVERNANCE.md
  - dimensions/SUPABASE_MODULE_REGISTRY.csv
  - ../Governance/canonicals/DATA_GOVERNANCE_POLICY.md
companion_to:
  - SUPABASE_ECOSYSTEM_GOVERNANCE.md
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
---

# Supabase PostgREST API Exposure (SUPA-MOD-24)

> **SSOT for which Postgres schemas are exposed through PostgREST** — both on the hosted
> MasterData project and in the local `supabase/config.toml` dev stack. Closes the
> config-vs-hosted drift called out in `SUPABASE_MODULE_REGISTRY.csv` (SUPA-MOD-24).

## 1. Why this exists

PostgREST exposes every table, view, and RPC in the configured schema list to clients using
the anon or authenticated API keys. A schema listed in `[api].schemas` without RLS policies
is readable and writable by anyone holding the anon key. Before I95 Round-2 EG-2, the hosted
Dashboard exposed `holistika_ops` and `finops` while `supabase/config.toml` listed only
`public` — operators could not trust local dev to mirror production API surface.

This canonical is the **authoritative exposure matrix**. DDL and RLS remain in migrations;
this doc governs **which schemas may appear in PostgREST** and the **SOC posture** per schema.

## 2. Exposure matrix (authoritative)

| Schema | Hosted (MasterData) | Local `config.toml` | RLS posture | API intent |
|:---|:---|:---|:---|:---|
| `public` | Exposed | Exposed | EG-2 deny-by-default on 13 survivors (2026-06-07); 24 legacy KiRBe-era tables reference-only | Legacy survivors; **no new tables** |
| `graphql_public` | Exposed (Supabase default) | Exposed (default) | Supabase-managed | GraphQL entry |
| `holistika_ops` | Exposed | **Reconciled 2026-06-09** | RLS deny `anon`/`authenticated`; `service_role` for AKOS + Edge | Company-plane ops (lead intake, billing link) |
| `finops` | Exposed | **Reconciled 2026-06-09** | RLS deny `anon`/`authenticated`; `service_role` + gated writers | Operational monetary facts (not CSV SSOT) |
| `compliance` | **Not exposed** | Not listed | Mirror tables deny-by-default; sync via `service_role` | CSV SSOT mirrors — backend-only |
| `kirbe` | **Not exposed** | Not listed | App-owned (32 tables); AKOS retention helper only | Reference-only legacy (SUPA-MOD-07) |
| `erp` / `governance` | **Not exposed** | Not listed | Views for ERP demo; backend/service_role | Internal analytics |
| `stripe_gtm` (FDW) | **Not exposed** | Not listed | Foreign tables — linter 0017 risk if exposed | Read projection only |
| `auth` / `storage` / `realtime` | Supabase-managed | Supabase-managed | Platform modules (SUPA-MOD-22/21/23) | Separate posture docs (EG-3..5) |

**Reconcile rule:** `supabase/config.toml` `[api].schemas` MUST match the **Hosted** column for
every Holistika-governed schema marked Exposed. Drift is a release-gate finding (see §5).

## 3. Config artifact (`supabase/config.toml`)

```toml
[api]
enabled = true
schemas = ["public", "graphql_public", "holistika_ops", "finops"]
extra_search_path = ["public", "extensions"]
max_rows = 1000
```

Prior drift (pre-2026-06-09): `schemas = ["public", "graphql_public"]` only — local stack did
not surface `holistika_ops` or `finops` endpoints that production already served.

**Dashboard-only settings:** Hosted project API settings live in the Supabase Dashboard
(Data API → Exposed schemas). Git `config.toml` is the **local dev SSOT**; quarterly MCP
reconcile (`list_tables` + API settings export) must confirm hosted ⊆ this matrix.

## 4. SOC posture (binding)

1. **Never expose FDW schemas** (`stripe_gtm`) via PostgREST — foreign tables bypass RLS
   ([Supabase linter 0017](https://supabase.com/docs/guides/database/database-linter?lint=0017_foreign_table_in_api)).
2. **Never add `compliance` to exposed schemas** without operator ratification + per-table RLS
   design — mirrors are CSV projections, not client-facing APIs.
3. **Exposed schema + no policy = deny-by-default** (EG-2 invariant). `service_role` bypasses
   RLS for AKOS sync jobs and Edge Functions.
4. **No secret values in git** — API keys and `SUPABASE_DB_URL` stay in `~/.openclaw/.env` or
   CI secrets only.

## 5. Verification

| Check | Command / probe |
|:---|:---|
| Registry row governed | `py scripts/validate_supabase_module_registry.py` — SUPA-MOD-24 `governed` |
| Config matches matrix | Manual: `config.toml` `[api].schemas` ⊆ §2 Exposed rows |
| RLS on exposed survivors | `py scripts/validate_hlk.py` + Supabase security advisors after DDL |
| Hosted reconcile (quarterly) | MCP read-only: compare Dashboard exposed schemas vs §2 table |

## 6. Cross-references

- Parent doctrine: [`SUPABASE_ECOSYSTEM_GOVERNANCE.md`](SUPABASE_ECOSYSTEM_GOVERNANCE.md) §3 EG-2
- Module inventory: [`dimensions/SUPABASE_MODULE_REGISTRY.csv`](dimensions/SUPABASE_MODULE_REGISTRY.csv) SUPA-MOD-24
- EG-2 live execution: [`docs/wip/planning/95-canonical-articulation-model/reports/supabase-eg2-execution-2026-06-07.md`](../../../../../../../../wip/planning/95-canonical-articulation-model/reports/supabase-eg2-execution-2026-06-07.md)
- Holistika two-plane ops: `.cursor/rules/akos-holistika-operations.mdc` § SOC and PostgREST exposure
- Initiative: I95 Round-2 L1 EG-2 (operator ratified A, 2026-06-09)
