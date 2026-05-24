---
name: applied-research-craft
description: Use when authoring or revising any canonical, cursor rule, skill, or decision-register row in this AKOS workspace and the framing introduces a novel position. Codifies the internal-evidence-sweep + external-research-sweep + citation-integration + wave-closure-research-enrichment rhythm per akos-applied-research-discipline.mdc RULES 1-3. Triggers on research grounding, applied research, external citation, novel framing, internal precedent, evidence sweep + research sweep, RESEARCH_HEAD_DISCIPLINE, wave-close research enrichment, citation integration. Pairs with .cursor/rules/akos-applied-research-discipline.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT; D-IH-86-T
authored: 2026-05-24
---

# Applied-Research Craft

> Codified at I86 Wave R close (drain7) from the operator's framing at the I86 Wave H Combo C+D Lane D ratify gate (2026-05-19): *"applied research is a hot topic today and a competitive advantage if properly industrialized"*. The craft turns research grounding from afterthought ornament into compounding doctrine. Ratified by D-IH-86-CT alongside the parent rule.

## When to use this skill

Read this skill before:

- Authoring a new canonical CSV (RULE 1 — internal + external research backing mandatory).
- Authoring a doctrine canonical, cursor rule, skill, or decision-register row that introduces a novel framing (RULE 2 — external citation mandatory).
- Closing a wave inside a cluster-coordinator initiative (RULE 3 — "Research enrichment" subsection in wave-closure report).
- Triaging a research need surfaced by an inline-ratify gate Principle 1.5 trigger.

