---
packet_id: FINANCE-F3-2026-06-05
phase: F3
seat: execution
model_pin: composer-2.5
tranche_class: internal_governance
prerequisites:
  - feat(i88-finance-f2b) committed
  - reports/finance-area-f3-tranche-charter.md
status: executed_2026-06-05
---

# F3 executor packet — tech plane + finance cursor rule

## Mission

Close Finance **AREA-11** (cursor rule + skill), elevate **AREA-10** to partial
(repo-native FINOPS mirror evidence), wire **FINOPS-SPINE** dataops probes, and
mint first monthly recon with **registered_fact SKIP** per entity gate.

## Verification

```powershell
py scripts/synthesis_before_tranche_check.py --check-charter reports/finance-area-f3-tranche-charter.md
py scripts/dataops_quality_check.py --data-fam FINOPS-SPINE
py scripts/finops_monthly_recon.py --self-test
py scripts/finops_monthly_recon.py --report --month 2026-06
py scripts/validate_area_completeness.py --matrix
py scripts/validate_hlk.py
```

## Commit

`feat(i88-finance-f3): FINOPS spine probes, finance-ops rule, monthly recon`
