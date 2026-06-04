---
intellectual_kind: regression_report
initiative: I93
phase: P5c
authored: 2026-06-04
verdict: remediated_pre_commit
---

# SOP end-to-end chain regression — P5c integration family

## Scope

Mapped **all governed processes** that touch engagement demo build, BI consumption, and
external send — embedded as `## End-to-end process chain` in each P5c SOP.

## Process inventory (complete)

| item_id | SOP / artefact | Linked from |
|:---|:---|:---|
| `hol_data_dtp_engagement_integration_scaffold_001` | Scaffold SOP | Entry gate |
| `hol_data_dtp_ms_demo_factory_001` | MS demo factory SOP | MS build |
| `hol_data_dtp_production_readiness_001` | Production readiness SOP | Revenue gate |
| `hol_data_dtp_bi_integration_readiness_001` | DATA_BI_GOVERNANCE §7 | Automated probes |
| `hol_data_dtp_contract_registry_mtnce_001` | Contract maintenance SOP | Registry rows |
| `env_tech_dtp_dataops_quality_001` | DATAOPS discipline | Mirror/registry mint |
| `SOP-ENG_ESTIMATION_DISCIPLINE_001` | Estimation SOP | Commercial effort |
| `SOP-RESEARCH_ACTION_001` | Research action | Novel stack research |
| `SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001` | Synthesis discipline | Pre-commit tranche |
| Pre-send regression spec | I86 planning | External send block |
| External render + brand baseline | Quality Fabric | Customer pack |
| `validate_collaborator_share.py` | Collaborator share | SUEZ commercial |
| `SOP-DATA_SUEZ_LIBELLE_001` | SUEZ scenario | F-05 routing |
| `hol_data_dtp_datafam_*` (×7, P6) | Forward | DATA-FAM umbrellas |

## Remediation applied

- Renamed `SOP-DATA_SUEZ_STREAM_B_LIBELLE_001` → `SOP-DATA_SUEZ_LIBELLE_001` (full ripple).
- Added E2E tables to all four integration SOPs + pairing registry rows.
- Minted `akos/hlk_production_readiness_methods.py` + tests.

## Verdict

**Ready for commit** — no orphan process in the engagement-demo spine.
