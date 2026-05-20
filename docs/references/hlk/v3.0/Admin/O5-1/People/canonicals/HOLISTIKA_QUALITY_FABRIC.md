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
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - RESEARCH_HEAD_DISCIPLINE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - HOLISTIKA_STAKEHOLDER_LENSES.md
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
companion_to:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - RESEARCH_HEAD_DISCIPLINE.md
forward_charters:
  - I-NN-CHANNEL-DOCTRINES (per-channel goods/bads research; activation gates HOLISTIKA_QUALITY_FABRIC P1 + 1 channel research pass)
  - UAT_DISCIPLINE.md (first instantiation; in flight at I86 Wave J)
  - UX_DISCIPLINE.md (second instantiation; depends on channel doctrines)
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
RULE 7 mint at Wave F, 2026-05-19) with channel codes
(CHAN-LINKEDIN-DM, CHAN-EMAIL-INBOUND, CHAN-EMAIL-OUTBOUND,
CHAN-WEB-FORM, CHAN-CAL-SCHEDULE, CHAN-EVENT-MEETING,
CHAN-AD-CAMPAIGN, etc.). **Per-channel doctrine documents — naming the
specific goods and bads of each channel — are largely missing.** This
is the operator-named gap. Forward-chartered as initiative
**I-NN-CHANNEL-DOCTRINES** (candidate-shape file under
`docs/wip/planning/_candidates/`).

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
| **UAT (verification)** | `UAT_DISCIPLINE.md` (in flight; this Wave J P1) | charter→active when minted | `compose_UAT(audience, channel, scenario, brand, governance) → UAT shape (closure / brand / send / render / regression / persona / deploy class)` |
| **UX (research + design + accessibility)** | `UX_DISCIPLINE.md` (forward-charter; depends on channel doctrines) | forward-chartered | `compose_UX(audience, channel, scenario, brand, governance) → UX research methods + design constraints + a11y bar` |
| **Brand render** | `akos-external-render-discipline.mdc` RULE 2 (audience × format matrix) | active | `compose_render(audience, channel, brand, governance) → 6-surface format choice + manifest contract` |
| **Send evidence** | (sub-section of UAT_DISCIPLINE.md and external-render-discipline) | partial | `compose_send(audience, channel, governance) → send-evidence trail (sha256 + SMTP + manifest)` |
| **Closure gate** | `akos-planning-traceability.mdc` §"UAT quality bar" + `akos-governance-remediation.mdc` §"Verification matrix" | active | `compose_closure(governance) → mechanical evidence + sign-off + registry edits` |

Future specialty materialisations (e.g. accessibility, i18n, security
review, performance budget) inherit the same compose() pattern — each is
a new column in this table without changing the fabric itself. This is
the scalability claim.

## 7. Forward-charter inventory

Three forward-chartered initiatives surface from this canonical's mint:

1. **I-NN-CHANNEL-DOCTRINES** — Per-channel goods/bads research +
   doctrine MDs + registry enrichment + drift-gate extension. Activation
   gates: this canonical at status active + UAT_DISCIPLINE.md at active +
   ≥ 1 channel research pass complete (proof of concept). Candidate-shape
   file to mint at `docs/wip/planning/_candidates/i-nn-channel-doctrines.md`.

2. **UX_DISCIPLINE.md mint** — Sibling to UAT_DISCIPLINE.md under
   People canonicals; UX research methodology + Figma-driven design +
   impeccable redesign skill + accessibility + i18n. Depends on
   I-NN-CHANNEL-DOCTRINES P1 (so the channel-aware UX bar derives from
   resolved channel doctrines, not from speculation).

3. **`scripts/derive_quality_bar.py` runbook** — Given (audience,
   channel, scenario_id, surface_class), compute the binding bar by
   composing the 5 axes; emit as JSON for ERP panel consumption + as
   Markdown for human reading. The "engineering of the link" runbook the
   operator named verbatim. Lands in a successor initiative after the
   per-channel doctrines are partially populated (otherwise the runbook
   has nothing to compose for the channel axis).

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
4. **Operator-explicit ratification** of the promotion (not
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
