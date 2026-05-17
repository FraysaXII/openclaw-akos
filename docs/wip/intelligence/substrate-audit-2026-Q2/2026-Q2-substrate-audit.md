---
report_id: substrate-audit-2026-Q2
cycle_id: substrate-audit-2026-Q2
authored: 2026-05-17
author: System Owner + Holistik Researcher (with agent assistance) via I84 Wave A3 successor pick-up
cycle_owner: Research Lead (or KM Officer + Founder interim per D-IH-84-H pre-Research-Director hire)
classification: tier-1-wip (working space; not canonical SSOT)
access_level: 5
language: en
linked_initiative: INIT-OPENCLAW_AKOS-84
linked_sop: SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md
linked_doctrine: SUBSTRATE_LANDSCAPE_DOCTRINE.md
linked_decisions: [D-IH-84-A, D-IH-84-B, D-IH-84-C, D-IH-84-D, D-IH-84-E, D-IH-84-F, D-IH-84-G, D-IH-84-H]
confidence_level: B2
source_taxonomy: holistika-internal-research-synthesis
---

# 2026-Q2 substrate audit (cycle 1 — founding-cycle baseline)

> **Cycle role.** This is the **founding-cycle** of the continuous Research-area substrate-audit discipline (per [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md) at status:review). It synthesises the I84 P1 + P2 + Tier-1 WIP evidence under one cycle-conformant cover so the cadence has a baseline to delta against in Q3+. Subsequent quarterly cycles read this baseline + emit deltas via `py scripts/peopl_research_substrate_audit_cadence.py --emit-delta <prior> <current>`.
>
> Per [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) section 3 (5-element audit shape): this cycle covers Landscape + Scorecard + Competitive + Regulatory + Past-PoC. Each element has a stand-alone Tier-1 WIP thread; this consolidated cycle report synthesises across them with citations to per-substrate `substrate_id` from [`SUBSTRATE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv).
>
> **Status of P4 substitution.** Sections 6 and 7 carry `<!-- post-P4 substitution -->` placeholder blocks awaiting operator answers on `D-IH-84-B/C/D/E` at the I84 P4 batched inline-ratify gate. The parent agent fills those blocks after the operator answers in the foreground.

## 1. Landscape (element 1 of 5) — synthesis of P1 audit

Source: [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) — operator-readable substrate landscape audit (18 substrates × 18-column SUBSTRATE_REGISTRY attribute schema).

### 1.1 Substrate taxonomy

Per P1 audit section 2, three substrate classes carry meaningfully different governance profiles:

- **Class 1 — Framework substrates** (8 rows) — code libraries imported into a host process; the host owns the runtime, the framework provides primitives.
- **Class 2 — Agent-SDK substrates** (7 rows) — vendor-managed agent-execution runtimes accessed via SDK + (often) hosted backend.
- **Class 3 — Architectural-posture substrates** (3 rows) — patterns combining the above (the load-bearing axis for `D-IH-84-B`).

### 1.2 Class 1 — Framework substrates (8 rows; canonical IDs)

| `substrate_id` | Vendor | `runtime_shape` | `akos_integration_state` | Audit highlight |
|:---|:---|:---|:---|:---|
| `SUBS-LANGCHAIN-AI-LANGCHAIN` | LangChain AI | `framework-library-python` | `in-production` | v0.3 stable as of 2026-Q2; mature ecosystem; high historical API churn (per AGENTIC_FRAMEWORK_LANDSCAPE.md section 1 risk column) |
| `SUBS-LANGCHAIN-AI-LANGGRAPH` | LangChain AI | `orchestration-engine` | `pilot` | F3 native fit per i76-madeira-elevation section 2; D-IH-84-E candidate finalist for KiRBe narrowing |
| `SUBS-RUN-LLAMA-LLAMAINDEX` | run-llama / LlamaIndex | `framework-library-python` | `in-production` | KiRBe runs on this stack; LlamaIndex Workflows GA 2026; D-IH-84-E candidate finalist for KiRBe narrowing |
| `SUBS-HOLISTIKA-OPENCLAW` | Holistika | `framework-library-python` | `in-production` | Holistika's current default; quarterly re-bless per AGENTIC_FRAMEWORK_LANDSCAPE.md section 5; B1 anchor for D-IH-84-B |
| `SUBS-CREWAI-INC-CREWAI` | CrewAI Inc. | `framework-library-python` | `pilot` | F2 peer-companion native fit; CrewAI Enterprise GA |
| `SUBS-OLLAMA-OLLAMA` | Ollama Inc. | `inference-provider` | `in-production` | Holistika local-iteration sandbox; production-stable for sandbox tier |
| `SUBS-VERCEL-VERCEL-AI-SDK` | Vercel Inc. | `agent-sdk-typescript` | `pilot` | F4 single-agent-rich-tools fit; Vercel AI SDK v4 GA |
| `SUBS-GROQ-GROQ-CLOUD` | Groq Inc. | `inference-provider` | `in-production` | One provider behind shared interface per model_catalog.py |

### 1.3 Class 2 — Agent-SDK substrates (7 rows; canonical IDs)

| `substrate_id` | Vendor | `runtime_shape` | `akos_integration_state` | Audit highlight |
|:---|:---|:---|:---|:---|
| `SUBS-ANYSPHERE-CURSOR-SDK` | Anysphere Inc. | `agent-sdk-typescript` | `pilot` | **SDK in BETA as of 2026-Q2** (founder framing 2026-05-16 named this as competitive window); Cursor 3 "Glass" GA 2026-04-02; B2/B3 anchor for D-IH-84-B; F1 native fit (`subagent_types`) |
| `SUBS-ANTHROPIC-CLAUDE-CODE-SDK` | Anthropic | `agent-sdk-typescript` | `forecasted` | F4 single-agent-rich-tools native fit; Claude Code GA 2025; SDK matured 2026-Q1 |
| `SUBS-OPENAI-AGENTS-SDK` | OpenAI | `agent-sdk-python` | `forecasted` | Agents SDK 1.0 GA 2025-Q4; Assistants API predecessor deprecated; most-adopted developer-agent SDK by volume |
| `SUBS-AG2-AG2` | AG2 OSS / Microsoft Research lineage | `framework-library-python` | `candidate` | F2 peer-companion fit (group-chat pattern); ecosystem naming churn (pin specific fork) |
| `SUBS-LETTA-LETTA` | Letta Inc. | `framework-library-python` | `candidate` | Persistent memory framework (formerly MemGPT); relevant to MADEIRA C-76-3 persistence question |
| `SUBS-COGNITION-DEVIN` | Cognition Labs | `hosted-agent-platform` | `rejected` | Not a substrate AKOS can run on — competitor product (autonomous SWE agent); row preserved per audit-trail per P1 section 4.6 reclassification finding |
| `SUBS-REPLIT-AGENT` | Replit Inc. | `hosted-agent-platform` | `rejected` | Same as Devin — competitor product; row preserved per audit-trail per P1 section 4.7 reclassification finding |

### 1.4 Class 3 — Architectural-posture substrates (3 rows; canonical IDs)

| `substrate_id` | Pattern | `akos_integration_state` | Audit highlight |
|:---|:---|:---|:---|
| `SUBS-PATTERN-OPENCLAW-THIN-ADAPTER` | OpenClaw thin-adapter | `in-production` | B1 anchor for D-IH-84-B; pattern AKOS currently runs on; Holistika owns policy + observability; AKOS-as-SSOT preserved by design |
| `SUBS-PATTERN-HYBRID-CURSOR-OPENCLAW` | Hybrid: Cursor SDK frontend + OpenClaw policy backend | `forecasted` | B3 anchor for D-IH-84-B (recommended-pending-evidence default per `decision-log.md`); inherits both governance discipline + operator-facing UX maturity |
| `SUBS-PATTERN-MADEIRA-DIRECT-OWN-RUNTIME` | MADEIRA-direct: build-your-own runtime per-method | `in-production` (KiRBe) | The historical baseline (Madeira-on-LlamaIndex era; KiRBe still runs this pattern per founder framing 2026-05-16); D1 library-only productization candidate per D-IH-84-D |

### 1.5 Per-substrate `last_audit_date`

Every row's `last_audit_date` is `2026-05-17` per the founding-cycle audit. Next-cycle (`2026-Q3`) advances the date for any row touched.

## 2. Scorecard (element 2 of 5) — synthesis of P2 scorecard

Source: [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) — 18 substrates × 6 governance dimensions; 5-level qualitative scoring (STRONG / GOOD / NEUTRAL / WEAK / N/A).

### 2.1 Scoring rubric

Per P2 scorecard section 1. The five-level qualitative scale is intentionally coarse — fine-grained numeric scoring would create false precision in a `B2`-confidence audit. Operator can pivot to finer scoring at P4 if needed.

### 2.2 Six dimensions

Per P2 scorecard sections 2.1-2.6:

1. **Governance fit (D1).** Does the substrate cooperate with AKOS canonical-CSV discipline, SOP-META ordering, PRECEDENCE.md classification, and dual-register brand-baseline-reality contract?
2. **Operator-runtime maturity (D2).** How production-ready is the substrate for operator-facing daily use as of 2026-Q2?
3. **Cost (D3).** Total cost of ownership at Holistika scale (~5-15 operator-days/month of agent runtime; ~10-100M tokens/month).
4. **Lock-in risk (D4).** How costly would migration off the substrate be?
5. **AKOS-as-SSOT compatibility (D5).** Does the substrate respect AKOS as the source of truth for canonicals?
6. **MADEIRA elevation alignment (D6).** Does the substrate enable the AIC framings F1-F5 from `i76-madeira-elevation` cleanly, and does it support the MADEIRA-as-method posture?

### 2.3 Aggregate scorecard grid (18 × 6)

Per P2 scorecard section 3. Reproduced here for cycle-self-containment:

| Substrate (citing `substrate_id`) | Governance | Maturity | Cost | Lock-in (low) | AKOS SSOT | MADEIRA alignment |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Class 1 — Framework substrates** | | | | | | |
| `SUBS-LANGCHAIN-AI-LANGCHAIN` | STRONG | GOOD | STRONG | STRONG | STRONG | NEUTRAL |
| `SUBS-LANGCHAIN-AI-LANGGRAPH` | STRONG | GOOD | STRONG | GOOD | STRONG | GOOD |
| `SUBS-RUN-LLAMA-LLAMAINDEX` | STRONG | STRONG | STRONG | STRONG | NEUTRAL | WEAK |
| `SUBS-HOLISTIKA-OPENCLAW` | STRONG | STRONG | STRONG | STRONG | STRONG | NEUTRAL |
| `SUBS-CREWAI-INC-CREWAI` | GOOD | GOOD | STRONG | GOOD | STRONG | GOOD |
| `SUBS-OLLAMA-OLLAMA` | STRONG | STRONG | STRONG | STRONG | STRONG | N/A |
| `SUBS-VERCEL-VERCEL-AI-SDK` | GOOD | GOOD | GOOD | NEUTRAL | STRONG | GOOD |
| `SUBS-GROQ-GROQ-CLOUD` | STRONG | STRONG | STRONG | STRONG | STRONG | N/A |
| **Class 2 — Agent-SDK substrates** | | | | | | |
| `SUBS-ANYSPHERE-CURSOR-SDK` | WEAK | WEAK | GOOD | WEAK | GOOD | STRONG |
| `SUBS-ANTHROPIC-CLAUDE-CODE-SDK` | GOOD | GOOD | NEUTRAL | NEUTRAL | GOOD | STRONG |
| `SUBS-OPENAI-AGENTS-SDK` | GOOD | GOOD | NEUTRAL | NEUTRAL | GOOD | GOOD |
| `SUBS-AG2-AG2` | STRONG | NEUTRAL | STRONG | STRONG | STRONG | GOOD |
| `SUBS-LETTA-LETTA` | GOOD | GOOD | GOOD | GOOD | NEUTRAL | GOOD |
| `SUBS-COGNITION-DEVIN` | WEAK | STRONG | WEAK | WEAK | WEAK | N/A |
| `SUBS-REPLIT-AGENT` | WEAK | STRONG | GOOD | WEAK | WEAK | N/A |
| **Class 3 — Architectural-posture substrates** | | | | | | |
| `SUBS-PATTERN-OPENCLAW-THIN-ADAPTER` (B1) | STRONG | STRONG | STRONG | STRONG | STRONG | NEUTRAL |
| `SUBS-PATTERN-HYBRID-CURSOR-OPENCLAW` (B3) | GOOD | WEAK | GOOD | NEUTRAL | GOOD | STRONG |
| `SUBS-PATTERN-MADEIRA-DIRECT-OWN-RUNTIME` | STRONG | NEUTRAL | STRONG | STRONG | STRONG | NEUTRAL |

### 2.4 Aggregate findings (5 observations from P2 section 4)

1. **OpenClaw thin-adapter (B1; `SUBS-PATTERN-OPENCLAW-THIN-ADAPTER`) is the governance + cost + lock-in winner; loses MADEIRA-alignment.** Status quo scoring; STRONG on 5 of 6 dimensions, NEUTRAL on MADEIRA-alignment.
2. **Cursor SDK (`SUBS-ANYSPHERE-CURSOR-SDK`) is the MADEIRA-alignment winner; loses governance + maturity + lock-in.** Pure-migration option scores as high-risk; strong on the dimension the founder directive named ("MADEIRA-interaction-like-Cursor-interaction"), weak on the dimensions AKOS governance prioritises.
3. **Hybrid (B3; `SUBS-PATTERN-HYBRID-CURSOR-OPENCLAW`) is the only candidate that scores GOOD or STRONG on all 6 dimensions.** Inherits OpenClaw's governance + SSOT + lock-in resistance on the policy backend + Cursor SDK's MADEIRA-alignment on the frontend. Maturity weakness inherits from Cursor SDK beta.
4. **AIC framing (`D-IH-84-C`; F1-F5) is empirically coupled to substrate choice.** STRONG MADEIRA-alignment scores accrue to Cursor SDK (F1), Claude Code SDK (F4), Hybrid (F1-via-Cursor). GOOD scores to LangGraph (F3), CrewAI (F2), VercelAI (F4), OpenAI Agents SDK (F1), AG2 (F2), Letta (orthogonal to F).
5. **MADEIRA productization shape (`D-IH-84-D`) maps to substrate class.** D1 library-only → framework substrates. D2 agent-only → agent-SDK substrates. D3 hybrid → architectural-posture substrates. **KiRBe framework-narrowing (`D-IH-84-E`)** likely lands on LlamaIndex-continue + LangGraph-workflow finalists with Letta as candidate memory layer pair (per past-PoC translation analysis in section 5 below).

## 3. Competitive (element 3 of 5) — synthesis of competitive-layer-positioning

Source: [`competitive-layer-positioning.md`](competitive-layer-positioning.md) — 8 competitors × structured rows; categorised in three families per the analysis.

### 3.1 Family 1 — Intelligence-layer competitors (closest to Madeira positioning)

- **Glean Technologies Inc.** — "Enterprise AI work assistant" / "intelligence layer beneath the interface"; directly Madeira's stated positioning per `i76-madeira-elevation` section 1; HIGH threat level; well-funded ($260M Series E 2024; $4.6B valuation); ~700 enterprise customers.
- **Notion Labs Inc. (Notion AI)** — "AI in the doc you already work in"; workspace-embedded AI assistant; MEDIUM threat (different distribution); $10/user/mo bundled add-on.
- **Anthropic (Projects)** — "Persistent workspaces for Claude conversations"; first-party "persistent agent workspace" closest to Madeira workspace feel; MEDIUM-HIGH threat.

### 3.2 Family 2 — Distribution/runtime competitors

- **OpenAI (Apps SDK)** — Distribution layer for third-party AI agents inside ChatGPT app store; ChatGPT 800M+ weekly users; MEDIUM threat (only if Madeira ships as consumer-facing app).
- **Microsoft (Copilot Studio)** — "Low-code build for enterprise Copilot agents"; M365 distribution; LOW threat (different persona).
- **Google (Gemini for Workspace)** — Workspace-native AI bundled with Google Workspace subscription; LOW threat (different persona).

### 3.3 Family 3 — Tool catalog / orchestration competitors

- **Composio (SignalCraft Inc.)** — "150+ tools your AI agent can use"; framework-agnostic adapter pattern; NIL competitor / POTENTIAL DEPENDENCY (Madeira could consume vs in-house MCP-server-per-vendor pattern).
- **Lindy AI Inc.** — "Build AI agents that handle your work"; no-code AI agent builder for SMBs; LOW threat (different persona + distribution).

### 3.4 Aggregate findings (4 observations from competitive section 5)

1. **The "intelligence layer" positioning is contested.** Glean owns the phrase at enterprise scale; Anthropic Projects + Claude Code SDK form a credible first-party alternative. Madeira's differentiation must rest on methodology-shape + ERP-transformable canonicals + brand-voice register.
2. **`D-IH-84-D` productization shape choice maps to a competitive lane choice.** D2 hosted-agent collides directly with Glean + Anthropic Projects; D1 library-only sidesteps; D3 hybrid hedges.
3. **Tool catalog layer is not a competitor; it's a dependency choice.** Composio vs in-house MCP-server-per-vendor pattern is a sub-decision under D1.
4. **Workspace-embedded AI is the dominant 2026 enterprise pattern** (Notion / Google / Microsoft); doesn't compete directly with Madeira but raises the strategic question of whether Madeira is "a workspace tool" or "a method that runs through whatever tools the operator already has".

## 4. Regulatory + ToS (element 4 of 5) — synthesis of regulatory-tos-forecast

Source: [`regulatory-tos-forecast.md`](regulatory-tos-forecast.md) — 4 regulatory topics; each section recommends ADVOPS engagement per `akos-adviser-engagement.mdc`.

### 4.1 EU AI Act provider-vs-deployer 2026 enforcement

Per the analysis: 2026-08-02 high-risk enforcement begins; 2027-08-02 full application. Holistika's exposure varies by substrate + productization shape:

- **Deployer-only (B1 OpenClaw + LLM provider; B2 Cursor SDK; B3 Hybrid)** — lowest baseline exposure; deployer obligations apply when EU operators use the system.
- **Provider (D2 MADEIRA-as-SaaS)** — full Annex III conformity assessment + risk management + technical documentation + human oversight + post-market monitoring if classified high-risk.
- **D1 (library-only)** — lower provider exposure since library shape disclaims being an AI system per se; GPAI obligations may still cascade.

### 4.2 GDPR-as-SaaS DPA cascading

Per the analysis: DPA cascade complexity scales with substrate-layer depth. B1 simplest; B2/B3 add a layer (through Cursor SDK to Anysphere); D2 extends cascade downward to Holistika's customers.

### 4.3 Cursor MSA + SDK ToS evolution

Per the analysis: SDK ToS is **beta-state**; GA transition likely 2026-Q3/Q4 per `[ext]`; material changes expected. Committing to B2 or B3 without formal MSA + SDK ToS review carries meaningful contract risk. Recommended mitigation: defer formal D-IH-84-B B2/B3 ratification until Cursor SDK ToS reaches GA, OR ratify with explicit re-ratify trigger at GA.

### 4.4 IP-indemnity carve-outs

Per the analysis: frontier Western providers (OpenAI / Anthropic / Google) offer the strongest indemnity; Cursor SDK pass-through-to-underlying-model indemnity is weakest for Moonshot Kimi 2.5 backed flows. B3 hybrid policy backend enables per-flow routing of customer-facing prose through indemnified providers regardless of operator-selected frontend.

### 4.5 ADVOPS engagement recommendation

Per the regulatory analysis section 7: ADVOPS engagement is recommended BEFORE `D-IH-84-B` and `D-IH-84-D` binding ratification. Detailed scoping in [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md) (four-discipline framework: EU AI Act counsel + GDPR/DPA counsel + IP/IT counsel + jurisdictional fiscal counsel).

## 5. Past-PoC translation (element 5 of 5) — synthesis of past-poc-translation-matrix

Source: [`past-poc-translation-matrix.md`](past-poc-translation-matrix.md) — 5 lineage rows: I10 closed + I11 active + I12+I13 superseded + KiRBe-still-on-LlamaIndex + R&L v2.7 framework references.

### 5.1 I10 Madeira eval hardening (closed 2026-04-15)

Substrate-relevant decisions D-B (Path B SSOT sandbox), D-C (Path C research spine), D-UI (gateway.controlUi removal), D-EVAL (Langfuse v4 telemetry). Translatable learnings: sandbox-mode is the operational-friction surface for OpenClaw; research-spine MCP pattern survives any substrate choice; Langfuse v4 telemetry integration is the load-bearing observability surface.

### 5.2 I11 Madeira ops copilot (active since 2026-04-15)

Substrate-relevant decisions D-OPS-1 through D-OPS-4 (overlay-only architecture; RBAC-as-config; persistence deferred; intent-routing). Translatable learnings: overlay-only architecture is substrate-portable; Madeira at suggest posture (no decide) is the established pattern; persistence deferral creates I76 C-76-3 entry point.

### 5.3 I12 + I13 Madeira research lineage (superseded by I84)

I12 + I13 vendor-handoff lineage produced brittle intelligence (one-time dossier doesn't keep pace with substrate-landscape velocity). The supersession is the right move — I84's continuous-cadence pattern with SUBSTRATE_REGISTRY as registry-shape persistence layer is structurally well-positioned.

### 5.4 KiRBe-still-on-LlamaIndex (parallel-track substrate continuity)

KiRBe never migrated off the LlamaIndex-era substrate per founder framing 2026-05-16. Inferred reasons: product profile is RAG-shaped not orchestration-shaped; per-tenant persistence model is mature on LlamaIndex; no operational pressure to migrate. **`D-IH-84-E` recommendation**: narrow to `SUBS-RUN-LLAMA-LLAMAINDEX` (continue) + `SUBS-LANGCHAIN-AI-LANGGRAPH` (workflow-stateful upgrade) finalists, with `SUBS-LETTA-LETTA` as candidate memory-layer pair.

### 5.5 R&L v2.7 framework references

The Research & Logic v2.7 folder carries Holistika's historical framework documents (pre-v3.0 vault). Substrate-relevance: methodology evolves; substrate must accommodate evolution; format-portability is the load-bearing requirement; methodology framework is the differentiator vs Glean / Notion AI / Anthropic Projects competitors.

### 5.6 Aggregate findings (4 observations from past-PoC section 7)

1. **AKOS substrate continuity has been remarkably durable across vault generations (v1.3 → v2.7 → v3.0).** Methodology is source of truth; substrate is implementation; transitions are operationally costly but methodologically-preservable.
2. **OpenClaw thin-adapter emerged from deliberate governance posture, not technical necessity.** B3 hybrid preserves the governance discipline; B2 pure-Cursor-SDK migration loses it.
3. **KiRBe-still-on-LlamaIndex is structurally correct, not an oversight.** `D-IH-84-E` should narrow to LlamaIndex-continue + LangGraph-workflow finalists; Cursor SDK + OpenClaw are not KiRBe-fit.
4. **I12 / I13 supersession is methodologically sound.** Continuous Research-area discipline + registry-shaped persistence + paired runbook is the right replacement pattern.

## 6. P4 ratifications block

> **Substituted 2026-05-17.** P4 batched inline-ratify gate (parent agent foreground; commit `3900787`) ratified all 4 architectural shape decisions. Full per-decision rationale + cross-decision coupling in [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/decision-log.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/decision-log.md) + the formal ratification record at [`reports/p4-shape-ratification-batch-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p4-shape-ratification-batch-2026-05-17.md).

