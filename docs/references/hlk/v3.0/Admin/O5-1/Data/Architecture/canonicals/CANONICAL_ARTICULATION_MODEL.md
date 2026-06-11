---
title: Holistika Canonical Articulation Model (HCAM)
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Architect
co_authors:
  - Data Governance Office
  - Data Steward
  - CDO
  - AI Engineer
last_review: 2026-06-10
last_review_by: Data Architect
last_review_at: 2026-06-10
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-95-A
  - D-IH-95-B
status: active
register: internal
linked_canonicals:
  - SEMANTIC_LAYER.md
  - DATA_ARCHITECTURE.md
  - dimensions/ENTITY_CATALOG.csv
  - dimensions/CANONICAL_RELATIONSHIP_REGISTRY.csv
  - ../Governance/canonicals/DATA_GOVERNANCE_POLICY.md
companion_to:
  - SEMANTIC_LAYER.md
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
---

# Holistika Canonical Articulation Model (HCAM)

> The **enterprise ontology** of Holistika — the entity-and-relationship tier of the
> Semantic Layer. It declares, for every canonical artifact type, **what it is** (entity
> catalog) and **how it links** (a closed ArchiMate verb set + a valid-triple registry).
> HCAM is the missing semantic layer of the three-tier Data Architecture (T1 git CSV →
> T2 Supabase → **T3 Neo4j**); together they form the **Digital Twin of the Organization
> (DTO)** — "the Singularity". Research base (168 sources):
> `docs/wip/intelligence/canonical-articulation-model-2026-06-05/`.

## 1. Purpose

Holistika has 42 canonical artifact types, each with internal layers, that must link to
each other (including the Data area's own world — data contracts, products, stores, models,
BI/analytics consumers, integration adapters, catalog, glossary, applications/ERP). Without a model, links accrete ad hoc (one FK column per CSV; one Neo4j edge
per initiative — the same whole-part relationship forked into `PARENT_OF` /
`PROGRAM_PARENT_OF` / `TOPIC_PARENT_OF`). HCAM sets the **bar**: one entity catalog, one
closed verb set, one governed valid-triple registry. CSVs stay SSOT (T1); Neo4j is the
projection (T3); HCAM is the metamodel above both.

## 2. The two registries (SSOT)

| Registry | Role | Validator |
|:---|:---|:---|
| `dimensions/ENTITY_CATALOG.csv` | 42 canonical types → ArchiMate aspect + Zachman cell + SSOT + Neo4j label + owning area (incl. the Data-area sweep: data_contract/product/store/model, bi_consumer, adapter, data_catalog, glossary_term, application) | `scripts/validate_canonical_articulation.py` |
| `dimensions/CANONICAL_RELATIONSHIP_REGISTRY.csv` | valid `(source_type, verb, target_type)` triples = an ISO/IEC 39075:2024 GQL *graph type* | (same; wired into `validate_hlk.py`) |

Pydantic SSOT: `akos/hlk_canonical_articulation.py`.

## 3. The closed verb set (ArchiMate-grounded)

`composition` · `aggregation` · `assignment` · `realization` · `serving` · `access` ·
`influence` · `triggering` · `flow` · `specialization` (+ `association` last-resort).

- **Intra-type layers** (process project→activity→task; role seniority; topic/area/program
  trees) = **composition**. One recursive verb — collapses the three forked `*_PARENT_OF`.
- **Inter-type links** = the dependency/dynamic verbs (assignment, realization, serving,
  influence, triggering, flow).
- Each verb maps to one **unified Neo4j edge** (`VERB_TO_NEO4J_EDGE`) — pre-wires the I91
  graph unify (I95 P2/C): forked edges migrate to the verb taxonomy; node labels disambiguate.

## 4. Layers (intra-type hierarchies)

Recursive parent-child (`item_parent_*_id`, `reports_to`, topic parent). For traversal at
scale use bridge-table or pathstring patterns (Kimball/MDM); shared-ownership (a node with
two parents, e.g. an initiative in two programs) is allowed via multiple `aggregation`
triples. Stable IDs survive renames (APQC element-ID pattern).

## 5. Ownership — Data-federated (D-IH-95-A)

| Seat | HCAM responsibility |
|:---|:---|
| **CDO** | Accountable; chairs the **Semantic Council** |
| **Data Architect** | Authors HCAM (entity catalog + verb taxonomy) |
| **Data Governance Office** | Owns `CANONICAL_RELATIONSHIP_REGISTRY` (masterdata relationship management) |
| **Data Steward** | Operational triple stewardship |
| **AI Engineer / System Owner** | Neo4j graph platform (T3) |
| **8 area reps** | Federate their area's concept definitions |

