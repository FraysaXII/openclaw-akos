---
packet_id: FINANCE-F2A-2026-06-05
phase: F2a
seat: execution
model_pin: composer-2.5
tranche_class: canonical_csv_mint
operator_gates:
  - PRICING_TIER_REGISTRY.csv
  - CAPABILITY_CONFIDENCE_REGISTRY.csv
  - DATA_CONTRACT_REGISTRY.csv
prerequisites:
  - feat(i88-finance-f1) committed
  - reports/research-f2a-revrec-pricing-2026-06-05.md
  - reports/finance-area-f2a-tranche-charter.md
status: executed_2026-06-05
---

# F2a executor packet — rev-rec + pricing + contracts + CONF

> **Prerequisite:** F1 complete (`fe1c246`). Research:
> [`research-f2a-revrec-pricing-2026-06-05.md`](research-f2a-revrec-pricing-2026-06-05.md).

## Mission

Close Finance **plane 2** SSOT gap and partial **AREA-06 / AREA-08 / AREA-09**:
rev-rec policy, pricing tier registry, five DC-FINOPS-* contracts, 16 CONF seeds.
Target matrix **≥77%** (from 77% baseline — must not regress; aim 82%+).

## Files (ordered)

| # | Action | Path |
|:---:|:---|:---|
| 1 | CREATE | `Finance/Business Controller/canonicals/FINOPS_REVENUE_RECOGNITION_POLICY.md` |
| 2 | CREATE | `Finance/Governance/canonicals/dimensions/PRICING_TIER_REGISTRY.csv` |
| 3 | CREATE | `akos/hlk_pricing_tier_registry_csv.py` + `scripts/validate_pricing_tier_registry.py` + tests |
| 4 | EDIT | `DATA_CONTRACT_REGISTRY.csv` — 5 rows (see §DC table) |
| 5 | EDIT | `CAPABILITY_CONFIDENCE_REGISTRY.csv` — 16 CONF rows for Finance `CAP-*` |
| 6 | EDIT | `process_list.csv` — `runbook_path` / instructions for `thi_finan_dtp_303` → `validate_finops_ledger.py` |
| 7 | EDIT | `CANONICAL_REGISTRY.csv` — rev-rec policy + pricing registry rows |
| 8 | EDIT | `validate_hlk.py` — wire pricing validator |

## DC-FINOPS-* rows (paste spec)

| contract_id | producer | consumers | data_surface |
|:---|:---|:---|:---|
| DC-FINOPS-REGISTERED-FACT-001 | `thi_finan_dtp_303` | RevOps;Data | `finops.registered_fact` |
| DC-LEGAL-FINOPS-INSTRUMENT-001 | Legal instrument process | Finance | mirror + FK `finops_counterparty_id` |
| DC-PEOPLE-FINOPS-PAYOUT-001 | People payout process | Finance | engagement fact |
| DC-MKT-FINOPS-CAPEX-001 | `thi_finan_dtp_272` | Marketing;Finance | campaign spend grain |
| DC-REVOPS-FINOPS-ENGAGEMENT-001 | `thi_finan_dtp_271` | RevOps;Finance | engagement revenue chain |

Follow `DATA_CONTRACT_STANDARD.md` columns; `quality_rules` use DATA-01..07 only.

## Rev-rec policy sections

1. IFRS 15 / Spain GAAP posture (charter → **active** at F2a)
2. Performance obligation table keyed to `pricing_tier_id`
3. Deferred revenue + annual prepay + refund/pro-ration
4. Evidence base: EXT-04 + OPS-81-5 + internal PMO PRICING_MODEL cross-ref

## Verification

```powershell
py scripts/synthesis_before_tranche_check.py --check-charter reports/finance-area-f2a-tranche-charter.md
py scripts/validate_pricing_tier_registry.py --self-test
py scripts/validate_data_contract_registry.py --self-test
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --matrix
```

## Stop conditions

- Operator gate not cleared for 3 CSV files
- Pricing tier without perf-obligation row in policy table
- DC row without resolvable `producer_process_id`

## Commit

`feat(i88-finance-f2a): rev-rec policy, pricing registry, DC-FINOPS seeds, CONF rows`
