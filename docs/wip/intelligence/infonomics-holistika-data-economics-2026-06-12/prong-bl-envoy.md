---
intellectual_kind: research_prong
prong: BL-ENVOY
topic_cluster: agentic-context-economics
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
downstream_decision: D-INF-ECON
linked_research_sources:
  - SRC-INF-INT-013
  - SRC-INF-INT-095
  - SRC-INF-EXT-093
  - SRC-INF-EXT-100
  - SRC-INF-EXT-300
---

# Prong BL-ENVOY — Envoy / MADEIRA (agentic context & token economics)

> Per [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md). Feeds **D-INF-ECON**: unit economics of agent context, tool RBAC, persistence, and seat routing.

## Header

| Field | Value |
|:---|:---|
| Baseline prong | `BL-ENVOY` — Envoy Tech Lab / MADEIRA consumer |
| Ledger rows | **54** cumulative (18 CORPINT + 36 OSINT) |
| Skeptic / tradeoff voices | **10** rows (agent hype, vendor CLI lock-in) |
| Downstream decision | **D-INF-ECON** — price agentic labour and context as information assets |

## Narrative findings

### E.1 MADEIRA registries already encode per-task agent economics

MADEIRA_AIC_PER_TASK_REGISTRY (`SRC-INF-INT-013`) ties tasks to model/seat patterns; PERSISTENCE_VEHICLE_REGISTRY (`SRC-INF-INT-023`) and TOOL RBAC (`SRC-INF-INT-058`) price storage + permission surfaces; TOOL CATALOG (`SRC-INF-INT-095`) and AGENTIC FRAMEWORK LANDSCAPE (`SRC-INF-INT-092`) inventory capability supply. RevOps handoff SOP (`SRC-INF-INT-024`) and UX review SOP (`SRC-INF-INT-043`) attach human gate labour. **Holistika delta:** context is not fungible tokens — it is **governed tool + persistence tuples** with RBAC.

### E.2 MCP + multi-agent OSINT defines integration tax for agent stacks

MCP specification (`SRC-INF-EXT-093`) and servers repo (`SRC-INF-EXT-094`), LangGraph (`SRC-INF-EXT-092`), OpenAI Agents SDK (`SRC-INF-EXT-091`), CrewAI/AutoGen/Semantic Kernel (`SRC-INF-EXT-096`–`098`) show exploding adapter count into agent runtime. Normalized Adapter Pattern on BL-ADAPTER must converge with MADEIRA tool catalog — otherwise **double TCO** (adapter registry + agent tool registry).

### E.3 Orchestration runners compete on human+AIC dispatch cost

Nx/Turborepo/Just/Invoke/Make (`SRC-INF-EXT-077`–`081`) and agent CLIs (Cursor `SRC-INF-EXT-082` skeptic vendor-specific, Claude Code `SRC-INF-EXT-083`, Aider `SRC-INF-EXT-084`) compete for default execution seat. Cursor agent modes (`SRC-INF-EXT-300`) document thinking vs execution routing — maps to Holistika two-seat doctrine. Infonomics must meter **seat minutes × context window**, not only API tokens.

### E.4 Skeptic corpus restrains agent-hype capitalization

Agent hype skeptic (`SRC-INF-EXT-100`, Ben Evans 2025), model eval skeptic (`SRC-INF-EXT-306`), Windsurf skeptic (`SRC-INF-EXT-301`), agent CLI hype (`SRC-INF-EXT-496`) warn against capitalizing unproven agent throughput. MADEIRA MODE PARITY (`SRC-INF-INT-094`) and METHODOLOGY MODE (`SRC-INF-INT-093`) are internal counters — Infonomics should expense R&D agent experiments separately from production engagement agents.

### E.5 Rendering + scenario lifecycle close the agent output asset loop

