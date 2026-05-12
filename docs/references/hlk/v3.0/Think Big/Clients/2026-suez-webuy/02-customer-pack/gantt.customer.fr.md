---
language: fr
status: active
audience: customer
register: external
program_id: ENG-SUEZ-WEBUY-2026
engagement_slug: 2026-suez-webuy
artifact_role: customer-deliverable
intellectual_kind: gantt
brand_voice_register: peer_consulting
collaboration_partner: EFA Académie
collaboration_since: 2025-10
mission_posture: Mission portée conjointement
gantt_variant: B
confidence_band: 4
ratify_cadence: discovery_week_1
brand_companion_to: proposal.customer.fr.md
last_review: 2026-05-12
---

<p class="lead">Gantt indicatif de la mission WeBuy. Variante B (Prototype) recommandée. Variantes A et C présentées en posture pour comparaison. Bande de confiance 4/5 (Probable) pour la variante B sur les dates ; les variantes A et C sont en posture (bande 3/5). Les dates se précisent à l'atelier de cadrage de la première semaine.</p>

# Gantt — Mission WeBuy / Holistika × EFA Académie

## Variante B — Prototype (recommandée)

```mermaid
gantt
    title ENG-SUEZ-WEBUY-2026 — Variante B (Prototype, recommandée)
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Cadrage
    Atelier de lancement (90 min)              :v_b_1, 2026-06-01, 1d
    Lecture du processus + entretiens          :v_b_2, after v_b_1, 5d
    Cahier des charges fonctionnel             :v_b_3, after v_b_2, 5d
    Plan de déploiement                        :v_b_4, after v_b_3, 3d

    section Prototype
    Prototype mesuré (lecture/composition)     :v_b_5, after v_b_4, 8d
    Module litige (prévention + suivi)         :v_b_6, after v_b_4, 6d
    Revue intermédiaire avec direction         :v_b_7, after v_b_6, 1d
    Itérations + validation opérationnelle     :v_b_8, after v_b_7, 4d

    section Transfert
    Documentation de passation                 :v_b_9, after v_b_8, 3d
    Atelier de transfert                       :v_b_10, after v_b_9, 1d
    Période de support post-transfert          :v_b_11, after v_b_10, 5d
```

**Lecture rapide :** quatre semaines de prototype suivies d'une semaine de transfert. La passation est totale ; aucune dépendance résiduelle. La période de support post-transfert est incluse au prix forfaitaire.

## Variante A — Cadrage seul (posture)

```mermaid
gantt
    title ENG-SUEZ-WEBUY-2026 — Variante A (Cadrage, posture)
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Cadrage
    Atelier de lancement (90 min)              :v_a_1, 2026-06-01, 1d
    Lecture du processus + entretiens          :v_a_2, after v_a_1, 5d
    Cahier des charges fonctionnel             :v_a_3, after v_a_2, 5d
    Plan de déploiement                        :v_a_4, after v_a_3, 3d
    Atelier de remise + transfert              :v_a_5, after v_a_4, 1d
```

**Lecture rapide :** trois semaines de cadrage seul ; pas de prototype. Le livrable est un cahier des charges et un plan de déploiement remis clés en main pour la direction des systèmes d'information. Bande de confiance 3/5 (posture) — les durées proviennent de notre cadence-type ; les dates se précisent à l'atelier de cadrage.

## Variante C — Industrialisation (posture)

```mermaid
gantt
    title ENG-SUEZ-WEBUY-2026 — Variante C (Industrialisation, posture)
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Cadrage
    Atelier + lecture + cahier des charges     :v_c_1, 2026-06-01, 14d

    section Prototype
    Prototype + module litige + revue          :v_c_2, after v_c_1, 21d

    section Industrialisation
    Extension périmètre + cadre de gouvernance :v_c_3, after v_c_2, 14d

    section Transfert
    Documentation + atelier + support          :v_c_4, after v_c_3, 9d
```

**Lecture rapide :** huit à neuf semaines pour l'industrialisation complète : cadrage + prototype + extension de périmètre + cadre de gouvernance + transfert. Bande de confiance 3/5 (posture) — l'extension de périmètre est calibrée à votre parc complet à mise en service. Les dates se précisent à l'atelier de cadrage et au point d'extension.

---

## Bandes de confiance

- **Variante B** — bande 4/5 (Probable) sur les dates : durées calibrées sur engagements analogues + capacité opérateur vérifiée.
- **Variantes A + C** — bande 3/5 (Posture) sur les dates : durées calibrées sur cadence-type Holistika ; précision attendue à l'atelier de cadrage.
- **Toutes variantes** — atelier de lancement à T+0 (date à confirmer dans les cinq jours ouvrés suivant l'engagement).

## Cadence de validation

Per ratify_cadence: discovery_week_1. Les dates de chaque variante sont confirmées (bande 5/5) à la sortie de l'atelier de lancement de la première semaine. Toute évolution de périmètre identifiée durant la phase de cadrage est tracée et soumise à votre validation avant impact tarifaire ou de calendrier.

## Cross-references

- Proposition d'engagement (narration) : [`proposal.customer.fr.md`](proposal.customer.fr.md) section 4 — variantes A / B / C.
- Tarification : [`tarification.customer.fr.md`](tarification.customer.fr.md) — modalités commerciales par variante.
- Présentation commerciale : [`deck.customer.fr.md`](deck.customer.fr.md) slide 11 — Trois variantes.
- Discipline Gantt parente : [`BRAND_GANTT_DISCIPLINE.md`](../../../../../Admin/O5-1/Marketing/Brand/UX%20Designer/canonicals/BRAND_GANTT_DISCIPLINE.md) — variante B est le motif de référence proof-of-discipline.
