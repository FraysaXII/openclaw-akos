# Initiative 25 — Risk Register

## Active risks

| ID | Description | Mitigation | Owner | Status |
|:---|:-----------|:-----------|:-----:|:------:|
| **PR-25-1** | Auto-gen marker overwrites hand-authored content (PMO hub or ENISA derived view). | Refuse-to-write semantics: marker absent / unbalanced → exit non-zero with `MARKER_NOT_FOUND`. Drift detection: END marker carries `sha256=<hex>` of rendered body; mismatch → `AUTOGEN_DRIFT_DETECTED`. Hand-authored content above BEGIN and below END is never touched. | Agent (P5 + P6) | OPEN |
| **PR-25-2** | Dual-SSOT for topic edges (manifest vs CSV). | D-IH-12 declares CSV authority; `validate_hlk_km_manifests.py` FK-resolves manifest edges into TOPIC_REGISTRY; drift fails the manifest validator. | Agent (P1 + P2) | OPEN |
| **PR-25-3** | Wikilink rot if convention misused (e.g. linking to a topic_id that doesn't exist in TOPIC_REGISTRY). | Wikilinks are explicitly out-of-scope for `validate_hlk_vault_links.py` (D-IH-12). Operator review covers wikilink discipline. | Operator | OPEN |
| **PR-25-4** | Neo4j projection edge collision with existing `:PARENT_OF` (Initiative 07 process tree) and `:PROGRAM_PARENT_OF` (Initiative 23). | Edge naming disambiguated: `:TOPIC_PARENT_OF`, `:TOPIC_SUBSUMES`, `:DEPENDS_ON`, `:RELATED_TO`. Validator-time assertion in `akos/hlk_graph_model.py` `EdgeType` enum. | Agent (Pgraph) | OPEN |
| **PR-25-5** | Graph staleness if `sync_hlk_neo4j.py` fails silently in CI. | `sync_hlk_neo4j_dry_run_smoke` verify profile asserts the parity-assert pass on Topic builders even without Bolt; SKIP only when driver lib missing, not silently. | Agent (Pgraph) | OPEN |
| **PR-25-6** | `manifest_path` becomes stale (file moves; Initiative 22 P2 precedent). | Validator asserts `manifest_path` resolves to an existing file at validation time; `git mv` operations cascade through the canonical CSV. | Agent (P2) | OPEN |
| **PR-25-7** | ENISA derived view loses operator hand-author when reframed as auto-gen. | P6 carefully partitions hand-authored prose (above/below markers) from auto-rendered facts/sources sections. Pre-flight diff review before commit. | Agent + Operator (P6) | OPEN |

## Cross-references

- Wave-2 plan §"Risk and rollback"
- Initiative 23 risk register (Neo4j projection edge collision precedent)
