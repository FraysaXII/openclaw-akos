---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P8
phase_name: PDF rendering + drift gates
recorded_at: 2026-05-10
---

# P8 — PDF rendering and drift gates self-checkpoint

## Files authored

| File | Role |
|:---|:---|
| `scripts/render_suez_engagement_pdfs.py` | Thin wrapper around `akos.hlk_pdf_render.render_pdf_branded`; renders the four FR external surfaces; strips the proposal's internal review checklist before rendering. |
| `artifacts/exports/2026-suez-webuy/cdc-feasibility-shape.fr.pdf` | CDC feasibility shape rendered PDF. |
| `artifacts/exports/2026-suez-webuy/discovery-questionnaire.fr.pdf` | Discovery questionnaire rendered PDF. |
| `artifacts/exports/2026-suez-webuy/proposal.fr.pdf` | Proposal rendered PDF (internal checklist stripped). |
| `artifacts/exports/2026-suez-webuy/deck-suez-webuy.fr.pdf` | Deck rendered PDF. |
| `artifacts/exports/2026-suez-webuy/render-manifest.json` | sha256 manifest for the closure trail. |

## Files redacted (forbidden-token sweep findings)

| File | Original | Replacement | Reason |
|:---|:---|:---|:---|
| `cdc-feasibility-shape.fr.md` §0 préambule (line 43) | `un agent logiciel peut générer la majorité` | `une application logicielle peut générer la majorité` | D-ENG-SUEZ-H — `agent` is forbidden in FR external surfaces (bridge-collaborator advisory at EFA prospection ~28:42). |
| `cdc-feasibility-shape.fr.md` F-03 (line 69) | `peut être pré-calculée par un agent logiciel` | `peut être pré-calculée par une application logicielle` | Same. |
| `deck-suez-webuy.objections.md` row 7 (line 33) | bridge-collaborator real name in objection wording | `Cette automatisation va remplacer la personne qui opère ?` | Collaborator-name redaction — D-ENG-SUEZ-D extends to internal companion files for this engagement. |

## Render-pipeline post-processing

`scripts/render_suez_engagement_pdfs.py` adds an in-pipeline `strip_internal_checklist()` step that removes the `## Liste de validation interne` block (and the preceding horizontal rule) from `proposal.fr.md` before handing the body to `render_pdf_branded`. The source markdown keeps the checklist for operator audit + the SOP-ENG_PROPOSAL_001 review trail; the PDF that ships externally never carries it.

