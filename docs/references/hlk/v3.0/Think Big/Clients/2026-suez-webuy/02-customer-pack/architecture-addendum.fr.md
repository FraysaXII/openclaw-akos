---
language: fr
status: draft
audience: customer
register: external
program_id: ENG-SUEZ-WEBUY-2026
engagement_slug: 2026-suez-webuy
artifact_role: customer-deliverable
intellectual_kind: architecture_addendum
brand_voice_register: peer_consulting
brand_pricing: excluded
brand_pricing_companion: tarification.customer.fr.md
collaboration_partner: EFA Académie
collaboration_since: 2025-10
mission_posture: Mission portée conjointement
target_pages: 2
target_send_date: 2026-05-27
render_target: pdf
linked_canonicals:
  - proposal.customer.fr.md
  - tarification.customer.fr.md
  - cdc-feasibility-shape.fr.md
last_review: 2026-05-25
---

<p class="lead">Cette addenda complète la <em>Proposition d'engagement</em> en précisant l'architecture en trois temps, le rôle de continuité tenu par notre opératrice partenaire, et la réplicabilité de la mécanique au-delà de ce premier périmètre. Deux pages, lisibles en cinq minutes, pour aligner les décisions techniques et organisationnelles.</p>

# Phase 1 — Générateur de libellés Power Query (livrable sous quinze jours)

Le premier livrable est un classeur Microsoft Excel adossé à Power Query. À partir d'un numéro d'engin, d'une catégorie et d'un devis fournisseur, l'outil compose **déterministiquement** la chaîne en cinq composants conforme à votre nomenclature WeBuy : `<préfixe-engin>_<catégorie>_<sous-catégorie>_<référence-devis>_<période>`.

Les règles de mappage sont consignées dans une feuille de référence éditable par votre office méthode — la mécanique se modifie sans intervention logicielle. Les six familles d'engagement (**CAPEX, maintenance, pneus, fournitures, transport, location**) sont couvertes dès la livraison. Une feuille de **validation** signale toute combinaison qui ne reconstitue pas un libellé valide.

**Surface ERP attendue :** intégration en tant que **macro Power Query** dans votre environnement Excel existant. Aucun déploiement serveur ni licence supplémentaire pour cette phase.

# Phase 2 — Application web légère Power Platform multi-catégories

La seconde phase déplace la mécanique du classeur Excel vers une **application Power Apps** adossée à SharePoint Lists, avec des automatismes Power Automate pour l'extraction des devis reçus par mail et la pré-composition des demandes d'achat. Cinq fonctionnalités prioritaires émergent du périmètre que vous nous avez décrit :

1. **Composition assistée des libellés** — généralisation de la phase 1 au flux quotidien.
2. **Mappage catégorie ↔ compte comptable** — déterministe, contrôlé, traçable.
3. **Extraction email → demande structurée** — module Power Automate qui transforme un devis fournisseur reçu par mail en projet de demande pré-rempli.
4. **Registre de prévention et gestion des litiges** — capture des écarts facture/devis/réception avec relance automatisée et historisation.
5. **Tableau de bord d'usage mensuel** — auto-généré par catégorie, fournisseur, engin et centre de coût.

**Surface ERP attendue :** application Power Apps accessible depuis l'environnement Microsoft de vos opérateurs WeBuy, avec **tableaux de bord opérateur** (votre vision quotidienne) **et tableaux de bord client/superviseur** (vision agrégée pour la direction approvisionnement).

# Phase 3 — Étude de faisabilité intégration WeBuy + reporting Power BI

La troisième phase est une **étude de faisabilité** — pas un développement engagé. Elle évalue, sur la base des deux premières phases en production :

- L'**intégration native** avec votre portail WeBuy (API, connecteur Power Platform, ou export-import batch selon ce que votre DSI valide).
- Une **couche de reporting Power BI** sur l'usage mensuel, branchée sur les données accumulées en phase 2 — visualisation des dérives, identification des fournisseurs à risque, prévision des engagements à venir.
- La **jointure avec votre ERP comptable** pour la réconciliation post-réception (jointure ERP-flux-de-travail).

La décision de poursuivre est entièrement à votre main au terme de la phase 2 — l'addenda ne précompte aucun engagement au-delà.

---

# Continuité opérationnelle après mise en service

Le risque principal d'un livrable de cette nature n'est pas technique mais **organisationnel** : que la mécanique vive trois mois après notre transfert puis dérive faute de propriétaire identifié. Notre proposition adresse ce risque par construction.

Notre **opératrice partenaire en continuité** — celle qui opère aujourd'hui votre processus WeBuy au quotidien et qui a participé à la conception de la mécanique — assure la maintenance, la formation des nouveaux opérateurs et l'évolution des règles de mappage après notre transfert. Elle reste votre interlocutrice de continuité, avec un **niveau d'accès restreint** aux seuls périmètres de la mission (les règles de mappage, le générateur, les tableaux de bord d'usage — pas les données comptables sensibles).

Cette continuité est la **clé de la pérennité** : sans elle, le livrable risque de devenir un actif orphelin. Avec elle, votre office méthode hérite d'un outil vivant.

# Réplicabilité à l'échelle de votre office CTO

Au-delà du processus WeBuy, l'architecture est **délibérément réplicable**. La mécanique en trois phases — règle déterministe en Power Query, application Power Platform, étude de faisabilité ERP — se transpose telle quelle à d'autres processus d'approvisionnement de votre office CTO :

- la gestion des contrats de location longue-durée ;
- la consolidation des demandes inter-établissements ;
- le suivi d'engagement budgétaire par projet ou par centre de coût ;
- toute mécanique récurrente où la friction provient d'une **répétition de calcul déterministe** plutôt que d'un arbitrage humain.

L'investissement consenti pour ce premier périmètre est donc **capitalisable** : votre office acquiert une compétence interne sur la chaîne Power Platform + une bibliothèque de patterns réutilisables. Le second processus coûte moins que le premier, et le troisième encore moins.

---

# Trois surfaces de gouvernance ERP

L'addenda repose sur une lecture systématique de la gouvernance des engagements (architecture conçue pour scaler sans dérive de périmètre) qui distingue **trois surfaces** :

1. **Tableau de bord opérateur** — votre vision quotidienne sur les demandes en cours, les libellés générés, les écarts détectés, les litiges ouverts. C'est l'écran que voient vos opérateurs WeBuy à la prise de service.

2. **Tableau de bord client/superviseur** — vision agrégée pour votre direction approvisionnement (volumes mensuels, taux de litige, top fournisseurs, dérive éventuelle des libellés). C'est l'écran qui se consulte une fois par semaine et qui se présente en revue mensuelle.

3. **Jointure flux de travail ERP** — l'intégration avec votre portail WeBuy + votre ERP comptable, qui matérialise la réconciliation automatique des engagements et des facturations.

Les trois surfaces sont **conçues ensemble** dès la phase 1 (même si la phase 1 ne livre que la mécanique de composition de libellés sous Excel + Power Query) — c'est ce qui permet de **prévenir la dérive de périmètre** lors du passage en phase 2 et en phase 3.

---

*Document de référence : `proposal.customer.fr.md` (proposition d'engagement complète) et `tarification.customer.fr.md` (calendrier commercial Variantes A, B, C).*

*Mission portée conjointement par Holistika Research et EFA Académie.*
