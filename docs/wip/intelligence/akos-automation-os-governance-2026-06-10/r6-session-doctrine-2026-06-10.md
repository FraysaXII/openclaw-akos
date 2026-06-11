---
authored: 2026-06-11
tranche: akos-automation-os-R6-research-intelops-radar
register_id: IO-CAP-AKOS-AUTOMATION-OS-2026-001
status: committed
---

# AKOS Automation OS — R6 session doctrine (2026-06-11)

## Deliverables

| # | Artifact | Validator |
|:---|:---|:---|
| D2 | `source-ledger.csv` cumulative **483 rows** (+32 CORPINT +44 OSINT) | `research_ledger.py validate` **PASS** |
| D2b | `tranche-r6-regression.md` — §7.1 **PASS** | operator-facing |
| D0 | `tranches/r6-manifest.json` — Research/IntelOps/radar harvest | idempotent via `research_ledger.py bootstrap` |
| D0 | This session doctrine | operator-facing closure |

## R6 scope delivered

- **32 CORPINT** — Methodology mint (prong lattice, HxPESTAL, pillars, synthesis/radar/action SOPs), Intelligence canonicals (elicitation, counterparty baseline, reliability grading, GOI/POI), radar chassis (`hlk_research_radar.py`, `research_ledger_ops.py`), cursor rules + craft skills, WIP templates + research-radar charter
- **44 OSINT** — Research pipeline DX (notebooks, citation graphs, open-access indexes) + academic method bar (PRISMA, GRADE, Cochrane) + OSINT tradecraft + skeptic voices (AI lit-review hype, predatory journals, vendor intel platforms)

## Cumulative progress (950-row target)

| Slice | CORPINT | OSINT | Total |
|:---|---:|---:|---:|
| R1 | 55 | 40 | 95 |
| R2 | 34 | 44 | 78 |
| R3 | 35 | 44 | 79 |
| R4 | 35 | 44 | 79 |
| R5 | 32 | 44 | 76 |
| R6 | 32 | 44 | 76 |
| **Cumulative** | **223** | **260** | **483** |
| Remaining | 177 | 290 | 467 |

## Recursive SSOT look-back

R6 mint is WIP ledger only — no Tier-A CSV edits.

| Registry | R6 action | Result |
|:---|:---|:---|
| PRECEDENCE | Harvest-only; Research/Intel surfaces pre-rowed (I86/I94 waves) | N/A |
| CANONICAL_REGISTRY | Methodology mint rows closed 2026-06-10/11; harvest confirms paths | No gap |
| CANONICAL_RELATIONSHIP_REGISTRY | No new HCAM pattern this tranche | N/A |
| INTELLIGENCEOPS_REGISTER | Charter appendix §A row drafted; operator CSV gate still required | **Deferred** — AskQuestion before append |
| process_list / CAPABILITY | Radar/research runbooks pair existing `hol_resea_*` / `hol_peopl_dtp_research_action_001` rows | **Deferred** — TECH_AUTOMATION_REGISTRY mint at D4/D5 |
| GOI_POI_REGISTER | Harvest-only (register inventoried; no row expansion) | N/A |

**AskQuestion gate (forward):** INTELLIGENCEOPS row `IO-CAP-AKOS-AUTOMATION-OS-2026-001` remains draft in charter appendix §A — do not append to CSV without explicit operator ratification.

## Next

**R7** — Vault Compliance + PRECEDENCE + process_list (+30 CORPINT, +44 OSINT per charter §7)
