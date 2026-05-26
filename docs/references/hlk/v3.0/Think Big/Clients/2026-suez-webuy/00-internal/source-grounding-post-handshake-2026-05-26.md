---
intellectual_kind: source_grounding_note
sharing_label: internal_only
access_level: 5
audience: J-OP
register: internal
language: en
program_id: ENG-SUEZ-WEBUY-2026
engagement_slug: 2026-suez-webuy
authored: 2026-05-26
last_review: 2026-05-26
authoring_session: I86 cluster Wave R+2 doctrine-rewrite — post-handshake debrief ingestion
ratifying_decisions:
  - D-IH-86-EJ  # SUEZ recommercialisation (4-base + 1-overlay enum landed in Commit 1)
  - D-IH-86-EK  # methodology-readiness axis (Commit 1)
  - D-IH-86-EL  # bd_commission_overlay shape (Commit 1)
  - D-IH-86-EM  # 13th specialty demotion to charter pending recommercialisation (Commit 1)
  - D-IH-86-EN  # supersede chain for D-IH-86-DA/DF (Commit 1)
status: active
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md
linked_artifacts:
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-grounding-2026-05-22.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/2026-05-13-suez-customer-meeting.mp3.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/2026-05-13-post-handshake-efa-holistika-debrief.m4a.md
linked_decisions:
  - D-IH-86-EJ
  - D-IH-86-EK
  - D-IH-86-EL
  - D-IH-86-EM
  - D-IH-86-EN
forward_charters:
  - Mint EFA partnership-convention template + 5-slide EFA proposal template under canonical templates (§3.3 + §3.4)
  - Promote pre-send regression gate to discipline-class artifact when 2-3 worked examples accumulate (cross-ref pre-send-regression-gate-spec-2026-05-26.md)
  - Document operator's "vends le savoir-faire" sales discipline as Marketing/Resonance pattern row (§4.4)
  - Mint operator's "no client screenshot" IP-protection principle as Legal canonical (§4.2)
---

# SUEZ POC — post-handshake debrief findings (2026-05-26)

## Why this note exists

This is the **second** SUEZ grounding note. Section 1 of [`source-grounding-2026-05-22.md`](source-grounding-2026-05-22.md) is the original 2026-05-22 regrounding (verified-from-primary-source) + §9 is the 2026-05-22 evening EFA folder discovery. This note drains the **post-handshake EFA-Holistika debrief of 2026-05-13** (a 21-minute audio recorded ~30 min after the customer handshake meeting), which was NOT in scope of either prior drain because the audio binary was still at repo root awaiting transcription.

The transcript landed at canonical path 2026-05-26 04:36 UTC after a ~21 min Whisper-small CPU pass (1752 segments / 52,704 chars). The binary was migrated from repo root to the canonical transcripts folder in the same session (gitignored per `.gitignore:167:*.m4a` — the `.md` transcript is the SSOT).

**Load-bearing for Wave R+2 doctrine rewrite Commit 2+** because the substrate materially shifts what the SUEZ "commercial frame" actually looks like in lived practice — confirming the operator's `consulting_direct + bd_commission_overlay` framing already landed in Commit 1, but adding a **separate EFA-to-SUEZ invoice stream** (5 k€/month maintenance contract) that Holistika does not share in.

## Section 1 — Two distinct commercial streams, two distinct invoicing entities

The transcript names two parallel B2B revenue streams flowing from SUEZ:

| Stream | Invoicing entity | Service | Pricing today | Holistika participation |
|:---|:---|:---|:---|:---|
| **Stream A — Automation project** | Holistika (operator-led; Aïsha as BD intro) | Cadrage → Prototype → Industrialisation per `tarification.customer.fr.md` (3 variants 38k / 53k / 87k) | Customer-pack rates | 94% revenue net of `bd_commission_overlay` to Aïsha |
| **Stream B — Operational continuity** | EFA (Aïsha's sole-trader) | Continuation of current saisie + future operator-of-the-automated-system role | 5 k€ / mois (proposed by Aïsha; SUEZ asked for written offer next week) | **ZERO** (this is Aïsha's standalone B2B contract with SUEZ; Holistika is not party) |

Operator's verbatim coaching to Aïsha on Stream B: *"il faut que j'assure cette partie maintenance que nous, on assure cette partie automatisation, et qu'on fasse que c'est deux choses différentes, en fait"* + *"je vais continuer les saisies, indépendamment de l'automatisation… et après, du coup, ça viendra comme une suite, en fait."*

