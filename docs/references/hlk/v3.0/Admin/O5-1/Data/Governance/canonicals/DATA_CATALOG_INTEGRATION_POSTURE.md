---
title: Data Catalog Integration Posture
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Governance Lead
co_authors:
  - CDO
  - System Owner
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_at: 2026-06-04
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
status: active
register: internal
linked_canonicals:
  - DATA_CONTRACT_STANDARD.md
  - DATA_GOVERNANCE_POLICY.md
  - SOP-DATA_CONTRACT_REGISTRY_MAINTENANCE_001.md
  - dimensions/DATA_CONTRACT_REGISTRY.csv
companion_to:
  - DATA_CONTRACT_STANDARD.md
---

# Data Catalog Integration Posture

> Where **OpenMetadata**, **Microsoft Purview**, and similar catalog platforms
> sit relative to Holistika's **git-native** data-contract registry — without
> replacing repo SSOT.

## 1. Default posture — repo-native SSOT **and** DAMA-tool-friendly

**Repo-native SSOT (Option A — operator ratified 2026-06-04):**

- `DATA_CONTRACT_REGISTRY.csv` in git is authoritative.
- Enforcement = Pydantic + `validate_data_contract_registry.py` + `validate_hlk.py`
  + P6 DataOps `--data-fam` probes.
- Discovery = vault paths, PRECEDENCE, CANONICAL_REGISTRY, initiative reports.

We **do not** require Purview or OpenMetadata for data governance to **function**.
We **do** require that vault SSOT stays **interoperable** with industry DAMA-aligned
tools (OpenMetadata, Purview, datacontract-cli) via **ODCS v3.1** — the same
pattern OpenMetadata documents: contracts stored in git, imported as projection,
never edited only in the catalog UI.

**DAMA-tool-friendly** means: DAMA-DMBOK is the **doctrine blueprint** (what good
looks like); git + validators are the **computational governance** layer (provable
control); catalog tools are the **optional operationalization UI** (discovery,
DQ dashboards, Azure classification) — analogous to ITIL doctrine + ServiceNow BPA,
not doctrine replaced by the tool.

See **§7–§9** for the three-layer model, DAMA coverage matrix, and governed-claim bar.

## 2. Capability comparison

| Capability | Holistika (today → I93) | OpenMetadata | Microsoft Purview |
|:---|:---|:---|:---|
| Data contracts (ODCS) | CSV registry; ODCS vocab aligned | Native ODCS 3.1 import/export API | Policy + quality via Unified Catalog; contracts via ecosystem |
| Schema SSOT | Git canonical CSV + Pydantic | Catalog entities + versions | Scanned metadata from connected sources |
| Lineage | Partial (Neo4j, KiRBe); P4 formalises | OpenLineage ingestion | Automated scan + lineage views |
| Quality enforcement | DATA-01..07 validators + probes | Contract validation + test suites | Data quality rules in catalog |
| Discovery UI | None (IDE + docs) | Web UI search | Unified Catalog portal |
| Audit trail | Git history | Platform audit log | Azure audit |

## 3. Hybrid path (Option B — accelerated to P3 per operator ratification 2026-06-04)

When operator need for **non-git discovery** or **external DAMA-tool validation** exceeds cost
(or per **A++ charter**: immediately after P3 architecture canonical):

