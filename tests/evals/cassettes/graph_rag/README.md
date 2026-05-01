---
language: en
status: scaffold
intellectual_kind: cassette_directory_marker
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_skill_registry
parent_topic: topic_skill_registry
---

# GraphRAG cassettes (placeholder; populates when I46 P5 ships a skill)

This directory is the canonical home for `live_llm` cassettes recorded against the GraphRAG hybrid retrieval path (Initiative 46 use-case B). It's empty today because no skill has been activated to `retrieval_mode='graph_rag'` yet.

## When this directory populates

1. Operator runs the I46 P3 PoC live (`AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py`)
2. PoC outcome documented in `docs/wip/planning/46-neo4j-strategic-posture/decision-log.md` as `D-IH-46-Decision-P3-2026-MM-DD`
3. If verdict = SHIP for `SKILL-MADEIRA-LOOKUP-V1`: operator sets `retrieval_mode=graph_rag` on the SKILL_REGISTRY row + activates `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TEMPLATE` clone
4. Operator records initial GraphRAG cassettes:
   ```
   AKOS_RECORD_LIVE=1 py scripts/eval.py record \
     --skill SKILL-MADEIRA-LOOKUP-V1 \
     --probe gr_role_lookup_q01 \
     --prompt "Who is the System Owner role responsible for?" \
     --kind live_llm \
     --model-id "<operator-set>" \
     --model-tier flagship \
     --by operator
   ```
5. Cassettes land here as `tests/evals/cassettes/graph_rag/<skill_id>/<probe_id>.jsonl`

## Replay path

When cassettes exist, `py scripts/eval.py --mode replay` picks them up automatically (the I45 P2 `replay_cassette` dispatcher routes by `probe_kind`). For GraphRAG cassettes the dispatcher lands in `replay_live_llm_cassette` which checks recorded final response against the golden rubric — does NOT re-call the LLM at replay time (cost-controlled per AgentEval pattern).

## Adversarial graph-escape probes

Adversarial probes that should NOT escape into GraphRAG live alongside other adversarial cassettes at:

- `tests/evals/cassettes/adversarial/SKILL-MADEIRA-LOOKUP-V1/ge_simple_role_id_lookup.jsonl`
- `tests/evals/cassettes/adversarial/SKILL-MADEIRA-LOOKUP-V1/ge_persona_id_direct.jsonl`
- `tests/evals/cassettes/adversarial/SKILL-MADEIRA-LOOKUP-V1/ge_process_item_id_direct.jsonl`

These shipped in I46 P6 as a guard against R-46-2 (GraphRAG hallucinations leak into MADEIRA answers): simple direct lookups must STAY on the CSV path, not get over-eagerly routed through expensive graph traversal once GraphRAG is wired.

## Status

- **Today (I46 P6)**: scaffold-only; 0 GraphRAG cassettes; 3 graph-escape adversarial cassettes shipped
- **After I46 P3 PoC ship**: ≥5 GraphRAG cassettes per active skill (covering the 20 golden_queries.json subset most likely to benefit from graph retrieval)

## Cross-references

- I46 P3 PoC scaffold: `scripts/graphrag_poc.py`
- I46 P5 conditional ship: `SKILL_REGISTRY.csv` `retrieval_mode` column + `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TEMPLATE`
- I45 P2 cassette format: `akos/eval_harness/cassette.py`
- I45 P5 adversarial format: `akos/eval_harness/adversarial.py`
- NEO4J_STRATEGY.md: `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md`