### 6.1 D-IH-84-B — AKOS substrate-baseline ratified as **B5** (novel framing)

**Ratified option**: **B5 — Bridge-with-strict-retractability (tactical) + deep-self-owned-LlamaIndex-or-similar-substrate (strategic endgame)**.

Operator delegated craft at the P4 gate ("trust you can browse our context and intent to craft the best solution"); encoded as `decision_source: agent_executive_call_per_operator_delegation` per `inline-ratify-craft/SKILL.md` Principle 6.

Architecture:
- **Tactical layer (today through 2026-Q4)**: B3-shaped hybrid (Cursor SDK frontend + OpenClaw policy backend) with the **retractability axiom** as binding architectural principle. Single integration boundary; same provider interface as `akos/model_catalog.py`; parity-with-OpenClaw is the retractability gate; ADVOPS engagement gates the contract surface.
- **Strategic layer (2026-Q4+ trajectory)**: deep self-owned substrate (LlamaIndex or successor open-source) as orchestration anchor; Cursor SDK reverts to optional operator-DX layer or full retraction once self-owned substrate matures.

Substrate-registry encoding (already live): `SUBS-PATTERN-OPENCLAW-THIN-ADAPTER` (B1 anchor; in-production) + `SUBS-PATTERN-HYBRID-CURSOR-OPENCLAW` (B3/B5 anchor; forecasted; flips to pilot at first integration) + `SUBS-RUN-LLAMA-LLAMAINDEX` (strategic-endgame anchor; active). A future `SUBS-PATTERN-DEEP-SELF-OWNED-LLAMAINDEX-CENTRIC` pattern row is forward-charter (operator-pending; not in I84 scope).

