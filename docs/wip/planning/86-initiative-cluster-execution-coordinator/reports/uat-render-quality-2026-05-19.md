---
report_id: uat-render-quality-2026-05-19
intellectual_kind: uat_evidence
sharing_label: internal_only
parent_initiative: INIT-OPENCLAW_AKOS-86
authored: 2026-05-19
last_review: 2026-05-19
linked_decisions:
  - D-IH-86-P (external-render discipline canonization)
  - D-IH-86-Q (Wave F INFO-to-FAIL gate promotion)
linked_strands:
  - Wave F Strand 3b (UAT-evidence pass on rendered artifacts)
status: operator-review
role_owner: System Owner
co_owner_role: Brand & Narrative Manager
language: en
audience: J-OP
---

# UAT-evidence — External-render quality pass (Wave F Strand 3b)

## 1 — Purpose

Per the operator's second axis-2 ratify gate (2026-05-19; option B1 "strict modes per locale" + option A3 "Wave F = all 5 strands"), Wave F minted [`scripts/validate_locale_orthography.py`](../../../../scripts/validate_locale_orthography.py) as the mechanical orthography gate over language-tagged external-delivery surfaces. The operator's underlying concern was broader than the mechanical gate alone: *"the visual renders are correct but still have bugs, feel a little bit artificial at times, have orthography errors"* — i.e., orthography is one dimension among several (naturalness, visual polish) that together determine whether a rendered artifact lands as intended.

This report is the Wave F UAT-evidence pass per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract" — a per-artifact findings table over the 6 in-scope rendered artifacts at the Wave F closure commit. Two of the three dimensions (orthography PASS/FAIL + visual polish PASS/REVIEW + naturalness PASS/REVIEW) are mechanical/automated; the third (naturalness) requires operator sign-off because no validator today can assess prose-naturalness without LLM evaluation (D-IH-71-S deferred LLM-eval to a successor wave).

## 2 — In-scope artifacts (6)

| # | Source markdown | Audience | Language | Rendered surfaces | Render artifact(s) |
|---|---|---|---|---|---|
| 1 | [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md`](../../../../docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md) | J-ENISA | es | mail + pdf | `artifacts/exports/cover_email_company_dossier_es-2026-05-19.html` + manifest sidecar |
| 2 | [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_story_es.md`](../../../../docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_story_es.md) | J-ENISA | es | pdf + slide | `artifacts/exports/holistika-company-dossier-enisa-2026-05-19.pdf` (14-slide deck export, ~69 KB) |
| 3 | [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md`](../../../../docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md) | J-ENISA | es | mail + pdf | `artifacts/exports/cover_email_es-2026-05-19.html` + manifest sidecar |
| 4 | [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md`](../../../../docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md) | J-ENISA | es | pdf | `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-05-19.pdf` (~273 KB) |
| 5 | [`docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/01-our-pack/cover_email_legal_constitutor_es.md`](../../../../docs/references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/cover_email_legal_constitutor_es.md) | J-AD | es | mail + pdf | `artifacts/exports/cover_email_legal_constitutor_es-2026-05-19.html` + manifest sidecar |
| 6 | [`docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md`](../../../../docs/references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md) | J-AD | en | pdf | `artifacts/exports/adviser-handoff-legal-PRJ-HOL-FOUNDING-2026-2026-05-19.pdf` (~201 KB) |

A 7th surface (`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck-visual-system.md`) carries `audience: J-OP` only — operator-internal — and is exempt from external-render-trail enforcement per RULE 4. It IS in scope for the orthography validator because it is language-tagged (en) and the validator scans language-tagged surfaces regardless of audience. Findings for surface 7 land in §4 below alongside surface 6.

## 3 — Findings table (per dimension)

Three dimensions per artifact:

- **Orthography**: mechanical — `validate_locale_orthography.py` output. PASS = no anti-pattern hits in that language; REVIEW = hits surfaced.
- **Visual polish**: mechanical-ish — paired manifest sha256 present + valid + file opens correctly + no obviously broken layout. PASS = manifest valid + file inspectable; REVIEW = operator should open + visually inspect.
- **Naturalness**: operator sign-off — does the prose read as authored-by-a-human-native-speaker or as auto-generated? PASS = operator confirms; REVIEW = operator to assess in next chat.

