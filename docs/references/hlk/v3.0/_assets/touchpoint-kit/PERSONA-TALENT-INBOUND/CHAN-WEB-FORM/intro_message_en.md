---
language: en
persona_id: PERSONA-TALENT-INBOUND
channel_id: CHAN-WEB-FORM
output_type_source: OT-PROSE-MARKDOWN
output_type_render: OT-PROSE-MARKDOWN
artifact_class: AC-INTRO-MESSAGE
component_primitive_inventory:
  - CP-GREETING
  - CP-BODY
  - CP-CTA
  - CP-SIGNATURE
layered_architecture_version: D-IH-86-BB
brand_voice: BRAND_VOICE_FOUNDATION
distance_variants_covered: [N4]
last_review: 2026-04-30
---

## Variant — N4 (cold talent inbound via web form)

Hi [Name],

Thanks for the message. We're not actively hiring at fixed-role headcount, but we keep a rolling sourcing register of professionals — designers, developers, marketers, translators, advisors — who can be engaged hourly when a brief lands that matches.

If that interests you, please reply with:

1. Discipline (designer / developer / marketer / writer / translator / advisor / other)
2. Languages you work in (EN / ES / FR / other)
3. Time-zone band you operate in
4. Hourly-rate range you target
5. A portfolio link or 2 - 3 representative work samples
6. One written reference (link or contact we can verify)

We'll add you to the sourcing register and reach out when a brief fits. We typically engage via the [Outbound Brief template](../../../../Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_en.md) so the scope, quality gates, and payment terms are clear from day one.

— [PMO contact]
Holistika Research

> **Brand voice rule (BRAND_VOICE_FOUNDATION):** N4 talent inbound — peer-grade, structured ask, transparent about the sourcing model. No false promise of immediate engagement; honest about the rolling-register pattern.

---

> **Operator note (not sent).** When the talent provides answers 1-6, capture them in `SOURCING_REGISTER.csv` with `distance_band_at_first_contact=N4` and `quality_band` initially blank (set after a first engagement). If a portfolio impresses, route to founder for a 15-min screening call.
