# Initiative 25 — Asset Classification

## Canonical (edit-here-first)

| Asset | Path | Owner / Notes |
|:------|:-----|:--------------|
| Topic registry | `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv` (P2) | Cross-cutting dimension; `topic_id`, `program_id` (FK to PROGRAM_REGISTRY or `shared`), edges (parent/depends/related/subsumes), manifest_path |
| akos field contract | `akos/hlk_topic_registry_csv.py` (P2) | Backwards-compatible add |
| Validator | `scripts/validate_topic_registry.py` (P2) | Cycle detection (parent + depends_on), uniqueness, FK to PROGRAM_REGISTRY/baseline_org, `manifest_path` exists |
| KM contract extension | `HLK_KM_TOPIC_FACT_SOURCE.md` (P1) | Updated to require manifest edges FK-resolve into TOPIC_REGISTRY |
| Topic graph render | `scripts/render_topic_graph.py` (P3) | Reads CSV → emits `_assets/_meta/topic_graph.{mmd,png,svg}` |
| PMO hub auto-render | `scripts/render_pmo_hub.py` (P5) | Reads GOI/POI + disciplines + PROGRAM_REGISTRY + open_questions; emits stakeholder section between auto-gen markers; idempotent |
| ENISA topic asset | `_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/topic_enisa_evidence.{mmd,manifest.md,md,png,svg}` (P6) | Reuses Initiative 22 forward-layout convention |
| `.mmd`-first rule update | `.cursor/rules/akos-planning-traceability.mdc` (P7) | D-IH-13 phrasing |
| Batch render | `scripts/render_km_diagrams.py` `--all` + `--dry-run` (P8) | Backwards-compatible single-file mode preserved |

## New tooling extensions

| Asset | Path | Notes |
|:------|:-----|:------|
| Sync flag | `scripts/sync_compliance_mirrors_from_csv.py --topic-registry-only` (P2) | Mirror UPSERT emit |
| Mirror DDL staging | `scripts/sql/i25_phase1_staging/<ts>_i25_compliance_topic_registry_mirror_{up,rollback}.sql` (P2) | RLS deny anon/authenticated; service_role only |
| Mirror DDL migration | `supabase/migrations/<ts>_i25_compliance_topic_registry_mirror.sql` (P2) | Filename matches remote `schema_migrations` ledger |
| Verify profile (PMO hub) | `config/verification-profiles.json` `render_pmo_hub_smoke` (P5) | `--check-only`; FAIL on `AUTOGEN_DRIFT_DETECTED` |
| Verify profile (batch render) | `config/verification-profiles.json` `render_km_diagrams_batch_smoke` (P8) | New |
| Graph projection extension | `akos/hlk_graph_model.py` `build_topic_graph()` (Pgraph) | `:Topic` nodes + edges; mirrors `build_program_graph` style |
| Graph constraints | `akos/hlk_neo4j.py` (Pgraph) | `Topic.topic_id IS UNIQUE`; range indexes on lifecycle/class/plane |
| Graph sync | `scripts/sync_hlk_neo4j.py` (Pgraph) | Adds Topic builder pass after Program/Role/Process |

## Mirrored / derived (do not hand-edit)

| Asset | Path | Sync direction |
|:------|:-----|:---------------|
| `compliance.topic_registry_mirror` | Live Supabase (P2) | `TOPIC_REGISTRY.csv` → MCP `apply_migration` (DDL) + `execute_sql` (DML, `service_role`) |
| Neo4j `:Topic` nodes + edges | Neo4j Community (Pgraph) | `TOPIC_REGISTRY.csv` → `sync_hlk_neo4j.py` rebuild |
| `_assets/_meta/topic_graph.{mmd,png,svg}` | Repo (P3) | `TOPIC_REGISTRY.csv` → `render_topic_graph.py` |
| Stakeholder section in `TOPIC_PMO_CLIENT_DELIVERY_HUB.md` | Repo (P5) | GOI/POI + disciplines + PROGRAM_REGISTRY + open_questions → `render_pmo_hub.py` (between auto-gen markers) |
| ENISA evidence pack derived view | Repo (P6) | `_assets/advops/.../topic_enisa_evidence.md` → `ENISA_EVIDENCE_PACK_*.md` derived view (auto-gen markers) |

## Reference-only

| Asset | Path | Notes |
|:------|:-----|:------|
| P2 mirror apply evidence | `reports/p2-mirror-apply-evidence.md` | Timestamps, advisor warnings, row counts |
| Pgraph apply evidence | `reports/pgraph-neo4j-apply-evidence.md` | Constraints + indexes added |
| UAT report | `reports/uat-i25-topic-graph-and-km-scalability-<DATE>.md` | PASS/SKIP/N/A per row; closure record |
