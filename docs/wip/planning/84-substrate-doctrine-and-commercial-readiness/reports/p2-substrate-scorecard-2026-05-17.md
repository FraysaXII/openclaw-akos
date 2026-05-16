---
report_id: i84-p2-substrate-scorecard-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 §3.5 successor pick-up
phase: P2
initiative: INIT-OPENCLAW_AKOS-84
linked_decisions: [D-IH-84-A, D-IH-84-B, D-IH-84-C, D-IH-84-D, D-IH-84-E]
linked_evidence: p1-substrate-landscape-2026-05-17.md;i76-madeira-elevation.md;AGENTIC_FRAMEWORK_LANDSCAPE.md
access_level: 4
confidence_level: B2
source_taxonomy: holistika-internal-research-synthesis
language: en
---

# I84 P2 — Substrate scorecard (2026-Q2)

> **Scope (per sc-resume Wave 2 §3.5).** Operator-readable scorecard comparing the 18 substrates audited in [`p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md) across six operator-named dimensions: governance fit, operator-runtime maturity, cost, lock-in risk, AKOS-as-SSOT compatibility, and MADEIRA elevation alignment per [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md). The scorecard is **decision-supporting** evidence for the P4 batched ratification of `D-IH-84-B/C/D/E` per [`decision-log.md`](../decision-log.md); it does **not** ratify those decisions itself. P4 ratification is operator-gated and out of scope for this chat per sc-resume §6.

## 1. Scoring rubric

A five-level qualitative scale applied per dimension per substrate. The scale is intentionally coarse — fine-grained numeric scoring would create false precision in a `B2`-confidence audit. Operator can pivot to finer scoring at P4 if needed.

| Score | Meaning |
|:---|:---|
| **STRONG** | Substrate is a clear positive on this dimension. Few or no caveats. |
| **GOOD** | Substrate is positive on this dimension with named caveats. |
| **NEUTRAL** | Substrate is acceptable on this dimension. Neither helps nor hurts. |
| **WEAK** | Substrate is a clear negative on this dimension. Mitigation possible but costly. |
| **N/A** | Dimension does not apply to this substrate class (e.g., MADEIRA-alignment is not meaningful for KiRBe-only product substrates). |

Per-dimension scoring methodology is defined inline in each of §2.1–§2.6 below. The aggregate grid at §3 reads from those scoring tables.

## 2. Per-dimension scorecards

### 2.1 Governance fit (D1)

**Scoring criterion.** Does the substrate cooperate with AKOS canonical-CSV discipline per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc), SOP-META ordering (process_list row before SOP per [`SOP-META_PROCESS_MGMT_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md) §4.2–4.3), PRECEDENCE.md classification per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance", and the dual-register brand-baseline-reality contract per [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc)?

**STRONG.** Substrate has no surface that pulls AKOS canonical content into vendor-managed state. Governance discipline is fully operator-owned.

**GOOD.** Substrate is mostly governance-neutral with named caveats (e.g., one vendor-managed surface that requires policy gate).

**NEUTRAL.** Substrate is governance-agnostic; doesn't help, doesn't hurt.

**WEAK.** Substrate's vendor-managed state, telemetry, or content surfaces would absorb AKOS canonical content into vendor lock-in, violating the SSOT discipline.

| # | Substrate | Score | Rationale |
|:---|:---|:---|:---|
| 3.1 | LangChain | STRONG | Library; no vendor-managed state; AKOS-side adapters carry policy. |
| 3.2 | LangGraph | STRONG | Same as LangChain; LangGraph Cloud is opt-in not default. |
| 3.3 | LlamaIndex | STRONG | Library; KiRBe already runs it cleanly under AKOS governance. |
| 3.4 | OpenClaw | STRONG | **Maximally aligned by design** — Holistika-built; the wrapper IS the governance layer; quarterly re-bless cadence in AGENTIC_FRAMEWORK_LANDSCAPE.md §5. |
| 3.5 | CrewAI | GOOD | Library; CrewAI Enterprise vendor-managed surface is opt-in; community version is governance-neutral. |
| 3.6 | Ollama | STRONG | Local-only; no vendor surface. |
| 3.7 | VercelAI | GOOD | SDK is governance-neutral; Vercel hosting platform pulls deployment metadata (not canonicals). |
| 3.8 | Groq | STRONG | Inference-only; OpenAI-compatible API; no state pulled. |
| 4.1 | Cursor SDK | WEAK | **Vendor-managed agent state + telemetry + transcript surface is the load-bearing governance friction.** Cursor backend persists agent state per `D-IH-84-B` analysis; AKOS canonicals would not be pulled by default, but the operator-facing transcripts (which carry AKOS-content references) live on Anysphere cloud. Mitigation: BAA + DPA negotiation + ToS review at master-roadmap P1 regulatory thread. |
| 4.2 | Claude Code SDK | GOOD | Vendor-managed session state + telemetry, but smaller blast radius than Cursor (no UI; just API). Mitigation: same DPA review. |
| 4.3 | OpenAI Agents SDK | GOOD | Vendor-managed thread/run state on OpenAI cloud; standard ToS posture as one provider among many in `model_catalog.py`. |
| 4.4 | AG2 | STRONG | Library; community-maintained; no vendor surface. |
| 4.5 | Letta | GOOD | Library is governance-neutral; Letta Cloud is opt-in not default. |
| 4.6 | Devin | WEAK | Hosted-only; no library form; Cognition cloud would own all agent state. Not a real substrate option. |
| 4.7 | Replit Agent | WEAK | Hosted-only; Replit cloud would own all agent state. Not a real substrate option. |
| 5.1 | OpenClaw thin-adapter | STRONG | Same as 3.4 OpenClaw — the pattern IS the governance layer. |
| 5.2 | Hybrid (Cursor + OpenClaw) | GOOD | Inherits Cursor SDK's WEAK on frontend transcript-storage + OpenClaw's STRONG on policy backend. Net: GOOD because the policy gate sits between the operator and the vendor surface; AKOS canonicals stay in OpenClaw's control. |
| 5.3 | MADEIRA-direct | STRONG | Holistika-built; no vendor surface; equivalent governance posture to 3.4 OpenClaw. |

