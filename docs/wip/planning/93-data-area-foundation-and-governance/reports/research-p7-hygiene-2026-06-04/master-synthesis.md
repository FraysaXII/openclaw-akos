---
intellectual_kind: research_master_synthesis
initiative: I93
pack_id: research-p7-hygiene-2026-06-04
authored: 2026-06-04
control_confidence_level: Safe
feeds_phase: P7
ratifying_decision: D-IH-93-E
---

# Master synthesis — P7 component + engagement + transcript hygiene

## Executive summary

P7 closes **D-IH-93-E** (operator ratified all four fixes): make the component matrix
declare real sensitivity/retention, reconcile `eng_*` registry IDs with `ENG-*` commercial
codes, add missing partner GOI rows, backfill five POC use-case realisations, and mint a
transcript-backfill tracker without promoting raw audio to SSOT.

## Deliverables (mint tranche)

| # | Artifact | Action |
|:---|:---|:---|
| 1 | `COMPONENT_SERVICE_MATRIX.csv` | Rule-based `data_classification`, `retention_policy_ref`, `legal_hold` |
| 2 | `ENGAGEMENT_REGISTRY.csv` | +`canonical_engagement_code` column; +`eng_2026_websitz_shopify`; alias map |
| 3 | `GOI_POI_REGISTER.csv` | +`GOI-PARTNER-WEBSITZ-2026`, +`GOI-PARTNER-RUSHLY-2026` |
| 4 | `USE_CASE_ARCHIVE.csv` | +5 rows (`USE-000002`..`USE-000006`) from POC map |
| 5 | `transcript-backfill-tracker-2026-06-04.csv` | 27 rows YES/PARTIAL/NO |
| 6 | `scripts/i93_p7_hygiene_apply.py` | Deterministic matrix population (re-run safe) |

## Engagement ID reconciliation rule

| Registry `engagement_id` | `canonical_engagement_code` |
|:---|:---|
| `eng_2026_suez_webuy` | `ENG-SUEZ-WEBUY-2026` |
| `eng_2026_websitz_shopify` (new) | `ENG-WEBSITZ-SHOPIFY-2026` |
| Others | empty until commercial spine adopts `ENG-*` |

Commercial/share artifacts keep using `ENG-*`; joins use `canonical_engagement_code`.

## Out of scope (P8 / follow-up)

- Supabase `engagement_registry_mirror` column for `canonical_engagement_code` (forward DDL tranche).
- Full Topic-Fact-Source promotion of all 27 transcripts (tracker only at P7).
