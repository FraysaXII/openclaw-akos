---
title: SOP — People PASS-WITH-FOLLOWUP Governance
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_PWF_GOVERNANCE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - PMO
co_authors:
  - System Owner
  - Founder/CEO
last_review: 2026-05-25
last_review_by: PMO
last_review_decision_id: D-IH-86-CX
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-CW
  - D-IH-86-CX
status: charter
register: internal
linked_canonicals:
  - PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md
  - UAT_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - INDEX_INTEGRITY_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
linked_runbooks:
  - scripts/validate_pwf_governance.py
linked_processes:
  - hol_peopl_dtp_pwf_governance_001
cadence: event_triggered
cadence_trigger: UAT authoring time (verdict=PASS-WITH-FOLLOWUP) OR wave-close commit
cadence_secondary: scheduled
cadence_secondary_schedule: per-wave-cadence
---

# SOP — People PASS-WITH-FOLLOWUP Governance

## Purpose

Operationalise the structural-rationale discipline named in
[`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md).
Every closure UAT report whose `verdict:` is `PASS-WITH-FOLLOWUP`
MUST carry a structured `verdict_followup_rationale` block matching
one of the 5 followup classes (monitoring-obligation /
deferred-work-with-tracker / convention-class-followup /
mechanical-recovery-with-eta / escalation-to-blocker-tracker).

Paired with runbook
[`scripts/validate_pwf_governance.py`](../../../../../../scripts/validate_pwf_governance.py)
per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1. Either the PMO (interim until COO activation per I76) — or an
AIC role_owner per [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc)
forward — executes via this SOP at UAT authoring time, OR the
validator fires at wave-close + at pre_commit (self-test mode). Both
surfaces are SSOT for the same process.

## Scope

In scope:

- Any closure UAT report under `docs/wip/planning/**/reports/uat-*.md`
  whose `verdict:` is `PASS-WITH-FOLLOWUP` and whose `last_review:` is
  ≥ 2026-05-19 (forward-only watershed per
  [`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md) §2).
- Disposition of WARN / FAIL findings via inline-ratify per
  [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc).
- Tracker / OPS-row mint per disposition outcome.

Out of scope:

- Pre-watershed reports (`last_review` < 2026-05-19): validator emits
  INFO findings only; no human disposition required.
- PASS / FAIL / PENDING-OPERATOR-WALK verdicts: validator no-ops; SOP
  does not apply.
- Non-UAT artifacts (phase reports, ratification artifacts): forward-
  charter pointer in the canonical; out of scope until promotion.

## Inputs

- Trigger code: `uat_authoring_time` OR `wave_close` OR `on_demand`.
- For `uat_authoring_time`: the report path being authored.
- For `wave_close`: closing wave letter (e.g., `Wave-S`) + parent
  initiative master-roadmap path.
- For `on_demand`: full-sweep or single-report selector.

## Steps (AC-HUMAN; AIC consumes same steps)

1. **Run self-test.** `py scripts/validate_pwf_governance.py --self-test`
   MUST exit 0. If FAIL, the validator is broken — halt and fix.
