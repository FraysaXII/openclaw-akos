---
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika
program_id: shared
topic_ids:
  - topic_brand_voice
  - topic_brand_visual_identity
artifact_role: canonical
intellectual_kind: brand_asset
authority: Operator (lived production sources)
last_review: 2026-04-29
sources:
  - upstream: c:\Users\Shadow\cd_shadow\root_cd\boilerplate\app\globals.css
    role: live token definitions (light + dark CSS custom properties)
  - upstream: c:\Users\Shadow\cd_shadow\root_cd\boilerplate\tailwind.config.ts
    role: keyframes + tailwind utility plugins (`bg-grid`, `bg-grid-small`, `bg-dot`, `spotlight` animation)
  - upstream: c:\Users\Shadow\cd_shadow\root_cd\boilerplate\app\layout.tsx
    role: typography selection (Inter, `next/font/google`) + default theme (`dark`)
  - upstream: c:\Users\Shadow\cd_shadow\root_cd\boilerplate\public\holistika-short-100x100.svg
    role: monogram logo asset (cover + favicon variant)
  - upstream: c:\Users\Shadow\cd_shadow\root_cd\boilerplate\public\logo.svg
    role: full wordmark logo asset
---

# BRAND_VISUAL_PATTERNS

> **Status — Active (Initiative 27 follow-up; Operator-supplied 2026-04-29).** Hand-authored companion to [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) capturing concrete **visual** identity patterns sourced verbatim from the Holistika Research production marketing site (`c:\Users\Shadow\cd_shadow\root_cd\boilerplate`). Cited by [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) `render_pdf_branded(profile="dossier")` when generating brand-aligned PDFs (ENISA dossier, partner pitches, investor decks). Operator-curated; **not** auto-rendered by the wave2 scaffolder. Edits land via direct PR.

## Why this exists

`BRAND_VOICE_FOUNDATION.md` defines who we are in words. `BRAND_SPANISH_PATTERNS.md` defines how we sound in Spanish. **This file defines how we look on a printed page or PDF** when a single canonical brand-aligned render is needed — typically for high-stakes external sends (ENISA certifying body, ICEX, advisers, investors, partners).

The browser-use recon originally planned for `holistikaresearch.com` is **dropped**: the boilerplate repo at `c:\Users\Shadow\cd_shadow\root_cd\boilerplate` is the **upstream source-of-truth** that ships the live site, so its tokens are authoritative without a network round-trip. Live recon stays available as a post-merge upgrade option if the site evolves and the boilerplate repo lags.

## 1. Tokens (HSL, Tailwind-compatible)

Sourced verbatim from `boilerplate/app/globals.css`. **Always cite as `hsl(<H> <S>% <L>%)`** to stay portable into ReportLab / WeasyPrint / fpdf2.

### 1.1 Light theme (the dossier base)

| Token | HSL | Hex (approx) | Role |
|:---|:---|:---|:---|
| `--background` | `40 20% 99%` | `#fefdfa` | Cream-warm; reduces harshness of pure white on long PDFs |
| `--foreground` | `220 12% 18%` | `#282d36` | Warm charcoal; less eye-strain than pure black |
| `--card` | `40 15% 98%` | `#fcfcf9` | Card / inner-panel surface |
| `--muted-foreground` | `220 8% 42%` | `#62666f` | Captions, footers, source-citation lines |
| `--border` | `220 8% 88%` | `#dee0e3` | Hairlines for tables, page rule, hr |
| `--accent-primary` (teal) | `168 55% 38%` | `#2b9077` | Headings, links, ring accents, primary callouts |
| `--accent-secondary` (amber) | `38 80% 50%` | `#e69408` | Stat-emphasis, "Operator decision" callout, key-figure highlights |
| `--destructive` | `0 75% 55%` | `#dd3838` | Risk / red-flag callouts only — sparing |
| `--ring` | `168 55% 38%` | `#2b9077` | Focus rings (interactive UI; not used in print) |
| `--radius` | `0.5rem` | — | All corner-rounding (cards, callouts, pull-quotes) |

### 1.2 Dark theme (cover hero band only)

The dossier cover uses a **dark hero band** drawn from the dark theme tokens:

| Token | HSL | Hex (approx) | Role |
|:---|:---|:---|:---|
| `--background` (dark) | `220 16% 7%` | `#0f1219` | Cover band base |
| `--foreground` (dark) | `210 15% 90%` | `#dfe2e8` | Cover title text |
| `--accent-primary` (dark) | `168 50% 44%` | `#39a98c` | Cover sub-title, program/discipline strip accent |
| `--accent-secondary` (dark) | `38 75% 55%` | `#e0a73e` | Cover stat-line "Estado: P1-Audit ready" |

