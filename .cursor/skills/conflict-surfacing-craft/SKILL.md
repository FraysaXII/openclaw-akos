---
name: conflict-surfacing-craft
description: Use when executing a multi-task push and discovering some-but-not-all named tasks meet activation criteria, OR when consolidation has phase-specific tradeoffs that would over-commit operator attention. Codifies the Option-5 default posture for surfacing conflicts as governance shapes (full charter vs scope-overlap-tracker vs blocker-tracker vs forward-charter). Triggers on multi-task push, Lane, Bundle, Wave, activation gate, conflict surfacing, scope-overlap-tracker, blocker-tracker, forward-charter, Option-5 default, promotion blocker. Pairs with .cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT; D-IH-86-O
authored: 2026-05-24
---

# Conflict-Surfacing Craft

> Codified at I86 Wave R close (drain7) from the operator's framing at D-IH-86-O ratification: *"i'd like you to be on guard for other tasks that have conflict or other topics in which option 5 is applicable, that will be the default way to go forward because it'll make you surface other questions"*. The craft turns conflicted multi-task pushes from "speculatively promote everything OR block everything" into "mint the right governance shape per task." Ratified by D-IH-86-CT alongside the parent rule.

## When to use this skill

Read this skill before:

- Authoring any push (Lane / Bundle / Wave) where ≥ 2 named tasks have different activation states.
- Minting a candidate file at `docs/wip/planning/_candidates/` when a sibling initiative is also in scope.
- Filing a tracker at `docs/wip/planning/_trackers/` or `_blockers/`.
- Choosing between speculative promotion (mint INITIATIVE_REGISTRY row now) vs deferral.

This skill assumes you have already read [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc), which defines the trigger conditions + the 4 artifact shapes + the YAML templates. This skill is the **craft layer** on top of that rule.

## Core principles

### Principle 1 — Never stub-promote

Speculative promotion (creating an `INITIATIVE_REGISTRY` row at `status: active` with a thin charter stub) is the most common failure mode. The `D-IH-86-F` / `D-IH-86-G` precedent (promotion → revert → tracker) made this durable doctrine. When activation criteria aren't met, the right shape is NEVER the charter — it's the blocker-tracker.

### Principle 2 — Never block the task

Refusing to ship anything because some-but-not-all tasks have activation gaps erases operator intent. If the operator named 5 tasks and 3 of them have clean gates while 2 don't, ship the 3 + mint trackers for the 2. The operator's bandwidth named the batch for a reason.

### Principle 3 — Per-task shape disposition (the decision tree)

Walk this tree for each named task:

```
For each task in the conflicted batch:
    if activation gates ALL MET:
        if active sibling scope overlap:
            mint FULL CHARTER + SCOPE-OVERLAP-TRACKER
        else if operator content density too high for current chat:
            FORWARD-CHARTER to next session/successor
        else:
            mint FULL CHARTER
    else (activation gates NOT met):
        if prior promotion reverted:
            mint BLOCKER-TRACKER with reverted-promotion lineage section
        else:
            mint BLOCKER-TRACKER
```

The 4 artifact shapes are mutually exclusive per task (a task gets exactly one shape).

### Principle 4 — Surface the conflict, don't absorb it

When you choose a shape, name the conflict explicitly in the artifact body. "Why this is a tracker and not a charter" is the load-bearing claim. Future readers must see the reasoning so they don't re-propose what was already considered + dispositioned.

### Principle 5 — Mint the YAML frontmatter exactly to template

Every blocker-tracker and scope-overlap-tracker uses the binding YAML template from the parent rule. Skipping fields, renaming fields, or merging fields produces drift. The validator (if minted at a future wave) will catch drift; until then, operator discipline catches it.

## Per-shape authoring craft

### Shape A — Full v3.1-doctrine charter

Used when activation gates ALL MET + no active sibling overlap (or sibling is decommissioned).

File: `docs/wip/planning/<NN-slug>/master-roadmap.md` per `akos-planning-traceability.mdc` §"Plan-quality bar".

Authoring sequence (the I76 P0 worked example):

1. Mint candidate file at `docs/wip/planning/_candidates/<slug>.md` first if not already there.
2. Append `INITIATIVE_REGISTRY.csv` row at `status: active` + `inception_decision_id: D-IH-NN-A`.
3. Author `master-roadmap.md` to the plan-quality bar (≥ 5 phases, multi-sentence YAML todos, 3 mermaid diagrams, per-phase deep section).
4. Mint paired `decision-log.md` + `risk-register.md` + `files-modified.csv` (initially empty header).
5. Cross-reference from `docs/wip/planning/README.md` + parent area's planning index.

### Shape B — Scope-overlap-tracker (charter + sibling-overlap surface)

Used when new charter overlaps active sibling initiatives + per-sibling consolidation has phase-specific tradeoffs.

File: `docs/wip/planning/_trackers/<short-slug>-scope-overlap-tracker.md` (alongside the full charter).

Per parent rule §"Scope-overlap-tracker file shape (binding template)" — the YAML frontmatter must carry:

