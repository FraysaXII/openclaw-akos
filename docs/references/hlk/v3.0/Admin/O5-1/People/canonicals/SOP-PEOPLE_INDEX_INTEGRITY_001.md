---
title: SOP — People Baseline Index Integrity Sweep
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_INDEX_INTEGRITY_001
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
last_review_decision_id: D-IH-86-CF
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-CD
  - D-IH-86-CE
  - D-IH-86-CF
status: charter
register: internal
linked_canonicals:
  - INDEX_INTEGRITY_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - UAT_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
linked_runbooks:
  - scripts/baseline_index_sweep.py
  - scripts/validate_index_freshness.py
linked_processes:
  - hol_peopl_dtp_index_integrity_001
cadence: event_triggered
cadence_trigger: wave-close commit OR canonical-CSV mint commit
cadence_secondary: scheduled
cadence_secondary_schedule: per-wave-cadence
---

# SOP — People Baseline Index Integrity Sweep

## Purpose

Operationalise the baseline-index integrity discipline named in
[`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md). Every
in-scope wave-close OR canonical-CSV mint runs the 8-dimension index-
freshness sweep before the wave's UAT verdict line is filled in / before
the CSV-mint commit lands.

Paired with runbook [`scripts/baseline_index_sweep.py`](../../../../../../scripts/baseline_index_sweep.py)
+ validator wrapper [`scripts/validate_index_freshness.py`](../../../../../../scripts/validate_index_freshness.py)
per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1. Either the PMO (interim until COO activation per I76) — or an
AIC role_owner per [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc)
forward — executes via this SOP, OR the runbook fires unattended at the
trigger commit. Both surfaces are SSOT for the same process.

## Scope

In scope:

- Wave-close sweep for any cluster-coordinator initiative (I86 precedent;
  future analogous coordinators).
- Canonical-CSV mint sweep for any new row landing in
  `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`
  or its `dimensions/` subdir.
- Disposition of drift / gap / blocked findings via inline-ratify per
  [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc).
- Forward-charter + tracker file mint per disposition.

Out of scope:

- Chore-only single-commit waves (typo fixes; link-rot fixes;
  formatting normalisations) — exempt per canonical §4 Exception 1.
- Multi-commit waves: sweep at wave-close only, not per-commit.
- Standalone (non-wave-cadence) initiatives — covered by
  `akos-planning-traceability.mdc` §"UAT quality bar".

## Inputs

- Trigger code: `wave_close` OR `canonical_csv_mint` OR `on_demand`.
- For `wave_close`: closing wave letter (e.g., `Wave-N`, `Wave-O`) +
  parent initiative master-roadmap path.
- For `canonical_csv_mint`: the freshly-minted CSV path + the row(s)
  added.
- Output target path (default: `docs/wip/planning/<NN-coordinator>/
  reports/index-sweep-<YYYY-MM-DD>.md`).

## Steps (AC-HUMAN; AIC consumes same steps)

1. **Run self-test.** `py scripts/baseline_index_sweep.py --self-test`
   AND `py scripts/validate_index_freshness.py --self-test` MUST both
   exit 0. If FAIL, the runbook is broken — halt and fix before
   continuing.
2. **Run full sweep.** `py scripts/baseline_index_sweep.py --sweep-trigger
   <trigger> --output <output_path>` emits the markdown report + the
   JSON sidecar.
3. **Read the findings table.** Count fresh / drift / gap / blocked /
   skip; verify total findings ≤ 16 (else propose wave-split or batch
   the disposition gates per Principle 5 of the paired skill).
4. **Post the disposition `AskQuestion` batch.** One question per
   drift/gap/blocked finding; 5-option enum per canonical §6 + cursor
   rule RULE 2 (deterministic-fix-now / manual-fix-now / defer-OPS /
   accept-as-canon / escalate-to-blocker-tracker); recommended-default
   per finding-severity + dimension auto-fix path.
5. **Execute ratified dispositions.** deterministic-fix → invoke
   `--fix --dimension IDX-NN` (only IDX-01 / IDX-02 / IDX-07 / IDX-08
   have safe paths today); manual-fix → operator/agent edits the index
   doc; defer-OPS → append OPS_REGISTER row; accept-as-canon → append
   contra-precedent + decision row; escalate → mint `_blockers/` tracker.
6. **Update operator-scratchpad.** Wave's sweep summary + disposition
   decision IDs + remaining drift MUST land in
   `docs/wip/intelligence/operator-scratchpad.md` before the wave's
   atomic commit.
7. **Finalize the wave's UAT report verdict.** Reference the sweep
   report path from §3 mechanical-evidence row under the index-integrity
   sub-class.

## Outputs

- `reports/index-sweep-<YYYY-MM-DD>.md` under parent initiative folder
  (markdown table operator-readable).
- `artifacts/index-sweep-<YYYY-MM-DD>.json` (machine-readable for
  downstream agents).
- Decision rows in DECISION_REGISTER.csv for each disposition.
- Tracker / candidate / OPS rows per disposition.
- Updated operator-scratchpad entry.
- Wave's UAT report §3 row pointing to sweep report.

## Acceptance criteria

### AC-HUMAN

A human (or AIC role_owner) can execute every Step above without
invoking the runbook — by reading the canonical §2 dimensions table,
manually inspecting each dimension's probe heuristic against the index
documents' state vs source-of-truth, drafting a findings table by hand,
then posting the inline-ratify `AskQuestion` batch. The output Markdown
report follows the same schema the runbook emits. Manual probe execution
is tedious but deterministic — for the 8 dimensions, expect 30-60min of
manual work vs ~5s of runbook execution.

### AC-AUTOMATION

The runbook `scripts/baseline_index_sweep.py --sweep-trigger
<trigger>` runs unattended (cron / event-triggered at wave-close OR
canonical-CSV mint / dispatch script) and emits the same markdown +
JSON outputs at the same paths. The self-test mode of both runbook +
validator wrapper runs at every `py scripts/verify.py pre_commit`
invocation via `validate_index_freshness_self_test` step in
`config/verification-profiles.json`.

## Failure modes + remediation

- **Self-test FAIL** → runbook or validator is broken; halt; fix before
  any wave-close commit; never skip the sweep to "ship the wave".
- **Findings count > 16** → batch the `AskQuestion` disposition into 2
  batches per skill Principle 5 (typically by dimension family:
  IDX-01..IDX-04 governance-doc drift; IDX-05..IDX-08
  registry-coverage drift).
- **Operator silence > 24h** → time-box recovery per
  `akos-inline-ratification.mdc`; reversible dispositions auto-default
  to recommended option; irreversible dispositions HALT and escalate.
- **Sweep report missing at wave-close commit time** → release-gate
  INFO advisory during Wave N backfill window; FAIL after operator-
  explicit FAIL promotion (D-IH-86-CD rationale or successor row).
- **Probe internal error** → runbook bug; finding emits `blocked`
  verdict with `PROBE-INTERNAL-ERROR` index_path; report does not
  represent index state; investigate probe internals before trusting
  the rest of the sweep.

## Cross-references

- Doctrine: [`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md).
- Cursor rule: [`akos-index-integrity.mdc`](../../../../../../.cursor/rules/akos-index-integrity.mdc).
- Skill: [`index-integrity-craft`](../../../../../../.cursor/skills/index-integrity-craft/SKILL.md).
- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).
- Sister discipline SOP: [`SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md`](SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md)
  (Wave M precedent — same shape).
- Runbook: [`scripts/baseline_index_sweep.py`](../../../../../../scripts/baseline_index_sweep.py).
- Validator wrapper: [`scripts/validate_index_freshness.py`](../../../../../../scripts/validate_index_freshness.py).
- Pydantic models: [`akos/hlk_index_integrity.py`](../../../../../../akos/hlk_index_integrity.py).
- Process catalog: `hol_peopl_dtp_index_integrity_001` in
  [`process_list.csv`](../Compliance/canonicals/process_list.csv).
- Decision lineage: D-IH-86-CD (canonical mint + INFO ramp),
  D-IH-86-CE (8-dimension probe set), D-IH-86-CF (paired SOP+runbook
  gate per `akos-executable-process-catalog.mdc` Rule 1).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md
@.cursor/rules/akos-index-integrity.mdc
