---
artifact_kind: collaboration_intelligence_redacted
audience: internal
register: internal
classification: source-grade
language: en
phase: P12.0
date: 2026-05-10
sources_status: redacted_at_extraction; raw_transcripts_in_temp_move_or_delete_pending_deletion_at_p12_9
governance:
  - SOP-HLK_TRANSCRIPT_REDACTION_001
  - SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001
  - .cursor/rules/akos-governance-remediation.mdc
references_goipoi:
  - GOI-PRT-EFA-2026
  - POI-PRT-EFA-LEAD-2026
  - GOI-CUS-SUEZ-2026
  - POI-CUS-SUEZ-LEAD-2026
---

# P12.0 EFA collaboration intelligence (redacted)

> Internal source-grade note. Distilled from four EFA-side transcripts and one supporting PDF that live in `temp-move-or-delete/EFA/` pending deletion at P12.9. Strict redaction: no real first names; no client surnames; the EFA founder is referred to as "the EFA partner lead" or "the bridge / incumbent operator" depending on hat. Any cross-reference to internal AKOS canonicals uses `GOI-*` / `POI-*` ref_ids only.

## 1. Source inventory (off-repo)

| handle | shape | duration | what it gives us |
|:---|:---|:---|:---|
| `[EFA-T1]` | conversational onboarding (bridge ↔ founder) | 1h08 | EFA partner lead's understanding of Holistika's submark architecture (Holistika R&S / Think Big / HLK Tech Lab); confirmation that `Madeira` registers in her vocabulary; her own admin program reference; the reasoning behind the *"trois équipes, un seul objectif"* framing she likes. |
| `[EFA-T2]` | proposal briefing #3 (bridge ↔ founder) | 21m05 | **Pivotal turn.** Bridge proposes to add 3 Holistika slides + 1 EFA host slide to the proposal deck. She asks for visual brand-blending; she validates the violet/green softening of the dark Tech Lab brand. Founder commits to the EFA host card and asks her to send a vocal with what she wants the EFA slide to say. She agrees. |
| `[EFA-T3]` | WhatsApp 2026-05-10 18:20 (bridge solo voicemail) | 0m55 | **Volume signal:** *"...autour d'une cinquantaine à peu près par jour de commandes."* Litige causes (operator-voiced): factures sans numéro de commande; fournisseurs envoient avec frais en plus, frais de transport — *"ça ne colle pas et ça crée des retards."* |
| `[EFA-T4]` | WhatsApp 2026-05-10 18:21 (bridge solo voicemail, follow-up) | 0m04 | *"OK, je reste à l'écoute si tu as besoin d'infos."* — confirms availability for follow-up probing. |
| `[EFA-PDF1]` | Création et Joie internal presentation | n/a (slide doc) | EFA partner's *other* business: Création et Joie (her own fashion brand with sub-marks). Logo and brand language. **Not used in customer-facing surfaces** — only informs how we shape the EFA host card so it can later flex to a Création et Joie host posture in another engagement. |

## 2. Date audit (D-12-14)

The plan flags October 2025 (not 2026) as the start of the Holistika ↔ EFA collaboration. Cross-checked against transcript `[EFA-T1]`: founder narrates that the partner lead first asked him to help organize her business processes after seeing the v2.7 boilerplate; this turn predates the SUEZ engagement and aligns with an October-2025 inception. Confirmed: **collaboration since October 2025**.

Other dates surfaced in the transcripts (founder-side):
- IBM Business Analyst — Jul 2012 to Jul 2015 (CV-confirmed)
- Volvo Finance Operations — Mar 2018 to Mar 2020 (CV-confirmed)
- Europ Assistance / Generali — Apr 2022 to Aug 2023 (CV-confirmed)
- RCD Legal — Nov 2023 to current (CV-confirmed)
- Founder cohort onboarding for the EFA partner: she explicitly references Marcos and Vince (Holistika researchers) as collaborators she has met.

