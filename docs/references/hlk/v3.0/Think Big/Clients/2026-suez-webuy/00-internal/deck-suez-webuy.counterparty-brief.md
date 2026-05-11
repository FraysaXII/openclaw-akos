---
status: draft
classification: operator_private
access_level: 5
language: en
register: internal
artifact_kind: deck_counterparty_brief
audience: customer-enterprise
deck: deck-suez-webuy.fr.md
engagement_slug: 2026-suez-webuy
counterparty_org_ref: GOI-CUS-SUEZ-2026
counterparty_lead_ref: POI-CUS-SUEZ-LEAD-2026
linked_engagement: 2026-05-10-suez-webuy-procure-to-pay
governance:
  - BRAND_BASELINE_REALITY_MATRIX
  - sales-8-slide.counterparty-brief.md (canonical template)
last_review: 2026-05-10
---

# Deck counterparty brief — SUEZ WeBuy

> Internal-register coaching artefact for the deck `deck-suez-webuy.fr.md`. Internal vocabulary is permitted here per the dual-register exemption for `*.counterparty-brief.md` files. This file does not ship externally.

## Reading lens

The counterparty class is **enterprise-procurement-operations** (CAC 40 holding, mature DSI, formal procurement chain). The expected reading lens at this meeting:

* « Une boutique espagnole avec un brief en français » — they will look for evidence that we read their context properly. The CDC feasibility shape is the centerpiece for this; it must be on the table from minute one.
* « Combien et quand » — enterprise procurement is calendar-locked. They want to know the par-duration first, the par-cost second.
* « Qui dans l'équipe » — they will probe the team shape. The bridge exists, the founder exists, a holistik researcher exists, a project manager exists; that's enough for this engagement.
* « Et la DSI ? » — they will surface the DSI question early. We are ready: scope (a) and (b) avoid live portal access; scope (c) requires a DSI conversation that is staged, not pre-empted.
* « C'est combien d'agents IA ? » — they will probe the technology stack. We use `application`, not `agent`; we cite Excel + Power Query for Phase 1 and a lightweight web app for Phase 2.

## Decision criteria (their side)

Per `BRAND_BASELINE_REALITY_MATRIX.md` enterprise-customer row + the EFA prospection brief:

* **Outcome clarity** — they want to know what they get, in plain terms, with measurable success criteria. Proposal §6 covers this.
* **Schedule predictability** — they want a calendar that respects their constraints (procurement windows, DSI validation cycles). Proposal §4 + commercial-schedule Mermaid Gantt cover this.
* **Confidentiality** — sensitive procurement data (supplier names, prices, internal codes) must stay within their perimeter. Proposal §8 cites the NDA + DPA path.
* **Time-to-value** — they want a Phase 1 visible result inside the year. Variant B targets week 11 prototype demonstration.
* **Practical competence evidence** — they want proof we already understand the WeBuy specifics, not a generic methodology pitch. The CDC feasibility shape is the proof.

## First doubt triggers

If any of these surface, recover deliberately:

* An English-only response when the conversation is in French (revert to FR; apologize once if it slips).
* A vague price ("ça dépend du contexte") — ground in the methodology and the par-band immediately. The PERT-expected number is the safest fallback.
* An over-technical pitch on Phase 2 (web app architecture, AI integration) — keep Phase 2 framed as a future-state outcome, not an opening proposition. Variant B prototype is the headline.
* A pitch that drops the bridge entity — the bridge is a **fact** of this engagement; not naming them reads as discomfort. Reference them by role (`notre partenaire de collaboration`).
* Any use of internal vocabulary leaking from the operator's mouth (`elicitation`, `baseline reality`, `counterparty`, `agent`) — recover with a clean restatement in the external register.

## Prep checklist

- [ ] Read `counterparty-brief.md` (this folder) §1–§4 the morning of the meeting.
- [ ] Confirm the four open placeholders are still expected to close at this meeting (`[counterparty_legal_entity]`, `[commercial_posture]`, `[primary_signatory_holistika_side]`, `[name_visibility_rule]`).
- [ ] Open `proposal.fr.md`, `discovery-questionnaire.fr.md`, `cdc-feasibility-shape.fr.md`, `commercial-schedule.md` in pre-meeting prep.
- [ ] Mental rehearsal of the eight-slide deck flow: 30 minutes max, 4 minutes per slide on average, leave 8 minutes for objections.
- [ ] Pre-load the deck objections companion (`deck-suez-webuy.objections.md`) for the eight typical objections.

## Post-meeting deliverables

Per `SOP-IO_INTELLIGENCE_REPORT_001` + the elicitation-plan.md follow-up rules:

* Update `counterparty-brief.md` §1 (baseline reality) with new signals captured.
* Update §4 placeholders with confirmed values.
* Re-grade sources `S5–S9` in `source-grade.csv` based on the meeting's reliability and credibility cues.
* Decide variant retained (A / B / C) and re-render `commercial-schedule.md` if any package count shifts.
* Update the proposal's cover block with confirmed legal entity + signatories.
* Send the post-meeting follow-up within 48 hours per the deck slide 08 commitment.
