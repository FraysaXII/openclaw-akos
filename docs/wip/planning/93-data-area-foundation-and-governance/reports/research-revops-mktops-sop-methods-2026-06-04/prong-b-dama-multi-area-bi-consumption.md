---
intellectual_kind: research_prong_synthesis
parent_pack: research-revops-mktops-sop-methods-2026-06-04
prong: B
feeds_decision: DATA governance for all-area BI consumption
authored: 2026-06-04
sources: SRC-I93-RSM-006..011
---

# Prong B — DAMA-aligned multi-area BI consumption (DATA entirely)

## Operator directive (binding intent)

> Every area WILL consume BI just like DAMA says and let them do. DATA needs nomenclature and governance so DATA is well governed for everyone — DATA entirely; BI is part of it.

## Current gap

`DATA_BI_GOVERNANCE.md` + `BI_CONSUMER_REGISTRY.csv` (P5b) name **tools/tiers** but not a **systematic per-area consumption contract**. `DATA_CATALOG_INTEGRATION_POSTURE.md` §7-9 has DAMA rows per knowledge area but Warehousing & BI was just updated — other areas lack BI consumer declarations.

Analytics Buckets: operator treats as **production on Holistika Supabase** regardless of vendor Public Alpha label (SRC-I93-RSM-015); customer revenue funds production hardening.

## Proposed governance model — `compose_AREA_BI`

Extend DATA plane with **three linked artefacts** (no parallel SSOT):

| Artefact | Purpose | Owner |
|:---|:---|:---|
| **`AREA_BI_PROFILE.csv`** (new dimension) | One row per O5-1 area: default BI tiers, steward role, primary tools, engagement_stream default | Data Governance Office |
| **`BI_CONSUMER_REGISTRY.csv`** (existing) | One row per **tool instance** (Langfuse, Meta BM, Power BI…) FK → `component_id` | Data Governance Office |
| **Area charter appendix** | Plain-language "how this area consumes data/BI" — links to profile row | Area head |

### `AREA_BI_PROFILE.csv` seed shape (proposed 15 cols)

```
area_id,steward_role,primary_bi_tiers,default_engagement_stream,analytics_buckets_posture,primary_adapters,paired_sop_family,contract_obligation,status,linked_decision_id,notes,...
```

**Seed rows (minimum credible):**

| area_id | steward_role | primary_bi_tiers | notes |
|:---|:---|:---|:---|
| Marketing | Marketing Analytics Manager | T4,T8 + Meta/Google | Campaign + ads; Analytics Buckets OLAP |
| Operations | RevOps Manager | T2,T7,T8 | Attribution spine; Power BI client exports |
| Data | Data Steward | T2,T4,T5 | Metabase; semantic layer; lineage |
| Tech | System Owner | T1,T3,T9 | ERP; Langfuse; control plane |
| Finance | Business Controller | T2,T7 | FDW finops; Stripe |
| People | CPO | T1 | ERP people panels |
| Research | Lead Researcher | T3,T6 | Langfuse; Streamlit probes |
| Legal | Legal Counsel | T1 | ERP compliance views only |
| Compliance | Compliance Manager | T1,T2 | Mirror health dashboards |

### DAMA mapping (per area)

Each area declares which **DAMA knowledge areas** it consumes for BI (not owns):

| DAMA area | DATA owns doctrine | Area consumes via |
|:---|:---|:---|
| Warehousing & BI | `DATA_BI_GOVERNANCE.md` | Area BI profile + consumer rows |
| Metadata | `CANONICAL_REGISTRY` | Index + ERP panels |
| Data Quality | `DATAOPS_DISCIPLINE` | Probes in area runbooks |
| Integration | `DATA_INTEGRATION_PLANE` + adapter registries | RevOps + area adapters |

**Rule:** DATA sets the **plane** (warehouse, tiers, contracts, validators). Areas declare **consumption**; they do not mint parallel BI doctrine.

## Marketing + Google + Meta (operator callout)

Component matrix already lists Google Workspace, Make, n8n; P5c should add/tag:

- Google Analytics / Looker Studio (Marketing Experimentation)
- Meta Business Manager / Ads reporting
- Supabase Analytics Buckets (Marketing OLAP offload)

Each → `BI_CONSUMER_REGISTRY` row + `component_id` FK + optional `DATA_CONTRACT_REGISTRY` row when mirror/export surface exists.

## Production funding model (operator amendment)

When an **engagement customer exists** (e.g. SUEZ Stream A):

1. **Phase 1** — Holistika Azure tenant build (proof + screenshots + PDF).
2. **Phase 2** — Client tenant handoff when DSI requires.
3. **Production hardening** — funded from engagement revenue; Analytics Buckets / Metabase / licensing treated as **billable infrastructure**, not deferred "alpha blockers."

Mint as **`SOP-DATA_PRODUCTION_READINESS_001`** family (forward P5c/P5d) with methods for infra activation checklist.

## Options for P5c mint

| Option | Scope |
|:---|:---|
| **B1 — Full AREA_BI_PROFILE.csv now** | 7+ area rows + amend DATA_BI_GOVERNANCE §multi-area + validator |
| **B2 — Extend BI_CONSUMER only** | Add MKT/Meta/Google/Buckets rows; profile CSV forward-charter |
| **B3 — DATA-FAM BI-CONSUMPTION family** | Umbrella in P6 with area batches |

**Recommended:** **B1 + consumer tranche** — operator said every area consumes BI; profile CSV makes that machine-checkable.
