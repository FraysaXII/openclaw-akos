---
title: SOP — People Area Governance (area buildout meta-process)
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_AREA_GOVERNANCE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - CPO
co_authors:
  - PMO
  - Compliance Officer
last_review: 2026-06-05
last_review_by: CPO
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-B
  - D-IH-94-A
status: charter
register: internal
doctrine_version: v2
linked_canonicals:
  - AREA_GOVERNANCE_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - _templates/AREA_CHARTER_TEMPLATE.md
  - _templates/AREA_README_TEMPLATE.md
linked_runbooks:
  - scripts/validate_area_completeness.py
linked_processes:
  - hol_peopl_dtp_area_governance_001
cadence: event_triggered
cadence_trigger: area charter mint OR area CSV tranche OR wave-close sweep OR harmonization sweep
---

# SOP — People Area Governance (area buildout meta-process) — v2

> **v2 (I94 / `D-IH-94-A`):** the bar is now the **16-component × L0–L5 maturity grid** over
> **8 areas** (Legal added). "Complete for tier" = all **critical** components at **L3**
> (Defined). The scorer is **action-emitting** (`--next`) so a human OR an AIC can execute the
> worklist directly. v1 (14-component flat checklist; `D-IH-93-B`) is superseded.

## Purpose

Operationalise [`AREA_GOVERNANCE_DISCIPLINE.md`](AREA_GOVERNANCE_DISCIPLINE.md) v2:
how People governs **creating or maturing** an O5-1 area using the 16-component maturity grid.
Owner **CPO**; co-owners **PMO** (chartering) + **Compliance** (CSV SSOT) + the area's own
role-owner (per `AREA_KIND_ENTITY`).

Paired runbook: [`scripts/validate_area_completeness.py`](../../../../../../scripts/validate_area_completeness.py).

## Scope

In scope:

- Chartering a new area or maturing an existing area under
  `docs/references/hlk/v3.0/Admin/O5-1/<Area>/`.
- CSV tranches (`process_list`, `baseline_organisation`, dimension
  registries) that belong to the area buildout.
- Baseline matrix before P8 harmonization close.

Out of scope:

- Authoring another area's domain canonicals — each area authors its own
  charter, processes, and registries; People owns only the meta-process
  (the discipline-of-disciplines rule, `akos-people-discipline-of-disciplines.mdc`
  RULE 1).
- Minting new governance decision rows — this SOP only references
  decisions already ratified in `DECISION_REGISTER.csv`.

## Steps (AC-HUMAN)

1. **Declare the area's kind + entity** (stream_aligned / platform / capability_meta /
   delivery_capacity; Holistika / Think Big / HLK Tech Lab) per discipline §2 + `AREA_KIND_ENTITY`.
2. **Get the worklist**: `py scripts/validate_area_completeness.py --area <Area> --next`.
   It prints the ranked next-actions (critical-first) with current→target level + owner + the
   exact next action. This is the do-this-next list — no manual checklist re-derivation needed.
3. **Raise critical components to L3** first, using the templates where they apply
   (`_templates/AREA_CHARTER_TEMPLATE.md` for AREA-02; `_templates/AREA_README_TEMPLATE.md` for
   AREA-13; sub-folder = role name for AREA-16).
4. **Re-run** `--area <Area> --next` until `crit@L3` = N/N (tier = COMPLETE on `--matrix`).
5. **Disposition** any remaining enhancing findings via inline-ratify (defer-OPS / accept-as-canon).
6. **File** the area score row + worklist delta in the initiative report before the commit.

## Acceptance criteria

### AC-HUMAN

The area's role-owner (or CPO/PMO) can take an area from current to **COMPLETE for tier** by
reading this SOP + running `--area <Area> --next` and working the emitted list top-down — without
re-deriving the bar. Critical-at-L3 is the gate; enhancing items are weighted, not blocking.

### AC-AUTOMATION

`py scripts/validate_area_completeness.py --self-test` exits 0 at pre_commit (chassis check);
`--matrix` emits the 8-area × 16-component grid with the `crit@L3` tier verdict; `--area <Area>
--next` emits the action worklist. The runbook is SSOT-equivalent to this SOP — neither supersedes
the other (per `akos-executable-process-catalog.mdc` RULE 1).

## Cross-references

- Process: `hol_peopl_dtp_area_governance_001` in `process_list.csv`
- Pattern: `pattern_area_buildout`
- Templates: [`_templates/AREA_CHARTER_TEMPLATE.md`](_templates/AREA_CHARTER_TEMPLATE.md), [`_templates/AREA_README_TEMPLATE.md`](_templates/AREA_README_TEMPLATE.md)
- Skill: [`area-governance-craft`](../../../../../../.cursor/skills/area-governance-craft/SKILL.md) (the HOW for AICs)
- [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 1
