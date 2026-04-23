# Initiative 16 — FINOPS vendor register mirror (staging SQL)

**Status:** Staging pack for operator-approved `apply_migration` / `execute_sql` against Supabase.

| File | Purpose |
|------|---------|
| [`20260420_i16_finops_vendor_mirror_up.sql`](20260420_i16_finops_vendor_mirror_up.sql) | `compliance.finops_vendor_register_mirror` + RLS deny `anon`/`authenticated` + `service_role` grant |
| [`20260420_i16_finops_vendor_mirror_rollback.sql`](20260420_i16_finops_vendor_mirror_rollback.sql) | Drop mirror table and policies |

**Upsert generator (historical):** use Initiative 18 **`--finops-counterparty-register-only`** against [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv); vendor-only mode was removed.

**Governance:** Same project as Initiative 14 mirrors. **Superseded (2026-04-23):** FINOPS CSV SSOT is now [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv) (Initiative 18); this folder remains for historical **`finops_vendor_register_mirror`** DDL reference only.
