---
title: SOP — SUEZ Libellé Demo (F-05)
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_SUEZ_LIBELLE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Lead
co_authors:
  - System Owner
  - Data Architect
  - RevOps Lead
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_decision_id: D-IH-93-J
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-J
  - D-IH-93-I
status: active
register: internal
linked_canonicals:
  - DATA_BI_GOVERNANCE.md
  - DATA_INTEGRATION_PLANE.md
  - SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md
  - SOP-DATA_MS_DEMO_FACTORY_001.md
  - SOP-DATA_PRODUCTION_READINESS_001.md
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - dimensions/RPA_ADAPTER_REGISTRY.csv
linked_runbooks:
  - scripts/bi_integration_readiness_check.py
linked_processes:
  - hol_data_dtp_engagement_integration_scaffold_001
cadence: event_triggered
cadence_trigger: SUEZ F-05 libellé capability build OR ENG-SUEZ-WEBUY-2026 demo tranche
---

# SOP — SUEZ Libellé Demo (F-05)

## Purpose

Deliver governed proof for **F-05 libellé generator** on engagement
`ENG-SUEZ-WEBUY-2026`: five-component deterministic naming (initiales, parc, code
intervention, fournisseur, devis/facture) plus CAPEX variant — matching the customer-pack
demo spec while building on **Holistika infrastructure first**.

## Customer-pack and internal references

| Artifact | Path |
|:---|:---|
| Demo spec (counterparty-facing) | `02-customer-pack/demo-libelle-generator.customer.fr.md` |
| Engagement fact | `DC-HOL-SUEZ-ENG-FACT-001` |
| Staging contract | `DC-HOL-SUEZ-LIBELLE-STAGING-001` |
| Internal build + IP policy | `00-internal/source-grounding-post-handshake-2026-05-26.md` §3.2, §5 |

## Capability shape (from demo spec)

| Piece | Tool | Governed role |
|:---|:---|:---|
| Referential (parc, suppliers, rules) | Excel on SharePoint **or** git CSV seed | Engagement referential — not SSOT |
| Operator form | Power Apps canvas | Validation UI |
| Composition logic | Power Automate cloud flow | RPA adapter `power_platform` |
| Reporting (optional) | Power BI or ERP export view | BI consumer row |

Anonymisation: generic supplier/parc names (e.g. Fournisseur-Alpha-001) — never SUEZ-actual rows in git or screenshots from prior clients.

## Routing (three paths — do not conflate)

| Path | Owner | When |
|:---|:---|:---|
| **Phase 1 — Holistika Microsoft** | RevOps Lead + System Owner | **Default primary** — invoke `SOP-DATA_MS_DEMO_FACTORY_001.md` |
| **Phase 2 — Client tenant** | SUEZ DSI | After Phase 1 evidence + DSI unblocks client environment |
| **Parallel proof — Edge + ERP** | System Owner | When client PA blocked **temporarily** — internal logic validation only |

**Not in scope:** SUEZ **commercial Stream B** (EFA maintenance invoicing) — see collaborator-share grounding; Holistika is not party to that invoice stream.

## End-to-end process chain

