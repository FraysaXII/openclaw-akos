---
tranche_id: FINANCE-F3-2026-06-05
tranche_class: internal_governance
tranche_title: Finance F3 — tech plane, FINOPS cursor rule, recon, mirror evidence
audiences_named: [J-OP, J-AIC]
channels_named: [CHAN-VAULT-CANONICAL]
scenarios_named: [finance_area_wires_finops_spine_before_closure_uat]
brand_register: internal-corpint
ratifying_decisions: [D-IH-88-E, D-IH-81-P]
is_atomic_commit: true
reversibility_class: low
reversibility_rationale: Cursor rule + skill + dataops family + recon runbook are additive; AREA-10 Finance moves from skip to partial.
closing_loop_test: synthesis PASS + dataops FINOPS-SPINE clean + finops_monthly_recon --self-test PASS + Finance matrix >=88%.
recipient_fallback_channel: n/a
operator_framing_quote: Continue F3 after F2 — wire FINOPS spine probes and finance cursor rule; push deferred.
operator_gate: none (no canonical CSV gate)
---

# F3 tranche charter

## In

- `.cursor/rules/akos-finance-ops.mdc` + `.cursor/skills/finance-ops-craft/SKILL.md`
- `dataops_quality_check.py --data-fam FINOPS-SPINE`
- `scripts/finops_monthly_recon.py` + first `finops-recon-2026-06.md`
- Finance AREA-10 partial probe + M2 threshold in charter
- Rule router row

## Out

- Live Supabase mirror apply (operator SQL gate — documented only)
- First live `registered_fact` row (entity gate SKIP)
- F4 closure UAT
