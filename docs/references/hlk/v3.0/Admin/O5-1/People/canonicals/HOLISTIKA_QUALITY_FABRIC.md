---
title: Holistika Quality Fabric
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
  - System Owner
co_authors:
  - PMO
  - People Operations Lead
last_review: 2026-05-20
last_review_by: Founder/CEO
last_review_at: 2026-05-20
last_review_decision_id: D-IH-86-AU
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-AU
  - D-IH-86-DA
  - D-IH-86-EA
  - D-IH-86-EJ
  - D-IH-86-EK
  - D-IH-86-EL
  - D-IH-86-EM
  - D-IH-86-EN
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - RESEARCH_HEAD_DISCIPLINE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - HOLISTIKA_STAKEHOLDER_LENSES.md
  - UAT_DISCIPLINE.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - INDEX_INTEGRITY_DISCIPLINE.md
  - PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md
  - COLLABORATOR_SHARE_DOCTRINE.md
  - SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md
  - DATAOPS_DISCIPLINE.md
  - MKTOPS_DISCIPLINE.md
  - TECHOPS_DISCIPLINE.md
  - UX_DISCIPLINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv
  - ../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - ../../Marketing/Brand/canonicals/BRAND_DO_DONT.md
linked_cursor_rules:
  - .cursor/rules/akos-external-render-discipline.mdc
  - .cursor/rules/akos-brand-baseline-reality.mdc
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
  - .cursor/rules/akos-applied-research-discipline.mdc
  - .cursor/rules/akos-planning-traceability.mdc
  - .cursor/rules/akos-collaborator-share.mdc
  - .cursor/rules/akos-synthesis-before-tranche.mdc
companion_to:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - RESEARCH_HEAD_DISCIPLINE.md
forward_charters:
  - I-NN-CHANNEL-DOCTRINES (per-channel goods/bads research; activation gates HOLISTIKA_QUALITY_FABRIC P1 + 1 channel research pass)
  - scripts/derive_quality_bar.py (the derivation runbook)
---

# Holistika Quality Fabric

> The People-area meta-doctrine that names how every Holistika artifact's
> quality bar is derived from five axes — audience, channel, scenario, brand,
> governance — composed multiplicatively. Codified at I86 Wave J from the
> operator's verbatim framing 2026-05-20:
>
> *"It depends on who the user is. Option D and ensure that every user as
> recipient/audience is taken into account, but that's why we have audience
> for. We need to engineer properly the link between both. There are also the
> channels, they each have their own rules of what is good and what is bad
> and their own doctrine which you need to research to help me backfill
> whatever we're lacking there. Then there is the scenario that may have
> additional rules to do's and don'ts, our brand which must be there to
> ensure everything looks n feels like us, and of course good governance.
> And scalable. That's the challenge i pose you. Do you accept?"*
>
> This canonical IS the engineered link.

## 1. Purpose

A flat taxonomy of UAT classes, UX practices, brand surfaces, send-evidence
patterns, or render formats is **descriptive** — it labels what we have
already done. The operator's challenge demands a **generative** doctrine:
one that tells us what to do for any new artifact, including cells of the
matrix we have not yet encountered.

The Quality Fabric names that every artifact's quality bar is the
composition of five axes' constraints. The five axes mostly already exist
as canonicals in this repo; the doctrine is in **how they compose** and in
**which axis owns which constraint**. The fabric is the durable record of
that composition, so future agents and operators inherit the same
architecture without re-deriving it from scratch.

## 2. The five axes

Every Holistika artifact answers five questions before its quality bar can
be computed:

| Axis | Question | Canonical SSOT (or gap) | Status |
|:---|:---|:---|:---|
| **Audience** | Who receives this? | [`AUDIENCE_REGISTRY.csv`](../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) (J-OP / J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO / J-AIC) | active |
| **Channel** | How does it reach them? | [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv) — registry exists; **per-channel doctrine documents largely missing** (the gap) | partial |
| **Scenario** | What are they doing? | [`PERSONA_SCENARIO_REGISTRY.csv`](../../Marketing/Resonance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv) + linked persona DO/DON'T lists | partial |
| **Brand** | How must it look and feel? | [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) (dual-register) + [`BRAND_DO_DONT.md`](../../Marketing/Brand/canonicals/BRAND_DO_DONT.md) (voice traits) + design system + Figma sources | active |
| **Governance** | What guardrails apply? | [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md) (asset class) + [`DECISION_REGISTER.csv`](../Compliance/canonicals/DECISION_REGISTER.csv) + [`INITIATIVE_REGISTRY.csv`](../Compliance/canonicals/INITIATIVE_REGISTRY.csv) + `config/verification-profiles.json` + `.cursor/rules/akos-*.mdc` | active |

When all five answers are known, the artifact's bar is derivable. When any
answer is missing or ambiguous, the artifact is under-specified and the
gap is itself an ops-row to close (see §5 derivation contract for the
ambiguity-handling rule).

