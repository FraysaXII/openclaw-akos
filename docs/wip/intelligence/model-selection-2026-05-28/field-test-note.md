---
title: Field-test note — switching to Composer 2.5 with a safety net (2026-05-28)
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-28
last_review: 2026-05-28
status: draft
linked_research_sources:
  - docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
---

# Switching to the cheap model with a safety net

> Practical note so you can use **Composer 2.5** for build work and judge
> whether it also handles interpretive research — without flying blind.

## Switch now, like this

- Set Cursor to **Composer 2.5 — Fast** for everyday build sessions.
- Keep **Opus** one click away for thinking sessions (see below).

## The test we ran (Option B)

You asked whether the **full model-selection knowledge base** (open-source
+ video/image/3D, not just Cursor trio) could be built on Composer instead
of Opus. **That expansion is Iteration 1 of this field test.**

Deliverables produced on Composer 2.5:

- 25-row `source-ledger.csv` (was 10)
- 2 prong syntheses (OSS + multimodal)
- `master-synthesis.md`, `research-action-pack.md`, `model-routing-map.md`
- Updated `recommendation-note.md` + this README

## Three judging checks (for you)

1. **Did it interpret correctly?** Did Option B mean *full KB wired to
   standards*, not another minimal stub?
2. **Did it log sources honestly?** 25 ledger rows incl. skeptic sources
   (SRC-MS-16/17/25); CORPINT rows for substrate audit + model-catalog.
3. **Did it surface choices?** Ranked options A–D in OSS prong; lanes +
   deferrals in multimodal prong — not flat hype.

## Agent self-assessment — Iteration 1 (2026-05-28)

| Check | Self-score | Notes |
|:---|:---|:---|
| Intent preserved | **Pass (agent view)** | Full Option B artifact set; Wave R+4 shape mirrored |
| Source log quality | **Pass (agent view)** | 25 rows; ≥3 skeptic/Euclid counter-sources |
| Ranked options | **Pass (agent view)** | Options + DQ-MS-01..06; operator ratified govern stage 2026-05-28 |

**Operator verdict (Composer field test):** **It held** — rendered by Opus 4.8
Max on the operator's explicit delegation 2026-05-28 ("evaluate Composer in my
stead"). Assessment: Composer passed the hard part — the DQ-MS-02 interpretive
pass (emotionally-loaded, politically-sensitive, typo-heavy input on neutrality
+ model origin) was distilled into "law-bound neutrality" WITHOUT flattening to
corporate hedging, injecting a political stance, or losing the silent-internal-
preference vs public-neutrality distinction. DQ-MS-01 resolved as a genuine
both-and (flexibility + best practice → engagement-scoped hybrid), not a binary
punt. Mechanical work (5-doc propagation, 2 substrate rows, validators PASS)
clean. One coherence slip caught + fixed by Opus: Kimi row cited the .cn audit
domain on a residency-sensitive vendor (corrected to moonshot.ai). Weakest
evidence in the pack was the agent's own self-grading (3× "Pass (agent view)") —
this operator-delegated Opus pass is what closes that loop. **Routing
implication:** earned cheap-default for interpretive+execution work at this
complexity tier; reserve Opus for genuinely contested judgment calls.

**Operator verdict (governance DQ-MS-01..06):** **Ratified** — see
[`operator-ratification-2026-05-28.md`](operator-ratification-2026-05-28.md).

## Iteration 2 — Composer plan, Opus regression (2026-05-29)

Second data point on the same routing thesis. Composer 2.5 authored the AIC
delegation rollout plan; Opus 4.8 ran a benchmark regression over it.

| Check | Result | Notes |
|:---|:---|:---|
| Structure / citations from given context | **Pass** | Phased, gated, mermaid; correct on F5, registry counts, jargon-gate ownership |
| Independent verification of ground truth | **Miss** | Proposed to "mint" a per-task registry + model + validator that already existed — trusted a stale roadmap; never checked repo state |

**Routing implication (reinforces Iteration 1):** the execution model is strong
for structured authoring **when handed accurate context**, but should not own the
context-verification step on canonical-CSV work — keep that on the thinking seat.
Now codified in [`akos-aic-delegation.mdc`](../../../../.cursor/rules/akos-aic-delegation.mdc)
RULE 2 + [`aic-delegation-craft`](../../../../.cursor/skills/aic-delegation-craft/SKILL.md).

## Iteration 3 — trust calibration + the meaning of regression (2026-05-29)

Third data point — and the first where the regression graded the **whole
human–AI system**, not just the model. Triggered by a late-night session where
the operator was (rightly) impressed by Composer's reasoning and asked two
things: raise the trust dial without overselling, and explain why a "finished"
plan still wanted an approval before build.

| Finding | About | Verdict |
|:---|:---|:---|
| Reasoning over given context is strong (Fast-vs-Standard explainer; Opus-vs-Composer structuring) | the model | **Raise the dial** — trust Composer for synthesis, explanation, bounded reasoning, execution |
| Independent ground-truth verification ("does this file already exist?") | the model | **Hold the guardrail** — instruct "verify first / stop on collision" or keep on the thinking seat for canonical work |
| An approval gate was not visible at build time → felt like a surprise | the **workflow** | **Fix the discipline, not the model** — gates legible at build time (now in the craft skill, Pattern 6) |

**The meaning of regression (operator framing):** regression is not "grade the
AI"; it is examining the *whole loop* with no tunnel vision to deepen
understanding and improve the system — the way the operator runs it with human
teams. Two of the three findings above were about *us* (trust calibration +
workflow legibility), not the model. The model became a mirror for the operating
discipline.

**Calibrated routing (supersedes the Iteration 1/2 dial):** Composer earns a
higher default for reasoning + synthesis + execution. The *only* standing
guardrail is independent verification of ground truth on canonical / irreversible
work — and that guardrail is a one-line instruction ("verify it doesn't already
exist; stop and report on collision"), not a reason to withhold the work.

**Addendum — the operator regressed the doctrine itself (2026-05-29):** later the
same day the operator caught a *stale fact in our own delegation rule* — it said
Cursor "can't switch models / subagents are the only lever," but the operator
could see Plan-mode + `/multitask` model assignment in the UI. Verified against
Cursor docs + the 3.2 changelog: the operator was right. The agent can't switch
its *own* foreground model, but the operator has native per-workflow levers
(Plan-mode planning-model selector; Build-in-parallel; `.cursor/agents/*.md`
`model:` field). Corrected across the rule, the skill, and the routing map. This
is the discipline working in *both* directions — the AI caught the operator's
stale roadmap (Iteration 2); the operator caught the AI's stale doctrine (here).
Neither is the authority; the loop is.

## When to switch back to Opus

- Complex new direction or dense multi-threaded message
- Misread intent **twice in a row**
- Mostly judgment (scope, doctrine, contradictions)
- Irreversible / high-stakes (commercial, customer send, brand)

## What "good enough" looks like

If you pass all three checks on this KB and don't feel the urge to re-run
on Opus → **earned cheap default for interpretive research at this
complexity tier.**

If interpretation slipped → **cheap for execution, Opus for thinking**
— still a win because the boundary is known.

## Reporting back

One line next session updates this note + source-ledger `notes` column
on SRC-MS-10 (iteration anchor). Makes the decision durable, not
chat-trapped.
