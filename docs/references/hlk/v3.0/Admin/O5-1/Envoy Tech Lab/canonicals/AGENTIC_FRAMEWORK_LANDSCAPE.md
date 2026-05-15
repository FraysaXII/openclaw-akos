---
title: Agentic Framework Landscape
language: en
intellectual_kind: tech-lab-canonical
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - System Owner
  - Tech Lead
last_review: 2026-05-15
last_review_by: System Owner
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-F
  - D-IH-79-L
  - D-IH-79-M
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - SOP-TECH_AGENTIC_INFRA_001.md
linked_runbooks:
  - scripts/tech_agentic_landscape_audit.py
linked_processes:
  - env_tech_dtp_agentic_landscape_mtnce_001
companion_to:
  - ../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md
---

# Agentic Framework Landscape

> The Tech Lab side of the agentic governance split. This canonical carries the **how** of agent infrastructure — the framework names, the runtime choices, the embedder and transformer surfaces, the MCP wiring, the integration matrix. Where the People-side [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) explains the **why** and the **what**, this canonical lists the **how**.

This document is the canonical home of the technical vocabulary that the People-side canonicals deliberately avoid (per `D-IH-79-F` round-3 directive: jargon-side to Tech Lab, clarity-side to People, red-lines to Ethics; per `D-IH-79-M` Tech Lab landscape ownership; per `D-IH-79-N` anti-jargon drift gate scope is People-only). Framework names, runtime tokens, integration adapters, and stack-specific identifiers belong here. They do not belong in the People manifesto, the People agentic doctrine, the People agentic operations SOP, the People design pattern library, or the Ethics red-lines anchor. This boundary is mechanically enforced by [`scripts/validate_design_pattern_registry.py --jargon-scan`](../../../../../../../../scripts/validate_design_pattern_registry.py).

---

## §1 Framework sub-disciplines

The frameworks below are the canonical agentic sub-disciplines we track. Each row carries: **purpose** (what it is built for), **when we use it** (the situation that earns this framework), **risk** (what can go wrong if we lean on it without the appropriate care), and **link** (the upstream source we audit against). The list is curated, not exhaustive; new entries land via P4 cross-area breakthrough propagation when a successor initiative documents adoption.

| Framework | Purpose | When we use it | Risk | Link |
|:---|:---|:---|:---|:---|
| **LangChain** | General-purpose agent orchestration library; chains, tools, retrievers, memory abstractions | When a workflow needs glue between an LLM, a retriever, and a tool surface and we want a battle-tested abstraction layer | High API churn historically; pin versions; abstract behind our own helper modules so an upgrade does not rewrite our agent code | <https://github.com/langchain-ai/langchain> |
| **LangGraph** | Stateful agent workflow engine; explicit graph + checkpoints; built on LangChain primitives but with deterministic state semantics | When an agent workflow needs to be inspectable, replayable, or human-in-the-loop pausable | LangGraph is younger than LangChain; state-shape contract changes have downstream impact; pair with explicit migration tests | <https://github.com/langchain-ai/langgraph> |
| **LlamaIndex** | Retrieval-augmented generation framework; document loaders, vector stores, query engines | When the agent's primary task is reading a knowledge base and synthesising answers (the dominant Holistika usage today) | Indexer drift between document edits and the live index; pin index rebuild cadence and treat the index as a derived artefact | <https://github.com/run-llama/llama_index> |
| **OpenClaw** | Holistika's own internal agent runtime; thin adapter over upstream frameworks; carries our policy and observability hooks | When we need a Holistika-shaped wrapper that enforces our policy gates, our logging, and our governance posture; the default for in-employ agent work | Bootstrap drift (the wrapper aging behind the upstream framework it adapts); explicit upstream-version pinning; quarterly re-bless | Internal — see [`scripts/legacy/verify_openclaw_inventory.py`](../../../../../../../../scripts/legacy/verify_openclaw_inventory.py) |
| **CrewAI** | Multi-agent orchestration framework; role-named agents collaborating on tasks | When a workflow benefits from explicit role-named agents (e.g. "Researcher" + "Writer" + "Reviewer") rather than a single agent juggling roles | Role-naming overhead; useful when the role boundaries are real, noise when they are imposed for symmetry | <https://github.com/crewAIInc/crewAI> |
| **Ollama** | Local LLM runtime; pulls and serves open-weights models on operator hardware | When we want to keep prompts on local hardware (privacy, sensitive data), or when we are iterating on prompt patterns and want zero-cost trial | Local hardware constraints; open-weights models lag frontier proprietary models; use as a sandbox, not as the production runtime for customer-facing surfaces | <https://github.com/ollama/ollama> |
| **VercelAI** | Edge-deployed LLM runtime SDK; integrates with Next.js applications and the Vercel platform | When an agent surface lives inside a Next.js application (e.g. a `boilerplate/`-style public website widget); pairs with the Vercel deployment lane | Vendor lock-in to the Vercel platform; abstract the agent invocation behind our own helper so the runtime can be swapped | <https://sdk.vercel.ai/docs> |
| **Groq** | High-throughput LLM inference provider; serves frontier and open-weights models with low latency | When latency matters more than model selection (e.g. a real-time customer-facing chat surface); behind the same provider abstraction as the rest of the agent stack | Provider availability + rate limits; treat as one of many providers behind a shared interface, not as the only path | <https://groq.com> |

