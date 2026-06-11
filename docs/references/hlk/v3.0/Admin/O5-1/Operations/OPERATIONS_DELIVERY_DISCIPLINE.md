---
title: Operations Delivery Doctrine
language: en
intellectual_kind: doctrine
access_level: 4
audience: J-OP;J-AIC
status: active
canonical: true
role_owner: COO
authored: 2026-06-10
last_review: 2026-06-10
last_review_by: COO
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-94-A
register: internal
linked_canonicals:
  - OPERATIONS_AREA_CHARTER.md
  - PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md
  - RevOps/canonicals/REVOPS_AREA_CHARTER.md
  - SMO/canonicals/SOP-SERVICE_MGMT_001.md
  - ../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - ../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
linked_cursor_rules:
  - .cursor/rules/akos-operations-delivery.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
  - .cursor/rules/akos-holistika-operations.mdc
upstream_ssot:
  - ../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md
companion_to:
  - OPERATIONS_AREA_CHARTER.md
---

# OPERATIONS_DELIVERY_DOCTRINE — PMBOK 7 performance domains (AREA-03)

> Unblocks AREA-03 on the area-completeness matrix. Maps PMI PMBOK Guide 7th
> Edition **eight performance domains** to Holistika Operations sub-areas.
> External grounding: [PMI PMBOK Guide](https://www.pmi.org/standards/pmbok) +
> thinking-seat synthesis Step 3.

## 1. Why this doctrine exists

`validate_area_completeness.py` flagged Operations at crit@L3 9/10 because no
area-level delivery doctrine existed — only sub-area charters (RevOps) and routing
doctrine (Operational Cohesion). Without AREA-03, the area-completeness scorer
cannot certify Operations as **COMPLETE for tier** even when registries are rich.

## 2. PMBOK 7 domains → Holistika Operations

| PMBOK 7 domain | Holistika owner | Primary artefacts | Automation hook |
|:---|:---|:---|:---|
| **Stakeholders** | PMO + RevOps | Adviser router, engagement handoffs, QBR | `render_operator_inbox.py` |
| **Team** | PMO + COO chain | baseline_organisation roles, engagement models | area completeness `--next` |
| **Development Approach & Life Cycle** | PMO + Engagement | Initiative/program anchors, engagement templates | `pmo_program_anchor_backfill.py` |
| **Planning** | PMO | WIP dashboard, initiative harmonisation SOP | `render_wip_dashboard.py` |
| **Project Work** | Engagement + PMO | Discovery → proposal → estimation SOPs | `scaffold_engagement.py` |
| **Delivery** | RevOps + Engagement | Revenue spine, template promotion, client delivery | `revops_dispatch.py` |
| **Measurement** | PMO + RevOps | Cohesion index, area score matrix, DORA posture | `render_operational_cohesion_index.py` |
| **Uncertainty** | PMO + SMO | Risk registers, SLA matrix, service catalog | `validate_area_completeness.py` |

PMBOK 8 seven domains (Governance, Scope, Schedule, Finance, Stakeholders,
Resources, Risk) map to ERP forward panels (I89/I92) without duplicating
Finance/Data canonicals — cross-reference only.

## 3. Project vs service tag

| Tag | Sub-areas | Examples |
|:---|:---|:---|
| **project** | PMO, RevOps, Engagement | Initiatives, client engagements, QBR cycles |
| **service** | SMO | SERVICE_CATALOG rows, SLA rhythm |
| **hybrid** | PMO programs | Long-running programs with service-like BAU tail |

The Operations **area** is unified; the tag drives which SOP family and cadence
apply — not a split of folder ownership.

## 4. Automation-first posture (operator ratification Q2)

Priority order for executable catalog pairing (P2 tranche):

1. Inbox / WIP / cohesion render loop (PMO)
2. Mirror emit trigger (Holistika two-plane handoff to Data)
3. Area completeness sweep (tier gate evidence)
4. Engagement scaffold + RevOps dispatch
5. Remaining PMO/SMO SOPs (AREA-09 cliff — enhancing, not tier-blocking)

Human-gated: canonical CSV edits, file moves (IntelligenceOps eviction), live
Supabase mirror apply.

Cross-area trigger register: [`canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md`](canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md)
(I94 P4). Operations fires; sister areas own doctrine per handoff class table there.

## 5. Quality Fabric composition

Operations delivery artefacts compose per
[`HOLISTIKA_QUALITY_FABRIC.md`](../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md):

- **Audience:** J-OP primary; J-AIC co-executor on runbooks.
- **Governance:** PRECEDENCE canonical; synthesis-before-tranche on P2+ commits.
- **Brand:** CORPINT-internal register for doctrine; translated-external only on
  client-facing Engagement deliverables (Engagement sub-area).

## 6. Evidence base

- Internal: [`i94-operations-area-source-ledger.csv`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-area-source-ledger.csv)
- Synthesis: [`i94-operations-area-research-synthesis-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-area-research-synthesis-2026-06-10.md)
- Upstream SSOT: [`i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md)

## 7. Cross-references

- Area charter: [`OPERATIONS_AREA_CHARTER.md`](OPERATIONS_AREA_CHARTER.md)
- Paired skill: [`.cursor/skills/operations-delivery-craft/SKILL.md`](../../../../../../.cursor/skills/operations-delivery-craft/SKILL.md)
- I94 charter P2–P6: [`i94-operations-operational-sweep-charter-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-charter-2026-06-10.md)
