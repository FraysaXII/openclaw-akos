---
intellectual_kind: source_grounding_note
sharing_label: internal_only
access_level: 5
audience: J-OP
register: internal
language: en
program_id: ENG-SUEZ-WEBUY-2026
engagement_slug: 2026-suez-webuy
authored: 2026-05-22
last_review: 2026-05-22
authoring_session: I86 cluster Wave R+1 P3 SUEZ POC FULL KIT regrounding
ratifying_decisions:
  - D-IH-86-DA  # 13th specialty doctrine mint (currently at status=active; this note initiates the supersede track)
  - D-IH-86-DE  # share_pattern enum extension (3-value)
  - D-IH-86-EA  # 14th specialty doctrine mint
status: active
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md
linked_artifacts:
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/deck.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/proposal.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/tarification.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/gantt.customer.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/01-operator-pack/cdc-feasibility-shape.fr.md
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-03.m4a.md
---

# SUEZ POC — source-grounding note (2026-05-22)

## Why this note exists

This session opened with a session-summary based on stale assumptions. The operator's correction surfaced four classes of drift:

1. The commercial frame for Aïsha-on-SUEZ was wrong in two prior session ratifies (first 6%-broker, then 35%-deep-partner). Today's ground truth is **`custom`** with a methodology-readiness narrative.
2. The customer-facing pack was **already built, rendered, and shown at a customer meeting** that I had no record of. My prior session was drafting from a pre-pitch assumption.
3. The architecture-addendum + cover-email I drafted this session **duplicate** the already-shown deck and CDC.
4. Two specialty active-promotions (13th = COLLABORATOR_SHARE; the 14th's worked-example #3 application) are anchored on the wrong SUEZ commercial example and must be reversed.

This note locks the ground truth as a durable internal artifact so future regrounding does not require re-reading transcripts.

## Section 1 — Verified from primary source

### 1.1 The customer meeting happened

- **Customer-pack render manifest** at `_exports/render-manifest.json` dated `issue_date: 2026-05-12` lists 7 rendered PDFs with sha256, all in `_exports/`. The customer pack was rendered and packaged 13 days before this regrounding session.
- **`deck.customer.fr.md`** carries `last_review: 2026-05-12`, `slide_count: 14`, `audience: customer`, `status: active`. Slide 02 names "Continuité d'opération depuis octobre 2025." Slide 09 names F·02 (Générateur de libellé, 5-component) + F·05 (Module de prévention et gestion des litiges).
- The operator stated this session: *"the export I've shown the customer deck and it's not here. Also we didn't get why so many redundant items."* — the deck IS here (`02-customer-pack/deck.customer.fr.md` + `_exports/deck.customer.fr.pdf`); the redundancy concern is that the architecture-addendum drafted this session repeats slide 08 (the 4-temps flow) + slide 10 (the 5-temps method) + CDC §9 Phase 1/2/3.

### 1.2 Aïsha's role per transcript-03 (the only usable transcript)

`00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-03.m4a.md` — transcript date metadata likely mis-labeled 2026 (real date probably 2025-12-12 per the "October 2025" since-date in the proposal). Briefing-01 transcript is **corrupted** (21 lines of audio-misrecognized noise) and not usable.

Aïsha's actual role per the transcript + operator's 2026-05-22 framing:

- **Brought the SUEZ deal** as introducer / business developer.
- **Content-coached** the proposal narrative (transcript-03: content review + tone calibration).
- **Will provide operational continuity** post-deployment as the operator who currently runs the WeBuy process at SUEZ.
- **Does NOT yet operate the Holistika methodology** the way Holistika does. Operator verbatim 2026-05-22: *"she can't follow our methodology the way we are and that is also a pending point in our KB so it's known because it's bound to happen with more people."*
- **Future deal pipeline** (tontine + others) discussed in transcript-03 but commercially uncommitted.

### 1.3 SUEZ commercial frame per `tarification.customer.fr.md`

- Variant A (Cadrage): **38,500 €** fixed-price
- Variant B (Prototype, recommended): **53,500 €** fixed-price
- Variant C (Industrialisation): **87,000 €** fixed-price
- Payment 30 / 40 / 30
- NDA + DPA
- Liability cap = mission amount
- **Holistika prime-bills SUEZ direct.** No broker/partner structure exposed to SUEZ. EFA Académie appears as "partenaire d'introduction et de continuité opérationnelle" on cover + slide 02 only.

### 1.4 What SUEZ DSI actually asked for (operator's 2026-05-22 framing)

- *"they actually asked if we don't have any screenshot we can add or something we can show or a demo even to see it works and then let us do the thing in their systems after winning over their DSI"*
- **The single net-new deliverable SUEZ DSI is waiting on**: the Excel + Power Query libellé generator demo (live or screenshot-shown) per CDC §9 Phase 1 + deck slide 09 F·02.

## Section 2 — Ground truth on the commercial model

### 2.1 The three commercial shapes (corrected from prior session)

| Shape | When it applies | Aïsha-on-SUEZ fit? |
|:---|:---|:---|
| `deep_partner_65_35` | Collaborator operates Holistika methodology + brings the deal + holds ongoing maintenance. Holistika contributes methodology + machinery + execution stack as value of its 65%. | ❌ Methodology-readiness gap — Aïsha cannot yet operate the methodology the way Holistika does. The 35% would be aspirational, not earned. |
| `orchestration_broker_thin_margin` (~6%) | Multiple billed collaborators (founder + ≥ 1 partner) share the bulk of revenue; Holistika orchestrates as thin-margin broker. | ❌ Operator rejected this at 2026-05-22: *"6% is unknown to me, like I would accept that... I would never accept to take over the operations of a business for less than 65%"*. |
| `custom` (mandatory override decision) | Neither pattern fits cleanly; commercial shape narrated in an override decision row. | ✅ This is the right shape for SUEZ #1. |

### 2.2 The methodology-readiness axis (NEW; doctrine amendment required)

Operator verbatim 2026-05-22: *"what's also there is me compromising for that 35% and I don't lie, so yeah. You see, we lose value if we don't have things ready because in reality A was correct. You understand me now and why it's D in the end but only because our backlog prevents us from shining."*

Translation:

- The doctrine's `deep_partner_65_35` pattern **silently assumes methodology-readiness** — that the collaborator can fully operate the Holistika method and earn the 35%.
- When the collaborator cannot yet operate the methodology (Aïsha case; future SUEZ-shaped cases), the relationship routes via **`custom`** + paid-services-billed for the collaborator's actual time + an optional BD-overlay if they brought the deal.
- The compromise the founder makes (accepting a less-than-ideal shape because the methodology isn't yet packaged for collaborator-operation) is itself a recurring pattern that should be **first-class in the doctrine**, not a one-off.
- This is the **pending KB item** the operator named — methodology-readiness as a doctrine axis is one of the gaps that prevents Holistika from "shining."

### 2.3 Concrete SUEZ #1 commercial shape

- **Holistika** prime-bills SUEZ at the variant price (53,500 € for variant B).
- **Aïsha** receives compensation for continuity-operator work as a paid-services line (`HOLISTIKA_VENDOR_SERVICES_BILLED.csv` row, classed as `operational_continuity_support` or similar; mode `bill_mode_decision_id` referencing this engagement override).
- **Aïsha** receives a **+15% BD margin overlay** on Holistika's post-cost margin for bringing the SUEZ deal (separate from revenue-share; paid from Holistika's margin, not exposed to SUEZ).
- **Future Aïsha collaborations** (tontine + others) get a separate `engagement_id` per engagement; commercial shape ratified per engagement; the methodology-readiness gate determines whether they route via `custom` or `deep_partner_65_35` at that point.

## Section 3 — What's redundant in this session's drafts

### 3.1 `architecture-addendum.fr.md` — drop or rescope

The drafted addendum overlaps:

- Deck slide 08 (4-temps flow) — duplicates the addendum's "Phase 1 architecture" diagram.
- Deck slide 10 (5-temps method) — duplicates the addendum's "method timeline."
- CDC `cdc-feasibility-shape.fr.md` §9 (Prototype léger Excel/Power Query, Phase 1) — duplicates the addendum's Phase 1/2/3 framing.

**Recommended disposition** (pending operator confirm): **drop the addendum entirely.** The 3-surface ERP-engagement-governance design (operator dashboard / supervisor dashboard / ERP workflow join) — if SUEZ needs it surfaced — belongs as a **CDC §9 amendment** or a **deck slide 09 sixth-cell** rather than as a standalone addendum.

### 3.2 `cover-email-2026-05-27.fr.md` — rewrite as follow-up, not pitch-send

The current draft frames the send as a pitch attachment ("here is our proposal + tarification + architecture"). The customer meeting already happened. The right framing is:

- **Acknowledge the meeting** (date + thanks).
- **Surface the Excel demo** as the net-new deliverable answering DSI's "show me it works" ask.
- **Soft-prompt** for the variant choice (A/B/C) per slide 13 closing.
- **Soften** "partenaire opérationnel" → "partenaire d'introduction et de continuité opérationnelle" per operator 2026-05-22 Q2 ratify.

## Section 4 — What's wrong in the in-flight CSV/decision rows

### 4.1 SHARE_REGISTRY rows to rewrite

Current 4 rows authored at Commit 4 (sha 50200c8): 3 orchestration_broker + 1 deep_partner across 2 engagement_ids. **All four are based on the superseded prior-session Q-B ratify.**

Correct rewrite shape:

- **1 SHARE_REGISTRY row** for engagement_id `ENG-SUEZ-WEBUY-2026`, `share_pattern: custom`, with `share_override_decision_id` pointing to a NEW decision row narrating the methodology-readiness + BD-overlay shape from §2.3 above.
- **1 VENDOR_SERVICES_BILLED row** for Aïsha's operational-continuity hours (rate + estimated hours per variant).
- **0 rows** for the second `engagement_id` (no Aïsha-on-future-deals yet; future engagements get their own SHARE_REGISTRY at chartering time).

### 4.2 Decision rows to supersede

- **D-IH-86-DF** (13th specialty active-promotion based on wrong SUEZ worked example) → mark `superseded`; mint successor decision once `custom`-pattern Aïsha-on-SUEZ worked example replaces it.
- **D-IH-86-EG** (splits anchor) → mark `superseded`; same successor cycle.
- **D-IH-86-DF / EF / EG / EH / EI quintet** authored at Commit 4 — review row-by-row; supersede the ones citing the wrong shape.

### 4.3 13th specialty demotion

`COLLABORATOR_SHARE_DOCTRINE.md` frontmatter currently at `status: active` (per D-IH-86-DF ratify at Commit 4). Demote back to `status: charter` until:

1. Methodology-readiness axis is added to §2.3 of the doctrine (new sub-section + worked example).
2. SUEZ #1 `custom`-pattern application is re-authored as worked example #1 + lands cleanly through validators.
3. Operator re-ratifies active-promotion via NEW decision row (e.g., D-IH-86-DF-V2).

## Section 5 — What's actually missing for SUEZ ship (corrected)

In execution priority order:

1. **Excel + Power Query libellé generator** — real `.xlsx` with the 5-component naming rule (catégorie, engin, type d'intervention, fournisseur, référence) per deck slide 09 F·02 + CDC F-05. Tested against 4-10 fixture demands. Screenshots + optional Loom walkthrough.
2. **Follow-up cover-email** (rewrite per §3.2) bundling: demo + reference to the pack already shown + soft-prompt for variant choice.
3. **Doctrine amendment** — add methodology-readiness axis to COLLABORATOR_SHARE_DOCTRINE §2.3 + worked example.
4. **SHARE_REGISTRY rewrite** + decision-row supersedes per §4.
5. **Render the cover-email + demo screenshots** to PDF/HTML via existing render pipeline; manifest sha256.
6. **Send-ready pack** assembled in `_exports/`; final operator sign-off gate before SMTP send.

## Section 6 — Multi-format / Figma / PPTX gap (operator's broader concern)

Per operator 2026-05-22: *"what about the Figma method and all the tools and skills we honed for this?? In different formats we need to be ready. If one day I ask you to help me go with visuals (like, advertiseable or brand visuals), you are going to short-circuit if we struggle only with PDF/Figma presentations (let alone if I ask a PPTX...)"*

**Existing surfaces** (no funnel vision): the 11 render scripts in `scripts/render_*.py` already cover PDF, HTML, mermaid-diagram, and topic-graph rendering. The Figma plugin skills (figma-use, figma-generate-design, figma-generate-library, figma-code-connect, etc.) are loaded and available. The gap is:

- **No PPTX render path** — would need a python-pptx or unoconv pipeline.
- **No "advertiseable visual" asset pipeline** beyond the deck render — would need a brand-visual generator with Figma-export + raster-asset export.
- **No video render** (Loom is manual capture today).

**Recommended posture** (pending operator ratify; not in scope for SUEZ ship): extend the existing `_candidates/i-nn-output-architecture.md` candidate (per prior summary) to enumerate the missing surfaces + ratify which are first-class.

## Section 7 — Meta-issue: funnel vision + scattered KB

Per operator 2026-05-22: *"each key word I say or any request I make is normally part of our methodology or needs to be integrated after crafting for me... funnel vision is a real issue. And scattered info too."*

This session demonstrated the failure mode three times in the same hour:

1. **First**: SHARE_REGISTRY rows authored against a 6% / 35% mental model neither of which matched the operator's actual commercial doctrine.
2. **Second**: Architecture-addendum + cover-email drafted without checking whether the customer pack was already built and shown (`02-customer-pack/` + `_exports/` were not loaded into the working substrate).
3. **Third**: Prior-session Q-B ratify (Aïsha = `deep_partner_65_35`) treated as durable ground truth even though it was a Time-box auto-default the operator hadn't explicitly ratified, and was overturned by today's methodology-readiness framing.

**Mitigations going forward in this session** (committed):

- Before drafting any customer-facing artifact: glob the engagement folder + read `_exports/render-manifest.json` + check `_archive/` for prior versions.
- Before any decision-row mint: grep DECISION_REGISTER + operator-scratchpad for prior ratifies on the same topic.
- Before doctrine amendment: re-read the canonical's existing §"Worked examples" to avoid duplicating or contradicting them.
- Before invoking a Trello research card / a Neo4j use case / an I82 capability / an I81 KB-integrity entry / an I28 investor-dossier slide: glob the existing initiative folder first.

**Tracking surface**: this session's drift instances are logged at `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` as `[unprocessed]` entries for next coordinator drain.

## Section 8 — Cross-references

- Customer pack: `02-customer-pack/{deck,proposal,tarification,gantt}.customer.fr.md` + `_exports/*.pdf`
- Operator pack: `01-operator-pack/cdc-feasibility-shape.fr.md` + `discovery-questionnaire.fr.md` + `proposal.fr.md` + `deck-suez-webuy.fr.md`
- Internal: `00-internal/deck-suez-webuy.counterparty-brief.md` + `00-internal/deck-suez-webuy.objections.md` + this note
- Source materials: `00-internal/source-materials/efa/CDC_WeBuy_SUEZ.{docx,pdf}` + `00-internal/source-materials/efa/mode-operatoire-passage-commande-webuy.fr.pdf` + transcript-03
- Archive: `_archive/2026-05-10-pre-efa-collab/README.md` + 10 snapshot files
- Coordinator scratchpad: `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` lines 1366-1438 (prior Q-A/B/C/D ratify; partially superseded by today's regrounding)
- Doctrine: `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md` (currently active; demotion track per §4.3)
- Doctrine amendment lineage: D-IH-86-DA (mint) → D-IH-86-DE (share_pattern enum) → D-IH-86-DF (active-promotion to be superseded) → D-IH-86-DF-V2 or successor (re-promotion after methodology-readiness axis lands)
- Related candidates: `_candidates/i81-vault-integrity-layout-milestones-retrofit.md` (KB scatter), `_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md` (commercial readiness — this doctrine's parent home), `_candidates/i83-ai-archivist-and-kirbe-ingestor.md` (input pipeline), `_candidates/i-nn-output-architecture.md` (multi-format render gap)
- Closed engineering-side: `docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md` (Business Strategy Dossier)
- Neo4j use cases (loaded as substrate; not directly SUEZ-relevant): `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md`

---

## Section 9 — EFA folder transcripts: deeper commercial-model discovery (2026-05-22 evening drain)

Operator pointed to a temporal `EFA/` folder at repo root after the §1-§8 ground truth landed. The folder contained 9 audio files (`.mp3`/`.m4a` + paired `.md` transcripts) covering the full Aïsha collaboration arc from 2026-04 (first prospection) to 2026-05-13 (most recent capture). **Six are duplicates of files already living under `2026-efa-collab/` and `2026-suez-webuy/00-internal/source-materials/efa/`. Three are net-new substrate.** This section processes the three net-new transcripts to lock the operator's actual commercial mental model — which has **4 patterns + 1 overlay**, not the 3-enum `share_pattern` the doctrine currently encodes.

### 9.1 The three net-new transcripts (substantive content)

| Transcript | Date | Duration | What it locks |
|:---|:---|:---|:---|
| `2026-04-08 19.02 EFA project prospection.mp3.md` | 2026-04-08 | ~1h31 | First operator-Aïsha commercial conversation. Operator walks through 4 concurrent project shapes (Suez / Aylid / Tontine / Mathias-Kevin-Rosly) and qualifies each commercially. Locks the full 4-pattern model end-to-end. |
| `2026-04-17 19.46 Holistika Research Researcher Onboarding.mp3.md` | 2026-04-17 | ~26min | Operator onboards Aïsha on the AI-product adoption curve + the Holistika market posture: target innovators + early-adopters (high-pay), avoid commoditised late-majority. Locks SUEZ qualification as "operational improvement for a tardive/closed enterprise" — not innovation work. |
| `2026-12-12 Holistika Research Business Developer Onboarding.m4a.md` | 2026-12-12 *(metadata; likely 2025-12-12 per arc)* | ~1h08 | Aïsha formally onboarded as Holistika business developer. Operator names the 4 commercial patterns explicitly + names Aïsha's SUEZ role as "BD full" (parallel to Mathias's pattern). |

The 4 audios under `EFA/` that ARE already mirrored elsewhere: WhatsApp 2026-05-10 18:20 + 18:21 (mirrored at `2026-suez-webuy/00-internal/source-materials/transcripts/`), briefing-01 + briefing-03 from 2026-12-12 (mirrored at `2026-efa-collab/2025-12-12-suez-proposal-briefing/`).

The 1 audio that is NEITHER mirrored NOR transcribed: **`EFA/13-05-2026 10.24.mp3`** (~unknown duration; recorded 3 days after the 2026-05-10 WhatsApp messages; date `2026-05-13` is the day after the customer-pack render manifest's `issue_date: 2026-05-12`). This is **highly likely the actual customer meeting recording OR the post-meeting Aïsha-operator debrief** that operator referenced 2026-05-22 (*"I got some feedback about the meeting how it went and about the deliverables"*). Operator confirmed 2026-05-22: *"sorry I have the mp3 only I think but I trust you can think of something good."* The agent's transcription pipeline (Whisper / equivalent) is not wired up; resolution path below in §9.5.

### 9.2 The 4 commercial patterns (operator's actual mental model)

From the 2026-12-12 Business Developer Onboarding transcript + the 2026-04-08 prospection transcript, the operator's actual commercial doctrine has **4 mutually-exclusive base patterns** + **1 overlay** (independent; applies to any base):

| Pattern | Operator's name for it | When it applies | Worked precedent in operator's portfolio |
|:---|:---|:---|:---|
| **`bd_intro_only`** | *"business development full"* / *"comme Mathias"* | Collaborator brings a deal as introducer only; Holistika prime-bills + delivers; collaborator receives BD% override on margin. NO operational share of revenue. | Mathias for any deal he brings; Aïsha-on-SUEZ on the **deal-brokering side** |
| **`consulting_direct`** | *"comme Boursoise"* / *"consulting direct"* | Holistika prime-bills client as paid consultant. Client pays Holistika directly. Costs covered by client. BD overlay if applicable. No collaborator on the engagement-revenue side. | Boursoise (live); **SUEZ-from-the-Holistika-side** (because SUEZ prime-bills Holistika at 38.5k / 53.5k / 87k per `tarification.customer.fr.md`) |
| **`joint_venture_aventure`** | *"aventure ensemble"* / *"tontine"* | Joint product/venture; % split per ops + IP + contacts contribution; revenue shared on the engagement-revenue surface, not on Holistika's margin. Mandatory operating agreement. | Tontine (the African e-commerce + payments venture discussed in onboarding; partly with Shario/Payload) |
| **`deep_partner_65_35`** | *"on prend leur ops, 65 nous / 35 eux"* | Holistika brings methodology + machinery + execution stack as the value of its 65%. Partner brings/operates the deal + their network + their ongoing customer maintenance, earning 35%. **Silent precondition: methodology-readiness** — partner can fully operate the Holistika method. | Websitz / Rushly (live 2026 marketing-agency extension) |
| **`custom`** | *"cas par cas"* | Anything that doesn't cleanly fit the 4 above. Mandatory `share_override_decision_id` FK to a DECISION_REGISTER row narrating the commercial shape. | Flagship investor-lighthouse deals; rare bespoke shapes |

**The overlay (independent; stackable on any base pattern):**

| Overlay | When it applies | How it stacks |
|:---|:---|:---|
| **`bd_commission_overlay`** | A BD partner brought the deal (intro, warmth, decision-maker access). They receive a % of Holistika's post-cost margin (typical: 15% per operator's 2026-05-22 framing; 10-20% range per 2026-04-08 transcript context). **Paid from Holistika's share, NOT from the engagement-revenue surface.** Invisible to the end client. | Models as a row in `COLLABORATOR_RATE_OVERRIDES.csv` with a new `override_kind: bd_commission_overlay` enum value, FK-pointing to the base SHARE_REGISTRY row. |

### 9.3 SUEZ #1 commercial shape — corrected definitive

Combining §2.3 above (the original ground-truth pass) with the §9.2 4-pattern model:

- **Base pattern**: `consulting_direct` (NOT `custom` as §2.3 originally stated; the §9 transcripts reveal `consulting_direct` is a first-class named pattern, not a `custom` exception).
- **Base SHARE_REGISTRY row**: 1 row for `engagement_id=ENG-SUEZ-WEBUY-2026`, `share_pattern=consulting_direct`, `holistika_share=100%` (because the client prime-bills Holistika directly; no engagement-revenue split).
- **BD overlay**: 1 row in `COLLABORATOR_RATE_OVERRIDES.csv`, `override_kind=bd_commission_overlay`, `collaborator_id=POI-PRT-EFA-LEAD-2026`, `overlay_pct=15%`, `overlay_base=margin_after_costs`, FK to the consulting_direct SHARE_REGISTRY row above.
- **Aïsha continuity-operator work**: separate rows in `HOLISTIKA_VENDOR_SERVICES_BILLED.csv` for any hours she actually works on continuity (beyond the BD intro); paid as services rendered, not as share or overlay.
- **Methodology-readiness gap** (§2.2): still real. It's the reason Aïsha-on-SUEZ is **NOT** `deep_partner_65_35` despite operator's verbatim *"I would never accept to take over the operations of a business for less than 65%"* preference. The transcripts confirm the gap is structural and recurring — every new BD-class collaborator will start at `bd_intro_only` or `consulting_direct + bd_commission_overlay` and only graduate to `deep_partner_65_35` once methodology-readiness is verified.

### 9.4 Doctrine impact — scope of the rewrite

The doctrine `COLLABORATOR_SHARE_DOCTRINE.md` as currently authored:

- Currently encodes **3 `share_pattern` enum values**: `deep_partner_65_35` / `orchestration_broker_thin_margin` / `custom`.
- Currently treats `orchestration_broker_thin_margin` as the SUEZ-shape (6% thin margin) — **this pattern does not exist in the operator's actual mental model.** It was an architectural invention by the agent during the original Wave R+1 P2 doctrine mint, never ratified by transcript evidence.
- Currently has **no `bd_commission_overlay`** concept; BD compensation was implicitly conflated with revenue-share, which is the source of the recurring confusion.
- Currently has **no `consulting_direct` named pattern** (the most-common shape in operator's portfolio: Boursoise, SUEZ, and most paid-services engagements default to this).
- Currently has **no `joint_venture_aventure` named pattern** (Tontine and any future joint product).
- Currently has **no `methodology-readiness` axis** as a precondition for `deep_partner_65_35`.

**The required scope is a rewrite, not an amendment.** Specifically:

1. **Remove** `orchestration_broker_thin_margin` from the enum (was an invented shape; no transcript backs it; supersede via decision row).
2. **Add** 3 new enum values: `bd_intro_only`, `consulting_direct`, `joint_venture_aventure`.
3. **Add** a new CSV concept: `bd_commission_overlay` as a new `override_kind` value in `COLLABORATOR_RATE_OVERRIDES.csv` (NOT a new 6th CSV — cleanly fits the existing overrides table).
4. **Add** the `methodology-readiness` axis as §2.4 of the doctrine + as a precondition test the validator checks when `share_pattern=deep_partner_65_35`.
5. **Rewrite** §3 worked examples: Websitz stays as `deep_partner_65_35`; SUEZ becomes `consulting_direct + bd_commission_overlay`; Tontine added as `joint_venture_aventure`; Mathias added as `bd_intro_only`.
6. **Rewrite** CS-03 + CS-04 per-pattern branching to cover all 5 enum values (currently 3).
7. **Add** CS-09 (NEW): `bd_commission_overlay` linkage check — every `bd_commission_overlay` override row FK-resolves to a SHARE_REGISTRY row in the same engagement, AND the overlay % is in the operator-ratified range (10-20% advisory band).
8. **Demote** doctrine `status: active` → `status: charter` pending re-application across all 4 new patterns (Stage-1 active-promotion gate per §9 of the existing doctrine requires real-engagement worked examples).

The cursor rule `akos-collaborator-share.mdc` + the SOP `SOP-PEOPLE_COLLABORATOR_SHARE_001.md` + the skill `collaborator-share-craft/SKILL.md` + the Pydantic chassis `akos/hlk_collaborator_share.py` + the validator `scripts/validate_collaborator_share.py` + the runbook `scripts/collaborator_share_calculate.py` + the Supabase mirror DDL all need parallel updates to match the new enum.

This is a **5-7 commit governance rewrite**, not a 1-commit amendment. The architectural scope is larger than the original Wave R+1 P2 13th-specialty mint.

### 9.5 The 13-05-2026 10.24.mp3 audio gap

The single unverified piece of substrate is **`EFA/13-05-2026 10.24.mp3`**. Date arc:

- 2026-05-10 — Aïsha WhatsApp voicemails to operator (already transcribed; covers SUEZ-side intel: 50 commandes/jour, litiges, monthly synthesis)
- 2026-05-12 — customer-pack render manifest `issue_date` (pack rendered + packaged)
- **2026-05-13 10:24 — this recording** (unknown content; likely the customer meeting OR a post-meeting debrief between operator + Aïsha)
- 2026-05-22 — operator references *"I got some feedback about the meeting how it went and about the deliverables"*

Three resolution paths (operator's call):

1. **Operator dumps the meeting feedback verbally in chat** — fastest (5 min), captures the load-bearing claims (DSI reaction, variant preference, demo ask) without requiring transcription. Agent commits the dump to a new internal note `00-internal/meeting-feedback-2026-05-13.md` as durable substrate.
2. **Operator runs the mp3 through their existing transcription pipeline** (the Whisper-shaped tool that produced the `.mp3.md` files in the EFA folder; appears to be a Mac-based local pipeline per the `source: /Users/fay/...` frontmatter) and pastes the transcript output. Agent commits to `00-internal/source-materials/transcripts/2026-05-13-suez-meeting.mp3.md` + processes the content same as the other EFA transcripts.
3. **Operator skips** — agent proceeds with cover-email rewrite based on the deck/proposal/CDC + Aïsha's WhatsApp intel + the 3 EFA transcripts; cover-email becomes a "follow-up to our recent exchange" rather than a "follow-up to the specific meeting on date X" because the meeting specifics aren't in substrate. Lower fidelity but unblocking.

**Recommended** (pending operator pick): Path 1 (verbal dump) — preserves operator's bandwidth + captures the load-bearing claims faster than transcription.

### 9.6 EFA temporal folder durable-home plan

Operator stated 2026-05-22: *"that folder is temporal so think of something out too."* Mapping each file to its durable home:

| File in `EFA/` | Durable home | Move action |
|:---|:---|:---|
| `2026-12-12 Business Developer Onboarding.m4a.md` | `docs/references/hlk/v3.0/Think Big/Advisers/2026-efa-collab/00-internal/source-materials/transcripts/` | **TODO: move** (foundational substrate; current home is EFA folder only) |
| `2026-04-08 EFA project prospection.mp3.md` | Same as above | **TODO: move** |
| `2026-04-17 Researcher Onboarding.mp3.md` | Same as above | **TODO: move** |
| `2026-12-12 SUEZ Briefing 1.m4a.md` | `2026-suez-webuy/00-internal/source-materials/transcripts/efa/` (already mirrored) | Compare; supersede if EFA version more complete (current suez-webuy version is corrupt — wrong language detection) |
| `2026-12-12 SUEZ Briefing 3.m4a.md` | Same as above | Compare; supersede if EFA version more complete |
| `WhatsApp 2026-05-10 18.20.opus.mp3.md` | `2026-suez-webuy/00-internal/source-materials/transcripts/` (likely already mirrored — verify) | Verify + delete EFA copy if duplicate |
| `WhatsApp 2026-05-10 18.21.opus.mp3.md` | Same | Same |
| `13-05-2026 10.24.mp3` | `2026-suez-webuy/00-internal/source-materials/transcripts/` AS the meeting recording, mirrored ALSO to `2026-efa-collab/` | **TODO: move + transcribe per §9.5** |
| `CDC_WeBuy_SUEZ.docx` (if duplicate) | `2026-suez-webuy/00-internal/source-materials/efa/` (already canonical) | Verify + delete EFA copy if byte-identical |
| Other PRESENTATION / logo assets (if duplicate) | `2026-efa-collab/brand-assets/` (already canonical) | Verify + delete EFA copy if duplicate |

After moves: delete the `EFA/` folder entirely; commit captures the move trail; CHANGELOG entry notes the temporal-to-durable migration.

### 9.7 Demotion + supersede plan (revised vs §4.3)

Given the §9.4 doctrine-rewrite scope, the original §4.3 demotion plan is **insufficient**. Revised:

1. **Demote `COLLABORATOR_SHARE_DOCTRINE.md`** `status: active` → `status: charter` immediately (single-commit; minimal blast radius).
2. **Supersede the following decision rows** in a single supersede-commit:
   - D-IH-86-DE (3-value `share_pattern` enum) → superseded by D-IH-86-DE-V2 (5-value enum + overlay)
   - D-IH-86-DF (active-promotion based on SUEZ wrong shape) → superseded by D-IH-86-DF-V2 (new gate language)
   - D-IH-86-EG (splits anchor) → superseded by D-IH-86-EG-V2
   - D-IH-86-EH / D-IH-86-EI (Commit 4 quintet remainder) → review row-by-row; supersede the ones that cite `orchestration_broker_thin_margin`
3. **Rewrite SHARE_REGISTRY rows** for SUEZ + Websitz per the new 4-pattern model (Websitz stays at `deep_partner_65_35`; SUEZ moves to `consulting_direct` + `bd_commission_overlay`).
4. **Stage the doctrine rewrite** as a multi-commit operation per §9.4 (5-7 commits to land cleanly through the validator + tests + sibling-repo updates).
5. **Re-promote** `status: active` only after all 4 new patterns have at least one real-engagement worked example landed:
   - `bd_intro_only` → Mathias-bringing-any-deal (forward-pending the first such commit)
   - `consulting_direct` → SUEZ (this rewrite cycle)
   - `joint_venture_aventure` → Tontine (forward-pending Tontine engagement charter)
   - `deep_partner_65_35` → Websitz (already exists; preserve as worked example)

The 14th specialty SYNTHESIS_BEFORE_TRANCHE worked-example #3 (engagement class, ratified at Commit 4) **does NOT need to be reversed** — the discipline was applied correctly; the underlying commercial pattern was the wrong shape. The synthesis sweep passed because the wrong shape was internally consistent. This is itself a data point for SYN-04 brand-register-citation: a synthesis sweep can pass on internally-consistent-but-wrong substrate. Surface as a learning at next coordinator drain.

### 9.8 Cross-references (this section)

- EFA-folder transcripts (3 net-new, fully readable): `EFA/2026-12-12 - Holistika Research - Business Developer Onboarding.m4a.md`, `EFA/08-04-2026 19.02 - EFA project prospection.mp3.md`, `EFA/2026-04-17 19.46 - Holistika Research - Researcher Onboarding.mp3.md`
- EFA-folder untranscribed audio: `EFA/13-05-2026 10.24.mp3`
- EFA-folder duplicates (already mirrored elsewhere): briefing-01, briefing-03, WhatsApp 18:20, WhatsApp 18:21, CDC docx, PRESENTATION assets, logo assets
- Doctrine pre-rewrite: `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md` (currently `status: active`; demotion track per §9.7)
- Decision rows to supersede: D-IH-86-DE, D-IH-86-DF, D-IH-86-EG, D-IH-86-EH, D-IH-86-EI (review row-by-row)
- Forward-pointers: I82 P2 (capability registry) will inherit the 4-pattern doctrine; I-NN-program-continuity-discipline candidate scope expands to include the BD-overlay pattern; investor stability dossier (I86 wave-deliverable) will cite the 4-pattern model as evidence of commercial-shape discipline.
