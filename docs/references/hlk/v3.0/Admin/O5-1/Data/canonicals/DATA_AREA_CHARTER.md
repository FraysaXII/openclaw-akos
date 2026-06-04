---
language: en
status: active
canonical: true
role_owner: CDO + Data Governance Lead
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-06-04
last_review: 2026-06-04
last_review_at: 2026-06-04
last_review_by: CDO
last_review_decision_id: D-IH-93-C
methodology_version_at_review: v3.1
inherited_pattern_id: pattern_area_buildout
ratifying_decisions:
  - D-IH-93-A
  - D-IH-93-C
  - D-IH-93-H
linked_canonicals:
  - ../Governance/canonicals/DATAOPS_DISCIPLINE.md
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
  - ../../../People/Compliance/canonicals/PRECEDENCE.md
companion_to:
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
---

# DATA_AREA_CHARTER — Data area (I93 P1)

> First worked example of the People area-governance meta-process
> (`pattern_area_buildout` / `compose_AREA`). Ratified under the DATA
> canonical-home decision (`D-IH-93-C`) and the DataOps relocation-ripple
> contract (`D-IH-93-H`). DATA sets **global data standards**; each O5-1 area owns
> its **domain data products** under a federated / data-mesh posture.

## 1. Mission

The Data area exists so **every Holistika function can trust the data it
consumes and produces** — governance is the key, DAMA-DMBOK is the driver.
DATA:

1. **Authors** area doctrine (this charter; Governance / Architecture /
   Science sub-domain canonicals per I93 P2+).
2. **Operates** the dual-plane model: git-canonical SSOT + Supabase mirrors /
   FDW projections / operational tables (see DataOps discipline).
3. **Publishes** cross-area standards (data contracts, lineage, MDM, semantic
   layer — forward-chartered at I93 P2–P5).
4. **Serves** each component and engagement via explicit data contracts
   (population tranche I93 P4).

The verb is **govern + enable**: DATA does not own every area's CRM copy or
engagement folder; it owns the **bar**, the **contracts**, and the **quality
evidence** that areas meet the bar.

## 2. Roles (CDO chain) + sub-domains

Sub-domains map to folder roots under `Data/`:

| Sub-domain | Folder | Role anchor (`baseline_organisation.csv`) | Status |
|:---|:---|:---|:---|
| **Governance** | `Data/Governance/` | CDO → Data Governance Lead → Data Steward | active (CDO Think Big; Gov Lead HLK Tech Lab) |
| **Architecture** | `Data/Architecture/` | CDO → Data Architect | active |
| **Science** | `Data/Science/` | CDO → Lead Data Scientist → Data Engineer | Lead DS planned; DE active |

| Role | Reports to | Entity | Notes |
|:---|:---|:---|:---|
| **CDO** (Chief Data Officer) | O5-1 | Think Big | Area head; accountable for DAMA posture |
| **Data Architect** | CDO | Think Big | Physical/logical architecture standards |
| **Lead Data Scientist** | CDO | Think Big | planned — analytics / science charter at P3 |
| **Data Governance Lead** | CDO | HLK Tech Lab | Policy, contracts, stewardship cadence |
| **Data Steward** | Data Governance Lead | HLK Tech Lab | Canonical CSV + registry hygiene |
| **Data Engineer** | Lead Data Scientist | Think Big | Pipelines, mirrors, KiRBe ingest DQ |
| **Database Owner** | Data Governance Lead | HLK Tech Lab | area=Tech; dotted-line execution in Tech |

**DataOps discipline ownership (DATA canonical-home decision `D-IH-93-C`):**
doctrine + paired SOP live under
`Data/Governance/canonicals/`. **System Owner** and **DevOPS** remain
**co-owners** for execution (validators, Supabase DDL, mirror emit) — Tech
implements; Data governs the bar.

## 3. Boundary (authoring vs consuming; federated / mesh)

| DATA owns | DATA does not own |
|:---|:---|
| Global data-governance policy, contract standard, lineage/MDM doctrine | Area-specific CRM tables, marketing copy, legal instruments |
| `DATAOPS_DISCIPLINE.md` quality bar + `compose_DATAOPS` | People specialty mints (People still owns `compose_AREA` meta-process) |
| Cross-area `DATA_CONTRACT_REGISTRY` (I93 P2) | Individual engagement delivery (PMO + delivery areas) |
| Federated **standards** + contract enforcement | Domain **data products** inside Marketing / Finance / Ops trees |

