---
report_type: tranche-regression
tranche: R7
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R7 regression — Compliance + PRECEDENCE + process_list

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R7 slice) | 30 | 30 (`SRC-AOS-R7I-*`) | PASS |
| OSINT (R7 slice) | 44 | 44 (`SRC-AOS-R7E-*`) | PASS |
| Cumulative ledger | 557 | 557 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-COMPLIANCE (PRECEDENCE, process_list, baseline_organisation, access/confidence levels, source taxonomy, INITIATIVE/DECISION registers) + OSINT-REG-AUDIT |
| 2 | Dual-source | PASS | 30 CORPINT + 44 OSINT |
| 3 | Voice diversity | PASS | DAMA/ISO registry bar (4.1), vendor MDM patterns (3.1), skeptic registry-sprawl (2.1) |
| 4 | Prong binding | PASS | P6-COMPLIANCE; ICS Load-bearing in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 557-row cumulative ledger |
| 6 | Skeptic balance | PASS | 11/44 OSINT (25%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D4 TECH_AUTOMATION_REGISTRY scope + D6 `research_ledger.py` + R8 Finance/Legal harvest |

## Dedup disposition

Manifest overflow candidates used where prior-tranche URL collisions would have left charter deficits; net-new URLs only in ledger append against 483-row baseline.

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `PRECEDENCE.md` | Canonical/mirror precedence doctrine |
| `process_list.csv` | Executable process catalog SSOT |
| `baseline_organisation.csv` | Role owner dimension for automation registry |
| `SOP-META_PROCESS_MGMT_001.md` | CSV-before-SOP mint order |
| `validate_hlk.py` | Umbrella compliance validator |

## Disposition

**PASS** — ready for phase commit.
