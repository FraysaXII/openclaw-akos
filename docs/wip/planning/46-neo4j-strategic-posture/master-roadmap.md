---
language: en
status: closed
initiative: 46-neo4j-strategic-posture
initiative_id: INIT-OPENCLAW_AKOS-46
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
closed_at: 2026-05-03
closure_decision_id: D-IH-46-CLOSURE
---
# Initiative 46 — Neo4j Strategic Posture: doctrine + GraphRAG PoC + agent memory ADR

**Folder:** `docs/wip/planning/46-neo4j-strategic-posture/`
**Status:** **Closed (2026-05-03)** via [Initiative 53 — GraphRAG PoC closure](../53-graphrag-poc-closure/master-roadmap.md). I46 P3-P7 closure is recorded in [`53-graphrag-poc-closure/reports/uat-i46-i53-graphrag-2026-05-03.md`](../53-graphrag-poc-closure/reports/uat-i46-i53-graphrag-2026-05-03.md). Ship-or-no-ship verdict: **NO-SHIP this cycle** (per `D-IH-46-Decision-P3-NO-SHIP-2026-05-03` in [`decision-log.md`](decision-log.md#decisions-made-during-execution)); cassettes preserved; live A/B forwarded as **OPS-53-1** to next AKOS_RECORD_LIVE cycle.
**Authoritative Cursor plan:** `~/.cursor/plans/i45-i46_eval_and_neo4j_6a72e6d7.plan.md`
**Predecessor:** [Initiative 7 — HLK Neo4j Graph Projection](../07-hlk-neo4j-graph-projection/master-roadmap.md) (built the projection) and [Initiative 32 P5/P6 — Topic axis + Neo4j extension](../32-holistik-ops-maturation/reports/p5-topic-axis-and-neo4j-extension-2026-04-30.md) (extended to 6 axes; D-IH-32-Q live sync proven 2026-05-01).
**Sister initiative:** [Initiative 45 — Live Eval Harness Modernisation](../45-live-eval-harness/master-roadmap.md) (parallel; I46 P3 + P6 use I45 P2 cassettes).

## Outcome

Write the missing doctrine for what Neo4j IS for at AKOS, then make small, opinionated investments where the doctrine says yes. Closes the unwritten-architecture gap that has accumulated across I7 → I23 → I25 → I32: every initiative extended the projection, none decided whether Neo4j should ALSO serve user/MADEIRA grounding (vs governance-only).

The phrase that triggered this initiative: *"speaking of neo4j, we need to properly think our approach on neo4j for the user and/or madeira. we've built a lot already"* (operator, 2026-05-01).

## The framing decision (re-stated)

The 2026 field has clear answers if we use the right framing. Neo4j is not one thing; it has three independent use-cases:

| Use-case | What it means at AKOS | Status today | I46 posture |
|:---------|:---------------------|:-------------|:------------|
| **A. Governance KG** | CSV-to-Neo4j projection of roles, processes, topics, personas, skills, policies (12 + 6 = 18 dimensions today) | Built and live | Keep + harden |
| **B. GraphRAG over the HLK vault** | MADEIRA queries Neo4j to ground answers in graph context (multi-hop, related-entity traversal), not just CSV row-lookups | Not built | Build a small, opinionated layer (PoC → conditional ship) |
| **C. Agent / user memory KG** | Temporal facts about user preferences, past sessions, conversation history, tenant-scoped memory | Not built | Defer with explicit trigger condition (write ADR, no build in I46) |

Background: per **Tianpan.co "GraphRAG in production 2026"**, *Neo4j Graphiti is explicitly NOT for document retrieval — it is for agent memory*. So the framing of "Neo4j" as one thing is itself the trap that has driven the unwritten doctrine.

## Why now

- **D-IH-32-Q closed proves the projection is production-grade** — both runs of `sync_hlk_neo4j.py` 2026-05-01 produced identical `roles_written: 65, processes_written: 1093, programs_written: 12, topics_written: 27, edges_written: 2330`. Idempotency is real.
- **MADEIRA does not currently consume Neo4j at routing time** — it has the optional `hlk_graph_*` MCP tools (per `agent-capabilities.json`) but no skill is wired to require them. We pay the projection cost and don't capture the value.
- **External repos (KiRBe, hlk-erp, boilerplate) ask "do you use Neo4j for user-facing things?"** — and we cannot give a doctrinal answer because we never wrote one. I32 cross-repo contracts (D-IH-32-K) implicitly answer "no, governance-only" but the operator wants this stated explicitly.
- **GraphRAG is not all-or-nothing** — the 2026 field has bifurcated into Microsoft GraphRAG (heavy: $50-200 indexing, 45min) and LightRAG (cheap: $0.50, 6000× fewer query tokens). Picking the right one is a doctrine decision.
- **Agent memory is being adopted broadly** (Mem0 49% LongMemEval, Zep/Graphiti 63.8% LongMemEval) but our use-case (governance assistant, not consumer chatbot) doesn't currently demand it. Saying "defer with trigger" instead of "no" or "yes" is the rigorous answer.

## Scope decisions

| In scope | Out of scope |
|:---|:---|
| Doctrine page `NEO4J_STRATEGY.md` in v3.0 vault under `Envoy Tech Lab/Neo4j/` (new sub-area) | Migrating away from Neo4j (HLK CSVs remain SSOT either way) |
| Use-case A hardening: 1 new MCP tool (`hlk_graph_skill_neighbourhood`), nightly drift canary, recurring idempotency proof | Use-case A schema redesign (closed by I32 P5/P6) |
| Use-case B PoC: 1-week LightRAG-style hybrid via `neo4j-graphrag-python`; A/B against `SKILL-MADEIRA-LOOKUP-V1` on 20 golden queries | Microsoft GraphRAG full adoption (D-IH-46-A alternative; revisit at I48 if PoC justifies) |
| Use-case C: ADR-only (defer with trigger condition; no build) | Building Zep-style temporal layer in I46 (D-IH-46-B alternative; trigger-gated) |
| `retrieval_mode` column on `SKILL_REGISTRY.csv` (graph_rag / vector_only / hybrid) — set in P5 if PoC ships | Multi-tenant memory scoping (waits on I34) |
| New POLICY_REGISTER row: `pol_neo4j_graph_rag_eligibility` per topic class (P5 conditional) | Cross-repo Neo4j sharing (KiRBe stays separate per D-IH-32-M) |
| Test wiring: GraphRAG cassettes via I45 P2 recorder; adversarial probes for graph escape | New Neo4j read endpoints beyond `hlk_graph_skill_neighbourhood` (incremental, not big-bang) |
| Drift-canary added to WIP dashboard (Neo4j node-counts vs CSV row-counts) | User-facing product surface ("does the deployed app query Neo4j?") — D-IH-46-G defers this |

## Asset classification (per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Paths | Rule |
|:------|:------|:-----|
| **New canonical (planning)** | `docs/wip/planning/46-neo4j-strategic-posture/{master-roadmap,decision-log,asset-classification,evidence-matrix,risk-register}.md` + `reports/` | Standard six-artifact contract |
| **New canonical (vault doctrine)** | `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md` (P1) | Vault-canonical with `language: en` |
| **New canonical (vault sub-area)** | `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/` directory itself | New sub-area; classified as `Tech / Envoy Tech Lab / Neo4j` |
| **New canonical (vault doctrine)** | `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md` (P4) | Architecture decision record with explicit trigger |
| **New canonical (registry column, conditional P5)** | `retrieval_mode` column added to `SKILL_REGISTRY.csv` | Set only if PoC ships |
| **New canonical (POLICY_REGISTER, conditional P5)** | `pol_neo4j_graph_rag_eligibility` per topic class | New `policy_class=graph_rag_eligibility` enum value |
| **New scripts** | `scripts/graphrag_poc.py` (P3) + `scripts/graphrag_drift_canary.py` (P2) | PoC + canary |
| **Modified canonical** | `prompts/overlays/OVERLAY_HLK_GRAPH.md` cites `NEO4J_STRATEGY.md` (P1) | Doctrine cross-reference |
| **Modified canonical** | `config/sync/kirbe-sync-contract.md` §11 cites `NEO4J_STRATEGY.md` (P1) | Cross-repo doctrine alignment |
| **Modified canonical** | `EXTERNAL_REPO_CONTRACT_TEMPLATE.md` (P1, optional) | If KiRBe/hlk-erp need Neo4j-related guidance, the template references the vault doctrine |
| **New CI** | Drift canary added to `verification-profiles.json` as `neo4j_governance_kg_drift_smoke` (P2) | Nightly + pre-commit |

## Phase plan (8 phases, ~2 weeks elapsed time)

| # | Phase | Output | Dependency |
|:--:|:------|:-------|:-----------|
| P0 | Bootstrap + audit | This initiative folder + 5 artifacts + `audit-current-neo4j-surface.md` evidence | — |
| P1 | Doctrine: `NEO4J_STRATEGY.md` | Vault doctrine page + cross-references in OVERLAY + kirbe-sync-contract + external repo contracts | P0 |
| P2 | Use-case A hardening | `hlk_graph_skill_neighbourhood` MCP tool + nightly drift canary + recurring idempotency proof in release-gate | P1 |
| P3 | Use-case B PoC | `scripts/graphrag_poc.py` + 20 golden queries + Langfuse-traced A/B run report | P1 (operator-funded budget — see R-46-1) |
| P4 | Use-case C ADR | `AGENT_MEMORY_DEFERRED_ADR.md` with trigger condition (operator picks one of 3 candidate triggers) | P1 |
| P5 | Conditional GraphRAG ship | If PoC meets bar, `retrieval_mode` column + `pol_neo4j_graph_rag_eligibility` row + `intent.py` integration | P3 (decision point) + I45 P3 (router refactor) |
| P6 | Test wiring | GraphRAG cassettes via I45 P2 recorder; adversarial probes; Neo4j health canary in WIP_DASHBOARD | I45 P2 |
| P7 | Tests + UAT + closure | New tests + UAT report + CHANGELOG + WIP_DASHBOARD re-render | All |

## Verification matrix

| Check | Profile | Cadence |
|:------|:--------|:--------|
| `validate_hlk.py` (full vault) | `pre_commit` | Every commit |
| `NEO4J_STRATEGY.md` cited by OVERLAY + kirbe-sync-contract + ≥1 external repo contract | new test in P1 | Every commit |
| `hlk_graph_skill_neighbourhood` MCP tool registered | new test in P2 | Every commit |
| Neo4j node counts ≈ CSV row counts (within ±1 row tolerance for in-flight syncs) | `neo4j_governance_kg_drift_smoke` | Nightly + pre-commit |
| `sync_hlk_neo4j.py` idempotency (2 consecutive runs same output) | `release_gate` | Per release |
| GraphRAG PoC scorecard (latency / cost / accuracy delta vs baseline) | manual P3 | Once at PoC + at conditional ship in P5 |

## Success metrics (closure conditions)

- `NEO4J_STRATEGY.md` lives in vault, cited by ≥3 other docs (OVERLAY, kirbe-sync-contract, ≥1 external repo contract)
- GraphRAG PoC outcome documented with concrete cost / latency / accuracy numbers (ship-or-no-ship decision logged in decision-log as D-IH-46-Decision-P3)
- Agent memory ADR signed, trigger condition selected by operator
- 1 skill running through GraphRAG hybrid retrieval (P5 conditional ship), OR a documented decision-not-to-ship with PoC numbers
- Neo4j drift canary green in WIP dashboard
- 1 new MCP tool (`hlk_graph_skill_neighbourhood`) operational

## Risks + rollback

See [`risk-register.md`](risk-register.md). Critical risk: PoC requires operator-funded LLM indexing budget for the vault — flagged as R-46-1 with ceiling proposal in P0.

## Reporting artifacts

- `reports/p<N>-*-YYYY-MM-DD.md` per phase (per AKOS convention)
- `reports/audit-current-neo4j-surface-2026-05-01.md` (P0 evidence)
- `reports/graphrag-poc-results-2026-05-XX.md` (P3 outcome)
- `reports/uat-i46-neo4j-strategic-posture-2026-05-XX.md` (P7 closure)

## Cross-cutting

- Decision IDs: `D-IH-46-A` through `D-IH-46-G` (7 seeded; user-ratified at greenlight 2026-05-01).
- All vault documents carry `language: en` frontmatter.
- WIP_DASHBOARD picks this row up automatically.
- CHANGELOG entry on closure (P7).

## What this is NOT

- Not a migration away from Neo4j.
- Not a Microsoft GraphRAG full adoption (PoC is LightRAG-style hybrid; D-IH-46-A).
- Not building Zep-style agent memory (D-IH-46-B defers).
- Not changing the user-facing product surface (D-IH-46-G defers).
- Not cross-merging KiRBe's local Neo4j with AKOS Neo4j (D-IH-32-M holds).
