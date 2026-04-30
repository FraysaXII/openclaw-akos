---
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika Research
program_id: PRJ-HOL-FOUNDING-2026
plane: advops
topic_ids:
  - topic_enisa_company_dossier
artifact_role: derived
intellectual_kind: figma_visual_source
authority: Operator (Figma file owner)
last_review: 2026-04-30
last_visual_fix_pass: 2026-04-30
---

# Figma file — Holistika Research Company Dossier

> **Initiative 28 P4 deliverable + Initiative 29 P1 visual fixes (2026-04-30).** This file records the Figma URL of the visual SSOT for the company dossier and the inventory of layout primitives. The Figma file is the **visual** SSOT; the slide content is sourced from `deck_slides.yaml`.

## Canonical Figma file

- **Name**: `Holistika Research - Company Dossier (ENISA 2026)`
- **File key**: `yiPav7BLxUulNFrrsoKJqW`
- **URL**: <https://www.figma.com/design/yiPav7BLxUulNFrrsoKJqW>
- **Team**: `Fayçal Njoya's team` (`team::1297934312456731046`)
- **Editor type**: Figma design
- **Page**: `Company Dossier v1`
- **Slide frames**: 14 frames at 1440 × 810 px each, named `01 · Cover` through `14 · Siguiente paso`
- **Authoring**: programmatic build via the Figma MCP `use_figma` Plugin API, sourced from [`deck_slides.yaml`](deck_slides.yaml) and [`deck-visual-system.md`](deck-visual-system.md)
- **Build date**: 2026-04-30

## Frame inventory

| Slide id | Frame name | Theme |
|:---|:---|:---|
| `01-cover` | `01 · Cover` | dark (gradient) |
| `02-problem` | `02 · Section: El problema` | dark |
| `03-insight` | `03 · Section: La idea` | dark |
| `04-solution` | `04 · Solución` | light |
| `05-method` | `05 · Método` | light |
| `06-proof` | `06 · Tracción / Proof` | light |
| `07-product-spotlight` | `07 · KiRBe Spotlight` | light |
| `08-why-now` | `08 · Section: Por qué ahora` | dark |
| `09-market-icp` | `09 · Mercado e ICP` | light |
| `10-business-model` | `10 · Modelo de entrega` | light |
| `11-moat` | `11 · Por qué difícil replicar` | light |
| `12-roadmap` | `12 · Roadmap 0-24m` | light |
| `13-enisa-fit` | `13 · Encaje ENISA` | light |
| `14-ask` | `14 · Siguiente paso` | light |

## Drift handling rule

Per the master roadmap §7 (Drift handling rule):

1. The **Markdown / YAML SSOT** (`deck_slides.yaml`, `deck_story_es.md`) wins for **content**.
2. The **Figma file** wins for **visual layout** decisions made directly on the canvas (component spacing, exact sizing, fine-typography refinements).
3. Any **Figma copy edit** that diverges from the YAML must be **backported to the YAML** before this initiative closes. The visual system stays governed.

## How to refresh the Figma file from the YAML

If the operator edits `deck_slides.yaml`, the simplest re-sync paths are:

- **Light edits (single slide, copy-only)**: edit the slide directly in Figma, then backport the change to `deck_slides.yaml` before commit.
- **Structural edits (slide added/removed/relayout)**: re-run the Figma MCP `use_figma` build. The build script body is preserved across the I28 commits in `docs/wip/planning/28-investor-style-company-dossier/reports/figma-build-log-2026-04-30.md` (one entry per `use_figma` call) and can be replayed by the agent in a fresh chat.

## Export to PDF

The Figma REST API export path requires an operator personal access token; it is not connected via the MCP today. Two operator paths produce the deck PDF:

1. **Figma desktop / web app**: open the file → `File` → `Export frames to PDF` → select all 14 frames → confirm. Output lands at the operator's chosen path.
2. **HTML preview re-export**: open [`docs/presentations/holistika-company-dossier/index.html`](../../../../../../presentations/holistika-company-dossier/index.html) in Chrome → `Ctrl + P` → `Save as PDF` → landscape, no margins, background graphics on. The HTML preview is the **derived deterministic** alternative to Figma; it produces visually-equivalent output via the governed `scripts/build_company_deck.py` pipeline.

The PDF hash + file path are recorded in `docs/wip/planning/24-hlk-communication-methodology/reports/uat-adviser-email-sent-2026-04-30.md` once the operator picks one of the two paths and exports.

## Initiative 29 P1 visual fix pass (2026-04-30)

The initial programmatic build (Initiative 28 P4) shipped frames whose interior auto-layout containers had the wrong sizing flags after `appendChild`. The screenshot survey showed body content children sized to ~100 px wide instead of 1280, and grid containers (capability grid, spotlight grid, ICP grid, business-model stack, moat grid, roadmap grid, ENISA fit, funds row, ask lines, method stripes, solution grid) had heights of ~100 px instead of HUG'ing to their content.

