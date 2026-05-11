---
status: draft
classification: external
access_level: 4
language: fr
register: external
audience: customer-enterprise
artifact_kind: cdc_feasibility_shape
engagement_slug: 2026-suez-webuy
counterparty_org_ref: GOI-CUS-SUEZ-2026
linked_engagement: 2026-05-10-suez-webuy-procure-to-pay
governance:
  - SOP-ENG_PROPOSAL_001
  - SOP-ENG_DISCOVERY_QUESTIONNAIRE_001
  - SOP-ENG_ESTIMATION_DISCIPLINE_001
  - BRAND_FRENCH_PATTERNS
last_review: 2026-05-10
---

# Cahier des charges — décomposition fonctionnelle du processus de demande d'achat WeBuy

> **Objet —** lecture point-par-point du processus actuel de passage de commandes WeBuy, structurée en livrables fonctionnels, telle qu'elle servira de base de travail pour le cahier des charges détaillé que [entité juridique du donneur d'ordre] souhaite construire.
>
> **Source —** mode opératoire « Process de passage de commandes WeBuy » version transmise le 2026-05. Aucune information confidentielle de [entité juridique du donneur d'ordre] n'est reproduite ici. Les références à des codes parc, codes types d'intervention, ou exemples de devis sont conservées en tant qu'illustrations méthodologiques.
>
> **Niveau de détail —** les blocs ci-dessous décrivent **ce que l'utilisateur fait, ce que le système attend, et ce que le système doit retourner**. Chaque fonctionnalité porte un drapeau d'éligibilité à l'automatisation : `actionnable`, `nécessite accès à l'application X`, ou `manuel uniquement (opérationnel)`.

## 0. Cadre commun — préambule applicable à toutes les catégories

Toutes les demandes d'achat, indépendamment de la catégorie (CAPEX, maintenance, pneus, fourniture de pièces, transport, location), partagent une enveloppe commune que nous décomposons une seule fois.

| Élément | Valeur attendue | Variabilité |
|:---|:---|:---|
| Centre de profit | `7MA2 – MM_ Engins` | Constante toutes catégories |
| Ressource / Ordre interne | `202 - Engins` | Constante toutes catégories |
| Code parc engin | Identifiant d'un engin du parc | Variable par demande |
| Centre de coût (code métier) | Issu du parc engins (par exemple `Z-XXXX – LMM`) | Variable par engin |
| Adresse de livraison | Site de livraison | Variable par catégorie : `SUEZ RV MATERIEL & LOGISTIQUE (BRETIGNY)` pour maintenance / pneus / transport / location ; site spécifique pour CAPEX et fournitures |
| Pièce jointe | Document du fournisseur (devis, facture, demande CAPEX) | Une au minimum |
| Compte comptable | Variable selon la catégorie (cf. tableau §6) | Mappage déterministe |
| Libellé | Construit selon une règle de nommage par catégorie | Génératif |

**Drapeau —** ce préambule est `actionnable` : une application logicielle peut générer la majorité de ces champs à partir d'un contexte minimal (numéro d'engin + catégorie + numéro de devis fournisseur + intentions du demandeur).

## 1. Workflow général — du déclenchement à la soumission

### F-01 — Déclenchement de la demande par e-mail

**Ce qui se passe.** Le demandeur (responsable d'intervention, gestionnaire de planification, responsable du service Engins TP) envoie un e-mail à l'opérateur de demande d'achat avec les informations nécessaires : numéro de parc, code métier, numéro de devis fournisseur, code type d'intervention.

**Ce que doit retourner le système cible.** Une instance de demande pré-remplie avec le contexte e-mail extrait, prête à être validée par l'opérateur.

**Drapeau.** `actionnable` — l'extraction structurée d'un e-mail vers un objet de demande d'achat est un cas d'usage standard ; un classifieur léger suffit pour identifier la catégorie et extraire les entités (numéro de parc, devis, code).

### F-02 — Recherche de l'article dans le portail

**Ce qui se passe.** L'utilisateur clique sur `Articles` puis `Rechercher des produits` dans la barre de recherche WeBuy. Une page de catégorisation s'affiche avec des encadrés à cocher.

**Ce que doit retourner le système cible.** Le bon article-source de la catégorie demandée, sans navigation manuelle. Pour la maintenance, l'article est constant (« Engins de chantier (Hors full services) – Maintenance et service – Autre »). Pour le CAPEX et la fourniture de pièces, l'article dépend du type d'engin (chargeur sur chenilles, pelle sur pneus, etc.).

**Drapeau.** `nécessite accès à l'application WeBuy` pour exécuter la sélection ; `actionnable` pour le calcul de l'article cible à partir du contexte de l'engin.

### F-03 — Sélection de l'article et ajout au panier

**Ce qui se passe.** L'utilisateur clique sur `Ajouter au panier` puis sur `Valider le panier`. Pour certaines catégories (CAPEX, location), une fenêtre supplémentaire demande des paramètres : tonnage, engagement horaire mensuel.

**Ce que doit retourner le système cible.** Un panier validé avec un identifiant de demande d'achat généré automatiquement par WeBuy (format `REQXXXXXXXX`).

**Drapeau.** `nécessite accès à l'application WeBuy`. La logique métier en amont (« quel tonnage, quel engagement, quelle pelle ») peut être pré-calculée par une application logicielle ; la pose dans le panier reste une action de portail.

### F-04 — Génération du numéro de demande

**Ce qui se passe.** WeBuy génère un identifiant `REQXXXXXXXX` à la validation du panier. L'opérateur ne saisit pas ce numéro ; il le récupère pour la suite du processus.

**Ce que doit retourner le système cible.** Le numéro de demande, capté et stocké dans le registre interne.

**Drapeau.** `nécessite accès à l'application WeBuy` pour la lecture ; `actionnable` pour le stockage et l'indexation côté processus.

## 2. Renseignement de la demande — bloc « orienté approvisionnement [entité juridique du donneur d'ordre] »

### F-05 — Construction du libellé selon la règle de nommage

**Ce qui se passe.** Le libellé doit suivre une règle de nommage spécifique à la catégorie. Pour la maintenance, les pneus, la fourniture, le transport et la location :

1. Initiales du demandeur,
2. Numéro de parc de l'engin,
3. Code type d'intervention,
4. Nom du fournisseur,
5. Numéro de devis ou de facture.

Pour la catégorie CAPEX, la règle est différente :

1. Initiales du demandeur,
2. Numéro de parc de l'engin,
3. Copier-coller de l'objet de l'e-mail de la demande CAPEX.

**Ce que doit retourner le système cible.** Un libellé entièrement formé à partir des entités extraites en F-01.

**Drapeau.** `actionnable` — c'est précisément le type de génération que la collaboratrice de [entité juridique du donneur d'ordre] décrit comme « la partie la plus consommatrice de temps » dans le processus actuel. Une fonction génératrice par catégorie suffit.

