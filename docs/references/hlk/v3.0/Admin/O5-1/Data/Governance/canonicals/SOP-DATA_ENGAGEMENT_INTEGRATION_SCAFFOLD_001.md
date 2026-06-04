---
title: SOP — Engagement Integration Scaffold
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Lead
co_authors:
  - Data Architect
  - System Owner
  - RevOps Lead
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_decision_id: D-IH-93-J
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-I
  - D-IH-93-D
  - D-IH-93-J
status: active
register: internal
linked_canonicals:
  - DATA_BI_GOVERNANCE.md
  - DATA_INTEGRATION_PLANE.md
  - dimensions/RPA_ADAPTER_REGISTRY.csv
  - dimensions/BI_CONSUMER_REGISTRY.csv
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - dimensions/AREA_BI_PROFILE.csv
linked_runbooks:
  - scripts/bi_integration_readiness_check.py
linked_processes:
  - hol_data_dtp_engagement_integration_scaffold_001
cadence: event_triggered
cadence_trigger: new engagement demo spec OR client BI/RPA ask OR stream ambiguity
---

# SOP — Engagement Integration Scaffold

## Purpose

Convert customer-pack **demo specs** (Power Automate / Power BI / Excel patterns) into
**governed internal artefacts before build starts** — preventing the SUEZ pain pattern
where demos exist without adapter rows, contracts, runbooks, or declared streams.

Every engagement with an integration or BI ask walks this scaffold **once per capability
batch** (e.g. F-05 libellé, F-05 dispute register).

## Scope

| In scope | Out of scope |
|:---|:---|
| Engagements under `Think Big/Clients/` with demo or integration specs | Implementing PA/PP flows inside AKOS repo |
| Stream A/B/C declaration per `DATA_BI_GOVERNANCE.md` §4 | SUEZ EFA commercial Stream B (collaborator-share — separate grounding) |
| Registry + matrix tranche in same commit as scaffold sign-off | Production hardening (downstream production readiness SOP) |
| Routing to MS demo factory when Microsoft stack declared | |

## Inputs

- Customer-pack or operator-pack demo spec (capabilities, tools, data surfaces).
- Engagement id + slug (e.g. `ENG-SUEZ-WEBUY-2026` / `2026-suez-webuy`).
- Consuming area(s) — update `AREA_BI_PROFILE.csv` steward if new tools appear.
- Internal grounding note when delivery language differs from build location.

## End-to-end process chain

| Stage | Process / artefact | Owner | Gate |
|:---|:---|:---|:---|
| **Upstream — charter** | Engagement folder + `ENG-*` registry row when exists | RevOps Lead | Engagement id known |
| **Upstream — commercial** | `SOP-ENG_ESTIMATION_DISCIPLINE_001` + `scripts/estimate_engagement.py` | Project Manager | Integration effort in scope |
| **Upstream — research** | `SOP-RESEARCH_ACTION_001` when stack posture novel | Research Director | Source ledger before new doctrine |
| **This SOP** | `hol_data_dtp_engagement_integration_scaffold_001` | Data Governance Lead | Registry tranche before build |
| **Downstream — MS** | `hol_data_dtp_ms_demo_factory_001` | RevOps Lead | Microsoft stack declared |
| **Downstream — scenario** | e.g. `SOP-DATA_SUEZ_LIBELLE_001.md` | Data Governance Lead | Engagement-specific |
| **Downstream — readiness** | `hol_data_dtp_bi_integration_readiness_001` | Data Steward | Automated PASS |
| **Downstream — production** | `hol_data_dtp_production_readiness_001` | CDO | Revenue booked |
| **Parallel — contracts** | `hol_data_dtp_contract_registry_mtnce_001` | Data Steward | Same tranche or prior |
| **Parallel — share** | `validate_collaborator_share.py` when commercial pack ships | Compliance | CS-01..CS-09 |
| **Tranche quality** | `synthesis_before_tranche_check.py` class `canonical_csv_mint` | PMO | Before commit |
| **Pre-send** | Pre-send regression gate spec | Operator | Before external send |
| **DataOps** | `env_tech_dtp_dataops_quality_001` | System Owner | Mirror/registry mint |

## Steps (AC-HUMAN)

1. **Classify DATA streams** — per `DATA_BI_GOVERNANCE.md` §4:
   - **A** — client or Holistika Microsoft tenant (Power Platform / Power BI).
   - **B** — Holistika Supabase + Edge + ERP.
   - **C** — hybrid (export views, FDW, webhooks).
2. **Declare Phase 1 build location** — default Holistika Microsoft tenant for MS stack; record in checklist. Customer-pack "your environment" text does not override unless operator ratifies client-tenant-first.
3. **Inventory demo surfaces** — table each trigger, store, UI, report, and referential file.
4. **Mint or update data contract** — one row per producer × `data_surface`.
5. **Mint or update RPA adapter** — `RPA_ADAPTER_REGISTRY.csv` with status + paired SOP path.
6. **Mint or update BI consumer** — tier + `component_id` FK in `BI_CONSUMER_REGISTRY.csv`.
7. **Matrix tranche** — row exists in `COMPONENT_SERVICE_MATRIX`; `integration_pattern` set.
8. **Route downstream SOP** — Microsoft → `SOP-DATA_MS_DEMO_FACTORY_001.md`; engagement scenario → e.g. `SOP-DATA_SUEZ_LIBELLE_001.md`.
9. **Sign checklist** — Data Governance Lead records stream + Phase 1 location in engagement folder.

## Dual-path reference (MS primary vs Edge parallel)

| Demo element | Phase 1 (Holistika MS tenant) | Parallel proof (Holistika Edge) |
|:---|:---|:---|
| Referential | SharePoint/Excel or git CSV (anonymised) | Git CSV + optional mirror |
| Trigger | Power Automate | Edge Function / pg_net |
| Validation UI | Power Apps | HLK-ERP panel |
| Reporting | Power BI or export view | ERP Recharts + `erp.vw_*` |

Operator ratifies which path is **primary** for each capability. When revenue funds MS production, MS path is primary unless explicitly waived.

## Steps (AC-AUTOMATION)

```powershell
py scripts/bi_integration_readiness_check.py --self-test
py scripts/bi_integration_readiness_check.py --report
py scripts/validate_bi_consumer_registry.py
py scripts/validate_adapter_registries.py
py scripts/validate_data_contract_registry.py
```

PASS: readiness self-test green; FK rows resolve; paired SOP paths exist on disk.

## Failure modes

| Failure | Recovery |
|:---|:---|
| Build started before scaffold signed | Pause build; complete steps 1–9 |
| Stream A assumed = client tenant by default | Amend to Phase 1 Holistika unless operator ratified otherwise |
| Dashboard wired without contract row | Mint contract before UI work merges |
| Confused commercial vs DATA stream labels | MS demo factory addendum disambiguation table |
| Missing matrix row for new tool | Matrix tranche in same commit as consumer row |

## Outputs

- Completed scaffold checklist (engagement `00-internal/` or tranche charter).
- Registry rows: contract, adapter, BI consumer (and area profile if new tools).
- Downstream SOP invocation recorded (demo factory, scenario SOP, production readiness).

## Cross-references

- SUEZ F-05 scenario: `SOP-DATA_SUEZ_LIBELLE_001.md`
- MS demo factory: `SOP-DATA_MS_DEMO_FACTORY_001.md`
- Production promotion: `SOP-DATA_PRODUCTION_READINESS_001.md`
- Research: `docs/wip/planning/93-data-area-foundation-and-governance/reports/research-platform-component-landscape-2026-06-04.md`
