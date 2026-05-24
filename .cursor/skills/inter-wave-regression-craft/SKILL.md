---
name: inter-wave-regression-craft
description: Use when running, dispositioning findings from, or wiring up the inter-wave regression sweep in this AKOS workspace. Codifies the craft for keeping the 13-dimension sweep healthy + the 5-option disposition enum + heuristic-evolution patterns. Wave R DIM-02 false-positive recovery is the worked example. Triggers on inter-wave regression, regression sweep, validate_inter_wave_regression.py, inter_wave_regression_sweep.py, DIM-NN finding, wave-close cadence, RegressionFindingRow, inter-wave drift. Pairs with .cursor/rules/akos-inter-wave-regression.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT; D-IH-86-BK; D-IH-86-BN
authored: 2026-05-24
---

# Inter-Wave Regression Craft

> Codified at I86 Wave R close (drain7) from the operator's framing: regression sweeps need to be **dispositioned thoughtfully**, not mechanically. The craft turns the 13-dimension sweep from a noise generator into a structural-integrity check. Ratified by D-IH-86-CT alongside the parent rule `akos-inter-wave-regression.mdc` (D-IH-86-BK).

## When to use this skill

Read this skill before:

- Running `py scripts/inter_wave_regression_sweep.py --wave-closing <wave-letter>` at any in-scope wave close.
- Dispositioning any WARN or FAIL finding from a regression sweep via inline-ratify.
- Patching the sweep heuristic itself (any of the 13 `_probe_dimension_N_*` functions in `scripts/inter_wave_regression_sweep.py`).
- Authoring a UAT closure report's §3.3 (regression-class mechanical evidence).

This skill assumes you have already read [`akos-inter-wave-regression.mdc`](../../../.cursor/rules/akos-inter-wave-regression.mdc), which defines what the sweep is + when it fires. This skill is the **craft layer** on top of that rule.

## Core principles

### Principle 1 — Run the self-test before the full sweep

`py scripts/inter_wave_regression_sweep.py --self-test` exercises all 13 probe functions against a tiny synthetic fixture set and verifies they return well-formed `RegressionFindingRow` Pydantic models. If the self-test fails, the sweep itself is broken — fix the runbook before running the real sweep. The full sweep against the entire workspace takes 30-90 seconds; debugging a broken runbook by running the full sweep wastes that time per iteration.

### Principle 2 — Inventory expected findings count BEFORE drafting the disposition gate

Before invoking the `AskQuestion` batch to disposition findings, compute the findings count from the JSON sidecar:

```python
import json
findings = json.load(open("artifacts/regression-sweep-<date>-wave-<letter>.json"))["findings"]
print(f"PASS={sum(1 for f in findings if f['verdict']=='PASS')}; WARN={sum(1 for f in findings if f['verdict']=='WARN')}; FAIL={sum(1 for f in findings if f['verdict']=='FAIL')}")
```

Findings count drives the disposition strategy:

- **≤ 10 findings**: fits in one `AskQuestion` batch (up to 10 questions).
- **11-20 findings**: splits into 2 batches (group by dimension; cite cross-references inline).
- **> 20 findings**: triggers the bandwidth-recovery pattern — halt + propose splitting the wave into Wave-N + Wave-N.5 (the dispositioning load is too high to land in one wave-close commit).

### Principle 3 — Distinguish true gaps from heuristic false-positives BEFORE filing the disposition

The 13 probes carry heuristics that can produce **false positives** (the probe flags a gap that isn't actually a gap because the heuristic doesn't see the evidence the canonical commits to). The Wave R precedent is concrete: `_probe_dimension_2_forward_charter_carryover` flagged 10 `forward_charters:` entries as gaps because its token-extraction logic missed evidence in `forward_charters_pending` and `linked_canonicals` frontmatter. Spot the false positives by:

- **Re-running with `--verbose`** to see the per-finding evidence trail.
- **Spot-checking 3-5 findings against the actual canonical body** — does the canonical genuinely lack the forward-charter resolution, or does the heuristic miss the resolution?
- **If false-positive rate > 20 %** of findings, halt and patch the heuristic before filing dispositions. Filing dispositions on noise wastes operator cycles.

