---
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika
program_id: PRJ-HOL-FOUNDING-2026
plane: advops
topic_ids:
  - topic_brand_visual_identity
  - topic_enisa_company_dossier
artifact_role: canonical
intellectual_kind: deck_visual_system
authority: Brand Manager + Founder
last_review: 2026-04-30
sources:
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md
  - docs/wip/planning/28-investor-style-company-dossier/deck-brief.md
  - docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml
---

# Deck visual system — Investor-style company dossier

> **Purpose.** Translate the brand tokens in `BRAND_VISUAL_PATTERNS.md` into the specific layout primitives this 16:9 deck needs. The HTML preview (P3) and the Figma deck (P4) both consume this document as the layout SSOT.

## 1. Frame

- **Aspect ratio**: 16:9 (1440 × 810 design, exported up to 1920 × 1080).
- **Safe area**: 80 px margin top / bottom / left / right.
- **Body grid**: 12 columns, 24 px gutter; content sits in cols 1–10 by default; cols 11–12 are reserved for stat / annotation accents on body slides.
- **Page chrome**: every body slide carries a small footer band (eyebrow + page count) inside the bottom safe area; cover and section openers do **not**.

## 2. Tokens (mirrored from `BRAND_VISUAL_PATTERNS.md` §1)

| Role | Light surface | Dark surface |
|:---|:---|:---|
| Background | `hsl(40 20% 99%)` (cream-warm) | `hsl(220 16% 7%)` (deep slate) |
| Surface (card) | `hsl(40 15% 98%)` | `hsl(220 14% 10%)` |
| Foreground | `hsl(220 12% 18%)` (charcoal) | `hsl(210 15% 90%)` (warm off-white) |
| Muted text | `hsl(220 8% 42%)` | `hsl(210 12% 65%)` |
| Border / hairline | `hsl(220 8% 88%)` | `hsl(220 12% 22%)` |
| Accent primary (teal) | `hsl(168 55% 38%)` | `hsl(168 50% 44%)` |
| Accent secondary (amber) | `hsl(38 80% 50%)` | `hsl(38 75% 55%)` |
| Risk (sparing) | `hsl(0 75% 55%)` | `hsl(0 60% 60%)` |

Radius scale: 4 px (tags, hairlines), 8 px (cards, callouts), 16 px (cover panels). All match the existing `--radius: 0.5rem` scaling.

## 3. Typography

- **Family**: Inter (Google Fonts) with Segoe UI / system fallbacks.
- **Display weights**: 700 for cover/section headlines; 600 for slide H1/H2.
- **Body weight**: 400 for prose; 500 for emphasis lines.
- **Monospace**: Consolas / Menlo / Courier New for footer page counters only — never for prose.

| Use | Family | Weight | Size (px @1440) | Line-height |
|:---|:---|:---|:---|:---|
| Cover headline | Inter | 700 | 88 | 1.05 |
| Cover subtitle | Inter | 400 | 28 | 1.35 |
| Section opener number | Inter | 700 | 220 | 0.9 |
| Section opener label | Inter | 600 | 20 (tracked +12 %, uppercase) | 1.2 |
| Section opener headline | Inter | 700 | 64 | 1.1 |
| Slide H1 (body slide) | Inter | 700 | 44 | 1.15 |
| Slide eyebrow | Inter | 600 | 14 (tracked +14 %, uppercase) | 1.2 |
| Slide body | Inter | 400 | 20 | 1.55 |
| Card title | Inter | 600 | 22 | 1.25 |
| Card body | Inter | 400 | 16 | 1.5 |
| Tag / pill | Inter | 500 | 12 (tracked +6 %) | 1.2 |
| Stat number | Inter | 700 | 96 | 0.9 |
| Stat label | Inter | 600 | 13 (tracked +14 %, uppercase) | 1.3 |
| Footer band | Inter | 500 | 12 | 1.2 |

## 4. Slide layouts

Each layout is named in `deck_slides.yaml` (`layout:` key). The HTML preview and Figma deck implement them under those names.

### 4.1 `cover_hero` (slide 01)

- Full-bleed dark surface with the canonical gradient from `BRAND_VISUAL_PATTERNS.md` §1.3 (radial teal + radial amber + linear slate).
- Top-left monogram (24 mm equivalent), top-right empty.
- Eyebrow line (uppercase, tracked) at 18 % from top.
- Oversized headline at 35 % from top, 60 % width, left-aligned.
- Subtitle directly under headline, 50 % width, muted opacity.
- Bottom strip (single horizontal line, full width inside safe area): three columns — `Holística Research`, `holistikaresearch.com`, `2026`.
- No page number on cover.

### 4.2 `section_opener` (slides 02, 03, 08)

- Dark surface, no gradient (a flatter cousin of the cover).
- Big two-digit section number (e.g. `01`) in faded teal, 220 px, top-left.
- Section label below in uppercase tracked teal.
- Single-line headline at 50 % from top, 80 % width, white-on-charcoal.
- Single supporting paragraph (max 60 words) under the headline.
- No cards or stats here — these slides are pure framing.

### 4.3 `solution_three_lines` (slide 04)

- Light surface.
- Eyebrow + headline at top (cols 1–10).
- Three vertical cards in a 3-column grid below, equal width.
- Each card: title (teal accent on first-letter rule), one-line body, no tags.
- Cards have hairline borders only — no shadows.

### 4.4 `method_three_columns` (slide 05)

- Light surface.
- Eyebrow + headline at top.
- Three horizontal stripes (one per line of the method), each with a tag on the left and prose on the right.
- Tags use the amber accent for line 3 ("Software de método") and teal for the other two.

