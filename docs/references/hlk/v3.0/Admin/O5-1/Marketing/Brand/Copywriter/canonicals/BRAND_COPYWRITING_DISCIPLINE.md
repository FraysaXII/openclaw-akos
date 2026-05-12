---
language: en
status: active
canonical: true
role_owner: Copywriter
classification: way_of_working
intellectual_kind: discipline_canonical
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - ../../canonicals/BRAND_DISCIPLINE_ONTOLOGY.md
  - ../../canonicals/BRAND_VOICE_FOUNDATION.md
  - ../../canonicals/BRAND_REGISTER_MATRIX.md
  - ../../canonicals/BRAND_FRENCH_PATTERNS.md
  - ../../canonicals/BRAND_SPANISH_PATTERNS.md
  - ../../canonicals/BRAND_JARGON_AUDIT.md
---

# BRAND_COPYWRITING_DISCIPLINE — "Impeccable for copywriting"

> Authored I70 P5. Sub-discipline canonical for **Brand/Copywriter** under `BRAND_DISCIPLINE_ONTOLOGY.md`. Codifies the prose register at the sentence level: 7 named **AI-tone tic families** + 11 named **anti-pattern seeds** with positive-claim replacements + per-language register considerations + the validator rule pack contract for `validate_brand_voice_register.py` (rule pack implementation deferred to I71).

This canonical is the verbal companion to the visual `Impeccable` Cursor skill — both ensure customer-facing artifacts read + look like Holistika authored them, not an automated tool. The SUEZ engagement (I12 P12) provided the empirical material; I70 P0 surfaced the gap; this canonical closes it.

## 1. The thesis

Customer-facing prose has a tone register. AI-authored prose tends to drift toward a **performative-discipline tone** — over-symmetric, abstract-noun-heavy, repeatedly contrastive — that reads as "automated" even when it's grammatically correct. Impeccable copywriting is the discipline of catching those tics and replacing them with **positive claims** anchored in concrete operational reality.

The 7 tic families codified here are derived from:
1. The SUEZ deck (`deck.customer.fr.pdf`) review at I70 P0 §0.4 (11 line-precise rewrites).
2. The Impeccable visual discipline's prior art (no-em-dash-in-headlines + plain-language-over-jargon).
3. External research at `Marketing/Brand/Copywriter/wip/2026-impeccable-copywriting/` (Tier 3 WIP per blueprint §17) surveying public anti-AI-tone catalogs.

## 2. Seven AI-tone tic families

### Family 1 — `X, pas Y.` (FR) / `X, not Y.` (EN) / `X, no Y.` (ES) — contrastive

**Pattern.** Two-noun sentence asserting one and rejecting the other.

**Why it reads automated.** Symmetry feels manufactured; the contrast often does no work because Y was never plausibly the answer.

**Worked example (SUEZ deck slide 05, P0 step 7):**
- Before: `Une mémoire opérationnelle, pas une équipe sur étagère.`
- After: `La matière documentaire que nous tenons en interne est celle que vous récupérez.` (positive claim with concrete object)

**Detection regex (FR):** `\b\w+, pas \w+\.`
**Detection regex (EN):** `\b\w+, not \w+\.`
**Replacement strategy.** Drop the negation; assert the positive directly. Pull a concrete operational fact into the sentence.

### Family 2 — `n'est pas X. C'est Y.` (FR) / `is not X. It's Y.` (EN) — chained negation-then-affirmation

**Pattern.** Two adjacent sentences where the first negates and the second affirms.

**Why it reads automated.** The setup-payoff is too clean; reads as ChatGPT cadence.

**Worked example (SUEZ deck slide 06, P0 step 10 + proposal lead, P0.6 fix):**
- Before: `La friction n'est pas la décision. C'est la répétition d'un calcul...`
- After: `La friction réside dans la répétition d'un calcul...`

**Detection regex (FR):** `n'est pas .{1,40}\.\s*C'est`
**Detection regex (EN):** `is not .{1,40}\.\s*It's`
**Replacement strategy.** Collapse to a single sentence with `réside dans / lies in / consiste en` instead of the negation-affirmation pair.

### Family 3 — `une seule X` epigram (FR) / `a single X` (EN) / `una sola X` (ES) — false-singularity

**Pattern.** Phrase asserting a singular abstract noun (`une seule discipline`, `un seul réflexe`) where the singularity claim does no work.

**Why it reads automated.** "Une seule" is a marketing-fluff intensifier; the actual information value is the noun, not the singularity.

**Worked example (SUEZ deck slide 04 H2, P0 step 4):**
- Before: `Deux récits, une seule discipline.`
- After: `Deux récits, une même méthode.` (drops the false-singularity AND the cold "discipline" register)

**Detection regex (FR):** `\b(une|un) seule? \w+\b` (idiomatic uses like `une seule fois` = "only once" should be allowed via context check)
**Replacement strategy.** Keep concrete idiomatic uses (`une seule fois`, `une seule personne`); drop epigrammatic uses on H2 / cover slides.

