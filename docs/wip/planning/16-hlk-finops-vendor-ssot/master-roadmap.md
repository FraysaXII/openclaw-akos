# Initiative 16 — FINOPS vendor SSOT + Supabase mirror

> **Superseded for FINOPS commercial metadata:** [**Initiative 18** — FINOPS counterparty SSOT + Stripe FDW](../18-hlk-finops-counterparty-stripe/master-roadmap.md) replaces the vendor-only CSV and `finops_vendor_register_mirror` with **`FINOPS_COUNTERPARTY_REGISTER.csv`** and **`finops_counterparty_register_mirror`**. This folder remains historical traceability for the 2026-04-20 vendor tranche.

**Folder:** `docs/wip/planning/16-hlk-finops-vendor-ssot/`  
**Status:** Executed (2026-04-20); vendor artifacts subsumed by Initiative 18 (2026-04-23)

## Outcome

Canonical **`FINOPS_VENDOR_REGISTER.csv`**, **`compliance.finops_vendor_register_mirror`** staging DDL (`scripts/sql/i16_phase3_staging/`), **`validate_finops_vendor_register.py`** + `validate_hlk.py` integration, **`sync_compliance_mirrors_from_csv.py --finops-vendor-register-only`**, Finance **SOP**, **`process_list.csv`** tranche (`thi_finan_ws_4`, `thi_finan_dtp_303`–`307`), **PRECEDENCE** + **sql-proposal-stack** §7, **hlk-erp handoff** report.

## Phases

1. **Done:** CSV + akos fieldnames + validator + process tranche + vault SOP + WIP traceability.  
2. **Operator:** Apply DDL on staging/production per `operator-sql-gate.md`; run FINOPS upsert SQL after each CSV merge.  
3. **Phase C (gated):** Native **`finops`** schema for monetary facts—**no** DDL until Legal/CFO sign-off (`thi_finan_dtp_306`).

## Links

- [decision-log.md](decision-log.md)  
- [evidence-matrix.md](evidence-matrix.md)  
- [reports/execution-tranche-20260420.md](reports/execution-tranche-20260420.md)  
- [reports/HLK_ERP_FRONTEND_HANDOFF_FINOPS_MIRROR.md](reports/HLK_ERP_FRONTEND_HANDOFF_FINOPS_MIRROR.md)
