---
title: Supabase Extension Manifest
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
last_review: 2026-06-10
last_review_by: Data Architect
last_review_at: 2026-06-10
last_review_decision_id: D-IH-95-G
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-95-G
status: active
register: internal
linked_canonicals:
  - SUPABASE_ECOSYSTEM_GOVERNANCE.md
  - dimensions/SUPABASE_MODULE_REGISTRY.csv
  - dimensions/SUPABASE_CRON_REGISTRY.csv
companion_to:
  - SUPABASE_ECOSYSTEM_GOVERNANCE.md
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
---

# Supabase Extension Manifest (SUPA-MOD-14/15 + related)

> **SSOT for Postgres extensions used by the AKOS MasterData project.** Closes the
> doctrine-only / live-only gap for `pg_cron`, `pg_net`, and related surfaces named in
> `SUPABASE_MODULE_REGISTRY.csv`. DDL for extensions remains in migrations; this manifest
> governs **inventory, owner, and forward debt**.

## 1. Why this exists

Before I95 EG-3, extensions were tracked only as module-registry rows with gaps like
*"CREATE EXTENSION absent"* (pg_cron) or *"no extension declaration"* (pg_net). Cron jobs
in I81 migrations invoke Edge Functions via `net.http_post` without a repo-level extension
inventory operators could reconcile against hosted `list_extensions`.

## 2. Extension matrix (authoritative)

| Extension | Module ID | Repo DDL | Hosted expectation | Used by | Owner | Status | Gap / forward debt |
|:---|:---|:---|:---|:---|:---|:---|:---|
| `pgmq` | SUPA-MOD-13 | `20260524000000_i81_p2_b2_finops_writer_substrate.sql` | Enabled | FINOPS writer queue + DLQ | System Owner | **governed** | Queue names not in separate CSV (acceptable) |
| `pg_cron` | SUPA-MOD-14 | Cron schedule migrations only | Enabled (Supabase managed) | 2 jobs in [`SUPABASE_CRON_REGISTRY.csv`](dimensions/SUPABASE_CRON_REGISTRY.csv) | System Owner | **partial** | No `CREATE EXTENSION` migration in repo; reconcile via MCP quarterly |
| `pg_net` | SUPA-MOD-15 | Implicit via cron SQL (`net.http_post`) | Enabled | Cron → Edge Function HTTP | System Owner | **partial** | No standalone declaration migration; no DB Webhook defs |
| `wrappers` | SUPA-MOD-16 | I18 privilege hardening only | Enabled | `stripe_gtm` FDW | Data Architect | **partial** | FDW DDL live-only — EG-5 reconcile |
| `vector` | SUPA-MOD-17 | Column comment only | May be enabled on hosted | KiRBe embeddings (forward) | AI Engineer | **forward** | I46 PoC; no AKOS embedding tables |

**Reconcile rule:** Before enabling a new extension on hosted MasterData, append a row here
and the matching `SUPABASE_MODULE_REGISTRY.csv` module row in the **same commit**.

## 3. Cron ↔ extension coupling

Both scheduled jobs in [`SUPABASE_CRON_REGISTRY.csv`](dimensions/SUPABASE_CRON_REGISTRY.csv)
depend on **`pg_cron`** (scheduler) + **`pg_net`** (HTTP invoke). Disabling either extension
breaks FINOPS writer cadence and ECB FX cache refresh.

## 4. SOC posture (binding)

1. **Never commit secret values** — cron migrations currently embed the project anon JWT
   (pre-EG-3 debt). Forward fix: migration replacing headers with `vault`-backed or
   `current_setting` pattern; tracked in cron registry `gap` column.
2. **Extension enablement is operator-gated** when it expands attack surface (new HTTP egress,
   new FDW server).
3. **Inventory-before-greenfield:** MCP `list_extensions` + reconcile against §2 before
   `CREATE EXTENSION` in a new migration.

## 5. Verification

| Check | Command / probe |
|:---|:---|
| Cron registry ↔ edge registry | `py scripts/validate_supabase_cron_registry.py` |
| Extension manifest present | `py scripts/validate_supabase_extension_manifest.py` |
| Module rows updated | `py scripts/validate_supabase_module_registry.py` — SUPA-MOD-14/15 |
| Hosted reconcile (quarterly) | MCP read-only: `list_extensions` vs §2 matrix |

## 6. Cross-references

- Parent doctrine: [`SUPABASE_ECOSYSTEM_GOVERNANCE.md`](SUPABASE_ECOSYSTEM_GOVERNANCE.md) §3 EG-3
- Edge inventory: [`dimensions/SUPABASE_EDGE_FUNCTION_REGISTRY.csv`](dimensions/SUPABASE_EDGE_FUNCTION_REGISTRY.csv)
- Cron inventory: [`dimensions/SUPABASE_CRON_REGISTRY.csv`](dimensions/SUPABASE_CRON_REGISTRY.csv)
- Module scorecard: [`dimensions/SUPABASE_MODULE_REGISTRY.csv`](dimensions/SUPABASE_MODULE_REGISTRY.csv)
- I81 live deploy: [`supabase/migrations/README.md`](../../../../../../../supabase/migrations/README.md)