### F-06 — Renseignement du centre de profit

**Ce qui se passe.** L'utilisateur sélectionne `7MA2 – MM_ Engins` dans la liste déroulante du centre de profit.

**Ce que doit retourner le système cible.** La valeur est constante ; elle peut être pré-remplie sans input.

**Drapeau.** `actionnable` — pré-remplissage déterministe.

### F-07 — Renseignement de l'adresse de livraison

**Ce qui se passe.** Pour la maintenance, les pneus, le transport et la location : adresse fixe `SUEZ RV MATERIEL & LOGISTIQUE (BRETIGNY)`. Pour la fourniture de pièces et le CAPEX : site spécifique du chantier ou de l'engin.

**Ce que doit retourner le système cible.** Pour la première classe : pré-remplissage. Pour la seconde : sélection à partir du parc engins (lookup déterministe).

**Drapeau.** `actionnable` — déterministe avec un référentiel de sites.

### F-08 — Renseignement du centre de coût

**Ce qui se passe.** L'utilisateur identifie le code métier de l'engin via le parc engins (par exemple `Z-XXXX – LMM`). C'est un lookup manuel actuellement.

**Ce que doit retourner le système cible.** Le code métier déduit automatiquement du numéro de parc.

**Drapeau.** `actionnable` — lookup en table.

### F-09 — Renseignement de la demande d'investissement (CAPEX uniquement)

**Ce qui se passe.** Pour les commandes CAPEX, l'opérateur doit envoyer le numéro de la D.I. à la responsable de la comptabilité, qui ouvre une `eOTP` ; cette eOTP n'est disponible qu'à `J+1`. L'opérateur attend le retour avant de poursuivre.

**Ce que doit retourner le système cible.** Une étape de workflow asynchrone : la demande passe en attente, l'eOTP est récupérée, la suite du processus reprend automatiquement à la réception.

**Drapeau.** `manuel uniquement (opérationnel)` pour l'instant — l'interface comptable n'est pas un service intégrable simplement. Une fois l'eOTP saisie en retour d'e-mail, la machine reprend la main.

