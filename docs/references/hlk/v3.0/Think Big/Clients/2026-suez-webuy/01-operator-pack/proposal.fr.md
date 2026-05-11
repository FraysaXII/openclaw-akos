---
status: draft
classification: external
access_level: 4
language: fr
register: external
audience: customer-enterprise
artifact_kind: proposal
engagement_slug: 2026-suez-webuy
counterparty_org_ref: GOI-CUS-SUEZ-2026
linked_engagement: 2026-05-10-suez-webuy-procure-to-pay
collaboration_partner: EFA Académie
collaboration_since: 2025-10
mission_posture: Mission portée conjointement
governance:
  - SOP-ENG_PROPOSAL_001
  - SOP-ENG_ESTIMATION_DISCIPLINE_001
  - PROPOSAL_TEMPLATE
  - BRAND_FRENCH_PATTERNS
  - FOUNDER_BIO
  - SERVICE_OFFERING_CATALOG
  - BRAND_COBRANDING_PATTERN
last_review: 2026-05-10
---

# Proposition d'engagement — automatisation du processus de demande d'achat WeBuy

| | |
|:---|:---|
| **Pour** | [entité juridique du donneur d'ordre] |
| **Préparée par** | Holistika Research SL |
| **Date** | 2026-05-10 (version 1.0, version de discussion) |
| **Type d'engagement** | Mission cadrée, avec option d'évolution vers mission embarquée selon la variante retenue |
| **Mise en relation** | Mission relayée par notre partenaire de collaboration ; le porteur du compte SUEZ côté Holistika reste l'interlocuteur principal pour le pilotage et la livraison |
| **Calendrier prévisionnel de démarrage** | Lancement souhaité 2026-05-19, à confirmer en séance de cadrage |
| **Annexes commerciales** | Calendrier commercial et tarification annexés séparément (variantes A, B, C) |

> Cette proposition est rédigée en français, dans un registre opérationnel-formel (vouvoiement). Elle adopte la structure canonique en huit sections de notre modèle interne de proposition. Les valeurs financières détaillées figurent dans le calendrier commercial annexé ; ce document de proposition s'engage sur le périmètre, la méthode, le calendrier et les critères de réussite.

---

## 1. Notre lecture de votre contexte

À l'issue de notre lecture du cahier des charges WeBuy (version 1.0, avril 2026) et du mode opératoire de passage de commandes que vous avez transmis, et après échanges avec le porteur du compte SUEZ côté Holistika, nous lisons la contrainte opérationnelle de la manière suivante :

> Le processus actuel de demande d'achat WeBuy mobilise une charge opérationnelle significative pour générer, à chaque demande, un libellé conforme à une règle de nommage à cinq composantes, à pré-remplir une dizaine de champs déterministes mais variables par catégorie, et à transférer en aval les documents fournisseurs sans perte d'information. La perspective d'un parc en croissance — environ sept-cent-cinquante engins aujourd'hui, près de neuf-cent-cinquante en juin — accentue cette charge sans que le système actuel ne propose d'allègement structurel.

Signaux concordants relevés dans votre documentation :

- Une règle de nommage à cinq composantes appliquée à la majorité des catégories, avec une variante pour la catégorie CAPEX ; cette règle est génératrice par construction.
- Six catégories distinctes (CAPEX, maintenance, pneus, fourniture de pièces, transport, location), chacune avec ses propres conventions de centre de coût, compte comptable et pièces jointes.
- Douze codes types d'intervention qui structurent l'ensemble des demandes et constituent une clé de classification stable.
- Un référentiel parc engins central, qui alimente plusieurs champs et conditionne la qualité des demandes émises.
- Une absence actuelle de reporting mensuel automatisé, alors que la croissance du parc rend ce pilotage de plus en plus utile.

Ce que cette situation crée, telle que nous l'observons :

- **Conséquence opérationnelle** — une part significative du temps de la personne qui opère le processus est consacrée à des tâches déterministes que des règles claires permettraient de pré-remplir.
- **Conséquence de qualité** — la variabilité des conventions par catégorie ouvre un risque d'erreurs ponctuelles (libellé incomplet, compte comptable inadéquat, pièce jointe manquante) que la croissance du parc va mécaniquement amplifier.
- **Conséquence de pilotage** — l'absence d'un reporting structuré à la maille mensuelle prive votre direction des engins TP d'une visibilité d'usage que le portail pourrait alimenter aujourd'hui.

## 2. Périmètre proposé

Nous proposons une mission cadrée en trois ou quatre phases. Trois variantes vous sont soumises ; vous choisissez celle qui correspond à votre niveau d'ambition initial et à votre fenêtre d'engagement.

### Variante A, cadrage et faisabilité (engagement le plus court)

| Phase | Discipline | Livrable principal | Durée prévisionnelle |
|:---|:---|:---|:---|
| 1 | Diagnostic de processus | Cahier des charges détaillé, lecture point-par-point des vingt-quatre fonctionnalités identifiées | 4 semaines |
| 2 | Étude de faisabilité | Étude de faisabilité par classe d'application (portail WeBuy et couche de reporting) | 3 semaines |
| 3 | Passation opérationnelle | Manuel opérationnel transmis et passation à votre équipe | 1 semaine |

### Variante B, cadrage, faisabilité et prototype (variante recommandée)

| Phase | Discipline | Livrable principal | Durée prévisionnelle |
|:---|:---|:---|:---|
| 1 | Diagnostic et étude de faisabilité | Cahier des charges détaillé et étude de faisabilité | 4 semaines |
| 2 | Conception conjointe | Atelier de conception et spécification fonctionnelle | 2 semaines |
| 3 | Construction (Phase 1) | Prototype Excel ou Power Query couvrant les fonctionnalités les plus génératives, dans un environnement conforme | 3 semaines |
| 4 | Formation et passation | Formation d'une vague d'opérateurs, manuel opérationnel et passation | 2 semaines |

### Variante C, opérationnalisation complète (variante la plus complète)

| Phase | Discipline | Livrable principal | Durée prévisionnelle |
|:---|:---|:---|:---|
| 1 | Diagnostic et étude de faisabilité | Identique à Variante B | 4 semaines |
| 2 | Conception conjointe | Identique à Variante B | 2 semaines |
| 3 | Construction (Phase 1) | Identique à Variante B | 3 semaines |
| 4 | Construction (Phase 2) | Application web légère multi-catégories, dans un environnement conforme | 6 semaines |
| 5 | Formation et passation | Deux vagues de formation, manuel opérationnel étendu et passation | 3 semaines |

### Hors-périmètre commun aux trois variantes

- L'industrialisation finale en environnement de production interne à [entité juridique du donneur d'ordre] (migration ultérieure, à conduire par votre direction des systèmes d'information).
- Le coût des licences ou abonnements internes à [entité juridique du donneur d'ordre] (Microsoft Azure, comptes de service, licences spécifiques).
- La refonte de la règle de nommage ou des conventions de centre de coût existantes (nous travaillons avec les conventions en vigueur).
- L'intégration directe en lecture-écriture avec le portail WeBuy : ce volet est traité en étude de faisabilité, jamais en construction sans validation préalable de votre direction des systèmes d'information.

## 3. Méthode

L'engagement suit un rythme simple, identique pour les trois variantes :

1. **Découvrir** — confirmer la lecture opérationnelle, le volume mensuel par catégorie, les contraintes de votre direction des systèmes d'information, et les critères de réussite spécifiques à votre direction des engins TP.
2. **Cadrer** — produire le cahier des charges détaillé (vingt-quatre fonctionnalités, drapeaux d'éligibilité, dépendances, priorisation par valeur opérationnelle).
3. **Construire** — selon la variante retenue, livrer l'étude de faisabilité, le prototype Phase 1, ou l'application web Phase 2.
4. **Transférer** — former les personnes qui opéreront le système, transmettre le manuel opérationnel, conduire la passation.
5. **Clore** — bilan d'engagement, capitalisation des enseignements, inscription des prochaines décisions au registre.

## 4. Calendrier et jalons

Calendrier indicatif sur la base d'un démarrage 2026-05-19. Le calendrier commercial annexé détaille les durées par lot de travail, les variations min / par / max, et les durées en jours ouvrés tenant compte des jours fériés français.

| Jalon | Décision attendue | Responsable | Cible |
|:---|:---|:---|:---|
| Réunion de lancement | Confirmation du périmètre retenu et des accès | Holistika + [entité juridique du donneur d'ordre] | 2026-05-19 |
| Clôture de la phase Découverte + cadrage | Cahier des charges détaillé accepté | [responsable côté donneur d'ordre] | semaine 4 |
| Clôture de l'étude de faisabilité | Étude de faisabilité acceptée par votre direction des systèmes d'information | [DSI] + Holistika | semaine 7 |
| Démonstration du prototype (variantes B et C) | Prototype validé fonctionnellement | [responsable côté donneur d'ordre] | semaine 10 |
| Clôture de la construction (variante C) | Application web acceptée | [DSI] + [responsable] | semaine 16 |
| Passation finale | Manuel opérationnel transmis, formation effectuée | Holistika | semaine 18 (variante C) / semaine 12 (B) / semaine 8 (A) |

## 5. Posture commerciale

Posture recommandée : **mission cadrée**.

- Le périmètre ci-dessus est le document qui pilote la mission. Toute extension matérielle fait l'objet d'un avenant écrit avant que le travail ne s'élargisse.
- Les variantes A, B et C sont équivalentes dans leur méthode ; elles diffèrent par leur ambition de sortie. La progression A → B → C est strictement additive, sans rupture méthodologique.
- La tarification est confirmée dans le calendrier commercial annexé ; elle est exprimée en fourchette (basse / par défaut / haute) pour chaque lot, et consolidée en prix forfaitaire par variante.
- Aucune relation de dépendance prolongée n'est recherchée : la passation finale est conçue pour rendre votre équipe autonome sur l'usage de l'outil livré.

## 6. Critères de réussite

L'engagement est réussi quand :

- **Critère opérationnel** — le temps moyen consacré à la génération d'une demande d'achat conforme par la personne qui opère le processus est réduit de manière objectivable. La cible exacte est fixée à la phase 1 sur la base de mesures de l'état actuel.
- **Critère de pilotage** — un reporting mensuel auto-généré couvre la répartition des demandes par catégorie, par fournisseur, par engin et par centre de coût ; il est livré sans intervention manuelle à partir du moment où il est mis en service.
- **Critère de passation** — le manuel opérationnel transmis permet à un nouvel opérateur de prendre en charge le processus dans un délai conforme à la cible que nous fixerons ensemble lors du lancement.
- **Critère de durabilité** — votre direction des systèmes d'information dispose de la documentation nécessaire pour reprendre l'outil en interne si vous le souhaitez après la phase 4 (variantes B et C).

## 7. À propos de Holistika

Holistika Research SL est une boîte de stratégie qui dispose d'un laboratoire technologique. La méthode rapproche trois disciplines qui sont d'habitude séparées : le diagnostic de processus, le cadrage opérationnel, et la construction d'outils techniques.

Notre fondateur :

> Fayçal Njoya a fondé Holistika pour aider les entreprises à rendre leur fonctionnement plus clair, plus reproductible et plus simple à opérer. Son parcours est aussi pratique que stratégique : il a construit des systèmes opérationnels dans des entreprises en activité, dont un précédent modèle multi-sites en franchise. Holistika apporte cette discipline opérationnelle aux missions clients, depuis le diagnostic et la conception de processus jusqu'à l'implémentation technique et la passation.

L'engagement avec [entité juridique du donneur d'ordre] sera piloté par le porteur du compte SUEZ côté Holistika, en lien direct avec notre fondateur sur les choix d'architecture et de méthode. Notre partenaire de collaboration assure la passerelle initiale et reste disponible pour les ajustements en cours d'engagement.

## 8. Acceptation

Cette proposition, une fois acceptée, devient la base de l'énoncé de mission. Les conditions juridiques sont régies par les modèles contractuels usuels (accord-cadre de services, énoncé de mission, accord de confidentialité, accord de traitement des données) qui vous seront transmis dans la foulée.

| | |
|:---|:---|
| **Acceptation côté [entité juridique du donneur d'ordre]** | [Nom — fonction — date] |
| **Acceptation côté Holistika Research SL** | [Nom — fonction — date] |

---

## Liste de validation interne (operator review checklist)

*Ce bloc est conservé dans la version interne uniquement ; il est retiré avant transmission externe.*

- [ ] Cellules de service explicites — `1A → 1B → 5C → 6C` couvrent les trois variantes.
- [ ] Périmètre dedans / dehors explicite — quatre éléments hors-périmètre listés en §2.
- [ ] Aucun terme du registre interne — vérifié manuellement (`elicitation`, `baseline reality`, `counterparty`, `agent`, `AKOS` absents).
- [ ] Variante de la biographie du fondateur conforme — variante Customer-SME / mid-market en §7.
- [ ] Critères de réussite mesurables — quatre critères en §6, dont les cibles précises sont fixées au lancement.
- [ ] Cheminement juridique clair — §8 cite le quatuor MSA / SOW / NDA / DPA.
- [ ] Aucun montant en euros n'apparaît dans la proposition v1 — tarification annexée séparément.
- [ ] Le porteur du compte SUEZ côté Holistika n'est pas nommé directement.
