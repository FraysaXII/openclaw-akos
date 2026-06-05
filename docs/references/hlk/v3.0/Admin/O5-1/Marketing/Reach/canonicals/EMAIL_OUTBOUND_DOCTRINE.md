---
title: Email Outbound Channel Doctrine
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
channel_id: CHAN-EMAIL-OUTBOUND
---

# Email Outbound Channel Doctrine

> Reach-owned doctrine for outbound email as a Holistika channel.
> Consumes the Research Action source ledger and the Wave R+4 C2
> brand propagation matrix. Validated structurally by
> `scripts/validate_mktops_campaign.py` when a campaign manifest names
> `CHAN-EMAIL-OUTBOUND`.

## 1. Purpose

Outbound email is the channel through which Holistika initiates
correspondence with a named recipient who has not necessarily opted
in. It is the workhorse of B2B Demand-Engaged through Conversation-Live
stages of `MARKETING_LIFECYCLE_TAXONOMY.md`.

## 2. Audience pairings

| Recipient class | When email outbound is appropriate | Notes |
|:---|:---|:---|
| J-CU customer SME | Discovery follow-up, proposal nudge, scope clarification | Most common use; honor lifecycle stage wording. |
| J-IN investor (warm referral or earned introduction) | Follow up on a meeting, attach a 1-pager, schedule next step | Use persona row (e.g. `PERSONA-INVESTOR-WARM`, `PERSONA-INVESTOR-HIGH-CRAFT`) to pick voice and depth. |
| J-PT partner | Co-delivery confirmation, joint-pipeline update | Match partner cadence; do not surprise on commercials. |
| J-AD advisor | NDA-gated handoff packs, mandate follow-ups | Hybrid register per `BRAND_BASELINE_REALITY_MATRIX.md`. |
| J-ENISA regulator | Formal reply, evidence packet correspondence | Strict external-translated register; never internal vocabulary. |

Cold outbound to investors or advisors without a bridge is out of scope
for this doctrine; that pattern is governed by
`SOP-GTM_QUALIFICATION_001.md` and remains operator-led.

## 3. Format pairings

`bd_commission_overlay`-free email body is the primary surface. Per
`akos-external-render-discipline.mdc` RULE 1 the `mail` surface is the
canonical delivery, with optional attached PDFs.

- Primary: HTML/plain email body (translated-external register).
- Secondary: attached PDF (1-pager, proposal, demo spec) with render
  trail through `scripts/render_dossier.py` or `scripts/render_suez_engagement_pdfs.py`.
- Never: raw `.md` attachments to non-`J-OP` recipients.

## 4. Goods

1. **Specific subject line** with a single action or topic; one
   thread per topic.
2. **Acknowledge prior context** in the first sentence; honor what the
   recipient already said.
3. **One ask, one deadline, one follow-up channel** (e.g., Cal link).
4. **Signed by a real human** (operator or named role owner); avoid
   role-only signatures unless the role is the recipient's only
   anchor.
5. **Tight body** (5-12 sentences); long-form belongs in attached PDF
   or web page.
6. **Per-recipient `notes` field captured** in the engagement folder
   for next-touch continuity.

## 5. Bads (anti-patterns)

1. Generic subject lines (`Following up`, `Quick question`).
2. Recap-only bodies that add no new ask or evidence.
3. Multiple asks competing for the same deadline.
4. Vanity attachments (decks the recipient already saw).
5. CORPINT-internal vocabulary leaking into the body (counterparty,
   elicitation, intelligence-collection). External-translated register
   is mandatory per dual-register contract.
6. No UTM on tracked links when the campaign manifest declares
   `measurement_event`.
7. Sending PDFs without a sha256 manifest where one exists.

## 6. Cadence + frequency norms

| Recipient state | Default cadence | Hard limit |
|:---|:---|:---|
| New thread (no prior reply) | 1 follow-up after 5-7 business days | Max 2 follow-ups before pause |
| Active conversation | Respond within 1 business day | Same |
| Paused or declined | Wait until trigger event (referenced) | Never re-introduce without operator approval |

Bulk outbound (more than 5 recipients in a single send) is out of scope
for this doctrine and routes to `SOP-GTM_INBOUND_SLA_001.md` plus
adapter governance per `EMAIL_ADAPTER_REGISTRY.csv`.

## 7. Brand-register translations

| Internal phrase | External phrase |
|:---|:---|
| counterparty | client / investor / partner / advisor (per persona) |
| elicitation | discovery, structured questions |
| intelligence report | research brief / engagement note |
| approach techniques | engagement design |

Forbidden tokens in body: `AKOS`, `PRJ-HOL-*`, `topic_*`, `plane`,
`MASTER`, `KM`, `RBAC`, `RLS`, `FDW`, `pgvector`, `kirbe.*` (schema
name only, not product), per `BRAND_BASELINE_REALITY_MATRIX.md` and
`BRAND_JARGON_AUDIT.md` §4.

## 8. Measurement primitives

- Reply rate per thread (>= 30% target for warm; >= 10% for first-touch
  cold-by-bridge).
- Time-to-first-response.
- Conversion from `Demand-Engaged` to `Conversation-Live` per
  `MARKETING_LIFECYCLE_TAXONOMY.md`.
- UTM-tagged click-through when links carry trackers.
- Manual stage transitions logged in engagement folder.

Per MKT-04 in `MKTOPS_DISCIPLINE.md`, every campaign manifest naming
this channel must declare `measurement_event` and UTM tags before
launch.

## 9. Cross-references

- `MARKETING_AREA_M3_REDESIGN.md` §3.1 propagation matrix (Reach Manager
  is owner; Brand & Narrative authors register; lifecycle taxonomy
  controls stage wording).
- `MARKETING_LIFECYCLE_TAXONOMY.md` (lifecycle stage vocabulary).
- `MKTOPS_DISCIPLINE.md` (MKT-01 through MKT-07 mandatory bar per
  campaign manifest).
- `BRAND_BASELINE_REALITY_MATRIX.md` (dual-register contract).
- `akos-external-render-discipline.mdc` RULE 1 (mail surface) + RULE 7
  (channel-format compatibility).
- `RESEARCH_ACTION_DISCIPLINE.md` (source ledger gate for new claims).
- `CHANNEL_TOUCHPOINT_REGISTRY.csv` row `CHAN-EMAIL-OUTBOUND` (channel
  row used by campaign manifests).
