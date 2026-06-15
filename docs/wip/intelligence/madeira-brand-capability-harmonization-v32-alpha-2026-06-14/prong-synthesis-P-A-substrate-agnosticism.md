---
intellectual_kind: research_synthesis_prong
prong_id: P-A
prong_topic: Substrate agnosticism — OpenClaw as method not product
authored: 2026-06-14
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
control_confidence: Euclid
---

# Prong P-A — Substrate agnosticism and adapter doctrine

## Load-bearing finding

Holistika's **2023/24 thesis is now industry consensus**: lock-in moved from the model API to the **execution layer** (managed sessions, sandbox filesystems, append-only agent logs). Your instinct not to vendor-lock to OpenClaw is correct and **already partially encoded** — `AGENTIC_FRAMEWORK_LANDSCAPE` lists OpenClaw as a *thin adapter*; `akos/openclaw_config.py` normalizes upstream drift without forking business logic; `SUBSTRATE_REGISTRY.csv` exists as the promotion target for explicit substrate rows.

External research (April 2026) confirms: portable frameworks (LangChain, LangGraph, LlamaIndex, CrewAI) run on K8s/laptop; **Bedrock Agents / Anthropic Managed Agents / Gemini Agent Runtime are not portable** — migration = rebuild, not config change (SRC-MBH-EXT-001..005).

## Internal evidence map

| PoC lineage | Substrate touched | Translatable to v3.2 alpha |
|:---|:---|:---|
| I10 eval hardening | OpenClaw sandbox + Langfuse | Eval harness + telemetry must survive substrate swap |
| I11 ops copilot | Overlay-only MADEIRA | RBAC-as-config pattern is substrate-agnostic |
| KiRBe parallel | LlamaIndex | Retrieval spine independent of agent runtime |
| Operator history | LangChain, Make, n8n, swarm | Validates multi-method experimentation; needs **registry**, not memory |

## Holistika posture (recommended)

Three-layer stack (matches Augment + Theorem patterns):

1. **Orchestration SSOT** — AKOS scripts, HLK MCP servers, `config/openclaw.json.example` inventory (policy + observability hooks), cursor rules/skills as context plane (not runtime).
2. **Adapter registry** — Extend `REVOPS_ADAPTER_REGISTRY` pattern to **`AGENT_RUNTIME_ADAPTER_REGISTRY`** (proposed; not minted — ratify gate): rows for OpenClaw-local, Cursor-SDK, LlamaIndex-worker, n8n-webhook, Make-scenario, future Rust/Nyx sandbox.
3. **Protocol-neutral tools** — MCP as tool spine (SRC-MBH-EXT-006..008); A2A only when multi-agent delegation is real (I76 dispatcher), not prematurely.

OpenClaw remains **one adapter row** for Cursor-local alpha scenario A, not the brand definition of MADEIRA.

## Gaps (Euclid)

| Gap | Severity | Closure tranche |
|:---|:---|:---|
| No canonical adapter registry for agent runtimes | High | I84/I90 tranche — CSV draft + SOP pair |
| State/session serialization not standardized | High | Research → Pydantic session envelope in `akos/` |
| Make/n8n/LangChain experiments not inventoried | Medium | Capability matrix rows + SUBSTRATE_REGISTRY backfill |
| Managed cloud runtimes not explicitly red-lined in vault | Medium | AGENTIC_FRAMEWORK_LANDSCAPE §1 add "non-portable cloud runtimes" row |

## Ranked insights

1. **Execution-layer lock-in > model lock-in** (EXT-001, EXT-003) — RANK 1
2. **MCP won tool layer; use it as Holistika's integration contract** (EXT-006, INT-028) — RANK 1
3. **OpenClaw = policy wrapper; prove via normalizer + repair runbook, not marketing** (INT-029, INT-015) — RANK 2
4. **Langfuse must remain adapter-agnostic observability spine** (INT-002 D-EVAL) — RANK 2