2. **Select rationale class.** Read
   [`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md)
   §3 (the 5-class enum). Pick the one class that matches the
   followup's substance. Worked examples are in the paired skill
   [`.cursor/skills/pwf-governance-craft/SKILL.md`](../../../../../../.cursor/skills/pwf-governance-craft/SKILL.md).
3. **Author the rationale block.** Add to the UAT report's
   frontmatter:

   ```yaml
   verdict: PASS-WITH-FOLLOWUP
   verdict_followup_rationale:
     followup_class: <one of the 5 classes>
     closure_target: <Wave-X close | YYYY-MM-DD | OPS-NN-N closed | D-IH-NN-X | FTW-CODE closes>
     owner: <role name from baseline_organisation.csv OR AIC:<role>>
     tracker_path: <docs/wip/planning/_trackers/<slug>.md OR _blockers/<slug>-tracker.md>  # if required by class
     closure_decision_id_target: <D-IH-NN-X if known>  # optional
     notes: <free-text context>
   ```

4. **Validate the single report.** `py scripts/validate_pwf_governance.py
   --report <path> --strict` MUST exit 0. If FAIL, address the finding
   codes per §6 disposition guide.
5. **Disposition any WARN / FAIL findings** via inline `AskQuestion`
   per [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc).
   Use the 5-option enum:
   - `deterministic-fix-now` (default for missing rationale fields)
   - `manual-fix-now` (default for malformed tracker_path)
   - `defer-OPS` (only for pre-watershed reports)
   - `accept-as-canon` (rare; appends contra-precedent)
   - `escalate-to-blocker-tracker` (when rationale gap is itself
     blocked on operator judgement)
6. **Author paired tracker if class requires it.** For
   `deferred-work-with-tracker` → mint under `_trackers/`. For
   `escalate-to-blocker-tracker` → mint under `_blockers/` per
   [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc).
7. **Wave-close sweep (PMO / AIC at every wave-close):**
   `py scripts/validate_pwf_governance.py --wave-closing <wave> --strict`
   MUST exit 0 once promoted (currently INFO until ramp closes per
   canonical §4.1). The wave's UAT closure report cites the sweep
   output as §3.3 mechanical evidence.
8. **Sync follow-ups.** Disposition outcomes that mint trackers or
   OPS rows update the parent initiative's `files-modified.csv` per
   [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc)
   §"Per-initiative file-changes CSV".

## Steps (AC-AUTOMATION; runbook unattended path)

The validator fires unattended at three triggers:

1. **pre_commit self-test**: `validate_pwf_governance_self_test` step
   in [`config/verification-profiles.json`](../../../../../../config/verification-profiles.json)
   `pre_commit` profile runs `--self-test` only (zero-cost circuit-
   breaker).
2. **release-gate advisory**: `run_pwf_governance_validation` in
   [`scripts/release-gate.py`](../../../../../../scripts/release-gate.py)
   sweeps all forward-only UAT reports and emits INFO findings during
   the ramp window. Promotes to FAIL at Wave T close per canonical §4.1.
3. **wave-close sweep**: invoked by the wave-close commit's UAT
   authoring agent OR by an AIC at wave-close gate; emits markdown
   findings report at `docs/wip/planning/<NN-coordinator>/reports/pwf-
   governance-sweep-<YYYY-MM-DD>-wave-<X>.md`.

## Outputs

- Authored UAT report with structural rationale (the PWF-class
  closure trail).
- Validator output (markdown human-readable OR JSON via `--json-log`)
  with finding count + per-finding code + remediation hint.
- Paired tracker file (when class requires) under `_trackers/` or
  `_blockers/`.
- Sync entries in parent initiative `files-modified.csv`.

## Failure modes

| Mode | Detection | Remediation |
|:---|:---|:---|
| Validator self-test FAIL | `--self-test` exit code ≠ 0 | Inspect runbook + Pydantic SSOT; fix; rerun |
| Forward-only report missing rationale | PWF-FM-01 finding | Author rationale per §3 class enum |
| Unknown class value | PWF-FM-02 finding | Pick closest enum value OR amend canonical §3 enum via operator decision |
| Missing closure_target | PWF-FM-03 finding | Add target field; use Wave-X / ISO date / OPS-NN-N / D-IH-NN-X shape |
| Missing tracker_path on tracker-requiring class | PWF-FM-04-MISSING | Mint tracker under `_trackers/` or `_blockers/`; cite path |
| Stale tracker_path (file does not exist) | PWF-FM-04-INVALID | Mint the cited tracker OR correct the path; FK against filesystem |
| Missing owner (WARN) | PWF-FM-05 finding | Add owner from baseline_organisation.csv or AIC:<role>; advisory only |

## Acceptance criteria

### AC-HUMAN (operator or AIC executes the SOP)

A PMO operator OR an AIC role_owner can author / amend a PWF UAT
report end-to-end via this SOP without invoking the validator:

1. Reads §3 class enum + picks class matching the followup substance.
2. Authors the rationale block per §3 step template + class-specific
   required fields (§3.1–§3.5).
3. Runs the validator at the end to confirm zero FAIL findings.
4. Dispositions any WARN findings (PWF-FM-05) at operator discretion.

### AC-AUTOMATION (validator fires unattended)

The validator fires automatically without operator intervention:

1. `py scripts/verify.py pre_commit` invokes `--self-test` step;
   PASS gate (FAIL halts pre_commit).
2. `py scripts/release-gate.py` invokes the full-sweep advisory;
   INFO findings during ramp; FAIL post-ramp.
3. Wave-close commit's UAT authoring agent invokes
   `--wave-closing <wave>` at wave-close gate; sweep findings land in
   the closing wave's UAT report §3.3 mechanical evidence row.

## Cross-references

- Parent canonical: [`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md).
- Parent meta-canonical: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).
- Sister specialty SOPs: [`SOP-PEOPLE_UAT_GOVERNANCE_001.md`](SOP-PEOPLE_UAT_GOVERNANCE_001.md) +
  [`SOP-PEOPLE_INDEX_INTEGRITY_001.md`](SOP-PEOPLE_INDEX_INTEGRITY_001.md) +
  [`SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md`](SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md).
- Paired cursor rule: [`.cursor/rules/akos-pwf-governance.mdc`](../../../../../../.cursor/rules/akos-pwf-governance.mdc).
- Paired skill: [`.cursor/skills/pwf-governance-craft/SKILL.md`](../../../../../../.cursor/skills/pwf-governance-craft/SKILL.md).
- Disposition rule: [`.cursor/rules/akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc).
- Escalation rule: [`.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc).
- Decision lineage: D-IH-86-CW (Wave R+1 Commit 1), D-IH-86-CX (this mint).