### 6.2 D-IH-84-C — AIC framing ratified as **F5**

**Ratified option**: **F5 — Hybrid; per-task operator picks**.

Preserves the I76 candidate F1-F5 framing as a choice-surface rather than a single binding. `SUBSTRATE_REGISTRY.csv` `aic_pattern_role` column across 18 rows already enumerates supervisor / sub-agent / peer / dispatcher / single-agent-rich-tools / not-applicable — F5 is the only option that does not reject half the inventory.

Couples cleanly with B5: hybrid substrate exposes multiple agentic patterns through the same provider abstraction — F5 is the agentic-pattern analog of B5's substrate-pattern hybrid posture.

### 6.3 D-IH-84-D — MADEIRA productization ratified as **D3**

**Ratified option**: **D3 — Hybrid: library for technically-mature customers + hosted agent for less-technical customers**.

Maps cleanly to BOTH TRIGGER-1 (hosted-agent when ≥3 external orgs request data-detached) AND TRIGGER-2 (library when ≥2 external orgs request AKOS-as-library) per `MADEIRA-AKOS/STATUS.md` §3 — D1 / D2 each ignore one trigger.

Couples cleanly with B5: hybrid productization mirrors hybrid substrate; library customers operate on their own substrate (any open-source stack the B5 self-governance principle endorses); hosted-agent customers operate on Holistika's B5-retractable-tactical + self-owned-strategic substrate.

