---
language: es
persona_id: PERSONA-VENDOR-OUTBOUND
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
brand_voice: BRAND_SPANISH_PATTERNS
distance_variants_covered: [N1, N3, N4]
last_review: 2026-04-30
---

## Variant — N1 (proveedor de confianza con historial)

Hola [Nombre],

Tenemos un encargo de [disciplina]. Adjunto el brief estructurado — misma plantilla que ya conoces:

- Entregable: [output concreto]
- Calendario: [fechas]
- Tarifa: [tarifa acordada o "tarifa a confirmar en el brief"]
- Criterios de calidad: [criterios de aceptación]
- Voz de marca: [BRAND_VOICE_FOUNDATION | BRAND_SPANISH_PATTERNS | BRAND_FRENCH_PATTERNS] según locale

Responde con disponibilidad + estimación; si cerramos términos hoy, el brief sirve de contrato de encargo.

Un saludo,
[Contacto PMO / Fundador]
Holistika Research

> **Regla de voz (BRAND_SPANISH_PATTERNS):** N1 proveedor — directo, brief-first, ciclo rápido. La relación ya es la credibilidad.

---

## Variant — N3 / N4 (proveedor en frío, sin historial)

Hola [Nombre],

He visto tu trabajo en [origen: portfolio / plataforma / búsqueda]. Tengo un encargo puntual que puede encajar con lo que haces; lo paso a un grupo pequeño de profesionales para recibir estimaciones.

Adjunto el brief estructurado: entregable, calendario, criterios de calidad, voz de marca, condiciones de pago. El brief es el alcance del trabajo — responde con:

1. Si puedes entregarlo tal y como está (sí / parcial / no)
2. Tarifa por hora o estimación cerrada
3. Calendario estimado dada tu disponibilidad actual
4. Dos referencias de trabajo comparable

Si cerramos términos, el brief sirve de contrato de encargo. Si no, sin problema — el brief queda como una petición clara.

Un saludo,
[Contacto PMO / Fundador]
Holistika Research

> **Regla de voz:** N3 / N4 proveedor — transparente sobre el modelo de sourcing en frío, brief-as-contract, sin negociación abierta. La especificidad genera confianza más rápido que la cordialidad.

---

> **Nota operativa (no se envía).** Capturar al proveedor en `SOURCING_REGISTER.csv` en primera respuesta con `distance_band_at_first_contact=N3|N4`, `current_distance_band=N3|N4`. Tras encargo exitoso, actualizar manualmente `current_distance_band` y `quality_band` según cadencia de la SOP.
