# I53 / P1 — Golden-set audit + pre-flight cost estimate

**Date:** 2026-05-03
**Phase:** P1 (Pre-flight + golden-set audit)

## Audit findings

### `config/graphrag/golden_queries.json` (20 queries)

```text
py scripts/graphrag_poc.py --validate-config
[graphrag-poc] golden_queries.json: PASS (20 queries)
```

Distribution per **D-IH-53-B** (already encoded at I46 P3 2026-05-01):

| Intent class | Count | %  |
|:--|--:|--:|
| single-hop (role / process / persona / channel / topic / policy lookup) | 6 | 30% |
| multi-hop (skill→owner, persona→channel, program→skills) | 4 | 20% |
| graph-traversal (topic dependencies, program ownership overlap) | 4 | 20% |
| anomaly-detection (roles with no processes; processes with no owner) | 2 | 10% |
| doctrine-lookup (BRAND_VOICE pillar; NEO4J_STRATEGY agent memory) | 2 | 10% |
| policy-lookup (RLS skill_registry_mirror; cost ceiling executor) | 2 | 10% |
| **Total** | **20** | **100%** |

**Graph-required share:** 70% (14/20 queries require traversal beyond a single CSV-row lookup) — this is the right shape to A/B vector-only against graph_rag.

### Pre-flight cost estimate (R-53-1 mitigation)

Conservative estimate for the live A/B:

| Component | Per-query | × 20 queries × 2 modes | Notes |
|:--|--:|--:|:--|
| Embedding (vector_only path) | $0 | $0 | `nomic-embed-text` via Ollama (local-zero) |
| Embedding (graph_rag path; node embeddings) | $0 | $0 | Same Ollama local model; one-time amortised over the run |
| Retrieval-LLM (graph_rag path only; planner-LLM via `neo4j-graphrag-python`) | ~$0.005 | ~$0.10 | Anthropic Sonnet input ~1.5k tokens / output ~0.3k tokens per query |
| Multi-judge accuracy scoring (I52 roster: Sonnet + gpt-4o consensus) | ~$0.02 | ~$0.80 | per the JUDGE_ROSTER_V1 cost cap; well under POL-EVAL-COST-CEILING-JUDGE-V1 envelope |
| **Subtotal estimate** | | **~$0.90** | |
| Headroom for retries + cassette re-records | | ~$5-10 | per R-53-1 |
| **Total estimated envelope use** | | **~$10 / $20** | |

**Conclusion:** $20 envelope is **sufficient**. R-53-1 mitigated; abort threshold ($25) not approached.

### Operator opt-in surface

Live A/B requires three operator confirmations:

1. **`pip install neo4j-graphrag-python`** — optional dependency per R-46-11 (not added to `requirements.txt`).
2. **`AKOS_GRAPHRAG_POC_LIVE=1`** — env var explicitly enables live mode.
3. **Provider env keys** — `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (for the retrieval-LLM and the I52 judge roster); `OLLAMA_*` for embeddings.

Plus implicit:
- Neo4j connection knobs (`NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`) confirmed in operator's environment.
- I52 multi-judge roster pinned: `vars.AKOS_JUDGE_ROSTER='anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o'`.

## Verification

- 20 queries present + governed: PASS.
- Cost estimate within R-46-1 ceiling: PASS.
- Opt-in surface documented: PASS.
- `tests/test_graphrag_poc.py` (14 tests; I46 P3): all PASS via the broader sweep (`py -m pytest tests/test_graphrag_poc.py tests/test_neo4j_retrieval_mode.py tests/test_neo4j_graph_escape.py tests/test_neo4j_usecase_a_hardening.py -q` → 46 passed in 5.21s).

## Forward look

P2 audits the runtime PoC infra (`scripts/graphrag_poc.py --dry-run`) and confirms the planned execution.
