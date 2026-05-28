---
title: Model selection recommendation — Cursor AI driver switch (2026-05-28)
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-28
last_review: 2026-05-28
status: draft
linked_research_sources:
  - docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
---

# Which AI model should drive Holistika's Cursor work?

> One-page recommendation for the operator. Scope: the three models you
> are weighing inside Cursor today — the expensive thinking model, the
> cheap Cursor-built coding model, and the OpenAI coding model. Open-
> source models and video/image/3D models are **deliberately deferred**
> to a later, larger version of this note (see "What is left out", below).
> Built using the research-to-decision discipline; the sources behind
> every claim are logged in `source-ledger.csv` in this folder.

## The three models in plain terms

| Model (and what you call it) | What it actually is | Its real strength | Cost vs the others |
|:---|:---|:---|:---|
| **Opus 4.8 Max** (what you've been on) | Anthropic's top "thinking" model | Reading intent out of messy input, judgment, long-context synthesis | Most expensive |
| **Composer 2.5** (the cheap Cursor one) | Cursor's own coding-specialised agent, released 18 May 2026, built on an open base model | Mechanical execution: multi-file edits, running scripts, git, refactors | ~10x cheaper per task |
| **Codex / GPT-5.5** (the OpenAI one) | OpenAI's terminal-and-automation specialist | Shell/terminal automation, token efficiency | Similar to Opus |

## The core finding

Every benchmark that makes the cheap model (Composer 2.5) look as good as
the expensive one (Opus) **measures coding only** — multi-file edits,
running commands, fixing tests. None of them measure the thing you most
rely on: **correctly interpreting a dense, stream-of-consciousness
strategic brief.** So the benchmarks are reassuring for half your work and
silent on the other half.

Your work here is two jobs in one coat:

- **Execution** (mechanical-with-rules): CSV edits, writing checker
  scripts, running validators, git commits. → The cheap model is
  genuinely strong here, at ~one-tenth the cost.
- **Interpretation** (judgment-heavy): reading what you *mean*,
  synthesising doctrine, deciding scope. → The expensive model keeps a
  real edge, and it is exactly where the benchmarks go quiet.

## The recommendation: route by session, don't pick one model

This is the one thing every independent source agreed on. Translated to
your budget:

1. **Default to the cheap Cursor model (Composer 2.5, Fast variant)** for
   execution-heavy sessions — which is most of the build work.
2. **Switch up to the expensive thinking model (Opus) only for "thinking"
   sessions** — a complex new direction, a garbled multi-part strategic
   message, or any task where interpretation *is* the job. (This very
   message is a textbook example of a "stay on Opus" task.)

That buys you cheap-by-default **with** a confidence safety valve, instead
of an all-or-nothing bet.

## On the OpenAI model (Codex) feeling "artificial" to you

This is not just taste, and it is traceable. Codex/GPT-5.5 is explicitly
built and tuned to be a *fast autonomous terminal worker* optimised for
token efficiency — not an interpreter of human nuance. For an operator
whose work is interpretation-heavy, that optimisation runs against your
grain, so your "artificial / unusable" reaction is consistent with what
the model is designed for. **Functional conclusion: keep Codex off your
interpretation lane regardless of its benchmark scores.** It may earn a
place later for pure terminal/CI automation, but not for the thinking you
depend on.

## Confidence (honest)

- Cheap model handles your **execution** work: **medium-high** — both the
  benchmarks and the genuinely coding-shaped nature of the build work
  support it.
- Cheap model handles your **interpretation** work: **low-to-medium,
  untested** — no benchmark measures it and your input style is the
  hardest interpretation case there is.

The only way to turn that low confidence into earned confidence cheaply is
a controlled field test (see `field-test-note.md` in this folder).

## What is left out (deliberately deferred)

This note covers Cursor's three models only. The bigger map you asked for
— open-source models, and models for video / image / 3D / other formats —
is **deferred on purpose** and teed up as the first real test of whether
the cheap model can do interpretive research work (see the field-test
note). Expanding this note into that full map is the test task.

## Sources

All claims trace to `source-ledger.csv` in this folder: an independent
benchmark organisation (highest trust), one balanced-skeptic journalism
piece (which flagged that the scores are vendor-produced and the base
model is foreign-built), and several comparison/review writeups (medium
trust). The skeptic source is logged at equal weight on purpose so the
recommendation is not built only on favourable coverage.
