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

## D-IH-95-E — articulation GOLD LAYER (visibility metrics) + S-13 regression surface + operating model (RATIFIED 2026-06-06, architecture, low reversibility)

Closes the operator's **visibility gap** (*"I don't know where/how/what it gives… no useful metrics
/ no gold layer / no UI for a DGO user"*). Adds the area-completeness **v3 gold layer**:
`validate_canonical_articulation.py --matrix` = a consistent single-pane scorecard (per-area
wiring% + orphans + enterprise rollup: entity coverage, triple activation, Zachman 6/6, DQ-badge
GREEN/AMBER/RED). Registers 3 **define-once** metrics in `METRICS_REGISTRY`
(`MET-HOL-ARTICULATION-WIRING-SCORE` / `-TRIPLE-ACTIVATION` / `ENTITY-CATALOG-COVERAGE`) so the
ERP/BI consume them (semantic layer, not bespoke). Adds **S-13** (articulation+visibility) to the
intent-ranked regression (ICS 32; IT-3 governance + IT-4 visibility) so the blind spot can't recur.
Grounded in research: 12-KPI balanced governance scorecard + medallion gold layer (DQ-cert badges
that let automated pipelines self-gate). **Baseline: 69% entity coverage, 63% triple activation,
AMBER.** Operating model: `reports/articulation-operating-model-2026-06-06.md`. Regression:
`reports/intent-ranked-regression-2026-06-06.md`. Also: `OPS-95-1` (Supabase mirror re-sync, tracked).

### Resolved
- **Ownership** — RATIFIED **Data-federated** + **full council** (operator 2026-06-05, under
  `D-IH-95-A`/`D-IH-95-D`; the AskQuestion ratifications, not a separate decision ID). Codified in
  `SOP-DATA_SEMANTIC_COUNCIL_001.md` + the `thi_data_dtp_semantic_council_001` process row.
- **Q2/Q3/Storytelling/council-row** — DONE (the 3-commit gated batch, `D-IH-95-D`).

## D-IH-95-G — Round-2 batch ratification: 9 ecosystem/linking decisions (RATIFIED 2026-06-07, architecture, high reversibility-mix)

Operator ratified the 9-decision Round-2 batch from the 4-agent research sweep
([`round2-research-synthesis-2026-06-06.md`](../../intelligence/canonical-articulation-model-2026-06-05/round2-research-synthesis-2026-06-06.md)).
This is the second AskQuestion-ratified batch (Round-1 had its own); together they clear the
operator's "+12 ratified" bar (**23 total**).

| # | Decision | Verdict |
|:--|:--|:--|
| R2-01 | Process ↔ Capability | **KEEP SEPARATE + de-densify** (1119→~50-150; `realization` link; no fusion) |
| R2-02 | Knowledge Management home | **3-way split**; sellable CI-quality → **Research** (KM Officer seat, no new role) |
| R2-03 | Supabase full-ecosystem governance | **mint the ecosystem registries** (phased EG-1..5) + drift-prevention CI |
| R2-04 | 40+ open-thread inventory + drift | **adopt as backlog SSOT** + fix index drift now |
| R2-05 | FK→verb mapping (all-out) | **per-registry tranches**, value-organized |
| R2-06 | Orphan burn-down order | **by area, equal slices** (operator override of value-ranked) |
| R2-07 | IntelligenceOps eviction | → **Research** + migrate `wip/intelligence` into a **governed topic structure** |
| R2-08 | DRIFT-8 biz-strategy artifacts | re-home → **Finance** (pricing/unit-econ) + **Marketing/Strategy** (theses) |
| R2-09 | Neo4j online-every-time | **free write keep-alive ping now** + budget ~$65/mo Professional |

### Executed at ratification (commit 1 — governance scaffold)
- **R2-03 EG-1:** `SUPABASE_MODULE_REGISTRY.csv` (27 modules: 9 governed / 7 partial / 11 ungoverned)
  + `SUPABASE_ECOSYSTEM_GOVERNANCE.md` canonical + `validate_supabase_module_registry.py` (wired into
  `validate_hlk`, PASS; critical-ungoverned flagged: public-legacy / Auth / API-exposure).
- **R2-04:** index drift fixed (research README KM-stale → Data-federated; roadmap B/C/E
  pending→ratified; hcam sign-off frontmatter → `signed_off`).
- **R2-09:** `.github/workflows/neo4j-aura-keepalive.yml` (daily write ping; secrets-gated).

