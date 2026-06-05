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

### Pending sub-decisions (to ratify at each gate)
- **D-IH-95-B** — `CANONICAL_RELATIONSHIP_REGISTRY.csv` schema + the closed verb set + initial
  valid-triple matrix (entity catalog freeze).
- **D-IH-95-C** — Neo4j edge-rename map + derivation/competency-question queries.
- **D-IH-95-E** — Knowledge Manager role definition + area-completeness v3 doctrine (+ the Q2 Lead
  simplification + Q3 ghost-folder merges fold in here as HCAM placement work).