Verification: source `proposal.fr.md` sha = `c5bc727acfef0488...` (carries the checklist body); rendered `proposal.fr.pdf` body strips the checklist (visual confirmation: PDF page count drops by one screen vs the markdown source's tail; rendered PDF sha = `14c295f16a5fb732...` after final re-render).

## Drift validators run

| Validator | Result | Notes |
|:---|:---|:---|
| `py scripts/validate_brand_baseline_reality_drift.py` | **PASS** | `BRAND_BASELINE_REALITY OK — dual-register contract holds; 7 internal token(s) checked` |
| `py scripts/validate_brand_jargon.py` | **PASS** | `BRAND_JARGON_AUDIT OK — 136 files scanned across 2 consumer repo(s); 0 forbidden tokens` |
| `py scripts/validate_brand_voice_register.py` | **PASS** | `BRAND_VOICE_REGISTER OK — 3 message file(s) scanned across 2 consumer repo(s); 0 register-pattern violations` |
| `py scripts/validate_hlk.py` | **PASS** for the four CSVs touched in this engagement (`baseline_organisation`, `process_list`, `GOI_POI_REGISTER`, `COUNTRY_WORK_CALENDAR`) — all dimension validators returned PASS. **Pre-existing FAIL** unrelated to this engagement: `INITIATIVE_REGISTRY: FAIL: 1 errors - INIT-OPENCLAW_AKOS-68: inception_decision_id 'D-IH-66-AC' not in DECISION_REGISTER.csv` (Initiative 68 dependency on a Initiative 66 decision row that has not landed). | This engagement does not depend on Initiative 68; pre-existing FAIL is a separate workstream's concern. |

The voice-register validator does not expose a `--locale fr` flag in this repo (per `py scripts/validate_brand_voice_register.py --help`); per plan fallback, the FR voice rules in `BRAND_FRENCH_PATTERNS.md` were applied during authoring (P4–P7) and grep-verified manually here.

## Manual grep pass — forbidden tokens

All grep performed against `docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/`.

| Token | Hits in body of FR external surfaces | Disposition |
|:---|---:|:---|
| bridge-collaborator real name (case-insensitive, accent-tolerant) | 0 | clean |
| `\bAKOS\b` | 0 (1 in proposal internal-checklist line 165, stripped before render) | clean in PDF |
| `\bCORPINT\b` | 0 | clean |
| `topic_` | 0 | clean |
| `baseline reality` | 0 (1 in proposal internal-checklist line 165, stripped before render) | clean in PDF |
| `\belicitation\b` | 0 (1 in proposal internal-checklist line 165, stripped before render) | clean in PDF |
| `\bcounterparty\b` (non-companion) | 0 (1 in deck frontmatter `companions:` field — frontmatter stripped before render) | clean in PDF |
| `\bagent\b` (non-companion) | 0 in CDC / proposal / deck / questionnaire body after redaction; 1 in proposal internal-checklist line 165 (stripped) | clean in PDF |
| competitor organisation name | 0 | clean |
| competitor end-client name | 0 | clean |
| competitor internal cost-model code | 0 | clean |
| Euro amount in `proposal.fr.md` | 0 | clean (per D-ENG-SUEZ-N — pricing is annexed in `commercial-schedule.md`, not inline) |
| Euro amount in `deck-suez-webuy.fr.md` | 0 | clean (deck slide 06 cites par-duration only, never euros) |

Companion files (`deck-suez-webuy.objections.md`, `deck-suez-webuy.counterparty-brief.md`) intentionally carry internal vocabulary per the dual-register exemption (`BRAND_TEMPLATE_REGISTRY.md` §3) and the explicit preamble note in each file body. The README.md in the same folder is a navigation/meta artefact, not a customer deliverable.

## Render-manifest summary

```
artifact: cdc-feasibility-shape.fr.pdf  md_sha=9feeb2bb7df01dff…  pdf_sha=4f312c2637f73b3f…
artifact: discovery-questionnaire.fr.pdf md_sha=0acc64ae87a811f6…  pdf_sha=3b0a29eb32862371…
artifact: proposal.fr.pdf                md_sha=c5bc727acfef0488…  pdf_sha=14c295f16a5fb732…
artifact: deck-suez-webuy.fr.pdf         md_sha=81c5dde266220c99…  pdf_sha=d6dcef97709767e9…
```

(values lifted from `artifacts/exports/2026-suez-webuy/render-manifest.json`)

## PDF renderer verdict

WeasyPrint wrote all four PDFs at first attempt — gradient cover hero band rendered successfully, branded body styling applied, no fallback to fpdf2 / pandoc. The cover metadata for each surface uses the FR title / subtitle / discipline strings declared in `scripts/render_suez_engagement_pdfs.py::SURFACES`.

## Cross-document consistency post-redaction

* `cdc-feasibility-shape.fr.md`: 24 functionalities preserved, all eligibility flags unchanged, `application logicielle` substitution carries the same technical meaning as `agent logiciel` did.
* Variant A / B / C scope references in the deck (slide 06) and proposal (§2 + §4) match the three `scope-{a,b,c}.yaml` files.
* `commercial-schedule.md` continues to be the single source of euro amounts for this engagement.

## Next

P9 — Cleanup + business-intent rename + competitor-inspiration deletion verification + .gitignore update + temp folder removal.
