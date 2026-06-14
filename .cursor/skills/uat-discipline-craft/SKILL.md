---
name: UAT Discipline Craft
description: >-
  Use when authoring or amending a closure-UAT report in this AKOS
  workspace. Codifies the craft for producing 11-section closure UATs
  that PASS the validator on the first run, surface real signal (not
  cargo-cult sections), and honor the PASS-WITH-FOLLOWUP discipline
  without abusing it. Triggers on any phrase like closure UAT, UAT
  report, uat-*.md authoring, verdict line, PASS-WITH-FOLLOWUP rationale,
  UAT-FM-NN finding, UAT-SEC-NN finding, validate_uat_report.py, 11
  sections, closure-criteria verification, deploy verification at
  closure, browser-evidence audit trail, or when closing a wave that
  needs a closure-UAT mint. Pairs with .cursor/rules/akos-uat-discipline.mdc
  (the WHEN); this skill is the HOW.
---

# UAT Discipline Craft

## Why this skill exists

The cursor rule `akos-uat-discipline.mdc` and the canonical
`UAT_DISCIPLINE.md` tell you **when** to mint a closure UAT and **what**
the 11 sections + frontmatter fields are. This skill tells you **how** to
write them well, how to fill `verdict_followup_rationale` without abusing
PWF, and how to disposition validator findings without producing
governance-debt or false-PASS closure.

Read this skill before drafting any `uat-*.md` report for the first time
in a session, OR before re-running the validator after a multi-section
revision (the most common error is mis-numbering a section heading or
forgetting the PWF rationale).

## Principle 1 — Run the validator BEFORE the verdict line

The validator (`scripts/validate_uat_report.py --report <path>`) is
mechanical evidence for the wave-close §3 row. If you fill in the verdict
line before running the validator, you have to amend the UAT when the
validator surfaces a missing section or a PWF without rationale. Always:

1. Bring the wave's prior commit into a clean state (no `git status`
   noise interferes with the validator; it only reads the target file
   but stale fixtures confuse the self-test).
2. Run `py scripts/validate_uat_report.py --self-test` — must PASS.
3. Run `py scripts/validate_uat_report.py --report
   docs/wip/planning/<NN>/reports/uat-<wave-or-initiative>-<YYYY-MM-DD>.md`.
4. Read the findings table. Note each FAIL.
5. Fix structurally (add the missing section / add the missing
   frontmatter field / change the verdict). Do NOT auto-paper-over by
   accepting-as-canon — that is the rule's RULE 5 option 4 and exists
   only when the validator misfires structurally, not when your draft
   forgot a section.
6. Re-run the validator. Iterate until FAIL=0 (or, in the field-test
   window, until all FAIL findings are explicitly dispositioned via
   inline `AskQuestion`).
7. THEN fill the verdict line.

This is the same shape as the INTER_WAVE_REGRESSION sweep + the
INDEX_INTEGRITY sweep. The three sweeps compose: a wave with clean
regression + clean index but a FAIL-laden UAT validator is NOT
closure-ready.

## Principle 2 — Disposition findings via inline-ratify, batched

When the validator surfaces ≥ 1 FAIL finding, you do NOT silently
auto-fix and move on. You disposition via the 5-option enum from the
canonical §6 + the rule's RULE 5, surfaced as `AskQuestion` per
`akos-inline-ratification.mdc`.

Bad (auto-fix without ratification):

```
# Validator says UAT-FM-11-PWF-WITHOUT-RATIONALE.
# Agent silently appends a one-line rationale "see follow-up".
# Operator never sees that PWF is being used to defer real work.
```

Good (inline-ratify):

```
AskQuestion: validator FAIL UAT-FM-11 — verdict is PASS-WITH-FOLLOWUP
  but verdict_followup_rationale is missing. Per 12th specialty
  D-IH-86-CX, this MUST name the PWF class (1 of 5 per
  PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md §3) + the follow-up artifact
  path + the closure-target ETA. Recommended: amend-followup-rationale
  with class=monitoring-obligation (3-wave field-test window for the
  UAT validator promotion itself); tracker=this UAT's §10 row 7;
  ETA=Wave U close. Alternatives: rework-now (downgrade verdict to
  PASS — only if the gap can be closed in this commit) / escalate-to-
  blocker-tracker.
```

