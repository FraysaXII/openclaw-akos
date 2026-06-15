---
intellectual_kind: research_action_charter
authored: 2026-06-14
last_review: 2026-06-14
trigger: Operator request — MADEIRA brand manifesto as harmonization spine for v3.2 closed alpha; vendor-agnostic substrate; full capability discovery across HLK v3.0 areas
parent_brand: MADEIRA
related_initiatives:
  - INIT-OPENCLAW_AKOS-76   # Madeira elevation
  - INIT-OPENCLAW_AKOS-74   # madeira-agent hosted/SDK
  - INIT-OPENCLAW_AKOS-96   # Research data plane + Research Center
  - INIT-OPENCLAW_AKOS-97   # Infonomics / data economics P0
  - INIT-OPENCLAW_AKOS-83   # KiRBe
  - INIT-OPENCLAW_AKOS-49   # MADEIRA management rollup
  - INIT-OPENCLAW_AKOS-84   # Substrate doctrine
  - INIT-OPENCLAW_AKOS-90   # Routing and wiring
status: active_research
audience: J-OP, J-AIC
language: en
---

# Research charter — MADEIRA brand capability harmonization + v3.2 closed alpha readiness

## Decision-first question

**Can MADEIRA (the product brand) open a v3.2 methodology-lane closed alpha only after we have a governed, cross-initiative inventory of capabilities, context planes, journeys, economics, and substrate adapters — with explicit gap closure for prompt/cache/postprocessing and anti-vendor-lock wiring?**

## Why MADEIRA as the spine

MADEIRA is the hardest surface we operate: multi-mode agent, vault-governed context, sibling-repo UI, eval harness, finops/token paths, and operator journey substitution. If wiring works here, it generalizes across HLK v3.0 areas and initiatives. The operator's intent (2026-06-13/14): use this project to **discover, polish, and harmonize** capabilities — not to treat OpenClaw as the product.

## Scope (in)

| Layer | What we inventory |
|:---|:---|
| **Substrate** | OpenClaw, LangChain, LlamaIndex, Make, n8n, Cursor SDK, future Rust/Nyx/sandbox paths — via adapter registry + thin-runtime doctrine |
| **Context planes** | Vault canonicals, KiRBe index, MCP tools, rules/skills, prompt tiers, cache boundaries, compaction, postprocessing |
| **Journeys** | Cursor-local, sibling vault workspace, hosted/SDK, multi-org voice (later) — per-mode expectations + experiential UAT bar |
| **Economics** | Finops registers, token economy, infonomics (I97), data contracts, BI consumers |
| **Ops** | Observability (Langfuse/OTEL), scalability, deploy-health, gateway health (CO-90-004) |
| **Governance** | Cross-area HLK wiring, Quality Fabric 5-axis, MADEIRA three-lights, capability registry |

## Scope (out — this research pass)

- Canonical CSV mint without operator gate
- Production multi-tenant launch
- Vault folder rename to `v3.2/` (methodology lane only per release taxonomy SOP)
- Replacing OpenClaw in this tranche (research informs adapter doctrine; execution is phased)

## Prongs

| Prong | Topic | Primary internal anchors |
|:---:|:---|:---|
| **P-A** | Substrate agnosticism + adapter pattern | I84 substrate audit, AGENTIC_FRAMEWORK_LANDSCAPE, SUBSTRATE_REGISTRY |
| **P-B** | Context / prompt / cache / postprocessing | Prong E wave R+4, KiRBe, rules/skills mass, arXiv cache study |
| **P-C** | User journey + functionality expectations | I17 mode parity, I47 personas, experiential UAT charter, alpha playbooks |
| **P-D** | Model management + finops + token economy | model-selection note, FINOPS registers, LiteLLM/gateway patterns |
| **P-E** | Observability + scalability | Langfuse, telemetry, release-gate, gateway repair |
| **P-F** | Data plane e2e + infonomics | I96, I97, DATA_CONTRACT, KiRBe ingest |
| **P-G** | Brand + Quality Fabric + multi-tenant posture | MADEIRA tool catalog, three-lights, brand registers |
| **P-H** | v3.2 closed alpha readiness crosswalk | SOP-RELEASE_TAXONOMY_001, beta exit gates, capability matrix |

## Deliverables (this folder)

- `source-ledger.csv` — rated sources (internal + external)
- `prong-synthesis-*.md` — eight prong syntheses
- `master-synthesis.md` — load-bearing findings + gap register
- `capability-functionality-inventory-matrix.md` — cross-initiative capability map
- `research-action-pack.md` — govern → implement → test loop for next tranches

## Verification

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv
```

## Promotion path (scheduled — not dropped)

Stable findings → inline-ratify → I76 charter amendment or forward initiative → vault touch under Envoy Tech Lab / MADEIRA-AKOS → INTELLIGENCEOPS_REGISTER row update → carryover index CO entries.
