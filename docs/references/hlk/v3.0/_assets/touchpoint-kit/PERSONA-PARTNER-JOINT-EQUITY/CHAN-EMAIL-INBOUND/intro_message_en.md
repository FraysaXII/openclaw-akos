---
language: en
persona_id: PERSONA-PARTNER-JOINT-EQUITY
channel_id: CHAN-EMAIL-INBOUND
artifact_class: intro_message
brand_voice: BRAND_VOICE_FOUNDATION
distance_variants_covered: [N2, N3]
last_review: 2026-04-30
---

## Variant — N2 (partner via known bridge)

Hi [Name],

[Bridge name] mentioned you have a SaaS hypothesis and you're looking for a team to build it in exchange for equity or revenue share. That's exactly the kind of engagement we keep in active pipeline.

To accelerate: here's the compact shape of how we run this model.

- Holistika delivers engineering + ongoing operation; the partner brings end-customer knowledge and demand.
- Frozen architecture before code; governed delivery with automated verification on every change.
- Compensation: equity / revenue share, calibrated case-by-case after fit assessment.
- Entry criteria (3-of-3 required): genuine recurring demand from the partner's customer base, ≥ 60% reuse of our existing stack, 24-month payback projection clearing our internal LTV:CAC threshold.

I propose 30 minutes to understand your product hypothesis and see whether the fit lands. If you prefer a written brief first, that also works.

— [Founder name]
Holistika Research

> **Brand voice rule (BRAND_VOICE_FOUNDATION):** N2 joint-equity — name the bridge, state the model in bullets, list the 3 entry criteria explicitly (non-negotiable). Peer-grade tone.

---

## Variant — N3 (partner via two-bridge chain)

Hi [Name],

This message reaches me via [closest bridge name], who in turn knows you through [further bridge / context]. Thanks for the chain of intros — I'll respond with the same compact format we use to evaluate joint-equity opportunities.

[Same body as N2 variant, with the introduction paragraph adjusted]

> **Brand voice rule:** N3 — make the chain explicit so the other side sees the relationship is mapped; rest of the message is N2-shape.

---

> **Operator note (not sent).** Capture the partner in `GOI_POI_REGISTER.csv` with `class=partner`, `distance_band=N2|N3`, `bridge_via=<closest bridge>`. Cross-reference the opportunity with `CHANNEL_STRATEGY.md` Channel 6.
