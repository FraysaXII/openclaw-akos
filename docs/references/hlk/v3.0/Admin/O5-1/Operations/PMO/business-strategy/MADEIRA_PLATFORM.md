---
language: es
status: active
role_owner: Founder + System Owner
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_madeira_platform
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: product_thesis
authority: Founder
last_review: 2026-04-30
deck_bound: true
deck_slides_consumed: ["04-solution", "05-method", "06-proof", "11-moat", "12-roadmap"]
---
# MADEIRA — Plataforma de agentes gobernada (segundo eje de producto)

## Lo que responde este documento

Qué es MADEIRA, por qué es el segundo eje de producto de Holística (junto con KiRBe), qué validación interna ya tiene hoy, y cómo recorre el camino comercial *interno → puente → SaaS*. Sirve de fuente para las diapositivas 04, 05, 06, 11 y 12 del dossier de compañía.

## 1. Qué es MADEIRA, en una frase

**MADEIRA es la capa de agentes estandarizados de Holística**: un marco operativo que estructura cómo los asistentes y agentes de inteligencia artificial obtienen su contexto, qué habilidades pueden ejecutar y cómo se comportan dentro de la operación de un cliente — todo gobernado por la misma disciplina que rige el resto del método.

Comparable, en categoría, a un Copilot o a un asistente Gemini empresarial — pero con dos diferencias que importan:

1. **Sourcing gobernado.** El contexto que ven los agentes no es un volcado de documentos. Es la misma capa de conocimiento canónico que utiliza el equipo humano: temas, hechos, fuentes, todo trazable.
2. **Comportamiento estandarizado.** Cada agente tiene un perfil de habilidades versionado, no una *prompt* improvisada. Cambiar un comportamiento es un cambio de versión, auditable y revertible.

## 2. Por qué ahora

El mercado de agentes empresariales en 2026 vive una tensión clara: las plataformas genéricas (Copilot, Gemini) ofrecen asistentes potentes pero con contexto débil; las soluciones a medida son potentes pero no escalan entre clientes. Holística llega con la respuesta operativa al medio: una plataforma genérica al usar, específica al contexto de cada cliente, gobernada por defecto.

La misma disciplina que ha permitido a Holística entregar cinco productos distintos sobre una sola pila técnica es la que permite a MADEIRA escalar a múltiples clientes sin reinventar el agente cada vez.

## 3. Evidencia interna ya disponible

MADEIRA no es una promesa: es un componente que ya opera dentro de Holística para productividad, investigación y entrega.

| Superficie interna | Evidencia |
|:-------------------|:----------|
| Documentación interna SOP | `SOP-MADEIRA_HLK_ERP_SHOWCASE_004.md`, `SOP-MADEIRA_ENVOYTECH_SHOWCASE_002.md` |
| Repositorio de plataforma | `Envoy Tech Lab/Repositories/platform/README.md` |
| Sección estratégica "Pensar en grande" | `Think Big/README.md` |
| Onboarding del programa KiRBe | `Admin/O5-1/People/programs/PRJ-HOL-KIR-2026/README.md` |
| Validación operativa | Holística usa MADEIRA en su propia entrega antes de venderla — la misma disciplina *internal-first* que aplicamos a KiRBe |

Todas las superficies anteriores son nombrables ante un auditor: el auditor puede leer las SOPs y verificar que MADEIRA no es marketing sino operación.

## 4. El camino comercial (hoy → puente → mañana)

| Fase | Quién paga | Qué entrega Holística | Qué demuestra |
|:-----|:-----------|:----------------------|:--------------|
| **Hoy — embebida en servicio** | Cliente del servicio profesional | Holística entrega ingeniería empresarial; MADEIRA está dentro de la entrega como capa operativa que acelera la propia entrega | El método llega al cliente con una capa agentic ya operativa, sin coste extra |
| **Puente — capa común con KiRBe** | Cliente KiRBe SaaS | Cuando el cliente accede a KiRBe, los agentes de MADEIRA son los que ejecutan búsqueda, re-clasificación y razonamiento sobre su corpus | KiRBe es el escaparate; MADEIRA es la maquinaria — cada cliente KiRBe es ya un cliente MADEIRA |
| **Mañana — SaaS independiente** | Empresas que necesitan una runtime de agentes con sourcing gobernado pero no necesitan KiRBe | Holística empaqueta MADEIRA como producto separado: runtime de agentes + plano de gobernanza + biblioteca de habilidades versionadas | Segundo eje de ingreso recurrente independiente del servicio profesional |