### F-10 — Cases obligatoires (CAPEX uniquement)

**Ce qui se passe.** L'utilisateur coche les cases « DA 2M » et « Sans envoi du bon de commande ».

**Ce que doit retourner le système cible.** Pré-remplissage des cases pour les demandes CAPEX.

**Drapeau.** `actionnable` — règle déterministe par catégorie.

### F-11 — Ajout des commentaires et de la pièce jointe

**Ce qui se passe.** L'utilisateur ajoute le numéro de la D.I. et sa précision dans la zone commentaires (CAPEX), et joint la pièce attendue (devis, facture, courrier).

**Ce que doit retourner le système cible.** Un attachement de pièce jointe automatisé à partir de l'e-mail entrant + une zone commentaires pré-remplie.

**Drapeau.** `nécessite accès à l'application WeBuy` pour l'attachement final ; `actionnable` pour le pré-remplissage du texte.

## 3. Détail de l'article — bloc « orienté fournisseur »

### F-12 — Modification du libellé d'article

**Ce qui se passe.** L'utilisateur clique sur l'icône crayon, supprime le libellé par défaut (le nom de la catégorie), et saisit le numéro de devis fournisseur en y ajoutant le code type d'intervention. Pour la catégorie CAPEX, le libellé est différent : le nom de la catégorie est conservé.

**Ce que doit retourner le système cible.** Le libellé construit selon la règle de chaque catégorie.

**Drapeau.** `actionnable` — règle déterministe.

### F-13 — Renseignement de la date de livraison

**Ce qui se passe.** Pour la maintenance, les pneus, la fourniture, le transport et la location : date du lendemain. Pour le CAPEX : fin de l'année du délai (champ libre).

**Ce que doit retourner le système cible.** Pré-remplissage par catégorie.

**Drapeau.** `actionnable` — déterministe.

### F-14 — Renseignement du prix unitaire hors taxe

**Ce qui se passe.** Le prix unitaire HT est saisi à partir du devis fournisseur joint à la demande.

**Ce que doit retourner le système cible.** Extraction du prix HT depuis le devis (PDF ou e-mail) ; suggestion à l'opérateur pour validation.

**Drapeau.** `actionnable` — extraction structurée d'un document fournisseur ; un classifieur léger suffit pour la majorité des formats.

### F-15 — Sélection du fournisseur (SIREN / SIRET / contact)

**Ce qui se passe.** L'utilisateur sélectionne dans des menus déroulants successifs le SIREN du fournisseur, l'établissement (SIRET), puis le contact (e-mail destinataire). Un document de référence fournisseur est fourni au moment de l'engagement initial.

**Ce que doit retourner le système cible.** Une suggestion fournie automatiquement à partir du devis et du référentiel fournisseur ; sélection en un clic à partir d'une liste pré-filtrée.

**Drapeau.** `actionnable` pour la suggestion ; `nécessite accès à l'application WeBuy` pour la sélection effective dans les menus déroulants.

### F-16 — Commentaire fournisseur

**Ce qui se passe.** Selon la catégorie, l'opérateur ajoute un libellé fonctionnel (`Resserrage raccords`, `Remplacement 4 pneus – ENG6072`, `Transfert ENG5846 TORCY → KLEBER 21`, `Location relai ET1820 – Décembre 2025`). C'est un texte libre orienté fournisseur.

**Ce que doit retourner le système cible.** Une suggestion de libellé construite à partir du contexte de la demande (catégorie + engin + paramètres spécifiques) ; validation rapide par l'opérateur.

**Drapeau.** `actionnable` — la pré-suggestion réduit l'effort cognitif sans dépouiller l'opérateur de son contrôle.

### F-17 — Ajout de la pièce jointe orientée fournisseur

**Ce qui se passe.** Le devis ou document du fournisseur est attaché à la section « pièce jointe » de l'article.

**Ce que doit retourner le système cible.** Pièce attachée automatiquement à partir de l'e-mail entrant.

**Drapeau.** `nécessite accès à l'application WeBuy` pour l'attachement final.

### F-18 — Sélection du compte comptable

**Ce qui se passe.** Le compte comptable est variable selon la catégorie :

| Catégorie | Compte comptable attendu |
|:---|:---|
| CAPEX | `IMMO EN COURS TECH IMMOB CORPORELLES` |
| Maintenance (PMR, PMC, PMS, PMV, FSC, FSR) | `Entretien et réparations véhicules` |
| Pneus | `Pneus et chambres` |
| Fourniture de pièces (PMF) | `Petit matériel et outillage` |
| Transport (FST, PMT) | `Sous-traitance transport amont` |
| Location (PML, FSL) | `Location matériels <6 mois` |

