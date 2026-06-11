---
report_type: tranche-regression
tranche: R8
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R8 regression — Finance + Legal audit bar

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R8 slice) | 28 | 28 (`SRC-AOS-R8I-*`) | PASS |
| OSINT (R8 slice) | 44 | 44 (`SRC-AOS-R8E-*`) | PASS |
| Cumulative ledger | 629 | 629 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-FIN (FINOPS discipline, counterparty/rev-rec/tax registries, mirror spine) + CORP-VAULT-LEGAL (trademark SOP, filed instruments) + OSINT-FINOPS-AUTO |
| 2 | Dual-source | PASS | 28 CORPINT + 44 OSINT |
| 3 | Voice diversity | PASS | ASC 606 / IFRS rev-rec (4.1), FinOps SaaS vendors (3.1), skeptic rev-rec theatre (2.1) |
| 4 | Prong binding | PASS | P7-FINOPS + P8-LEGAL; ICS in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 629-row cumulative ledger |
| 6 | Skeptic balance | PASS | 12/44 OSINT (27%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D4 adapter FK columns + R9 Marketing/CRM harvest |

## Dedup disposition

Manifest overflow candidates used where prior-tranche URL collisions would have left charter deficits; net-new URLs only in ledger append.

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `FINOPS_DISCIPLINE.md` | Finance ops governance bar |
| `SOP-TRADEMARK_NAMING_GOVERNANCE_001.md` | Legal naming clearance process |
| `validate_finops_ledger.py` | FINOPS register validator |
| `finance_mcp_server.py` | Finance research MCP chassis |

## Disposition

**PASS** — ready for phase commit.
