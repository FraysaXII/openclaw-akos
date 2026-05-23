---
name: inline-ratify-craft
description: Use when authoring an inline AskQuestion ratification gate during phase execution in this AKOS workspace. Codifies the craft for transforming evidence-dependent and spot-check operator decisions into structured option sets that compound the operator's reasoning rather than extract a yes/no. Triggers on any phrase like inline-ratify, AskQuestion, ratification gate, operator decision, option set, evidence sweep + ratify, or when a phase plan contains a gate_type of inline-ratify. Pairs with .cursor/rules/akos-inline-ratification.mdc (the rule that governs when to inline-ratify); this skill governs how to do it well.
version: 1.0.0
ratifying_decisions: D-IH-80-A; D-IH-80-E
authored: 2026-05-16
---

# Inline-Ratify Craft

> Codified at I80 P3 from the I79 closure conversation. The operator framing that earned this skill: *"i'd like you to help other agents nail them like you did!"* The craft turns AskQuestion calls from decision-extraction into thinking-amplification. Ratified by D-IH-80-E.

## When to use this skill

Read this skill before authoring any AskQuestion call inside a phase that hits an inline-ratify gate. Also read it before designing a phase plan that contains a gate_type of inline-ratify. Do not read it for stop-and-clarify blockers (those follow `.cursor/rules/akos-governance-remediation.mdc` — write a 5-line summary and halt; do not ask).

The skill assumes you have already read [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc), which defines what an inline-ratify gate is. This skill is the craft layer on top of that rule.

## Core principles (the six that compound)

These six principles compound — applying any one without the others underperforms; applying all six produces the multiplier effect the I79 closure conversation called out. The order matters: each builds on the prior one.

### Principle 1 — Run the evidence sweep first

Before posing any question, run the relevant `Grep`, `Read`, `Glob`, or `SemanticSearch` calls and inventory the actual repo state that bears on the decision. Identify:

- the files involved by full path
- the rows in canonical CSVs that bear on the decision
- the prior decision-register rows that ratified related material
- the current code-or-text state of any function or section the decision will modify

The evidence sweep is non-negotiable. Skipping it produces options that look like brainstorming rather than options grounded in repo state. Operators waste cycles re-deriving evidence the agent should have surfaced.

The sweep is also the agent's own thinking aid. About half the time the sweep collapses what the agent thought were two or three plausible options into one obvious option (because the repo state already commits to a direction). The other half it reveals an option neither the agent nor the operator had named.

### Principle 1.5 — Research-sweep when the question is novel

Principle 1 names the evidence sweep — `Grep`, `Read`, `Glob`,
`SemanticSearch` over **repo state**. This is the right move for most
inline-ratify gates because most decisions can be ratified from what the
repo already commits to.

But some inline-ratify gates pose questions the repo has no prior
commitment on. The operator's framing is genuinely novel; the closest
sibling canonical does not yet take a position; no decision-register row
ratifies the relevant axis. For these gates, the evidence sweep collapses
to "the repo is silent" and the agent needs a second sweep: the
**research sweep** over industry precedent.

The research sweep is `WebSearch` + `WebFetch` + (optionally) reads of
named precedent corpus (DAMA-DMBOK 3.0; ResearchOps Community publications;
Kate Towsey *Research That Scales*; industry analyst notes; academic
papers). The sweep is **conditional on novelty** — if the evidence sweep
already converged on an obvious authoring direction, research sweep is
light (1-2 confirmatory queries). If the evidence sweep surfaced genuine
silence, research sweep is heavier (5-10 queries; multiple precedent
sources).

How to know when novelty fires:

- The inline-ratify gate's options that the agent can draft from repo state
  alone all carry low-confidence rationales (every option boils down to
  "the operator should pick because we don't know"). That is the signal
  that the repo cannot make the call alone.
- The closest sibling canonical's `last_review` predates the topic the gate
  poses (e.g., posing a 2026 LLM substrate question against a canonical
  whose last review was 2025).