### 6.4 D-IH-84-E — KiRBe narrowing ratified as **E1**

**Ratified option**: **E1 — LlamaIndex-continue + LangGraph-workflow** (2 finalists; I83 P0 picks between them or composes both).

Both finalists are **MIT open-source** aligned with B5 self-governance + retractability + no-vendor-lock-in principle. The "somehow D" Cursor SDK option from the initial gate was structurally precluded by the B5 principle (Cursor SDK license_class=proprietary-saas conflicts with self-governance endgame); follow-up AskQuestion presented the B5-grounded analysis and operator ratified E1.

Rationale: best fit for KiRBe's pipeline-shaped INGESTOR role; preserves KiRBe substrate continuity per `SUBSTRATE_LANDSCAPE_DOCTRINE.md` §4 principle 2 ("incremental evolution over discontinuous migration"); LangGraph dispatcher pattern matches F3 in F5 framing.

### 6.5 Forward-charter implications

- **DECISION_REGISTER.csv canonical row mints for D-IH-84-B/C/D/E** remain operator-pending forward-charter (canonical-CSV gate per `akos-governance-remediation.mdc` §"HLK compliance governance"). Recommend bundling with the next operator-approved canonical-CSV tranche.
- **Per-candidate D-IH-NN-X pre-ratification rows** (D-IH-76-A inheriting D-IH-84-C; D-IH-74-D inheriting D-IH-84-D; D-IH-83-A inheriting D-IH-84-E) land at each candidate's P0 charter when promoted — not in I84 scope.
- **ADVOPS engagement** per [`reports/advops-engagement-scoping-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md) is the B5 tactical-layer contract-surface gate for any binding Cursor SDK integration. Operator decides timing (engage now vs defer to first concrete Cursor SDK integration).

### 6.6 Risk-register updates

- **R-IH-84-3 (4-decision batched ratification produces operator fatigue + rubber-stamp outcomes)** — **closed**. Operator engaged substantively at all 4 gates (delegated B with explicit principle; cleanly selected C/D; asked for help on E with mixed signals → follow-up AskQuestion ratified). No rubber-stamping observed; inline-ratify-craft principles held.
- **R-IH-84-2 (SUBSTRATE_REGISTRY.csv column shape locks early; later ALTER cost)** — **monitor** (no change in this cycle). 18 columns + 9 enum frozensets remain coherent through P4; first ALTER likely triggered by SUBS-PATTERN-DEEP-SELF-OWNED-LLAMAINDEX-CENTRIC row mint (forward-charter).
- **R-IH-84-NEW-ADVOPS** — **mitigation in flight** per ADVOPS scoping note; operator activation gate Options A-D.
- **R-IH-84-NEW-CURSOR-TOS-VELOCITY** — **mitigated by B5 retractability axiom**. Any Cursor SDK GA-related ToS change is contained behind the integration boundary; B5 trajectory is to retract toward self-owned substrate regardless.

## 7. Cross-area implications

> **Substituted 2026-05-17.** P4 batched ratification cascade landed at commit `3900787` with non-destructive candidate-stub cross-reference headers. Pre-staged handoff document at [`reports/cross-area-unlock-handoff-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/cross-area-unlock-handoff-2026-05-17.md) carries the full per-candidate cascade specification.

