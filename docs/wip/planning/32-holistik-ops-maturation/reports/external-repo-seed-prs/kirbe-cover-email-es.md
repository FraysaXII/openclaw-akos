---
language: es
status: draft
audience: KiRBe team lead (outreach directo)
delivery_method: email u outreach directo
---

**Asunto:** [Holistika Ops] KiRBe — PR semilla y contrato cruzado entre repositorios

Hola,

Hace dos semanas te enviamos una nota informando que `config/sync/kirbe-sync-contract.md` §2 sería reescrito. La reescritura está hecha hoy como parte de Initiative 32 P7 en el repo AKOS, junto con tres entregables para tu equipo:

**1. Parche PR (2 ficheros)** — `kirbe.patch` bajo `docs/wip/planning/32-holistik-ops-maturation/reports/external-repo-seed-prs/` en AKOS.

El parche aporta un contrato de una página (`EXTERNAL_REPO_CONTRACT.md`) para la raíz de tu repositorio y una pequeña regla de cursor (`akos-mirror.mdc`) bajo `.cursor/rules/`. El contrato no toca tu pila técnica (FastAPI, LlamaIndex, Pydantic, Logfire, Stripe FDW, tu Neo4j local) — esos siguen siendo tuyos. Solo fija la superficie de doctrina HLK.

**2. Memo de auditoría arquitectónica** — `kirbe-architecture-audit-2026-04-30.md`.

Leímos tu README y tus 36 reglas de cursor. KiRBe está en v1.2 producción: búsqueda híbrida (BM25 + vectorial + RRF), registro de auditoría (preparado SOC2/GDPR), facturación Stripe FDW + webhook, métricas de uso por inquilino, flujo WebSocket, DI orientada a servicios, Neo4j local para búsqueda en bóvedas. La auditoría recomienda 5 cambios a nivel de arquitectura, todos enfocados en consumir los nuevos espejos I31/I32 en modo lectura. Ninguno toca tu disciplina de plano de facturación (`hlk_billing_plane`, separación entre `kirbe.*` y `holistika_ops.*`), tu Neo4j local (queda separado del Neo4j de AKOS por D-IH-32-M), ni tu canal LlamaIndex.

**3. `kirbe-sync-contract.md`** §2 actualizado + nueva §11.

§2 ahora enumera los 16 espejos canónicos (antes 3) con `sync_direction; rls_posture; consumer_role`. La nueva §11 codifica el contrato cruzado entre repositorios que estás reconociendo al fusionar el parche.

**Lo que necesitamos por tu parte, en orden:**

1. Revisa el parche + memo + auditoría. Responde con observaciones o "fusionar tal cual".
2. Elige un patrón de consumo para los nuevos espejos (pregunta abierta Q6): lectura RLS vía Supabase (recomendado; alinea con cómo consumes `process_list_mirror` hoy) o instantáneas JSON versionadas.
3. Fusiona el parche cuando estés listo. La siguiente instantánea semanal REPO_HEALTH_SNAPSHOT del lado AKOS recogerá el cambio automáticamente.

**Lo que explícitamente NO pedimos cambiar:**

- Disciplina de plano de facturación (`hlk_billing_plane`, `kirbe.*` vs `holistika_ops.*`).
- Canal LlamaIndex y composición de lectores.
- Tu Neo4j local (queda separado del Neo4j de AKOS; D-IH-32-M).
- Las 36 reglas de cursor existentes.

Los 5 cambios sugeridos en la auditoría no son bloqueantes. Initiative 33 (diferida) recogerá trabajo específico de KiRBe en un ciclo futuro.

Un saludo,

— Holistika AKOS governance (Founder + System Owner)

---

**Referencias cruzadas:**

- Repo AKOS: https://github.com/FraysaXII/openclaw-akos
- Hoja de ruta Initiative 32: `docs/wip/planning/32-holistik-ops-maturation/master-roadmap.md`
- Documento de precedencia HLK: `docs/references/hlk/compliance/PRECEDENCE.md`
- Doctrina Holistik Ops 6 ejes: `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md`