RENDERING_PIPELINE_REGISTRY (`SRC-INF-INT-059`), MADEIRA PLATFORM strategy doc (`SRC-INF-INT-099`), scenario lifecycle SOP (`SRC-INF-INT-100`) tie agent outputs to deliverable assets (PDF, deck, ERP). Agent context spend without registered output consumer (`BI_CONSUMER` pattern on BL-DATA) is **pure cost**.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political / regulatory | Tool RBAC (`SRC-INF-INT-058`) and agentic infra SOP (`SRC-INF-INT-096`) anticipate policy on autonomous action — compliance cost embedded in permission matrix. |
| **E** | Economic | Agent hype skeptic (`SRC-INF-EXT-100`) vs per-task registry (`SRC-INF-INT-013`) — capitalize only tasks with FinOps tag; CLI vendor skeptics (`SRC-INF-EXT-082`, `496`) raise switching cost. |
| **S** | Social | Human-in-the-loop patterns (AutoGen HITL on BL-OPS `SRC-INF-EXT-348` cross-ref) — social acceptance of agent labour requires UX review SOP (`SRC-INF-INT-043`). |
| **T** | Technological | MCP (`SRC-INF-EXT-093`–`094`) as lingua franca; multi-framework sprawl (`SRC-INF-EXT-091`–`098`) increases integration depreciation rate. |
| **E** | Environmental | Persistence vehicles (`SRC-INF-INT-023`) — stale context stores are digital waste; refresh policy is environmental Infonomics for token-heavy agents. |
| **L** | Legal | MADEIRA TOOL RBAC + personality SOPs (`SRC-INF-INT-098`) bound lawful tool use; agent outputs crossing external register require brand dual-register (BL-MKT cross-ref). |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | Model vendors + IDE agents (Cursor `SRC-INF-EXT-300`, Copilot CLI `SRC-INF-EXT-313`) control pricing; MCP servers (`SRC-INF-EXT-094`) add connector fees. |
| **Buyer power** | RevOps/PMO consumers (`SRC-INF-INT-024`) demand attributable agent outcomes — uninstrumented agents lose budget. |
| **Threat of substitutes** | Manual operator execution substitutes agent cost with people cost; per-task registry (`SRC-INF-INT-013`) enables substitution analysis. |
| **Threat of new entrants** | Gemini CLI / Amazon Q CLI (`SRC-INF-EXT-311`–`312`) — commoditise coding agents; Holistika differentiates on MADEIRA governance stack. |
| **Competition synthesis** | Envoy Infonomics wins on **instrumented context per deliverable**, not raw agent count. 54-row depth supports token+tool+ persistence composite cost model; skeptics (`SRC-INF-EXT-100`) block inflated asset capitalization. |

## Infonomics hook

**Economic levers:** tokens per task (`SRC-INF-INT-013`), tool call count, persistence GB-hours (`SRC-INF-INT-023`), seat routing premium (thinking vs execution), render pipeline cost (`SRC-INF-INT-059`).

**Holistika delta:** MADEIRA already registers tasks/tools/persistence — extend with FinOps columns; avoid third-party-only telemetry (Helicone on BL-TECH) without vault row linkage.

**Govern options (ranked; no vault edit):**

1. **OPTION A (recommended)** — Extend MADEIRA_AIC_PER_TASK_REGISTRY + TOOL RBAC with `context_budget_tokens`, `finops_cost_center`, `output_artifact_class` — ties spend to deliverables.
2. **OPTION B** — Unified agent FinOps dashboard (Langfuse/OpenTelemetry cross-ref from BL-DATA `SRC-INF-EXT-346`–`347`) — rich telemetry, weaker canonical SSOT unless mirrored into registries.
3. **OPTION C** — Flat per-initiative agent budget caps — simple, blinds per-tool ROI (`SRC-INF-INT-095`).
4. **OPTION D** — Outsource agents to vendor IDE only — skeptic blocked (`SRC-INF-EXT-100`, `496`); **scheduled** only if operator ratifies vendor spine.
