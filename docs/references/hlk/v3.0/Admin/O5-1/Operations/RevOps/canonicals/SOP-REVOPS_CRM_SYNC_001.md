---
language: en
status: review
canonical: true
role_owner: RevOps Manager
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-06-10
last_review: 2026-06-10
last_review_at: 2026-06-10
last_review_by: PMO
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.1
linked_runbooks:
  - scripts/revops_dispatch.py
companion_to:
  - REVOPS_AREA_CHARTER.md
  - dimensions/REVOPS_ADAPTER_REGISTRY.csv
---

# SOP-REVOPS_CRM_SYNC_001 — Daily CRM adapter sync

> I94 P7 T2 stub (operator ratified Option A 2026-06-10). Pairs `tbi_ops_dtp_revops_crm_sync_001`
> in `process_list.csv`. Interim automation: [`scripts/revops_dispatch.py`](../../../../../../../scripts/revops_dispatch.py).

## 1. Purpose

Run the daily RevOps CRM adapter sync so engagement and counterparty rows stay aligned with
the normalized adapter registry without manual spreadsheet drift.

## 2. Scope

In scope: dispatch via `revops_dispatch.py` for the CRM sync adapter row.
Out of scope: CRM vendor API credentials (Tech adapter registry maintenance).

## 3. Runbook

```powershell
py scripts/revops_dispatch.py
```

## 4. Acceptance criteria

- **AC-HUMAN:** RevOps Analyst runs §3 using this SOP only.
- **AC-AUTOMATION:** `revops_dispatch.py` exits 0; `validate_adapter_registries.py` PASS on CRM sync row.
