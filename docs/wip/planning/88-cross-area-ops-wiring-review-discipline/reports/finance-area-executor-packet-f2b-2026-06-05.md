---
packet_id: FINANCE-F2B-2026-06-05
phase: F2b
seat: execution
tranche_class: canonical_csv_mint
operator_gates: [FINOPS_TAX_CALENDAR.csv]
prerequisites: [F2a optional — parallel OK per operator]
status: stub_ready
---

# F2b executor packet — tax calendar (stub)

> Full spec after F2a or in parallel thread. Research:
> [`research-f2b-tax-calendar-2026-06-05.md`](research-f2b-tax-calendar-2026-06-05.md).

## Mission

Mint `FINOPS_TAX_CALENDAR.csv` with Spain filing obligations (Modelo 036/037, 200, 202, 720, IVA, IRPF withholding). **Counsel-encoded** dates — operator must ratify row set before commit.

## Operator gate

⛔ **AskQuestion required:** confirm filing obligation row set with operator/counsel before CSV commit.

## Verification

`validate_finops_tax_calendar.py --self-test` + `validate_hlk.py` + matrix unchanged regression.
