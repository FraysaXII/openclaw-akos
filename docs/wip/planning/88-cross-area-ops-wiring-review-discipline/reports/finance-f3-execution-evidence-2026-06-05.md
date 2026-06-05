---
evidence_id: FINANCE-F3-EVIDENCE-2026-06-05
phase: F3
program: FINANCE-AREA-FULL
authored: 2026-06-05
verdict: PASS
---

# F3 execution evidence — tech plane + finance cursor rule

## Verification matrix

| Gate | Result |
|:---|:---|
| `synthesis_before_tranche_check.py` (F3 charter) | PASS 7/7 |
| `dataops_quality_check.py --self-test` | PASS (8 families) |
| `dataops_quality_check.py --data-fam FINOPS-SPINE` | 3/3 clean |
| `finops_monthly_recon.py --self-test` | PASS |
| `finops_monthly_recon.py --report --month 2026-06` | [`finops-recon-2026-06.md`](finops-recon-2026-06.md) |
| `validate_area_completeness.py --matrix` | Finance **93%** (12 pass / 2 partial / 0 gap) |
| pytest FINOPS tests | 10/10 PASS |

## Matrix delta (Finance)

| Component | F2b | F3 |
|:---|:---|:---|
| AREA-10 SUPABASE-MIRRORS | skip | **partial** (repo-native I18 DDL + sync emit) |
| AREA-11 CURSOR-RULE-SKILL | gap | **pass** (`akos-finance-ops.mdc` + `finance-ops-craft`) |

## Minted artefacts

- `.cursor/rules/akos-finance-ops.mdc`
- `.cursor/skills/finance-ops-craft/SKILL.md`
- `scripts/finops_monthly_recon.py`
- `FINOPS-SPINE` dataops family in `akos/hlk_dataops_quality.py`
- M2 floor **N=25** documented in `FINANCE_AREA_CHARTER.md`
- Rule router Finance/FINOPS row

## Entity gate (M3)

`registered_fact` first live row: **SKIP** — `thi_finan_dtp_306` entity gate open.
Documented in monthly recon report.

## Operator follow-up (not blocking F3)

1. Generate + apply finops counterparty mirror DML via `sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only`
2. Stripe `finops_counterparty_id` link coverage SQL at incorporation
3. F4 closure UAT + `compose_FINOPS` promote to **active**
