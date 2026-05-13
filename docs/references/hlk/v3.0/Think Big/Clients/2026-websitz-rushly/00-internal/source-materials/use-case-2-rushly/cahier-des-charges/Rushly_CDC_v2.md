---
source: /Users/fay/cd/projects/nfq/ue-quickwins/supporting_docs/recordings/delete/Rushly_Cahier_des_charges_v2.docx
source_type: .docx
converted_at: 2026-04-08T02:12:30
title: "1. Présentation du projet"
---

R


| Rushly |
| --- |


Cahier des charges technique

SaaS de gestion, tri et montage vidéo par IA

pour marques e-commerce


| Version | 1.0 |
| --- | --- |
| Date | Mars 2026 |
| Statut | À développer |
| Client | Rushly |
| Document | Cahier des charges |



# 1. Présentation du projet



## 1.1 Contexte et vision


Rushly est un SaaS B2B destiné aux marques e-commerce et aux monteurs vidéo freelance. Le produit résout un problème central dans la production de contenu publicitaire vidéo : le temps perdu à trier, organiser et sélectionner les bons rushes avant de monter une pub.

Aujourd'hui, les équipes e-commerce passent des heures à fouiller dans des dossiers Google Drive désorganisés pour retrouver le bon clip. Rushly automatise ce travail grâce à l'IA et permet de produire plus de pubs, plus rapidement, avec moins de friction.


## 1.2 Positionnement


Rushly se positionne comme l'outil de production vidéo pour les marques e-commerce qui veulent scaler leur production de créas publicitaires sans exploser leur budget montage.

Concurrent principal de référence : ClipCrafter (clipcrafter.io) — Rushly se différencie par :

- Le découpage automatique de vidéos brutes en rushes classifiés

- La génération de montage depuis un script (IA)

- La fonctionnalité Clone de pub concurrente

- La recherche sémantique dans la médiathèque

- Un pricing plus accessible (Solo 69€/mois vs 81€ chez ClipCrafter)


## 1.3 Cibles utilisateurs



| Profil | Besoin principal | Plan cible |
| --- | --- | --- |
| Marque e-commerce solo | Organiser ses rushes, produire plus de pubs sans monteur à plein temps | Solo / Pro |
| Équipe e-commerce (2-5) | Collaboration monteurs + pipeline de production | Pro |
| Monteur vidéo freelance | Gérer plusieurs clients, brief clair, livraison rapide | Pro |
| Agence vidéo / performance | Volume de créas, multi-marques, reporting | Scaling |



# 2. Fonctionnalités détaillées



## 2.1 Tableau récapitulatif



| # | Fonctionnalité | Description | Priorité | Phase |
| --- | --- | --- | --- | --- |
| 1 | Import flexible | Vidéo brute, rush prêt, Google Drive, drag & drop, lien UGC | Critique | Phase 1 |
| 2 | Découpage + tri IA | Analyse, découpe et classifie chaque segment automatiquement | Critique | Phase 1 |
| 3 | Rush Library | Médiathèque avec miniatures, tags, filtres, prévisualisation | Critique | Phase 1 |
| 4 | Recherche sémantique | Recherche par description visuelle (OpenAI Embeddings) | Critique | Phase 1 |
| 5 | Brief scène par scène | Script lié aux rushes + instructions pour le monteur | Critique | Phase 2 |
| 6 | Script → montage IA | Génération automatique d'une séquence depuis un script | Haute | Phase 2 |
| 7 | Clone de pub concurrent | Analyse vidéo concurrente + matching avec rushes disponibles | Haute | Phase 2 |
| 8 | Kanban Production | Pipeline de suivi avec 6 colonnes de statut | Critique | Phase 1 |
| 9 | Collaboration équipe | Invitation, rôles, assignation, notifications | Haute | Phase 2 |
| 10 | Feedback frame par frame | Commentaires horodatés directement sur la vidéo | Haute | Phase 2 |
| 11 | Lien UGC créateurs | Upload externe sans compte Rushly | Moyenne | Phase 3 |
| 12 | Multi-projets / Workspaces | Un workspace par marque, médiathèque indépendante | Critique | Phase 1 |
| 13 | Templates de scripts | Scripts pré-faits par type de pub (unboxing, témoignage...) | Moyenne | Phase 3 |
| 14 | Stats de réutilisation | Quels rushes sont les plus utilisés dans les pubs | Moyenne | Phase 3 |
| 15 | Détection doublons | Signalement automatique des clips similaires | Moyenne | Phase 3 |



