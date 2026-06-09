---
authored: 2026-06-10
tranche: I94-P3-ops-sweep
parent_initiative: INIT-OPENCLAW_AKOS-94
upstream_ssot: i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md
status: completed
---

# I94 P3 Operations sweep — session doctrine (2026-06-10)

Binding rule/skill card for P3 execution (AREA-09 tranche + placement).

| When I touch… | Load… | One-line when |
|:---|:---|:---|
| Upstream SSOT | [`i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md`](i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md) | All packets cite thinking-seat c4097ca4 |
| Charter | [`i94-operations-operational-sweep-charter-2026-06-10.md`](i94-operations-operational-sweep-charter-2026-06-10.md) | P0–P6 phased execution |
| AREA-09 tranche evidence | [`i94-p3-area09-process-list-tranche-2026-06-10.md`](i94-p3-area09-process-list-tranche-2026-06-10.md) | process_list pairing |
| P3 placement research | [`i94-p0-research-p3-placement-2026-06-10.md`](i94-p0-research-p3-placement-2026-06-10.md) | File-move + FK rationale |
| I95 L6 tracker | [`i95-operations-pmo-business-strategy-placement-tracker.md`](../../_trackers/i95-operations-pmo-business-strategy-placement-tracker.md) | business-strategy deferral |
| Operations delivery | [`akos-operations-delivery.mdc`](../../../../.cursor/rules/akos-operations-delivery.mdc) + [`operations-delivery-craft/SKILL.md`](../../../../.cursor/skills/operations-delivery-craft/SKILL.md) | P1 doctrine + P2/P3 execution |
| Operator ratification | AskQuestion **Both** — AREA-09 CSV + P3 placement same wave | 2026-06-10 |

## P3 deliverables (completed)

1. **AREA-09 tranche** — `sop_path`/`runbook_path` columns + 12 Operations pairings (7 new rows + 5 updates)
2. **IntelligenceOps eviction** — `git mv` 2 SOPs → `Research/Intelligence/canonicals/`; process_list paths fixed
3. **Engagement AREA-16 FK** — PMO `sub_area=Engagement` in `baseline_organisation.csv`
4. **I95 L6 forward-charter** — business-strategy placement tracker (no mass moves)
5. Validators: `validate_hlk.py`, `validate_area_completeness.py`, `pre_commit_fast`

## Gates honored

- Operator-ratified `process_list.csv` + `baseline_organisation.csv` edits
- No mirror DDL
- Documented file moves; PRECEDENCE cross-link updated

## Next tranche

**P4** — Cross-area handoffs (People methodology consolidation slice per charter).
