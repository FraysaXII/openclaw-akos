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

<!-- post-P4 substitution: D-IH-84-B/C/D/E batched ratification outcomes -->
<!-- ============================================================== -->
<!-- This block awaits operator answers on the I84 P4 batched         -->
<!-- inline-ratify gate (D-IH-84-B substrate baseline + D-IH-84-C AIC -->
<!-- framing F1-F5 + D-IH-84-D MADEIRA productization shape + D-IH-84-E -->
<!-- KiRBe framework narrowing). The parent agent substitutes this    -->
<!-- block with the ratified outcomes once operator answers in the    -->
<!-- foreground. Structure per cycle:                                 -->
<!--   - D-IH-84-B ratified option (B1 / B2 / B3) + rationale         -->
<!--   - D-IH-84-C ratified option (F1 / F2 / F3 / F4 / F5) + rationale -->
<!--   - D-IH-84-D ratified option (D1 / D2 / D3) + rationale         -->
<!--   - D-IH-84-E narrowed finalists (2 substrates) + rationale     -->
<!--   - Forward-charter implications for each ratification           -->
<!--   - Risk-register updates (R-IH-84-3 batched ratification        -->
<!--     fatigue closeout; R-IH-84-2 column-shape lock-in monitor)   -->
<!-- ============================================================== -->

**Pending P4 substitution.** Until the operator answers, this cycle report reflects the **pre-ratification evidence baseline**. The scorecard surface in section 2 + the regulatory + competitive + past-PoC analyses in sections 3-5 are the inputs the P4 batched ratification weighs; the ratification outcome lands here.

## 7. Cross-area implications

<!-- post-P4 substitution: cross-area cascade per D-IH-84-B/C/D/E      -->
<!-- ============================================================== -->
<!-- This block awaits operator answers on the I84 P4 batched         -->
<!-- inline-ratify gate. After P4, the parent agent substitutes this  -->
<!-- block with the per-candidate cross-area cascade summary:         -->
<!--   - I76 (MADEIRA elevation): unlocked by D-IH-84-C ratification  -->
<!--     (closes C-76-1 AIC framing); Strand A external research      -->
<!--     deliverable substituted by I84 P1 audit dossier              -->
<!--   - I74 (brand-tooling productization): unlocked by D-IH-84-D     -->
<!--     ratification (closes C-74-3 MADEIRA gate-criteria); Cursor   -->
<!--     SDK ToS findings inform C-74-4 license-separation            -->
<!--     enforceability                                                -->
<!--   - I83 (AI archivist + KiRBe ingestor): unlocked by D-IH-84-E    -->
<!--     framework narrowing (closes C-83-1 to 2-finalist choice);    -->
<!--     KiRBe-P0 picks between finalists                              -->
<!--   - I82 (capability doctrine + commercial readiness):            -->
<!--     CAPABILITY_REGISTRY extends with substrate_id FK to          -->
<!--     SUBSTRATE_REGISTRY                                            -->
<!--   - Recommended cross-area pings: Tech Lab                       -->
<!--     AGENTIC_FRAMEWORK_LANDSCAPE.md extension per D-IH-84-B/C;    -->
<!--     People HOLISTIKA_AGENTIC_DOCTRINE.md cross-reference review  -->
<!--     for any AIC framing implications surfaced                    -->
<!-- ============================================================== -->

**Pending P4 substitution.** Cross-area cascade fires per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) workflow once the P4 ratification lands. Pre-staged handoff document at [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/cross-area-unlock-handoff-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/cross-area-unlock-handoff-2026-05-17.md) (sibling to this report; carries the same P4-substitution placeholder structure).

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