## 3. The composition rule

The five axes compose **multiplicatively** — every constraint from every
axis must be satisfied. Composition is **not** additive (where any one
axis can dominate) and **not** sequential (where the last axis "wins").
This is the load-bearing claim of the fabric and what makes it generative.

### 3.1 The 4-layer output hierarchy parametrised by the fabric

The 5 axes resolve **what** quality bar applies to an artifact. They do
not resolve **what shape the artifact takes**. Operator G4 extension at
Wave K (2026-05-20 per `D-IH-86-BB`):

> *"we are speaking of components in a UI and there could be more
> scenarios, slides of pdf/pptx, images, voice for agents, reading for
> different readers platforms, scenarios, etc, excalidraw, mermaids,
> graphs, gantts, please try to think of a way to properly organize the
> output type"*

Below the 5-axis fabric sit **4 layers** that name the artifact's shape
decomposition:

```
Quality Fabric (Audience × Channel × Scenario × Brand × Governance)
   ↓ derives quality bar, parametrised at every layer:
Layer 1: OUTPUT TYPE (medium / shape — prose / slide / image / voice /
         mermaid / gantt / excalidraw / web / pdf / video; ~17 codes)
   ↓ assembled into:
Layer 2: ARTIFACT CLASS (named purpose — dossier / cover_email /
         intro_message / deck / topic_graph / km_diagram / uat_report;
         ~20 codes)
   ↓ composed of:
Layer 3: COMPONENT PRIMITIVE (sub-units — greeting / hook / CTA /
         signature / evidence-block / slide-hero / slide-the-ask;
         ~25 codes; Shadcn-shape per-primitive doctrine)
   ↓ rendered to:
Layer 4: RENDER SURFACE (PDF / Web / ERP / Mail / Slide / Broadcast —
         already exists per akos-external-render-discipline.mdc RULE 1)
```

Each layer = registry CSV + canonical MD library doctrine. The Quality
Fabric is **not** extended with a 6th axis; the 4-layer hierarchy is
**parametrised by** the 5 axes (every layer's bar derives from
`compose(audience, channel, scenario, brand, governance)`). The 4 layers
land as registries + libraries at Wave K (`D-IH-86-BB` + `D-IH-86-BC`)
under the new initiative
[I-NN-OUTPUT-ARCHITECTURE](../../../../../../docs/wip/planning/_candidates/i-nn-output-architecture.md).
Per-layer Shadcn-equivalent depth (Layer 3 component-primitive doctrine
pages with variants × accessibility × research grounding × composition
rules) matures at I-NN-OUTPUT-ARCHITECTURE P1-P3 once activation gates
clear. Reference the `D-IH-86-BB` rationale + the candidate file for the
load-bearing structural claim and orthogonality argument.

The reason composition is multiplicative rather than additive is that
quality is governed by the most-constrained axis on each dimension:

- An investor pitch on LinkedIn DM (audience J-IN × channel LinkedIn-DM)
  must satisfy both the investor-class evidence bar AND the LinkedIn DM
  brevity/professionalism norms. Either constraint alone is insufficient.
- An ENISA dossier in a customer onboarding scenario (audience J-ENISA ×
  scenario customer-onboarding) is a category error — the composition
  surfaces the contradiction immediately and forces a re-scoping.
- A regulator-class surface (audience J-ENISA × governance regulatory)
  must render as PDF with sealed sha256 manifest (per
  `akos-external-render-discipline.mdc` RULE 2) AND must use
  jargon-clean external register (per `akos-brand-baseline-reality.mdc`
  RULE 4) AND must be ratified by an explicit decision row before send
  (per governance axis). Three constraints, all binding, all derived.

## 4. Per-axis doctrine inventory and gap statement

### 4.1 Audience axis — `AUDIENCE_REGISTRY.csv`

**Status: active.** Canonicalized at I85 P2 (per D-IH-85-A). Eight
production codes (J-OP, J-IN, J-CU, J-PT, J-AD, J-ENISA, J-RC, J-CO) plus
J-AIC for the AI O5-1 role class. Each row carries DO/DON'T columns + an
activation status. Cross-referenced from
[`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc)
RULE 2 (audience × format matrix). No further mint required for v1.

### 4.2 Channel axis — `CHANNEL_TOUCHPOINT_REGISTRY.csv` + per-channel doctrines (THE GAP)

**Status: partial.** Registry exists (per
[`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc)
RULE 7 mint at Wave F, 2026-05-19) with **10 registered channel codes**
as of Wave J (2026-05-20): CHAN-LINKEDIN-DM, CHAN-LINKEDIN-POST-RESPONSE,
CHAN-EMAIL-INBOUND, CHAN-WEB-FORM, CHAN-CAL-SCHEDULE, CHAN-AD-CAMPAIGN,
CHAN-SEARCH-ORGANIC, CHAN-DIRECT-DM, CHAN-PARTNER-REFERRAL,
CHAN-EVENT-MEETING. **Per-channel doctrine documents — naming the
specific goods and bads of each channel — are largely missing for ALL
10.** This is the operator-named gap. Forward-chartered as initiative
**I-NN-CHANNEL-DOCTRINES** (candidate-shape file under
`docs/wip/planning/_candidates/`).

