---
authored: 2026-06-14
lane: DG-A
parent: t0-c-execution-spec
---

# SUBSTRATE + adapter data governance audit (T0 DG-A)

## Summary

`SUBSTRATE_REGISTRY.csv` already documents **22 substrate rows** including OpenClaw, LangChain, LlamaIndex, Cursor SDK, and pattern rows (thin-adapter, hybrid, KiRBe). **Gaps:** operator-history platforms **Make, n8n, Make swarm** are not registered; **managed cloud agent runtimes** (Bedrock AgentCore, Anthropic Managed Agents) are absent as explicit **rejected/non-portable** rows.

## Visibility gaps (lose sight without DATA_CONTRACT)

| Gap ID | Risk | T1 action |
|:---|:---|:---|
| DG-A-01 | No DATA_CONTRACT for substrate adapter migrations | Draft `DC-HOL-SUBSTRATE-ADAPTER-001` |
| DG-A-02 | Make/n8n not in SUBSTRATE_REGISTRY | Propose rows at CSV gate |
| DG-A-03 | Gateway repair not in PROOF_ADAPTER | Link CO-90-004 to proof class |
| DG-A-04 | Langfuse traces not BI_CONSUMER bound | Proposal row for dossier + finops |
| DG-A-05 | LAB_PLATFORM_DIMENSION not linked to adapter env semantics | I100 charter crosswalk |

## Draft DATA_CONTRACT (WIP — not minted)

| Field | Proposed value |
|:---|:---|
| `contract_id` | `DC-HOL-SUBSTRATE-ADAPTER-001` |
| `owner_area` | Tech / Envoy Tech Lab |
| `consumer_areas` | Research; Operations; Finance |
| `ssot_path` | `SUBSTRATE_REGISTRY.csv` + `AGENTIC_FRAMEWORK_LANDSCAPE.md` |
| `freshness_sla` | `on_change` |
| `proof_class` | `automated+trace` for migration claims; `experiential` for operator-facing substrate switches |

## PROOF_ADAPTER proposals

| adapter_id | proof_surface | evidence |
|:---|:---|:---|
| `PROOF-GATEWAY-REPAIR` | `scripts/openclaw_gateway_repair.py --json` | CO-90-004 |
| `PROOF-LANGFUSE-TRACE` | Langfuse session URL + trace ID | I10 D-EVAL |
| `PROOF-SUBSTRATE-INVENTORY` | `verify_openclaw_inventory.py` | Full inventory contract |

## BI_CONSUMER proposals

| consumer_id | consumes | dashboard use |
|:---|:---|:---|
| `BI-MADEIRA-DOSSIER` | Langfuse cost + eval | Three-lights Section 1 |
| `BI-GATEWAY-HEALTH` | gateway repair JSON | Operator light |
| `BI-SUBSTRATE-AUDIT` | SUBSTRATE_REGISTRY diff | Adapter migration review |

## HCAM triples (draft)

- `SUBSTRATE_REGISTRY` — `GOVERNED_BY` — `SOP-TECH_AGENTIC_INFRA_001`
- `DC-HOL-SUBSTRATE-ADAPTER-001` — `DECLARES` — `SUBSTRATE_REGISTRY`
- `MADEIRA` — `REALIZED_ON` — `SUBS-HOLISTIKA-OPENCLAW` (one row; not exclusive)

## EVIDENCE_CLASS binding

Substrate migration completion claims require **≥ automated inventory PASS + Langfuse trace**; operator-facing "we switched runtime" additionally requires **experiential** dossier note.
