---
language: es
status: active
template_kind: outbound_brief
role_owner: PMO
area: Operations / PMO
entity: Holistika Research
authority: Founder + PMO
last_review: 2026-04-30
derived_from: docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_en.md
---

# Brief de encargo — PLANTILLA (español)

> **Nota operativa.** Plantilla canónica para contratar profesionales externos (diseño, desarrollo, marketing, traducción, asesoría). El brief es el contrato del encargo — una vez firmado/acordado, no hace falta SoW separado. La versión canónica en inglés está en [`TEMPLATE_OUTBOUND_BRIEF_en.md`](TEMPLATE_OUTBOUND_BRIEF_en.md). Per [`SOP-HLK_LOCALISATION_001.md`](../../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md), reescritura por locale (no traducción literal). Voz adaptada según `BRAND_SPANISH_PATTERNS.md` (peer_consulting, "tú", apertura "Hola", cierre "Un saludo,").

---

## 1. Contexto

**Quiénes somos.** Holística Research es una empresa española de ingeniería operativa. Productizamos nuestro propio método en KiRBe SaaS y la plataforma agentic MADEIRA. Operamos sobre cientos de artefactos canónicos gobernados (registros de procesos, validadores, sondas de drift); la voz de marca está codificada en [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md) y [`BRAND_SPANISH_PATTERNS.md`](../../../Marketing/Brand/BRAND_SPANISH_PATTERNS.md).

**Por qué este encargo.** [TODO[OPERATOR-brief-context] — un párrafo: qué iniciativa, por qué ahora, qué papel juega el entregable en el conjunto]

**Material de referencia.** [Lista de 1 - 3 documentos que el contratista debe leer antes de empezar]

## 2. Entregable

**Output concreto.** [TODO[OPERATOR-brief-deliverable] — una frase]

**Formato y nomenclatura.** [Requisitos de formato; ej. ".fig + exportación PNG/SVG; nombres `slide-NN-<descriptor>.svg`"]

**Cantidad y granularidad.** [Cuántas unidades; qué cuenta como una]

**Fuera de alcance.** [Lo que el brief explícitamente NO cubre]

## 3. Criterios de calidad

El entregable pasa la revisión solo cuando se cumplen TODOS:

- **Cumplimiento de voz de marca.** Cumple [`BRAND_SPANISH_PATTERNS.md`](../../../Marketing/Brand/BRAND_SPANISH_PATTERNS.md) y la voz fundacional cuando aplique.
- **Cumplimiento de especificación.** Coincide con la definición del entregable (formato, nomenclatura, cantidad).
- **Criterio de calidad 1.** [TODO[OPERATOR-brief-quality-1]]
- **Criterio de calidad 2.** [TODO[OPERATOR-brief-quality-2]]
- **Criterio de calidad 3.** [TODO[OPERATOR-brief-quality-3]]

Hacemos una ronda de revisiones si la primera entrega no cumple algún criterio. Tras la segunda ronda, el encargo se cierra (con pago de unidades entregadas) o continúa con alcance renegociado.

## 4. Reglas de voz de marca

Para entregables de prosa: [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md) (EN) / [`BRAND_SPANISH_PATTERNS.md`](../../../Marketing/Brand/BRAND_SPANISH_PATTERNS.md) (ES) / [`BRAND_FRENCH_PATTERNS.md`](../../../Marketing/Brand/BRAND_FRENCH_PATTERNS.md) (FR) según locale del output.

Para entregables visuales: [`BRAND_VISUAL_PATTERNS.md`](../../../Marketing/Brand/BRAND_VISUAL_PATTERNS.md). Los tokens (colores, tipografía, espaciado) no son negociables.

Para cualquier entregable: las superficies externas deben pasar el filtro de [`BRAND_JARGON_AUDIT.md`](../../../Marketing/Brand/BRAND_JARGON_AUDIT.md). Sin nombres internos en output dirigido al cliente.