When findings exceed 10, **split into 2 AskQuestion batches**, grouped by
class:

- Batch 1: UAT-FM-NN frontmatter findings (usually structural; one fix
  per finding).
- Batch 2: UAT-SEC-NN section findings (usually one big append per
  section).

When findings exceed 20, **halt + propose structural rework**. A 20+
finding UAT report is mis-shapen: either the validator is misfiring (RULE
5 option 4 inline-ratify with operator) OR the draft skipped the
template entirely (rework-now: copy a known-good report as scaffold).

## Principle 3 — Section headers: use the verbose form for ratifying clarity

The validator accepts BOTH compact form (`## 1 — Closure summary`) and
verbose form (`## Section 1 — Closure summary`). The verbose form is
**preferred** for closure UATs because:

- The "Section" prefix is a J-OP-readable cue (the operator-scratchpad
  drain reader, the auditor, the System Owner) that this is the
  canonical UAT shape, not an ad-hoc heading.
- Future agents skimming the report don't need to count to know they're
  at section 7 vs section 8.
- The I86 Wave R closure precedent (the worked example that motivated
  the validator regex broadening) uses verbose form.

Compact form is acceptable when space is tight (e.g. the
`docs/wip/planning/_templates/uat-closure-template.md` may use compact
form to keep the template skimmable), but production reports default to
verbose.

## Principle 4 — `verdict_followup_rationale` is load-bearing prose, not a checkbox

When verdict=PASS-WITH-FOLLOWUP, the rationale field is the entire
governance signal. Write it as one sentence per PWF class element:

```yaml
verdict: PASS-WITH-FOLLOWUP
verdict_followup_rationale: >-
  PWF class = deferred-work-with-tracker. Wave R Lane B drain dispositioned
  53 findings; 6 forward-chartered as OPS-86-15..20 (Wave R+1 trigger). Tracker:
  this UAT §9 closure registry edits row 4 (OPS_REGISTER appends).
  ETA: Wave R+1 close (≤ 7 calendar days from this report).
```

Bad rationale (the false-PASS anti-pattern the 12th specialty exists to
prevent):

```yaml
verdict: PASS-WITH-FOLLOWUP
verdict_followup_rationale: "follow-up in next wave"
```

The bad version is what motivated the operator's META4-b ratification +
the META5-c full-specialty-mint (`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`).
The five PWF classes are NOT optional categorization — they are the
forcing function that surfaces whether the deferred work has a real
tracker, a real ETA, and a real owner.

## Principle 5 — `verdict_history` is mandatory for amendments

When you amend an existing closure UAT (e.g., operator review at Wave
M.5 surfaces a missed dimension; the I77 P3-P4 amendment precedent
applies), populate `verdict_history` with one entry per prior verdict:

```yaml
verdict_history:
  - "v1 — 2026-05-19 — PASS — amended at v2 to add dimension F.7 finding"
  - "v2 — 2026-05-20 — PASS-WITH-FOLLOWUP — added deploy regression context"
verdict: PASS-WITH-FOLLOWUP
verdict_followup_rationale: >-
  PWF class = monitoring-obligation. Wave M.5 amendment added Vercel
  deploy-class verification per D-IH-86-AT. Field-test window: next 2
  releases observed for build-context-class regression.
```

Skipping `verdict_history` on an amendment violates RULE 2 + erases the
audit trail. The validator catches this via `UAT-FM-09-VERDICT-HISTORY-
MISSING-ON-AMENDMENT` (when an amendment is detectable from git history
or commit message).

## Principle 6 — Section 6 (SOP+runbook pair) is the most-skipped section

When the parent initiative shipped a `process_list.csv` row, Section 6 is
mandatory + carries the AC-HUMAN + AC-AUTOMATION acceptance criteria per
`akos-executable-process-catalog.mdc` Rule 1 §5. Most drafts forget this
section because:

- The author of the UAT often isn't the author of the SOP.
- The runbook is usually a single script invocation; the section feels
  redundant when the runbook is cited elsewhere.

It is not redundant. Section 6 is the **paired-closure attestation**:
the human can run the SOP without the runbook AND the runbook fires
unattended. Both must be PASS-tested at closure.

