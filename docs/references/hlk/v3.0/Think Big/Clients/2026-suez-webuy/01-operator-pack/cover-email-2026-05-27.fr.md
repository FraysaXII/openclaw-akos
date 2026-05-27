---
language: fr
status: draft
audience: customer
register: external
program_id: ENG-SUEZ-WEBUY-2026
engagement_slug: 2026-suez-webuy
artifact_role: customer-deliverable
intellectual_kind: cover_email
brand_voice_register: peer_consulting
brand_pricing: excluded
collaboration_partner: EFA Académie
collaboration_since: 2025-10
mission_posture: Mission portée conjointement
target_send_date: 2026-05-27
target_recipient_placeholder: "[NOM_LECTEUR_SUEZ]"
attachments:
  - 02-customer-pack/deck.customer.fr.pdf
  - 02-customer-pack/proposal.customer.fr.pdf
  - 02-customer-pack/demo-libelle-generator.customer.fr.pdf
  - 02-customer-pack/demo-dispute-register-litigation-detection.customer.fr.pdf
render_target: mail
render_pipeline_note: "Rendered to HTML body at SMTP-send time via downstream mail tooling; .md is the source-of-truth and is NEVER sent externally per akos-external-render-discipline.mdc RULE 1; operator finalises [NOM_LECTEUR_SUEZ] resolution + Aïsha first-name reveal (if appropriate at SMTP-send time per BBR identity discipline) + attaches the 4 PDFs (deck + proposal + 2 demos) rendered from their .md counterparts in 02-customer-pack/; architecture-addendum.fr.pdf is NOT in this send (deleted at Wave R+3 Commit 1 per D-IH-86-EQ — content overlap with the deck + proposal + demos already covers the architecture story without a separate addendum)."
last_review: 2026-05-27
ratifying_decisions:
  - D-IH-86-EP
  - D-IH-86-EQ
  - D-IH-86-ER
  - D-IH-86-ES
  - D-IH-86-ET
linked_canonicals:
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/deck.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/proposal.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/demo-libelle-generator.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/demo-dispute-register-litigation-detection.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/01-operator-pack/cdc-feasibility-shape.fr.md
---

# Cover mail — SUEZ WeBuy procure-to-pay, suite à notre échange du 13 mai

> **DRAFT — operator-final-pass required.** Resolve `[NOM_LECTEUR_SUEZ]` + decide Aïsha first-name reveal at SMTP-send time per BBR identity discipline. Attach the 4 PDFs from `02-customer-pack/` after WeasyPrint render (deck + proposal + 2 demos). Stream B (continuité opérationnelle 5 k€/mois) is **not** mentioned in detail in this body — Aïsha sends her own EFA-branded proposal separately on her side per operator coaching of 13/05.

---

**Objet :** Suite à notre échange du 13 mai — proposition et deux démonstrations concrètes

**De :** Holistika Research — en collaboration avec EFA Académie
**À :** [NOM_LECTEUR_SUEZ]
**Pièces jointes :**

- Présentation commerciale (14 pages)
- Proposition d'engagement (cadrage → prototype → industrialisation)
- Démonstration n°1 — générateur de libellés
- Démonstration n°2 — registre des litiges avec détection précoce

---

Bonjour [NOM_LECTEUR_SUEZ],

Merci à vous et à vos équipes pour la qualité de notre échange du **13 mai dernier**. Comme convenu à cette occasion, nous vous adressons aujourd'hui une proposition écrite et concrète, structurée autour des deux priorités opérationnelles que vous avez nommées : la composition fiable des demandes WeBuy, et la prévention des litiges fournisseurs.

## Ce que vous trouverez en pièce jointe

**1. La présentation commerciale (14 pages).** Le cadrage que vous avez vu en séance, mis au propre. Elle reprend notre lecture des six familles d'engagement de votre parc, la chaîne de friction observée (libellés flottants, factures sans numéro de commande, allers-retours fournisseurs), et la mécanique en trois temps que nous proposons pour la traiter.

**2. La proposition d'engagement.** Trois étapes : un cadrage opérationnel court, un prototype livré sous une quinzaine de jours, et une phase d'industrialisation multi-catégories sur votre tenant Microsoft. Le détail tarifaire fait l'objet d'un document séparé que nous vous adresserons sous le même envoi si vous le souhaitez.

**3. Démonstration n°1 — générateur de libellés.** Trois à quatre pages illustrées qui décrivent, étape par étape, comment l'opérateur compose un libellé conforme à votre nomenclature en cinq composants à partir d'une référence catégorie–compte comptable. La démonstration s'appuie sur Excel et la suite Power Platform — l'environnement Microsoft dans lequel vos équipes travaillent déjà.

**4. Démonstration n°2 — registre des litiges avec détection précoce.** Trois à quatre pages dédiées à ce que vous avez décrit en séance comme un **coût souvent invisible** dans la chaîne d'approvisionnement : la facture qui arrive sans numéro de commande, l'écart de montant non détecté à temps, le fournisseur inconnu du registre. La démonstration décrit le rapprochement automatique facture/registre, les trois alertes typées que vous avez nommées au cahier des charges, le tableau de bord par ancienneté (J / J+7 / J+30 / au-delà), et le mécanisme de signalement précoce des fiches qui présentent un profil de risque cumulé — celles qui, sans intervention, finissent en contentieux.

## La logique du calendrier

Vous avez mentionné en séance que **juin et juillet sont des fenêtres mobilisables, août l'est moins**, et que la décision de mise en œuvre se prend en septembre. Cette lecture nous convient. Nous vous proposons donc deux étapes pour les prochaines semaines :

1. **Un point de quinze à vingt minutes**, en début de semaine prochaine si votre agenda le permet, pour répondre à vos questions sur les quatre documents joints et caler ensemble la fenêtre de cadrage.

2. **Une rencontre avec votre Direction des Systèmes d'Information**, idéalement dans les deux semaines qui suivent. Vous nous aviez signalé que la DSI n'avait pas encore été briefée sur le périmètre d'automatisation. Une pré-validation technique conjointe nous permettrait de partir, en septembre, sur un cadrage déjà aligné avec vos contraintes d'environnement Microsoft et de gouvernance des accès.

## Continuité d'opération

Comme évoqué le 13 mai, notre partenaire EFA Académie — qui opère aujourd'hui votre processus WeBuy et qui assurera la continuité opérationnelle pendant et après la mise en service — vous adressera **séparément**, dans le courant de la semaine, sa propre proposition pour le volet maintenance opérationnelle. Les deux volets sont articulés mais distincts dans leur portage commercial, afin que chacun reste lisible et que vos arbitrages internes soient simples à conduire.

---

Nous restons à votre disposition pour toute précision en amont de notre prochain échange.

Bien à vous,

**Équipe Holistika Research × EFA Académie**

— Mission portée conjointement —

---

*Cette adresse est suivie conjointement par notre équipe et celle d'EFA Académie ; vos réponses seront traitées dans la continuité de notre échange du 13 mai.*