### 1.1 What this means for the 13th specialty doctrine

The current Commit 1 doctrine rewrite correctly demoted SUEZ to `consulting_direct + bd_commission_overlay`. **It does NOT need to also encode Stream B** — Stream B is not a Holistika engagement, it is Aïsha's separate sole-trader contract. The 13th specialty's `COLLABORATOR_SHARE_REGISTRY` does NOT row for Stream B because there is no share to compute (100% goes to Aïsha; Holistika is not invoiced and does not invoice).

However, the doctrine SHOULD acknowledge **cobranding** as a discipline-level concern: the 5-slide EFA proposal (§3) is EFA-branded but appears as part of the same SUEZ engagement scope from SUEZ's perspective. This is a brand-coexistence concern, not a revenue-split concern.

## Section 2 — Customer (SUEZ) decision-pattern intelligence

### 2.1 The decisionmaker chain

- **M. Régal** — "le bras droit de la directrice" — the actual decisionnaire. The 2026-05-13 handshake meeting was with a technical interlocutor (not decisionnaire). Forward path = touch Régal at next meeting.
- **DSI (CIO/IT director)** — *"peut-être que la DSI, c'est pas dans le projet, ils ne connaissent pas tout ça"* — not yet briefed on the automation scope. Next-meeting (in ~2 weeks per the customer-meeting transcript landed prior session) MUST include DSI for technical pre-validation.
- **Brian** — newly-appointed "responsable performance" (~6 months in role; ex-Banque Populaire); has cross-process visibility. Operator + Aïsha will schedule a 1-hour Teams call with him next week to map the workflow handoffs between gestionnaires d'intervention + techniciens + responsable maintenance + responsable réglementaire.

### 2.2 The interlocutor's explicit asks (verbatim)

1. *"Faites-nous quelque chose de concret, d'ici une semaine, pour cette partie maintenance"* → EFA 5-page proposal next week (Stream B).
2. *"Faites-nous une proposition écrite et concrète"* → Holistika cadrage proposal (Stream A; already drafted as `proposal.customer.fr.md`).
3. *"Comment on fait, parce que là, juin, juillet, ça va être les vacances, tout le monde s'en va, septembre, ça va être fini"* → SUEZ wants both proposals committed BEFORE summer break; September = decision window. Aligns with our 27-28/05 SUEZ ship target.
4. Implicit (operator's reading of Régal): *"je voudrais vraiment vous aider à sécuriser cette partie-là"* → Régal will champion Stream B continuity as the door-opener for Stream A automation.

### 2.3 SUEZ pain-point validation

The transcript confirms what the customer-meeting transcript (`2026-05-13-suez-customer-meeting.mp3.md`) named:

- **3 gestionnaires d'intervention for all France** (under-staffed; already asked for a 4th; would need a 5th but management refuses cost). *"Ils sont prêts à craquer au mois de juillet."*
- **Litiges** (dispute management) — the **F·05 module** in `deck.customer.fr.md` slide 09 is genuinely load-bearing: *"les causes des litiges, yatsous"* + *"il y a des allers-retours qui se font entre eux et les fournisseurs."* Operator's framing *"litige c'est un coup caché"* was received well.
- **Réglementaire** (regulatory control inspections) — 700+ machines with mandatory contrôles techniques. A separate person handles this stream; cost-leakage suspected when fournisseurs invoice for both maintenance AND contrôle without cross-check.

## Section 3 — Brand + cobranding architecture (operator's voice)

### 3.1 The 5-slide EFA-branded proposal (operator coached Aïsha live)

Operator dictated a 5-slide structure for Aïsha's EFA-to-SUEZ Stream B proposal — slide-by-slide:

| Slide | Content | Visual treatment |
|:---|:---|:---|
| **1 — Cover** | EFA proposal title page | EFA dark-green background + cream-white (blanc cassé) typography; thin sans-serif lettering; small green accents (*"vers obscure que tu as et le balcon"*) |
| **2 — Your world** | Aïsha's positioning: who EFA is, what her domain is (saisie + maintenance opérationnelle). NO PHOTO (Aïsha doesn't like). Mirror the operator's own "World" slide convention. | Cream background; the EFA "world" element (the typical anchor she uses in her docs) |
| **3 — Pourquoi + Procès** | TWO-COLUMN layout: **Left (narrow)** = 3 problem statements + 3 horizontal numeric facts (commandes per period, etc.) at bottom. **Right (wider)** = 5 cadres (frames) titled by procès name, mirroring the CDC sommaire structure. | Cream + green accents |
| **4 — Proposition économique** | The 5 k€/month line + scope cap + exclusions | Cream + tarification block |
| **5 — Contre-couverture** | Mirror of slide 1 | EFA dark-green |

