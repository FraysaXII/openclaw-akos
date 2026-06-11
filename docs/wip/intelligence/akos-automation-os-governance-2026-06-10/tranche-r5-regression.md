---
report_type: tranche-regression
tranche: R5
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R5 regression — People + Quality Fabric + regression harvest

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R5 slice) | 32 | 32 (`SRC-AOS-R5I-*`) | PASS |
| OSINT (R5 slice) | 44 | 44 (`SRC-AOS-R5E-*`) | PASS |
| Cumulative ledger | 407 | 407 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-PEOPLE + QF specialty lattice + regression runbooks/rules + OSINT-EVAL + OSINT-SKEP |
| 2 | Dual-source | PASS | 32 CORPINT + 44 OSINT |
| 3 | Voice diversity | PASS | QA/UAT industry (2.1–4.1), LLM-eval vendors (3.1), skeptic postmortems (2.1) |
| 4 | Prong binding | PASS | P5-PEOPLE primary + P6-COMPLIANCE crossover; ICS in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 407-row cumulative ledger |
| 6 | Skeptic balance | PASS | 14/44 OSINT (32%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D3 prong synthesis (People/QF) + R6 Research/IntelOps harvest |

## Dedup disposition

| Skipped URL | Prior tranche | Replacement |
|:---|:---|:---|
| `https://principlesofchaos.org/` | R2 (`SRC-AOS-R2E-040`) | Gremlin chaos-engineering tutorial (`SRC-AOS-R5E-044`) |

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `HOLISTIKA_QUALITY_FABRIC.md` | Five-axis Quality Fabric meta-doctrine |
| `UAT_DISCIPLINE.md` | Closure UAT taxonomy + deploy-class bar |
| `SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` | Pre-commit scope review |
| `INTENT_RANKED_REGRESSION_DISCIPLINE.md` | Value-weighted regression ordering |
| `validate_uat_report.py` / `intent_ranked_regression.py` | Paired automation runbooks |

## Disposition

**PASS** — ready for phase commit.