Holistika's "since-2025" framing in customer-pack metadata is therefore correct as a *partnership inception year*. No further date-drift surfaced.

## 3. Two-hat posture

The EFA partner lead operates in two distinct registers across these conversations, and the customer-facing artefacts must respect both:

| Hat | When it shows | Customer-pack consequence |
|:---|:---|:---|
| **Bridge / business developer** (the one she introduces herself as in `POI-PRT-EFA-LEAD-2026` notes) | When she walks Holistika into the SUEZ context, recommends slide structure, asks for the 3 Holistika slides. | She is **named on the proposal cover** as the collaboration partner (via EFA Académie), not as a person. Cover-strip carries `EN COLLABORATION AVEC EFA ACADÉMIE`. |
| **Incumbent operator** of the WeBuy procure-to-pay process (the one whose KPIs the proposal will improve) | When she describes the litige causes, the volume cadence, and her post-launch maintenance role. | She is referred to as **"la personne qui opère"** in slide 03 cell 04 and in the Continuité §3 — never named. Her operator voice anchors the litige reframe (D-12-15) without exposing identity. |

Both hats coexist on a single human; the customer pack must avoid conflating them in ways that would over-expose her or under-credit her contribution. The host-card on slide 02 (D-12-5) handles this: it cites EFA as the collaboration partner and references "the operator who runs this process today" without saying they are the same person.

## 4. Volume signal consolidation (D-12-13)

| Signal | Source | Use |
|:---|:---|:---|
| `~20/jour` | Bridge's earlier off-mic remark to founder ("twenty per day, but also fifty") | Conservative anchor; surfaces in `proposal.customer.fr.md` lead paragraph if the voice gate (P12.4) judges the range prose awkward. |
| `~50/jour` | `[EFA-T3]` verbatim *"autour d'une cinquantaine à peu près par jour de commandes"* | High-cadence anchor; surfaces as the upper bound of the range. |
| Range `20 ↔ 50/jour` | Plan D-12-13 synthesis | Lead-paragraph default with operating-rhythm gloss (*"selon la cadence du parc"*). Stat grid uses `20 ↔ 50` over `Demandes par jour, selon cadence du parc`. |

The downstream value-prop anchor is the FTE-equivalent (one full-time post consumed by the mechanic today; two at parc-doubling), which stays defensible at either end of the range.

## 5. Litige causes (operator-voiced, D-12-15 spine)

Verbatim from `[EFA-T3]`, redacted of any name reference:

> *"Et puis les litiges, les litiges qui sont dus aux factures qui arrivent sans numéro de commande, aux fournisseurs qui envoient avec des frais en plus, des frais de transport, des frais. Et du coup, ça ne colle pas et ça crée des retards. Voilà donc tout ça qui crée des relances."*

Three triggers, one consequence:

1. **Trigger A — facture sans numéro de commande.** PO-bypass at the supplier end; classic procurement-side litigation pattern.
2. **Trigger B — frais ajoutés hors devis.** Most often transport / FST / PMT line items the supplier adds without re-quoting; breaks the rapprochement automatique.
3. **Trigger C — fournisseur envoie un montant qui ne colle pas** (combination of A and B, or simple typing error).
4. **Consequence — la chaîne de relances.** The operator's time goes to chasing the supplier and reconciling, not to the original saisie. Payment is blocked the whole time → working-capital cost layered on top of the operational cost.

This is exactly the two-layer narrative the plan calls for in D-12-15: operational (relances time) + financial (trésorerie immobilisée). The customer pack will write to this without citing CDC sections.

## 6. Maintenance posture (D-12-4)

`[EFA-T2]` confirms: the EFA partner will handle post-launch maintenance of the automated solution as her continuation of the operator role. Two postures coexist in `proposal.customer.fr.md` §3 "Continuité opérationnelle":

