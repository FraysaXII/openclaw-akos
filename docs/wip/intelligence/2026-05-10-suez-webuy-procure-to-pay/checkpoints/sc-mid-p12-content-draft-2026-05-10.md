---
artifact_kind: voice_gate_content_drafts
audience: internal
register: internal
classification: working
language: fr
phase: P12.1
date: 2026-05-10
status: awaiting_voice_gate_p12_4
purpose: Verbatim content drafts staged for line-by-line operator approval at P12.4 voice gate. NO COMMITS to canonical surfaces in this phase.
governance:
  - voice-corpus.md (P12.0 cadence comparator)
  - efa-redacted.md (P12.0 source intelligence)
  - BRAND_VOICE_FOUNDATION.md
  - BRAND_DO_DONT.md
  - BRAND_FRENCH_PATTERNS.md
  - BRAND_REGISTER_MATRIX.md
  - BRAND_JARGON_AUDIT.md
linked_decisions:
  - D-12-2 (network claim retired)
  - D-12-3 (slide 04 deux récits une seule discipline)
  - D-12-4 (continuité §3 two postures)
  - D-12-5 (co-branding host-card)
  - D-12-8 (slide architecture, count 13)
  - D-12-13 (volume range with FTE anchor; fallback rule)
  - D-12-14 (EFA-since-Oct-2025)
  - D-12-15 (litige reframe spine)
  - D-12-16 (triadic pull-quote)
  - D-12-17 (external-prose discretion)
---

# P12.1 content drafts — verbatim prose for the voice gate

> Internal staging of every verbatim sentence the customer-pack will gain at P12.5. Operator reviews each block at P12.4 before any commit. Where the plan permits a fallback (D-12-13 conservative `~20`), both versions appear here side-by-side and the gate picks one. Where D-12-17 forbids citation patterns, the prose is written without article numbers, `Besoin N`, or *"comme spécifié dans votre cahier des charges"* constructions. Every block carries an in-line voice-test note for the gate.

## Reading guide for the operator at the voice gate

Each block below has four parts:

1. **Where it lands.** File + section anchor where the prose will be inserted at P12.5.
2. **The verbatim French.** Exactly what gets written to the markdown file.
3. **Voice-test note.** A short line stating which voice-corpus pattern this prose draws on (per `voice-corpus.md` §6 five-test matrix).
4. **Approval line.** A single-sentence approval slot the operator marks `OK / REWRITE / REJECT` at the gate. Leave blank in this draft; populated at P12.4.

If a block fails the voice gate, the operator marks REWRITE with a one-line redirection (e.g. *"shorter, drop the lead-in clause"*) and the agent emits a v2 in the same checkpoint file.

## Index of blocks

| # | Surface | Block | Decision link |
|:---|:---|:---|:---|
| 1a-01 | `proposal.customer.fr.md` lead | Volume framing — option C (range default) | D-12-13 |
| 1a-02 | `proposal.customer.fr.md` lead | Volume framing — option B (fallback `~20`) | D-12-13 |
| 1a-03 | `proposal.customer.fr.md` stat-grid | Stat tiles for each option | D-12-13 |
| 1b-01 | `proposal.customer.fr.md` §2 | New signal — *Le coût caché : les litiges* | D-12-15 |
| 1b-02 | `proposal.customer.fr.md` §2 | Revised signal — *Compétence interne préservée* (kept, second slot) | D-12-15 |
| 1b-03 | `proposal.customer.fr.md` after §2 | Triadic pull-quote | D-12-16 |
| 1b-04 | `proposal.customer.fr.md` §3 | Section header revision (4→5 fonctionnalités) | D-12-15 |
| 1b-05 | `proposal.customer.fr.md` §3 | New 5th feature card — module litige | D-12-15, D-12-17 |
| 1b-06 | `proposal.customer.fr.md` §7 | Three new commitment KPIs | D-12-15, D-12-17 |
| 1b-07 | `cdc-feasibility-shape.fr.md` §11 | New section — lecture du module de prévention et gestion des litiges | D-12-15, D-12-17 |
| 1b-08 | `discovery-questionnaire.fr.md` §B2-bis | Probe — volume of open litiges + resolution cycle | D-12-17 |
| 1b-09 | `discovery-questionnaire.fr.md` §B2-ter | Probe — litige dashboard integration | D-12-17 |
| 1c-01 | `proposal.customer.fr.md` metadata | Mission portée conjointement + EFA-since-Oct-2025 | D-12-5, D-12-14 |
| 1c-02 | `FOUNDER_TRAJECTORY_INTERNAL.md` | EFA-since-Oct-2025 already correct (verified) | D-12-14 |
| S2 | `deck.customer.fr.md` slide 02 | EFA host-card | D-12-5, D-12-8 |
| S3 | `deck.customer.fr.md` slide 03 | Holistika in three lines (no network claim) | D-12-2, D-12-8 |
| S4 | `deck.customer.fr.md` slide 04 | Deux récits, une seule discipline | D-12-3, D-12-8 |
| S5 | `deck.customer.fr.md` slide 05 | How we work today (KM + AKOS-MADEIRA) | D-12-8 |
| S2-stat | `deck.customer.fr.md` (renumbered) slide 06 | Stat-grid update for new volume + litige tile | D-12-13, D-12-15 |
| S3-cell | `deck.customer.fr.md` (renumbered) slide 07 cell 04 | Replace *Compétence préservée* with *Le coût caché* | D-12-15 |
| S5-card | `deck.customer.fr.md` (renumbered) slide 09 | New 5th feature card — module litige | D-12-15, D-12-17 |
| S8-cells | `deck.customer.fr.md` (renumbered) slide 12 | KPIs phrased as commitments | D-12-15, D-12-17 |
| C3 | `proposal.customer.fr.md` §3 | Continuité opérationnelle | D-12-4 |
| CSM | all customer-pack metadata | Cover-strip 4-field — `EN COLLABORATION AVEC EFA ACADÉMIE` | D-12-5 |

End of index. Block content begins below.

---

## P12.1a — Volume framing (D-12-13)

### Block 1a-01 — Volume lead, option C (range default; recommended)

