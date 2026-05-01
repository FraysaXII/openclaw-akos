---
language: en
status: active
initiative: 46-neo4j-strategic-posture
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 46 — Asset Classification

## New canonical (planning artifacts)

| Path | Class | Owner | Validator |
|:-----|:------|:------|:----------|
| `docs/wip/planning/46-neo4j-strategic-posture/master-roadmap.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/46-neo4j-strategic-posture/decision-log.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/46-neo4j-strategic-posture/evidence-matrix.md` | canonical | Founder + System Owner | none (prose) |
| `docs/wip/planning/46-neo4j-strategic-posture/asset-classification.md` (this file) | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/46-neo4j-strategic-posture/risk-register.md` | canonical | Founder + System Owner | `validate_planning_traceability` |

## New canonical (vault doctrine)

| Path | Class | Owner | Validator |
|:-----|:------|:------|:----------|
| `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md` (P1) | canonical doctrine | System Owner | `validate_localisation_frontmatter` (en/es/fr) + `BRAND_JARGON_AUDIT` (external prose section) |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md` (P4) | canonical doctrine (ADR) | System Owner | same as above |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/` (sub-area directory) | canonical sub-area | System Owner | filesystem-only |

## New canonical (registry surface, conditional)

| Path | Class | Owner | Conditional on |
|:-----|:------|:------|:----------------|
| `retrieval_mode` column on `SKILL_REGISTRY.csv` (P5) | canonical | System Owner | P3 PoC meets bar (D-IH-46-E) |
| New POLICY_REGISTER row: `pol_neo4j_graph_rag_eligibility_<topic_class>` (P5) | canonical | System Owner | Same as above |
| New `policy_class` enum value: `graph_rag_eligibility` | canonical | System Owner | Same as above |
| `SKILL-MADEIRA-LOOKUP-V1` row updated: `retrieval_mode=graph_rag` (P5) | canonical edit | System Owner | Same as above |

## New scripts

| Path | Class | Purpose | Phase |
|:-----|:------|:--------|:------|
| `scripts/graphrag_poc.py` | canonical (governed-script) | P3 PoC runner: indexes vault subset, runs 20 golden queries via both A (current) and B (GraphRAG hybrid), emits scorecard | P3 |
| `scripts/graphrag_drift_canary.py` | canonical | Compares Neo4j node counts to CSV row counts; fails on >1 row deviation (allows for in-flight syncs) | P2 |
| `tests/evals/cassettes/graph_rag/<query_id>.jsonl` | mirrored / derived | Recorded GraphRAG trajectories via I45 P2 recorder | P6 |
| `tests/evals/cassettes/graph_rag_adversarial/<probe_id>.jsonl` | mirrored / derived | Adversarial probes that should NOT escape into GraphRAG (e.g., simple ID lookups stay on direct CSV path) | P6 |

## New MCP tools

| Tool name | Class | Source | Phase |
|:----------|:------|:-------|:------|
| `hlk_graph_skill_neighbourhood` | canonical | New helper in `akos/hlk_neo4j.py` + new MCP tool registration in `scripts/hlk_graph_mcp_server.py` | P2 |

## New CI

| Profile | Trigger | Phase |
|:--------|:--------|:------|
| `neo4j_governance_kg_drift_smoke` (added to `verification-profiles.json`) | Nightly + pre-commit | P2 |
| `neo4j_idempotency_recurring_check` (added to release-gate) | Per release | P2 |

## Modified canonical

| Path | Change | Phase |
|:-----|:-------|:------|
| `prompts/overlays/OVERLAY_HLK_GRAPH.md` | Cite `NEO4J_STRATEGY.md` | P1 |
| `config/sync/kirbe-sync-contract.md` §11 | Cite `NEO4J_STRATEGY.md` + restate KiRBe Neo4j separation per D-IH-32-M | P1 |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md` | Optional Neo4j section pointing at `NEO4J_STRATEGY.md` | P1 |
| `scripts/hlk_graph_mcp_server.py` | Register `hlk_graph_skill_neighbourhood` tool | P2 |
| `akos/hlk_neo4j.py` | Add `skill_neighbourhood()` helper | P2 |
| `config/agent-capabilities.json` | Add `hlk_graph_skill_neighbourhood` to `madeira` role | P2 |
| `docs/wip/planning/README.md` | New row for I46 | P0 |
| `docs/wip/planning/WIP_DASHBOARD.md` | Re-rendered | P0 + P7 |
| `CHANGELOG.md` | Closure entry | P7 |

## Reference-only / external (cited but not authored)

| Source | Citation use |
|:-------|:-------------|
| **Neo4j GraphRAG Manifesto** (neo4j.com/blog/genai/graphrag-manifesto) | NEO4J_STRATEGY.md doctrine context (Use-case B framing) |
| **neo4j-graphrag-python** docs (neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) | D-IH-46-A library choice + P3 PoC implementation reference |
| **Tianpan.co** "GraphRAG in production 2026" | E5, E6, E10 evidence + D-IH-46-A cost argument |
| **AgentMarketCap** "Agent Memory at Scale 2026" | E7 evidence + D-IH-46-B alternatives analysis |
| **AgentMarketCap** "Agent Memory in Production 2026" | E7 supplementary |
| **Microsoft GraphRAG** (techcommunity.microsoft.com cost explainer) | E5 cost reference |
| **LightRAG** (github / arXiv) | D-IH-46-A library choice (referenced via Tianpan.co) |
| **Zep / Graphiti** | D-IH-46-B alternatives + use-case C distinction |
| **Mem0** | D-IH-46-B alternatives |
| **Cognee** | D-IH-46-B alternatives (multimodal ingest pattern) |
| **Letta** | D-IH-46-B alternatives (virtual memory paging) |

## What is explicitly NOT changed

- `sync_hlk_neo4j.py` interior (works; idempotent per D-IH-32-Q).
- `akos/hlk_graph_model.py` (current 6-axis projection is correct).
- `akos/api.py` graph endpoints (untouched; new MCP tool is additive).
- KiRBe's local Neo4j (D-IH-32-M holds).
- Existing 4 read endpoints (`/hlk/graph/summary`, process and role neighbourhood, explorer).
- HLK CSV vault SSOT posture (Neo4j stays projection).

## Cross-classification with I45

- I45 P3 adds `routing_condition` column to SKILL_REGISTRY.
- I46 P5 adds `retrieval_mode` column to the same CSV.
- Both columns coexist; validator updates in both initiatives must be coordinated to avoid lock-step rebase pain. Coordination point: P5 here depends on I45 P3 having shipped first.
