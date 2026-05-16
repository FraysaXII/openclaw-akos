---
evidence_id: competitive-layer-positioning-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 §3.5 Option D execution
classification: intelligence (working-space; not canonical SSOT)
access_level: 5
language: en
target_initiatives: [INIT-OPENCLAW_AKOS-84]
target_strands:
  - I84 P1 Layer 1 Thread B (competitive layer)
  - I84 P4 D-IH-84-D (MADEIRA productization shape ratification — competitive positioning informs library-vs-agent-vs-hybrid)
  - I84 P3 §7 (OpenClaw/LlamaIndex/Cursor-SDK retrospective — competitive context for substrate choice)
confidence_level: B2
source_taxonomy: holistika-internal-research-synthesis
---

# Competitive layer positioning — Tier-1 WIP (2026-Q2)

> **Scope.** Per [master-roadmap §3 P1 Layer 1 thread B](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) — the **competitive layer** of the substrate landscape. Eight vendors whose products overlap, adjacent, or could plausibly displace Madeira's value proposition. Each row carries structured attributes (positioning, value-prop, differentiation axis, threat-level, MADEIRA-implication) so the P4 batched ratification (specifically `D-IH-84-D` MADEIRA productization shape) has competitive evidence to weigh.

## 1. Audit scope and confidence posture

The 8 competitors per [master-roadmap §3 P1](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) Layer 1 thread B list. Categorised in three loose families:

