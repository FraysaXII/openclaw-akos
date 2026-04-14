# Canonical CSV bulk tranche — operator approval template (C0)

**Initiative:** `02-hlk-on-akos-madeira`  
**Phase plan:** [phase-canonical-csv-tranche-plan.md](../phase-canonical-csv-tranche-plan.md)  
**Gate:** D-CSV-1 — **No** merge to `baseline_organisation.csv` or `process_list.csv` without this artifact completed and referenced in the commit message or linked plan.

---

## Approval block (fill before C1)

| Field | Value |
|:------|:------|
| **Approval ID** | `CSV-TRANCHE-YYYY-MM-DD-###` |
| **Operator / role** | |
| **Date (UTC)** | |
| **Scope** | Rows to add/update/delete (summary only; attach diff outside repo if large) |
| **Source of truth** | Confirm edits originate from canonical governance process (not mirror-only) |
| **validate_hlk** | I will run / have run `py scripts/validate_hlk.py` after apply |
| **USER_GUIDE / ARCHITECTURE** | I will sync HLK Operator Model counts if role/process totals change |

**Sign-off:** (name) — I approve applying this tranche to canonical CSVs under `docs/references/hlk/compliance/`.

---

## C1 status (2026-04-14)

**No batch applied in this change set.** Awaiting a completed approval ID and diff per D-CSV-1. When approved, apply rows, run `validate_hlk.py`, update `docs/USER_GUIDE.md` and `docs/ARCHITECTURE.md` counts, and reference **Approval ID** in the commit message.
