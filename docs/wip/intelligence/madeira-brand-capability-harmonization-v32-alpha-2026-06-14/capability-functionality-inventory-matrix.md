---
intellectual_kind: capability_inventory
authored: 2026-06-14
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
audience: J-OP
---

# Capability ↔ functionality ↔ journey inventory (seed matrix)

> **Purpose.** One place to answer: *what does this do, for whom, how do we know it works, which initiative owns it?* Rows are **seeds** — extend via CAPABILITY_REGISTRY promotion after operator ratify.

Legend: **Maturity** — `Built` | `Partial` | `Gap` | **Evidence** — last proof artifact class

## Core MADEIRA capabilities

| ID | Functionality (plain) | Category | Journeys | Owner initiative | Maturity | Evidence class | Expectation (good looks like) |
|:---|:---|:---|:---|:---|:---|:---|:---|
| CAP-M01 | Chat with governed agent in IDE | Converse | A | I76, I17 | Partial | Eval + gateway | Mode-appropriate tools; no canonical CSV writes without gate |
| CAP-M02 | Five interaction modes (Ask→Methodology) | Converse | A | I17, I76 | Partial | Coverage matrix | Each mode has UC coverage ≥ target; RBAC enforced |
| CAP-M03 | Tool category RBAC (16 cats) | Govern | A | I76 | Built | validate_madeira_tool_rbac | Wrong-mode tool call blocked deterministically |
| CAP-M04 | Inline operator ratification | Govern | A,B | I86 | Built | Rules + skills | Agent stops at CSV/canonical/spine decisions |
| CAP-M05 | Research action loop (ledger→synth) | Research | A,B | I86 | Built | validate_research_action | Every strategic decision has rated sources |
| CAP-M06 | Research radar freshness | Research | B | IntelligenceOps | Partial | validate_research_radar | Staleness posture before govern |
| CAP-M07 | Research Center UI | Research | B | I96 | Partial | Experiential UAT | Post-login panels live; director/operator POVs |
| CAP-M08 | KiRBe retrieval / indexing | Research | A,B | I83 | Partial | Substrate matrix | Index rebuild cadence; query trustworthy |
| CAP-M09 | Source ledger → vault promote | Research | B | I96 | Partial | Ingest contract | WIP intelligence promotes with touch gate |
| CAP-M10 | Langfuse traces + evals | Observe | A,C | I10, I45 | Built | release-gate | Every session attributable; rubric regressions run |
| CAP-M11 | MADEIRA dossier three-lights | Observe | A,B,C | I49 | Built | render_uat_dossier | GO only when all three green |
| CAP-M12 | Gateway health + repair | Observe | A | I90 | Built | gateway-tranche + check-only | RPC+HTTP ready; PROOF_ADAPTER mint T1b |
| CAP-M13 | Two-seat model routing | Economize | A | model-selection | Built | AIC_REGISTRY | Thinking for ratify; execution for tranches |
| CAP-M14 | Finops provider registers | Economize | C | FINOPS | Built | validate_finops | API spend mappable to counterparty |
| CAP-M15 | Infonomics / data value framing | Economize | B | I97 | Partial | I97 charter | Freshness strip shows economic signal |
| CAP-M16 | Prompt/cache boundary policy | Context | A,B,C | **Gap** | Gap | — | Static prefix cached; cost predictable |
| CAP-M17 | Postprocessing pipeline | Context | A,B,C | **Gap** | Gap | — | Brand lint + cite before user sees output |
| CAP-M18 | Context compaction policy | Context | A | **Gap** | Partial | OpenClaw upstream | Long sessions don't rot; per-task rules |
| CAP-M19 | OpenClaw adapter normalize | Substrate | A | I90 | Built | test_openclaw_config | Upstream schema drift absorbed |
| CAP-M20 | LangChain/LlamaIndex/n8n/Make paths | Substrate | A,C | I84 | Partial | Past-PoC matrix | Each method has SUBSTRATE_REGISTRY row |
| CAP-M21 | MCP tool integration | Substrate | A,B | I79 | Built | AGENTIC_FRAMEWORK §3 | Posture read/suggest/write/decide enforced |
| CAP-M22 | Hosted MADEIRA SDK/API | Converse | C | I74 | Partial | I74 roadmap | Deploy smoke + auth |
| CAP-M23 | Deploy health consumer repos | Observe | B,C | deploy-health | Built | CICD smoke | Vercel/Render green + viewports |
| CAP-M24 | Experiential UAT (browser) | Govern | B | I96, experiential charter | Partial | UAT manifests | Operator would sign what they see |
| CAP-M25 | Quality Fabric composition | Brand | A,B,C,D | Quality Fabric | Built | compose_UAT | 5 axes resolved per surface |
| CAP-M26 | Persona/scenario library | Journey | A,B | I47 | Built | PERSONA_SCENARIO_REGISTRY | Alpha cohort from registry rows |
| CAP-M27 | Multi-org brand voice | Brand | D | I76/I74 | Gap | — | Tenancy + cobranding pattern |
| CAP-M28 | Cursor Browser MCP walk | Journey | B | planning traceability | Built | artifacts/uat-screenshots | sha256 manifest per tranche |
| CAP-M29 | Planning tranche synthesis gate | Govern | A | synthesis-before-tranche | Built | validate_synthesis | Scope creep caught pre-commit |
| CAP-M30 | Carryover posture index | Govern | All | OPERATOR_STEERING | Built | carryover index | Deferred ≠ dropped |

## Cross-area HLK wiring (discovered)

| Area | Registers / canonicals touching MADEIRA alpha |
|:---|:---|
| **Envoy Tech Lab** | AGENTIC_FRAMEWORK_LANDSCAPE, MADEIRA_*, OPENCLAW triage SOP |
| **People / Compliance** | CAPABILITY_REGISTRY, SUBSTRATE_REGISTRY, AIC_REGISTRY, PERSONA_SCENARIO |
| **Research** | RESEARCH_ACTION_DISCIPLINE, INTELLIGENCEOPS_REGISTER |
| **Data / Governance** | DATA_CONTRACT_REGISTRY, BI_CONSUMER_REGISTRY |
| **Finance** | FINOPS registers, PRICING_TIER |
| **Marketing / Brand** | Quality Fabric, UX charter, cobranding |
| **Operations** | RevOps adapter pattern, PMO research backlog |

## Priority gaps for alpha (Keter/Euclid)

1. CAP-M16, M17, M18 — context economics (P-B)
2. CAP-M07, M24 — Scenario B experiential PASS (I96)
3. CAP-M12 — CO-90-004 live closure (I90)
4. CAP-M20 — substrate registry completeness (I84)
5. CAP-M15 — infonomics visible on Research Center (I97 × I96)
