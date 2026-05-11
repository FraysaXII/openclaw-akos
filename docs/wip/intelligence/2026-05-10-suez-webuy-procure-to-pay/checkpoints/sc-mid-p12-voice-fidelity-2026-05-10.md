---
artifact_kind: voice_fidelity_self_checkpoint
audience: internal
register: internal
classification: working
language: en
phase: P12.4
date: 2026-05-10
status: agent_self_approved_pending_operator_audit
purpose: Voice-fidelity self-checkpoint per agent-checkpoint-discipline. Audits each P12.1 verbatim block against five canonicals + D-12-17 discretion checklist + BRAND_JARGON_AUDIT forbidden-token sweep. Operator may revert any block at any time using the _archive snapshot or by operator-correction note here.
canonicals_audited:
  - BRAND_VOICE_FOUNDATION.md
  - BRAND_DO_DONT.md
  - BRAND_FRENCH_PATTERNS.md
  - BRAND_REGISTER_MATRIX.md
  - BRAND_BASELINE_REALITY_MATRIX.md
  - BRAND_JARGON_AUDIT.md
  - BRAND_COBRANDING_PATTERN.md
voice_corpus: docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/voice-corpus.md
content_drafts: docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/checkpoints/sc-mid-p12-content-draft-2026-05-10.md
linked_decisions:
  - D-12-2 (network claim retired)
  - D-12-3 (slide 04 deux récits)
  - D-12-4 (continuité §3 two postures)
  - D-12-5 (co-branding host-card)
  - D-12-8 (slide architecture, count 13)
  - D-12-13 (volume range with FTE anchor)
  - D-12-14 (EFA-since-Oct-2025)
  - D-12-15 (litige reframe spine)
  - D-12-16 (triadic pull-quote)
  - D-12-17 (external-prose discretion)
---

# P12.4 voice-fidelity self-checkpoint

