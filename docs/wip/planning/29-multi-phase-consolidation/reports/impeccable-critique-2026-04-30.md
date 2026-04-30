# Impeccable critique + audit findings — Holística company dossier (HTML preview)

**Date**: 2026-04-30
**Target**: [`docs/presentations/holistika-company-dossier/index.html`](../../../presentations/holistika-company-dossier/index.html) (rendered from `deck_slides.yaml` via `scripts/build_company_deck.py`)
**Method**: read-through of `.cursor/skills/impeccable/reference/critique.md` + `audit.md` + `cognitive-load.md` + `heuristics-scoring.md` + `typography.md`, applied as a **structured first-pass review** against the rendered HTML deck. The interactive `/critique` and `/audit` slash-commands (browser-overlay live-detection mode) remain available to the operator post-merge for a deeper second-pass review.
**Scope**: 14-slide HTML preview deck, all slides visible as `<section class="slide">` elements with the deck stylesheet inlined.

> **Why this report exists.** Initiative 29 P3 captures a baseline review the moment Impeccable lands in the repo, before the strategy SSOT (P4) lifts the deck content from qualitative claims to concrete numbers. After P5 wiring, a follow-up `/polish` pass will convert these findings into surgical diffs.

---

## 1. Headline scores (Impeccable rubric)

### `/critique` heuristic scores (Nielsen 0-4)

| Heuristic | Score | Note |
|:---|:---:|:---|
| Visibility of system status | n/a | Static deck — not applicable |
| Match between system and the real world | 4 | Spanish-native, audience-appropriate, no internal codenames |
| User control and freedom | n/a | Static deck — not applicable |
| Consistency and standards | 3 | Brand tokens applied consistently; one inconsistency: stat numbers use 64 px, section openers use 220 px — intentional but tag pills size differently between slide 6 (HUG) and slide 9 (now HUG too) post-P1 |
| Error prevention | n/a | Static deck — not applicable |
| Recognition rather than recall | 4 | Section openers number `01`/`02`/`03`; capability cards numbered; ICP signals tagged — the reader never has to remember |
| Flexibility and efficiency of use | n/a | Static deck — not applicable |
| Aesthetic and minimalist design | 3 | Generally clean; **one violation**: the deck currently has redundant capability-card body text (slide 6 cards) AND a pull quote on slide 7 saying "no es una promesa, es la prueba viva" — peak-message-density risk |
| Help users recognize, diagnose, recover | n/a | Static deck — not applicable |
| Help and documentation | n/a | Static deck — not applicable |

**Effective score**: 3.5 / 4 on the 4 applicable heuristics. Strong baseline.

### Cognitive Load checklist (Impeccable 8-item rubric)

| Item | Pass / Fail |
|:---|:---:|
| Each slide has one primary message | PASS — every slide has one headline + supporting evidence |
| Visible options at decision points ≤ 4 | PASS — except slide 6 (5 capability cards) which is intentional and uses the stat-grid as anchor |
| Progressive disclosure | PASS — section openers gate transitions between thematic segments |
| Visual hierarchy (3 levels max per slide) | PASS — eyebrow → headline → body, three levels max |
| No simultaneous color signals | PASS — teal + amber are clearly differentiated; risk red is unused |
| Font weight contrast | PASS — 700 / 600 / 400 / 500 used purposefully |
| Reading order matches visual order | PASS — F-pattern on body slides, Z-pattern on capability grid |
| Scannable in 5 seconds per slide | PARTIAL — slide 7 (KiRBe spotlight) right column has 4 proof points without scanning anchors |

**Failure count**: 1 (low). Cognitive load = **good**.

### `/audit` technical dimensions (0-4)

| Dimension | Score | Notes |
|:---|:---:|:---|
| Accessibility (a11y) | 3 | Headings (`h1`, `h2`, `h3`) used; `lang="es"` set; contrast ratios meet WCAG AA on all body slides; **gap**: section opener numbers (`220 px hsla 0.18 opacity`) are decoration but read as text by screen readers (no `aria-hidden="true"`); some teal-on-cream caption text is right at 4.5:1 threshold — WCAG AA Large is fine but body 8.5 pt italic muted-foreground edges close to AA |
| Performance | 4 | Self-contained HTML (~37 KB markup + ~8 KB CSS inlined); no external assets except Inter fonts via Google Fonts CSS import; no JS; print media query strips shadows for PDF — minimal |
| Theming | 4 | Every color references a CSS custom property defined in `:root`; no hardcoded hex codes outside the `:root` declarations themselves; brand tokens mirror `BRAND_VISUAL_PATTERNS.md` §1 |
| Responsive design | 1 | **Major gap**: the deck is fixed at 1440 × 810 px with `width: var(--slide-w)` — viewing at <1024 px width forces horizontal scroll. This is **deliberate** (decks are 16:9, not responsive web pages) but the deck-header `.deck-container` does not currently include any "scale to fit" logic for narrower viewports. Acceptable for the current external-send use case (operator opens in desktop Chrome → prints to PDF); not acceptable if the HTML preview becomes a public web page |
| Anti-patterns | 4 | **Zero AI-slop tells.** Reviewed against the Impeccable DON'Ts list: no AI color palette (we use brand teal/amber not the typical violet/pink/cyan AI rainbow); no gradient text; no dark glows / glassmorphism; no hero metric grids (the stat grid on slide 6 is hairline-bounded and minimal, not the typical "huge number with dropshadow" pattern); no identical card grids (capability cards differ in tag count and content per card); no generic AI fonts (Inter is intentional and brand-canonical); no cluttered card-after-card pattern (sections breathe) |

