---
language: en
intellectual_kind: area-readme
area: "<Area>"
---

# <AREA> — area index

> Fill-in template for **AREA-13 (area README)** at L3. Place at the area root
> (`docs/references/hlk/v3.0/Admin/O5-1/<Area>/README.md`). Delete this quote block on use.

## What lives here

One-line orientation: what this area governs and who owns it (`<owner_role>`, kind `<kind>`,
entity `<entity>`).

## Map of the area

| Sub-folder (= role/sub_area) | What it holds |
|:---|:---|
| `<Sub>/canonicals/` | `<disciplines, registries>` |

## Key canonicals

- Charter: [`<AREA>_AREA_CHARTER.md`](...) (AREA-02)
- Discipline: [`<AREA>_DISCIPLINE.md`](...) (AREA-03)
- Dimension registries: `<...>` (AREA-08)

## Governance

- Maturity grid: `py scripts/validate_area_completeness.py --area <Area> --matrix`
- Worklist: `py scripts/validate_area_completeness.py --area <Area> --next`
- Discipline: [`AREA_GOVERNANCE_DISCIPLINE.md`](../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md)