- **Operator-led continuity** (default) — incumbent operator (anonymous) assumes maintenance of the automated chain post-handover. Holistika provides quarterly governance review. Pricing TBD post-discovery (depends on whether the maintenance scope is "patch + governance" or "patch + governance + new-feature pipeline").
- **Holistika-led continuity** (option) — Holistika carries maintenance directly under a recurring engagement. Higher cost-of-service; appropriate if the customer organisation prefers a single supplier covering build + run.

The customer-facing language: **"Mission portée conjointement"** (D-12-5 metadata) signals the mixed posture without forcing a choice in the proposal.

## 7. Brand-blending insight for slide 02 host-card (D-12-5)

`[EFA-T2]` includes a remarkable brand-design exchange. The bridge tells the founder she likes that he added violet and green to soften the previously all-black Tech Lab brand:

> *"Ah ouais, non, non, là, ça m'a attiré, en plus, le violet. Ouais, ouais, tout de suite, tu vois, ça, ça, ça fait, ça, ça change tout, quoi, parce que c'était vraiment noir, noir, noir, noir, noir."*

Her instinct here informs the **host-card color-bridge rule** in `BRAND_COBRANDING_PATTERN.md` (P12.2): the host (Holistika light variant) keeps its full palette; the guest (EFA Académie) contributes a single warm/neutral accent that softens the host canvas without collapsing the host palette. Specifically:

- Host palette: Holistika light variant (white canvas, teal accent, ink for body, slate for context).
- Guest accent: a single warm neutral lifted from the EFA Académie palette (the cream/beige tone visible in their print materials, not the saturated ones). Used once, on the host-card border or footer rule, not as a color block.
- Logo placement: EFA Académie logo at 0.7× host-monogram scale, centered in the card with min-padding 8mm.
- Typography: Inter throughout (host's typeface always — never EFA's display face on a Holistika-hosted surface).

This rule is generic, polarity-flippable, and codifies the bridge's own design instinct. P12.2 will write it up as the canonical.

## 8. Voice-corpus seed quotes (read across into voice-corpus.md)

Six representative passages from the EFA partner lead, useful as a *contrast comparator* against the founder's voice — confirming the EFA-side cadence is shorter, warmer, more anecdotal, and more validation-driven:

1. *"C'est important que le client est là et qu'il ait envie de rester."* — closing-the-meeting register
2. *"Il faut commencer par un et après on verra comment ça va se faire."* — pragmatic single-step register
3. *"Ah ouais, c'est sombre, c'est triste."* — sensory register, used in brand feedback
4. *"Ça c'est ce qui est bien. Ça prend du temps. C'est nickel, là, c'est bien."* — staccato approval register
5. *"Et puis ils aiment bien la preuve sociale."* — pragmatic-sales register; advice-giving
6. *"Ça nous permet après de rentrer bien en mode collaboration en mode voilà quoi."* — flow-into-work register

These are sourced as a comparator, not for copy-paste. Customer-pack prose stays in the founder's voice; EFA host-card prose may borrow her cadence for one or two sentences, with explicit operator approval at the P12.4 voice gate.

## 9. EFA's request for the proposal structure

`[EFA-T2]` makes the structural ask explicit:

> *"juste une seule slide création et joie avec les différentes les différentes marques de création et joie et voilà c'est tout mais juste sans trop et puis après tu mets deux slides sur toi par rapport au Lastika"*

Final agreed structure (ratified in `[EFA-T2]`, slide architecture per D-12-8):

| Slide | Purpose | Owner of voice |
|:---|:---|:---|
| 02 (NEW) | EFA host-card: who introduces this engagement | EFA partner lead's voice (cleared at voice gate) |
| 03 (NEW) | Holistika in three lines (no callable-network claim) | Founder's voice |
| 04 (NEW) | Deux récits, une seule discipline (method anchors) | Founder's voice |
| 05 (NEW) | How we work today (KM + AKOS-MADEIRA orchestration) | Founder's voice |
| 06-13 | Existing 02-09 renumbered; cover stays at 01 | Founder's voice |

`slide_count: 13`. Confirmed.

