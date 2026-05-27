---
title: MKTOps Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - PMO
  - System Owner
last_review: 2026-05-27
last_review_by: Founder/CEO
last_review_at: 2026-05-27
last_review_decision_id: D-IH-86-EY
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-BW
  - D-IH-86-EY
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
  - DATAOPS_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - MARKETING_LIFECYCLE_TAXONOMY.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
linked_cursor_rules:
  - .cursor/rules/akos-mktops-discipline.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
  - .cursor/rules/akos-brand-baseline-reality.mdc
  - .cursor/rules/akos-quality-fabric.mdc
linked_runbooks:
  - scripts/validate_mktops_campaign.py
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
forward_charters:
  - SOP-MKT_CAMPAIGN_LIFECYCLE_001.md (paired SOP; lands at C3a follow-up)
  - CRO + COO executive activation per D-IH-72-AD (Data Owner shifts when ratified)
---

# MKTOps Discipline

> The People-area meta-doctrine that names how every Holistika marketing
> artefact's quality bar is derived — across campaign briefs, creative,
> landing pages, funnel-stage UX, attribution trails, and channel
> adapters. Minted at Wave M P5 per operator ratification 2026-05-21
> (Cluster B rework-now, full canonical not stub). This canonical is
> the 7th specialty materialisation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).

## 1. Purpose

Marketing operations span the **outbound surface area** — from
top-of-funnel ad campaigns through middle-funnel content / nurture
through bottom-funnel conversion + retention. Each stage has its own
quality bar: a brand-aligned ad creative that converts at 2% is a
different artifact-class than a discovery-call landing page that
converts at 30%, but both inherit the same governance + brand axes.

Without an explicit discipline, marketing quality drifts in three
predictable ways: (a) **brand drift** — creative copies prior campaigns'
voice rather than reading `BRAND_DO_DONT.md`; (b) **persona-fit drift**
— targeting persona mismatches campaign offer; (c) **attribution drift**
— UTM tagging gaps make funnel-stage measurement unreliable.

MKTOps Discipline names the quality bar that prevents these drifts.
It is owned by **Marketing/Reach** (primary) with **Operations/RevOps**
+ **CRO** (forward; per `D-IH-72-AD` activation) as co-owners. It
applies to every campaign brief, every creative asset, every landing
page, every adapter (CRM / EMAIL / COMMUNICATION / SCHEDULING /
ATTRIBUTION), and every funnel-stage measurement event.

## 2. The 7 MKTOps quality dimensions

| Dim | Quality property | Measurement | Drift signal |
|:---|:---|:---|:---|
| **MKT-01** Campaign lifecycle quality | Every campaign moves brief → creative → review → launch → measure with operator approval at each gate | Per-campaign `lifecycle_state` row in CRM with timestamped transitions | Campaign launches without measurement plan; campaign measures without brief |
| **MKT-02** Funnel-stage UX | Each funnel stage (TOFU / MOFU / BOFU) has UX bar derived from UX_DISCIPLINE.md | Stage-class persona-fit + cognitive-load + call-to-action clarity audit | Stage CTR < benchmark by > 50%; persona-mismatch flagged in review |
| **MKT-03** Landing-page conversion | LP Core Web Vitals + brand voice + persona alignment + form friction | Vercel Analytics + Lighthouse + form-completion rate vs benchmark | LCP > 2.5s, INP > 200ms, CLS > 0.1, OR conversion rate < persona-class benchmark |
| **MKT-04** Attribution trail | Every campaign artefact tags UTM correctly + FK-resolves into ATTRIBUTION_ADAPTER_REGISTRY.csv | UTM consistency scan + attribution_adapter status check | Missing UTM, broken UTM source name, or adapter status `inactive` for in-use adapter |
| **MKT-05** Channel coverage | CRM + EMAIL + COMMUNICATION + SCHEDULING adapter health = active per registry | Adapter registry `status` column scan | Any registered `active` adapter unreachable; any `inactive` adapter referenced by live campaign |
| **MKT-06** Persona-fit | Every campaign targets ≥ 1 FK-resolved persona from PERSONA_REGISTRY | Campaign metadata `target_persona_ids` audit | Empty / null `target_persona_ids`; non-resolving persona FK |
| **MKT-07** Brand-voice integrity | Every external-facing artefact passes BRAND_DO_DONT scan + brand-baseline-reality dual-register check | `validate_brand_baseline_reality_drift.py` + brand-jargon-audit scan | Forbidden tokens in external artefacts; CORPINT-internal tokens leaked into external rendering |

These 7 dimensions are **mandatory** for every campaign launch
(per RULE 1 in paired cursor rule
[`akos-mktops-discipline.mdc`](../../../../../../.cursor/rules/akos-mktops-discipline.mdc)).

## 3. The compose_MKTOPS rule

```
compose_MKTOPS(audience, channel, scenario, brand, governance, *, funnel_stage)
  → marketing_quality_bar
```

Where `funnel_stage` is one of: `awareness` / `consideration` /
`decision` / `retention` / `advocacy`.

The bar derives multiplicatively from the 5 fabric axes + the 7
discipline dimensions + the funnel-stage modifier:

- **audience axis** → which persona class the campaign targets (FK
  to `PERSONA_REGISTRY.csv`); determines MKT-06 fit.
- **channel axis** → which CHANNEL_TOUCHPOINT the campaign emits on;
  determines MKT-04 attribution shape + MKT-05 adapter coverage.
- **scenario axis** → which persona-scenario row the artifact serves;
  derives the funnel-stage-specific CTA + offer.
- **brand axis** → BRAND_DO_DONT + BRAND_BASELINE_REALITY_MATRIX
  compliance per artifact (MKT-07).
