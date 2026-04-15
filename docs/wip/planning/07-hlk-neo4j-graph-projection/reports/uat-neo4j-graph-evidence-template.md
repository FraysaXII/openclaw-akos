# UAT evidence: HLK Neo4j graph (template)

**Date:** YYYY-MM-DD  
**Operator / agent:**  
**Neo4j:** configured / unconfigured  
**AKOS API:** URL + auth method (never paste secrets)

## 1. Automated gates

| Check | PASS/FAIL | Notes |
|-------|-----------|-------|
| release-gate | | |
| browser-smoke --playwright | | |
| validate_hlk_vault_links | | |

## 2. Dashboard (manual / exploratory)

| Scenario | PASS/FAIL | Notes |
|----------|-----------|-------|
| Madeira HLK role lookup | | |
| Process tree by id | | |
| Graph API summary (if Neo4j on) | | |
| Graph neighbourhood depth 1–3 | | |
| Missing API key rejected | | |
| Neo4j down / unconfigured behaviour | | |

## 3. Neo4j multi-style checks

| Style | PASS/FAIL | Notes |
|-------|-----------|-------|
| `scripts/sync_hlk_neo4j.py` parity line | | |
| MCP `hlk_graph_process_neighbourhood` | | |
| MCP `hlk_graph_role_neighbourhood` | | |
| REST `/hlk/graph/process/{id}/neighbourhood` | | |
| Count `MATCH (n) RETURN labels(n), count(*)` | | |
| Parameter injection attempt rejected | | |

## 4. Query categories exercised

(List Cypher or tool calls run; keep payloads non-secret.)

---

Replace placeholders after each major release or phase sign-off.
