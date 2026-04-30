# Holistika Research — Company Dossier (HTML preview)

> **Initiative 28 P3 deliverable.** Self-contained HTML deck rendered from the canonical slide narrative SSOT. The HTML is **derived**: edits go to the source files first, then `py scripts/build_company_deck.py` re-renders this folder.

## What this is

A 14-slide investor-style company dossier in Spanish. Aspect ratio 16:9 (1440 × 810 px design canvas). Targets ENISA advisers, certifiers, and investor-style readers in a single artifact.

The deck is the primary external send. The pre-existing structured founder dossier (`dossier_es.md`) is now its **adviser evidence appendix**, attached only when an adviser asks for detail.

## Source-of-truth files

| Role | Path |
|:---|:---|
| Slide structured data (SSOT) | [`deck_slides.yaml`](../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml) |
| Slide narrative (SSOT mirror, prose) | [`deck_story_es.md`](../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_story_es.md) |
| Visual system spec | [`deck-visual-system.md`](../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md) |
| Brand tokens | [`BRAND_VISUAL_PATTERNS.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md) |
| Jargon audit | [`BRAND_JARGON_AUDIT.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) |
| Build script | [`scripts/build_company_deck.py`](../../../scripts/build_company_deck.py) |
| Stylesheet | [`styles.css`](styles.css) |

## How to operate

### Build

```powershell
py scripts/build_company_deck.py
```

Re-renders [`index.html`](index.html) from the YAML SSOT plus `styles.css`. The rendered HTML is self-contained — the stylesheet is inlined so the file works as a single attachment.

### Validate without building

```powershell
py scripts/build_company_deck.py --check-only
```

Confirms the YAML schema, slide count (12-16), required fields per layout, and runs the jargon-audit token check (rejects `TODO[OPERATOR]` leaks, internal codenames, stack jargon, etc.).

### Open in browser

Open [`index.html`](index.html) directly in any modern browser. Use full-screen view for the closest match to the printed PDF.

### Print to PDF

In Chrome / Edge:

1. `Ctrl + P`.
2. Destination → **Save as PDF**.
3. Layout → **Landscape**.
4. Pages → **All**.
5. Paper size → **A4** *or* a custom 1440 × 810 px paper (more deck-like).
6. Margins → **None**.
7. Background graphics → **On**.

Result lands at the operator's chosen path. The `print` media query in `styles.css` strips the deck header band, removes shadows, and forces page breaks between slides.

## Drift handling

If the YAML, the rendered HTML, the Figma deck, and the operator-saved PDF disagree:

1. **Markdown / YAML SSOT wins** for content (slide copy, structure, ask).
2. **Figma wins** for visual layout (component sizes, exact spacing).
3. The HTML preview is a fast iteration surface, never the source of truth — it is re-rendered on every build.
4. The PDF is disposable and re-exported.
5. Any visual change made in Figma that affects copy must be backported to `deck_slides.yaml` before Initiative 28 closes.

## Status

- 14 slides covering: cover, problem, insight, solution, method, proof grid, KiRBe spotlight, why now, market & ICP, business model, moat, roadmap, ENISA fit & use of funds, ask.
- Zero `TODO[OPERATOR]` leaks (operator-side markers excluded by the jargon-audit gate in the build script).
- Brand tokens: teal `hsl(168 55% 38%)`, amber `hsl(38 80% 50%)`, warm-cream `hsl(40 20% 99%)`, deep-slate `hsl(220 16% 7%)`, Inter typography.
- This deck is **not** the same artifact as the structured founder dossier — that one is now the adviser evidence appendix, role-tagged in the master roadmap.