The Wave R recovery shrunk DIM-02 false-positives from 10 to 4 by:

1. Expanding evidence sources from "decision-log files only" to "filesystem walk + canonical body content + frontmatter sub-keys."
2. Normalising token comparison to alphanumeric-only (`_alnum`) so `forward_charters: I-NN-...` matches `linked_canonicals: I_NN_...`.
3. Adding stop-prefix filter (`OPS-`, `D-IH-`, `R-IH-`) so non-initiative IDs don't get treated as forward-charter targets.

The patch is in `scripts/inter_wave_regression_sweep.py` lines ~280-360.

### Principle 4 — Disposition via the 5-option enum, never ad-hoc

Per the parent rule §RULE 2, every WARN/FAIL finding gets dispositioned via exactly one of:

1. `rework-now` (FAIL on baseline dimensions; the finding must be fixed in this commit).
2. `forward-charter-next-wave` (WARN on conditional dimensions; mint an OPS row or candidate file scoped to the next wave).
3. `defer-OPS` (INFO; mint OPS row but don't gate on it).
4. `accept-as-canon` (operator ratifies the drift was deliberate; append contra-precedent + decision-register row).
5. `escalate-to-blocker-tracker` (mint `_blockers/<slug>-tracker.md` per `akos-conflict-surfacing-and-blocker-trackers.mdc`).

Ad-hoc dispositions ("we'll address it later" without OPS row OR decision row) violate the rule and create silent governance debt.

### Principle 5 — Heuristic-evolution is a craft, not a bug-fix

When a probe heuristic produces false positives at rate > 20 %, the response is NOT just to file dispositions and move on. Patch the heuristic in the same commit (or the next commit in the same wave) so the next sweep doesn't repeat the noise. The patch must:

- Expand evidence sources (filesystem + canonical body + frontmatter sub-keys, not just decision-log).
- Improve token normalisation (alphanumeric-only comparison, stop-prefix filters, case-insensitive matching).
- Add unit tests in `tests/test_inter_wave_regression.py` to lock in the heuristic against regression.
- Document the heuristic evolution in the parent canonical's evidence-base section.

The Wave R DIM-02 heuristic patch is the worked example: 4 commits across the wave (sweep run → false-positive analysis → heuristic patch → tests + re-sweep) landed as a clean tightening of the rule.

## Per-dimension craft (13 dimensions, key gotchas)

| Dim | Probe focus | Common false-positive | Disposition default |
|:--|:---|:---|:---|
| 1 | decision_lineage | FK fails because decision row not yet appended (race condition between OPS row + DECISION row landing) | rework-now (add the missing decision row first) |
| 2 | forward_charter_carryover | Token-extraction misses evidence in `linked_canonicals` or `forward_charters_pending` | re-run after heuristic patch; if true gap, forward-charter-next-wave |
| 3 | validator_ramp_consistency | Threshold change without paired decision (often legitimate at INFO ramp; document in decision row) | accept-as-canon (after decision row) |
| 4 | canonical_csv_pair_completeness | Pydantic module missing OR Supabase mirror missing | rework-now (mints fail without full quartet) |
| 5 | sop_runbook_pairing | SOP exists but `linked_runbooks:` not populated in frontmatter | rework-now (1-line frontmatter edit) |
| 6 | uat_report_class_completeness | UAT report missing a §-class that `compose_UAT` requires for the initiative's audience tags | rework-now if class is mandatory; forward-charter if optional |
| 7 | render_trail_audience_match | External-tagged surface lacks paired render artifact | re-run `validate_external_render_trail.py --strict`; rework-now if confirmed |
| 8 | brand_baseline_register_match | CORPINT-internal token leaked into external surface | rework-now (translation back to external register) |
| 9 | cross_area_breakthrough_announcement | New PEOPLE_DESIGN_PATTERN_REGISTRY row without paired announcement evidence | defer-OPS if pattern is too new (< 1 wave old); rework-now otherwise |
| 10 | deploy_evidence_completeness | Sibling-repo commit without deploy_id evidence in files-modified | rework-now (capture the deploy_id from vendor MCP) |
| 11 | cursor_rule_skill_pairing | This skill's domain; new rule without paired skill | forward-charter-next-wave (most common); decline if rule is declarative-only |
| 12 | operator_scratchpad_continuity | Scratchpad last-review timestamp older than last commit | rework-now (drain scratchpad in same wave-close) |
| 13 | role_process_pairing_completeness | New role row without paired process_list row OR new process without resolvable role FK | rework-now for orphan-process (high severity); defer-OPS for ghost-role (low severity) |

## Pre-flight checklist (before each sweep)

1. Self-test PASSES (`py scripts/inter_wave_regression_sweep.py --self-test`).
2. Wave-letter argument is correct (`--wave-closing R` not `--wave-closing Q`).
3. Wave is **in-scope** per parent rule §"When this rule applies" (≥ 2 canonicals OR ≥ 2 cursor rules OR canonical-CSV mint).
4. Report path follows convention (`reports/regression-sweep-<YYYY-MM-DD>-wave-<letter>-close.md`).
5. JSON sidecar path is conventional (`artifacts/regression-sweep-<YYYY-MM-DD>-wave-<letter>.json`).
6. Findings count computed BEFORE drafting disposition gates.
7. False-positive spot-check (3-5 findings inspected against canonical body) completed.
8. Disposition enum (5 options) is the only mode used; no ad-hoc text.
9. Operator-scratchpad will be drained in the same wave-close commit (DIM-12 PASS guaranteed).
10. UAT report §3.3 reserves a row to cite this sweep + its disposition outcomes.

## Anti-patterns (don't do these)

- **AP1 — Sweep then move on without disposition.** Findings without dispositions = silent governance debt; never lands.
- **AP2 — Dispose by ad-hoc note.** "Will fix later" without OPS or DECISION row = breaks rule + audit trail.
- **AP3 — Skip the false-positive spot-check.** Filing 20 dispositions on noise wastes operator cycles + creates fatigue.
- **AP4 — Patch the heuristic in a separate wave.** Heuristic + dispositions belong in the same wave so the next sweep is clean.
- **AP5 — Treat all 13 dimensions as equal-weight.** Baseline 7 always fire; conditional 6 fire only when applicable; ignoring the rule wastes time.

## Recovery patterns

- **R1 — Too many findings (>20)**: halt + propose Wave-N + Wave-N.5 split; don't try to disposition all in one shot.
- **R2 — Heuristic broken**: write a failing unit test that reproduces the false positive; patch the probe; re-run sweep; verify tests pass.
- **R3 — Operator silent on dispositions**: per `akos-inline-ratification.mdc` Time-box recovery, auto-default after 24h+ silence only for reversible options (defer-OPS, forward-charter); never for accept-as-canon (irreversible) or escalate-to-blocker (high-blast).

## Cross-references

- Parent rule: [`akos-inter-wave-regression.mdc`](../../../.cursor/rules/akos-inter-wave-regression.mdc).
- Parent canonical: [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md).
- Paired runbook: [`scripts/inter_wave_regression_sweep.py`](../../../scripts/inter_wave_regression_sweep.py).
- Validator wrapper: [`scripts/validate_inter_wave_regression.py`](../../../scripts/validate_inter_wave_regression.py).
- Pydantic models: [`akos/hlk_inter_wave_regression.py`](../../../akos/hlk_inter_wave_regression.py).
- Sister skills: [`inline-ratify-craft`](../inline-ratify-craft/SKILL.md) (for disposition gates), [`index-integrity-craft`](../index-integrity-craft/SKILL.md) (sister wave-close discipline).
- Wave R worked example: `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/regression-sweep-2026-05-24-wave-r-close.md` (DIM-02 false-positive recovery).
- Ratifying decision: D-IH-86-CT (this skill's mint), D-IH-86-BK (parent rule mint).