**Composite audit score**: 3.2 / 4 (a11y 3, perf 4, theming 4, responsive 1, anti-patterns 4). Pulled down by responsive — but the deck use case is fixed-aspect-ratio export, so the score is calibrated to the wrong rubric. **In-context score (deck, not web page): 3.8 / 4.**

---

## 2. What's working (high-confidence keepers)

1. **Brand consistency is rock-solid.** Every accent color, every spacing scale, every type weight maps to a token in `BRAND_VISUAL_PATTERNS.md`. The risk of "the next slide deck looks different from this one" is low.
2. **Section openers are the right device.** The `01` / `02` / `03` faded-teal numerals create thematic transitions without slide ornaments. The dark surface contrasts against the cream body slides for natural pacing.
3. **Capability grid is information-dense without being cluttered.** Five cards in one row, each with order number + category eyebrow + title + outcome + tag pills + visibility footer. The reader gets a 5-deliverable proof in one glance.
4. **The pull-quote on slide 7 lands.** "No es una promesa: es la prueba viva de que el método se puede operar sin nosotros." That's a sharp claim, brand-voice-correct, and visually emphasized by the teal italic.
5. **Footer band is restrained.** Small uppercase letterspaced `Holística Research · Dossier de Compañía` + `06 / 14` — auditable without being decorative.

---

## 3. Priority issues (high-leverage fixes for the next polish pass)

### P1 — Slide 6 capability-card body text reads slightly truncated

**What.** On slide 6 the KiRBe card body line ends with "despliegue cloud productivo" but renders visually as "despliegue cloud" because the card body text wraps mid-line.

**Why.** Card body text has `font-size: 13px` with `line-height: 150%` and the card width is 241.6 px (FILL within the 5-card row). The text content is just slightly over the column's effective width.

**Fix (next polish pass)**. Either: (a) tighten the body copy in `deck_slides.yaml` for the KiRBe card to fit ~22 words, or (b) reduce the body font-size to 12 px, or (c) add `padding: 14px 14px` (was 16) to give 4 px more horizontal breathing room. Option (a) is cleanest and aligns with the "≤22 words per card" rule in `deck-visual-system.md`.

### P2 — Section opener numbers should be `aria-hidden`

**What.** Slides 02, 03, 08 render `01`, `02`, `03` at 220 px in faded teal. Sighted users read them as section indicators; screen readers will read them as actual content ("zero one — el problema — Las companias estan...").

**Why.** No `aria-hidden="true"` on the `.section-number` element.

**Fix.** In `styles.css` or directly on the rendered HTML element, add `aria-hidden="true"` to `.section-number`. Cost: one CSS / template tweak. Improves a11y from 3 → 4.

### P3 — Slide 7 right-column scanning anchors

**What.** The 4 proof points on slide 7 use a teal vertical bar + horizontal teal dash before each point. Visually distinguishable, but the scanning order isn't anchored — a busy reader's eye may jump to the pull-quote on the left first.

**Why.** No numeric or visual hierarchy among the 4 right-column points.

**Fix (post-strategy P4/P5)**. After the strategy SSOT is wired, the proof-points slide can carry concrete metrics (e.g. "1 producto en producción", "X clientes B2B activos", "Y tier de ingreso recurrente"). Once those exist, replace the 4 plain points with stat-block style entries (oversized number + label).

### P4 — Stat 4 on slide 6 ("Pila técnica replicada en 5 contextos") clips the label

**What.** The fourth stat block label reads "PILA TECNICA REPLICADA EN 5 CONT" — last word truncated.

**Why.** Stat label width is constrained to 240 px with `font-size: 12 pt`, but the full label is wider.

**Fix.** Either: (a) shorten the label to "REPLICADA EN 5 CONTEXTOS" (drop "PILA TECNICA"), or (b) reduce `letter-spacing` from 0.14em to 0.10em. Option (a) is cleanest — the headline already says "una sola pila técnica".

