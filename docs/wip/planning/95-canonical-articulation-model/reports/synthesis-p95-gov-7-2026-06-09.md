---
tranche_id: P95-GOV-7
tranche_class: canonical_csv_mint
ratifying_decisions:
  - D-IH-95-B
  - D-IH-93-D
  - D-IH-93-I
  - D-IH-88-E
reversibility_class: medium
synthesis_complete: true
verdict: PASS
---

# Synthesis — P95-GOV-7 (forward-charter mirror DDL tranche)

**Date:** 2026-06-09  
**Tranche:** Activate Plane-2 DDL + main-bundle emit for six forward-charter surfaces

## Fire set (canonical_csv_mint)

| Dimension | Status | Note |
|:---|:---:|:---|
| SYN-01 Audience completeness | PASS | Finance + Data Governance + Compliance techops surfaces named |
| SYN-05 Ratification lineage | PASS | D-IH-95-B + Finance F2a/F2b + I93 data-contract / RPA precedents |
| SYN-07 Tranche atomicity | PASS | migrations + emit + registry + validators + tests in one tranche |
| SYN-08 Reversibility | PASS | medium — DROP TABLE rollback + revert emit/registry rows |
| SYN-09 Closing-loop test | PASS | `validate_pydantic_mirror_enum_ssot.py` + `validate_mirror_emit_contract.py` + `validate_hlk.py` |
| SYN-02/03/04/06/10 | INFO | No new external prose |

## Deliverables

| Surface | Emit profile | Sync policy | Mirror table |
|:---|:---:|:---:|:---|
| `PRICING_TIER_REGISTRY.csv` | `main` | `active` | `pricing_tier_registry_mirror` |
| `FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv` | `main` | `active` | `finops_performance_obligation_registry_mirror` |
| `FINOPS_TAX_CALENDAR.csv` | `main` | `active` | `finops_tax_calendar_mirror` |
| `DATA_CONTRACT_REGISTRY.csv` | `main` | `active` | `data_contract_registry_mirror` |
| `RPA_ADAPTER_REGISTRY.csv` | `main` | `active` | `rpa_adapter_registry_mirror` |
| `COMPONENT_SERVICE_MATRIX.csv` | `main` | `active` | `component_service_matrix_mirror` |

## Mirror apply evidence stub

| Step | Status | Note |
|:---|:---:|:---|
| Prod DDL inventory (read-only) | **PENDING-OPERATOR** | Apply four `2026060912*` migrations after SQL gate approval |
| Operator walkthrough minted | **DONE** | [`operator-mirror-apply-walkthrough-2026-06-09.md`](operator-mirror-apply-walkthrough-2026-06-09.md) Phase B DDL + DML steps |
| `npx supabase db push --linked` (GOV-7) | **NOT RUN** | No Supabase auth in execution session; linked project-ref present locally |
| `gh workflow run supabase-mirror-sync.yml -f apply=true` | **NOT RUN** | Blocked on operator SQL gate |
| Post-apply row-count parity | **NOT RUN** | After apply; `validate_mirror_emit_contract.py` + §4.2 query in walkthrough |

## Verification (mechanical)

```text
py scripts/validate_pydantic_mirror_enum_ssot.py
py scripts/validate_mirror_emit_contract.py
py scripts/validate_hlk.py
py scripts/verify.py pre_commit_fast
py -m pytest tests/test_sync_compliance_mirrors_from_csv.py -v
```