| # | Source | Orthography | Visual polish | Naturalness | Operator-actionable findings |
|---|---|---|---|---|---|
| 1 | `cover_email_company_dossier_es.md` | PASS (0 ES hits) | PASS (HTML manifest valid; opens in browser) | REVIEW | Operator: confirm tone matches BRAND_SPANISH_PATTERNS §3 (peer_consulting register). |
| 2 | `deck_story_es.md` | PASS (0 ES hits) | PASS (14-slide PDF ~69 KB; renders 1440×810 px) | REVIEW | Operator: spot-check 3 random slides for typographic polish (em-dash discipline + curly quotes). Deck is the surface most likely to surface mechanical visual-typography drift (e.g., un-curly-quoted "..."). |
| 3 | `cover_email_es.md` | PASS (0 ES hits) | PASS (HTML manifest valid; opens in browser) | REVIEW | Operator: confirm tone is consistent with surface 1 (sibling cover email under same engagement). Two cover emails to J-ENISA in the same program should read as authored by the same hand. |
| 4 | `dossier_es.md` | PASS (0 ES hits) | PASS (PDF ~273 KB; renders via WeasyPrint per manifest) | REVIEW | Operator: confirm Spanish reads as authored by a native speaker — this is the longest-form ES surface (highest fatigue risk for "feels artificial" feedback). |
| 5 | `cover_email_legal_constitutor_es.md` | PASS (0 ES hits) | PASS (HTML manifest valid; opens in browser) | REVIEW | Operator: confirm tone is appropriate for J-AD (advisor pre-NDA register). Different than J-ENISA register. |
| 6 | `legal-constitutor-handoff-2026-05-18.md` | **REVIEW** (46 straight-double-quote hits in body prose; EN smart-quote threshold breach) | PASS (PDF ~201 KB; renders via WeasyPrint per manifest) | REVIEW | **Operator: triage the 46 straight-quotes**. Decide one of: (a) auto-curl via a render-step pass (preferred; transparent); (b) hand-edit the source markdown to use curly quotes (durable but tedious); (c) accept ASCII quotes as legitimate (lower brand-polish bar for adviser handoff). Per operator's standing feedback ("feel a little bit artificial at times"), recommend (a). |
| 7 | `deck-visual-system.md` (J-OP-only; out of external-render-trail scope; orthography in-scope) | **REVIEW** (22 straight-double-quote hits in body prose; EN smart-quote threshold breach) | N/A (operator-internal design doc) | N/A | Operator: same triage as surface 6 (a/b/c) but lower stakes — J-OP-only doc; no external recipient. Recommend (b) hand-edit if the doc is referenced by external surfaces, otherwise (c) accept. |

## 4 — Mechanical evidence — orthography validator output (full)

```text
[INFO] orthography en: docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck-visual-system.md — 22 straight-double-quote characters in body prose (threshold 4); consider curly quotes per BRAND_ENGLISH_PATTERNS §10 LLM-tone-tells
[INFO] orthography en: docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md — 46 straight-double-quote characters in body prose (threshold 4); consider curly quotes per BRAND_ENGLISH_PATTERNS §10 LLM-tone-tells
[INFO] PASS: validate_locale_orthography — scanned 38 ; language-tagged 38 ; with hits 2 ; total hits 68 (es=0 fr=0 en=68 ; strict_es=False strict_fr=False strict_en=False)
```

ES + FR have **zero** orthography findings across all 38 language-tagged surfaces under the validator's SCAN_GLOBS. The operator's specific concern about `ñ` / accent-leak in ES surfaces does **not** manifest in any in-scope ES surface today. EN surfaces carry the only orthography signal (straight-quote leak in 2 surfaces).

## 5 — Mechanical evidence — render-trail validator output (full)

```text
[INFO] PASS: validate_external_render_trail — scanned 76 ; external-tagged 6 ; with trail 6 ; pending tracker 0 ; missing trail 0 ; stale renders 0 ; with channel-tag 0 ; unknown channel codes 0 (strict=True ; strict_freshness=True)
```