**Key operator coaching points to Aïsha**:
- *"Ce qu'on rajoute en plus le fait de j'ai des comptes Microsoft… on a tout activé… les composants qu'on a vus ensemble en France"* — operator explicitly does NOT want EFA proposal to depend on Holistika Microsoft tenant; EFA stands alone.
- *"Une fois que j'ai fait mes slides, je demande de me générer la propose à l'FESAN [Affaires]"* — slides first, full multi-page proposal as second artifact (auto-generated from slides via Madeira/Claude).
- *"Une convention de partenariat"* needed in parallel — formal Holistika ↔ EFA partnership document explicit to SUEZ (operator offered to draft from existing exports template).

### 3.2 The "no client screenshot" IP-protection principle (operator NEVER ratified compromise on this)

Aïsha proposed showing IBM / L'Oréal / Volvo case-study screenshots from prior consulting work to convince SUEZ. **Operator categorically refused** — verbatim, three times for emphasis:

> *"Je peux pas montrer ça… je pourrais jamais faire une photo à un cas usage d'IBM. Et spécialement d'IBM."*
> *"Je peux pas faire un screenshot. Je peux pas faire un screenshot. Et même pas, comme tu disais, pour lever la marque. Non, non, je peux pas faire un screenshot."*
> *"J'explique bien, je lui ai dit je peux pas porter des images de mes clients. Et c'est vrai, je peux pas faire un screenshot."*

**Counter-strategy operator named** (load-bearing for FUTURE use-case demos):
- Operator has Microsoft / Google / multiple-vendor accounts activated on his own tenant.
- Operator will **build the use-case demos using his own tenant** with anonymized but realistic data — NOT extract screenshots from prior client work.
- *"On est dans la création des cas usage plutôt"* — create-from-scratch new cas usage rather than extract-from-history.

**Forward-charter to Legal canonical**: this principle should be promoted to a Legal canonical (Sub-area: IP / Confidentiality / Client-data-handling) as a binding rule for ALL future sales materials. Tentative location: `docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/SOP-NO_CLIENT_ARTIFACT_EXTRACTION_001.md`.

### 3.3 The cobranding model + EFA brand evolution forward-pointer

Operator's verbatim framing: *"il a compris que c'est un co-branque que tu avais la contrainte de passer en partenariat après, que tu as décidé, aller voir un externe."* The interlocutor at SUEZ already understands the cobrand shape.

EFA brand maturity status today: *"je suis en train de l'améliorer pour pouvoir faire. Donc c'est seulement parce que c'est très tôt. Mais si c'était pour juin, à partir de juin, comptes avec ça."*

→ **EFA brand evolution window = June 2026**. Operator offered: *"je voudrais qu'on… l'agence à la maison… j'ai pensé à toi tout le temps"* — Holistika to operate as EFA's brand agency (in-house) from June 2026 forward. This is a forward-charter for both Marketing/Resonance (brand-agency service offering) AND for the EFA partnership shape (deeper integration once brand is mature).

### 3.4 The 6-domain diagram opener works (Aïsha's verbatim feedback)

Operator's *"6 cadrans / 6 domains"* opener — the diagram operator shows at the start of every deck — was explicitly praised by Aïsha as load-bearing in the SUEZ meeting:

> *"c'est bien de présenter les six facteurs pour que les entreprises voient bien qu'on n'est pas en train de révoler [survoler]. Parce que ça, ça m'a transformé de savoir que voilà, t'es dans l'opérationnel et t'as oublié de regarder les finances, t'as oublié de regarder ça, t'as oublié de regarder ça."*

This is empirical validation of `BRAND_ARCHITECTURE.md` "Branded House — 6-domain Holistika frame" as the right opener for B2B SME prospect meetings. Cite as worked example in next brand-canon amendment.

## Section 4 — Operator's sales discipline (load-bearing patterns surfaced)

### 4.1 *"On est à plusieurs"* — never sell as solo founder