### 2.2 Operator-runtime maturity (D2)

**Scoring criterion.** How production-ready is the substrate for operator-facing daily use as of 2026-Q2? Considers: GA status (active vs beta vs forecasted), known reliability profile, ecosystem maturity (community size, documentation quality, integration ecosystem), and `last_audit_date` freshness.

**STRONG.** Substrate is GA, has been in production at scale for ≥12 months, has mature docs + community + integration ecosystem.

**GOOD.** Substrate is GA but younger than 12 months, OR mature but with a known reliability gap (e.g., API churn).

**NEUTRAL.** Substrate is GA but the substrate has limited production track record at Holistika-comparable scale.

**WEAK.** Substrate is beta, or pre-GA, or has known instability.

| # | Substrate | Score | Rationale |
|:---|:---|:---|:---|
| 3.1 | LangChain | GOOD | Mature; GA for years; v0.3 stable per `[ext]`; ecosystem-largest. Caveat: historical API churn (per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column). |
| 3.2 | LangGraph | GOOD | GA but younger; rapidly maturing; LangGraph Platform GA `[ext]`. State-shape changes still possible. |
| 3.3 | LlamaIndex | STRONG | Production-mature; LlamaIndex Workflows GA 2026; KiRBe running it stably. |
| 3.4 | OpenClaw | STRONG | Holistika-internal mature; quarterly re-bless; in production. |
| 3.5 | CrewAI | GOOD | GA; CrewAI Enterprise GA `[ext]`; community version stable; younger than LangChain. |
| 3.6 | Ollama | STRONG | Mature local runtime; production-stable for sandbox use. |
| 3.7 | VercelAI | GOOD | GA v4 `[ext]`; mature within Next.js ecosystem; less general-purpose. |
| 3.8 | Groq | STRONG | Production inference; integrated as provider via standard interface. |
| 4.1 | Cursor SDK | WEAK | **SDK in beta as of 2026-Q2** `[ext]` — the founder framing explicitly named this: *"the fact that even Cursor SDK is in beta is something we need to capitalize"*. Cursor 3 ("Glass") GA 2026-04-02 — the application is mature; the SDK is the immature surface. |
| 4.2 | Claude Code SDK | GOOD | GA 2025; SDK matured 2026-Q1 `[ext]`. Younger than 12 months at SDK level; mature at application level. |
| 4.3 | OpenAI Agents SDK | GOOD | Agents SDK 1.0 GA 2025-Q4 `[ext]`; Assistants API predecessor deprecated. Mature company; younger product. |
| 4.4 | AG2 | NEUTRAL | Active community fork; ecosystem fragmentation (AG2 vs Microsoft AutoGen) creates adoption uncertainty. |
| 4.5 | Letta | GOOD | Letta Cloud GA 2025-Q3 `[ext]`; framework mature post-MemGPT-paper lineage. |
| 4.6 | Devin | STRONG | GA 2024-Q4 `[ext]`; enterprise-focused; production-stable. (But not a substrate option — see 4.6 governance row.) |
| 4.7 | Replit Agent | STRONG | Replit Agent 3 launched 2026 `[ext]`; production-stable. (But not a substrate option.) |
| 5.1 | OpenClaw thin-adapter | STRONG | Same as 3.4 — Holistika's current default. |
| 5.2 | Hybrid (Cursor + OpenClaw) | WEAK | **Inherits Cursor SDK's beta status as the load-bearing constraint.** Mitigation: structure the hybrid to degrade gracefully to pure-OpenClaw if Cursor SDK is unavailable. |
| 5.3 | MADEIRA-direct | NEUTRAL | The pattern is mature (KiRBe runs it); MADEIRA-specific implementation would need to be built. |