## 5. Calendario y hitos

| Hito | Fecha | Entregable | Lado operador |
|:-----|:------|:-----------|:--------------|
| Kick-off | [TODO[OPERATOR-brief-kickoff-date]] | Brief firmado; material de referencia compartido | PMO confirma accesos |
| Punto medio | [TODO[OPERATOR-brief-midpoint-date]] | Borrador / entrega parcial | PMO + Brand Manager revisan |
| Entrega | [TODO[OPERATOR-brief-delivery-date]] | Entregable completo | Empieza la revisión de aceptación |
| Aceptación | en 3 días hábiles tras Entrega | Aprobado / revisiones / declinado | Trigger de pago |

Si el contratista anticipa retraso > 48h, lo notifica por escrito de inmediato. Renegociamos alcance o ampliamos plazo; no penalizamos avisos honestos a tiempo.

## 6. Condiciones de pago

**Tarifa.** [TODO[OPERATOR-brief-rate] — banda horaria, tarifa cerrada, o pagos por hito]

**Moneda.** EUR (por defecto) o [TODO[OPERATOR-brief-currency-alt] si otra acordada].

**Cadencia.** 50% en Aceptación, 50% en 30 días tras Aceptación, salvo pagos por hito acordados en §5.

**Facturación.** El contratista envía factura citando el `vendor_id` del brief (asignado al inicio del encargo) y los hitos cubiertos. Formato: PDF, importes EUR, NIF/CIF del contratista, datos bancarios.

**Pago tardío.** Si nos pasamos de los 30 días, añadimos 1% por semana de retraso al saldo pendiente, automático. No hace falta que el contratista nos persiga.

## 7. Normas de comunicación

**Canal principal.** Email (o Direct DM si `current_distance_band` del proveedor en `SOURCING_REGISTER.csv` es `N1`).

**SLA de respuesta.** Respondemos preguntas del contratista en 1 día hábil durante el encargo. Fuera (fines de semana, festivos), best-effort.

**Asíncrono primero.** Evitamos llamadas síncronas salvo que desbloqueen algo. Cuando hace falta llamada, el contratista propone 2 - 3 ventanas y elegimos.

**Sin sorpresas.** Si algo material cambia en cualquiera de las dos partes (alcance, plazo, bloqueadores), lo comunicamos en 24h. Las sorpresas matan la confianza más rápido que los retrasos honestos.

## 8. Criterios de aceptación

El encargo se cierra cuando:

1. El entregable pasa todos los criterios de calidad de §3.
2. El pago final aterriza según §6.
3. Ambas partes confirman cierre (un email de una línea basta).

Tras cierre exitoso, Holistika actualiza el `quality_band` del proveedor en `SOURCING_REGISTER.csv`; eso decide si volvemos a trabajar contigo. Banda A → invitación a conversaciones de re-encargo en 30 días; banda B → registro rotativo; banda C → solo backup.

## 9. Referencias cruzadas

- [`SOURCING_REGISTER.csv`](../../../../../compliance/dimensions/SOURCING_REGISTER.csv) — tu fila en el registro de proveedores; verás tu `vendor_id` citado en facturas.
- [`SOP-HLK_LOCALISATION_001.md`](../../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md) — reglas de locale.
- [`BRAND_SPANISH_PATTERNS.md`](../../../Marketing/Brand/BRAND_SPANISH_PATTERNS.md) — voz ES.
- [`BRAND_JARGON_AUDIT.md`](../../../Marketing/Brand/BRAND_JARGON_AUDIT.md) — regla jargon-free.
- [Touchpoint kit `PERSONA-VENDOR-OUTBOUND` × `CHAN-DIRECT-DM`](../../../../../v3.0/_assets/touchpoint-kit/PERSONA-VENDOR-OUTBOUND/CHAN-DIRECT-DM/intro_message_es.md) — mensaje de primer contacto.
