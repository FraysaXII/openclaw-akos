# Initiative 25 — Topic Graph + Graph Projection + KM Scalability

**Folder:** `docs/wip/planning/25-hlk-topic-graph-and-km-scalability/`  
**Status:** **Closed (2026-04-29)** — UAT [`reports/uat-i25-topic-graph-and-km-scalability-20260429.md`](reports/uat-i25-topic-graph-and-km-scalability-20260429.md).  
**Authoritative Cursor plan:** `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md` §"Initiative 25".  
**Bootstrap dependency:** Initiative 23 (PROGRAM_REGISTRY) and Initiative 22 (forward layout convention).

> **Closure note (2026-04-29)** — All 11 phases (P0–P9) complete: P0+P1+P2+Pgraph in PR #19; P3+P4+P5+P6+P7+P8+P9 in the closure PR. **4 topics registered** in `TOPIC_REGISTRY.csv` (external_adviser_handoff, kirbe_billing_plane_routing, km_governance, enisa_evidence); Postgres mirror live; Neo4j `:Topic` projection extended with typed edges (`:DEPENDS_ON`, `:TOPIC_PARENT_OF`, `:RELATED_TO`, `:TOPIC_SUBSUMES`, `:UNDER_PROGRAM`); `render_topic_graph.py` emits the cross-program topic graph deterministically; **PMO hub stakeholder index auto-rendered** from canonical CSVs between BEGIN/END markers with sha256 drift detection; **ENISA backfill** ships a full Topic-Fact-Source bundle with `topic_enisa_evidence depends_on topic_external_adviser_handoff`; `.mmd`-first P0 discipline codified in `akos-planning-traceability.mdc`; `render_km_diagrams.py --all --dry-run` enables batch operations. New verify profiles: `render_pmo_hub_smoke`, `render_km_diagrams_batch_smoke`. Wikilinks adopted as secondary nav in `topic_external_adviser_handoff` companion (out-of-scope for `validate_hlk_vault_links.py` per D-IH-12).

## Outcome

Make topics first-class governed entities (separate CSV dimension, not just per-topic manifests), project them into Neo4j alongside `:Program` (Initiative 23 P-graph), and reframe ENISA + PMO hub as derived views via an auto-gen marker contract.

## Phase plan

| Phase | Purpose | Key deliverable |
|:-----:|:--------|:----------------|
| **P0** | Bootstrap initiative folder + 6 standard artifacts | This roadmap; decision log; asset classification; evidence matrix; risk register; reports/ |
| **P1** | KM contract extension | `HLK_KM_TOPIC_FACT_SOURCE.md` gains topic edges as **per-topic projections** that FK-resolve into `TOPIC_REGISTRY.csv`; manifest validator FK-resolves edges. |
| **P2** | Canonical TOPIC_REGISTRY (G-25-1) | `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv` + akos field contract + validator + Postgres mirror DDL applied via MCP |
| **Pgraph** | Neo4j Topic projection (G-25-3) | `:Topic` nodes + `:DEPENDS_ON` / `:TOPIC_PARENT_OF` / `:RELATED_TO` / `:TOPIC_SUBSUMES` / `:UNDER_PROGRAM` edges; sync + dry-run smoke |
| **P3** | Render topic graph deterministically | `scripts/render_topic_graph.py` emits `_assets/_meta/topic_graph.{mmd,png,svg}` from CSV |
| **P4** | Obsidian wikilink layer | `[[topic_id]]` adopted as **secondary** nav in topic companion `.md` (markdown links remain primary; out-of-scope for `validate_hlk_vault_links.py`) |
| **P5** | PMO hub auto-gen marker contract | `scripts/render_pmo_hub.py` emits stakeholder section between auto-gen markers; `render_pmo_hub_smoke` verify profile |
| **P6** | ENISA backfill (G-25-2 marker reuse) | `topic_enisa_evidence.{mmd,manifest.md,md,png,svg}` under `_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/`; reframe `ENISA_EVIDENCE_PACK_*.md` as derived view |
| **P7** | `.mmd`-first P0 rule | `akos-planning-traceability.mdc` updated per D-IH-13 |
| **P8** | `render_km_diagrams.py` batch + dry-run | `--all` + `--dry-run`; `render_km_diagrams_batch_smoke` verify profile |
| **P9** | Docs/rules sync + UAT + closure | ARCHITECTURE/USER_GUIDE/CHANGELOG/CONTRIBUTING; cursor-rules triggers; UAT report; closure |

## Operator approval gates

| Gate | Phase | What it covers |
|:----:|:-----:|:---------------|
| **G-25-1** | P2 | Apply `compliance.topic_registry_mirror` DDL via MCP `apply_migration` + seed via `service_role` `execute_sql` |
| **G-25-2** | P5 + P6 | Auto-gen marker contract reuse for PMO hub (`render_pmo_hub_smoke`) and ENISA derived view |
| **G-25-3** | Pgraph | Neo4j Topic projection extension applied (extends Initiative 23 P-graph schema; SKIPs when Neo4j unconfigured) |

## Decision references

- **D-IH-12** Topic graph SSOT — CSV is dimension authority, manifest is per-topic projection, Neo4j is graph projection. Drift = canonical wins per `PRECEDENCE.md`.
- **D-IH-13** `.mmd`-first P0 discipline — initiatives producing/modifying a Topic must commit `.mmd` source-of-truth in P0; consume-only initiatives exempt.
- **D-IH-18** Neo4j as graph DDL surface — extends Initiative 07 baseline + Initiative 23 `:Program` extension.

## Verification matrix

- `py scripts/validate_hlk.py` (each phase touching CSVs)
- `py scripts/validate_topic_registry.py` (P2+)
- `py scripts/validate_hlk_km_manifests.py` (FK-resolves topic edges into TOPIC_REGISTRY post-P1)
- `py scripts/sync_hlk_neo4j.py --dry-run` (Pgraph parity assert with `:Topic`)
- `py scripts/verify.py render_pmo_hub_smoke` (P5 — operator runs after PMO hub auto-render)
- `py scripts/verify.py render_km_diagrams_batch_smoke` (P8 — batch render)
- MCP `execute_sql` row-count probe for `compliance.topic_registry_mirror` after apply
- `py scripts/verify.py compliance_mirror_drift_probe` (operator-pasted; ensures topic_registry_rows in parity)

## Out of scope

- Re-architecting `process_list.csv` per-plane (Initiative 27, slot reserved).
- Auto-generating EVERY vault MD (only PMO hub + ENISA in this initiative; further auto-renders per-initiative).
- Promoting Neo4j from optional to mandatory in the agent ladder (D-IH-18 trigger; Initiative 26 P0 trigger template).

## Cross-references

- [decision-log.md](decision-log.md)
- [asset-classification.md](asset-classification.md)
- [evidence-matrix.md](evidence-matrix.md)
- [risk-register.md](risk-register.md)
- Initiative 23 (program registry — Topic projection joins to `:Program`): [`23-hlk-program-registry-and-program-2/`](../23-hlk-program-registry-and-program-2/master-roadmap.md)
- Initiative 22a wave-2 bootstrap: [`22a-i22-post-closure-followups/`](../22a-i22-post-closure-followups/master-roadmap.md)
