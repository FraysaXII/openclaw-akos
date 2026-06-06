---
title: SOP — HCAM Semantic Council
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_SEMANTIC_COUNCIL_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Office
co_authors:
  - CDO
  - Data Architect
  - Data Steward
last_review: 2026-06-06
last_review_by: Data Governance Office
last_review_decision_id: D-IH-95-C
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-95-A
  - D-IH-95-C
status: active
register: internal
linked_canonicals:
  - ../../Architecture/canonicals/CANONICAL_ARTICULATION_MODEL.md
  - ../../Architecture/canonicals/dimensions/ENTITY_CATALOG.csv
  - ../../Architecture/canonicals/dimensions/CANONICAL_RELATIONSHIP_REGISTRY.csv
  - DATA_GOVERNANCE_POLICY.md
  - ../../../People/Compliance/canonicals/DECISION_REGISTER.csv
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
linked_runbooks:
  - scripts/validate_canonical_articulation.py
  - scripts/validate_area_completeness.py
linked_processes:
  - thi_data_dtp_semantic_council_001
cadence: scheduled
cadence_trigger: quarterly review (aligned with area-completeness sweep) OR new entity type / verb / cross-area triple OR forked-edge cutover (I91) OR competency-question regression
---

# SOP — HCAM Semantic Council

## Purpose

Operationalise **how the Holistika Canonical Articulation Model (HCAM) is governed** —
the closed entity catalog, the closed verb set, and the valid-triple registry — under a
**federated** model (per `D-IH-95-A`): Data authors + stewards the metamodel; **each area
federates its own concept definitions**; cross-area changes ratify through the existing
`DECISION_REGISTER`. The council is the standing body; this SOP is its runbook.

> **Reuse, not parallel governance.** The council sits *inside* the existing fabric — O5
> Executive Governance Board oversight, `DECISION_REGISTER` ratification, this SOP as a
> governed `process_list` process, the area-governance methodology for per-area concepts,
> `OPS_REGISTER` for actions, `CANONICAL_REGISTRY` for the HCAM canonicals.

## Membership

| Seat | Role | Mandate |
|:---|:---|:---|
| **Chair** | CDO | Accountable; convenes; final sign-off on enterprise-level changes (escalates to O5) |
| **Author** | Data Architect | Owns the entity catalog + verb taxonomy |
| **Registry owner** | Data Governance Office | Owns `CANONICAL_RELATIONSHIP_REGISTRY` + valid-triple standards |
| **Operations** | Data Steward | Day-to-day triple stewardship (masterdata relationship management) |
| **Platform** | AI Engineer + System Owner | Neo4j graph (T3) projection + parity |
| **Area reps (8)** | one owner per scored area — Data, Tech, Finance, Marketing, Operations, People, Research, Legal | Federate their area's concept/triple definitions |

## Scope

| In scope | Out of scope |
|:---|:---|
| Entity catalog adds/changes (`ENTITY_CATALOG.csv`) | Re-authoring area content (areas own their canonicals) |
| Verb-set changes (closed; additions need strong justification) | Per-CSV FK schema (owned by each register's validator) |
| Valid-triple adds/promotions (`planned` → `active`) | Neo4j infra provisioning (Tech / I91) |
| Forked-edge cutover decisions (I91 unblock) | Area-completeness *scoring grid* (People area-governance) |

## Preconditions

1. Proposed entity types ∈ a real SSOT (or marked `planned` with the SSOT named).
2. Proposed triples use the **closed verb set** (`association` only as last-resort, flagged).
3. `neo4j_edge_type` matches the verb (`VERB_TO_NEO4J_EDGE`).
4. Cross-area triples have the consuming area rep's sign-off (federation).

## Steps (AC-HUMAN)

1. **Propose** — area rep (or Data Architect) drafts the entity row / triple with `status=planned`;
   names the backing FK or the forward SSOT.
2. **Federate** — affected area reps confirm the concept matches their domain (no silent cross-area
   redefinition; business meaning has a named area home).
3. **Validate** — run AC-AUTOMATION; fix FAIL before review.
4. **Council review** — quarterly (or event-triggered): chair + registry owner + affected reps
   approve; `association` rows get extra scrutiny (must justify why no stronger verb fits).
5. **Ratify** — material/cross-area changes recorded as a `DECISION_REGISTER` row (`D-IH-*`);
   `status: planned → active` once the backing FK is wired.
6. **Project** — on next Neo4j sync, active triples project to the unified edges (parity-checked);
   forked-edge cutover follows the staged plan (dual-emit one cycle → retire legacy) when I91 unblocks.
7. **Record** — council action logged in `OPS_REGISTER`; entity/triple deltas cited in the
   wave-close evidence.

## Steps (AC-AUTOMATION)

```powershell
py scripts/validate_canonical_articulation.py                 # schema + catalog<->triple integrity + verb<->edge
py scripts/validate_canonical_articulation.py --self-test
py scripts/validate_canonical_articulation.py --articulation <Area>   # CQ5: is the area wired (no orphan canonicals)?
py scripts/validate_hlk.py                                    # golden path (CANONICAL_ARTICULATION row)
```

## Cadence

| Trigger | Action |
|:---|:---|
| Quarterly (aligned with area-completeness sweep) | Review catalog + triple health; promote `planned`→`active` where FKs now exist |
| New entity type / verb / cross-area triple | Propose → federate → validate → ratify |
| Forked-edge cutover (I91 unblock) | Approve dual-emit cycle then legacy retirement (`hlk_graph_articulation.py` map) |
| Competency-question regression | Restore the broken articulation; do not silence the query |

## Escalation

Area rep → Data Governance Office → CDO (chair) → O5 Executive Governance Board for
enterprise-level or contested cross-area changes, per `DATA_GOVERNANCE_POLICY.md` §3.

## Cross-references

- Model: `../../Architecture/canonicals/CANONICAL_ARTICULATION_MODEL.md`
- Registries: `ENTITY_CATALOG.csv`, `CANONICAL_RELATIONSHIP_REGISTRY.csv`
- Edge unify map (I95 P2/C): `akos/hlk_graph_articulation.py` + `reports/p2-neo4j-edge-unify-2026-06-05.md`
- Decisions: `D-IH-95-A` (model + Data-federated ownership), `D-IH-95-B` (catalog), `D-IH-95-C` (edge unify)
- `linked_processes` row `thi_data_dtp_semantic_council_001` minted in `process_list.csv` (I95 Q2
  batch 3, `D-IH-95-D`): area=Data, owner=Data Governance Office, paired to this SOP.
