---
language: en
status: completed
phase: P10 — Customer-impeccable pack + WeasyPrint hsl drift fix
engagement_slug: 2026-suez-webuy-procure-to-pay
program_id: ENG-SUEZ-WEBUY-2026
artifact_role: agent_self_checkpoint
intellectual_kind: phase_record
checkpoint_for: docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/
date: 2026-05-10
---

# P10 — Customer-impeccable pack + WeasyPrint <53 brand-color drift fix

> **Trigger.** Operator review of the four PDFs rendered in P8/P9: "they are good for me and my collaborator but not for the customer. We have different audiences remember? use [the brand canon] where we cover things like jargon (which I saw), ways of speaking, volume of words, audiences, design pattern". Operator also asked: "how do we address the economical part of the proposal? I usually have a proposal with economic and the other without. think of the best design".

## 1. Audience differentiation — explicit

| Audience | Pack | Surfaces | Reading-lens source |
|:---|:---|:---|:---|
| Operator + bridge collaborator | Complete pack (kept as-is) | `cdc-feasibility-shape.fr.pdf`, `discovery-questionnaire.fr.pdf`, `proposal.fr.pdf` (now subtitled "version complète"), `deck-suez-webuy.fr.pdf` | J-OP, J-CO rows in `BRAND_BASELINE_REALITY_MATRIX.md` |
| Customer (procurement / DSI lead at SUEZ) | Customer-impeccable pack (new) | `proposal.customer.fr.pdf`, `tarification.customer.fr.pdf` | J-CU row, with enterprise overlay (volume + price-band) |

The complete pack is correct for the operator + bridge: it cites internal scaffolding (engagement program id on every cover, full method depth, capability cards). It is **not** correct for the customer: it ignores J-CU's "first-doubt trigger" rules (price quote with vague qualifiers, English fragments inside a French exchange) and over-cites internal vocabulary at the seams (the embedded "Liste de validation interne" in the source markdown).

The customer pack is built for the J-CU + enterprise-overlay reading-lens:

- "Professional like a big company acting on behalf of SMEs" bridge frame, sharpened for an enterprise reader.
- Outcome-clarity, price-predictability, time-to-value as the three load-bearing decision criteria.
- 60-day price validity + flat closed-price tarification (no multiplier breakdown) as the procurement hygiene signals.

## 2. Economic-split design — operator question, recommendation, rationale

Operator question: "how do we address the economical part of the proposal? I usually have a proposal with economic and the other without. think of the best design".

**Recommendation shipped.** One pricing-free customer proposal + one separate single-page tarification annexe (transmitted on operator decision per meeting cadence).

**Rationale.**

1. **Procurement filing.** A pricing-free proposal sits on the strategic-buying desk and gets discussed; a pricing-included proposal triggers immediate procurement vetting that locks the conversation into "is the price acceptable?" instead of "is the scope right?".
2. **Operator control.** The operator decides per meeting whether to attach the annexe — no re-rendering required.
3. **Conversation hygiene.** The proposal answers "what we'll do together"; the annexe answers "how we transact". Physically separating them signals commercial discipline.
4. **Reusability.** Future engagements (e.g. the EFA project, the lawyers/RCD parallel) reuse the same template; only the tarification annexe varies.

The current `proposal.fr.md` (operator-and-collaborator complete pack) keeps the embedded internal review checklist for the SOP-ENG_PROPOSAL_001 audit trail and is rendered with the eyebrow `Holistika Research · Proposition (version complète)` so the surface is unambiguous internally.

## 3. WeasyPrint <53 brand-color drift fix — root cause + fix

### 3.1 Symptom

Every PDF rendered before P10 shipped with the dark hero cover band rendered as **plain white** (instead of the canonical slate `#0f1219` with teal+amber radial gradients). Every body H2's teal underline was missing. Every `.stat-grid` numeric color, every `.pull-quote` accent, every callout border was the browser default (transparent / browser fallback).

