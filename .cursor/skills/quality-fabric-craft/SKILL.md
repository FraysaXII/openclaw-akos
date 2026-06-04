---
name: quality-fabric-craft
description: Use when authoring or shipping any quality-bound artifact in this AKOS workspace (audience-tagged, closure UAT, sibling-repo work, brand-touching surface, Quality Fabric specialty canonical). Codifies the craft for resolving + composing the 5 axes (audience × channel × scenario × brand × governance) multiplicatively. Triggers on Quality Fabric, compose_UAT, compose_render, 5-axis composition, audience resolution, channel resolution, scenario resolution, brand register, governance binding, multiplicative-AND composition. Pairs with .cursor/rules/akos-quality-fabric.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT; D-IH-86-AU
authored: 2026-05-24
---

# Quality-Fabric Craft

> Codified at I86 Wave R close (drain7) to operationalise the 5-axis composition that the operator ratified at D-IH-86-AU (2026-05-20). The craft turns the multiplicative-AND rule from doctrinal claim into authoring practice. Ratified by D-IH-86-CT alongside the parent rule.

## When to use this skill

Read this skill before authoring or revising any **quality-bound artifact** — anything carrying an `audience:` frontmatter tag, any closure UAT, any sibling-repo deploy-triggering work, any brand-touching surface (deck slide body, dossier prose, web page, email body), or any Quality Fabric specialty canonical.

This skill assumes you have already read [`akos-quality-fabric.mdc`](../../../.cursor/rules/akos-quality-fabric.mdc) (the *when*) + [`HOLISTIKA_QUALITY_FABRIC.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md) (the parent meta-doctrine).

## Core principles

### Principle 1 — Resolve all 5 axes BEFORE drafting prose

The most common failure mode is to draft the artifact first and reverse-engineer the bar after-the-fact. The bar then bends to fit the draft, not vice versa. Always:

1. **Audience** — FK-resolve `audience:` against `AUDIENCE_REGISTRY.csv`. Multi-audience → strictest constraint per downstream axis.
2. **Channel** — FK-resolve `channel:` against `CHANNEL_TOUCHPOINT_REGISTRY.csv` (optional today; advisory). Absence → audience-class default.
3. **Scenario** — FK-resolve `scenario:` against `PERSONA_SCENARIO_REGISTRY.csv` (optional today). Absence → parent-initiative scope description.
4. **Brand** — always non-null; the variable is the register (CORPINT-internal vs translated-external per `akos-brand-baseline-reality.mdc`).
5. **Governance** — always non-null; determined by asset class per `PRECEDENCE.md`.

Cite the resolved axes in the artifact's frontmatter so the resolution is auditable.

### Principle 2 — Multiplicative-AND, not additive, not last-axis-wins

When constraints from two axes appear in conflict, BOTH apply. Don't drop one. Don't average. Don't let the latest-considered axis win. The compose() function is a logical AND across all 5 axes; the artifact must satisfy every constraint from every axis.

When constraints genuinely conflict (e.g., audience demands brevity but governance demands completeness), surface as inline-ratify gate per `akos-inline-ratification.mdc` — let operator pick the reconciliation rather than silently choosing.

### Principle 3 — Per-axis doctrine is the source of truth (don't infer from prior outputs)

Don't infer brand voice from prior outputs you've authored; read [`BRAND_DO_DONT.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_DO_DONT.md). Don't infer channel norms from intuition; read the per-channel doctrine (when minted) or call out the gap explicitly in `notes:` frontmatter. Don't infer audience expectations from "what investors want"; read `AUDIENCE_REGISTRY.csv` row for the specific J-IN class.

Each axis has a canonical SSOT; the skill is to consult the SSOT not to wing it.

### Principle 4 — Under-specified artifacts cannot reach PASS

