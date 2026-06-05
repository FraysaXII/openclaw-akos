---
research_kind: phase_research_packet
phase: F2b
authored: 2026-06-05
---

# F2b research — Spain tax calendar + counsel overlay

## Internal

- OPS-81-13 CRITICAL — `FINOPS_TAX_CALENDAR.csv` not minted
- OPS-81-14/16 — adviser-answer encoding still open
- `Finance/Business Controller/Taxes/` — empty (.gitkeep only)
- Entity gate `thi_finan_dtp_306` — no production amounts until entity ready

## External

- AEAT 2026 filing cadence (counsel-encoded rows; AIC does not invent deadlines)
- D-IH-81-P internal-first — tax doctrine = counsel + operator ratification

## F2b mint

1. `Finance/Governance/canonicals/dimensions/FINOPS_TAX_CALENDAR.csv`
2. `akos/hlk_finops_tax_calendar_csv.py` + `validate_finops_tax_calendar.py`
3. Optional `FINOPS_TAX_STRATEGY_DOCTRINE.md` stub at **charter** (full OPS-81-20 deferred)

## Out

- Rev-rec / pricing (F2a)
- Board reporting SOP (OPS-81-20 item v)
