---
name: Index Integrity Craft
description: >-
  Use when running, dispositioning findings from, or wiring up the
  baseline-index integrity sweep in this AKOS workspace. Codifies the
  craft for keeping baseline indexes (planning README, PRECEDENCE,
  CHANGELOG, INITIATIVE_DEPENDENCIES, USER_GUIDE, ARCHITECTURE,
  dashboards, Quality Fabric specialty list) in sync with their source-
  of-truth (filesystem + canonical CSVs). Triggers on any phrase like
  index integrity, baseline index sweep, PRECEDENCE drift, planning
  README drift, CHANGELOG behind wave, INITIATIVE_DEPENDENCIES stale,
  IDX-NN finding, baseline_index_sweep.py, validate_index_freshness.py,
  or after a wave-close UAT or canonical-CSV mint commit. Pairs with
  .cursor/rules/akos-index-integrity.mdc (the WHEN); this skill is the
  HOW.
---

# Index Integrity Craft

## Why this skill exists

The cursor rule `akos-index-integrity.mdc` and the canonical
`INDEX_INTEGRITY_DISCIPLINE.md` tell you **when** to run the sweep and
**what** the 8 dimensions are. This skill tells you **how** to run them
well, how to disposition findings without producing brand-drift or
governance-debt, and how to wire the discipline into a new specialty
mint without copy-pasting mistakes.

Read this skill before running `scripts/baseline_index_sweep.py` for the
first time in a session, OR before authoring a follow-up specialty mint
that should inherit the INDEX_INTEGRITY mint pattern (Wave N P3
worked-example).

## Principle 1 — Run the sweep BEFORE the UAT verdict line

The sweep is mechanical evidence for the wave-close UAT. If you fill in
the UAT verdict line before running the sweep, you have to amend the UAT
when the sweep surfaces drift. Always:

1. Bring the wave's last commit into a clean state (no `git status`
   noise — uncommitted edits will skew probes).
2. Run `py scripts/baseline_index_sweep.py --sweep-trigger wave_close
   --output docs/wip/planning/<NN-coordinator>/reports/index-sweep-<date>-wave-<X>-close.md`.
3. Read the report top-to-bottom. Note each non-fresh finding.
4. THEN draft the UAT §3 mechanical-evidence row citing the sweep
   report.
5. THEN fill the UAT verdict line.

This is the same shape as the INTER_WAVE_REGRESSION sweep (Wave M
precedent). The two sweeps compose: a wave with a clean
INTER_WAVE_REGRESSION sweep but a drift-laden INDEX_INTEGRITY sweep is
NOT closure-ready.

## Principle 2 — Disposition findings via inline-ratify, batched

When the sweep surfaces ≥ 1 non-fresh finding, you do NOT silently
auto-fix and move on. You disposition via the 5-option enum from the
canonical §6, surfaced as `AskQuestion` per `akos-inline-ratification.mdc`.

Bad (auto-fix without ratification):

```
# Sweep says PRECEDENCE missing 5 CSV rows.
# Agent appends them silently.
# Operator never sees the drift.
```

Good (inline-ratify):

```
AskQuestion: 5 IDX-02 gaps — for each missing CSV, recommended:
  deterministic-fix-now via manual append (judgement-call: each CSV
  needs canonical-class + mirror-class declaration). Alternatives:
  defer-OPS / accept-as-canon / escalate.
```

When findings exceed 10, **split into 2 AskQuestion batches**, grouped by
dimension. Sample batching:

- Batch 1: IDX-01..IDX-04 (governance-doc drift; usually mechanical fix).
- Batch 2: IDX-05..IDX-08 (registry-coverage drift; often judgement-call).

Time-box recovery (24h+ operator silence + clean validators + reversible
dispositions auto-default to recommended) applies only to reversible
findings. Per `akos-inline-ratification.mdc` §"Time-box recovery":
irreversible findings (e.g., PRECEDENCE row that names canonical-class
incorrectly) NEVER auto-default.

## Principle 3 — Deterministic-fix paths vs judgement-call paths

The runbook supports 4 deterministic-fix paths (IDX-01 / IDX-02 / IDX-07
/ IDX-08) and 4 judgement-call paths (IDX-03 / IDX-04 / IDX-05 / IDX-06).

**Deterministic-fix** = the runbook can compute the correct state from
the source-of-truth (filesystem + CSV row counts) and write it
mechanically. Safe to auto-apply IF operator ratifies the path choice.

**Judgement-call** = the runbook can detect the drift but cannot
auto-compose the correct prose (CHANGELOG bullet; dependency narrative;
USER_GUIDE sentence; ARCHITECTURE registry row). These require an agent
or operator to author the prose. Do NOT pretend the runbook can
auto-write these; the result will be brand-drift slop.

