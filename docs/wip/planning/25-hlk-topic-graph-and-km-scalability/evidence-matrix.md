# Initiative 25 — Evidence Matrix

## Phase → evidence map

| Phase | Deliverable | Source / evidence |
|:-----:|:-----------|:------------------|
| P0 | Initiative folder bootstrap | This roadmap; decision log; asset classification; risk register |
| P1 | KM contract extension | Existing `HLK_KM_TOPIC_FACT_SOURCE.md`; Wave-2 plan §"D-IH-12" |
| P2 | TOPIC_REGISTRY canonical | Existing topics in `_assets/` (Initiative 21 + 22 + 23 P6 KIR topic); Initiative 23 PROGRAM_REGISTRY pattern |
| P2 | Postgres mirror DDL | Initiative 21 P7 + Initiative 23 P2 precedents (DDL via MCP `apply_migration`; ledger parity rename) |
| Pgraph | Neo4j Topic projection | Initiative 23 P-graph `build_program_graph` pattern; existing `akos/hlk_graph_model.py` + `akos/hlk_neo4j.py` |
| P3 | Topic graph render | Existing `scripts/render_km_diagrams.py` for Mermaid → PNG/SVG; new aggregator reads CSV |
| P4 | Wikilinks | Wave-2 plan §"D-IH-12" — out of scope for `validate_hlk_vault_links.py` |
| P5 | PMO hub auto-render | Existing `TOPIC_PMO_CLIENT_DELIVERY_HUB.md` (operator hand-maintained today); new auto-gen marker contract |
| P6 | ENISA backfill | Existing `ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`; Initiative 22 P5 mermaid render pipeline |
| P7 | `.mmd`-first rule | Existing `akos-planning-traceability.mdc`; D-IH-13 phrasing |
| P8 | Batch render | Existing `scripts/render_km_diagrams.py` (single-file mode); add `--all` + `--dry-run` |
| P9 | UAT report | All preceding evidence + final validator outputs |

## Cross-references

- Plan: `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md` §"Initiative 25"
- Initiative 23 master roadmap (PROGRAM_REGISTRY + Neo4j P-graph baseline)
- Initiative 22a (operator-answers YAML — no Section for I25 today; topics are agent-discoverable from `_assets/`)
- Initiative 21 (ADVOPS plane + topic_external_adviser_handoff seed)
