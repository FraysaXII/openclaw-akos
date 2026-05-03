---
language: en
status: active
initiative: 53-graphrag-poc-closure
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 53 — Asset classification

Per [`PRECEDENCE.md`](../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (edit here first)

- [`docs/references/hlk/compliance/dimensions/SKILL_REGISTRY.csv`](../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv) — `retrieval_mode` column already added at I46 P5; this initiative may flip the `SKILL-MADEIRA-LOOKUP-V1` row from `vector_only` to `graph_rag` at **P5 (conditional)** if the P3 A/B passes one of the three D-IH-53-C bars.
- [`docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv`](../../references/hlk/compliance/dimensions/POLICY_REGISTER.csv) — `pol_neo4j_graph_rag_eligibility` row + `policy_class=graph_rag_eligibility` enum already present (I46 P5); this initiative may add per-topic-class rows in P5 if needed.

## Mirrored / derived

- `compliance.skill_registry_mirror` (Supabase) — auto-synced from CSV via `scripts/sync_compliance_mirrors_from_csv.py --skill-registry-only` after any `retrieval_mode` flip.
- Cassettes under `tests/evals/cassettes/graph_rag/<query_id>.jsonl` — recorded, not authored; via I45 P2 recorder once the live PoC executes.

## Reference-only (do not edit)

- [`docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md`](../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md) — vault doctrine; cited, not edited.
- [`docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md`](../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md) — vault ADR; out of scope for I53.

## Code (no canonical-status edits)

- [`scripts/graphrag_poc.py`](../../../scripts/graphrag_poc.py) — I46 P3 scaffold; this initiative drives it through real exercise but does not re-author the scaffold.
- [`scripts/graphrag_drift_canary.py`](../../../scripts/graphrag_drift_canary.py) — I46 P6 canary; this initiative confirms wiring.
- [`akos/intent.py`](../../../akos/intent.py) — already reads `retrieval_mode` from registry (I46 P5).
- [`config/graphrag/golden_queries.json`](../../../config/graphrag/golden_queries.json) — 20-query golden set (I46 P3).

## Tests

- `tests/test_graphrag_poc.py` (14 tests; I46 P3) — confirmed at I53 P1.
- `tests/test_neo4j_graph_escape.py` (adversarial; I46 P6).
- `tests/test_neo4j_retrieval_mode.py` (I46 P5).
- `tests/test_neo4j_usecase_a_hardening.py` (I46 P2).