### Family 4 — Triadic abstract-noun stack — `noun-phrase, noun-phrase, noun-phrase`

**Pattern.** Three abstract-noun phrases comma-separated in a single sentence.

**Why it reads automated.** Symmetric triplets are LLM-default rhetorical patterns; especially noticeable when the three terms are abstract (mécanique / litige / parc).

**Worked example (SUEZ deck slide 06 H2, P0 step 9):**
- Before: `Une mécanique répétée, un litige à éviter, sur un parc qui double.`
- After: `Vingt à cinquante demandes par jour, un parc qui double.` (concrete number + concrete fact)

**Detection regex.** Sentence with 2+ commas separating noun phrases that don't include verbs or concrete numbers.
**Replacement strategy.** Replace at least one element with a concrete number drawn from the operational reality. If three abstracts are needed, demand a verb anchor.

### Family 5 — `discipline` overuse — `Discipline X / Discipline Y / Discipline Z` repeating

**Pattern.** Three (or more) anchor titles starting with "Discipline" within 30 lines.

**Why it reads automated.** "Discipline" as a register prefix reads cold and academic; bulk-applied it implies the author can't think of an active verb.

**Worked example (SUEZ deck slide 04 anchor titles, P0 step 6):**
- Before: `Discipline qualité-donnée / Discipline gouvernance multinationale / Discipline projet vers logiciel`
- After: `Cadrer la qualité avant l'entrée / Tenir la règle entre filiales / Du cadre projet au logiciel`

**Detection.** Count `Discipline` in `<h3 class="anchor-title">` siblings; flag if ≥3 in 30 lines.
**Replacement strategy.** Replace each with the **anchor frame** (the active verb describing what the discipline does), not the methodology-tag.

### Family 6 — `C'est le X qui...` (FR) / `It's the X that...` (EN) — repeated openings

**Pattern.** Three (or more) anchor bodies starting with `C'est le réflexe qui...` / `It's the X that...`

**Why it reads automated.** Repetition of identical sentence openings reads as template fill-in. Breaks on the third instance.

**Worked example (SUEZ deck slide 04 anchor bodies, P0 step 5):**
- Before: `C'est le réflexe qui prévient un litige. C'est le réflexe qui protège l'opération. C'est le réflexe qui rend une mission reproductible.`
- After: Vary openings: `Le litige se prévient à l'entrée, pas à la facturation. La règle protège l'opération quand l'échelle change. Une mission reproductible sans son auteur — voilà le test.`

**Detection.** Three or more sibling `<p>` elements with identical 4-token openings.
**Replacement strategy.** Vary openings; let the second and third openings be different sentence structures; force concreteness.

### Family 7 — Operator-instruction echo — leaked-instruction prose in customer surfaces

**Pattern.** Customer-facing prose that reads as the operator's brief echoed back. Examples: `Présentation à votre direction des engins TP`, `démontrer que`, `montrer que`, `ce document a pour objectif de`, `nous présentons ici`, `cette présentation vise à`.

**Why it reads automated.** The customer doesn't need to be told what the document is; they're holding it. Reading the brief in the deliverable is meta and slightly cringe.

**Worked example (SUEZ deck cover-subtitle, P0 step 2):**
- Before: `Présentation à votre direction des engins TP, sur l'automatisation de la demande d'achat.`
- After: `Automatiser la composition. Tracer la commande. Prévenir le litige.` (3-imperative triad: what the deliverable does, not what the deliverable is)

**Detection regex (FR/EN).** Phrase patterns: `(présentation à|démontrer|montrer|ce document a pour objectif|nous présentons|cette présentation vise|presentation to|in this document|this document aims|we present here)`.
**Replacement strategy.** Replace with imperative-form claim about what the deliverable DOES; never describe the deliverable itself.

## 3. Eleven anti-pattern seeds (positive-claim replacements ready for validator rule pack)

These are concrete sentence-level replacements with the SUEZ engagement as the worked example. The validator rule pack on `validate_brand_voice_register.py` (deferred to I71 implementation) checks for the anti-pattern + suggests the positive-claim replacement.

