---
authored: 2026-06-10
tranche: I95-T2
parent_initiative: INIT-OPENCLAW_AKOS-95
wave: N
---

# I95 Tranche 2 session doctrine (INDEX_INTEGRITY Wave N)

Binding rule/skill card for this execution session. Refer back at each major action.

| When I touch… | Load… | One-line when |
|:---|:---|:---|
| Baseline index documents (README, PRECEDENCE, CHANGELOG, INITIATIVE_DEPENDENCIES, USER_GUIDE, ARCHITECTURE, QF §6) | [`akos-index-integrity.mdc`](../../../../.cursor/rules/akos-index-integrity.mdc) + [`index-integrity-craft/SKILL.md`](../../../../.cursor/skills/index-integrity-craft/SKILL.md) | Any wave-close or canonical-CSV mint triggers 8-dimension sweep before UAT verdict |
| Planning README / INITIATIVE_DEPENDENCIES / cluster map | [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) | Initiative index + dependency narrative must match INITIATIVE_REGISTRY SSOT |
| P0 evidence before edits | [`akos-applied-research-discipline.mdc`](../../../../.cursor/rules/akos-applied-research-discipline.mdc) + [`applied-research-craft/SKILL.md`](../../../../.cursor/skills/applied-research-craft/SKILL.md) | Internal sweep mandatory; external only if novel framing |
| Wave N scope authority | [`i86_cluster_end-to-end_+_index_integrity_525c25e6.plan.md`](file:///c:/Users/Shadow/.cursor/plans/i86_cluster_end-to-end_+_index_integrity_525c25e6.plan.md) | N.3–N.4 deliverables: INDEX_INTEGRITY already minted; backfill indexes |
| I95 cluster edges (interim until deps refresh) | [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) | I90–I95 dependency prose source until INITIATIVE_DEPENDENCIES updated |
| I86 cluster INDEX_INTEGRITY references | [`86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md`](../../86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md) | Wave N burndown rank 1 exit gate |
| Doctrine SSOT for index discipline | [`INDEX_INTEGRITY_DISCIPLINE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md) | 8 probes IDX-01..08 + 5-option disposition enum |
| Mechanical sweep + validator | [`scripts/baseline_index_sweep.py`](../../../../scripts/baseline_index_sweep.py) + [`scripts/validate_index_freshness.py`](../../../../scripts/validate_index_freshness.py) | Run before commit; cite sweep report in evidence |

## Tranche 2 action checklist (Wave N full)

1. P0 research mint (`i95-p0-research-index-integrity-wave-n-2026-06-10.md`) — **before** doc edits
2. Run `baseline_index_sweep.py` — disposition findings (5-option enum; no AskQuestion unless fork)
3. Fix planning README drift (I78/I85/I87 closed; I90–I95 present)
4. Refresh `INITIATIVE_DEPENDENCIES.md` with I90–I95 edges + bump `last_generated`
5. Remediate sweep gaps: PRECEDENCE (IDX-02), ARCHITECTURE (IDX-06), QF §6 (IDX-08)
6. Update cluster map burndown rank 1 → DONE; PMO sweep §7; `files-modified.csv`
7. Validators: `validate_index_freshness.py`, `validate_hlk.py`, `verify.py pre_commit_fast`
8. Single phase commit per operator gate

## Gates honored

- No `process_list.csv` / `baseline_organisation.csv` edits
- No INITIATIVE_REGISTRY CSV edits (registry already truth; README/deps narrative sync only)
- AskQuestion skipped — no genuine fork (deterministic-fix-now for IDX gaps)
