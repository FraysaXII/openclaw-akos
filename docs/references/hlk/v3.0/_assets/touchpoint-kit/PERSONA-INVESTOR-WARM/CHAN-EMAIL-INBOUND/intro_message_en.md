---
language: en
persona_id: PERSONA-INVESTOR-WARM
channel_id: CHAN-EMAIL-INBOUND
output_type_source: OT-PROSE-MARKDOWN
output_type_render: OT-PROSE-EMAIL-RICH
artifact_class: AC-INTRO-MESSAGE
component_primitive_inventory:
  - CP-GREETING
  - CP-CONTEXT-ANCHOR
  - CP-HOOK
  - CP-BODY
  - CP-CTA
  - CP-SIGNATURE
layered_architecture_version: D-IH-86-BB
brand_voice: BRAND_VOICE_FOUNDATION
distance_variants_covered: [N1, N2]
last_review: 2026-04-30
---

## Variant — N1 (direct relationship, deep context)

Hi [Name],

Thanks for the message. I'll keep it short since we already have shared context.

- We're at: [TODO[OPERATOR-state-current-funding-status]] — happy to walk you through where we are vs where we want to be.
- I propose: 30 min next week to walk you through the company-dossier deck (12 slides) plus the strategy SSOT we just shipped. After that we'll know whether a deeper conversation makes sense.

Pick a slot here: [Cal scheduling link]. Or pick three windows that work for you and I'll match.

— [Founder name]

> **Brand voice rule (BRAND_VOICE_FOUNDATION):** N1 messages skip the qualifying gate; the relationship is the qualifier. Tone is direct, peer-grade, scheduling-friendly.

---

## Variant — N2 (warm referral, bridge person known)

Hi [Name],

[Bridge name] mentioned you might be interested in what we're building at Holistika. Thanks for taking the time.

For the first 5 minutes of context: Holistika is the operations-engineering company [Bridge name] knows from [Bridge context]. We productize the operations method as KiRBe SaaS + MADEIRA agentic platform; today's revenue is service-led, with the bridge to recurring already built in code.

If that's still relevant after the 5-minute version, I'd suggest a 30-min call — I'll walk you through the 12-slide company dossier and the strategy SSOT, and we'll know whether a deeper conversation makes sense.

Pick a slot here: [Cal scheduling link]. Or pick three windows and I'll match.

— [Founder name], Holistika Research

> **Brand voice rule:** N2 opens by **explicitly naming the bridge** (no "a friend mentioned"). The bridge is the credibility carry. Specificity in the bridge mention strengthens the relationship.

---

> **Operator note (not sent).** Capture the contact in `GOI_POI_REGISTER.csv` within 24h with `distance_band=N2` and `bridge_via=<bridge POI ref_id>`. If after the first call the relationship escalates to direct (post-meeting follow-up cadence), update to `N1`.
