# Initiative 28 — Investor-Style Holistika Company Dossier

**Document owner**: Compliance + Brand Manager (joint)
**Version**: 0.1 (Draft)
**Date**: 2026-04-30
**Status**: In execution
**Program mapping**: Initiative 27 follow-up (G-24-3 closure unblocked by a deck-grade artifact)
**Canonical plan**: `c:\Users\Shadow\.cursor\plans\investor_style_company_dossier_d4ca7ab6.plan.md`
**Workspace mirror**: this file

---

## 1. Executive summary

Initiative 27 shipped a brand-aligned, jargon-free founder dossier. Operator review identified that the artifact is still a workbench — useful for the founder and counsel, but not what an external reader (ENISA adviser / certifier / investor) actually expects. The expected artifact is an **investor-style company dossier**: short, persuasive, evidence-led, designed for visual reading rather than detailed operational consumption.

This initiative creates the new artifact, demotes the existing dossier to an **adviser evidence appendix**, and establishes a governed Markdown-SSOT → Figma → PDF workflow.

## 2. Mission

Replace the founder dossier as the primary external send with a 12-14 slide deck that:

- positions Holística Research as a serious operating company;
- proves capability with shipped products, not promises;
- explains the service-to-product path (KiRBe productization);
- demonstrates ENISA fit without leading with paperwork;
- preserves the existing structured evidence as a separately-attached appendix when an adviser asks for detail.

## 3. Accepted decisions

| ID | Decision | Source |
|:---|:---|:---|
| D-IH-28-1 | Audience = ENISA adviser + certifier-style reader + investor-like reader (single deck for all three) | Operator confirmation 2026-04-30 |
| D-IH-28-2 | Format = Figma deck (visual SSOT) + PDF deck (export, disposable) + governed Markdown narrative SSOT | Operator confirmation 2026-04-30 |
| D-IH-28-3 | Tone = hybrid: institutional enough for ENISA, compelling enough for a certifier or investor | Operator confirmation 2026-04-30 |
| D-IH-28-4 | Disclosure = full, but Holística-execution-led; partner names secondary, kept low-key (we may have many other partners; the lever is how we handle delivery, not who) | Operator confirmation 2026-04-30 |
| D-IH-28-5 | Workflow = Markdown narrative SSOT → React/HTML preview deck (governed) → optional Figma capture/refinement → PDF export | Plan canonical |
| D-IH-28-6 | Existing `dossier_es.md` is renamed in role to "Adviser Evidence Appendix" and is no longer the primary external send | Plan canonical |
| D-IH-28-7 | External tools (v0.dev, Lovable, Bolt, Gamma, Beautiful.ai, Claude Artifacts) are **inspiration-only**; canonical source stays in this repo | Plan canonical |
| D-IH-28-8 | Slack MCP is **optional**: useful for stakeholder review canvas only; not on the critical path | Plan canonical |

## 4. Constraints and non-goals

- **Out of scope**: building a full pitch tool, fundraising pitch deck for a specific round, marketing website redesign, web product redesign.
- **Out of scope**: re-architecting the existing `render_pdf_branded` pipeline — the new deck PDF comes from Figma export or a new HTML→PDF flow, not the dossier renderer.
- **Out of scope**: replacing the `dossier_es.md` content — it stays canonical for adviser-evidence purposes; only its **role** changes.
- **Constraint**: every slide claim must be traceable to a Holística-shipped artefact (existing repos, existing canonical CSV, brand asset). No fabricated metrics.
- **Constraint**: jargon-free per `BRAND_JARGON_AUDIT.md`. The existing render-time `TODO[OPERATOR]` → "Pregunta abierta" transform remains as a safety net, but the deck SSOT must be jargon-free in source.

## 5. Current-state reality

