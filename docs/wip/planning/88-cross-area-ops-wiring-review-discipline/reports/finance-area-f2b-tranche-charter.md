---
tranche_id: FINANCE-F2B-2026-06-05
tranche_class: canonical_csv_mint
tranche_title: Finance F2b — Spain tax filing calendar (counsel-encoded obligations)
audiences_named: [J-OP, J-AIC]
channels_named: [CHAN-VAULT-CANONICAL]
scenarios_named: [business_controller_mints_tax_calendar_before_incorporation_filing_cycle]
brand_register: internal-corpint
ratifying_decisions: [D-IH-88-E, D-IH-81-N, D-IH-81-P]
is_atomic_commit: true
reversibility_class: medium
reversibility_rationale: Tax calendar CSV + validator wire revert via git revert; obligation rows use cadence rules not production amounts; entity-specific due dates remain counsel/AT-Pymes confirmed.
closing_loop_test: synthesis PASS + validate_finops_tax_calendar.py PASS + validate_hlk.py PASS + Finance matrix >=88% (no regression).
recipient_fallback_channel: n/a
operator_framing_quote: Continue F2b after F2a — scaffold Spain filing obligations per OPS-81-13; AT-Pymes executes Layer A per D-IH-81-P.
operator_gate: FINOPS_TAX_CALENDAR.csv obligation row set (8 rows; next_due_at empty until entity live)
---

# F2b tranche charter

## In

- `Finance/Governance/canonicals/dimensions/FINOPS_TAX_CALENDAR.csv` + Pydantic + validator
- `CANONICAL_REGISTRY` row
- `validate_hlk.py` wire
- FINOPS discipline plane 3 pointer update

## Out

- `FINOPS_TAX_STRATEGY_DOCTRINE.md` full mint (OPS-81-20 deferred)
- Hacienda Foral territoriality doctrine (OPS-81-14)
- ENISA filing row (OPS-81-16; gated Q-CRT-001)
- Mirror apply (F3)