The list is **bounded by the operator's canonical 8** declared at I79 charter (`D-IH-79-F` round-3 directive). Successor frameworks (e.g. AutoGPT-derivatives, Anthropic SDK) are tracked as candidates in successor-initiative work; this canonical is revised when a successor initiative ratifies addition.

## §2 Knowledge base infrastructure (4 dimensions)

The KB layer is intentionally **agnostic by design** so that any one tooling choice can be swapped without rewriting the doctrine that depends on it. The four dimensions:

1. **Obsidian compatibility.** Every Markdown canonical is authored in Obsidian-compatible syntax (CommonMark + frontmatter; wikilink-or-relative-path discipline). The KB reads cleanly in Obsidian without conversion. This is the operator's "you must be able to read every canonical with no tool installed" mandate operationalised.
2. **Embedder-agnostic.** The vector embeddings derived from the KB live in a separate index; the canonicals stay plain text. Today's embedder is one of several candidates (OpenAI, Cohere, Voyage, BGE, sentence-transformers); tomorrow's is whatever the audit at the next quarterly review picks. The canonicals do not change when the embedder changes.
3. **Transformer-agnostic.** The LLM that consumes the embedded KB is one of several candidates (frontier proprietary, frontier open-weights via Groq, local via Ollama). The canonicals do not change when the LLM changes; the prompt-shape adapter changes.
4. **ERP-transformable.** The same canonicals are projected into the HLK-ERP relational schema (`compliance.*_mirror`, `kirbe.*` views) for SQL-side queries. The CSV canonicals are the SSOT; the ERP projection is a derived artefact. Edits land in CSVs; mirrors re-emit; ERP catches up.

These four dimensions are the operator's spec from I79 charter. They are stable surfaces; tooling within each dimension is replaceable.

## §3 MCP postures + tooling matrix

The Model Context Protocol (MCP) is the integration spine between Cursor, our agent runtimes, and external services (Supabase, Sentry, Langfuse, GitHub, Stripe, Neo4j, Slack, Composio, etc.). Each MCP server is classified by **posture** — what the agent is allowed to do via that surface. Four postures, in order of increasing autonomy:

