---
evidence_id: FINANCE-F2A-EVIDENCE-2026-06-05
phase: F2a
program: FINANCE-AREA-FULL
authored: 2026-06-05
verdict: PASS
---

# F2a execution evidence — rev-rec, pricing registry, DC seeds

## Verification matrix

| Gate | Result |
|:---|:---|
| `synthesis_before_tranche_check.py` (F2a charter) | PASS 9/9 |
| `validate_pricing_tier_registry.py --self-test` | PASS |
| `validate_pricing_tier_registry.py` | PASS (6 tiers; 5 obligations) |
| `validate_data_contract_registry.py` | PASS (14 rows) |
| `validate_hlk.py` | OVERALL PASS |
| `validate_area_completeness.py --matrix` | Finance **88%** (11 pass / 1 partial / 1 gap) |
| `pytest tests/test_pricing_tier_registry.py` | 2/2 PASS |

## Matrix delta (Finance)

| Component | F1 | F2a |
|:---|:---|:---|
| AREA-06 CAPABILITY-CONFIDENCE | partial (probe bug: CONF lacks `area` column) | **pass** (probe joins via `capability_id`) |
| AREA-08 DIMENSION-REGISTRIES | gap | **pass** (2 dimension CSVs) |
| AREA-09 PAIRED-SOP-RUNBOOK | partial | partial (runbook note on `thi_finan_dtp_303`; full pairing deferred to F3/F4) |
| AREA-11 CURSOR-RULE-SKILL | gap | gap (F3) |

## Minted artefacts

- `Finance/Business Controller/canonicals/FINOPS_REVENUE_RECOGNITION_POLICY.md` (status **active**)
- `Finance/Governance/canonicals/dimensions/PRICING_TIER_REGISTRY.csv`
- `Finance/Governance/canonicals/dimensions/FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv`
- `akos/hlk_pricing_tier_registry_csv.py` + `scripts/validate_pricing_tier_registry.py`
- 5 `DC-HOL-FINOPS-*` rows in `DATA_CONTRACT_REGISTRY.csv`
- `CANONICAL_REGISTRY` rows: rev-rec policy, pricing registry, perf-obligation registry

## Notes

- CONF rows for Finance CAP-* already seeded at I82; **not duplicated** — AREA-06 fixed via probe join.
- F2b (`FINOPS_TAX_CALENDAR.csv`) remains operator/counsel gate.
