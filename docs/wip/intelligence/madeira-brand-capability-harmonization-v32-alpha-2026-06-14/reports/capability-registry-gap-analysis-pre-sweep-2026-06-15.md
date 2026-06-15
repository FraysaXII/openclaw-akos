---
intellectual_kind: gap_analysis
phase: pre_sweep
authored: 2026-06-15
operator_gate: D-MBH-05 full registry review + governance improvements
baseline_validator: validate_capability_registry.py PASS (99 rows)
---

# Capability registry — pre-sweep gap analysis (KB integrity pass)

> **Why now:** v3.2 alpha binds substrate adapters, proof classes, and context economics. The capability map (what Holistika can do) has not been reviewed since **I95 de-densify (2026-06-08)**. This is the best moment to test **knowledge-base integrity for AICs** — validators green, but semantic FKs are hollow.

## Executive summary (plain language)

The registry **passes shape validation** but is **not yet trustworthy for alpha claims** because:

1. **Every row (99/99) has an empty `substrate_id`** — we cannot answer “which runtime realizes this capability?” from the CSV alone.
2. **Alpha inventory (CAP-M01..M30) uses a different ID scheme** than vault rows (`CAP-MADEIRA-*`, `CAP-RES-*`) — no formal crosswalk table.
3. **AIC implementation matrix (ACIM) has 7 rows** vs 99 capabilities — implementation proof is sparse outside MADEIRA verdict + lab platform.
4. **Context economics (CAP-M16..M18) are gaps** in both matrix and registry — now ratified for T2 implementation.

## Baseline metrics (pre-sweep)

| Metric | Value | Risk |
|:---|:---:|:---|
| Registry rows | 99 | — |
| `validate_capability_registry.py` | PASS | Shape only |
| Empty `substrate_id` | **99 (100%)** | **Keter** — breaks substrate-agnostic α0 claim |
| Empty `definition` | 0 | OK (I95-I) |
| Empty `capability_tier` | 0 | OK |
| Empty `l1_domain` | 0 | OK |
| ACIM rows | 7 | **Euclid** — ECB-0006 cannot bind most capabilities |
| SUBSTRATE rows (post-T1b) | 25 | FK target exists but unused |

## Governance lattice gaps (not capability-only)

| Layer | SSOT | Gap |
|:---|:---|:---|
| **Capability** | `CAPABILITY_REGISTRY.csv` | No substrate FK populated; alpha grain mismatches I95 collapse |
| **Implementation** | `AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` | 7/99 coverage; CAP-M* not represented |
| **Substrate** | `SUBSTRATE_REGISTRY.csv` | T1b minted; capability join missing |
| **Proof** | `EVIDENCE_CLASS_REGISTRY` + PROOF_ADAPTER | Gateway proof exists; not linked to capability rows |
| **Context economics** | WIP spec **ratified 2026-06-15** | T2 code not landed (`akos/postprocess.py`, Langfuse fields) |
| **Semantic** | `METRICS_REGISTRY.csv` | No capability_id dimension for economic signals (I97 join) |
| **HCAM** | `CANONICAL_RELATIONSHIP_REGISTRY.csv` | No `REALIZED_ON` triples capability→substrate at scale |

## CAP-M alpha crosswalk (seed → vault)