### Executed LIVE on Supabase (commit 2 — operator execution grant 2026-06-07)
Operator granted direct execution ("I approve you doing it… when a canonical changes we sync
supabase"). Done via Supabase MCP on project MasterData (`swrmqpelgoblaquequzb`), verified, repo-synced:
- **DB-02 (drop dead):** dropped 10 verified-dead KiRBe-era test/dupe `public.*` tables
  (`test_aapl` 1258 rows, `test_clients/contract/process/product`, `example_csv`, `document_vectors`
  dupe, `users2` dupe, `"Test access"`, `"Process list"`) — pre-checked: no FK, no view deps.
  Public tables 34 → 24.
- **DB-03 (RLS):** RLS **deny-by-default** on the 13 surviving RLS-disabled `public.*` tables +
  enabled RLS on `kirbe.kirbe_organizations` (had inert policies). **Critical `rls_disabled`
  advisory 16 → 0; 0 security ERRORs** (verified via catalog query, not just cached advisor).
  `service_role` (AKOS backend) bypasses RLS, so nothing breaks.
- **Repo sync:** 3 migration files written matching remote versions
  (`20260607191541/191554/191652`) — two-plane DDL ledger stays in sync.
- **DB-01 (mirror re-sync):** drift-prevention **automated** — `supabase-mirror-sync.yml` emits the
  mirror DML on every canonical-CSV push to main + gated apply via the `SUPABASE_DB_URL` secret. The
  one-time re-sync DML is 6.9 MB / 2727 statements (too large to hand-apply via MCP — CI `psql` is the
  right mechanism). `SUPA-MOD-09` ungoverned→**governed**; `OPS-95-1` updated. Evidence:
  [`reports/supabase-eg2-execution-2026-06-07.md`](reports/supabase-eg2-execution-2026-06-07.md).
- **Operator action remaining:** set repo secrets `SUPABASE_DB_URL` (mirror auto-apply) +
  `NEO4J_URI/USERNAME/PASSWORD` (keep-alive).

### Sequenced (next phases — see master-roadmap)
- **R2-01** capability de-densify · **R2-05** FK→verb tranches · **R2-06** orphan by-area ·
  **R2-07** IntelligenceOps→Research + topic restructure · **R2-08** biz-strategy re-home ·
  **EG-2..5** Supabase sub-registries (edge-fn / cron / extension / RLS-posture / API-exposure / FDW).

### Gated (operator/SOC approval per step)
- Capability collapse (canonical CSV) · KM Officer seat activation (`baseline_organisation`) ·
  legacy `public.*`/`kirbe.*` DDL drop + RLS-on-survivors (data-loss + SOC).

## D-IH-95-H — L2 + L5 execution ratification (RATIFIED 2026-06-07, architecture, mixed reversibility)

Operator ratified the 8 parameter decisions from the two research-backed findings docs
([L2 capability](../../intelligence/canonical-articulation-model-2026-06-05/l2-capability-densify-findings-2026-06-07.md),
[L5 topic](../../intelligence/canonical-articulation-model-2026-06-05/l5-topic-structure-findings-2026-06-07.md)).

**L2 — capability de-densify** (keep-separate upheld; collapse 1,119 → stable map):
| # | Decision | Verdict |
|:--|:--|:--|
| Band | target count | **area-by-area, count falls out organically** (operator override of the ~60–110 band) |
| Shape | 4 refinements | **accept all** — evict ~27 code-symbols → component registry; merge cross-entity dups → one bearer-agnostic capability; `bearer_class` → realization edge (TRP-006/038); add `capability_tier` |
| Rating | cadence | **hybrid** rolling ~8/wk + event-triggered + value-tier (weekly cron) |
| Tranche | execution | **per-domain slices** (gated canonical-CSV) |

**L5 — topic structure** (chassis ~80% exists; govern + bind + curate, not build):
| # | Decision | Verdict |
|:--|:--|:--|
| Physical | move vs key-in-place | **PHYSICAL MOVE authorized** into a topic-keyed tree + **`akos-research-area.mdc` amended** (governed moves allowed; unilateral untraced drift still forbidden) |
| Schema | facets + ownership | **accept all 3** — orthogonal `subject_kind` facets + binding columns; registry populates the HCAM `topic` dimension; activate dormant **KM Officer** steward (no new role) |
| Data | cleanup | **accept + EXPANDED** — lifecycle-gate triage of 11 stranded rows + mint 5 missing rows + **repo-wide sweep of ALL scattered topics** into `TOPIC_REGISTRY` |
| Tranche | execution | **two tranches** (schema → data), each `validate_hlk`-gated |

### Executed at ratification (this commit)
- `akos-research-area.mdc` RULE 2 + anti-patterns **amended** (governed-move authorization).
- `D-IH-95-H` recorded; both findings docs marked ratified; L2+L5 sequenced as phases (roadmap).
- **Dispatched:** background subagent for the **repo-wide scattered-topic inventory** (feeds L5 data tranche).

### Schema pre-steps EXECUTED (2026-06-07, additive/reversible — operator chose "both schema pre-steps now, stop before data tranches")
- **L5 T1 (topic schema):** `TOPIC_REGISTRY.csv` +5 cols (`subject_kind` seeded by mechanical map
  from `topic_class` which is kept; `steward_role`/`working_area_path`/`knowledge_index_path` empty;
  `physical_model=keyed_in_place`) + `TOPIC_REGISTRY_FIELDNAMES` + `validate_topic_registry.py`
  (new enums + optional checks) + mirror DDL (`20260607220031`, applied via MCP).
- **L2 capability pre-step:** `CAPABILITY_REGISTRY.csv` +`capability_tier` (empty) + Pydantic
  `CapabilityRegistryRow` + `VALID_CAPABILITY_TIERS` + mirror DDL (`20260607220044`, applied via MCP).
  (`bearer_class`→edge is deferred to **collapse-time** — no edge home exists pre-de-densification.)
- `validate_hlk` OVERALL PASS. Data tranches (populate `subject_kind`, bind paths, mint the 19 rows,
  triage 11 stranded, the physical move, the area-by-area collapse) remain gated for next session.

### Gated / sequenced (operator-approval per tranche)
- L2 capability collapse (area-by-area slices, canonical-CSV) · L5 **data tranche** (bind/move/mint/triage,
  canonical-CSV) · the physical `wip/intelligence` move · KM Officer seat activation (`baseline_organisation`).

### Pending sub-decisions (to ratify at each gate)
- **D-IH-95-F (future):** I91 graph-edge cutover (dual-emit → retire legacy) when Neo4j unblocks.
- 8-area articulation sweep: burn down the orphan worklist (`--matrix`) via the Semantic Council.
