---
title: Cal Schedule Channel Doctrine
language: en
status: active
canonical: true
role_owner: Reach Manager
classification: way_of_working
intellectual_kind: channel_doctrine
access_level: 4
authored: 2026-05-27
last_review: 2026-05-27
last_review_by: Founder
last_review_decision_id: D-IH-86-EZ
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-EZ
linked_canonicals:
  - REACH_AREA_CHARTER.md
  - ../../canonicals/MARKETING_AREA_M3_REDESIGN.md
  - ../../canonicals/MARKETING_LIFECYCLE_TAXONOMY.md
  - ../../canonicals/MKTOPS_DISCIPLINE.md
  - ../../../People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
  - ../../../People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv
linked_runbooks:
  - scripts/validate_mktops_campaign.py
linked_research_sources:
  - docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/source-ledger.csv
channel_id: CHAN-CAL-SCHEDULE
---

# Cal Schedule Channel Doctrine

> Reach-owned doctrine for the Cal.com scheduling link as a Holistika
> channel. Per `CHANNEL_TOUCHPOINT_REGISTRY.csv` this is an N1
> channel: the link is shared deliberately and a deep context is
> assumed when a booking lands. The cadence rules here are tight
> because every booking consumes founder time directly.

## 1. Purpose

The Cal link converts a soft interest signal into a concrete time
commitment on both sides. It is the conversion mechanism between
`Conversation-Live` (email or DM thread) and a real meeting in
`MARKETING_LIFECYCLE_TAXONOMY.md`. Cal bookings are the canonical
N1 channel: they are NEVER cold; they always follow a shared link.

## 2. Audience pairings

| Recipient class | When the Cal link is appropriate to share | Notes |
|:---|:---|:---|
| J-CU customer SME (active conversation) | Discovery call, scope refinement, demo walk-through | Tag the meeting type so PMO can pre-brief. |
| J-IN investor (warm or referral) | First operator call, follow-up update call | Default 30 minutes; founder-led. |
| J-PT partner (active) | Co-pipeline sync, co-delivery checkpoint | Match partner cadence. |
| J-AD advisor (post-NDA) | Mandate kickoff, evidence walk-through | Restricted Cal type with NDA gating in the booking form. |
| J-CO collaborator | Methodology peer review or co-author session | Currently rare; default to founder time. |

J-OP and J-AIC do not consume this channel; internal scheduling lives
elsewhere.

## 3. Format pairings

- Primary: Cal.com booking link plus subsequent calendar invite body
  (mail surface with structured meeting agenda).
- Secondary: per-meeting prep doc shared in advance (PDF or web page,
  translated-external register).
- Never: Cal link shared cold to someone who has not engaged in a
  thread or content; cold Cal bookings are a quality signal that
  someone misused the link.

## 4. Goods

1. **Multiple Cal types** with explicit intent labels (Discovery /
   Demo / Partnership / Advisor) so founder time is pre-budgeted.
2. **Pre-meeting required field** asking for context (1-2 sentences)
   so founder can pre-brief.
3. **Agenda in calendar invite body** (3-5 bullets) so both sides
   share an outcome expectation.
4. **Follow-up template** prepared in advance: thank-you plus 1-line
   recap plus single next step plus next-channel suggestion.
5. **Per-engagement tagging** in CRM so meeting cadence aggregates
   with the engagement record.
6. **Cal link rotation per persona-class** when high-craft investor
   pipeline opens (separate booking template from generic founder
   call link).

## 5. Bads (anti-patterns)

1. Sharing the Cal link as a cold opener.
2. Empty calendar invites without agenda.
3. Generic meeting titles ("call with Jordi").
4. No pre-meeting context capture (founder walks in cold).
5. Founder-time over-booking; protect deep-work blocks.
6. CORPINT-internal vocabulary in invite body (defaults to external-
   translated register; counterparty-class words instead).
7. No follow-up template; meetings vanish into engagement folders
   without next-step propagation.

## 6. Cadence + frequency norms

| Recipient state | Default duration | Follow-up |
|:---|:---|:---|
| Discovery call | 30 minutes | Recap email within 24h |
| Demo or technical walk | 45-60 minutes | Recap plus next-step proposal within 24h |
| Partnership sync | 30-45 minutes | Joint recap or shared doc edit within 48h |
| Advisor session | 60 minutes | Recap plus mandate update within 48h |

Per `CHANNEL_TOUCHPOINT_REGISTRY.csv` SLA: immediate (the booking
itself IS the response).

## 7. Brand-register translations

Calendar invite bodies, agenda bullets, and follow-up templates use
external-translated register. No internal vocabulary in the visible
parts of the invite. Forbidden tokens: same as
`EMAIL_OUTBOUND_DOCTRINE.md` §7 plus operator-side process tokens
(`TODO[OPERATOR-x]`, `dtp_`, `wsto_`, `ws_`).

## 8. Measurement primitives

- Booking conversion (per `Conversation-Live` thread): target >= 25%
  of qualified threads.
- Show-up rate (target >= 90%; below that, review pre-meeting context
  and invite quality).
- Post-meeting stage promotion in engagement folder.
- Founder-time efficiency (meetings per week vs deep-work blocks).
- Per-Cal-type funnel depth (which intent labels convert).

Per MKT-04 in `MKTOPS_DISCIPLINE.md`, every campaign manifest naming
this channel must declare its measurement event (typically
`cal_booking_completed`).

## 9. Cross-references

- `CHANNEL_TOUCHPOINT_REGISTRY.csv` row `CHAN-CAL-SCHEDULE`.
- `MARKETING_AREA_M3_REDESIGN.md` §3.1 propagation matrix.
- `MARKETING_LIFECYCLE_TAXONOMY.md` (Conversation-Live to Engagement-Open
  bridge).
- `MKTOPS_DISCIPLINE.md` MKT-04 plus MKT-05 plus MKT-06 plus MKT-07
  apply.
- `BRAND_BASELINE_REALITY_MATRIX.md` dual-register contract.
- `RESEARCH_ACTION_DISCIPLINE.md` for source-grounded claims discussed
  in meetings.
- `akos-external-render-discipline.mdc` RULE 7 channel-format matrix
  (Cal as ERP-class scheduling plus mail-surface invite body).
