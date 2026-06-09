---
language: en
Item Name: PMO operator inbox render
Item Number: SOP-PMO_OPERATOR_INBOX_RENDER_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Holistika
Area Owner: Operations — PMO
Process Owner: PMO
Version: 1.0
Revision Date: 2026-06-10
Status: active
Inherited Pattern: pattern_paired_sop_runbook
linked_runbooks:
  - scripts/render_operator_inbox.py
Acceptance Criteria Human: PMO can triage OPS_REGISTER rows and manually update OPERATOR_INBOX.md structure per SOP without the runbook.
Acceptance Criteria Automation: render_operator_inbox.py --check-only PASS; stable sha256 across runs.
---

## 1. Purpose

Render a single ranked operator surface at [`docs/wip/planning/OPERATOR_INBOX.md`](../../../../../../../wip/planning/OPERATOR_INBOX.md) from [`OPS_REGISTER.csv`](../../../People/Compliance/canonicals/OPS_REGISTER.csv) SSOT (D-IH-59-A).

## 2. Scope

In scope: `status=open` rows with `owner_class in (operator, mixed)`; RICE-descending sort.

Out of scope: minting new OPS rows (initiative-specific); closing initiatives (registry edits).

## 3. Inputs

- `OPS_REGISTER.csv`, `INITIATIVE_REGISTRY.csv`, `baseline_organisation.csv` for FK joins.

## 4. Procedure

1. Daily (or after OPS_REGISTER edits), run `py scripts/render_operator_inbox.py --check-only`.
2. On drift, run `py scripts/render_operator_inbox.py` to refresh.
3. Operator triages top rows; updates OPS status or owner_class in CSV SSOT.
4. Re-render and commit when CSV tranche merges.

## 5. Failure modes

| Symptom | Action |
|:---|:---|
| Unresolved initiative FK | Fix `originating_initiative_id` in OPS_REGISTER |
| Stale RICE ordering | Recompute rice_score in CSV; re-render |
| Empty inbox with open OPS rows | Check owner_class filter (operator/mixed only) |

## 6. Cross-references

- Runbook: [`scripts/render_operator_inbox.py`](../../../../../../../scripts/render_operator_inbox.py)
- Catalog: [`OPERATIONS_PROCESS_CATALOG.yaml`](../../canonicals/OPERATIONS_PROCESS_CATALOG.yaml)
