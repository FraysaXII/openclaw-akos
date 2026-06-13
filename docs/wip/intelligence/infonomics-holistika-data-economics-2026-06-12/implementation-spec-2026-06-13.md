---
intellectual_kind: implementation_spec
parent_initiative: INIT-OPENCLAW_AKOS-97
authored: 2026-06-13
status: active
language: en
ratifying_decisions:
  - D-IH-97-C
  - D-IH-97-D
  - D-IH-97-E
gate: P5 closed — vault edits authorized at P6a/P6b only
---

# Implementation spec — Infonomics vault tranches (post-P5)

> **Plain language:** P5 locked *what* gets built and *in what order*. This spec is the P6 execution contract — no canonical touch until each tranche’s operator gates pass.

## Ratified sequence (D-IH-97-C compound A+D)

| Tranche | Purpose | Primary outputs | Operator gates |
|:---|:---|:---|:---|
| **P6a** | **DCAM level axis** in area completeness (Option D prerequisite) | Area bar maturity-level dimension; I93 matrix/validator alignment | I93 area-completeness coordination; CSV gate if new register rows |
| **P6b** | **Infonomics doctrine mint** (Option A) | `INFONOMICS_DISCIPLINE.md`, PRECEDENCE row, amend Data/FINOPS/RevOps economic columns | Canonical CSV gate; `validate_hlk.py` |
| **P6c** | Optional `process_list` row (D-IH-97-F) | Maintenance process if PMO approves | PMO + process_list gate |
| **P6d** | I94 economic-value component (D-IH-97-G) | Area bar extension or forward-charter | CDO ratify |

## I96 consumption contract (D-IH-97-D Option B)

| Consumer | Waits for | Consumes |
|:---|:---|:---|
| **I96 Track D** (Research Center insight/remediation economics) | I97 **P6b** doctrine stable | `INFONOMICS_DISCIPLINE.md` vocabulary + prong economic hooks — not duplicate Track D doctrine in intelligence pack |
| **I96 BFF / UI** | P6b + I96 P10-T2 unpause | Insight-card economics labels, remediation cost hints per governed-actionable-analytics surfaces |

Cross-ref: I96 **D-IH-96-J** in [`../../planning/96-research-data-plane-and-research-center/decision-log.md`](../../planning/96-research-data-plane-and-research-center/decision-log.md).

## P6a scope sketch (DCAM integrity)

1. Add **maturity level** axis to area completeness bar (2-D component × level per `SRC-INF-EXT-004`, `SRC-INF-EXT-001`).
2. Preserve deterministic heuristic (intersubjective verifiability — area-completeness Prong B).
3. Do **not** mint Infonomics doctrine in P6a — vocabulary only in area bar + planning notes.

## P6b scope sketch (doctrine mint)

1. Mint `docs/references/hlk/v3.0/Research/Methodology/canonicals/INFONOMICS_DISCIPLINE.md` (or Admin/O5-1 Data per PRECEDENCE placement at govern).
2. PRECEDENCE + CANONICAL_REGISTRY rows.
3. Amend (not replace): `DATA_CONTRACT_REGISTRY` economic columns, FINOPS registers, RevOps value-map surfaces per prong syntheses.
4. `implementation-spec` closes when `validate_hlk.py` + research-action ledger still PASS.

## Verification matrix (P6)

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/source-ledger.csv
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --matrix
py scripts/validate_carryover_posture.py --index docs/wip/planning/_trackers/carryover-posture-index.md --strict
```

## Cross-references

- P5 ratify: [`../../planning/97-infonomics-holistika-data-economics/reports/p5-govern-ratify-2026-06-13.md`](../../planning/97-infonomics-holistika-data-economics/reports/p5-govern-ratify-2026-06-13.md)
- Master synthesis: [`master-synthesis.md`](master-synthesis.md)
- Overlap tracker: [`../../planning/_trackers/i96-i97-infonomics-scope-overlap-tracker.md`](../../planning/_trackers/i96-i97-infonomics-scope-overlap-tracker.md)
