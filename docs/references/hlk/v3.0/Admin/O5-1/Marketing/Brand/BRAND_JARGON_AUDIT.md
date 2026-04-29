---
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika
program_id: shared
topic_ids:
  - topic_brand_voice
  - topic_external_communications
artifact_role: canonical
intellectual_kind: brand_asset
authority: Operator (lived protocols)
last_review: 2026-04-29
---

# BRAND_JARGON_AUDIT

> **Status — Active (Initiative 27 follow-up; Operator-supplied 2026-04-29).** Hand-authored companion to [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — the **operational rule** for keeping internal jargon out of every external-bound deliverable. Cited by the four-layer composer ([`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)) and by every external dossier / cover email / pitch / partner pack. Operator-curated; **not** auto-rendered by the wave2 scaffolder.

## 1. The principle (one paragraph)

We do the heavy lifting internally so external readers do not have to. Internal vocabulary — codenames, schema names, framework jargon, methodology shorthand — stops at the team boundary. External communications use the language **the recipient already speaks at work**: domain terms they know (CNAE, objeto social, ENISA, escritura, plan de negocio), plain Spanish/English for everything else. If we would not say it out loud to the recipient on a phone call without explaining it, we do not write it in a document we are about to send them.

This is the operational consequence of narrative pillar 3 in [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md): *"Plain words externally; jargon stays internal (we do the heavy lifting)"*. Without this audit, the pillar is a nice slogan; with this audit, it becomes a checkable contract.

## 2. Why this exists

Internal documentation, codebases, and SOPs evolve fast and need precise codenames so the team can refer unambiguously to canonical structures (`topic_*`, `program_id`, `GOI/POI`, `plane`, etc.). When that vocabulary leaks into an external dossier, three things happen — all bad:

1. **The recipient feels excluded.** They are reading our shorthand, not our argument. Cognitive load goes up; trust goes down.
2. **The brand reads as junior.** Mature consultancies translate. Junior ones quote their internal Slack.
3. **The argument hides.** The objective claim ("we built five products in six months") gets buried under stack lists and codenames; the certifier has to do the unpacking we should have done.

This SOP exists so that no external-bound deliverable ever ships with the failure mode visible.

## 3. Scope

| In scope | Out of scope |
|:---|:---|
| Dossiers (ENISA, ICEX, banking, partner pitches) | Internal SOPs, decision logs, planning docs (jargon allowed and expected) |
| Cover emails to external advisers, regulators, investors | Internal Slack / chat / standups |
| Investor / partner pitch decks | Code comments, commit messages, PR bodies |
| Public-facing marketing copy (web, blog, brand assets) | Internal architecture docs, runbooks, MCP descriptors |
| Press / PR materials | Migration ledgers, tooling SOPs |
| Subject-line + body of any outbound email signed by Holistika | The Q-tracker appendix tables in dossiers (where row ids are a checklist for the adviser to tick) |

The Q-tracker tables are the **only** place in an external dossier where internal `Q-LEG-001`-style ids are allowed. They function as a checklist; the adviser ticks them off as they answer. In **prose** of the same dossier, refer to questions in plain language (*"la pregunta sobre el objeto social y el paquete CNAE"*) and let the appendix carry the formal id.

## 4. Forbidden tokens (external-bound deliverables only)

These tokens MUST NOT appear in external prose. They MAY appear inside the structured Q-tracker appendix and in machine-readable provenance metadata (frontmatter / footer source lines).

### 4.1 Internal codenames (drop entirely or replace)

- `AKOS` — drop or rephrase as *"nuestro sistema interno de gestión del conocimiento"* / *"our internal knowledge platform"*
- `topic_<anything>` — drop entirely; describe the underlying concept in plain language
- `plane`, `ADVOPS`, `TECHOPS`, `FINOPS`, `MKTOPS`, `OPS` — drop or *"área operativa"* / *"operating area"*
- `GOI`, `POI`, `ref_id`, `GOI-…`, `POI-…` — drop entirely from prose; allowed in formal Q-tracker / instruments appendix tables only
- `program_id`, `PRJ-HOL-…` — drop from prose, keep in the dossier metadata footer only
- `repo_slug` — drop; cite repos by their public name
- `holistika_ops.*`, `kirbe.*`, `compliance.*` (schema names) — drop
- `process_list.csv`, `<register>.csv` — drop; cite the artefact by its purpose (*"nuestro registro de cuestiones abiertas"*)

### 4.2 Stack / framework jargon (replace with outcome)

- `RBAC` → *"control de acceso por roles"* / *"role-based access control"*
- `RLS` → *"aislamiento por organización a nivel de base de datos"*
- `pgvector` → *"búsqueda semántica"* / *"semantic search"*
- `RRF` (Reciprocal Rank Fusion) → *"fusión de resultados"* or just drop
- `Cohere reranking` → *"re-clasificación de resultados por relevancia"*
- `Logfire` → *"observabilidad continua"* / *"continuous observability"*
- `BullMQ`, `Redis`, `Mux`, `Cloudflare R2` → *"colas de procesamiento"*, *"vídeo bajo demanda"*, *"almacenamiento de objetos"* — name the **capability**, not the vendor
- `pgvector + RRF + Cohere` → *"búsqueda en lenguaje natural"*
- `JWT`, `OAuth2` → *"autenticación segura"* / *"secure authentication"*
- `next-intl`, `Pydantic`, `shadcn`, `Polaris`, `Liquid` — drop; describe the outcome (*"sitio multilingüe en producción"*)
- `Mermaid`, `WeasyPrint`, `pandoc`, `mmdc` → drop; readers don't care which renderer made the diagram

### 4.3 Methodology shorthand (replace with what we mean)

- `4-layer methodology` → *"Brand voice → Concept → Use-case → Eloquence"* (spell it the first time it appears)
- `Strict mode` / `AKOS Strict` → *"método auditado"* / *"audited method"*
- `Topic-Fact-Source` → *"hechos canónicos con fuente verificable"*
- `manifest` (in the KM sense) → *"ficha técnica"*
- `derived view` → *"vista derivada"* (only if the recipient is a data person; otherwise drop)
- `mirror` (in the Postgres sense) → *"copia espejo"* (only if the recipient is technical)

### 4.4 Operator-side process tokens (always strip from rendered output)

These should never reach the rendered PDF/DOCX of an external deliverable:

- `TODO[OPERATOR]` — replace at render time with friendly framing: *"Pregunta abierta para tu confirmación"* / *"Open question for your confirmation"*
- `[OPERATOR]` — same
- `<OPERATOR_CONFIRM>` placeholders — same
- Markdown HTML class hints like `{: .callout-operator}` — must be CSS-only, not visible text

A render-time test in [`tests/test_render_dossier.py`](../../../../../../../tests/test_render_dossier.py) enforces this.

## 5. Translation gallery (Before / After)

### 5.1 Capability description (KiRBe SaaS, Spanish, ENISA dossier)

**Before** (jargon-leaking, pre-audit):

> Plataforma SaaS B2B con FastAPI (Python 3.11), Pydantic, Supabase (Postgres + pgvector), 20+ routers HTTP, búsqueda híbrida (semántica + keyword fusionada vía RRF), reranking con Cohere, RBAC granular sobre Postgres con políticas RLS, Stripe metered billing, observabilidad Logfire, sincronización proyectiva Neo4j.

**After** (jargon-free, post-audit):

> Plataforma SaaS B2B para gestión de conocimiento empresarial. Búsqueda en lenguaje natural con re-clasificación semántica de resultados. Aislamiento por organización con auditoría completa. Facturación por uso integrada. Despliegue cloud productivo con observabilidad continua.

### 5.2 Operating model (Spanish, ENISA dossier)

**Before**:

> El plano de entrega de Holística Research está documentado en el topic `topic_external_adviser_handoff` (Initiative 21 / 22) y se resume así: el routing de billing entre `kirbe.*` y `holistika_ops.*` está documentado en el topic `topic_kirbe_billing_plane_routing`.

**After**:

> Holística Research entrega hoy investigación estructurada e ingeniería empresarial como servicio facturado, y al mismo tiempo opera la plataforma de gestión de conocimiento (KiRBe) que productiza ese método. Servicio y producto comparten infraestructura, métricas y facturación.

### 5.3 Open question (Spanish, ENISA dossier)

**Before**:

> **TODO[OPERATOR]** — Decisión del fundador (cierra `Q-LEG-001` antes de la firma). Opción A — `7219` primario + `6202` secundario, redacción I+D-céntrica (recomendación interna).

**After**:

> **Pregunta abierta para tu confirmación.** Antes de la firma necesitamos cerrar el texto exacto del *objeto social* y el paquete CNAE. Nuestra recomendación interna es `CNAE 7219` como primario (investigación y desarrollo) y `6202` como secundario (consultoría informática) para anclar la narrativa de innovación que pide ENISA. ¿Lo confirmas?

## 6. Audit checklist (every external deliverable)

Run this before pressing Send. Five questions; if any is "no", revise.

1. **Codename leak check** — does the body contain any of the §4.1 forbidden tokens? Scan with `rg -P "(?i)\b(akos|topic_\w+|advops|techops|finops|goi-|poi-|ref_id|program_id|prj-hol-|holistika_ops\.|kirbe\.|repo_slug)\b" <doc>.md`. Expected: zero hits in prose; matches in metadata frontmatter / Q-tracker / footer are OK.
2. **Stack-dump check** — does any sentence chain three or more pieces of stack jargon (e.g. *"FastAPI + Pydantic + Supabase + pgvector"*)? Replace with a single outcome statement.
3. **Methodology-shorthand check** — does the body cite our internal methodology by codename without spelling it the first time? Spell it once, then use plain language thereafter.
4. **Operator-side leak check** — does the rendered output (PDF / DOCX) contain `TODO[OPERATOR]` or `[OPERATOR]` or `<OPERATOR_*>` strings? It must not. The render pipeline replaces these with friendly framing or drops them.
5. **Recipient-language check** — would the recipient read this document and understand every sentence on first pass without a glossary? If they would have to ask "what does X mean?", X is jargon for them — translate.

## 7. Render-time enforcement

[`scripts/render_dossier.py`](../../../../../../../scripts/render_dossier.py) and the broader [`akos.hlk_pdf_render.render_pdf_branded`](../../../../../../../akos/hlk_pdf_render.py) pipeline:

1. **Strip `TODO[OPERATOR]` callout labels at render time** — markdown `> **TODO[OPERATOR]**` blocks render with the friendly heading *"Pregunta abierta para tu confirmación"* (Spanish) / *"Open question for your confirmation"* (English).
2. **Frontmatter is invisible** — YAML metadata is stripped before HTML rendering.
3. **Footer never carries internal codenames** — only program code + discipline label + ISO date + page number.
4. **A pre-render guard test** ([`tests/test_render_dossier.py::test_dossier_es_body_is_jargon_free`](../../../../../../../tests/test_render_dossier.py)) fails the build if any §4.1 token appears in the dossier body (excluding the Q-tracker appendix and provenance footer where ids are part of the contract).

If the operator wants to run a one-off audit without rendering:

```powershell
py -c "import re,pathlib; t = pathlib.Path('docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md').read_text(encoding='utf-8'); print(re.findall(r'(?i)\b(?:AKOS|topic_\w+|ADVOPS|TECHOPS|FINOPS|MKTOPS|GOI-\w+|POI-\w+|ref_id|program_id|holistika_ops\.|kirbe\.|repo_slug)\b', t))"
```

Expected: a small list of matches, all confined to the Q-tracker appendix tables, the metadata footer, and the YAML frontmatter (which gets stripped at render).

## 8. Cross-references

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — pillar 3 *"Plain words externally; jargon stays internal"*
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — voice IS NOT row "Jargon-leaking (internal codenames externally)"
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — register selection matrix
- [`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md) — Spanish-language patterns from real exchanges
- [`BRAND_VISUAL_PATTERNS.md`](BRAND_VISUAL_PATTERNS.md) — visual identity for external rendered output
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) — four-layer methodology
- [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) — sister SOP for tooling invocations
