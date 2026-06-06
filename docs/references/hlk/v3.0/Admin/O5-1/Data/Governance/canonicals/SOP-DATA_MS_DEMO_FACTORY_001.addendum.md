---
title: SOP — Microsoft Demo Factory (addendum)
language: en
intellectual_kind: data-canonical-sop-addendum
parent_sop: SOP-DATA_MS_DEMO_FACTORY_001.md
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
role_owner: Data Governance Office
last_review: 2026-06-04
last_review_by: Data Governance Office
last_review_decision_id: D-IH-93-J
methodology_version_at_review: v3.1
status: active
register: internal
---

# Addendum — Microsoft Demo Factory

## Phase 1 vs Phase 2 handoff

| Phase | Tenant | Evidence | Owner |
|:---|:---|:---|:---|
| **1** | Holistika Microsoft | Screenshots + internal validation + build log | RevOps Manager + System Owner |
| **2** | Client Azure (optional) | DSI sign-off; `pac solution export/import` | Client DSI + Holistika delivery |

Internal SSOT for build location: `Think Big/Clients/2026-suez-webuy/00-internal/source-grounding-post-handshake-2026-05-26.md` §5 (operator tenant + anonymised data).

## Stream naming disambiguation (do not conflate)

Three different "stream" vocabularies appear in SUEZ and DATA artefacts:

| Vocabulary | Meaning | Example |
|:---|:---|:---|
| **DATA engagement stream A/B/C** | Integration plane per `DATA_BI_GOVERNANCE.md` §4 — where code and data run | Stream A = client Power Platform tenant; Stream B = Holistika Edge/ERP |
| **SUEZ commercial Stream A/B** | Collaborator-share grounding — **who invoices** | Stream A = Holistika automation project; Stream B = EFA maintenance (Holistika not party) |
| **Phase 1 / Phase 2 (this SOP)** | **Build location** for Microsoft demos | Phase 1 = Holistika tenant; Phase 2 = client tenant handoff |

Auditors and executors must cite which vocabulary applies in each checklist row.

## Validator + registry FKs

| Check | Command / row |
|:---|:---|
| BI consumer | `validate_bi_consumer_registry.py` — `BI-HOL-POWER-PLATFORM` |
| RPA adapter | `validate_adapter_registries.py` — `power_platform` |
| Matrix parent | `COMPONENT_SERVICE_MATRIX` — `comp_matriz_00013` |
| Method drift | `pytest tests/test_ms_demo_methods.py` |

## Licensing audit material

Document SKU + seat count in engagement folder only — never in git secrets.
Operator ratified dual-path 2026-06-04: Method A (CLI + pac) and Method B (Browser) both active.

## Parallel technical proof (Edge + ERP)

When client Power Automate is **blocked**, Holistika may still run **Stream B integration
proof** (Edge Function + HLK-ERP panel) per `DATA_INTEGRATION_PLANE.md`. That path validates
internal logic but **does not replace** Phase 1 Microsoft demo build when engagement revenue
funds the production MS stack (operator ratification D-IH-93-J).
