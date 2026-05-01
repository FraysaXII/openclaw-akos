---
language: en
status: active
initiative: 46-neo4j-strategic-posture
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 46 — Decision Log

Seven decisions seeded with default positions per the cursor plan; ratified by operator at greenlight (2026-05-01 04:30 CET).

## D-IH-46-A — GraphRAG layer choice: `neo4j-graphrag-python` with LightRAG-style hybrid retrieval

**Decision:** Use [neo4j-graphrag-python](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) (provider-agnostic; supports Ollama / OpenAI / Anthropic / VertexAI / Mistral / Cohere) with a LightRAG-style hybrid retrieval pattern (vector + graph traversal, dual-level keys, no community clustering).

**Alternatives considered:**
- **Build atop existing `hlk_graph_*` MCP tools** (no new dependency). Rejected: those are role/process/program-shaped neighbourhood queries; not a retrieval framework. Would require building the LightRAG primitives ourselves (4-6 weeks vs 1-week PoC).
- **Microsoft GraphRAG (full)** — heavy: $50-200 per 500-page corpus indexing, 58% of indexing tokens consumed by entity extraction alone (per Tianpan.co 2026 piece). Rejected: overkill for our scale (~1000 process rows + ~65 roles + ~30 dimensions ≈ small corpus); cost-benefit doesn't justify Microsoft's hierarchical community summary approach.
- **No GraphRAG, vector-RAG only** (e.g., pgvector + OpenAI embeddings against a flattened CSV). Rejected: misses the multi-hop / related-entity strength of having a graph; we already paid the projection cost in I7 + I23 + I25 + I32.

**Rationale:** LightRAG-style hybrid is the right cost-efficiency tier for our scale; `neo4j-graphrag-python` keeps the LLM provider open (matches our model-tiers approach); we already have the graph (free upside).

**Reversibility:** High — provider-agnostic; could swap to alternative retrieval framework or fall back to vector-only via SKILL_REGISTRY's `retrieval_mode` column.

---

## D-IH-46-B — Agent memory in I46: defer (write ADR, no build)

**Decision:** Use-case C (agent / user memory KG) is **deferred** in I46. P4 ships an Architecture Decision Record (`AGENT_MEMORY_DEFERRED_ADR.md`) with an explicit trigger condition. When the trigger fires, a future initiative will evaluate Zep/Graphiti vs Mem0 vs in-house Neo4j layer.

**Trigger candidates (operator picks one in P4):**
1. **Multi-tenant load** — when Initiative 34 closes, persistent per-tenant memory becomes a real ask.
2. **Conversation depth** — a user session crosses N skills in 1 conversation (N TBD; can baseline from Madeira UAT).
3. **Compliance ask** — "what did we tell user X 6 weeks ago?" lands as a Holistika legal/compliance request.

**Alternatives considered:**
- **Build minimal Zep-like temporal layer in our existing Neo4j** (~3-week effort, ~$0 incremental Aura cost). Rejected for I46: blocks I46 closure (already 8 phases) and ships a half-built memory system that may need Initiative 34 context to scope correctly.
- **Adopt Zep/Graphiti (managed)** — per AgentMarketCap 2026, 63.8% LongMemEval (best benchmark). Rejected for I46: external dependency in production with no current use-case; revisit when trigger fires.

**Rationale:** Building agent memory before there's a user need produces a half-built system that costs maintenance with no return. Trigger-gated defer is the rigorous posture. Per the cursor plan §"Field grounding" Tianpan.co citation: *Neo4j Graphiti is explicitly for agent memory, NOT document retrieval* — confirms we shouldn't conflate use-case B (P3) with use-case C.

**Reversibility:** N/A (defer is reversible by definition once trigger fires).

---

## D-IH-46-C — `NEO4J_STRATEGY.md` lives in vault as canonical doctrine

**Decision:** The doctrine page lives at `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md` with `language: en` frontmatter, classified as `intellectual_kind: doctrine`.

**Alternatives considered:**
- **Live in `config/architecture/`** — config-canonical, less discoverable, doesn't enter the brand jargon audit / language frontmatter discipline.
- **Live in `docs/wip/planning/46-neo4j-strategic-posture/` only** — planning-canonical (transient lifecycle); doctrine should outlive the initiative that authored it.

**Rationale:** Doctrine is permanent; vault is the right home. Brand-jargon audit applies (must not contain forbidden tokens for any external-prose section). Cross-referenced by KiRBe/hlk-erp via `EXTERNAL_REPO_CONTRACT_TEMPLATE.md` updates in P1.

