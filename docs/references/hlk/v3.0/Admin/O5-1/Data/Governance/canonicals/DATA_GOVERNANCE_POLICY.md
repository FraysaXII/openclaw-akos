---
title: Data Governance Policy
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - CDO
co_authors:
  - Data Governance Lead
  - Data Steward
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_at: 2026-06-04
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
  - D-IH-93-C
status: active
register: internal
linked_canonicals:
  - DATA_CONTRACT_STANDARD.md
  - DATA_CATALOG_INTEGRATION_POSTURE.md
  - SOP-DATA_CONTRACT_REGISTRY_MAINTENANCE_001.md
  - DATA_PRIVACY_RETENTION_POLICY.md
  - SOP-DATA_MASTERDATA_GOLDEN_RECORD_001.md
  - DATA_BI_GOVERNANCE.md
  - DATA_INTEGRATION_PLANE.md
  - dimensions/BI_CONSUMER_REGISTRY.csv
  - dimensions/RPA_ADAPTER_REGISTRY.csv
  - DATAOPS_DISCIPLINE.md
  - ../../canonicals/DATA_AREA_CHARTER.md
  - ../../../People/Compliance/canonicals/PRECEDENCE.md
  - dimensions/DATA_CONTRACT_REGISTRY.csv
companion_to:
  - ../../canonicals/DATA_AREA_CHARTER.md
  - DATA_CONTRACT_STANDARD.md
---

# Data Governance Policy

> Holistika's **data-governance function** — who decides what about data
> assets, how that differs from execution, and how enforcement is baked into
> validators and mirrors rather than document review alone. Minted at I93 P2
> under the eight-DAMA-doctrine charter (`D-IH-93-D` — the decision that DATA
> authors governance + integration + quality + architecture + security +
> master/reference + warehousing + metadata doctrines).

## 1. Scope and definition

**Data governance** (DAMA-DMBOK Ch.3) is the exercise of **authority,
control, and shared decision-making** (planning, monitoring, enforcement)
over the management of data assets.

This policy applies to:

- Git-canonical CSVs under the HLK v3.0 vault (schema SSOT).
- Supabase mirrors, FDW projections, and graph representations (operational
  and analytic planes).
- Cross-area data products registered in `DATA_CONTRACT_REGISTRY.csv`.

It does **not** replace area-specific delivery SOPs (RevOps engagement
scaffold, FinOps Stripe stewardship, etc.) — it sets the **bar** those
processes must meet when they produce or consume governed data.

## 2. Governance vs management

| Governance (DATA decides) | Management (Tech / areas execute) |
|:---|:---|
| Policy, contract standard, classification enums | Supabase DDL, mirror emit jobs, FDW servers |
| Contract approval and registry hygiene | Pipeline implementation, KiRBe ingest runs |
| Quality-bar interpretation (DataOps DATA-01..07) | Validator scripts, drift gates, release-gate |
| Federated standards for domain data products | Area-owned CRM copies, engagement folders |

**Rule:** Data governs the bar; Tech implements the platform. The DataOps
re-home decision (`D-IH-93-C`) preserves this split — doctrine lives under
`Data/Governance/`; System Owner and DevOPS remain co-owners for execution.

## 3. Decision-rights matrix

Accountable roles resolve from `baseline_organisation.csv` (CDO chain).

| Decision class | Accountable role | Consulted | Informed |
|:---|:---|:---|:---|
| New / amended data contract | Data Governance Lead | Data Steward, producer area owner | CDO, PMO |
| Canonical CSV schema change (governed register) | Data Steward | Data Governance Lead, System Owner | Affected area heads |
| Data classification / retention (P5 policy) | Data Governance Lead | Legal, CDO | Area stewards |
| Mirror DDL / FDW server add | Database Owner | System Owner, DevOPS | Data Steward |
| Contract breach / quality FAIL | Data Steward | Data Governance Lead | Producer process owner |

Escalation path: Data Steward → Data Governance Lead → CDO → O5-1.

## 4. Federated operating model

Holistika adopts a **federated** posture (central standards + domain
execution):

