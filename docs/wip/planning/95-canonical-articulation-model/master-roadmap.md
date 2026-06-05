---
initiative: INIT-OPENCLAW_AKOS-95
title: Canonical Articulation Model (the Singularity)
owner_role: CPO (doctrine home migrating to Knowledge Manager)
status: active
derived_from: INIT-OPENCLAW_AKOS-94
inception_decision: D-IH-95-A
research_base: docs/wip/intelligence/canonical-articulation-model-2026-06-05/
authored: 2026-06-05
---

# I95 — Canonical Articulation Model / the Singularity

**Mission.** Give Holistika the missing third layer of its Digital Twin: an **enterprise ontology
(HCAM)** that says — for every canonical artifact — *what links to what, with which verb, across
which layers*. Built on ArchiMate's closed relationship taxonomy, typed via ISO GQL over the
existing Neo4j projection, owned by a Knowledge Manager, and used to re-frame what "a complete
area" means.

**Why now.** The operator's inception-era unsolved problem; surfaced by I94's sub-folder=role +
placement-integrity work. Articulation-first because Operations/Legal/Envoy (I94 P3/P5/P6) cannot
wire roles↔processes correctly until the verbs + valid triples exist.

## Phase map

| Phase | Scope | Key deliverables | Gate |
|:---|:---|:---|:---|
| **P0** | Research + inception (DONE) | 115-source ledger, brainstorm, master-synthesis, D-IH-95-A, I95 scaffold | operator (this turn) |
| **P1 (=B)** | **Relationship-registry SSOT** | `CANONICAL_RELATIONSHIP_REGISTRY.csv` (entity catalog ~30 types + ~10 verbs + valid `(src,verb,tgt)` triples) + Pydantic `akos/hlk_canonical_articulation.py` + `scripts/validate_canonical_articulation.py` + tests | D-IH-95-B (schema + verb set review) |
| **P2 (=C)** | **Neo4j unify** | edge-rename map (collapse `*_PARENT_OF`→`composition`); verb-typed edges; derivation queries answering the 5 competency questions; parity check vs CSV SSOT | D-IH-95-C (edge map; bidirectional w/ graph rework) |
| **P3 (=E.1)** | **Knowledge Manager doctrine home** | mint/rework KM role in `baseline_organisation.csv`; HCAM published as KM-owned meta-canonical; cursor rule + skill | **canonical-CSV gate** (baseline_organisation) |
| **P4 (=E.2)** | **Area-completeness v3** | re-express the 16-component model as required HCAM triples + articulation-completeness definition; re-prove Data/Finance/People don't regress | D-IH-95 (area model v3 review) |
| **P5 (=E.3)** | **Repo-wide FK→verb mapping** ("the all-out of D") | map every CSV FK column + canonical type to its ArchiMate element/verb; populate triples; the DTO is queryable e2e | per-tranche |
| **P6** | **Fold-in concrete items** | Q2 Lead simplification (keep Data Governance Lead) + Q3 Marketing ghost-folder merge/delete-empties — both are HCAM placement work | canonical-CSV gate (Q2) |
| **P7** | **Closure UAT** | competency questions pass; no Data/Finance/People regression; Neo4j parity; closure verdict | operator closure |

## Competency questions (the acceptance test — must run as one query each)
1. Which processes is role R assigned to, and which capabilities do those realize?
2. What serves engagement E end-to-end, back to the roles that perform it?
3. If capability C is retired, which areas/roles/engagements are impacted?
4. Show process P's full layer path (project → … → task).
5. Is every canonical in area A wired (no orphans; valid triples only)?

## Verification gates (per phase)
- `py scripts/validate_canonical_articulation.py` (new; P1+)
- `py scripts/validate_area_completeness.py --matrix` (no Data/Finance/People regression)
- `py scripts/validate_hlk.py` + `py scripts/check-drift.py`
- Neo4j parity check (P2+); `py scripts/validate_research_action.py` (research base)

## Risks
- **Over-modeling** (ontology-design anti-pattern): mitigate by adopting ArchiMate's fixed verb set
  (no local invention) + starting triples narrow.
- **Big-bang re-wire:** mitigate by staging B→C→E; B is additive/zero-rewire.
- **KM role churn:** baseline_organisation is gated; Lead simplification (Q2) batched with it.
- **Coupling drift with Neo4j rework:** treat as one workstream; edge-rename map is shared SSOT.

## Cross-references
- Research: [`../intelligence/canonical-articulation-model-2026-06-05/master-synthesis.md`](../../intelligence/canonical-articulation-model-2026-06-05/master-synthesis.md)
- Decisions: [`decision-log.md`](./decision-log.md) (D-IH-95-A; B/C/E pending)
- Parent: I94 area model v2 (`docs/wip/planning/94-area-architecture-and-completeness-v2/`)
- Subject: `akos/hlk_graph_model.py`, `baseline_organisation.csv`, `process_list.csv`
