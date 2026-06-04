---
title: SOP — People Area Governance — Addendum (auditor depth)
language: en
intellectual_kind: people-canonical-sop-addendum
sop_id: SOP-PEOPLE_AREA_GOVERNANCE_001
access_level: 5
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - CPO
  - System Owner
last_review: 2026-06-04
last_review_by: CPO
last_review_decision_id: D-IH-93-B
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-B
status: charter
register: internal
parent_sop: SOP-PEOPLE_AREA_GOVERNANCE_001.md
companion_to:
  - SOP-PEOPLE_AREA_GOVERNANCE_001.md
  - AREA_GOVERNANCE_DISCIPLINE.md
ssot: true
---

# SOP — People Area Governance — Addendum

> Access level 5. Auditor + System Owner depth for the 14-component bar,
> heuristic limits, and harmonization sequencing (P0 meta-process vs P1
> DATA worked example vs P8 cross-area propagation).

## A. Heuristic limits (what the runbook does not prove)

- **AREA-10** defaults to `skip` — mirror parity needs Supabase MCP/SQL
  evidence, not repo-only scans.
- **AREA-11** uses filename heuristics for cursor rules/skills; a area
  can pass with partial coverage while doctrine is still charter-only.
- **Marketing** maps to `MKT` in `process_list.csv` — auditors should
  verify the column mapping when interpreting AREA-04/14 rows.

## B. Harmonization sequencing

| Phase | Area focus | Expected matrix posture |
|:---|:---|:---|
| I93 P0 | Meta-process only | People row strongest; Data gaps expected |
| I93 P1 | DATA charter + folders | Data score should rise on AREA-02/03/13 |
| I93 P8 | All areas | Target: no `gap` on baseline components 1–9, 13–14 |

## C. Promotion to FAIL

Do not promote `validate_area_completeness.py --strict` to pre_commit
until P8 operator sign-off per AREA_GOVERNANCE_DISCIPLINE §5.
