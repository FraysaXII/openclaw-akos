---
language: en
Item Name: Operations compliance mirror emit trigger
Item Number: SOP-OPS_MIRROR_EMIT_TRIGGER_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Holistika
Area Owner: Operations — PMO (trigger); Data — System Owner (apply)
Process Owner: PMO
Version: 1.0
Revision Date: 2026-06-10
Status: active
Inherited Pattern: pattern_dataops_discipline
linked_runbooks:
  - scripts/verify.py
  - scripts/sync_compliance_mirrors_from_csv.py
Acceptance Criteria Human: PMO can run emit + hand off SQL batches to operator without applying DML directly.
Acceptance Criteria Automation: py scripts/verify.py compliance_mirror_emit exits 0 after CSV tranche.
---

## 1. Purpose

Operations **triggers** compliance mirror SQL emit after canonical CSV tranches; **Data** owns linked Supabase apply per two-plane model ([`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc)).

## 2. Scope

In scope: emit profile `compliance_mirror_emit`; operator-gated apply via [`holistika-mirror-dml-apply.md`](../../../../../../../guides/holistika-mirror-dml-apply.md).

Out of scope: authoring canonical CSV rows (People/compliance gates); DDL migrations (supabase/migrations/).

## 3. Procedure

1. After operator-approved canonical CSV merge, run `py scripts/verify.py compliance_mirror_emit`.
2. Review emitted SQL under `artifacts/sql/` (row counts, no secrets).
3. Hand off to System Owner for `pwsh -File scripts/apply_mirror_batches.ps1` (operator SQL gate).
4. Record apply evidence under initiative `reports/operator-mirror-apply-*.md`.

## 4. Failure modes

| Symptom | Action |
|:---|:---|
| Emit FAIL | Run validate_hlk.py; fix CSV/schema drift |
| Apply drift | Canonical wins; resync mirror per PRECEDENCE |
| Large batch timeout | Use scoped emit flags per holistika-operations rule |

## 5. Cross-references

- Tech SOP: [`SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001.md`](../../../Tech/System Owner/canonicals/SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001.md)
- Catalog: [`OPERATIONS_PROCESS_CATALOG.yaml`](../../canonicals/OPERATIONS_PROCESS_CATALOG.yaml)
