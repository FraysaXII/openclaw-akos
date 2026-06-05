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

# Area Governance Craft (v2)

## Why this skill exists

`akos-area-governance.mdc` + `AREA_GOVERNANCE_DISCIPLINE.md` v2 say **when** to score areas.
This skill says **how** to run the **2-D maturity model** (D-IH-94-A) so it's activatable by
humans AND AICs: read the grid, work the action worklist, raise components to level without
scope creep.

## Principle 1 — Worklist over matrix (the activation lever)

The matrix diagnoses; the **worklist acts**. To mature an area:

1. `py scripts/validate_area_completeness.py --area <Area> --next` — ranked next-actions
   (critical-first) with current→target level, owner role, and the exact next action.
2. Work it **top-down**: critical components to **L3** first; the worklist's `next_action`
   tells you the move (often "fill a template" or "git mv a drifted file").
3. Re-run `--next` until `crit@L3` = N/N → `--matrix` shows tier **COMPLETE**.
4. Disposition residual **enhancing** findings via inline-ratify (defer-OPS / accept-as-canon).

The **closure gate is `crit@L3` tier COMPLETE**, not the `%` score. The `%` is a maturity badge.

## Principle 2 — Critical-must-pass; enhancing is weighted (don't over-gate)

- **Critical** (must reach L3): AREA-01/02/03/04/05/06/07/08/14/15.
- **Enhancing** (weighted badge, never blocks): AREA-09/10/11/12/13/16.
- **AREA-09 (paired SOP+runbook) is enhancing** — the pairing cliff is forward debt that was
  `partial` for every area in v1; gating closure on it wrongly breaks Data/Finance (I94 P1
  calibration finding). Track it; do not block on it.

## Principle 3 — Declare kind + entity; respect placement + file-plan

- Every area declares **kind** (stream_aligned / platform / capability_meta / delivery_capacity)
  + **entity** (Holistika / Think Big / HLK Tech Lab) in `AREA_KIND_ENTITY` (AREA-14).
- **AREA-15 placement-integrity**: an area-operational discipline (MKTOPS / TECHOPS / DATAOPS /
  UX) belongs in its consuming area, not parked in People. If `--next` flags drift, `git mv` it.
- **AREA-16 file-plan**: sub-folder names FK to `baseline_organisation` role/`sub_area`.
- Use the templates: `_templates/AREA_CHARTER_TEMPLATE.md` (AREA-02), `AREA_README_TEMPLATE.md`
  (AREA-13) — "raise to L3" is a fill-in, not an invention.

## Principle 4 — Do not fake evidence; register the process completely

- `AREA-10` mirrors: emit `skip`/L0 without live SQL evidence (per `akos-holistika-operations.mdc`).
- New area processes: `inherited_pattern_id=pattern_area_buildout` + paired SOP + runbook +
  `event_triggered` cadence.
- Marketing uses area code `MKT` in `process_list`, not `Marketing`.

## Anti-patterns

- **Scoring without the worklist** — committing area changes off the matrix alone (no action list).
- **Over-gating on AREA-09** — treating the pairing cliff as a closure blocker.
- **Inventing levels** — emit L0 when evidence is absent; the heuristic must stay deterministic.
- **Inventing decision IDs** — only reference `D-IH-*` rows already in `DECISION_REGISTER.csv`.
- **Parking area-ops disciplines in People** — that is the AREA-15 drift the v2 model exists to catch.

## Cross-references

- [`AREA_GOVERNANCE_DISCIPLINE.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md)
- [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md)
- [`scripts/validate_area_completeness.py`](../../scripts/validate_area_completeness.py)
- [`akos/hlk_area_completeness.py`](../../akos/hlk_area_completeness.py)