### P5 — Slide 13 use-of-funds reads as a list of intents, not a budget

**What.** The use-of-funds row carries 4 directional lines: "Productización de KiRBe...", "Contratación de 2-3 ingenieros senior...", "Infraestructura productiva...", "Asesoría legal...". They're presented as equal — but a reader expecting a budget breakdown finds none.

**Why.** Strategy SSOT (P4) doesn't exist yet — there's no `INVESTMENT_THESIS.md` or `BOOTSTRAPPING_PLAN.md` to source allocation bands from.

**Fix (this is the I29 P4/P5 thesis)**. Once `BOOTSTRAPPING_PLAN.md` ships with monthly burn ranges + 3 scenarios, `sync_deck_from_strategy.py` can replace the 4 plain lines with allocation bands ("≈ 40 % productización, 30 % personal, 20 % infraestructura, 10 % asesoría" — operator-confirmed). The deck stops promising directional intent and starts showing real allocation.

---

## 4. Minor observations (nice-to-have, not blocking)

- **Cover hero gradient.** The dual-radial + linear-slate gradient renders well in modern Chrome but may look flat in older Safari or in some PDF readers. The current solid teal fallback (used by `fpdf2` if WeasyPrint unavailable) is a graceful degrade. No fix needed.
- **Slide footer page counter.** `06 / 14` is right-aligned at 12 pt, muted-foreground. Reads cleanly. **Suggestion** for future polish: replace the literal `/` with a thinner Unicode glyph (`⁄`) for typographic consistency.
- **Spanish accents.** All slide copy renders Spanish accents (á, é, í, ó, ú, ñ, ¿, ¡) correctly via Inter's Latin Extended. No issues.
- **Card eyebrow categories** ("WEB PUBLICA + CRM", "ERP INTERNO", etc.) are uppercase + 11 pt + letter-spaced 0.18em. **Possible micro-improvement**: drop the `+` in "WEB PUBLICA + CRM" to "WEB PUBLICA / CRM" for cleaner parsing.

---

## 5. Provocative questions (for the founder, post-strategy SSOT)

These are the questions an investor-style reader will silently form between slides 1 and 14. The strategy SSOT (P4) should answer them:

1. **What does an engagement actually cost?** Slide 10 says "Hoy facturamos servicio" but never says €X / day or €Y / project.
2. **What is KiRBe's pricing?** Slide 10 says "SaaS recurrente" but no tier, no €/month, no usage metric.
3. **How do you sell?** Slide 9 ICP is precise enough, but how does a partner B2B engagement get initiated? Inbound? Outbound? Network?
4. **Where's the runway proof?** Slide 12 says "Consolidación 0-6 meses" without a months-of-runway figure or break-even hypothesis.
5. **Is there a raise on the table?** Slide 13 says "ENISA" but says nothing about whether external capital is sought.

---

## 6. Recommended next runs (operator-driven, post-merge)

The interactive Impeccable commands give richer evidence than this read-through. After this PR merges, the operator should run:

1. **`/critique docs/presentations/holistika-company-dossier/index.html`** — full critique with the browser-overlay live-detection. The overlay highlights anti-patterns directly on the rendered page. Expected runtime: ~5 min including the browser session.
2. **`/audit docs/presentations/holistika-company-dossier/index.html`** — technical 5-dimension audit with concrete CSS / DOM evidence. Expected runtime: ~3 min.
3. **`/polish docs/presentations/holistika-company-dossier/index.html`** — surgical fixes for the P1 / P2 / P4 priority issues above. Expected runtime: ~10 min.
4. **(After Phase 4 / 5 of I29 ships)** Re-run `/critique` to verify the strategy SSOT integration didn't introduce new issues.

Each run should append to a follow-up report in `docs/wip/planning/29-multi-phase-consolidation/reports/`.

---

## 7. Provenance

- **Skill bundle**: Impeccable Style v3.0.5, Apache 2.0, sourced from <https://github.com/pbakaus/impeccable> commit cloned 2026-04-30, extracted into [`.cursor/skills/impeccable/`](../../../../../.cursor/skills/impeccable/).
- **Bridge files**: [`PRODUCT.md`](../../../../../PRODUCT.md), [`DESIGN.md`](../../../../../DESIGN.md) at repo root.
- **Governance contract**: [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7.
- **Brand SSOT** (consumed by every Impeccable command): `BRAND_VOICE_FOUNDATION.md`, `BRAND_VISUAL_PATTERNS.md`, `BRAND_DO_DONT.md`, `BRAND_SPANISH_PATTERNS.md`, `BRAND_JARGON_AUDIT.md`, `BRAND_REGISTER_MATRIX.md`.
