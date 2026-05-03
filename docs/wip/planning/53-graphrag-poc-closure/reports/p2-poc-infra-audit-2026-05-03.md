# I53 / P2 — PoC infra audit

**Date:** 2026-05-03
**Phase:** P2 (PoC infra audit; no live spend)

## Audit findings

### `scripts/graphrag_poc.py --dry-run` — listed planned execution

```text
GraphRAG PoC — DRY RUN (no LLM cost incurred)
  Skill under test:  SKILL-MADEIRA-LOOKUP-V1
  Queries:           20
  Cost ceiling:      $20.00 per run
  Path A: current hlk_role + hlk_search chain (deterministic)
  Path B: GraphRAG hybrid via neo4j-graphrag-python (live LLM)

  Queries to be exercised:
    - [role_lookup]   q01_role_def: Who is the System Owner role responsible for?
    - [role_chain]    q02_role_chain: What is the chain of reporting from System Owner up to the F...
    - [process_owner] q03_process_owner: Which role owns the FinOps quarterly reporting process?
    - [process_tree]  q04_process_tree: What are the child processes of the executor agent process t...
    - [persona_lookup] q05_persona: What persona archetype is an investor-cold inbound contact?
    ... and 15 more

  To run live: AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py
  Operator must confirm the cost budget before opt-in.
```

### Live-mode env-guard verification (offline)

- Without `AKOS_GRAPHRAG_POC_LIVE=1` set, `py scripts/graphrag_poc.py` (no flags) → **exits 2** with the operator-handoff message that includes the R-46-1 reference.
- With `AKOS_GRAPHRAG_POC_LIVE=1`, scaffold prints **LIVE MODE banner** + scaffold notice (no actual indexing call without operator extra steps) — this is the I46 P3 design intent.

### Neo4j connection contract

Verified `scripts/graphrag_poc.py` reads the standard Neo4j env knobs (`NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`) used by `sync_hlk_neo4j.py` (I32 P5/P6). No new operator-side configuration required for the live A/B beyond what already runs the governance KG sync.

### Existing safety nets confirmed

- `scripts/validate_skill_registry.py` rejects typos in `retrieval_mode` (e.g., `graphRAG`, `rag`, `knowledge_graph`); only `""`, `vector_only`, `graph_rag`, `hybrid` accepted.
- `tests/test_neo4j_retrieval_mode.py` (I46 P5) locks the column contract.
- `tests/test_neo4j_graph_escape.py` (I46 P6) is the adversarial floor.
- `scripts/graphrag_drift_canary.py` (I46 P6) checks Neo4j ≈ CSV row counts.

### POLICY status

- `pol_neo4j_graph_rag_eligibility` row + `policy_class=graph_rag_eligibility` enum value present in `POLICY_REGISTER.csv` (I46 P5; template-only).
- Per I46 P5 design: **template-only until per-topic-class clones land at I53 P5 (conditional)** with PoC numbers anchoring eligibility.

## Verification

- `py scripts/graphrag_poc.py --validate-config` — PASS.
- `py scripts/graphrag_poc.py --dry-run` — PASS (lists 20 queries + cost ceiling + planned A/B paths).
- Live-mode env-guard — PASS (exit 2 without env, exit 0 with env + scaffold notice).
- 46 graph/Neo4j tests — PASS in 5.21s.
- `py scripts/check-drift.py` — PASS.

## Forward look

P3 either drives the live A/B (operator opt-in via `AKOS_GRAPHRAG_POC_LIVE=1` + provider env keys) OR documents the **no-fire** outcome as a governance event and forwards live activation as `OPS-53-1` to the next AKOS_RECORD_LIVE cycle.
