---
title: Web Form Channel Doctrine
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
  - SOP-GTM_INBOUND_SLA_001.md
  - SOP-GTM_QUALIFICATION_001.md
  - ../../canonicals/MARKETING_AREA_M3_REDESIGN.md
  - ../../canonicals/MARKETING_LIFECYCLE_TAXONOMY.md
  - ../../canonicals/MKTOPS_DISCIPLINE.md
  - ../../../People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
  - ../../../People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv
linked_runbooks:
  - scripts/validate_mktops_campaign.py
linked_research_sources:
  - docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/source-ledger.csv
channel_id: CHAN-WEB-FORM
---

# Web Form Channel Doctrine

> Reach-owned doctrine for the web contact form as a Holistika channel.
> The form on `holistikaresearch.com` is the canonical N4 cold-inbound
> path; everything else routes through a known bridge first.

## 1. Purpose

The web form exists to absorb cold inbound from people who found
Holistika through search, content, or word-of-mouth without an
established bridge. It functions as the front door for prospects who
have already decided to reach out and need a structured way to do it.

## 2. Audience pairings

| Recipient class | When the form is appropriate | Notes |
|:---|:---|:---|
| J-CU customer SME (prospect) | Inbound prospects; service or product enquiry | Most common; routes to PMO triage. |
| J-RC recruiter or talent (inbound) | Talent enquiry; co-founder approach | Routes to Founder when role row is operator-only. |
| J-PT partner (cold) | Co-delivery or co-marketing offer | Routes to PMO; partner-fit triage first. |
| J-CO collaborator | Methodology peer enquiry | Currently `planned`; routes to Founder when active. |

J-IN cold investors should not arrive here; LinkedIn DM or warm
referrals are the expected investor inbound paths.

## 3. Format pairings

- Primary: web form on `holistikaresearch.com` (translated-external).
- Secondary: auto-acknowledge email body (mail surface) confirming
  receipt and naming the triage SLA.
- Never: free-text upload of attachments without size cap or content
  scan.

## 4. Goods

1. **Required fields only** for first contact (name, email, intent,
   one optional context field). Extra fields drop conversion.
2. **Intent dropdown** with 4-6 options aligned to lifecycle stages
   (Service enquiry / Product enquiry / Partnership / Other) so PMO
   can triage fast.
3. **Auto-acknowledge** confirming receipt and naming a 7-day triage
   SLA per `SOP-GTM_INBOUND_SLA_001.md`.
4. **Form preserves UTM** in a hidden field so attribution per
   `MKTOPS_DISCIPLINE.md` MKT-04 stays clean.
5. **Confirmation page** doubles as a content nudge (link to a
   research artifact, blog post, or About page).
6. **Accessibility per `UX_DISCIPLINE.md`** UX-07 WCAG AA bar.

## 5. Bads (anti-patterns)

1. Overlong forms (more than 6 fields at first contact).
2. CAPTCHA so aggressive it breaks accessibility.
3. Missing UTM passthrough; conversion attribution dies at the form.
4. Auto-acknowledge with no SLA, only thank-you.
5. CORPINT-internal vocabulary leaking into form labels or
   confirmation copy (e.g. `counterparty`, `intelligence collection`).
6. Routing every inbound to the founder; PMO is the first triage.

## 6. Cadence + frequency norms

- Auto-acknowledge: immediate.
- First human reply: within 7 business days per SLA band.
- Re-engagement after silent triage: not via this channel; route to
  email outbound once a bridge is established.

Bulk-form spam is filtered by basic anti-bot measures plus PMO
heuristic triage; spam triage is governed by
`SOP-GTM_INBOUND_SLA_001.md`, not this doctrine.

## 7. Brand-register translations

Form labels, microcopy, validation messages, and confirmation copy
are external-translated register. No internal vocabulary. Forbidden
tokens: `AKOS`, `PRJ-HOL-*`, `topic_*`, `plane`, `MASTER`, `KM`,
`RBAC`, `RLS`, `FDW`, `pgvector`. Use plain client-facing nouns.

## 8. Measurement primitives

- Form submission rate (target >= 3% of unique visitors when content
  funnel is active).
- Bot vs human ratio (anti-bot effectiveness signal).
- Time-to-triage (PMO triage within 7 days).
- Conversion from `Demand-Engaged` to `Conversation-Live` per
  `MARKETING_LIFECYCLE_TAXONOMY.md`.
- Per-intent funnel depth (which intent dropdown values convert).

Per MKT-04 in `MKTOPS_DISCIPLINE.md`, every campaign manifest naming
this channel must declare measurement events plus UTM tags.

## 9. Cross-references

- `CHANNEL_TOUCHPOINT_REGISTRY.csv` row `CHAN-WEB-FORM`.
- `MARKETING_AREA_M3_REDESIGN.md` §3.1 propagation matrix.
- `MARKETING_LIFECYCLE_TAXONOMY.md` lifecycle vocabulary.
- `MKTOPS_DISCIPLINE.md` (full 7 dimensions apply to form-fed
  campaign manifests).
- `SOP-GTM_INBOUND_SLA_001.md` (triage SLA).
- `SOP-GTM_QUALIFICATION_001.md` (post-triage qualification).
- `BRAND_BASELINE_REALITY_MATRIX.md` (dual-register contract).
- `akos-external-render-discipline.mdc` RULE 7 (web surface).
- `UX_DISCIPLINE.md` (accessibility bar).