- `parent_initiative: <new INIT ID>`
- `tracked_initiatives: [list of sibling INIT IDs]`
- `next_review_trigger: <phase entry e.g. "I76 P1 entry">`
- `status: active`

Body must include:

- §1 Why this tracker exists (narrative: why up-front consolidation over-commits).
- §2 Per-sibling scope-overlap inventory table.
- §3 Per-phase consolidation ratify gates forward-chartered (one per sibling).
- §4 Tracker status update cadence.
- §5 Cross-references.

The I76 P0 worked example tracks I11 + I13 + I17 against I76 across 6 phases.

### Shape C — Blocker-tracker (candidate exists, activation blocked)

Used when activation gates NOT met.

File: `docs/wip/planning/_blockers/<candidate-slug>-promotion-blocker-tracker.md`.

Per parent rule §"Blocker-tracker file shape (binding template)" — YAML carries:

- `parent_candidate: <candidate ID>`
- `candidate_file: docs/wip/planning/_candidates/<slug>.md`
- `next_review_trigger: <human-readable condition>`
- `status: active`

Body must include:

- §1 Why <candidate> is not promoted today (activation criteria table).
- §2 Already-cleared sub-decisions (if any).
- §3 Resolution conditions (numbered).
- §4 Next-review trigger.
- §5 Reverted-promotion lineage (only if applicable).
- §6 Cross-references.

### Shape D — Forward-charter

Used when operator content density exceeds current chat's ratify budget (operator-content-gate conflict).

Form: no new file; instead, append OPS-row(s) to `OPS_REGISTER.csv` with `next_review_trigger` scoped to next cycle.

The OPS row(s) carry the forward-charter intent without committing to a charter file shape (which would be premature without operator content).

## Pre-flight checklist (before minting any shape)

1. Identify ALL named tasks in the push (don't silently drop any).
2. Per task: check activation criteria from candidate file vs current state (citations in your sweep).
3. Per task: check for active sibling scope overlap (Grep INITIATIVE_REGISTRY.csv for related rows).
4. Per task: check for prior reverted promotion (Grep decision-log.md files for `D-IH-NN-X` revert language).
5. Per task: walk Principle 3 decision tree → name the shape.
6. Confirm operator can tolerate the ratify density for full charters in this chat (otherwise forward-charter).
7. Mint each shape per its binding template (no field skipping; no field renaming).
8. Cross-reference all minted shapes in the umbrella push's commit message.
9. Append `DECISION_REGISTER.csv` row recording the disposition (one row per task or one umbrella row).
10. Update operator-scratchpad with per-task disposition + governing decision ID.

## Anti-patterns (forbidden by parent rule §"Anti-patterns")

- **AP1 — Stub-promote-and-defer.** Mint INITIATIVE_REGISTRY rows at active with thin stubs. Failure mode: speculative-promotion debt + downstream agents treat stubs as canonical.
- **AP2 — Block-the-task.** Refuse to ship anything. Failure mode: erases operator intent.
- **AP3 — Stub-charters-with-deferred-OPS.** Mint thin master-roadmaps + put deferral notes in OPS. Failure mode: same as AP1 with extra steps.
- **AP4 — Single-up-front-consolidation.** Force operator to ratify "supersede / extend / parallel" at parent-charter time. Failure mode: over-commits operator attention to phase-specific tradeoffs.

## Worked example — I76 P0 (2026-05-18)

The I76 P0 charter applied all 4 shapes simultaneously in commit `534ce3f`:

- **Shape A (Full charter)** for I76 (activation gates met: D-IH-84-C AICs F5 pre-ratification + I84 closed).
- **Shape B (Scope-overlap-tracker)** for I11 + I13 + I17 (active siblings; consolidation phase-specific tradeoffs).
- **Shape C (Blocker-trackers)** for I74 + I75 + I83 (activation gates not met; reverted-promotion lineage for I74 + I75 from D-IH-86-F/G).
- **Shape D (Forward-charter via OPS-76-1)** for I76 P1..P6 execution (operator-ratify density too high for current chat).

All 4 shapes landed in the same commit. Operator visibility preserved across all 7 candidates. Speculative-promotion debt avoided. Consolidation decisions deferred to phases where they're sharpest.

## Cross-references

- Parent rule: [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc).
- Sister rule (sibling discipline): [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) (governs *when* and *how* to inline-ratify; this skill governs *what to do when ratification surfaces structural conflict*).
- Worked example: [`docs/wip/planning/76-madeira-elevation/master-roadmap.md`](../../../docs/wip/planning/76-madeira-elevation/master-roadmap.md) + [`docs/wip/planning/_trackers/i11-i13-i17-scope-overlap-tracker.md`](../../../docs/wip/planning/_trackers/i11-i13-i17-scope-overlap-tracker.md) + the 3 `_blockers/i7N-...` blocker-trackers.
- Cross-cutting craft: [`akos-planning-traceability.mdc` §"Plan-quality bar"](../../../.cursor/rules/akos-planning-traceability.mdc) — full-charter shape inherits from this bar.
- Ratifying decisions: D-IH-86-CT (this skill mint), D-IH-86-O (operator-ratification of default posture), D-IH-86-F + D-IH-86-G (reverted-promotion precedent).