This skill assumes you have already read [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc) (the *when*) + [`RESEARCH_HEAD_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md) (the parent doctrine).

## Core principles

### Principle 1 — Distinguish evidence-sweep from research-sweep

These are two different sweeps with different tools:

| Sweep | Tools | What it searches | When it fires |
|:---|:---|:---|:---|
| Evidence-sweep | `Grep`, `Read`, `Glob`, `SemanticSearch` | Repo state (canonicals, decision rows, code, prior planning) | EVERY canonical/rule/skill mint (per `akos-inline-ratification.mdc` Principle 1) |
| Research-sweep | `WebSearch`, `WebFetch`, optional reads of cited corpus | Industry precedent (academic papers, vendor docs, industry analysts, named books) | Conditional on novelty (per RULE 2 of parent rule) |

They are NOT substitutes. Novel framings require BOTH. Evidence-sweep alone surfaces "the repo is silent on this" — that's the signal to invoke research-sweep, not the conclusion that grounding isn't needed.

### Principle 2 — Cite inline, not in a separate dossier

External citations belong in the canonical body or its Evidence-base section, NOT in a separate research-dossier file. Inline citation is half of the load-bearing claim — the doctrine says "X because Y (per Source Z)" and the reader can verify in seconds. A separate dossier breaks the citation-to-claim adjacency and creates inventory rot.

Citation format: prefer named author + year + title + (chapter/section) for books and reports; URL for vendor docs; DOI or stable URL for academic papers. The drain7 proposal §4 is a worked example of a 5-citation block.

### Principle 3 — The novelty test for external citation

Ask: *"Would a future reader, reading this canonical/rule/skill cold, encounter a position they could not derive from prior Holistika doctrine + first-principles thinking?"*

- **Yes** → novel framing → external citation MANDATORY (3-5 cites for the framing).
- **No** → refinement of prior Holistika ratification → external citation OPTIONAL (the prior decision-register row IS the precedent).

Refinements include: v2 extensions of v1 doctrine, tightenings of existing rules, new specialty mints that follow the established quartet pattern. Novel framings include: new pillars (e.g., Quality Fabric architecture), new mechanical contracts (e.g., the rule × skill pairing contract), new posture defaults (e.g., Option-5 conflict surfacing).

### Principle 4 — Wave-closure research enrichment is structural, not ornamental

Every wave-close UAT (per `akos-planning-traceability.mdc` §"UAT quality bar" §10 + parent rule RULE 3) carries a `## Research enrichment` subsection naming:

- Which canonicals were enriched with new research material during the wave.
- Which canonicals were identified as needing enrichment but deferred to a future wave.
- Which external sources were newly surfaced during the wave that should inform future authoring.

The subsection is brief (5-15 lines) and makes the operator's lived research practice **trackable across waves**.

## Per-canonical-class craft

### Canonical CSV mint (RULE 1)

Authoring sequence:

1. **Internal evidence-sweep**: Grep + Read every existing canonical CSV + every decision row + every process_list row + every baseline_organisation row that bears on the new register. Document the inventory in the ratifying decision row's `rationale` cell or in a planning-notes file.
2. **Novelty test**: is the new register a clone-of-existing-pattern (e.g., new sibling adapter registry following Normalised Adapter Pattern) or a novel framing? Clone → optional external cite. Novel → mandatory 3+ external cites.
3. **External research-sweep**: if novel, `WebSearch` 5-10 queries on the new register's domain. Capture authoritative sources. Cite at least 3 in the canonical's Evidence-base section.
4. **Inline citations in `linked_canonicals:` frontmatter** for internal precedents.
5. **Evidence-base section** in the canonical body for external citations + the novelty rationale.

### Doctrine canonical / cursor rule / skill mint (RULE 2)

Same as CSV mint above, but the novelty test is the gating mechanism. Refinements need 0 external cites (Holistika precedent suffices); novel framings need 3-5 external cites.

The drain7 proposal itself is a worked example: rule × skill pairing as a workspace-binding contract is novel enough to warrant 5 citations (ACT-R + Pattern Language + SRE Book + SECI + Anthropic Skills); the per-skill mints inside drain7 are refinements (each skill is a refinement of inline-ratify-craft's shape) so no per-skill external cites.

### Wave-closure research enrichment subsection authoring

Template:

```markdown
## Research enrichment (Wave <letter>)

### Canonicals enriched this wave

- `<canonical-path>` — added §"Evidence base" rows for [topic]; cites [Source A] + [Source B] (per RULE 1 backfill protocol).

### Canonicals identified as needing enrichment (deferred)

- `<canonical-path>` — forward-charter to Wave <letter+1> via OPS-NN-MM (next-review-trigger: <condition>).

### External sources newly surfaced this wave

- [Source A: full citation + URL] — relevant for [domain X canonicals]; consider citing in future mints.
- [Source B: full citation + URL] — relevant for [domain Y canonicals].
```

Keep this subsection ≤ 15 lines per wave-close.

## Pre-flight checklist (before any canonical/rule/skill mint)

1. Internal evidence-sweep completed (`Grep` + `Read` + `Glob` over relevant repo state).
2. Novelty test answered (yes → external cites mandatory; no → optional).
3. If novel: external research-sweep completed (5-10 queries; sources captured).
4. Inline citations integrated into canonical body (not separate dossier).
5. `linked_canonicals:` frontmatter populated for internal precedents.
6. Evidence-base section (or equivalent) carries external citations.
7. Wave-closure UAT will include `## Research enrichment` subsection.
8. Operator-discretion exemption checked (commit message carries `rule-exempt-research-discipline: <reason>` only when time-pressed AND backfill-deferred-and-tracked).

## Anti-patterns (forbidden by parent canonical §7)

- **AP1 — Research-as-ornament**: citing 1 paper to look rigorous, without integrating the source's actual position into the doctrine. The cite is decorative; the doctrine ignores the source.
- **AP2 — Research-after-the-fact-to-justify**: drafting doctrine first, then googling cites that match. Inverts the discipline; the doctrine is unfalsifiable.
- **AP3 — Research-as-procrastination**: spending 5 hours on WebSearch instead of authoring; the research becomes the deliverable, the doctrine never lands.
- **AP4 — Copy-paste-citations**: citing a source's abstract without reading the source. The cite is unverifiable; future readers can't validate.

## Recovery patterns

- **R1 — Time-pressed mint**: invoke operator-discretion exemption via `rule-exempt-research-discipline: <one-clause reason>` in commit message; backfill in next wave's research enrichment subsection.
- **R2 — Research-sweep returns nothing useful**: collapse to "the field is silent on this" + cite the search query + cite at least 1 first-principles reasoning chain. Acceptable when the doctrine is genuinely first-of-its-kind.
- **R3 — Found contradicting sources**: surface as inline-ratify gate (per `akos-inline-ratification.mdc`) — let operator choose framing rather than silently pick one.

## Cross-references

- Parent rule: [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc).
- Parent canonical: [`RESEARCH_HEAD_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md).
- Sister skills: [`inline-ratify-craft`](../inline-ratify-craft/SKILL.md) Principle 1.5 (research-sweep at inline-ratify gates), [`index-integrity-craft`](../index-integrity-craft/SKILL.md), [`external-render-craft`](../external-render-craft/SKILL.md).
- Worked examples: drain7 proposal §4 (5-citation block) + I86 Wave H Lane D dispatch (Combo C+D ratification) + I84 P3 substrate doctrine evidence-base (named author + year per-row).
- Ratifying decisions: D-IH-86-CT (this skill mint), D-IH-86-T (cluster burndown plan that included Combo C+D Research Head discipline).