- **Intelligence-layer competitors** (closest to Madeira's stated positioning per [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) §1): Glean, Notion AI, Anthropic Projects.
- **Distribution/runtime competitors** (where Madeira would deploy if D2 hosted-agent shape ratifies): OpenAI Apps SDK, Microsoft Copilot Studio, Google Gemini for Workspace.
- **Tool catalog / orchestration competitors** (where Madeira would integrate / depend on if D1 library shape ratifies): Composio, Lindy.

Confidence `B2` throughout (Holistika-internal-research-synthesis); per-row `[ext]` flags should be re-verified before any competitor analysis writes to a public-facing surface (e.g., brand positioning doc) per [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) dual-register discipline.

## 2. Intelligence-layer competitors (closest to Madeira positioning)

### 2.1 Glean

| Attribute | Value |
|:---|:---|
| Vendor | Glean Technologies Inc. |
| Founded | 2019 |
| Positioning (2026-Q2) | "Enterprise AI work assistant" / "intelligence layer beneath the interface" `[ext]` — directly Madeira's stated positioning per [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) §1 founder framing |
| Value proposition | Federated search across 100+ enterprise SaaS sources (Drive, Slack, Notion, Salesforce, etc.) + LLM-grounded answers + workflow automation. Sits as horizontal layer beneath whatever apps the operator already uses. |
| Differentiation axis | Federation depth (100+ connectors) + enterprise-grade RBAC + permission-aware retrieval (answers respect source-system ACLs by design) |
| Pricing model | Seat-billed; enterprise contracts; no public per-seat pricing `[ext]` (typically $30-50/user/mo at enterprise scale) |
| Funding / scale | $260M Series E 2024; valuation $4.6B `[ext]`; ~700 enterprise customers |
| Threat level to Madeira | **HIGH** — directly overlaps stated positioning; well-funded; mature product; permission-aware retrieval is a non-trivial technical moat |
| Madeira differentiation candidates (per `D-IH-84-D`) | (a) Holistika-method-shaped — Madeira IS the methodology, not just a generic LLM assistant; (b) ERP-transformable canonicals — Madeira reads + reasons over `compliance.*` mirror schema, not just unstructured doc indexes; (c) Resonance-area discipline — Madeira's brand-voice register is operator-method-tuned, not generic-corporate |
| MADEIRA-implication | **D2 (hosted-agent)** path puts Madeira on direct collision with Glean for "intelligence layer" enterprise positioning; **D1 (library-only)** path sidesteps the competition entirely (Madeira ships as toolkit consumed by orgs that already have or don't want a Glean-shaped layer); **D3 (hybrid)** is moot vs Glean since Glean has no library form |
| Notes | The Madeira-positioning gravitational pull toward "intelligence layer" was named in [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) §1 — knowing Glean owns this phrase at enterprise scale should weigh on `D-IH-84-D` ratification |

### 2.2 Notion AI

| Attribute | Value |
|:---|:---|
| Vendor | Notion Labs Inc. |
| Founded | 2013 (Notion); AI features 2023+ |
| Positioning (2026-Q2) | "AI in the doc you already work in" — workspace-embedded AI assistant `[ext]` |
| Value proposition | Search + write + summarise + Q&A across Notion workspace + connected apps (Drive, Slack, GitHub). Less federated than Glean but deeper integration within Notion. |
| Differentiation axis | Workspace-native (Notion users get AI without context-switching) + low-friction adoption (turnkey for existing Notion customers) |
| Pricing model | $10/user/mo add-on to existing Notion plan `[ext]` |
| Funding / scale | $343M Series C 2021; $10B valuation `[ext]`; ~30M users |
| Threat level to Madeira | **MEDIUM** — different distribution (workspace-tool not standalone-intelligence-layer); not directly methodology-shaped |
| Madeira differentiation candidates | (a) Madeira is method-shaped, not workspace-shaped — it doesn't compete on the doc-editing surface; (b) operator-facing AI in Holistika doesn't require Notion adoption (we run on Cursor + boilerplate + hlk-erp surfaces; Notion is not an operator daily-driver in our stack); (c) the AKOS canonicals are Markdown-in-git, not Notion documents — different distribution origin |
| MADEIRA-implication | Largely orthogonal — Madeira's competitive lane is not Notion's; the comparison is informative for understanding "workspace-embedded AI is the dominant 2026 pattern" but doesn't directly bear on D-IH-84-D |
| Notes | Relevant if Holistika ever adopts Notion as workspace; current AKOS stack does not |

### 2.3 Anthropic Projects

| Attribute | Value |
|:---|:---|
| Vendor | Anthropic |
| Founded | 2021 (Anthropic); Projects feature 2024 `[ext]` |
| Positioning (2026-Q2) | "Persistent workspaces for Claude conversations" — context-window-scaling via Projects + Files + custom instructions `[ext]` |
| Value proposition | Per-project persistent context (system prompt + Files + history) accessible across Claude conversations. Closest first-party analogue to a "Madeira methodology workspace". |
| Differentiation axis | Frontier model quality (Claude is one of top-3 frontier-model providers `[ext]`) + native first-party UX (no SDK assembly required) |
| Pricing model | Bundled with Claude Pro ($20/user/mo) and Claude Team ($25/user/mo) `[ext]` |
| Funding / scale | $7.3B+ raised; valuation ~$60B `[ext]`; market-leader-tier AI safety positioning |
| Threat level to Madeira | **MEDIUM-HIGH** — Projects is a first-party "persistent agent workspace" that captures part of the Madeira workspace-feel; less methodology-shaped than Madeira would be; doesn't carry AKOS canonicals natively |
| Madeira differentiation candidates | (a) Madeira IS the method, not a generic project workspace — the doctrine vocabulary, the LOGIC_CHANGE_LOG awareness, the engagement-template promotion machinery, the brand-voice register all are Madeira-specific; (b) Anthropic Projects requires the operator to construct the workspace themselves — Madeira ships with the methodology pre-loaded |
| MADEIRA-implication | If `D-IH-84-D` ratifies **D2** (hosted-agent), the comparison is "Madeira-as-hosted-agent vs Claude-Project-with-AKOS-Files-attached". The differentiator must be the methodology + persistence shape, not raw model capability |
| Notes | The Claude Code SDK substrate (per [`p1-substrate-landscape-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) §4.2) is the SDK-side complement of Anthropic Projects; the two together form a credible "Claude + Files + SDK" surface |

## 3. Distribution/runtime competitors

### 3.1 OpenAI Apps SDK

| Attribute | Value |
|:---|:---|
| Vendor | OpenAI |
| Founded | 2015; Apps SDK 2025-Q4 GA `[ext]` |
| Positioning (2026-Q2) | "Build and distribute AI apps in ChatGPT" — distribution layer for third-party AI agents inside ChatGPT app store `[ext]` |
| Value proposition | Apps SDK developers ship agent-apps that ChatGPT users can invoke (analogue to mobile app stores). Plus first-party distribution to ChatGPT's hundreds-of-millions-of-MAU user base `[ext]`. |
| Differentiation axis | Distribution scale (ChatGPT user base) + first-party UX inside ChatGPT |
| Pricing model | Free SDK + ChatGPT subscription gate for end-users + revenue-share for app developers `[ext]` |
| Funding / scale | $13B+ raised; valuation $500B `[ext]`; ChatGPT 800M+ weekly users `[ext]` |
| Threat level to Madeira | **MEDIUM** — distribution channel competitor (if Madeira ships as consumer-facing app); not relevant if Madeira stays B2B-Holistika-internal or B2B-enterprise |
| Madeira differentiation candidates | If competing in ChatGPT app store: (a) methodology-shaped value prop (no other ChatGPT app ships the Holistika doctrine); (b) operator-method-tuned brand voice; (c) ERP-transformable canonicals as differentiator vs generic doc-RAG apps |
| MADEIRA-implication | Only relevant if Madeira eventually ships as a ChatGPT app — a TRIGGER-3+ scenario not in the founder-framing 2026-05-16 directive. **Out of scope for current `D-IH-84-D` ratification cycle**; flag for future if ChatGPT-app-store distribution becomes a Madeira product channel |
| Notes | The OpenAI Agents SDK substrate (per [`p1-substrate-landscape-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) §4.3) is the SDK-side complement of Apps SDK — building on OpenAI Agents SDK creates a forward-compatible path to Apps SDK distribution if that channel opens later |

### 3.2 Microsoft Copilot Studio

| Attribute | Value |
|:---|:---|
| Vendor | Microsoft |
| Founded | (Microsoft); Copilot Studio 2024 `[ext]` |
| Positioning (2026-Q2) | "Low-code build for enterprise Copilot agents" — bring your business data, build custom Copilot, deploy across M365 surfaces `[ext]` |
| Value proposition | Enterprise-grade Copilot builder for M365 customers. Pre-built connectors to all Microsoft services. Targets the "enterprise IT department builds custom AI assistants" persona. |
| Differentiation axis | M365 distribution + enterprise IT-grade deployment story + low-code abstraction |
| Pricing model | $200/tenant/mo + per-message billing `[ext]` |
| Funding / scale | Microsoft scale; enterprise penetration ~70% of Fortune 500 has M365 |
| Threat level to Madeira | **LOW** — different persona (enterprise IT department building generic Copilot agents) + different distribution (M365); doesn't overlap Madeira's founder-method-shape |
| Madeira differentiation candidates | Madeira is not a Copilot builder; not relevant to direct competition |
| MADEIRA-implication | Largely orthogonal. Relevant only if Holistika-clients-of-Madeira are enterprises already standardised on Copilot Studio — then Madeira may need a Copilot Studio adapter for in-app embedding |
| Notes | If a future engagement targets a Microsoft-standardised enterprise, the Copilot Studio integration becomes a competitive necessity. Out of scope for `D-IH-84-D` substrate-choice ratification |

### 3.3 Google Gemini for Workspace

| Attribute | Value |
|:---|:---|
| Vendor | Google |
| Founded | (Google); Gemini for Workspace 2024 `[ext]` |
| Positioning (2026-Q2) | "AI assistance in Google Docs / Sheets / Slides / Gmail / Drive / Meet" `[ext]` |
| Value proposition | Workspace-native AI bundled with Google Workspace subscription. Pre-built Workspace integration; no extra deployment. |
| Differentiation axis | Workspace distribution + Gemini frontier-model + zero-friction-deployment for Workspace customers |
| Pricing model | Bundled with Workspace plans (Business Plus $18/user/mo includes AI as of 2024) `[ext]` |
| Funding / scale | Google scale; ~10M+ paying Workspace organisations |
| Threat level to Madeira | **LOW** — workspace-tool not methodology-shaped; no direct overlap |
| Madeira differentiation candidates | Same as Notion AI (§2.2) — Madeira's lane is method-shape, not workspace-embedded |
| MADEIRA-implication | Orthogonal. Pattern-relevant: "frontier model bundled into existing workspace tools at zero marginal cost" is the dominant 2026 enterprise AI pattern; Madeira's value-prop must be incremental over this baseline |
| Notes | Holistika does not use Google Workspace as primary surface; Workspace AI features don't compete directly |

## 4. Tool catalog / orchestration competitors

### 4.1 Composio

| Attribute | Value |
|:---|:---|
| Vendor | Composio (RagaAI / SignalCraft Inc.) |
| Founded | 2024 `[ext]` |
| Positioning (2026-Q2) | "150+ tools your AI agent can use" — pre-built tool catalog for agentic workflows `[ext]` |
| Value proposition | Pre-integrated tool surface (Slack, GitHub, Linear, Gmail, Notion, etc.) consumable by any agent framework (LangChain, LangGraph, CrewAI, etc.). Eliminates the "build the integration shim per tool" tax. |
| Differentiation axis | Breadth of tool catalog + framework-agnostic adapter pattern |
| Pricing model | Token-billed + seat-billed for enterprise tier `[ext]` (free tier with limits) |
| Funding / scale | Series A 2025 `[ext]`; growing rapidly |
| Threat level to Madeira | **NIL as competitor; POTENTIAL DEPENDENCY** — Composio is not a Madeira-shaped product; it's an upstream integration layer Madeira could consume |
| Madeira differentiation candidates | N/A — Composio is in a different layer (tool catalog, not agent runtime or methodology) |
| MADEIRA-implication | If `D-IH-84-D` ratifies **D1 (library-only)** and the library needs to integrate with operator tools (Slack, Linear, GitHub, etc.), Composio is a candidate dependency vs building each integration in-house. Trade-off: dependency on yet another vendor vs in-house engineering cost |
| Notes | The MCP server topology in [`AGENTIC_FRAMEWORK_LANDSCAPE.md` §3](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) is the AKOS-native alternative to Composio — Holistika has been building per-vendor MCP servers (Supabase, Sentry, Slack, GitHub, Stripe, etc.) rather than depending on Composio. Pattern decision: continue MCP-server-per-vendor (Holistika owns the integration; high quality) vs swap to Composio (single vendor for breadth; quality varies) |

### 4.2 Lindy

| Attribute | Value |
|:---|:---|
| Vendor | Lindy AI Inc. |
| Founded | 2023 `[ext]` |
| Positioning (2026-Q2) | "Build AI agents that handle your work" — no-code AI agent builder for SMBs and individuals `[ext]` |
| Value proposition | Drag-and-drop agent builder + 1000+ pre-built integrations + scheduled / event-triggered execution. Targets the "no-code AI agent for individuals + SMBs" market. |
| Differentiation axis | No-code abstraction + breadth of pre-built agents + freemium go-to-market |
| Pricing model | Free tier + $50/mo Pro + $200/mo Business `[ext]` |
| Funding / scale | Seed + Series A `[ext]`; consumer + SMB focused |
| Threat level to Madeira | **LOW** — different persona (no-code SMB users) + different distribution (consumer / SMB freemium); doesn't overlap Madeira |
| Madeira differentiation candidates | Madeira is methodology-shaped + B2B + founder-companion-tier; not no-code-SMB |
| MADEIRA-implication | Orthogonal. Pattern-relevant: "no-code AI agent builders are the 2026 SMB go-to-market pattern"; if Madeira ever targets SMBs, a no-code surface may be necessary. Not in current scope |
| Notes | Comparison useful for understanding the broader "AI agent product" market; not direct competition |

## 5. Aggregate findings (4 observations)

1. **The "intelligence layer" positioning is contested.** Glean owns the phrase at enterprise scale; Anthropic Projects + Claude Code SDK form a credible first-party alternative. Madeira's claim to "intelligence layer beneath the interface" per [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) §1 must differentiate on a non-rhetoric axis — the methodology-shape + ERP-transformable canonicals + brand-voice register are the strongest differentiators that don't collapse on direct comparison.

2. **D-IH-84-D productization shape choice maps to a competitive lane choice.** D2 hosted-agent puts Madeira on direct collision with Glean + Anthropic Projects (enterprise intelligence layer; well-funded; mature). D1 library-only sidesteps these competitors entirely (Madeira ships as toolkit; consumers integrate). D3 hybrid hedges. **Strategic implication for P4 ratification**: D2 requires Madeira to win on differentiation against $4-60B-funded competitors; D1 requires Madeira to win on toolkit quality + adoption among orgs that want methodology-as-toolkit. The competitive bar is higher for D2 but the addressable market is larger.

3. **Tool catalog layer is not a competitor; it's a dependency choice.** Composio is the canonical alternative to building per-vendor MCP servers in-house. Holistika's current pattern is in-house (Supabase MCP, Sentry MCP, Slack MCP, etc.); Composio would consolidate breadth but reduce control quality. This is a sub-decision under D1 library-only path (if D1 ratifies); not relevant under D2/D3.

4. **Workspace-embedded AI is the dominant 2026 enterprise pattern (Notion AI, Google Gemini for Workspace, Microsoft Copilot Studio).** This pattern doesn't compete with Madeira directly (different persona, different distribution), but raises a strategic question: is Madeira a "workspace tool the operator opens" or "a method that runs through whatever tools the operator already has"? The latter framing matches the I76 operating story ("MADEIRA is a method that runs on an agent runtime") and suggests D3 hybrid is the natural fit — Madeira-as-policy-layer-plus-toolkit consumed by the operator's existing tools (Cursor SDK, etc.).

## 6. Implications for `D-IH-84-D` (MADEIRA productization shape)

The competitive analysis sharpens the three productization options:

- **D1 (library-only)**: lowest competitive friction; positions Madeira as toolkit consumed by orgs with their own runtime; differentiation = methodology + canonicals + brand voice; market = teams that want methodology-as-toolkit; closest analogues = LangGraph templates, CrewAI crews; pricing model = per-seat or per-org license
- **D2 (agent-only)**: highest competitive friction; positions Madeira as hosted intelligence layer; direct competition with Glean + Anthropic Projects; differentiation must be operator-method-shape + Holistika brand voice — both narrower than competitors; market = orgs that adopt Holistika methodology; pricing model = seat-billed similar to Glean
- **D3 (hybrid)**: hedges competitive risk; library form for technically-mature customers (low friction) + agent form for less-technical (higher market reach); operational complexity higher; pricing model = per-product

## 7. Cross-references

- [I84 master-roadmap](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) §3 P1 Layer 1 thread B — the deliverable contract.
- [I84 P1 audit report](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) — paired audit (Thread A scope).
- [I84 P2 scorecard](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) — `D-IH-84-D` mapping per substrate class.
- [I84 decision-log](../../planning/84-substrate-doctrine-and-commercial-readiness/decision-log.md) D-IH-84-D — the productization-shape decision this analysis feeds.
- [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) — Madeira elevation; positioning vocabulary cross-references.
- [`i74-brand-tooling-productization.md`](../../planning/_candidates/i74-brand-tooling-productization.md) — productization candidate; D1/D2/D3 mapping aligns with i74 Strand C `@holistika/madeira-agent` packaging shape.
- [`MADEIRA-AKOS/STATUS.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md) §3 TRIGGER-1 + TRIGGER-2 — productization triggers that gate D-IH-84-D activation.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) §3 MCP server topology — Composio alternative to MCP-server-per-vendor pattern.
- [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — dual-register discipline if any of this competitive prose flows to external-facing surfaces.
