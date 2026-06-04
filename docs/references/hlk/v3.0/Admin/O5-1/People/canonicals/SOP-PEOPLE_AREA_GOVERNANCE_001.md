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
last_review: 2026-06-04
last_review_by: CPO
last_review_decision_id: D-IH-93-B
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-B
status: charter
register: internal
linked_canonicals:
  - AREA_GOVERNANCE_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
linked_runbooks:
  - scripts/validate_area_completeness.py
linked_processes:
  - hol_peopl_dtp_area_governance_001
cadence: event_triggered
cadence_trigger: area charter mint OR area CSV tranche OR harmonization sweep
---

# SOP — People Area Governance (area buildout meta-process)

## Purpose

Operationalise [`AREA_GOVERNANCE_DISCIPLINE.md`](AREA_GOVERNANCE_DISCIPLINE.md):
how People governs **creating or maturing** an O5-1 area using the
14-component bar. Owner **CPO**; co-owners **PMO** (chartering) +
**Compliance** (CSV SSOT).

Paired runbook: [`scripts/validate_area_completeness.py`](../../../../../../scripts/validate_area_completeness.py).

## Scope

In scope:

- Chartering a new area or maturing an existing area under
  `docs/references/hlk/v3.0/Admin/O5-1/<Area>/`.
- CSV tranches (`process_list`, `baseline_organisation`, dimension
  registries) that belong to the area buildout.
- Baseline matrix before P8 harmonization close.

Out of scope at P0:

- DATA area charter relocation (I93 P1).
- Minting `D-IH-93-BI` or other initiative decision rows beyond
  `D-IH-93-B`.

## Steps (AC-HUMAN)

1. Confirm `pattern_area_buildout` row + library narrative resolve.
2. Walk the 14 components in AREA_GOVERNANCE_DISCIPLINE §2 for the
   target area.
3. Run `py scripts/validate_area_completeness.py --matrix` and record
   the area score row in the initiative report.
4. Disposition gap/partial findings via inline-ratify (defer to P1/P8
   when area-specific work is already chartered).
5. File operator-scratchpad entry before the area-buildout commit.

## Acceptance criteria

### AC-HUMAN

CPO or PMO can charter an area by reading this SOP + the discipline §2
without invoking the runbook (30–45 min manual checklist).

### AC-AUTOMATION

`py scripts/validate_area_completeness.py --self-test` exits 0 at
pre_commit; `--matrix` emits the seven-area table.

## Cross-references

- Process: `hol_peopl_dtp_area_governance_001` in `process_list.csv`
- Pattern: `pattern_area_buildout`
- [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 1