The teal/amber pairing is **intentionally identical conceptually** between modes — the dark variant is slightly lighter for contrast on the dark background.

### 1.3 Cover hero gradient (canonical)

The boilerplate spotlight + grid + radial-vignette pattern is unique to Holistika and identifies the brand instantly. The print-adapted variant approximates it CSS-only:

```css
.cover-hero {
  background:
    radial-gradient(ellipse 60% 50% at 30% 30%,
      hsl(168 55% 38% / 0.18) 0%,
      transparent 60%),
    radial-gradient(ellipse 80% 70% at 70% 60%,
      hsl(38 80% 50% / 0.12) 0%,
      transparent 70%),
    linear-gradient(160deg,
      hsl(220 16% 7%) 0%,
      hsl(220 14% 10%) 55%,
      hsl(220 12% 14%) 100%);
}
```

Reasoning: the live site uses a JS-animated spotlight (`spotlight 2s ease .75s 1 forwards` keyframes from `tailwind.config.ts`) plus a `bg-grid` SVG overlay. PDFs are static. The dual-radial-gradient simulation **preserves the identity** (off-center bright spot + warm secondary glow + slate base) without requiring rasterized hero PNGs.

## 2. Typography

Source: `app/layout.tsx` line 11 — `const inter = Inter({ subsets: ["latin"] });`

| Element | Family | Weight | Size | Notes |
|:---|:---|:---|:---|:---|
| Body | **Inter**, fallback `-apple-system`, `Segoe UI`, `Roboto`, `Helvetica Neue`, `Arial`, sans-serif | 400 | 10.5pt | Inter is the canonical web brand font |
| H1 (cover title) | Inter | 700 | 26pt | White on cover hero band |
| H1 (body section) | Inter | 700 | 20pt | Foreground charcoal |
| H2 | Inter | 600 | 15pt | Teal `#2b9077`; bottom border 1px `--border` |
| H3 | Inter | 600 | 12pt | Foreground charcoal |
| Captions / source citations | Inter | 400 | 8.5pt | `--muted-foreground` `#62666f`; italic |
| Code / `ref_id` codes | "Consolas", "Menlo", "Courier New", monospace | 400 | 9.5pt | Subtle slate background `#f4f4f6` |

Print fallback: Spanish accents and en-dashes require a Unicode TTF. `akos/hlk_pdf_render.py` already registers `Segoe UI` / `Arial` / `DejaVu Sans` in priority order — Inter is **CSS-only** (WeasyPrint pulls it from Google Fonts when online); fpdf2 falls back to Segoe UI on Windows, which is visually close enough and Unicode-safe.

## 3. Layout primitives

### 3.1 Cover page

```
+-----------------------------------------------------------+
|  [HOLISTIKA MONOGRAM 28mm sq.]                            |
|                                                           |
|        DOSSIER ENISA                                      |
|        Empresa Emergente — Certificación                  |
|        ─────────────────────────────                      |
|        Programa: PRJ-HOL-FOUNDING-2026                    |
|        Disciplina: Asesoría Jurídica                      |
|        Estado: P1-Audit ready                             |
|        Fecha de emisión: 2026-04-29                       |
|                                                           |
|                                                           |
|        Holistika Research                                 |
|        holistikaresearch.com                              |
+-----------------------------------------------------------+
```

Implementation: a single `<section class="cover-hero">` with `min-height: 297mm` for A4, `padding: 28mm 24mm`, white text. Logo via `<img src="…/holistika-short-100x100.svg" />` at 28mm × 28mm.

### 3.2 Body page

```
+---------------------------------+
| Pilar I — Mercantil          [#] |  ← H1, foreground charcoal
| ──────────────────────────────  |  ← 1pt teal rule (--accent-primary)
|                                 |
| Estructura societaria...        |  ← H2 in teal
|                                 |
| ┌─────────────────────────────┐ |
| │  Operator decision          │ |  ← amber-tinted callout
| │  TODO[OPERATOR]: 6202 vs... │ |
| └─────────────────────────────┘ |
|                                 |
| Tabla 1.1 — CNAE candidates     |  ← H3 + caption
| ┌────┬────────┬─────────────┐  |
| │ #  │ CNAE   │ Narrative   │  |  ← slate-100 header, hairlines
| ├────┼────────┼─────────────┤  |
| │ 1  │ 6202   │ Consultoría │  |
| └────┴────────┴─────────────┘  |
|                                 |
| Fuente: ADVISER_OPEN_QUESTIONS  |  ← muted caption
| .csv (Q-LEG-001), 2026-04-29   |
+---------------------------------+
```

### 3.3 Callouts

Three variants (CSS class names land in `render_pdf_branded`):

