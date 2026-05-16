---
report_id: i84-p1-substrate-landscape-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 §3.5 successor pick-up
phase: P1
initiative: INIT-OPENCLAW_AKOS-84
linked_decisions: [D-IH-84-A, D-IH-84-B, D-IH-84-C, D-IH-84-D, D-IH-84-E, D-IH-84-F, D-IH-84-G]
linked_evidence: i86-sc-resume-wave2-architectural-2026-05-16.md;AGENTIC_FRAMEWORK_LANDSCAPE.md;i76-madeira-elevation.md
access_level: 4
confidence_level: B2
source_taxonomy: holistika-internal-research-synthesis
language: en
---

# I84 P1 — Substrate landscape audit (2026-Q2)

> **Scope (per sc-resume Wave 2 §3.5).** Operator-readable substrate-landscape audit covering the substrates AKOS, MADEIRA, and KiRBe could plausibly run on as of 2026-Q2. Each substrate carries a structured attribute row aligned with the proposed [`SUBSTRATE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/) 18-column schema (per `D-IH-84-F` in [`decision-log.md`](../decision-log.md)) so that P3 canonical mint — if ratified — can seed directly from these rows without re-derivation. This is the **slimmed-down operator-readable form** of the [master-roadmap §3 P1](../master-roadmap.md) Tier-1 WIP dossier; the full 4-thread audit (agent-SDKs + competitive layer + regulatory/ToS + past-PoC translation) is deferred to a future chat per the I86 Wave 2 chat-boundary discipline.

## 1. Audit method and confidence posture

This audit blends two source classes:

1. **Repo synthesis** (confidence **A1** — Holistika canonical SSOT). The existing 8 framework rows in [`AGENTIC_FRAMEWORK_LANDSCAPE.md` §1](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) and the architectural framings in [`i76-madeira-elevation.md` §2](../../_candidates/i76-madeira-elevation.md) (F1–F5 AIC patterns) plus the OpenClaw thin-adapter description in [`scripts/legacy/verify_openclaw_inventory.py`](../../../../scripts/legacy/verify_openclaw_inventory.py).
2. **External knowledge synthesis** (confidence **B2** — Holistika-internal-research-synthesis from agent training corpus, not live-web fetched in this chat). Vendor names, runtime shapes, license posture, pricing-class, and 2026-Q2 status claims are flagged **`[ext]`** in the per-row notes and should be re-verified at the master-roadmap-grade P1 audit before any row writes to `SUBSTRATE_REGISTRY.csv` as `confidence_level: A1`.

The audit deliberately **does not** make architectural decisions. It produces evidence to feed the P4 batched ratification (`D-IH-84-B/C/D/E`). Per [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) §"When NOT to use" — architectural decisions surfaced mid-execution must stop-and-clarify, not be inferred from audit prose alone.

### Out-of-scope for this chat (deferred to master-roadmap P1)

The following audit threads from [master-roadmap §3 P1](../master-roadmap.md) are explicitly **not** in this report:

- Competitive layer (Glean, Notion AI, Anthropic Projects, OpenAI Apps SDK, Microsoft Copilot Studio, Google Gemini for Workspace, Composio, Lindy) — needs dedicated `competitive-layer-positioning.md` Tier-1 WIP under `docs/wip/intelligence/substrate-audit-2026-Q2/`.
- Regulatory layer (EU AI Act provider-vs-deployer 2026 enforcement, GDPR-as-SaaS DPA cascading, Cursor MSA evolution forecast, IP-indemnity carve-outs) — needs dedicated `regulatory-tos-forecast.md`.
- Past-PoC translation matrix (LlamaIndex-era Madeira retrospective, KiRBe-still-on-LlamaIndex assessment, I10/I11/I12/I13 active-stack synthesis, R&L v2.7 PoC catalogue) — needs dedicated `past-poc-translation-matrix.md`.

These threads are surfaced as P3 entry options (see [`p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) §7 closing decision).

## 2. Substrate taxonomy (3 classes; 18 substrates audited)

Three substrate classes carry meaningfully different governance profiles:

1. **Framework substrates** — code libraries imported into a host process; the host owns the runtime, the framework provides primitives. Examples: LangChain, LlamaIndex, CrewAI, LangGraph.
2. **Agent-SDK substrates** — vendor-managed agent-execution runtimes accessed via SDK + (often) hosted backend. The vendor owns the runtime; the SDK is the integration surface. Examples: Cursor SDK, Claude Code SDK, OpenAI Agents SDK, Devin, Replit Agent.
3. **Architectural-posture substrates** — not vendors but **patterns** for combining the above. Examples: OpenClaw thin-adapter (Holistika's current default), MADEIRA-direct (build-your-own runtime per the LlamaIndex-era pattern KiRBe still uses), Hybrid (Cursor SDK frontend + OpenClaw policy backend per `D-IH-84-B` Option B3).

The class distinction matters because:

- Framework substrates are **substitutable** — swap LangChain for LlamaIndex with adapter shim work; AKOS-as-SSOT is preserved because the framework is library-shape.
- Agent-SDK substrates are **opinionated** — the vendor's agent lifecycle, persistence model, tool-protocol, and observability surface are taken as-given. AKOS-as-SSOT must be projected through the SDK's contracts; risk of leakage.
- Architectural-posture substrates are **structural commitments** — they determine which class above the operator's day-to-day reaches. They are the load-bearing choice the founder directive 2026-05-16 named.

## 3. Class 1 — Framework substrates (8 rows; existing AGENTIC_FRAMEWORK_LANDSCAPE roster)

These 8 rows are the canonical Tech-Lab roster per `D-IH-79-F` round-3 directive + `D-IH-79-M` Tech-Lab ownership. Each row below preserves the existing landscape canonical's purpose + when-we-use + risk + link triple and adds the audit attributes the P3 SUBSTRATE_REGISTRY would require.

### 3.1 LangChain

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-LANGCHAIN-AI-LANGCHAIN` |
| `vendor` | LangChain AI |
| `runtime_shape` | `framework-library-python` (also TS via `@langchain/core`) |
| `persistence_model` | `ephemeral` (per-process; persistence is a userland concern) |
| `tool_protocol` | `langchain-native` (Tool/Toolkit abstractions); MCP via community adapter `[ext]` |
| `license_class` | `open-source-mit` (MIT) `[ext]` |
| `status` | `active` (most-adopted general-purpose agent library; mature) |
| `cost_class` | `bring-your-own-key` (LLM costs flow through configured provider) |
| `akos_integration_state` | `in-production` (under OpenClaw wrapper for some adapters) |
| `madeira_productization_role` | `library-import` (would be a dep of `@holistika/madeira-agent` if F4 single-agent shape) |
| `aic_pattern_role` | `dispatcher` (F3) | also `sub-agent` (F1) via LangGraph extension |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://github.com/langchain-ai/langchain |
| `notes` | High API churn historically; pin versions per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column. v0.3 stable as of 2026-Q2 `[ext]`. |

### 3.2 LangGraph

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-LANGCHAIN-AI-LANGGRAPH` |
| `vendor` | LangChain AI |
| `runtime_shape` | `orchestration-engine` (stateful agent workflow engine; built on LangChain primitives but with explicit graph + checkpoints) |
| `persistence_model` | `session-scoped` (checkpoint-based; can persist via configured store) |
| `tool_protocol` | `langchain-native` |
| `license_class` | `open-source-mit` `[ext]` |
| `status` | `active` (younger than LangChain; rapidly maturing; LangGraph Platform GA `[ext]`) |
| `cost_class` | `bring-your-own-key` + optional `seat-billed` (LangGraph Cloud hosted runtime) `[ext]` |
| `akos_integration_state` | `pilot` (candidate for stateful-workflow needs e.g. governance-cascade flows) |
| `madeira_productization_role` | `library-import` (if F3 ad-hoc-dispatcher MADEIRA shape ratified) |
| `aic_pattern_role` | `dispatcher` (F3 native fit — tool-call subgraphs) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://github.com/langchain-ai/langgraph |
| `notes` | Pair with explicit migration tests per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column. Cited as F3 native fit in [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2. |

### 3.3 LlamaIndex

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-RUN-LLAMA-LLAMAINDEX` |
| `vendor` | run-llama / LlamaIndex |
| `runtime_shape` | `framework-library-python` (document loaders, vector stores, query engines) |
| `persistence_model` | `persistent` (index is the persistence — built once, queried many) |
| `tool_protocol` | `langchain-native`-compatible + `native-only` for advanced workflows |
| `license_class` | `open-source-mit` `[ext]` |
| `status` | `active` (dominant RAG framework in Holistika usage today; LlamaIndex Workflows GA 2026 `[ext]`) |
| `cost_class` | `bring-your-own-key` for LLM + storage costs |
| `akos_integration_state` | `in-production` (KiRBe runs on LlamaIndex era stack per `MADEIRA-AKOS/STATUS.md` historical note + founder framing 2026-05-16: *"KiRBe is still on the LlamaIndex-era stack"*) |
| `madeira_productization_role` | `library-import` (Madeira-on-LlamaIndex was the original shape pre-OpenClaw) |
| `aic_pattern_role` | `not-applicable` (LlamaIndex is RAG-side, not orchestration-side; pairs with an orchestrator) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://github.com/run-llama/llama_index |
| `notes` | Indexer drift between document edits and live index per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column — pin index rebuild cadence; treat index as derived artefact. KiRBe is the load-bearing reason this row stays active in AKOS even though OpenClaw is the current default. |

### 3.4 OpenClaw

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-HOLISTIKA-OPENCLAW` |
| `vendor` | Holistika (internal) |
| `runtime_shape` | `framework-library-python` (thin adapter over upstream frameworks; carries Holistika policy + observability hooks) |
| `persistence_model` | `ephemeral` (inherited from host process; persistence delegated to upstream adapters) |
| `tool_protocol` | `mcp` (primary) + framework-native (per upstream adapter) |
| `license_class` | `commercial-license` (Holistika-internal; not open-sourced) |
| `status` | `active` (Holistika's default agent runtime; quarterly re-bless cadence per AGENTIC_FRAMEWORK_LANDSCAPE.md §1) |
| `cost_class` | `bring-your-own-key` (proxies to whichever upstream framework + LLM provider) |
| `akos_integration_state` | `in-production` (the load-bearing substrate for AKOS today; verified via [`scripts/legacy/verify_openclaw_inventory.py`](../../../../scripts/legacy/verify_openclaw_inventory.py)) |
| `madeira_productization_role` | `agent-runtime` (Madeira-on-OpenClaw is the current shape post-LlamaIndex-era migration) |
| `aic_pattern_role` | `not-applicable` natively but adaptable to any of F1-F5 via upstream framework choice |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | Internal (see `verify_openclaw_inventory.py`) |
| `notes` | **Load-bearing substrate for AKOS.** Bootstrap drift risk: the wrapper aging behind the upstream framework it adapts (per `R-IH-84-bootstrap-drift` not yet minted). Founder framing 2026-05-16: *"why we're currently on OpenClaw instead of our own build like Madeira was in the LlamaIndex days like KiRBe still is"*. This row is the **B1 anchor** of `D-IH-84-B` (stay-on-OpenClaw). |

### 3.5 CrewAI

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-CREWAI-INC-CREWAI` |
| `vendor` | CrewAI Inc. |
| `runtime_shape` | `framework-library-python` (multi-agent orchestration; role-named agents collaborating on tasks) |
| `persistence_model` | `session-scoped` (crew + task state lives per execution) |
| `tool_protocol` | `langchain-native` + `native-only` |
| `license_class` | `open-source-mit` + Enterprise tier `[ext]` |
| `status` | `active` (CrewAI Enterprise GA `[ext]`; community version stable) |
| `cost_class` | `bring-your-own-key` (core) + `seat-billed` (Enterprise) `[ext]` |
| `akos_integration_state` | `pilot` (candidate if F2 peer-companion AIC framing ratified) |
| `madeira_productization_role` | `library-import` (if F2 wins) |
| `aic_pattern_role` | `peer` (F2 — native fit for "team of AICs" framing per [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2 F2 row) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://github.com/crewAIInc/crewAI |
| `notes` | Role-naming overhead per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column. Cited as F2 native fit; "team" rhetoric maps directly to crew abstraction. |

### 3.6 Ollama

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-OLLAMA-OLLAMA` |
| `vendor` | Ollama Inc. |
| `runtime_shape` | `inference-provider` (local LLM runtime; pulls and serves open-weights models on operator hardware) |
| `persistence_model` | `persistent` (model weights cached locally; conversation state per-request) |
| `tool_protocol` | `openai-functions` (OpenAI-compatible API surface) |
| `license_class` | `open-source-mit` (Ollama itself) + `open-weights-model` (served models vary) `[ext]` |
| `status` | `active` (Holistika's local-iteration sandbox; per `process_list.csv` env_tech_* rows) |
| `cost_class` | `free-tier-only` (operator hardware cost only; no per-token billing) |
| `akos_integration_state` | `in-production` (sandbox tier; not production customer-facing) |
| `madeira_productization_role` | `backend-only` (LLM serving layer; not architectural) |
| `aic_pattern_role` | `not-applicable` (substrate-layer, not orchestration-layer) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://github.com/ollama/ollama |
| `notes` | Per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column — local hardware constraints; open-weights models lag frontier proprietary models. Use as sandbox, not production. |

### 3.7 VercelAI

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-VERCEL-VERCEL-AI-SDK` |
| `vendor` | Vercel Inc. |
| `runtime_shape` | `agent-sdk-typescript` (edge-deployed LLM runtime SDK; integrates with Next.js + Vercel platform) |
| `persistence_model` | `session-scoped` (edge function lifecycle) |
| `tool_protocol` | `openai-functions` + Vercel-native streaming primitives |
| `license_class` | `open-source-mit` (SDK) + `proprietary-saas` (Vercel platform) `[ext]` |
| `status` | `active` (Vercel AI SDK v4 GA `[ext]`; default for Next.js-deployed agent surfaces) |
| `cost_class` | `bring-your-own-key` (LLM) + `seat-billed` (Vercel hosting) |
| `akos_integration_state` | `pilot` (candidate for `boilerplate/`-style public website widgets; `hlk-erp` operator surfaces) |
| `madeira_productization_role` | `agent-runtime` (if MADEIRA ever ships as in-page web widget) |
| `aic_pattern_role` | `single-agent-rich-tools` (F4 fit — SDK is designed for single-agent flows) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://sdk.vercel.ai/docs |
| `notes` | Vendor lock-in to Vercel platform per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column. Abstract agent invocation behind helper layer so runtime can be swapped. |

### 3.8 Groq

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-GROQ-GROQ-CLOUD` |
| `vendor` | Groq Inc. |
| `runtime_shape` | `inference-provider` (high-throughput LLM inference; LPU-backed low-latency serving) |
| `persistence_model` | `ephemeral` (per-request; no built-in session state) |
| `tool_protocol` | `openai-functions` (OpenAI-compatible API surface) |
| `license_class` | `proprietary-saas` (Groq Cloud) + `open-weights-model` (Llama family, Kimi, etc. served) `[ext]` |
| `status` | `active` (used as one provider behind shared LLM-provider abstraction) |
| `cost_class` | `token-billed` (very low per-token; flagship Groq pricing advantage) `[ext]` |
| `akos_integration_state` | `in-production` (one of several providers behind shared interface per `model_catalog.py`) |
| `madeira_productization_role` | `backend-only` |
| `aic_pattern_role` | `not-applicable` |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://groq.com |
| `notes` | Provider availability + rate-limit risk per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column. Treat as one of many providers behind shared interface. |

## 4. Class 2 — Agent-SDK substrates (7 rows; net-new vs existing landscape)

These 7 substrates are **not** in the existing AGENTIC_FRAMEWORK_LANDSCAPE roster. They represent the 2025-2026 generation of vendor-managed agent-execution runtimes the founder directive 2026-05-16 named as "the future not only of our agentic stance or what exactly Madeira will be made of". Adding any of these rows to the landscape canonical (P3 deliverable) requires the cross-coherence check in master-roadmap §4 P3.

### 4.1 Cursor SDK (Anysphere)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-ANYSPHERE-CURSOR-SDK` |
| `vendor` | Anysphere Inc. |
| `runtime_shape` | `agent-sdk-typescript` + `agent-sdk-python` (multi-agent, multi-repo, parallel-agent-fleet capabilities `[ext]`) |
| `persistence_model` | `cloud-managed` (Cursor backend persists agent state + transcripts; operator-readable via Cursor app) |
| `tool_protocol` | `mcp` (Cursor is the canonical MCP integration surface) + `cursor-native` (subagent dispatch, browser-use, etc.) |
| `license_class` | `proprietary-saas` (Anysphere) `[ext]` |
| `status` | `active` but **SDK in beta** as of 2026-Q2 `[ext]`; Cursor 3 ("Glass") GA 2026-04-02 per founder directive 2026-05-16 |
| `cost_class` | `seat-billed` ($20/user Pro; $40/user Business `[ext]`) + LLM costs included up to plan limit |
| `akos_integration_state` | `pilot` (the operator's day-to-day MADEIRA-as-Cursor-agent interactions empirically embody this per `D-IH-70-V`); SDK not yet wired into AKOS production paths |
| `madeira_productization_role` | `agent-runtime` (if MADEIRA productizes as a Cursor-SDK-backed agent; relates to `D-IH-84-D`) |
| `aic_pattern_role` | `supervisor` + `sub-agent` (F1 native fit — `subagent_types`: explore, browser-use, render-assistant per [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2 F1 row) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://cursor.com/docs (live), https://cursor.com/sdk `[ext]` |
| `notes` | **The center of gravity for `D-IH-84-B`.** Anysphere reportedly at $2B ARR with 60% enterprise penetration `[ext]`; Composer 2 built on Moonshot Kimi 2.5 `[ext]`. Beta SDK status is the **competitive window** the founder directive named: *"the fact that even Cursor SDK is in beta is something we need to capitalize"*. Vendor lock-in + license/ToS exposure are the load-bearing risks (per `R-IH-84-3`+`R-IH-84-4` proposed). |

### 4.2 Claude Code SDK (Anthropic)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-ANTHROPIC-CLAUDE-CODE-SDK` |
| `vendor` | Anthropic |
| `runtime_shape` | `agent-sdk-typescript` + `agent-sdk-python` (single-agent + rich-tools architecture `[ext]`) |
| `persistence_model` | `session-scoped` (conversation-window-bound; Anthropic Projects extends via Files/MCP) |
| `tool_protocol` | `anthropic-tools` + `mcp` (Anthropic is one of the MCP standard's primary backers) |
| `license_class` | `proprietary-saas` (Anthropic) `[ext]` |
| `status` | `active` (Claude Code GA 2025; SDK matured 2026-Q1 `[ext]`) |
| `cost_class` | `token-billed` (Claude pricing; high per-token but high capability) `[ext]` |
| `akos_integration_state` | `forecasted` (candidate substrate; not currently wired into AKOS production) |
| `madeira_productization_role` | `agent-runtime` (alt to Cursor-SDK if F4 single-agent shape wins) |
| `aic_pattern_role` | `single-agent-rich-tools` (F4 native fit; Claude Code's architectural choice per [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2 F4 row) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://docs.anthropic.com/en/api/claude-code `[ext]` |
| `notes` | The "F4 anchor" — if Anthropic's single-agent + rich-tools pattern is the right shape for MADEIRA, this is the natural substrate. Competes with Cursor SDK on developer-agent UX; loses on multi-repo / parallel-agent posture but wins on raw model capability + first-party tooling. |

### 4.3 OpenAI Agents SDK

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-OPENAI-AGENTS-SDK` |
| `vendor` | OpenAI |
| `runtime_shape` | `agent-sdk-python` + `agent-sdk-typescript` (Assistants API successor; Apps SDK companion `[ext]`) |
| `persistence_model` | `cloud-managed` (OpenAI manages thread + run state) |
| `tool_protocol` | `openai-functions` (canonical) + `mcp` (post-2025 Anthropic interop `[ext]`) |
| `license_class` | `proprietary-saas` (OpenAI) `[ext]` |
| `status` | `active` (Agents SDK 1.0 GA 2025-Q4 `[ext]`; Assistants API deprecated in favor of Agents SDK `[ext]`) |
| `cost_class` | `token-billed` |
| `akos_integration_state` | `forecasted` (one provider among many in `model_catalog.py`; SDK orchestration not currently wired) |
| `madeira_productization_role` | `agent-runtime` (alt; one of three frontier-provider options alongside Cursor SDK + Claude Code SDK) |
| `aic_pattern_role` | `supervisor` + `sub-agent` (F1) — Swarm pattern + nested-agent calls are first-party `[ext]` |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://platform.openai.com/docs/guides/agents `[ext]` |
| `notes` | Most-adopted developer-agent SDK by volume `[ext]`. Apps SDK companion targets distribution surface (ChatGPT app store) — competitive layer concern, not substrate-layer; tracked in deferred `competitive-layer-positioning.md`. |

### 4.4 AG2 (formerly AutoGen)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-AG2-AG2` |
| `vendor` | AG2 Open Source (community fork; Microsoft Research lineage) |
| `runtime_shape` | `framework-library-python` (multi-agent group-chat pattern; AutoGen v2 / AG2 fork) |
| `persistence_model` | `session-scoped` |
| `tool_protocol` | `openai-functions` (primary) + framework-native |
| `license_class` | `open-source-apache` (AG2) `[ext]` |
| `status` | `active` (post-AutoGen community fork ratified 2025; Microsoft maintains separate AutoGen successor `[ext]`) |
| `cost_class` | `bring-your-own-key` |
| `akos_integration_state` | `candidate` (alternative to CrewAI for F2 peer-companion AICs) |
| `madeira_productization_role` | `library-import` (if F2 wins and CrewAI is rejected) |
| `aic_pattern_role` | `peer` (F2 fit — group-chat pattern matches "team of AICs" rhetoric per [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §3 Strand A external research target) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://github.com/ag2ai/ag2 `[ext]` |
| `notes` | Naming churn (AutoGen → AG2 fork → Microsoft AutoGen continuation) creates ecosystem confusion; pin a specific fork at adoption time. CrewAI is the more polished alternative for F2 today; AG2 carries the deeper research lineage. |

### 4.5 Letta (formerly MemGPT)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-LETTA-LETTA` |
| `vendor` | Letta Inc. |
| `runtime_shape` | `framework-library-python` (stateful memory framework; agent has persistent core memory + recall memory) |
| `persistence_model` | `persistent` (the framework's load-bearing differentiator — agent state survives context-window boundaries) |
| `tool_protocol` | `openai-functions` + framework-native |
| `license_class` | `open-source-apache` (core) + `proprietary-saas` (Letta Cloud) `[ext]` |
| `status` | `active` (Letta Cloud GA 2025-Q3 `[ext]`; founder agents company spin-out post-MemGPT paper) |
| `cost_class` | `bring-your-own-key` (self-hosted) + `seat-billed` (Letta Cloud) |
| `akos_integration_state` | `candidate` (relevant to MADEIRA persistence question per `C-76-3` in [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §5) |
| `madeira_productization_role` | `library-import` (memory layer; orthogonal to orchestration shape) |
| `aic_pattern_role` | `not-applicable` (substrate-layer for memory; pairs with any of F1-F5) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://github.com/letta-ai/letta `[ext]` |
| `notes` | Specifically named in [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §3 Strand A as MADEIRA persistence research target. If `C-76-3` ratifies methodology-scoped persistence, Letta is a leading library candidate. |

### 4.6 Devin (Cognition Labs)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-COGNITION-DEVIN` |
| `vendor` | Cognition Labs |
| `runtime_shape` | `hosted-agent-platform` (Devin as a hosted autonomous software-engineering agent; not an SDK in the traditional sense) |
| `persistence_model` | `cloud-managed` (Devin sessions persist on Cognition cloud) |
| `tool_protocol` | `native-only` (Devin's tool surface is internal; limited external SDK surface as of 2026-Q2 `[ext]`) |
| `license_class` | `proprietary-saas` (Cognition) `[ext]` |
| `status` | `active` (Devin GA 2024-Q4; enterprise-focused 2026 `[ext]`) |
| `cost_class` | `seat-billed` ($500/mo Team plan `[ext]`) |
| `akos_integration_state` | `rejected` for AKOS substrate role (Devin is a competitor product to MADEIRA, not a substrate AKOS could run on; relevant only for competitive-positioning analysis deferred to master-roadmap P1) |
| `madeira_productization_role` | `not-applicable` |
| `aic_pattern_role` | `not-applicable` (Devin IS an AIC-shaped thing, not a substrate AICs run on) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://www.cognition.ai/devin `[ext]` |
| `notes` | Included in this audit per master-roadmap §3 P1 agent-SDK list. Reclassification recommendation: move to competitive-layer analysis at master-roadmap P1; not a substrate row in P3 SUBSTRATE_REGISTRY mint. |

### 4.7 Replit Agent

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-REPLIT-AGENT` |
| `vendor` | Replit Inc. |
| `runtime_shape` | `hosted-agent-platform` (Replit Agent integrated into Replit IDE; primarily app-generation focused) |
| `persistence_model` | `cloud-managed` (Replit account-scoped) |
| `tool_protocol` | `native-only` |
| `license_class` | `proprietary-saas` (Replit) `[ext]` |
| `status` | `active` (Replit Agent 3 launched 2026 `[ext]`) |
| `cost_class` | `seat-billed` ($25/mo Core `[ext]`) |
| `akos_integration_state` | `rejected` for AKOS substrate role (same logic as Devin — Replit Agent is a competitor product, not a substrate) |
| `madeira_productization_role` | `not-applicable` |
| `aic_pattern_role` | `not-applicable` |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | https://replit.com/agent `[ext]` |
| `notes` | Same reclassification recommendation as Devin (4.6). Cited in [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §3 Strand A mode-parity benchmarks alongside Cursor + Aider + Continue.dev — relevant for I76 mode-design research, not as an AKOS substrate. |

## 5. Class 3 — Architectural-posture substrates (3 rows; the load-bearing `D-IH-84-B` axis)

These three are not vendors but **patterns** for how the substrates above are combined into AKOS's day-to-day runtime. They are the directly load-bearing options for `D-IH-84-B` (AKOS substrate-baseline-choice) per [`decision-log.md`](../decision-log.md) — Stay-on-OpenClaw (B1), Migrate-to-Cursor-SDK (B2), Hybrid (B3).

### 5.1 OpenClaw thin-adapter (current default; B1 anchor)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-PATTERN-OPENCLAW-THIN-ADAPTER` |
| `vendor` | Holistika (internal) |
| `runtime_shape` | `orchestration-engine` (thin-wrapper pattern; OpenClaw owns the agent-loop, upstream framework owns the primitives) |
| `persistence_model` | `ephemeral` (per-process; persistence delegated to upstream) |
| `tool_protocol` | `mcp` (primary) |
| `license_class` | `commercial-license` (Holistika-internal) |
| `status` | `active` (Holistika's current default per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 OpenClaw row) |
| `cost_class` | `bring-your-own-key` (proxies through upstream) |
| `akos_integration_state` | `in-production` |
| `madeira_productization_role` | `agent-runtime` (Madeira-on-OpenClaw is the current shape) |
| `aic_pattern_role` | adaptable to any of F1-F5 via upstream framework choice |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | Internal (see `verify_openclaw_inventory.py`) |
| `notes` | **B1 anchor for `D-IH-84-B`**. Strength: Holistika owns the policy + observability surface; AKOS-as-SSOT is preserved by design. Weakness: bootstrap drift risk (wrapper aging behind upstream); the operator's day-to-day Cursor-agent interactions (per `D-IH-70-V` empirically embodying MADEIRA) are happening **outside** OpenClaw's wrapper, exposing a coverage gap. |

### 5.2 Hybrid: Cursor-SDK frontend + OpenClaw policy backend (B3 anchor; recommended pending P4 evidence)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-PATTERN-HYBRID-CURSOR-OPENCLAW` |
| `vendor` | Holistika (composition; Anysphere is upstream of frontend) |
| `runtime_shape` | `orchestration-engine` (Cursor SDK is the operator-facing agent runtime; OpenClaw retained as policy + observability middleware behind the SDK) |
| `persistence_model` | `cloud-managed` (Cursor backend persists frontend) + `ephemeral` (OpenClaw-side per-policy-check) |
| `tool_protocol` | `mcp` (Cursor + AKOS MCP servers wire through both layers) |
| `license_class` | `proprietary-saas` (Cursor) + `commercial-license` (OpenClaw) |
| `status` | `forecasted` (not yet implemented; the "B3 hybrid" option named in `D-IH-84-B` decision-log) |
| `cost_class` | `seat-billed` (Cursor) + `bring-your-own-key` (LLM through configured providers) |
| `akos_integration_state` | `forecasted` (would require P4 ratification + dedicated implementation initiative) |
| `madeira_productization_role` | `agent-runtime` (MADEIRA-as-Cursor-flow with AKOS-policy-enforcement) |
| `aic_pattern_role` | `supervisor` + `sub-agent` (F1 via Cursor's `subagent_types`) is the natural fit |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | (forecasted; no canonical implementation yet) |
| `notes` | **B3 anchor for `D-IH-84-B` — recommended pending P1 audit + P4 ratification** per `decision-log.md` D-IH-84-B options. Strength: best-of-both — operator-facing UX maturity + Holistika policy retention. Weakness: integration surface complexity; OpenClaw must be repackaged as middleware compatible with Cursor SDK's agent lifecycle; Anysphere vendor risk concentrated in the operator's day-to-day. |

### 5.3 MADEIRA-direct: build-your-own runtime per-method (KiRBe legacy pattern; B-equivalent for product side)

| Attribute | Value |
|:---|:---|
| `substrate_id` (proposed) | `SUBS-PATTERN-MADEIRA-DIRECT-OWN-RUNTIME` |
| `vendor` | Holistika (internal; product-pattern) |
| `runtime_shape` | `framework-library-python` (build-your-own agent on framework primitives; no wrapper layer) |
| `persistence_model` | `persistent` (KiRBe runs LlamaIndex+vector-store with per-tenant persistence; Madeira-on-LlamaIndex era was similar) |
| `tool_protocol` | framework-native (whatever the chosen framework provides) |
| `license_class` | `commercial-license` (Holistika-internal) |
| `status` | `active` (KiRBe still runs this pattern per founder framing 2026-05-16) + `deprecated-for-AKOS-substrate-role` (replaced by OpenClaw for AKOS-side; remains the KiRBe product pattern) |
| `cost_class` | `bring-your-own-key` (LLM) |
| `akos_integration_state` | `rejected` for AKOS (was the Madeira-on-LlamaIndex era; replaced by OpenClaw) + `in-production` for KiRBe product |
| `madeira_productization_role` | `not-applicable` for MADEIRA forward (the pattern MADEIRA migrated away from) + `agent-runtime` for KiRBe (still actively shipped) |
| `aic_pattern_role` | `not-applicable` (substrate-pattern, not AIC-pattern) |
| `last_audit_date` | 2026-05-17 |
| `audit_source_url` | Internal (KiRBe codebase; not yet open) |
| `notes` | **The historical baseline.** Founder framing 2026-05-16: *"like Madeira was in the LlamaIndex days like KiRBe still is"*. Relevant because the MADEIRA productization decision (`D-IH-84-D`) could revisit this pattern — if D1 (library-only) wins, `@holistika/madeira-agent` ships as a build-your-own-runtime library similar to LlamaIndex's positioning, just MADEIRA-method-shaped. KiRBe's continued use of this pattern is a P3 cross-reference (`D-IH-84-E` framework-narrowing input for the KiRBe ingestor — see [`i83-ai-archivist-and-kirbe-ingestor.md`](../../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) C-83-1). |

## 6. Audit findings summary (5 observations)

1. **The OpenClaw vs Cursor-SDK question is genuinely load-bearing.** Both substrates have plausible paths forward; neither is dominated on every dimension. The hybrid (B3) is the recommended-pending-evidence default per `D-IH-84-B` decision-log because it preserves Holistika's policy ownership while absorbing the operator-facing UX maturity Cursor SDK brings. This row needs the master-roadmap P1 regulatory/ToS thread (deferred from this chat) before P4 ratification — Cursor SDK's beta-status + MSA evolution + vendor-lock-in profile are not yet evidenced enough for a high-confidence ratify.

2. **The AIC pattern question (F1-F5; `D-IH-84-C`) has natural substrate fits per framing.** F1 supervised-sub-agents → Cursor SDK or OpenAI Agents SDK. F2 peer-companions → CrewAI or AG2. F3 ad-hoc-dispatchers → LangGraph. F4 single-agent-rich-tools → Claude Code SDK or VercelAI. F5 hybrid → composition. The substrate choice and the AIC pattern choice are **coupled** — ratifying F1 strongly suggests Cursor-SDK-backed or OpenAI-Agents-SDK-backed; ratifying F4 strongly suggests Claude-Code-SDK-backed. P4 batched ratification should surface this coupling explicitly.

3. **The MADEIRA productization shape question (`D-IH-84-D`) maps cleanly to substrate-class.** D1 library-only → framework-substrate (LlamaIndex / LangGraph / CrewAI). D2 agent-only → agent-SDK-substrate (Cursor SDK / Claude Code SDK). D3 hybrid → architectural-posture (OpenClaw thin-adapter or B3 hybrid). The MADEIRA-direct pattern (5.3) is the historical anchor that informs D1 — KiRBe's continued use of this pattern is evidence the pattern is durable for some product profiles.

4. **The KiRBe framework-narrowing question (`D-IH-84-E`) has a cleaner shape than the AKOS substrate question.** KiRBe today runs the LlamaIndex-era pattern (5.3 MADEIRA-direct). The narrowing-to-2-finalists likely comes from: (a) keep LlamaIndex-as-current; (b) migrate to LangGraph (workflow stateful); (c) consider Letta for memory-heavy needs. Per the master-roadmap §3 P1 KiRBe-specific dimension, the load-bearing axis for KiRBe is the `knowledge-base infrastructure` dimensions per AGENTIC_FRAMEWORK_LANDSCAPE.md §2 — KiRBe is a RAG-shaped product, so LlamaIndex's strength on the RAG axis is the gravitational anchor; LangGraph would need to demonstrate equivalent retrieval primitives or pair with LlamaIndex as a thin layer.

5. **Two of the seven net-new agent-SDK rows (Devin, Replit Agent) are misclassified as substrates.** They are competitor products, not substrates AKOS could run on. The master-roadmap §3 P1 grouped them in the agent-SDK class for breadth; this audit recommends reclassifying them to the competitive-layer analysis at master-roadmap P1 proper. If they stay in P3 SUBSTRATE_REGISTRY mint, they should carry `akos_integration_state: rejected` and a `notes` cell explaining the reclassification (see §4.6 + §4.7 above).

## 7. Cross-references

- [`master-roadmap.md`](../master-roadmap.md) §3 P1 — the full deliverable contract this report scopes down from.
- [`decision-log.md`](../decision-log.md) — D-IH-84-A through D-IH-84-I full rationale; this report is the evidence input for D-IH-84-B/C/D/E P4 ratification.
- [`risk-register.md`](../risk-register.md) — R-IH-84-1 (broad-but-shallow audit risk); this report mitigates by deferring competitive + regulatory + past-PoC threads explicitly rather than glossing.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — the existing Tech-Lab canonical; §3 of this report is the audit form of the 8 framework rows.
- [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) — §2 F1-F5 AIC framings cross-referenced throughout; §3 Strand A external research targets supplement the agent-SDK class audit.
- [`i74-brand-tooling-productization.md`](../../_candidates/i74-brand-tooling-productization.md) — `D-IH-84-D` productization-shape decision cross-references; not deeply analysed in this audit (deferred to dedicated `competitive-layer-positioning.md`).
- [`i83-ai-archivist-and-kirbe-ingestor.md`](../../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) — `D-IH-84-E` framework-narrowing decision cross-references.
- [`sc-resume-wave2-architectural-2026-05-16.md`](../../86-initiative-cluster-execution-coordinator/reports/sc-resume-wave2-architectural-2026-05-16.md) §3.5 — the I86 Wave 2 hand-off that scoped this audit to two operator-readable reports.
- [`p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) — the paired scorecard that compares the 17 substrates above across 6 dimensions and surfaces the P3 entry decision.

## 8. Provenance and confidence labels

Authored by the successor agent in fresh chat per [`sc-resume-wave2-architectural-2026-05-16.md`](../../86-initiative-cluster-execution-coordinator/reports/sc-resume-wave2-architectural-2026-05-16.md) §3.5 directive. Confidence `B2` (Holistika-internal-research-synthesis from agent training corpus + repo reading) overall; per-row attributes flagged `[ext]` should be re-verified before any row writes to `SUBSTRATE_REGISTRY.csv` as `confidence_level: A1` (the SSOT confidence floor per [`confidence_levels.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md)).

This report is **Tier-1 reference-only** per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) classes. It is not canonical until the rows promote into `SUBSTRATE_REGISTRY.csv` via P3 mint (operator-gated; out of scope for this chat).
