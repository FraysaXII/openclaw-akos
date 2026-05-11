---
status: draft
classification: operator_private
access_level: 5
language: en
register: internal
artifact_kind: deck_objection_companion
audience: customer-enterprise
deck: deck-suez-webuy.fr.md
engagement_slug: 2026-suez-webuy
counterparty_org_ref: GOI-CUS-SUEZ-2026
linked_engagement: 2026-05-10-suez-webuy-procure-to-pay
governance:
  - BRAND_BASELINE_REALITY_MATRIX
  - sales-8-slide.objections.md (canonical template)
last_review: 2026-05-10
---

# Deck objection companion — SUEZ WeBuy

> Internal-register coaching artefact for the deck `deck-suez-webuy.fr.md`. Internal vocabulary (`counterparty`, `elicitation`, `agent`, `baseline reality`) is permitted here per the dual-register exemption for `*.objections.md` files. This file does not ship externally.

## Anchor objections (most likely to surface in the meeting)

| # | Objection | Response frame | Evidence we can cite |
|:---|:---|:---|:---|
| 1 | « C'est combien ? » (price-first opener) | Scope first; price follows clear deliverables. The proposal exposes a single closed-price band per variant; the per-package math sits in the engagement folder. | `commercial-schedule.md` totals (par 38 / 53 / 87 k€); §5 of the proposal. |
| 2 | « Vous allez vous installer chez nous longtemps ? » (fear of consultancy lock-in) | The handoff is a phase, not an option. The deck slide 08 opens explicitly on the transfer-and-close engagement rhythm. | `ENGAGEMENT_PLAYBOOK.md` Transfer + Close phases; deck §05 + §08. |
| 3 | « Vous connaissez notre métier ? » (industry-credibility test) | Discovery starts from the counterparty's operating reality; we don't pretend to know the field, we read the field. The CDC feasibility shape is the proof we already did the reading. | `cdc-feasibility-shape.fr.md` (24 functionalities sourced from the mode opératoire); §1 of the proposal. |
| 4 | « Et la sécurité de nos données ? » (DSI / RGPD / NDA) | NDA + DPA before sensitive discovery. The proposal §8 cites the legal template suite; we don't request data that isn't already in our scope. | Legal template suite (`MSA / SOW / NDA / DPA`); §8 of the proposal. |
| 5 | « Pourquoi pas en interne ? » (build vs buy) | We never argue against an internal build; we argue for a parallel discovery that lets the internal team start better-informed. The capability transfer phase is designed to enable internal continuation. | §6C of the service matrix (capability building); deck §07 (engagement borné). |
| 6 | « C'est un agent IA, ça non ? » (technical-risk flinch on the word "agent") | We use the word `application`, not `agent`, throughout the deck and the proposal. The Phase 1 prototype is Excel + Power Query; the Phase 2 application is a multi-category web app. | Deck §06; CDC feasibility shape §6 eligibility flag distribution. |
| 7 | « Cette automatisation va remplacer la personne qui opère ? » (operator-displacement concern) | The automation removes the deterministic burden, not the role. The Phase 1 prototype gives the operator more time for the parts that require judgment (relations fournisseurs, suivi des litiges, anomalies). The capability transfer phase actively trains the operator on the new tool. | §6 of the proposal (success criteria — opérateur autonome); F-23 of the CDC shape (suivi de la demande, kept human-in-the-loop). |
| 8 | « Microsoft Azure, c'est obligatoire ? » (DSI environment lock-in) | Phase 1 prototype runs in any compliance-friendly environment — Azure is a common choice in your context but not a constraint. We confirm the environment in the discovery call. | §2 hors-périmètre of the proposal (license costs are pass-through); discovery questionnaire B4. |

## Operator notes

* **Price ambiguity creates distrust at this counterparty class.** Per the EFA prospection brief, the bridge has explicitly observed that vague pricing reads as inexperience in enterprise procurement. If the par-band is questioned, fall back on the methodology (PERT three-point + multipliers) without exposing the multiplier numerics — those stay in the engagement folder.
* **Avoid the word `agent` entirely.** The bridge advisory (EFA prospection transcript ~28:42) was explicit: in this context, `agent` reads as risky / experimental / foreign. Use `application` for the web variant and `outil` for the Phase 1 prototype.
* **Don't oversell the bridge entity.** The bridge introduces; the engagement is Holistika's. The bridge is mentioned by role (`notre partenaire de collaboration`) but not by name in the deck or proposal.
* **The 24 functionalities count is a strong anchor.** Cite it whenever industry credibility is questioned. It is the single piece of evidence that demonstrates we already did the reading, not just a generic discovery pitch.
* **The "first-of-kind" multiplier (× 1.15) is internal-only.** It compounds onto pricing in `commercial-schedule.md` but never surfaces externally; if pricing is renegotiated, dropping `first_of_kind` is the cleanest concession to offer (≈ 13 % of par-cost in Variant B).
* **Time-to-value matters more than ambition.** The Variant B recommendation is exactly because the Phase 1 prototype shows real value at week 11; Variant C is technically richer but defers the proof point to week 18. Anchor on Variant B unless the counterparty signals high ambition.

## Pre-meeting prep checklist

- [ ] Read the latest counterparty signals from `counterparty-brief.md`.
- [ ] Confirm with the bridge that the four open placeholders (legal entity, commercial posture, primary signatory, name visibility rule) are still being closed at this meeting.
- [ ] Print or pre-load the proposal + commercial schedule + CDC feasibility shape in their FR rendered form (P8).
- [ ] Have the discovery questionnaire ready as a fallback if the meeting derails — it gives the conversation a structured path back to substance.
- [ ] Pre-read the elicitation-plan.md questions A–E (12 internal questions) so the spontaneous follow-ups land on the right depth.