All 6 external-tagged surfaces have paired render artifacts. Zero stale renders (every manifest's `source_sha256` matches the current source sha). Strict + strict-freshness modes both PASS at the Wave F closure commit. The validator is mechanically ready for the D-IH-86-Q gate promotion (P5 of Wave F).

## 6 — Operator sign-off checklist (≤ 7 items)

The operator reviews this report in the next chat session + signs off on each row by marking PASS / REVIEW-PENDING / REVIEW-CLOSED beside it. Per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract", this checklist is the SSOT acceptance signal.

1. **Orthography mechanical state acknowledged**: ES + FR clean; EN smart-quote findings on 2 surfaces named and triage path agreed (preferred: option (a) render-step auto-curl).
2. **Naturalness sign-off — surface 1 (cover_email_company_dossier_es)**: tone matches BRAND_SPANISH_PATTERNS §3 peer_consulting register. PASS / REVIEW.
3. **Naturalness sign-off — surface 2 (deck_story_es)**: spot-check 3 slides for typographic polish. PASS / REVIEW.
4. **Naturalness sign-off — surface 3 (cover_email_es)**: consistent voice with surface 1. PASS / REVIEW.
5. **Naturalness sign-off — surface 4 (dossier_es)**: longest-form ES surface; native-speaker assessment. PASS / REVIEW.
6. **Naturalness sign-off — surface 5 (cover_email_legal_constitutor_es)**: J-AD register (different from J-ENISA). PASS / REVIEW.
7. **Naturalness sign-off — surface 6 (legal-constitutor-handoff)**: EN prose quality (independent of smart-quote triage). PASS / REVIEW.

When all 7 rows close PASS or REVIEW-CLOSED, the operator marks the UAT report `status: closed` in frontmatter + commits an addendum citing the closure decision.

## 7 — Forward enhancements (deferred to next wave)

- **Render-step auto-curl (option (a) for surface 6)**: add a post-render step to `render_dossier.py` / `export_adviser_handoff.py` that runs a smart-quote conversion pass on the HTML/PDF output before the manifest seal. This is the systemic fix to the smart-quote leak class. Effort: small (1 commit; ~50 LoC).
- **Strict-EN orthography promotion**: once surfaces 6 + 7 close (option (a) or (b) or (c) ratified), promote `validate_locale_orthography.py` to `--strict-en` in the release-gate + verification-profiles. Mirror today's ES + FR posture (clean = ready for strict promotion).
- **LLM-eval for naturalness dimension**: per D-IH-71-S, an LLM-eval pass on each rendered artifact (with a per-locale rubric pulling from BRAND_<LANG>_PATTERNS.md as the SSOT contract) can replace operator-naturalness sign-off for most surfaces. Forward-charter to a successor initiative (suggested: I88+ once I76 MADEIRA productization closes).
- **Visual-polish automated audit**: integrate `axe-core` + visual-regression snapshots (`playwright + snapshot`) over the 6 rendered artifacts as a release-gate INFO row, mirroring [`playwright_a11y_smoke`](../../../../config/verification-profiles.json) precedent.

## 8 — Cross-references

- [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) — the umbrella rule this report evidences.
- [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract" — the report shape contract.
- [`scripts/validate_external_render_trail.py`](../../../../scripts/validate_external_render_trail.py) — render-trail validator.
- [`scripts/validate_locale_orthography.py`](../../../../scripts/validate_locale_orthography.py) — orthography validator (sister of above).
- [`SOP-EXTERNAL_RENDER_GATE_PROMOTION_001`](../../../../docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md) — the operator runbook for the D-IH-86-Q gate promotion that follows this UAT pass.
- [`BRAND_SPANISH_PATTERNS.md`](../../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_SPANISH_PATTERNS.md), [`BRAND_FRENCH_PATTERNS.md`](../../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_FRENCH_PATTERNS.md), [`BRAND_ENGLISH_PATTERNS.md`](../../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ENGLISH_PATTERNS.md) — the orthography rule SSOT per locale.
- D-IH-86-P + D-IH-86-Q in [`DECISION_REGISTER.csv`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
