---
report_type: tranche-regression
tranche: R6
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R6 regression — Research + IntelligenceOps + radar harvest

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R6 slice) | 32 | 32 (`SRC-AOS-R6I-*`) | PASS |
| OSINT (R6 slice) | 44 | 44 (`SRC-AOS-R6E-*`) | PASS |
| Cumulative ledger | 483 | 483 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-RESEARCH (methodology mint, pillars, prong lattice, HxPESTAL) + CORP-VAULT-INTEL (elicitation, counterparty baseline, GOI/POI) + radar SOP/discipline |
| 2 | Dual-source | PASS | 32 CORPINT + 44 OSINT |
| 3 | Voice diversity | PASS | Research DX vendors (2.1–4.1), academic method bar (4.1), OSINT tradecraft (3.1–4.1), skeptic postmortems (2.1) |
| 4 | Prong binding | PASS | P4-RESEARCH + P10-INTEL-OPS; ICS in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 483-row cumulative ledger |
| 6 | Skeptic balance | PASS | 12/44 OSINT (27%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D3 prong synthesis (Research/IntelOps) + D6 `research_ledger.py` contract + R7 compliance harvest |

## Dedup disposition

No URL collisions skipped — all 76 manifest candidates were net-new against the 407-row cumulative ledger.

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `RESEARCH_PRONG_LATTICE_DISCIPLINE.md` | Prong binding for ledger ingest |
| `HXPESTAL_INTENT_TRACKING_DISCIPLINE.md` | Intent fidelity before govern |
| `RESEARCH_RADAR_DISCIPLINE.md` | Freshness/staleness register discipline |
| `SOP-IO_ELICITATION_DISCIPLINE_001.md` | Structured discovery (internal register) |
| `GOI_POI_REGISTER.csv` | Counterparty stance dimension |
| `hlk_research_radar.py` / `research_ledger_ops.py` | Radar + ledger engine chassis |

## Disposition

**PASS** — ready for phase commit.
