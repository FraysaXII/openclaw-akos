---
language: en
persona_id: PERSONA-VENDOR-OUTBOUND
channel_id: CHAN-DIRECT-DM
artifact_class: intro_message
brand_voice: BRAND_VOICE_FOUNDATION
distance_variants_covered: [N1, N3, N4]
last_review: 2026-04-30
---

## Variant — N1 (trusted vendor we've worked with before)

Hi [Name],

We have a brief for [discipline]. Attached is the structured brief — same template you've seen from us before:

- Deliverable: [concrete output]
- Timeline: [dates]
- Rate: [agreed rate or "rate to be confirmed via brief"]
- Quality gates: [acceptance criteria]
- Brand voice: [BRAND_VOICE_FOUNDATION | BRAND_SPANISH_PATTERNS | BRAND_FRENCH_PATTERNS] per locale

Reply with availability + an estimate; if we land on terms today, the brief becomes the engagement contract.

— [PMO contact / Founder]
Holistika Research

> **Brand voice rule (BRAND_VOICE_FOUNDATION):** N1 vendor — direct, structured-brief-first, fast-cycle. No need to re-establish credibility; the relationship is the credibility.

---

## Variant — N3 / N4 (cold vendor sourcing, no prior history)

Hi [Name],

I came across your work on [source: portfolio site / referral platform / search]. I have a one-off brief that may match what you do; I'm reaching out to a small number of professionals to get estimates.

Attached is the structured brief: deliverable, timeline, quality gates, brand voice rules, payment terms. The brief itself is the scope-of-work — please reply with:

1. Whether you can deliver as-described (yes / partial / no)
2. Hourly rate or fixed-fee estimate
3. Estimated timeline given current bandwidth
4. Two reference links from comparable work

If we land on terms, the brief becomes the engagement contract. If not, no harm — the brief stays a clean ask.

— [PMO contact / Founder]
Holistika Research

> **Brand voice rule:** N3 / N4 vendor — transparent about the cold sourcing pattern, structured brief-as-contract, no salesy back-and-forth. Specificity buys trust faster than warmth here.

---

> **Operator note (not sent).** Capture vendor in `SOURCING_REGISTER.csv` at first reply with `distance_band_at_first_contact=N3|N4`, `current_distance_band=N3|N4`. After successful first engagement, manually update `current_distance_band` and `quality_band` per the SOP cadence.
