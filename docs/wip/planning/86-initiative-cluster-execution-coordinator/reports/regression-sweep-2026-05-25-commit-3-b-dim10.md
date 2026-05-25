# Regression sweep — Wave-R close — 2026-05-25

**Report ID:** `regression-sweep-2026-05-25`  
**Swept by:** agent:inter_wave_regression_sweep  
**Wave closing:** Wave-R  

## Counts

| Verdict | Count |
| --- | --- |
| clean | 1 |
| drift | 0 |
| gap | 0 |
| blocked | 0 |
| skip | 0 |
| **TOTAL** | **1** |

## Findings

| Dimension | Surface | Verdict | Severity | Proposed action | Notes |
| --- | --- | --- | --- | --- | --- |
| DIM-10-DEPLOY-EVIDENCE-COMPLETENESS | `planning/files-modified-scan` | clean | low |  | 45 sibling-repo rows across all CSVs; every initiative folder whose own files-modified.csv carried sibling-repo rows has UAT with deploy/READY/HTTP-200 evidence |

---

Per `akos-inter-wave-regression.mdc` RULE 3: every non-clean finding
MUST become one `AskQuestion` option set at P4 (inline-ratify gate).
