---
language: en
status: active
canonical: true
role_owner: Brand Manager + UX Designer + PMO (joint)
classification: way_of_working
intellectual_kind: contract_canonical
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - BRAND_COUNTERPARTY_README_CONTRACT.md
  - BRAND_FRENCH_PATTERNS.md
  - BRAND_SPANISH_PATTERNS.md
  - BRAND_REGISTER_MATRIX.md
  - BRAND_DISCIPLINE_ONTOLOGY.md
---

# BRAND_MULTILINGUAL_CONTRACT — Per-engagement language + four-surface matrix

> Authored I70 P7 per plan section 7. Codifies the per-engagement language declaration discipline + the four-surface multilingual matrix + cross-language register considerations. Cross-references existing `BRAND_FRENCH_PATTERNS.md` + `BRAND_SPANISH_PATTERNS.md` + `BRAND_REGISTER_MATRIX.md` (all post-P4.5 wave 1 at federated home).

## 1. The thesis

Multilingual operability is a **governance property, not a translation cost** (per `KM_CHANNEL_VALUE_NARRATIVE.md` §3 Claim 4). Each customer-facing engagement declares its language(s) up-front via frontmatter; the render pipeline + per-language validators enforce per-language register discipline; the four-surface matrix below codifies which surfaces ship in which languages.

Today three audience languages are active: **French** (SUEZ + customer surfaces; Tier 0 register), **Spanish** (Asesoría + future ES legal advisor; Tier 1 register), **English** (operator-internal + advisor-EN; Tier 2 register). Future engagements may add German + Portuguese; the contract scales by adding new BRAND_<LANG>_PATTERNS.md per language.

## 2. Per-engagement language declaration (frontmatter contract)

Every engagement folder under `Think Big/Clients/<YYYY>-<slug>/` or `Think Big/Advisers/<YYYY>-<slug>/` declares its language inventory at the engagement-folder README. Per the `BRAND_COUNTERPARTY_README_CONTRACT.md` (sibling at this canonicals/) the structure is **3 separate files** per Conundrum 7 + D-IH-70-P:

```
2026-<slug>/
├── README.md            (5-line pointer; lists the per-language READMEs)
├── README.fr.md         (full FR; if FR is in the language inventory)
├── README.en.md         (full EN; if EN is in the language inventory)
├── README.es.md         (full ES; if ES is in the language inventory)
├── 00-internal/
├── 01-operator-pack/
├── 02-customer-pack/
└── ...
```

The 5-line `README.md` pointer:

```markdown
# <Engagement title>

This engagement is bilingual / trilingual / etc. Per-language READMEs:
- [README.fr.md](README.fr.md) — version française (audience client + EFA Académie partenaire)
- [README.en.md](README.en.md) — English version (advisor + investor + AKOS-internal)
- [README.es.md](README.es.md) — versión en español (Asesoría sister-business)
```

## 3. Four-surface multilingual matrix

Each engagement consists of four surfaces; each surface declares its language(s) per the matrix:

| Surface | Languages | Voice tier | Register source |
|:---|:---|:---|:---|
| **Engagement README** | All declared engagement languages (per §2; 3 files) | Tier 1 (peer_consulting) | BRAND_REGISTER_MATRIX |
| **Counterparty README** | Counterparty's primary language only | Tier 1 (peer_consulting) | BRAND_REGISTER_MATRIX + BRAND_COUNTERPARTY_README_CONTRACT |
| **Customer pack** (deck + proposal + tarification + Gantt) | Customer's primary language; brand cobranding aware | Tier 1 (peer_consulting) | BRAND_<LANG>_PATTERNS + BRAND_COPYWRITING_DISCIPLINE |
| **Operator pack** (cdc-feasibility-shape + discovery-questionnaire + operator proposal + operator deck) | Operator's working language (typically EN; engagement-specific override allowed) | Tier 2 (academic-formal) | BRAND_REGISTER_MATRIX |

**Worked example — SUEZ engagement:**

- Engagement language inventory: FR (customer + EFA partner), EN (operator-internal).
- Engagement README: 3 files (README.md pointer + README.fr.md + README.en.md) — sibling commit.
- Counterparty README: FR only (counterparty primary; SUEZ is FR-corp).
- Customer pack: FR (deck.customer.fr.md, proposal.customer.fr.md, tarification.customer.fr.md, gantt.customer.fr.md). Tier 1 peer_consulting register.
- Operator pack: FR for SUEZ-specific docs (cdc-feasibility-shape.fr.md, etc.) — exception to default-EN because operator's working language for this engagement happens to be FR (operator + EFA partner co-author in FR). Tier 2 academic-formal.

## 4. Per-language register considerations