| Posture | What the agent can do | When to grant | Example MCP servers (this repo, 2026-05) |
|:---|:---|:---|:---|
| **read** | Query, list, fetch, read-only enumeration. Cannot mutate state | Default for any new MCP server until trust is established | `user-langfuse-docs`, `user-llama_index_docs`, `user-postman_mcp_server`, `user-shopify-dev-mcp`, `user-sentry` (read-only queries) |
| **write** | Mutate state, create rows, update records, delete with confirmation | When the agent's named role explicitly carries the write mandate AND the canonical defining the role names the write surfaces | `plugin-supabase-supabase` (DDL + DML, gated by operator-SQL-gate); `user-github` (PRs, issues — gated by branch protection); `user-stripe` (test mode); `plugin-slack-slack` (post messages — gated by channel scope) |
| **suggest** | Propose actions to the operator without executing; the operator reviews and approves before mutation | When the action is high-blast-radius (production write, irreversible delete, financial operation) and warrants a human checkpoint regardless of the agent's named role | `cursor-ide-browser` (suggested clicks); `user-vercel` (suggested deploys); `user-runpod` (suggested resource allocations) |
| **decide** | Take action autonomously based on policy gates encoded in the agent's named role; operator audits after the fact | When the action is reversible, frequent, and well-bounded by the agent's role contract | Currently no MCP server is wired at the **decide** posture by default. Promotion to **decide** requires explicit ratification per the [People agentic doctrine](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) §4 cadence and Ethics review per [`ETHICAL_AGENTIC_BOUNDARIES.md`](../../People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) red-line 3 (no autonomous action on canonical CSVs without operator gate). |

The matrix above is non-exhaustive; the live MCP servers in `~/.cursor/projects/c-Users-Shadow-cd-shadow-openclaw-akos/mcps/` are the SSOT for what is configured. The matrix is curated for representative coverage of each posture so a Tech Lab review can spot whether a new MCP server is being added at the right posture or sneaking up the autonomy ladder without ratification.

## §4 Cross-references back to the People doctrine

This canonical is one corner of the agentic governance triangle. The other two corners:

- **The why and the what** — [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md). Why agents in our employ exist (extend Holistika's bandwidth without diluting the doctrine). What they do (named-role discipline-of-disciplines anchored in People). The Agent-in-Charge frame, the knowledge-test cadence, the Madeira role-class footnote.
- **The forbidden** — [`ETHICAL_AGENTIC_BOUNDARIES.md`](../../People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md). Eight red lines an agent must never cross. Sibling Ethics anchor to [`ETHICAL_AUTOMATION_POSTURE.md`](../../People/Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) (I70 P9 class-level posture).

The triangle is load-bearing. Revising one corner without the others creates drift. The cross-area breakthrough propagation SOP (P4 deliverable, `SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`) explicitly pings the Tech Lab landscape (this canonical) when the People agentic doctrine is revised substantively, so the framework rows above stay coherent with the People-side why.

## §5 Maintenance

Owned by **System Owner**. Co-authors: **Tech Lead**, **CTO** (forward-charted, not yet activated). Quarterly review default; off-cycle revision when:

- A new framework is adopted (audit row added).
- An existing framework is sunset (audit row removed; migration plan filed).
- An MCP server changes posture (suggest → write, write → decide).
- A KB infrastructure dimension is replaced (e.g. embedder swap).

Verified mechanically by the paired runbook [`scripts/tech_agentic_landscape_audit.py`](../../../../../../../../scripts/tech_agentic_landscape_audit.py) — confirms each framework row's upstream link still resolves, each MCP server posture matches its current configuration, and each `linked_canonicals` cross-reference resolves.

The anti-jargon drift gate ([`scripts/validate_design_pattern_registry.py --jargon-scan`](../../../../../../../../scripts/validate_design_pattern_registry.py)) does **not** apply to this canonical. Tech Lab canonicals legitimately carry framework jargon by design (per `D-IH-79-N` scope: People-only). The People-side canonicals are the gated surface; this one is the unfettered surface.

## §6 Cross-references

- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) — the People-side why.
- [`ETHICAL_AGENTIC_BOUNDARIES.md`](../../People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) — the Ethics-side red lines.
- [`SOP-TECH_AGENTIC_INFRA_001.md`](SOP-TECH_AGENTIC_INFRA_001.md) — paired SOP for Tech Lab agentic infrastructure operations.
- [`scripts/tech_agentic_landscape_audit.py`](../../../../../../../../scripts/tech_agentic_landscape_audit.py) — paired runbook.
- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md) — the People manifesto framing both halves of the agentic split.
- [`PRECEDENCE.md`](../../People/Compliance/canonicals/PRECEDENCE.md) — registers this canonical.
