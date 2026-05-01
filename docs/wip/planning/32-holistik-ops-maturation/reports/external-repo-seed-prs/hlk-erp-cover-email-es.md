---
language: es
status: draft
audience: ERP team lead (outreach directo)
delivery_method: email u outreach directo
---

**Asunto:** [Holistika Ops] hlk-erp — PR semilla, auditoría arquitectónica, paquete de entrega

Hola,

Initiative 32 en el repo AKOS incluye tres entregables para el lado hlk-erp:

**1. Parche PR (2 ficheros)** — `hlk-erp.patch` bajo `docs/wip/planning/32-holistik-ops-maturation/reports/external-repo-seed-prs/` en AKOS.

El parche aporta un contrato de una página (`EXTERNAL_REPO_CONTRACT.md`) para la raíz del repo y una pequeña regla de cursor (`akos-mirror.mdc`) bajo `.cursor/rules/`. Ambos derivan de plantillas canónicas en AKOS; el contrato no toca tu pila técnica (Next.js / shadcn / Tailwind / Supabase / FastAPI).

**2. Memo de auditoría arquitectónica** — `erp-architecture-audit-2026-04-30.md`.

Leímos tu README, tus 13 reglas de cursor y tu carpeta `documentation/`. La auditoría detecta dos derivas latentes:

- Tu regla local `data-ssot.mdc` dice "centraliza en `lib/*`", pero el documento de precedencia AKOS indica que las CSV canónicas viven en `docs/references/hlk/compliance/` (en AKOS, no en tu repo). Recomendación: la nueva `akos-mirror.mdc` toma precedencia sobre `data-ssot.mdc` (vía Q10); mantén `data-ssot.mdc` solo para constantes/tipos no-HLK. Initiative 44 (diferida) reescribirá o eliminará `data-ssot.mdc` tras un trimestre limpio bajo el patrón de supersesión.
- `other_documentation/kirbe/` y `other_documentation/hlk/documentation-hlk/` son snapshots obsoletos. Recomendación: archívalos y reemplaza por punteros a la SSOT AKOS y a la SSOT KiRBe.

**3. Paquete de entrega ERP** — carpeta `erp-handoff-bundle-2026-04-30/` con 7 ficheros.

El paquete da al equipo ERP el mapa del lado-lectura: esquema de los 16 espejos canónicos con consultas de ejemplo (`01-mirror-schema-map.md`), especificación de integración de los 5 ejes para pantallas ERP (`02-five-axis-integration-spec.md`), puntero al runbook del gate de SQL del operador (`03`), puntero al SOP de localización reubicado (`04`), extracto de changelog (`05`), puntero a `TEAM_SOTA_HLK_ERP.md` (`06`).

**Lo que necesitamos por tu parte, en orden:**

1. Revisa el parche + memo + paquete. Responde con observaciones o "fusionar tal cual".
2. Confirma si la recomendación Q10 (akos-mirror.mdc toma precedencia) es aceptable para tu equipo, o propón alternativa.
3. Fusiona el parche cuando estés listo.

**Lo que explícitamente NO pedimos cambiar:**

- Patrones del Next.js App Router y la regla `chart-wrapper-enforcement`.
- Tokens de tema shadcn / Tailwind e identidad visual.
- Integración Supabase Auth.
- Tu patrón de directorios `hooks/`, `components/`, `lib/`.

Los gates de preparación-producción del ERP (auth, RLS de inquilinos, runbook de reversión) viajan en una Initiative 33 separada — fuera de alcance aquí, pero en la hoja de ruta.

Un saludo,

— Holistika AKOS governance (Founder + System Owner)

---

**Referencias cruzadas:**

- Repo AKOS: https://github.com/FraysaXII/openclaw-akos
- Paquete ERP: `docs/wip/planning/32-holistik-ops-maturation/reports/erp-handoff-bundle-2026-04-30/`
- Documento de precedencia HLK: `docs/references/hlk/compliance/PRECEDENCE.md`
- Initiative 33 (diferida): gates de preparación-producción ERP
