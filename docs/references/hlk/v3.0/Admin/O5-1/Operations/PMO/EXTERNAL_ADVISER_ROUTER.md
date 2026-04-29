# External Adviser Router (ADVOPS plane)

**Document owner**: PMO
**Version**: 1.0
**Date**: 2026-04-28
**Status**: Final (P3)

---

## Purpose

Single navigation entrypoint for **external-adviser engagements** routed through the [External Adviser Engagement plane (`hol_opera_ws_5`)](../../../../compliance/process_list.csv). Use this document to find:

- The **discipline lookup** (which adviser type owns what).
- The **canonical assets** an adviser may produce (questions, instruments, POI/GOI rows).
- The **handoff entrypoint** advisers read first.
- The **escalation path** when a question or instrument crosses disciplines.

This file is **not** the SOP — see [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md). It is the **operator-facing index** routed from PMO.

## Discipline routing

| discipline_id | code | display_name | canonical role | entrypoint process | counsel handoff section (P4) |
|:--------------|:----:|:-------------|:---------------|:-------------------|:-----------------------------|
| `legal` | LEG | Legal & Corporate | Legal Counsel | [`thi_legal_dtp_302`](../../../../compliance/process_list.csv) | "Legal & Corporate" |
| `fiscal` | FIS | Fiscal & Tax | Business Controller | [`thi_finan_dtp_302`](../../../../compliance/process_list.csv) | "Fiscal & Tax" |
| `ip` | IPT | IP & Trademark | Legal Counsel | [`thi_legal_dtp_303`](../../../../compliance/process_list.csv) | "IP & Trademark" |
| `banking` | BNK | Banking | Legal Counsel | [`thi_legal_dtp_302`](../../../../compliance/process_list.csv) | "Banking" |
| `certification` | CRT | Startup Certification | Compliance | [`hol_peopl_dtp_302`](../../../../compliance/process_list.csv) | "Startup Certification" |
| `notary` | NOT | Notary | Legal Counsel | [`thi_legal_dtp_302`](../../../../compliance/process_list.csv) | "Notary" |

The lookup is **CSV-canonical**: [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../../compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv). To add a discipline, add a row (no schema change).

## Adviser-facing entrypoint

External advisers read [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) first. From P4 onwards it carries one section per discipline (`Legal & Corporate`, `Fiscal & Tax`, `IP & Trademark`, `Banking`, `Startup Certification`, `Notary`), each linking to the discipline-filtered slice of:

- The **open questions register** ([CSV `ADVISER_OPEN_QUESTIONS.csv`](../../../../compliance/) — graduates in P4 — and human view [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](../../People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md)).
- The **filed instruments register** ([CSV `FOUNDER_FILED_INSTRUMENTS.csv`](../../../../compliance/) — graduates in P5 — and human view [`FOUNDER_FILED_INSTRUMENT_REGISTER.md`](../../People/Legal/FOUNDER_FILED_INSTRUMENT_REGISTER.md)).
- The **fact pattern** ([`FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md`](../../People/Legal/FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md)) with all real names substituted by `POI-*`/`GOI-*` `ref_id`.

## Stakeholder reference

Real organisations and persons are captured in [`GOI_POI_REGISTER.csv`](../../../../compliance/GOI_POI_REGISTER.csv). Documents reference `ref_id` only; identity mapping is off-repo per [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001`](../../People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md).

| Lens | Example `ref_id` |
|:-----|:-----------------|
| External adviser firm | `GOI-ADV-ENTITY-2026` |
| ENISA-track adviser lead | `POI-LEG-ENISA-LEAD-2026` |
| Fiscal-track adviser | `POI-LEG-FISCAL-LEAD-2026` |
| Pre-kick-off intake contact | `POI-ADV-INTAKE-LEAD-2026` |
| Constitution-desk bank | `GOI-BNK-INC-2026` |
| Constitution-desk lead | `POI-BNK-DESK-LEAD-2026` |

## Escalation path

| Trigger | Escalation |
|:--------|:-----------|
| Cross-discipline question (e.g. fiscal residence affects legal route) | PMO routes a copy of the question into both disciplines (one row per discipline in `ADVISER_OPEN_QUESTIONS.csv`); cross-link via `notes`. |
| `confidential` / `restricted` POI surface area | Compliance + Legal Counsel review before raising the GOI/POI sensitivity band. |
| Missing process_list entrypoint | PMO opens an operator-gated tranche (per [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc)) before adding new discipline rows. |
| New program (e.g. a second founder entity) | Pick a fresh `program_id` (`PRJ-<E>-<TOPIC>-<YYYY>`), reuse all registers; no new schemas. |

## Related

- Plane SOP: [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
- GOI/POI SOP: [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001`](../../People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md)
- Redaction SOP: [`SOP-HLK_TRANSCRIPT_REDACTION_001`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md)
- Cursor rule: [`akos-adviser-engagement.mdc`](../../../../../../../.cursor/rules/akos-adviser-engagement.mdc)
- Initiative roadmap: [`master-roadmap.md`](../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)