- Initiative 27 final hashes: dossier PDF `248E0B7B…`, appendix handoff PDF `FB36EF6F…`, cover email DOCX `F7793B2E…` (UAT report at `docs/wip/planning/24-hlk-communication-methodology/reports/uat-adviser-email-sent-2026-04-29.md`).
- Existing dossier still passes the jargon-audit (PR #25), but it is not deck-grade.
- Five capability cards and brand tokens are reusable.

## 6. Phase plan

| Phase | Goal | Primary outputs | Status |
|:---|:---|:---|:---|
| P0 | Deck brief + evidence triage | `deck-brief.md`, `evidence-triage.md` | In progress |
| P1 | Narrative SSOT | `deck_story_es.md`, `deck_slides.yaml` | Pending |
| P2 | Visual direction + design system mapping | `deck-visual-system.md` | Pending |
| P3 | Web/HTML preview deck (governed v0-style) | `docs/presentations/holistika-company-dossier/index.html` + assets, served via repo file or HTTP | Pending |
| P4 | Figma deck (capture + refine) | Figma file URL recorded in `figma-link.md` | Pending |
| P5 | PDF export + send-pack assembly | `artifacts/exports/holistika-company-dossier-…pdf`, hashes recorded | Pending |
| P6 | Governance + tests + closure | `tests/test_deck_jargon.py`, UAT update, decision-log close | Pending |

## 7. Asset classification

### Canonical (edit here first)

- [`docs/wip/planning/28-investor-style-company-dossier/deck-brief.md`](deck-brief.md) — deck audience/promise/proof/objections/ask
- [`docs/wip/planning/28-investor-style-company-dossier/evidence-triage.md`](evidence-triage.md) — main vs appendix vs discard mapping
- `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_story_es.md` — slide narrative (P1)
- `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml` — slide structured data (P1)
- `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md` — visual system (P2)

### Mirrored / derived

- `docs/presentations/holistika-company-dossier/` — HTML preview (P3)
- Figma file URL recorded at `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/figma-link.md` (P4)
- `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf` — gitignored export (P5)

### Reference-only

- Existing `dossier_es.md` → role change to **adviser evidence appendix**; content unchanged.
- Brand tokens (`BRAND_VISUAL_PATTERNS.md`), jargon audit (`BRAND_JARGON_AUDIT.md`), tooling SOP (`SOP-HLK_TOOLING_STANDARDS_001.md`) remain canonical and govern this work.

### Drift handling rule

If Markdown SSOT, HTML preview, Figma, and PDF disagree:

1. Markdown narrative SSOT wins for **content**.
2. Figma wins for **visual layout**.
3. HTML preview is a fast iteration surface, never the source of truth.
4. PDF is disposable and re-exported.
5. Any visual change made in Figma that affects copy must be backported to the Markdown SSOT before this initiative closes.

## 8. Verification matrix

- `py scripts/validate_hlk.py` — registry parity unaffected, but run for safety
- `py scripts/validate_hlk_vault_links.py` — new MD links must resolve
- `py scripts/validate_hlk_km_manifests.py` — new manifest (if any) for the deck topic
- New: `tests/test_deck_jargon.py` — assert deck SSOT contains zero forbidden tokens
- New: `tests/test_deck_slides_schema.py` — assert `deck_slides.yaml` has 12-14 slides each with required fields
- Manual: open the HTML preview in browser, eyeball the visual quality, then evaluate the Figma deck

## 9. Risks and rollback

| Risk | Mitigation | Rollback |
|:---|:---|:---|
| Deck still sounds AI-flavoured | Founder voice review after P1; keep slide copy short (≤ 80 words/slide); use sharp claims, not paragraphs | Revert to existing dossier as send artifact (no quality regression — old artifact still works) |
| Figma build takes too long | P3 HTML preview first; `generate_figma_design` capture as a layout reference; only refine final frames | Ship the HTML preview as a `print-to-PDF` artifact if Figma blocked |
| Visual quality regression vs current dossier | Reuse brand tokens; eyeball every slide before committing | Keep current `dossier_es.pdf` available as a fallback send |
| Partner names over-disclosed | "What we did" framing per slide; partner names optional footnotes; appendix-only for context | Strip partner mentions before send |
| Markdown ↔ Figma drift | Backport every Figma copy change before close; lint job in P6 | Re-render from Markdown SSOT |

## 10. Commit strategy

One commit per phase, phase-scoped. Each commit body includes the phase id, files changed, and the verification log.

## 11. Exit criteria

- Main deck PDF feels like a company / investor dossier (eyeball test).
- Figma file exists and is the visual SSOT.
- Main deck contains zero open questions, zero internal IDs, and zero TODO markers in slide copy.
- Existing `dossier_es.md` is unambiguously **role-tagged** as the adviser evidence appendix.
- Cover email references the deck first, appendix second.
- UAT report records: Figma URL, deck PDF hash, appendix PDF hash, optional HTML preview URL.

## 12. Cross-references

- Plan: `c:\Users\Shadow\.cursor\plans\investor_style_company_dossier_d4ca7ab6.plan.md`
- Brand tokens: [`BRAND_VISUAL_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md)
- Jargon audit: [`BRAND_JARGON_AUDIT.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md)
- Tooling SOP: [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md)
- Existing dossier (now appendix): [`dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md)
- I27 UAT report: [`uat-adviser-email-sent-2026-04-29.md`](../24-hlk-communication-methodology/reports/uat-adviser-email-sent-2026-04-29.md)
