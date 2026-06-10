---
name: brand-baseline-reality-craft
description: Use when authoring, editing, or generating prose for any public-facing surface OR internal counterparty-side artefact in this AKOS workspace. Codifies the craft for the dual-register translation (CORPINT-internal vs translated-external) per D-IH-66-M. Triggers on brand baseline reality, dual register, CORPINT internal, translated external, counterparty brief, objections brief, deck slide body, dossier prose, recruiter copy, partner pitch, ENISA evidence, founder bio, brand jargon audit, BRAND_BASELINE_REALITY_MATRIX. Pairs with .cursor/rules/akos-brand-baseline-reality.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT; D-IH-66-M
authored: 2026-05-24
---

# Brand-Baseline-Reality Craft

> Codified at I86 Wave R close (drain7) to operationalise the D-IH-66-M dual-register contract (I66 P2 ratification). The craft turns brand voice from intuitive choice into deterministic translation. Ratified by D-IH-86-CT alongside the parent rule.

## When to use this skill

Read this skill before authoring or editing prose for any **public-facing surface** (`boilerplate/`, public deck slide bodies, ENISA evidence, partner pitch body, founder bio, email signatures, recruiter copy) OR any **internal counterparty-side artefact** (`*.counterparty-brief.md`, `*.objections.md`, `docs/wip/intelligence/`).

This skill assumes you have already read [`akos-brand-baseline-reality.mdc`](../../../.cursor/rules/akos-brand-baseline-reality.mdc) + [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md).

## Core principles

### Principle 1 — Ask the recipient-frame question FIRST

Before writing any prose that will reach a customer, investor, advisor, ENISA reviewer, partner, recruiter, collaborator, or press journalist, ask:

> *"Does the recipient assume the tradecraft frame? If no, translate to external register before rendering."*

The translation table in `BRAND_BASELINE_REALITY_MATRIX.md` §3 is the binding SSOT. The question is asked BEFORE drafting, not after. Post-hoc translation always leaves residue.

### Principle 2 — Default to external register when in doubt

When unsure which surface a piece of prose will reach, render in external register. Translation back (external → internal) is harder than translation forward (internal → external). Defaulting to external is the safe move.

### Principle 3 — Never auto-translate the canonical matrix

Edits to `BRAND_BASELINE_REALITY_MATRIX.md` must preserve the dual-register structure (internal column + external column side by side). Collapsing to a single column is a brand-canon collapse failure. The matrix's structural shape carries doctrinal information that the row-level translations alone don't.

### Principle 4 — Cite the matrix when in doubt

If the agent is unsure which side of the register a token belongs to, link to the matrix in an inline-ratify gate and ask the operator. The matrix is the SSOT; the operator clarifies edge cases.

### Principle 5 — HUMINT-as-ornament is the most common abuse

Do NOT gratuitously sprinkle internal-register tokens into private docs to "sound CORPINT." The vocabulary is functional; use it where it carries information value (per-engagement counterparty briefs, intelligence collection SOPs), not as branding for internal-facing prose.

### Principle 6 — External register is not "dumber"

External register translates discipline into recipient-readable language; it is not a simplification or softening. Drafts that read as marketing-fluff in external register are evidence of bad translation, not evidence that internal register is being lost. Re-translate.

## Translation table (key tokens)

Per `BRAND_BASELINE_REALITY_MATRIX.md` §3:

| Internal token | External rendering (context-dependent) |
|:---|:---|
| counterparty | client (B2B SME) / investor (fundraise) / regulator (ENISA) / counterparty-of-engagement |
| elicitation | structured discovery / discovery-call / discovery-questionnaire |
| reliability grading | source confidence / source quality / data confidence |
| intelligence collection | research / market research / structured research / context-gathering |
| intelligence report | research brief / engagement report / context memo / discovery output |
| approach techniques | engagement design / outreach approach / discovery design |
| baseline reality assessment | counterparty understanding / context understanding / audience analysis |

The translation is context-dependent (B2B SME vs investor vs ENISA pick different external tokens for "counterparty"). Don't substitute mechanically; pick the audience-appropriate rendering.

## Allowed / forbidden contexts (quick reference)

**Internal register OK** (J-OP / J-AIC audiences):

- `BRAND_BASELINE_REALITY_MATRIX.md` (the canonical itself).
- `docs/wip/intelligence/**/*.md`.
- Operator-private SOPs under `docs/references/hlk/v3.0/Research/Intelligence/canonicals/`.
- `*.counterparty-brief.md` + `*.objections.md` companions to decks.
- Internal AKOS-vault SOPs / decision logs / risk registers.
- Cursor rules + commit messages + PR bodies.
- Agent transcripts.

**External register only** (any non-J-OP/J-AIC audience):

- `boilerplate/` rendered DOM.
- `boilerplate/messages/*.json` (i18n strings).
- `hlk-erp/app/(public)/**`.
- Investor / advisor / ENISA / partner / recruiter / customer deck slide bodies.
- External dossiers (`docs/references/hlk/v3.0/_assets/advops/**/dossier_*.md`).
- Founder bio canonical.
- Email signatures.
- Press kit, recruiter copy, partner pitch bodies.

## Pre-flight checklist

1. Recipient-frame question answered FIRST (Principle 1).
2. Audience tag identified (J-OP / J-AIC = internal OK; any other = external only).
3. Translation table consulted for each candidate token.
4. Context-dependent rendering picked per audience (B2B vs investor vs ENISA).
5. Dual-register structure of matrix preserved if editing the canonical.
6. Drift gate `validate_brand_baseline_reality_drift.py` runs clean on the artifact.
7. No HUMINT-as-ornament in internal-facing prose.

## Anti-patterns

- **AP1 — Render internal tokens to external audience.** Most common failure; brand-canon collapse.
- **AP2 — Default to internal register.** Reverse of Principle 2; harder to translate back.
- **AP3 — Collapse matrix to single column.** Doctrinal information lost.
- **AP4 — Edit external surface and "let translation happen later".** Drift compounds; never gets translated.
- **AP5 — Mechanical token substitution.** Audience-context lost; "counterparty → client" for an ENISA dossier is wrong (should be "regulator").
- **AP6 — Soften external register to "fix" perceived dumbness.** Bad translation; doctrine integrity lost.

## Cross-references

- Parent rule: [`akos-brand-baseline-reality.mdc`](../../../.cursor/rules/akos-brand-baseline-reality.mdc).
- Canonical SSOT: [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md).
- Sister doctrine: [`BRAND_JARGON_AUDIT.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_JARGON_AUDIT.md) §4.1 (broader external-jargon list).
- Drift gate: [`scripts/validate_brand_baseline_reality_drift.py`](../../../scripts/validate_brand_baseline_reality_drift.py).
- Sister skill: [`external-render-craft`](../external-render-craft/SKILL.md) (the orthogonal format axis).
- Worked example: I66 P2 (rule mint) + I66 P5 (boilerplate rewrite).
- Ratifying decisions: D-IH-86-CT (this skill mint), D-IH-66-M (parent rule ratification).