Minimum Section 6 shape:

```markdown
## Section 6 — SOP + runbook pair

| AC | Surface | Verification | Status |
|---|---|---|---|
| AC-HUMAN | [`SOP-PEOPLE_<NAME>_001.md`](../../../references/.../SOP-PEOPLE_<NAME>_001.md) | Operator (or AIC role_owner) ran the SOP steps end-to-end at <date>; outputs match expected | PASS |
| AC-AUTOMATION | [`scripts/<runbook>.py`](../../../../../scripts/<runbook>.py) | `py scripts/<runbook>.py --<flags>` exits 0; self-test mode wired into pre_commit | PASS |
```

## Principle 7 — Section 5 (D-IH-86-D mechanical cross-check) is N/A for standalone initiatives

The I86 cluster-coordinator pattern requires a 4-signal cross-check for
cluster siblings:

1. ✓ `release-gate.py` INFO advisory: parent initiative row green.
2. ✓ `validate_hlk.py` OVERALL PASS.
3. ✓ Paired-runbook contract honored (or N/A-with-reason).
4. ✓ UAT report present (this report).

For standalone initiatives (NOT inside an I86 cluster), Section 5 is N/A
— but the section MUST still exist as a one-line N/A statement. The
validator's regex requires the section heading; the body can be:

```markdown
## Section 5 — D-IH-86-D mechanical cross-check (cluster wave closure)

N/A — this initiative is standalone (not registered as an I86 cluster
sibling per [`INITIATIVE_REGISTRY.csv`](../../../references/.../INITIATIVE_REGISTRY.csv)
cluster_membership column). The 4-signal cross-check applies to I86
sibling closures only per D-IH-86-D.
```

Omitting the section entirely triggers `UAT-SEC-05-MISSING` FAIL.

## Principle 8 — Section 10 (operator sign-off) is ≤ 7 items

Per `akos-agent-checkpoint-discipline.mdc` §"Operator pause point
contract", the sign-off checklist is ≤ 7 items. More items = pause
fatigue. Fewer items = under-specified review surface.

Each item should:

- Be specific and binary (PASS / N/A / DEFERRED).
- Cite the section/evidence it confirms.
- Be auto-clear-eligible (reversible) OR require explicit operator
  acknowledgement (irreversible). Mark irreversible items explicitly.

Bad row:

```markdown
- [ ] Review the report.
```

Good row:

```markdown
- [ ] (reversible) §3.2 validator outputs reviewed; `validate_uat_report
  --self-test` PASS confirmed at <commit-sha>.
- [ ] (IRREVERSIBLE) §9 DECISION_REGISTER appends confirmed via
  `validate_decision_register PASS` at <commit-sha>; no row reordering;
  D-IH-86-CW/CX rows match operator ratification.
```

## Pre-flight checklist (run before opening the report file)

1. □ Validator self-test PASS (`py scripts/validate_uat_report.py
   --self-test`).
2. □ Parent initiative master-roadmap §"Closure criteria" identified +
   read.
3. □ All `D-IH-NN-X` decision IDs ratifying this closure listed.
4. □ All `R-IH-NN-N` risk IDs from the risk register listed.
5. □ All sibling-repo deploy IDs identified (per RULE 7); vendor-MCP
   credentials available OR code-evidence fallback acceptable.
6. □ Verdict pre-decided (PASS / PWF / FAIL / PENDING-OPERATOR-WALK);
   if PWF, the PWF class is pre-decided (one of 5 per `PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md` §3).
7. □ Closure-template at `docs/wip/planning/_templates/uat-closure-template.md`
   open as scaffold reference.

## Anti-patterns (don't do these)

- **Anti-pattern A: Verdict-first authoring.** Filling the verdict line
  at the top of the file before the §1-§11 body content is written +
  validator-checked. Common failure mode: PWF rationale gets written
  last as boilerplate.
- **Anti-pattern B: Section omission via "this section is N/A so I
  removed it".** The validator's regex requires section headings even
  when the body is one-line N/A. Removing the heading triggers a FAIL.
- **Anti-pattern C: Multi-section findings collapsed into one finding
  row.** Each FAIL finding from the validator gets its own disposition.
  Bundling 5 findings into "rework all 5" hides which dispositions are
  reversible.