| Stage | Process / artefact | Owner | Gate |
|:---|:---|:---|:---|
| **Upstream — commercial** | `SOP-ENG_ESTIMATION_DISCIPLINE_001` + engagement `scope.yaml` | Project Manager | Proposal rates before build budget |
| **Upstream — share frame** | `COLLABORATOR_SHARE_DOCTRINE` + SUEZ grounding §1 (Holistika Stream A vs EFA Stream B) | RevOps Lead / CPO | Commercial streams documented before registry |
| **Upstream — research** | `SOP-RESEARCH_ACTION_001` when demo strategy changes | Research Director | Source ledger before doctrine edits |
| **Entry** | `hol_data_dtp_engagement_integration_scaffold_001` → scaffold SOP | Data Governance Lead | Registry rows before build |
| **Primary build** | `hol_data_dtp_ms_demo_factory_001` → MS demo factory SOP | RevOps Lead | Phase 1 Holistika tenant |
| **Parallel** | Edge + ERP per integration plane | System Owner | Optional; not substitute for MS when funded |
| **Registry** | `hol_data_dtp_contract_registry_mtnce_001` | Data Steward | Contracts active |
| **Readiness** | `hol_data_dtp_bi_integration_readiness_001` | Data Steward | Automated probes PASS |
| **Production** | `hol_data_dtp_production_readiness_001` | CDO / Data Governance Lead | On revenue booking |
| **Pre-send gate** | Pre-send regression spec (6 layers) | Operator | Before any customer-pack PDF/mail send |
| **External delivery** | External render discipline + brand baseline reality | Brand / Reach | Translated register; render trail fresh |
| **Quality tranche** | `SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001` class `canonical_csv_mint` | PMO | SYN sweep before commit |
| **DataOps** | `env_tech_dtp_dataops_quality_001` on registry mint | System Owner | DATA-01..07 on mirror upsert |

## Steps (AC-HUMAN) — Phase 1 primary

1. Run **engagement integration scaffold** — declare DATA stream A with Phase 1 build on Holistika tenant.
2. Invoke **Microsoft demo factory** — Methods A and/or B; seed three-tab referential per demo spec §3.
3. Implement composition for **maintenance + CAPEX** rule branches; test ≥3 fixture emails each.
4. Activate contract `DC-HOL-SUEZ-LIBELLE-STAGING-001`; set adapter `power_platform` → `active`.
5. Capture evidence under `00-internal/evidence/`.
6. Run **pre-send regression** per `docs/wip/planning/86-initiative-cluster-execution-coordinator/pre-send-regression-gate-spec-2026-05-26.md` before shipping customer PDF.
7. On revenue booking → **production readiness** SOP for Buckets/licensing hardening.

## Steps (AC-HUMAN) — Parallel Edge proof (optional)

1. Confirm contract + adapter `holistika_edge` active.
2. Implement Edge Function + HLK-ERP validation panel per `DATA_INTEGRATION_PLANE.md`.
3. Compare libellé output intent against Phase 1 MS demo — discrepancies feed build log, not customer send.

## Steps (AC-AUTOMATION)

```powershell
py scripts/bi_integration_readiness_check.py --self-test
py scripts/bi_integration_readiness_check.py --report
py -m pytest tests/test_ms_demo_methods.py tests/test_production_readiness_methods.py -v
py scripts/validate_collaborator_share.py --engagement-id ENG-SUEZ-WEBUY-2026
```

PASS: readiness green; staging contract + adapters resolve; share validators PASS when commercial artefacts ship.

## Failure modes

| Failure | Recovery |
|:---|:---|
| Built only Edge proof while MS demo unfunded but revenue exists | Schedule Phase 1 MS build — Edge is parallel, not primary |
| Used client tenant for Phase 1 without ratification | Rebuild on Holistika tenant |
| Confused EFA commercial Stream B with DATA Stream B | MS demo factory addendum disambiguation table |
| Customer-pack "votre environnement" treated as build SSOT | Internal grounding wins |
| Libellé misses CAPEX branch | Add rule branch before sign-off |
| Shipped customer pack without pre-send regression | Hold send; run 6-layer sweep |

## Outputs

- Phase 1 demo on Holistika tenant + evidence folder.
- Registry rows current (contract, adapter, BI consumer).
- Pre-send regression report when external surfaces ship.
- Build log noting Phase 2 readiness gaps if any.

## Cross-references

- Demo factory: `SOP-DATA_MS_DEMO_FACTORY_001.md`
- Production: `SOP-DATA_PRODUCTION_READINESS_001.md`
- Scaffold: `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`
- Send pack charter: `docs/wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-3-suez-poc-send-pack.md`
- Stream disambiguation: `SOP-DATA_MS_DEMO_FACTORY_001.addendum.md`
