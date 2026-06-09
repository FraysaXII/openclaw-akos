---
tranche_id: P95-GOV-1
tranche_class: canonical_csv_mint
ratifying_decisions:
  - D-IH-95-B
reversibility_class: medium
synthesis_complete: true
verdict: PASS
---

# Synthesis — P95-GOV-1 (canonical_csv_mint)

**Date:** 2026-06-09  
**Tranche:** Mint `CANONICAL_GOVERNANCE_REGISTRY.csv` + validator (registry-only scope guard)

## Fire set (canonical_csv_mint)

| Dimension | Status | Note |
|:---|:---:|:---|
| SYN-01 Audience completeness | PASS | J-OP internal governance inventory |
| SYN-04 Brand register | PASS | N/A — no external prose |
| SYN-05 Ratification lineage | PASS | D-IH-95-B cited per row |
| SYN-07 Tranche atomicity | PASS | Registry + validator only; no mirror/workflow refactor |
| SYN-08 Reversibility | PASS | medium — revert registry commit |
| SYN-09 Closing-loop test | PASS | `validate_canonical_governance_registry.py` + `validate_hlk.py` |
| SYN-02/03/10 | INFO | No dashboard surface in this tranche |

## Scope guard honored

No mirror-sync refactor, emit functions, migrations, PRECEDENCE edits, or workflow path changes (deferred P95-GOV-2..3).

## Inventory note

Charter §2 summary cites 74 vault CSVs; filesystem inventory at mint is **73** (41 People/Compliance + 32 sibling-area). Registry rows match filesystem 1:1.
