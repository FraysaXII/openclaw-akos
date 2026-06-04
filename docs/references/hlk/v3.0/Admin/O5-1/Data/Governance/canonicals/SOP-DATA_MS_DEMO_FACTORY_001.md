---
title: SOP — Microsoft Demo Factory
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_MS_DEMO_FACTORY_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Lead
co_authors:
  - RevOps Lead
  - System Owner
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_decision_id: D-IH-93-J
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-J
  - D-IH-93-I
status: active
register: internal
companion_to:
  - SOP-DATA_MS_DEMO_FACTORY_001.addendum.md
linked_canonicals:
  - DATA_BI_GOVERNANCE.md
  - DATA_INTEGRATION_PLANE.md
  - dimensions/RPA_ADAPTER_REGISTRY.csv
  - dimensions/BI_CONSUMER_REGISTRY.csv
linked_runbooks:
  - docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/runbooks/ms-demo-cli-method-a.md
  - docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/runbooks/ms-demo-browser-method-b.md
linked_processes:
  - hol_data_dtp_ms_demo_factory_001
cadence: event_triggered
cadence_trigger: engagement declares Microsoft stack OR use-case demo build on Holistika tenant
---

# SOP — Microsoft Demo Factory (Phase 1 Holistika tenant)

## Purpose

Build **use-case demos** (Excel referential + Power Apps + Power Automate + Power BI)
on the **Holistika Microsoft tenant** with anonymised data, governed registry rows, and
evidence suitable for customer-pack PDFs — **before** any optional handoff to a client
tenant (Phase 2).

Customer-pack prose that reads *"dans votre environnement Microsoft Azure"* is
**translated delivery language** for the counterparty. Internal build location is
Holistika tenant unless the operator explicitly ratifies client-tenant-first.
See post-handshake grounding: operator builds on own tenant; no screenshots from
prior client work (`source-grounding-post-handshake-2026-05-26.md` §3.2, §5).

## Scope

| In scope | Out of scope |
|:---|:---|
| Phase 1 demo build on Holistika Microsoft tenant | Storing PA/PP solution JSON inside AKOS repo |
| Method A (CLI + pac) and Method B (portal + Browser) | Client DSI production cutover (Phase 2 — addendum) |
| Registry mint: adapter, BI consumer, contract, matrix | EFA-only proposals on EFA tenant (separate commercial stream) |
| Evidence capture under engagement `00-internal/evidence/` | Prior-client screenshot reuse (IP policy) |

## Inputs

- Engagement demo spec under `Think Big/Clients/<slug>/02-customer-pack/` (or operator-pack feasibility shape).
- Completed **engagement integration scaffold** checklist (`SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`).
- Holistika Microsoft tenant access (operator gate for auth).
- Anonymised referential CSV or Excel seed (generic supplier/parc names — never counterparty-actual rows in git).
- Target capability id (e.g. SUEZ F-05 libellé generator).

## Roles

| Role | Responsibility in this SOP |
|:---|:---|
| **RevOps Lead** | Owns demo-factory execution coordination; adapter lifecycle |
| **Data Governance Lead** | Signs registry tranche + stream declaration |
| **System Owner** | Tenant auth gate; Edge parallel proof when PA blocked |
| **AIC (hybrid methods)** | Runs deterministic CLI or Browser steps under operator watch |

## Method selection

| Situation | Method |
|:---|:---|
| `pac` + `az` available; solution export/import needed | **MS-DEMO-METHOD-A** |
| Licensing or canvas design is UI-only; PDF needs screenshots | **MS-DEMO-METHOD-B** |
| Both viable (typical) | **A** for solution structure and repeatability; **B** for evidence capture |
| Client PA permanently blocked before Phase 1 completes | Finish Phase 1 on Holistika tenant anyway; parallel Edge proof per SUEZ scenario SOP — not a substitute for MS build when engagement revenue funds production |

## Method library

| method_id | Label | Executor | Runbook | When |
|:---|:---|:---|:---|:---|
| `MS-DEMO-METHOD-A` | Azure CLI + pac | Hybrid | `../runbooks/ms-demo-cli-method-a.md` | Export/import, repeatable builds, CI-friendly steps |
| `MS-DEMO-METHOD-B` | Portal + Browser | Hybrid | `../runbooks/ms-demo-browser-method-b.md` | UI licensing, canvas layout, screenshot deliverable |

Registry SSOT: `akos/hlk_ms_demo_methods.py` (must match this table; drift test in `tests/test_ms_demo_methods.py`).

## End-to-end process chain

