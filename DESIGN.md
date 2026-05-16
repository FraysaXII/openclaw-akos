# DESIGN — Holistika Research

> **Bridge file for Impeccable Style** (`.cursor/skills/impeccable/`). Per [`SOP-HLK_TOOLING_STANDARDS_001.md`](docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7, this file is a **thin redirect** to canonical visual SSOT under `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/` plus deck-specific layout at `_assets/advops/`. It does **not** duplicate visual content. Impeccable skills MUST read the canonical files before any visual command.

## Canonical visual SSOT (authoritative)

The visual canon has expanded since the original 2 sources (I29 P3, 2026-05-05) through Initiative 66 (Brand Vision Ops Sweep — Logo System for visual identity), Initiative 70 (Cobranding Pattern for joint deliverables), and Initiative 71 (Pack A2 + Gantt discipline). The visual SSOT now spans 5 canonical files plus 1 surface-specific deck system.

### Tokens + typography + layout primitives

- **Brand tokens, typography, hero gradient, layout primitives, anti-patterns** → [`BRAND_VISUAL_PATTERNS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VISUAL_PATTERNS.md)
- **Deck-specific layout primitives, slide layouts, anti-patterns** (surface-specific for the company-dossier deck family) → [`deck-visual-system.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md)
- **Per-locale number / currency / date formats** (visual formatting on dates and figures) → [`BRAND_LOCALISED_FORMATS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LOCALISED_FORMATS.md)

### Visual identity

- **Logo system** (monogram + wordmark + lockup variants; clear space + minimum sizes + per-surface usage; sub-mark cobranding precedence) → [`BRAND_LOGO_SYSTEM.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LOGO_SYSTEM.md) (I66 P1)
- **Cobranding pattern** (host / guest split; logo precedence on joint deliverables; closing-line attribution) → [`BRAND_COBRANDING_PATTERN.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_COBRANDING_PATTERN.md) (I70)
- **Figma file inventory** (visual SSOT location pointer; canonical filename pattern) → [`FIGMA_FILES_REGISTRY.md`](docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/FIGMA_FILES_REGISTRY.md)

## Token snapshot (read the canonical file for full detail)

Tokens are HSL, Tailwind-compatible, sourced verbatim from the production marketing site. Use the named tokens; never hardcode hex. The shared design laws in `.cursor/skills/impeccable/SKILL.md` reference OKLCH as the preferred working space for new color work; existing HSL tokens are the authoritative production values to match.

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

## Logo system snapshot

Logo lockups, monogram clear space, minimum sizes, and per-surface usage rules live in [`BRAND_LOGO_SYSTEM.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LOGO_SYSTEM.md). When `/polish` or `/critique` proposes a logo placement, position, or sizing change, it MUST cite the relevant `BRAND_LOGO_SYSTEM.md` section. Sub-mark logo precedence (Holistika R&S vs Think Big vs HLK Tech Lab) follows the Branded House topology in `BRAND_ARCHITECTURE.md` §"Visual hierarchy". Cobranded surfaces (joint client deliverables, partner pages) follow [`BRAND_COBRANDING_PATTERN.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_COBRANDING_PATTERN.md).

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
- Side-stripe borders (`border-left` / `border-right` > 1 px as colored accent) — banned per Impeccable shared design law.
- Gradient text (`background-clip: text` + gradient) — banned per Impeccable shared design law.
- Decorative glassmorphism — rare and purposeful, or nothing.
- The hero-metric template (big-number + small-label + supporting-stats + gradient-accent) — SaaS cliché, banned.

For the full list, see [`BRAND_VISUAL_PATTERNS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VISUAL_PATTERNS.md) §6 and [`SKILL.md`](.cursor/skills/impeccable/SKILL.md) §"Absolute bans".

## Per-locale visual formatting

Numbers, currency, and dates render per-locale per [`BRAND_LOCALISED_FORMATS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LOCALISED_FORMATS.md):

- **EN** thousands `,` decimal `.` (e.g., `1,234.56`); currency prefix `EUR1,234.56` (uncommon — usually USD prefix `$1,234.56`).
- **FR** thousands NARROW NO-BREAK SPACE U+202F, decimal `,` (e.g., `1 234,56`); EUR suffix `1 234,56 €`.
- **ES** thousands `.` decimal `,` (e.g., `1.234,56`); EUR suffix `1.234,56 €`.
- **Dates**: ISO `2026-05-16` canonical/technical; EN `May 16, 2026`; FR `16 mai 2026`; ES `16 de mayo de 2026`.

Cross-locale parity is enforced by `scripts/validate_brand_voice_register.py` (I71 P2 Pack A2 + Addition 11).

## Accessibility

- Body-text contrast ≥ 4.5:1 against the backing surface (WCAG AA).
- Display-text contrast ≥ 3:1 (WCAG AA Large).
- Tag pills meet 4.5:1 against tinted backgrounds.
- Dark gradient panels keep titles at full opacity (no <95 % opacity on dark surfaces).
- Logo monogram clear-space minimums per `BRAND_LOGO_SYSTEM.md` preserved at all viewport sizes.

## Surfaces

This DESIGN.md is calibrated for the company dossier deck family + adjacent brand-register surfaces. Per-sub-mark variants:

- **Holistika R&S** (Tier 1 umbrella voice + dossier deck primitives) — this DESIGN.md is the primary surface.
- **Think Big** (Tier 2 sub-mark voice; founder-coaching arm) — uses brand tokens + adjacent layout primitives; surface-specific DESIGN forthcoming when Think Big product surfaces ship.
- **HLK Tech Lab** (Tier 2 sub-mark voice; engineering arm) — uses brand tokens + engineering-arm voice register per `BRAND_VOICE_FOUNDATION.md`; primary public surface is `/tech-lab`.

Other Holistika surfaces (HLK ERP operator dashboard, KiRBe SaaS UI, MADEIRA agent UI, marketing site) have their own DESIGN-equivalent files in their respective product repos. Brand tokens are shared; layout primitives are surface-specific. Cobranded surfaces follow [`BRAND_COBRANDING_PATTERN.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_COBRANDING_PATTERN.md).

## AKOS precedence rule (non-negotiable)

If an Impeccable command's visual / layout / motion suggestion conflicts with `.cursor/rules/akos-*.mdc` (governance, planning traceability, asset classification, brand-token authority, baseline reality), the AKOS rule wins. In practice for visual work:

- Token suggestions (hex → CSS var) MUST use names from `BRAND_VISUAL_PATTERNS.md` §1; raw hex codes are forbidden when a token exists.
- Logo suggestions MUST cite `BRAND_LOGO_SYSTEM.md`; ad-hoc logo arrangements outside the lockup variants are forbidden.
- Layout suggestions stay phase-scoped per `akos-planning-traceability.mdc`; one commit per phase.
- Component / token additions to the deck visual system require an update to [`deck-visual-system.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md) before any rendered output changes.
- Cobranded-surface visual work MUST cite `BRAND_COBRANDING_PATTERN.md` precedence before placing partner logos.

## Cross-references

- [`PRODUCT.md`](PRODUCT.md) — sister bridge file for audience / brand voice / anti-references.
- [`BASELINE_REALITY.md`](BASELINE_REALITY.md) — sister bridge file for per-audience reading (Impeccable v3.1+ multi-audience gate).
- [`SOP-HLK_TOOLING_STANDARDS_001.md`](docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7 — Impeccable governance contract (thin-redirect pattern).
- `.cursor/skills/impeccable/SKILL.md` — Impeccable entry skill.
- `.cursor/skills/impeccable/reference/` — per-command reference (e.g. `polish.md`, `critique.md`, `audit.md`, `typography.md`).
