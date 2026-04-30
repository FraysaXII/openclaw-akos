# Holistika-tracked Figma files (canonical registry)

**Item type:** Canonical registry (see [PRECEDENCE.md](../../../compliance/PRECEDENCE.md))
**SSOT for visual layout:** Figma — not this file
**Revision:** Operators update rows when files are added, archived, renamed, or change ownership.
**Created:** 2026-04-30 (Initiative 29 P2)

---

## How to use

1. Add or edit a row when Holistika **starts tracking** a Figma file as a canonical visual SSOT.
2. Set `figma_url` to the canonical `https://www.figma.com/design/<file_key>` URL.
3. Set `linked_yaml_ssot` to the repo-relative path of the Markdown / YAML SSOT that drives this file's content (drift-handling rule §1: YAML wins for content). Use `—` for libraries that are not content-driven.
4. Add the file's `topic_ids` so the file is reachable from `TOPIC_REGISTRY.csv` and the KM Output 1 manifest contract.
5. Link the row from any vault doc that references the file.

**Security:** Do not paste service-account tokens, file passwords, or proprietary content. Use the Figma file URL only — access is gated by Figma's own permission system on the team workspace.

---

## Registry table

| file_slug | figma_url | team_key | class | primary_owner_role | topic_ids | linked_yaml_ssot | notes |
|-----------|-----------|----------|-------|--------------------|-----------|------------------|-------|
| `holistika-company-dossier-2026` | `https://www.figma.com/design/yiPav7BLxUulNFrrsoKJqW` | `team::1297934312456731046` | deck | Brand Manager | `topic_enisa_dossier_es` | [`docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml`](../../_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml) | Holistika Research — Company Dossier (ENISA 2026). 14 frames at 1440×810 px. Page `Company Dossier v1`. Built programmatically via Figma MCP `use_figma`; visual fix pass shipped in Initiative 29 P1. Referenced by [`figma-link.md`](../../_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/figma-link.md). |
| `holistika-design-system` | `https://www.figma.com/design/<TBD>` | `team::1359995555907300869` | design-system | Brand Manager | `topic_brand_visual_identity` | [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md`](../../Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md) | **Reserved slot — file not yet created.** Future Holistika design system: brand tokens (Variables collections per `BRAND_VISUAL_PATTERNS.md` §1), reusable components (capability card, stat block, section opener, body shell, ask line, roadmap window), foundations page. Triggers creation: when a second deck or partner-pitch file needs the same primitives, promote them here first, then consume by reference. Lives on the **holistika** team. |

### Class values

- **deck** — Stand-alone presentation deck or dossier (one deliverable; one or more pages of frames; content driven by a YAML SSOT in the repo).
- **design-system** — Reusable token + component library shared across multiple decks/products.
- **prototype** — Wireframe / interaction prototype for product or marketing exploration. Promoted to one of the other classes when stable.
- **library** — General-purpose reusable assets (icon set, illustration kit, photo library) that aren't a full design system.

---

## Drift handling rule (mirrors [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.6)

1. Markdown / YAML SSOT (named in `linked_yaml_ssot`) wins for **content**.
2. Figma wins for **visual layout** decisions made directly on the canvas.
3. Any Figma copy edit that diverges from the YAML must be backported to the YAML before the consuming initiative closes.

---

## Cross-references

- [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.6 — Figma SSOT contract, MCP tooling, naming conventions
- [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md) §"Output 1" — KM manifest extension with `paths.figma_url` and `paths.deck_yaml`
- [`REPOSITORIES_REGISTRY.md`](REPOSITORIES_REGISTRY.md) — sister registry for GitHub repositories (same governance shape)
- [`TOPIC_REGISTRY.csv`](../../../compliance/dimensions/TOPIC_REGISTRY.csv) — topic FK targets for the `topic_ids` column
- [`PRECEDENCE.md`](../../../compliance/PRECEDENCE.md) — overall compliance ranking
