---
name: Finance Ops Craft
description: >-
  Use when minting or maintaining FINOPS artefacts — counterparty register,
  rev-rec policy, pricing/tax registries, mirror spine evidence, monthly recon,
  or registered_fact entity gate. Codifies the HOW of FIN-01..05 and
  compose_FINOPS. Triggers on FINOPS, finops_counterparty, rev-rec,
  PRICING_TIER_REGISTRY, FINOPS_TAX_CALENDAR, validate_finops_ledger,
  finops_monthly_recon, FINANCE-AREA-FULL F3/F4. Pairs with
  .cursor/rules/akos-finance-ops.mdc (WHEN); this skill is HOW.
---

# Finance Ops Craft

## Principle 1 — Plane order

1. **Plane 1** counterparty register (live SSOT in Compliance `finops/`)
2. **Plane 2** rev-rec + pricing (Finance Governance dimensions)
3. **Plane 3** tax calendar (counsel-encoded)
4. **Planes 4–5** O2C / PTP (forward-chartered to F4)

Do not skip plane 1 FK checks when adding monetary bridges.

## Principle 2 — Tranche verification stack

```powershell
py scripts/validate_finops_ledger.py
py scripts/validate_pricing_tier_registry.py
py scripts/validate_finops_tax_calendar.py
py scripts/dataops_quality_check.py --data-fam FINOPS-SPINE
py scripts/validate_area_completeness.py --matrix
py scripts/validate_hlk.py
```

## Principle 3 — Mirror apply without inventing PASS

Repo-native FIN-02 (`FINOPS-SPINE` family) proves DDL + sync emit symbols.
Live mirror row-count parity requires operator SQL apply per
`akos-holistika-operations.mdc` — document evidence, do not fake AREA-10 PASS.

## Principle 4 — Entity gate SKIP is valid at F3

If `thi_finan_dtp_306` is not closed, document **SKIP** for first
`registered_fact` in the monthly recon report — not a programme failure until F4 M3.

## Principle 5 — M2 counterparty floor

`FINOPS_COUNTERPARTY_REGISTER.csv` row count must stay ≥
`FINOPS_M2_COUNTERPARTY_ROW_FLOOR` (25 at F3 documentation). Probe in
`finops_monthly_recon.py --report`.

## Anti-patterns

- Duplicating PMO `PRICING_MODEL.md` prose into Finance policy (cross-ref only).
- Minting tax deadlines without counsel source_ref.
- Committing Stripe charge amounts into git CSVs.

## Cross-references

- [`FINOPS_DISCIPLINE.md`](../../docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/FINOPS_DISCIPLINE.md)
- [`FINANCE_AREA_CHARTER.md`](../../docs/references/hlk/v3.0/Admin/O5-1/Finance/canonicals/FINANCE_AREA_CHARTER.md)
- [`scripts/finops_monthly_recon.py`](../../scripts/finops_monthly_recon.py)
