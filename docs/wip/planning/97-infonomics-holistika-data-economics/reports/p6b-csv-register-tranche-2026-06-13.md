---
report_type: phase_closure
initiative_id: INIT-OPENCLAW_AKOS-97
phase: P6b-CSV
authored: 2026-06-13
authored_by: AIC
audience: J-OP
language: en
---

# I97 P6b-CSV — Register economic column tranche (2026-06-13)

## Outcome

Infonomics doctrine **§4 register hooks** are now physical columns on the governed CSV registers — not schema-only declarations. Pydantic fieldnames, validators, row backfills, and Supabase mirror DDL are in lockstep.

## Registers amended

| Register | New columns | Rows |
|:---|:---|:---|
| `DATA_CONTRACT_REGISTRY` | `economic_value_class`, `carrying_cost_band`, `monetization_status` | 14 — evidence-rated per contract |
| `FINOPS_COUNTERPARTY_REGISTER` | `information_asset_ref` | 28 — 9 vendor rows linked to `DC-HOL-*` contracts |
| `FINOPS_PERFORMANCE_OBLIGATION_REGISTRY` | `information_asset_ref` | 5 — all PO rows linked |
| All 9 `*_ADAPTER_REGISTRY` | `handoff_cost_band`, `value_stream_id` | REVOPS 4 rows populated; others empty pending cross-area bridges |

## SSOT + mirrors

| Layer | Path |
|:---|:---|
| Shared enums | `akos/hlk_infonomics_register.py` |
| Data contracts | `akos/hlk_data_contract_csv.py` |
| FINOPS counterparty | `akos/hlk_finops_counterparty_csv.py` |
| FINOPS perf obligation | `akos/hlk_pricing_tier_registry_csv.py` |
| Adapters | `akos/hlk_adapter_registry_csv.py` |
| Mirror DDL | `supabase/migrations/20260613120000_i97_p6b_infonomics_register_columns.sql` |
| Backfill script | `reports/_apply_i97_register_columns.py` |

## Verification

```powershell
py scripts/validate_data_contract_registry.py
py scripts/validate_finops_counterparty_register.py
py scripts/validate_pricing_tier_registry.py
py scripts/validate_adapter_registries.py
py scripts/validate_compliance_schema_drift.py
py scripts/validate_hlk.py
```

All **PASS** after tranche close.

## Next

P7 closure UAT — full I97 program sign-off.
