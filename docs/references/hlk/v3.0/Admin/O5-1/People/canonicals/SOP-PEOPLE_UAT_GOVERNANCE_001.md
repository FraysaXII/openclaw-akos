---
title: SOP — People — UAT governance bar enforcement
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_UAT_GOVERNANCE_001
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - PMO
co_authors:
  - System Owner
  - Founder/CEO
last_review: 2026-05-24
last_review_by: PMO
last_review_at: 2026-05-24
last_review_decision_id: D-IH-86-CW
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-AV
  - D-IH-86-AS
  - D-IH-86-CW
status: active
register: internal
parent_canonical: UAT_DISCIPLINE.md
companion_to:
  - UAT_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md
linked_canonicals:
  - UAT_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - ../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
linked_runbooks:
  - scripts/validate_uat_report.py
  - scripts/uat_governance_sweep.py
linked_skills:
  - .cursor/skills/uat-discipline-craft/SKILL.md
  - .cursor/skills/inline-ratify-craft/SKILL.md
linked_cursor_rules:
  - .cursor/rules/akos-uat-discipline.mdc
  - .cursor/rules/akos-planning-traceability.mdc
  - .cursor/rules/akos-quality-fabric.mdc
ssot: true
---

# SOP — People — UAT governance bar enforcement

> Paired SOP for the [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) canonical. Codifies the human-facing (AC-HUMAN) execution contract for enforcing the post-2026-05-19 UAT quality bar at every closure UAT report mint per [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT quality bar". Paired runbook: [`scripts/validate_uat_report.py`](../../../../../../scripts/validate_uat_report.py) (full 11-section strict v1, forward-only by date per the canonical's §migration posture).
>
> Operator-ratified at I86 Wave R+1 (D-IH-86-CW; 2026-05-24) as the missing SOP+runbook pair that closes [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §10 promotion criterion #3 ("Paired SOP + runbook lands; this enables UAT report machine-validation"). UAT_DISCIPLINE.md flipped from `status: charter` → `status: active` in the same commit with an explicit 3-wave field-test window monitoring obligation per ex5 ratification.

## Purpose

Every closure UAT report — for any initiative meeting the [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT quality bar" §"When this bar applies" trigger conditions — must satisfy the 11-section structure + frontmatter shape + per-class bar defined in [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §8.5 + §4 `compose_UAT(audience, channel, scenario, brand, governance) → 7-class UAT shape`. This SOP names the human + AIC execution contract for enforcing the bar; the paired runbook automates the structural + frontmatter checks.

## Scope

Applies to **every closure UAT report** authored at `docs/wip/planning/<NN-slug>/reports/uat-*.md` OR at any cluster-coordinator wave-close path (`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-wave-*.md`) whose parent initiative satisfies any of the §"When this bar applies" conditions:

- The initiative has **≥ 5 phases**.
- The initiative touches a **canonical CSV** under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`.
- The initiative ships **sibling-repo work** per `REPOSITORY_REGISTRY.csv`.
- The initiative is part of an **I86 cluster** (D-IH-86-D mechanical cross-check applies).
- The initiative promised **browser**, **dashboard**, **WebChat**, **Cursor IDE Browser MCP**, or **human-in-the-loop** verification.

Explicitly out of scope (the prior contract suffices: results table with PASS / SKIP / N/A + short notes): 1-3 phase quick fixes, single-file refactors, ad-hoc proposals under `_candidates/` or `99-proposals/`.

## Inputs

- **The closure UAT report markdown** at the canonical path above.
- **The parent initiative's `master-roadmap.md`** (for §"Closure criteria" rows to verify in UAT report §2).
- **The parent initiative's `decision-log.md`** (for `D-IH-<NN>-<X>` decisions referenced in UAT report §8).
- **The parent initiative's `risk-register.md`** (for `R-IH-<NN>-<N>` rows referenced in UAT report §7).
- **The parent initiative's `files-modified.csv`** (for §3 mechanical-evidence cross-references).
- **The cluster coordinator master-roadmap** (when applicable; for §5 mechanical cross-check signals).
- **`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`** (for `ratifying_decisions:` frontmatter FK resolution).
- **`scripts/<NAME>.py` runbooks** (for `linked_runbooks:` frontmatter FK resolution).

## Steps (AC-HUMAN; AIC consumes same steps)

1. **Run self-test.** `py scripts/validate_uat_report.py --self-test` MUST exit 0. If FAIL, the runbook is broken — halt and fix before continuing.
2. **Identify all in-scope UAT reports for this trigger.** For a wave-close trigger, the in-scope set is the wave's closure UAT report. For an initiative-close trigger, the in-scope set is the initiative's closure UAT report. For a CSV-mint trigger, the in-scope set is empty (the UAT report comes at the parent wave/initiative close, not at the CSV mint commit).
3. **Run full validation per report.** `py scripts/validate_uat_report.py --report <path>` emits the per-report findings. Validator enforces:
   - **Mandatory frontmatter fields** per [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §8.5 §"Mandatory frontmatter fields": `verdict:`, `closure_decision_source:`, `ratifying_decisions:`, `linked_runbooks:`, `verdict_history:` (only when amendment).
   - **`verdict:`** enum: PASS / PASS-WITH-FOLLOWUP / FAIL / PENDING-OPERATOR-WALK.
   - **`closure_decision_source:`** enum: agent_inline_default / operator_explicit / n/a.
   - **`ratifying_decisions:`** FK-resolve each row against `DECISION_REGISTER.csv`.
   - **`linked_runbooks:`** FK-resolve each row against `scripts/*.py` existence.
   - **11 mandatory sections** per §8.5 §"Mandatory sections" in binding order: §1 Closure summary, §2 Closure-criteria verification, §3 Mechanical evidence, §4 Per-dimension findings, §5 D-IH-86-D mechanical cross-check (when cluster sibling), §6 SOP+runbook pair (when applicable), §7 Risk-register closure, §8 Decision close-outs, §9 Closure registry edits, §10 Verdict + 7-item operator sign-off checklist, §11 Cross-references. Each section may collapse to a one-line N/A statement but cannot be omitted.
4. **Read the findings table.** Count FAIL / WARN / INFO / N/A; verify total findings ≤ 10 (else propose UAT-split bandwidth-recovery per [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc) §"Time-box recovery").
5. **Post the disposition `AskQuestion` batch.** One question per WARN/FAIL finding; 5-option enum per [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §6 + cursor rule RULE 2; recommended-default per finding-severity.
6. **Execute ratified dispositions.** rework-now → fix in-UAT before verdict; amend-followup-rationale → append explicit `verdict_followup_rationale:` field if verdict is PASS-WITH-FOLLOWUP; defer-OPS → append OPS_REGISTER row; accept-as-canon → append contra-precedent + decision row; escalate → mint `_blockers/` tracker.
7. **Finalize the UAT verdict.** When all findings PASS or N/A: verdict=PASS. When ≥1 finding requires followup with genuine rationale: verdict=PASS-WITH-FOLLOWUP (with mandatory `verdict_followup_rationale:` field per [`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md) — operator-ratified at I86 Wave R+1 / D-IH-86-CX as the discipline that closes the PWF abuse pattern).

## Outputs

- **Validated closure UAT report** at the canonical path; verdict line filled in.
- **Per-finding decision rows** in DECISION_REGISTER.csv for dispositions requiring operator-explicit ratification.
- **OPS_REGISTER.csv rows** for `defer-OPS` dispositions (one per row).
- **Tracker / candidate / blocker files** per `escalate-to-blocker-tracker` dispositions.
- **§10 7-item operator sign-off checklist** — operator marks PASS / N/A / DEFERRED per item before initiative closure flip in INITIATIVE_REGISTRY.

## Acceptance criteria

### AC-HUMAN

A human (or AIC role_owner per [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md)) can execute every Step above without invoking the runbook — by reading [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §8.5 directly, manually walking the 11-section checklist + frontmatter checklist against the in-scope UAT report markdown, drafting a findings table by hand, then posting the inline-ratify `AskQuestion` batch per [`inline-ratify-craft`](../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md). The output verdict + dispositions follow the same shape the runbook emits.

### AC-AUTOMATION

The runbook `scripts/validate_uat_report.py --report <path>` runs unattended (event-triggered at UAT report commit OR cron at wave-close commit OR dispatch from `scripts/release-gate.py`) and emits the same findings + frontmatter validation. The self-test mode `--self-test` runs at every `py scripts/verify.py pre_commit` invocation via [`config/verification-profiles.json`](../../../../../../config/verification-profiles.json) `validate_uat_report_self_test` step.

## Failure modes + remediation

- **Self-test FAIL** → runbook is broken; halt; fix the runbook before any UAT commit; never skip the validation to "ship the UAT".
- **Findings count > 10** → bandwidth-recovery; propose UAT-split or extend operator-walk window per [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc) §"Time-box recovery"; operator-explicit decision row records the split.
- **Operator silence > 24h on §10 sign-off** → time-box recovery; reversible items auto-default to recommended option; **irreversible items (initiative status flip; canonical-CSV gate sign-off; decision-register row appends) NEVER auto-default** — halt and escalate per [`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc).
- **PASS-WITH-FOLLOWUP without `verdict_followup_rationale:`** → validator FAIL; report must add the rationale field or change verdict to PASS / FAIL. This is the structural fix for the PWF abuse pattern (D-IH-86-CW / D-IH-86-CX framing).
- **Mandatory section missing** (forward-only reports dated ≥ 2026-05-19) → validator FAIL; UAT author MUST add the section (even as one-line N/A statement) before commit.
- **Historical UAT report** (`last_review:` < 2026-05-19) → validator emits INFO only; no FAIL per the canonical's §migration posture exempting pre-watershed reports.

## 3-wave field-test window (D-IH-86-CW promotion obligation)

Per the operator-explicit promotion-with-revocability framing (ex5 + meta4-b ratifications at the I86 Wave R+1 META-RATIFY batch, 2026-05-24): the UAT_DISCIPLINE.md `status: charter → active` flip carries a **3-wave field-test window monitoring obligation**:

- Wave S close, Wave T close, and Wave U close are the field-test waves.
- At each field-test wave-close, `scripts/validate_uat_report.py` runs against the wave's closure UAT report (mandatorily; no skip).
- If the validator misfires across ≥1 field-test wave AND the misfire is attributable to validator scope-creep (false positives) OR validator scope-gap (false negatives that should have caught real drift), the operator may invoke `D-IH-86-CW-revoke` to demote UAT_DISCIPLINE back to `status: charter` for v2 hardening.
- Successful field-test (zero validator misfires across Waves S+T+U) records the bar as durably-active in a closure decision row.

This is **NOT a PASS-WITH-FOLLOWUP-style deferred obligation** — it is an explicit committed-with-revocability monitoring posture per operator's PWF-abuse-correction framing. The distinction: PWF is "we shipped + the followup is vague + maybe never resolves"; field-test-window is "we shipped + the followup has a definite trigger + a definite revocation path".

## Cross-references

- Doctrine: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md).
- Cursor rule: [`akos-uat-discipline.mdc`](../../../../../../.cursor/rules/akos-uat-discipline.mdc).
- Paired skill: [`.cursor/skills/uat-discipline-craft/SKILL.md`](../../../../../../.cursor/skills/uat-discipline-craft/SKILL.md).
- Sister specialty SOP: [`SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md`](SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md).
- Sister specialty SOP (12th, this session): [`SOP-PEOPLE_PWF_GOVERNANCE_001.md`](SOP-PEOPLE_PWF_GOVERNANCE_001.md) — paired closure on PWF abuse pattern.
- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).
- Addendum: [`SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md`](SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md) (access_level 5; audit-detail).
- Runbook: [`scripts/validate_uat_report.py`](../../../../../../scripts/validate_uat_report.py) + [`scripts/uat_governance_sweep.py`](../../../../../../scripts/uat_governance_sweep.py).
- Pydantic models: [`akos/hlk_uat_report.py`](../../../../../../akos/hlk_uat_report.py).
- Tests: [`tests/test_validate_uat_report.py`](../../../../../../tests/test_validate_uat_report.py).
- Process catalog: `hol_peopl_dtp_uat_governance_001` in [`process_list.csv`](../Compliance/canonicals/process_list.csv).
- Pattern registry: `pattern_uat_class_taxonomy` in [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv).
- Decision lineage: D-IH-86-AV (canonical mint), D-IH-86-AS (UAT quality bar canonization), D-IH-86-CW (charter→active promotion via this SOP+runbook pair landing).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md
@.cursor/rules/akos-uat-discipline.mdc