Additional channel codes that surfaced in Wave G B-G2 closure +
Wave J regression as forward-charters (NOT yet in registry; require
canonical-CSV gate per `akos-holistika-operations.mdc` "New git-canonical
compliance registers"; gating prerequisite for **I-NN-CHANNEL-DOCTRINES P0**):
**CHAN-EMAIL-OUTBOUND** (operator-initiated cold/warm send),
**CHAN-EMAIL-MARKETING** (campaign send at scale; distinct UX norms),
**CHAN-EMAIL-TRANSACTIONAL** (account / verification / calendar invite),
**CHAN-PDF-DOWNLOAD** (rendered dossier delivered as link or attachment),
**CHAN-WHATSAPP-DM** (Holistik mobile inbound; per R-31-10 risk),
**CHAN-VOICE-NOTE** (founder mobile voice memo), **CHAN-DECK-SHARE**
(Figma file shared as broadcast surface), **CHAN-PRESS-KIT** (publish
to /press/ on holistikaresearch.com). Registry expansion 10→18 is P0
of I-NN-CHANNEL-DOCTRINES; per-channel doctrine MDs are P1+ of the
same initiative.

Channels that need per-channel doctrine MDs (non-exhaustive list per
operator scope at 2026-05-20):

- **LinkedIn DM** — message length norms, response time expectations,
  professional tone, mutual-connection etiquette, follow-up cadence,
  what counts as spam, when to escalate to email or call.
- **Cold email (J-IN / J-CU outbound)** — subject line craft,
  personalization-vs-templating tradeoff, deliverability hygiene
  (SPF / DKIM / DMARC), unsubscribe footer, CAN-SPAM compliance,
  sender warmup, body length, CTA discipline.
- **Transactional email** (account verification, calendar invite,
  ratify confirmation) — must look like the brand AND must follow the
  transactional-not-marketing UX norms (no marketing CTA in
  transactional context).
- **Marketing email** (campaign send to J-CU at scale) — distinct from
  transactional in cadence, segmentation, and CTA structure.
- **Cal.com / Calendly invite** — title format, agenda, prep-materials
  link, cancellation policy, time-zone handling, follow-up artifact.
- **Web form** (intake on holistikaresearch.com or kirbe.com) — field
  count discipline, error messages, success state, accessibility-AA
  minimum, form completion rate as the quality KPI.
- **Calendar event body** (the meeting itself, post-Cal-schedule) —
  agenda format, materials to attach, video link presence, recording
  policy.
- **WhatsApp Business** (when activated) — message-window rules,
  template approval, opt-in posture.
- **ENISA cover letter / regulatory cover** — PDF + sealed sha256
  manifest minimum, language register (formal external Spanish for
  ENISA), specific section requirements per regulator template.
- **Investor deck-share** (Figma share link / Pitch / Notion preview /
  PDF attachment) — view-only vs comment-on permissions, pre-share
  redaction, post-share follow-up cadence.
- **Press kit landing page** — public, broadcast-class, must render
  brand identity at full strength + must not leak internal vocabulary.

The forward-charter scope is to mint a per-channel
**`<CHAN-CODE>_DOCTRINE.md`** under
`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/channels/`
or equivalent, plus enrich the registry with a `doctrine_path` column
that resolves to the doctrine file. Drift gate
`validate_external_render_trail.py` extends with a
channel-doctrine-resolution sub-check at INFO until backfill closes.

### 4.3 Scenario axis — `PERSONA_SCENARIO_REGISTRY.csv` + persona DO/DON'T

**Status: partial.** Persona scenarios catalogued for MADEIRA quality
rollup (per [`akos-madeira-management.mdc`](../../../../../../.cursor/rules/akos-madeira-management.mdc)).
Engagement-class scenarios (cold-pitch / customer-onboarding /
advisor-handoff / regulatory-evidence / press-pitch / recruiter-outreach
/ partner-co-sell / investor-update / etc.) need richer DO/DON'T
attached. Forward-charter scope: every scenario row carries an explicit
`do_donts_doctrine_path` column resolving to a
**`<SCENARIO-ID>_DOCTRINE.md`** under the owning area's canonicals folder.
This is lower-priority than the channel-doctrine gap because most
scenarios reuse the do/dont blocks from their parent persona +
engagement-class cells.

### 4.4 Brand axis — `BRAND_BASELINE_REALITY_MATRIX.md` + `BRAND_DO_DONT.md` + design system

**Status: active.** Dual-register internal/external matrix codified at
I66 P2. Voice traits + visual identity + design tokens already in place.
Figma sources tracked via [`FIGMA_FILES_REGISTRY.csv`](../../../../Marketing/Brand/canonicals/dimensions/FIGMA_FILES_REGISTRY.csv).
Anti-jargon drift gate at `scripts/validate_brand_baseline_reality_drift.py`
in FAIL mode for external surfaces. No further mint required for v1
beyond ongoing brand-canon maintenance.

### 4.5 Governance axis — PRECEDENCE.md + DECISION_REGISTER + verification-profiles + cursor rules

**Status: active.** Asset classification per
[`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md). Decision
ratification per `DECISION_REGISTER.csv` + initiative gating per
`INITIATIVE_REGISTRY.csv` + automated gates per
`config/verification-profiles.json` + cursor rules at
`.cursor/rules/akos-*.mdc` covering the load-bearing disciplines
(planning-traceability, governance-remediation, holistika-operations,
mirror-template, executable-process-catalog, conflict-surfacing,
inline-ratification, applied-research-discipline,
agent-checkpoint-discipline). No further mint required for v1.

## 5. The derivation contract

Given an artifact, the bar is derived in five steps:

1. **Resolve audience** — frontmatter `audience:` tag (single or list)
   FK-resolved against `AUDIENCE_REGISTRY.csv`. Multi-audience artifacts
   resolve to the **strictest** constraint per axis (e.g., a surface
   tagged `audience: J-IN; J-CU` inherits investor-class evidence bar AND
   customer-class onboarding norms).
2. **Resolve channel** — frontmatter `channel:` tag (optional today;
   advisory per `akos-external-render-discipline.mdc` RULE 7).
   FK-resolved against `CHANNEL_TOUCHPOINT_REGISTRY.csv`. When channel
   is unset, the bar derives audience-only and the channel-side
   constraints fall back to the audience-class default (which itself
   may name a default channel — e.g., J-ENISA defaults to PDF).
3. **Resolve scenario** — frontmatter `scenario:` tag (optional today).
   FK-resolved against `PERSONA_SCENARIO_REGISTRY.csv`. When unset,
   scenario falls back to the artifact's parent-initiative scope
   description.
4. **Apply brand axis** — universal: every artifact is brand-bound.
   The brand axis is never null; the only variable is the register
   (internal CORPINT vs external translated per
   `akos-brand-baseline-reality.mdc`).
5. **Apply governance axis** — universal: every artifact is
   governance-bound by its asset classification + the cursor rules
   that scope it. The governance axis is never null.

When any of axes 1-3 is unresolvable, the artifact is **under-specified**.
Under-specified artifacts cannot reach a PASS verdict in their UAT/UX bar
— they must either resolve the axis (operator decision row) or carry
the under-specification flag explicitly.

## 6. Quality bar materialisation per axis-class

The fabric materialises into existing canonicals as follows. Each
materialisation is a **specialisation** of the fabric's compose() rule
for the specialty's domain.

| Specialty | Materialisation canonical | Status | Compose function |
|:---|:---|:---|:---|
| **UAT (verification)** | `UAT_DISCIPLINE.md` (Wave J P1 mint at status: charter; 11-class promotion gated on `D-IH-86-AY` — promoted Wave R+1 P1 per `D-IH-86-CW` with paired SOP+addendum+runbook `validate_uat_report.py` + cursor rule `akos-uat-discipline.mdc` + paired skill `uat-discipline-craft` + `process_list.csv hol_peopl_dtp_uat_governance_001` + `PEOPLE_DESIGN_PATTERN_REGISTRY pattern_uat_class_taxonomy` + machine-readable `field_test_window:` frontmatter per Q3-b/Q4-b; 3-wave field-test window across Waves S/T/U closes per META4-b) | **active** (provisional, 3-wave field-test window open) | `compose_UAT(audience, channel, scenario, brand, governance) → UAT 11-class taxonomy (closure / brand / send / render / regression / persona / deploy / localisation / accessibility / performance / privacy) + 11-section structural bar enforced by validate_uat_report.py forward-only-by-date (2026-05-19 watershed) + 5-option disposition enum + INFO→FAIL ramp at Wave R+4 post-window` |
| **UX (research + design + accessibility)** | `UX_DISCIPLINE.md` (Wave M P5 mint at status: charter per `D-IH-86-BY`; fulfils forward-charter `D-IH-86-AX`; owned by Brand & Narrative Manager + Front-End Developer co-owner) | charter | `compose_UX(audience, channel, scenario, brand, governance) → UX research methods + design constraints + a11y bar + i18n strategy` |
| **Brand render** | `akos-external-render-discipline.mdc` RULE 2 (audience × format matrix) | active | `compose_render(audience, channel, brand, governance) → 6-surface format choice + manifest contract` |
| **Send evidence** | (sub-section of UAT_DISCIPLINE.md and external-render-discipline) | partial | `compose_send(audience, channel, governance) → send-evidence trail (sha256 + SMTP + manifest)` |
| **Closure gate** | `akos-planning-traceability.mdc` §"UAT quality bar" + `akos-governance-remediation.mdc` §"Verification matrix" | active | `compose_closure(governance) → mechanical evidence + sign-off + registry edits` |
| **MKTOPS (campaign / GTM funnel quality)** | `MKTOPS_DISCIPLINE.md` (Wave M P5 mint at status: charter per `D-IH-86-BW`; fulfils forward-charter `D-IH-86-AZ`; owned by Marketing/Reach + Operations/RevOps + CRO forward) | charter | `compose_MKTOPS(audience, channel, scenario, brand, governance) → campaign quality bar + funnel-stage UX + landing-page conversion + attribution trail` |
| **TECHOPS (system uptime / observability / Web Vitals)** | `TECHOPS_DISCIPLINE.md` (Wave M P5 mint at status: charter per `D-IH-86-BX`; fulfils forward-charter `D-IH-86-AZ`; owned by Tech/System Owner + DevOPS) | charter | `compose_TECHOPS(audience, channel, scenario, brand, governance) → system quality bar + uptime SLO + Core Web Vitals threshold + observability evidence` |
| **DATAOPS (data quality / pipeline integrity / mirror sync)** | `DATAOPS_DISCIPLINE.md` (Wave M P5 mint at status: charter per `D-IH-86-BV`; fulfils forward-charter `D-IH-86-AZ`; owned by Tech/Data + System Owner) | charter | `compose_DATAOPS(audience, channel, scenario, brand, governance) → data quality bar + pipeline freshness + mirror parity + FDW posture` |
| **Output-architecture (4-layer hierarchy)** | `OUTPUT_TYPE_LIBRARY.md` + `ARTIFACT_CLASS_LIBRARY.md` + `COMPONENT_PRIMITIVE_LIBRARY.md` (Wave K skeleton mint per `D-IH-86-BB`; full doctrine matures at I-NN-OUTPUT-ARCHITECTURE P1-P3) | charter | `compose_layer(audience, channel, scenario, brand, governance, layer: output-type|artifact-class|component-primitive) → per-layer bar (medium-specific authoring rule / artifact-class purpose+composition / Shadcn-shape primitive doctrine)` |
| **Inter-wave regression (multi-wave initiative integrity)** | `INTER_WAVE_REGRESSION_DISCIPLINE.md` (Wave M P1 mint at status: charter per `D-IH-86-BK`; 12-dimension sweep + 5-option inline-ratify enum + INFO→FAIL ramp per `D-IH-86-BN`) | charter | `compose_REGRESSION(audience, channel, scenario, brand, governance, wave_closing) → 12-dimension regression sweep (7 baseline + 5 conditional) + per-finding inline-ratify gate` |
| **Index integrity (baseline index documents)** | `INDEX_INTEGRITY_DISCIPLINE.md` (Wave N P3 mint at status: charter per `D-IH-86-CD`; 8-dimension sweep + 5-option inline-ratify enum + INFO→FAIL ramp per `D-IH-86-CD` + paired SOP+runbook per `D-IH-86-CF`) | charter | `compose_INDEX(governance) → 8-dimension index-freshness sweep (6 baseline IDX-01/02/03/04/07/08 + 2 conditional IDX-05/06) + per-finding inline-ratify gate + deterministic-fix paths for IDX-01/02/07/08` |
| **PASS-WITH-FOLLOWUP governance (closure-UAT content axis)** | `PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md` (Wave R+1 Commit 3-a mint at status: charter per `D-IH-86-CX`; 5-class followup taxonomy + structured `verdict_followup_rationale` block + 5-finding-code validator (PWF-FM-01..05) + INFO→FAIL ramp gated on Wave T at earliest per §4.1 + paired SOP `SOP-PEOPLE_PWF_GOVERNANCE_001.md` + paired cursor rule `akos-pwf-governance.mdc` + paired skill `pwf-governance-craft`) | charter | `compose_PWF(governance) → 5-class followup taxonomy (monitoring-obligation / deferred-work-with-tracker / convention-class-followup / mechanical-recovery-with-eta / escalation-to-blocker-tracker) + structured rationale block (followup_class + closure_target + owner + tracker_path + closure_decision_id_target + notes) + per-finding inline-ratify gate; composes multiplicatively with UAT_DISCIPLINE's classification axis` |
| **Collaborator share economics (engagement-economic axis)** | `COLLABORATOR_SHARE_DOCTRINE.md` (Wave R+1 P3 Commit 2 mint at status: charter per `D-IH-86-DA`; Wave R+2 doctrine rewrite per `D-IH-86-EJ` extends to **4-base + 1-overlay = 5-value enum** (consulting_direct / bd_intro_only / deep_partner_65_35 / joint_venture_aventure + `bd_commission_overlay` overlay) — supersedes the 3-shape model in `D-IH-86-DE`; ratifying decisions D-IH-86-EJ (enum + 20-col SHARE_REGISTRY) + D-IH-86-EK (parallel_invoice_stream_indicator) + D-IH-86-EL (SUEZ recommercialisation from orchestration_broker to consulting_direct + bd_commission_overlay) + D-IH-86-EM (overlay_pct_deviation override_kind enum extension) + D-IH-86-EN (methodology_readiness 4-value axis gating share_pattern eligibility); 5-CSV chassis (`COLLABORATOR_SHARE_REGISTRY` 20-col + `HOLISTIKA_VENDOR_SERVICES_BILLED` + `PARTNER_OVERLAP_EXCLUSION_CLAUSES` + `COLLABORATOR_MARKET_RATE_REFERENCE` + `COLLABORATOR_RATE_OVERRIDES` 3-value override_kind); 9-check validator (CS-01..CS-09; CS-03 unified across-rows sum-to-100; CS-04 composition-branching; CS-08 5-value enum; CS-09 NEW overlay-base pairing + methodology-pattern coherence); paired SOP `SOP-PEOPLE_COLLABORATOR_SHARE_001.md` (v3.1 quality bar) + paired runbook `scripts/collaborator_share_calculate.py` (unified TRUE-MARGIN + advisory-notes engine) + paired cursor rule `akos-collaborator-share.mdc` (6 RULES incl. RULE 6 overlay-stacking) + paired skill `collaborator-share-craft` (Principle 1 Q1/Q2/Q3 + Principle 3 settlement arithmetic) + Supabase mirror DDL with CHECK constraints (forward migration at Commit 6); INFO→FAIL ramp gated on Stage 1 (Aïsha-on-SUEZ Commit 3 worked example + `D-IH-86-DF` active-promotion decision) → Stage 2 (3+ engagements with **≥2 of the 4 base patterns + ≥1 overlay** exercised + 0 CS-01/02/03/08/09 findings + quarterly cross-engagement audit pass)) | charter | `compose_SHARE(governance, share_pattern, share_overlay, methodology_readiness, engagement_id) → 5-CSV row kit (atomic; 20-col SHARE_REGISTRY) + per-composition math (4 base patterns with unified TRUE-MARGIN formula + bd_commission_overlay carving from BASE row's net position so cross-row sum-to-100 holds + custom via DECISION_REGISTER FK) + 9-check validator gate + inline-ratify gates for share_pattern triple-resolution (base + overlay + methodology_readiness) + commercial deviation disposition` |
| **Synthesis before tranche (ERP-engagement-governance UX design substrate axis)** | `SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` (Wave R+1 P3 Commit 2c-b mint at status: charter per `D-IH-86-EA`; 10-dimension probe set per `D-IH-86-EB` (SYN-01 audience-completeness + SYN-02 channel-coverage + SYN-03 scenario-inventory + SYN-04 brand-register-citation + SYN-05 governance-ratification-lineage + SYN-06 ERP-surface-citation + SYN-07 tranche-atomicity + SYN-08 reversibility-declaration + SYN-09 closing-loop-test + SYN-10 recipient-fallback-channel); 6 tranche classes (engagement / specialty_mint / internal_governance / canonical_csv_mint / brand_surface / external_deliverable) with per-class `DIMENSION_FIRE_RULES` fire-set; 5-option disposition enum per `D-IH-86-EC` (scope-complete / scope-extend / scope-narrow / defer-OPS / escalate-to-blocker-tracker); broad-fire INFO ramp per `D-IH-86-ED`; paired SOP `SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md` + paired runbook `scripts/synthesis_before_tranche_check.py` + paired validator `scripts/validate_synthesis_before_tranche.py` + paired cursor rule `akos-synthesis-before-tranche.mdc` + paired skill `synthesis-before-tranche-craft` + paired SOP+runbook gate per `D-IH-86-EE`; INFO→FAIL ramp gated on Stage 1 (this canonical's own mint as specialty_mint worked example + Commit 3 I82 P1 capability registry as canonical_csv_mint worked example + Commit 4 SUEZ POC FULL KIT as engagement worked example) → Stage 2 (5+ tranches across ≥ 3 classes + quarterly cross-tranche audit + operator-ratified successor decision row)) | charter | `compose_SYNTHESIS(audience, channel, scenario, brand, governance, tranche_class) → 10-dimension probe set (multiplicative-AND verdict) + per-class fire-set + 5-option disposition enum + Markdown-shaped synthesis report at reports/synthesis-<tranche_id>-<date>.md + ERP-engagement-governance UX design substrate citation (3 surfaces — operator dashboard + customer dashboard with recipient-fallback per SYN-10 + ERP workflow join — explicitly walked when SYN-06 fires for engagement-class tranches per operator Q-A 2026-05-25 framing)` |

Future specialty materialisations inherit the same compose() pattern —
each is a new row in this table without changing the fabric itself. This
is the scalability claim. Wave K demonstrated the claim by extending
from 5 → 9 materialisations (MKTOPS / TECHOPS / DATAOPS / output-architecture
added) without touching the 5-axis composition rule itself; Wave M extended
to 10 (inter-wave regression added); Wave N extended to 11 (index integrity
added); Wave R+1 extended to 12 along two complementary axes — UAT_DISCIPLINE
promoted `charter` → `active` per `D-IH-86-CW` AND PASS-WITH-FOLLOWUP
governance landed at `charter` per `D-IH-86-CX` as the **content axis**
pairing with UAT_DISCIPLINE's **classification axis**. Wave R+1 P3
extends to **13** with COLLABORATOR_SHARE_DOCTRINE landing at status
`charter` per `D-IH-86-DA` as the first **engagement-economic axis**
specialty — moving the fabric out of pure governance-of-process and into
governance-of-money. The discipline's three `share_pattern` shapes
(deep_partner_65_35 / orchestration_broker_thin_margin / custom) per
`D-IH-86-DE` demonstrate the composition rule at fine grain: per-pattern
CS-03/CS-04 branching is the multiplicative-AND of (governance axis ×
engagement-pattern dimension) without changing the 5-axis fabric itself.
Wave R+1 P3 Commit 2c-b extends to **14** with SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE
landing at status `charter` per `D-IH-86-EA` as the first **ERP-engagement-
governance UX design substrate axis** specialty — materialising the operator's
2026-05-25 Q-A verbatim framing *"the main goal is to properly govern our
engagements via cleverly crafting erp workflow and UX just like i want my
dashboard they would also like to have it"* as a discipline that fires before
any meaningful tranche commits. The 10-dimension probe set per `D-IH-86-EB`
(SYN-01..SYN-10) + 6 tranche classes per `D-IH-86-EC` + per-class
`DIMENSION_FIRE_RULES` demonstrate the composition rule at the highest grain
yet: SYN-06 ERP-surface-citation forces engagement-class tranches to walk the
3 ERP-engagement-governance surfaces (operator dashboard + customer dashboard
with recipient-fallback per SYN-10 + ERP workflow join) so the design
substrate inherits from doctrine, not from intuition. Recursive self-
application is built into the structure: this very mint is itself a
specialty_mint tranche; fires 7 baseline dimensions; all 7 satisfied at
commit by design (locked at unit-test time via `TestRecursiveSelfApplication`).
All without touching the 5-axis composition rule.

## 7. Forward-charter inventory

Two forward-chartered initiatives surface from this canonical's mint
(reduced from three at Wave M P5 — UX_DISCIPLINE.md landed per
`D-IH-86-BY`):

1. **I-NN-CHANNEL-DOCTRINES** — Per-channel goods/bads research +
   doctrine MDs + registry enrichment + drift-gate extension. Activation
   gates: this canonical at status active + UAT_DISCIPLINE.md at active +
   ≥ 1 channel research pass complete (proof of concept). Candidate-shape
   file to mint at `docs/wip/planning/_candidates/i-nn-channel-doctrines.md`.

2. **`scripts/derive_quality_bar.py` runbook** — Given (audience,
   channel, scenario_id, surface_class), compute the binding bar by
   composing the 5 axes; emit as JSON for ERP panel consumption + as
   Markdown for human reading. The "engineering of the link" runbook the
   operator named verbatim. Lands in a successor initiative after the
   per-channel doctrines are partially populated (otherwise the runbook
   has nothing to compose for the channel axis). The runbook signature
   now resolves the 4 fresh specialty bars (`compose_DATAOPS` /
   `compose_MKTOPS` / `compose_TECHOPS` / `compose_UX`) in addition to
   the 6 prior bars per the §6 materialisation table (10 total).

## 8. Self-discipline rules for agents

When generating any external artifact, internal closure-UAT, brand
surface, dossier, deck, email, DM, page, form, dashboard, or any other
quality-bound deliverable, the agent must:

1. **Resolve the five axes BEFORE drafting.** If any axis is
   under-resolved, ask via inline-ratify (per
   `akos-inline-ratification.mdc`) before the prose lands. Drafting
   first and reverse-engineering the bar is an anti-pattern that
   produces brand drift and audience-mismatch failures.
2. **Cite the resolved axes inline in frontmatter.** `audience:`,
   `channel:` (when known), `scenario:` (when known) tags should appear
   on every quality-bound artifact's frontmatter. Absence is itself a
   signal the agent should flag.
3. **Compose, don't substitute.** When two axes appear to conflict, the
   compose() rule says BOTH constraints apply — neither dominates. If
   the conflict is genuine (e.g., audience demands brevity but governance
   demands completeness), surface as an inline-ratify gate; do not
   silently pick one axis.
4. **Read the per-axis doctrine before drafting.** Do not infer brand
   voice from prior outputs; read `BRAND_DO_DONT.md`. Do not infer
   channel norms from intuition; read the per-channel doctrine (when
   minted) or call out the gap in the artifact's frontmatter
   `notes:` field.
5. **Refuse under-specified artifacts.** When asked to produce an
   artifact whose audience or channel cannot be resolved, the agent
   refuses or requires inline-ratify before proceeding. This is the
   shield that prevents brand drift.

## 9. When this canonical applies

This canonical applies to **every Holistika artifact intended for any
audience** — operator-internal (J-OP), AIC-internal (J-AIC), or any
external class. Operator-internal artifacts still inherit brand-axis +
governance-axis constraints; only the audience + channel + scenario
axes simplify to internal defaults.

It does **not** apply to:

- Code that is purely runtime infrastructure (no human-facing surface).
  Runtime code inherits governance-axis only (lint + test + type
  contracts) but no audience / channel / scenario / brand axes.
- Internal session scratchwork (operator-scratchpad entries; agent
  self-checkpoints; debugging notes). These are recorded under the
  governance axis only.
- Test fixtures and ephemeral artifacts.

## 10. Migration posture (charter → active)

This canonical lands at **`status: charter`** at mint time (D-IH-86-AU,
2026-05-20). Charter status means: the architecture is ratified;
implementation is phased; specific specialty canonicals (UAT_DISCIPLINE,
UX_DISCIPLINE) and the channel-doctrine backfill are forward-chartered.

Promotion to **`status: active`** requires:

1. **UAT_DISCIPLINE.md** minted at active and instantiated against ≥ 1
   real closure UAT (worked example: I65 closure UAT post-rework).
2. **At least 1 per-channel doctrine** authored as proof-of-concept (any
   single CHAN-* row's doctrine MD) — proves the gap can be closed.
3. **Cursor rule `akos-quality-fabric.mdc`** minted referencing this
   canonical's compose() contract (mechanical enforcement of frontmatter
   axis-tag presence on quality-bound artifacts).
4. **`scripts/derive_quality_bar.py` runbook lands** (per `D-IH-86-BA`
   Wave K regression) — implements compose() as code. Without the
   runbook, the fabric is unfalsifiable in CI. The runbook signature:
   `derive_quality_bar(audience, channel, scenario, brand, governance, *, layer)`
   returns a Pydantic-validated `QualityBar` with per-layer derivation
   when `layer` is set (per the 4-layer hierarchy in §3.1). Runbook
   delegates to `compose_UAT` / `compose_UX` / `compose_render` /
   `compose_send` / `compose_closure` / `compose_MKTOPS` /
   `compose_TECHOPS` / `compose_DATAOPS` / `compose_layer` for specialty
   bars per the §6 materialisation table. Tests in
   `tests/test_derive_quality_bar.py` exercise paired audience/channel/
   scenario/brand/governance fixtures across all 9 audience codes
   (J-OP / J-AIC / J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO).
5. **Operator-explicit ratification** of the promotion (not
   agent-default).

Until promotion, this canonical is the durable record of the operator's
intent and the architecture future agents inherit. Charter status does
NOT prevent specialty canonicals from instantiating against it — it only
defers the mechanical drift-gate enforcement.

## 11. Cross-references

- Sister canonicals under People:
  [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) (organizing
  pattern; this canonical is its quality-axis sibling),
  [`RESEARCH_HEAD_DISCIPLINE.md`](RESEARCH_HEAD_DISCIPLINE.md) (the research
  discipline this canonical's authoring inherits from),
  [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) (agentic
  collaboration substrate — agents apply this canonical's compose()
  every time they produce a quality-bound artifact),
  [`HOLISTIKA_STAKEHOLDER_LENSES.md`](HOLISTIKA_STAKEHOLDER_LENSES.md)
  (stakeholder framing that informs the audience axis).
- Per-axis SSOT registries:
  [`AUDIENCE_REGISTRY.csv`](../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv),
  [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv),
  [`PERSONA_SCENARIO_REGISTRY.csv`](../../Marketing/Resonance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv),
  [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md),
  [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md).
- Cursor rules that materialise specialty composes:
  [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc)
  (audience × channel × format render bar),
  [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)
  (brand axis dual-register),
  [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc)
  §"UAT quality bar" (closure-UAT bar materialisation),
  [`akos-applied-research-discipline.mdc`](../../../../../../.cursor/rules/akos-applied-research-discipline.mdc)
  (canonical mints require research grounding — applies to this canonical's
  successor charters).
- Governance lineage: D-IH-86-AU (operator-ratified architecture mint
  2026-05-20). Sibling decisions D-IH-86-AT (Vercel hotfix evidence that
  proved deploy-UAT axis is real), D-IH-86-AV (forward-charter for
  UAT_DISCIPLINE.md), D-IH-86-AW (forward-charter for
  I-NN-CHANNEL-DOCTRINES), D-IH-86-AX (forward-charter for
  UX_DISCIPLINE.md).
- Operator's verbatim challenge that motivated this canonical: see
  intro epigraph + I86 operator-scratchpad entry 2026-05-20.

@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
@docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
