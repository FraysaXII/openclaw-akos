---
language: en
status: review
canonical: true
role_owner: RevOps Manager
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-T
methodology_version_at_review: v3.0
companion_to:
  - REVOPS_AREA_CHARTER.md
  - REVOPS_PROCESS_CATALOG.yaml
  - dimensions/REVOPS_ADAPTER_REGISTRY.csv
---

# SOP-MADEIRA_REVOPS_HANDOFF_001 — RevOps process catalog → MADEIRA workflow execution

> Authored I72 P9 per `D-IH-72-T` + `D-IH-72-O`. Codifies how the **madeira_revops_handoff** adapter routes RevOps process catalog entries to MADEIRA workflow execution (when MADEIRA is the implementation surface). Cadence: on_demand (via `revops_dispatch.py`).

## 1. Purpose

Bridge RevOps catalog YAML to MADEIRA workflow runtime so AICs (per D-IH-72-S) can invoke catalog processes through the MADEIRA agent surface.

## 2. Scope

In scope: any REVOPS_PROCESS_CATALOG.yaml entry where `runbook_pointer` references a MADEIRA workflow. Out of scope: MADEIRA workflow authoring (handled by MADEIRA stack).

## 3. Steps

### 3.1 Catalog lookup

`revops_dispatch.py` resolves the catalog entry by `--process <id>`.

### 3.2 MADEIRA dispatch

When `runbook_pointer` references a MADEIRA workflow, dispatch via the MADEIRA invocation surface (TODO[I72-followup-madeira-runbook] specifies the actual call shape).

### 3.3 Result capture

Capture MADEIRA workflow output + log to PMO_HUB_LOG with catalog entry id + invocation timestamp.

## 4. Acceptance criteria

- **AC-HUMAN**: RevOps Manager invokes via `py scripts/revops_dispatch.py --process <id>` for relevant catalog entries.
- **AC-AUTOMATION**: `validate_adapter_registries.py` PASS on madeira_revops_handoff row + revops_dispatch.py exits 0.

## 5. Cross-references

- Adapter row: REVOPS_ADAPTER_REGISTRY.csv (madeira_revops_handoff).
- Catalog: REVOPS_PROCESS_CATALOG.yaml.
- Dispatcher: scripts/revops_dispatch.py.
- Decisions: D-IH-72-T, D-IH-72-O, D-IH-72-N (process catalog architecture), D-IH-72-S (AIC role_owner pattern).
