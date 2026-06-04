---
title: Area Governance Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - CPO
  - PMO
last_review: 2026-06-04
last_review_by: Founder/CEO
last_review_at: 2026-06-04
last_review_decision_id: D-IH-93-B
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-B
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - ../Compliance/canonicals/PRECEDENCE.md
linked_cursor_rules:
  - .cursor/rules/akos-area-governance.mdc
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
  - .cursor/rules/akos-quality-fabric.mdc
linked_skills:
  - .cursor/skills/area-governance-craft/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
forward_charters:
  - process_list.csv row hol_peopl_dtp_area_governance_001
  - PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_area_buildout
  - paired runbook scripts/validate_area_completeness.py
  - .cursor/rules/akos-area-governance.mdc
  - .cursor/skills/area-governance-craft/SKILL.md
---

# Area Governance Discipline

> Seventeenth Quality Fabric specialty (I93 P0). People mints the
> **area-completeness shape** any O5-1 area inherits when created or
> matured. Codifies `compose_AREA(governance) → 14-component bar +
> conservative heuristic sweep + area score matrix`. Ratified under the
> area-governance meta-process decision (`D-IH-93-B` — the operator's
> instruction to make "create an area" a People-governed, countable
> process, 2026-06-04).

## 1. Purpose

Holistika areas (Data, Tech, Finance, Marketing, Operations, People,
Research) must be **governable at comparable depth** — not ad-hoc folder
trees with uneven process coverage. People is the discipline of
disciplines: People mints the **pattern** (`pattern_area_buildout`);
each area authors its own charter, roles, processes, and canonicals
inheriting the shape.

Without a countable bar, "harmonize area quality" stays prose. This
discipline makes it measurable: `py scripts/validate_area_completeness.py
--matrix` emits pass/partial/gap/skip/blocked per component per area.

DATA is the **first worked example** at I93 P1; P0 ships only the
meta-process (this canonical + SOP + validator).

## 2. The 14 components

| # | Component code | What it checks |
|:--|:---|:---|
| 1 | **AREA-01-PARENT-REDESIGN** | O5-1 area folder tree exists with role/sub-area structure |
| 2 | **AREA-02-AREA-CHARTER** | Area charter markdown (`*AREA*CHARTER*` or equivalent) |
| 3 | **AREA-03-DISCIPLINE-CHARTERS** | Discipline / governance canonicals under the area |
| 4 | **AREA-04-PROCESS-LIST** | `process_list.csv` rows for the area |
| 5 | **AREA-05-BASELINE-ROLES** | `baseline_organisation.csv` roles for the area |
| 6 | **AREA-06-CAPABILITY-CONFIDENCE** | `CAPABILITY_REGISTRY` + `CAPABILITY_CONFIDENCE_REGISTRY` rows |
| 7 | **AREA-07-CANONICAL-PRECEDENCE** | `CANONICAL_REGISTRY` + `PRECEDENCE.md` coverage |
| 8 | **AREA-08-DIMENSION-REGISTRIES** | Area-local dimension / adapter CSV registries |
| 9 | **AREA-09-PAIRED-SOP-RUNBOOK** | SOP + runbook pairing on area processes |
| 10 | **AREA-10-SUPABASE-MIRRORS** | Mirror parity (live evidence; conservative **skip** at P0) |
| 11 | **AREA-11-CURSOR-RULE-SKILL** | Area-scoped cursor rule + craft skill where applicable |
| 12 | **AREA-12-QUALITY-FABRIC** | Area disciplines cited in Quality Fabric §6 |
| 13 | **AREA-13-AREA-README** | Area root `README.md` index |
| 14 | **AREA-14-INHERITED-PATTERN** | `process_list.inherited_pattern_id` adoption |

Default scored areas: **Data, Tech, Finance, Marketing, Operations,
People, Research** (seven rows in the matrix).

## 3. The compose_AREA rule

```
compose_AREA(governance) -> 14-component sweep per area
  where:
    scored_areas = {Data, Tech, Finance, Marketing, Operations, People, Research}
    verdicts = {pass, partial, gap, blocked, skip}
    conservative_posture = emit skip when live evidence unavailable
    runbook = scripts/validate_area_completeness.py
    matrix_mode = --matrix  # operator-facing area score table
```

AREA governance depends **primarily on the governance axis** (charters,
CSV SSOT, process catalog, PRECEDENCE class). Audience is J-OP / J-AIC
(internal harmonization), not external delivery.

## 4. Cadence

- **on_demand** — operator or agent requests a baseline matrix.
- **area_buildout** — before closing an area charter / CSV tranche /
  cross-area breakthrough tranche (pairs with
  `SOP-PEOPLE_AREA_GOVERNANCE_001`).
- **pre_commit_self_test** — Pydantic + probe registry only (~2s).

Full heuristic sweep is **not** wired to every pre_commit (98 probes =
7 areas × 14 components). Self-test is the always-on circuit-breaker.

## 5. INFO → FAIL ramp (forward-charter)

P0 lands at **charter** with INFO posture (validator exits 0 unless
`--strict`). Promotion to FAIL requires:

1. DATA area scores at/above the bar on a full sweep (I93 P1+).
2. P8 harmonization sweep across all areas with operator sign-off.
3. Operator-explicit decision row ratifying FAIL promotion.

## 6. Cross-references

- Pattern: `pattern_area_buildout` in `PEOPLE_DESIGN_PATTERN_REGISTRY.csv`
- SOP: [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](SOP-PEOPLE_AREA_GOVERNANCE_001.md)
- Runbook: [`scripts/validate_area_completeness.py`](../../../../../../scripts/validate_area_completeness.py)
- Pydantic: [`akos/hlk_area_completeness.py`](../../../../../../akos/hlk_area_completeness.py)
- Initiative: [`docs/wip/planning/93-data-area-foundation-and-governance/`](../../../../../../wip/planning/93-data-area-foundation-and-governance/)
