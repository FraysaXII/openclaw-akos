---
language: en
Item Name: Operations area completeness sweep
Item Number: SOP-OPS_AREA_COMPLETENESS_SWEEP_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Holistika
Area Owner: Operations
Process Owner: COO
Version: 1.0
Revision Date: 2026-06-10
Status: active
Inherited Pattern: pattern_area_buildout
linked_runbooks:
  - scripts/validate_area_completeness.py
Acceptance Criteria Human: COO or PMO walks --next worklist and dispositions gaps via inline-ratify before tranche commit.
Acceptance Criteria Automation: validate_area_completeness.py --self-test + --area Operations --matrix PASS.
---

## 1. Purpose

Run the 16-component area-completeness matrix for **Operations** at tranche boundaries; target crit@L3 tier COMPLETE (10/10).

## 2. Scope

In scope: `--area Operations --next` and `--matrix`; conservative AREA-10 skip.

Out of scope: other areas (use People meta-process SOP); process_list column pairing (forward tranche).

## 3. Procedure

1. Before Operations tranche commit: `py scripts/validate_area_completeness.py --area Operations --next`.
2. Work critical components to L3 first (AREA-03 closed at P1; AREA-09 enhancing).
3. Run `--matrix` for evidence row in phase report.
4. Disposition partial/gap findings per AREA_GOVERNANCE_DISCIPLINE §5–§6.

## 4. Failure modes

| Symptom | Action |
|:---|:---|
| AREA-09 0/N paired | Expected until process_list sop_path/runbook_path tranche; catalog SSOT holds pairs |
| crit@L3 INCOMPLETE | Address blocking critical component from --next |
| False AREA-10 PASS | Re-run with conservative skip posture |

## 5. Cross-references

- Meta-process: [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](../../../People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md)
- Runbook: [`scripts/validate_area_completeness.py`](../../../../../../../scripts/validate_area_completeness.py)
- Catalog: [`OPERATIONS_PROCESS_CATALOG.yaml`](../../canonicals/OPERATIONS_PROCESS_CATALOG.yaml)