When in doubt about which path to use: default to manual-fix-now.
Reversible. Always recoverable. Mechanical-fix-now is the optimisation
when the path is unambiguous; manual is the safe default.

## Principle 4 — Cite the sweep report from the UAT mechanical-evidence row

The UAT report's §3 mechanical-evidence section MUST cite the sweep
report path. Bad:

```
- Index sweep: clean.
```

Good:

```
- Index sweep: see [`reports/index-sweep-2026-05-21-wave-n-close.md`](reports/index-sweep-2026-05-21-wave-n-close.md)
  — 8 findings (6 fresh, 2 drift), all 2 drifts dispositioned via
  deterministic-fix-now at D-IH-86-CD.X / D-IH-86-CD.Y.
```

The citation makes the audit trail traceable. Every closure UAT amender
3 months from now needs to find the sweep without grepping git.

## Principle 5 — Specialty mint contract (the 15-surface quartet)

When minting a NEW Quality Fabric specialty (this skill's mint at Wave
N P3 is the third worked example after UAT_DISCIPLINE at Wave J P1 and
INTER_WAVE_REGRESSION at Wave M P1), inherit the 15-surface quartet from
`akos-index-integrity.mdc` RULE 5. Land all 15 in the same commit (or
the next material commit). Common mistakes:

- **Skipping the skill.** The rule + canonical alone leave future agents
  without the *how* layer; the skill is what they read when they're
  about to run the sweep for the first time.
- **Skipping the SOP+runbook pair.** Per `akos-executable-process-catalog.mdc`
  Rule 1, every process_list row needs an AC-HUMAN SOP + AC-AUTOMATION
  runbook. The runbook ships in this quartet; the SOP must too.
- **Skipping the PEOPLE_DESIGN_PATTERN_REGISTRY.csv row.** Per
  `akos-people-discipline-of-disciplines.mdc` Rule 1, every specialty is
  a People-area pattern that other areas inherit from. The registry row
  is the load-bearing reference for cross-area adoption.
- **Skipping the CHANGELOG entry.** The validator IDX-03 will catch this
  on the next sweep; better to catch yourself first.
- **Skipping the HOLISTIKA_QUALITY_FABRIC.md §6 row.** The validator
  IDX-08 will catch this on the next sweep; same self-discipline
  argument.

## Principle 6 — Pre-flight checklist (run before every sweep)

Before running `py scripts/baseline_index_sweep.py`:

- [ ] Working tree clean OR uncommitted changes intentional (probes
      read filesystem state).
- [ ] Most recent commit's wave letter is what you expect (`git log
      -1`).
- [ ] If sweep_trigger=canonical_csv_mint: the new CSV row landed in
      the previous commit (not this one).
- [ ] Output path matches the parent initiative's reports/ folder.

After running:

- [ ] Read every non-fresh finding before dispositioning.
- [ ] Disposition via AskQuestion (not silent auto-fix).
- [ ] Cite the sweep report from the UAT §3 row.
- [ ] If new wave's findings include "INFO" promotion to FAIL: ratify
      via operator-explicit decision row (not agent-default).

## Anti-patterns

- **"Sweep is clean today, skip tomorrow."** Cadence is per-wave +
  per-canonical-CSV-mint; not per-discretion. A "clean today, drift
  tomorrow" sweep is exactly what the cadence catches.
- **"I'll fix the drift after closing the wave."** Sweep MUST gate the
  UAT verdict. If you close first and fix later, the UAT is misleading
  (says clean when it isn't).
- **"The drift is small; I'll just edit the index doc directly."**
  Direct edits without disposition skip the audit trail. Even
  deterministic-fix needs an AskQuestion ratify so the decision is
  recorded.
- **"INFO mode means I can ignore findings."** INFO ramp is for the
  Wave N backfill window. After Wave N close + FAIL promotion, INFO is
  no longer an excuse.

## Cross-references

- Rule: [`.cursor/rules/akos-index-integrity.mdc`](../../rules/akos-index-integrity.mdc)
  (the *when* layer).
- Canonical: `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md`
  (the doctrine).
- Sister skill: [`.cursor/skills/inline-ratify-craft/SKILL.md`](../inline-ratify-craft/SKILL.md)
  (Principle 1 evidence sweep + Principle 5 batching apply directly to
  this discipline's findings disposition).
- Wave M precedent: `INTER_WAVE_REGRESSION_DISCIPLINE.md` + paired
  runbook `scripts/inter_wave_regression_sweep.py` (the sister
  discipline minted at Wave M P1; same quartet shape).
- Wave J precedent: `UAT_DISCIPLINE.md` (the 5th specialty minted; first
  worked example of the quartet shape).
