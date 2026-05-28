---
title: Model selection research action (2026-05-28)
language: en
intellectual_kind: wip_intelligence_index
sharing_label: internal_only
audience: J-OP
authored: 2026-05-28
last_review: 2026-05-28
status: draft
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
---

# Model selection — research action folder

> A governed research action answering: which AI model should drive
> Holistika's Cursor work, and how do we switch to a cheaper one with
> confidence? Built with the research-to-decision discipline (the rulebook
> that makes sure research gets logged with sources + trust scores before
> it drives a decision).

## What's here

| File | What it is |
|:---|:---|
| `source-ledger.csv` | The log of every source used, with where it came from + how much we trust it + how credible others would find it. 10 public-web sources, all routine/low-risk. |
| `recommendation-note.md` | The one-page answer: route by session — cheap model (Composer 2.5) for execution, expensive model (Opus) for interpretation; keep the OpenAI model (Codex) off the interpretation lane. |
| `field-test-note.md` | The practical switch-with-a-safety-net guide, including the deliberate test: have the cheap model try to expand this note into the full open-source + video/image/3D map, then judge it on three checks. |

## Why this is minimal on purpose

Scope was set to "Cursor models only, now" for budget reasons. The full
map (open-source models + multi-format: video / image / 3D) is deferred
and **doubles as the field test** of whether the cheap model can do
Holistika's interpretive research work. Expanding this folder is the test
task, not separate busywork.

## Status

This is Tier-1 working intelligence (a draft research output), not a
frozen canonical. When the field test reports back, the result gets
recorded in the source log's iteration stage so the model-selection
decision becomes durable instead of living in one chat.
