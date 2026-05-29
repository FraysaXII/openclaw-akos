---
name: aic-delegation-craft
description: Use when deciding which model-seat drives a piece of work in Cursor, setting up the operator's thinking-seat / execution-seat workflow, dispatching Composer subagents from an Opus session, configuring Custom Modes or the statusline for seat awareness, or recovering when an execution model misreads intent. Codifies the HOW of the AIC delegation protocol. Triggers on phrases like model routing, thinking seat, execution seat, Opus vs Composer, subagent dispatch, Custom Mode, statusline, switch back, misread recovery, delegate to AIC. Pairs with .cursor/rules/akos-aic-delegation.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-84-C; DQ-TAX-04 (2026-05-29)
authored: 2026-05-29
---

# AIC Delegation Craft

> The *how* layer paired with [`akos-aic-delegation.mdc`](../../rules/akos-aic-delegation.mdc).
> The rule says *when* to route between seats; this skill shows *how* to do it
> well, matched to the operator's working style (fast, messy, high-context
> input). Ratified 2026-05-29 (DQ-TAX-04 advisory-only; F5 per `D-IH-84-C`).

## When to use this skill

Read this before setting up the delegation workflow, dispatching subagents, or
recovering from a misread. Assumes you have read the paired rule, which defines
the two seats and the advisory non-goal (Cursor can't auto-switch the foreground
model).

## The two seats, in plain terms

| | Foreground thinking seat | Background execution seats |
|:---|:---|:---|
| Model class | Opus / thinking models | Composer-pinned subagents |
| Best at | judgment, scope, doctrine, messy input, irreversible calls | bounded mechanical work against a settled plan |
| The operator | talks to this seat first | rarely talks to directly; receives decomposed packets |
| Cost posture | expensive — use deliberately | cheap — parallelise freely |

The operator's deepest need: **stay messy in the thinking seat without guilt.**
Dump high-context, multi-topic, typo-heavy input to Opus; let it sort, decompose,
and dispatch. Do not make the operator pre-sort work into the "right" model.

## Principle — the seat frames, the operator decides

The thinking seat does **not** "own" the decision; it *frames* it and hands the
operator a clean choice with a recommended default. Judgment calls — which shape,
which trade-off, go / hold — are the **operator's**, surfaced as an inline-ratify
gate. Saying "let me switch to the thinking model to decide" is a category error:
the model *structures* the call; the human *makes* it. (Worked example: the
2026-05-29 entity-registry shape — the seat laid out three options + a
recommended default; the operator chose Option 1. The seat never needed to
"decide" anything; it needed to make the decision easy.)

## Pattern 1 — Opening prompts that signal the seat (no model names needed)

The operator should not have to remember model names. Teach these openers:

- *"Think with me about ..."* / *"Help me decide ..."* / *"Is this coherent ..."*
  → thinking seat (judgment).
- *"Go do ..."* / *"Apply ... across ..."* / *"Run the validators and fix ..."*
  → execution seat (mechanical), usually dispatched to subagents.

If an opener is ambiguous, the thinking seat asks one clarifying question rather
than guessing — cheaper than a misread.

## Pattern 2 — Decompose, then dispatch (the multitask shape)

The high-leverage workflow:

1. **One Opus chat** receives the messy input and decomposes it into bounded
   packets — each packet names files, validators, decision IDs, acceptance check.
2. **N Composer subagents** (Task tool, `run_in_background: true`) each take one
   packet and execute in parallel.
3. **The Opus chat** collects the results and renders the verdict / synthesis —
   the judgment layer the execution seats should not own.

Dispatch template (per subagent):

> "Execute packet K: edit `<paths>`; the change is `<precise spec>`; run
> `<validator>`; do NOT make judgment calls — if you hit an ambiguity or a
> validator FAIL, stop and report. Return: files changed + validator result."

The judgment ("is this the right change?") stays with the thinking seat; the
execution ("make exactly this change") goes to the subagents.

## Pattern 3 — Assign the seat in each workflow (Agent / Plan / Multitask)

The two-seat split is **operator-configurable in the UI + config**, not just an
advisory recommendation. (Verified 2026-05-29 against Cursor Plan Mode docs + the
3.2 `/multitask` changelog — this corrects an earlier draft that framed subagents
as the only lever.) Three workflows, three places to set the model:

### Agent mode — Custom Modes (save the setup once)

Cursor Custom Modes preselect a model + instructions. Save two:

- **Holistika Interpret** — Opus + "focus on judgment, scope, doctrine; decompose
  before delegating; surface decisions as inline-ratify gates." Pair with the
  research-action craft.
- **Holistika Execute** — Composer + "make precise, settled changes; run
  validators; stop and report on any ambiguity or FAIL." Pair with this rule.

Switch with the mode picker (or a keyboard shortcut) — a one-click seat change.

### Plan mode (`Shift+Tab`) — pick the planning model, then choose how to build

The **planning model** is the model selector in the chat input — set it to Opus
(or Codex) so judgment drives the plan. When the plan is ready you get two build
buttons:

- **Build Locally** — the foreground Agent (your picked execution model) runs it.
- **Build in parallel** — kicks off `/multitask` (the execution fleet).

