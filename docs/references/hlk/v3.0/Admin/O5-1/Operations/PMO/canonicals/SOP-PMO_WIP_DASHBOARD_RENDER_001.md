---
language: en
Item Name: PMO WIP dashboard render
Item Number: SOP-PMO_WIP_DASHBOARD_RENDER_001
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
  - scripts/render_wip_dashboard.py
Acceptance Criteria Human: PMO refreshes WIP_DASHBOARD.md when --check-only reports drift without invoking automation.
Acceptance Criteria Automation: render_wip_dashboard.py --check-only PASS in CI smoke profile.
---

## 1. Purpose

Keep [`docs/wip/planning/WIP_DASHBOARD.md`](../../../../../../../wip/planning/WIP_DASHBOARD.md) in parity with every initiative `master-roadmap.md` frontmatter so the operator sees accurate program status without manual table maintenance.

## 2. Scope

In scope: all `docs/wip/planning/<NN>-*/master-roadmap.md` folders; status taxonomy sections per InitiativeStatus SSOT.

Out of scope: editing initiative roadmaps (source SSOT); canonical CSV promotion (see vault promotion gate SOP).

## 3. Inputs

- Initiative master-roadmap frontmatter (`status`, `last_review`, program anchors).
- [`OPERATIONS_PROCESS_CATALOG.yaml`](../../canonicals/OPERATIONS_PROCESS_CATALOG.yaml) entry `pmo_wip_dashboard_render`.

## 4. Procedure

1. After any initiative status or phase change, run `py scripts/render_wip_dashboard.py --check-only`.
2. On exit 1 (drift), run `py scripts/render_wip_dashboard.py` without flags to refresh the auto block.
3. Review section placement (Closed / Active / Gated / Unknown).
4. Commit `WIP_DASHBOARD.md` in the same phase commit when roadmap edits landed.

## 5. Failure modes

| Symptom | Action |
|:---|:---|
| Unknown section overflow | Audit initiative frontmatter `status:` against taxonomy; fix in master-roadmap |
| Missing initiative folder | Add planning README row or archive folder per planning traceability |
| Repeated drift on unchanged roadmaps | Check marker corruption in WIP_DASHBOARD auto block |

## 6. Cross-references

- Runbook: [`scripts/render_wip_dashboard.py`](../../../../../../../scripts/render_wip_dashboard.py)
- Catalog: [`OPERATIONS_PROCESS_CATALOG.yaml`](../../canonicals/OPERATIONS_PROCESS_CATALOG.yaml)
- Doctrine: [`OPERATIONS_DELIVERY_DOCTRINE.md`](../../OPERATIONS_DELIVERY_DOCTRINE.md) §4 automation-first
