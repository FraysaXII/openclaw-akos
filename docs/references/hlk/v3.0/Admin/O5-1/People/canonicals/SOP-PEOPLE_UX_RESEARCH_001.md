---
title: SOP — People UX Research and Quality Bar
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_UX_RESEARCH_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Brand & Narrative Manager
co_authors:
  - Front-End Developer
  - PMO
last_review: 2026-06-04
last_review_by: Brand & Narrative Manager
last_review_decision_id: D-IH-90-AD
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BY
  - D-IH-90-AD
status: active
register: internal
linked_canonicals:
  - UX_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
linked_runbooks:
  - scripts/validate_locale_orthography.py
  - scripts/lint_brand_voice_offline.py
  - scripts/browser-smoke.py
linked_processes:
  - hol_peopl_dtp_ux_research_001
cadence: event_triggered
cadence_trigger: brand-surface deploy OR component primitive change OR locale file change
---

# SOP — People UX Research and Quality Bar

## Purpose

Operationalise the seven UX dimensions in
[`UX_DISCIPLINE.md`](UX_DISCIPLINE.md) for every user-facing surface
(component primitive, artifact-class composition, or route-level IA change).

Closes the forward-charter on OPS-86-9 with a composite automation surface
until a dedicated `scripts/ux_quality_check.py` chassis lands at I91 P2.

## Scope

| In scope | Out of scope |
|:---|:---|
| boilerplate / hlk-erp / kirbe-platform UI routes | Backend-only API changes |
| i18n message files (`messages/*.json`) | Internal CORPINT-only markdown |
| Accessibility on J-IN / J-CU / J-RC public routes | Pre-NDA adviser-only ERP panels |

## Steps (AC-HUMAN)

1. **Cite persona + channel** — FK-resolve PERSONA_REGISTRY + CHANNEL_TOUCHPOINT rows.
2. **Walk UX-01..07** per doctrine section 2; use impeccable skill for UX-06.
3. **Disposition gaps** via inline-ratify before deploy.
4. **Attach UAT evidence** — browser audit trail per planning-traceability when closing.

## Steps (AC-AUTOMATION)

```powershell
py scripts/validate_locale_orthography.py --strict
py scripts/lint_brand_voice_offline.py
py scripts/browser-smoke.py --playwright
```

Dedicated `ux_quality_check.py --self-test` forward-charter: I91 DATA/UX tranche P2.

## Acceptance criteria

| Surface | Human | Automation |
|:---|:---|:---|
| AC-HUMAN | Brand Manager or Front-End Developer walks UX-01..07 | N/A |
| AC-AUTOMATION | N/A | locale + brand lint PASS; browser-smoke PASS on touched routes |

## Cross-references

- Cursor rule: `.cursor/rules/akos-ux-discipline.mdc`
- Forward charter superseded: `docs/wip/planning/_trackers/ux-research-sop-forward-charter.md`
