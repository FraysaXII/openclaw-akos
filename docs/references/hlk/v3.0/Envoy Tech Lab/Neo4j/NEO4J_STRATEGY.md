---
language: en
status: active
intellectual_kind: doctrine
role_owner: System Owner
area: Tech / Envoy Tech Lab / Neo4j
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: canonical_doctrine
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# NEO4J_STRATEGY — what Neo4j IS for at AKOS

> **Status:** canonical doctrine (ratified 2026-05-01 as part of Initiative 46 P1).
> **Supersedes:** the implicit framing scattered across [`OVERLAY_HLK_GRAPH.md`](../../../../../prompts/overlays/OVERLAY_HLK_GRAPH.md), the I7/I23/I25/I32 master-roadmaps, and informal operator answers to "should we use Neo4j for X?".
> **Cross-referenced from:** OVERLAY (P1), [`kirbe-sync-contract.md`](../../../../../config/sync/kirbe-sync-contract.md) §11 (P1), [`EXTERNAL_REPO_CONTRACT_TEMPLATE.md`](../Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md) (P1).

## Summary

Neo4j is **one platform serving three independent use-cases**. Conflating them is the trap that has driven the unwritten doctrine across 4 prior initiatives. This page separates them, classifies each, and sets the decision-frame for new graph features.

| Use-case | Definition | Status today | Posture |
|:---------|:-----------|:-------------|:--------|
| **A. Governance KG** | CSV-to-Neo4j projection of governance dimensions (roles, processes, programs, topics, personas, channels, sourcing, skills, touchpoint-kit cells, policies, GOI/POI) | Built, idempotent (D-IH-32-Q proven 2026-05-01) | **Keep + harden** |
| **B. GraphRAG over the HLK vault** | LLM queries Neo4j to ground answers in graph context (multi-hop, related-entity traversal); used by MADEIRA for vault questions that exceed direct CSV row lookup | Not built | **PoC then conditional ship** (I46 P3, P5) |
| **C. Agent / user memory KG** | Temporal facts about user preferences, past sessions, conversation history, tenant-scoped memory | Not built | **Defer with explicit trigger ADR** (I46 P4) |

Background framing per **Tianpan.co "GraphRAG in production 2026"**: *Neo4j Graphiti is explicitly NOT for document retrieval — it is for agent memory*. So treating "Neo4j" as one thing routes us to the wrong pattern at every decision.

---

## Use-case A — Governance KG (the projection we have)

### What it is

`scripts/sync_hlk_neo4j.py` rebuilds a Neo4j graph from the HLK CSV vault on demand. The graph carries:
- **Node labels:** `:Role` (65), `:Process` (1100), `:Program` (12), `:Topic` (28), and the I32 P5/P6 axis-6 set: `:Persona` (16), `:Channel` (10), `:Sourcing` (1), `:Skill` (5), `:TouchpointKitCell` (15), `:Policy` (14)
- **Edge types:** `:OWNED_BY`, `:PARENT_OF`, `:UNDER_PROGRAM`, `:UNDER_TOPIC`, `:DEPENDS_ON`, `:CONSUMES`, plus role/process reporting edges
- **Read endpoints:** `GET /hlk/graph/summary`, `/hlk/graph/process/{item_id}/neighbourhood`, `/hlk/graph/role/{role_name}/neighbourhood`, `/hlk/graph/explorer` (HTML shell)
- **MCP tools:** `hlk_graph_summary`, `hlk_graph_process_neighbourhood`, `hlk_graph_role_neighbourhood` (3 today; +`hlk_graph_skill_neighbourhood` in I46 P2)
- **Total: ~2330 edges across 6 axes (incl. 14 program-side, 81 topic-side, 66 axis-6).**

### What it is FOR

- **Multi-hop governance queries** that are awkward in flat CSVs: "what skills depend on a topic that's owned by which role under which program?"
- **Visual exploration via the Streamlit explorer** (`scripts/hlk_graph_explorer.py`) for operator + auditor + new hire onboarding
- **Agent traversal as a complement to CSV lookup** when the answer is relational — not "what is the System Owner role definition" (CSV) but "who owns the process tree that touches the FinOps plane and the kirbe.* schema" (graph)
- **Drift detection** — if Neo4j node counts diverge from CSV row counts, something broke (the I46 P2 nightly canary)

