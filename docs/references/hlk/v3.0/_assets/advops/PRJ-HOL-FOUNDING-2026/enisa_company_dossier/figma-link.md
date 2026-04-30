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
---

# Figma file — Holistika Research Company Dossier

> **Initiative 28 P4 deliverable.** This file records the Figma URL of the visual SSOT for the company dossier. The Figma file is the **visual** SSOT; the slide content is sourced from `deck_slides.yaml`.

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

## Cross-references

- [`deck_slides.yaml`](deck_slides.yaml) — slide structured data SSOT
- [`deck_story_es.md`](deck_story_es.md) — slide narrative SSOT
- [`deck-visual-system.md`](deck-visual-system.md) — visual system spec
- [`scripts/build_company_deck.py`](../../../../../../../scripts/build_company_deck.py) — HTML preview build script
- [`docs/presentations/holistika-company-dossier/`](../../../../../../presentations/holistika-company-dossier/) — HTML preview folder
- [`docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md`](../../../../../../wip/planning/28-investor-style-company-dossier/master-roadmap.md) — initiative master roadmap
