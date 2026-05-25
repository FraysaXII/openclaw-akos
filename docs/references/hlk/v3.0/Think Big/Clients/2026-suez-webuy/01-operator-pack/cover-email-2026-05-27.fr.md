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
attachment_pdf: architecture-addendum.fr.pdf
render_target: mail
render_pipeline_note: "Rendered to HTML body at SMTP-send time via downstream mail tooling; .md is the source-of-truth and is NEVER sent externally per akos-external-render-discipline.mdc RULE 1; operator finalises [NOM_LECTEUR_SUEZ] + Aïsha first-name reveal (if appropriate) + attaches architecture-addendum.fr.pdf at SMTP-send time."
last_review: 2026-05-25
---

# Cover mail — SUEZ WeBuy procure-to-pay, prochaine étape

> **DRAFT — operator-final-pass required.** Resolve `[NOM_LECTEUR_SUEZ]` + decide Aïsha first-name reveal at SMTP-send time per BBR identity discipline. Attach `architecture-addendum.fr.pdf` from `_exports/`.

---

**Objet :** Suite à notre échange — proposition de POC et architecture en trois temps

**De :** Holistika Research — en collaboration avec EFA Académie
**À :** [NOM_LECTEUR_SUEZ]
**Pièce jointe :** Architecture-addendum.fr.pdf (2 pages)

---

Bonjour [NOM_LECTEUR_SUEZ],

Merci pour notre échange de la semaine dernière sur le processus de demande d'achat WeBuy. Comme convenu, nous avons mis au propre une proposition resserrée autour de ce qui nous semble être votre priorité immédiate : **stopper la dérive des libellés** sans attendre un projet ERP de grande ampleur.

Vous trouverez en pièce jointe une **addenda architecturale de deux pages** qui complète la proposition que nous vous avons remise. Elle décrit :

- une **phase 1** sous Microsoft Power Query — un générateur de libellés déterministe, livré sous quinze jours, qui produit la chaîne en cinq composants conforme à votre nomenclature ;
- une **phase 2** sous Microsoft Power Platform — application web légère multi-catégories pour étendre la mécanique à vos six familles d'engagement (CAPEX, maintenance, pneus, fournitures, transport, location) ;
- une **phase 3** d'étude de faisabilité d'intégration avec votre portail WeBuy, plus une couche de reporting Power BI sur l'usage mensuel par catégorie, fournisseur, engin et centre de coût.

Le document précise également deux points qui ont émergé de votre relecture :

1. **La continuité opérationnelle après mise en service.** L'addenda décrit le rôle que tiendra notre opératrice partenaire en continuité — celle qui opère le processus aujourd'hui chez vous et qui assurera la maintenance et la formation après transfert. Cette continuité est la clé de la pérennité de la mécanique.

2. **La réplicabilité au-delà de ce premier périmètre.** L'architecture est pensée pour que votre office CTO puisse, à terme, dupliquer la mécanique sur d'autres processus d'approvisionnement — l'investissement initial est donc capitalisable.

Nous proposons un point de quinze à vingt minutes en début de semaine prochaine pour répondre à vos questions sur l'addenda et caler ensemble la fenêtre de lancement de la phase 1.

Nous restons à votre disposition.

Bien à vous,

**Équipe Holistika Research × EFA Académie**

— Mission portée conjointement —

---

*Cette adresse est aussi celle de notre opératrice partenaire et de l'équipe EFA Académie ; vos réponses seront traitées dans la continuité de notre échange.*
