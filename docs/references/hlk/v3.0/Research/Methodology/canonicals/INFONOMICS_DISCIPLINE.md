---
title: Infonomics Discipline
language: en
status: active
canonical: true
role_owner: CDO + Business Controller
classification: way_of_working
intellectual_kind: discipline_charter
access_level: 4
authored: 2026-06-13
last_review: 2026-06-13
last_review_by: Operator
last_review_decision_id: D-IH-97-E
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-97-C
  - D-IH-97-E
linked_runbooks:
  - scripts/validate_hlk.py
  - scripts/validate_area_completeness.py
linked_canonicals:
  - RESEARCH_ACTION_DISCIPLINE.md
  - AREA_GOVERNANCE_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_CONTRACT_STANDARD.md
  - docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/FINOPS_REVENUE_RECOGNITION_POLICY.md
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md
evidence_pack: docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/
---

# Infonomics Discipline

## 1. Purpose

Holistika already runs a **governed information economy** — contract registries, FINOPS spine, collaborator share, mirrors, research trust scores, and area completeness gates. What was missing is a **named cross-area doctrine** that ties those surfaces to **valuation posture**, **carrying cost**, and **incentive alignment** without repeating consumer-facing UX economics (I96 Track D consumes this vocabulary; see §7).

Infonomics here means **management + measurement first**, monetization where evidence supports it — not asset slogans (`SRC-INF-EXT-482`, `SRC-INF-EXT-483` in the I97 research pack).

Research-owned evidence; **Data, Finance, Operations, Tech, People, Compliance, and Research** consume the hooks.

## 2. Working definition — Holistika information asset

A **Holistika information asset** is a governed artifact (register row, canonical, mirror table, or research pack) with:

| Property | Where it lives today |
|:---|:---|
| **Named consumers** | `DATA_CONTRACT_REGISTRY`, BI consumer registry, adapter registries |
| **Maintenance owner** | `process_list` pairing + `owner_role` on contracts |
| **Verify / mirror cost** | Verification profiles, mirror emit runbooks, CI gates |
| **Trust grade** | Research Action ledger scores; capability confidence |

**Economic outcome** must be classifiable as at least one of: *rework avoided*, *revenue enabled*, *risk reduced*, or *explicit opex* — even when EUR/USD is not yet recorded on the row.

## 3. Three economic lenses (Laney-aligned, Holistika-scoped)

| Lens | Question | Holistika primary surfaces |
|:---|:---|:---|
| **Management** | Is the asset inventoried, owned, and contract-bound? | Area completeness L3+, DATA_CONTRACT, PRECEDENCE |
| **Measurement** | Can we prove quality, freshness, and consumer fit? | Validators, mirrors, FINOPS recon, research radar |
| **Monetization** | Does the asset tie to cash flow, share, or priced risk? | FINOPS registers, collaborator share, RevOps value map |

**Rule:** Do not claim monetization on a row that only satisfies management. Skeptic corpus in I97 requires evidence-backed cost/benefit.

## 4. Register economic hooks (amend targets)

These columns extend existing registers **without replacing** them. Physical CSV tranche landed **2026-06-13** (P6b-CSV); Pydantic SSOT in `akos/hlk_*` modules + mirror DDL `20260613120000_i97_p6b_infonomics_register_columns.sql`.

### 4.1 DATA_CONTRACT_REGISTRY (Data)

| Column | Type | Meaning |
|:---|:---|:---|
| `economic_value_class` | enum | `rework_avoided` / `revenue_enabled` / `risk_reduced` / `opex_only` / `unclassified` |
| `carrying_cost_band` | enum | `negligible` / `low` / `medium` / `high` — mirror + verify + operator toil |
| `monetization_status` | enum | `not_applicable` / `indirect` / `direct` / `deferred` |

### 4.2 FINOPS companion registers (Finance)

| Register | Hook |
|:---|:---|
| Performance obligation / counterparty rows | `information_asset_ref` — optional FK to contract_id or canonical_id |
| Rev-rec policy narratives | Cite economic_value_class when PO is information-product shaped |

### 4.3 RevOps adapter / handoff surfaces (Operations)

| Surface | Hook |
|:---|:---|
| `REVOPS_ADAPTER_REGISTRY` rows | `handoff_cost_band` + `value_stream_id` on cross-area bridges |
| Engagement templates | `min/par/max_rev_value_eur` already present — join to information assets via contract_id |

## 5. Maturity prerequisite (P6a — D-IH-97-C Option D)

Enterprise Infonomics rests on **2-D maturity** (component × L0–L5) per [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../../Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) (`D-IH-94-A`). DCAM v3 maps to AREA-01..16 per I97 crosswalk (`dcam-area-completeness-crosswalk-2026-06-13.md` in the evidence pack).

**Critical bar:** platform areas (Data, Finance) at **critical@L3** before treating Infonomics hooks as COMPLETE tier signals.

## 6. Anti-patterns

1. **Asset ornament** — naming registers "assets" without consumer + cost linkage.
2. **Mesh sprawl** — decentralizing integration without federated PRECEDENCE cost.
3. **Ethics washing** — compliance spend mistaken for ethics value (see BL-ETHICS).
4. **Duplicate consumer economics** — rebuilding Track D insight-machine pricing inside enterprise registers (I96 boundary).
5. **Premature FAIL ramp** — economic columns empty on day one is WARN, not doctrine rejection.

## 7. I96 consumption boundary (D-IH-97-D)

| Owner | Scope |
|:---|:---|
| **I97 / this discipline** | Enterprise register, mirror, contract, FINOPS, RevOps **infrastructure** economics |
| **I96 Research Center** | Operator-facing insight cards, remediation cost hints, consumer inventory UX |

I96 **waits for P6b** stable vocabulary (`D-IH-96-J`). Do not mint parallel Infonomics doctrine in the I96 intelligence pack.

## 8. Verification

```powershell
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --matrix
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/source-ledger.csv
```

## 9. Evidence and ratification

| Artifact | Path |
|:---|:---|
| 800-row ledger + 14 prongs | `docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/` |
| Master synthesis | `master-synthesis.md` |
| P5 ratify | `docs/wip/planning/97-infonomics-holistika-data-economics/reports/p5-govern-ratify-2026-06-13.md` |
| P6b closure | `docs/wip/planning/97-infonomics-holistika-data-economics/reports/p6b-doctrine-mint-2026-06-13.md` |

Ratified **2026-06-13** under **D-IH-97-E** after P6a DCAM integrity crosswalk.
