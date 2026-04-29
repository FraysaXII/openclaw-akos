# UAT — Initiative 25 (Topic Graph + Graph Projection + KM Scalability)

**Date**: 2026-04-29  
**Operator approvals captured**:

- **G-25-1** — `compliance.topic_registry_mirror` DDL applied via MCP `apply_migration` + 4 rows seeded (`topic_external_adviser_handoff`, `topic_kirbe_billing_plane_routing`, `topic_km_governance`, `topic_enisa_evidence`).
- **G-25-2** — Auto-gen marker contract reuse: `render_pmo_hub.py` (PMO hub stakeholder index) and ENISA derived view both employ the BEGIN/END marker contract with sha256 drift detection.
- **G-25-3** — Neo4j Topic projection extension: dry-run parity assert PASS (4 topics + 7 topic-side edges); live Bolt apply on next operator-driven sync.

## Verification matrix

| Check | Result |
|:------|:------:|
| `py scripts/validate_hlk.py` (incl. PROGRAM_REGISTRY + PROGRAM_ID_CONSISTENCY + TOPIC_REGISTRY) | **PASS** |
| `py scripts/validate_topic_registry.py` | **PASS** (4 topics, cycle-free) |
| `py scripts/validate_hlk_km_manifests.py` | **PASS** (all manifest topic_ids FK-resolve into TOPIC_REGISTRY.csv) |
| `py scripts/validate_hlk_vault_links.py` | **PASS** (wikilinks correctly out-of-scope per D-IH-12) |
| `py -m pytest tests/test_compose_adviser_message.py tests/test_wave2_backfill.py tests/test_validate_program_id_consistency.py tests/test_probe_compliance_mirror_drift.py -q` | **44/44 PASS** |
| `py scripts/sync_hlk_neo4j.py --dry-run` | **PASS** — `programs=12 topics=4 edges=2256 (incl. 14 program-side, 7 topic-side)` |
| `py scripts/render_topic_graph.py` | **PASS** — emits `_assets/_meta/topic_graph.{mmd,png,svg}`; PNG sha256 `d128962c45d674ee...`; clusters by program_id |
| `py scripts/verify.py render_pmo_hub_smoke` | **PASS** — section_id=pmo_stakeholder_index_v1; body sha256 matches |
| `py scripts/verify.py render_km_diagrams_batch_smoke` | **PASS** — discovers 4 .mmd sources (topic_graph, topic_external_adviser_handoff, topic_kirbe_billing_plane_routing, topic_enisa_evidence) |
| `py scripts/verify.py compliance_mirror_drift_probe` | **PASS** — 9/9 mirrors at parity (topic_registry_rows = 4 = CSV) |
| MCP `execute_sql` row-count probe (`compliance.topic_registry_mirror`) | **4 rows** matching CSV |

## Phase closure

- **P0** — Initiative folder + 6 standard artifacts (PR #19).
- **P1** — KM contract extension: `HLK_KM_TOPIC_FACT_SOURCE.md` + `validate_hlk_km_manifests.py` FK-resolution (PR #19).
- **P2** — TOPIC_REGISTRY.csv + akos contract + validator + Postgres mirror via MCP (PR #19).
- **Pgraph** — Neo4j `:Topic` projection + constraints + indexes + sync (PR #19).
- **P3** — `scripts/render_topic_graph.py` emits `_assets/_meta/topic_graph.{mmd,png,svg}` (this PR).
- **P4** — Wikilinks adopted in `topic_external_adviser_handoff.md` companion (this PR).
- **P5** — `scripts/render_pmo_hub.py` + auto-gen marker contract; `TOPIC_PMO_CLIENT_DELIVERY_HUB.md` stakeholder index now auto-rendered between BEGIN/END markers; `render_pmo_hub_smoke` verify profile (this PR).
- **P6** — ENISA backfill: `topic_enisa_evidence` under `_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/` with `.mmd` + manifest + companion + rendered PNG/SVG; topic edge `depends_on=topic_external_adviser_handoff` registered in CSV + Neo4j projection (this PR).
- **P7** — `.mmd`-first P0 rule added to `akos-planning-traceability.mdc` (this PR).
- **P8** — `scripts/render_km_diagrams.py --all` batch + `--dry-run`; `render_km_diagrams_batch_smoke` verify profile (this PR).
- **P9** — UAT report (this document); planning README updated; closure note in master roadmap.

## Manual review items

- **Topic graph aesthetic** — operator may wish to refine the auto-rendered `topic_graph.{png,svg}` layout (subgraph clustering by program_id is functional but could be tuned per-deliverable).
- **PMO hub stakeholder load** — auto-rendered `open_questions` count column relies on `ADVISER_OPEN_QUESTIONS.csv` `poi_ref_id` / `goi_ref_id` columns; operator confirms join fidelity at next PMO review cadence.
- **ENISA derived view reframe** — Initiative 25 P6 ships the topic asset and TOPIC_REGISTRY row; the existing `ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md` continues to carry operator-authored narrative. A future operator pass may insert auto-gen markers around the data-driven sections of that vault doc; the marker contract is ready (same as PMO hub).

## Closure

Initiative 25 is **complete**: all 11 phases (P0–P9) shipped across PR #19 and this PR. Topic registry is canonical; PMO hub is auto-rendered; ENISA is backfilled as a Topic-Fact-Source bundle; `.mmd`-first discipline is codified in cursor rules.

## Cross-references

- Plan: `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md`
- PRs: #19 (P0–Pgraph), this branch's PR (P3–P9 + closure)
- Decision log: [`decision-log.md`](../decision-log.md) (D-IH-12 / D-IH-13 / D-IH-18 / D-IH-25-A / D-IH-25-B)
- Risk register: [`risk-register.md`](../risk-register.md)
- Drift probe artifact: `artifacts/probes/mirror-drift-20260429.json` (gitignored)
