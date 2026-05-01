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

# I46 P4 — Agent memory ADR (defer with trigger)

**Phase:** P4 (D-IH-46-B operationalized: write defer-with-trigger ADR)
**Closes:** I46 P4 + R-46-4 mitigation (no half-built memory system).
**Date:** 2026-05-01

## Actions

1. **Shipped** [`AGENT_MEMORY_DEFERRED_ADR.md`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md) (~155 lines) in vault sub-area `Envoy Tech Lab/Neo4j/`:
   - **Status: ACCEPTED 2026-05-01**
   - **Decision: Do NOT build agent/user memory KG in I46.** Defer until trigger fires.
   - **3 trigger conditions** (operator picks; default = Trigger 1):
     - Trigger 1 — Multi-tenant load (when I34 closes; default)
     - Trigger 2 — Conversation depth (≥10% MADEIRA traces with skills_invoked_count ≥4 in 7d window)
     - Trigger 3 — Compliance ask (highest urgency; non-deferrable)
   - **Evaluation framework** when trigger fires (4 steps):
     - Step 1: buy vs build (default Zep/Graphiti; alternatives Mem0; in-house only if cost ceiling fails)
     - Step 2: schema sketch (`:User`, `:Fact`, `:Session` nodes with temporal columns)
     - Step 3: privacy + retention (PII scope, retention windows, right-to-erasure, cross-tenant isolation)
     - Step 4: eval (LongMemEval-style, I45 cassettes, I45 P7 promotion gate)
   - **12-month sunset clause** (review-not-revive)
   - Cited 2026 sources (Tianpan.co + AgentMarketCap) explaining why Zep/Graphiti's 63.8% LongMemEval is the benchmark to beat

## Verification

- `validate_hlk`: PASS (153 files now in vault including the new ADR; new doctrine has `language: en` frontmatter)
- ADR cross-references resolve: NEO4J_STRATEGY.md, decision-log D-IH-46-B, D-IH-32-M, I34 (future), I21 (closed)

## What this does NOT do

- **No build, no schema, no Supabase migration, no MCP tool** — the entire point of P4 is "no build"
- **No automated trigger detection** — operator-side judgement; the ADR documents the signals to watch

## Operator-applied steps

1. Read the ADR at `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md`
2. Confirm the **default trigger** (Trigger 1 — Multi-tenant load via I34) — or pick a different trigger by editing the decision-log
3. Review at 12-month mark (sunset clause)
4. When trigger fires, open Initiative 47+ with the evaluation framework as starting context

## Next phase

P5 — Conditional GraphRAG ship. Adds `retrieval_mode` column to SKILL_REGISTRY (placeholder; populates when P3 PoC operator-side ships); adds `pol_neo4j_graph_rag_eligibility` POLICY_REGISTER row (template; per-topic-class policies populated when first ship lands).