**Ce que doit retourner le système cible.** Mappage déterministe `catégorie → compte` ; pré-remplissage automatique.

**Drapeau.** `actionnable` — table de correspondance.

### F-19 — Sélection de la ressource / ordre interne

**Ce qui se passe.** L'utilisateur sélectionne `202 - Engins` dans la liste déroulante.

**Ce que doit retourner le système cible.** Pré-remplissage constant.

**Drapeau.** `actionnable` — déterministe.

### F-20 — Sélection du code parc

**Ce qui se passe.** L'utilisateur sélectionne l'engin concerné par la demande dans la liste déroulante.

**Ce que doit retourner le système cible.** Pré-remplissage à partir du contexte de l'e-mail entrant (le numéro de parc est extrait dès F-01).

**Drapeau.** `actionnable` pour la suggestion ; `nécessite accès à l'application WeBuy` pour la sélection effective.

### F-21 — Vérification du montant HT (location uniquement)

**Ce qui se passe.** Pour la catégorie location, le montant HT renseigné en section 1 doit s'afficher automatiquement en section 4. Sinon, l'opérateur le saisit manuellement.

**Ce que doit retourner le système cible.** Une vérification automatique de cohérence ; alerte si le report n'est pas fait.

**Drapeau.** `actionnable` — règle de cohérence simple.

### F-22 — Soumission à validation

**Ce qui se passe.** L'utilisateur clique sur `Enregistrer et fermer` puis sur `Soumettre à validation`. La demande passe ensuite dans le circuit de validation interne (hors périmètre du processus opérateur).

**Ce que doit retourner le système cible.** Soumission de la demande, capture de l'identifiant final, archivage local.

**Drapeau.** `nécessite accès à l'application WeBuy`.

## 4. Suivi et reporting — bloc actuellement manuel

### F-23 — Suivi de la demande

**Ce qui se passe.** Une fois la demande soumise, l'opérateur suit les retours (validation, rejet, demande de précision) par e-mail.

**Ce que doit retourner le système cible.** Un tableau de bord interne reflétant le statut de chaque demande ; relances automatisées.

**Drapeau.** `actionnable` pour le tableau de bord et les relances ; `nécessite accès à l'application WeBuy` pour la lecture du statut côté portail.

### F-24 — Reporting mensuel

**Ce qui se passe.** Aucun reporting automatisé n'existe actuellement. La collaboratrice qui opère le processus produit un point manuel sur demande.

**Ce que doit retourner le système cible.** Un rapport mensuel auto-généré : nombre de demandes par catégorie, par fournisseur, par engin, par centre de coût ; alertes (volume anormal, dérives, doublons).

**Drapeau.** `actionnable` — c'est un cas d'usage classique de tableau de bord opérationnel et le souhait explicite formulé dans le brief initial.

## 5. Récapitulatif — codes types d'intervention

Les douze codes types d'intervention identifiés dans le mode opératoire structurent l'ensemble des demandes. Ils servent de clé de routage primaire :

| Catégorie de demande | Code | Définition | Cas d'utilisation |
|:---|:---:|:---|:---|
| CAPEX | `CAP` | Capex (investissement) | Achat d'un nouvel engin |
| Maintenance | `PMR` | Plan de Maintenance Réparation | Réparation sur engins en gestion PM |
| Maintenance | `PMC` | Plan de Maintenance Casse | Casse sur engins en gestion PM |
| Maintenance | `PMS` | Plan de Maintenance Stationnement | Entretien |
| Maintenance | `PMV` | Plan de Maintenance Vérification | VGP sur engins en gestion PM |
| Maintenance | `FSC` | Full Service Casse | Casse sur engins en gestion FS |
| Maintenance | `FSR` | Full Service Réparation | Réparation sur engins en gestion FS |
| Fournitures | `PMF` | Plan de Maintenance Fournitures | Fourniture de pièces pour un engin en gestion PM |
| Transport | `FST` | Full Service Transport | Transport d'un engin en gestion FS |
| Transport | `PMT` | Plan de Maintenance Transport | Transport d'un engin en gestion PM |
| Location | `PML` | Plan de Maintenance Location | Location d'un engin pour remplacer un engin en gestion PM |
| Location | `FSL` | Full Service Location | Location d'un engin pour remplacer un engin en gestion FS |

**Drapeau.** `actionnable` — ce tableau alimente directement la classification automatique en F-01.

