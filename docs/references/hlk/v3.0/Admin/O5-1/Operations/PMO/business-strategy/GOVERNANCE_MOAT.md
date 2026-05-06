---
language: es
status: active
role_owner: PMO + Database Owner
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_governance_moat
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: moat_thesis
authority: PMO
last_review: 2026-04-30
deck_bound: true
deck_slides_consumed: ["11-moat"]
---
# Foso de gobernanza — la operación es medible, no retórica

## Lo que responde este documento

Por qué la disciplina operativa de Holística es un foso real (no una narrativa de marketing), expresado en cifras que cualquier auditor puede verificar en el repositorio. Es la fuente de la diapositiva 11 (Pilar 1: "Operación gobernada y medible").

## 1. Cuatro cifras que se pueden auditar

A fecha de **2026-04-30**, el repositorio canónico de Holística contiene:

| Métrica | Valor | Cómo se verifica |
|:--------|:------|:-----------------|
| **Temas gobernados** | **28** | `py scripts/validate_topic_registry.py` reporta `Rows validated: 28` (Initiative 32 P10: +4 — skill_registry, touchpoint_kit_cell_registry, policy_register, repo_health_snapshot; Initiative 47 P1: +1 — persona_scenario_registry) |
| **Procesos gobernados** | **1.103** | `py scripts/sync_compliance_mirrors_from_csv.py --count-only` reporta `process_list_rows=1103` (Initiative 49: +7 filas MADEIRA quality / verdict / lifecycle management; Initiative 63 P4: +3 filas blessing/drift/schema-propagation, role_owner=DevOPS/System Owner) |
| **Roles definidos** | **65** | `py scripts/sync_compliance_mirrors_from_csv.py --count-only` reporta `baseline_organisation_rows=65` |
| **Manifests Output 1 (KM visuales)** | **16** | `py scripts/validate_hlk_km_manifests.py` reporta 16 archivos con `OVERALL: PASS` (Initiative 59 P9: +2 — SOP-INITIATIVE_GOVERNANCE_001, SOP-INITIATIVE_PROCESS_HARMONISATION_001; Initiative 63 P0: +3 — SOP-EXTERNAL_REPO_BLESSING_001, SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001, SOP-CROSS_REPO_SCHEMA_PROPAGATION_001) |

Cada cifra está respaldada por un CSV canónico con un validador determinista. No son promesas: son inventarios vivos que fallan la integración continua si alguien los altera sin actualizar la fuente.

> **Nota sobre el crecimiento.** Estas cifras crecen con la operación (cada nuevo programa, cada nuevo cliente, cada nuevo tema documentado las hace crecer). El test [`tests/test_governance_moat_metrics.py`](../../../../../../../../tests/test_governance_moat_metrics.py) enforce que este artefacto no se quede desfasado: tolera +0/-0 en temas y roles, ±5 % en procesos, ±1 en manifests KM (margen para crecimiento operativo natural). Cualquier desfase mayor surge como fallo de CI y obliga al operador a refrescar el documento.

## 2. Tres capas de validación deterministas

Las cifras anteriores se mantienen sanas gracias a un sistema de validadores en tres capas:

| Capa | Qué verifica | Script |
|:-----|:-------------|:-------|
| **Artefacto** | Cada CSV canónico cumple su contrato de campos, tipos y valores enumerados | `scripts/validate_hlk.py` (orquestador) |
| **FK / consistencia** | Cada `program_id`, `topic_id`, `role_name` referenciado en cualquier artefacto se resuelve en el registro canónico correspondiente | `scripts/validate_program_id_consistency.py` |
| **Drift de mirrors** | Los conteos en Postgres (Supabase mirrors) coinciden con los CSV en Git, fila a fila | `scripts/probe_compliance_mirror_drift.py` |

Cada capa puede ejecutarse de forma aislada o como parte del *probe* completo. Cualquier desviación se detecta en menos de cinco segundos sobre el repositorio actual.

