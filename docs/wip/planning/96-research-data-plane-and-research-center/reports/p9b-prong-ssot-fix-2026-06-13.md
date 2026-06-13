---
initiative_id: INIT-OPENCLAW_AKOS-96
report_kind: prong-ssot-fix
parent_phase: P9b-figma-hifi
authored: 2026-06-13
status: complete
audience: J-OP;J-AIC
unblocks: P9b Phase A (ledger/freshness truth); Track A R12 prong aggregates
linked_decisions:
  - D-IH-96-H
  - D-IH-96-J
  - D-IH-97-D
---

# P9b prong SSOT fix — baseline BL-* ledger rewrite (2026-06-13)

> **Outcome:** Automation OS and holistic-agentic source ledgers now store **baseline consumer prongs** (`BL-*`) only. The research-action validator rejects charter aliases (`P1-TECH`, `P7-AGENT-CLI`, …) in CSV cells so BFF aggregates and Research Center prong strips match git SSOT.

## Why we did this

P9b Phase A hard-depends on prong-fixed ledgers ([`p9b-revision-tranche-plan-2026-06-12.md`](p9b-revision-tranche-plan-2026-06-12.md) §Phase dependency). Gate C (**D-IH-96-H**) requires a prong-coverage strip on every POV lens fed by live aggregates — not charter shorthand buried in CSV.

**We did not defer this.** Without the rewrite, localhost ledger panels and Director completion cards lie about prong distribution.

## What changed

| Pack | Rows | Prong cells rewritten | Validator |
|:---|---:|---:|:---|
| Automation OS | 949 | 95 | `validate_research_action.py` PASS |
| Holistic-agentic | 305 | 305 | `validate_research_action.py` PASS |
| GOJ (prior tranche) | 60 | 29 (2026-06-12) | Already PASS |

### Alias mapping highlights

| Legacy charter id | Baseline consumer | Functional name |
|:---|:---|:---|
| `P1-TECH` … `P12-RPA-ADAPTERS` | Matching `BL-*` | Automation OS charter → lattice |
| `P7-AGENT-CLI` | `BL-ENVOY` | Agent CLI / monorepo OSINT block → Envoy/MADEIRA consumer |
| `P1-DATA` … `P8-MADEIRA` | Matching `BL-*` | Holistic-agentic charter → lattice |

Engine: `py scripts/research_ledger.py normalize-prongs --pack <slug>` (uses `akos/research_ledger_ops.normalize_ledger_prong_rows`).

## Verification

```powershell
py scripts/research_ledger.py validate --pack akos-automation-os-governance-2026-06-10
py scripts/research_ledger.py validate --pack holistic-agentic-capability-orchestration-2026-06-10
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/source-ledger.csv
py -m pytest tests/test_research_ledger_ops.py tests/test_validate_research_action.py -q
```

All PASS on 2026-06-13.

## What this unblocks

| Next step | Owner | Repo |
|:---|:---|:---|
| **P9b Phase A** — visual polish + broken fixes (A-B1..A-B5, IF-01..IF-10) | Execution seat | `hlk-erp` (sibling) |
| **P9b Phase B** — journey components (matrix already at GOJ pack) | Execution seat | `hlk-erp` |
| Track A R12 / D4 ratification | Operator + Research Director | AKOS WIP |

## What we still do not do (reasoning)

| Item | Decision | Reason |
|:---|:---|:---|
| **P9b Phase A in AKOS** | NO | UI lives in HLK-ERP sibling repo — not in this workspace |
| **Figma Phase C refresh** | NO until Phase A+B localhost evidence | Prevents Figma ↔ localhost drift repeat (R-P9b-01) |
| **DECISION_REGISTER D-IH-96-F/G/H CSV mint** | NO this tranche | Canonical CSV operator gate — markdown ratify only until approved |

## Cross-references

- Prong lattice SSOT: [`RESEARCH_PRONG_LATTICE_DISCIPLINE.md`](../../../../references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md)
- GOJ pack binding: [`source-ledger-prong-ssot-2026-06-12.md`](../../../intelligence/governed-operator-journey-ux-uat-2026-06-12/source-ledger-prong-ssot-2026-06-12.md)
- I97 closure (economics doctrine stable): [`uat-i97-closure-2026-06-13.md`](../../97-infonomics-holistika-data-economics/reports/uat-i97-closure-2026-06-13.md)
- P9b revision plan: [`p9b-revision-tranche-plan-2026-06-12.md`](p9b-revision-tranche-plan-2026-06-12.md)
