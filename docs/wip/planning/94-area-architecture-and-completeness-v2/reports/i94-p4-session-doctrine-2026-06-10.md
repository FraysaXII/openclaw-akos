---
authored: 2026-06-10
tranche: I94-P4-ops-handoffs
parent_initiative: INIT-OPENCLAW_AKOS-94
upstream_ssot: i94-operations-master-sweep-design-2026-06-10.md
status: completed
ratifying_decisions:
  - D-IH-94-A
operator_ratification:
  batch: batch2_2026-06-10
  posture: PWF_on_AREA09_not_blocking_P6
  scope: P4_plus_P7_combined_wave
  dual_track: A/A/A/A
---

# I94 P4 Operations sweep — cross-area handoffs session doctrine (2026-06-10)

Binding rule/skill card for P4 execution (handoffs canonical + design-wave closure).

| When I touch… | Load… | One-line when |
|:---|:---|:---|
| Master sweep design | [`i94-operations-master-sweep-design-2026-06-10.md`](i94-operations-master-sweep-design-2026-06-10.md) | P4–P8 phased plan + operator ratification batch2 |
| Cross-area map | [`i94-operations-cross-area-execution-map-2026-06-10.md`](i94-operations-cross-area-execution-map-2026-06-10.md) | Handoff class taxonomy (OPS-LOCAL-DO / TRIG-*) |
| Execution spec | [`i94-operations-p4-p6-execution-spec-2026-06-10.md`](i94-operations-p4-p6-execution-spec-2026-06-10.md) | Composer packet boundaries P4–P6 |
| Handoffs SSOT | [`OPERATIONS_CROSS_AREA_HANDOFFS.md`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md) | Trigger → owner → script → evidence |
| Operations delivery | [`akos-operations-delivery.mdc`](../../../../.cursor/rules/akos-operations-delivery.mdc) + [`operations-delivery-craft/SKILL.md`](../../../../.cursor/skills/operations-delivery-craft/SKILL.md) | DO vs REGISTER; automation-first order |
| P4 wave research | [`i94-operations-p4-wave2-research-synthesis-2026-06-10.md`](i94-operations-p4-wave2-research-synthesis-2026-06-10.md) | 428-source ledger; PWF posture on AREA-09 |
| Research charter | [`holistic-agentic-capability-orchestration-2026-06-10/RESEARCH_CHARTER_AND_EXECUTION_PLAN.md`](../../../../intelligence/holistic-agentic-capability-orchestration-2026-06-10/RESEARCH_CHARTER_AND_EXECUTION_PLAN.md) | IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001 |

## P4 deliverables (completed)

1. **Cross-area handoffs canonical** — `OPERATIONS_CROSS_AREA_HANDOFFS.md` (register-only; six handoff classes; Data / People / Finance / Tech / Research trigger tables)
2. **README + PRECEDENCE + delivery doctrine wiring** — `Operations/README.md`, `PRECEDENCE.md` row, `OPERATIONS_DELIVERY_DISCIPLINE.md` §handoffs cross-link
3. **Design wave reports** — master sweep design, cross-area execution map, P4 wave-2 source ledger (428 rows), P4 wave-2 research synthesis
4. **Research charter path** — holistic agentic capability orchestration charter + `INTELLIGENCEOPS_REGISTER.csv` append (`IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001`)
5. **Ledger bootstrap runbook** — `scripts/i94_p4_ops_research_ledger_bootstrap.py`
6. Validators: `validate_hlk.py`, `validate_area_completeness.py`, `validate_research_action.py` (P4 ledger)

## Gates honored

- Operator-ratified **batch2** — three tranche classes in one wave (P4 handoffs + P7 AREA-09 T2 + design artifacts); **PWF posture** on AREA-09 (32/53 paired acceptable for P6 UAT; not blocked on 53/53)
- **Dual-track A/A/A/A** — automation depth + cross-area map + solo-operator spine + AREA-09 tranche sequencing per master sweep design
- No mirror DDL; no IntelligenceOps file moves in P4
- SOP-META order for P7 TBI RevOps SOPs landed **before** CSV tranche (Option A)

## Evidence

```powershell
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --area Operations --next
py scripts/validate_area_completeness.py --area Operations --matrix
```

**`validate_hlk.py` (key lines):**

```
OVERALL: PASS
MIRROR_EMIT_CONTRACT: PASS
MASTER_ROADMAP_FRONTMATTER: PASS
LANGUAGE_FRONTMATTER: PASS
```

**`validate_area_completeness.py --area Operations --matrix` (key lines):**

```
Operations | delivery_capacity | 13 | 2 | 0 | 1 | 93% | 10/10 | COMPLETE
Operations AREA-09-PAIRED-SOP-RUNBOOK partial (medium): paired processes=32/53
Operations AREA-12-QUALITY-FABRIC partial (low): area disciplines=1 not all cited in §6 table
```

**`validate_area_completeness.py --area Operations --next`:** empty worklist (critical tier closed; AREA-09 enhancing partial is forward debt per PWF posture).

## Next tranche

- **P5** — I88 wiring (solo-operator daily spine scripts + master-roadmap cross-links)
- **P6** — Closure UAT **PASS-WITH-FOLLOWUP** on AREA-09 pairing cliff (target documented in master sweep design; not 53/53 gate)
