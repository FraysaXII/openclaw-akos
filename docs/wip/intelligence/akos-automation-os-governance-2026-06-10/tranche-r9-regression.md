---
report_type: tranche-regression
tranche: R9
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R9 regression — Marketing + CRM adapters

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R9 slice) | 28 | 28 (`SRC-AOS-R9I-*`) | PASS |
| OSINT (R9 slice) | 44 | 44 (`SRC-AOS-R9E-*`) | PASS |
| Cumulative ledger | 701 | 701 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-MKT (brand canon, dual-register matrix) + CORP-VAULT-ADAPTERS (CRM/RPA/RevOps registries) + OSINT-RPA/INTEROP |
| 2 | Dual-source | PASS | 28 CORPINT + 44 OSINT |
| 3 | Voice diversity | PASS | Gartner iPaaS (3.1), RPA analyst reports (3.1), skeptic RPA hype (2.1) |
| 4 | Prong binding | PASS | P9-MARKETING + P12-RPA-ADAPTERS; ICS in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 701-row cumulative ledger |
| 6 | Skeptic balance | PASS | 11/44 OSINT (25%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D4 `linked_adapter_id` column + R10 verify/CI harvest |

## Dedup disposition

Manifest overflow candidates used where prior-tranche URL collisions would have left charter deficits; net-new URLs only in ledger append.

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `BRAND_BASELINE_REALITY_MATRIX.md` | Dual-register translation SSOT |
| `SOP-CRM_INTEGRATION_001.md` | CRM integration process |
| `CRM_ADAPTER_REGISTRY.csv` / `RPA_ADAPTER_REGISTRY.csv` | Adapter inventory |
| `validate_adapter_registries.py` | Adapter registry validator |

## Disposition

**PASS** — ready for phase commit.
