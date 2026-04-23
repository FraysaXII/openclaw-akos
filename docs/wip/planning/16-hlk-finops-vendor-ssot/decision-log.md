# Decision log — Initiative 16 (FINOPS vendor SSOT)

**Status:** Execution tranche 2026-04-20

## D-16-1 — Canonical FINOPS register and mirror name

**Decision:** `FINOPS_VENDOR_REGISTER.csv` is the git SSOT under `docs/references/hlk/compliance/`. Supabase mirror table **`compliance.finops_vendor_register_mirror`** with `source_git_sha` and `synced_at`.

## D-16-2 — Process list anchor

**Decision:** Workstream **`thi_finan_ws_4`** (FINOPS and vendor economics) under `thi_finan_prj_1`; child processes **`thi_finan_dtp_303`–`307`** per execution report.

## D-16-3 — Supabase access

**Decision:** **Server-only** mirror access: RLS **deny** for `anon` and `authenticated`; **`service_role`** (or trusted DB connection) for sync and application servers. No browser `anon` queries to the mirror.

## D-16-4 — Phase C monetary data

**Decision:** Production **amounts** and ledger-style facts live **only** in Postgres under a future **`finops`** schema (separate migrations). **Never** in git CSV or `compliance` mirror. Gate: **`thi_finan_dtp_306`** + CFO/Legal alignment before any Phase C DDL.

## D-16-5 — Phase C DDL deferral

**Decision:** This tranche **does not** create `finops` schema or monetary tables. Rollback and forward DDL for Phase C will be a **separate operator-approved** migration after D-16-4 gate is recorded.

## D-16-6 — MAROPS / TECHOPS vs Postgres schemas

**Decision:** **MAROPS** and **TECHOPS** are **stewardship / process planes** (Growth, marketing ops, technical operations in SOPs and matrices)—**not** required first-class Postgres schemas for DAMA alignment in this workspace. Git-canonical compliance data is mirrored under **`compliance.*_mirror`**; operational facts live in approved app schemas (e.g. **`holistika_ops`**). Introducing dedicated `marops` or `techops` **schemas** would be a **new** architecture change (update `PRECEDENCE.md`, sql-proposal stack, and this log)—not an implied gap from prose mentions alone.

## D-16-7 — Supabase migration SSOT + mirror emit façade

**Decision:** FINOPS mirror **DDL** is versioned in **[`supabase/migrations/`](../../../../supabase/migrations/)** (file `20260420202847_i16_finops_vendor_register_mirror.sql`, parity with staging). **Upserts** use repo profile **`compliance_mirror_emit`** (`py scripts/verify.py compliance_mirror_emit`), not ad-hoc script READMEs. Cross-ref Initiative 14 **D-GTM-DB-**\* (including **D-GTM-DB-5** migration ledger parity) and [`docs/ARCHITECTURE.md`](../../../ARCHITECTURE.md) § Supabase schema and compliance mirror governance.