The operator's complaint that the rendered PDFs "didn't use [the brand] at all, or not properly" was not a perception issue — it was a **silent rendering-pipeline failure** that had been in place since the brand visual upgrade in Initiative 27.

### 3.2 Root cause

`BRAND_VISUAL_PATTERNS.md` codifies brand colors in CSS Color Module Level 4 syntax — space-separated `hsl(168 55% 38%)`. The `BRAND_TOKENS_LIGHT` / `BRAND_TOKENS_DARK` dicts in `akos/hlk_pdf_render.py` mirrored that syntax verbatim. WeasyPrint **52.5** (the operator-workstation version) does **not** parse modern space-separated `hsl()` calls — it silently drops them as transparent. Modern syntax was introduced in WeasyPrint 53 (2021).

Verified empirically with two minimal HTML fixtures (deleted after the experiment):

| Syntax | WeasyPrint 52.5 result |
|:---|:---|
| `hsl(220 16% 7%)` (modern, space-separated) | Renders as **white** (transparent fallback). |
| `hsl(220, 16%, 7%)` (legacy, comma-separated) | Renders as the expected dark slate. |

### 3.3 Fix architecture

Two-layer separation, preserving canonical syntax in the SSOT:

1. `BRAND_TOKENS_LIGHT` / `BRAND_TOKENS_DARK` keep the **modern** CSS Color Level 4 syntax (matching `BRAND_VISUAL_PATTERNS.md` and the upstream boilerplate `globals.css`). They remain the documentation-aligned source of truth.
2. A new helper `_to_legacy_hsl(css)` regex-converts `hsl(H S% L%)` → `hsl(H, S%, L%)` at the **emission boundary** (`_brand_pdf_css()` return). Only the WeasyPrint-bound CSS string is converted; downstream consumers (console HTML rendering, sparkline coloring, CSS variable surfaces in browser-rendered dossiers) keep the modern syntax.
3. New drift safeguard: `tests/test_render_dossier.py::test_brand_pdf_css_emits_legacy_hsl_only` asserts the emitted CSS contains zero space-separated `hsl(...)` calls. If a future edit reintroduces a modern call without going through the converter, the test fails.

### 3.4 Tests

```
py -m pytest tests/test_render_dossier.py tests/test_dossier_console.py \
              tests/test_dossier_html_render.py tests/test_dossier_sparkline.py -v
```

→ **58 / 58 passed.** Includes:

- `test_brand_tokens_light_match_pattern_doc` — token dict still mirrors `BRAND_VISUAL_PATTERNS.md` (modern syntax preserved in SSOT).
- `test_brand_pdf_css_contains_all_dossier_classes` — emitted CSS now correctly contains `hsl(168, 55%, 38%)` (legacy form).
- `test_brand_pdf_css_emits_legacy_hsl_only` (new) — drift safeguard.

## 4. FR localization — cover strip + friendly callouts + eyebrow

`render_pdf_branded` previously hardcoded Spanish cover-strip labels (`Programa`, `Fecha`, `Disciplina`) and the eyebrow (`Holistika Research · Dossier`) on every rendered PDF — including the four French SUEZ surfaces in P8/P9. That alone was a brand-drift issue on a French customer document.

Fix:

- `_COVER_STRIP_LABELS` table in `akos/hlk_pdf_render.py` carrying `es` / `en` / `fr` columns (`Programa` / `Program` / `Programme`, etc.).
- `_CALLOUT_QUESTION_LABEL` table extended with `fr` ("Question ouverte pour confirmation").
- `render_pdf_branded` accepts a new `language: str | None` parameter (auto-detected from subtitle hints when unset; defaults to `es`); also a new `eyebrow: str | None` for per-surface override (fallback: `Holistika Research` for `fr` / `en`, `Holistika Research · Dossier` for `es`).
- `scripts/render_suez_engagement_pdfs.py` now passes `language="fr"` and a per-surface `eyebrow` for each of the six surfaces, e.g. `Holistika Research · Cadrage fonctionnel`, `Holistika Research · Découverte`, `Holistika Research · Proposition`, `Holistika Research · Calendrier commercial`.

