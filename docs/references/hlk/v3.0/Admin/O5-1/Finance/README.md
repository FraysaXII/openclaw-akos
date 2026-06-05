---
language: en
status: active
role_owner: CFO
classification: index
ssot: false
authored: 2026-06-05
last_review: 2026-06-05
last_review_decision_id: D-IH-88-E
---

# Finance area — v3.0 vault index

> O5-1 **Finance** area under Admin. Charter:
> [`canonicals/FINANCE_AREA_CHARTER.md`](canonicals/FINANCE_AREA_CHARTER.md)
> (`inherited_pattern_id=pattern_area_buildout`, FINANCE-AREA-FULL F1).

## Sub-domains

| Sub-domain | Path | Purpose |
|:---|:---|:---|
| **Governance** | [`Governance/canonicals/`](Governance/canonicals/) | FINOPS discipline; rev-rec / tax policy (F2+) |
| **Business Controller** | [`Business Controller/`](Business Controller/) | Counterparty SOPs, founder capital, pricing/tax folders |

## Key canonicals (F1)

| Artifact | Path |
|:---|:---|
| Area charter | [`canonicals/FINANCE_AREA_CHARTER.md`](canonicals/FINANCE_AREA_CHARTER.md) |
| FINOPS discipline | [`Governance/canonicals/FINOPS_DISCIPLINE.md`](Governance/canonicals/FINOPS_DISCIPLINE.md) |
| Counterparty maintenance SOP | [`Business Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md`](Business%20Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md) |

## Compliance SSOT (dual-plane)

Git-canonical FINOPS CSVs remain under
[`People/Compliance/canonicals/finops/`](../People/Compliance/canonicals/finops/)
per programme decision **D-IH-88-E**. Finance owns **doctrine**; Compliance CSVs +
Pydantic validators remain the register SSOT.

## Verification

```powershell
py scripts/validate_area_completeness.py --matrix
py scripts/validate_hlk.py
py scripts/validate_finops_ledger.py --self-test
```

Programme evidence:
[`docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-buildout-roadmap-2026-06-05.md`](../../../../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-buildout-roadmap-2026-06-05.md).