| Alpha ID | Plain function | Vault anchor (if any) | Pre-sweep verdict |
|:---|:---|:---|:---|
| CAP-M01 | Governed IDE chat | `CAP-CONVERSATIONAL-AI-ENGINE`, `CAP-AGENTIC-OPERATIONS` | **Partial** — merge via crosswalk; needs substrate |
| CAP-M02 | Five MADEIRA modes | *(none)* — lives in `MADEIRA_MODE_PARITY.md` | **Gap** — propose `CAP-MADEIRA-MODE-PARITY` |
| CAP-M03 | Tool category RBAC | *(none)* — `MADEIRA_TOOL_RBAC.csv` | **Gap** — propose `CAP-MADEIRA-TOOL-RBAC` |
| CAP-M04 | Inline operator ratify | I86 rules/skills (not a capability row) | **Gap** — propose `CAP-GOVERNANCE-INLINE-RATIFY` |
| CAP-M05 | Research action loop | `CAP-RES-HXPESTAL-ANALYSIS`, `CAP-RES-KB-PIPELINE-RADAR` | **Partial** |
| CAP-M06 | Research radar freshness | `CAP-RES-KB-PIPELINE-RADAR` | **Partial** |
| CAP-M07 | Research Center UI | *(none at capability grain)* | **Gap** — propose `CAP-MADEIRA-RESEARCH-CENTER` |
| CAP-M08 | KiRBe retrieval | `CAP-KNOWLEDGE-RETRIEVAL-RAG` | **Partial** — substrate `SUBS-HOLISTIKA-KIRBE` |
| CAP-M09 | Ledger → vault promote | Research ingest processes | **Partial** |
| CAP-M10 | Langfuse traces | `CAP-AI-EVALUATION-BENCHMARKING` | **Partial** |
| CAP-M11 | Dossier three-lights | `CAP-MADEIRA-SCENARIO-LIFECYCLE` | **Mapped** |
| CAP-M12 | Gateway health | T1b PROOF_ADAPTER (not capability row) | **Gap** — propose `CAP-OPENCLAW-GATEWAY-HEALTH` |
| CAP-M13 | Two-seat routing | `CAP-AGENTIC-OPERATIONS` + AIC_REGISTRY | **Partial** |
| CAP-M14 | Finops registers | Finance capabilities / FINOPS | **Partial** |
| CAP-M15 | Infonomics framing | *(none)* | **Gap** — I97 join |
| CAP-M16..M18 | Context economics | *(none)* — spec ratified T2 | **Gap** — post-T2 |
| CAP-M19 | OpenClaw normalize | `CAP-AI-AGENT-ORCHESTRATION` | **Partial** — substrate T1b |
| CAP-M20 | Multi-substrate paths | Substrate registry (25 rows) | **Improved** post-T1b |
| CAP-M21 | MCP integration | `CAP-AI-AGENT-ORCHESTRATION` | **Partial** |
| CAP-M22 | Hosted SDK/API | `CAP-MULTIPLATFORM-DEPLOYMENT` | **Partial** |
| CAP-M23 | Deploy health | deploy-health discipline | **Partial** |
| CAP-M24 | Experiential UAT | UAT discipline / PAD-001 | **Partial** |
| CAP-M25 | Quality Fabric | Quality Fabric canonical | **Partial** |
| CAP-M26 | Persona/scenario | PERSONA_SCENARIO_REGISTRY | **Partial** |
| CAP-M27 | Multi-tenant voice | *(none)* | **Gap** — post-α2 |
| CAP-M28 | Browser MCP walk | PAD-001 pattern | **Partial** |
| CAP-M29 | Synthesis-before-tranche | process + validator | **Gap** — governance utility |
| CAP-M30 | Carryover index | OPERATOR_STEERING | **Partial** |

**Count:** 4 mapped, 14 partial, 12 gap (alpha grain finer than I95 collapse).

## Proposed governance improvements (for operator confirm at mint gate)

| ID | Proposal | Touches |
|:---|:---|:---|
| **GCI-01** | **`substrate_id` backfill** on Applied AI & MADEIRA l1_domain rows (minimum 12 rows) | CAPABILITY_REGISTRY |
| **GCI-02** | **`CAPABILITY_ALPHA_CROSSWALK.csv`** (WIP dimension): `alpha_capability_id`, `vault_capability_id`, `relationship` (maps\|extends\|supplements) | New dimension + validator |
| **GCI-03** | **ACIM expansion** — one row per CAP-M gap with `tool_catalog_ref` or validator script | AIC_CAPABILITY_IMPLEMENTATION_MATRIX |
| **GCI-04** | **Validator WARN→FAIL ramp** — empty `substrate_id` when `l1_domain=Applied AI & MADEIRA` and `lifecycle_status=active` | `validate_capability_registry.py` |
| **GCI-05** | **HCAM triple batch** — `CAP-*` `REALIZED_ON` `SUBS-*` for backfilled rows | CANONICAL_RELATIONSHIP_REGISTRY |
| **GCI-06** | **Methodology version refresh** — `methodology_version_at_review=v3.2` on touched rows | Same CSV tranche |

## Out of scope for this sweep (scheduled, not dropped)

- Full 1112-row process→capability re-collapse (I95 area-by-area continues)
- Multi-tenant brand voice (CAP-M27 / CO-MBH-008)
- Supabase mirror DML for capability mirror

## Next step (AIC)

Post-sweep report after: crosswalk CSV draft, proposed registry amendments, validator dry-run, regression compare to this baseline.