The I29 P1 fix pass walked every body slide and:

1. Set every direct child of `body content` / `section content` to `layoutSizingHorizontal: 'FILL'` (35 children fixed across 11 slides).
2. Set every grid/stack container to `layoutSizingVertical: 'HUG'` (14 containers fixed; capability grid is now 353 tall, spotlight grid 442 tall, business-model stack 387 tall, roadmap grid 470 tall, etc.).
3. For slide 06: walked into each capability card and forced `card head / body / tags / foot` to FILL the card width (241.6 px), and forced each tag pill to HUG horizontally so the full label is visible.
4. For slide 09: forced each ICP signal pill to HUG so labels like `CLIENTE DIRECTO · SERVICIO PROFESIONAL` fit fully.
5. For slide 10: forced each `bm tag` pill to HUG so `PRODUCTO - METODO EJECUTABLE` and `SAAS RECURRENTE` render fully.
6. For slide 13: changed `funds row` to `layoutWrap: 'WRAP'` so the four use-of-funds lines render as a 2x2 grid (was clipped 1x4).
7. For slide 07: cleared explicit `maxWidth` on the spotlight-left body and pull-quote text and forced FILL within the column so prose wraps properly.

Visual verification: every slide screenshot via Figma MCP `get_screenshot` matches the [`deck-visual-system.md`](deck-visual-system.md) spec.

## Reusable layout primitives (current state)

The 14 frames currently use the following layout primitives directly. Each is a candidate for promotion to a Figma Component when the operator wants the design-system upgrade (deferred follow-up):

| Primitive | Used on slides | Promote to Component? |
|:---|:---|:---|
| Brand monogram (`H` in teal-bordered tile) | 01 (cover) | High value — appears once but identity-critical |
| Body slide shell (eyebrow + headline + content + footer) | 04, 05, 06, 07, 09, 10, 11, 12, 13, 14 | Highest value — 10 slides reuse it |
| Section opener shell (big number + label + headline + body, dark surface) | 02, 03, 08 | High value — 3 slides reuse it |
| Capability card (head/body/tags/foot) | 06 (×5) | High — already a clear card pattern |
| Stat block (big number + small-caps label) | 06 (×4) | High |
| ICP card (title + body + signal pill) | 09 (×3) | Medium |
| Business-model row (tag-wrap + title + body) | 10 (×3) | Medium |
| Moat card (title-teal + body) | 11 (×4) | Medium |
| Roadmap window (dot + window-label + title + deliverables) | 12 (×3) | Medium |
| Fit card (title-teal + body) | 13 (×3) | Medium |
| Ask line (arrow circle + body) | 14 (×3) | Medium |
| Slide footer (org + page count) | 04-14 | High — appears 11 times |

**Componentization is deferred to a follow-up initiative.** The 14 slides are visually correct as-is; converting primitives to components is a future-proofing investment best done when the next deck (e.g. an investor-specific variant) needs the same primitives.

## How to apply small copy edits in Figma

Single-slide copy fixes can be done directly on the slide frames. For text-only changes:

1. Open the Figma file at the URL above.
2. Navigate to the relevant frame (e.g. `06 · Tracción / Proof`).
3. Edit the text node directly.
4. **Backport** the change to [`deck_slides.yaml`](deck_slides.yaml) before commit (drift-handling rule §1).

For structural changes (new slide, new card, new section), prefer the YAML route: edit `deck_slides.yaml`, run `py scripts/build_company_deck.py` (HTML preview), then re-apply the YAML structural change to Figma via a `use_figma` MCP call.

## Cross-references

- [`deck_slides.yaml`](deck_slides.yaml) — slide structured data SSOT
- [`deck_story_es.md`](deck_story_es.md) — slide narrative SSOT
- [`deck-visual-system.md`](deck-visual-system.md) — visual system spec
- [`scripts/build_company_deck.py`](../../../../../../../scripts/build_company_deck.py) — HTML preview build script
- [`docs/presentations/holistika-company-dossier/`](../../../../../../presentations/holistika-company-dossier/) — HTML preview folder
- [`docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md`](../../../../../../wip/planning/28-investor-style-company-dossier/master-roadmap.md) — Initiative 28 master roadmap
- [`docs/wip/planning/29-multi-phase-consolidation/master-roadmap.md`](../../../../../../wip/planning/29-multi-phase-consolidation/master-roadmap.md) — Initiative 29 master roadmap (this fix pass)
- [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../../Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.6 — canonical Figma governance contract
- [`FIGMA_FILES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/FIGMA_FILES_REGISTRY.md) — canonical registry of governed Figma files
