---
name: agent-checkpoint-craft
description: Use when planning, executing, or auditing a long-running multi-phase initiative (≥ 5 phases, ≥ 1 calendar week, or any initiative with explicit operator pause points or agent self-checkpoints). Codifies the craft for authoring pause-record artifacts + self-checkpoint reports + the 7-item operator approval checklist + pause-fatigue mitigation. Triggers on operator pause point, agent self-checkpoint, pause record, pre-phase self-checkpoint, mid-phase self-checkpoint, post-phase self-checkpoint, operator approval checklist, soft-pause auto-clear, pause-point fatigue. Pairs with .cursor/rules/akos-agent-checkpoint-discipline.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT; D-IH-66-Q
authored: 2026-05-24
---

# Agent-Checkpoint Craft

> Codified at I86 Wave R close (drain7) to operationalise the D-IH-66-Q discipline (I66 P2 ratification). The craft turns long-running initiative governance from "agent drifts for 5.5 weeks without operator visibility" into structured checkpoint rhythm. Ratified by D-IH-86-CT alongside the parent rule.

## When to use this skill

Read this skill before:

- Designing a phase plan that crosses ≥ 5 phases or ≥ 1 calendar week.
- Reaching a phase boundary that warrants a pause-point file.
- Starting a phase that will produce multiple substantive deliverables (3+ canonicals, ≥ 1 day of work, multi-file refactor).
- Authoring the operator-facing 7-item approval checklist at phase close.
- Triaging pause-point fatigue signals.

This skill assumes you have already read [`akos-agent-checkpoint-discipline.mdc`](../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc).

## Core principles

### Principle 1 — Operator pause points control direction; agent self-checkpoints control reasoning quality

The two are complementary, not interchangeable:

- **Operator pause point** = formal hand-off; blocks next phase until operator signs off; file at `reports/p<N>-pause-record-<YYYY-MM-DD>.md`.
- **Agent self-checkpoint** = informal pre-flight; doesn't block; file at `reports/checkpoints/sc-<purpose>-<YYYY-MM-DD>.md`.

Skipping either weakens the rhythm. Pause-points without self-checkpoints = operator gets a deliverable they can't audit (no reasoning trail). Self-checkpoints without pause-points = agent thinks well but drifts away from operator-approved direction.

### Principle 2 — Pause-record shape (binding template)

Every pause-record at `reports/p<N>-pause-record-<YYYY-MM-DD>.md` carries:

1. **Mechanical evidence** — files created / modified / deleted with paths + line counts; validators run with verdicts; tests added.
2. **Documentary evidence** — decisions encoded; cross-canon link integrity; CHANGELOG entry.
3. **Pre-next-phase self-checkpoint** — what's outstanding; what's not blocking; first actions for next phase.
4. **Operator approval checklist** — numbered confirmations the operator must validate before next-phase entry (≤ 7 items per parent rule).

Skipping any of these 4 = pause-record is invalid; operator review can't proceed.

### Principle 3 — Self-checkpoint shape (binding template)

Every self-checkpoint at `reports/checkpoints/sc-<purpose>-<YYYY-MM-DD>.md` carries:

1. **What I have read** — file paths or topic descriptors; what I now know.
2. **What I have authored** — file paths + brief description; committed vs in-progress.
3. **What is outstanding** — numbered list of next actions in execution order.
4. **What I have decided not to do** — out-of-scope deferrals with reason ("DEFER to phase X" or "OUT OF SCOPE per D-IH-NN-X").
5. **First three concrete next actions** — specific files, specific changes.

The `<purpose>` follows the convention: `pre-p<N>` / `mid-p<N>-<topic>` / `post-p<N>-<topic>`.

### Principle 4 — 7-item operator approval checklist craft

The ≤ 7-item limit is binding. More items = operator skim-fatigue; fewer items = checklist insufficient.