- **`.callout-info`** (teal-tinted): default. Background `hsl(168 55% 38% / 0.06)`, left border 3px `--accent-primary`, body `--foreground`.
- **`.callout-operator`** (amber-tinted): `TODO[OPERATOR]` decision points. Background `hsl(38 80% 50% / 0.08)`, left border 3px `--accent-secondary`, label "Decisión del fundador" in amber.
- **`.callout-risk`** (red-tinted): risks / pitfalls. Background `hsl(0 75% 55% / 0.05)`, left border 3px `--destructive`. Used **sparingly** — the brand voice is rigor-as-care, not fear.

### 3.4 Tables

- Header row: `--foreground` (charcoal) text on `--secondary` (`hsl(220 8% 95%)` `#f0f0f2`) background.
- Zebra rows: even rows white, odd rows `hsl(40 15% 98%)` (card surface).
- Hairlines: 1px `--border` (`#dee0e3`).
- Caption: H3 sized + muted caption directly above.

## 4. Iconography & assets

| Asset | Location (boilerplate repo) | Use in dossier |
|:---|:---|:---|
| Monogram logo | `public/holistika-short-100x100.svg` | Cover, footer page-numbers |
| Wordmark logo | `public/logo.svg` | Inside-cover acknowledgment block |
| Grid pattern | `public/grid.svg` | (Optional) cover band texture overlay |
| Footer grid | `public/footer-grid.svg` | (Optional) inside-back-cover ornament |

The full list of supplementary marks (`p1.svg` through `p4.svg`, `b1.svg`, `b4.svg`, `b5.svg`, `host.svg`, `cloud.svg`, etc.) belongs to the marketing site's "stack badge" pattern; we do **not** import those into the dossier — they read as web-marketing chrome, not certifying-body documentation.

## 5. Print-adapted variant rules

When `render_pdf_branded(profile="dossier")` runs, the boilerplate's web-first identity translates to a **print-first variant** with these adaptations:

1. **Light body, dark cover**. The web defaults to dark mode; certifying bodies print PDFs and dark-mode prints waste toner and look unserious. The cover keeps the dark hero band as a **single concentrated brand statement**; everything else is light.
2. **Teal as accent, not background**. The dark-mode `bg-accent` (`hsl(220 12% 16%)`) reads as flat slate on print. Use teal only on H2 headings, links, table-header underlines, and `.callout-info` borders.
3. **Amber for emphasis only**. Operator-decision callouts and stat-emphasis numerals (e.g. "12 días para entregar" if cited in evidence) — never as full-line backgrounds.
4. **Embed diagrams via PNG**, not SVG. WeasyPrint and fpdf2 differ in SVG fidelity; the canonical KM topic diagrams (`topic_kirbe_billing_plane_routing.png`, `topic_enisa_evidence.png`, `topic_external_adviser_handoff.png`, `topic_graph.png`) are the print embed format.
5. **Page-number footer = `<program_id> · <discipline> · <ISO date> · pg X / Y`**. Auditable.
6. **Animations dropped silently**. The `spotlight` and `shimmer` keyframes are CSS-only; they do not render to PDF anyway. The radial-gradient simulation in §1.3 is the print approximation.

## 6. Don't-do (anti-patterns specific to print)

- **Don't** apply the full dark theme to body pages. Reads as "consultancy black turtleneck", not "rigorous research firm".
- **Don't** apply the teal/amber gradient as a full-page background. The boilerplate uses it as a **mood** behind hero copy; in print it becomes a flat blob.
- **Don't** stack more than two callouts in a single section. They are signal devices, not paragraph delimiters.
- **Don't** use the `bg-grid-small` pattern at body-text scale. It vibrates on certain printers.
- **Don't** invent new colors. Anything outside §1.1 / §1.2 is off-brand. `BRAND_DO_DONT.md` and `BRAND_REGISTER_MATRIX.md` cover voice; this section covers visuals.

## 7. Maintenance

- **Trigger to update**: any change to `boilerplate/app/globals.css`, `tailwind.config.ts`, or the public-folder logo assets.
- **Operator runbook**: when the public site rebrands (e.g. teal hue rotation, new logo), open this file, re-copy the relevant token rows from the upstream sources cited in the frontmatter, bump `last_review`, regenerate one canonical sample dossier, eyeball-compare with the live site.
- **Drift safeguard**: a PR-time grep test checks that the HSL strings cited in §1.1 / §1.2 match the values currently in the boilerplate `globals.css`. If they drift, the failure points the operator at this file.

## 8. Cross-references

- **Brand voice** (sister canonical): [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md), [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md), [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md), [`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md)
- **Communication SOP**: [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)
- **PDF helper that consumes these tokens**: [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) `render_pdf_branded`
- **Canonical dossier output template**: [`docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md`](../../../../_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md)