- The topic appears in `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` as a
  `candidate` (i.e., the operator has flagged it for research but has not
  yet written the synthesis).
- The topic surfaces in `docs/wip/intelligence/` as in-flight WIP without
  yet a canonical home.

When novelty fires, the agent runs the research sweep BEFORE posing the
inline-ratify gate. The sweep's output enriches the option set with
industry-precedent framings the agent could not have generated from repo
state alone. This is responsible for the "third path" emergence Principle
6 names — many of those third paths are not novel-to-the-industry, they
are novel-to-Holistika because the agent surfaced them via research sweep.

Cite the research sweep inline in the inline-ratify call's option labels
(per Principle 4: cite evidence inline by file path or URL). Example:

```
Option C — adopt the ResearchOps 8-Pillar shape (novel framing —
ResearchOps Community canonical at https://researchops.community/about/
adopted in 2018 + reaffirmed in Kate Towsey 2024)
```

The research sweep's full output (URLs + retrieval dates + relevance
summaries) goes in the Evidence-base section of whichever canonical the
inline-ratify gate ratifies into (per `RESEARCH_HEAD_DISCIPLINE.md` §6
Backfill protocol). The inline-ratify call cites only the load-bearing
snippet, not the full sweep.

Cross-references for this principle:

- [`RESEARCH_HEAD_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md)
  §3.2 (Sourcing pillar) + §5 (External-research checklist).
- [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc)
  RULE 2 (external citation when novel framing).
- Principle 1 (evidence sweep) above — the foundation; Principle 1.5
  extends rather than replaces.
- Principle 6 (welcome novel framings) below — the receiver; many novel
  framings emerge from research sweeps.

### Principle 2 — Distil to ranked options with rationale embedded inline

Two to five options per question. More than five and the operator's working memory degrades; fewer than two and you do not need an inline-ratify in the first place — you need an executive call (which is a different posture; do not gate-ask when the right move is just-do).

Each option must carry:

- a short headline label (the choice itself, in 5-12 words)
- a one-paragraph rationale that names why this option is plausible
- where applicable, the tradeoff this option makes against the other options

Bare option labels with no rationale are the most common failure mode. Operators decide better with reasoning attached than from labels alone. A label like "option B" with no rationale forces the operator to reverse-engineer the rationale from context, which is slower than just reading it.

### Principle 3 — Mark the recommended default when one exists

When the agent's analysis has a clear leader, label it. Use the format `(recommended — <one-clause reason>)` in the option label. Examples:

- `Option A — body file at level 4, addendum at level 5 (recommended — DAMA-ready paired-file pattern)`
- `Option C — defer to I72 follow-up (recommended — out of scope for this phase per D-IH-79-Z)`

The recommended-default mechanism is asymmetric — it lowers the cost of operator-agreement (a single message: "go with the recommendation") while preserving the cost of operator-disagreement (the operator still has to articulate the alternative they prefer and why). This asymmetry is correct: most decisions the operator delegates to agent expertise should pass through quickly; the few that warrant operator pivoting deserve the friction.

Do not mark a recommendation when:

- the agent's analysis is genuinely split (e.g., 50/50 between two legitimate paths)
- the decision is irreversible and high-blast-radius (let the operator carry the full weight)
- the operator has explicitly asked for the call to be deferred to them (read prior conversation context)

### Principle 4 — Cite evidence inline by file path and line range

When an option references a specific row in a canonical CSV, a specific section of an SOP, or a specific decision-register row, name the file and the row or line range. Examples:

- `Option A — extend pattern_class enum (per D-IH-79-D — DECISION_REGISTER.csv L42)`
- `Option B — add to existing register_dimension class (per akos/hlk_design_pattern_csv.py L18 VALID_PATTERN_CLASSES frozenset)`
- `Option C — defer (per akos-planning-traceability.mdc §"Plan-quality bar" — three-mermaid requirement)`

This lets the operator verify the claim in seconds rather than asking the agent to repeat the underlying evidence. It also disciplines the agent — if you cannot cite a file path for an option, the option is probably under-evidenced and you should run more sweep before posing the question.

### Principle 5 — Batch tightly-coupled decisions in a single AskQuestion call

When two or three sub-decisions are coupled — e.g., "which framing for the 3 Group-G rows" plus "should we add a baseline_organisation row" plus "what cadence should the runbook fire on" — surface them as a single batched call. The AskQuestion tool supports up to 6+ questions per call.

Why batch:

- the operator answers the set as a coherent unit; downstream agent work continues without round-trip latency
- coupling becomes visible — the operator may notice an inconsistency between their answers to coupled questions and self-correct mid-batch
- the agent's reasoning quality is more transparent — coupled questions surface the structural shape of the decision

Do not batch decisions that are independent. If question A and question B can be answered in either order without affecting each other, they can be separate calls. Batching independents bloats the operator's working memory.

### Principle 6 — Welcome novel framings when they unlock paths the operator had not considered

Sometimes the right options are not the obvious dichotomy. When the agent's evidence sweep surfaces a third path neither the agent nor the operator had named at the start, surface it as a labelled option with rationale. This is responsible for most of the "advancing three months in a single initiative" compounding the operator named at I79 closure.

Novel-framing options should be marked clearly:

- `Option D — paired-file with cross-area access-level routing (novel framing — allows level-4 body for executors AND level-5 addendum for system-owners simultaneously, satisfies DAMA + scalability + granularity all at once)`

Novel framings are not contrarian for the sake of contrarian. They emerge when the agent has done the evidence sweep thoroughly and notices a structural option the operator's framing did not anticipate. If you are tempted to add a novel-framing option but cannot cite the structural insight that motivated it, the option is probably half-baked; either think it through more or do not surface it.

### Principle 7 — Surface internal-first as a first-class option, not just outsource-path (placeholder; full mint per OPS-81-21)

> **Placeholder per D-IH-81-P amendment 2026-05-23 (P1-c extended scope item 8).** Full Principle authoring is forward-chartered as **OPS-81-21** (forwarded to I80; pairs with D-IH-80-E skill-craft promotion). When the OPS row executes, this section expands with the full anti-pattern dissection + worked-example + counter-discipline.

**The failure mode this Principle closes:** when authoring an inline-ratify option set for a backbone-Ops-area judgment-layer question (FINOPS revenue recognition / LegalOps adviser routing / PeopleOps role activation / RevOps engagement orchestration), the agent reflexively defaults to *industry-standard outsource-path framing* (CFOaaS / external counsel / external HR firm / external SDR firm) and presents internal-first ownership only as a secondary or implicit option. This is a class of failure-mode — not a single bug. The worked example: the FINOPS end-to-end synthesis (`docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md` §6 original framing pre-amendment) framed CFOaaS-at-incorporation as the conservative default; the operator's project thesis is internal-first-with-research-grounded-confidence-rising; the agent had to be corrected post-ratification via a doctrine amendment (D-IH-81-P).

**Counter-discipline:** when authoring an option set for any Ops-area judgment-layer question, the agent surfaces internal-first ownership as a first-class option alongside any outsource-path option, with rationale rooted in the operator's project thesis (per Principle 1 evidence sweep — read the operator's prior framings + scratchpad entries + active doctrine + research-grounding posture per `akos-applied-research-discipline.mdc` RULE 1) before defaulting to industry-standard outsource framing. If the operator's stated thesis is internal-first, that should be the recommended default, with outsource-path as the reserved option triggered by discrete signals — not the inverse.

**Sanity-check before posting:** "Have I read the operator's project thesis on this area? Have I surfaced internal-first as a first-class labelled option (not just a footnote / not just embedded inside Option B / not just implicit)? Have I named the activation triggers for the outsource-path option (so it's a *reserved option*, not the default)?"

**Cross-area Ops-wiring discipline implication (per D-IH-81-O):** when the cross-area Ops-wiring review discipline activates (per `_candidates/i-nn-cross-area-ops-wiring-review.md`), this failure-mode sanity-check becomes part of every backbone-Ops-area sweep — the discipline inherits the failure-mode guard automatically.

## Anatomy of a great inline question

A complete inline-ratify call has this shape:

```
title: <short title naming the gate>
questions:
  - id: <stable-slug>
    prompt: <one-sentence question naming the decision + brief context (1-2 lines max)>
    options:
      - id: <option-slug-a>
        label: Option A — <headline> (recommended — <reason if applicable>)
      - id: <option-slug-b>
        label: Option B — <headline>
      - id: <option-slug-c>
        label: Option C — <headline> (novel framing — <structural insight>)
```

The prompt is one sentence. Context that does not fit in one sentence belongs in the option labels (which can be longer). Multi-sentence prompts confuse the operator about which decision is being asked.

The option labels are the rationale-bearing surface. Every option label contains the choice plus the rationale plus (where applicable) the recommendation flag plus (where applicable) the novel-framing flag.

Stable IDs let the operator reference an option in free-text replies (e.g., "Selected option(s) p6-fk-seed-bundle-decision: option A and don't hesitate to..."). Use kebab-case slugs that name the decision class.

## Worked examples — good inline questions

### Example 1 — paired-file naming convention (I80 P0)

```
title: SOP body/addendum naming convention
questions:
  - id: sop-addendum-naming
    prompt: Should the body/addendum split be implemented as paired files (SOP-XYZ.md + SOP-XYZ.addendum.md) or as a single file with body and addendum sections separated by a marker?
    options:
      - id: paired-files
        label: Option A — Paired files (recommended — DAMA-ready; each file is a discrete metadata row consumable by Supabase mirror / Neo4j / RAG without parsing markdown structure; cleaner access-level routing per file)
      - id: single-file
        label: Option B — Single file with section marker (simpler initial implementation; harder to consume programmatically; access-level routing degrades to within-file section parsing)
```

Why this works: two ranked options; recommendation marked with one-clause reason; rationale embedded inline; the tradeoff is named explicitly (DAMA-ready vs simpler-initial); operator can verify the claim by checking the cited consumers.

### Example 2 — engagement template framing (I79 P6 Round 6)

```
title: Group-G framing for inherited_pattern_id seeding
questions:
  - id: p6-fk-seed-bundle-decision
    prompt: For the 3 Group-G rows (outsourced helper SOC review + percentage collaborator payout + investor advisor round review), which parent pattern should they declare given the single-FK column constraint?
    options:
      - id: paired-sop-runbook
        label: Option A — pattern_paired_sop_runbook (the rows are paired SOP+runbook; this captures the implementation form)
      - id: engagement-model-taxonomy
        label: Option B — pattern_engagement_model_taxonomy (recommended — the rows instantiate engagement model classes; this captures the load-bearing parent without which the row collapses)
      - id: defer-many-to-many
        label: Option C — defer all 3 to a successor initiative that adds many-to-many FK support (preserves both framings; cost is delaying baseline tranche by ~1 phase)
      - id: split-bundle
        label: Option D — split: row 1 paired_sop_runbook, rows 2-3 engagement_model_taxonomy (preserves per-row truth; cost is asymmetric framing within a single tranche)
```

Why this works: four options including one defer-to-successor and one split-bundle (novel framing surfacing the heterogeneity). The recommendation is the load-bearing parent option B with a clear "without which the row collapses" rationale. The operator can pivot to D ("option A but I wonder why option D seems right too — I'll need your expertise here") and the agent's reply has a clean path forward because the analysis is already on the table.

### Example 3 — access level routing (I80 P0)

```
title: Stakeholder lenses access level routing
questions:
  - id: lenses-access-level
    prompt: Where should the stakeholder lenses canonical sit in the access-level lattice?
    options:
      - id: level-4-body-only
        label: Option A — single file at level 4 internal-team (simplest; matches existing PEOPLE_DESIGN_PATTERN_LIBRARY.md posture)
      - id: level-5-cleared-only
        label: Option B — single file at level 5 internal-cleared (matches the founder-reflection access target; trades discoverability for confidentiality)
      - id: paired-files-routed
        label: Option C — paired files (level 4 body + level 5 addendum for founder-reflection layer) (novel framing — DAMA-ready paired-file structure; satisfies access-level granularity requirement; first instantiation of pattern_sop_addendum_split)
```

Why this works: three options with the novel-framing option C marked clearly; the rationale names DAMA + access-level granularity + first-instance benefit explicitly; the operator's response ("option C is even better because I think it ensures DAMA, scalability, and makes ready for more knowledge management system in a lot of supports because of the granularity") shows the option's framing unlocked operator reasoning that produced a more articulate ratification than option A alone would have.

## Worked examples — common bad patterns and how to fix them

### Bad pattern 1 — bare option labels with no rationale

```
prompt: Body/addendum naming convention?
options:
  - Option A
  - Option B
  - Option C
```

What is wrong: no rationale; operator must derive why each option is plausible from prior conversation. Likely outcome: operator picks A by default ("first option = recommendation"), missing the structural call.

Fix: replace each bare label with a headline + one-paragraph rationale per Principle 2.

### Bad pattern 2 — five-sentence prompt that buries the decision

```
prompt: We've been discussing the body/addendum pattern, and I think there are several ways to implement it. We could go with paired files, or we could use a single file with section markers, or we could defer the whole thing. Each has tradeoffs. The paired-file approach is more DAMA-aligned, but the single-file approach is simpler. What do you think?
```

What is wrong: the prompt re-states what should be in the options. By the time the operator reads the options, their working memory is already half-spent on the prompt. Also, the prompt's "what do you think" framing is decision-extraction (yes/no), not thinking-amplification.

Fix: prompt becomes one sentence — `Should the body/addendum split be implemented as paired files or as a single file with section markers?` — and all the rationale moves into the option labels.

### Bad pattern 3 — irrelevant options to inflate the choice count

```
options:
  - Option A — paired files
  - Option B — single file
  - Option C — defer to next quarter
  - Option D — do nothing
  - Option E — outsource to consultant
```

What is wrong: D and E are not real options; they pad the choice count without adding signal. The operator's working memory is consumed by parsing options that should not be on the table.

Fix: cut to the two real options. If a defer option is genuinely on the table (e.g., the team is over-loaded), keep it; otherwise drop. Two ranked options + one defer + one novel framing is usually the sweet spot (3-4 options total).

### Bad pattern 4 — over-batching independent decisions

```
title: I80 architectural decisions
questions:
  - id: q1
    prompt: Body/addendum naming?
    options: [...]
  - id: q2
    prompt: Initiative packaging?
    options: [...]
  - id: q3
    prompt: Adapter status enum extension?
    options: [...]
  - id: q4
    prompt: Quarterly cadence for stakeholder lenses?
    options: [...]
  - id: q5
    prompt: Where to put the inline-ratify skill?
    options: [...]
  - id: q6
    prompt: Engagement template promotion threshold?
    options: [...]
```

What is wrong: q1 + q2 are coupled (both about I80 packaging); q3 belongs to a different initiative entirely; q4 + q5 are tangentially related but not coupled; q6 is unrelated. The operator's working memory is fragmented.

Fix: split into multiple smaller batches. q1 + q2 + q5 in one call (I80 packaging set); q4 in a separate call (operational cadence); q6 in a different phase entirely (engagement template lifecycle); q3 should not be in this phase at all.

### Bad pattern 5 — recommendation flag with no rationale

```
options:
  - Option A — paired files (recommended)
  - Option B — single file
```

What is wrong: the recommendation flag is empty calorie. Operators learn to ignore recommendation flags that do not carry the one-clause reason. The flag becomes noise.

Fix: every recommendation flag carries a one-clause reason — `(recommended — DAMA-ready paired-file pattern)`. If you cannot articulate the one-clause reason, you should not be recommending the option.

## Pre-flight checklist (run before every AskQuestion call)

Before invoking AskQuestion, walk this checklist mentally:

- [ ] Have I run the evidence sweep? (Grep + Read + Glob covering the affected files + canonical CSVs + decision register)
- [ ] Are the options 2-5? (Not 1, not 6+)
- [ ] Does each option carry a headline + rationale?
- [ ] If there is a clear leader, is it labelled `(recommended — <reason>)`?
- [ ] Do options that cite repo state name the file path and where applicable the line range?
- [ ] Are the questions in this batch tightly coupled? (If not, split.)
- [ ] Is the prompt one sentence?
- [ ] Does any option introduce a novel framing? (Check: the operator might pivot to it.)
- [ ] Have I avoided the recommendation flag with no rationale?
- [ ] Have I avoided padding options just to inflate the choice count?

If any item fails, fix before posting.

## Time-box recovery — what to do when the operator does not answer

The inline-ratify rule allows the agent to fall back to the recommended default after a reasonable window of operator silence and clean validators. Concrete posture:

- if the operator is mid-conversation and engaged elsewhere in the same session, wait for their attention to come back to this question; do not ping
- if the operator has not responded for 24+ hours and the question has a recommended default + clean validators + the decision is reversible, the agent may continue with the recommended option AND log the auto-decision in the decision register with `decision_source: agent_inline_default`
- if the decision is irreversible (canonical CSV mutation + trademark filing + public prose publish + production deploy), do not auto-default; halt and escalate per `akos-governance-remediation.mdc` posture

Auto-default is a safety valve, not a default mode of operation. Operator silence on a high-blast-radius decision is itself a signal — it usually means the decision warrants more thinking than a 24-hour window allows. Respect the signal.

## Anti-patterns to avoid

- **Decision-extraction framing.** Asking "does this look right?" or "are you ok with this?" is decision-extraction. Asking "which of these N options should we adopt?" with rationale-bearing labels is thinking-amplification. The latter compounds; the former does not.

- **Re-asking what was already ratified.** Before authoring a new AskQuestion, check the decision register and prior conversation for a pre-existing ratification. If `D-IH-NN-X` already covered this decision class, cite it and proceed; do not re-ask. The exception is when material conditions changed (new evidence, new constraint, ratifying-decision was conditional on a state that no longer holds) — in that case cite the prior decision in the prompt and frame the new question as "given that <new condition>, should we revisit?"

- **Asking architectural questions during execution.** If the question changes the plan's architecture (sub-decision ripples back to multiple phases), it is a planning-time question. Halt execution; emit a `STOP-AND-CLARIFY` summary; re-plan. Inline-ratify is for evidence-dependent and spot-check decisions, not for architectural decisions surfaced mid-execution.

- **Ignoring operator's free-text alongside structured replies.** Operators sometimes reply with `Selected option(s) X: option B` followed by free-text that pivots to option D or asks for a hybrid. The free-text is the more important signal; never ignore it. The structured selection is the agent-friendly form; the free-text is the operator's actual reasoning.

- **Surfacing technical jargon in option labels.** The agent is the technical layer; the operator reads the option labels in the operator-facing register. Internal-jargon tokens (validator names, schema field names, FK column names) are fine when they refer to concrete repo artifacts; gratuitous technical jargon (shorthand, internal codenames, methodology shorthand) is noise.

- **Industry-default outsource-path reflex.** When the inline-ratify gate is about Ops-area judgment-layer ownership (FINOPS revenue-rec / LegalOps adviser routing / PeopleOps role activation / RevOps engagement orchestration / similar), reflexively defaulting to industry-standard outsource-path (CFOaaS / external counsel / external HR firm / external SDR firm) as the recommended option without first checking the operator's project thesis is a class of failure-mode. See Principle 7 above + OPS-81-21 for the full mint + worked example (FINOPS synthesis §6 original framing pre-D-IH-81-P amendment).

## Common pitfalls and recoveries

### Pitfall: I have run the evidence sweep but I do not see clear options

Sometimes the sweep reveals that there is no real option to ratify — the repo state already commits to a direction. Recovery: do not author an AskQuestion. Continue executing the obvious direction; if you must record the decision, mint it as `decision_source: agent_executive_call` in the decision register with a one-paragraph rationale. The operator will review during normal cadence; if they disagree, they revert.

### Pitfall: my recommended default conflicts with the operator's stated preference earlier in the session

Recovery: surface the conflict explicitly in the option label or the prompt. Format: `Option A — paired files (recommended — DAMA-ready; note: tension with your earlier framing of "simplest initial path" — this option trades initial simplicity for DAMA readiness)`. The operator can pivot to A or back to their earlier framing; either way, the conflict is named.

### Pitfall: the operator answers ambiguously or with mixed signals

Recovery: ask one clarifying question with the ambiguity surfaced. Format: `Your reply selected option B but the free-text mentions option D — would you like to ratify D as the choice (and I'll re-author the relevant deliverables to match), or stay with B and incorporate the D framing as a future-charter note?` Most ambiguities are accidental — the operator typed quickly. The clarification call lets them disambiguate without pretending the structured selection is canonical when their reasoning is in the free-text.

### Pitfall: the operator pivots to an option that requires a phase-plan revision

Recovery: name the revision explicitly. Format: `Adopting your option D requires extending Phase N from 1 day to 2 days (additional deliverables: X, Y, Z). I will update master-roadmap.md + files-modified.csv to reflect. Confirm to proceed?` This is itself an inline-ratify call (the option-D pivot was the first; the plan-revision is the second). The operator confirms or backtracks; either way, the revision is governed.

## Integration with akos rules and skills

This skill sits under `.cursor/skills/inline-ratify-craft/` and pairs with these rules:

- [`.cursor/rules/akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) — defines when to inline-ratify (evidence-dependent + spot-check + architectural-during-planning); this skill defines how to do it well.
- [`.cursor/rules/akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar" — phase plans declare gate_type per phase; this skill is the executor-side complement that fires at gate moments.
- [`.cursor/rules/akos-agent-checkpoint-discipline.mdc`](../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — pause-record vs self-checkpoint cadence; inline-ratify supersedes pause-record for evidence-dependent gates.
- [`.cursor/rules/akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc) — opt-stop-report for blockers (validator failures, security incidents); this skill governs only the decisions, not the blockers.
- The `hlk-planning-system` skill in the personal skill set — the planning-time complement; this skill is the execution-time complement.

When an agent is uncertain whether to use inline-ratify or a different posture (executive call + stop-and-clarify + pause-record), this skill's "When NOT to use" section in [`.cursor/rules/akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) is the disambiguator.

## Provenance

This skill was minted at I80 P3 (2026-05-16) per D-IH-80-E. The craft codified here was demonstrated across seven inline-ratify rounds in I79 (2026-05-13 through 2026-05-15) plus the I80 P0 charter session. The operator's framing at I79 closure named the multiplier explicitly — the inline ratification craft as the lever that compresses the operator's reasoning cycle from months into hours, when the architecture is also clear.

The skill is durable across agent generations: any successor agent reading this file inherits the craft without having to re-derive it. Future I-NN initiatives that surface refinements to the craft (e.g., novel question shapes, new failure modes, additional anti-patterns) should extend this skill rather than authoring a sibling skill.
