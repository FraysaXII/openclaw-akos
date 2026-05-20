---
language: es
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
brand_voice: BRAND_SPANISH_PATTERNS
distance_variants_covered: [N1, N2]
last_review: 2026-04-30
---

## Variant — N1 (relación directa, contexto profundo)

Hola [Nombre],

Gracias por escribir. Lo dejo corto porque ya tenemos contexto compartido.

- Cómo estamos: [TODO[OPERATOR-state-current-funding-status]] — encantado de contarte dónde estamos hoy y dónde queremos llegar.
- Propongo: 30 min la semana que viene para repasar contigo el dossier de compañía (12 láminas) y la SSOT estratégica que acabamos de cerrar. Tras eso veremos si tiene sentido profundizar.

Hueco directo aquí: [Cal scheduling link]. O propónme tres ventanas y nos cuadramos.

Un saludo,
[Nombre del fundador]

> **Regla de voz (BRAND_SPANISH_PATTERNS):** N1 omite la cualificación inicial — la relación ya cualifica. Tono peer_consulting, "tú", apertura "Hola", cierre "Un saludo,".

---

## Variant — N2 (referencia warm, puente conocido)

Hola [Nombre],

[Nombre del puente] me sugirió ponerme en contacto contigo, y agradezco la introducción.

Para los primeros cinco minutos de contexto: Holistika es la compañía de ingeniería operativa que [Nombre del puente] conoce de [Contexto del puente]. Productizamos el método operativo en KiRBe SaaS + plataforma agentic MADEIRA; los ingresos hoy son servicio profesional y el puente al recurrente ya está construido en código.

Si después del resumen sigue siendo relevante, propongo 30 min para repasar el dossier de compañía (12 láminas) y la SSOT estratégica, y vemos si tiene sentido profundizar.

Hueco directo aquí: [Cal scheduling link]. O propónme tres ventanas y nos cuadramos.

Un saludo,
[Nombre del fundador]
Holistika Research

> **Regla de voz:** N2 abre **nombrando explícitamente al puente**. La credibilidad la lleva el puente; la especificidad refuerza la relación.

---

> **Nota operativa (no se envía).** Capturar el contacto en `GOI_POI_REGISTER.csv` en 24h con `distance_band=N2` y `bridge_via=<ref_id del puente>`. Si tras la primera llamada la relación pasa a directa, actualizar a `N1`.