| Stage | Process / artefact | Owner | Gate |
|:---|:---|:---|:---|
| **Upstream** | `hol_data_dtp_engagement_integration_scaffold_001` | Data Governance Lead | Scaffold signed first |
| **Upstream** | `hol_data_dtp_contract_registry_mtnce_001` | Data Steward | Contract rows per surface |
| **Upstream** | `SOP-ENG_ESTIMATION_DISCIPLINE_001` (build methods in scope.yaml) | Project Manager | Effort for `build_prototype_excel` / `build_webapp` |
| **This SOP** | `hol_data_dtp_ms_demo_factory_001` | RevOps Lead | Phase 1 demo complete |
| **Scenario** | `SOP-DATA_SUEZ_LIBELLE_001.md` (when ENG-SUEZ-WEBUY-2026) | Data Governance Lead | F-05-specific routing |
| **Downstream** | `hol_data_dtp_bi_integration_readiness_001` | Data Steward | Probes before commit |
| **Downstream** | `hol_data_dtp_production_readiness_001` | CDO | On revenue |
| **Pre-send** | Pre-send regression spec (L1–L6) | Operator | Before customer PDF |
| **External** | External render + brand baseline | Brand Manager | Counterparty-facing artefacts |
| **Tranche** | `SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001` | PMO | `canonical_csv_mint` class |
| **DataOps** | `env_tech_dtp_dataops_quality_001` | System Owner | On registry/mirror mint |

## Steps (AC-HUMAN)

1. **Confirm scaffold complete** — streams declared; contract + adapter stubs exist or are minted in the same tranche.
2. **Choose method(s)** — apply table above; record choice in engagement `00-internal/build-log.md` (create on first build).
3. **Seed referential** — three-tab Excel pattern (parc, suppliers, naming rules) or git CSV equivalent with anonymised values per demo spec.
4. **Build canvas app + cloud flow** on Holistika tenant — compose libellé (or target capability logic) per customer-pack worked example; validate against ≥3 fixture emails.
5. **Wire reporting** — Power BI or ERP export view row if demo spec includes dashboard tile.
6. **Capture evidence** — screenshots + short operator validation note; **no** prior-client imagery.
7. **Registry tranche** — activate `power_platform` adapter + `BI-HOL-POWER-PLATFORM` consumer; matrix FK resolves.
8. **Sign-off** — RevOps Lead + Data Governance Lead confirm demo matches spec **intent** (wording in customer-pack may stay counterparty-facing).
9. **Production promotion** — when engagement revenue lands, invoke `SOP-DATA_PRODUCTION_READINESS_001.md` (do not defer because vendor labels a feature "alpha").

## Steps (AC-AUTOMATION)

```powershell
py scripts/bi_integration_readiness_check.py --self-test
py scripts/bi_integration_readiness_check.py --report
py scripts/validate_bi_consumer_registry.py
py scripts/validate_adapter_registries.py
py -m pytest tests/test_ms_demo_methods.py -v
```

PASS: readiness report green; registry validators PASS; method registry matches SOP table.

## Failure modes

| Failure | Recovery |
|:---|:---|
| Built on client tenant first without operator ratification | Rebuild on Holistika tenant; update stream declaration in scaffold checklist |
| Demo works but no adapter/consumer rows | Stop — mint registry tranche before declaring build complete |
| Method A auth fails | Switch to Method B for build; file OPS note for CLI credential path |
| Method B screenshot lacks anonymisation | Re-capture with generic referential; never ship counterparty-actual fields |
| Customer-pack Stream A/B language confused with DATA stream A/B/C | Use addendum disambiguation table; DATA streams govern **integration plane** only |
| Phase 2 requested before Phase 1 evidence | Complete Phase 1 sign-off + PDF trail first |

## Outputs

- Working demo on Holistika Microsoft tenant (flows live in tenant, not git).
- `00-internal/evidence/` screenshot set + build log.
- Updated registry rows (RPA adapter, BI consumer, data contract, matrix).
- Optional customer-pack PDF update (external render discipline applies).
- Phase 2 handoff pack (addendum) when DSI requires client tenant.

## Cross-references

- Upstream scaffold: `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`
- SUEZ F-05 scenario: `SOP-DATA_SUEZ_LIBELLE_001.md`
- Production hardening: `SOP-DATA_PRODUCTION_READINESS_001.md`
- Internal grounding: `Think Big/Clients/2026-suez-webuy/00-internal/source-grounding-post-handshake-2026-05-26.md` §5
- Addendum (validators, Phase 2, stream disambiguation): `SOP-DATA_MS_DEMO_FACTORY_001.addendum.md`
