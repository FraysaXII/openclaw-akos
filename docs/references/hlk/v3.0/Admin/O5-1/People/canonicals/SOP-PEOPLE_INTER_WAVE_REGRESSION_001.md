---
title: SOP — People Inter-Wave Regression Sweep
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_INTER_WAVE_REGRESSION_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - PMO
co_authors:
  - System Owner
  - Founder/CEO
last_review: 2026-05-21
last_review_by: PMO
last_review_decision_id: D-IH-86-BP
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BK
  - D-IH-86-BP
status: charter
register: internal
linked_canonicals:
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
linked_runbooks:
  - scripts/inter_wave_regression_sweep.py
linked_processes:
  - hol_peopl_dtp_inter_wave_regression_001
cadence: event_triggered
cadence_trigger: wave-close commit landing for in-scope multi-wave initiative
cadence_secondary: scheduled
cadence_secondary_schedule: per-wave-cadence
---

# SOP — People Inter-Wave Regression Sweep

## Purpose

Operationalise the wave-close regression discipline named in
[`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md).
Every in-scope multi-wave initiative (cluster-coordinator pattern;
I86 precedent) runs the 12-dimension regression sweep at every
wave-close before the wave's UAT report verdict line is finalized.

Paired with runbook [`scripts/inter_wave_regression_sweep.py`](../../../../../../scripts/inter_wave_regression_sweep.py)
per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1. Either the PMO (or AIC role_owner per `akos-people-discipline-of-disciplines.mdc`
forward) executes via this SOP, OR the runbook fires unattended at
wave-close commit. Both surfaces are SSOT for the same process.

## Scope

In scope:

- Wave-close sweep for any initiative registered in
  [`INITIATIVE_REGISTRY.csv`](../Compliance/canonicals/INITIATIVE_REGISTRY.csv)
  with a wave-cadence master-roadmap.
- Disposition of WARN/FAIL findings via inline-ratify per
  [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc).
- Forward-charter + tracker file mint per disposition.

Out of scope:

- Standalone (non-wave-cadence) initiatives — covered by
  `akos-planning-traceability.mdc` §"UAT quality bar".
- Single-commit chore waves — exempt per canonical §4 Exception 3.
- Sibling-area UAT classes — covered by `UAT_DISCIPLINE.md` §5
  cross-area inheritance contract.

## Inputs

- Closing wave letter (e.g., `Wave-L`, `Wave-M`).
- Prior wave letters in scope (default: all prior waves of the same
  parent initiative).
- The parent initiative's master-roadmap path.
- The wave's files-modified.csv subset for this wave.

## Steps (AC-HUMAN; AIC consumes same steps)

1. **Run self-test.** `py scripts/inter_wave_regression_sweep.py --self-test` MUST exit 0. If FAIL, the runbook is broken — halt and fix before continuing.
2. **Run full sweep.** `py scripts/inter_wave_regression_sweep.py --wave-closing <wave-letter>` emits `reports/regression-sweep-<YYYY-MM-DD>.md` under the parent initiative folder.
3. **Read the findings table.** Count FAIL / WARN / INFO / N/A; verify total findings ≤ 20 (else propose wave-split bandwidth-recovery).
4. **Post the disposition `AskQuestion` batch.** One question per WARN/FAIL finding; 5-option enum per canonical §6 + cursor rule RULE 2; recommended-default per finding-severity.
5. **Execute ratified dispositions.** rework-now → fix in-wave; forward-charter → mint `_candidates/`/`_trackers/` file; defer-OPS → append OPS_REGISTER row; accept-as-canon → append contra-precedent + decision row; escalate → mint `_blockers/` tracker.
6. **Update operator-scratchpad.** Wave's summary + decision IDs + gaps + forward-pointers MUST land in `docs/wip/intelligence/operator-scratchpad.md` before the wave's atomic commit (dimension 12 guaranteed PASS).
7. **Finalize the wave's UAT report verdict.** Reference the sweep report path from §3.3 row under regression class.

## Outputs

- `reports/regression-sweep-<YYYY-MM-DD>.md` under parent initiative folder.
- Decision rows in DECISION_REGISTER.csv for each disposition.
- Tracker / candidate / OPS rows per disposition.
- Updated operator-scratchpad entry.
- Wave's UAT report regression-class §3.3 row pointing to sweep report.

## Acceptance criteria

### AC-HUMAN

A human (or AIC role_owner) can execute every Step above without invoking the runbook — by reading the canonical §2 dimensions table, manually inspecting each dimension's probe heuristic against the wave's deliverables, drafting a findings table by hand, then posting the inline-ratify `AskQuestion` batch. The output Markdown report follows the same schema the runbook emits.

### AC-AUTOMATION

The runbook `scripts/inter_wave_regression_sweep.py --wave-closing <wave-letter>` runs unattended (cron / event-triggered at wave-close commit / dispatch script) and emits the same Markdown report at the same path. The self-test mode runs at every pre_commit invocation via verification-profiles.json.

## Failure modes + remediation

- **Self-test FAIL** → runbook is broken; halt; fix the runbook before any wave-close commit; never skip the sweep to "ship the wave".
- **Findings count > 20** → bandwidth-recovery; propose wave-split into Wave-N + Wave-N.5; operator-explicit decision row records the split.
- **Operator silence > 24h** → time-box recovery per `akos-inline-ratification.mdc`; reversible dispositions auto-default to recommended option; irreversible dispositions HALT and escalate.
- **Sweep report missing** at wave-close commit time → release-gate INFO advisory (Wave M+3 forward; FAIL when ramp completes per D-IH-86-BN).

## Cross-references

- Doctrine: [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md).
- Cursor rule: [`akos-inter-wave-regression.mdc`](../../../../../../.cursor/rules/akos-inter-wave-regression.mdc).
- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).
- Sister SOP: [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) (announces this SOP's pattern mint).
- Runbook: [`scripts/inter_wave_regression_sweep.py`](../../../../../../scripts/inter_wave_regression_sweep.py).
- Pydantic models: [`akos/hlk_inter_wave_regression.py`](../../../../../../akos/hlk_inter_wave_regression.py).
- Tests: [`tests/test_inter_wave_regression.py`](../../../../../../tests/test_inter_wave_regression.py).
- Process catalog: `hol_peopl_dtp_inter_wave_regression_001` in [`process_list.csv`](../Compliance/canonicals/process_list.csv).
- Decision lineage: D-IH-86-BK (canonical mint), D-IH-86-BP (this SOP's mint pairing).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md
@.cursor/rules/akos-inter-wave-regression.mdc