If any of the 5 axes is unresolvable (e.g., audience tag missing; can't determine the right strictness), the artifact is **under-specified** and cannot reach a PASS verdict in its UAT/UX bar. Either:

- Resolve the axis (via inline-ratify per Principle 2 when contested).
- Carry the under-specification flag explicitly in `notes:` frontmatter with a closure-target.

Refusing to author under-specified artifacts is correct behaviour, not blocking behaviour.

### Principle 5 — Specialty canonicals inherit the fabric

When authoring a new specialty canonical that materialises a compose() function (per parent rule RULE 7), the canonical:

1. Cross-references `HOLISTIKA_QUALITY_FABRIC.md` as parent meta-doctrine.
2. Names its compose() function explicitly (e.g., `compose_UAT(audience, channel, scenario, brand, governance) → 7-class UAT shape`).
3. Lands at `status: charter` if not yet exercised; promotes to `status: active` per QF §10 criteria.
4. Cites internal precedents per `akos-applied-research-discipline.mdc` RULE 1.
5. Cites at least one external research source if novel per RULE 2.

## Per-axis craft

### Audience axis

- Resolve `audience:` against `AUDIENCE_REGISTRY.csv` (J-OP / J-AIC / J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO).
- Multi-audience tags use `;`-separated list; resolution picks the STRICTEST constraint per downstream axis.
- Read the row's `register_class` + `delivery_format` + `voice_register` columns to derive per-axis constraints.

### Channel axis

- Optional today (advisory per `akos-external-render-discipline.mdc` RULE 7).
- When present, resolve `channel:` against `CHANNEL_TOUCHPOINT_REGISTRY.csv` (CHAN-EMAIL-OUTBOUND / CHAN-LINKEDIN-DM / CHAN-WEB-FORM / etc.).
- When absent, fall back to audience-class default channel (look up in `AUDIENCE_REGISTRY.csv` `default_channel` column).

### Scenario axis

- Optional today.
- When present, resolve `scenario:` against `PERSONA_SCENARIO_REGISTRY.csv`.
- When absent, scenario falls back to the artifact's parent-initiative scope description.

### Brand axis

- Always non-null.
- Variable: CORPINT-internal register (audience J-OP / J-AIC only) vs translated-external register (any other audience).
- Read `BRAND_BASELINE_REALITY_MATRIX.md` §3 translation table; never render internal tokens to external audience.

### Governance axis

- Always non-null.
- Determined by asset class per `PRECEDENCE.md`.
- For canonical CSVs: canonical-CSV gate per `akos-baseline-governance.mdc`.
- For deploy-triggering work: per-vendor gate per `akos-deploy-health.mdc`.
- For external-delivery surfaces: render-trail per `akos-external-render-discipline.mdc`.

## Pre-flight checklist

1. All 5 axes resolved BEFORE drafting any prose.
2. Frontmatter declares the resolved axes (`audience:`, `channel:` if known, `scenario:` if known, `linked_decisions:` for governance, brand register implicit in content).
3. Per-axis doctrine consulted (NOT inferred from prior outputs).
4. Multiplicative-AND composition applied; conflicts surfaced as inline-ratify (not silently chosen).
5. Under-specified axes either resolved OR explicitly flagged in `notes:` with closure-target.
6. If new specialty: cross-references QF parent + names compose() function + cites precedents.
7. UAT report's findings table addresses each axis (PASS/SKIP/N/A per axis).

## Anti-patterns

- **AP1 — Reverse-engineer the bar from the draft.** The draft bends governance to fit; bad doctrine.
- **AP2 — Drop the conflicting axis.** Multiplicative-AND violated; one stakeholder loses.
- **AP3 — Last-axis-wins.** Whoever the agent thought of last wins; arbitrary.
- **AP4 — Silent reconciliation.** Agent picks reconciliation without surfacing; operator can't audit.
- **AP5 — Infer brand voice from prior outputs.** Doctrinal drift compounds across artifacts; the SSOT loses authority.

## Cross-references

- Parent rule: [`akos-quality-fabric.mdc`](../../../.cursor/rules/akos-quality-fabric.mdc).
- Parent canonical: [`HOLISTIKA_QUALITY_FABRIC.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md).
- Specialty SSOTs: [`UAT_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md), [`UX_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UX_DISCIPLINE.md), [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md), [`INDEX_INTEGRITY_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md), [`DATAOPS_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md), [`MKTOPS_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/MKTOPS_DISCIPLINE.md), [`TECHOPS_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/TECHOPS_DISCIPLINE.md).
- Axis SSOTs: [`AUDIENCE_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv), [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv), [`PERSONA_SCENARIO_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Resonance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv), [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md), [`PRECEDENCE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md).
- Sister skills: [`inline-ratify-craft`](../inline-ratify-craft/SKILL.md), [`applied-research-craft`](../applied-research-craft/SKILL.md), [`external-render-craft`](../external-render-craft/SKILL.md).
- Ratifying decisions: D-IH-86-CT (this skill mint), D-IH-86-AU (parent rule ratification).
