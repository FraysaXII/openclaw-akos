---
title: SOP — Data Production Readiness
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_PRODUCTION_READINESS_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Office
co_authors:
  - CDO
  - RevOps Manager
last_review: 2026-06-04
last_review_by: Data Governance Office
last_review_decision_id: D-IH-93-J
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-J
status: active
register: internal
linked_canonicals:
  - DATA_BI_GOVERNANCE.md
  - dimensions/AREA_BI_PROFILE.csv
  - dimensions/BI_CONSUMER_REGISTRY.csv
  - DATA_PRIVACY_RETENTION_POLICY.md
linked_runbooks:
  - scripts/bi_integration_readiness_check.py
linked_processes:
  - hol_data_dtp_production_readiness_001
cadence: event_triggered
cadence_trigger: engagement customer signed OR operator promotes pilot surface to production
---

# SOP — Data Production Readiness (engagement-funded)

## Purpose

Promote a data or BI surface from **pilot / vendor-alpha / demo** to **production posture**
when a **paying engagement customer exists** and revenue covers infra, licensing, and
hardening work. Vendor marketing labels (e.g. "Public Alpha") inform risk documentation —
they do **not** block promotion when the operator has activated the surface and funded
hardening is booked to the engagement.

Pairs `hol_data_dtp_production_readiness_001`.

## Scope

| In scope | Out of scope |
|:---|:---|
| Analytics Buckets, Metabase, Power Platform, ERP panels, export views | Net-new warehouse platform selection (Snowflake/BQ) |
| AREA_BI_PROFILE + BI consumer alignment per area | Rewriting customer-pack delivery prose |
| Privacy class + contract rows for each production surface | Client-tenant production without Phase 1 MS evidence |
| Commercial trace to `engagement_id` when revenue posts | |

## Inputs

- Signed engagement or operator ratification memo with revenue allocation for infra/licensing.
- Target surface list (tools, schemas, dashboards) from demo factory or area BI profile.
- Current `AREA_BI_PROFILE.csv` row for consuming area(s).
- Privacy classification per `DATA_PRIVACY_RETENTION_POLICY.md`.
- Phase 1 evidence when promoting Microsoft stack (`SOP-DATA_MS_DEMO_FACTORY_001.md`).

## Method selection

| Surface pattern | Method |
|:---|:---|
| Holistika-owned Supabase / ERP / Buckets / Metabase | **PROD-METHOD-INTERNAL** |
| Microsoft stack (Holistika or client tenant) | **PROD-METHOD-CLIENT-MS** |
| Client BI reads Holistika exports (FDW, views, webhooks) | **PROD-METHOD-HYBRID** |

## Method library

| method_id | Label | Typical surfaces | Paired upstream SOP |
|:---|:---|:---|:---|
| `PROD-METHOD-INTERNAL` | Holistika stack hardening | Analytics Buckets, Metabase, `erp.vw_*`, Langfuse | `DATA_BI_GOVERNANCE.md` |
| `PROD-METHOD-CLIENT-MS` | Microsoft production path | Power Platform, Power BI, SharePoint referential | `SOP-DATA_MS_DEMO_FACTORY_001.md` |
| `PROD-METHOD-HYBRID` | Stream C bridge | FDW finops, export views, Make/n8n bridges | `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md` |

Registry SSOT: `akos/hlk_production_readiness_methods.py` (drift test in `tests/test_production_readiness_methods.py`).

## End-to-end process chain

| Stage | Process / artefact | Owner | Gate |
|:---|:---|:---|:---|
| **Upstream — demo** | `hol_data_dtp_ms_demo_factory_001` + Phase 1 evidence | RevOps Manager | Required for PROD-METHOD-CLIENT-MS |
| **Upstream — scaffold** | `hol_data_dtp_engagement_integration_scaffold_001` | Data Governance Office | Streams + contracts declared |
| **Upstream — finops** | Engagement revenue spine / `finops.registered_fact` (RevOps P7 forward) | Business Controller | Revenue trace |
| **This SOP** | `hol_data_dtp_production_readiness_001` | CDO / Data Governance Office | Signed promotion record |
| **Parallel — area BI** | `AREA_BI_PROFILE.csv` steward alignment | Area heads | Per-area consumption |
| **Parallel — privacy** | `DATA_PRIVACY_RETENTION_POLICY.md` | Legal Counsel | Classification set |
| **Downstream — DataOps** | `env_tech_dtp_dataops_quality_001` `--data-fam` (P6) | System Owner | Live probes post-promotion |
| **Downstream — P6** | DATA-FAM umbrella CAP rows (forward) | CDO | Family-level data products |

## Steps (AC-HUMAN)

1. **Confirm funding** — engagement_id linked; infra/licensing line visible in commercial schedule or operator memo.
2. **Pick method** — table above; one method per surface batch (may combine INTERNAL + CLIENT-MS on same engagement).
3. **Refresh area profile** — steward role and `primary_consumer_ids` match production tools.
4. **Mint or activate contracts** — one row per producer × `data_surface`; no dashboard-only shortcuts.
5. **Set privacy class** — per surface; escalate Legal Counsel if counterparty PII crosses tenant boundary.
6. **Run hardening checklist** — backups, RLS review, idempotency (Edge), licensing seats documented off-repo.
7. **Operator sign-off** — CDO or Data Governance Office signs promotion record in engagement folder.
8. **Billback note** — Finance/Business Controller tags infra cost to engagement where applicable.

## Steps (AC-AUTOMATION)

```powershell
py scripts/validate_area_bi_profile.py
py scripts/validate_bi_consumer_registry.py
py scripts/bi_integration_readiness_check.py --report
py scripts/validate_data_contract_registry.py
py -m pytest tests/test_production_readiness_methods.py -v
```

PASS: area profile FKs resolve; readiness report green; contracts cover all promoted surfaces.

## Failure modes

| Failure | Recovery |
|:---|:---|
| Promoted surface lacks BI consumer row | Mint consumer + matrix row before go-live |
| Analytics Buckets deferred for vendor label alone | Re-run with operator production posture (D-IH-93-J); document residual vendor risk |
| Client tenant production without Phase 1 evidence | Complete demo factory Phase 1 first |
| Area steward not in `baseline_organisation.csv` | Fix steward role on profile row |
| No engagement_id when revenue exists | Link finops spine row before declaring production |

## Outputs

- Signed production promotion record (engagement `00-internal/` or governance report folder).
- Updated `AREA_BI_PROFILE.csv` / `BI_CONSUMER_REGISTRY.csv` / contract rows with `active` status.
- Operator-visible runbook note for on-call (which probes fire, which SOP owns recovery).

## Cross-references

- Microsoft demos: `SOP-DATA_MS_DEMO_FACTORY_001.md`
- Multi-area consumption: `DATA_BI_GOVERNANCE.md` §3a
- P6 DATA-FAM: `docs/wip/planning/93-data-area-foundation-and-governance/reports/cross-area-data-map-2026-06-04.md`