**Where it lands.** `proposal.customer.fr.md` line 16 (the `<p class="lead">…</p>` tag), replacing the current *"Vos équipes traitent une vingtaine de demandes d'achat WeBuy par mois sur un parc qui doublera d'ici juin."*

**Verbatim FR.**

> Vos équipes traitent entre vingt et une cinquantaine de demandes WeBuy par jour, selon la cadence du parc. La friction n'est pas la durée de saisie. C'est la facture qui arrive sans numéro de commande, le frais de transport ajouté hors devis, le rapprochement qui ne tient pas, et la chaîne de relances qui en découle. Nous proposons une mécanique qui prévient ces ruptures à la source : cadrer la règle, prototyper l'outil, transférer la maîtrise.

**Voice-test note.** Triadic close (*cadrer · prototyper · transférer*) ✓ ; concrete-noun-anchored (facture, frais de transport, rapprochement, relances) ✓ ; you-then-we frame (*Vos équipes...* before *Nous proposons...*) ✓ ; D-12-17 clean (no CDC citation, no `Besoin N`, no *"comme spécifié dans votre cahier des charges"*) ✓ ; aphoristic close (*"cadrer la règle, prototyper l'outil, transférer la maîtrise"*) ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — operator marks at P12.4.

### Block 1a-02 — Volume lead, option B fallback (~20 conservative)

**Where it lands.** Same anchor as 1a-01 *if* operator judges 1a-01 awkward at the voice gate.

**Verbatim FR.**

> Vos équipes traitent une vingtaine de demandes WeBuy par jour, et jusqu'à une cinquantaine sur les jours hauts. La friction n'est pas la durée de saisie. C'est la facture qui arrive sans numéro de commande, le frais de transport ajouté hors devis, le rapprochement qui ne tient pas, et la chaîne de relances qui en découle. Nous proposons une mécanique qui prévient ces ruptures à la source : cadrer la règle, prototyper l'outil, transférer la maîtrise.

**Voice-test note.** Same shape as 1a-01; *"jusqu'à une cinquantaine sur les jours hauts"* removes the *"selon la cadence du parc"* hedge that the operator may judge wordy. The discovery questionnaire B2-bis (block 1b-08) carries the range probe in this fallback path.

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1a-03 — Stat-grid (three tiles)

**Where it lands.** `proposal.customer.fr.md` lines 18-22 (`<div class="stat-grid">…</div>`), replacing the current three tiles (`~20`, `× 2`, `23`).

**Verbatim FR — option C (default, paired with 1a-01).**

```html
<div class="stat-grid">
  <div class="stat"><span class="stat-num">20 ↔ 50</span><span class="stat-label">Demandes par jour, selon cadence du parc</span></div>
  <div class="stat"><span class="stat-num">~1 ETP</span><span class="stat-label">Mécanique consommée aujourd'hui</span></div>
  <div class="stat"><span class="stat-num">~2 ETP</span><span class="stat-label">À mise en service du parc complet</span></div>
</div>
```

**Verbatim FR — option B (fallback, paired with 1a-02).**

```html
<div class="stat-grid">
  <div class="stat"><span class="stat-num">~20</span><span class="stat-label">Demandes par jour</span></div>
  <div class="stat"><span class="stat-num">~1 ETP</span><span class="stat-label">Mécanique consommée aujourd'hui</span></div>
  <div class="stat"><span class="stat-num">~2 ETP</span><span class="stat-label">À mise en service du parc complet</span></div>
</div>
```

**Voice-test note.** ETP-equivalent anchor stays in both options (the value-prop survives the range vs conservative choice). The `× 2` tile and the `23 champs` tile both retire from the customer-pack lead — the doubling stays in section 2 prose, and `23 champs` moves to slide 06 (renumbered) only.

**Approval.** `[ OK / REWRITE / REJECT ]` — operator picks A=option-C or B=option-B. The two options ride together; the gate's choice cascades to slide 06 (renumbered) stat-tile and to the Continuité §3 prose.

---

## P12.1b — Litige reframe (D-12-15, D-12-17)

### Block 1b-01 — New signal *Le coût caché : les litiges* (replaces signal #4)

**Where it lands.** `proposal.customer.fr.md` line 33, replacing the current bullet *"**Compétence interne préservée.** La personne qui opère garde le jugement..."*. The competence-preserved bullet moves to a new position (block 1b-02).

**Verbatim FR.**

> - **Le coût caché : les litiges.** Une facture sans numéro de commande, un frais de transport ajouté hors devis : la chaîne de relances qui en découle pèse plus que la saisie initiale, et bloque le règlement fournisseur le temps de la régularisation. C'est l'enjeu qui mérite la priorité, et c'est celui que nous inscrivons au cœur de la solution.

