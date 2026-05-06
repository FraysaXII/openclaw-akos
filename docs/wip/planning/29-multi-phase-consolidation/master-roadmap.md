---
language: en
status: closed
initiative: 29-multi-phase-consolidation
initiative_id: INIT-OPENCLAW_AKOS-29
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-05
closed_at: 2026-05-05
closure_decision_id: D-IH-29-CLOSURE
---
# Initiative 29 — Multi-phase consolidation (visual fixes, design governance, Impeccable, Business Strategy SSOT)

**Document owner**: Brand Manager + System Owner + Founder (joint)
**Version**: 1.0 (Closed)
**Date**: 2026-04-30 → closed 2026-05-05 (engineering side, via I58 B.2)
**Status**: **Closed** — all six phases shipped (P1 Figma fix pass + P2 governance scaffolds + P3 Impeccable bridge + P4 Business Strategy SSOT + P5 deck-from-strategy wiring + P6 tests + closure UAT). UAT report at [`reports/uat-i29-multi-phase-consolidation-2026-04-30.md`](reports/uat-i29-multi-phase-consolidation-2026-04-30.md) carries `status: closed` since 2026-04-30; I58 B.2 ratifies via master-roadmap frontmatter flip and D-IH-29-CLOSURE note.
**Closed by**: Initiative 58 B.2 (Cycle 2 multi-track forward) per `docs/wip/planning/58-cycle-2-multi-track-forward/reports/b2-close-i29-2026-05-05.md`
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
| P1 | Fix all 14 Figma slide auto-layout breakage (in-place) + document componentization as deferred follow-up | **Closed** |
| P2 | Governance scaffolds: SOP §3.6 (Figma) + §3.7 (External design skill bundles) + `FIGMA_FILES_REGISTRY.md` + KM Output 1 Figma extension + cursor-rule sync triggers | **Closed** |
| P3 | Impeccable install + [`PRODUCT.md`](../../../../PRODUCT.md) + [`DESIGN.md`](../../../../DESIGN.md) bridge files + first critique/audit report at [`impeccable-critique-2026-04-30.md`](reports/impeccable-critique-2026-04-30.md) | **Closed** |
| P4 | Business Strategy SSOT scaffolds (10 artifacts) + `POC_TO_COMMERCIAL_MAP.csv` + 11 topic-registry rows | **Closed** |
| P5 | Deck integration: [`sync_deck_from_strategy.py`](../../../../scripts/sync_deck_from_strategy.py) + slide 9/10/12/13 wiring | **Closed** |
| P6 | Tests ([`test_business_strategy.py`](../../../../tests/test_business_strategy.py) 15 tests + [`test_impeccable_bridge.py`](../../../../tests/test_impeccable_bridge.py) 8 tests + [`test_figma_files_registry.py`](../../../../tests/test_figma_files_registry.py) 6 tests; combined 49 / 49 PASS) + validators + closure UAT [`uat-i29-multi-phase-consolidation-2026-04-30.md`](reports/uat-i29-multi-phase-consolidation-2026-04-30.md) | **Closed (2026-04-30; ratified 2026-05-05 via I58 B.2)** |

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
- I58 master roadmap: [`docs/wip/planning/58-cycle-2-multi-track-forward/master-roadmap.md`](../58-cycle-2-multi-track-forward/master-roadmap.md)

## 8. Closure note (D-IH-29-CLOSURE)

`status: closed` set 2026-05-05 under I58 Phase B.2 per the Cycle 2 multi-track forward plan
(`c:\Users\Shadow\.cursor\plans\cycle_2_multi-track_forward_(i58)_769da1a3.plan.md`).

**Engineering rationale (B.2 scope):**

- All six phases (P1 Figma fix, P2 governance scaffolds, P3 Impeccable bridge, P4 Business Strategy SSOT scaffolds, P5 deck-from-strategy wiring, P6 tests + UAT) shipped as independent commits between 2026-04-30 and 2026-05-05.
- The closure UAT report at [`reports/uat-i29-multi-phase-consolidation-2026-04-30.md`](reports/uat-i29-multi-phase-consolidation-2026-04-30.md) carried `status: closed` since 2026-04-30; only the master-roadmap frontmatter remained on `In execution` because the file is a long-form mirror of the canonical Cursor plan and was deliberately left in execution status pending final ratification at the I58 closure gate.
- I58 B.2 ratifies via:
  1. Frontmatter flip to `status: closed` (this commit).
  2. Phase plan rows P3-P6 flipped from `In progress` / `Pending` to **Closed** with cross-links to the actual delivered artifacts.
  3. Re-run of the I29 P6 regression suite: `py -m pytest tests/test_business_strategy.py tests/test_impeccable_bridge.py tests/test_figma_files_registry.py -q` → **49 / 49 PASS** (verified 2026-05-05).
  4. B.2 closure phase report at [`docs/wip/planning/58-cycle-2-multi-track-forward/reports/b2-close-i29-2026-05-05.md`](../58-cycle-2-multi-track-forward/reports/b2-close-i29-2026-05-05.md).

**Operator-side follow-ups (out of agent scope, tracked in backlog):**

- Figma componentization (full library + slides as instances) — explicitly deferred per D-IH-29-8; tracked in [I06 backlog](../06-planning-backlog-registry/master-roadmap.md).
- Founder-paced fill of `TODO[OPERATOR]` markers in the 10 Business Strategy SSOT artifacts — by design (D-IH-29-5); not a closure blocker.
- Re-render of the HTML/PDF dossier preview after any post-closure strategy edits — operator-triggered; templates and `sync_deck_from_strategy.py` are now in place.

**Per `.cursor/rules/akos-governance-remediation.mdc` commit discipline:** B.2 closure is one commit (frontmatter flip + this closure note + B.2 phase report under I58). No mixed concerns; no canonical CSV touched (P4's CSV work was already committed during the original I29 run).
