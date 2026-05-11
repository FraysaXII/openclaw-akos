---
artifact_kind: voice_corpus_comparator
audience: internal
register: internal
classification: source-grade
language: en
phase: P12.0
date: 2026-05-10
sources_status: redacted_extracts; raw_transcripts_in_temp_move_or_delete_pending_deletion_at_p12_9
purpose: P12.4 voice-fidelity gate comparator; ground all customer-pack prose in operator's actual idiom (FR), not in agent-generated patterns
governance:
  - BRAND_VOICE_FOUNDATION.md
  - BRAND_DO_DONT.md
  - BRAND_FRENCH_PATTERNS.md
  - BRAND_REGISTER_MATRIX.md
  - BRAND_BASELINE_REALITY_MATRIX.md
---

# P12.0 voice corpus — operator's idiom (FR), with comparators

> Internal source-grade note for the P12.4 voice-fidelity gate. Distilled from two long French transcripts where the operator speaks at length: 1h08 onboarding (`[EFA-T1]`) and 21min proposal-briefing (`[EFA-T2]`), plus the EFA-side voicemails (volume + litige). Names redacted; what stays is the **shape of the prose** the operator actually uses when he is not writing a customer document — i.e. the cadence the AI-generated draft must converge towards, not away from.

## 1. The operator's voice — load-bearing patterns

### 1.1 Triadic and quadriadic enumerations are the default rhythm

The operator structures arguments in three or four parallel terms more often than in pairs. Direct from `[EFA-T1]`:

> *"Découvrir, planifier, exécuter, et les voletifs."* — four-term sequence, present tense.
> *"Stratégie de business, opérations, et la partie technologique."* — three-term sequence, naming domains.
> *"Anticipation et Résilience. C'est-à-dire Foresight, Process Engineering, Business Engineering."* — bilingual triadic.

Customer-pack consequence: every value-prop line in `proposal.customer.fr.md` and `deck.customer.fr.md` should pass the *triadic test*. The existing aphorism *"Cadrer · prototyper · transférer"* already passes; the new triadic pull-quote *"Automatiser ce qui se calcule, prévenir ce qui se rompt, préserver ce qui se juge"* (D-12-16) is in-cadence by design.

### 1.2 Concrete-noun-heavy, verb-anchored, abstraction-light

The operator's natural prose names objects of work, not categories. Direct from `[EFA-T1]`:

> *"Tu prends ton image, par exemple, et partir de là."*
> *"Le poste du rechercheur. Les rechercheurs, c'est ça, ce qu'ils font."*
> *"Tu as un programme."* — singular, named, not "a portfolio of strategic initiatives."
> *"Le manuel d'utilisateur."* — said five times across `[EFA-T4]` (08-04 prospection); never abstracted into "operational documentation."

Customer-pack consequence: replace any latinate-noun-cluster ("la mise en œuvre opérationnelle") with verb-anchored concrete prose ("ce que fait l'application", "ce que vous voyez à l'écran"). The current `proposal.customer.fr.md` lead paragraph already complies; the new litige feature card (P12.1b) is written in the same register.

### 1.3 Diagnosis-then-method, not deliverable-list

The operator describes work as *what becomes legible* before he describes deliverables. Direct from `[EFA-T1]`:

> *"Une fois que c'est là, le temps, c'est le temps fort à l'argent. C'est là où entre la période du business."* — the *what becomes possible* frame.
> *"Tu prends quelqu'un, tu lui proposes tant de deals."* — the *what we do with the diagnosis* frame.

Customer-pack consequence: the proposal Section 2 ("Notre lecture de votre situation") leads with *what we see*, not with *what we deliver*. Section 3 ("Ce que nous construisons") is the deliverable layer and stays grounded in concrete features. The reframe in P12.1b respects this order.

### 1.4 Pragmatic, lived-experience-grounded — never abstract appeals

The operator's authority moves comes from named situations, not from claims of expertise. Direct from `[EFA-T4]`:

> *"À L'Oréal, on avait un camion bloqué pendant une semaine et demie, parce que c'était l'unique personne qui savait débloquer le truc. Et l'argent qu'ils ont perdu, c'était un truc de malade."*

(Internal-only quote; **not** for customer surface — see D-12-2 retirement of the network claim.)

Customer-pack consequence: keep the lived-experience tone *without the named-employer authority move*. Slide 04 method-anchors (D-12-3) translate three career-shaped intuitions (data-quality discipline; multinational governance; PMP-to-software discipline) into method names, not into employer namedrops. The intuition stays; the proof moves to the internal trajectory file.

### 1.5 Self-referential clarity moves — "I" used to mark uncertainty, "on" used to claim discipline

The operator switches person to mark epistemic distance. Direct from `[EFA-T4]`:

> *"Je crois que..."* — uncertainty marker
> *"On découpe les tâches"* — discipline claim (collective ownership)
> *"On commence à demander alors à la personne qui a ça en charge"* — collaborative-procedure register
> *"C'est pour ça que je..."* — explanation-of-self register

Customer-pack consequence: customer-pack uses *"nous"* (formal-collaborative) almost exclusively, with *"je"* reserved for one or two lines where founder-side judgment is the substance (e.g. the operator-voice pull-quote). This already matches existing customer-pack practice.

### 1.6 The aphoristic close

The operator closes longer arguments on a short, memorable line. Direct from `[EFA-T1]`:

> *"Aujourd'hui, on facture du service, mais demain, on facture du produit. Le pont, c'est du code."*
> *"On est tous holistiques, surtout si t'es entrepreneur."*
> *"Le show doit continuer."*

Customer-pack consequence: each section of `proposal.customer.fr.md` ends on an aphoristic close, never on a deliverable list. The pull-quote *"Automatiser ce qui se calcule, prévenir ce qui se rompt, préserver ce qui se juge"* (D-12-16) is the canonical operator-voice aphorism for this engagement.

### 1.7 No em-dash in headlines

The operator uses commas and middle dots in conversational French; em-dashes appear in his prose only when paraphrasing English source. Customer-pack discipline (per Impeccable + D-12-3): em-dashes are banned from titles and headlines; commas or restored middle dots replace them. Body text may use em-dashes sparingly where French prose calls for them.

## 2. What the operator does NOT do — for AI-detection

These are the patterns to *avoid* in the customer pack. They are common AI-prose tells the operator finds off:

| AI-tell | Operator-natural replacement |
|:---|:---|
| *"À l'ère de l'intelligence artificielle..."* (epochal opener) | *"Vos équipes traitent entre vingt et une cinquantaine de demandes WeBuy par jour."* (situated, dated, grounded) |
| *"Une approche holistique permet de..."* (the H-word as a claim) | *"Une mécanique qui prévient ces ruptures à la source."* (the H-word retired from external prose per BRAND_JARGON_AUDIT.md) |
| *"Notre méthodologie éprouvée garantit..."* (claim without reference) | *"Cadrer la règle, prototyper l'outil, transférer la maîtrise."* (concrete verbs, no guarantee posture) |
| *"En leveraging l'expertise..."* (anglicism + abstraction) | *"Vos équipes gardent le jugement sur ce qui demande du discernement."* (clean French, named subject) |
| *"Une solution de transformation digitale clé-en-main"* (corp-deck deck-speak) | *"Une application qui traite la mécanique, pour libérer le temps du jugement."* (problem-side first) |
| Long sentences with two semicolons (~30+ words) | Three-clause sentence with ten-to-fifteen words per clause; period after each clause where rhythm allows. |
| *"Nous accompagnons nos clients dans..."* (consultancy-cliché opener) | *"Vous traitez aujourd'hui... La friction n'est pas... C'est..."* (you-then-we frame, problem-named-first) |

These are enforcement examples, not exhaustive. The voice-gate at P12.4 picks any line in the new draft and tests it against this comparator.

## 3. EFA partner lead voice — for the host-card slide 02 only

The bridge's voice is shorter, warmer, more anecdote-driven. Distilled from `[EFA-T2]`:

