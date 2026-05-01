---
language: en
status: active
initiative: 46-neo4j-strategic-posture
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 46 — Evidence Matrix

| ID | Observation | Source | Impact | Resolved by |
|:---|:------------|:-------|:-------|:------------|
| **E1** | Neo4j projection at AKOS has been extended in 4 initiatives (I7 base, I23 program axis, I25 topic axis, I32 6-axis) but no doctrine page explains what it IS for. The strategy is implicit. | Read of `prompts/overlays/OVERLAY_HLK_GRAPH.md` (overlay, not doctrine) + planning README scan | Operator + external teams cannot answer "should we use Neo4j for X?" without spelunking through 4 master-roadmaps | P1 NEO4J_STRATEGY.md |
| **E2** | MADEIRA does not consume Neo4j at routing time. `agent-capabilities.json` lists `hlk_graph_summary`, `hlk_graph_process_neighbourhood`, `hlk_graph_role_neighbourhood` for the `madeira` role, but no skill is wired to require them. | Read of `config/agent-capabilities.json` + grep `intent.py` for `neo4j` (zero hits) + read of `prompts/base/MADEIRA_BASE.md` "Allowed Tools" list (does not include `hlk_graph_*`) | We pay Aura cost + projection maintenance cost, capture zero MADEIRA value. The graph is a write-side investment with read-side latency. | P3 PoC + P5 conditional ship |
| **E3** | I32 P5/P6 extended the projection to 6 axes (skills, cells, policies, GOI/POI, channels, sourcing — 6 new node labels, `:UNDER_TOPIC` edges) but no MCP tool exposes these new dimensions. The graph knows about skills; the agents don't know how to ask. | Read of `scripts/hlk_graph_mcp_server.py` (3 tools: summary, process_neighbourhood, role_neighbourhood) | New axes are write-only at the MCP boundary; agents see them via `hlk_search` over CSVs but not via graph traversal | P2 add `hlk_graph_skill_neighbourhood` (and document the future expansion path) |
| **E4** | D-IH-32-Q live sync evidence (2026-05-01) confirms idempotency: 2 consecutive `sync_hlk_neo4j.py` runs produce identical output `{roles_written: 65, processes_written: 1093, programs_written: 12, topics_written: 27, edges_written: 2330}`. Production-grade. | Operator-pasted terminal `terminals/1.txt:841-981` | Use-case A (governance KG) is technically sound; gap is doctrine + reads, not the projection itself | P1 (doctrine) + P2 (more reads) |
| **E5** | The 2026 GraphRAG field has bifurcated into Microsoft GraphRAG (heavy: $50-200/index, ~45min, 58% of tokens on entity extraction) vs LightRAG (cheap: $0.50/index, 6000× fewer query tokens). Picking is a doctrine call. | Tianpan.co "GraphRAG in production 2026" web search (2026-05-01) | Without doctrine, the next "let's add GraphRAG" task could land Microsoft GraphRAG and cost $50-200 per re-index | P1 doctrine sets LightRAG-style as default; D-IH-46-A enforces |
| **E6** | Neo4j Graphiti (Zep) is explicitly NOT for document retrieval — it is for agent memory. Conflating use-case B (GraphRAG over the vault) with use-case C (agent memory) is a known industry trap. | Tianpan.co 2026 piece direct quote | Without separating the use-cases, an "add Neo4j" decision could pick the wrong tool entirely | P1 doctrine separates A/B/C; D-IH-46-A vs D-IH-46-B align tools to use-cases |
| **E7** | Agent memory benchmarks (2026): Mem0 49% LongMemEval, Zep/Graphiti 63.8% LongMemEval (best), Letta 90% token savings. We have zero memory today. | AgentMarketCap "Agent Memory at Scale 2026" web search | We don't have the use-case yet (single-session governance assistant), but if/when we do, building from scratch is expensive vs adopting these | P4 ADR-only with trigger condition |
| **E8** | KiRBe and hlk-erp ask "do you use Neo4j for user-facing things?" — and we have no doctrinal answer. I32 EXTERNAL_REPO_CONTRACT implicitly answers "no, governance-only" but the contract template doesn't link to a strategy doc. | I32 P7 + P8 cross-repo handoff bundles | External teams cannot align their own Neo4j decisions to ours; risk of drift | P1 doctrine + P1 cross-references in EXTERNAL_REPO_CONTRACT_TEMPLATE |
| **E9** | KiRBe has its own local Neo4j for vault search (per `kirbe-sync-contract.md` §11 + I32 architecture audit). D-IH-32-M decided "stays separate from AKOS Neo4j". We have no governance contract for what each Neo4j IS for. | I32 KiRBe architecture audit + D-IH-32-M | Without doctrine in P1, the next initiative might accidentally try to merge them | P1 doctrine explicitly states "AKOS Neo4j = governance KG; KiRBe Neo4j = vault search; do not merge" |
| **E10** | The HLK CSV vault is small (~1000 process rows + ~65 roles + ~30 dimensions ≈ small corpus per the 2026 cost piece). Microsoft GraphRAG is overkill; LightRAG is appropriate. | Read of `docs/references/hlk/compliance/dimensions/` + `process_list.csv` row count | Confirms the D-IH-46-A choice; if vault grows 100× (e.g., embedded Obsidian), revisit | P1 doctrine includes scale-trigger note |
| **E11** | Drift between Neo4j and CSV is currently caught only via `sync_hlk_neo4j.py` re-run (manual). No nightly canary. If a CSV is edited between syncs, Neo4j is stale and no alert fires. | Read of `verification-profiles.json` + `scripts/sync_hlk_neo4j.py` (manual invocation) | Stale graph could give MADEIRA wrong answers; no detection | P2 nightly drift canary + WIP_DASHBOARD surface |
| **E12** | I32 P9 added per-skill canaries via `eval_per_skill.py`; canary 3 (Langfuse trace shape > 3 skills) is shape-only. If GraphRAG ships in P5, it changes trace shape — canary 3 would either silently pass or noisily fail. | Read of `eval_per_skill.py` + I32 P9 report | P5 ship needs canary 3 promoted to semantic, not shape | P5 + I45 P5 alignment (semantic canary 3 belongs in I45 P5; cross-references here) |

## Cross-references to other initiatives

- **Initiative 7** — built the original Neo4j projection (E1, E4 origin).
- **Initiative 23** — added `:Program` (E1).
- **Initiative 25** — added `:Topic` (E1).
- **Initiative 32 P5/P6** — added 6 new node labels + `:UNDER_TOPIC` edges (E3, E4).
- **Initiative 32 P7** — KiRBe handoff (E9 source).
- **Initiative 45 P2** — cassette recorder (consumed by P6 here).
- **Initiative 45 P5** — adversarial cassettes (E12 cross-reference for canary 3 promotion).
- **Initiative 34 (future)** — multi-tenant memory (E7 trigger).
