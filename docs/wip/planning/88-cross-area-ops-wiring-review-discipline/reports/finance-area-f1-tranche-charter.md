---
tranche_id: FINANCE-F1-2026-06-05
tranche_class: internal_governance
tranche_title: Finance F1 — area shell (charter, FINOPS discipline, pattern_area_buildout)
initiative: INIT-OPENCLAW_AKOS-88
program: FINANCE-AREA-FULL
phase: F1
authored: 2026-06-05
author_seat: thinking
executor_packet: finance-area-executor-packet-f1-2026-06-05.md
audiences_named:
  - J-OP
  - J-AIC
channels_named:
  - CHAN-VAULT-CANONICAL
scenarios_named:
  - cfo_and_business_controller_mint_finance_area_charter_and_finops_discipline_before_csv_tranche
brand_register: internal-corpint
ratifying_decisions:
  - D-IH-88-A
  - D-IH-93-B
is_atomic_commit: true
reversibility_class: low
reversibility_rationale: New Finance markdown tree + two CANONICAL_REGISTRY rows + process_list pattern columns revert via single git revert; no DDL or mirror apply; Compliance finops CSVs untouched.
closing_loop_test: py scripts/synthesis_before_tranche_check.py --check-charter reports/finance-area-f1-tranche-charter.md PASS + py scripts/validate_area_completeness.py --matrix (Finance ≥65%, AREA-02/03/13 gaps cleared) + py scripts/validate_hlk.py OVERALL PASS.
recipient_fallback_channel: n/a — internal governance tranche; no external recipient.
operator_framing_quote: go all out with the F1 executor packet and make the workflow a practice — 2026-06-05.
operator_gate: process_list.csv + CANONICAL_REGISTRY.csv (canonical-CSV tranche)
---

# F1 tranche charter — Finance area shell (internal_governance)

## Scope (in)

- Vault tree: `Finance/README.md`, `Finance/Governance/canonicals/FINOPS_DISCIPLINE.md`, `Finance/canonicals/FINANCE_AREA_CHARTER.md`
- `process_list.csv`: +1 row `hol_finan_dtp_area_buildout_001`; `inherited_pattern_id=pattern_area_buildout` on Finance umbrella `item_id`s
- `CANONICAL_REGISTRY.csv`: +2 rows (`finance_area_charter`, `finops_discipline`)
- `HOLISTIKA_QUALITY_FABRIC.md` §6: +1 row (`compose_FINOPS`, status `charter`)
- Planning cross-refs only (roadmap, executor packet, workflow doc)

## Scope (out)

- No `PRICING_TIER_REGISTRY`, `FINOPS_TAX_CALENDAR`, rev-rec policy (F2)
- No `DATA_CONTRACT_REGISTRY` rows (F2)
- No `CAPABILITY_CONFIDENCE_REGISTRY` CONF seeds (F2)
- No Supabase mirror apply / `registered_fact` (F3)
- No `akos-finance-ops.mdc` / skill (F3)
- No `SOP-FINANCE_AREA_BUILDOUT_001` (F2 or F4 — optional)
- No I88 P3 canonical (`CROSS_AREA_OPS_WIRING_DISCIPLINE`) — blocked on F4

## Evidence inputs (Composer reads only these)

| Artifact | Path |
|:---|:---|
| Executor packet (binding spec) | [`finance-area-executor-packet-f1-2026-06-05.md`](finance-area-executor-packet-f1-2026-06-05.md) |
| Research master synthesis | [`research-finance-full-governed-area-2026-06-05/master-synthesis.md`](research-finance-full-governed-area-2026-06-05/master-synthesis.md) |
| DATA worked example | `docs/references/hlk/v3.0/Admin/O5-1/Data/canonicals/DATA_AREA_CHARTER.md` |
| DATAOps discipline shape | `docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md` |
| People area meta-process | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md` |

## Synthesis gate (run before Composer dispatch)

```powershell
py scripts/synthesis_before_tranche_check.py --check-charter docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-f1-tranche-charter.md
```

Expected: PASS on internal_governance fire-set (5 baseline dimensions).

## Operator gate checklist

- [ ] F0 assumptions accepted (see executor packet §0) OR explicit inline ratification in chat
- [ ] Approve `process_list.csv` + `CANONICAL_REGISTRY.csv` edit in this tranche
- [ ] Composer seat pinned to **composer-2.5** (Holistika — Execute mode)
