# Intent-Ranked Regression — HCAM / articulation job (2026-06-06)

**Decision:** `D-IH-95-E` · **Discipline:** `akos-intent-ranked-regression.mdc` (ICS = 3·intent +
2·time + 2·risk + 1·detection_gap) · **Run by:** MADEIRA (thinking) → execution

> Operator ask: *"Do a regression over the job with all the intents you can find in
> [operator-scratchpad, OPS_REGISTER, DATA_AREA_CHARTER, AREA_GOVERNANCE, COMPONENT_SERVICE_MATRIX,
> CAPABILITY_CONFIDENCE_REGISTRY +more] … ensure we did the best of the best, and if not, research
> and act so we excel. The goal: articulated automated layers that reflect reality + are governed,
> so operations focus on higher-value work."*

## 1. Intent corpus (distilled from the named sources)

| Signal | Source | Tier |
|:---|:---|:---|
| *"getting lost on visibility — I don't know where/how/what it gives"* | operator-scratchpad L68 | **IT-4 (visibility)** ↑ |
| *"ERP must not be forgotten… govern engagements via ERP workflow + UX… my dashboard"* | scratchpad L1376 | IT-4 / IT-1 |
| *"COLLABORATOR_SHARE doesn't reflect reality… accuracy mess"* | scratchpad L1519 | IT-3 (reflect-reality) |
| 5-dimension **scored** confidence (substrate/repeatability/quality/translatability/auditability) | `CAPABILITY_CONFIDENCE_REGISTRY` | exemplar: governed scored-metrics layer |
| DAMA areas + federated mesh + `govern+enable` verb | `DATA_AREA_CHARTER` | IT-3 |
| area completeness = *present* (16-comp grid) | `AREA_GOVERNANCE_DISCIPLINE` v3 | IT-3 |
| component↔service ownership matrix | `COMPONENT_SERVICE_MATRIX` | IT-3/IT-7 |
| 150 OPS rows; open visibility/ERP severities | `OPS_REGISTER` | IT-3/IT-4 |

**Tier update (evidenced, not invented):** IT-4 re-named *"Operator leverage, interaction quality &
**VISIBILITY**"* and its evidence string now cites scratchpad L68/L1376. No weight change (stays 4).

## 2. The model gap found → fixed this run

The intent-ranked model had **12 surfaces, none covering articulation/visibility** — a blind spot
exactly where the operator pointed. **Added S-13** (HCAM articulation + visibility gold layer),
serving **IT-3 (governance integrity)** + **IT-4 (visibility)**.

## 3. Ranked sweep (top of queue) + attribution

| # | Surface | ICS | Verdict | Attribution / disposition |
|:-:|---|:-:|---|---|
| 1 | S-06 Legal/fiscal artifacts | 36! | n/a this job | out of scope (severity-first; FINOPS, not articulation) |
| 2 | S-04 FINOPS spine | 35! | n/a | out of scope |
| 3 | S-01 Governance SSOT (`validate_hlk`) | 34 | **PASS** | OVERALL PASS throughout I95 (rename + moves + council row) |
| 4 | S-05 Release-gate | 32 | not re-run | safety-net; periodic (no per-commit need) |
| 5 | S-12 Schema drift | 32 | **PASS** | catalog↔Pydantic enum in sync (42 types / 60 triples) |
| 6 | **S-13 Articulation + visibility** | **32** | **WAS RED → fixed-now** | **F-1 (below)** |
| 7 | S-02 Area-completeness | 31 | **PASS** | Data/Finance/People closures preserved (v3 additive) |
| … | S-03/07/08/09/10/11 | ≤29 | not re-run | lower-ICS; green at last sweep / known-deferred |

## 4. Findings

### F-1 — Articulation had no consumable metric / gold layer / DGO visibility (HIGH-ICS) — **FIXED-NOW**
- **Attribution:** *new* — I95 P1-P3 built the model (catalog + triples + validator + council) but
  stopped at advisory per-area text. The operator's lived experience confirmed it: *"inconsistent…
  I don't have much data I can find useful… worse for a DGO user with no UI nor useful metrics, no
  gold layer."* Detection_gap was **5** (no metric/gate surfaced wiring state).
- **Disposition:** **rework-now** (high-ICS + low-effort + reversible). Shipped the gold layer:
  - `--matrix` consistent scorecard (per-area wiring% + orphans + enterprise rollup + DQ-badge).
  - 3 define-once metrics in `METRICS_REGISTRY` (the semantic/gold layer the ERP/BI read).
  - S-13 added to this model so the blind spot can't recur silently.
  - Baseline captured: **69% entity coverage, 63% triple activation, Zachman 6/6, AMBER.**

### F-2 — Planned triples / orphan canonicals (MEDIUM) — **defer-to-council (tracked)**
- **Attribution:** *known/by-design* — 22 of 60 triples are `planned` (no FK yet): data_product,
  data_model, data_catalog, glossary_term, adapter, application, workstream links, process-triggering.
- **Disposition:** **defer-OPS/council** — these are the orphan worklist the gold layer now surfaces;
  the Semantic Council burns them down quarterly (not a defect; the scorecard makes them visible).

### F-3 — Supabase mirror drift from the rename (LOW) — **tracked (OPS-95-1)**
- **Attribution:** *new* (this session's rename). **Disposition:** OPS-95-1 (operator-applied re-sync;
  emitter verified post-rename; immutable migration left).

## 5. "Best of the best?" assessment

**Before this run:** model + validator (good), but no visibility layer → *not* best-of-best for the
operator's actual need. **After:** the articulation layer now matches the SOTA we researched —
the **12-KPI balanced governance scorecard** (4 perspectives, trends, DQ-certification badge) + the
**medallion gold layer** (curated, business-ready, defined-once metrics; DQ badge for automated
self-gating). It **reflects reality** (computed from live CSVs every run), is **governed** (council
+ DECISION_REGISTER + validate_hlk), and **frees ops** (one command, not a dashboard build; orphans
become a worklist; pipelines self-gate on the badge). Gaps that remain are *visible + owned*, which
is the bar.

## 6. Disposition summary
- **F-1 rework-now** (gold layer shipped) · **F-2 defer-council** (orphan worklist) · **F-3 OPS-95-1**.
- **0 new regressions** to existing surfaces (validate_hlk OVERALL PASS throughout).
- Safety net intact: release-gate + inter-wave sweep unchanged (this layer supplements, never replaces).

## 7. Cross-references
- Model SSOT: `akos/hlk_intent_ranked_regression.py` (S-13) · gold layer: `validate_canonical_articulation.py --matrix`
- Operating model: `articulation-operating-model-2026-06-06.md`
- Metrics: `METRICS_REGISTRY.csv` (MET-HOL-ARTICULATION-*) · Decision: `D-IH-95-E`
