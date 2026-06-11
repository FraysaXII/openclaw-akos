---
report_type: tranche-regression
tranche: R3
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R3 regression — Data + RPA / integration plane harvest

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R3 slice) | 35 | 35 (`SRC-AOS-R3I-*`) | PASS |
| OSINT (R3 slice) | 44 | 44 (`SRC-AOS-R3E-*`) | PASS |
| Cumulative ledger | 252 | 252 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-DATA + CORP-VAULT-ADAPTERS + OSINT-RPA + OSINT-DATA-LINEAGE |
| 2 | Dual-source | PASS | 35 CORPINT + 44 OSINT |
| 3 | Voice diversity | PASS | RPA vendors, low-code platforms, lineage/catalog vendors, DAMA, skeptic |
| 4 | Prong binding | PASS | P2-DATA + P12-RPA-ADAPTERS; ICS in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 252-row cumulative ledger |
| 6 | Skeptic balance | PASS | 10/44 OSINT (23%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D5 adapter column spec + R4 Ops/RevOps harvest |

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `DATAOPS_DISCIPLINE.md` | Data operations doctrine (R1; not re-harvested) |
| `RPA_ADAPTER_REGISTRY.csv` | Normalized RPA adapter inventory |
| `DATA_CONTRACT_REGISTRY.csv` | Engagement data-contract SSOT |
| `SOP-OPS_MIRROR_EMIT_TRIGGER_001.md` | Compliance mirror emit operator path |
| `sync_compliance_mirrors_from_csv.py` | Mirror DML automation runbook |

## Disposition

**PASS** — ready for phase commit.
