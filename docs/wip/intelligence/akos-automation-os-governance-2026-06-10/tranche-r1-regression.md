---
report_type: tranche-regression
tranche: R1
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-10
status: pass
---

# Tranche R1 regression — repo script census + anti-pattern audit

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R1 slice) | 55 | 55 (`SRC-AOS-R1I-*`) | PASS |
| OSINT (R1 slice) | 40 | 40 (`SRC-AOS-R1E-*`) | PASS |
| Cumulative ledger | 95 | 95 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-RUNTIME, CORP-INCIDENT (one-offs), CORP-CANON, OSINT-SCRIPT-GOV/CICD-OS |
| 2 | Dual-source | PASS | 55 CORPINT + 40 OSINT |
| 3 | Voice diversity | PASS | Vendor CI, OSS runners, practitioner skeptics |
| 4 | Prong binding | PASS | Tiered: manifest → `process_list` runbook_path → `prong-binding:unresolved` (registry debt visible in `notes`) |
| 5 | KiRBe schema | PASS | Validator PASS on 95-row ledger |
| 6 | Skeptic balance | PASS | 6/40 OSINT (15%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D6 engine (`research_ledger.py`); R2 vault Tech harvest |

## Engine wedge

- `akos/research_ledger_ops.py` — append/dedup chassis
- `scripts/research_ledger.py` — bootstrap from `tranches/r1-manifest.json`
- Replaces per-tranche one-off pattern starting this tranche

## Disposition

**PASS** — ready for operator AskQuestion → commit.