## 5. Diferenciación competitiva

| Dimensión | Plataforma genérica (Copilot, Gemini) | Solución a medida | MADEIRA |
|:----------|:--------------------------------------|:------------------|:--------|
| Velocidad de despliegue | Alta | Baja | Alta (KiRBe como base) |
| Contexto del cliente | Débil (documentos sueltos) | Fuerte (ad hoc) | Fuerte (mismo grafo de conocimiento que el equipo humano) |
| Gobernanza por defecto | No | A elección del cliente | Sí (capa AKOS) |
| Coste de migración entre clientes | N/A (no se migra) | Alto | Bajo (perfiles versionados, no *prompts* improvisados) |
| Capacidad de descalado limpio | Alta | Baja | Alta (un programa MADEIRA se da de baja en una sola operación gobernada) |

## 6. Por qué encaja con la narrativa ENISA

La certificación "Empresa Emergente" exige innovación, escalabilidad y presencia en España. MADEIRA refuerza los tres pilares:

- **Innovación.** Es un marco propio (no un *fork* de Copilot), construido sobre KiRBe + AKOS, y operativo internamente desde 2024.
- **Escalabilidad.** Cada nuevo cliente KiRBe es ya un cliente MADEIRA en el plano técnico; el camino a SaaS independiente es una empaquetación, no una nueva construcción.
- **Presencia en España.** Toda la operación, el equipo de ingeniería y la infraestructura son nacionales — la productización SaaS de MADEIRA no introduce dependencias geográficas nuevas.

## 7. Decisión pendiente

> **Pregunta abierta para confirmación del fundador**
> TODO[OPERATOR-madeira-saas-window] — ventana de productización de MADEIRA como SaaS independiente: 6 meses (agresivo, exige equipo dedicado), 12 meses (base, en paralelo con tracción KiRBe), 18 meses (conservador, post-tracción KiRBe estable). La elección depende de la velocidad real de cierre del primer cliente KiRBe externo de pago.

## Deck-bound facts

Estos son los valores que las diapositivas del dossier citan; cualquier cambio aquí debe ir acompañado de un re-render del deck (`py scripts/build_company_deck.py && py scripts/export_company_deck_pdf.py`).

```yaml
slide_04_solution_third_line:
  title: "Software propio (KiRBe + MADEIRA)"
  body: "Productizamos el método: KiRBe como plataforma de conocimiento; MADEIRA como capa de agentes estandarizados con sourcing y comportamiento gobernados."

slide_05_method_third_column:
  body: "El método se materializa en código, en flujos automatizados, en una plataforma propia (KiRBe) y en una capa de agentes estandarizados (MADEIRA) que el cliente — o nosotros — operamos."

slide_06_proof_card_madeira:
  id: card-madeira
  category: "Plataforma de agentes propia"
  title: "MADEIRA — Capa agentic gobernada"
  outcome: "Sourcing gobernado, habilidades versionadas, comportamiento auditable. Hoy operativa en interno y dentro de KiRBe."
  tags: ["Agentes propios", "Sourcing gobernado", "Versionado por habilidades"]
  footer: "Componente operativo · ruta SaaS evaluada"

slide_11_moat_madeira_pillar_extension:
  body_addendum: "La capa MADEIRA hace que cada nuevo cliente herede una runtime de agentes ya gobernada — no es un *prompt* improvisado, es una habilidad versionada."

slide_12_roadmap_12_24m_first_bullet:
  text: "Plataforma KiRBe como ingreso recurrente principal; primer cliente externo de MADEIRA (capa de agentes estandarizados gobernados)."
```
