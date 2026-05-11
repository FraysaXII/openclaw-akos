---
status: draft
classification: working
access_level: 5
language: en
register: internal
artifact_kind: elicitation_plan
counterparty_org_ref: GOI-CUS-SUEZ-2026
counterparty_lead_ref: POI-CUS-SUEZ-LEAD-2026
governance: SOP-IO_ELICITATION_DISCIPLINE_001
recorded_at: 2026-05-10
---

# Elicitation plan — `GOI-CUS-SUEZ-2026` / WeBuy CDC review

> Internal working plan. Internal-register vocabulary is permitted here. Section A–E questions below are written **in French** (the language of the meeting); surrounding commentary is English. The FR external-register version of the questions ships at `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/01-operator-pack/discovery-questionnaire.fr.md` (P5; relocated to the canonical client-engagement home in P12.3).

## Frame for the meeting

* **Slot**: Monday 2026-05-11 with `POI-CUS-SUEZ-LEAD-2026`.
* **Bridge**: `POI-PRT-EFA-LEAD-2026` introduces; we anchor in their CDC and the WeBuy mode opératoire.
* **Tone**: peer-consulting + formal_legal hybrid (enterprise context; first contact). Tutoiement off; vouvoiement on.
* **Structure**: 12 questions across 5 sections. We move them in order but treat them as cards — a question can be skipped or returned to depending on what the counterparty offers spontaneously.
* **Not a script** — the 12 questions are an internal map. The outward question deck is the FR discovery questionnaire (P5), trimmed to the most useful subset.

## Section A — Frame-setting (acknowledge their work)

1. Nous avons lu votre cahier des charges (version 1.0 d'avril 2026) et le mode opératoire WeBuy. Avant d'aller plus loin, pouvez-vous confirmer ce qui a déclenché la rédaction du CDC à ce moment précis : un seuil de litiges franchi, une contrainte DSI, une mutation d'équipe ?
2. Sur les six derniers mois, qu'est-ce qui a changé dans la manière dont vous percevez ce processus de passage de commande — au-delà de la perte de temps que le CDC documente déjà ?

## Section B — Direct elicitation (operational reality)

3. Pouvez-vous nous décrire une journée typique d'un gestionnaire de commandes : à quelle étape se concentre la perte de temps réelle, et à quelle étape se concentre le risque d'erreur générant un litige ?
4. Le numéro de bon de commande (PO) est central dans le CDC. Pouvez-vous nous donner un ordre de grandeur du taux actuel de factures sans PO et du délai moyen de régularisation, même approximatif ?
5. La règle de nommage à cinq composantes (initiales, n° parc, code intervention, fournisseur, n° devis) — comment a-t-elle été construite, et qu'est-ce qui rend son application difficile aujourd'hui ?
6. Le fichier Excel de référence du parc engins : qui le tient à jour, à quelle fréquence, et quelles sources alimentent ses mises à jour ?

## Section C — Indirect elicitation (DSI + peer anchoring)

7. Comment se passe la coordination avec la DSI lorsque vous proposez un nouvel outil interne : quels sont les jalons de validation typiques, et quels sont les sujets sur lesquels la DSI a tendance à pousser le plus loin (hébergement, RGPD, audit, intégrations) ?
8. Avez-vous connaissance, chez SUEZ ou dans des entités voisines, de tentatives passées d'automatisation de la saisie WeBuy — y compris celles qui n'ont pas abouti ? Qu'est-ce qui a fait la différence ?

## Section D — Reverse-elicitation (push-back invited)

9. Lecture du CDC : où trouvez-vous que nous (lecteurs externes) risquons de mal interpréter le périmètre — par exemple en sous-estimant une catégorie comme les pneus ou une particularité comme la gestion des vérifications périodiques (VGP) ?
10. Le CDC propose trois options technologiques (Excel/VBA, application web légère, RPA). Quelles sont les options que vous avez écartées avant l'écriture du CDC, et pour quelles raisons ?
11. Si nous proposions une trajectoire en trois phases (Phase 1 outil pré-rempli sous 4 semaines, Phase 2 application web sous 2 mois, Phase 3 étude de faisabilité d'intégration sous 2 mois supplémentaires), qu'est-ce qui vous ferait dire « non » dès la phase 1 ?

## Section E — Closing (commitments + cadence)

12. Pour passer d'une discussion à une proposition signée, qu'est-ce que nous devrions démontrer ou nous engager à faire en amont — et qui sont les autres voix internes à embarquer dans la décision (DSI, ServDel, contrôle de gestion) ?

## Reading rules (operator notes)

* **Q4 (PO numbers)** is the most informationally dense question — even a rough percentage anchors the entire commercial discussion. If the answer is "I don't know exactly", we propose the discovery questionnaire as a 1-week ramp-up.
* **Q7 (DSI posture)** is the single highest-leverage question for proposal viability. If DSI has a hard-on-prem rule, we re-shape the proposal toward an Excel/Power Query Phase 1 plus a SUEZ-internal-cloud Phase 2.
* **Q11 (push-back on the trajectory)** is where reverse-elicitation pays off. Whatever the counterparty pushes back on becomes the explicit "out of scope" line in the proposal.
* Q12 closes with a question about *who else needs to be in the room*. We never propose without knowing the full decision graph.

## Post-call deliverables

* Update `counterparty-brief.md` §1 (baseline reality) and §4 (placeholders) with the answers.
* Re-grade sources `S5`–`S9` in `source-grade.csv` based on the call's reliability and credibility cues.
* Write the FR external-register discovery questionnaire (`P5`) and proposal (`P6`) on the basis of the post-call updated brief.

## Cross-references

* `counterparty-brief.md` (this folder).
* `source-grade.csv` (this folder).
* `BRAND_FRENCH_PATTERNS.md` — voice rules for the FR external-register version of this plan (`P5`).
* `SOP-IO_ELICITATION_DISCIPLINE_001` — methodology canon.
