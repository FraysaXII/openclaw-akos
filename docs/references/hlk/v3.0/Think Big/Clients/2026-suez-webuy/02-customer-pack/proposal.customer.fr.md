---
language: fr
status: active
audience: customer
register: external
program_id: ENG-SUEZ-WEBUY-2026
engagement_slug: 2026-suez-webuy
artifact_role: customer-deliverable
intellectual_kind: proposal
brand_voice_register: peer_consulting
brand_pricing: excluded
brand_pricing_companion: tarification.customer.fr.md
collaboration_partner: EFA Académie
collaboration_since: 2025-10
mission_posture: Mission portée conjointement
last_review: 2026-05-10
---

<p class="lead">Vos équipes traitent entre vingt et une cinquantaine de demandes WeBuy par jour, selon la cadence du parc. La friction se loge dans la facture qui arrive sans numéro de commande, le frais de transport ajouté hors devis, le rapprochement qui ne tient pas, et la chaîne de relances qui en découle. Nous proposons une mécanique qui prévient ces ruptures à la source : cadrer la règle, prototyper l'outil, transférer la maîtrise.</p>

<div class="stat-grid">
  <div class="stat"><span class="stat-num">20 ↔ 50</span><span class="stat-label">Demandes par jour, selon cadence du parc</span></div>
  <div class="stat"><span class="stat-num">~1 ETP</span><span class="stat-label">Mécanique consommée aujourd'hui</span></div>
  <div class="stat"><span class="stat-num">~2 ETP</span><span class="stat-label">À mise en service du parc complet</span></div>
</div>

# Notre lecture de votre situation

Le processus actuel est entièrement déterministe : à partir d'un numéro d'engin, d'une catégorie et d'un devis fournisseur, l'opérateur construit la demande WeBuy en suivant des règles stables — compte comptable, libellé, magasin, périmètre PR ou SQS. La friction réside dans la **répétition** d'un calcul qu'une application logicielle peut prendre en charge, et dans la **chaîne de relances** qu'un litige déclenche.

Cinq signaux, croisés avec le contexte que vous décrivez, orientent notre lecture :

- **Volume.** Vingt à une cinquantaine de demandes par jour selon la cadence du parc, sur une mécanique qui doublera avec la mise en service du parc complet.
- **Stabilité de la règle.** Le rapprochement catégorie ↔ compte comptable est tabulé ; il évolue lentement.
- **Maturité de WeBuy.** Le portail expose une demande typée et acceptable côté SI ; nos contrôles d'entrée sont alignés.
- **Le coût caché : les litiges.** Une facture sans numéro de commande, un frais de transport ajouté hors devis : la chaîne de relances qui en découle pèse plus que la saisie initiale, et bloque le règlement fournisseur le temps de la régularisation. C'est l'enjeu qui mérite la priorité, et c'est celui que nous inscrivons au cœur de la solution.
- **Compétence interne préservée.** La personne qui opère garde le jugement sur ce qui demande du discernement : relations fournisseurs, négociation, traitement des anomalies. L'application logicielle traite la mécanique et prévient les ruptures à la source.

> Automatiser ce qui se calcule, prévenir ce qui se rompt, préserver ce qui se juge.{: .pull-quote }

# Ce que nous construisons

Une application logicielle légère qui prend en charge la mécanique de la demande WeBuy, et qui laisse à la personne qui opère ce qui demande du jugement.

## Le parcours d'une demande, avant et après

| Aujourd'hui | Avec l'application |
|:---|:---|
| Une vingtaine de minutes pour reconstruire chaque demande à partir d'un courriel fournisseur. | Quelques minutes pour vérifier et valider une demande pré-construite. |
| Le compte comptable, le libellé et la pièce jointe sont saisis manuellement à chaque fois. | Ces champs sont calculés à partir du numéro d'engin et de la catégorie. |
| La conformité au référentiel de nommage repose sur la mémoire de la personne qui opère. | Le libellé respecte la règle par construction, sans relecture obligatoire. |
| Le suivi des demandes est dispersé dans les courriels et les exports manuels. | Un tableau de bord récapitule les demandes par catégorie, fournisseur et engin. |

