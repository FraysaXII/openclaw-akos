---
report_kind: finops_monthly_recon
month: 2026-06
authored: 2026-06-05
program: FINANCE-AREA-FULL
phase: F3
entity_gate_process: thi_finan_dtp_306
registered_fact_verdict: SKIP
---

# FINOPS monthly recon — 2026-06

## Summary

| Check | Evidence | Verdict |
|:---|:---|:---|
| Counterparty register rows | 28 (floor 25) | PASS |
| `validate_finops_ledger.py` | rc=0 | PASS |
| FINOPS-SPINE dataops sweep | clean=3 gap=0 | PASS |
| `finops.registered_fact` live rows | entity gate open | SKIP |

## FINOPS-SPINE probes

| Dimension | Verdict | Notes |
|:---|:---|:---|
| DATA-01-FK-INTEGRITY | clean | FINOPS-SPINE: counterparty register SSOT + validate_finops_ledger.py present |
| DATA-02-MIRROR-PARITY | clean | FINOPS-SPINE: 1 mirror target has DDL + emit symbol |
| DATA-07-QUALITY-METRICS | clean | FINOPS-SPINE: 3 plane validators present |

## Entity gate (M3 partial)

Production monetary facts in `finops.registered_fact` are **deferred** until
entity readiness process `thi_finan_dtp_306` closes. Synthetic validator coverage
via `validate_finops_ledger.py` remains the git SSOT check at F3.

## Mirror apply (operator SQL gate)

Generate DML with:

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only --output docs/wip/planning/88-cross-area-ops-wiring-review-discipline/artifacts/finops-counterparty-mirror-upsert.sql
```

Apply per `akos-holistika-operations.mdc` after operator approval.

## Validator excerpt

```
FINOPS Ledger Validator (B-2a substrate)
  ========================================
  REGISTERED_FACT_FIELDNAMES: 14 columns (14 expected)
  VALID_FACT_TYPES: 10 enum values
  VALID_FX_SOURCES: 5 enum values
  VALID_RESOLUTION_STRATEGIES: 5 enum values
  Synthetic facts validated: 4

  PASS: all synthetic facts + resolution strategies + FX ladder + OPS emit round-tripped clean.
```