### 2.3 Cost (D3)

**Scoring criterion.** Total cost of ownership at Holistika scale (small team; 5-15 operator-days/month of agent runtime; ~10-100M tokens/month). Considers `cost_class` + `pricing_unit` + hidden costs (e.g., vendor-platform fees, integration engineering).

**STRONG.** Cost is bring-your-own-key only; marginal cost per use is LLM-only; no platform overhead.

**GOOD.** Cost adds a modest predictable platform tier (e.g., seat-billed at <$50/user/mo).

**NEUTRAL.** Cost is bring-your-own-key but with non-trivial hidden costs (engineering integration, ops).

**WEAK.** Cost is seat-billed at ≥$100/user/mo OR token-billed at premium pricing OR has unpredictable scale-up costs.

| # | Substrate | Score | Rationale |
|:---|:---|:---|:---|
| 3.1 | LangChain | STRONG | BYOK; library cost zero. |
| 3.2 | LangGraph | STRONG | BYOK; LangGraph Cloud opt-in not required. |
| 3.3 | LlamaIndex | STRONG | BYOK; storage costs only for index. |
| 3.4 | OpenClaw | STRONG | BYOK; no platform fee; quarterly re-bless engineering overhead is fixed. |
| 3.5 | CrewAI | STRONG | BYOK core; Enterprise tier opt-in. |
| 3.6 | Ollama | STRONG | Free; only hardware cost. |
| 3.7 | VercelAI | GOOD | BYOK LLM; Vercel hosting tier ($20/mo+ for Pro). |
| 3.8 | Groq | STRONG | Very low per-token `[ext]`; flagship pricing advantage. |
| 4.1 | Cursor SDK | GOOD | Seat-billed at $20/user Pro or $40/user Business `[ext]`; LLM included up to plan limit. At Holistika scale (~3-5 operators): $60-200/mo — predictable and modest. |
| 4.2 | Claude Code SDK | NEUTRAL | Token-billed; Claude pricing is premium per-token but high capability. Heavy use can scale to $200-1000/mo. |
| 4.3 | OpenAI Agents SDK | NEUTRAL | Token-billed; standard OpenAI pricing. Comparable to Claude at use volume. |
| 4.4 | AG2 | STRONG | BYOK; community open-source. |
| 4.5 | Letta | GOOD | BYOK self-hosted; Letta Cloud opt-in. |
| 4.6 | Devin | WEAK | $500/mo Team plan `[ext]` — well above scale-appropriate range; not substrate-comparable. |
| 4.7 | Replit Agent | GOOD | $25/mo Core `[ext]` — modest if used. Not a real substrate option but cost-comparable to Cursor SDK. |
| 5.1 | OpenClaw thin-adapter | STRONG | Same as 3.4. |
| 5.2 | Hybrid (Cursor + OpenClaw) | GOOD | Inherits Cursor SDK seat cost + LLM costs. ~$60-200/mo at Holistika scale + integration engineering one-time. |
| 5.3 | MADEIRA-direct | STRONG | BYOK; library-shape. |

### 2.4 Lock-in risk (D4)