**Reversibility:** Low (doctrine moves are governed via PRECEDENCE.md + alias map per I32 P7 pattern).

---

## D-IH-46-D — A/B PoC routes through MADEIRA only

**Decision:** P3 PoC swaps `SKILL-MADEIRA-LOOKUP-V1`'s retrieval path from current (`hlk_role` + `hlk_search` chain) to GraphRAG hybrid; runs both A and B against the same 20 golden queries; compares latency / cost / accuracy.

**Alternatives considered:**
- **Also Architect** — broader signal, more risk. Rejected: Architect's prompts are bigger surface area; PoC ambiguity grows non-linearly.
- **All 5 skills** — rejected: cassette recording cost × 5 skills × 2 retrieval modes = 10× the spend.

**Rationale:** MADEIRA is the highest-value-per-query skill (operator-facing dashboard) and has the most direct user-perceived signal. Single skill keeps the PoC scope honest.

**Reversibility:** High (extending to other skills is incremental).

---

## D-IH-46-E — Successful PoC ships for 1 skill in P5

**Decision:** If P3 PoC meets ≥1 of the bars (≥3pp accuracy lift OR ≥30% latency reduction OR ≥40% cost reduction), ship the GraphRAG retrieval mode for `SKILL-MADEIRA-LOOKUP-V1` only. Other skills opt-in case-by-case in future initiatives.

**Alternatives considered:**
- **Ship for the topic class** (all topic_*-bound skills). Rejected: most other skills (`SKILL-ARCHITECT-PLAN-V1`, `SKILL-EXECUTOR-RUN-V1`, etc.) don't have a graph-traversal natural fit; would force GraphRAG on inappropriate paths.
- **Ship for none even if PoC succeeds** (PoC as exploration only). Rejected: a green PoC must convert to action or it's wasted; the operator framing was "let's go all out".

**Rationale:** 1 skill → real production signal → informs whether to expand. PoC-then-ship is the lighter-weight version of the standard "build a thing, see if it sticks, expand if it does" pattern.

**Reversibility:** High — flip the SKILL_REGISTRY row's `retrieval_mode` back to `vector_only`.

---

## D-IH-46-F — Add a dedicated Neo4j sub-area in vault (`Envoy Tech Lab/Neo4j/`)

**Decision:** New vault sub-directory `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/` houses both `NEO4J_STRATEGY.md` (P1) and `AGENT_MEMORY_DEFERRED_ADR.md` (P4) and serves as the canonical home for future Neo4j doctrine.

**Alternatives considered:**
- **Nest under existing `Envoy Tech Lab/Repositories/`** — clutters the repo registry with non-repo doctrine.
- **Top-level `docs/references/hlk/v3.0/Neo4j/`** — breaks the existing role-based vault structure (`Admin/`, `Envoy Tech Lab/`, `Operations/`).

**Rationale:** Symmetry with the existing vault structure (each role has its area; Tech / Envoy Tech Lab is the System Owner area; Neo4j is a Tech sub-concern).

**Reversibility:** Low (vault moves are governed; see I32 P7).

---

## D-IH-46-G — User-facing surface: not in I46 scope

**Decision:** Whether the deployed Holistika product (boilerplate / future client surfaces) queries Neo4j when a user asks something is **not in I46 scope**. I46 is doctrine + back-end PoC only. Product surface decisions are in product-team territory.

**Alternatives considered:**
- **Include a UX phase** that decides what to expose via the public web. Rejected: too cross-functional for I46; conflates governance doctrine with product UX.

**Rationale:** Doctrine should be product-agnostic (the same rules apply whether the consumer is MADEIRA-the-internal-assistant or Holistika.com-the-public-site). Product team can consume the doctrine when ready.

**Reversibility:** N/A (defer is reversible by adding a future initiative).

---

## Decisions deferred (out of I46 scope, candidates for I47+)

- **D-DEFER-46-α** — Microsoft GraphRAG full adoption (see D-IH-46-A alternative).
- **D-DEFER-46-β** — Build agent memory layer in Neo4j (see D-IH-46-B alternative; trigger-gated).
- **D-DEFER-46-γ** — Cross-repo Neo4j sharing (KiRBe's local Neo4j stays separate per D-IH-32-M).
- **D-DEFER-46-δ** — Public/product Neo4j surface (D-IH-46-G; product-team territory).
- **D-DEFER-46-ε** — Per-tenant retrieval mode (waits on Initiative 34 multi-tenancy).

---

## Decisions made during execution

These will be appended as P3 PoC outcomes land (e.g., `D-IH-46-Decision-P3-2026-05-XX` with the actual measured numbers and the ship/no-ship verdict).
