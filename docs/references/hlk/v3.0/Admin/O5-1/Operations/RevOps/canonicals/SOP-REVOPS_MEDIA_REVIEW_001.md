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

# SOP-REVOPS_MEDIA_REVIEW_001 — Event-triggered media counterparty review

> I94 P7 T2 stub (operator ratified Option A 2026-06-10). Pairs
> `tbi_ops_dtp_revops_media_review_001`. Event-triggered Research IO handoff.

## 1. Purpose

When a media or counterparty event fires (press inquiry, analyst note, partnership signal),
RevOps dispatches the media-review adapter and routes IntelligenceOps refresh to Research.

## 2. Scope

In scope: event-triggered `revops_dispatch.py` run + IO register pointer.
Out of scope: media brief authoring (Research / Marketing).

## 3. Runbook

```powershell
py scripts/revops_dispatch.py
```

## 4. Acceptance criteria

- **AC-HUMAN:** RevOps Analyst documents event source + dispatch outcome in engagement notes.
- **AC-AUTOMATION:** `revops_dispatch.py` exits 0 for media-review adapter row.