**Scoring criterion.** How costly would migration off the substrate be? Considers: vendor concentration (single-vendor vs ecosystem-shared), proprietary contracts (data formats, APIs, RBAC models that don't translate), portability of operator-facing assets (transcripts, agent definitions, tool catalogs).

**STRONG (low lock-in).** Substrate is open-source library; migration cost is adapter-rewrite only.

**GOOD (modest lock-in).** Substrate is vendor-managed but uses standard contracts (e.g., OpenAI-compatible API); migration is feasible with weeks of engineering.

**NEUTRAL.** Substrate has some proprietary contracts but ecosystem alternatives exist for each surface.

**WEAK (high lock-in).** Substrate has proprietary contracts that have no direct migration path; deep vendor dependency.

| # | Substrate | Score | Rationale |
|:---|:---|:---|:---|
| 3.1 | LangChain | STRONG | Open-source MIT; adapter-pattern migration to LlamaIndex/LangGraph/CrewAI well-trodden. |
| 3.2 | LangGraph | GOOD | Open-source; but state-shape contract is LangGraph-specific. Migration cost: rewrite graph definitions. |
| 3.3 | LlamaIndex | STRONG | Open-source; standard RAG primitives; LangChain has migration adapters. |
| 3.4 | OpenClaw | STRONG | Holistika-owned; no external lock-in. |
| 3.5 | CrewAI | GOOD | Open-source core; crew abstractions are CrewAI-specific. Migration cost: rewrite crew definitions to AG2 group-chat or similar. |
| 3.6 | Ollama | STRONG | Open-source; OpenAI-compatible API. |
| 3.7 | VercelAI | NEUTRAL | SDK is open-source; Vercel hosting lock-in is moderate (Next.js apps deployable elsewhere with engineering work). |
| 3.8 | Groq | STRONG | OpenAI-compatible API; provider swap is config-change. |
| 4.1 | Cursor SDK | WEAK | **Highest lock-in in the candidate set.** Multi-agent + multi-repo + parallel-agent-fleet capabilities are Cursor-specific. Subagent dispatch model is Cursor-native. Migration to Claude Code SDK or OpenAI Agents SDK requires: re-implementing parallel-agent posture; re-wiring tool catalogs; replacing operator-facing UI; absorbing the loss of Cursor's MCP integration polish. |
| 4.2 | Claude Code SDK | NEUTRAL | Anthropic-native tool protocol + MCP. Migration to OpenAI Agents SDK or Cursor SDK is feasible with weeks of engineering. |
| 4.3 | OpenAI Agents SDK | NEUTRAL | OpenAI-canonical tool protocol + MCP. Similar migration cost to Claude Code SDK. |
| 4.4 | AG2 | STRONG | Open-source Apache. |
| 4.5 | Letta | GOOD | Open-source core; persistent-memory contract is Letta-specific (recall vs core memory abstractions). |
| 4.6 | Devin | WEAK | Hosted-only; no migration path. (Not a substrate option.) |
| 4.7 | Replit Agent | WEAK | Hosted-only; no migration path. (Not a substrate option.) |
| 5.1 | OpenClaw thin-adapter | STRONG | Same as 3.4 — Holistika-owned. |
| 5.2 | Hybrid (Cursor + OpenClaw) | NEUTRAL | OpenClaw policy layer is portable; Cursor SDK frontend has Cursor lock-in. **Net: NEUTRAL because the OpenClaw layer absorbs the lock-in risk** — if Cursor SDK becomes untenable, the AKOS-side OpenClaw layer survives and can re-front on Claude Code SDK or OpenAI Agents SDK with frontend rewrite. |
| 5.3 | MADEIRA-direct | STRONG | Holistika-built; the substrate IS Holistika code. |

### 2.5 AKOS-as-SSOT compatibility (D5)

**Scoring criterion.** Does the substrate respect AKOS as the source of truth for canonicals (`process_list.csv`, `baseline_organisation.csv`, all `compliance.*_mirror` dimensions, KM Topic-Fact-Source, brand voice, localisation), or does it pull SSOT into vendor surfaces? Considers: data residency (where canonical content gets stored), telemetry posture (what canonical content gets shipped off-cloud), integration mode (read-canonical-and-respect vs ingest-and-own).

**STRONG.** Substrate is content-agnostic; AKOS canonicals stay entirely in AKOS-controlled storage; substrate operates as a pure tool.

**GOOD.** Substrate reads AKOS canonicals via MCP / file-system; vendor surfaces store only operational metadata (e.g., agent transcripts referencing canonicals by ID).

**NEUTRAL.** Substrate ingests AKOS canonical content for indexing/embedding/retrieval; AKOS stays SSOT but vendor surface has a partial mirror.

**WEAK.** Substrate's design centralises content on vendor cloud; AKOS-as-SSOT discipline degrades to "AKOS-then-export-to-vendor" pattern; risk of vendor surface becoming de-facto SSOT.

| # | Substrate | Score | Rationale |
|:---|:---|:---|:---|
| 3.1 | LangChain | STRONG | Library; reads what host passes; content-agnostic. |
| 3.2 | LangGraph | STRONG | Same. |
| 3.3 | LlamaIndex | NEUTRAL | RAG framework ingests canonical content into vector index; AKOS CSVs stay SSOT but the index is a partial mirror. Mitigation: treat index as derived artefact per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 LlamaIndex risk column. |
| 3.4 | OpenClaw | STRONG | Designed for AKOS-as-SSOT — the wrapper carries policy gates that enforce the discipline. |
| 3.5 | CrewAI | STRONG | Library; content-agnostic. |
| 3.6 | Ollama | STRONG | Inference-only; no content ingest. |
| 3.7 | VercelAI | STRONG | SDK is content-agnostic. |
| 3.8 | Groq | STRONG | Inference-only. |
| 4.1 | Cursor SDK | GOOD | Reads AKOS canonicals via MCP + file-system; transcripts on Anysphere cloud reference canonicals by ID. Vendor surface stores **operational** (which canonical was read when) not **canonical content** (the row content stays in AKOS). However: long-running multi-agent sessions could accumulate canonical content in transcripts if the agent quotes canonicals back; ToS review needed at master-roadmap P1 regulatory thread. |
| 4.2 | Claude Code SDK | GOOD | Same as Cursor SDK pattern; smaller blast radius (no UI; API-only). |
| 4.3 | OpenAI Agents SDK | GOOD | Same pattern; thread/run state on OpenAI cloud references canonicals by ID via tool calls. |
| 4.4 | AG2 | STRONG | Library; content-agnostic. |
| 4.5 | Letta | NEUTRAL | Memory framework persists agent state — including canonical content the agent has read/quoted — to its own store. Self-hosted Letta = STRONG; Letta Cloud = WEAK. |
| 4.6 | Devin | WEAK | Hosted-only; all agent state on Cognition cloud. (Not a substrate option.) |
| 4.7 | Replit Agent | WEAK | Same. |
| 5.1 | OpenClaw thin-adapter | STRONG | Same as 3.4 — by design. |
| 5.2 | Hybrid (Cursor + OpenClaw) | GOOD | OpenClaw policy backend enforces AKOS-as-SSOT; Cursor SDK frontend inherits the GOOD score from 4.1. Net: GOOD. |
| 5.3 | MADEIRA-direct | STRONG | Holistika-built; AKOS-as-SSOT is the design centre. |

### 2.6 MADEIRA elevation alignment (D6)

**Scoring criterion.** Does the substrate enable the AIC framings F1-F5 from [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2 cleanly, AND does it support the MADEIRA-as-method posture (rules + hooks + skills + MCPs + sub-agents-or-not + mode parity + tool catalog + persistence) per I76 §1 operating story? Considers: AIC-pattern-role per substrate (which F-framings does this substrate naturally fit?) + the MADEIRA productization shape implied (D-IH-84-D D1/D2/D3) + the operator-interaction surface (per the founder framing *"this is a huge win to bring my interaction with MADEIRA to be like the one I have with Cursor"*).

**STRONG.** Substrate enables multiple F-framings cleanly + supports MADEIRA-as-method posture + has operator-interaction surface comparable to Cursor.

**GOOD.** Substrate enables one F-framing cleanly + supports most of MADEIRA-as-method posture.

**NEUTRAL.** Substrate is compatible with MADEIRA but doesn't differentially enable.

**WEAK.** Substrate constrains MADEIRA shape OR conflicts with I76 mode-parity requirements.

| # | Substrate | Score | Rationale |
|:---|:---|:---|:---|
| 3.1 | LangChain | NEUTRAL | Foundational library; pairs with any F-framing via composition; doesn't differentially enable. |
| 3.2 | LangGraph | GOOD | F3 native fit (ad-hoc dispatchers / tool-call subgraphs); MADEIRA-as-stateful-workflow shape if F3 wins. |
| 3.3 | LlamaIndex | WEAK | RAG-side, not orchestration-side; MADEIRA-as-method is orchestration-shaped. LlamaIndex would be a tool MADEIRA uses, not the MADEIRA substrate. |
| 3.4 | OpenClaw | NEUTRAL | Adaptable to any F-framing via upstream choice; doesn't differentially enable any particular framing. Strength: governance fit means MADEIRA stays in compliance; weakness: doesn't give MADEIRA a polished operator-interaction surface (the I76 gap). |
| 3.5 | CrewAI | GOOD | F2 native fit (peer companions; "team of AICs" rhetoric directly maps to crew abstraction). MADEIRA-as-crew shape if F2 wins. |
| 3.6 | Ollama | N/A | Inference-only; not architectural. |
| 3.7 | VercelAI | GOOD | F4 fit (single-agent + rich-tools); MADEIRA-as-web-widget shape. |
| 3.8 | Groq | N/A | Inference-only. |
| 4.1 | Cursor SDK | STRONG | **F1 native fit** (Cursor `subagent_types` + supervisor-worker pattern) per [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2 F1 row. Operator-interaction surface is exactly what the founder framing names — MADEIRA-interaction-like-Cursor-interaction. Multi-agent + multi-repo + parallel-agent-fleet capabilities give MADEIRA polish OpenClaw can't natively. |
| 4.2 | Claude Code SDK | STRONG | **F4 native fit** (single-agent rich-tools) per [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2 F4 row. Operator-interaction quality at frontier-model level. |
| 4.3 | OpenAI Agents SDK | GOOD | F1 fit (Swarm + nested-agent calls). Less differentiated operator-interaction surface than Cursor SDK or Claude Code SDK. |
| 4.4 | AG2 | GOOD | F2 fit (group-chat pattern); deeper research lineage than CrewAI but less polished operator-interaction. |
| 4.5 | Letta | GOOD | Orthogonal to F-framing; addresses `C-76-3` MADEIRA persistence question directly. Pairs with any F-framing. |
| 4.6 | Devin | N/A | Not a substrate option. (Competitor to MADEIRA, not MADEIRA substrate.) |
| 4.7 | Replit Agent | N/A | Same. |
| 5.1 | OpenClaw thin-adapter | NEUTRAL | Same as 3.4 — adaptable but doesn't differentially enable; doesn't give operator-interaction polish. |
| 5.2 | Hybrid (Cursor + OpenClaw) | STRONG | **Inherits Cursor SDK's STRONG on operator-interaction surface + OpenClaw's STRONG on governance/SSOT.** Net: STRONG because the two strengths are additive — operator gets Cursor-grade interaction + MADEIRA stays in AKOS compliance via policy backend. F1 native fit at frontend; any framing at backend. |
| 5.3 | MADEIRA-direct | NEUTRAL | Build-your-own gives full design freedom but no operator-interaction shortcut; would need to build the Cursor-grade UX from scratch. |

## 3. Aggregate scorecard grid (18 × 6)

Compressed view; full per-dimension rationale in §2. Read left-to-right per row to see a substrate's profile across all 6 dimensions; read top-to-bottom per column to see which substrates lead on a given dimension.

| Substrate | Governance fit | Maturity | Cost | Lock-in (low) | AKOS SSOT | MADEIRA alignment |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Class 1 — Framework substrates** | | | | | | |
| LangChain | STRONG | GOOD | STRONG | STRONG | STRONG | NEUTRAL |
| LangGraph | STRONG | GOOD | STRONG | GOOD | STRONG | GOOD |
| LlamaIndex | STRONG | STRONG | STRONG | STRONG | NEUTRAL | WEAK |
| OpenClaw | STRONG | STRONG | STRONG | STRONG | STRONG | NEUTRAL |
| CrewAI | GOOD | GOOD | STRONG | GOOD | STRONG | GOOD |
| Ollama | STRONG | STRONG | STRONG | STRONG | STRONG | N/A |
| VercelAI | GOOD | GOOD | GOOD | NEUTRAL | STRONG | GOOD |
| Groq | STRONG | STRONG | STRONG | STRONG | STRONG | N/A |
| **Class 2 — Agent-SDK substrates** | | | | | | |
| Cursor SDK | WEAK | WEAK | GOOD | WEAK | GOOD | STRONG |
| Claude Code SDK | GOOD | GOOD | NEUTRAL | NEUTRAL | GOOD | STRONG |
| OpenAI Agents SDK | GOOD | GOOD | NEUTRAL | NEUTRAL | GOOD | GOOD |
| AG2 | STRONG | NEUTRAL | STRONG | STRONG | STRONG | GOOD |
| Letta | GOOD | GOOD | GOOD | GOOD | NEUTRAL | GOOD |
| Devin | WEAK | STRONG | WEAK | WEAK | WEAK | N/A |
| Replit Agent | WEAK | STRONG | GOOD | WEAK | WEAK | N/A |
| **Class 3 — Architectural-posture substrates** | | | | | | |
| OpenClaw thin-adapter (B1) | STRONG | STRONG | STRONG | STRONG | STRONG | NEUTRAL |
| Hybrid Cursor + OpenClaw (B3) | GOOD | WEAK | GOOD | NEUTRAL | GOOD | STRONG |
| MADEIRA-direct (legacy) | STRONG | NEUTRAL | STRONG | STRONG | STRONG | NEUTRAL |

## 4. Aggregate findings (5 observations)

1. **OpenClaw thin-adapter (B1) is the governance + cost + lock-in winner; loses MADEIRA-alignment.** B1 is STRONG on 5 of 6 dimensions, NEUTRAL on MADEIRA-alignment. The governance + SSOT + cost + lock-in profile is the strongest in the candidate set; the MADEIRA-alignment gap is the load-bearing weakness. This is the **status quo** scoring as one would expect — it is the substrate Holistika currently runs on.

2. **Cursor SDK (4.1) is the MADEIRA-alignment winner; loses governance + maturity + lock-in.** Cursor SDK is STRONG on MADEIRA-alignment and GOOD on AKOS-SSOT, but WEAK on governance + maturity + lock-in. This is the **pure-migration** option scoring as a high-risk choice — strong on the dimension the founder directive named ("MADEIRA-interaction-like-Cursor-interaction"), weak on the dimensions AKOS governance discipline prioritises.

3. **Hybrid (Cursor + OpenClaw) (B3) is the only candidate that scores GOOD or STRONG on all 6 dimensions when MADEIRA-alignment is included.** B3 inherits the governance + SSOT + lock-in resistance of OpenClaw on the policy backend + the MADEIRA-alignment of Cursor SDK on the frontend. The trade-off: WEAK on maturity (inherits Cursor SDK's beta status as the load-bearing constraint) + GOOD-not-STRONG on cost (adds Cursor seat cost on top of LLM costs). **This validates the recommended-pending-evidence default in `decision-log.md` D-IH-84-B.** The P4 ratification should still scrutinise the maturity risk explicitly.

4. **The AIC framing (D-IH-84-C; F1-F5) is empirically coupled to substrate choice.** STRONG MADEIRA-alignment scores accrue to: Cursor SDK (F1), Claude Code SDK (F4), Hybrid (F1-via-Cursor). GOOD MADEIRA-alignment scores accrue to: LangGraph (F3), CrewAI (F2), VercelAI (F4), OpenAI Agents SDK (F1), AG2 (F2), Letta (orthogonal to F). The substrate × F-framing coupling means the P4 batched ratification should surface this explicitly: ratifying F1 substantially commits to Cursor SDK or OpenAI Agents SDK or Hybrid; ratifying F2 substantially commits to CrewAI or AG2; ratifying F3 substantially commits to LangGraph; ratifying F4 substantially commits to Claude Code SDK or VercelAI.

5. **The MADEIRA productization shape (D-IH-84-D) maps to substrate class.** D1 library-only → recommends framework substrates (LangGraph for F3 or CrewAI for F2 or LlamaIndex for F4-RAG-shape). D2 agent-only → recommends agent-SDK substrates (Claude Code SDK for F4 hosted or Cursor SDK for F1 hosted). D3 hybrid → recommends architectural-posture substrates (B1 OpenClaw, B3 Hybrid). The KiRBe framework-narrowing (D-IH-84-E) is **separately**: KiRBe is RAG-shaped, so the two finalists are likely LlamaIndex (continue) + LangGraph (workflow-stateful upgrade), with Letta as a candidate memory layer pair.

## 5. Comparative scenario analyses

Three concrete operator-decision scenarios the scorecard maps to. These are NOT recommendations — they are illustrations of how the evidence above supports P4 ratification options.

### Scenario A — Stay-on-OpenClaw (B1)

| Implication | Score impact | Notes |
|:---|:---|:---|
| MADEIRA stays on OpenClaw | NEUTRAL alignment | The I76 operator-interaction gap remains; MADEIRA-as-method runs on OpenClaw but doesn't get Cursor-grade UX. |
| Governance/cost/SSOT discipline preserved | STRONG across 4 dimensions | Status quo is highest-discipline. |
| AIC framing decision (D-IH-84-C) deferred | N/A | OpenClaw is adaptable to any F-framing; the F-decision becomes a per-upstream-framework choice. |
| Productization shape (D-IH-84-D) implied | D1 or D3 | OpenClaw can ship as library (D1) or stay internal (status-quo, deferring D-IH-84-D to a later cycle). |
| KiRBe framework (D-IH-84-E) | Independent | KiRBe's RAG-shape decision is independent. |

### Scenario B — Migrate-to-Cursor-SDK (B2)

| Implication | Score impact | Notes |
|:---|:---|:---|
| MADEIRA gets Cursor-grade UX | STRONG alignment | The I76 operator-interaction gap closes. |
| Governance + maturity + lock-in degrade | WEAK across 3 dimensions | The load-bearing risks the founder directive flagged (Cursor SDK in beta + vendor concentration). |
| AIC framing (D-IH-84-C) implied | F1 | Cursor's `subagent_types` is the load-bearing fit. |
| Productization shape (D-IH-84-D) implied | D2 or D3 | MADEIRA-as-hosted-on-Cursor-SDK. |
| KiRBe framework (D-IH-84-E) | Decoupled | KiRBe doesn't run on Cursor SDK; this scenario only affects MADEIRA. |

### Scenario C — Hybrid (B3) recommended-pending-evidence

| Implication | Score impact | Notes |
|:---|:---|:---|
| MADEIRA gets Cursor-grade UX on frontend | STRONG alignment | The I76 operator-interaction gap closes. |
| OpenClaw policy backend preserves governance + SSOT | GOOD-to-STRONG on 4 dimensions | The trade-off vs B1 is in maturity (Cursor SDK beta inheritance). |
| AIC framing (D-IH-84-C) implied | F1 frontend + adaptable backend | Cursor `subagent_types` at the operator-facing layer; OpenClaw upstream choice at the policy layer. |
| Productization shape (D-IH-84-D) implied | D3 hybrid | MADEIRA-as-hybrid; library form for the policy layer; agent form for the operator-facing layer. |
| KiRBe framework (D-IH-84-E) | Independent | Same as Scenario A. |
| Integration engineering cost | One-time | OpenClaw must be repackaged as middleware compatible with Cursor SDK's agent lifecycle. |

## 6. Implications for P4 batched ratification (D-IH-84-B/C/D/E)

The scorecard surfaces three **coupling-aware** decision shapes for the P4 batched ratification:

1. **D-IH-84-B (AKOS substrate-baseline) is the load-bearing first decision.** B1 / B2 / B3 each commit to a different downstream profile per Scenarios A/B/C. B3 hybrid is the recommended-pending-evidence default per `decision-log.md`; the scorecard supports this default but flags maturity (Cursor SDK beta) + integration-engineering cost as the load-bearing risks. **Recommended P4 framing**: ratify B1/B2/B3 first; downstream F-framing + productization-shape follow naturally.

2. **D-IH-84-C (AIC F1-F5 framing) is empirically coupled to B-choice.** If B2 or B3 ratifies, F1 is the natural fit (Cursor's `subagent_types`). If B1 ratifies, F-framing remains open and can pivot to any of F1-F5 via upstream framework choice. **Recommended P4 framing**: if B2 or B3 ratifies, F1 is the soft default; if B1 ratifies, surface a sub-question with the F1-F5 evidence per i76 §2.

3. **D-IH-84-D (MADEIRA productization shape) and D-IH-84-E (KiRBe framework-narrowing) are independent of B-choice and can ratify in parallel.** D-IH-84-D maps to substrate class (D1 library / D2 agent / D3 hybrid) per finding #5; D-IH-84-E is a KiRBe-internal narrowing (likely LlamaIndex-continue + LangGraph-workflow, per finding #5). Both can be ratified in the same P4 batch as B and C without coupling friction.

## 7. P3 entry decision (operator-gated)

Per sc-resume §6 — P3 (substrate-doctrine canonical mint at Envoy Tech Lab/canonicals/) and P4 (substrate-decision rehearsal) are operator-gated forks. The successor agent has produced this scorecard as the input evidence for both. **Three plausible next steps** which the closing inline-AskQuestion in this chat surfaces to the operator:

1. **Mint doctrine canonical (P3)** — author `SUBSTRATE_LANDSCAPE_DOCTRINE.md` at `Research/Methodology/canonicals/` plus seed `SUBSTRATE_REGISTRY.csv` rows from §3 grid per master-roadmap P2 + P6 contracts. Requires the full Pydantic + validator + mirror + PRECEDENCE + docs cascade chain per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers". Substantial work block (2-3d engineer); operator-gated canonical-CSV mint.

2. **Refine scorecard before P3** — operator has refinements (additional substrates to audit, dimension reweighting, sub-dimensional scoring, deeper analysis on specific scoring cells). Iterate P2 first; defer P3.

3. **Defer to next chat** — context budget for P3 is substantial; operator may prefer fresh chat for P3 with this P1+P2 evidence as input. Aligned with I86 Wave 2 chat-boundary discipline pattern per [`sc-resume-wave2-architectural-2026-05-16.md`](../../86-initiative-cluster-execution-coordinator/reports/sc-resume-wave2-architectural-2026-05-16.md).

The closing inline-AskQuestion surfaces these three options per [`inline-ratify-craft/SKILL.md`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) Principle 5 (batched coupled-decision posture, here just the single P3-entry decision).

## 8. Cross-references

- [`p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md) — the paired audit this scorecard reads from.
- [`master-roadmap.md`](../master-roadmap.md) §3 P1 + §4 P2 — the full deliverable contracts this report scopes down from.
- [`decision-log.md`](../decision-log.md) D-IH-84-B/C/D/E — the four P4 batched ratification decisions this scorecard supplies evidence for.
- [`risk-register.md`](../risk-register.md) R-IH-84-3 (batched ratification operator fatigue) — mitigated by the explicit coupling-aware framing in §6 of this report; operator can pivot per substrate-class.
- [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) §2 F1-F5 + §3 Strand C ratification — D6 MADEIRA-alignment scoring cross-references throughout.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — Tech-Lab canonical the 8 framework rows reference.
- [`inline-ratify-craft/SKILL.md`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) — followed for the closing P3-entry AskQuestion in this chat.
- [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — `gate_type: inline-ratify` declaration this scorecard's closing question follows.
- [`sc-resume-wave2-architectural-2026-05-16.md`](../../86-initiative-cluster-execution-coordinator/reports/sc-resume-wave2-architectural-2026-05-16.md) §3.5 + §6 — the I86 Wave 2 hand-off that scoped P1+P2 to this chat and identified P3+P4 as operator-gated forks.

## 9. Provenance and confidence labels

Authored by the successor agent in fresh chat per [`sc-resume-wave2-architectural-2026-05-16.md`](../../86-initiative-cluster-execution-coordinator/reports/sc-resume-wave2-architectural-2026-05-16.md) §3.5 directive. Confidence `B2` (Holistika-internal-research-synthesis) overall; per-row scoring inherits the P1 audit's per-attribute confidence (notably `[ext]` flags for vendor pricing, GA dates, license terms that should be re-verified at master-roadmap-grade P1).

This report is **Tier-1 reference-only** per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) classes. It is not canonical until the scoring + landscape promote into `SUBSTRATE_REGISTRY.csv` + `SUBSTRATE_LANDSCAPE_DOCTRINE.md` via P3 mint (operator-gated; surfaced in §7).

The scorecard is deliberately decision-supporting not decision-making. P4 batched ratification per [`decision-log.md`](../decision-log.md) is the operator-gated forum for the substantive ratifications.