- **governance axis** → which process_list rows + decisions cover the
  campaign; per `akos-executable-process-catalog.mdc` RULE 1
  (every campaign is a paired SOP + runbook process).

The bar tightens at promotion (`charter → active`) when CRO + COO
executive layer activates (per `D-IH-72-AD`); pre-promotion, the bar
is operator-discipline-enforced.

**Wave R+4 C3a status flip (2026-05-27 per `D-IH-86-EY`)**: the
discipline moved from `charter` to `active`. The promotion landed with
the paired runbook `scripts/validate_mktops_campaign.py` and Pydantic
SSOT `akos/hlk_mktops.py`, which give every campaign manifest a
structural quality bar against the 7 dimensions. The runbook fires at
pre_commit (`--self-test`) and at campaign-authoring time
(`--check-campaign <manifest.yaml>`). The CRO + COO executive activation
per `D-IH-72-AD` remains forward-chartered; until it lands, the bar
is operator-discipline-enforced through this runbook + the paired
cursor rule.

## 4. Cadence

This discipline fires:

1. **At every campaign brief authoring** — MKT-01 (lifecycle entry)
   + MKT-06 (persona fit) + MKT-07 (brand voice) are exercised
   pre-launch.
2. **At every creative asset review** — MKT-02 (funnel-stage UX) +
   MKT-07 (brand voice) per artefact.
3. **At every landing-page deploy** — MKT-03 (Core Web Vitals +
   conversion benchmark) via Vercel Analytics + Lighthouse + form-
   completion rate measurement (fires post-deploy + at 7-day window).
4. **At every adapter registry mint or status change** — MKT-04 +
   MKT-05 are exercised via paired adapter-registry validators.
5. **At every monthly RevOps cycle** — MKT-01 lifecycle audit for
   stalled campaigns + MKT-04 attribution audit for funnel-stage
   measurement parity.
6. **At every brand-canon update** — MKT-07 forward-scan on all
   in-flight campaign creative.

## 5. Integration with sister disciplines

- **`UAT_DISCIPLINE.md`** — UAT's `brand-class` + `send-class` rows
  cover MKT-07 mechanically; MKT-04 (attribution) sits in UAT's
  governance evidence trail.
- **`UX_DISCIPLINE.md`** — funnel-stage UX (MKT-02) inherits from
  UX research methods + a11y bar; MKTOps owns the campaign-specific
  conversion measurement; UX owns the underlying UX research +
  design constraints.
- **`DATAOPS_DISCIPLINE.md`** — attribution trail (MKT-04) is a
  DataOps lineage problem; persona FK resolution (MKT-06) is a
  DataOps FK integrity problem; campaign lifecycle state (MKT-01)
  is a DataOps schema problem.
- **`TECHOPS_DISCIPLINE.md`** — landing-page Core Web Vitals
  (MKT-03) inherits from TECHOPS's Web Vitals thresholds + uptime
  SLO + deploy posture; MKTOps consumes the bar TECHOPS sets.
- **`akos-executable-process-catalog.mdc`** — adapter registry
  metadata + paired SOP+runbook pattern; MKTOps inherits the
  Normalised Adapter Pattern for cross-stack integrations.

## 6. Cross-references

- Quality Fabric parent: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md)
  §6 row (this canonical materialises `compose_MKTOPS`).
- Sister specialty canonicals: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md),
  [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md),
  [`DATAOPS_DISCIPLINE.md`](DATAOPS_DISCIPLINE.md),
  [`TECHOPS_DISCIPLINE.md`](TECHOPS_DISCIPLINE.md),
  [`UX_DISCIPLINE.md`](UX_DISCIPLINE.md).
- Paired cursor rule: [`.cursor/rules/akos-mktops-discipline.mdc`](../../../../../../.cursor/rules/akos-mktops-discipline.mdc).
- Adapter registries (per
  `akos-executable-process-catalog.mdc` Rule 2):
  [`CRM_ADAPTER_REGISTRY.csv`](../../Marketing/Reach/canonicals/dimensions/CRM_ADAPTER_REGISTRY.csv),
  [`EMAIL_ADAPTER_REGISTRY.csv`](../../Marketing/Reach/canonicals/dimensions/EMAIL_ADAPTER_REGISTRY.csv),
  [`COMMUNICATION_ADAPTER_REGISTRY.csv`](../../Marketing/Reach/canonicals/dimensions/COMMUNICATION_ADAPTER_REGISTRY.csv),
  [`SCHEDULING_ADAPTER_REGISTRY.csv`](../../Marketing/Reach/canonicals/dimensions/SCHEDULING_ADAPTER_REGISTRY.csv),
  [`ATTRIBUTION_ADAPTER_REGISTRY.csv`](../../Marketing/Experimentation/canonicals/dimensions/ATTRIBUTION_ADAPTER_REGISTRY.csv).
- Brand canonicals: [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md),
  [`BRAND_DO_DONT.md`](../../Marketing/Brand/canonicals/BRAND_DO_DONT.md).
- External research grounding per
  `akos-applied-research-discipline.mdc` RULE 2: Forrester Wave
  B2B Marketing Operations 2024 (campaign-lifecycle discipline
  benchmark); MarTech Stack 2026 (Normalised Adapter Pattern
  consensus); RevOps Co-op Framework 2025 (CRO + RevOps
  accountability model).
- Ratifying decision: D-IH-86-BW (Wave M P5 Cluster B sub-decision).
- Sibling decisions: D-IH-86-BU (Cluster B umbrella),
  D-IH-72-AD (CRO + COO executive activation forward),
  D-IH-86-AZ (forward-charter precedent that this canonical
  fulfils).

@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