| Pattern | Example |
|:---|:---|
| Short approval | *"C'est nickel."* / *"C'est bien."* / *"C'est bien parce que..."* |
| Sensory brand feedback | *"Là, ça m'a attiré, en plus, le violet."* |
| Pragmatic single-step | *"Il faut commencer par un et après on verra."* |
| Validation-of-other | *"Oui, oui, c'est ça."* (used as cadence anchor, not filler) |
| Closing the meeting | *"OK, ça marche."* / *"On fait comme ça."* |
| Customer-relationship intuition | *"Il faut que la personne reste sur le site et tout."* |
| Reasoning-by-example | *"Quand quelqu'un vient sur le site, pour un entrepreneur, c'est..."* |

The host-card slide 02 has at most 2-3 sentences. If it draws from the bridge's cadence, it should sound like the closing-the-meeting register (warm, declarative, brief). Suggested line shape (verbatim text drafted in P12.4):

> *"EFA Académie accompagne les équipes opérationnelles depuis [duration]. Ce dossier est porté avec Holistika, qui apporte la discipline méthodologique et l'outillage."*

(Two sentences. Declarative. No claims. Names the partner relationship, not the partner individual.)

## 4. Founder voice exemplars — for direct cadence comparison

Side-by-side, the operator's voice in `[EFA-T1]` versus the AI-prose to AVOID (paraphrased):

### 4.1 On the trois-équipes-un-objectif framing

**Operator:**
> *"Trois équipes, un seul objectif... Donc rechercheurs, ThinkBig et TechLab, pour faire une seule chose."*

**AI-prose to avoid:**
> *"Notre organisation tripartite synergique permet une délivrance intégrée."* (abstraction-cluster, no concrete subject)

### 4.2 On the AI-orchestration architecture

**Operator:**
> *"Madeira, l'unique chose qu'elle fait, c'est avoir mes questions. Je te jure. Elle prend mon prompt, elle prend ma documentation, elle voit comment je pense et comment je [travaille], où on en est, ou qu'est-ce qu'on a. Et avec ça, elle pose ma question mieux."*

