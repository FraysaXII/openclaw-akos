---
language: es
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
brand_voice: BRAND_SPANISH_PATTERNS
distance_variants_covered: [N4]
last_review: 2026-04-30
---

## Variant — N4 (talento frío vía formulario web)

Hola [Nombre],

Gracias por escribir. No tenemos contratación abierta para roles fijos hoy, pero mantenemos un registro rotativo de profesionales — diseñadores, desarrolladores, marketers, traductores, asesores — a los que contratamos por hora cuando llega un encargo que encaja.

Si te interesa, responde con estos seis puntos:

1. Disciplina (diseño / desarrollo / marketing / redacción / traducción / asesoría / otro)
2. Idiomas en los que trabajas (EN / ES / FR / otros)
3. Banda horaria en la que operas
4. Rango de tarifa por hora que buscas
5. Enlace a portfolio o 2 - 3 muestras representativas
6. Una referencia escrita (enlace o contacto que podamos verificar)

Te añadimos al registro y te contactamos cuando llegue un encargo que encaje. Normalmente trabajamos con el [Outbound Brief template](../../../../Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_es.md) para que el alcance, los criterios de calidad y las condiciones de pago estén claros desde el primer día.

Un saludo,
[Contacto PMO]
Holistika Research

> **Regla de voz (BRAND_SPANISH_PATTERNS):** N4 talento — peer_consulting, "tú", apertura "Hola", cierre "Un saludo,". Honesto sobre el modelo de registro rotativo (no prometer contratación inmediata).

---

> **Nota operativa (no se envía).** Capturar al candidato en `SOURCING_REGISTER.csv` con `distance_band_at_first_contact=N4` y `quality_band` vacío hasta primer encargo. Si el portfolio impresiona, derivar a llamada de 15 min con el fundador.
