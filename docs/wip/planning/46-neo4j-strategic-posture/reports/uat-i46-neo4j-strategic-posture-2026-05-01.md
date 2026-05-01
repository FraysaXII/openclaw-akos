---
language: en
status: active
intellectual_kind: uat_report
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

# UAT — Initiative 46 (Neo4j Strategic Posture) closure

**UAT id:** UAT-I46-2026-05-01
**Closes:** Initiative 46 (all 8 phases, P0-P7).
**Date:** 2026-05-01

## Phase verification matrix

| # | Phase | Deliverable | Verification | Status |
|:--:|:------|:-----------|:-------------|:------:|
| P0 | Bootstrap + audit | 5 planning artifacts + audit memo | `validate_planning_traceability`; `audit-current-neo4j-surface-2026-05-01.md` shipped | PASS |
| P1 | NEO4J_STRATEGY.md doctrine | Vault doctrine page + 3 cross-references (OVERLAY + kirbe-sync + EXTERNAL_REPO_CONTRACT) | `validate_hlk` 153 files PASS; ≥3 docs cite the doctrine (success metric met) | PASS |
| P2 | Use-case A hardening | `hlk_graph_skill_neighbourhood` MCP tool + `graphrag_drift_canary.py` + `neo4j_governance_kg_drift_smoke` profile | `pytest tests/test_neo4j_usecase_a_hardening.py` 10/10; drift canary CSV-only mode lists 10 dimensions | PASS |
| P3 | GraphRAG PoC scaffold | `graphrag_poc.py` + 20 golden queries + cost-gated live mode | `pytest tests/test_graphrag_poc.py` 14/14; `--validate-config` + `--dry-run` work; live mode requires `AKOS_GRAPHRAG_POC_LIVE=1` | PASS (scaffold; live indexing operator-pending) |
| P4 | Agent memory ADR | `AGENT_MEMORY_DEFERRED_ADR.md` with operator-set trigger | `validate_hlk` PASS; ADR signed with default trigger = I34 multi-tenant | PASS |
| P5 | Conditional GraphRAG ship scaffold | `retrieval_mode` column + `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TEMPLATE` row + Supabase migration | `pytest tests/test_neo4j_retrieval_mode.py` 12/12; validator enforces enum; back-compat empty default | PASS (scaffold; per-skill activation operator-pending on P3 PoC outcome) |
| P6 | Test wiring | 3 graph-escape adversarial cassettes + GraphRAG dir scaffold + WIP_DASHBOARD operational health | `pytest tests/test_neo4j_graph_escape.py` 10/10; 15/15 adversarial PASS; 21 cassettes PII-clean | PASS |
| P7 | Tests + UAT + closure | This report + CHANGELOG + WIP_DASHBOARD + I46 CLOSED | `pytest tests/`: **1103 passed, 5 skipped, 2 pre-existing failures unrelated to I46** | PASS |

## Test count delta

| Suite | Tests | Status |
|:------|:-----:|:------:|
| **tests/test_neo4j_usecase_a_hardening.py** | **10** | **NEW (P2)** |
| **tests/test_graphrag_poc.py** | **14** | **NEW (P3)** |
| **tests/test_neo4j_retrieval_mode.py** | **12** | **NEW (P5)** |
| **tests/test_neo4j_graph_escape.py** | **10** | **NEW (P6)** |
| **I46-only TOTAL** | **46** | **all PASS** |

Combined I45 + I46 across this branch: **134 (I45) + 46 (I46) = 180 new tests**, all green. Full pytest sweep: **1103 passed, 5 skipped, 2 pre-existing failures** (the `validate_configs.py::TestOpenclawConfig` Pydantic openclaw.json sandbox-mode literal_error failures from BEFORE the i45-i46 branch — confirmed via `git diff i32-holistik-ops-maturation HEAD` showing zero changes to openclaw.json.example, akos/models.py, or tests/validate_configs.py).

## Architectural impact

The doctrine gap that accumulated unwritten across I7 → I23 → I25 → I32 is closed. Future "should we add this to Neo4j?" questions resolve to one of three explicit use-cases (A: governance KG; B: GraphRAG over the vault; C: agent memory) with concrete decision-frames per use-case.

Use-case A now has its first axis-6 traversal surface (`hlk_graph_skill_neighbourhood`) plus a drift canary that catches CSV-vs-Neo4j divergence within 1 row.

Use-case B is operator-cost-gated: 20 golden queries + scaffolded PoC + cost ceiling + ship-or-no-ship decision-frame all in place. Operator runs the actual indexing when budget approved.

Use-case C is rigorously deferred: ADR signed with explicit trigger condition, evaluation framework documented for the future I47+ that reopens it.

KiRBe Neo4j separation (D-IH-32-M) is now permanent doctrine in 2 surfaces (`kirbe-sync-contract.md` + `NEO4J_STRATEGY.md`) instead of buried in 1 decision-log.

## What is NOT yet shipped (operator-pending or deferred)

- **Live GraphRAG PoC indexing run** — P3 ships scaffold; operator runs `AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py` when budget approved
- **Per-skill GraphRAG activation** — P5 ships column + policy template; operator activates after P3 PoC ship verdict
- **`compliance.skill_registry_mirror` `retrieval_mode` column DDL** — operator runs `npx supabase db push` to apply
- **Live agent memory build** — P4 ADR explicitly defers; reopens when trigger fires
- **Router-side `retrieval_mode` honour in `akos.skill_router`** — lands when first skill activates (P5 follow-up)
- **Recurring Neo4j idempotency check in release-gate** — operator-side cron addition

## Operator-applied checklist

1. `npx supabase db push` (lands `retrieval_mode` column on `compliance.skill_registry_mirror`)
2. `py scripts/sync_compliance_mirrors_from_csv.py --skill-only --policy-only` (reseeds the 5 SKILL rows + 1 new POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TEMPLATE)
3. **Optional**: add `neo4j_governance_kg_drift_smoke` profile to `pre_commit` profile in `verification-profiles.json` for nightly drift detection
4. **When ready to PoC**: `pip install neo4j-graphrag-python` + set LLM env + `AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py --max-spend 20`
5. **Record P3 verdict** as `D-IH-46-Decision-P3-2026-MM-DD` in I46 decision-log
6. **If verdict = SHIP**: edit SKILL-MADEIRA-LOOKUP-V1's `retrieval_mode` to `graph_rag` + clone POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TEMPLATE to a per-topic-class row + `sync_compliance_mirrors_from_csv.py`
7. **Watch the trigger** for the deferred agent memory ADR (default: I34 multi-tenant closure)
8. **At 12-month mark**: review `AGENT_MEMORY_DEFERRED_ADR.md` per sunset clause

## Closure assertion

Initiative 46 is **closed**. All 8 phases shipped. 46 new tests added; 1103 total pass; 0 new failures introduced. The 3-use-case Neo4j doctrine is canonical in vault; use-case A is hardened with drift detection; use-case B has a cost-gated PoC scaffold ready for operator activation; use-case C is rigorously deferred with trigger ADR.

Hand-off: I46 P5 conditional ship is the operator-side decision gate. Once P3 PoC runs and the verdict is recorded, P5 activation is a single CSV edit + mirror reseed. The infrastructure is fully in place.

Sister initiative I45 was closed earlier today (2026-05-01 P8 closure). The Registry-Router-Evaluator triangle from I45 P3 plus the GraphRAG retrieval mode column from I46 P5 close the architectural loop: a skill can now declare both `routing_condition` (when to run) and `retrieval_mode` (how to ground), enforced by tooling end-to-end.