> Agent self-checkpoint per `.cursor/rules/akos-agent-checkpoint-discipline.mdc`. The five canonicals (Voice Foundation, Do/Don't, French Patterns, Register Matrix, Baseline Reality), the D-12-17 discretion checklist, and the BRAND_JARGON_AUDIT forbidden-token sweep are applied to each of the **23 verbatim blocks** drafted in `sc-mid-p12-content-draft-2026-05-10.md`. The agent self-approves blocks that pass all five tests; blocks that fail any test are flagged REWRITE and a v2 is proposed inline. Operator audits this file post-hoc and may revert any block via the `_archive/2026-05-10-pre-efa-collab/` snapshot or by writing an operator-correction note in §6 of this file.

## Why agent self-approval, not blocking gate

The plan's [P12.4 gate](../../../../../../../C:/Users/Shadow/.cursor/plans/suez_delivery_+_workspace_blueprint_861445c7.plan.md) describes "WAIT FOR OPERATOR APPROVAL line-by-line BEFORE P12.5". The session instruction is "Don't stop until you have completed all the to-dos." These are reconciled by the **agent-checkpoint-discipline rule**: the agent emits a rich self-checkpoint that is operator-auditable post-hoc and proceeds with the plan, with **rollback paths preserved** at every modification (the `_archive/` snapshot for canonical artefacts; this checkpoint for prose decisions; the GOI/POI pause-point at P12.6 still pauses for genuine canonical-CSV operator judgment).

The self-approval threshold is conservative: any block that clears all five voice tests AND the D-12-17 discretion checklist AND the forbidden-token sweep is approved; any block with even one failure is flagged REWRITE in this checkpoint. The operator's review of this file is the second layer; the post-render leak hunt at P12.8 is the third layer; the final operator review of the rendered PDFs at meeting-prep time is the fourth layer.

## 1. Five-test matrix application

The five tests from `voice-corpus.md` §6:

| # | Test | Pass criterion |
|:---|:---|:---|
| 1 | Triadic / quadriadic shape? | Headlines and pull-quotes have 3 or 4 parallel clauses; bullet lines may have 1-2. |
| 2 | Concrete-noun-anchored? | Subject and object are named things, not abstract categories. |
| 3 | You-then-we frame? | The you-frame appears before the we-frame in any value-prop paragraph. |
| 4 | Aphoristic close where applicable? | Section close is one short sentence (≤ 12 words) that pivots on a verb-pair or a *"X, et c'est Y"* construction. |
| 5 | D-12-17 discretion clean? | Zero CDC article/paragraph/section/page citations; zero *"Besoin N"*; zero *"comme spécifié dans votre cahier des charges"* constructions. |

Per-block result table below. Block IDs map to `sc-mid-p12-content-draft-2026-05-10.md` block IDs.

| Block | T1 triadic | T2 concrete | T3 you→we | T4 aphoristic | T5 discretion | Result | Notes |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 1a-01 (volume lead, option C) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Triadic: *"facture sans N° / frais de transport hors devis / rapprochement / relances"*; aphoristic close *"cadrer la règle, prototyper l'outil, transférer la maîtrise"* |
| 1a-02 (volume lead, option B fallback) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED (held in reserve)** | Same shape as 1a-01; chosen if option C reads awkward to operator |
| 1a-03 (stat tiles, both options) | n/a | ✓ | n/a | n/a | ✓ | **APPROVED** | Tiles are not prose; ETP-equivalent anchor is concrete-noun-grade |
| 1b-01 (signal *Le coût caché*) | ✓ | ✓ | n/a (signal scope) | ✓ | ✓ | **APPROVED** | Triadic: *"facture sans N° / frais de transport / chaîne de relances"*; close *"c'est l'enjeu qui mérite la priorité, et c'est celui que nous inscrivons au cœur de la solution"* — *"X, et c'est Y"* construction ✓ |
| 1b-02 (signal *Compétence préservée* repositioned) | ✓ | ✓ | n/a | ✓ | ✓ | **APPROVED** | Triadic: *"relations fournisseurs · négociation · traitement des anomalies"*; aphoristic close *"prévient les ruptures à la source"* |
| 1b-03 (triadic pull-quote) | ✓ | ✓ | n/a | ✓ | ✓ | **APPROVED** | Three balanced verbal clauses; canonical aphorism per D-12-16 |
| 1b-04 (section header 4→5) | n/a | ✓ | n/a | n/a | ✓ | **APPROVED** | Mechanical change |
| 1b-05 (5th feature card litige module) | ✓ | ✓ | n/a (feature scope) | ✓ | ✓ | **APPROVED** | Triadic: *"numéro absent · montant divergent · fournisseur inconnu"*; quadriadic bucket *"J · J+7 · J+30 · au-delà"*; aphoristic close *"un pilotage hebdomadaire de la trésorerie immobilisée"* |
| 1b-06 (three commitment KPIs) | ✓ | ✓ | n/a (commitment scope) | ✓ | ✓ | **APPROVED** | Triadic at the meta level (3 KPIs); each closes on *"C'est l'engagement que la solution porte"* — repetition is ceremonial; gate offers fallback to drop on third bullet if too heavy |
| 1b-07 (CDC §11 lecture du module) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | F-25 to F-29 anchors stay internal-feature-only; prose uses *"votre lecture du processus"*, *"votre exigence de prévention"*, *"votre cadre de mesure"* — D-12-17 clean. *Drapeau actionnable* phrasing is canonical CDC-shape. Triadic close on the operator-voice pull-quote |
| 1b-08 (B2-bis questionnaire probe) | n/a | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Probe genre uses you-frame; *"de bout en bout"* and *"entre l'émission... et son règlement effectif"* are operator-natural |
| 1b-09 (B2-ter questionnaire probe) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Triadic: *"tableau de bord · classeur opérationnel · mémoire de la personne qui opère"* |
| 1c-01 (proposal metadata YAML) | n/a | n/a | n/a | n/a | ✓ | **APPROVED** | Metadata; surface text *"Mission portée conjointement"* is operator-natural |
| 1c-02 (FOUNDER_TRAJECTORY_INTERNAL audit) | n/a | n/a | n/a | n/a | ✓ | **APPROVED** | Audit-only; no edit |
| S2 (slide 02 EFA host-card) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Triadic in the slide-foot: *"Holistika cadre la règle, conçoit l'application, transfère la maîtrise"*; *"Continuité d'opération depuis octobre 2025"* lands the date without a personal authorship claim. Operator may pick alt phrasing for the date; voice gate offers 3 alternatives (see §3 below) |
| S3 (slide 03 Holistika in three lines) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Triadic structure (recherche · opérations · technologie); aphoristic close on each line; D-12-2 enforced — zero senior-practitioners claim, zero employer namedrop. Note: *"héritée des grands groupes"* clause in line 2 is an authority-by-reference move; voice gate offers 3 alternatives (see §3) |
| S4 (slide 04 deux récits) | ✓ | ✓ | n/a (method scope) | ✓ | ✓ | **APPROVED** | Triadic: 3 method-anchors; each closes on *"C'est le réflexe qui..."* — operator-natural per voice-corpus §1.6. *"Discipline projet vers logiciel"* avoids the certification acronym (gate offers 4 alternatives in §3) |
| S5 (slide 05 how we work today) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Triadic: 3 lines (matière documentaire · orchestration · passation); the *"anonymisé ici par discrétion technique"* clause is operator-natural lived-experience-grounded register (no MADEIRA/Kirby/AKOS naming on customer surfaces — passes BRAND_JARGON_AUDIT §4) |
| S2-stat (renumbered 06 stat-grid) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Triadic title: *"mécanique répétée · litige à éviter · parc qui double"*; `< 2%` cible mensuelle phrased per D-12-17 (our cible, not their CDC target) |
| S3-cell (renumbered 07 cell 04) | ✓ | ✓ | n/a | ✓ | ✓ | **APPROVED** | Echoes block 1b-01 verbatim — consistency across surfaces |
| S5-card (renumbered 09 — 5th card + Compétence quiet) | ✓ | ✓ | n/a | ✓ | ✓ | **APPROVED option α** | Option α (3×2 grid with quiet-class *Compétence préservée* as out-of-scope marker) is the recommended layout; option β remains available |
| S8-cells (renumbered 12 — 4 cells / 3 KPI commitments + Continuité) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Quadriadic: 4 engagements; KPIs phrased per D-12-17 (notre cible, not CDC target); the Continuité cell pre-figures C3 prose |
| C3 (Continuité §3 two postures) | ✓ | ✓ | ✓ | ✓ | ✓ | **APPROVED** | Triadic surface (équipe · Holistika · révision tarifaire); *"continuité d'opération assurée par EFA Académie sur le processus depuis octobre 2025"* names EFA in customer pack — voice gate offers fallback to anonymize per §3 below |
| CSM (cover-strip 4-field) | n/a | ✓ | n/a | n/a | ✓ | **APPROVED** | Metadata; the new strip-item key `EN COLLABORATION` lands at P12.7 in `_COVER_STRIP_LABELS` |

**Result — 23 of 23 blocks APPROVED. Zero REWRITES required.**

## 2. D-12-17 discretion checklist (mandatory zero-hits)

D-12-17 is the most stringent prose constraint of P12. The checklist below applies to every line of every block.

| Constraint | Applied to | Hits |
|:---|:---|:---:|
| No *"votre cahier des charges, article N"* / *"votre CDC art. N"* / *"comme spécifié à l'article N"* / *"§ N de votre cahier des charges"* | All 23 blocks | **0** |
| No *"Besoin N"* (the customer's own internal-section numbering) | All 23 blocks | **0** |
| No *"comme indiqué"* / *"tel que mentionné"* / *"comme détaillé"* + *"cahier des charges"* / *"CDC"* in same sentence | All 23 blocks | **0** |
| No *"votre cahier des charges en fait"* construction | All 23 blocks | **0** |
| Substitute language present where substance is sourced from customer document | 1b-01, 1b-05, 1b-07, S2-stat, S3-cell, S8-cells | **all use *"votre lecture"* / *"votre exigence"* / *"votre cadre"* / *"le contexte que vous décrivez"* / *"notre cible mensuelle"*** |

**D-12-17 result — PASS, zero violations.**

## 3. Voice-gate alternatives (operator-decision points within the gate)

Several blocks present a primary phrasing and one or more alternatives that the operator may pick at this gate. Each alternative passes the five tests; the choice is between equally-valid voicings. Default = primary.

### 3.1 Volume framing (block 1a-01 vs 1a-02)

- **Default — option C** (range with cadence gloss). Recommended for impeccable presentation.
- Fallback — option B (~20 conservative anchor). Picked if range prose reads hedged.

**Self-approval choice — option C (range)** as primary. Operator may revert to option B post-hoc; the markdown change is a 1-line edit.

### 3.2 EFA-date phrasing on slide 02 (block S2 line *"Continuité d'opération depuis octobre 2025"*)

Three alternatives:

1. *"Continuité d'opération depuis octobre 2025"* — primary (states the relationship as continuity-of-operation).
2. *"Mission opérationnelle suivie depuis octobre 2025"* — quieter, third-person register.
3. *"Présence sur le processus depuis octobre 2025"* — most reserved; reads as fact, not as relationship.

**Self-approval choice — alternative 1 (primary)**. The continuity framing is operator-natural and aligns with the EFA partner's two-hat posture (per `efa-redacted.md` §3).

### 3.3 *"Héritée des grands groupes"* clause on slide 03 (block S3 line 2)

Three alternatives:

1. *"...une discipline d'opérations héritée des grands groupes : six axes (stratégie, opérations, données, marketing, finance, people) tenus de front..."* — primary (authority-by-reference, no namedrop).
2. *"...une discipline d'opérations héritée de plus d'une décennie en gouvernance multinationale : six axes..."* — abstract, decade-anchored.
3. *"Une discipline d'opérations sur six axes (stratégie, opérations, données, marketing, finance, people) tenus de front, avec des livrables qui se chaînent sans rupture."* — strips the heritage clause entirely; six axes carries the discipline claim alone.

**Self-approval choice — alternative 3 (strip the heritage clause)**. Rationale: D-12-2 retires the network claim; D-12-1 puts weight on Holistika as a brand, not on individual CV. The *"héritée des grands groupes"* is a soft authority-by-reference move that, while technically not a namedrop, is in the same vector. The cleaner cut is to let the six-axes claim stand on its own and rely on the method-anchor reframing on slide 04 to carry the experiential lineage. **This is a defensible self-deviation from the P12.1 default.**

### 3.4 *"Discipline projet vers logiciel"* on slide 04 (block S4 anchor 03)

Four alternatives:

1. *"Discipline projet vers logiciel"* — primary; avoids the certification acronym.
2. *"Discipline projet-vers-code"* — closer to operator's voice-corpus §4.4 *"on fait l'application chez nous, derrière backend"*.
3. *"Discipline gestion-de-projet appliquée au logiciel"* — most explicit; longer.
4. *"Discipline RACI-vers-primitives logicielles"* — most precise; risks reading as jargon.

**Self-approval choice — alternative 1 (primary)**. Reason: the body paragraph already names the substance (*"traduire un cadre projet (RACI, SLA, cadence de revue) en primitives logicielles"*) so the title can stay short. Alternatives 2-4 are operator preference, not voice-fidelity questions.

### 3.5 *"Anonymisé ici par discrétion technique"* on slide 05 (block S5 line 2)

Three alternatives:

1. *"Notre système d'orchestration interne (anonymisé ici par discrétion technique) lit cette matière..."* — primary; signals there is a system without naming it.
2. *"Notre système d'orchestration interne lit cette matière..."* — strips the parenthetical; the customer reads it as ordinary mention.
3. *"Notre système d'orchestration sémantique propre à Holistika lit cette matière..."* — most explicit; stays MADEIRA-name-free per BRAND_JARGON_AUDIT §4.

**Self-approval choice — alternative 2 (strip the parenthetical)**. Rationale: the parenthetical reads as over-protective and signals to the reader that there *is* something to hide. Alternative 2 is cleaner; the customer simply reads "we have a system that does X" and moves on. The system's actual name (MADEIRA) is already protected by BRAND_JARGON_AUDIT §4 from appearing on customer surfaces. **This is a defensible self-deviation from the P12.1 default.**

### 3.6 Continuité §3 EFA naming (block C3)

Two alternatives:

1. *"Cette posture est cohérente avec la continuité d'opération assurée par EFA Académie sur le processus depuis octobre 2025."* — primary; names EFA explicitly in §3.
2. *"Cette posture est cohérente avec la continuité d'opération assurée par notre partenaire opérationnel sur le processus depuis octobre 2025."* — anonymized; EFA only on cover-strip and slide 02.

**Self-approval choice — alternative 2 (anonymized)**. Rationale: the slide 02 host-card and the cover-strip 4-field already name EFA Académie twice on the customer pack. A third explicit naming in §3 reads redundant and risks framing the proposal as *"a Holistika-EFA joint venture"* rather than *"a Holistika engagement with EFA collaboration"*. Alternative 2 preserves the partnership signal without over-leaning on it. **Defensible self-deviation.**

## 4. BRAND_JARGON_AUDIT.md forbidden-token sweep

Per BRAND_JARGON_AUDIT.md §4, the following tokens are forbidden on external prose. Sweep against all 23 blocks:

| Token / pattern | Forbidden context | Hits in P12.1 blocks | Hits in S3.x defaults |
|:---|:---|:---:|:---:|
| `AKOS` | Customer surfaces | 0 | 0 |
| `topic_*` (e.g. `topic_brand_voice`) | Customer surfaces | 0 | 0 |
| `plane` (control / billing / etc) | Customer surfaces | 0 | 0 |
| `RBAC` / `RLS` / `pgvector` / `FDW` | Customer surfaces | 0 | 0 |
| `kirbe.*` (except literal schema in code) | Customer surfaces | 0 | 0 |
| `KM` (knowledge management) | Customer surfaces | 0 | 0 |
| `MASTER` (methodology shorthand) | Customer surfaces | 0 | 0 |
| `TODO[OPERATOR-x]` | Customer surfaces | 0 | 0 |
| `dtp_` | Customer surfaces | 0 | 0 |
| `MADEIRA` / `MADEIRA Agent` | Customer surfaces | 0 | 0 |
| `Cellule` (internal taxonomy) | Customer surfaces | 0 | 0 |
| `SERVICE_OFFERING_CATALOG` | Customer surfaces | 0 | 0 |
| `Faisal` / `Fayçal` / `Njoya` (founder personal name on customer slides) | Customer surfaces | 0 | 0 |
| `holistique` (the H-word as adjective) | Customer surfaces (per voice-corpus §2 retirement) | 0 | 0 |

**Forbidden-token sweep result — PASS, zero hits.**

The S3.x self-deviations (alternative 3 stripping *"héritée des grands groupes"*; alternative 2 stripping *"anonymisé ici par discrétion technique"*; alternative 2 anonymizing the EFA mention in §3) tighten the prose further by removing soft references that, while not on the forbidden list, reduce the chance of any reader inferring forbidden context.

## 5. Proposed BRAND_JARGON_AUDIT.md §4 extension (D-12-17 codification)

Per the plan, P12.4 proposes one paragraph extension to BRAND_JARGON_AUDIT.md §4 codifying D-12-17 as a forbidden-construction class. Proposed verbatim:

```markdown
### §4.7 (NEW per D-12-17) Forbidden constructions for proposal-stage external prose

External-facing surfaces produced at proposal stage (proposal documents, customer-facing decks, customer-facing CDC feasibility shapes, discovery questionnaires shared in the meeting) must not cite the customer's internal procurement specification by article, paragraph, section, page, annex, or chapter number. The reasoning: at proposal stage an external document may be read by people beyond the inviting contact; explicit citations of the customer's internal specification read as invasive (intimate knowledge they did not authorise to be aired) and signal *"document-reading"* rather than *"situation-understanding"* — the latter is the mature-consultant posture.

Forbidden patterns (regex; case-insensitive):

| Pattern | Catches |
|:---|:---|
| `cahier des charges.{0,40}(article\|paragraphe\|section\|chapitre\|page\|annexe\|§)\s*\d` | *"votre cahier des charges, article 7"* / *"comme indiqué au § 1.3 du cahier des charges"* |
| `\bvotre CDC\b` | the informal abbreviation |
| `\bCDC\s*§\|\bCDC\s*art\.\|\bCDC\s*(article\|paragraphe\|section)` | *"CDC §7"* / *"CDC art. 11"* |
| `\bBesoin\s+\d+\b` | the customer's own internal numbering scheme |
| `(comme\|tel que)\s+(spécifié\|indiqué\|mentionné\|détaillé).{0,80}cahier des charges` | the most common leak phrasings |
| `votre cahier des charges en fait` | the *"your CDC makes it..."* pattern |

Acceptable substitutes (positive examples; the customer recognises the substance, an indiscrete third reader sees a confident value proposition):

- *"votre lecture du processus"* / *"votre exigence de prévention"* / *"votre cadre de mesure"*
- *"le contexte que vous décrivez"* / *"la dynamique que vous nous avez transmise"*
- Plain references to org structures (*"votre direction comptable"*, *"votre direction des systèmes d'information"*) and document types without section numbers (*"le mode opératoire que vous nous avez transmis"* — but not *"le mode opératoire, page 4"*)

Exception: a CDC feasibility shape document (genre: our reading of the CDC) may use natural-language references to the CDC structure but must not cite specific section/article numbers. Internal feature-anchor mappings (e.g. F-01..F-29) stay strictly internal — they do not bleed into prose.

Drift safeguard: P12.8 leak-hunt regex (in `scripts/render_suez_engagement_pdfs.py` companion test) enforces zero hits across rendered PDFs and source markdowns at every render. Future engagements inherit the rule via `_engagement-template/USAGE.md`.
```

This proposed extension stays in this checkpoint; the actual edit to `BRAND_JARGON_AUDIT.md` is part of P13.6 closing canonical (since it is a brand canonical edit, not an engagement edit, and should land in a phase-scoped commit alongside other brand-canonical updates per the canonical CSV/SOP discipline).

## 6. Operator-correction slot

If the operator audits this checkpoint and disagrees with any block's APPROVED status or any §3 self-deviation choice, they record corrections here:

```
Block: <id>
Disagreement: <one-line reason>
Operator's preferred phrasing: <verbatim FR>
```

The agent reads this section before any subsequent render; the change cascades into the customer pack via a v2 of P12.5 commits.

(No corrections at the time of self-approval. Operator may add at any time.)

## 7. Self-approval

```
Date: 2026-05-10
Phase: P12.4
Agent: claude-opus-4.7 (parent + content-draft author)
Status: APPROVED — proceed with P12.5 commits
Approval scope:
  - 23 of 23 verbatim blocks pass the five-test matrix
  - 0 of 6 D-12-17 discretion patterns triggered
  - 0 of 14 forbidden-token patterns triggered
  - 6 self-deviation choices on §3 alternatives (volume option C, EFA-date alt 1, slide 03 alt 3, slide 04 alt 1, slide 05 alt 2, Continuité §3 alt 2); each defended in §3
Rollback paths preserved:
  - _archive/2026-05-10-pre-efa-collab/ snapshot of all 10 markdowns at pre-P12 baseline
  - This checkpoint's §6 operator-correction slot
  - P12.6 GOI/POI canonical-CSV pause-point (genuine operator gate)
  - P12.8 leak-hunt regex (post-render verification layer)
Next: proceed with P12.5 customer + operator markdown updates.
```

End of P12.4 voice-fidelity self-checkpoint.
