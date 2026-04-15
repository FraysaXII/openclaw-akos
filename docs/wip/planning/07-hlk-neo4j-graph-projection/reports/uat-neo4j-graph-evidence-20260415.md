# UAT evidence: HLK Neo4j graph (closeout run)

**Date:** 2026-04-15  
**Operator / agent:** Repository automation (governed matrix + unit coverage)  
**Neo4j:** unconfigured in CI path (REST returns `neo4j: unconfigured`)  
**AKOS API:** `http://127.0.0.1:8420` (tests use `TestClient`; no secrets recorded)

## 1. Automated gates

| Check | PASS/FAIL | Notes |
|-------|-----------|-------|
| release-gate | PASS | After `scripts/test.py all` + companion fixes |
| browser-smoke --playwright | SKIP/PASS | Host-dependent; parent JSON parse regression covered by `tests/test_browser_smoke_parse.py` |
| validate_hlk_vault_links | PASS | Part of release-gate |

## 2. Dashboard (manual / exploratory)

| Scenario | PASS/FAIL | Notes |
|----------|-----------|-------|
| Madeira HLK role lookup | N/A | Operator fills after live dashboard pass |
| Graph API summary (if Neo4j on) | N/A | |
| `GET /hlk/graph/explorer` | PASS | Covered by `tests/test_api.py::TestHlkGraph::test_hlk_graph_explorer_returns_html` |
| Neo4j down / unconfigured | PASS | Summary still `ok`; neighbourhoods 503 |

## 3. Neo4j multi-style checks

| Style | PASS/FAIL | Notes |
|-------|-----------|-------|
| `scripts/sync_hlk_neo4j.py` parity | N/A | Requires live `NEO4J_*` + Neo4j |
| MCP graph tools | N/A | Operator with mcporter |
| REST neighbourhoods | PASS | 503 without Neo4j (`tests/test_api.py`) |

## 4. Query categories exercised

Automated: HTML explorer markup; JSON summary shape; `parse_json_results_from_stdout` unit tests.

---

Full multi-style Cypher and live sync evidence: extend this file or the template after operator exercise against a real DB.