### 7.1 I76 (MADEIRA elevation) — unlocked by D-IH-84-C F5 ratification

- C-76-1 AIC framing **closed** as F5 hybrid per-task.
- Strand A external research deliverable **substituted** by the I84 P1 audit dossier + this founding-cycle quarterly report + the 3 Tier-1 WIP threads.
- I76 P0 charter is now free to focus on **per-pattern instantiation** (which task-classes default to F1 / F2 / F3 / F4 in operator workflow).
- D-IH-76-A pre-ratification row appends to i76 decision register at I76 P0 charter (forward-charter).
- Candidate stub `i76-madeira-elevation.md` carries non-destructive cascade header per commit `3900787`.

### 7.2 I74 (brand-tooling productization) — unlocked by D-IH-84-D D3 ratification

- C-74-3 MADEIRA gate-criteria **closed** as D3 hybrid library + agent platform.
- C-74-4 license-separation enforceability **informed** by Cursor SDK MSA + IP-indemnity analyses in [`regulatory-tos-forecast.md`](regulatory-tos-forecast.md) §4 + §5; ADVOPS engagement recommended pre-binding per [`reports/advops-engagement-scoping-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md).
- I74 P0 charter is free to focus on **library API surface + hosted-agent runtime architecture** decisions.
- D-IH-74-D pre-ratification row appends to i74 decision register at I74 P0 charter (forward-charter).
- Candidate stub `i74-brand-tooling-productization.md` carries non-destructive cascade header per commit `3900787`.

### 7.3 I83 (AI archivist + KiRBe ingestor) — unlocked by D-IH-84-E E1 narrowing

- C-83-1 framework-class-narrowing **closed to 2 finalists**: `SUBS-RUN-LLAMA-LLAMAINDEX` + `SUBS-LANGCHAIN-AI-LANGGRAPH`. I83 P0 picks between them or composes both (likely outcome since they natively compose via langchain-native tool protocol).
- `SUBS-LETTA-LETTA` flagged as candidate memory-layer pair (orthogonal; KiRBe P0 evaluates per product-roadmap fit).
- I83 P0 charter is free to focus on the orchestration anchor pick + composition pattern + memory-layer evaluation.
- D-IH-83-A pre-ratification row appends to i83 decision register at I83 P0 charter (forward-charter).
- Candidate stub `i83-ai-archivist-and-kirbe-ingestor.md` carries non-destructive cascade header per commit `3900787`.

### 7.4 I82 (capability doctrine + commercial readiness) — CAPABILITY_REGISTRY FK target now live

- CAPABILITY_REGISTRY column-spec **should extend** to include `substrate_id` nullable FK to SUBSTRATE_REGISTRY for capabilities that name an underlying technical substrate.
- 18-row SUBSTRATE_REGISTRY canonical (live; Supabase mirror harmonized) is the FK target.
- I82 P0 charter incorporates the column-spec refresh into the CAPABILITY_REGISTRY.csv mint scope (P2 facet 2a).
- Candidate stub `i82-holistika-capability-doctrine-and-commercial-readiness.md` carries non-destructive cascade header per commit `3900787`.

### 7.5 Recommended cross-area pings (operator-pending forward-charter)

- **Tech Lab `AGENTIC_FRAMEWORK_LANDSCAPE.md` extension** — original master-roadmap §3 P3 contract; as-shipped P3a minted the sibling Research-area `SUBSTRATE_LANDSCAPE_DOCTRINE.md` (per `D-IH-84-G` DoD-recursive posture). Tech-Lab extension can ship as a separate follow-on tranche if operator desires (the doctrine canonical is currently complete enough to support I84 P4 ratification; extension is value-added, not blocking).
- **People `HOLISTIKA_AGENTIC_DOCTRINE.md` cross-reference review** — F5 hybrid per-task framing may warrant a cross-reference paragraph from the People doctrine to this Research doctrine + the Tech-Lab landscape per the agentic-triangle pattern. Light-touch; no anti-jargon risk since the cross-reference is hyperlink-only.
- **SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md propagation** — fires when the substrate-audit-cadence SOP promotes from `status:review` to `status:active` (gated on operator-pending `process_list.csv` row `env_tech_dtp_substrate_landscape_mtnce_001` mint).

## 8. Cross-references

- [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md) — paired SOP; this report follows its 5-element audit shape.
- [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) — paired Research-area doctrine; this report grounds in its section 3 5-element shape.
- [`SUBSTRATE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) — canonical state-of-record; every `SUBS-*` substrate_id cited in this report FK-resolves here.
- [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) — P1 audit (the landscape element source).
- [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) — P2 scorecard (the scorecard element source).
- [`competitive-layer-positioning.md`](competitive-layer-positioning.md) — Tier-1 WIP thread B (competitive element source).
- [`regulatory-tos-forecast.md`](regulatory-tos-forecast.md) — Tier-1 WIP thread C (regulatory element source).
- [`past-poc-translation-matrix.md`](past-poc-translation-matrix.md) — Tier-1 WIP thread D (past-PoC element source).
- [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md) — ADVOPS engagement scoping (cross-link from section 4.5).
- [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) — I84 master-roadmap (this report is the master-roadmap section 3 P7 deliverable).
- [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/decision-log.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/decision-log.md) — D-IH-84-A through D-IH-84-H full rationale.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — Tech-Lab canonical paired with the Research-side doctrine.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) — People canonical; cross-area handoff target for any AIC framing material change per section 7.
- [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) — cross-area handoff SOP that fires per section 7.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) section 17 — Tier-1 WIP convention this folder follows.
- [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) — vault classification; this report is Tier-1 reference-only.

## 9. Provenance and confidence labels

Authored at I84 Wave A3 (parallel-to-P4-foreground gate per I86 successor-pickup) 2026-05-17. Confidence `B2` (Holistika-internal-research-synthesis) overall; per-row attribute claims inherit per-row `[ext]` flags from the upstream P1 audit + Tier-1 WIP threads. Sections 6 and 7 carry `<!-- post-P4 substitution -->` placeholder blocks awaiting operator ratification at the I84 P4 batched gate.

**Brand-baseline-reality posture.** This report is internal Research-area working-space (access_level: 5) per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) classes; the internal register (per [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc)) is fine throughout. No sections of this report are explicitly external-quotable; if any future cycle promotes synthesis content to public-facing surface (e.g., founder bio update; brand voice update), translate to external register at promotion time.

**Cycle close.** This founding-cycle (`substrate-audit-2026-Q2`) baseline ships under the I84 initiative folder context. Subsequent cycles (`substrate-audit-2026-Q3` and beyond) ship as stand-alone cadence artifacts under [`docs/wip/intelligence/`](../) once the SOP promotes to `status: active` (after process_list row `env_tech_dtp_substrate_landscape_mtnce_001` mints per SOP-META ordering — operator-pending tranche).