Cross-references the existing per-language pattern canonicals:

- **FR** → `BRAND_FRENCH_PATTERNS.md` (Marketing/Brand/canonicals/) §5 anglicism table + §5.1 performative-French anti-patterns. Tier 0 (peer_consulting; concrete-numbers-anchored) is preferred for customer-facing FR. Tier 2 (formal *vous*; academic register) for advisor-facing FR. Drift gate: `validate_brand_voice_register.py` strict mode (since I66 P5 incr 4).
- **ES** → `BRAND_SPANISH_PATTERNS.md` (Marketing/Brand/canonicals/) §13 boilerplate ES copy alignment. Tier 1 academic-formal *usted* register; no anglicisms. Drift gate same as FR.
- **EN** → no dedicated patterns canonical (the existing `BRAND_VOICE_FOUNDATION.md` covers EN as default). Tier 1 (peer_consulting) for customer-facing; Tier 2 (academic-formal) for investor / ENISA / advisor-facing.

When adding a new language: author `BRAND_<LANG>_PATTERNS.md` at `Marketing/Brand/canonicals/`, extend `validate_brand_voice_register.py` to parse + apply the new patterns, and update this contract's §3 matrix.

## 5. Cross-language consistency contract

When an engagement ships in multiple languages, per-language artifacts must:

1. **Carry equivalent semantic content.** A claim made in the FR deck must be present in the EN deck (and vice versa). Drift surfaces via the `validate_dossier_companion_drift.py` validator (existing; I66 P7).
2. **Use per-language register, not translation.** `BRAND_FRENCH_PATTERNS.md` §5 explicitly forbids anglicisms; `BRAND_SPANISH_PATTERNS.md` §13 enforces *usted* + no-anglicisms. The agent does NOT translate-then-render; it re-authors per-language.
3. **Honor cross-language idiom.** A FR positive-claim register replacement (per `BRAND_COPYWRITING_DISCIPLINE.md` 7-tic-families) doesn't always translate as a positive-claim in EN — the EN register may use slightly different rhetorical primitives. Per-language authoring respects per-language idiom.
4. **Pass per-language validators independently.** Each language has its own validator gate; FR + EN + ES surfaces all green before render.

## 6. Renderer extension contract

The render pipeline (`scripts/render_*_engagement_pdfs.py`) honors the per-language register at three points:

- **Frontmatter language detection** — every input markdown declares `language: fr | en | es | de | pt | ...`; renderer routes to per-language CSS variant (cover-strip labels, footer, page-counter format).
- **Per-language patterns embedded** — `_COVER_STRIP_LABELS` in `akos/hlk_pdf_render.py` carries per-language label translations (FR / EN / ES already shipped per I12 P12 + I66; future languages add as new entries).
- **Per-language brand-voice validation** — render fails with explicit error if `validate_brand_voice_register.py` red on the rendered language.

The renderer extension for P7 reserves: per-language footer customization (e.g., copyright + privacy policy text per language) — implementation deferred to I71.

## 7. Validator hooks (forward-link to I71)

- `validate_brand_multilingual_contract.py` (NEW; reserved): confirms every engagement folder declares `language:` inventory in `README.md`; confirms per-language READMEs match inventory; confirms customer-pack frontmatter `language:` matches engagement primary language.
- `validate_brand_voice_register.py` (existing) — extended in I71 with per-language tic-detection rule packs.
- `validate_dossier_companion_drift.py` (existing) — already checks deck/proposal/tarification companion presence; extends in I71 with per-language coverage check.

## 8. Cross-references

- Sister canonical: [`BRAND_COUNTERPARTY_README_CONTRACT.md`](BRAND_COUNTERPARTY_README_CONTRACT.md) — counterparty-README 3-rule pattern + path-portability + non-technical register.
- Per-language canonicals: `BRAND_FRENCH_PATTERNS.md`, `BRAND_SPANISH_PATTERNS.md` (Marketing/Brand/canonicals/).
- Voice charter: `BRAND_VOICE_FOUNDATION.md` (Marketing/Brand/canonicals/).
- Register matrix: `BRAND_REGISTER_MATRIX.md` (Marketing/Brand/canonicals/).
- Render pipeline: `akos/hlk_pdf_render.py` `_COVER_STRIP_LABELS` + per-language CSS variants.
- Existing validators: `validate_brand_voice_register.py`, `validate_dossier_companion_drift.py`.
- D-IH-70-P (P3 ratification): bilingual README pattern (3 separate files).
- Conundrum 7 — bilingual README pattern resolution.
- I70 plan section 7 — full P7 deliverable spec.
- Worked example: SUEZ bilingual READMEs (sibling commit at engagement folder).
