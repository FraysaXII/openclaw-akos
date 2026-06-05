---
evidence_id: FINANCE-F2B-EVIDENCE-2026-06-05
phase: F2b
program: FINANCE-AREA-FULL
authored: 2026-06-05
verdict: PASS
---

# F2b execution evidence — Spain tax filing calendar

## Verification matrix

| Gate | Result |
|:---|:---|
| `synthesis_before_tranche_check.py` (F2b charter) | PASS |
| `validate_finops_tax_calendar.py --self-test` | PASS |
| `validate_finops_tax_calendar.py` | PASS (8 obligations; 7 WARN empty `next_due_at` until entity live) |
| `validate_hlk.py` | OVERALL PASS |
| `validate_area_completeness.py --matrix` | Finance **88%** (no regression) |
| `pytest tests/test_finops_tax_calendar.py` | 2/2 PASS |

## Minted artefacts

- `Finance/Governance/canonicals/dimensions/FINOPS_TAX_CALENDAR.csv` (8 rows per OPS-81-13)
- `akos/hlk_finops_tax_calendar_csv.py` + `scripts/validate_finops_tax_calendar.py`
- `CANONICAL_REGISTRY` row `finops_tax_calendar`

## Posture

- **Cadence rules** cite AEAT public references; **no production amounts** in git.
- **`next_due_at`** left empty on active rows until incorporation / fiscal year known — AT-Pymes Layer A executes per **D-IH-81-P**.
- **OPS-81-14** (foral doctrine) and **OPS-81-16** (ENISA / Q-CRT-001) remain forward-chartered.
