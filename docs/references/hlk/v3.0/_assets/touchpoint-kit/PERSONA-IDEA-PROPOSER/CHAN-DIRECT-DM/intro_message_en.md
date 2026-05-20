---
language: en
persona_id: PERSONA-IDEA-PROPOSER
channel_id: CHAN-DIRECT-DM
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
distance_variants_covered: [N1, N2]
last_review: 2026-04-30
---

## Variant — N1 (known person with project idea)

Hi [Name],

Thanks for sharing the idea. Before committing anything, give me three lines of context so I can understand the angle:

1. Demand: are there actual customers asking for this, or is it your hypothesis?
2. Your role: how do you fit inside the idea (customer, seller, operator, investor)?
3. Timeline: what's the urgency for you?

With that I'll tell you whether it makes sense for Holistika (service, joint-equity, honest decline) and propose the next step. If the idea fits our joint-equity model, I'll send you the evaluation format we use.

— [Founder name]

> **Brand voice rule (BRAND_VOICE_FOUNDATION):** N1 known person — direct, no cushioning, three concrete questions. The relationship is the context; no need to introduce Holistika.

---

## Variant — N2 (idea proposer via known bridge)

Hi [Name],

[Bridge name] mentioned you have an idea that might fit what we do. Before I get into details, here's the compact format we use to evaluate opportunities — three questions:

1. Demand: actual customers asking, or hypothesis?
2. Your role: how do you fit inside the idea (customer, seller, operator, investor)?
3. Timeline: what's the urgency?

With that I'll tell you whether it fits Holistika (professional service, joint-equity, honest decline). If it fits, I'll send you the next-step format.

— [Founder name]
Holistika Research

> **Brand voice rule:** N2 idea-proposer — open by naming the bridge, three questions, same format as N1 with a bit more context.

---

> **Operator note (not sent).** If after the three answers the idea fits, route to `PERSONA-PARTNER-JOINT-EQUITY` (Channel 6) or `PERSONA-CUSTOMER-SERVICE-PROSPECT` as appropriate. Capture in GOI/POI with `distance_band=N1|N2`.
