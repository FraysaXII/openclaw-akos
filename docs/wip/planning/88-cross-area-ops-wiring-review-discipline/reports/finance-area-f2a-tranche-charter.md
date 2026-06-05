---
tranche_id: FINANCE-F2A-2026-06-05
tranche_class: canonical_csv_mint
tranche_title: Finance F2a — rev-rec policy, pricing registry, DC seeds, CONF rows
audiences_named: [J-OP, J-AIC]
channels_named: [CHAN-VAULT-CANONICAL]
scenarios_named: [business_controller_mints_plane_2_ssot_before_first_sale]
brand_register: internal-corpint
ratifying_decisions: [D-IH-88-E, D-IH-81-N]
is_atomic_commit: true
reversibility_class: medium
reversibility_rationale: New Finance dimension CSV + DATA_CONTRACT_REGISTRY rows + CONF seeds revert via git revert; validators wire into validate_hlk.py compounds if left partial.
closing_loop_test: synthesis PASS + validate_pricing_tier_registry.py --self-test PASS + validate_data_contract_registry.py PASS + validate_hlk.py PASS + Finance matrix >=77%.
recipient_fallback_channel: n/a
operator_framing_quote: F2 parallel tranches — F2a rev-rec/pricing first per operator 2026-06-05.
operator_gate: PRICING_TIER_REGISTRY.csv + CAPABILITY_CONFIDENCE_REGISTRY Finance CONF tranche + DATA_CONTRACT_REGISTRY DC-FINOPS rows
---

# F2a tranche charter

## In

- `Finance/Business Controller/canonicals/FINOPS_REVENUE_RECOGNITION_POLICY.md`
- `Finance/Governance/canonicals/dimensions/PRICING_TIER_REGISTRY.csv` + validator fleet
- 5 `DATA_CONTRACT_REGISTRY` rows (DC-FINOPS-* family)
- 16 `CAPABILITY_CONFIDENCE_REGISTRY` CONF rows (Finance CAP-*)
- `runbook_path` pilot on `thi_finan_dtp_303`

## Out

- Tax calendar (F2b)
- METRICS_REGISTRY bulk (F2a may add ≤3 seed metrics only if zero extra CSV gate)
- Mirror apply (F3)
