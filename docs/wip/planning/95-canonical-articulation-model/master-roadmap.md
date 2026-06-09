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

## P95-GOV universal canonical governance wave (2026-06-09)

Execution wave under I95 (charter: [`reports/universal-canonical-governance-charter-2026-06-09.md`](reports/universal-canonical-governance-charter-2026-06-09.md); plan: [`reports/p95-gov-wave-plan-2026-06-09.md`](reports/p95-gov-wave-plan-2026-06-09.md)).

| Packet | Status | Base commit |
|:---|:---|:---|
| P95-GOV-1 — Registry mint | **closed** | `30ed6d8` |
| P95-GOV-2 — HCAM quintet index A | **closed** | (GOV-2 tranche) |
| P95-GOV-3 — Registry-driven CI | **closed** | (GOV-3 tranche) |
| P95-GOV-4 — Index backfill B | **closed** | (GOV-4 tranche) |
| P95-GOV-5 — Mirror emit gap | **closed** | `ba95dd1` |
| P95-GOV-6 — Plane-1 hardening | **closed** | `8746715` |
| P95-GOV-7 — Forward-charter DDL | **closed** | `14f8521` |
| P95-GOV-8 — Closure UAT | **closed** | PASS-WITH-FOLLOWUP — [`uat-universal-canonical-governance-2026-06-09.md`](reports/uat-universal-canonical-governance-2026-06-09.md) |

**Follow-up (operator gate):** prod mirror apply for GOV-5 + GOV-7 **APPLIED** 2026-06-09 — [`reports/operator-mirror-apply-execution-2026-06-09.md`](reports/operator-mirror-apply-execution-2026-06-09.md) (migration drift repair + DDL push + 171-batch DML; row-count parity **PASS** 12/12). Walkthrough: [`reports/operator-mirror-apply-walkthrough-2026-06-09.md`](reports/operator-mirror-apply-walkthrough-2026-06-09.md). Neo4j CQ1–5 **BLOCKED-AUTH** (retry 2026-06-09) — [`reports/i95-neo4j-cq-uat-2026-06-09.md`](reports/i95-neo4j-cq-uat-2026-06-09.md). L3 TRP-030/036 ratification: [`reports/l3-trp-030-036-ratification-2026-06-09.md`](reports/l3-trp-030-036-ratification-2026-06-09.md) — both stay **planned**. I95 INIT remains **active** for Round-2 lanes (L1–L6).

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
| **L2 — Capability de-densify** (R2-01; params **ratified D-IH-95-H**) | collapse 1,119 **area-by-area** (count organic, not a fixed band); evict ~27 code-symbols→`COMPONENT_PRIMITIVE_REGISTRY`; merge cross-entity dups→one bearer-agnostic capability; move `bearer_class`→realization edge (TRP-006/038); add `capability_tier`; activate TRP-014; then **hybrid weekly-cron** rating (~8/wk + event + value-tier) | schema pre-step (`bearer_class`→edge + `capability_tier` col) → then **per-domain slice 1** | canonical-CSV gate per slice |
| **L3 — FK→verb tranches** (R2-05) | "all-out of D" but per-registry tranches: map every CSV FK column → ArchiMate verb; populate triples; DTO queryable e2e | tranche order = by registry, highest-articulation-value first (process_list, baseline_org, capability, metrics, ops) | per-tranche (additive) |
| **L4 — Orphan burn-down** (R2-06) | raise `--matrix` AMBER 69%→GREEN; **by area, equal slices** | next equal slice = activate the `planned` triples for one area per pass via the Semantic Council | Semantic Council disposition |
| **L5 — Topics + IntelligenceOps** (R2-07; **ratified D-IH-95-H**) | chassis ~80% built → **govern+bind+curate** (not build): **T1 schema** = orthogonal `subject_kind` facets + binding cols (`working_area_path`/`knowledge_index_path`/`steward_role`/`physical_model`) + Pydantic + mirror sync; **T2 data** = bind folders + **physical move** `wip/intelligence`→topic-keyed tree (authorized) + mint 5 missing + triage 11 stranded + **repo-wide scattered-topic sweep**; activate **KM Officer** steward | scattered-topic inventory (dispatched) → **T1 schema tranche** | canonical-CSV gate per tranche |
| **L6 — biz-strategy re-home** (R2-08) | `PRICING_MODEL` / `UNIT_ECONOMICS` → **Finance**; GTM theses → **Marketing/Strategy**; placement-integrity fix | locate the artifacts under `Operations/PMO/business-strategy/` + map per-row target | placement-integrity (file moves + ref updates) |

**Drift-prevention backbone (R2-04):** the 40+ open-thread inventory is the **backlog SSOT**; index
drift fixed this commit. **Neo4j (R2-09):** keep-alive workflow live; **2026 spend posture** per **D-IH-95-L** + **D-IH-95-M** — F6 Free restore primary; Professional deferred; Startup + EIC tracks parallel; self-hosted ~$30/mo post-credits default.

## Master execution queue (PMO pointer — ratified 2026-06-09, D-IH-95-M)

Authoritative operator-facing sweep: [`reports/i95-pmo-status-sweep-2026-06-09.md`](reports/i95-pmo-status-sweep-2026-06-09.md). FQ closure record: [`reports/i95-fq2-ratification-2026-06-09.md`](reports/i95-fq2-ratification-2026-06-09.md).

| Step | Lane | Gate |
|:---|:---|:---|
| 1 | **F6 Neo4j restore** (F6-R0..R7) | Probe exit 0; vault backup; no `.backup` in git |
| 2 | **Probe + CQ UAT** | `neo4j_connectivity_probe.py`; `run_cq_uat.py` PASS |
| 3 | **Self-hosted spike charter** | I07 env contract preserved; ~$30/mo TCO note |
| 4 | **EIC Pre-Accelerator screen + Open LOI draft** | FQ-1 D parallel track |
| 5 | **Neo4j Startup application pack** | Eligibility + use-case A/B narrative |
| 6 | **I95 open lanes** | L3 bundle C + tranche-5 (10 active triples still unbound — see regression F-11) · EG-3 registries · orphan `--matrix` · full `pre_commit` |

**Current blockers:** Neo4j **BLOCKED-AUTH** until F6-R3..R4 complete (`wrong_password_or_user` / GHA `42NFF`). GOV wave **closed**; prod mirror **APPLIED** + parity **PASS** @ 2026-06-09.

## Cross-references
- Round-2 synthesis: [`../intelligence/canonical-articulation-model-2026-06-05/round2-research-synthesis-2026-06-06.md`](../../intelligence/canonical-articulation-model-2026-06-05/round2-research-synthesis-2026-06-06.md)
- Supabase ecosystem governance: `docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_ECOSYSTEM_GOVERNANCE.md`
- Research: [`../intelligence/canonical-articulation-model-2026-06-05/master-synthesis.md`](../../intelligence/canonical-articulation-model-2026-06-05/master-synthesis.md)
- Decisions: [`decision-log.md`](./decision-log.md) (D-IH-95-A/B/C/D/E ratified; D-IH-95-G Round-2 batch 2026-06-06; D-IH-95-H L2+L5 execution params 2026-06-07; D-IH-95-F graph cutover gated on Neo4j)
- Parent: I94 area model v2 (`docs/wip/planning/94-area-architecture-and-completeness-v2/`)
- Subject: `akos/hlk_graph_model.py`, `baseline_organisation.csv`, `process_list.csv`
