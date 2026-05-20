---
language: en
persona_id: PERSONA-INVESTOR-COLD
channel_id: CHAN-LINKEDIN-DM
output_type_source: OT-PROSE-MARKDOWN
output_type_render: OT-PROSE-DM
artifact_class: AC-INTRO-MESSAGE
component_primitive_inventory:
  - CP-GREETING
  - CP-CONTEXT-ANCHOR
  - CP-BODY
  - CP-CTA
  - CP-SIGNATURE
layered_architecture_version: D-IH-86-BB
brand_voice: BRAND_VOICE_FOUNDATION
distance_variants_covered: [N3, N4]
last_review: 2026-04-30
---

## Variant — N3 / N4 (cold investor inbound on LinkedIn)

Hi [Name],

Thanks for reaching out. To make sure we're a fit before scheduling time:

- Stage / sector: Holistika is a Spanish operations-engineering company productizing the same method we sell as a service (KiRBe SaaS, MADEIRA agentic platform). Pre-revenue at the SaaS line; service-revenue funded.
- Ticket band: not currently raising; if we do, the band will be in the EU SaaS seed range. Happy to talk anyway when fit is clear.
- Geography: Madrid · operating in EN/ES/FR.

If that aligns roughly with where you invest, send me a one-pager on your fund and I'll send a 12-page deck back. Otherwise, no harm — happy to keep in touch.

— [Founder name], Holistika Research

> **Brand voice rule (BRAND_VOICE_FOUNDATION):** peer-grade, specific, no salesy cushion. The cold response is short by design — qualification first, deck second.

---

> **Operator note (not sent).** If the LinkedIn message references a bridge person (warm), switch to the `PERSONA-INVESTOR-WARM × CHAN-EMAIL-INBOUND` cell instead. Capture the new contact in `GOI_POI_REGISTER.csv` with the assessed `distance_band` within 24h regardless of whether the conversation continues.
