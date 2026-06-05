---
packet_id: FINANCE-F2B-2026-06-05
phase: F2b
seat: execution
model_pin: composer-2.5
tranche_class: canonical_csv_mint
operator_gates:
  - FINOPS_TAX_CALENDAR.csv
prerequisites:
  - feat(i88-finance-f2a) committed
  - reports/research-f2b-tax-calendar-2026-06-05.md
  - reports/finance-area-f2b-tranche-charter.md
status: executed_2026-06-05
---

# F2b executor packet — tax calendar

> **Prerequisite:** F2a complete (`0ed091c`). Research:
> [`research-f2b-tax-calendar-2026-06-05.md`](research-f2b-tax-calendar-2026-06-05.md).

## Mission

Mint `FINOPS_TAX_CALENDAR.csv` with Spain filing obligations (Modelo 036/037, 200, 202, 720, IVA, IRPF withholding, 130). **Counsel-encoded cadence rules** — entity-specific due dates backfilled at incorporation.

## Files (ordered)

| # | Action | Path |
|:---:|:---|:---|
| 1 | CREATE | `Finance/Governance/canonicals/dimensions/FINOPS_TAX_CALENDAR.csv` |
| 2 | CREATE | `akos/hlk_finops_tax_calendar_csv.py` + `scripts/validate_finops_tax_calendar.py` + tests |
| 3 | EDIT | `CANONICAL_REGISTRY.csv` — `finops_tax_calendar` row |
| 4 | EDIT | `FINOPS_DISCIPLINE.md` — plane 3 pointer |
| 5 | EDIT | `validate_hlk.py` — wire tax validator |

## Verification

```powershell
py scripts/synthesis_before_tranche_check.py --check-charter reports/finance-area-f2b-tranche-charter.md
py scripts/validate_finops_tax_calendar.py --self-test
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --matrix
```

## Commit

`feat(i88-finance-f2b): FINOPS tax calendar + validator (OPS-81-13)`
