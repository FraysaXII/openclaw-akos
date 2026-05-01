---
language: en
status: active
intellectual_kind: phase_report
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# I46 P3 — GraphRAG PoC scaffold

**Phase:** P3 (1-week PoC scaffold ships; live indexing operator-cost-gated per R-46-1)
**Closes:** I46 P3 scaffold portion + sets up the actual A/B run for operator
**Date:** 2026-05-01

## Actions

1. **Golden queries**: new `config/graphrag/golden_queries.json` with 20 queries for `SKILL-MADEIRA-LOOKUP-V1`:
   - 6 single-hop intents (role / process / persona / channel / topic / policy lookup)
   - 4 multi-hop intents (skill→owner, persona→channel, program→skills, etc.)
   - 4 graph-traversal intents (topic dependencies, program ownership overlap, etc.)
   - 2 anomaly-detection intents (roles with no processes; processes with no owner)
   - 2 doctrine-lookup intents (BRAND_VOICE pillar; NEO4J_STRATEGY agent memory)
   - 2 policy-lookup intents (RLS for skill_registry_mirror; cost ceiling for executor skill)

2. **PoC runner scaffold** `scripts/graphrag_poc.py`:
   - Three modes: `--validate-config`, `--dry-run` (default; no LLM cost), live (requires `AKOS_GRAPHRAG_POC_LIVE=1`)
   - `--max-spend` flag (default $20; matches R-46-1 ceiling)
   - Live mode is currently a SCAFFOLD that prints the planned execution + cost ceiling + the operator handoff steps. Implementation of the actual `neo4j-graphrag-python` indexing loop lands when operator opts in (per R-46-1 cost-control posture).

3. **14 new tests** in `tests/test_graphrag_poc.py`:
   - Golden queries config (6 tests): file presence + count + skill targeting + required-field schema + ID uniqueness + intent diversity
   - PoC scaffold CLI (6 tests): --validate-config PASS + --dry-run exits 0 + lists skill + live-without-env exits 2 + live-with-env emits scaffold notice + --max-spend respected
   - validate_config helper (2 tests): catches missing fields + few-queries

## Verification

- `py scripts/graphrag_poc.py --validate-config`: PASS (20 queries)
- `py scripts/graphrag_poc.py --dry-run`: lists 20 queries with intents; cost ceiling $20.00; planned A/B paths shown
- `py scripts/graphrag_poc.py` (no env guard): exits 2 with "AKOS_GRAPHRAG_POC_LIVE=1 is required" + R-46-1 reference
- `AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py`: exits 0 with LIVE MODE banner + scaffold notice
- `tests/test_graphrag_poc.py`: **14/14 PASS** in 1.0s

## What this does NOT do (operator-pending)

- **No actual `neo4j-graphrag-python` indexing implementation yet** — the live mode is a SCAFFOLD that points at the operator handoff. The implementation lands when:
  1. Operator runs `pip install neo4j-graphrag-python` (introduces optional dependency per R-46-11)
  2. Operator confirms the per-run cost ceiling (per R-46-1)
  3. Operator confirms an LLM provider via env (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY` or `OLLAMA_*`)
- **No A/B execution loop** — the loop logic is documented in the scaffold; needs operator to wire the actual indexing call
- **No `reports/graphrag-poc-results-YYYY-MM-DD.md`** yet — this is the deliverable that emerges from the live run

## Decision: ship-or-no-ship for I46 P5

Per master-roadmap, P5 conditional ship requires **any-of** the 3 bars met:
- ≥3pp accuracy lift on the 20 golden queries
- ≥30% latency reduction
- ≥40% cost reduction

If any bar met → P5 ships `retrieval_mode=graph_rag` for `SKILL-MADEIRA-LOOKUP-V1`. If no bar met → P5 documents the decision-not-to-ship with the actual numbers (column added but inactive).

## Operator-applied steps to actually run the PoC

1. `pip install neo4j-graphrag-python` (~5 min; optional dep)
2. Set LLM provider env vars (`OPENAI_API_KEY` for cheap-tier embeddings, optionally `ANTHROPIC_API_KEY` for entity extraction)
3. Confirm cost ceiling (default $20; can lower with `--max-spend N`)
4. `AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py`
5. Review the emitted `reports/graphrag-poc-results-YYYY-MM-DD.md`
6. Decide P5 ship-or-no-ship; record in I46 decision-log as `D-IH-46-Decision-P3-2026-MM-DD`

## Next phase

P4 — Use-case C ADR. 1-page architecture decision record for agent memory: defer with explicit operator-chosen trigger condition (multi-tenant load OR conversation depth OR compliance ask). Document Zep/Mem0/in-house Neo4j evaluation framework for when trigger fires.