## 2.2 Détail des fonctionnalités critiques


Fonctionnalité 1 — Import flexible

L'utilisateur peut importer du contenu vidéo de plusieurs façons :

- Drag & drop depuis son ordinateur (formats MP4, MOV, AVI, MKV)

- Import depuis Google Drive (connexion OAuth)

- Lien partageable pour créateurs UGC externes (sans compte Rushly)

- Deux modes : vidéo brute longue (→ découpage IA) ou rush déjà prêt (→ import direct)

La vidéo est uploadée sur le stockage cloud (Cloudflare R2 ou AWS S3) avant traitement IA.

Fonctionnalité 2 — Découpage + tri IA automatique

C'est le cœur du produit. Le pipeline de traitement IA fonctionne en 5 étapes :

- Étape 1 — Transcription audio : OpenAI Whisper transcrit la totalité de la piste audio en texte horodaté

- Étape 2 — Analyse visuelle : GPT-4 Vision analyse les frames clés de la vidéo et détecte actions, produits, plans, émotions

- Étape 3 — Segmentation : l'IA identifie les points de découpe naturels (changements de plan, de sujet, de ton)

- Étape 4 — Classification : chaque segment est étiqueté (Hook / B-roll / Body / CTA / Show Problem / Unboxing / Témoignage + tags custom)

- Étape 5 — Génération embeddings : description textuelle de chaque clip pour la recherche sémantique

Coût estimé : 0,02€ à 0,10€ par vidéo analysée selon la durée.

Fonctionnalité 3 — Rush Library (médiathèque)

Interface principale de navigation dans les rushes :

- Grille de cartes vidéo avec miniature générée automatiquement

- Durée, tags colorés, badge 'IA' visibles sur chaque carte

- Sidebar avec dossiers par type (Hook, B-roll, CTA...) et tags custom

- Filtres multi-critères : type, date, durée, monteur

- Bouton play pour prévisualisation inline

- Vue liste ou grille (toggle)

Fonctionnalité 4 — Recherche sémantique

Barre de recherche intelligente à 3 niveaux :

- Niveau 1 — Par tag : clique sur 'B-roll' → tous les B-rolls

- Niveau 2 — Par mot-clé exact : filtre par nom de fichier ou tag

- Niveau 3 — Par description sémantique : tape 'plan rapproché mains produit' → l'IA trouve les clips correspondants visuellement

Technologie : OpenAI Embeddings — chaque clip a une description vectorisée, la recherche compare les vecteurs et retourne les clips les plus proches.

Fonctionnalité 5 — Brief scène par scène

Création d'un brief de production complet :

- Script importé ou saisi ligne par ligne

- Chaque ligne de script est liée manuellement ou automatiquement au rush correspondant

- Instructions visuelles et d'édition par scène

- Bouton 'Suggérer rushes' : l'IA propose les meilleurs clips pour chaque ligne

- Export du brief en PDF pour le monteur

- Onglets : Brief / Structure / Feedbacks / Créa finale

Fonctionnalité 6 — Script → montage IA automatique

Génération automatique d'une proposition de montage :

- L'utilisateur colle ou écrit son script

- Rushly analyse chaque ligne du script et son intention (Hook, B-roll, CTA...)

- L'IA cherche dans les rushes disponibles les clips les plus pertinents pour chaque scène

- Une séquence complète est proposée avec les clips sélectionnés

- Le monteur valide, remplace ou ajuste librement — l'IA est une assistance