**Federated / data-mesh rule:** DATA sets standards and contracts; **areas
own domain products** (canonical CSVs, engagement facts, GTM mirrors) and
must register producers/consumers in the contract registry. No central
team becomes bottleneck for every schema change — contract-gated changes
with Data Steward review.

## 4. DAMA cross-area integration table

Primary DAMA-DMBOK 2.0 knowledge areas DATA authors or coordinates (the
eight-DAMA-doctrine mint, `D-IH-93-D`):

| DAMA area | DATA role | Owning / co-owning area | I93 phase |
|:---|:---|:---|:---|
| **Data Governance** | Primary author | Data / Governance | P2 policy |
| **Data Architecture** | Primary author | Data / Architecture | P3 three-tier doc |
| **Data Modeling & Design** | Standards + review | Data + Tech | P3 / ongoing |
| **Data Storage & Operations** | Mirror/FDW posture | Tech (DevOPS) executes | P0–P1 DataOps |
| **Data Integration** | Contracts + adapters | Data + RevOps | P2 registry |
| **Reference & MDM** | Golden-record SOP | Data + Finance/Ops consumers | P4 MDM SOP |
| **Metadata & Lineage** | Lineage SOP | Data + Compliance | P4 lineage |
| **Data Quality** | `DATAOPS_DISCIPLINE` (active) | Data / Governance | P1 re-home |
| **Data Security / Privacy** | Retention policy | Data + Legal | P5 |
| **Warehousing / BI** | BI governance charter | Data / Governance | P5 decision gate |

## 5. Process catalog (initial)

Executable `area=Data` processes (from `process_list.csv`; umbrella + KiRBe
program). New area-governance processes should declare
`inherited_pattern_id=pattern_area_buildout` when minted (I93 P8 harmonization).

| Process | `item_id` | Cadence | SOP / runbook |
|:---|:---|:---|:---|
| DataOps quality check (7-dimension bar) | `env_tech_dtp_dataops_quality_001` | event_triggered | `SOP-TECH_DATAOPS_QUALITY_001.md` + `scripts/dataops_quality_check.py` |
| Enterprise MasterData | `thi_data_dtp_32` | (legacy) | forward-charter |
| Formal Data Lineage | `thi_data_dtp_275` | (legacy) | forward-charter |
| KiRBe Ingestion DQ | `thi_data_dtp_274` | (legacy) | forward-charter |
| Data Modeling | `thi_data_dtp_77` | (legacy) | forward-charter |
| RPA (data plane) | `thi_data_dtp_34` | (legacy) | forward-charter |

Full `thi_data_*` pairing review is **I93 P4** / OPS hygiene — not P1 scope.

## 6. Activation cadence

- **P1 (this charter):** area tree + Governance canonical home + DataOps
  re-home + area README; `validate_area_completeness.py --matrix` baseline.
- **P2–P5:** DAMA doctrine + contract registry per roadmap; operator gates on
  canonical CSV mints.
- **P8:** harmonize all seven areas to `pattern_area_buildout` completeness bar.
- **Area completeness:** run `py scripts/validate_area_completeness.py --matrix`
  before each DATA tranche commit; disposition gaps via inline-ratify per
  [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md).

## 7. Cross-references

- Area-governance meta-process: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) (`compose_AREA`, 14 components).
- DataOps discipline (Governance): [`DATAOPS_DISCIPLINE.md`](../Governance/canonicals/DATAOPS_DISCIPLINE.md).
- Quality Fabric §6 row: [`HOLISTIKA_QUALITY_FABRIC.md`](../../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md).
- I93 roadmap: [`docs/wip/planning/93-data-area-foundation-and-governance/master-roadmap.md`](../../../../../../wip/planning/93-data-area-foundation-and-governance/master-roadmap.md).
- Research synthesis: [`reports/research-synthesis-2026-06-04.md`](../../../../../../wip/planning/93-data-area-foundation-and-governance/reports/research-synthesis-2026-06-04.md).
- Cursor rule: [`.cursor/rules/akos-area-governance.mdc`](../../../../../../.cursor/rules/akos-area-governance.mdc).
- Decisions: **D-IH-93-A** (initiative), **D-IH-93-C** (area home + move), **D-IH-93-H** (ripple contract).
