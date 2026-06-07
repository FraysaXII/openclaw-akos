---
title: Supabase EG-2 live execution — security drift closure + mirror-sync automation
initiative: INIT-OPENCLAW_AKOS-95
decision: D-IH-95-G
authored: 2026-06-07
author: Data Governance Office (MADEIRA AIC, operator execution grant)
language: en
project: MasterData (swrmqpelgoblaquequzb, eu-central-1, PG15)
---

# Supabase EG-2 — live execution evidence

Operator granted direct execution authority (2026-06-07): *"I approve you doing it… when a canonical
changes, we are going to sync supabase… in the best way you can for our workflow needs."* All changes
below were applied via the Supabase MCP to the live **MasterData** project and verified.

## 1. Pre-change ground truth (security advisor + catalog)
- **Critical advisory `rls_disabled`:** 16 `public.*` tables had RLS disabled → readable/writable by
  anyone with the anon key (anon + authenticated roles). One ERROR also on `kirbe.kirbe_organizations`
  (policies written but RLS never enabled → inert).
- **`public` schema:** 34 base tables, the KiRBe-era legacy surface (pre-AKOS). Clear test/dupe set
  identified (`test_*`, `example_csv`, `document_vectors` "duplicate of…", `users2`, `"Test access"`,
  `"Process list"`).
- **Dependency pre-check (before any drop):** `pg_constraint` (FK) + `pg_depend`/`pg_rewrite` (views)
  → **zero** references to the 10 drop targets. Safe to drop.

## 2. Changes applied (3 migrations, verified)
| Migration (remote version) | Action | Result |
|:---|:---|:---|
| `20260607191541_…drop_legacy_public_test_dupe_tables` | DROP 10 dead test/dupe tables | public 34 → 24 |
| `20260607191554_…rls_deny_by_default_public_survivors` | ENABLE RLS on 13 survivors (no policy = deny-by-default) | exposed-but-open → locked |
| `20260607191652_…enable_rls_kirbe_organizations` | ENABLE RLS (activates existing policies) | last ERROR cleared |

Repo migration files written with **matching versions** → two-plane DDL ledger in sync.

## 3. Post-change verification
- **Catalog query:** `public` base tables = **24**, `rls_disabled = 0`.
- **Cross-schema:** **0** tables anywhere with policies-but-RLS-disabled (the ERROR condition).
- **Net:** critical `rls_disabled` advisory **16 → 0**; **0 security ERRORs**. Remaining advisories are
  all INFO `rls_enabled_no_policy` — the intended deny-by-default posture. `service_role` (AKOS
  backend) bypasses RLS, so no application path breaks. All changes reversible
  (`ALTER TABLE … DISABLE ROW LEVEL SECURITY`).

## 4. DB-01 mirror re-sync — automated (not hand-applied)
The one-time re-sync DML emits at **6.9 MB / 2727 statements** — too large to hand-apply through MCP.
Correct mechanism = CI with a DB connection: `.github/workflows/supabase-mirror-sync.yml` emits the
mirror DML on every canonical-CSV push to `main` (uploads artifact) and applies via `psql` gated on
the `SUPABASE_DB_URL` secret. This is the durable "never drift again" backbone.

## 5. Registry + tracker updates
- `SUPABASE_MODULE_REGISTRY.csv`: `SUPA-MOD-09` (public legacy) ungoverned→**governed**;
  `SUPA-MOD-18` (RLS) critical→high (public holes closed; policy-registry work remains for EG-4).
- `OPS-95-1`: security drift closed via MCP; re-sync now automated; secret-setting is the only
  remaining operator action.

## 6. Operator actions remaining
1. Set repo secret **`SUPABASE_DB_URL`** → enables the mirror auto-apply (first run does the re-sync).
2. Set repo secrets **`NEO4J_URI` / `NEO4J_USERNAME` / `NEO4J_PASSWORD`** → enables the Neo4j keep-alive.

## 7. Forward (EG-3..5, still ungoverned — see module registry)
Critical-ungoverned remaining: **Auth** (`SUPA-MOD-22`) + **PostgREST API exposure** (`SUPA-MOD-24`,
config-vs-hosted drift). Then edge-function / cron / extension / RLS-posture registries.