### What it is NOT for

- **NOT the SSOT** — HLK CSVs in `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/` remain SSOT. Neo4j is rebuildable projection. Loss of the Aura instance = single `sync_hlk_neo4j.py` re-run away from full restoration.
- **NOT for KiRBe vault search** — KiRBe operates its own local Neo4j for tenant document search. AKOS Neo4j and KiRBe Neo4j **do not cross-merge** (D-IH-32-M). Two separate stores, two separate purposes, two separate cost lines.
- **NOT for agent memory** — that's use-case C. Different schema, different lifecycle, different access pattern.

### Doctrine for adding new node labels / edge types

A new dimension wanting a Neo4j projection follows this 4-step contract (codified in `akos.hlk_graph_model`):

1. The dimension has a canonical CSV under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/` with an akos field contract + validator.
2. Add the new `GraphLabel` + `EdgeType` enum members to `akos/hlk_graph_model.py`.
3. Add a `build_<dimension>_graph(registry) → (nodes, edges)` function.
4. Wire into `sync_hlk_naco4j.py` so the next `sync` re-run projects it.

If a new use case asks "should we add this to the graph?", answer with: **"Does it have a canonical CSV that already validates? If not, build that first; the graph is a downstream projection, not a SSOT."**

---

## Use-case B — GraphRAG over the HLK vault (the PoC, then conditional ship)

### What it is (would be)

A retrieval layer that lets MADEIRA answer vault questions by traversing the Neo4j graph + querying a vector store of HLK SOP / process / topic body text, then composing an LLM response grounded in the retrieved subgraph.

### Why we'd consider it

Per the **Neo4j GraphRAG Manifesto** + **Tianpan.co 2026 piece**, vector-only RAG fails on:
- Multi-hop questions (who owns the team that built product Y?)
- Causal / temporal chains (how did the FinOps process evolve through the I18→I19 transitions?)
- Related-entity grounding (return the role + the process + the policy in one coherent context, not 3 disconnected chunks)

Our HLK vault is ~1000 process rows + ~65 roles + ~30 dimensions + ~150 SOP / topic markdown files. **That's a small corpus** by the 2026 "500-page" benchmark — meaning we'd be a poor fit for **Microsoft GraphRAG** (heavy: $50-200 indexing, ~45min, 58% of tokens on entity extraction) and a good fit for **LightRAG-style hybrid** (cheap: $0.50/index, 6000× fewer query tokens; per Tianpan.co citation).

### Library choice (D-IH-46-A default)

[`neo4j-graphrag-python`](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) with a LightRAG-style hybrid pattern:
- Provider-agnostic LLM (Ollama / OpenAI / Anthropic / VertexAI / Mistral / Cohere)
- `VectorRetriever` for chunk-level, `GraphCypherQAChain` for relational
- Hybrid mode layers them: single-fact lookups stay fast (vector), relational queries traverse the graph (Cypher)

**Rejected alternatives** (operator-ratified D-IH-46-A):
- *Microsoft GraphRAG full*: overkill for our scale; cost-benefit doesn't justify hierarchical community summary approach
- *Build atop existing `hlk_graph_*` MCP tools*: would re-implement LightRAG primitives ourselves (4-6 weeks vs 1-week PoC)
- *Vector-RAG only* (e.g., pgvector + OpenAI embeddings): misses the multi-hop strength; we already paid the projection cost

### Decision-frame for ship vs no-ship

I46 P3 ships a 1-week PoC against `SKILL-MADEIRA-LOOKUP-V1` only. Bar (any-of):
- ≥3pp accuracy lift on 20 golden vault queries vs the current `hlk_role` + `hlk_search` chain
- ≥30% latency reduction
- ≥40% cost reduction

If bar met → P5 ships for 1 skill (operator-set `retrieval_mode=graph_rag` on the SKILL_REGISTRY row). If bar not met → P5 documents the decision-not-to-ship with the actual numbers; column added but inactive (revisit at I47).

### Doctrine for adding GraphRAG to other skills

Each `SKILL_REGISTRY` row carries a `retrieval_mode` column (added in I46 P5; values: `vector_only` / `graph_rag` / `hybrid` / empty=default). Promotion of a new skill to GraphRAG retrieval mode:
1. The skill's queries must show ≥3pp / 30% / 40% improvement on a per-skill golden query set
2. `pol_neo4j_graph_rag_eligibility_<topic_class>` policy must exist (operator-set per topic class)
3. Cassette regression suite must cover the new retrieval path

---

## Use-case C — Agent / user memory KG (deferred)

### What it would be

A Zep/Graphiti-style temporal knowledge graph storing per-user / per-tenant facts: preferences, past session conclusions, "what did we tell you 6 weeks ago", "your billing plan changed January 15". Time is a first-class dimension; every fact carries validity windows tracking when it became true and when superseded.

### Why we don't have one

- **Use-case absent today**: AKOS is single-operator; no multi-tenant load yet (Initiative 34 not started)
- **No conversational depth signal**: Madeira sessions today don't span N skills with cross-session continuity needs
- **No compliance ask yet**: no "what did we tell user X 6 weeks ago" request has landed

Per **AgentMarketCap "Agent Memory at Scale 2026"**: Mem0 (49% LongMemEval), Zep/Graphiti (63.8% LongMemEval — best benchmark), Cognee (multimodal ingest), Letta (90% token savings via virtual memory paging). **Buying when the trigger fires is cheaper than building before it does.**

### Trigger conditions (operator picks one in I46 P4 ADR)

1. **Multi-tenant load** — Initiative 34 closes
2. **Conversation depth** — a user session crosses N skills in 1 conversation (N TBD; Madeira UAT can baseline)
3. **Compliance ask** — Holistika legal / compliance asks "what did we tell user X 6 weeks ago"

When a trigger fires, a new initiative (I47+) evaluates Zep/Graphiti vs Mem0 vs in-house Neo4j layer. **Do not build agent memory in I46.**

---

## Cross-repo posture

| Repo | Has Neo4j? | Purpose | Cross-merge? |
|:-----|:-----------|:--------|:-------------|
| AKOS | Yes (Aura) | Governance KG (use-case A) | Authoritative for HLK doctrine |
| KiRBe | Yes (separate Aura) | Vault search (per `kirbe-sync-contract.md` §11 + I32 architecture audit) | **NO** — D-IH-32-M holds; AKOS Neo4j and KiRBe Neo4j stay separate |
| hlk-erp | No | — | — |
| boilerplate | No | — | — |

**D-IH-32-M (restated permanent)**: AKOS Neo4j and KiRBe Neo4j are independent stores with independent lifecycles. They serve different purposes (governance KG vs vault search). Cross-merging them would entangle two cost lines, two RLS regimes, and two upgrade cadences without product benefit. Revisit only when both products demand the same graph shape — not before.

---

## Cost / performance envelope

For operator planning:

| Operation | Today | Notes |
|:----------|:------|:------|
| Aura free tier ceiling | 200k nodes / 400k edges | We use ~2.3k edges; 0.6% of free ceiling |
| Full sync (rebuild) | ~10s on 1100-row vault | Idempotent (D-IH-32-Q) |
| `/hlk/graph/summary` | <100ms | Cached read |
| Process neighbourhood | <500ms | Bounded depth + limit |
| Future GraphRAG indexing (PoC scope) | ~$0.50-2.00 (LightRAG-style on small corpus) | One-time per re-index; capped by `GRAPHRAG_POC_USD_CEILING=$20` per R-46-1 |
| Future GraphRAG query | Comparable to vector-only (~6000× fewer tokens than Microsoft GraphRAG) | Per Tianpan.co 2026 piece |

Aura cost stays effectively $0 (free tier) until vault grows >100×. **Scale trigger** for self-hosted Neo4j: >200k nodes (free tier ceiling) OR Aura monthly cost >$50.

---

## Vendor lock-in posture

- **HLK CSV vault is SSOT** → Neo4j is rebuildable projection → loss of Aura = `sync` re-run away from full restoration
- **`neo4j-graphrag-python` is provider-agnostic on the LLM side** (D-IH-46-A) — no LLM lock-in
- **The Neo4j side is locked but Cypher is portable** to other graph stores with similar Cypher dialects (NebulaGraph, Memgraph). I46 does NOT support those backends; Initiative 47+ if scale demands

If Aura ever costs more than makes sense, migrate to self-hosted Neo4j (single VM; ~$30/mo). The doctrine is portable; only the ops bill changes.

---

## Operator-known gotchas

- **`AKOS_API_KEY` SPA fallback**: when no API key is set, `/hlk/graph/*` endpoints return the OpenClaw Control SPA HTML shell instead of JSON. Don't write tests that assume `Content-Type: application/json` without setting the API key in the test env.
- **Aura broken-chain TLS** (resolved D-IH-32-Q): some Aura-copy URI strings ship a different SSL cert chain than `neo4j+s://` expects. Use `NEO4J_TRUST=all` env or `neo4j+ssc://` URI variant. Documented in `akos/hlk_neo4j.py` `get_neo4j_driver()` docstring.
- **Aura password truncation** (lesson from D-IH-32-Q): copy passwords from the Aura console's modal **Copy** button, not from field-select-Ctrl+C — some browsers visually truncate the field. The HTTP 401 from the Aura Query API is the definitive signal that the password mismatches.
- **Post-restore Free-tier username** (I95 F6, 2026-06-09): after restoring from a `.backup` onto a new Aura Free instance, the console may issue credentials where **`NEO4J_USERNAME` equals the instance id** (e.g. `6c0d76bf`), not `neo4j`. AKOS preserves that username when it matches the URI host prefix (`akos/hlk_neo4j.py`). Do not force `neo4j` unless Browser login confirms it works.

---

## Backup exports (binary) vs doctrine (git)

| Class | Where it lives | Governed by |
|:------|:---------------|:------------|
| **Binary `.backup` exports** | Operator vault `%USERPROFILE%\.openclaw\vault\neo4j-backups\` — never git | I95 retention process ([`i95-neo4j-backup-retention-process-2026-06-09.md`](../../../../../docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-backup-retention-process-2026-06-09.md)); SHA256 sidecar required |
| **Strategy / runbook prose** | This file under legacy vault path `Envoy Tech Lab/Neo4j/`; forward governance home is `Admin/O5-1/Envoy Tech Lab` per area doctrine | [`COMPONENT_SERVICE_MATRIX.csv`](../../Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv) row `comp_i93_neo4j`; [`DATA_GOVERNANCE_POLICY.md`](../../Admin/O5-1/Data/Governance/canonicals/DATA_GOVERNANCE_POLICY.md) (git-canonical SSOT for schema; vault binaries are out-of-band) |

Graph sync (`scripts/sync_hlk_neo4j.py`) rebuilds use-case A from CSV SSOT — loss of Aura is one sync away from restoration; `.backup` files preserve live graph state beyond CSV projection when F6-style incidents require it.

---

## Cross-references

- **Overlay**: [`prompts/overlays/OVERLAY_HLK_GRAPH.md`](../../../../../prompts/overlays/OVERLAY_HLK_GRAPH.md) — the prompt-side companion that tells agents which graph tools exist
- **MCP server**: [`scripts/hlk_graph_mcp_server.py`](../../../../../scripts/hlk_graph_mcp_server.py) — the runtime tools surface
- **Driver**: [`akos/hlk_neo4j.py`](../../../../../akos/hlk_neo4j.py) — connection helpers + allowlisted reads
- **Sync**: [`scripts/sync_hlk_neo4j.py`](../../../../../scripts/sync_hlk_neo4j.py) — the projection rebuilder
- **Streamlit explorer**: [`scripts/hlk_graph_explorer.py`](../../../../../scripts/hlk_graph_explorer.py)
- **KiRBe sync contract** §11: [`config/sync/kirbe-sync-contract.md`](../../../../../config/sync/kirbe-sync-contract.md) — restates D-IH-32-M
- **External repo contract template**: [`../Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md`](../Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md)
- **Decision context**: D-IH-46-A through D-IH-46-G in [`docs/wip/planning/46-neo4j-strategic-posture/decision-log.md`](../../../../../docs/wip/planning/46-neo4j-strategic-posture/decision-log.md)
- **D-IH-32-M (KiRBe Neo4j separation)** in [`docs/wip/planning/32-holistik-ops-maturation/decision-log.md`](../../../../../docs/wip/planning/32-holistik-ops-maturation/decision-log.md)

## Review cadence

This doctrine is reviewed annually by System Owner (or when a new initiative wants to add to use-case A/B/C, whichever comes first). 90-day staleness alarm fires via `validate_localisation_frontmatter` (last_review field).
