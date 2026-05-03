# I53 / P6 — Test wiring + canaries

**Date:** 2026-05-03
**Phase:** P6 (Test wiring + canaries — non-conditional verification)

## Verifications

### Adversarial probes

```text
py -m pytest tests/test_neo4j_graph_escape.py -v
```

All adversarial probes (graph-escape + citation spoofing) **PASS**. The probe surface is the floor regardless of ship/no-ship verdict.

### Retrieval-mode contract

```text
py -m pytest tests/test_neo4j_retrieval_mode.py -v
```

`SKILL_REGISTRY.csv` `retrieval_mode` column contract locked:
- Empty default for all 5 existing skill rows (back-compat preserved).
- Enum constraint enforced in `scripts/validate_skill_registry.py`: only `""`, `vector_only`, `graph_rag`, `hybrid` accepted.
- Typos rejected (`graphRAG`, `rag`, `knowledge_graph` all fail).

### Use-case A hardening (governance KG)

```text
py -m pytest tests/test_neo4j_usecase_a_hardening.py -v
```

`hlk_graph_skill_neighbourhood` MCP tool registered + green; nightly drift canary preserved.

### GraphRAG PoC scaffold (I46 P3)

```text
py -m pytest tests/test_graphrag_poc.py -v
```

14 / 14 PASS — golden queries config + scaffold CLI + helper tests all green.

### Combined sweep

```text
py -m pytest tests/test_graphrag_poc.py tests/test_neo4j_retrieval_mode.py tests/test_neo4j_graph_escape.py tests/test_neo4j_usecase_a_hardening.py -v
=> 46 passed in 3.51s
```

### Drift canary live smoke (CSV-only mode; no Neo4j required)

```text
py scripts/graphrag_drift_canary.py --csv-only
Neo4j drift canary (CSV-only mode)
==================================================
  Channel                   10
  Persona                   16
  Policy                    32
  Process                 1100
  Program                   12
  Role                      65
  Skill                      5
  Sourcing                   1
  Topic                     28
  TouchpointKitCell         15
```

CSV row counts visible without a live Neo4j connection (per the I46 P2 design intent that the canary degrades gracefully).

### Verification profile wiring

[`config/verification-profiles.json`](../../../config/verification-profiles.json) → `neo4j_governance_kg_drift_smoke` profile present (line 222), wired to `scripts/graphrag_drift_canary.py`. Skips gracefully when Neo4j env is unconfigured.

### Cassettes folder

[`tests/evals/cassettes/graph_rag/`](../../../tests/evals/cassettes/graph_rag/) folder + README present from I46 P6. Recorded cassettes will land here when OPS-53-1 fires.

## Verification

All verification surfaces required by I53/I46 are green:

- 46 graph/Neo4j tests PASS (5.21s sweep earlier in session; 3.51s sweep this phase).
- Drift canary CSV-only smoke renders all 10 dimensions.
- `neo4j_governance_kg_drift_smoke` profile wired.
- Adversarial probes (graph-escape) green.
- Retrieval-mode contract locked.

## Forward look

P7 closes both I46 and I53 on the no-ship path. The OPS-53-1 forward (operator-funded live A/B run) preserves cassettes, scaffold, and infrastructure for the next cycle.
