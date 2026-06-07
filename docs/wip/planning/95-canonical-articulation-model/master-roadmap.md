---
initiative: INIT-OPENCLAW_AKOS-95
title: Canonical Articulation Model (the Singularity)
owner_role: Data Governance Office (HCAM doctrine home; Data-federated per D-IH-95-D)
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
existing Neo4j projection, owned **Data-federated** via the Semantic Council (`D-IH-95-D` — *not* a
new Knowledge Manager role), and used to re-frame what "a complete area" means.

**Why now.** The operator's inception-era unsolved problem; surfaced by I94's sub-folder=role +
placement-integrity work. Articulation-first because Operations/Legal/Envoy (I94 P3/P5/P6) cannot
wire roles↔processes correctly until the verbs + valid triples exist.

## Phase map

| Phase | Scope | Key deliverables | Gate |
|:---|:---|:---|:---|
| **P0** | Research + inception (DONE) | 115-source ledger, brainstorm, master-synthesis, D-IH-95-A, I95 scaffold | operator (this turn) |
| **P1 (=B)** | **Relationship-registry SSOT** | `CANONICAL_RELATIONSHIP_REGISTRY.csv` (entity catalog ~30 types + ~10 verbs + valid `(src,verb,tgt)` triples) + Pydantic `akos/hlk_canonical_articulation.py` + `scripts/validate_canonical_articulation.py` + tests | D-IH-95-B (schema + verb set review) |
| **P2 (=C)** | **Neo4j unify** | edge-rename map (collapse `*_PARENT_OF`→`composition`); verb-typed edges; derivation queries answering the 5 competency questions; parity check vs CSV SSOT | D-IH-95-C (edge map; bidirectional w/ graph rework) |
| **P3 (=E.1)** | **HCAM doctrine home (Data, federated)** | publish HCAM as a **Data-Architecture canonical** (sibling to `SEMANTIC_LAYER.md`); stand up the **Semantic Council** (CDO chair + 1 rep/area); federated area-authorship model; cursor rule + skill. *No new role* (uses Data Architect / Data Governance Office / Data Steward / AI Engineer). Couple with **I91**. | D-IH-95-E (ownership ratify) |
| **P4 (=E.2)** | **Area-completeness v3** | re-express the 16-component model as required HCAM triples + articulation-completeness definition; re-prove Data/Finance/People don't regress | D-IH-95 (area model v3 review) |
| **P5 (=E.3)** | **Repo-wide FK→verb mapping** ("the all-out of D") | map every CSV FK column + canonical type to its ArchiMate element/verb; populate triples; the DTO is queryable e2e | per-tranche |
| **P6** | **Fold-in concrete items** | Q2 Lead simplification (keep Data Governance Office) + Q3 Marketing ghost-folder merge/delete-empties — both are HCAM placement work | canonical-CSV gate (Q2) |
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

## Round-2 execution lanes (D-IH-95-G, ratified 2026-06-07)

The 9-decision Round-2 batch. **EG-1 / R2-04 / R2-09 executed at ratification.** The rest are
sequenced lanes (each is a tranche with its own gate); run **value-first**, but R2-06 burns down
**by area in equal slices** per operator override.

| Lane | Scope | First concrete step | Gate |
|:---|:---|:---|:---|
| **L1 — Supabase EG-2..5** (R2-03) | close the 11 ungoverned + 7 partial modules: legacy drop + RLS, then edge-fn / cron / extension / RLS-posture / API-exposure / FDW registries | EG-2 critical: `SUPABASE_API_EXPOSURE.md` (config-vs-hosted drift) + legacy-drop inventory | operator (DDL drop + RLS = data-loss/SOC) |
| **L2 — Capability de-densify** (R2-01) | collapse `CAPABILITY_REGISTRY` 1119→~50-150 stable map; activate `realization` (TRP-006/014); processes realize N:N; then weekly cron rating of *active* capabilities | draft the ~150-capability target map (cluster the 1119 by capability, not process) for operator review | canonical-CSV gate (the collapse) |
| **L3 — FK→verb tranches** (R2-05) | "all-out of D" but per-registry tranches: map every CSV FK column → ArchiMate verb; populate triples; DTO queryable e2e | tranche order = by registry, highest-articulation-value first (process_list, baseline_org, capability, metrics, ops) | per-tranche (additive) |
| **L4 — Orphan burn-down** (R2-06) | raise `--matrix` AMBER 69%→GREEN; **by area, equal slices** | next equal slice = activate the `planned` triples for one area per pass via the Semantic Council | Semantic Council disposition |
| **L5 — IntelligenceOps + topics** (R2-07) | IntelligenceOps register → **Research**; migrate `docs/wip/intelligence` into a **governed topic structure** (rework the minted-but-ungoverned `TOPIC_REGISTRY`) | inventory `TOPIC_REGISTRY` + the wip/intelligence corpus; design the topic taxonomy + migration map | operator (taxonomy sign-off) |
| **L6 — biz-strategy re-home** (R2-08) | `PRICING_MODEL` / `UNIT_ECONOMICS` → **Finance**; GTM theses → **Marketing/Strategy**; placement-integrity fix | locate the artifacts under `Operations/PMO/business-strategy/` + map per-row target | placement-integrity (file moves + ref updates) |

**Drift-prevention backbone (R2-04):** the 40+ open-thread inventory is the **backlog SSOT**; index
drift fixed this commit. **Neo4j (R2-09):** keep-alive workflow live; budget ~$65/mo Professional.

## Cross-references
- Round-2 synthesis: [`../intelligence/canonical-articulation-model-2026-06-05/round2-research-synthesis-2026-06-06.md`](../../intelligence/canonical-articulation-model-2026-06-05/round2-research-synthesis-2026-06-06.md)
- Supabase ecosystem governance: `docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_ECOSYSTEM_GOVERNANCE.md`
- Research: [`../intelligence/canonical-articulation-model-2026-06-05/master-synthesis.md`](../../intelligence/canonical-articulation-model-2026-06-05/master-synthesis.md)
- Decisions: [`decision-log.md`](./decision-log.md) (D-IH-95-A/B/C/D/E ratified; D-IH-95-G Round-2 batch ratified 2026-06-06; D-IH-95-F graph cutover gated on Neo4j)
- Parent: I94 area model v2 (`docs/wip/planning/94-area-architecture-and-completeness-v2/`)
- Subject: `akos/hlk_graph_model.py`, `baseline_organisation.csv`, `process_list.csv`
