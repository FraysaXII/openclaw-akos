---
language: en
status: active
canonical: true
role_owner: UX Designer
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
---

# BRAND_UX_DESIGNER_CHARTER — Brand/UX-Designer sub-discipline

> Authored I70 P5. Cross-link to BRAND_GANTT_DISCIPLINE.md (P6 forward-link, sibling at this canonicals/ folder) + BRAND_COUNTERPARTY_README_CONTRACT.md (P7 forward-link). Codifies the UX-Designer sub-discipline's interaction-pattern + information-architecture craft.

## 1. Mission

Owns interaction patterns + information-architecture primitives for Holistika brand surfaces:
- **Slide layout primitives** in `akos/hlk_pdf_render.py` `_brand_pdf_css_slides()` function: `.host-card`, `.method-anchors`, `.grid-3x2`, `.three-lines`, `.timeline-5`, `.flow-4`, `.stat-narrative`, `.slide-counter-cover` (P0 §0.5 added). Each primitive is a reusable layout pattern integrating Design's visual primitives + Copywriter's prose register.
- **Gantt discipline** (P6 BRAND_GANTT_DISCIPLINE.md sibling): joint UX-Designer + PMO ownership; Mermaid Gantt SSOT; 4-quadrant audience matrix; confidence ladder for thinner-data engagements.
- **Counterparty-README contract** (P7 BRAND_COUNTERPARTY_README_CONTRACT.md forward-link): 3-rule pattern + path-portability + non-technical register; per-engagement multilingual READMEs.
- **Slide-legibility QA discipline** (cross-cutting; see §3 below).

## 2. Operating posture today

Active. UX-Designer sub-discipline operates the discipline today via:
- The `_brand_pdf_css_slides()` function in `akos/hlk_pdf_render.py` (8 slide primitives shipped through I12 P12 + I70 P0 + future P6 BRAND_GANTT_DISCIPLINE primitives).
- The render pipeline's customer-pack outputs (SUEZ deck.customer.fr.pdf as worked example, post-P0 14-page version).
- The future Gantt discipline canonical (P6).

## 3. Slide-legibility QA discipline (UX-Designer owns; cross-cutting)

Per `BRAND_DISCIPLINE_ONTOLOGY.md` §5: every customer-facing deck slide passes a 5-gate QA before render:

1. **Headline gate** — H2 ≤ 60 chars; not start with internal-jargon-tokens (per `BRAND_JARGON_AUDIT.md` §4); pass anti-AI-tone tic regex (per `BRAND_COPYWRITING_DISCIPLINE.md`).
2. **Body gate** — paragraph max 4 sentences; no triadic noun-phrase stacks; no `X, pas Y` AI-tic.
3. **Visual gate** (Design-owned, UX-Designer integrates) — contrast ≥ 4.5:1 (WCAG 2.2 AA); no overlapping interactive regions; cover-strip 4 fields max.
4. **Multilingual gate** (P7) — per-language register matches per-engagement language declaration.
5. **Counterparty gate** (P7) — no operator-jargon visible to counterparty; proper register tier per `BRAND_REGISTER_MATRIX.md`.

QA runs as part of `scripts/render_*_engagement_pdfs.py --check` (or equivalent per-engagement render script) before PDF emission. Today some gates run mechanically (1 + 3 partial); others are operator-eye (2 + 4 + 5 partial). I71 makes them all mechanical.

## 4. Slide layout primitive design rules

When authoring a new slide primitive (e.g., the `.slide-counter-cover` added at P0 §0.5):

- **Reusability** — primitive must be reusable across engagements; no SUEZ-specific styling.
- **CSS-grade-aware** — WeasyPrint 52.5 has no CSS grid support; use `display: table` or basic flex (matching the existing `_brand_pdf_css_slides()` constraints).
- **Tokens-first** — all colors come from `BRAND_TOKENS_LIGHT` / `BRAND_TOKENS_DARK` (Design-owned); no hardcoded hex.
- **Mobile-considerate** — landscape A4 (297×210mm) is fixed for slides; portrait A4 for dossiers. Print size is fixed but on-screen preview should be readable.
- **Print-bleed-aware** — 22-32mm padding on cover-class slides; 14-26mm on body slides.

## 5. Cross-references

- Parent: [`BRAND_DISCIPLINE_ONTOLOGY.md`](../../canonicals/BRAND_DISCIPLINE_ONTOLOGY.md) §2 (UX-Designer sub-discipline).
- Sibling at this canonicals/: BRAND_GANTT_DISCIPLINE.md (P6 forward-link).
- Sister sub-disciplines: Copywriter (prose register; UX-Designer integrates); Design (visual primitives; UX-Designer integrates); AV (audio-visual; UX-Designer integrates if video-embedded surfaces).
- Render pipeline: `akos/hlk_pdf_render.py` `_brand_pdf_css_slides()` function (8 layout primitives shipped).
- Worked example: SUEZ deck (`deck.customer.fr.md`) post-I70 P0 — 14 slides using all 8 primitives + new `.slide-counter-cover`.
- P7 forward-links: `BRAND_MULTILINGUAL_CONTRACT.md` + `BRAND_COUNTERPARTY_README_CONTRACT.md` — UX-Designer co-owns counterparty-README pattern with PMO.
