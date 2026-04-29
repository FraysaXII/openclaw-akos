---
status: active
role_owner: Compliance
area: Operations / PMO
entity: Holistika Research
program_id: PRJ-HOL-FOUNDING-2026
plane: advops
topic_ids:
  - topic_enisa_dossier_es
parent_topic: topic_enisa_evidence
language: es
artifact_role: canonical
intellectual_kind: founder_dossier
authority: Operator (Compliance + Legal Counsel)
last_review: 2026-04-29
sources:
  - docs/references/hlk/compliance/GOI_POI_REGISTER.csv
  - docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv
  - docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv
  - docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv
  - docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv
  - docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md
  - docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/Taxes/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md
  - docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/topic_enisa_evidence.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md
---

# Dossier ENISA — Holística Research

> **Documento canónico (Initiative 27 P2).** Fuente única de verdad para la versión española del dossier de certificación ENISA — Empresa Emergente del programa `PRJ-HOL-FOUNDING-2026`. Cada afirmación cita la fila CSV (`Q-…`, `INST-…`, `GOI-…`, `POI-…`) o el documento canónico que la respalda. Las decisiones que requieren confirmación del fundador se marcan explícitamente como `TODO[OPERATOR]` con la recomendación interna correspondiente. La versión PDF se genera por `scripts/render_dossier.py` invocando `akos.hlk_pdf_render.render_pdf_branded(profile="dossier")`.

---

## 1. Resumen ejecutivo

Holística Research es una compañía de **inteligencia corporativa e ingeniería empresarial** con una metodología propia, escalable y habilitada por tecnología. El programa `PRJ-HOL-FOUNDING-2026` cubre la constitución del primer vehículo legal en España, en paralelo con la candidatura a la certificación ENISA — Empresa Emergente.

La tesis central, sostenida por la base operativa actual (cinco entregas de producción documentadas en el Apéndice C) y por el corpus metodológico interno (`AKOS`, marcos de análisis, biblioteca de SOPs), es que el primer vehículo no debe encajarse como consultoría genérica: la oferta combina **investigación**, **ingeniería de procesos**, **arquitectura tecnológica** y **una ruta clara hacia productización** (la plataforma KiRBe ya en producción para uso interno). Esta postura es deliberada y está alineada con el rationale recogido en `FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md`.

El dossier se organiza en cuatro pilares (Mercantil / Mercado / Financiación / Operativa), seguidos de cinco apéndices: cuestionario abierto a asesores (Apéndice A — 13 preguntas), instrumentos archivados (Apéndice B), capacidades demostradas (Apéndice C), glosario cruzado (Apéndice D) y trazabilidad (Apéndice E).

> **Estado del programa**: P1 — Listo para auditoría externa. La firma en notaría queda condicionada al cierre por escrito de las cinco preguntas críticas marcadas como `before_signing` en `ADVISER_OPEN_QUESTIONS.csv` (ver Apéndice A). La candidatura ENISA no es prerrequisito de la constitución, pero la coherencia entre `objeto social`, `CNAE` y narrativa de innovación es trabada desde el día 1 (ver §2 y `Q-LEG-001`).

### 1.1 Tesis breve para la persona certificadora

Cuatro frases para abrir el expediente:

1. La sociedad se constituye como vehículo único, fundador-líder, con `objeto social` que recoge tres ejes (investigación, ingeniería empresarial, ingeniería de procesos) y un eje opcional para futura productización (`FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md`).
2. La innovación no es declarativa: una pila de cinco entregas de producción ya operativas ([Apéndice C](#9-apendice-c-capacidades-demostradas)) acredita la capacidad técnica, los marcos de calidad (CI multi-job, e2e, observabilidad, RBAC) y la transición consultoría → SaaS productizado en curso (KiRBe).
3. La escalabilidad es estructural: la metodología y la arquitectura de conocimiento (`AKOS`) están diseñadas para reuso entre clientes y entre disciplinas; los registros canónicos (CSV → mirrors Postgres) hacen la operación auditable.
4. La España-nexus se mantiene desde el día 1: domicilio social, plan de personal y banca operativa en territorio español; los fondos pre-incorporación están documentados en `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`.

---

## 2. Pilar I — Mercantil

### 2.1 Estructura societaria

Vehículo único, fundador-líder y socio único en arranque. La justificación (sección "Recommended First Entity" de `FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md`):

- la actividad sigue concentrada en el fundador y orientada a servicio + investigación;
- investigación e ingeniería tecnológica permanecen estratégicamente unidas;
- la complejidad estructural prematura (holding, multi-entidad) añade carga legal sin retorno hoy;
- la separación Research / Tech Lab queda como opción documentada para más adelante (`RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md`).

### 2.2 Objeto social y CNAE

Esta es la **decisión crítica del expediente**. La pregunta abierta correspondiente es `Q-LEG-001` (vinculada al asesor de constitución `GOI-ADV-ENTITY-2026` y al lead ENISA `POI-LEG-ENISA-LEAD-2026`).

Recomendación interna del programa, a confirmar por el fundador con el asesor jurídico:

- **CNAE primario**: `7219` — *Otra investigación y desarrollo experimental en ciencias naturales y técnicas*. Ancla la narrativa I+D que ENISA exige.
- **CNAE secundario**: `6202` — *Actividades de consultoría informática*. Recoge la realidad de ingresos por servicio actual sin desplazar la narrativa I+D.
- **CNAE a evitar**: `9511` — *Reparación de ordenadores y equipos periféricos*. Trampa documentada en la conversación con el banco (`Q-BNK-001`); nada en el `objeto social` debe ser interpretable como reparación.

Texto recomendado de `objeto social` (esqueleto interno; redacción final del notario):

> *Inteligencia corporativa, investigación aplicada e ingeniería empresarial, incluyendo el diseño y desarrollo de metodologías propias y herramientas tecnológicas que automatizan, instrumentan y escalan dichas actividades. Comprende la prestación de servicios de análisis estratégico, ingeniería de procesos y arquitectura organizacional, así como la investigación, desarrollo y comercialización de productos de software propios derivados de dicha actividad.*

<blockquote class="callout-operator">

**TODO[OPERATOR]** — Decisión del fundador (cierra `Q-LEG-001` antes de la firma).

- Opción A — `7219` primario + `6202` secundario, redacción I+D-céntrica (recomendación interna).
- Opción B — `6202` primario + `7219` secundario, redacción consultoría-céntrica.
- Opción C — paquete combinado con tercer CNAE (ej. `7022`) si el asesor lo justifica para la candidatura ENISA.

Confirmar la opción y pegar la redacción final aprobada por el asesor jurídico antes de la firma. La elección tiene impacto cruzado en `Q-BNK-001` (canal bancario debe contar la misma historia).

</blockquote>

### 2.3 Ruta de constitución

La pregunta abierta `Q-LEG-002` plantea CIRCE telemático vs notario ordinario. La pregunta `Q-LEG-003` examina cómo CIRCE limita la flexibilidad del `objeto social`. Recomendación interna: priorizar **fidelidad legal sobre velocidad** (sección "Default Recommendation" de `FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md`). Si CIRCE no permite una redacción amplia y precisa del `objeto social` (cláusula de productización + I+D), ir por notario ordinario.

### 2.4 Capital social inicial

`Q-LEG-004` examina la base legal del régimen de 1 EUR (formación sucesiva, obligación de reservas legales). Recomendación interna desde `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`: **no lanzar con caja efectivamente cero** cuando ya hay gasto recurrente conocido en infraestructura (≈ 150 EUR/mes en idle, 300–500 EUR/mes en uso pleno).

Heurística operativa interna (no es mínimo legal): mantener un colchón mínimo de **EUR 1.000** o aproximadamente **3× el burn mensual activo**, lo que sea mayor.

<blockquote class="callout-operator">

**TODO[OPERATOR]** — Decisión del fundador (capital social).

- Opción A — Capital nominal 1 EUR vía formación sucesiva. Optimiza caja en arranque; introduce obligación de reservas legales y fricción narrativa con bancos / certificadora.
- Opción B — Capital ≥ 3.000 EUR (suficiente para cubrir 6× burn idle + 1× burn activo). Quita fricción regulatoria, cuenta una historia de "lanzamos con runway".
- Opción C — Cifra intermedia (ej. 1.000–2.000 EUR) ajustada al colchón heurístico interno.

Confirmar la cifra y declararla en §4.1 antes de la firma. Cierra parcialmente `Q-LEG-004`.

</blockquote>

### 2.5 Gobierno y administración

Administrador único (fundador) en arranque. La pregunta `Q-LEG-005` solicita listar las restricciones que conviene **no asumir hoy** para no limitar una eventual estructura holding más adelante (cap-table, estatutos, drag-along, derechos de adquisición preferente). El asesor cierra esta pregunta con la documentación final de los estatutos.

---

## 3. Pilar II — Mercado

### 3.1 Tesis de innovación

(Reformulación en prosa de las secciones "Innovation Case" y "Working Innovation Narrative" de `ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`.)

Holística Research no vende dictamen experto puntual. La compañía construye un **método operativo estructurado** en el que:

- la arquitectura empresarial y el conocimiento de procesos se capturan de forma sistemática (registros canónicos, grafos de proceso, SOPs versionadas);
- la inteligencia artificial puede leer y operar **sobre** dicha arquitectura, no en lugar de ella (modelo "AKOS Strict": predicados explícitos, retrieval gobernado, sin hallucination latente);
- la metodología, la investigación y la entrega habilitada por software se combinan en una sola unidad de trabajo;
- la pila tecnológica subyacente está diseñada para soportar productización futura, en lugar de quedar permanentemente en operación manual.

Señales de respaldo estables (extraídas del propio expediente operativo):

- el fundador opera una base tecnológica desplegada desde 2023;
- existe ya un corpus operativo y de arquitectura suficiente para soportar entrega estructurada;
- existe demanda externa documentada de extensión software-céntrica de la metodología (ver Apéndice C — entregas a partner Websitz).

### 3.2 Posición en mercado

Holística Research ocupa una franja que la consultoría tradicional no cubre bien y que las empresas SaaS puras tampoco: análisis estructurado y entrega tecnológica gobernada **dentro del mismo proveedor**. ICP (Ideal Customer Profile) en operación actual:

- pyme tecnológica que necesita estructurar su operación interna antes de escalar;
- partner B2B (ej. integradores Shopify, agencias) que necesita capacidad de ingeniería de producto sin contratar plantilla in-house;
- candidato a producto SaaS interno (KiRBe — gestión de conocimiento gobernada).

### 3.3 PESTEL — factores materiales

<blockquote class="callout-operator">

**TODO[OPERATOR]** — Decisión del fundador (PESTEL).

Recomendación interna (semilla; el fundador confirma 2–3 factores realmente materiales antes de la firma): los siguientes dos son los más relevantes según el contexto del programa.

- **Político / Regulatorio (P)** — Ley de Startups (Ley 28/2022) + marco ENISA: ventana fiscal y administrativa favorable durante los primeros 5 años; obligación correlativa de mantener `objeto social` y CNAE coherentes con la narrativa I+D para no perder la calificación.
- **Tecnológico (T)** — Aceleración del despliegue de IA generativa en operación empresarial; abre oportunidad real para metodologías auditables (AKOS Strict) que separan el ruido de los productos productivos.

Pueden añadirse Económico (E — tipos / acceso a financiación pública), Social (S — talento técnico en España), Ambiental (E2 — huella infra) si el asesor los considera relevantes para la certificación.

</blockquote>

### 3.4 Por qué España / UE

España domicilia el vehículo desde el día 1 (sociedad mercantil registrada en jurisdicción `ES`, ver `INST-LEG-ESCRITURA-DRAFT-2026`). La operación mantiene España-nexus en infraestructura y banca, alineada con los criterios ENISA. La obligación de "workforce-in-Spain" se valida en el momento de la presentación efectiva (ver `Q-CRT-001`).

<blockquote class="callout-operator">

**TODO[OPERATOR]** — Plan de personal en España.

Línea base interna (semilla): "Single founder operando desde España. Crecimiento previsto a 2–3 ingenieros senior en territorio nacional durante el ejercicio 1 si entran financiación o cliente ancla; resto de la red de colaboradores externos contractualizados como freelance via España preferentemente." Confirmar/ajustar en redacción final antes del envío.

</blockquote>

---

## 4. Pilar III — Financiación

### 4.1 Modelo de capitalización

La política operativa interna está documentada en `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`. Resumen aplicado al arranque del programa:

| Concepto | Recomendación interna | Pregunta abierta |
|:---|:---|:---|
| Aportación inicial | Capital + posibles aportes en especie (infraestructura ya operativa) | `Q-LEG-004`, `Q-FIS-002` |
| Préstamo de socio | Disponible para financiar runway adicional cuando capital no llegue, **documentado por escrito** | — |
| Reembolso de gastos | Solo para gastos puntuales del fundador ya documentados con factura, **no como modelo recurrente** | `Q-FIS-002` |

### 4.2 Uso de fondos (planificación operativa)

Buckets internos a partir de `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`:

- **Infraestructura (idle)** — ≈ EUR 150 / mes (hosting, bases de datos, dominios, herramientas mínimas);
- **Infraestructura (uso pleno)** — EUR 300 a EUR 500 / mes (LLMs comerciales, GPU horas, servicios propios desplegados);
- **Asesoría externa** — partidas puntuales de honorarios legal / fiscal / certificación (ver Apéndice A);
- **Costes notariales y registrales** — pago único en constitución;
- **Marketing / GTM** — partida controlada hasta validar tracción comercial.

<blockquote class="callout-operator">

**TODO[OPERATOR]** — Decisión del fundador (presupuesto operativo).

Confirmar las cifras EUR exactas para los seis primeros meses, separadas por bucket. El dossier deja los rangos de la nota de capitalización como semilla; la redacción final debe sustituirlos por importes concretos antes del envío al asesor.

</blockquote>

### 4.3 Tratamiento de aportaciones del fundador

`Q-FIS-002` solicita la confirmación contable y fiscal del tratamiento de la infraestructura financiada por el fundador antes de la constitución (servidores GPU `ShadowGPU/RunPod`, dominios, suscripciones, equipos). Recomendación interna: tratarla como **aportación en especie capitalizable** en sede de constitución cuando los activos sean identificables, valorables y útiles para la actividad; el resto, como reembolso documentado de gastos.

### 4.4 Vínculo con ayudas ENISA

La narrativa de innovación + escalabilidad de §3.1 y §5 está construida deliberadamente para satisfacer los dos criterios ENISA centrales (art. 3 y 4 Ley 28/2022). El expediente no asume que ENISA financiará automáticamente: la candidatura es una **opción de extensión** del programa, no un prerrequisito del lanzamiento operativo.

---

## 5. Pilar IV — Operativa

### 5.1 Modelo de entrega (consultoría → producto)

El plano de entrega de Holística Research está documentado en el topic `topic_external_adviser_handoff` (Initiative 21 / 22) y se resume así:

- entrega actual = **investigación estructurada + ingeniería empresarial + ingeniería de procesos** facturada como servicio;
- entrega futura = **mismo método, productizado** vía la plataforma KiRBe (gestión de conocimiento auditable, ya en producción para uso interno);
- el puente entre ambos planos está implementado en software, no en presentaciones: el routing de billing entre `kirbe.*` y `holistika_ops.*` está documentado en el topic `topic_kirbe_billing_plane_routing` (Initiative 23 P6).

### 5.2 Stack tecnológico

Consolidado y comprobado en producción (ver Apéndice C para evidencia por entrega):

- **Frontend / web** — Next.js 14, React, Tailwind CSS, shadcn/Radix UI, multilingüe (en/es/fr) vía next-intl, Sentry, Playwright e2e;
- **API / backend** — FastAPI (Python 3.11+), validación Pydantic, observabilidad Logfire, dockerizado, despliegue en Cloud Run con Cloud Build CI;
- **Datos** — Supabase (Postgres con `pgvector`), búsqueda híbrida (semántica + keyword vía RRF), reranking con Cohere, sincronización proyectiva a Neo4j para grafos de conocimiento;
- **Productividad operativa** — n8n para flujos auditables, Stripe para billing y metering de uso, RBAC granular sobre Postgres con políticas RLS;
- **Gobernanza** — `AKOS` (este propio repositorio) como sistema de conocimiento canónico: registros CSV → mirrors Postgres → diagramas Mermaid versionados.

Punto crítico de marca: la pila no es retórica de pitch. Cada componente está acreditado por al menos una entrega productiva listada en el Apéndice C.

### 5.3 Gobernanza del conocimiento

El propio repositorio operativo (AKOS) demuestra el método: los hechos canónicos viven en CSVs versionados (`GOI_POI_REGISTER`, `ADVISER_OPEN_QUESTIONS`, `FOUNDER_FILED_INSTRUMENTS`, `PROGRAM_REGISTRY`, `TOPIC_REGISTRY`, `process_list`); los espejos Postgres se mantienen en sincronía mediante una sonda periódica (`scripts/probe_compliance_mirror_drift.py`); los diagramas Mermaid son fuente única de verdad y se renderizan deterministamente (`scripts/render_km_diagrams.py`); los topics se cruzan en un grafo navegable (`docs/references/hlk/v3.0/_assets/_meta/topic_graph.png`).

### 5.4 Plan de personal en España

Ver `TODO[OPERATOR]` en §3.4. Línea base: fundador único operando desde España; crecimiento condicionado a financiación / cliente ancla.

---

## 6. Apéndice A — Cuestionario abierto a asesores (Q-Tracker)

Trece preguntas registradas en `ADVISER_OPEN_QUESTIONS.csv` para `program_id = PRJ-HOL-FOUNDING-2026`. Las cinco con `target_date = before_signing` son críticas para no firmar a ciegas.

### A.1 Disciplina LEG (Asesoría Jurídica)

| Q-id | Pregunta | Target | POI | GOI |
|:---|:---|:---|:---|:---|
| `Q-LEG-001` | Confirmar texto exacto del `objeto social` y CNAE (con justificación) antes de la firma. | `before_signing` | `POI-LEG-ENISA-LEAD-2026` | `GOI-ADV-ENTITY-2026` |
| `Q-LEG-002` | Recomendación: constitución telemática CIRCE vs notario ordinario (incluyendo plazos y perfil de honorarios). | `before_signing` | — | `GOI-ADV-ENTITY-2026` |
| `Q-LEG-003` | Trade-offs CIRCE frente a `objeto social` a medida (impacto en flexibilidad y modificaciones). | `before_signing` | — | `GOI-ADV-ENTITY-2026` |
| `Q-LEG-004` | Base legal de la ruta de capital social de 1 EUR (incluyendo obligaciones de reserva). | `before_signing` | — | `GOI-ADV-ENTITY-2026` |
| `Q-LEG-005` | Restricciones de estructura holding a evitar hoy (decisiones que limitarían un holding futuro). | `before_signing` | — | `GOI-ADV-ENTITY-2026` |

### A.2 Disciplina FIS (Asesoría Fiscal)

| Q-id | Pregunta | Target | POI | GOI |
|:---|:---|:---|:---|:---|
| `Q-FIS-001` | Beneficio exacto de pluriactividad / cuota aplicable (asunciones y dependencias). | `before_signing` | `POI-LEG-FISCAL-LEAD-2026` | `GOI-ADV-ENTITY-2026` |
| `Q-FIS-002` | Tratamiento de la infraestructura financiada por el fundador (pre vs post incorporación). | `before_signing` | `POI-LEG-FISCAL-LEAD-2026` | — |

### A.3 Disciplina IPT (Propiedad Intelectual)

| Q-id | Pregunta | Target | POI | GOI |
|:---|:---|:---|:---|:---|
| `Q-IPT-001` | Desglose de tasas de marca (oficiales vs servicio) por territorio y clase para la estrategia de registro elegida. | `tbd` | — | `GOI-ADV-ENTITY-2026` |

### A.4 Disciplina BNK (Banca de Constitución)

| Q-id | Pregunta | Target | POI | GOI |
|:---|:---|:---|:---|:---|
| `Q-BNK-001` | Coordinación CNAE / constitución entre banca y asesoría de certificación: quién propone el CNAE final y cómo se mantiene coherente con `objeto social`. | `before_signing` | `POI-BNK-DESK-LEAD-2026` | `GOI-BNK-INC-2026` |

### A.5 Disciplina CRT (Certificación Empresa Emergente)

| Q-id | Pregunta | Target | POI | GOI |
|:---|:---|:---|:---|:---|
| `Q-CRT-001` | Reparto documental ENISA: qué artefactos produce el fundador vs el asesor (matriz de responsabilidad). | `tbd` | `POI-LEG-ENISA-LEAD-2026` | `GOI-ADV-ENTITY-2026` |
| `Q-CRT-002` | Entrega del plan de negocio consolidado + análisis PESTEL al asesor de certificación. | `asap` | `POI-LEG-ENISA-LEAD-2026` | `GOI-ADV-ENTITY-2026` |
| `Q-CRT-003` | Sección de financiación del plan ENISA: narrativa mínima creíble (asesor revisa con un encuadre más positivo). | `tbd` | `POI-LEG-ENISA-LEAD-2026` | `GOI-ADV-ENTITY-2026` |

---

## 7. Apéndice B — Instrumentos archivados / en curso

Una entrada activa en `FOUNDER_FILED_INSTRUMENTS.csv` para el programa `PRJ-HOL-FOUNDING-2026`:

| Instrument id | Tipo | Jurisdicción | Estado | Almacenamiento | Owner | Counterparty |
|:---|:---|:---|:---|:---|:---|:---|
| `INST-LEG-ESCRITURA-DRAFT-2026` | escritura de constitución | ES | draft | off-repo (operator Drive) | Legal Counsel | `GOI-ADV-ENTITY-2026` |

Próximas filas previstas (no presentes hasta que existan): `INST-LEG-ESCRITURA-SIGNED-…`, `INST-LEG-PODERES-…`, `INST-FIS-MOD036-…`, `INST-CRT-ENISA-…`. Cada una se materializa como nueva fila en el CSV en cuanto el documento exista.

---

## 8. Apéndice C — Capacidades demostradas

> **Lectura para la persona certificadora.** Esta sección no son referencias de pitch ni capturas de marketing. Son cinco entregas de software de producción, accesibles bajo NDA si el asesor lo requiere, que acreditan la pila técnica, la disciplina de calidad y la capacidad de delivery de Holística Research. Cada tarjeta cita las características objetivas del repositorio (tests, CI gates, integraciones de terceros, despliegue) y deja los nombres de partners y URLs públicas como `TODO[OPERATOR]` para que el fundador decida qué desclasificar en el envío.

### 8.1 Producto 1 — Holistika Boilerplate (sitio público + intake CRM/ERP)

| | |
|:---|:---|
| **Naturaleza** | Sitio marketing + intake comercial + lead-routing |
| **Stack** | Next.js 14, React, Tailwind CSS, shadcn/Radix UI |
| **Internacionalización** | next-intl, tres idiomas (en / es / fr) en producción |
| **Integraciones** | Stripe (gateway de cobro), Google Tag Manager, Meta Pixel, Sentry (error tracking), Supabase (lead store) |
| **Calidad** | Playwright e2e, suite de pruebas de integración, despliegue en Vercel con CI |
| **Marca** | Fuente única de los tokens visuales del programa (teal / amber / warm-slate; spotlight + grid hero; Inter) |
| **Visibilidad pública** | `holistikaresearch.com` (TODO[OPERATOR]: confirmar si se cita la URL en el envío al asesor) |

Lectura ENISA: acredita que la compañía construye y opera **su propio canal de adquisición** sobre la misma pila que vende a clientes; no externaliza su infra de marca. La propia identidad visual de este dossier hereda los tokens de este repositorio (ver `BRAND_VISUAL_PATTERNS.md`).

### 8.2 Producto 2 — HLK ERP (operación interna)

| | |
|:---|:---|
| **Naturaleza** | ERP interno multi-módulo (gestión operativa propia) |
| **Stack** | Next.js 14, React, Tailwind CSS, shadcn/Radix (≈ 53 componentes integrados) |
| **Theming** | Multi-tema con siete modos (light, dark, dark-blue, light-blue, brown, white …); gobierno de tokens centralizado |
| **Integraciones** | Stubs de API contra KiRBe SaaS para gestión de conocimiento operativa |
| **Calidad** | typecheck estricto, lint, Jest unit, cobertura, gates de CI completos |
| **Visibilidad pública** | Privado (TODO[OPERATOR]: decidir si se ofrece walkthrough bajo NDA) |

Lectura ENISA: la consultora **opera con su propio producto** (dogfooding). El método se valida internamente antes de exponerlo a clientes externos.

### 8.3 Producto 3 — KiRBe SaaS (plataforma de gestión de conocimiento gobernada)

| | |
|:---|:---|
| **Naturaleza** | SaaS B2B de gestión de conocimiento empresarial con búsqueda semántica gobernada |
| **Stack** | FastAPI (Python 3.11), Pydantic, Supabase (Postgres + `pgvector`), 20+ routers HTTP |
| **Recuperación** | Búsqueda híbrida (semántica + keyword, fusionada vía RRF); reranking con Cohere; modo "Strict" sin recuperación latente |
| **Multitenancy** | RBAC granular por organización, RLS sobre Postgres, audit trail de consultas |
| **Billing** | Stripe metered billing con events de uso; sincronización con `holistika_ops.*` (ver topic `topic_kirbe_billing_plane_routing`) |
| **Despliegue** | Docker, Google Cloud Build → Cloud Run, observabilidad Logfire, sincronización proyectiva Neo4j para grafos de conocimiento |
| **Gobernanza interna** | SOPs de retrieval + SOPs de gobernanza versionadas en repositorio |
| **Visibilidad pública** | Producto en operación (TODO[OPERATOR]: confirmar URL pública si procede) |

Lectura ENISA: este producto **es la materialización software** de la metodología. Es la prueba de la transición consultoría → producto sin necesidad de un cambio narrativo. El topic `topic_kirbe_billing_plane_routing` documenta el routing real de billing entre planos.

### 8.4 Producto 4 — Use Case Holistika × Websitz (entrega para partner B2B Shopify)

| | |
|:---|:---|
| **Naturaleza** | App de carrito-bundle para partner B2B sobre Shopify |
| **Stack admin** | Remix + React, Shopify Polaris UI, Prisma + Postgres |
| **Stack storefront** | Vanilla JS + Liquid (extensión de tema Shopify) |
| **Internacionalización** | Seis idiomas en producción (en, es, fr, de, it, pt) |
| **Calidad** | Vitest unit + Playwright e2e (≈ 91 + 30 tests entre admin y storefront); CI multi-job; consideraciones Lighthouse |
| **Despliegue** | Vercel para el panel admin; extensión publicada en el ecosistema Shopify |
| **Partner** | TODO[OPERATOR]: nombre del partner si se desclasifica al asesor |

Lectura ENISA: acredita la capacidad de **operar como ingeniería externalizada para terceros con calidad de producto**, no en modo project-based ad-hoc. El partner entrega esto a sus propios clientes finales.

### 8.5 Producto 5 — Use Case Rushly (scaffold de SaaS para partner B2B)

| | |
|:---|:---|
| **Naturaleza** | SaaS B2B para marcas de e-commerce + operadores de vídeo (en fase de diseño con scaffold operativo) |
| **Estructura** | Monorepo (npm workspaces, TypeScript strict), separación clara API + worker |
| **Datos / queue** | Cloudflare R2 (storage), Mux (vídeo), BullMQ + Redis (jobs), Supabase (Postgres + `pgvector` + Auth JWT) |
| **Calidad** | Multi-job CI, contratos de tipo estrictos, governance docs versionados |
| **Estado** | Fase de diseño con arquitectura ya congelada y scaffold productivo |
| **Partner** | TODO[OPERATOR]: nombre del partner si se desclasifica al asesor |

Lectura ENISA: acredita el patrón "compliance-aware product program" — la disciplina de planificar, congelar arquitectura y poner CI antes de codificar fuerte. Es la metodología Holística aplicada al diseño de un producto de partner.

### 8.6 Lectura agregada

Los cinco productos comparten **la misma pila** que el dossier presenta en §5.2 y respaldan la misma metodología. No son trabajos disconexos: son la misma estrategia de ingeniería aplicada a distintos contextos (sitio propio, ERP interno, producto SaaS propio, entrega a partner Shopify, scaffold para partner SaaS). La velocidad de entrega es alta y la trazo metodológico es atestable; los plazos exactos quedan como observación del fundador (no figuran como afirmaciones objetivas en este expediente).

---

## 9. Apéndice D — Glosario cruzado

Para términos transversales del dossier (`POI`, `GOI`, `lens`, `sensitivity`, `sharing_label`, `discipline_id`, `program_id`, `topic_id`, `plane`), ver `docs/reference/glossary-cross-program.md`. Esta sección queda como puntero deliberado: el glosario es cross-program y se mantiene fuera del programa para evitar duplicación al crecer la cartera de programas.

---

## 10. Apéndice E — Trazabilidad y procedencia

- **Generador**: este `dossier_es.md` es la fuente única de verdad. La versión PDF se produce por `scripts/render_dossier.py` invocando `akos.hlk_pdf_render.render_pdf_branded(profile="dossier")`.
- **Topic registry**: el dossier figura como `topic_id = topic_enisa_dossier_es`, hijo de `topic_enisa_evidence`, en `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv`.
- **Etiquetas de difusión**: `internal_only` para borradores; `counsel_and_named_counterparty` para envío al asesor de certificación; `counsel_ok` solo después de redactar las cinco filas TODO[OPERATOR].
- **Sensibilidad de las filas referenciadas**: las identidades reales (nombres, correos, teléfonos) se mantienen off-repo y se citan únicamente vía `ref_id` (`POI-…`, `GOI-…`). El operador resuelve la dirección real solo en el momento del envío SMTP.
- **Hashes**: el script `scripts/render_dossier.py` captura `sha256(.md)`, `sha256(.pdf)`, `sha256(.docx)` al renderizar. Los hashes se registran en el informe UAT correspondiente (`docs/wip/planning/24-hlk-communication-methodology/reports/uat-adviser-email-sent-2026-04-29.md`).
- **Reglas de compliance aplicables**: `.cursor/rules/akos-governance-remediation.mdc`, `.cursor/rules/akos-holistika-operations.mdc`, `.cursor/rules/akos-planning-traceability.mdc`.
