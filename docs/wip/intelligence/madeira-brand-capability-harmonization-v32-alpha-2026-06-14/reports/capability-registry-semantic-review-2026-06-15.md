---
intellectual_kind: semantic_review
authored: 2026-06-15
scope: CAPABILITY_REGISTRY 99 rows + pydantic schema
operator_gate: pre-mint evidence for D-IH-76-CAP-GCI
---

# Capability registry — semantic review (99 rows + schema)

> **Functional name:** the “does this capability map make sense?” pass — not just shape validation, but whether names, domains, tiers, and FK targets support alpha claims and AIC queryability.

## Schema assessment (`akos/hlk_capability_registry_csv.py`)

| Field | Verdict | Notes |
|:---|:---|:---|
| `capability_id` | **Keep** | `CAP-[A-Z0-9-]+` stable; 99 unique |
| `capability_name` | **Keep** | No duplicate names |
| `area` vs `l1_domain` | **Keep; document** | 3 intentional splits (e.g. `CAP-AGENTIC-OPERATIONS`: area=People, l1=Applied AI & MADEIRA) — doctrine-owned cross-area |
| `originating_process_ids` | **Keep** | N:N realization; all IDs resolve to process_list or BUILDOUT_BACKLOG |
| `substrate_id` | **Populate + enforce** | HCAM TRP-041 expects FK; 100% empty is the Keter finding |
| `alpha_inventory_refs` | **Propose add** | Semicolon list of `CAP-M*` on vault rows — reuses registry instead of orphan people-table |
| `capability_tier` | **Keep** | 100% populated post-I95 |
| `definition` | **Keep** | 100% populated; no stubs under 20 chars |
| `methodology_version_at_review` | **Refresh** | 97/99 still `v3.1`; touched rows → `v3.2` at mint |

**Proposed schema addition (mint tranche):**

```text
alpha_inventory_refs  # optional; pattern ^(CAP-M[0-9]{2})(;CAP-M[0-9]{2})*$
```

Validator: FK-resolve each `CAP-M*` against crosswalk WIP + matrix; WARN if crosswalk missing until junction promoted.

## Domain distribution (sanity)

| l1_domain | Rows | Alpha touch |
|:---|:---:|:---|
| People, Org Design & Quality Fabric | 20 | M04, M24–M30 governance cluster |
| Product & Platform Engineering | 18 | M12, M19–M23 substrate/observe |
| Corporate Intelligence & Research | 15 | M05–M09 research cluster |
| Go-to-Market & Brand | 13 | M25 brand (via UX quality) |
| Applied AI & MADEIRA | 8 | M01–M03, M10–M11, M16–M18 core |
| Delivery & Client Engagement Operations | 8 | M30 carryover via PMO |
| Finance & Revenue Operations | 6 | M14 |
| Data Governance & Enterprise Knowledge | 6 | M15 infonomics join |
| Legal, Compliance & Privacy | 5 | — |

No orphan domains; counts match I95 collapse intent.

## Semantic flags (actionable)

| ID | Finding | Disposition at mint |
|:---|:---|:---|
| **SEM-01** | 99/99 empty `substrate_id` | Backfill 18 alpha-critical rows (see mint packet) |
| **SEM-02** | Alpha grain finer than I95 collapse | Crosswalk 36 edges; 4 net-new CAP-* rows |
| **SEM-03** | ACIM 7/99 (7%) | +23 ACIM rows for alpha partial/gap capabilities |
| **SEM-04** | CAP-M27 no vault anchor | **Scheduled** post-α2 (CO-MBH-008) — not minted |
| **SEM-05** | CAP-M16–M18 gaps | Net-new `CAP-MADEIRA-CONTEXT-ECONOMICS` **planned** until T2 code |
| **SEM-06** | `CAP-AGENTIC-OPERATIONS` cross-area | **Keep** — notes already explain People doctrine / MADEIRA execution |
| **SEM-07** | Lab capabilities (D-IH-99/100) | ACIM uses `AIC-CURSOR-BORROWED`; substrate empty OK until lab binding generalizes |
| **SEM-08** | Research PESTEL row on v3.2 | Model for methodology refresh on touched rows |