## 3. Compuertas externas (lo que no sale sin pasar el filtro)

Toda salida pública (dossiers, decks, emails al asesor, exportaciones a PDF) pasa por compuertas automáticas antes de renderizarse:

- **Compuerta de jargon** (`scripts/build_company_deck.py`): rechaza cualquier despliegue que filtre tokens internos a copia externa. Validada contra [`BRAND_JARGON_AUDIT.md`](../../Marketing/Brand/BRAND_JARGON_AUDIT.md).
- **Compuerta de manifest KM** (`scripts/validate_hlk_km_manifests.py`): rechaza cualquier asset visual sin frontmatter completo (`paths.mermaid`, hashes, `figma_url` opcional, etc.).
- **Compuerta de FK** (`scripts/validate_program_id_consistency.py`): rechaza cualquier referencia a `program_id` o `topic_id` huérfana.
- **Compuerta de cita determinista** (`tests/test_render_dossier.py`): rechaza dossiers donde se cite un `Q-row` que no existe en `ADVISER_OPEN_QUESTIONS.csv`.

## 4. Pipeline de despliegue determinista

Cada artefacto público nace de la misma secuencia:

```
YAML/Markdown SSOT  →  build_company_deck.py  →  HTML preview deck  →  export_company_deck_pdf.py  →  PDF + manifest.json (sha256)
```

Reproducir la salida es trivial: `git checkout <sha> && py scripts/build_company_deck.py && py scripts/export_company_deck_pdf.py` produce el mismo HTML y el mismo PDF, byte a byte. El manifest JSON guarda los sha256 de cada paso para el rastro de cierre.

## 5. La consecuencia operativa: descalado sin impacto

Lo que las cifras y validadores producen no es solo trazabilidad — es **descalado limpio**. Holística puede:

- **Dar de baja un programa** en una operación de cuatro pasos: borrar la fila en `PROGRAM_REGISTRY.csv`, archivar la carpeta `_assets/<plane>/<program_id>/`, archivar la carpeta `programs/<program_id>/` en cada rol relevante, ejecutar `validate_hlk` para confirmar cero referencias huérfanas. Tiempo: minutos. Sin código que reescribir.
- **Reactivar un programa** restaurando los cuatro elementos. El estado vuelve a ser auditable como si el programa nunca se hubiera detenido.
- **Reasignar un rol** entre programas reescribiendo una sola fila de mapeo en `process_list.csv`. La cadena de FK y los validadores garantizan que no queden referencias rotas.

Esa es la propiedad real: la operación no se rompe cuando un programa empieza, pausa o termina. Es la diferencia entre una consultoría con clientes activos (frágil al cambio) y una compañía con métodos versionados (resistente al cambio).

## 6. Por qué es difícil replicar

| Dimensión | Consultoría tradicional | Boutique digital | Holística |
|:----------|:------------------------|:-----------------|:----------|
| Inventario auditado de procesos | No | Parcial | 1.093 procesos en CSV canónico |
| Validadores deterministas | No | Ad hoc | 3 capas integradas en CI |
| Compuertas de calidad externa | Manual (revisión humana) | Manual | Automáticas en cada render |
| Coste de descalado | Alto (todo se rompe) | Medio | Bajo (cuatro pasos auditables) |
| Trazabilidad cliente-a-decisión | Memoria del consultor | Documental | CSV → tema → SOP → registro |

Replicar esta capa es un proyecto de 12-24 meses con un equipo dedicado. Pre-existir con ella desde el día 1 — porque Holística la construyó para sí misma — es la diferencia que un inversor cuenta.

## Deck-bound facts

```yaml
slide_11_moat_pillar_1:
  title: "Operacion gobernada y medible"
  body: "23 temas gobernados, 1.093 procesos catalogados, 65 roles definidos. Tres capas de validadores deterministas y compuertas automaticas en cada salida publica. Lo que se promete se puede auditar."
```
