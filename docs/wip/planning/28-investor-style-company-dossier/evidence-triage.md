# Evidence triage — what goes in the deck vs the appendix vs the bin

**Document owner**: Brand Manager + Founder
**Version**: 0.1 (P0 of Initiative 28)
**Date**: 2026-04-30

---

## 1. Method

Every block of content in the existing `dossier_es.md` (which becomes the **adviser evidence appendix**) was reviewed against three filters:

- **Does it sell the company?** → **Main deck** (slide candidate).
- **Does it provide structured evidence the adviser/certifier may ask for?** → **Appendix** (already written).
- **Is it process detail for the founder/team only?** → **Discard** for the external send.

This file is the audit log of that triage.

## 2. Triage table

| # | Source block (in current `dossier_es.md`) | Bucket | Slide / appendix anchor | Reason |
|:---|:---|:---|:---|:---|
| 1 | Resumen ejecutivo (lead paragraph) | Deck | Slides 1, 4, 5 (split) | This is exactly the company-dossier framing we need; redistributed across cover, solution and what-we-do slides |
| 2 | Stat grid (5 entregas / 3 idiomas / 2023 / 12 preguntas) | Deck (partial) | Slide 6 | Drop "12 preguntas abiertas a cerrar" — that's a workbench artefact, not a company-dossier stat. Replace with a stat that sells: e.g. "≥ 4 años operando el método" or "5 entregas con la misma pila técnica" |
| 3 | "En una línea para la persona certificadora" callout | Deck | Slide 4 (insight) | Keep the spirit ("método propio + software de producción + queremos cerrar el objeto social/CNAE") but split: the company part lands in slide 4; the certification ask lands in slide 14 |
| 4 | Pilar I §"Estructura societaria" | Appendix only | Existing `dossier_es.md` Pilar I (unchanged) | Important for the adviser; not for the dossier reader |
| 5 | Pilar I §"Objeto social y CNAE" — recommendation | Appendix only | Existing `dossier_es.md` Pilar I §2.2 (unchanged) | Founder/adviser conversation; not deck content |
| 6 | Pilar I §"Objeto social y CNAE" — `TODO[OPERATOR]` callout | Appendix only (with friendly framing) | Existing dossier already renders as "Pregunta abierta" via the I27 transform | Stays where it is |
| 7 | Pilar I §"Ruta de constitución" (CIRCE vs notary) | Appendix only | Existing dossier Pilar I §2.3 | Adviser conversation; not deck |
| 8 | Pilar I §"Capital social inicial" | Appendix only | Existing dossier Pilar I §2.4 | Adviser conversation |
| 9 | Pilar I §"Gobierno y administración" | Appendix only | Existing dossier Pilar I §2.5 | Adviser conversation |
| 10 | Pilar II §"Tesis de innovación" — bullet list | Deck (rewritten) | Slide 4 (insight) + Slide 5 (what we do) | Strong content. Rewrite as one sharp claim per slide rather than a bullet dump |
| 11 | Pilar II §"Posición en mercado" — ICP bullets | Deck | Slide 9 (market + ICP) | Lift the three ICP bullets directly; turn into three vertical cards |
| 12 | Pilar II §"Análisis del entorno (PESTEL)" | Discard from deck; keep in appendix | Existing dossier Pilar II §3.3 | PESTEL is form-filling; investor-style deck doesn't need it; the certifier expects it in the appendix |
| 13 | Pilar II §"Por qué España y la Unión Europea" | Deck (compact) | Slide 13 (ENISA fit) | One paragraph max; the appendix carries the structured detail |
| 14 | Pilar III §"Modelo de capitalización" | Appendix only | Existing dossier Pilar III §4.1 | Operational; not for the deck |
| 15 | Pilar III §"Uso de fondos" | Deck (transformed) | Slide 13 (use of funds) | Replace cost-bucket detail with a 3-line "where the money goes" framing |
| 16 | Pilar III §"Tratamiento de aportaciones del fundador" | Appendix only | Existing dossier Pilar III §4.3 | Tax / accounting; not for the deck |
| 17 | Pilar III §"Vínculo con ayudas ENISA" | Deck (one line) | Slide 13 | Compress to "ENISA es opción de extensión, no requisito" or similar |
| 18 | Pilar IV §"Modelo de entrega" — three-line "Hoy / Mañana / El puente" | Deck | Slide 10 (business model) | Strong; lift directly. This is the heart of the service-to-product story |
| 19 | Pilar IV §"Pila tecnológica" — bullet list | Deck (compact) | Slide 11 (moat) | Compress to 4 short lines; do not reproduce the bullet list verbatim |
| 20 | Pilar IV §"Gobernanza del conocimiento" | Discard from deck; keep in appendix | Existing dossier Pilar IV §5.3 | Process discipline; reader doesn't buy this directly |
| 21 | Pilar IV §"Plan de personal en España" cross-ref | Deck (compact) | Slide 13 | One line in the ENISA / use-of-funds slide |
| 22 | Apéndice A — Q-tracker (12 questions) | Appendix only | Existing dossier Apéndice A (unchanged) | This is exactly the appendix's job |
| 23 | Apéndice B — Instrumentos archivados | Appendix only | Existing dossier Apéndice B | Same |
| 24 | Apéndice C — 5 capability cards | Deck (rewritten visual) | Slide 6 (proof, 5 cards) + Slide 7 (KiRBe spotlight) | Lift the substance; rewrite as deck-grade cards (2 lines max per card on the slide); the long card text stays in the appendix |
| 25 | Apéndice D — Glosario | Discard from deck | Existing dossier Apéndice D | Not needed for any deck reader |
| 26 | Apéndice E — Trazabilidad y procedencia | Discard from deck | Existing dossier Apéndice E | Internal traceability metadata |