| # | Anti-pattern | Family | Positive-claim replacement template |
|:---:|:---|:---:|:---|
| 1 | `Une discipline qui tient en trois lignes` | F5 | `Notre métier tient en trois lignes` (active possessive; drops "discipline" overuse) |
| 2 | `Le code suit le cadrage, pas l'inverse` | F1 | `Le cadrage précède le code` (positive assertion; same idea) |
| 3 | `Deux récits, une seule discipline` | F3+F5 | `Deux récits, une même méthode` (drops false-singularity AND "discipline") |
| 4 | `Discipline qualité-donnée` | F5 | `Cadrer la qualité avant l'entrée` (active verb; concrete frame) |
| 5 | `Discipline gouvernance multinationale` | F5 | `Tenir la règle entre filiales` (active verb; concrete object) |
| 6 | `Discipline projet vers logiciel` | F5 | `Du cadre projet au logiciel` (concrete frame; drops "discipline") |
| 7 | `C'est le réflexe qui [verb]` (3x) | F6 | Vary openings with passive-construction or noun-phrase-anchor (`Le litige se prévient à l'entrée, pas à la facturation` / `La règle protège l'opération quand l'échelle change` / `Une mission reproductible sans son auteur — voilà le test`) |
| 8 | `Une mémoire opérationnelle, pas une équipe sur étagère` | F1 | `La matière documentaire que nous tenons en interne est celle que vous récupérez` (positive claim with concrete object + register match to operational reality) |
| 9 | `Une passation totale, pas un attachement` | F1 | `La passation est totale` (drops the false-contrast; affirmative declaration) |
| 10 | `Une mécanique répétée, un litige à éviter, sur un parc qui double` | F4 | `Vingt à cinquante demandes par jour, un parc qui double` (drops abstract triplet; pulls in concrete number from data) |
| 11 | `La friction n'est pas la décision. C'est la répétition...` | F2 | `La friction réside dans la répétition...` (collapses chained-negation into single positive sentence) |

## 4. Per-language register considerations

The 7 tic families above use FR examples (from the SUEZ engagement). EN + ES require per-language register checks per `BRAND_FRENCH_PATTERNS.md` + `BRAND_SPANISH_PATTERNS.md`.

**FR-specific:**
- The `discipline` overuse is FR-specific (the word reads colder in FR than in EN).
- `n'est pas X. C'est Y.` chains are stronger AI-tic in FR than in EN (FR formal register relies less on negation-affirmation than EN does).
- Anglicism check (per `BRAND_FRENCH_PATTERNS.md` §5.1) runs alongside this discipline.

**ES-specific:**
- `una sola X` epigrams + `no es X. Es Y.` chains are equivalent ES tics.
- Tier-1 academic-formal *usted* register (per `BRAND_SPANISH_PATTERNS.md` §13) prohibits anglicisms.
- Performative-discipline tics (Spanish copywriting) are softer than FR; less aggressive in detection regex.

**EN-specific:**
- `It's not X. It's Y.` chains and `a single X` epigrams are most prevalent in EN-LLM-prose.
- Voice tier per `BRAND_REGISTER_MATRIX.md` (peer_consulting → investor_aspirational) influences which tics are acceptable; tier-2 admits more rhetorical contrastive structure.

## 5. Validator rule pack contract (deferred to I71 implementation)

The `validate_brand_voice_register.py` validator (active per I66 P5 incr 3 strict-mode promotion) gets a new **copywriting-discipline rule pack** that implements the 7 family detections + the 11 anti-pattern seed checks.

**Rule pack interface:**

- **Input:** target file path + language (`fr` / `en` / `es`).
- **Per-rule output:** `(file, line, rule_family, rule_id, original_text, suggested_replacement_template, severity)`.
- **Severity:** `error` for cover slides + customer-pack body prose; `warning` for operator-pack body prose; `info` for internal canonicals.
- **Allowlist:** explicit per-line opt-out via `<!-- copy-discipline-allow: F1 -->` HTML comment for cases where the operator deliberately uses a tic for rhetorical effect.

**Implementation deferred to I71 (CICD + AI-ops baseline maturity)** — author the rule pack as Pydantic-backed regex patterns + integration tests with SUEZ deck before-and-after as fixtures.

## 6. Operating posture

This canonical takes effect immediately for **manual review** of customer-facing prose. Operators (Founder, Brand Manager, Copywriter, future Account Manager) consult the 7 tic families + 11 anti-pattern seeds during deck/proposal/email drafting. The render pipeline today (`scripts/render_suez_engagement_pdfs.py`) does not enforce mechanically; that's I71.

Until then, the SUEZ deck (post-P0 polish) is the worked-example reference. Future engagements consult this canonical + the SUEZ before-and-after rewrites.

## 7. Cross-references

- Parent: [`BRAND_DISCIPLINE_ONTOLOGY.md`](../../canonicals/BRAND_DISCIPLINE_ONTOLOGY.md) §2 (Copywriter sub-discipline).
- Sister: `BRAND_VOICE_FOUNDATION.md`, `BRAND_REGISTER_MATRIX.md`, `BRAND_FRENCH_PATTERNS.md`, `BRAND_SPANISH_PATTERNS.md`.
- Validator (forward-link to I71): [`scripts/validate_brand_voice_register.py`](../../../../../../../scripts/validate_brand_voice_register.py) — copywriting-discipline rule pack reserved.
- Worked example: SUEZ I12 P12 + I70 P0 deck rewrites (see commit `8f479d2`).
- External research brief (Tier 3 WIP): `Marketing/Brand/Copywriter/wip/2026-impeccable-copywriting/` (forward-link).
- I70 plan section 5 — full P5 deliverable spec.
- D-IH-70-X (P2.5 audit): Storytelling-authors / Resonance-consumes boundary; Brand authors register; Storytelling integrates; Resonance deploys.
