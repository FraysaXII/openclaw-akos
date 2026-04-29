# Initiative 23 — Evidence Matrix

Tracks the source artifacts behind each phase deliverable.

## Phase → evidence map

| Phase | Deliverable | Source / evidence |
|:-----:|:-----------|:------------------|
| P0 | Initiative folder bootstrap | This roadmap; decision log (D-IH-8/9/16/18/23-A); asset classification; risk register; reports/ |
| P0.5 | Tier-3 cell defaults in YAML | Wave-2 plan T2 tier definition; `process_list.csv` rows for the 11 projects; existing process descriptions |
| P1 | `PROGRAM_REGISTRY.csv` 12 rows | Operator-answers YAML Section 1 (Tier-1/2 + Tier-3 defaults); `process_list.csv` `item_granularity = project` rows |
| P1 | akos field contract | `akos/hlk_goipoi_csv.py`, `akos/hlk_finops_counterparty_csv.py` patterns |
| P1 | validator | `scripts/validate_goipoi_register.py` patterns |
| P2 | Postgres mirror DDL | `supabase/migrations/20260429081728_i21_compliance_goipoi_register_mirror.sql` (Initiative 21 P7 reference); RLS policies; index pattern |
| P2 | Mirror apply via MCP | user-supabase MCP `apply_migration` + `execute_sql` (Initiative 22 P7 precedent) |
| Pgraph | Neo4j projection | `akos/hlk_graph_model.py` existing `build_hlk_csv_graph` + `EdgeType` + `GraphLabel`; `akos/hlk_neo4j.py` `_ensure_constraints`; `scripts/sync_hlk_neo4j.py` builder pass |
| Pgraph | Edge naming | Wave-2 plan §"Graph projection (Neo4j) — schema extension reference" |
| P3 | Cross-asset validator | `GOI_POI_REGISTER.csv` `program_id` column + `ADVISER_OPEN_QUESTIONS.csv` + `FOUNDER_FILED_INSTRUMENTS.csv` + `_assets/<plane>/<program_id>/` paths |
| P4 | Drift probe | Initiative 22 P7 row-count probe pattern (MCP `execute_sql`) |
| P5 | Glossary | Wave-2 plan §"Cross-program glossary"; existing `docs/GLOSSARY.md` |
| P6 | KiRBe role roots | Wave-2 plan §"KiRBe truth (for I23 program-2 onboarding)" — process_list rows `env_tech_prj_2`, `env_tech_ws_k1`, `thi_data_dtp_274/275`, `env_tech_dtp_269`, `thi_finan_dtp_261`, `env_tech_dtp_285` |
| P7 | Docs sync | `akos-docs-config-sync.mdc` triggers |
| P8 | UAT report | All preceding evidence + final validator outputs |

## Decision evidence

- **D-IH-8 program_id PRJ-HOL-style** — Wave-2 plan §"Decisions (D-IH-8..D-IH-18)"; preserves path stability across `process_list.csv` reorganizations.
- **D-IH-9 forward-reference policy** — Wave-2 plan §"D-IH-9 (REVISED)"; cycle-detection cost analysis.
- **D-IH-16 KiRBe duality** — `process_list.csv` (KiRBe rows in Tech/Data/Finance/People); `v3.0/index.md` ("Ingest as a source"); `akos-holistika-operations.mdc` §"Schema responsibilities (DAMA)" (kirbe.* product plane).
- **D-IH-18 Neo4j as graph DDL surface** — Initiative 07 master roadmap (allowlisted Cypher; CSV SSOT; rebuildable read index); existing `:PARENT_OF` collision avoided by `:PROGRAM_PARENT_OF` naming.
- **D-IH-23-A Agent defaults** — Wave-2 plan T2 tier definition; reviewable diff in operator-answers YAML.

## Cross-references

- Plan: `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md`
- Initiative 22 closure: `docs/wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md`
- Initiative 22a bootstrap: `docs/wip/planning/22a-i22-post-closure-followups/master-roadmap.md`
- Initiative 07 (Neo4j foundation): `docs/wip/planning/07-hlk-graph-stack/master-roadmap.md` (existing)
- Cursor rules: `akos-governance-remediation.mdc`, `akos-holistika-operations.mdc`, `akos-planning-traceability.mdc`, `akos-docs-config-sync.mdc`, `akos-adviser-engagement.mdc`
