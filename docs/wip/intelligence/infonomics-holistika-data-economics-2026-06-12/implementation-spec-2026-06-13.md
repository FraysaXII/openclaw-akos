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

## P6a scope sketch (DCAM integrity) — **closed 2026-06-13**

1. ~~Add **maturity level** axis~~ — **already live** via I94 `D-IH-94-A` L0–L5 grid.
2. Crosswalk + matrix evidence: [`dcam-area-completeness-crosswalk-2026-06-13.md`](dcam-area-completeness-crosswalk-2026-06-13.md).
3. Closure: [`../../planning/97-infonomics-holistika-data-economics/reports/p6a-dcam-integrity-2026-06-13.md`](../../planning/97-infonomics-holistika-data-economics/reports/p6a-dcam-integrity-2026-06-13.md).

## P6b scope sketch (doctrine mint) — **closed 2026-06-13**

1. Mint [`INFONOMICS_DISCIPLINE.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/INFONOMICS_DISCIPLINE.md) ✅
2. PRECEDENCE + CANONICAL_REGISTRY rows ✅
3. Register economic hook **schema declared** in doctrine §4; physical CSV column append operator-gated (see p6b report)
4. Closure: [`../../planning/97-infonomics-holistika-data-economics/reports/p6b-doctrine-mint-2026-06-13.md`](../../planning/97-infonomics-holistika-data-economics/reports/p6b-doctrine-mint-2026-06-13.md)

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
