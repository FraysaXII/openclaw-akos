---
title: Holistika Semantic Layer
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Architect
co_authors:
  - Data Steward
  - CDO
last_review: 2026-06-04
last_review_by: Data Architect
last_review_at: 2026-06-04
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
status: active
register: internal
linked_canonicals:
  - dimensions/METRICS_REGISTRY.csv
  - DATA_ARCHITECTURE.md
  - ../../Governance/canonicals/DATA_CONTRACT_STANDARD.md
  - ../../Governance/canonicals/dimensions/DATA_CONTRACT_REGISTRY.csv
  - ../../Governance/canonicals/DATA_GOVERNANCE_POLICY.md
companion_to:
  - DATA_ARCHITECTURE.md
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
---

# Holistika Semantic Layer

> **Define-once-use-everywhere** metric governance for Holistika — business and
> technical owners, grain, dimensions, and source contracts declared in
> `METRICS_REGISTRY.csv` and consumed by dashboards, MCP tools, and agents.
> Pairs `thi_data_dtp_31` (Query, KPI & Reporting Catalog).

## 1. Purpose

Without a semantic layer, every dashboard and agent reinvents SQL and naming —
drift follows. This canonical sets the **bar** for governed metrics:

1. **One metric_id** per measurable concept (`MET-HOL-*`).
2. **Dual ownership** — business accountable for meaning; technical for execution.
3. **Contract linkage** — `source_contract_id` FK to `DATA_CONTRACT_REGISTRY` when
   the metric reads a governed surface.
4. **Access control** — `access_level` mirrors vault lattice (3–5).

## 2. Registry shape

SSOT: `dimensions/METRICS_REGISTRY.csv` validated by
`scripts/validate_metrics_registry.py` (wired into `validate_hlk.py`).

| Column | Role |
|:---|:---|
| `metric_id` | Stable identifier (`MET-HOL-*`) |
| `metric_name` | Human label |
| `definition_sql_ref` | SQL view, script path, or documented query anchor |
| `grain` | Atomic unit (area, register, engagement, sync_run, …) |
| `dimensions` | Semicolon-list of slice keys |
| `owner_business_role` / `owner_technical_role` | Dual ownership (DAMA) |
| `source_contract_id` | Optional FK → data contract |
| `access_level` | `3` \| `4` \| `5` per `access_levels.md` |
| `status` | `active` \| `draft` \| `deprecated` |

## 3. Consumption paths

| Consumer | How metrics are read |
|:---|:---|
| Operator dashboards / ERP | Mirror or FDW queries referenced in `definition_sql_ref` |
| MCP / agents | Read registry CSV or future mirror; never invent parallel defs |
| DataOps / area score | Scripts named in `definition_sql_ref` (e.g. area completeness) |
| External BI (P5 decision) | Export from registry; defer warehouse until P5 |

## 4. Stewardship (pairs `thi_data_dtp_31`)

1. Draft row with `status=draft`.
2. Link `source_contract_id` when metric reads a contracted surface.
3. Run `py scripts/validate_metrics_registry.py`.
4. Data Steward promotes to `active` on operator-approved tranche.

Cadence: **scheduled** quarterly review aligned with area-completeness sweep.

## 5. MCP / AI-readiness

Metric rows are **machine-readable** via Pydantic (`akos/hlk_metrics_registry_csv.py`).
Agents must cite `metric_id` when reporting KPIs in governed contexts. Forward-charter:
METRICS mirror + ERP panel (same pattern as other compliance registers).

## 6. Cross-references

- Architecture tiers: `DATA_ARCHITECTURE.md`
- Data contracts: `DATA_CONTRACT_STANDARD.md`
- Lineage: `SOP-DATA_LINEAGE_001.md`
- Process: `process_list` `thi_data_dtp_31`

## Evidence base

**Internal:** P3 three-tier model; P2 contract registry; area-completeness validator;
`thi_data_dtp_31` / CAP-THI-DATA-DTP-31 capability row.

**External:**

- dbt metrics — define-once semantic layer pattern (https://docs.getdbt.com/docs/build/metrics)
- AtScale / semantic-layer governance class (industry define-once-use-everywhere)
- DAMA-DMBOK2 Ch.10 Metadata + Ch.11 Data Quality linkage (DAMA International, 2017)
