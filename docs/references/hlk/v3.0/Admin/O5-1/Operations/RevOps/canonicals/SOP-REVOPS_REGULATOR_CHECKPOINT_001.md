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
  - ../../../Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
---

# SOP-REVOPS_REGULATOR_CHECKPOINT_001 — Quarterly regulator-relationship checkpoint

> I94 P7 T2 stub (operator ratified Option A 2026-06-10). Pairs
> `tbi_ops_dtp_revops_regulator_checkpoint_001`. Fires Research IO handoff per
> [`OPERATIONS_CROSS_AREA_HANDOFFS.md`](../../canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md).

## 1. Purpose

Quarterly checkpoint that RevOps orchestrates before regulator-facing engagements move —
surfacing stale `INTELLIGENCEOPS_REGISTER` rows and routing refresh to Research.

## 2. Scope

In scope: quarterly dispatch + Research radar sweep trigger.
Out of scope: regulator dossier authoring (Research area).

## 3. Runbook

```powershell
py scripts/revops_dispatch.py
py scripts/research_radar_sweep.py
```

## 4. Acceptance criteria

- **AC-HUMAN:** RevOps Manager runs §3 and records checkpoint note in operator inbox.
- **AC-AUTOMATION:** `validate_intelligenceops_register.py` PASS; radar sweep surfaces due rows.
