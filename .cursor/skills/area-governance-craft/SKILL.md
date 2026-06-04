---
name: Area Governance Craft
description: >-
  Use when chartering or maturing an O5-1 area, running the area-
  completeness matrix, or wiring I93 area-governance artefacts. Codifies
  the craft for the 14-component bar, conservative skip on mirrors,
  and pattern_area_buildout inheritance. Triggers on area governance,
  compose_AREA, validate_area_completeness.py, AREA-NN component,
  area score matrix, pattern_area_buildout, hol_peopl_dtp_area_governance_001.
  Pairs with .cursor/rules/akos-area-governance.mdc (WHEN); this skill is HOW.
---

# Area Governance Craft

## Why this skill exists

`akos-area-governance.mdc` and `AREA_GOVERNANCE_DISCIPLINE.md` say **when**
to score areas. This skill says **how** to read the matrix, fix gaps without
scope creep, and wire a new area process without breaking HLK CSV gates.

## Principle 1 — Matrix before CSV tranche

1. `py scripts/validate_area_completeness.py --matrix`
2. List non-pass rows for the target area only.
3. Inline-ratify each `gap` (fix-now / defer-OPS / accept-as-canon).
4. Re-run `--matrix` until the target area has no unexpected `gap` on
   components 1–9 and 13–14.

## Principle 2 — Do not fake AREA-10

At P0, `skip` on Supabase mirrors is correct. Promoting to `pass` requires
mirror SQL evidence per `akos-holistika-operations.mdc`, not folder heuristics.

## Principle 3 — Register the process row completely

When adding `hol_peopl_dtp_area_governance_001` or an area-local derivative:

- `inherited_pattern_id=pattern_area_buildout`
- Paired SOP path in the SOP column
- Runbook path in the automation column
- `event_triggered` cadence aligned with charter mint / CSV tranche

## Principle 4 — P0 vs P1 boundary

- **P0** ships People meta-process only (`AREA_GOVERNANCE_DISCIPLINE`, validator,
  pattern row). DATA may show `gap` on AREA-02 — expected until P1 charter.
- **P1** raises Data on AREA-02/03/13; do not fold Data charter into P0 commits.

## Anti-patterns

- Committing area CSV rows without reading `--matrix` output.
- Using `Marketing` in `process_list` instead of `MKT`.
- Inventing governance decision IDs: only reference decisions already
  ratified in `DECISION_REGISTER.csv`; never mint a new `D-IH-*` row to
  satisfy a phase note.

## Cross-references

- [`AREA_GOVERNANCE_DISCIPLINE.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md)
- [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md)
- [`scripts/validate_area_completeness.py`](../../scripts/validate_area_completeness.py)
- [`akos/hlk_area_completeness.py`](../../akos/hlk_area_completeness.py)