### 4.5 `capability_grid` (slide 06)

- Light surface, but with a 4-cell stat-grid band immediately under the eyebrow line, hairline-bounded top + bottom.
- Below the stat band: 5 capability cards in a 2-2-1 grid (the 5th centred on its row) **or** a 5-column row at smaller card sizes — pick the one that breathes better at 16:9 (default to **5-column row** for visual rhythm).
- Each card: order number top-left, category eyebrow under it, title, one-line outcome, three tag pills, footer line.
- Card body is at most 22 words; the long-form lives in the appendix.

### 4.6 `product_spotlight` (slide 07)

- Light surface.
- Eyebrow + headline left, 60 % width.
- Right 35 % column: product mark (KiRBe) + 4 proof points as bulletless lines, each prefixed with a teal dash.
- Pull-quote at bottom in italic teal: "No es una promesa: es la prueba viva de que el método se puede operar sin nosotros."

### 4.7 `market_icp` (slide 09)

- Light surface.
- Eyebrow + headline at top.
- Three vertical cards in a 3-column grid below; each card: title, body, signal tag (teal pill: "Cliente directo · servicio profesional", "Canal indirecto · entrega gobernada", "Producto · ingreso recurrente").

### 4.8 `business_model_today_tomorrow` (slide 10)

- Light surface.
- Eyebrow + headline.
- Three vertically stacked rows (Hoy → El puente → Mañana), each with a left tag column (e.g. "Servicio profesional", "Producto · método ejecutable", "SaaS recurrente") and a right body column.
- A teal vertical connector runs through the left column to imply progression.

### 4.9 `moat_pillars` (slide 11)

- Light surface.
- Eyebrow + headline.
- Four equal pillar cards in a 4-column grid; each card has only a title and a short body (no tags, no number).
- Hairline-bounded only; the moat slide is intentionally calm.

### 4.10 `roadmap_three_phases` (slide 12)

- Light surface.
- Eyebrow + headline.
- Horizontal three-band timeline below: each band a card with a window label (e.g. "0 – 6 meses"), a title (e.g. "Consolidación") and three deliverables as tagless bulletless lines.
- A continuous teal line connects the three windows along the top.

### 4.11 `enisa_fit_use_of_funds` (slide 13)

- Light surface.
- Eyebrow + headline.
- Top half: three fit-points in a 3-column grid (Innovación, Escalabilidad, Presencia en España).
- Bottom half: a use-of-funds band with 4 lines, no numbers — explicitly **directional**, not budgeted.

### 4.12 `ask_signature` (slide 14)

- Light surface, restrained.
- Eyebrow + headline.
- Three ask lines stacked vertically, each prefixed with a teal arrow.
- Closing block bottom-left: "Un saludo, **Holística Research**" + contact hint.

## 5. Components (Figma + HTML names)

| Component | Figma name | HTML class |
|:---|:---|:---|
| Brand monogram | `Brand / Monogram` | `.brand-monogram` |
| Cover gradient panel | `Slide / Cover Hero` | `.slide-cover` |
| Section opener panel | `Slide / Section Opener` | `.slide-section-opener` |
| Body slide frame | `Slide / Body` | `.slide-body` |
| Eyebrow | `Type / Eyebrow` | `.eyebrow` |
| Section number | `Type / Section Number` | `.section-number` |
| Stat block | `Block / Stat` | `.stat-block` |
| Stat grid (4-up) | `Block / Stat Grid` | `.stat-grid` |
| Capability card | `Card / Capability` | `.capability-card` |
| Tag pill (teal) | `Tag / Pill / Teal` | `.tag` |
| Tag pill (amber) | `Tag / Pill / Amber` | `.tag-amber` |
| Pull-quote | `Block / Pull Quote` | `.pull-quote` |
| Roadmap window | `Block / Roadmap Window` | `.roadmap-window` |
| Ask line | `Block / Ask Line` | `.ask-line` |
| Footer band | `Slide / Footer` | `.slide-footer` |

These names are stable across the HTML preview and the Figma deck; renaming on either side requires updating both.

## 6. Imagery rules

- No stock photography. Period.
- No clip-art icons. Period.
- Allowed visual elements:
  - Brand monogram (`boilerplate/public/holistika-short-100x100.svg`).
  - Custom abstract treatments built from the gradient + grid pattern (mirrors the live site).
  - Real product screenshots **only when authorised by the founder before send** — placeholder frames are fine in the deck source until then.
- Card emojis or unicode symbols are forbidden in slide copy (we keep the deck pre-2010-internet professional).

## 7. Anti-patterns (forbidden)

- Two-column body slides with dense paragraphs on both sides.
- More than 80 words per slide (excluding capability slide where 5 cards × 22 words = 110 max).
- Tag pills on every slide (use them only on slide 6 + the ICP signal tags on slide 9).
- Drop shadows, gradients on cards, beveled edges.
- More than two accent colours on the same slide.
- Page numbers on the cover or section openers.

## 8. Accessibility

- Text contrast ratio ≥ 4.5:1 against the backing surface for body copy; ≥ 3:1 for display text per WCAG AA Large.
- Tag pills meet 4.5:1 against their tinted background.
- The dark gradient panels keep the white text at full opacity (we do not push titles below 95 % opacity on dark surfaces).

## 9. Cross-references

- [`BRAND_VISUAL_PATTERNS.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md) — token source of truth.
- [`deck_slides.yaml`](deck_slides.yaml) — slide structured data.
- [`deck_story_es.md`](deck_story_es.md) — slide narrative in prose.
