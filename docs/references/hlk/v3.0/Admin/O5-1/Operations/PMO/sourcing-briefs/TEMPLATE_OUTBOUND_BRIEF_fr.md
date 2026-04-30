---
language: fr
status: stub
template_kind: outbound_brief
role_owner: PMO
area: Operations / PMO
entity: Holistika Research
authority: Founder + PMO
last_review: 2026-04-30
derived_from: docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_en.md
---

# Brief de mission — MODÈLE (français, version stub)

> **Note opérateur.** Ce fichier est l'**exercice de la chaîne de dérivation locale** — la première instance d'un sibling FR canonical né d'un sibling EN canonical (per [`SOP-HLK_LOCALISATION_001.md`](../../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md)). Statut `stub` jusqu'à ce qu'un premier livrable FR réel arrive et déclenche la promotion vers `active`. Les règles de ton FR définitives vivront dans [`BRAND_FRENCH_PATTERNS.md`](../../../Marketing/Brand/BRAND_FRENCH_PATTERNS.md) lorsque cette ressource sera promue de stub à canonique.
>
> **Voix actuelle (provisoire).** Vouvoiement par défaut ; ouverture `Bonjour [Prénom],` ; clôture `Cordialement,` ; signature `Holística Research`. Le ton suit les principes locale-agnostiques de `BRAND_VOICE_FOUNDATION.md` (peer-grade, jargon-free, spécifique).

---

## 1. Contexte

**Qui nous sommes.** Holística Research est une société espagnole d'ingénierie opérationnelle. Nous productivisons notre propre méthode sous la forme du SaaS KiRBe et de la plateforme agentic MADEIRA. Notre socle interne est gouverné par des centaines d'artefacts canoniques (registres de processus, validateurs, sondes de drift) ; la voix de marque est codifiée dans [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md).

**Pourquoi cette mission.** [TODO[OPERATOR-brief-context] — un paragraphe : pour quelle initiative, pourquoi maintenant, quel rôle joue le livrable]

**Documents de référence.** [Liste de 1 - 3 documents que le contractant doit lire avant de commencer]

## 2. Livrable

**Sortie concrète.** [TODO[OPERATOR-brief-deliverable] — une phrase]

**Format et nomenclature.** [Exigences de format ; ex. ".fig + export PNG/SVG ; noms `slide-NN-<descriptor>.svg`"]

**Quantité et granularité.** [Combien d'unités ; ce qui compte comme une unité]

**Hors périmètre.** [Ce que le brief n'inclut PAS explicitement]

## 3. Critères de qualité

Le livrable passe la revue d'acceptation uniquement quand TOUS les critères suivants sont remplis :

- **Conformité voix de marque.** Respecte [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md) et le fichier de patterns locale applicable.
- **Conformité spécification.** Correspond à la définition du livrable ci-dessus.
- **Critère qualité 1.** [TODO[OPERATOR-brief-quality-1]]
- **Critère qualité 2.** [TODO[OPERATOR-brief-quality-2]]
- **Critère qualité 3.** [TODO[OPERATOR-brief-quality-3]]

Une ronde de révisions est prévue si la première livraison ne passe pas un critère. Après la deuxième ronde, la mission se clôture (avec paiement des unités livrées) ou continue avec un périmètre renégocié.

## 4. Règles de voix de marque

Pour les livrables texte : suivre [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md) (EN) / [`BRAND_SPANISH_PATTERNS.md`](../../../Marketing/Brand/BRAND_SPANISH_PATTERNS.md) (ES) / [`BRAND_FRENCH_PATTERNS.md`](../../../Marketing/Brand/BRAND_FRENCH_PATTERNS.md) (FR — actuellement stub) selon la locale de la sortie.

Pour les livrables visuels : suivre [`BRAND_VISUAL_PATTERNS.md`](../../../Marketing/Brand/BRAND_VISUAL_PATTERNS.md). Les tokens (couleurs, typographie, espacement) ne sont pas négociables.

Pour tout livrable : les surfaces externes doivent passer le filtre de [`BRAND_JARGON_AUDIT.md`](../../../Marketing/Brand/BRAND_JARGON_AUDIT.md). Pas de noms de code internes dans une sortie destinée au client.

## 5. Calendrier et jalons

| Jalon | Date | Livrable | Côté opérateur |
|:------|:-----|:---------|:---------------|
| Kick-off | [TODO[OPERATOR-brief-kickoff-date]] | Brief signé ; documents de référence partagés | PMO confirme les accès |
| Mi-parcours | [TODO[OPERATOR-brief-midpoint-date]] | Brouillon / livraison partielle | PMO + Brand Manager revoient |
| Livraison | [TODO[OPERATOR-brief-delivery-date]] | Livrable complet | Début de la revue d'acceptation |
| Acceptation | sous 3 jours ouvrés après la Livraison | Validé / révisions / refus | Déclencheur de paiement |

Si le contractant anticipe un retard > 48h, il prévient par écrit immédiatement. Nous renégocions le périmètre ou prolongeons ; nous ne pénalisons pas les avis honnêtes en avance.

## 6. Conditions de paiement

**Tarif.** [TODO[OPERATOR-brief-rate]]

**Devise.** EUR (par défaut) ou [TODO[OPERATOR-brief-currency-alt] si autre devise convenue].

**Cadence.** 50 % à l'Acceptation, 50 % sous 30 jours après l'Acceptation, sauf si des paiements par jalon sont convenus en §5.

**Facturation.** Le contractant envoie une facture citant le `vendor_id` du brief (attribué au début de la mission) et les jalons couverts.

**Retard de paiement.** Si nous dépassons les 30 jours, nous ajoutons 1 % par semaine de retard au solde restant, appliqué automatiquement.

## 7. Normes de communication

**Canal principal.** Email (ou Direct DM si le `current_distance_band` du fournisseur dans `SOURCING_REGISTER.csv` est `N1`).

**SLA de réponse.** Nous répondons sous 1 jour ouvré pendant la mission. En dehors, best-effort.

**Asynchrone d'abord.** Pas d'appel synchrone sauf pour débloquer.

**Sans surprise.** Si quelque chose de matériel change, nous le remontons sous 24h.

## 8. Critères d'acceptation

La mission se clôture quand :

1. Le livrable passe tous les critères qualité de §3.
2. Le paiement final est exécuté selon §6.
3. Les deux parties confirment la clôture (un email d'une ligne suffit).

## 9. Références croisées

- [`SOURCING_REGISTER.csv`](../../../../../compliance/dimensions/SOURCING_REGISTER.csv)
- [`SOP-HLK_LOCALISATION_001.md`](../../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md)
- [`BRAND_FRENCH_PATTERNS.md`](../../../Marketing/Brand/BRAND_FRENCH_PATTERNS.md) (stub)
- [`BRAND_JARGON_AUDIT.md`](../../../Marketing/Brand/BRAND_JARGON_AUDIT.md)