## 5. Customer pack content — what shipped

### 5.1 `proposal.customer.fr.md` (5-page rendered PDF)

- Lead paragraph (FR external register): "Vos équipes traitent une vingtaine de demandes d'achat WeBuy par mois sur un parc qui doublera d'ici juin. Nous proposons une mécanique simple : cadrer la règle, prototyper l'outil, transférer la maîtrise."
- Stat-grid (3 stats): `~20 / Demandes par mois` · `× 2 / Parc d'engins à compter de juin` · `23 / Champs par demande`.
- Six numbered sections (01–06): **Notre lecture de votre situation**, **Ce que nous proposons** (3-variant table), **Notre méthode** (5-step rhythm table), **Calendrier prévisionnel**, **Critères de réussite**, **Étapes suivantes**.
- One pull-quote: "Automatiser ce qui se calcule, préserver ce qui se juge."
- No pricing inline; closing line points to the tarification annexe as a separate document.
- Forbidden tokens absent (verified by the existing drift gates + manual review): `agent` (replaced with `application logicielle` / `outil` per operator-stated FR external rule), `AKOS`, `KM`, `topic_*`, `counterparty`, `elicitation`, `intelligence`, `baseline reality`.
- Brand-voice traits: vous register throughout, triadic constructions (`cadrer la règle, prototyper l'outil, transférer la maîtrise`), `concrètement`-shape transitions, no anglicisms, no em-dashes (per Impeccable shared-design-laws ban).

### 5.2 `tarification.customer.fr.md` (3-page rendered PDF)

- Lead paragraph framing this as a "document complémentaire" with explicit 60-day validity.
- Three numbered sections: **Tarification par variante** (4-column table — Variante / Posture / Effort de référence / Tarification de référence — with closed-price magnitudes 38 500 € / 53 500 € / 87 000 €), **Modalités** (5 commercial bullets — échéancier / engagement / confidentialité / propriété intellectuelle / responsabilité), **Hypothèses de calcul** (4 transparency bullets), **Validité**.
- Pull-quote: "Tarification calibrée sur le marché conseil français, pondérée par la nature itérative et mesurée du livrable."
- No multiplier breakdown, no blended-rate disclosure, no PERT math — those stay in the operator-private `commercial-schedule.md`.

## 6. Visual verification — browser MCP trail

- Local HTTP server on `127.0.0.1:8765` serving `artifacts/exports/2026-suez-webuy/` (sidesteps the `file://` URL restriction in the Cursor browser MCP).
- Six rendered surfaces inspected page-by-page via `browser_navigate` + `browser_take_screenshot`:
  - `proposal.customer.fr.pdf` — cover (dark hero band rendering, teal eyebrow, white oversized title, cover-strip with FR labels visible), pages 2–5 (lead + stat-grid + numbered sections + variant table + method table + criteria list).
  - `tarification.customer.fr.pdf` — cover (dark hero, "Calendrier commercial" title, "Variantes A · B · C — édition mai 2026" subtitle), pages 2–3 (4-column tarification table with right-aligned bold prices, modalités bullets, hypothèses).
  - `proposal.fr.pdf` (operator-and-collaborator complete pack) — cover with the differentiator eyebrow `Holistika Research · Proposition (version complète)`.
  - `cdc-feasibility-shape.fr.pdf` body — uppercase teal-tinted column headers, code-styled inline tokens, hairline rules.
  - `deck-suez-webuy.fr.pdf` body — numbered slide-section openers (01, 02, …), teal-bordered blockquote callouts.
  - `discovery-questionnaire.fr.pdf` (cover-only spot-check; full body inherits the same pipeline).

Two render-cycle iterations:

1. First render after FR-localization patch: cover came back **white** (modern hsl drop). Empirical 2-fixture verification isolated the WeasyPrint <53 syntax incompatibility.
2. Re-render after `_to_legacy_hsl` converter: dark hero band, teal accents, amber emphasis all firing correctly across all six surfaces.

