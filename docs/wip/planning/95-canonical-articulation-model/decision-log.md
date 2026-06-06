# I95 Decision Log — Canonical Articulation Model (the Singularity)

Derived from I94 per operator instruction (2026-06-05). Research base:
[`docs/wip/intelligence/canonical-articulation-model-2026-06-05/`](../../intelligence/canonical-articulation-model-2026-06-05/)
(115 sources; validator PASS).

## D-IH-95-A — I95 inception + model ratification (2026-06-05, architecture, medium reversibility)

**Decision.** Adopt the **Holistika Canonical Articulation Model (HCAM)** as the enterprise
ontology that binds every canonical artifact, and frame the end-to-end pairing as **the
Singularity = Digital Twin of the Organization (DTO)**.

**Operator inputs (verbatim intent).**
- d_artic: **Option D — "go all out"**; pass gains bidirectionally to/from the planned Neo4j graph
  rework; enrich + research **"the Singularity"** (physics-inspired e2e enterprise pairing); liked
  the **ArchiMate enterprise-architecture metamodel** framing ("SOTA, less pseudoscience; depends
  on channel/audience"); **E** but doctrine home is **People → Knowledge Manager** (KM needs
  rework — "we got more value from being holistik than from them; the sub-area is not par"); and
  *"is an area complete with all those things?"* → mint a **SOTA-quality** completeness definition;
  research **50+ internal + 50+ external** on ArchiMate and **mint** it.
- init_shape: **I95** (derived from I94, start now).
- sequence_vs_i94: **articulation-first** (it informs Operations/Legal/Envoy wiring).

**What was ratified.**
1. **The Singularity = DTO** (Gartner; enterprise ontology + knowledge graph + meta-metamodel).
   Two registers: "Singularity/DTO" (vision/internal/brand) vs "ArchiMate + ISO GQL" (technical/
   external) — Quality-Fabric resolves per surface.
2. **HCAM** = closed entity catalog (~30 types → ArchiMate element + Zachman cell) + closed **~10
   ArchiMate verbs** + **`CANONICAL_RELATIONSHIP_REGISTRY.csv`** of valid `(source,verb,target)`
   triples (= an ISO/IEC 39075:2024 **GQL graph type**).
3. **De-fork** `PARENT_OF`/`PROGRAM_PARENT_OF`/`TOPIC_PARENT_OF` → one `composition` verb
   (ArchiMate 4.0 precedent).
4. **Layers** = composition + ragged-hierarchy patterns (APQC 5-level / Kimball bridge+pathstring /
   MDM recursive + shared-ownership).
5. **Stay LPG (Neo4j)** + impose the typed schema (TPG); RDF mapping deferred to any future
   federation.
6. **Knowledge Manager** role minted under People to own HCAM (gated `baseline_organisation`
   change); KM is currently diffused across CPO / Learning Curator / AI Engineer.
7. **Area-completeness v3 = articulation completeness** (every canonical wired with valid triples),
   subsuming the 16-component grid (AREA-15/16 are already HCAM relationships).

**Build.** Option D staged **B (relationship registry SSOT) → C (Neo4j unify, bidirectional with
graph rework) → E (KM doctrine home + area-completeness v3 + repo-wide FK→verb mapping)**. Each
phase operator-gated; B is zero-rewiring.

**Reversibility: medium.** B is additive (low risk). C renames live edges (rebuildable index, so
recoverable). E touches `baseline_organisation` (gated) + the area model (v3). Staging keeps each
step recoverable.

**Supersedes:** none (extends `D-IH-94-A`). **Confidence:** Keter (115-source backed).

---

## D-IH-95-B — HCAM catalog + verbs + triples (RATIFIED 2026-06-05, architecture, low reversibility)

Operator signed off (catalog_signoff_first) then build executed. **ENTITY_CATALOG.csv** = 33 types
(31 + operator-added **Workstream** + **Brand**), each → ArchiMate aspect + Zachman cell + SSOT +
Neo4j label + owning area. **CANONICAL_RELATIONSHIP_REGISTRY.csv** = 38 triples on the closed 10+1
ArchiMate verb set, incl operator-added **Skill→Role** (TRP-028), **Use-case→Capability** (TRP-029),
**AIC→Process** (TRP-030) + Workstream/Brand links. Pydantic `akos/hlk_canonical_articulation.py` +
`scripts/validate_canonical_articulation.py` wired into `validate_hlk.py` (PASS; 6 tests; self-test).
`neo4j_edge_type` pre-wires the I91 unify (C) — forked `*_PARENT_OF` → `COMPOSED_OF`. Published as
Data-Architecture canonical `CANONICAL_ARTICULATION_MODEL.md` (sibling to `SEMANTIC_LAYER.md`).
Coupled with **I91**. Zachman coverage 6/6.