> *"Pour lui, pour justifier ça, il faut toujours dire qu'on est à plusieurs. Sinon, c'est pas croyable… nous, on a des ingénieurs qui vont sortir la solution, bien sûr."*

Holistika sales discipline = always present as a team (founder + engineering + research + brand) even when execution is solo. Aligns with `akos-people-discipline-of-disciplines.mdc` Rule 1 + the 6-domain Branded House frame. Cite this as worked example in the Marketing/Reach BD lifecycle SOP.

### 4.2 *"Quand le client te dit la même chose que ton partenaire"*

> *"Quand tu dis la même chose que moi, j'écoutais de lui, comme aujourd'hui… Si quelqu'un a ta maison, parle comme ton client, ça veut dire que tu es bien."*

Operator's sales-confidence diagnostic: when the customer + the partner-collaborator + the founder converge on the same problem statement independently, the methodology is well-grounded. Empirical confirmation pattern. Forward-charter to Marketing/Resonance as a SALES_CONFIDENCE_DIAGNOSTIC pattern row.

### 4.3 *"Tu vends ta capacité, pas un produit fini"*

> *"Surtout, je veux que tu vends de la capacité de Holistika de les faire. Il faut que tu vends de le faire. Si tu veux que l'on d'un ici, il faut vendre notre savoir-faire."*

Methodology-first sales discipline (already a 14th specialty SYNTHESIS_BEFORE_TRANCHE design intent). Reinforces the methodology-readiness axis just landed in Commit 1 of the doctrine rewrite. Cite as worked example in `SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` §3.

### 4.4 *"Vends le savoir-faire"* anti-pattern: technical jargon in sales

Operator self-corrected during the debrief: *"des choses comme ne parle pas technique, les choses comme ça, que je m'en sais, qui sont mes défauts. Ce qu'il faut faire, ce qu'il faut faire."* — operator's own brand rules to Madeira/Claude include "ne parle pas technique," acknowledged as a recurring defect.

This is empirical evidence that the `akos-brand-baseline-reality.mdc` dual-register rule (internal CORPINT vocabulary vs translated external) is correctly load-bearing — and that operator self-awareness on it is high but not always self-enforced under pressure. Forward-charter to brand drift gate: extend `validate_brand_baseline_reality_drift.py` to scan SUEZ + EFA-cobranded artifacts at pre-send time.

## Section 5 — SUEZ use-case demo strategy (forward-charter)

The transcript confirms 2 use-case demos as the highest-leverage Stream A deliverable:

| Demo | Source slide / CDC reference | Operator framing | Anonymisation strategy |
|:---|:---|:---|:---|
| **Demo 1 — Libellé generator** | `deck.customer.fr.md` slide 09 F·02 + `cdc-feasibility-shape.fr.md` §9 Phase 1 | Excel template + Power Automate flow + Power Apps form wireframe; 5-component composition logic per the deck's worked example | Generic supplier names (Fournisseur-Alpha-001, etc.); SUEZ-realistic but never SUEZ-actual data |
| **Demo 2 — Dispute register + litigation prevention** | `deck.customer.fr.md` slide 09 F·05 | Intake form + classification flow + litigation-detection-heuristic + operator dashboard mockup | Same — operator's own Microsoft tenant; anonymized supplier + product names |

Authoring deferred per Commit 4 D-IH-86-EH artifact-shape ratification (post-commercial-close cycle) — but the operator now wants them mentioned in the SUEZ follow-up cover email as "coming next" to elevate the "vends le savoir-faire" framing. Forward-pointer to `suez-use-case-demo-authoring` todo (post-doctrine-rewrite cycle).

## Section 6 — Pre-send regression gate (operator's verbatim mandate)

Operator at session open: *"bear in mind I agree with you and we need a regression everytime (now that we still haven't sent anything)."*

This codifies a **NEW discipline**: before any external send to SUEZ (or any external recipient), a composite regression sweep runs over the candidate artifact + the engagement's full source-grounding state. The sweep spec is at:

→ [`docs/wip/planning/86-initiative-cluster-execution-coordinator/pre-send-regression-gate-spec-2026-05-26.md`](../../../../../../../wip/planning/86-initiative-cluster-execution-coordinator/pre-send-regression-gate-spec-2026-05-26.md)

The sweep composes the existing specialty validators in a specific order: brand-baseline-reality drift → external-render-trail freshness → collaborator-share CS-01..CS-08 → synthesis-before-tranche (when applicable) → grounding-vs-latest-transcripts (NEW probe). FAIL on any layer blocks the send.