## 3. Net result

| Bucket | Block count |
|:---|:---|
| Lifted to the deck (rewritten / compressed / split) | 11 |
| Appendix only (unchanged) | 13 |
| Discarded for the external send | 2 |

The deck is built **net new** at slide level — copy is rewritten, not pasted — but every claim has a traceable source row in this triage table.

## 4. Capability disclosure rules (from operator confirmation)

- "Full disclosure" is honoured: all five capability cards remain in the deck.
- Partner names (Websitz, Rushly) appear **once**, in the proof captions, in small text. The lever in the narrative is *what we did and how we worked*, not *who we worked with*.
- The Holística public domain (`holistikaresearch.com`) is allowed to appear in the cover and in the website-card footer.
- KiRBe is named everywhere — it is our own product.
- "HLK ERP" is named as our internal ERP; product name is fine, no codenames.
- The capability card numbers stay 1-5; the slide-6 layout shows all 5 simultaneously, then slide 7 spotlights KiRBe.

## 5. Stat-grid revision

The current dossier opens with this set:

| # | Stat (current) | Bucket |
|:---|:---|:---|
| 1 | 5 — Entregas en producción | Keep |
| 2 | 3 — Idiomas en el sitio público | Keep |
| 3 | 2023 — Año de inicio del método | Keep |
| 4 | 12 — Preguntas abiertas a cerrar | **Drop** (workbench leak) |

Replacement candidate (pick one for slide 6):

- "≥ 4 — Años operando el método internamente" (anchors continuity from 2023 → today)
- "1 — Pila técnica replicada en 5 entregas" (anchors method consistency)
- "5 — Disciplinas (web, ERP, SaaS, app de partner, scaffold)" (anchors execution breadth)

Decision: use **"5 — Disciplinas distintas resueltas con la misma pila"** as the fourth stat. It tells the reader the same engineering team and the same playbook produced very different products, which is the moat.

## 6. Open decisions for the founder before P1

These are real founder decisions that affect deck copy, not appendix content:

| ID | Question | Recommendation | Where it shows up |
|:---|:---|:---|:---|
| D-IH-28-DECK-1 | What public URL appears on the cover and in the website card? | `holistikaresearch.com` | Cover, slide 6 card 1 footer |
| D-IH-28-DECK-2 | Do we name partner Websitz / Rushly explicitly on slide 6, or only as "partner B2B" / "partner SaaS"? | Mention by name, low-key, in the card footer only ("Entrega para Websitz" / "Diseño para Rushly"); never on slide 1 / 4 / 11 | Slide 6 cards 4–5 |
| D-IH-28-DECK-3 | Do we put the founder's name on the cover or only "Holística Research"? | Holística Research; founder name appears on slide 14 (Ask) signature only | Cover + slide 14 |
| D-IH-28-DECK-4 | What's the single-sentence positioning at the top of the deck? | "Sistemas operativos para empresas que ordenan su operación antes de escalar" | Slide 1 (cover subtitle) |

These are low-risk decisions and the deck can ship with the recommended values; the founder confirms them before the actual external send (not before the build).

## 7. Cross-references

- [`master-roadmap.md`](master-roadmap.md)
- [`deck-brief.md`](deck-brief.md)
- Source dossier (now appendix role): [`dossier_es.md`](../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md)
