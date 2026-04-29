# Founder Open Questions — External Counsel (derived view)

> **Program**: [`PRJ-HOL-FOUNDING-2026`](programs/PRJ-HOL-FOUNDING-2026/README.md). New program-scoped Legal casework lands under that subfolder; this derived view remains at the role-folder root for backwards compatibility (Initiative 22 P3, D-IH-1).


**Document owner**: Legal Counsel
**Version**: 2.0
**Date**: 2026-04-28
**Status**: Final

---

## Status: derived view (Initiative 21 / P4)

This document is a **derived human view** grouped by adviser discipline. The **single source of truth** is the canonical CSV [`ADVISER_OPEN_QUESTIONS.csv`](../../../../../compliance/ADVISER_OPEN_QUESTIONS.csv). Update the CSV first, validate (`py scripts/validate_hlk.py`), then refresh the tables below to match. Real organisations and persons appear as `GOI-*` / `POI-*` `ref_id`s; identity mapping is off-repo per [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001`](../Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md).

**Handoff entrypoint**: [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md).

**Plane**: External Adviser Engagement (`hol_opera_ws_5`); see [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001`](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) and the [`EXTERNAL_ADVISER_ROUTER`](../../Operations/PMO/EXTERNAL_ADVISER_ROUTER.md).

**Historical snapshot (2026-04-14):** [`founder-incorporation-section7-structured-table.md`](../../../../../../../wip/planning/04-holistika-company-formation/reports/founder-incorporation-section7-structured-table.md) §7.1–§7.3 — original `Q-001`–`Q-009` ids retained in the `notes` column for traceability.

---

## Legal & Corporate (`legal`)

| question_id | question | owner | target_date | status | refs | notes |
|:------------|:---------|:------|:------------|:-------|:-----|:------|
| `Q-LEG-001` | Confirm exact `objeto social` text and CNAE codes (with rationale) before signing | Legal Counsel | before_signing | open | `POI-LEG-ENISA-LEAD-2026`, `GOI-ADV-ENTITY-2026` | from Q-001 |
| `Q-LEG-002` | Recommendation: CIRCE telematic constitution vs ordinary notary route (incl. timing and fee profile) | Legal Counsel | before_signing | open | `GOI-ADV-ENTITY-2026` | from Q-002 |
| `Q-LEG-003` | CIRCE trade-offs vs bespoke `objeto social` (impact on flexibility and amendments) | Legal Counsel | before_signing | open | `GOI-ADV-ENTITY-2026` | from Q-003 |
| `Q-LEG-004` | Legal basis for the `1 euro` share-capital path explanation (incl. reserve-build obligations) | Legal Counsel | before_signing | open | `GOI-ADV-ENTITY-2026` | from Q-005 |
| `Q-LEG-005` | Holding-structure constraints to avoid taking now (decisions that would limit a future holding) | Legal Counsel | before_signing | open | `GOI-ADV-ENTITY-2026` | from Q-009 |

## Fiscal & Tax (`fiscal`)

| question_id | question | owner | target_date | status | refs | notes |
|:------------|:---------|:------|:------------|:-------|:-----|:------|
| `Q-FIS-001` | Exact pluriactivity / quota benefit believed to apply (assumptions and dependencies) | Business Controller | before_signing | open | `POI-LEG-FISCAL-LEAD-2026`, `GOI-ADV-ENTITY-2026` | from Q-006 |
| `Q-FIS-002` | Founder-funded infrastructure handling: tax treatment and bookkeeping path (pre vs post incorporation) | Business Controller | before_signing | open | `POI-LEG-FISCAL-LEAD-2026` | from Q-008; cross-link [`SOP-FOUNDER_COMPANY_FUNDING_001`](../../Finance/Business%20Controller/Taxes/SOP-FOUNDER_COMPANY_FUNDING_001.md) |

## IP & Trademark (`ip`)

| question_id | question | owner | target_date | status | refs | notes |
|:------------|:---------|:------|:------------|:-------|:-----|:------|
| `Q-IPT-001` | Trademark fee breakdown (official vs service) by territory and class for chosen filing strategy | Legal Counsel | tbd | open | `GOI-ADV-ENTITY-2026` | from Q-007 |