1. **Central standards** — this policy, `DATA_CONTRACT_STANDARD.md`,
   `DATAOPS_DISCIPLINE.md`, and forward-chartered MDM / privacy / semantic
   layer canonicals (I93 P3–P5).
2. **Domain execution** — each O5-1 area owns its domain data products
   (Marketing CRM adapters, Finance Stripe FDW, compliance mirrors, etc.).
3. **Computational enforcement** — contracts, validators, and mirror emit
   bake policy into the platform (data-mesh *federated computational
   governance* principle).

No central team becomes a bottleneck for every schema tweak — changes are
**contract-gated** with Data Steward review, not ad-hoc edits.

## 5. Role anchors (business accountability)

| Role | Governance responsibility |
|:---|:---|
| **CDO** | Area head; accountable for DAMA posture and cross-area integration |
| **Data Governance Lead** | Policy owner, contract standard, registry cadence |
| **Data Steward** | Day-to-day canonical + registry hygiene; contract row quality |
| **Data Owner (business-accountable)** | Named per contract `owner_role`; accountable for semantics and SLA intent on the producer side |
| **Database Owner** | Schema operations on Supabase; dotted-line to Tech |
| **System Owner / DevOPS** | Validator wiring, mirror jobs, platform health |

**Data Owner** is the business-accountable party for a data product's meaning
and fitness-for-purpose (DAMA). In the registry, `owner_role` must resolve to
`baseline_organisation.csv`.

## 6. Enforcement mechanisms

Governance is **computational**, not checklist-only:

1. **`DATA_CONTRACT_REGISTRY.csv`** — declared producer/consumer/SLA/quality
   obligations per data surface.
2. **`scripts/validate_data_contract_registry.py`** — FK + enum gate wired
   into `validate_hlk.py`.
3. **`DATAOPS_DISCIPLINE.md`** — seven-dimension quality bar (DATA-01..07);
   contract `quality_rules` reference these codes, not a parallel model.
4. **Two-plane drift discipline** — git-canonical wins; mirror resync on
   drift (`.cursor/rules/akos-holistika-operations.mdc`).
5. **Synthesis-before-tranche** — canonical-CSV mints pass pre-commit scope
   review (`akos-synthesis-before-tranche.mdc`).

Warn-first posture on net-new contract fields; FAIL ramp follows DataOps
INFO→WARN→FAIL cadence for probes.

## 7. Cross-references

- Area charter: `Data/canonicals/DATA_AREA_CHARTER.md`
- **Three-tier architecture:** `Data/Architecture/canonicals/DATA_ARCHITECTURE.md`
- Contract vocabulary: `DATA_CONTRACT_STANDARD.md`
- Registry SSOT: `dimensions/DATA_CONTRACT_REGISTRY.csv`
- Quality bar: `DATAOPS_DISCIPLINE.md`
- Initiative roadmap: `docs/wip/planning/93-data-area-foundation-and-governance/master-roadmap.md`

## Evidence base (internal precedent + external grounding)

**Internal precedent**

- CDO chain and decision-rights anchors in `baseline_organisation.csv`
  (Data Governance Lead → Data Steward → Capability Curator).
- DataOps governance-vs-execution split after P1 re-home:
  `Data/Governance/canonicals/DATAOPS_DISCIPLINE.md` (`D-IH-93-C`).
- Area charter federated/mesh boundary:
  `Data/canonicals/DATA_AREA_CHARTER.md` §3.

**External grounding**

- DAMA-DMBOK2 Ch.3 Data Governance (DAMA International, 2017): governance =
  authority + control + shared decision-making; governance decides, management
  executes; federated operating model — primary lens for this policy.
- Dehghani, Z. (2019), "Data Mesh Principles and Logical Architecture",
  martinfowler.com: federated computational governance — standards baked
  computationally into the platform (validators + mirror emit).
- EDM Council DCAM — capability-maturity lens complementing DAMA's
  knowledge-area lens (pairs with `compose_AREA` area-completeness bar).
- Open Data Contract Standard (ODCS) v3.1.0 cited in companion
  `DATA_CONTRACT_STANDARD.md` (Bitol/Linux Foundation, Dec 2025).
