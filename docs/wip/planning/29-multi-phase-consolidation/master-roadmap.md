# Initiative 29 — Multi-phase consolidation (visual fixes, design governance, Impeccable, Business Strategy SSOT)

**Document owner**: Brand Manager + System Owner + Founder (joint)
**Version**: 0.1 (Draft → in execution)
**Date**: 2026-04-30
**Status**: In execution
**Canonical plan**: `c:\Users\Shadow\.cursor\plans\initiative_29_multi-phase_consolidation_6617fb36.plan.md`
**Workspace mirror**: this file

---

## 1. Executive summary

Initiative 28 shipped a brand-aligned, jargon-clean company dossier in HTML + Figma + PDF, but two operator-flagged gaps remained: (a) some Figma slides had broken auto-layout sizing from the programmatic build, and (b) the deck's content layer ends without commercial substance — pricing, channels, unit economics, bootstrapping math, ROI, and POC-to-commercial mapping are all missing. Initiative 29 closes both gaps in one governed multi-phase run while also formalizing Figma as a first-class visual SSOT class and integrating the Impeccable Style design-skill bundle as a polish/critique layer that consumes (not duplicates) our existing brand SSOT.

## 2. Mission

Make the deck *say something* — pricing, channels, economics, milestones, ask — backed by canonical, governed strategy artifacts the founder owns and the agent can read. Make Figma a first-class governed visual SSOT class. Add Impeccable as a polish layer without parallel brand truth.

## 3. Accepted decisions (all operator-confirmed)

| ID | Decision | Source |
|:---|:---|:---|
| D-IH-29-1 | Single multi-phase initiative covering all four threads | Operator confirmation 2026-04-30 |
| D-IH-29-2 | Figma is a canonical visual SSOT class (governed via SOP §3.6 + new registry + KM Output 1 schema extension) | Operator: Figma now Pro plan |
| D-IH-29-3 | Impeccable installs at repo root in `.cursor/skills/`; bridge files (`PRODUCT.md` + `DESIGN.md`) replace `/impeccable teach` auto-output and redirect to canonical brand SSOT | Plan canonical |
| D-IH-29-4 | Business Strategy SSOT lives under `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/`; each artifact is a registered topic with `parent_topic=topic_business_strategy` | Plan canonical |
| D-IH-29-5 | Strategy artifacts ship with structure + research-grounded recommendations + `TODO[OPERATOR]` markers; founder fills at their pace | Plan canonical |
| D-IH-29-6 | Deck integration is **wiring** (`scripts/sync_deck_from_strategy.py`), not copy-paste; YAML stays SSOT | Plan canonical |
| D-IH-29-7 | All slide copy that lifts numbers must continue to pass `BRAND_JARGON_AUDIT.md` and the deck-build jargon gate | Plan canonical |
| D-IH-29-8 | Deck componentization in Figma (full library + slides as instances) is **deferred** to a post-merge follow-up; the in-place layout-sizing fixes from P1 are sufficient for the current send | Operator pragmatism — slides now visually correct |

## 4. Phase plan

| Phase | Goal | Status |
|:---|:---|:---|
| P1 | Fix all 14 Figma slide auto-layout breakage (in-place) + document componentization as deferred follow-up | Closed |
| P2 | Governance scaffolds: SOP §3.6 (Figma) + §3.7 (External design skill bundles) + `FIGMA_FILES_REGISTRY.md` + KM Output 1 Figma extension + cursor-rule sync triggers | Closed |
| P3 | Impeccable install + `PRODUCT.md` + `DESIGN.md` bridge files + first critique/audit report | In progress |
| P4 | Business Strategy SSOT scaffolds: 10 artifacts + POC CSV + 11 topic-registry rows | Pending |
| P5 | Deck integration: `sync_deck_from_strategy.py` + slide 9/10/12/13 wiring | Pending |
| P6 | Tests + validators + closure trail + commit + PR + admin-merge | Pending |

## 5. Asset classification

### Canonical (edit here first)

- `docs/wip/planning/29-multi-phase-consolidation/` — initiative folder (this doc + reports)
- `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-HLK_TOOLING_STANDARDS_001.md` §3.6 + §3.7 — Figma + Impeccable governance
- `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/FIGMA_FILES_REGISTRY.md` — registry of governed Figma files
- `docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md` — Output 1 Figma extension
- `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/` — 10 strategy artifacts (P4)
- `docs/references/hlk/compliance/dimensions/POC_TO_COMMERCIAL_MAP.csv` — POC mapping (P4)
- `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv` — 11 new topic rows (P4)
- `PRODUCT.md` + `DESIGN.md` — Impeccable bridge files at repo root

### Mirrored / derived

- Figma file `yiPav7BLxUulNFrrsoKJqW` — visual layout SSOT for the deck
- `docs/presentations/holistika-company-dossier/index.html` — re-derived after P5 wiring
- `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf` — re-rendered, gitignored

### Reference-only

- `.cursor/skills/impeccable/` — vendor bundle (Apache 2.0); not modified

### Drift handling rule

1. Markdown / YAML SSOT wins for **content**.
2. Figma wins for **visual layout**.
3. Strategy artifacts win over deck copy: the deck pulls from them, never the other way round.
4. PDF and HTML preview are disposable; re-render after any source change.
5. Impeccable's `PRODUCT.md` / `DESIGN.md` bridges never duplicate brand content.

## 6. Verification matrix

- `py scripts/validate_hlk.py` — overall PASS
- `py scripts/validate_hlk_vault_links.py` — PASS
- `py scripts/validate_hlk_km_manifests.py` — PASS
- `py scripts/validate_topic_registry.py` — PASS (16 topics after P4)
- `py scripts/probe_compliance_mirror_drift.py --verify` — PASS after P4 reseed
- New: `tests/test_business_strategy.py` — schema + jargon-audit on the 10 artifacts (P6)
- New: `tests/test_impeccable_bridge.py` — bridge-file integrity (P6)
- New: `tests/test_figma_files_registry.py` — registry schema + URL format + FK (P6)
- Existing tests: all continue to pass (≥ 71 + new ≈ 12 = 83+)

## 7. Cross-references

- Plan: `c:\Users\Shadow\.cursor\plans\initiative_29_multi-phase_consolidation_6617fb36.plan.md`
- I28 master roadmap: [`docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md`](../28-investor-style-company-dossier/master-roadmap.md)
- Tooling SOP: [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md)
- Brand SSOT: `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_*.md`