## Overlap check (no erroneous duplicates)

- **M02 vs CAP-CONVERSATIONAL-AI-ENGINE:** modes are orthogonal to “delivery engine” — net-new row justified.
- **M03 vs CAP-AI-AGENT-ORCHESTRATION:** RBAC is governance slice, not orchestration — net-new row justified.
- **M12 vs CAP-TECHOPS-RELIABILITY-OBSERVABILITY:** gateway proof is agentic infra, not generic deploy-health — maps to `CAP-AGENTIC-INFRA-OPS`.
- **M04 vs CAP-CANONICAL-GOVERNANCE:** inline ratify is operationalization of canonical gate — **maps**, not duplicates.

## Substrate backfill proposal (18 rows)

| capability_id | substrate_id | Rationale |
|:---|:---|:---|
| CAP-CONVERSATIONAL-AI-ENGINE | SUBS-HOLISTIKA-OPENCLAW-WINDOWS | Scenario A primary |
| CAP-AGENTIC-OPERATIONS | SUBS-ANYSPHERE-CURSOR-SDK | Cursor two-seat + dispatch |
| CAP-AI-PERSONA-PERSONALITY | SUBS-HOLISTIKA-OPENCLAW | Runtime persona config |
| CAP-KNOWLEDGE-RETRIEVAL-RAG | SUBS-HOLISTIKA-LLAMAINDEX-WORKER | KiRBe worker |
| CAP-AI-EVALUATION-BENCHMARKING | SUBS-HOLISTIKA-OPENCLAW | Langfuse + eval hooks |
| CAP-AI-AGENT-ORCHESTRATION | SUBS-HOLISTIKA-OPENCLAW | OpenClaw orchestration |
| CAP-MADEIRA-SCENARIO-LIFECYCLE | SUBS-ANYSPHERE-CURSOR-SDK | Verdict/dossier in Cursor |
| CAP-AGENTIC-INFRA-OPS | SUBS-HOLISTIKA-OPENCLAW-WINDOWS | Gateway health (M12) |
| CAP-RES-DEEP-METHODOLOGY | SUBS-HOLISTIKA-OPENCLAW | Research-action in IDE |
| CAP-RES-KB-PIPELINE-RADAR | SUBS-HOLISTIKA-KIRBE | KB + radar storage |
| CAP-CANONICAL-GOVERNANCE | SUBS-ANYSPHERE-CURSOR-SDK | AskQuestion ratify surface |
| CAP-CLOSURE-ASSURANCE-GOVERNANCE | SUBS-ANYSPHERE-CURSOR-SDK | UAT/browser evidence |
| CAP-PRECOMMIT-SYNTHESIS-DISCIPLINE | SUBS-ANYSPHERE-CURSOR-SDK | Pre-commit synthesis |
| CAP-TECHOPS-RELIABILITY-OBSERVABILITY | SUBS-HOLISTIKA-OPENCLAW | Deploy-health smoke |
| CAP-API-LIFECYCLE-GOVERNANCE | SUBS-HOLISTIKA-OPENCLAW | MCP catalog |
| CAP-MULTIPLATFORM-DEPLOYMENT | SUBS-VERCEL-VERCEL-AI-SDK | Hosted path forecast |
| CAP-MADEIRA-RESEARCH-CENTER-SURFACE | SUBS-HOLISTIKA-LLAMAINDEX-WORKER | I96 BFF (net-new) |
| CAP-MADEIRA-CONTEXT-ECONOMICS | SUBS-HOLISTIKA-OPENCLAW | T2 planned (net-new) |

Remaining 81 rows: `substrate_id` stays empty at α0; validator FAIL applies only to **active + Applied AI & MADEIRA** per GCI-04 ramp.

## References

- Pre-sweep baseline: `capability-registry-gap-analysis-pre-sweep-2026-06-15.md`
- Crosswalk WIP: `../wip/CAPABILITY_ALPHA_CROSSWALK.csv`
- Matrix seeds: `../capability-functionality-inventory-matrix.md`
