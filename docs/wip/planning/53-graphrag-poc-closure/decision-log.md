---
language: en
status: active
initiative: 53-graphrag-poc-closure
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 53 — Decision log

Four decisions seeded with defaults per the cursor plan; operator-ratified at I50-I56 master roadmap greenlight 2026-05-03.

## D-IH-53-A — Judge model used in PoC accuracy scoring

**Decision (default):** **Re-use I52 pinned roster** (`anthropic:claude-3-5-sonnet-20241022` + `openai:gpt-4o` N=2 consensus, per [`prompts/judge/JUDGE_ROSTER_V1.md`](../../../prompts/judge/JUDGE_ROSTER_V1.md)).

**Rationale:** Multi-judge consensus (per D-IH-52-B) mitigates single-model sycophancy on the accuracy axis. Same threshold (POL-EVAL-JUDGE-THRESHOLD-PERSONA-FIT-V1 `min_pass_score=4`) applies. Cost cap stays at `MAX_JUDGE_USD_PER_RUN=$15` (D-IH-52-C); for 20 queries × 2 modes × 2 judges this is well under the operator-funded $20 envelope.

**Reversibility:** High — env-var roster swap via `AKOS_JUDGE_ROSTER`.

---

## D-IH-53-B — 20-query selection criteria

**Decision (default):** **60% multi-hop / 40% single-hop; mix of OPERATOR + Tier-1 persona shapes**, already encoded in I46 P3 [`config/graphrag/golden_queries.json`](../../../config/graphrag/golden_queries.json).

The I46 P3 set:
- 6 single-hop intents (role / process / persona / channel / topic / policy lookup)
- 4 multi-hop intents (skill→owner, persona→channel, program→skills)
- 4 graph-traversal intents (topic dependencies, program ownership overlap)
- 2 anomaly-detection intents (roles with no processes; processes with no owner)
- 2 doctrine-lookup intents (BRAND_VOICE pillar; NEO4J_STRATEGY agent memory)
- 2 policy-lookup intents (RLS skill_registry_mirror; cost ceiling executor)

= **20 queries**, **70% requiring graph traversal beyond a single CSV-row lookup**, which is the right shape to A/B vector-only against graph_rag.

**Reversibility:** High — JSON file edit + decision-log row.

---

## D-IH-53-C — Trade-off thresholds (non-additive)

**Decision (default):** **Any one of the three I46 P5 bars qualifies; non-additive per D-IH-46-E.**

The three bars:
1. ≥3pp accuracy lift over baseline `hlk_role + hlk_search` chain.
2. ≥30% latency reduction (median).
3. ≥40% cost reduction (per query, including indexing amortisation over the cassette set).

**Non-additivity:** "Two-thirds of each bar" is **not** a ship signal. Each bar is independently meaningful: accuracy is the primary signal; latency matters because MADEIRA is interactive; cost matters because graph_rag adds indexing overhead that must be amortised.

**Forbids:** Partial-credit ship (e.g., 2pp + 15% latency + 20% cost).

**Reversibility:** Low — this decision is the operator's ship-bar; revisiting requires explicit decision-log row.

---

## D-IH-53-D — Rollback procedure

**Decision (default):** **SKILL_REGISTRY `retrieval_mode=vector_only` flip + decision-log row; cassettes preserved.**

The retrieval mode is a single-row CSV edit. Rollback path:

1. Flip [`SKILL_REGISTRY.csv`](../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv) `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode` from `graph_rag` to `vector_only`.
2. Re-run `py scripts/sync_compliance_mirrors_from_csv.py --skill-registry-only`.
3. Append decision-log row noting the rollback rationale + correlation ID for the regression that triggered it.
4. **Preserve cassettes** under `tests/evals/cassettes/graph_rag/` — they remain replayable against the prior `graph_rag` mode if a future initiative re-runs the A/B with corrections.

**Reversibility:** High — bidirectional with the ship path.

---

## Decisions made during execution

(Will be appended as P0-P7 phases execute.)
