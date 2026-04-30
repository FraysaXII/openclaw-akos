---
language: en
status: active
template_kind: outbound_brief
role_owner: PMO
area: Operations / PMO
entity: Holistika Research
authority: Founder + PMO
last_review: 2026-04-30
derived_locales: [es, fr]
---

# Outbound brief — TEMPLATE (English canonical)

> **Operator note.** This is the canonical template for engaging external professionals (designers, developers, marketers, translators, advisors). The brief itself is the engagement contract — once signed/agreed, no separate SoW is needed. Locale variants in [`TEMPLATE_OUTBOUND_BRIEF_es.md`](TEMPLATE_OUTBOUND_BRIEF_es.md) and [`TEMPLATE_OUTBOUND_BRIEF_fr.md`](TEMPLATE_OUTBOUND_BRIEF_fr.md). Per [`SOP-HLK_LOCALISATION_001.md`](../../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md), the brief is rewritten per locale (not literally translated).

---

## 1. Context

**Who we are.** Holística Research is a Spanish operations-engineering company. We productize our own method as KiRBe SaaS + the MADEIRA agentic platform. Our internal stack is governed by hundreds of canonical artifacts (process registries, validators, drift probes); brand voice is codified in [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md).

**Why this engagement.** [TODO[OPERATOR-brief-context] — one paragraph: what initiative is this for, why now, what role does the deliverable play in the bigger picture]

**Reference materials.** [List the 1 - 3 docs the contractor should read before starting; e.g., a deck, a SOP, a brand artefact]

## 2. Deliverable

**Concrete output.** [TODO[OPERATOR-brief-deliverable] — one sentence; e.g., "12 illustrations in SVG format at 1440x810 px, source files included"]

**File format and naming convention.** [Specific format requirements; e.g., ".fig + exported PNG/SVG; filenames `slide-NN-<descriptor>.svg`"]

**Quantity and granularity.** [How many units; what counts as one unit]

**Out of scope.** [What this brief explicitly does NOT cover; protects both parties from scope creep]

## 3. Quality gates

The deliverable passes acceptance review only when ALL of the following hold:

- **Brand voice compliance.** Adheres to [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md) and the relevant locale pattern file.
- **Specification compliance.** Matches the deliverable definition above (file format, naming, quantity).
- **Quality criterion 1.** [TODO[OPERATOR-brief-quality-1]]
- **Quality criterion 2.** [TODO[OPERATOR-brief-quality-2]]
- **Quality criterion 3.** [TODO[OPERATOR-brief-quality-3]]

We perform one round of revisions if the first delivery falls short on any criterion. After the second round, the engagement either closes (with payment for delivered units) or continues at re-negotiated scope.

## 4. Brand voice rules

For prose deliverables: follow [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md) (English) / [`BRAND_SPANISH_PATTERNS.md`](../../../Marketing/Brand/BRAND_SPANISH_PATTERNS.md) (Spanish) / [`BRAND_FRENCH_PATTERNS.md`](../../../Marketing/Brand/BRAND_FRENCH_PATTERNS.md) (French) per the locale of the output.

For visual deliverables: follow [`BRAND_VISUAL_PATTERNS.md`](../../../Marketing/Brand/BRAND_VISUAL_PATTERNS.md). Tokens (colors, type, spacing) are non-negotiable.

For all deliverables: external surfaces must pass the [`BRAND_JARGON_AUDIT.md`](../../../Marketing/Brand/BRAND_JARGON_AUDIT.md) jargon-free rule. No internal codenames in client-facing output.

## 5. Timeline and milestones

| Milestone | Date | Deliverable | Operator-side |
|:----------|:-----|:------------|:--------------|
| Kick-off | [TODO[OPERATOR-brief-kickoff-date]] | Brief signed; reference materials shared | PMO confirms access |
| Mid-point check | [TODO[OPERATOR-brief-midpoint-date]] | Draft / partial delivery | PMO + Brand Manager review |
| Delivery | [TODO[OPERATOR-brief-delivery-date]] | Full deliverable | Acceptance review starts |
| Acceptance | within 3 business days of Delivery | Pass / revisions / decline | Payment trigger |

Deadline slips by the contractor: if the contractor anticipates a slip > 48 hours, they notify us in writing immediately. We re-negotiate scope or extend; we do not penalize honest early notification.

## 6. Payment terms

**Rate.** [TODO[OPERATOR-brief-rate] — hourly band, fixed fee, or milestone payments]

**Currency.** EUR (default) or [TODO[OPERATOR-brief-currency-alt] if other agreed].

**Payment cadence.** 50% on Acceptance, 50% within 30 days of Acceptance, unless milestone payments are agreed in §5.

**Invoicing.** Contractor sends invoice referencing this brief's `vendor_id` (assigned at engagement start) and the milestone(s) covered. Invoice format: PDF, EUR figures, contractor's tax ID, contractor's bank details.

**Late payment.** If we go over the 30-day cadence, we add 1% per week of delay to the outstanding balance, applied automatically. We do not require the contractor to chase us.

## 7. Communication norms

**Primary channel.** Email (or Direct DM if the contractor's `current_distance_band` in `SOURCING_REGISTER.csv` is `N1`).

**Response SLA.** We respond to contractor questions within 1 business day during the engagement window. Outside the window (weekends, holidays), best-effort.

**Asynchronous-first.** Avoid synchronous calls unless they unblock something. When a call is needed, the contractor proposes 2 - 3 windows and we pick.

**No surprises rule.** If anything material changes on either side (scope, timeline, blockers), we surface it within 24 hours. Surprises kill trust faster than honest delays.

## 8. Acceptance criteria

The engagement closes when:

1. The deliverable passes all quality gates in §3.
2. Final payment lands per §6.
3. Both parties confirm the engagement is closed (a one-line email is enough).

After successful closure, the contractor's `quality_band` in `SOURCING_REGISTER.csv` is updated by Holistika; this drives whether we engage them again. A-band contractors are invited to repeat-hire conversations within 30 days; B-band stay on the rolling register; C-band move to backup-only.

## 9. Cross-references

- [`SOURCING_REGISTER.csv`](../../../../../compliance/dimensions/SOURCING_REGISTER.csv) — your row in our vendor register; you will see your `vendor_id` quoted in invoices.
- [`SOP-HLK_LOCALISATION_001.md`](../../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md) — locale rules.
- [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md) — voice rules.
- [`BRAND_JARGON_AUDIT.md`](../../../Marketing/Brand/BRAND_JARGON_AUDIT.md) — jargon-free rule.
- [Touchpoint kit cell `PERSONA-VENDOR-OUTBOUND` × `CHAN-DIRECT-DM`](../../../../../v3.0/_assets/touchpoint-kit/PERSONA-VENDOR-OUTBOUND/CHAN-DIRECT-DM/intro_message_en.md) — first-touch outbound message that links to this brief.
