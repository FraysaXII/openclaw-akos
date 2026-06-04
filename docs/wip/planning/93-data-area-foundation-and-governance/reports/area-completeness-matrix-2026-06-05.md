---
intellectual_kind: verification_report
initiative: I93
phase: P8
authored: 2026-06-05
sweep_id: area-completeness-2026-06-05
---

# Area completeness matrix — I93 P8 harmonization sweep

**Command:** `py scripts/validate_area_completeness.py --matrix`  
**Date:** 2026-06-05  
**Doctrine:** `AREA_GOVERNANCE_DISCIPLINE.md` (14-component bar)

## Summary scores

| Area | pass | partial | gap | skip | blocked | score |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Data** | 10 | 3 | **0** | 1 | 0 | **88%** |
| People | 9 | 2 | 2 | 1 | 0 | 77% |
| Marketing | 8 | 3 | 2 | 1 | 0 | 73% |
| Operations | 7 | 3 | 3 | 1 | 0 | 65% |
| Finance | 5 | 3 | 5 | 1 | 0 | 50% |
| Research | 6 | 4 | 3 | 1 | 0 | 62% |
| Tech | 6 | 4 | 3 | 1 | 0 | 62% |

## Interpretation (I93 exit criteria §15)

| Criterion | Result |
|:---|:---|
| DATA at/above 14-component bar | **Met** — zero `gap`; partials are CONF pairing + paired SOP coverage + cursor skill (expected at federated scale) |
| All other areas scored | **Met** — this report |
| Gap trackers filed | **Met** — [`_trackers/area-governance-gap-tracker-2026-06-05.csv`](../_trackers/area-governance-gap-tracker-2026-06-05.csv) |
| `pattern_area_buildout` propagation | **Met** — breakthrough digests 2026-06 (see propagation record) |

## DATA partials (acceptable at closure)

| Component | Status | Note |
|:---|:---|:---|
| AREA-06-CAPABILITY-CONFIDENCE | partial | 17 CAP rows; CONF registry pairing is forward tranche |
| AREA-09-PAIRED-SOP-RUNBOOK | partial | 0/17 processes have runbook column populated — forward per area |
| AREA-11-CURSOR-RULE-SKILL | partial | `akos-area-governance.mdc` present; skill exists at repo level |

## Cross-area recurring gaps (tracker disposition)

High-severity `gap` clusters repeat across Finance, People, Research, Tech, Marketing, Operations:

- **AREA-02** — no `*_AREA_CHARTER.md` in area tree (except Data)
- **AREA-13** — missing area `README.md` index (except Data)
- **AREA-03** — discipline/governance canonicals thin or absent
- **AREA-11** — no area-local cursor rule + skill pair (Data partial only)

These are **forward-charter** work for each area's role-owner, not I93 Composer scope.
