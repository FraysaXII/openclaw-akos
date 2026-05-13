---
candidate_id: I74
title: Brand-tooling productization (TRIGGER-2 OS-library fork preparation)
status: candidate
authored: 2026-05-12
last_review: 2026-05-13
parent_initiative: 70 (closing scaffold)
priority: 4
language: en
---

# I74 candidate — Brand-tooling productization

> **Candidate scaffold (deepened 2026-05-13).** Promoted to `active` only when **TRIGGER-2** fires (≥2 external requests for AKOS doctrine consumption without source-fork) AND I70 + I71 + I72 + I73 are closed AND HLK Tech Lab capacity is available. Reactive trigger: today there are **0** external requests, so this candidate sits dormant by design. Master-roadmap to be authored at `docs/wip/planning/74-brand-tooling-productization/master-roadmap.md` upon promotion.

## 1. Operating story

I70 P5–P7 produced a brand-discipline canon-set that is, in aggregate, **portable methodology** rather than a Holistika-only artifact: the 7 tic families (`BRAND_COPYWRITING_DISCIPLINE`), the 5-level confidence ladder × 4-quadrant audience matrix (`BRAND_GANTT_DISCIPLINE`), the 3-file bilingual README pattern (`BRAND_MULTILINGUAL_CONTRACT`), the engagement-counterparty README contract (`BRAND_COUNTERPARTY_README_CONTRACT`), the per-locale register matrix (`BRAND_REGISTER_MATRIX`). I71 makes this canon **enforceable** via four validator packs. The next governance question is whether the canon is also **distributable**: can a non-Holistika org consume the brand-discipline as a methodology library (per `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §15.2 TRIGGER-2 = "AKOS-as-library consumed externally")?

The license posture is already set in `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`: **the brand marks are Holistika's; the discipline is portable methodology**. So the productization shape is:

- A library (e.g. `@holistika/akos-brand`) that exports the **rules** (validators + rule-pack YAMLs) without the **identity** (no Holistika logos / palette / counter-cover marks).
- A second library (`@holistika/madeira-agent` or similar) that productizes the AIC-as-category MADEIRA agent-companion pattern (per `MADEIRA-AKOS/STATUS.md` §3 + `HLK_ERP_ARCHITECTURE` §8 AKOS-complete-enough trigger).
- License documentation that distinguishes **methodology consumption** (free / open) from **brand-mark licensing** (Holistika-only).

This is **reactive**, not proactive: I74 should not productize speculatively. The trigger is concrete — 2+ external orgs requesting the doctrine without wanting to fork the AKOS repo. If that signal stays at zero indefinitely, I74 stays a candidate; the canon serves Holistika's customers and that's enough.

## 2. Strands

### Strand A — Brand-discipline library (`@holistika/akos-brand`)

| Deliverable | Source |
|:---|:---|
| `validators/` | I71-shipped Strand A packs (A1–A4 = voice register + Gantt confidence + multilingual + render ownership). |
| `rule-packs/` | YAML rule packs from I71 P1–P5 (`register-pack.yml`, `gantt-pack.yml`, `multilingual-pack.yml`, `render-ownership-pack.yml`). |
| `templates/` | Bilingual README 3-file pattern + counterparty README template + per-locale register matrix scaffold. |
| `docs/` | Methodology overview (no brand marks); installation; per-validator usage guide. |

### Strand B — Render pipeline as reusable Python package

- Extract `scripts/render_*_engagement_pdfs.py` + `akos/hlk_pdf_render.py` into `@holistika/akos-render` (Python package).
- License: discipline portable; brand marks (counter-cover, color palette) injected only when consumer is a Holistika-licensed org.
- Distribution channel: PyPI (or private index initially while pre-1.0).

### Strand C — MADEIRA agent productization (`@holistika/madeira-agent`)

- Trigger gate: per `HLK_ERP_ARCHITECTURE` §8, MADEIRA productization gates on **AKOS-complete-enough** (a separate operator ratification).
- AIC-as-category framing per `D-IH-70-V`: MADEIRA was originally conceived as the L6 founder-companion AI agent that today's Cursor-agent interactions empirically embody. Productization = packaging this pattern.
- Deliverable: agent-prompt library + tool catalog + MCP cross-reference contract; consumer plugs into their own LLM stack.

### Strand D — License documentation + brand-mark separation

- `LICENSE_METHODOLOGY.md` — methodology = portable; brand-marks = Holistika-only.
- `BRAND_LICENSING_GUIDE.md` for would-be consumers.
- Trademark filings reconciliation per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`.

## 3. Phase scaffold

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P0** | — | Charter + INITIATIVE / DECISION / OPS rows + master-roadmap (post-TRIGGER-2 firing) | — |
| **P1** | D | License documentation + brand-mark separation contracts | OPS-74-1 |
| **P2** | A | `@holistika/akos-brand` library: validators + rule-packs + templates | OPS-74-2 |
| **P3** | B | `@holistika/akos-render` package extraction + PyPI publication | OPS-74-3 |
| **P4** | C | `@holistika/madeira-agent` (gated on AKOS-complete-enough trigger) | OPS-74-4 |
| **P5** | — | First external consumer onboarding UAT | — |
| **P6** | — | Closing UAT + INITIATIVE_REGISTRY closure | — |

## 4. Conundrums (open at candidate stage)

1. **C-74-1 — Library scope: validators-only vs validators+templates+SOPs**: a thin validators-only library is faster to ship; a thick library is more useful. Default = validators+templates; SOPs stay in vault. Ratify pre-P2.
2. **C-74-2 — Distribution channel: public PyPI vs private index pre-1.0**: private index reduces blast radius if API breaks; public PyPI signals seriousness. Default = private until 1.0. Ratify pre-P3.
3. **C-74-3 — MADEIRA gate criteria**: what counts as "AKOS-complete-enough"? Need a concrete checklist (e.g. all I70+I71+I72+I73 closed + 2 quarters of stable operator usage + ≥3 distinct engagement classes consumed). Ratify pre-P4.
4. **C-74-4 — License separation enforceability**: how does the library detect brand-mark misuse without phoning home? Default = honor system + audit clause in license; no telemetry. Ratify pre-P1.
5. **C-74-5 — Versioning relationship to AKOS SemVer**: library SemVer follows AKOS SemVer minor (so I74 library v1.x tracks AKOS v3.x) OR independent SemVer? Default = independent (I71 Strand C1 codifies AKOS as a release line, not a methodology channel). Ratify pre-P2.

## 5. Decision preview (D-IH-74-* rows likely to mint)

- **D-IH-74-A** — license documentation + brand-mark separation contract.
- **D-IH-74-B** — `@holistika/akos-brand` library architecture (scope + distribution channel).
- **D-IH-74-C** — `@holistika/akos-render` package architecture + PyPI publication.
- **D-IH-74-D** — `@holistika/madeira-agent` architecture (post-AKOS-complete-enough ratification).
- **D-IH-74-CLOSURE** — initiative closure.

## 6. Spin-out trigger conditions (all-of)

- **TRIGGER-2 fires**: ≥2 external orgs request AKOS doctrine consumption without source-fork — **NOT MET (count: 0)**.
- I70 closed — **MET** 2026-05-13.
- I71 closed — **PENDING** (active).
- I72 closed — **PENDING** (candidate).
- I73 closed — **PENDING** (candidate).
- Founder + Brand Manager approval (license posture + brand boundaries) — **PENDING**.
- HLK Tech Lab capacity available (per `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16.3 transition trigger) — **PENDING**.

## 7. Risk register (top 5)

| Risk | Severity | Mitigation |
|:---|:---:|:---|
| Speculative productization without TRIGGER-2 firing → wasted effort | Critical | Reactive trigger gate; this candidate sits dormant until ≥2 external requests land. Document the trigger threshold prominently in §6 above. |
| Brand-mark licensing erosion (consumers ship with Holistika marks intact) | High | C-74-4 default = honor system + audit clause; no auto-detection feasible without telemetry; review at P5 first-consumer UAT. |
| Library API breaks downstream consumers | Medium | C-74-2 default = private index until 1.0; SemVer per C-74-5; deprecation policy in license. |
| MADEIRA productization premature (before AKOS-complete-enough) | Medium | C-74-3 explicit gate criteria; P4 cannot start until criteria met. |
| Library + vault drift (validators in library lag behind I71 vault canon) | Medium | Library imports validators from a single SSOT (the vault) rather than copy; release-gate checks equivalence. |

## 8. Cross-references

- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §15.2 — TRIGGER-2 (AKOS-as-library consumed externally) + Scenario B (full OS-library fork).
- `MADEIRA-AKOS/STATUS.md` §3 — TRIGGER-2 details + Scenario B activation.
- `HLK_ERP_ARCHITECTURE.md` §8 — AKOS-complete-enough trigger gates MADEIRA productization.
- `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` — license posture for non-Holistika orgs.
- `D-IH-70-V` (P2.5 sub-decision) — AIC-as-category framing; MADEIRA productization vector.
- I71 master roadmap (Strand A packs are the source for `@holistika/akos-brand` validators): [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md).
- I71 Strand C1 `D-IH-71-D` (release-taxonomy ratification) — informs C-74-5 SemVer relationship.
- I70 P5 commit `240c448` (Brand sub-discipline ontology + 4 charters + `BRAND_COPYWRITING_DISCIPLINE.md`).
- I70 P6 commit `070aa53` (`BRAND_GANTT_DISCIPLINE.md`).
- I70 P7 commit `98c80f2` (`BRAND_MULTILINGUAL_CONTRACT.md` + `BRAND_COUNTERPARTY_README_CONTRACT.md`).