## D-IH-95-C — Neo4j edge unify map + competency queries (RATIFIED 2026-06-05, architecture, low reversibility)

`akos/hlk_graph_articulation.py` maps all **13 legacy edges → 6 unified verb-edges** (the three
forked `*_PARENT_OF` + `REPORTS_TO` + `UNDER_PROGRAM` → `COMPOSED_OF`; subsumes + `UNDER_TOPIC` →
`AGGREGATES`; `OWNED_BY` → `ASSIGNED_TO`; `CONSUMES`/`PRODUCES_FOR` → `FLOWS_TO`; `DEPENDS_ON` →
`SERVES`; `RELATED_TO` → `ASSOCIATED_WITH`). Adds the **5 competency-question** Cypher sketches +
`assert_edge_coverage()` parity (13→6). **Additive / non-destructive** — the live projection +
parity + sync are untouched (Neo4j preflight-blocked per I91). The edge rename is a **gated
cutover** (Semantic Council + I91 unblock; dual-emit one cycle). 9 tests PASS. Report:
`reports/p2-neo4j-edge-unify-2026-06-05.md`.

## D-IH-95-D — area-completeness v3 (articulation tier) + Semantic Council SOP (RATIFIED 2026-06-06, architecture, low reversibility)

Extends area-governance **v2** (`D-IH-94-A`) with a **v3 articulation tier**: completeness =
*present* (the v2 16-component L0–L5 grid, **unchanged**) **and** *wired* (every entity type an
area owns participates in ≥1 active HCAM triple). Runnable as **CQ5**:
`scripts/validate_canonical_articulation.py --articulation <Area>` (advisory; surfaces orphans for
the Semantic Council; **does not gate** the v2 bar → Data/Finance/People closures preserved).
Authored **`SOP-DATA_SEMANTIC_COUNCIL_001.md`** (CDO chair + Data core + 8 area reps; federated
authorship; `DECISION_REGISTER` ratification; reuses the existing governance fabric).
`AREA_GOVERNANCE_DISCIPLINE.md` → doctrine **v3** (§7.5). `LOGIC_CHANGE_LOG` **BT-08**.
First articulation run: Data 3/8, Marketing 5/7, Tech 4/5, People 7/9, Finance 1/1 wired
(orphans = the `planned` types — correct signal). Council `process_list` row is a **gated** mint
(Q2/Storytelling baseline tranche). `validate_hlk` OVERALL PASS.

### Resolved
- **D-IH-95-E (ownership)** — RATIFIED **Data-federated** + **full council** (operator 2026-06-05).
  The council is now codified in `SOP-DATA_SEMANTIC_COUNCIL_001.md`. Remaining gated piece: the
  council's `process_list` row + member instantiation land with the Q2 baseline tranche.

### Pending sub-decisions (to ratify at each gate)
- **GATED (next):** Q2 Lead-simplification baseline tranche (keep Data Governance Office) +
  Storytelling→Brand merge (`D-IH-72-AO`) + council `process_list` row — one operator-approved
  `baseline_organisation`/`process_list` session.
- **D-IH-95-E** — HCAM ownership + doctrine home. **Corrected recommendation (2026-06-05, Prong E,
  53 sources):** home HCAM in **Data** as the entity/relationship tier of `SEMANTIC_LAYER.md`,
  governed **federated** (Data Architect authors; Data Governance Office owns the relationship
  registry — their charter says "masterdata relationship management"; Data Steward operates; AI
  Engineer/System Owner run the graph platform; CDO chairs a **Semantic Council** with one rep per
  area; **People/Compliance keeps the area-governance *methodology***). **Not** Learning Curator→KM
  (wrong skillset); Research = contributor, not owner. Couple with **I91** graph rework as one
  workstream. The Q2 Lead simplification + Q3 ghost-folder merges fold in here as HCAM placement
  work. *Pending operator ratification of the ownership model.* See
  [`../../intelligence/canonical-articulation-model-2026-06-05/data-governance-ownership-findings.md`](../../intelligence/canonical-articulation-model-2026-06-05/data-governance-ownership-findings.md).