**AI-prose to avoid:**
> *"Notre AI propriétaire Madeira optimise l'expérience utilisateur grâce à une compréhension contextuelle avancée."* (vendor-deck pattern; loses the operator's *"je te jure"* and the *"elle prend mon prompt, elle prend ma documentation"* concrete enumeration)

### 4.3 On Holistika's positioning

**Operator:**
> *"Nous, on fait stratégie direction, surtout opérationnelle. On travaille sur les données, tout ce que tu as, les systèmes aussi. On travaille avec ton équipe, tout seul, et on gère le marketing. Dès la conception de ta marque jusqu'à ce qu'on se voit, jusqu'à les problèmes qu'encore on a sur les systèmes. Donc on est transversal. Il faut vraiment que tu les dises qu'on est transversal."*

**AI-prose to avoid:**
> *"Holistika offre une expertise transversale couvrant la stratégie, les opérations et la technologie."* (the operator says this in 7 lines of concrete verbs; the AI-prose collapses to one abstract noun-cluster)

### 4.4 On the proof-of-concept register

**Operator:**
> *"On fait l'application chez nous, derrière backend, on utilise [le SaaS partenaire]. Donc les gens vont voir un peu un truc similaire à ce que tu vois ici."*

**AI-prose to avoid:**
> *"Nous concevons une architecture front-end personnalisée intégrée avec un back-end de confiance."* (vendor-deck-speak; loses the *"chez nous"* and the gestural *"un truc similaire à ce que tu vois ici"* that grounds the claim in something the listener is literally looking at)

## 5. Operator-voice exemplars on litige (the engagement spine, D-12-15)

Direct from `[EFA-T3]`, recombined with the founder's framing in `[EFA-T1]` on procurement automation:

> *"Une facture qui arrive sans numéro de commande, un fournisseur qui envoie avec des frais en plus, des frais de transport. Et du coup, ça ne colle pas et ça crée des retards. Voilà donc tout ça qui crée des relances."*

This is the source for the customer-pack signal *"Le coût caché : les litiges"* (P12.1b). The customer-facing version applies the founder's tightening pattern (concrete-nouns + you-frame + aphoristic close):

> *"**Le coût caché : les litiges.** Une facture sans numéro de commande, un frais de transport ajouté hors devis : la chaîne de relances qui en découle pèse plus que la saisie initiale, et bloque le règlement fournisseur le temps de la régularisation. C'est l'enjeu qui mérite la priorité, et c'est celui que nous inscrivons au cœur de la solution."*

Note the discipline: the operator's litige description uses three triggers; the customer-pack version uses two (the third is implied by *"ça ne colle pas"* → *"bloque le règlement fournisseur"*) to keep the cadence tight at customer-pack length.

## 6. Voice-fidelity test for new prose (used at P12.4 gate)

Each line of new customer-pack prose passes through these five tests at the voice gate. A line passing zero or one of these is rejected and rewritten.

| # | Test | Pass criterion |
|:---|:---|:---|
| 1 | **Triadic / quadriadic shape?** | Headlines and pull-quotes have 3 or 4 parallel clauses; bullet lines may have 1-2. |
| 2 | **Concrete-noun-anchored?** | Subject and object are named things, not abstract categories. |
| 3 | **You-then-we frame?** | The you-frame appears before the we-frame in any value-prop paragraph. |
| 4 | **Aphoristic close where applicable?** | Section close is one short sentence (≤ 12 words) that pivots on a verb-pair or a *"X, et c'est Y"* construction. |
| 5 | **D-12-17 discretion clean?** | Zero CDC article/paragraph/section/page citations; zero *"Besoin N"*; zero *"comme spécifié dans votre cahier des charges"* constructions; positive substitutes (*"votre lecture"*, *"votre cadre"*, *"le contexte que vous décrivez"*) where the substance needs anchoring. |

A sixth test, *register hygiene* (no internal vocabulary like Cellule, KM, Topic, Madeira, AKOS, MADEIRA on customer surfaces) is enforced at the leak-hunt step (P12.8).

## 7. Sources to delete at P12.9

- `temp-move-or-delete/EFA/2026-12-12 - Holistika Research - Business Developer - EFA x GDF SUEZ We Buy - Proposal Briefing - 3.m4a.md`
- `temp-move-or-delete/EFA/2026-12-12 - Holistika Research - Business Developer Onboarding.m4a.md`
- `temp-move-or-delete/EFA/WhatsApp Audio 2026-05-10 at 18.20.47.opus.mp3.md`
- `temp-move-or-delete/EFA/WhatsApp Audio 2026-05-10 at 18.21.10.opus.mp3.md`
- `temp-move-or-delete/EFA/08-04-2026 19.02 - EFA project prospection.mp3.md`
- `temp-move-or-delete/EFA/2026-04-17 19.46 - Holistika Research - Researcher Onboarding.mp3.md`
- `temp-move-or-delete/EFA/CDC_WeBuy_SUEZ.docx[.pdf]`
- `temp-move-or-delete/EFA/Mode opératoire - Process de passage de commande WeBuy.pdf`
- `temp-move-or-delete/EFA/PRESENTATION CREATION ET JOIE.docx[.pdf]`
- `temp-move-or-delete/EFA/EFA ACCADEMIE Logo png.png` and `EFA ACCADEMIE sur fonds Blancs.png` — these stay long enough to be base64-embedded into the render pipeline at P12.7 (logo asset paths are referenced by `_build_cover_html`), then deleted at P12.9 with a permanent copy stored alongside the canonical engagement folder under `_external_marks/efa-academie/`.
- `temp-move-or-delete/CV Fayçal Njoya En.pdf` — content extracted into `extracts/founder_cv_raw.txt` at P12.0 as the source for `FOUNDER_TRAJECTORY_INTERNAL.md`. Deleted at P12.9.

End of P12.0 voice corpus.