## 6. Synthèse — répartition des fonctionnalités par drapeau d'éligibilité

| Drapeau | Fonctionnalités concernées | Nombre |
|:---|:---|---:|
| `actionnable` (génération, calcul, mapping, extraction, suggestion) | F-01, F-04 (capture), F-05, F-06, F-07, F-08, F-10, F-11 (texte), F-12, F-13, F-14, F-15 (suggestion), F-16, F-18, F-19, F-20 (suggestion), F-21, F-23 (tableau de bord), F-24 | 19 |
| `nécessite accès à l'application WeBuy` (interaction effective avec le portail) | F-02, F-03, F-04 (lecture), F-11 (attachement), F-15 (sélection), F-17, F-20 (sélection), F-22, F-23 (lecture statut) | 9 |
| `manuel uniquement (opérationnel)` (interface tierce non intégrée) | F-09 (échange comptabilité pour eOTP) | 1 |

> **Lecture commerciale —** la grande majorité du processus est génératif ou déterministe (catégorie `actionnable`). Une part minoritaire mais incompressible nécessite de poser des actions effectives dans le portail. Une seule étape (F-09, échange e-mail avec la comptabilité pour l'eOTP) reste à ce stade purement opérationnelle. C'est dans cette répartition que se loge l'opportunité d'allègement substantiel pour la collaboratrice qui opère le processus.

## 7. Pré-conditions à la conception détaillée

Pour passer de cette lecture fonctionnelle à un cahier des charges contractualisable, trois précisions sont attendues de [entité juridique du donneur d'ordre] (et apparaissent dans le questionnaire de cadrage) :

1. **Le statut de l'accès au portail WeBuy** — un compte de service dédié, un accès délégué, ou aucun accès (auquel cas le périmètre se limite aux étapes `actionnable` et la collaboratrice conserve les actions portail).
2. **L'environnement informatique du donneur d'ordre** — Microsoft Azure est mentionné dans le brief initial ; nous confirmerons les contraintes de conformité (DSI, sécurité, gestion des identités) avant la phase de prototypage.
3. **Le volume mensuel et la répartition par catégorie** — le brief évoque environ 750 véhicules en gestion, +200 en juin ; la répartition des demandes par catégorie (CAPEX vs maintenance vs location, etc.) ajustera la priorisation des fonctionnalités.

## 8. Hypothèses ouvertes — à valider lors du cadrage

- Tous les fournisseurs ont un référentiel SIREN / SIRET / contact stable et accessible ; sinon l'étape F-15 nécessite un sous-projet de constitution du référentiel.
- Les codes parc et codes métier sont accessibles en consultation depuis l'extérieur du portail ; sinon F-08 et F-20 nécessitent une copie locale du référentiel parc.
- Les e-mails entrants suivent un format suffisamment régulier pour permettre l'extraction automatique en F-01 ; sinon une phase de structuration du formulaire-source côté demandeur est à prévoir.
- L'eOTP en F-09 reste un échange manuel ; aucune intégration avec l'outil comptable n'est envisagée à ce stade.

## 9. Suite de la démarche

Cette lecture fonctionnelle alimente trois livrables successifs :

1. Un **cahier des charges détaillé** consolidant les vingt-quatre fonctionnalités ci-dessus avec leurs critères d'acceptation, leurs dépendances, et leur priorisation par valeur opérationnelle ressentie par la collaboratrice qui opère actuellement le processus.
2. Une **étude de faisabilité** par classe d'application, validant l'éligibilité des fonctionnalités `actionnable` et qualifiant les contraintes pour les fonctionnalités `nécessite accès à l'application`.
3. Un **prototype léger** (Excel / Power Query, Phase 1 du périmètre recommandé) couvrant les fonctionnalités les plus génératives (F-05, F-12, F-13, F-14, F-16, F-24) pour démonstration concrète avant industrialisation.

## 10. Documents associés

- Le **questionnaire de découverte** prolonge la lecture ci-dessus par des questions de cohérence à confirmer en séance.
- La **proposition d'engagement** structure la mission en huit sections cadrées.
- Le **support de présentation** offre une lecture synthétique en huit pages pour la séance commerciale.

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

---

*Document élaboré par Holistika sur la base du mode opératoire transmis. Aucune information confidentielle de [entité juridique du donneur d'ordre] n'est reproduite ; les exemples conservés (`ENG5846`, `ENG6072`, `BRO00000759`, etc.) sont des illustrations méthodologiques issues du document source. Validé pour discussion lors de la prochaine séance de cadrage.*