1. Export registry rows to **ODCS 3.1 YAML** via P3 deliverable `scripts/export_data_contract_odcs.py`.
2. Import into [OpenMetadata ODCS endpoints](https://docs.open-metadata.org/v1.11.x/api-reference/data-contracts/odcs)
   as **read-oriented replica** — git remains SSOT; catalog is projection.
3. Re-export on each contract tranche commit (CI step); optional `POST .../odcs/validate/yaml` in CI.

**Anti-pattern:** editing contracts only in OpenMetadata without git PR — creates
SSOT drift.

## 4. Purview path (Option C — conditional)

Consider Purview **only** for assets already in Microsoft Azure / Fabric that
need enterprise scan/classification — not as replacement for HLK vault CSVs.
Holistika compliance canonicals stay git-authoritative per baseline governance.

## 5. Mapping to DATA-FAM (P6)

Each **DATA-FAM umbrella** (`CAP-HOL-DATA-FAM-*-001`) corresponds to a **data
product** in catalog-tool language. Contract rows are the **per-surface
interface** of that product — analogous to OpenMetadata data-product contract
inheritance, but declared explicitly in CSV until export lands.

## 6. Decision log hook

Operator ratified **Option A** (repo-native SSOT) 2026-06-04. **DAMA-tool-friendly
interop binding:** **A++ accelerate L3 to P3** (ODCS export + CI validate after architecture
canonical). **Governed-claim bar:** strict + forward-declared (§9). Option B/C full tool
deployment requires successor decision row at activation (ID allocated at approve time,
not pre-minted).

## 7. Three-layer DAMA stack (Holistika binding)

Industry pattern (not Holistika-only): **contracts-as-code in git** + **catalog as
discovery/DQ projection** + **CI enforcement** (datacontract-cli, OpenMetadata
ODCS validate API, or native validators). Sources: OpenMetadata issue #21078
(git-stored ODCS → API import); datacontract-specification README; dbt data-mesh
catalog + contract validation split; ThoughtSpot data-contracts explainer (2024).

| Layer | Role | Holistika SSOT | DAMA analogue |
|:---|:---|:---|:---|
| **L1 — Doctrine** | What good looks like | `DATA_GOVERNANCE_POLICY.md`, `DATA_CONTRACT_STANDARD.md`, `DATA_AREA_CHARTER.md`, PRECEDENCE | DAMA-DMBOK knowledge areas (blueprint) |
| **L2 — Computational governance** | Provable control | Pydantic CSVs, `validate_hlk.py`, DATA-01..07 probes, `validate_area_completeness.py`, area score matrix | Federated computational governance (data mesh); ISO 8000-style measurable quality |
| **L3 — Tool projection** | Discovery + DQ UI + cloud scan | ODCS 3.1 YAML export → OpenMetadata import; Purview Unified Catalog for Azure/Fabric assets only | Purview/OpenMetadata as operational toolkit (Medium DMBOK↔Purview mapping; Victoria Holt 2026 convergence essay) |

**Binding rule:** L3 never overrides L1/L2. Catalog edits without git PR = drift
(anti-pattern per §3).

## 8. DAMA 11-area coverage matrix (honest status → I93 phases)

Maps DAMA-DMBOK knowledge areas to Holistika components and optional tool lane.
Source: `reports/research-synthesis-2026-06-04.md` §5 + P2b research sweep.

| # | DAMA area | Holistika component (SSOT) | L2 enforcement | L3 tool lane (optional) | I93 phase |
|:---|:---|:---|:---|:---|:---|
| 1 | Data Governance | Policy + charter + area score | `validate_area_completeness.py` | — | P2 ✅ / P8 harmonize |
| 2 | Data Architecture | Three-tier canonical (P3) | drift + graph model tests | Purview scan (Azure only) | P3 |
| 3 | Data Modeling | Register-centric schemas | Pydantic per CSV | OpenMetadata entity attach | P4+ |
| 4 | Storage & Operations | Mirrors + Supabase DDL | DataOps `--data-fam` probes | Purview Data Map | P6 |
| 5 | Data Security | Privacy policy (P5) | POLICY_REGISTER RLS rows | Purview classification | P5 |
| 6 | Integration & Interop | **DATA_CONTRACT_REGISTRY** | contract + registry validators | ODCS export | P2 ✅ / export P8 |
| 7 | Document & Content | KM Topic-Fact-Source | manifest validators | — | exists / P7 |
| 8 | Reference & Master Data | MDM SOP (P5) | golden-record checks | Purview glossary (optional) | P5 |
| 9 | Warehousing & BI | explicit defer or policy (P5) | — | Power BI + Purview (if adopted) | P5 decision |
| 10 | Metadata | CANONICAL_REGISTRY + PRECEDENCE | index integrity sweep | OpenMetadata / Purview catalog | P4 / P8 |
| 11 | Data Quality | DATA-01..07 + DataOps | probes + contract `quality_rules` | OpenMetadata contract DQ tests; Purview quality rules | P6 |

**Adjacency rows (I93 charter):** Data contracts (P2 ✅), semantic/metrics (P4),
data products = DATA-FAM umbrellas (P6), lineage (P4), DataOps (P1/P6).

## 9. Governed-claim bar (anti gap-theatre)

A surface or area may be called **governed** only when **all** applicable rows pass:

| Claim | Required evidence |
|:---|:---|
| **Contract governed** | Row in `DATA_CONTRACT_REGISTRY.csv` + passing `validate_data_contract_registry.py` + producer FK in `process_list` |
| **Forward mirror governed** | Contract row marked forward + **open OPS tracker** (e.g. OPS-86-15) + quarterly review cadence in maintenance SOP — language: **"forward-declared"**, not "fully enforced" |
| **Area governed** | `validate_area_completeness.py` ≥ operator threshold (currently 80% bar) with **no silent partials** on AREA-09 (paired SOP+runbook) or AREA-14 (pattern FK) without dated closure target |
| **DAMA-aligned** | L1 doctrine row exists for the knowledge area **and** L2 validator or probe wired **or** explicit defer decision in initiative decision log |

This closes the historical failure mode: claiming governance while validators,
paired runbooks, or registry rows were missing.

## Evidence base

**Internal:** P2 registry mint; `reports/research-p2b-registry-operating-model-2026-06-04.md`;
two-plane model (`.cursor/rules/akos-holistika-operations.mdc`).

**External:**

- OpenMetadata ODCS 3.1 import/export — https://docs.open-metadata.org/v1.11.x/api-reference/data-contracts/odcs
- OpenMetadata 1.12 ODCS + OpenLineage — https://blog.open-metadata.org/announcing-openmetadata-1-12-9e15b66e7748
- Microsoft Purview Unified Catalog — https://learn.microsoft.com/en-us/purview/data-governance-overview
- Purview data products — https://learn.microsoft.com/en-us/purview/unified-catalog-data-products
- datacontract-specification (contracts-as-code + CLI) — https://github.com/datacontract/datacontract-specification
- OpenMetadata git-first contract workflow — https://github.com/open-metadata/OpenMetadata/issues/21078
- DMBOK↔Purview mapping (practitioner) — https://medium.com/@edyau/we-mapped-microsoft-purview-to-every-dmbok-knowledge-area-heres-what-we-found-cbefd7b73517
- Framework convergence (DAMA / ISO / Purview operationalization) — https://blog.victoriaholt.co.uk/2026/05/how-data-governance-frameworks-converge.html
