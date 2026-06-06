# HCAM Articulation — operating model (how we maintain + use it to make us better)

**Decision:** `D-IH-95-E` · **Date:** 2026-06-06 · **Owner:** Data Governance Office (federated) ·
**Audience:** J-OP (operator) · J-AIC

> Operator ask: *"Ensure our D is properly reflected and explain how we're going to maintain and
> use these processes to make us better … the goal is articulated automated layers that reflect
> reality and are properly governed so that our operations can focus on other things with more value."*
> This is that explanation.

## 1. The three layers (where truth lives, what's automated)

HCAM is now a **medallion-style** governed stack — each boundary a contract with a quality gate
(external grounding: Databricks/medallion + the 12-KPI governance scorecard):

| Layer | What it is | SSOT | Automated gate |
|:---|:---|:---|:---|
| **Bronze — raw model** | the entity catalog (42 types) + relationship registry (60 triples) | `ENTITY_CATALOG.csv` + `CANONICAL_RELATIONSHIP_REGISTRY.csv` (git T1) | `validate_canonical_articulation.py` (schema + referential integrity + verb↔edge) — wired into `validate_hlk` |
| **Silver — projection** | the typed graph (verb edges) + the FK links that back each triple | Neo4j T3 (rebuildable) ← `hlk_graph_articulation.py` map | edge-coverage parity test (13→6) + `--self-test` |
| **Gold — consumption** | the **DGO/operator scorecard**: per-area wiring %, orphans, enterprise rollup, DQ-badge | `--matrix` + 3 metrics in `METRICS_REGISTRY` (define-once) | the scorecard itself + the metrics the ERP/BI read |

**"Our D is properly reflected":** the Data area owns all three layers — `CANONICAL_ARTICULATION_MODEL.md`
+ `SEMANTIC_LAYER.md` + `DATA_ARCHITECTURE.md` (the T1/T2/T3 three-tier), authored by the Data
Architect, the registry owned by the **Data Governance Office**, metrics in the Data semantic layer.

## 2. How we MAINTAIN it (the cadence — automated where possible)

| Trigger | Who | Action | Surface |
|:---|:---|:---|:---|
| **Every commit / `validate_hlk`** | automated (CI) | schema + referential-integrity gate on the catalog + registry | `validate_canonical_articulation.py` (in the golden path) |
| **New canonical type / FK / cross-area link** | area rep → Data Governance Office | propose `planned` triple → federate → ratify (`DECISION_REGISTER`) → wire FK → flip `active` | Semantic Council SOP `SOP-DATA_SEMANTIC_COUNCIL_001` |
| **Quarterly (+ wave-close)** | Semantic Council (CDO chair) | run `--matrix`; disposition orphans (planned→active or accept/defer); review the DQ-badge trend | the gold-layer scorecard |
| **I91 unblock (Neo4j)** | AI Engineer + Council | dual-emit legacy+unified edges one cycle → retire legacy | `hlk_graph_articulation.py` cutover plan |

The maintenance is **mostly automated** (the validator runs on every commit; the scorecard is one
command) — humans only act on the **orphan worklist** the gold layer surfaces.

## 3. How we USE it to make us better (the value — free ops for higher-value work)

This is the operator's goal — *"operations focus on other things with more value."* Concretely:

1. **Visibility without a UI.** `py scripts/validate_canonical_articulation.py --matrix` gives the
   DGO/operator the single-pane answer to "where/how/what" in one command — no dashboard build
   required. (Baseline: 69% entity coverage, 63% triples active, AMBER.) When the ERP lands, the
   3 `METRICS_REGISTRY` rows render straight into it (define-once, no rework).
2. **Orphans become a worklist, not a mystery.** Each below-100% area shows *exactly which*
   canonicals aren't wired (e.g., Data's `data_product`/`data_model`/`catalog` are `planned`).
   That's a prioritized backlog the council burns down — turning "I don't know what happens" into
   "here are the 13 specific links to wire next."
3. **Automated self-gating (the SOTA move).** The DQ-badge + metrics let downstream pipelines/agents
   *gate themselves on the badge* (per the medallion DQ-certification pattern) instead of a human
   re-checking — e.g., an AIC can refuse to act on an un-wired canonical. Humans stop being the gate.
4. **Drift reflects reality.** Because the metrics are computed from the live CSVs every run, the
   scorecard can't lie — it always reflects the current wiring (vs a stale hand-maintained doc).
5. **Growth stops accreting debt.** New canonical types reuse the closed verb set + are scored by
   the same matrix — so the model absorbs growth instead of forking (the original problem).

## 4. The KPI set (governance-scorecard aligned)

Mapped to the 4-perspective balanced scorecard (Data Governor / Dataworkers 12-KPI):

| Perspective | HCAM metric | Target |
|:---|:---|:---|
| Foundation | `MET-HOL-ENTITY-CATALOG-COVERAGE` (Zachman 6/6) | 6/6 |
| Data quality | `MET-HOL-ARTICULATION-WIRING-SCORE` (entity coverage %) | GREEN ≥80% |
| Process effectiveness | `MET-HOL-ARTICULATION-TRIPLE-ACTIVATION` (active/total) | trend up |
| Business value | orphans burned down per quarter (council) | trend down |

**Trend, not snapshot:** review monthly/quarterly; red-flag any metric below target for two
consecutive reviews (governance-scorecard rule).

## 5. Cross-references
- Model + gold layer: `CANONICAL_ARTICULATION_MODEL.md` · `validate_canonical_articulation.py --matrix`
- Council: `SOP-DATA_SEMANTIC_COUNCIL_001.md` · process `thi_data_dtp_semantic_council_001`
- Metrics: `METRICS_REGISTRY.csv` (MET-HOL-ARTICULATION-*) · area-governance v3 §7.5
- Regression: `reports/intent-ranked-regression-2026-06-06.md` (S-13)
- Decisions: `D-IH-95-A/B/C/D/E`
