---
title: "<AREA> Area Charter"
language: en
intellectual_kind: area-charter
area: "<Area>"
area_kind: "<stream_aligned | platform | capability_meta | delivery_capacity>"
entity: "<Holistika | Think Big | HLK Tech Lab>"
owner_role: "<C-level role from baseline_organisation.csv>"
access_level: 4
status: charter
register: internal
ratifying_decisions:
  - "<D-IH-NN-X>"
last_review: "<YYYY-MM-DD>"
last_review_by: "<owner_role>"
methodology_version_at_review: v3.1
---

# <AREA> Area Charter

> Fill-in template for **AREA-02 (area charter)** at L3 per `AREA_GOVERNANCE_DISCIPLINE.md` v2.
> Delete this quote block on use. Run `py scripts/validate_area_completeness.py --area <Area>
> --next` to see what else the area needs.

## 1. What this area is (bounded-context definition)

One paragraph: the **internally consistent model + language** this area owns, the **value stream**
it serves, the **APQC function** it maps to, and why its boundary is where it is. (Per discipline §2.)

## 2. Kind + entity + owner

| Field | Value |
|:---|:---|
| Kind | `<stream_aligned / platform / capability_meta / delivery_capacity>` |
| Entity | `<Holistika / Think Big / HLK Tech Lab>` |
| Owner role | `<role>` (from `baseline_organisation.csv`) |
| Tier bar | `<full bar / full + SLO / full + pattern-adoption / PMBOK-domain bar>` |

## 3. Sub-areas (file-plan: sub-folder = role/sub_area)

List the area's sub-areas, each FK to a `baseline_organisation` `sub_area`/`role_name`
(this is **AREA-16**). Every sub-folder under the area root maps to one of these.

| Sub-area folder | Role(s) | Owns |
|:---|:---|:---|
| `<Sub>` | `<role>` | `<what>` |

## 4. The contract this area exposes (AREA-15 outcome)

What consumable contract / SLO does this area ship to other areas? (≥1 row in
`DATA_CONTRACT_REGISTRY.csv` with this area as producer/consumer.)

## 5. Disciplines + processes

- Discipline canonical(s): `<AREA>_DISCIPLINE.md` (AREA-03).
- `process_list.csv` rows with `inherited_pattern_id` (AREA-04 + AREA-14).
- Paired SOP + runbook per process (AREA-09; enhancing — retrofit per wave).

## 6. Cross-references

- Discipline: [`AREA_GOVERNANCE_DISCIPLINE.md`](../AREA_GOVERNANCE_DISCIPLINE.md)
- SOP: [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](../SOP-PEOPLE_AREA_GOVERNANCE_001.md)
- Scorer: `py scripts/validate_area_completeness.py --area <Area> --next`