The read-only *exploration* subagents Plan mode spawns to scout context have their
own model at **Settings → Subagents → Explore subagent model** (default is a cheap
model; leave it cheap). So the native pattern is literally: **Opus plans → build
on Composer.** No vibes required.

### `/multitask` — pin per-subagent models in `.cursor/agents/`

`/multitask` (Agents Window, Cursor 3.2+) runs an async fleet in worktrees. By
default subagents **inherit** the parent model; to pin a seat per role, create one
file per agent:

```
---
name: executor
description: Mechanical multi-file edits + validators against a settled packet.
model: composer-2.5          # inherit | fast | a slug that matches your picker
readonly: false
---
<instructions: make exactly the specified change; stop + report on collision/FAIL>
```

- `model:` accepts `inherit`, `fast`, or an exact picker slug (e.g.
  `claude-4.6-opus-high-thinking`, `composer-2.5`, `gpt-5.3-codex-xhigh`).
- **Caveat — verify it took:** in early `/multitask` the `model:` field was
  sometimes ignored and fell back to inherit (fix rolling in ~3.3). Check the
  request's model before trusting a per-seat pin on irreversible work.
- A read-only `planner` / `reviewer` agent (`readonly: true`) on a thinking model
  is the safe first one to add — it can't write, so it can't break anything.

## Pattern 4 — Statusline (know which seat you're in)

Configure the Cursor statusline via the **Cursor-bundled statusline skill** at
`~/.cursor/skills-cursor/statusline/SKILL.md` (a built-in skill, **not** a repo
skill) to show the active model + context-window %. Free, no tokens, persistent
visual cue. Keep the config on the operator's machine; never commit
machine-specific config or secrets.

## Pattern 5 — Misread recovery (the two-strike rule)

If an execution seat misreads intent twice in a row:

1. Stop dispatching to it for this task class.
2. Escalate the session to the thinking seat.
3. Treat it as a knowledge-test signal (per the People agentic doctrine): the
   misread means doctrine absorption degraded for this task class; the thinking
   seat re-establishes the packet spec, then may re-dispatch.

Two misreads is the trigger, not one — a single misread is noise; a pattern is
signal.

## Pattern 6 — Make governance gates legible at build time

A plan that contains an approval gate must make that gate the **explicit first
todo**, clearly labelled (e.g. "⛔ OPERATOR APPROVAL — canonical-CSV gate"), so
that pushing the build button never surprises the operator with an approval they
did not know they owed. A buried gate produces exactly the friction the operator
named on 2026-05-29 — *"I thought the plan was completely drafted and I wanted to
push the build button … maybe it's me that didn't see I had to approve
something."* That confusion is a workflow defect, not an operator error.

Two clean ways to clear a gate before building:

1. **Pre-clear in chat** — the operator says "go, <option>"; the thinking seat
   records the clearance in the durable ratification doc; the operator then
   pushes build with the execution model.
2. **Front-load it as todo #1** — the plan's first todo *is* the approval, so the
   build pauses there visibly rather than mid-stream.

The fix is never "add more gates." It is making the *one* real gate legible up
front, then handing the mechanical build to the execution seat with a
verify-first instruction. And remember: a fully drafted plan plus one cleared
gate **is** ready to build on the execution model — the gate is a checkpoint, not
a reason to keep the work on the thinking seat.

## Worked example — the 2026-05-29 regression (why the seats matter)

A Composer-authored rollout plan was structurally excellent but proposed to
"mint" a per-task registry, data model, and validator that **already existed**
(it trusted a stale roadmap's file list without checking repo reality). An Opus
pass caught the collision, reframed the phase, and fixed the upstream drift.

The lesson is exactly the seat split: the execution model nailed everything
answerable from the context it was handed, and missed the one thing requiring
independent verification of ground truth. Keep context-verification on the
thinking seat for canonical-CSV work. Recorded as a field-test data point in
[`field-test-note.md`](../../../docs/wip/intelligence/model-selection-2026-05-28/field-test-note.md).

## Anti-patterns

- **Dispatching un-decomposed intent.** Handing a messy brief straight to an
  execution subagent → it pattern-matches. Decompose first (Pattern 2).
- **Letting the execution seat make judgment calls.** Scope, doctrine, and
  irreversible decisions are the thinking seat's job.
- **Claiming auto-switching.** Cursor can't switch the foreground model; this is
  advisory + Custom Modes only.
- **Over-routing trivial work to Opus.** A one-line CSV fix does not need the
  thinking seat — that wastes budget. Reserve Opus for genuine judgment.
- **Single-misread overreaction.** Escalate on a *pattern* (two strikes), not on
  one slip.

## Cross-references

- Paired rule (the *when*): [`akos-aic-delegation.mdc`](../../rules/akos-aic-delegation.mdc).
- Routing lookup: [`model-routing-map.md`](../../../docs/wip/intelligence/model-selection-2026-05-28/model-routing-map.md) Layer 0.
- Inline-ratify craft (for the decompose → surface-decisions step): [`inline-ratify-craft`](../inline-ratify-craft/SKILL.md).
- Taxonomy + AKOS identity: [`master-synthesis.md`](../../../docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/master-synthesis.md).