## 7. Files authored / modified

```
new        docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/proposal.customer.fr.md
new        docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/tarification.customer.fr.md
new        artifacts/exports/2026-suez-webuy/proposal.customer.fr.pdf  (+ .md sidecar)
new        artifacts/exports/2026-suez-webuy/tarification.customer.fr.pdf  (+ .md sidecar)
mod        akos/hlk_pdf_render.py
             - _CALLOUT_QUESTION_LABEL table (es/en/fr)
             - _COVER_STRIP_LABELS table (es/en/fr) + _cover_labels_for helper
             - _build_cover_html: language + eyebrow params; eyebrow defaults from labels
             - render_pdf_branded: language + eyebrow params (back-compat: language=None auto-detects)
             - fpdf2 fallback meta_lines now use _cover_labels_for(language_hint)
             - _LEGACY_HSL_RE + _to_legacy_hsl helper
             - _brand_pdf_css now returns _to_legacy_hsl(css) at the boundary
mod        scripts/render_suez_engagement_pdfs.py
             - SURFACES dict adds proposal_customer + tarification_customer
             - per-surface "eyebrow" key on every entry
             - cover render call now passes language="fr" + eyebrow=meta.get("eyebrow")
             - --only help string updated ("all six")
             - existing 4 surfaces re-rendered with FR cover-strip labels +
               eyebrow + dark hero band (the prior renders silently dropped colors)
mod        tests/test_render_dossier.py
             - test_brand_pdf_css_contains_all_dossier_classes asserts legacy hsl literals
             - new test_brand_pdf_css_emits_legacy_hsl_only drift safeguard
mod        artifacts/exports/2026-suez-webuy/render-manifest.json  (auto-regenerated; 6 surfaces)
```

## 8. Renderer verdict

WeasyPrint chosen for all six surfaces (cover gradient + brand identity preserved). fpdf2 fallback would lose the gradient cover but would still emit the localized cover labels via `_cover_labels_for(language_hint)`.

`renderer_rc=0` for all six entries in the manifest.

## 9. Follow-ups (out of scope for P10)

- Update `BRAND_VISUAL_PATTERNS.md` §1.1 footnote to mention the WeasyPrint <53 emit-time legacy-syntax conversion. Currently the canonical states "Always cite as `hsl(<H> <S>% <L>%)` to stay portable into ReportLab / WeasyPrint / fpdf2" — that statement is correct for citation but glosses over the runtime emit-side conversion. Light edit only; no behavior change.
- Optional: pin `weasyprint>=53` in `pyproject.toml` to deprecate the converter and rely on native modern-syntax support. Trade-off: harder install on Windows (pango / GTK dependencies); the converter approach keeps the install footprint identical to today.
- Optional: introduce a `proposal_template` profile distinct from `dossier` that drops the leading-zero section counter (`01 / 02 / ...`) for the customer surfaces. The current dossier counter reads as institutional; for a 5-page proposal it works but a sub-mark variant could feel even lighter. Not a blocker — current rendering is brand-impeccable.

## 10. Cross-references

- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) — J-CU row.
- [`BRAND_VOICE_FOUNDATION.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md), [`BRAND_DO_DONT.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_DO_DONT.md), [`BRAND_FRENCH_PATTERNS.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_FRENCH_PATTERNS.md) — voice canonicals.
- [`BRAND_VISUAL_PATTERNS.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md) — visual canonicals (token SSOT).
- [`p8-render-and-drift-gates-2026-05-10.md`](p8-render-and-drift-gates-2026-05-10.md), [`p9-cleanup-2026-05-10.md`](p9-cleanup-2026-05-10.md) — predecessor checkpoints.
- Impeccable skill `setup` gate (BASELINE_REALITY) — the J-CU row served as the BASELINE_REALITY-equivalent loader for this surface.
