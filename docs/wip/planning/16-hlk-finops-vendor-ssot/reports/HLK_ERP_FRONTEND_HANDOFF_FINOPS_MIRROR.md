# Holistika ERP — FINOPS counterparty mirror (frontend / client guidance)

**Date:** 2026-04-23 (updated from 2026-04-20 vendor-only handoff)  
**Audience:** `hlk-erp` team (Next.js 14 App Router)  
**Schema owner:** openclaw-akos — `supabase/migrations/` + `scripts/sql/i18_phase1_staging/`

## Summary

Commercial counterparty **metadata** (vendors, customers, partners) is canonical in git [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../../references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv) and projected to Postgres as **`compliance.finops_counterparty_register_mirror`** (plus `source_git_sha`, `synced_at`). Initiative 18 **drops** the legacy **`finops_vendor_register_mirror`** table after a one-step data migration.

**Stripe bridge:** `holistika_ops.stripe_customer_link` may include **`finops_counterparty_id`** (CSV slug). **Stripe API** is authoritative for payments; **`stripe_gtm`** foreign tables (if present) are a **read-only FDW projection** — same server-only access pattern as mirrors.

## Forbidden

- **Do not** query `finops_counterparty_register_mirror` or **`stripe_gtm.*`** foreign tables from the **browser** using `NEXT_PUBLIC_SUPABASE_ANON_KEY` / `createClient` from `lib/supabase/client.ts`.
- **Do not** add permissive RLS policies for `anon` / `authenticated` on mirror or FDW relations without CFO + security review (foreign tables do not honor RLS).

## Required pattern

- Use a **server-only** Supabase client (service role or direct DB from trusted backend) in **Route Handlers**, **server actions**, or a **BFF** — same discipline as other internal mirrors.
- Expose **sanitized DTOs** to the client (fields you intend to show); avoid passing raw mirror rows to React state if classification is sensitive.
- After DDL apply in Supabase, regenerate **`lib/supabase-types.ts`** (or equivalent) so types match the new table and `stripe_customer_link` column.

## References

- [SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md](../../../../../references/hlk/v3.0/Admin/O5-1/Finance/Business%20Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md) §6  
- [sql-proposal-stack-20260417.md](../../../14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md) §7  
- **Initiative 18:** [`master-roadmap.md`](../../../18-hlk-finops-counterparty-stripe/master-roadmap.md)  
- **hlk-erp:** `documentation/supabase.md` and `documentation/architecture.md` (server vs public Supabase clients).
