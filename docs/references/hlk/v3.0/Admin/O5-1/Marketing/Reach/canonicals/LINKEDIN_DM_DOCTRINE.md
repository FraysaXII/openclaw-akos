---
title: LinkedIn DM Channel Doctrine
language: en
status: active
canonical: true
role_owner: Resonance Manager
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
channel_id: CHAN-LINKEDIN-DM
---

# LinkedIn DM Channel Doctrine

> Resonance-owned doctrine for LinkedIn direct messages as a Holistika
> channel. Per `MARKETING_AREA_M3_REDESIGN.md` §3.1 the channel owner
> is Resonance Manager because LinkedIn DM is 1:1 deepening, not 1:N
> reach. Brand & Narrative continues to author the register; the channel
> deploys it.

## 1. Purpose

LinkedIn DM is the channel where Holistika engages individuals in
1:1 conversation off the public timeline. It is the primary inbound
path for cold investors and cold advisors per
`CHANNEL_TOUCHPOINT_REGISTRY.csv`, and a secondary outbound path when
the operator initiates a context-rich follow-up.

## 2. Audience pairings

| Recipient class | When LinkedIn DM is appropriate | Notes |
|:---|:---|:---|
| J-IN investor (cold or warm) | First-touch after content trigger; bridge confirmation | Use `PERSONA-INVESTOR-COLD` / `PERSONA-INVESTOR-WARM` triage per persona qualification gate. |
| J-AD advisor | Cold pitch acknowledgement, mandate scoping pre-NDA | Default low priority unless prior context. |
| J-PT partner | Soft re-engagement, public-context warm-up | Avoid commercial terms in DM. |
| J-RC recruiter | Talent inbound, employer-brand questions | Currently `inactive` per `AUDIENCE_REGISTRY`; activates when recruiter pipeline opens. |
| J-CU customer SME | Rare; only after content or event trigger | Default to email or Cal once interest is confirmed. |

J-OP and J-AIC do not consume this channel.

## 3. Format pairings

- Primary: short HTML message in LinkedIn UI (translated-external).
- Secondary: link to public artifact (web page, dossier PDF) hosted
  outside LinkedIn so authorship and lineage stay durable.
- Never: long-form proposals or commercial terms in DM body. Move to
  email or Cal once the conversation warrants attachments.

## 4. Goods

1. **Single-thread, single-topic** discipline; do not branch into
   multiple asks.
2. **Reference the public trigger** (post, event, mutual connection)
   that warranted the DM.
3. **Concise opener** that names the persona-fit assumption
   transparently ("you mentioned X in Y; this seemed adjacent").
4. **Soft ask** plus next-channel suggestion (link to Cal, link to
   public page) so the recipient picks the medium.
5. **Voice consistent with profile** (operator's own voice when
   operator-sent; Resonance Manager voice when delegated).

## 5. Bads (anti-patterns)

1. Cold pitch templates with generic openers.
2. Asking for time before establishing topic fit.
3. Attaching commercial terms or scope in the body.
4. Sending links without UTM when the campaign manifest expects
   measurement.
5. Sending CORPINT-internal vocabulary into a public-network channel.
6. Burst messaging (3+ messages without a reply).
7. Treating LinkedIn DM as bulk outbound; bulk-outreach belongs to
   email plus adapter governance.

## 6. Cadence + frequency norms

| Recipient state | Default cadence | Hard limit |
|:---|:---|:---|
| First-touch cold | 1 follow-up after 48h reply window | Stop after 2 silent rounds |
| Warm (bridge confirmed) | Respond within 24h | Same |
| Active conversation | Same-day or next-day reply | Same |
| Paused | Wait for trigger event (post, event) before re-engaging | Operator approval required |

Per `CHANNEL_TOUCHPOINT_REGISTRY.csv` SLA band: 48h response.

## 7. Brand-register translations

LinkedIn DM is a public-network channel; translated-external register
is mandatory per `BRAND_BASELINE_REALITY_MATRIX.md`. Forbidden tokens:
all CORPINT-internal vocabulary (counterparty, elicitation,
intelligence-collection, baseline-reality-assessment, etc.). Use
named-counterparty class words instead (investor, advisor, partner,
client).

## 8. Measurement primitives

- Reply rate per first-touch DM (target >= 20% when persona is matched).
- Time-to-first-response.
- Conversion to next-channel (Cal booking, email reply) within 14
  days of first reply.
- Manual stage promotion in engagement folder when a DM thread crosses
  into `Conversation-Live` per `MARKETING_LIFECYCLE_TAXONOMY.md`.

## 9. Cross-references

- `CHANNEL_TOUCHPOINT_REGISTRY.csv` row `CHAN-LINKEDIN-DM`.
- `MARKETING_AREA_M3_REDESIGN.md` §3.1 propagation matrix.
- `MARKETING_LIFECYCLE_TAXONOMY.md` lifecycle vocabulary.
- `MKTOPS_DISCIPLINE.md` MKT-04 plus MKT-06 plus MKT-07 apply.
- `BRAND_BASELINE_REALITY_MATRIX.md` dual-register contract.
- `RESEARCH_ACTION_DISCIPLINE.md` for the source ledger that backs
  new claims surfaced in DM threads.
- `akos-external-render-discipline.mdc` RULE 7 channel-format matrix.