Fonctionnalité 7 — Clone de pub concurrent

Reproduction d'une vidéo concurrente avec ses propres rushes :

- Étape 1 : l'utilisateur colle le lien de la vidéo concurrente (TikTok, Instagram, YouTube, Meta Ads Library)

- Étape 2 : Rushly télécharge et analyse la structure scène par scène

- Étape 3 : pour chaque scène détectée, l'IA cherche dans la médiathèque de l'utilisateur les rushes qui correspondent

- Étape 4 : un brief pré-rempli est généré avec la structure concurrente + les rushes suggérés

- Étape 5 : l'utilisateur valide ou remplace chaque suggestion, le brief est envoyé au monteur

Fonctionnalité 8 — Kanban Production

Pipeline visuel de suivi de toute la production :

- 6 colonnes : Briefs → Attente contenu → À éditer → Feedback → À lancer → Lancé

- Chaque carte = une vidéo avec monteur assigné, deadline, tags

- Filtres : par tag, par monteur, par deadline

- Modal de brief complet au clic sur une carte

- Drag & drop entre colonnes pour changer le statut


# 3. Stack technique recommandée


Vu que le développeur travaille en no-code / low-code, voici la stack recommandée :


| Outil | Rôle | Catégorie |
| --- | --- | --- |
| Bubble.io | Interface utilisateur, logique applicative, base de données, authentification | Frontend + Backend |
| Cloudflare R2 | Stockage vidéos et rushes (moins cher qu'AWS S3, CDN intégré) | Stockage cloud |
| OpenAI Whisper | Transcription audio des vidéos importées | IA — Audio |
| OpenAI GPT-4 Vision | Analyse visuelle des frames vidéo, classification des scènes | IA — Vision |
| OpenAI GPT-4o | Génération de scripts, analyse de structure, clone concurrent | IA — Texte |
| OpenAI Embeddings | Vectorisation des descriptions de clips pour recherche sémantique | IA — Recherche |
| FFmpeg (via api.video) | Découpage physique des vidéos en segments, génération miniatures | Traitement vidéo |
| Mux ou api.video | Streaming vidéo, lecteur intégré, génération de thumbnails | Vidéo player |
| Stripe | Paiements, abonnements récurrents, gestion des plans | Paiement |
| Make (Integromat) | Automatisations : pipeline IA au trigger upload, notifications | Automatisation |
| Resend ou Sendgrid | Emails transactionnels (invitation équipe, notifications) | Emails |
| Supabase (optionnel) | Base de données vectorielle pour les embeddings sémantiques | BDD vectorielle |



# 4. Structure de la base de données


Les Data Types à créer dans Bubble (ou base de données équivalente) :


## 4.1 Tables principales


User

- email, nom, avatar

- plan (Solo / Pro / Scaling)

- date_inscription, stripe_customer_id

Workspace

- nom, logo, couleur de marque

- owner (lien User)

- membres (liste de Users)

- storage_used (Go), storage_limit (Go)

Project

- nom, description

- workspace (lien Workspace)

- date_création

Rush (clip vidéo)

- fichier_url (lien Cloudflare R2)

- miniature_url, durée, taille

- type_tag (Hook / B-roll / CTA / etc.)

- tags_custom (liste de textes)

- description_ia (texte — pour recherche sémantique)

- embedding_vector (vecteur — pour recherche sémantique)

- trié_par_ia (booléen)

- project (lien Project)

- date_import

Brief

- titre, script_texte

- project (lien Project)

- monteur_assigné (lien User)

- statut (Briefs / Attente contenu / À éditer / Feedback / À lancer / Lancé)

- deadline (date)

- scènes (liste de Scene)

- date_création

Scene (ligne de brief)

- numéro_scène, texte_script

- rush_lié (lien Rush)

- instruction_visuelle, instruction_édition

- brief (lien Brief)

Feedback

- timecode (secondes)

- texte_commentaire

- auteur (lien User)

- brief (lien Brief)

- date_création


# 5. Pages et écrans à développer



| Page | Contenu principal | Phase |
| --- | --- | --- |
| Landing page | Page marketing publique (déjà développée) | Terminé |
| Inscription / Connexion | Auth email + Google OAuth | Phase 1 |
| Workspace (accueil) | Liste des projets avec statuts et compteur rushes | Phase 1 |
| Rush Library | Médiathèque avec grille, filtres, recherche sémantique | Phase 1 |
| Import | Drag & drop, Google Drive, lien UGC | Phase 1 |
| Kanban Production | Pipeline 6 colonnes avec cartes et drag & drop | Phase 1 |
| Dashboard | Stats, activité récente, métriques clés | Phase 1 |
| Brief (modal) | Script scène par scène + rushes liés + feedbacks | Phase 2 |
| Paramètres | Profil, équipe, plan, facturation Stripe | Phase 2 |
| Clone concurrent | Import lien + analyse + matching rushes | Phase 2 |
| Notifications | Centre de notifications in-app | Phase 3 |
| Editeur leger | Timeline rushes + voix off IA + sous-titres + export MP4 | Phase 3 |



# 6. Modèle tarifaire (exemple indicatif)


Important : Les prix ci-dessous sont donnés à titre d'exemple indicatif. Ils sont susceptibles d'évoluer avant le lancement officiel en fonction des coûts d'infrastructure, des retours utilisateurs et du positionnement marché final.


| Plan | Mensuel (indicatif) | Annuel/mois (ind.) | Limites principales |
| --- | --- | --- | --- |
| Solo | ~69€ | ~42€ | 50 Go · 1 monteur · 1 workspace |
| Pro | ~89€ | ~63€ | 200 Go · 5 monteurs · 3 workspaces + montage IA + clone concurrent |
| Scaling | ~149€ | ~105€ | 500 Go · illimités · onboarding personnalisé |


3 cycles de facturation disponibles : mensuel / trimestriel (-15%) / annuel (-30%). Gestion via Stripe Billing + webhooks.

Essai gratuit 14 jours sur tous les plans. Aucune carte requise à l'inscription.

Les prix définitifs seront fixés après validation du MVP et analyse des coûts réels d'infrastructure IA.


# 7. Editeur leger — Assemblage de rushes



## 7.1 Description generale


Rushly integre un editeur leger permettant d'assembler les rushes selectionnés, d'ajouter une voix off IA et des sous-titres automatiques, directement dans l'application. Ce n'est pas un editeur professionnel — c'est un outil d'assemblage rapide qui produit une video de travail prete a valider ou affiner dans un logiciel de montage classique.


## 7.2 Fonctionnalites de l'editeur


Timeline d'assemblage

- Affichage des rushes selectionnes dans le brief, dans l'ordre des scenes

- Drag & drop pour reordonner les clips sur la timeline

- Previsualisation de chaque clip avant integration

- Decoupe simple : point d'entree et de sortie par clip (trim basique)

- Script affiche en reference a cote de la timeline

Voix off IA

- Saisie ou import du texte de voix off (depuis le script existant)

- Choix d'une voix parmi une selection (hommes / femmes, accents)

- Generation de la voix off via ElevenLabs ou OpenAI TTS

- Synchronisation automatique avec la timeline

- Possibilite d'uploader sa propre voix off enregistree

Sous-titres automatiques

- Generation automatique depuis la transcription Whisper ou le script

- Choix du style : position, police, couleur, taille

- Affichage word-by-word (mot par mot) ou par phrase

- Previsualisation des sous-titres sur la video en temps reel

- Export avec sous-titres incrustés (hardcoded) ou fichier SRT separe

Export final

- Rendu de la video assemblee en MP4 via Creatomate API

- Resolutions disponibles : 9:16 (TikTok/Reels), 1:1 (carre), 16:9 (YouTube)

- Qualite export : HD 1080p par defaut

- Notification quand le rendu est pret (1-3 minutes selon duree)

- Video disponible en telechargement direct depuis la plateforme


## 7.3 Stack technique pour l'editeur



| Outil | Role | Categorie |
| --- | --- | --- |
| Creatomate | Assemblage video, incrustation sous-titres, rendu MP4 final via API | Rendu video |
| ElevenLabs | Generation de voix off IA avec choix de voix realistes | Voix off IA |
| OpenAI TTS | Alternative moins chere a ElevenLabs pour la voix off | Voix off IA |
| OpenAI Whisper | Transcription pour generation automatique des sous-titres | Sous-titres |
| Mux / api.video | Streaming et previsualisation des rushes dans l'editeur | Player video |



## 7.4 Limites de l'editeur


L'editeur Rushly N'EST PAS un outil de montage professionnel. Il ne remplace pas Premiere Pro, DaVinci ou CapCut pour un montage fin. Son objectif est de produire une video de travail rapidement assemblee.

Ce que l'editeur NE fait PAS :

- Pas de transitions complexes entre clips

- Pas d'effets visuels ou de filtres

- Pas d'ajout de musique de fond (prevu en version future)

- Pas de multi-piste audio complexe

- Pas d'animations de texte avancees


# 8. Contraintes et exigences techniques



## 8.1 Performance


- Temps de traitement IA : < 60 secondes pour une vidéo de 2 minutes

- Chargement de la Rush Library : < 2 secondes

- Lecture vidéo inline : démarrage < 1 seconde (streaming HLS)

- Recherche sémantique : résultats < 500ms


## 8.2 Sécurité


- Authentification JWT + refresh tokens

- Isolation des données par workspace (aucune fuite entre clients)

- Vidéos stockées avec URLs signées (accès temporaire, non-publiques)

- Conformité RGPD : consentement, droit à l'effacement, stockage EU


## 8.3 Scalabilité


- Architecture asynchrone pour le traitement IA (file d'attente)

- Stockage cloud scalable (Cloudflare R2 sans limite)

- Rate limiting sur les appels API OpenAI


## 8.4 Formats acceptés


- Vidéo : MP4, MOV, AVI, MKV, WebM

- Taille max par fichier : 4 Go

- Résolution : jusqu'à 4K

- Audio : MP3, WAV, M4A (pour import de rushes audio)


# 9. Livrables attendus



## 9.1 Livrables Phase 1 — MVP


- Application Bubble fonctionnelle en production

- Pipeline IA opérationnel (import → tri → library)

- Stripe connecté avec les 3 plans

- URL de production + domaine custom

- Documentation technique des workflows Bubble


## 9.2 Livrables Phase 2 — Features avancees


- Toutes les features différenciantes fonctionnelles

- Tests utilisateurs réalisés avec 5 bêta-testeurs

- Rapport de bugs et corrections


## 9.3 Livrables Phase 3 — Version complete


- Application complète v1.0 prête au lancement public

- Guide d'utilisation pour les utilisateurs finaux

- Monitoring et alertes configurés


# 10. Informations complémentaires



## 10.1 Ressources disponibles


- Landing page déjà en production sur Vercel (index.html fourni)

- Maquettes UI complètes de tous les écrans (réalisées avec Claude)

- Liste des fonctionnalités validée et priorisée (ce document)

- Accès aux wireframes interactifs sur demande


## 10.2 Références


- Concurrent principal : clipcrafter.io (analyser l'interface et les fonctionnalités)

- Inspiration UX : Notion, Linear, Loom

- Palette de couleurs : orange #E85D24, vert #1D9E75, violet #7F77DD

- Typographies : Syne (titres) + Inter (corps)


## 10.3 Questions ouvertes à clarifier


- Choix entre Bubble.io pur ou Bubble + backend Node.js pour le traitement IA lourd

- Budget mensuel maximum pour les APIs OpenAI (estimation : 50-200€/mois selon le volume)

- Hébergement des vidéos : Cloudflare R2 (recommandé) ou AWS S3

- Langue de l'interface : français uniquement ou multilingue dès le départ

Document préparé avec Rushly · Version 1.0 · Mars 2026