**Voice-test note.** Triadic surface (*facture sans numéro de commande, frais de transport ajouté, chaîne de relances*) ✓ ; concrete-noun-anchored ✓ ; aphoristic close (*"c'est celui que nous inscrivons au cœur de la solution"*) ✓ ; D-12-17 clean — no *"votre cahier des charges en fait l'enjeu principal"* construction; the priority signal is operator-voiced (*"l'enjeu qui mérite la priorité"*) without sourcing from the CDC ✓ ; the financial layer (*"bloque le règlement fournisseur"*) lands without the audit-framing register (no *"trésorerie immobilisée"* yet — that lands in the feature card 1b-05) ✓.

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1b-02 — Signal *Compétence interne préservée* (kept, repositioned as #5)

**Where it lands.** `proposal.customer.fr.md` line 34 (a new bullet appended after 1b-01).

**Verbatim FR.**

> - **Compétence interne préservée.** La personne qui opère garde le jugement sur ce qui demande du discernement : relations fournisseurs, négociation, traitement des anomalies. L'application logicielle traite la mécanique et prévient les ruptures à la source.

**Voice-test note.** Existing operator-approved cadence; the addition is *"négociation"* (third triadic term in the *"relations fournisseurs · suivi des litiges · traitement des anomalies"* trio that the litige-reframe makes redundant) and *"prévient les ruptures à la source"* (paraphrase of the new signal). D-12-17 clean ✓.

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1b-03 — Triadic pull-quote (D-12-16)

**Where it lands.** `proposal.customer.fr.md` line 35, replacing the current binary aphorism *"Automatiser ce qui se calcule, préserver ce qui se juge."*

**Verbatim FR.**

> > Automatiser ce qui se calcule, prévenir ce qui se rompt, préserver ce qui se juge.{: .pull-quote }

**Voice-test note.** Three balanced verbal clauses, each 5-6 syllables in FR; the middle clause carries the litige-prevention spine without naming "litige" (verbal-rhythm working at the prosodic level). This is the canonical operator-voice aphorism for this engagement (per voice-corpus §1.6 aphoristic-close pattern).

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks whether the deck slide 01 cover keeps the binary version (existing `deck.customer.fr.md` does NOT yet carry an aphorism on slide 01; new aphorism may land directly on slide 13 closing or on slide 06 method).

### Block 1b-04 — Section header revision (4→5)

**Where it lands.** `proposal.customer.fr.md` line 57, the H2 header *"Quatre fonctionnalités, parmi les vingt-quatre identifiées"*.

**Verbatim FR.**

> ## Cinq fonctionnalités, parmi les vingt-quatre identifiées

**Voice-test note.** Mechanical change. The "5/24" wording stays operator-natural per voice-corpus §1.1 (triadic/quadriadic enumerations are the natural rhythm; "5 of 24" reads as a working-extract from a larger inventory, not as an exhaustive list).

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1b-05 — New 5th feature card *Module de prévention et gestion des litiges*

**Where it lands.** `proposal.customer.fr.md` after line 62 (the existing *"Tableau de bord d'usage"* bullet), appended as the 5th bullet in the same list.

**Verbatim FR.**

> - **Module de prévention et gestion des litiges.** Chaque demande porte son numéro de commande, transmis au fournisseur et conservé dans un registre central. À réception d'une facture, le rapprochement automatique au registre identifie immédiatement les écarts — numéro absent, montant divergent, fournisseur inconnu. Un tableau de bord montre la charge en cours, l'ancienneté par bucket (J, J+7, J+30, au-delà), et les fournisseurs récurrents, pour un pilotage hebdomadaire de la trésorerie immobilisée.

**Voice-test note.** Triadic enumeration (*numéro absent, montant divergent, fournisseur inconnu*) ✓ ; concrete-noun-anchored (registre, tableau de bord, ancienneté par bucket) ✓ ; quadriadic bucket nomenclature (*J, J+7, J+30, au-delà*) — operator pattern ✓ ; aphoristic close (*"un pilotage hebdomadaire de la trésorerie immobilisée"*) ✓ ; D-12-17 clean — no CDC citation; the *"trésorerie immobilisée"* phrasing reads as our financial-discipline framing, not as a CDC quote ✓.

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1b-06 — Three commitment KPIs

**Where it lands.** `proposal.customer.fr.md` §7 *Critères de réussite*, after the existing four bullets (lines 106-109). These three new bullets append at the end.

**Verbatim FR.**

> - **Taux de factures en litige (sans numéro de commande).** Cible : moins de 2 %, mesure mensuelle. C'est l'engagement que la solution porte.
> - **Délai moyen de résolution d'un litige.** Cible : moins de cinq jours ouvrés, mesure mensuelle. C'est l'engagement que la solution porte.
> - **Couverture du registre des bons de commande.** Cible : cent pour cent des demandes tracées, mesure hebdomadaire. C'est l'engagement que la solution porte.

**Voice-test note.** Three numbered commitments, each closed with the same incantation *"C'est l'engagement que la solution porte"* — repetition signals discipline (per voice-corpus §1.1 quadriadic enumerations and §1.6 aphoristic close). D-12-17 clean — phrased as commitments we make, not as targets we read out of the CDC. The repetition reads as ceremonial emphasis, not as boilerplate; if the gate finds it heavy, fallback drops the third occurrence and keeps the first two.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks whether to keep the repetition on all three bullets, or only on the first two.

### Block 1b-07 — `cdc-feasibility-shape.fr.md` §11 *Lecture du module de prévention et gestion des litiges*

**Where it lands.** `cdc-feasibility-shape.fr.md` after line 325 (after §10 *Documents associés*, before the closing `---` and footer paragraph).

**Verbatim FR.**

```markdown
## 11. Lecture du module de prévention et gestion des litiges

Votre lecture du processus place la prévention des litiges au cœur de la chaîne de valeur. Notre lecture rejoint la vôtre : c'est l'étape où la mécanique procédurale et la mécanique financière convergent — un numéro de bon de commande absent ou divergent immobilise la trésorerie le temps de la régularisation, et fait peser sur la personne qui opère une charge de relance qui dépasse celle de la saisie initiale.

Cinq fonctionnalités complètent les vingt-quatre identifiées au §6 et couvrent la prévention en substance, sans rien retirer à votre exigence de prévention :

- **F-25 — Registre central des bons de commande.** À chaque émission de demande, le numéro de commande est enregistré côté Holistika dans un registre interne, avec son rattachement au fournisseur, à la catégorie, et à l'engin. La traçabilité est intégrale et accessible en lecture sans intervention manuelle.
  *Drapeau.* `actionnable`.

- **F-26 — Rapprochement automatique facture / registre.** À réception d'une facture (manuelle ou par lecture d'un courriel structuré), le rapprochement au registre identifie en quelques secondes la concordance, l'écart de montant, l'absence de numéro de commande, ou la non-correspondance fournisseur. Le verdict est émis sans relecture humaine.
  *Drapeau.* `actionnable`.

- **F-27 — Alertes litige typées.** Trois alertes structurées : facture sans numéro de commande, écart de montant supérieur au seuil convenu, fournisseur inconnu du registre. Chaque alerte ouvre une fiche litige avec son tag, son ancienneté, et le contexte minimum nécessaire à la résolution.
  *Drapeau.* `actionnable`.

- **F-28 — Tableau de bord 4-buckets.** Lecture hebdomadaire de la charge en cours, ventilée par ancienneté (J, J+7, J+30, au-delà) et par fournisseur récurrent. Le tableau de bord est lisible sans intervention manuelle, à partir du moment où il est mis en service.
  *Drapeau.* `actionnable`.

- **F-29 — Modèle d'e-mail de régularisation.** Un modèle pré-constitué pour la relance fournisseur, paramétrable par catégorie de litige. Le contenu de la relance s'aligne avec votre exigence de prévention sur la documentation fournisseur. La pièce jointe (le bon de commande absent) est attachée par construction.
  *Drapeau.* `actionnable`.

Le pilotage de l'ensemble repose sur trois indicateurs cohérents avec votre cadre de mesure : taux de factures en litige (sans numéro de commande), délai moyen de résolution, et couverture du registre des bons de commande. Ces trois indicateurs sont des engagements que la solution porte, mesurés sur la cadence mensuelle pour les deux premiers et hebdomadaire pour le troisième.

> Automatiser ce qui se calcule, prévenir ce qui se rompt, préserver ce qui se juge.

Le module de prévention et gestion des litiges est le segment où la triade s'applique au plus près de la trésorerie : la mécanique du rapprochement est entièrement déterministe ; la prévention de la rupture est ce que la solution porte ; et le jugement humain reste la signature finale sur chaque fiche litige avant clôture.
```

**Voice-test note.** Triadic surface throughout (three alertes typées, three KPIs, four buckets, five fonctionnalités) ✓ ; concrete-noun-anchored (registre, fiche litige, modèle d'e-mail, J/J+7/J+30) ✓ ; D-12-17 clean — *"votre lecture du processus"*, *"votre exigence de prévention"*, *"votre cadre de mesure"* are the three anchors that replace any CDC citation; never *"Besoin 5"*, never *"comme spécifié à l'article X"*, never CDC paragraph numbers ✓ ; the F-25..F-29 internal feature-anchors are referenced because `cdc-feasibility-shape.fr.md` is by genre our feature-mapping document, but no CDC section number bleeds through ✓ ; closes on the triadic pull-quote ✓.

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1b-08 — `discovery-questionnaire.fr.md` §B2-bis (volume of open litiges + resolution cycle)

**Where it lands.** `discovery-questionnaire.fr.md` after line 67 (after the existing B2 *Lecture attendue* paragraph), inserted as a new sub-question.

**Verbatim FR.**

```markdown
### B2-bis — Le stock de litiges ouverts

**Combien de litiges sont aujourd'hui ouverts en moyenne sur le parc, et quel est le délai moyen de résolution de bout en bout, entre l'émission d'une facture problématique et son règlement effectif ?**

*Lecture attendue —* la distinction entre « charge ponctuelle » (un litige qui surgit) et « stock cumulé » (le nombre de fiches ouvertes à un instant t) éclaire la nature de la charge sur la personne qui opère. Une fourchette ou un ordre de grandeur nous suffisent ; un « nous n'avons pas encore le chiffre, mais voici notre lecture qualitative » est une réponse également utile à ce stade.
```

**Voice-test note.** Direct probe phrased without CDC reference; *"de bout en bout"* and *"entre l'émission d'une facture problématique et son règlement effectif"* are the operator-natural cadence (concrete-noun-anchored, you-frame). D-12-17 clean — no Besoin 5 reference, no article numbering. The *Lecture attendue* paragraph echoes the questionnaire's existing register.

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1b-09 — `discovery-questionnaire.fr.md` §B2-ter (litige dashboard integration)

**Where it lands.** `discovery-questionnaire.fr.md` after the new B2-bis block, as a sibling probe.

**Verbatim FR.**

```markdown
### B2-ter — Le suivi des litiges aujourd'hui

**Disposez-vous aujourd'hui d'un tableau de bord du suivi des litiges, ou bien le suivi se fait-il dans un classeur opérationnel à part, ou encore dans la mémoire de la personne qui opère ?**

*Lecture attendue —* nous cherchons à savoir si l'outil cible doit s'intégrer à un tableau de bord existant, en construire un de novo, ou se loger d'abord à côté du suivi actuel le temps que la confiance se construise. Les trois postures sont valides et orientent différemment le module de prévention et gestion des litiges.
```

**Voice-test note.** Three-option probe (*tableau de bord du suivi des litiges, classeur opérationnel à part, mémoire de la personne qui opère*) ✓ ; you-frame ✓ ; D-12-17 clean — *"le tableau de bord du suivi des litiges"* is the natural noun phrase, no CDC article reference ✓.

**Approval.** `[ OK / REWRITE / REJECT ]`

---

## P12.1c — EFA-since-October-2025 corrections (D-12-14)

### Block 1c-01 — `proposal.customer.fr.md` metadata frontmatter additions

**Where it lands.** `proposal.customer.fr.md` frontmatter block (lines 1-14), inserting two new keys before `last_review`.

**Verbatim YAML diff.**

```yaml
+ collaboration_partner: EFA Académie
+ collaboration_since: 2025-10
+ mission_posture: Mission portée conjointement
```

**Voice-test note.** YAML metadata; the surface text *"Mission portée conjointement"* appears in the cover-strip (per D-12-5 and block CSM below) and may appear once in the proposal §1 metadata table if the operator opts to surface it. Otherwise these keys are render-only; they feed `_build_cover_html` and the EFA logo URI substitution.

**Approval.** `[ OK / REWRITE / REJECT ]`

### Block 1c-02 — `FOUNDER_TRAJECTORY_INTERNAL.md` audit confirmation

**Where it lands.** Already correct in the P12.0 draft (the file does not assert an EFA-collaboration date directly; the date appears only in `efa-redacted.md` §2 where it is documented as October-2025). Audit pass: no further edit required at the gate.

**Approval.** `[ OK confirming the audit ]` — operator marks at P12.4. The internal trajectory file final at P12.9 will carry the date if the operator opts to surface it under §6 advisor-network framing.

---

## Slide blocks — `deck.customer.fr.md` four new intro slides + amendments to renumbered slides

The deck moves from 9 slides to 13 (`slide_count: 13`). The cover stays at 01. Four new intro slides land at 02-05. Existing slides 02-09 renumber to 06-13. The amendments below cover the new slides AND the cells that change in the renumbered slides (volume, litige reframing, KPI commitments).

### Block S2 — Slide 02 EFA host-card (D-12-5)

**Where it lands.** Inserted between current slide 01 (cover) and current slide 02 (Le constat); will become the new slide 02.

**Verbatim FR (raw HTML for precise layout).**

```html
<!-- Slide 02 — EFA host-card -->
<section class="slide">
  <div class="slide-meta"><span class="number">02</span><span class="eyebrow">Mission portée conjointement</span></div>
  <h2>Holistika et EFA Académie, une lecture croisée.</h2>
  <p class="slide-sub">Cette mission est portée par Holistika Research et EFA Académie. La discipline méthodologique vient de l'une, la lecture opérationnelle du quotidien procurement vient de l'autre.</p>
  <div class="host-card">
    <div class="host">
      <img class="host-mark" src="{{MONOGRAM_URI}}" alt="Holistika Research" />
      <div class="host-name">Holistika Research</div>
      <div class="host-line">Recherche, opérations, technologie. Discipline méthodologique de bout en bout.</div>
    </div>
    <div class="guest">
      <img class="guest-mark" src="{{EFA_LOGO_LIGHT_URI}}" alt="EFA Académie" />
      <div class="guest-name">EFA Académie</div>
      <div class="guest-line">Lecture opérationnelle du processus WeBuy. Continuité d'opération depuis octobre 2025.</div>
    </div>
  </div>
  <p class="slide-foot">Holistika cadre la règle, conçoit l'application logicielle, et transfère la maîtrise. EFA Académie porte la lecture opérationnelle, valide chaque livrable au plus près du terrain, et accompagne la continuité.</p>
</section>
```

**Voice-test note.** Two-column host-card primitive (D-12-5); host = Holistika at full prominence, guest = EFA Académie at deferred scale; copy avoids any personal name; *"Continuité d'opération depuis octobre 2025"* lands the EFA-since-2025 date without a personal authorship claim ✓ ; D-12-17 clean ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks whether the *"Continuité d'opération depuis octobre 2025"* phrasing reads natural, or whether the operator prefers *"Mission opérationnelle suivie depuis octobre 2025"* / *"Présence sur le processus depuis octobre 2025"* / no date at all on the customer slide.

### Block S3 — Slide 03 Holistika in three lines (D-12-2 network claim retired)

**Where it lands.** New slide inserted as slide 03 (after the EFA host-card).

**Verbatim FR.**

```html
<!-- Slide 03 — Holistika en trois lignes -->
<section class="slide">
  <div class="slide-meta"><span class="number">03</span><span class="eyebrow">Qui nous sommes</span></div>
  <h2>Une discipline qui tient en trois lignes.</h2>
  <p class="slide-sub">Holistika Research est une société de recherche, d'opérations et de technologie, fondée pour faire travailler ensemble ce que beaucoup d'organisations gardent séparé.</p>
  <div class="three-lines">
    <div class="line">
      <h3 class="line-title">Recherche d'abord.</h3>
      <p class="line-body">Avant chaque mission, une lecture du contexte qui distingue ce qui se calcule de ce qui se juge. La règle n'est jamais inventée ; elle est extraite de votre matière.</p>
    </div>
    <div class="line">
      <h3 class="line-title">Opérations ensuite.</h3>
      <p class="line-body">Une discipline d'opérations héritée des grands groupes : six axes (stratégie, opérations, données, marketing, finance, people) tenus de front, avec des livrables qui se chaînent sans rupture.</p>
    </div>
    <div class="line">
      <h3 class="line-title">Technologie en bout de chaîne.</h3>
      <p class="line-body">Une application logicielle est livrée seulement quand la règle qu'elle automatise tient sans elle. Le code suit le cadrage, pas l'inverse.</p>
    </div>
  </div>
</section>
```

**Voice-test note.** Triadic structure (recherche · opérations · technologie) ✓ ; you-frame in second clause (*"votre matière"*) ✓ ; aphoristic close (*"Le code suit le cadrage, pas l'inverse"*) ✓ ; D-12-2 enforced — zero mention of senior practitioners, no callable network, no employer name (IBM/L'Oréal/Volvo/Generali) ✓ ; the *"héritée des grands groupes"* phrasing borrows authority by reference without naming, which is the line-by-line voice-gate question to settle ; D-12-17 clean ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks: keep *"héritée des grands groupes"* (current draft, 6 words of weight by reference), or replace with *"héritée de plus d'une décennie en gouvernance multinationale"* (more abstract, no group-noun), or strip the heritage clause entirely and let the *"six axes"* carry the discipline claim.

### Block S4 — Slide 04 Deux récits, une seule discipline (D-12-3)

**Where it lands.** New slide inserted as slide 04.

**Verbatim FR.**

```html
<!-- Slide 04 — Deux récits, une seule discipline -->
<section class="slide">
  <div class="slide-meta"><span class="number">04</span><span class="eyebrow">D'où vient la méthode</span></div>
  <h2>Deux récits, une seule discipline.</h2>
  <p class="slide-sub">Le cas WeBuy combine deux récits qu'Holistika a déjà tenus ailleurs. La méthode n'est pas inventée pour vous ; elle est ajustée à votre contexte.</p>
  <div class="method-anchors">
    <div class="anchor">
      <span class="anchor-num">01</span>
      <h3 class="anchor-title">Discipline qualité-donnée</h3>
      <p class="anchor-body">Décider de la qualité d'une donnée avant qu'elle entre dans un système. C'est le réflexe qui prévient un litige avant qu'il existe.</p>
    </div>
    <div class="anchor">
      <span class="anchor-num">02</span>
      <h3 class="anchor-title">Discipline gouvernance multinationale</h3>
      <p class="anchor-body">Tenir une règle qui voyage entre filiales, sites, devises, langues. C'est le réflexe qui protège l'opération quand elle change d'échelle.</p>
    </div>
    <div class="anchor">
      <span class="anchor-num">03</span>
      <h3 class="anchor-title">Discipline projet vers logiciel</h3>
      <p class="anchor-body">Traduire un cadre projet (RACI, SLA, cadence de revue) en primitives logicielles plutôt qu'en pratiques de réunion. C'est le réflexe qui rend une mission reproductible sans son auteur.</p>
    </div>
  </div>
</section>
```

**Voice-test note.** Triadic structure ✓ ; each anchor closes on a *"C'est le réflexe qui..."* aphoristic line — operator-natural per voice-corpus §1.6 ✓ ; D-12-2 enforced — no employer name on the surface; the lineage table (*FOUNDER_TRAJECTORY_INTERNAL.md* §4) carries the IBM/Volvo/Generali attribution internally ✓ ; *"Discipline projet vers logiciel"* is the customer-pack name for *"PMP-vers-logiciel discipline"* — the *"projet vers logiciel"* phrasing avoids the certification-acronym which would read as credentialism ; D-12-17 clean ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks: keep *"Discipline projet vers logiciel"* (current), or *"Discipline projet-vers-code"*, or *"Discipline gestion-de-projet appliquée au logiciel"*, or any operator-preferred phrasing.

### Block S5 — Slide 05 How we work today (KM + AKOS-MADEIRA)

**Where it lands.** New slide inserted as slide 05.

**Verbatim FR.**

```html
<!-- Slide 05 — Comment nous travaillons aujourd'hui -->
<section class="slide">
  <div class="slide-meta"><span class="number">05</span><span class="eyebrow">Comment nous travaillons</span></div>
  <h2>Une mémoire opérationnelle, pas une équipe sur étagère.</h2>
  <p class="slide-sub">Holistika gouverne ses missions par la documentation. Chaque décision, chaque règle, chaque livrable est consigné dans un système de connaissance qui rend le travail reproductible et la passation totale.</p>
  <div class="three-lines">
    <div class="line">
      <h3 class="line-title">Une matière documentaire vivante.</h3>
      <p class="line-body">Avant d'écrire votre cahier des charges, nous avons écrit le nôtre — sur la façon dont nous opérons, sur les règles que nous appliquons, sur les sources que nous citons. Cette matière est curée, versionnée, datée.</p>
    </div>
    <div class="line">
      <h3 class="line-title">Une orchestration qui sait ce que nous savons.</h3>
      <p class="line-body">Notre système d'orchestration interne (anonymisé ici par discrétion technique) lit cette matière et la mobilise pour cadrer chaque mission. La règle qui a fait ses preuves chez nous est celle que nous proposons d'abord chez vous.</p>
    </div>
    <div class="line">
      <h3 class="line-title">Une passation totale, pas un attachement.</h3>
      <p class="line-body">Cette même matière est ce que vous récupérez en fin de mission. La documentation que vous lirez à la passation est la documentation à laquelle nous nous tenons en interne. Aucune dépendance résiduelle n'est conservée.</p>
    </div>
  </div>
</section>
```

**Voice-test note.** Triadic structure ✓ ; concrete-noun-anchored (matière documentaire, orchestration, passation) ✓ ; aphoristic close on each line ✓ ; *"anonymisé ici par discrétion technique"* is the operator's voice on his orchestration system — voice-corpus §1.4 lived-experience-grounded but here without naming MADEIRA/Kirby/AKOS (per BRAND_JARGON_AUDIT.md §4 forbidden tokens on customer surfaces) ✓ ; D-12-17 clean ✓ ; *"qui rend le travail reproductible et la passation totale"* echoes the founder's natural cadence in `[EFA-T1]` ("on découpe les tâches", "le transfert de connaissances en bas") ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks: keep the *"anonymisé ici par discrétion technique"* clause (current draft, signals there is a system without naming it), or strip it entirely (the customer doesn't need to know the system has a name), or reveal the name with operator-defined phrasing (e.g. *"un système d'orchestration sémantique propre à Holistika"*).

### Block S2-stat — Renumbered slide 06 *Le constat* stat-grid update (D-12-13, D-12-15)

**Where it lands.** Existing `deck.customer.fr.md` slide 02 (which becomes slide 06 after renumbering), lines 32-57. Updates the H2, slide-sub, anchor row, and one of the three context tiles.

**Verbatim FR (paired with option C above).**

```html
<!-- Slide 06 — Le constat (renumbered from 02) -->
<section class="slide">
  <div class="slide-meta"><span class="number">06</span><span class="eyebrow">Le constat</span></div>
  <h2>Une mécanique répétée, un litige à éviter, sur un parc qui double.</h2>
  <p class="slide-sub">La friction n'est pas la décision. C'est la répétition d'un calcul que l'application logicielle peut prendre en charge, et la chaîne de relances qu'un litige déclenche.</p>
  <div class="stat-narrative">
    <div class="anchor">
      <div class="anchor-row"><span class="anchor-num">20</span><span class="anchor-arrow">↔</span><span class="anchor-num">50</span></div>
      <div class="anchor-label">Demandes WeBuy par jour, selon la cadence du parc.</div>
    </div>
    <div class="context">
      <div class="context-item">
        <span class="context-num">23</span>
        <div class="context-label">Champs par demande, dont la majorité déterministe.</div>
      </div>
      <div class="context-item">
        <span class="context-num">&lt; 2 %</span>
        <div class="context-label">Factures en litige sans numéro de commande, cible mensuelle.</div>
      </div>
      <div class="context-item">
        <span class="context-num">5</span>
        <div class="context-label">Composantes de la règle de nommage à respecter sans erreur.</div>
      </div>
    </div>
  </div>
</section>
```

**Voice-test note.** Triadic title (*mécanique répétée · litige à éviter · parc qui double*) ✓ ; *"50"* and *"↔"* (instead of *"40"* and *"→"*) align the slide with the corrected daily volume and the range framing ; D-12-15 *"Le coût caché"* signal injected via the context tile (*"Factures en litige sans numéro de commande, cible mensuelle"* — phrased per D-12-17 as our cible, not as their CDC target) ✓ ; D-12-17 clean — the `< 2%` figure is presented as our cible mensuelle, not as a CDC quote ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate's option-C/B choice cascades here (option B reverts the anchor to `~20` per jour and drops the `↔` separator).

### Block S3-cell — Renumbered slide 07 *Notre lecture* cell 04 (D-12-15)

**Where it lands.** Existing `deck.customer.fr.md` slide 03 (renumbered to 07), the 4th `<div class="cell">` block (lines 83-87).

**Verbatim FR.**

```html
<div class="cell">
  <span class="cell-num">04 · Le coût caché</span>
  <h3 class="cell-title">Le litige pèse plus que la saisie.</h3>
  <p class="cell-body">Une facture sans numéro de commande, un frais de transport hors devis : la chaîne de relances qui en découle bloque le règlement fournisseur le temps de la régularisation. C'est l'enjeu qui mérite la priorité, et c'est celui que la solution porte au cœur.</p>
</div>
```

**Voice-test note.** Replaces the cell that was previously *"Compétence préservée"* with *"Le coût caché"* signal (D-12-15) ; the *Compétence préservée* shape moves to a new place — see block S5-card below for the redistribution ; *"C'est l'enjeu qui mérite la priorité"* echoes the proposal block 1b-01 verbatim (consistency across surfaces) ✓ ; D-12-17 clean ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks: where does *Compétence préservée* land now? Two options surface in S5-card.

### Block S5-card — Renumbered slide 09 *Ce que fait l'application* — 5th feature card (D-12-15) + restoration of *Compétence préservée*

**Where it lands.** Existing `deck.customer.fr.md` slide 05 (renumbered to 09). The slide currently has a 2×2 grid of 4 features; we change to either:
- **Option α** — 3×2 grid with **5 features + 1 *Compétence préservée* note tile** (bottom-right). Layout: F-01 / F-02 / F-03 / F-04 / F-05 (litige module) / *Compétence préservée*.
- **Option β** — keep 2×2 grid, drop *Compétence préservée* from the deck (it stays in the proposal §2 only), surface F-05 litige in its own row beneath the grid.

**Verbatim FR — option α (default; gate picks).**

```html
<!-- Slide 09 — Ce que fait l'application (renumbered from 05) -->
<section class="slide">
  <div class="slide-meta"><span class="number">09</span><span class="eyebrow">Ce que fait l'application</span></div>
  <h2>Cinq fonctionnalités, parmi les vingt-quatre identifiées.</h2>
  <p class="slide-sub">La cinquième concerne directement la prévention des litiges. Le périmètre complet figure dans le cahier des charges fonctionnel transmis avec cette présentation.</p>
  <div class="grid-3x2">
    <!-- F-01..F-04 cells unchanged from current deck.customer.fr.md lines 128-149 -->
    <div class="cell">
      <span class="cell-num">F · 05</span>
      <h3 class="cell-title">Module de prévention et gestion des litiges</h3>
      <p class="cell-body">Chaque demande porte son numéro de commande, transmis et tracé. Le rapprochement automatique aux factures identifie les écarts. Un tableau de bord montre la charge en cours par ancienneté, pour un pilotage hebdomadaire de la trésorerie immobilisée.</p>
    </div>
    <div class="cell quiet">
      <span class="cell-num">Hors périmètre logiciel</span>
      <h3 class="cell-title">Compétence interne préservée</h3>
      <p class="cell-body">La personne qui opère garde le jugement sur ce qui demande du discernement : relations fournisseurs, négociation, traitement des anomalies. Aucune fonctionnalité n'empiète sur cette zone.</p>
    </div>
  </div>
</section>
```

**Voice-test note.** Five-feature grid ✓ ; F-05 carries the litige module verbatim per block 1b-05 (consistency); the bottom-right cell with the `quiet` class flags the *Compétence préservée* zone as **out-of-scope-by-design** rather than as a feature, which preserves the operator's sovereignty signal without inflating the feature count ; D-12-17 clean ✓ ; closes with *"Aucune fonctionnalité n'empiète sur cette zone"* — operator-natural aphoristic close ✓.

**Approval.** `[ OK option α / OK option β / REWRITE / REJECT ]`

### Block S8-cells — Renumbered slide 12 *Critères de réussite* — KPIs as commitments (D-12-15, D-12-17)

**Where it lands.** Existing `deck.customer.fr.md` slide 08 (renumbered to 12), the 4-cell `grid-2x2` block (lines 224-249). Replaces the four existing cells with three commitment KPIs + one composite *Continuité* tile.

**Verbatim FR.**

```html
<!-- Slide 12 — Critères de réussite (renumbered from 08) -->
<section class="slide">
  <div class="slide-meta"><span class="number">12</span><span class="eyebrow">Critères de réussite</span></div>
  <h2>Quatre engagements, mesurés conjointement.</h2>
  <p class="slide-sub">Trois engagements financiers et opérationnels portés par la solution, et un engagement de continuité porté par Holistika.</p>
  <div class="grid-2x2">
    <div class="row">
      <div class="cell">
        <span class="cell-num">01 · Litige sans numéro de commande</span>
        <h3 class="cell-title">Moins de 2 %, mesure mensuelle.</h3>
        <p class="cell-body">Le taux de factures réceptionnées sans numéro de commande associé est notre cible mensuelle, calculée sur le périmètre traité par la solution.</p>
      </div>
      <div class="cell">
        <span class="cell-num">02 · Délai de résolution</span>
        <h3 class="cell-title">Moins de cinq jours ouvrés.</h3>
        <p class="cell-body">Le délai moyen entre l'ouverture d'une fiche litige et son règlement effectif est notre cible mensuelle, calculé sur la même base.</p>
      </div>
    </div>
    <div class="row">
      <div class="cell">
        <span class="cell-num">03 · Couverture du registre</span>
        <h3 class="cell-title">Cent pour cent, mesure hebdomadaire.</h3>
        <p class="cell-body">Toutes les demandes émises portent un numéro de commande tracé dans le registre central. Cette couverture est l'engagement le plus structurant, parce qu'elle conditionne les deux autres.</p>
      </div>
      <div class="cell">
        <span class="cell-num">04 · Continuité opérationnelle</span>
        <h3 class="cell-title">Sans dépendance résiduelle.</h3>
        <p class="cell-body">À la fin de la mission, votre direction des SI dispose de la documentation pour reprendre en interne, et la personne qui opère continue sans rupture.</p>
      </div>
    </div>
  </div>
</section>
```

**Voice-test note.** *"Quatre engagements"* ladders the operator's quadriadic-enumeration register ✓ ; the three financial-operational KPIs match the proposal block 1b-06 verbatim (consistency); the *Continuité opérationnelle* cell ties to D-12-4 (the operator-led/Holistika-led posture is referenced obliquely without forcing a choice on the slide); D-12-17 clean — *"notre cible mensuelle"* / *"calculée sur le périmètre traité par la solution"* without CDC reference ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks whether to use *"engagement"* (current draft) or *"repère"* (existing word in the slide before reframe). *"Engagement"* leans into our ownership of the metric; *"repère"* is more peer-collaborative.

---

## Continuité §3 (D-12-4) — proposal new section

### Block C3 — `proposal.customer.fr.md` new §3 *Continuité opérationnelle*

**Where it lands.** Inserted between the existing `# Ce que nous construisons` block (proposal current §3, which becomes §4) and `# Ce que nous proposons` (current §4, which becomes §5). New section gets the H1 *"# Continuité opérationnelle"* and renumbering cascades through §4-§9.

**Verbatim FR.**

```markdown
# Continuité opérationnelle

La mécanique livrée par cette mission ne remplace pas la personne qui opère ; elle libère son temps pour ce qui demande du jugement. À la fin de la mission, deux postures de continuité sont possibles, selon le souhait de votre direction.

## Posture A — Continuité portée par l'équipe opérationnelle

La personne qui opère reprend la maintenance courante de l'application logicielle (mise à jour du référentiel des catégories, ajustement des règles de nommage, suivi des évolutions WeBuy mineures). Holistika reste disponible sur une cadence trimestrielle pour la revue de gouvernance — nouvelles fonctionnalités, ajustements de seuil, support en cas de rupture inattendue. Cette posture est la posture de référence ; elle est cohérente avec la continuité d'opération assurée par EFA Académie sur le processus depuis octobre 2025.

## Posture B — Continuité portée par Holistika

Holistika porte la maintenance directement sur une cadence mensuelle, avec un engagement de service reformulé. Cette posture convient aux organisations qui préfèrent un fournisseur unique sur le triptyque conception-construction-exploitation.

## Tarification de la continuité

Le coût de la continuité, dans l'une ou l'autre posture, ne peut être fixé avant la phase de découverte. Il dépend de la profondeur des évolutions prévues sur les douze mois qui suivent la mise en service, et du périmètre exact de l'application logicielle livrée. Une fourchette indicative est intégrée à l'annexe commerciale, à révision après l'atelier de cadrage.
```

**Voice-test note.** Triadic posture (équipe · Holistika · révision tarifaire) ✓ ; you-frame in *"selon le souhait de votre direction"* and *"votre direction des SI"* references ✓ ; *"continuité d'opération assurée par EFA Académie sur le processus depuis octobre 2025"* lands the EFA-since-2025 date in customer-pack prose (D-12-14) without a personal authorship claim — operator approves at gate ✓ ; *"triptyque conception-construction-exploitation"* is the operator's natural register (per voice-corpus §1.1) ✓ ; D-12-17 clean ✓ ; tarification deferred to annexe per D-12-4 ✓.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks: keep the *"continuité d'opération assurée par EFA Académie sur le processus depuis octobre 2025"* phrasing (current draft, names EFA explicitly in customer pack), or replace with *"par notre partenaire opérationnel sur le processus depuis octobre 2025"* (anonymized, EFA only on the cover-strip). The S2 host-card already names EFA, so the second occurrence in §3 may read as redundant — gate decides.

---

## Cover-strip metadata (D-12-5)

### Block CSM — Cover-strip 4-field across all customer-pack surfaces

**Where it lands.** All customer-pack rendered surfaces (`proposal.customer.fr.pdf`, `tarification.customer.fr.pdf`, `deck.customer.fr.pdf`). The cover-strip, currently 3 fields (Programme · Date · Discipline), becomes 4 fields (Programme · Date · Discipline · En collaboration avec).

**Verbatim FR — cover-strip block (rendered by `_build_cover_html`).**

```html
<div class="cover-strip">
  <div class="strip-item"><span class="strip-label">Programme</span><span class="strip-value">ENG-SUEZ-WEBUY-2026</span></div>
  <div class="strip-item"><span class="strip-label">Date</span><span class="strip-value">2026-05-10</span></div>
  <div class="strip-item"><span class="strip-label">Discipline</span><span class="strip-value">Présentation commerciale</span></div>
  <div class="strip-item"><span class="strip-label">En collaboration avec</span><span class="strip-value">EFA Académie</span></div>
</div>
```

**Voice-test note.** The new strip-item key `EN COLLABORATION` is added to `_COVER_STRIP_LABELS` in P12.7 (FR / EN / ES localization) per D-12-5 ✓. The cover-strip stays at 4 fields on portrait surfaces; the slide-deck cover layout may compress to 3 (drops *Discipline*) if the deck cover-strip becomes too dense — gate decides at P12.4.

**Approval.** `[ OK / REWRITE / REJECT ]` — gate also picks portrait-surface 4-field vs landscape-deck 3-field-or-4-field.

---

## End of P12.1 content drafts

The blocks above are staged for line-by-line operator approval at the P12.4 voice gate. P12.5 commits the approved blocks into the canonical surfaces; P12.7 implements the render pipeline primitives that some blocks reference (`.host-card`, `.method-anchors`, `.three-lines`, `.grid-3x2`, `EN COLLABORATION` cover-strip, EFA logo URI substitution). The two voice-corpus tests (concrete-noun-anchor + D-12-17 discretion) run again at P12.8 leak hunt.

Total blocks in this draft: **23** (3 volume / 9 litige / 1 EFA date / 1 internal-audit / 4 new slides / 4 amended slides / 1 continuité / 1 cover-strip).

P12.4 voice gate is the single MANDATORY operator-approval moment for all of the above. No commit lands on canonical files between this draft and the gate.

