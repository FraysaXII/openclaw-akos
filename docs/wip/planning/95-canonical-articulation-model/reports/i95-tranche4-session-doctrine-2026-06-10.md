---
authored: 2026-06-10
tranche: I95-T4
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L3-Bundle-C
---

# I95 Tranche 4 session doctrine (L3 Bundle C)

Binding rule/skill card for this execution session. Refer back at each major action.

| When I touch… | Load… | One-line when |
|:---|:---|:---|
| L3 Bundle C charter | [`i95-l3-parallel-bundles-charter-2026-06-09.md`](i95-l3-parallel-bundles-charter-2026-06-09.md) | TRP-030/036 FK gate + Semantic Council posture |
| Prior ratification | [`l3-trp-030-036-ratification-2026-06-09.md`](l3-trp-030-036-ratification-2026-06-09.md) | Conservative deferral precedent |
| Cluster burndown rank 3 | [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) | Exit: Bundle C disposition logged |
| P0 evidence before edits | [`akos-applied-research-discipline.mdc`](../../../../.cursor/rules/akos-applied-research-discipline.mdc) + [`applied-research-craft/SKILL.md`](../../../../.cursor/skills/applied-research-craft/SKILL.md) | Internal sweep mandatory; external only if novel |
| Operator gate (FK missing) | [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) + [`inline-ratify-craft/SKILL.md`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) | Pre-digest options; promote columns vs defer |
| FK bindings SSOT | [`akos/hlk_canonical_articulation.py`](../../../../akos/hlk_canonical_articulation.py) `L3_FK_BINDINGS` | 44 tuples post tranche-5; no Bundle C bindings without FK |
| Planning traceability | [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) | `files-modified.csv` + PMO sweep on touch |

## Tranche 4 action checklist

1. P0 research mint (`i95-p0-research-l3-bundle-c-2026-06-10.md`) — **before** disposition
2. Re-verify FK columns on `AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` + `INITIATIVE_REGISTRY.csv`
3. If FK absent: charter-only disposition + inline-ratify evidence packet (promote vs defer)
4. If FK present + operator gate clear: mint `L3_TRANCHE4C_FK_BINDINGS` per tranche-5 pattern
5. Update cluster map rank 3 → DONE; PMO sweep §7; `files-modified.csv`
6. Validators: `validate_fk_verb_coverage.py`, `validate_canonical_articulation.py`, `verify.py pre_commit_fast`
7. Single commit: `docs(i95): tranche-4 L3 Bundle C — TRP-030/036 disposition`

## Gates honored

- No `process_list.csv` / `baseline_organisation.csv` edits
- No `INITIATIVE_REGISTRY.csv` column mint (canonical-CSV gate deferred)
- No dishonest `planned` → `active` promotion without populated FK
- **Next tranche (do not start):** L1 EG-3 → OPS-95-2 → full PMO sweep