**Wired into existing Governance (reuse, not parallel):** cross-area changes ratify via
`DECISION_REGISTER`; the council operates as a governed process (`process_list` + SOP-META);
per-area concepts flow through the area-governance methodology with **area-completeness v3
(articulation completeness)** as the acceptance check; actions in `OPS_REGISTER`; HCAM
registered in `CANONICAL_REGISTRY` across the Data three-tier architecture. People/Compliance
keeps the area-governance **methodology** (distinct from HCAM). *Semantic Council stand-up +
its SOP land in I95 P3/E.*

## 6. Competency questions (acceptance test)

1. Which processes is role R assigned to, and which capabilities do those realize?
2. What serves engagement E end-to-end, back to the roles that perform it?
3. If capability C is retired, which areas/roles/engagements are impacted?
4. Show process P's full layer path (project → … → task).
5. Is every canonical in area A wired (no orphans; valid triples only)?

ArchiMate **derivation** (weakest-link) answers Q1–Q3 without modeling every hop.

## 7. Stewardship cadence

Quarterly review aligned with the area-completeness sweep (same cadence as `SEMANTIC_LAYER.md`).
New triples: draft `status=planned` → Semantic Council review → `active` on operator-approved
tranche → projected to Neo4j on next sync (parity-checked).

## 8. Methodology prong articulation (D-IH-94-A)

Research Methodology mint wires through **three registries** — not a parallel framework:

| Layer | Registry | What got registered |
|:---|:---|:---|
| **Artifact inventory** | `CANONICAL_REGISTRY.csv` | Prong lattice, HxPESTAL intent tracker, pillars (PESTEL/Porter/HxPESTAL), synthesis SOP, plus backfill of Research Action + Radar disciplines |
| **Precedence / audit** | `PRECEDENCE.md` | Already complete at methodology mint |
| **Relationship verbs** | `CANONICAL_RELATIONSHIP_REGISTRY.csv` | TRP-061 canonical⊃canonical; TRP-062 canonical→serves→process; TRP-063 AIC→realizes→capability (planned) |

Markdown doctrines are **git-only** (T1) — they do **not** get `CANONICAL_GOVERNANCE_REGISTRY.csv` rows
(that registry is CSV/mirror inventory only per P95-GOV-1). `entity_type=canonical` in
`ENTITY_CATALOG.csv` already covers them.

**Executable pairing (closed 2026-06-10):** `process_list.csv` rows `hol_resea_dtp_99`, `hol_resea_dtp_315`,
and umbrella `hol_resea_dtp_prong_synthesis_001` pair to `SOP-RESEARCH_PRONG_SYNTHESIS_001.md`
(commit `1d5c2c62`; D-IH-94-A).

**Standing discipline (all areas):** [`../Governance/canonicals/SSOT_REGISTRY_AUDIT_DISCIPLINE.md`](../Governance/canonicals/SSOT_REGISTRY_AUDIT_DISCIPLINE.md)
— four-registry sweep on every mint; AskQuestion touch-gate balance; J-OP prose bar.
Agent rule: `.cursor/rules/akos-ssot-canonical-touch.mdc`.

## 9. Cross-references

- Semantic Layer (metrics tier): `SEMANTIC_LAYER.md`
- Data Architecture (T1/T2/T3): `DATA_ARCHITECTURE.md`
- Graph projection: `akos/hlk_graph_model.py`; graph rework: I91
- Research base: `docs/wip/intelligence/canonical-articulation-model-2026-06-05/` (brainstorm + master-synthesis + DG findings; 168-source ledger)
- Decisions: `D-IH-95-A` (model), `D-IH-95-B` (catalog + verbs + triples)

## Evidence base

**Internal:** the fork in `hlk_graph_model.py`; `process_list.item_granularity` layers; the
existing `SEMANTIC_LAYER.md` + `DATA_ARCHITECTURE.md`; the Data roster (Architect/Governance
Lead/Steward "masterdata relationship management").

**External:** ArchiMate 3.1/3.2/4.0 closed relationship set + 4.0 process de-fork (The Open
Group); ISO/IEC 39075:2024 GQL graph types; TOGAF content metamodel; Zachman coverage lattice;
DAMA-DMBOK metadata management; data-mesh federated computational governance; DTO / enterprise
knowledge graph (Gartner); APQC 5-level decomposition. Full ledger: 168 sources.