This is a candidate **15th Quality Fabric specialty** in the making. INFO ramp at first instantiation; promotes to discipline-class doctrine once 2-3 worked examples accumulate (SUEZ being #1 candidate).

## Section 7 — What this changes for Commits 2-7 of the doctrine rewrite

Commit 1 already landed (sha 5cd9793) and correctly demoted COLLABORATOR_SHARE doctrine + amended `share_pattern` enum to 4 base + 1 overlay + added methodology-readiness axis + ratified D-IH-86-EJ/EK/EL/EM/EN. Post-handshake findings **CONFIRM** that landing but add the following NEW gates for the remaining commits:

| Commit | Existing scope | NEW addition from post-handshake findings |
|:---|:---|:---|
| **Commit 2 — Pydantic chassis update** | 4-value enum + bd_commission_overlay Literal + methodology_readiness Literal + overlay_pct_deviation extension | NEW: explicit `parallel_invoice_stream_indicator: Optional[bool]` field on SHARE_REGISTRY to flag engagements where a collaborator has an INDEPENDENT B2B invoice stream with the customer that Holistika is not party to (Stream B at SUEZ; clarifies CS-03 scope) |
| **Commit 3 — Validator CS-09** | Bd_commission_overlay + methodology_readiness coherence check | Same — no change. CS-09 stays scoped to overlay + readiness coherence only |
| **Commit 4 — Cursor rule + skill + SOP** | RULE 1/3/5 update + new RULE 6 (overlay stacking) | NEW: add **RULE 7 — parallel invoice streams** to `akos-collaborator-share.mdc`, naming that a collaborator's INDEPENDENT B2B contract with the same customer is OUT OF SCOPE for SHARE_REGISTRY and is documented in the engagement folder's `00-internal/source-grounding-*.md` instead |
| **Commit 5 — Registries + supersede decisions** | DECISION_REGISTER supersede + SHARE_REGISTRY SUEZ rows + HOLISTIKA_QUALITY_FABRIC §6 + PRECEDENCE + CHANGELOG | NEW: SHARE_REGISTRY rows for SUEZ now carry `parallel_invoice_stream_indicator=true` + free-text note pointing at Stream B EFA contract |
| **Commit 6 — Supabase mirror DDL** | ALTER TABLE CHECK enum + ADD COLUMN share_overlay | NEW: ADD COLUMN `parallel_invoice_stream_indicator BOOLEAN DEFAULT FALSE` to `collaborator_share_registry_mirror` |
| **Commit 7 — Closing-loop verification** | Full pytest + ReadLints + validate_hlk + synthesis_before_tranche --check-charter + files-modified +30 + scratchpad drain | NEW: also run the pre-send regression sweep against the SUEZ customer pack as a worked example of the new gate spec'd in §6 |

## Section 8 — Cross-references

- Prior grounding note: [`source-grounding-2026-05-22.md`](source-grounding-2026-05-22.md) §1-9 (original regrounding + EFA folder discovery)
- Companion transcript landed prior session: [`source-materials/transcripts/2026-05-13-suez-customer-meeting.mp3.md`](source-materials/transcripts/2026-05-13-suez-customer-meeting.mp3.md)
- THIS post-handshake transcript: [`source-materials/transcripts/2026-05-13-post-handshake-efa-holistika-debrief.m4a.md`](source-materials/transcripts/2026-05-13-post-handshake-efa-holistika-debrief.m4a.md)
- Customer pack (already shipped at customer meeting): [`02-customer-pack/`](../02-customer-pack/)
- Pre-send regression gate spec: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/pre-send-regression-gate-spec-2026-05-26.md`](../../../../../../../wip/planning/86-initiative-cluster-execution-coordinator/pre-send-regression-gate-spec-2026-05-26.md)
- Commit 1 atomic commit: `5cd9793` (Wave R+2 doctrine-rewrite Commit 1; landed prior cycle)
- Wave R+2 tranche charter: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-2-doctrine-rewrite-collaborator-share-4-base-1-overlay.md`](../../../../../../../wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-2-doctrine-rewrite-collaborator-share-4-base-1-overlay.md)
- Decision lineage: D-IH-86-EJ (SUEZ recommercialisation) + EK (methodology-readiness) + EL (bd_commission_overlay) + EM (13th demotion to charter) + EN (supersede chain) — all status=active in DECISION_REGISTER.csv per Commit 1.

