---
title: UX Discipline
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
last_review: 2026-05-21
last_review_by: Founder/CEO
last_review_at: 2026-05-21
last_review_decision_id: D-IH-86-BY
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BY
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
  - MKTOPS_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv
linked_cursor_rules:
  - .cursor/rules/akos-ux-discipline.mdc
  - .cursor/rules/akos-brand-baseline-reality.mdc
  - .cursor/rules/akos-external-render-discipline.mdc
  - .cursor/rules/akos-quality-fabric.mdc
linked_skills:
  - .cursor/skills/impeccable/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - MKTOPS_DISCIPLINE.md
forward_charters:
  - SOP-PEOPLE_UX_RESEARCH_001.md (paired SOP; activation gate when channel doctrines mature)
  - I-NN-CHANNEL-DOCTRINES (per-channel UX bar derivation per HOLISTIKA_QUALITY_FABRIC §7)
---

# UX Discipline

> The People-area meta-doctrine that names how every Holistika user-
> experience artefact's quality bar is derived — across UX research,
> design constraints, accessibility, internationalisation, information
> architecture, visual design, and interaction patterns. Minted at
> Wave M P5 per operator ratification 2026-05-21 (Cluster B rework-now,
> full canonical not stub). This canonical is the 10th specialty
> materialisation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) and was
> originally forward-chartered per `D-IH-86-AX`.

## 1. Purpose

UX is the **discipline of getting out of the user's way** — making the
right thing easy + the wrong thing hard, without making the surface
feel paternalistic. It is cross-cutting: every audience-class (J-IN
through J-CO + J-OP + J-AIC) has its own UX expectation; every
channel (PDF / Web / ERP / Mail / Slide / Broadcast per
`akos-external-render-discipline.mdc` RULE 1) has its own UX vocabulary;
every persona-scenario has its own friction-tolerance.

Without an explicit discipline, UX quality drifts in three predictable
ways: (a) **persona-blindness** — designers infer user behaviour from
their own intuition instead of from PERSONA_REGISTRY + AUDIENCE_REGISTRY
rows; (b) **accessibility theatre** — surfaces ship with WCAG 2.1 AA
claims but fail keyboard navigation in production; (c) **i18n
afterthought** — locale support bolted on after launch produces
orthography drift + RTL bugs.

UX Discipline names the quality bar that prevents these drifts. It is
owned by **Brand & Narrative Manager** (primary; per 2026-05-15
absorption) with **Front-End Developer** co-owner. It applies to every
component primitive, every artifact-class composition, every page-level
information architecture, every interactive state, every locale-aware
surface, and every accessibility audit.

## 2. The 7 UX quality dimensions

| Dim | Quality property | Measurement | Drift signal |
|:---|:---|:---|:---|
| **UX-01** Research methods grounded in real personas | Design backed by user interviews / usability testing / heuristic evaluation per PERSONA_REGISTRY targeting | Design-doc citation of PERSONA_REGISTRY rows + research evidence per persona | Design that targets a persona without ≥ 1 documented research interaction with that persona class |
| **UX-02** Per-channel design constraints | Each surface respects its channel doctrine (web vs PDF vs ERP vs mail vs slide vs broadcast) | Channel-tag frontmatter present + per-channel design checklist completed | Web component used in PDF render context; mail design used in web context |
| **UX-03** Accessibility bar (WCAG 2.1 AA minimum) | Keyboard navigation + screen-reader semantics + colour contrast + focus indicators + text resize | Axe-core + Lighthouse a11y + manual keyboard sweep per route | Any axe-core error; failed keyboard nav; AAA contrast threshold breach on public surfaces |
| **UX-04** Internationalisation strategy | Locale-aware orthography + RTL support + per-locale brand voice + locale-aware date / number / currency formatting | `validate_locale_orthography.py` + per-locale design review | Locale-mismatched orthography (per `akos-external-render-discipline.mdc` RULE 7 sister validator); RTL layout breakage; locale-specific brand-voice drift |
| **UX-05** Information architecture | Cognitive load minimised; clear hierarchy; scannable structure; predictable navigation | IA audit per route + cognitive-load heuristic + 5-second test per persona | More than 7 top-level navigation items; nested depth > 3 without breadcrumb; F-pattern broken on text-heavy routes |
| **UX-06** Visual design quality | Typography + colour + spacing + alignment per impeccable craft + design-system tokens | Component sweep via `.cursor/skills/impeccable/SKILL.md` checklist + design-token coverage audit | Hardcoded hex / spacing / radius values; type scale inconsistency; misaligned grid |
| **UX-07** Interaction patterns | Consistent affordances + responsive feedback + error states + empty states + loading states + success states | Per-component state inventory + interaction-pattern audit | Component without empty state; component without error state; inconsistent affordance between two routes |

These 7 dimensions are **mandatory** at every component primitive mint,
artifact-class composition, and route-level deploy that ships
user-facing surface.

## 3. The compose_UX rule

```
compose_UX(audience, channel, scenario, brand, governance, *, surface_layer)
  → ux_quality_bar
```

Where `surface_layer` is one of: `component_primitive` / `artifact_class`
/ `output_type` / `route_composition` (per the 4-layer output architecture
in [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) §3.1).

The bar derives multiplicatively from the 5 fabric axes + the 7
discipline dimensions + the layer modifier:

- **audience axis** → which persona class consumes the surface; FK
  to AUDIENCE_REGISTRY + PERSONA_REGISTRY; determines UX-01 research
  grounding + UX-03 a11y tightening for accessibility-needing personas.
- **channel axis** → which surface medium the artefact lives in;
  determines UX-02 channel-constraint set.
- **scenario axis** → which persona-scenario row the surface serves;
  determines UX-05 IA priority + UX-07 interaction pattern fit.
- **brand axis** → BRAND_DO_DONT compliance per surface;
  brand-baseline-reality dual-register applies; determines UX-06
  visual design quality bar.
- **governance axis** → which decisions / cursor-rules / SOPs cover
  the surface; per `akos-external-render-discipline.mdc` for render
  surfaces, per impeccable skill for visual craft, per
  `akos-people-discipline-of-disciplines.mdc` for People-canonical
  governance.

The bar tightens for external-facing audiences (J-IN through J-CO);
internal-only (J-OP / J-AIC) surfaces inherit a lighter bar focused on
UX-05 (IA) + UX-07 (interaction) + UX-03 (a11y for operator
keyboards).

## 4. Cadence

This discipline fires:

1. **At every new component primitive mint** — UX-06 (visual quality
   per impeccable) + UX-03 (a11y baseline) + UX-07 (state coverage)
   exercised.
2. **At every artifact-class composition** — UX-02 (channel
   constraints) + UX-05 (IA) + UX-07 (interaction patterns) per the
   composition's parent output-type.
3. **At every route-level deploy** — UX-03 (a11y) + UX-04 (i18n) +
   UX-06 (visual) full sweep; gated via Lighthouse + axe-core in CI.
4. **At every persona research cycle** — UX-01 (research grounding)
   refreshed; persona-fit re-confirmed; design-doc citations updated.
5. **At every brand-canon update** — UX-06 (visual quality) forward-
   scan on all in-flight design work.
6. **At every wave-close** (per
   `akos-inter-wave-regression.mdc`) — UX-04 (i18n) sister-validator
   coverage probed via DIM-09 cursor-rules drift dimension.

## 5. Integration with sister disciplines

- **`MKTOPS_DISCIPLINE.md`** — funnel-stage UX (MKT-02) inherits
  this discipline's UX-05 (IA) + UX-07 (interaction); landing-page
  conversion (MKT-03) inherits UX-06 (visual) + UX-03 (a11y).
  MKTOps consumes the bar UX sets; UX owns the research +
  craft methodology.
- **`UAT_DISCIPLINE.md`** — UAT's `accessibility-class` row maps
  directly to UX-03; UAT's `persona-class` row maps to UX-01;
  UAT's `localisation-class` row maps to UX-04.
- **`TECHOPS_DISCIPLINE.md`** — Core Web Vitals (TECH-02) sets the
  performance bar that UX-06 (visual quality) operates inside;
  UX inherits the threshold + designs to it.
- **`DATAOPS_DISCIPLINE.md`** — persona FK integrity (DATA-01)
  underpins UX-01 (research grounding); empty-state design (UX-07)
  depends on accurate data-fetch failure signals from DataOps.
- **`akos-external-render-discipline.mdc`** — 6-surface render
  enum is the canonical channel-axis input for UX-02.

## 6. Cross-references

- Quality Fabric parent: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md)
  §6 row (this canonical materialises `compose_UX`) + §7
  forward-charter inventory (this canonical was item 2;
  Wave M P5 fulfils the charter).
- Sister specialty canonicals: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md),
  [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md),
  [`MKTOPS_DISCIPLINE.md`](MKTOPS_DISCIPLINE.md),
  [`TECHOPS_DISCIPLINE.md`](TECHOPS_DISCIPLINE.md),
  [`DATAOPS_DISCIPLINE.md`](DATAOPS_DISCIPLINE.md).
- Paired cursor rule: [`.cursor/rules/akos-ux-discipline.mdc`](../../../../../../.cursor/rules/akos-ux-discipline.mdc).
- Paired skill: [`.cursor/skills/impeccable/SKILL.md`](../../../../../../.cursor/skills/impeccable/SKILL.md)
  — visual craft + UX redesign methodology (UX-06 + UX-07 backbone).
- Audience + persona registries:
  [`AUDIENCE_REGISTRY.csv`](../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv),
  [`PERSONA_SCENARIO_REGISTRY.csv`](../../Marketing/Resonance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv).
- Channel taxonomy:
  [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv).
- External research grounding per
  `akos-applied-research-discipline.mdc` RULE 2: Nielsen Norman Group
  Heuristic Evaluation 2024 (UX-01 + UX-05 method backbone); WCAG 2.1
  AA Quick Reference 2024 (UX-03 accessibility threshold);
  Unicode CLDR 45 (UX-04 i18n locale data); IDEO Field Guide to
  Human-Centered Design 2024 (UX-01 research methodology); Material
  Design 3 Foundations 2024 + Shadcn UI Patterns 2026 (UX-06 visual
  craft + UX-07 interaction patterns).
- Ratifying decision: D-IH-86-BY (Wave M P5 Cluster B sub-decision).
- Sibling decisions: D-IH-86-BU (Cluster B umbrella),
  D-IH-86-AX (forward-charter precedent that this canonical
  fulfils), D-IH-86-AY (UAT_DISCIPLINE.md mint precedent for the
  specialty-canonical pattern).

@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
