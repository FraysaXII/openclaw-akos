---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P7
phase_name: Deck (FR, 8 slides) + objections + counterparty-brief companions
recorded_at: 2026-05-10
---

# P7 — Deck and companions self-checkpoint

## Files authored

| File | Format | Lines |
|:---|:---|---:|
| `docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/deck-suez-webuy.fr.md` | FR external register | ~120 |
| `docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/deck-suez-webuy.objections.md` | EN internal register | ~75 |
| `docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/deck-suez-webuy.counterparty-brief.md` | EN internal register | ~70 |

## Deck structure (8 slides per `sales-8-slide.deck.md` template)

| # | Slide | Content highlight |
|:---|:---|:---|
| 01 | Couverture | Faciliter votre processus de demande d'achat WeBuy |
| 02 | La contrainte opérationnelle | Parc 750 → 950 vehicles, 3 conséquences (charge / qualité / pilotage) |
| 03 | Ce que fait Holistika | Boîte de stratégie + laboratoire technologique; 4 temps Lire/Concevoir/Construire/Transférer |
| 04 | La matrice de services | Cells `1A → 1B → 5C → 6C` highlighted with FR labels |
| 05 | Le rythme d'engagement | Découvrir / Cadrer / Construire / Transférer / Clore |
| 06 | Ce que vous obtenez | 3 variants A / B / C with par-duration; price annexed |
| 07 | Pourquoi Holistika | 4 bullets: research-execution-tech as one loop, founder track-record, boutique structurée, engagement borné |
| 08 | Prochaine étape | 30-min discussion, questionnaire, variant choice, 48h proposal commitment |

## FR external register adherence (deck only)

* Vous register held throughout (no `tu`).
* Word `agent` not used in the deck — `application` for the web variant, `outil` and `prototype` for the Phase 1 prototype.
* No euros in the deck; tarification in the annexed commercial schedule.
* Counterparty referenced as `[entité juridique du donneur d'ordre]`.
* Bridge referenced as `notre partenaire de collaboration`.
* The bridge collaborator referenced as `le porteur du compte SUEZ côté Holistika` (slide 08 only).
* Triadic structure: 4 temps in slide 03, 4 cells in slide 04, 5 steps in slide 05 (deliberate cadence-respect).

## Companions (internal register OK per dual-register exemption)

* **Objections companion** — 8 anchor objections (price, lock-in, industry credibility, security, build-vs-buy, agent terminology, operator displacement, Azure environment) + operator notes + pre-meeting prep checklist.
* **Counterparty brief companion** — reading lens (5 bullets), decision criteria (5), first doubt triggers (5), prep + post-meeting checklists.

Both companions explicitly note in their preamble that they do not ship externally. The deck file references them in its frontmatter.

## Cross-document consistency

* Variants A / B / C in deck slide 06 match `proposal.fr.md` §2 and the three `scope-{a,b,c}.yaml` files exactly.
* Service cells `1A → 1B → 5C → 6C` in slide 04 match the proposal cover header.
* The FR engagement-rhythm verbs (`Découvrir / Cadrer / Construire / Transférer / Clore`) match the proposal §3 method.
* Slide 07 founder framing aligns with the proposal §7 founder bio variant (Customer-SME translated to FR).
* Counterparty brief references the four open placeholders to close at the meeting (D-ENG-SUEZ-A through -D).

## Verification

* Manual review against the deck template: 8 slides, all in correct order, all using FR external register.
* Manual review against the objections template: 4 base objections (cost, lock-in, industry, security) all present + 4 SUEZ-specific objections (build-vs-buy, agent terminology, operator displacement, Azure environment).
* Manual review against the counterparty-brief template: reading lens + decision criteria + first doubt triggers + prep checklist all present + post-meeting deliverables added per the elicitation-plan.md cadence.
* All three files carry counterparty placeholder `[entité juridique du donneur d'ordre]` (deck) or generic `the counterparty` (companions internal-register).

## Next

P8 — PDF rendering of `proposal.fr.md`, `discovery-questionnaire.fr.md`, `deck-suez-webuy.fr.md`, `cdc-feasibility-shape.fr.md` + drift-gate validators (`validate_brand_baseline_reality_drift.py`, `validate_brand_jargon.py`, `validate_brand_voice_register.py --locale fr`, `validate_hlk.py`) + manual grep for forbidden tokens.
