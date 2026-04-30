# DESIGN — Holística Research

> **Bridge file for Impeccable Style** (`.cursor/skills/impeccable/`). Per [`SOP-HLK_TOOLING_STANDARDS_001.md`](docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7, this file is a **thin redirect** to canonical visual SSOT under `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md` and the deck-specific layout system at `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md`. It does **not** duplicate visual content.

## Canonical visual SSOT

- **Brand tokens, typography, hero gradient, anti-patterns** → [`BRAND_VISUAL_PATTERNS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md)
- **Deck-specific layout primitives, slide layouts, anti-patterns** → [`deck-visual-system.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md)
- **Figma file (visual SSOT for the company dossier)** → see [`FIGMA_FILES_REGISTRY.md`](docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/FIGMA_FILES_REGISTRY.md)

## Token snapshot (read the canonical file for full detail)

Tokens are HSL, Tailwind-compatible, sourced verbatim from the production marketing site. Use the named tokens; never hardcode hex.

| Role | Light surface | Dark surface |
|:---|:---|:---|
| Background | `hsl(40 20% 99%)` (cream-warm) | `hsl(220 16% 7%)` (deep slate) |
| Foreground | `hsl(220 12% 18%)` (warm charcoal) | `hsl(210 15% 90%)` (warm off-white) |
| Muted text | `hsl(220 8% 42%)` | `hsl(210 12% 65%)` |
| Border / hairline | `hsl(220 8% 88%)` | `hsl(220 12% 22%)` |
| Accent primary (teal) | `hsl(168 55% 38%)` | `hsl(168 50% 44%)` |
| Accent secondary (amber) | `hsl(38 80% 50%)` | `hsl(38 75% 55%)` |
| Risk (sparing) | `hsl(0 75% 55%)` | `hsl(0 60% 60%)` |

Radius scale: 4 px (tag pills, hairlines), 8 px (cards, callouts), 16 px (cover panels). Default to 8 px when unsure.

## Typography snapshot

- **Family**: Inter (Google Fonts) with Segoe UI / system fallbacks. Never substitute.
- **Display weights**: 700 for cover/section headlines; 600 for slide H1/H2.
- **Body weight**: 400 for prose; 500 for emphasis lines.
- **Line height**: 1.55 for body, 1.15 for display.
- **Letter spacing**: −0.025em on cover title; +0.14em uppercase on small-caps labels.
- **Caption / source citations**: 8.5 pt italic muted-foreground.

For complete type scale and per-element specs, read [`deck-visual-system.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md) §3.

## Layout primitives (deck context)

Twelve canonical primitives are documented in [`deck-visual-system.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md) §4 and inventoried in [`figma-link.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/figma-link.md). Examples:

- Cover hero (dark gradient, oversized title, monogram, bottom strip)
- Section opener (big two-digit number, label, headline, dark surface)
- Body slide shell (eyebrow + headline + content area + footer band)
- Capability card (charcoal head + body + tag pills + footer)
- Stat block (oversized number + small-caps label, hairline-bounded)
- Roadmap window (dot indicator + window-label + title + deliverables)
- Pull quote (italic teal, left-bordered)
- Ask line (arrow-circle + body)

When `/polish` or `/critique` proposes layout changes, they MUST reuse these primitives. New primitives require an update to `deck-visual-system.md` first.

## Visual anti-patterns (forbidden)

- Two-column body slides with dense paragraphs on both sides.
- More than 80 words per slide (capability slide is the only exception, capped at ~110).
- Tag pills on every slide — they are signal devices, used only on slide 6 capability cards and slide 9 ICP signals.
- Drop shadows, gradients on cards, beveled edges.
- More than two accent colors on the same slide.
- Page numbers on the cover or section openers.
- Stock photography, clip-art icons, hero illustrations from generic libraries.

For the full list, see [`BRAND_VISUAL_PATTERNS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md) §6.

## Accessibility

- Body-text contrast ≥ 4.5:1 against the backing surface (WCAG AA).
- Display-text contrast ≥ 3:1 (WCAG AA Large).
- Tag pills meet 4.5:1 against tinted backgrounds.
- Dark gradient panels keep titles at full opacity (no <95 % opacity on dark surfaces).

## Surfaces

This DESIGN.md is calibrated for the company dossier deck. Other Holística surfaces (HLK ERP, KiRBe SaaS, Madeira agent UI, marketing site) have their own DESIGN-equivalent files in their respective product repos. The brand tokens are shared; the layout primitives are surface-specific.

## AKOS precedence rule (non-negotiable)

If an Impeccable command's visual / layout / motion suggestion conflicts with `.cursor/rules/akos-*.mdc` (governance, planning traceability, asset classification, brand-token authority), the AKOS rule wins. In practice for visual work:

- Token suggestions (hex → CSS var) MUST use names from `BRAND_VISUAL_PATTERNS.md` §1; raw hex codes are forbidden when a token exists.
- Layout suggestions stay phase-scoped per `akos-planning-traceability.mdc`; one commit per phase.
- Component / token additions to the deck visual system require an update to [`deck-visual-system.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md) before any rendered output changes.

## Cross-references

- [`PRODUCT.md`](PRODUCT.md) — sister bridge file for audience / brand voice / anti-references
- [`SOP-HLK_TOOLING_STANDARDS_001.md`](docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7 — Impeccable governance contract
- `.cursor/skills/impeccable/SKILL.md` — Impeccable entry skill
- `.cursor/skills/impeccable/reference/` — per-command reference (e.g. `polish.md`, `critique.md`, `audit.md`, `typography.md`)
