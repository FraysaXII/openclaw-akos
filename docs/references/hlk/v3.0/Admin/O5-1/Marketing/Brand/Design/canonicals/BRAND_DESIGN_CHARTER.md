---
language: en
status: active
canonical: true
role_owner: Design
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
---

# BRAND_DESIGN_CHARTER — Brand/Design sub-discipline

> Authored I70 P5. Cross-links to existing `BRAND_VISUAL_PATTERNS.md` (P1 active canonical at Marketing/Brand/canonicals/) which is the substantive design-primitives canonical. This charter codifies the Design sub-discipline's role + operating contract.

## 1. Mission

Owns visual-systems primitives for Holistika brand surfaces:
- Color tokens + per-mode palette per `BRAND_VISUAL_PATTERNS.md` §1.1-§1.2 (BRAND_TOKENS_LIGHT + BRAND_TOKENS_DARK).
- Typography scale (Inter font; type sizes for cover / H1 / H2 / body / footnote).
- Brand mark application + cobranding pattern per `BRAND_LOGO_SYSTEM.md` + `BRAND_COBRANDING_PATTERN.md`.
- Illustrations + brand mark variants + on-light/on-dark logo handling.
- Per-engagement visual customization (e.g., SUEZ × EFA host-card primitive at I12 P12).

## 2. Operating posture today

Active. Design sub-discipline operates the discipline today via:
- The render pipeline (`akos/hlk_pdf_render.py` `_BRAND_TOKENS_LIGHT` + `_BRAND_TOKENS_DARK` constants — bound by `validate_brand_canon_drift.py` to `BRAND_VISUAL_PATTERNS.md`).
- The `BRAND_LOGO_SYSTEM.md` canonical at Marketing/Brand/canonicals/.
- The Cobranding pattern at `BRAND_COBRANDING_PATTERN.md` (Holistika × EFA host-card; future co-branding scenarios).

## 3. Per-engagement Design responsibilities

When a new engagement starts:
- Confirm if cobranding applies (per `BRAND_COBRANDING_PATTERN.md` host/guest semantics).
- Validate per-engagement visual additions (e.g., SUEZ slide-counter-cover P0 §0.5) against the brand token table.
- Author per-engagement guest mark assets (e.g., EFA logo variants) at `_external_marks/` of the engagement folder.
- Cross-check `validate_brand_canon_drift.py` PASS before ship.

## 4. Slide-legibility QA support (cross-cutting; see UX-Designer charter)

Design owns:
- **Visual gate** — contrast ratio ≥ 4.5:1 for body text (WCAG 2.2 AA); palette tokens enforce this by construction.
- **Brand mark gate** — logo placement per `BRAND_LOGO_SYSTEM.md` §X.X; never overlapping content.
- **Cover-strip discipline** — 4 fields max per `BRAND_COBRANDING_PATTERN.md`.

UX-Designer owns the integration of Design's visual primitives into interaction patterns (slide layouts, Gantt, counterparty-README structure).

## 5. Cross-references

- Parent: [`BRAND_DISCIPLINE_ONTOLOGY.md`](../../canonicals/BRAND_DISCIPLINE_ONTOLOGY.md) §2 (Design sub-discipline).
- Substantive canonical: `BRAND_VISUAL_PATTERNS.md` (Marketing/Brand/canonicals/) — color tokens + typography scale.
- Logo: `BRAND_LOGO_SYSTEM.md` (Marketing/Brand/canonicals/).
- Cobranding: `BRAND_COBRANDING_PATTERN.md` (Marketing/Brand/canonicals/).
- Validator: `validate_brand_canon_drift.py` (CANON_DIR points to Marketing/Brand/canonicals/ post-P4.5 wave 1).
- Render pipeline: `akos/hlk_pdf_render.py` BRAND_TOKENS_LIGHT/DARK constants.
- Sister sub-disciplines: Copywriter (prose register), AV (audio-visual primitives), UX-Designer (interaction patterns).
