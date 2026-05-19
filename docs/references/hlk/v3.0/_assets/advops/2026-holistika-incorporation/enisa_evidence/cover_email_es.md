---
status: active
role_owner: Compliance
area: Operations / PMO
entity: Holistika Research SL
program_id: PRJ-HOL-FOUNDING-2026
program_label: "Holistika Research SL — Programa de fundación 2026"
plane: advops
topic_ids:
  - topic_enisa_dossier_es
parent_topic: topic_enisa_evidence
language: es
artifact_role: cover_email
intellectual_kind: cover_email_body
authority: Operator (Founder + Compliance)
recipient_ref_id: POI-LEG-ENISA-LEAD-2026
discipline_id: certification
voice_register: peer_consulting
pronoun_register: tu
sharing_label: counsel_and_named_counterparty
last_review: 2026-05-18
sources:
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_SPANISH_PATTERNS.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VOICE_FOUNDATION.md
  - docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md
audience: [J-ENISA]
channel: [CHAN-DIRECT-DM]
---

# Cover email (ES) — apéndice de evidencias ENISA

> **Asunto sugerido**: `Apéndice de evidencias ENISA — Holistika Research SL`

Hola [nombre del asesor],

Te hago llegar el apéndice de evidencias ENISA de Holistika Research SL, en versión PDF, como complemento al dossier de compañía que te envié por separado. Cubre los cuatro pilares — Mercantil, Mercado, Financiación y Operativa — y los cuatro apéndices: instrumentos legales en curso, capacidades demostradas (cinco entregas de software ya en producción), glosario y trazabilidad.

El documento está pensado para tu lectura técnica antes de la firma. Si después de revisarlo necesitas ampliación en alguna sección — especialmente el objeto social, los CNAE o el plan de capitalización — podemos cerrarlo en una llamada de 30 minutos esta semana. Te paso enseguida un par de huecos concretos.

Si prefieres dejar comentarios por escrito sobre el dossier antes de hablar, perfecto también.

Un saludo,

Holistika Research SL  
holistikaresearch.com

<!-- ============================================================
     NOTAS INTERNAS (no enviar — operator-side only)
     ============================================================ -->

> **Notas internas (no enviar).**
>
> - **Recipiente**: ref `POI-LEG-ENISA-LEAD-2026`; nombre real se resuelve off-repo (per `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`) en el momento del envío SMTP.
> - **Adjunto principal**: PDF generado a partir de `enisa_evidence/dossier_es.md` (versión actual: 2026-05-18). Nombre de archivo sugerido: `apendice-evidencias-enisa-holistika-research-sl-2026-05-18.pdf`.
> - **Adjunto opcional** (sólo si el asesor pide tracking estructurado de preguntas abiertas): exportar `ADVISER_OPEN_QUESTIONS.csv` filtrado por `program_id = PRJ-HOL-FOUNDING-2026` vía `scripts/export_adviser_handoff.py`.
> - **Tono**: `peer_consulting` + `tu` per `BRAND_SPANISH_PATTERNS.md` §"Founder reply pattern". Apertura `Hola [nombre]` (informal-profesional, no `Buenos días`); cierre `Un saludo,` + firma corporativa.
> - **Cuerpo**: ≈ 130 palabras. Rango objetivo 120-150.
> - **Cross-referencia con preguntas abiertas**: las cinco preguntas `Q-LEG-001..005` con `target_date = before_signing` ya están listadas en `FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md` (canonical) + el legal-constitutor handoff bundle (`Think Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md`). NO repetirlas en el cuerpo del cover email — el dossier técnico ya las cubre.
> - **Refresh history**: revisado 2026-05-18 (I86 / OPS-86-5) para alinear con la marca "Holistika Research SL", eliminar recomendaciones CNAE específicas del cuerpo (ya viven en el dossier técnico), y endurecer la separación operator-internal vs external-facing.
