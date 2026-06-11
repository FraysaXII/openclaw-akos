---
report_type: tranche-regression
tranche: R10
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R10 regression — Verify profiles + CI/CD automation OS

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R10 slice) | 25 | 25 (`SRC-AOS-R10I-*`) | PASS |
| OSINT (R10 slice) | 46 | 46 (`SRC-AOS-R10E-*`) | PASS |
| Cumulative ledger | 772 | 772 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-RUNTIME/TECH (`verification-profiles.json`, `verify.py`, release-gate, SOP-CICD_BASELINE) + OSINT-CICD-OS depth |
| 2 | Dual-source | PASS | 25 CORPINT + 46 OSINT |
| 3 | Voice diversity | PASS | DORA metrics (4.1), GitHub Actions patterns (3.1), skeptic quality-gate fatigue (2.1) |
| 4 | Prong binding | PASS | P1-TECH + P2-VERIFY; ICS Load-bearing in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 772-row cumulative ledger |
| 6 | Skeptic balance | PASS | 13/46 OSINT (28%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D5/D8 verify-profile wiring spec + R11 agent CLI harvest |

## Dedup disposition

Manifest overflow candidates used where prior-tranche URL collisions would have left charter deficits; net-new URLs only in ledger append.

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `config/verification-profiles.json` | CI profile SSOT |
| `scripts/verify.py` | Operator golden-path runner |
| `SOP-CICD_BASELINE_001.md` | Fleet CICD baseline SOP |
| `validate_cicd_baseline.py` | CICD posture validator |

## Disposition

**PASS** — ready for phase commit.