Item structure: each item is a one-sentence confirmation the operator can answer yes/no without re-reading the body. Examples:

- "Confirm all canonical CSV row appends are reviewed and approved."
- "Confirm sibling-repo deploy is verified READY at vendor MCP."
- "Confirm validator suite OVERALL PASS at HEAD."

Avoid items that require operator to re-derive evidence; the evidence is in §1 + §2.

### Principle 5 — Pause-fatigue mitigation

Risk: too many operator pause points → reviewer fatigue → rubber-stamp approval → governance erosion.

Mitigations (per parent rule):

- **Front-load** the substantive operator review at P0 (charter) and P1 (canon hardening). Once architecture is approved, downstream pauses are mostly "did you do what you said you would?" — much faster.
- **Make pause records skimmable.** Mechanical evidence FIRST (10 lines of file paths + verdicts). Documentary evidence SECOND. Approval checklist LAST.
- **Allow batched approvals.** If P3 + P4 are tightly coupled, operator can pre-authorise "P3 closes → P4 may auto-start" — but pause records for BOTH still get filed.
- **Distinguish soft vs hard pauses.** Soft pauses (intermediate canon hardening) can auto-clear after 24h of operator silence + clean validators. Hard pauses (canonical CSV gate, trademark filings, public-prose publish) are non-skippable.

## Pause-point depth heuristic

| Trigger | Recommended pause-point density |
|:---|:---|
| Single-phase / single-day work | 0 |
| 2-3 phases / ≤ 3 days | 1 (at closure) |
| 4-6 phases / 1-2 weeks | 2-3 (phase boundaries) |
| 7+ phases / ≥ 3 weeks | 1 per 2-3 phases (≥ 4 total) |
| ≥ 5 weeks (e.g. I66) | 1 per phase (≥ 8 total) |
| Touching canonical CSV | **mandatory** pause point at canonical-CSV gate |
| Trademark filings / legal templates | **mandatory** pause point at handoff |
| Public-facing prose rewrite | **mandatory** pause point before publish |

## Self-checkpoint depth heuristic

| Phase scope | Recommended self-checkpoints |
|:---|:---|
| 1-2 deliverables | 1 (pre-phase) |
| 3-5 deliverables | 2 (pre + mid) |
| 6+ deliverables / mixed-asset-class phase | 3 (pre + mid × 2 + post) |

## Pre-flight checklist

1. Initiative trigger conditions met (≥ 5 phases OR ≥ 1 week OR explicit pause-points).
2. Pause-point density chosen per heuristic.
3. Self-checkpoint density chosen per heuristic.
4. Pause-record template followed exactly (4 sections + 7-item checklist max).
5. Self-checkpoint template followed exactly (5 sections).
6. Pause-record skimmable (mechanical evidence first).
7. Approval checklist items are yes/no answerable without re-derivation.
8. Soft vs hard pause classified explicitly.

## Anti-patterns

- **AP1 — Skip the pause-record at phase close.** Operator can't audit; downstream agents lose context.
- **AP2 — Self-checkpoint with no "what I decided not to do" section.** Out-of-scope items go unexamined; rework risk.
- **AP3 — > 7 items in approval checklist.** Operator fatigue; rubber-stamp risk.
- **AP4 — Pause-record buried under prose.** Mechanical evidence not first; operator skims.
- **AP5 — Soft-pause auto-cleared on hard-pause topic.** Canonical-CSV gate silently bypassed.

## Cross-references

- Parent rule: [`akos-agent-checkpoint-discipline.mdc`](../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc).
- Sister rule: [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) (initiative discipline + plan-quality bar).
- Sister skill: [`planning-traceability-craft`](../planning-traceability-craft/SKILL.md) (the per-phase deep section + closure UAT bar).
- Worked example: I66 master-roadmap §"Pause and checkpoint discipline".
- Ratifying decisions: D-IH-86-CT (this skill mint), D-IH-66-Q (parent rule ratification).