## 10. EFA's request for personal credentials (and operator-corrected re-framing)

`[EFA-T2]` extensively encourages the founder to use personal credentials (L'Oréal, IBM, Volvo, Generali) as social proof on slide 03:

> *"Aujourd'hui, nous travaillons avec des groupes comme L'Oréal. Ils aiment bien ça tout de suite."*
> *"Donc, tu vois, tu dis voilà, je m'appelle Faisal Julia, je suis un opérationnel comme Aïcha vient de le dire. J'ai travaillé, tu donnes tes références."*

The operator's correction (recorded in the transcript with the parent agent of this engagement):

> "I prefer my customer-facing slides to put weight on Holistika as a brand, not on me as an individual. The CV content goes into the founder bio and other related artefacts; not on customer slides."

**Resolution per D-12-1 + D-12-2:**

- Slide 03 closes on what is true *now*: research-first method, six-axis ops, governed delivery. **Zero personal name on the customer-pack surfaces.**
- Slide 04 reframes as *Deux récits, une seule discipline* — three method-anchors derived from career-shaped intuitions (data-quality discipline; multinational governance; PMP-to-software discipline). Names are abstracted to method names. Real employer names live in the internal trajectory file (P12.0 sibling artefact, see §11).
- Network claim explicitly retired (D-12-2 revision): no *"réseau de praticiens senior mobilisable"* phrasing.

## 11. FOUNDER trajectory architecture decision (deviation from plan literal)

The plan's D-12-9 specifies an **internal-only** trajectory file at `docs/references/hlk/v3.0/Admin/O5-1/People/FOUNDER_BIO.md`. The existing file at that path is ratified `register: external` / `access_level: 4` and serves as the canonical external bio (used in decks, press kit, recruiter materials, advisor briefs). It is `status: active` and governed by `SOP-PEOPLE_FOUNDER_BIO_001`.

**Deviation:** rather than overwriting an active external canonical, P12.0 creates a sibling file at the same role-folder root:

- `docs/references/hlk/v3.0/Admin/O5-1/People/FOUNDER_TRAJECTORY_INTERNAL.md` — `register: internal`, `access_level: 5`, brand-jargon allowed, real employer names allowed (subject to standard SOP-HLK_TRANSCRIPT_REDACTION_001 and SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001 rules for *third-party* private names). This file carries the IBM 2014 / L'Oréal Data Quality / Volvo Finance Ops / Generali / RCD trajectory and the intellectual-influence narrative.

The two files coexist:

| File | Register | Audience | Real employer names? | Brand jargon? |
|:---|:---|:---|:---|:---|
| `FOUNDER_BIO.md` (existing) | external | decks, press kit, public bio variants | NO (anonymized) | NO |
| `FOUNDER_TRAJECTORY_INTERNAL.md` (new at P12.0 draft, finalized P12.9) | internal | operator + agent only | YES (PUBLIC names: IBM, Volvo, Generali; private third-party names redacted per SOP) | YES |

Rationale documented in the P12.9 closing checkpoint. The plan's intent (D-12-9) is fully served; only the file name changes to avoid clobbering an active canonical.

## 12. Open items to test at the voice gate (P12.4)

- Whether the EFA host-card uses the bridge's verbatim cadence (e.g. *"Holistika apporte les procès des grosses boîtes pour les rendre opérables chez les petites et moyennes"*) or a Holistika-styled paraphrase. Operator picks at P12.4.
- Whether the volume-range prose stays as `vingt à une cinquantaine de demandes par jour selon la cadence du parc` (option C) or reverts to `~20 conservative` (option B fallback). Operator picks at P12.4.
- Whether the litige pull-quote stays triadic (*"Automatiser ce qui se calcule, prévenir ce qui se rompt, préserver ce qui se juge"*) on the slide cover, or whether the cover keeps the binary version and the triadic appears only in the proposal. Operator picks at P12.4.

End of P12.0 EFA-redacted intelligence.