## Banking (`banking`)

| question_id | question | owner | target_date | status | refs | notes |
|:------------|:---------|:------|:------------|:-------|:-----|:------|
| `Q-BNK-001` | CNAE / constitution sequencing: align constitution-desk bank with certification adviser on who proposes final CNAE and how it stays consistent with `objeto social` | Legal Counsel | before_signing | open | `POI-BNK-DESK-LEAD-2026`, `GOI-BNK-INC-2026` | from Q-011 (real bank + desk-lead names redacted to GOI/POI ref_ids) |

## Startup Certification (`certification`)

| question_id | question | owner | target_date | status | refs | notes |
|:------------|:---------|:------|:------------|:-------|:-----|:------|
| `Q-CRT-001` | ENISA documentation split: which artifacts founder produces vs adviser-produced (responsibility matrix) | Compliance | tbd | open | `POI-LEG-ENISA-LEAD-2026`, `GOI-ADV-ENTITY-2026` | from Q-004 |
| `Q-CRT-002` | Deliver consolidated business plan + PESTEL / market analysis to certification adviser by email | Legal Counsel | asap | open | `POI-LEG-ENISA-LEAD-2026`, `GOI-ADV-ENTITY-2026` | from Q-010 (2026-08-04 kick-off) |
| `Q-CRT-003` | Startup / ENISA business plan: financing section — credible minimal narrative (adviser to revisit with more positive framing) | Legal Counsel | tbd | open | `POI-LEG-ENISA-LEAD-2026`, `GOI-ADV-ENTITY-2026` | from Q-012 (2026-08-04 kick-off) |

## Notary (`notary`)

_No open questions today; new rows go directly into the CSV with `Q-NOT-NNN` ids._

---

## Source transcripts (non-canonical, redacted)

Staging folder: [`delete-legal-transcripts` README](../../../../../business-intent/delete-legal-transcripts/README.md). Real names substituted with `POI-*` / `GOI-*` `ref_id` per [`SOP-HLK_TRANSCRIPT_REDACTION_001`](../Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md).

| Session | Transcript |
|:--------|:-----------|
| 2026-08-04 Kick-Off (`certification` / business plan) | [Part 1](../../../../../business-intent/delete-legal-transcripts/2026-08-04%20-%20Kick-Off%20-%20Constituci%C3%B3n%20Sociedad%20-%20Plan%20de%20Negocio%20Startup%20y%20ENISA_1.mp3.md), [Part 2](../../../../../business-intent/delete-legal-transcripts/2026-08-04%20-%20Kick-Off%20-%20Constituci%C3%B3n%20Sociedad%20-%20Plan%20de%20Negocio%20Startup%20y%20ENISA_2.m4a.md) |
| 2026-04-06 Pre-Kick-Off (`fiscal`) | [Fiscal call](../../../../../business-intent/delete-legal-transcripts/2026-04-06%20-%20Pre-Kick-Off%20-%20Constituci%C3%B3n%20Sociedad%20-%20Fiscal.m4a.md) |

---

## Maintenance

- **Source of truth:** `ADVISER_OPEN_QUESTIONS.csv`. Edit there first; this view is regenerated manually until [`scripts/export_adviser_handoff.py`](../../../../../../../scripts/export_adviser_handoff.py) (Initiative 21 / P7) replaces the manual step.
- **Validation:** `py scripts/validate_hlk.py` (PASS gate — discipline FK, GOI/POI FK, owner_role FK, status enum, target_date format, no `@` leak).
- **Closing a question:** Set `status = answered | closed | deferred` in CSV; capture canonical answers in case memos or [`FOUNDER_FILED_INSTRUMENT_REGISTER.md`](FOUNDER_FILED_INSTRUMENT_REGISTER.md) when they become filed fact.
- **Bumping version:** Bump `Version` here when the CSV header drifts or sections are added; refresh `Date` on every material refresh.
