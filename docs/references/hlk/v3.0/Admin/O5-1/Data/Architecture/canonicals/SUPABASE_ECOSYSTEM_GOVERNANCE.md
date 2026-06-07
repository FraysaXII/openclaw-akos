---
title: Supabase Ecosystem Governance
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Architect
co_authors:
  - CDO
  - Data Governance Office
  - System Owner
last_review: 2026-06-07
last_review_by: Data Architect
last_review_at: 2026-06-07
last_review_decision_id: D-IH-95-G
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-95-G
status: active
register: internal
linked_canonicals:
  - DATA_ARCHITECTURE.md
  - DATA_INTEGRATION_PLANE.md
  - dimensions/SUPABASE_MODULE_REGISTRY.csv
  - ../Governance/canonicals/DATA_GOVERNANCE_POLICY.md
  - ../Governance/canonicals/dimensions/RPA_ADAPTER_REGISTRY.csv
companion_to:
  - DATA_ARCHITECTURE.md
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
---

# Supabase Ecosystem Governance

> **The Data Architect governs the *whole* Supabase ecosystem, not just tables.** Operator mandate
> (2026-06-06, `D-IH-95-G` / DB-02): *"tables are not everything in supabase; we have places,
> functions, and more; look at every module Supabase has in store and ensure everything is governed
> from our side so that every time we use the modules we don't delude ourselves to only managing
> tables when we have an ecosystem to hold here."* This canonical closes the gap between the
> three-tier data architecture (which governs T2 tables/mirrors + one FINOPS pipeline well) and the
> **full Supabase product surface**.

## 1. Why this exists (the drift fear, named)

The operator cannot work on the O5-1 areas while fearing **drift in every layer**. A 2026-06-06
live assessment (Supabase MCP) found: mirrors lapsed vs CSV SSOT (decision_register 468/522,
process 1187/1207, ops 139/150); **16 `public.*` tables RLS-disabled** (anon read/write); ~30
untracked legacy `public.*`/`kirbe.*` tables; and **Auth, Storage, Realtime, Edge-function registry,
extensions, cron, FDW, RLS-as-a-system, and PostgREST exposure live-only or doctrine-only.** The
three-tier doctrine *names* nine modules but governs mostly tables. This canonical makes the **whole
ecosystem governable from the repo**.

## 2. SSOT — the module registry

`dimensions/SUPABASE_MODULE_REGISTRY.csv` is the **single inventory** of every Supabase-governable
surface, each row carrying `governed_status` (governed / partial / ungoverned / forward),
`owner_role`, `priority`, and the named `gap`. Validated by
`scripts/validate_supabase_module_registry.py` (wired into `validate_hlk.py`); it prints a governance
scorecard + flags **critical-priority ungoverned** modules.

**Baseline (2026-06-07): 27 modules — 9 governed · 7 partial · 11 ungoverned.** Critical-ungoverned:
`public` legacy schema (SUPA-MOD-09), Auth (SUPA-MOD-22), PostgREST API exposure (SUPA-MOD-24).

## 3. The closure plan (phased — Data Architect owns)

| Phase | Mint | Closes |
|:---|:---|:---|
| **EG-1 (now)** | this canonical + `SUPABASE_MODULE_REGISTRY` + validator | the inventory + the scorecard |
| **EG-2 (critical)** | `public`/`kirbe` legacy drop (DB-02) + RLS-on-survivors (DB-03) + `SUPABASE_API_EXPOSURE.md` | SUPA-MOD-09/22/24 (the critical-ungoverned) |
| **EG-3** | `SUPABASE_EDGE_FUNCTION_REGISTRY.csv` + `SUPABASE_CRON_REGISTRY.csv` + `SUPABASE_EXTENSION_MANIFEST` | SUPA-MOD-11/14/15/19 |
| **EG-4** | `SUPABASE_RLS_POSTURE.md` + validator (fail RLS-enabled-without-policy) | SUPA-MOD-18 |
| **EG-5** | FDW inventory runbook (`stripe_gtm` reconcile) + Realtime/Storage/Vault posture | SUPA-MOD-08/16/21/23 |

Gated surfaces (Auth/Storage/RLS DDL, legacy drop) need operator approval (SOC + data-loss risk).

## 4. Drift-prevention (so it never happens again)

1. **CI gate:** `validate_supabase_module_registry.py` in `validate_hlk.py` (every commit) — a
   ungoverned/partial module must carry a named `gap` + owner; new live modules without a registry
   row are caught at the next reconcile.
2. **Mirror re-sync cadence:** `OPS-95-1` — automate the emit on every canonical-CSV commit (CI);
   apply stays operator-gated (creds). Closes the T2-behind-T1 staleness.
3. **Inventory-before-greenfield:** before adding any Supabase surface, run the live MCP assessment
   (`list_tables` / `list_migrations` / `get_advisors`) and reconcile against this registry — never
   create a live-only module. Periodic (quarterly) MCP reconcile filed against the registry.
4. **RLS invariant:** no table ships RLS-enabled-without-policy (EG-4 validator) and no `public.*`
   table is anon-writable (DB-03).

## 5. Ownership

Data Architect owns the registry + this doctrine; Data Governance Office owns RLS/API-exposure
posture; System Owner + DevOPS execute DDL/migrations/cron/extensions; AI Engineer owns Edge
Functions + the graph/vector surfaces. Federated, but the **registry is the one place** that says
who owns what and whether it's governed.

## 6. Cross-references
- Three-tier architecture: `DATA_ARCHITECTURE.md` (§9 Supabase capability module table — the seed this registry operationalizes)
- Integration plane: `DATA_INTEGRATION_PLANE.md` · adapters: `RPA_ADAPTER_REGISTRY.csv`
- Mirror re-sync: `OPS-95-1`; guide `docs/guides/holistika-mirror-dml-apply.md`
- Assessment: `docs/wip/intelligence/canonical-articulation-model-2026-06-05/round2-research-synthesis-2026-06-06.md` §3
- Decision: `D-IH-95-G`