## Le parcours, en quatre temps

1. **Lecture.** La personne qui opère saisit ou colle les éléments de contexte : numéro d'engin, catégorie, devis fournisseur. La pièce jointe est associée d'un seul geste.
2. **Composition.** L'application calcule les champs déterministes : compte comptable selon la catégorie, libellé selon la règle de nommage, magasin selon le périmètre.
3. **Revue.** La personne qui opère relit la demande pré-construite, ajuste ce qui doit l'être, et valide. Aucun champ n'est inscrit dans WeBuy sans cette validation.
4. **Soumission.** La demande validée est posée dans le panier WeBuy par la personne qui opère, dans les conditions d'accès qui sont les siennes aujourd'hui. Le portail reste l'autorité de décision.

## Cinq fonctionnalités, parmi les vingt-quatre identifiées

- **Mappage catégorie ↔ compte comptable.** Un référentiel maintenu côté Holistika, validé avec votre direction comptable, qui fixe sans ambiguïté le compte à utiliser pour chaque catégorie.
- **Générateur de libellé.** La règle de nommage à cinq composantes (catégorie, engin, type d'intervention, fournisseur, référence) est calculée par construction, sans saisie libre.
- **Pré-remplissage par catégorie.** Magasin, périmètre PR ou SQS, type d'engagement : chaque catégorie hérite d'un tableau de pré-remplissage issu de votre mode opératoire actuel.
- **Tableau de bord d'usage.** Un récapitulatif mensuel auto-généré des demandes par catégorie, fournisseur, engin et centre de coût. Lisible sans intervention manuelle, à partir du moment où il est mis en service.
- **Module de prévention et gestion des litiges.** Chaque demande porte son numéro de commande, transmis au fournisseur et conservé dans un registre central. À réception d'une facture, le rapprochement automatique au registre identifie immédiatement les écarts — numéro absent, montant divergent, fournisseur inconnu. Un tableau de bord montre la charge en cours, l'ancienneté par bucket (J, J+7, J+30, au-delà), et les fournisseurs récurrents, pour un pilotage hebdomadaire de la trésorerie immobilisée.

# Continuité opérationnelle

La mécanique livrée par cette mission ne remplace pas la personne qui opère ; elle libère son temps pour ce qui demande du jugement. À la fin de la mission, deux postures de continuité sont possibles, selon le souhait de votre direction.

## Posture A — Continuité portée par l'équipe opérationnelle

La personne qui opère reprend la maintenance courante de l'application logicielle (mise à jour du référentiel des catégories, ajustement des règles de nommage, suivi des évolutions WeBuy mineures). Holistika reste disponible sur une cadence trimestrielle pour la revue de gouvernance — nouvelles fonctionnalités, ajustements de seuil, support en cas de rupture inattendue. Cette posture est cohérente avec la continuité d'opération assurée par notre partenaire opérationnel sur le processus depuis octobre 2025.

## Posture B — Continuité portée par Holistika

Holistika porte la maintenance directement sur une cadence mensuelle, avec un engagement de service reformulé. Cette posture convient aux organisations qui préfèrent un fournisseur unique sur le triptyque conception-construction-exploitation.

## Tarification de la continuité

Le coût de la continuité, dans l'une ou l'autre posture, ne peut être fixé avant la phase de découverte. Il dépend de la profondeur des évolutions prévues sur les douze mois qui suivent la mise en service, et du périmètre exact de l'application logicielle livrée. Une fourchette indicative est intégrée à l'annexe commerciale, à révision après l'atelier de cadrage.

# Ce que nous proposons

Trois parcours, une même posture. Vous gardez le contrôle de la donnée, des accès WeBuy, et la validation de chaque demande.

| Variante | Posture | Périmètre | Durée indicative |
|:---|:---|:---|:---|
| **A — Cadrage** | Vous voulez une règle écrite avant tout outil. | Cahier des charges fonctionnel et plan de déploiement, livrés clés en main pour votre direction des systèmes d'information. | 3 à 4 semaines |
| **B — Prototype** *(recommandée)* | Vous voulez un outil tangible mesuré sur 4 demandes pilotes. | Cadrage A complet, prototype d'application logicielle, mesure de l'écart, transfert de maîtrise à la personne qui opère. | 7 à 9 semaines |
| **C — Industrialisation** | Vous visez un déploiement à plusieurs équipes après pilote. | Variante B complète, extension à un deuxième périmètre, cadre de gouvernance partagé. | 12 à 14 semaines |

La variante **B** est notre recommandation : elle livre une preuve mesurable en moins de deux mois, sans engager l'organisation au-delà de ce que le pilote justifie. Les variantes A et C couvrent les cas où la règle prime ou bien où le pilote est déjà acquis.

# Notre méthode

Cinq temps, structurés pour respecter le rythme de votre cycle d'achat et la disponibilité de la personne qui opère.

| Temps | Étape | Objectif |
|:---:|:---|:---|
| 1 | Découverte | Comprendre la maille opérationnelle : tableaux de catégories, exceptions, parties prenantes, points durs. |
| 2 | Cadrage | Écrire la règle d'automatisation en langage de gestion, validée par la personne qui opère. |
| 3 | Prototype | Construire une application logicielle légère qui reproduit la règle sur 4 demandes pilotes. |
| 4 | Mesure | Quantifier l'écart : temps gagné, anomalies évitées, conformité du libellé. |
| 5 | Transfert | Documenter, former, retirer notre présence sans dépendance résiduelle. |

Chaque temps se conclut sur une revue partagée. Aucun livrable ne progresse tant que le précédent n'est pas reconnu de votre côté.

# Calendrier prévisionnel

Sur la base de la semaine ouvrée française (35 heures) et du calendrier des jours fériés de l'année en cours.

| Variante | Démarrage | Livrable principal | Clôture cible |
|:---|:---|:---|:---|
| A | T+0 | Cahier des charges et plan de déploiement | T+4 semaines |
| B | T+0 | Prototype mesuré et transfert de maîtrise | T+9 semaines |
| C | T+0 | Périmètre étendu et cadre de gouvernance | T+14 semaines |

Le démarrage est conditionné à deux éléments : la signature du contrat-cadre et la mise à disposition d'un accès lecture sur WeBuy pour la phase de cadrage.

# Critères de réussite

Sept repères, mesurés conjointement. Quatre concernent l'engagement opérationnel ; trois portent l'engagement financier et opérationnel sur la prévention des litiges.

## Repères opérationnels

- **Temps de demande.** La durée moyenne de traitement d'une demande passe de la valeur de référence mesurée en semaine 1 à un seuil convenu, validé en semaine 2.
- **Conformité du libellé.** Les libellés générés respectent la règle de nommage par catégorie sans correction manuelle sur 90 % des demandes pilotes.
- **Autonomie opérationnelle.** La personne qui opère produit une demande complète sans assistance dans les 30 jours suivant le transfert.
- **Continuité.** Aucune dépendance de production sur Holistika passé la fin de la mission.

## Engagements sur la prévention des litiges

- **Taux de factures en litige (sans numéro de commande).** Cible : moins de 2 %, mesure mensuelle. C'est l'engagement que la solution porte.
- **Délai moyen de résolution d'un litige.** Cible : moins de cinq jours ouvrés, mesure mensuelle. C'est l'engagement que la solution porte.
- **Couverture du registre des bons de commande.** Cible : cent pour cent des demandes tracées, mesure hebdomadaire. C'est la couverture qui conditionne les deux précédents.

# Étapes suivantes

Trois actions à votre main, deux à la nôtre.

- **De votre côté.** Confirmer la variante retenue, désigner la personne qui valide chaque livrable, autoriser un accès lecture WeBuy pour la phase de cadrage.
- **De notre côté.** Remettre un contrat-cadre dans les cinq jours ouvrés et planifier l'atelier de lancement sous quinzaine.

Une fois ces points alignés, nous proposons un atelier de lancement de 90 minutes pour figer le périmètre, la cadence des revues, et les correspondants côté Holistika.

---

*Le calendrier commercial — variantes A, B, C avec tarification et conditions — fait l'objet d'un document distinct, transmis sur demande de votre référent achats.*
