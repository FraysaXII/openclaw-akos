---
language: es
persona_id: PERSONA-ADVISOR-REFERRAL
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
brand_voice: BRAND_SPANISH_PATTERNS
distance_variants_covered: [N1, N2]
last_review: 2026-04-30
---

## Variant — N1 (asesor con relación directa)

Hola [Nombre],

Gracias por la disponibilidad. Comparto el alcance compacto para que entremos rápido en materia:

- Tema: [tema concreto del asesor — fiscal, legal, ENISA, banca, IP, etc.]
- Estado: [estado actual / pregunta abierta]
- Documentación adjunta: [adjunto] (apéndice de evidencias para asesoría externa)

Propongo 30 min en cualquier hueco que te encaje. Si prefieres respuesta por escrito antes de la llamada, dime y la preparo.

Un saludo,
[Nombre del fundador]
Holistika Research

> **Regla de voz (BRAND_SPANISH_PATTERNS):** N1 con asesor — directo, profesional, sin cushioning. Adjunta el dossier técnico desde el primer mensaje.

---

## Variant — N2 (asesor referido, puente conocido)

Hola [Nombre],

[Nombre del puente] me ha dicho que serías la persona adecuada para tratar [tema del asesor]. Agradezco la introducción.

Contexto rápido para empezar:

- Empresa: Holistika Research, compañía de ingeniería operativa con sede en Madrid; en proceso de constitución como Empresa Emergente.
- Tema concreto: [tema del asesor, p.ej. fiscal, legal, ENISA, banca]
- Documentación: adjunto el apéndice de evidencias estructurado para asesoría externa.

Propongo 30 min en una ventana de la semana que viene. Si prefieres respuesta por escrito antes de la llamada, lo preparo en formato Q&A para que sea más eficiente.

Un saludo,
[Nombre del fundador]
Holistika Research

> **Regla de voz:** Asesor referido — abrir nombrando al puente, contexto rápido en bullet, propuesta de seguimiento eficiente. Tono `formal_legal` o `peer_consulting` según el voice_register del POI en GOI/POI.

---

> **Nota operativa (no se envía).** Si el asesor solicita material adicional, derivar a `dossier_es.md` de la evidencia ENISA en `_assets/advops/2026-holistika-incorporation/enisa_evidence/`. Registrar al asesor en `GOI_POI_REGISTER.csv` con `class=external_adviser`, `distance_band=N2`, `bridge_via=<puente>`.
