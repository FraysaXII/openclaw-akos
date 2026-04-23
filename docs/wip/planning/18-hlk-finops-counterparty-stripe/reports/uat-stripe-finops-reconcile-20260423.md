# UAT — Stripe × FINOPS × FDW reconcile (2026-04-23)

## Purpose

Three-way reconciliation for Initiative 18 close: **Stripe API** ↔ **`holistika_ops.stripe_customer_link`** ↔ **`stripe_gtm`** FDW (if present). No card data; redact PII in samples.

## Preconditions

- Migration **`i18_finops_counterparty`** applied; mirror **`compliance.finops_counterparty_register_mirror`** populated from CSV sync.
- Optional: seed at least one **`holistika_ops.stripe_customer_link`** row with **`finops_counterparty_id`** matching a **`customer`** row in the register (test org label only).

## MCP evidence (2026-04-23 session)

| Check | Result |
|-------|--------|
| Supabase `list_migrations` | `20260418165339`, `20260418183239`, `20260418193915`, `20260420202847` — **i18 not yet on remote** |
| Supabase `list_extensions` | **`wrappers`** installed (`0.5.3`) |
| `pg_foreign_server` | **`stripe_gtm_server`** present |
| `compliance.finops_vendor_register_mirror` | **1** row (pre-cutover) |
| `holistika_ops.stripe_customer_link` | **0** rows |
| `compliance.process_list_mirror` | **1083** rows (behind git until next sync) |
| Stripe `get_stripe_account_info` | Account **Holistika** (`acct_1O6DaPAKBWx1b32d`) |
| Stripe `list_customers` / `list_subscriptions` | **`[]`** (empty account or restricted MCP) |
| FDW `count(*)` on `stripe_gtm.stripe_gtm_customers` | **Error:** Wrappers vault SPI (`HV000`) — treat as **N/A** until operator-run SQL with service context; use Dashboard or `service_role` path |

**`get_advisors` (security):** Large pre-existing lint set (Kirbe/public RLS, `foreign_table_in_api` on `public.O51`, etc.). **No Initiative 18–specific regression attributed** until i18 DDL is applied; re-run after `db push` for net-new issues.

## Matrix A — Counts

| Source | Check | Result | Notes |
|--------|-------|--------|-------|
| Stripe MCP | `list_customers` (limit) | **N/A** | Returned `[]` (2026-04-23) |
| Stripe MCP | `list_subscriptions` (limit) | **N/A** | Returned `[]` |
| Supabase | `select count(*) from holistika_ops.stripe_customer_link` | **PASS** | **0** (matches empty bridge) |
| Supabase | `select count(*) from stripe_gtm.stripe_gtm_customers` | **N/A** | Vault/SPI error via MCP SQL path |

## Matrix B — `hlk_billing_plane` (routing intent)

Validate on real Stripe objects (MCP or Dashboard) that metadata aligns with [`supabase/functions/stripe-webhook-handler/`](../../../../../supabase/functions/stripe-webhook-handler/) routing: Holistika company plane → `holistika_ops.*`; KiRBe SaaS → `kirbe.*`.

| Object id | `hlk_billing_plane` (expected) | Target schema | PASS/FAIL |
|-----------|--------------------------------|---------------|-----------|
| *(fill on UAT)* | | | |

## Advisors

After DDL changes attributable to Initiative 18, run **`get_advisors` (security + performance)** and file links to any **new** lints introduced.

## Evidence notes

- This document may be completed incrementally as MCP access and staging data become available.
- **PASS with N/A** is acceptable when the environment has no customers yet, with reason documented in Matrix A.