- **Anti-pattern D: PASS-WITH-FOLLOWUP as default verdict.** PWF is
  reserved for cases where the closure is real but a bounded follow-up
  remains. When in doubt, use PASS + add the follow-up as an OPS row, OR
  use FAIL + escalate. Defaulting to PWF for "I'm not sure" is what
  motivated the 12th specialty.
- **Anti-pattern E: `closure_decision_source: agent_inline_default`
  without time-box compliance.** This source is reserved for the 24h+
  silence + clean validators + reversible items path per
  `akos-inline-ratification.mdc` §"Time-box recovery". Using it for
  irreversible items is a discipline violation.

## Recovery patterns (when something went wrong)

- **Recovery A: Validator FAIL after report committed.** Mint an
  amendment commit per Principle 5 (populate `verdict_history`); cite
  the amending decision row (e.g., `D-IH-NN-X-amend`); revise the report
  in-place; re-run validator; re-commit. Do NOT delete the prior
  commit's history.
- **Recovery B: PWF rationale was omitted in the original commit.**
  Same as Recovery A — amend with `verdict_history` + populate the
  rationale + cite the PWF class + tracker + ETA. The original commit
  stays as v1; the amendment is v2.
- **Recovery C: Section ordering wrong.** Re-order the sections to match
  §8.5 canonical order. The validator does not enforce ordering today
  (regex matches by content, not position), but downstream readers
  expect §1 → §11 top-to-bottom. Mis-ordering surfaces in operator
  review even when the validator PASSes.

## Principle 8 — Experiential walks: capture ≠ review (L3.0)

For **L3 / L3.5 browser-evidence** UAT (not the 11-section closure bar):

1. **Never delegate visual review** to a subagent. The parent agent must
   `Read` every journey PNG in the foreground session.
2. Write `agent_visual_review.json` in the capture folder (`delegation_allowed: false`).
3. Run `py scripts/validate_uat_screenshot_evidence.py --session-dir …`
   **before** the UAT verdict line.
4. Capture hygiene: 1280×800, **sidebar collapsed**, scroll audit panels
   into view; duplicate sha256 across journey stages = FAIL.

I96 worked example: [`SOP-EXPERIENTIAL_UAT_AGENT_VISUAL_REVIEW_001.md`](../../../docs/wip/planning/96-research-data-plane-and-research-center/reports/SOP-EXPERIENTIAL_UAT_AGENT_VISUAL_REVIEW_001.md).

## Cross-references

- Parent rule: [`.cursor/rules/akos-uat-discipline.mdc`](../../rules/akos-uat-discipline.mdc) — the WHEN.
- Parent canonical: [`UAT_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md) — the doctrine.
- Paired SOP: [`SOP-PEOPLE_UAT_GOVERNANCE_001.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.md) — AC-HUMAN execution contract.
- Paired runbook: [`scripts/validate_uat_report.py`](../../../scripts/validate_uat_report.py) — AC-AUTOMATION enforcement.
- Pydantic SSOT: [`akos/hlk_uat_report.py`](../../../akos/hlk_uat_report.py) — frozen models.
- Template: [`docs/wip/planning/_templates/uat-closure-template.md`](../../../docs/wip/planning/_templates/uat-closure-template.md) — the scaffold.
- Sister skill: [`.cursor/skills/inline-ratify-craft/SKILL.md`](../inline-ratify-craft/SKILL.md) — for disposition AskQuestion craft (used by Principle 2).
- Sister skill: [`.cursor/skills/index-integrity-craft/SKILL.md`](../index-integrity-craft/SKILL.md) — sister 11th specialty (same compose() function shape).
- Worked precedents: I85 closure UAT (Bundle D Wave B, 2026-05-19), I87 closure UAT (Bundle D Wave C, 2026-05-19), I86 Wave R closure UAT (Wave R, 2026-05-24; the worked example for the verbose section-header form + the PWF-without-rationale field-test catch).
- Decision lineage: D-IH-86-AV (canonical mint) + D-IH-86-AS (bar canonization) + D-IH-86-CW (charter→active promotion + this skill's mint) + D-IH-86-CX (PWF discipline; Principle 4 dependency).
