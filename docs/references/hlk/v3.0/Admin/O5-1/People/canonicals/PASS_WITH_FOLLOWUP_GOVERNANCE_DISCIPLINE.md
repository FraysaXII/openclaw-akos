---
title: PASS-WITH-FOLLOWUP Governance Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - PMO
  - System Owner
last_review: 2026-05-25
last_review_by: Founder/CEO
last_review_at: 2026-05-25
last_review_decision_id: D-IH-86-CX
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-CW
  - D-IH-86-CX
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - INDEX_INTEGRITY_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
linked_cursor_rules:
  - .cursor/rules/akos-pwf-governance.mdc
  - .cursor/rules/akos-uat-discipline.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc
  - .cursor/rules/akos-inline-ratification.mdc
  - .cursor/rules/akos-planning-traceability.mdc
linked_skills:
  - .cursor/skills/pwf-governance-craft/SKILL.md
  - .cursor/skills/uat-discipline-craft/SKILL.md
  - .cursor/skills/inline-ratify-craft/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
forward_charters:
  - process_list.csv row hol_peopl_dtp_pwf_governance_001
  - PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_pwf_governance_discipline
  - paired SOP SOP-PEOPLE_PWF_GOVERNANCE_001.md
  - cursor rule .cursor/rules/akos-pwf-governance.mdc (binding rules 1-6)
  - paired skill .cursor/skills/pwf-governance-craft/SKILL.md (the *how* layer)
  - INFO->FAIL ramp at Wave T+ once Commit-3-c amend closes Wave R PWF-FM-01
  - 3-wave field-test-window monitoring obligation closes Wave U (per UAT_DISCIPLINE.md §10 promotion log)
---

# PASS-WITH-FOLLOWUP Governance Discipline

> The People-area canonical that names the structural shape required of
> any `PASS-WITH-FOLLOWUP` (PWF) closure verdict. Twelfth specialty
> instantiation of [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md)
> (per D-IH-86-CX) and the **content axis** that pairs with
> [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md)'s **classification axis**.
> Where UAT_DISCIPLINE governs *which class of UAT applies*, this
> canonical governs *what the PWF verdict's followup obligation actually
> says*. The two compose multiplicatively per
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) §3.

## 1. Why this canonical exists

`PASS-WITH-FOLLOWUP` is the most-used closure verdict across the I86
cluster (≥ 60% of closure UATs across Waves Q/R landed PWF). It is also
the most-abused: in the inter-wave regression sweeps for Wave Q and
Wave R, the recurring failure mode was *"PWF verdict carried no
structural rationale; reader cannot tell whether the followup is a
2-week monitoring obligation or a 6-month deferred-work tracker."*
Without structural rationale, PWF degrades into a deferral anti-pattern
— *"PASS because we said so, FOLLOWUP because we couldn't be bothered
to say what we mean."*

Operator framing at Wave R+1 Commit 1 ratification (2026-05-24):
*"PASS-WITH-FOLLOWUP can become invisible debt very fast if we don't
discipline it. Mint a specialty so the next chat reads the same way."*

The 12th specialty exists to convert PWF from a vague closure shape
into a **structured commitment** — every PWF verdict carries a
`verdict_followup_rationale` block whose 5 fields (followup_class +
closure_target + owner + tracker_path + closure_decision_id_target +
notes) describe what was deferred, why, to when, and by whom.

## 2. Scope — what counts as a PWF artifact

A closure verdict is in scope for this canonical when **all** of:

- The artifact is a closure UAT report under
  `docs/wip/planning/<NN>-<slug>/reports/uat-*.md` per
  [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §3.
- The report's `verdict:` frontmatter is `PASS-WITH-FOLLOWUP`.
- The report's `last_review:` is ≥ 2026-05-19 (forward-only watershed
  per [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §"Migration posture").

Out of scope: PASS / FAIL / PENDING-OPERATOR-WALK / FORWARD-CHARTERED
verdicts (the specialty no-ops on these). Pre-watershed reports get
INFO-only findings per §"Migration posture" below.

Forward scope (when this canonical promotes from `charter` → `active`):
the discipline may extend to non-UAT artifacts that carry PWF-shaped
verdicts (phase reports, ratification artifacts, pre-pause records).
Forward-charter pointer; out of scope for this mint.

## 3. The 5-class followup taxonomy (binding enum)

Every `verdict_followup_rationale` MUST declare a `followup_class`
matching exactly one of the 5 classes below. The enum is closed —
escalations beyond the 5 classes require an operator-explicit decision
row amending this section.

### 3.1 `monitoring-obligation`

The UAT verdict is PASS **in substance** — the closure criteria
clearly cleared. The FOLLOWUP is the cadence to keep observing a
multi-wave field-test window OR a post-promotion observation rhythm
that doesn't change the substance of what shipped.

**Required fields**: `closure_target` (e.g., "Wave U close" or an ISO
date), `owner`. **Optional**: `tracker_path`,
`closure_decision_id_target`.

**Canonical worked example**: Wave R+1 P1 UAT promoting
[`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) to `active` carries a 3-wave
field-test window per §10 promotion log; observation entries land at
Wave S close, Wave T close, Wave U close. The verdict is PASS — the
charter clearly clears the 7-criterion bar — and the FOLLOWUP is the
3-wave monitoring discipline.

### 3.2 `deferred-work-with-tracker`

The UAT verdict carries forward **concrete work** that was scoped-out
of the current wave but is named + tracked. The closure trail
requires a tracker file under
`docs/wip/planning/_trackers/<slug>-tracker.md` OR an OPS_REGISTER row.

**Required fields**: `closure_target`, `tracker_path`, `owner`.
**Optional**: `closure_decision_id_target`.

**Canonical worked example**: B-2c closure UAT carries live MCP
spot-checks for the FX cache + DLQ replay path deferred to a future
wave with a named tracker; the operator authenticates the relevant
vendor MCPs when ready, then the tracker promotes to OPS-row close-out.

### 3.3 `convention-class-followup`

The UAT verdict carries forward a **doctrinal / convention-class**
refinement that surfaced during the wave but is not blocking. Often
shapes a successor wave's authoring; sometimes ratifies into a
follow-up decision row.

**Required fields**: `closure_target` (the wave or decision where the
convention promotes), `owner`. **Optional**:
`closure_decision_id_target` (often known at PWF authoring time when
the convention is well-formed).

**Canonical worked example**: Wave R surfacing *"PWF discipline needs
its own specialty"* itself — which became this very canonical's birth
artifact at Wave R+1 Commit 3-a per D-IH-86-CX.

### 3.4 `mechanical-recovery-with-eta`

The UAT verdict carries forward a known **mechanical fix** that the
agent has identified but has not landed in the wave's commit window
(e.g., validator threshold tweak, sync emit regeneration, mirror
reseed, ramp INFO→FAIL flip pending one more clean wave).

**Required fields**: `closure_target` (ISO date or wave), `owner`,
ETA-shaped `notes`.

**Canonical worked example**: A release-gate INFO advisory that should
flip to FAIL after a paired commit lands at Wave T close; PWF verdict
records the planned flip with a wave-target.

### 3.5 `escalation-to-blocker-tracker`

The UAT verdict **could not clear** because of external dependency or
operator-judgement gap; tracker file under
`docs/wip/planning/_blockers/<slug>-tracker.md` records the
escalation per [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc).

**Required fields**: `closure_target`, `tracker_path` (under
`_blockers/`), `owner`.

**Canonical worked example**: An initiative whose closure depends on
external counsel sign-off; the UAT verdict closes the substance the
agent could land but escalates the operator-judgement gate to a
blocker-tracker.

## 4. compose_PWF rule + INFO→FAIL severity ramp

The specialty materialises the compose rule:

```text
compose_PWF(uat_class, verdict, frontmatter) -> structural finding set

  where:
    if verdict != "PASS-WITH-FOLLOWUP": no-op
    else:
      rationale = parse_followup_rationale(frontmatter.get("verdict_followup_rationale"))
      if rationale is None or rationale.followup_class is None:
        emit PWF-FM-01-CLASS-MISSING  (FAIL forward-only; INFO pre-watershed)
      if rationale.followup_class not in VALID_FOLLOWUP_CLASSES:
        emit PWF-FM-02-CLASS-UNKNOWN  (FAIL forward-only)
      if rationale.followup_class in REQUIRED_CLOSURE_TARGET_CLASSES and not rationale.closure_target:
        emit PWF-FM-03-CLOSURE-TARGET-MISSING  (FAIL forward-only)
      if rationale.followup_class in REQUIRED_TRACKER_PATH_CLASSES and not rationale.tracker_path:
        emit PWF-FM-04-TRACKER-PATH-MISSING  (FAIL forward-only)
      if rationale.tracker_path and not Path(rationale.tracker_path).exists():
        emit PWF-FM-04-TRACKER-PATH-INVALID  (FAIL forward-only)
      if rationale.owner is None or rationale.owner.strip() == "":
        emit PWF-FM-05-OWNER-MISSING  (WARN always)
```

| Code | Severity (forward) | Severity (pre-watershed) | Trigger |
|:---|:---|:---|:---|
| `PWF-FM-01-CLASS-MISSING` | FAIL | INFO | rationale missing OR class field empty/null |
| `PWF-FM-02-CLASS-UNKNOWN` | FAIL | INFO | class value not in 5-class enum |
| `PWF-FM-03-CLOSURE-TARGET-MISSING` | FAIL | INFO | class requires closure_target but absent |
| `PWF-FM-04-TRACKER-PATH-MISSING` | FAIL | INFO | class requires tracker_path but absent |
| `PWF-FM-04-TRACKER-PATH-INVALID` | FAIL | INFO | tracker_path cited but file does not exist on disk |
| `PWF-FM-05-OWNER-MISSING` | WARN | WARN | owner field empty (always advisory, never blocking) |

### 4.1 Watershed + ramp posture

Per D-IH-86-CX: the FAIL ramp activates on the **2026-05-19 watershed**
(the same date [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) anchored its
forward-only enforcement per D-IH-86-AS). Reports with `last_review`
before that date get INFO findings only — they are the migration-grace
window. The validator detects forward-only vs pre-watershed via the
report's `last_review:` frontmatter.

The validator stays at INFO ramp (release-gate advisory) until **Wave T
close** at the earliest — and only promotes to FAIL when:

1. The Wave R UAT amendment closes (Commit 3-c per the parent
   workspace plan), supplying the structural rationale that
   PWF-FM-01-CLASS-MISSING currently catches.
2. Three consecutive wave-close sweeps emit zero forward-only FAIL
   findings.
3. Operator-explicit decision row (`D-IH-86-CX-V2` or successor)
   records the promotion.

This mirrors the same INFO→FAIL ramp pattern that
[`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md) and
[`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md)
adopted — three-clean-waves + operator-explicit ratification is the
canonical promotion rhythm for new specialty validators.

## 5. Cadence

The default sweep cadence is **single-report at UAT authoring time** +
**wave-close-sweep at every wave-close gate** per
[`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md)
DIM-06 (UAT report class completeness) — this canonical extends DIM-06
with the *content* dimension that DIM-06's classification axis can't
see.

Exceptions:

- **Chore-only single-commit waves**: exempt entirely.
- **Pre-watershed reports** (`last_review` < 2026-05-19): INFO-only;
  do not block.
- **Pre-commit self-test**: always-on, zero-cost Pydantic fixture
  validation only (`--self-test` mode of the validator) — the full
  sweep is event-triggered at wave-close and at UAT-authoring-time
  (not at every pre_commit).

## 6. Findings disposition per inline-ratify 5-option enum

Every WARN or FAIL finding from a PWF governance sweep MUST be
dispositioned via an inline `AskQuestion` gate per
[`akos-inline-ratification.mdc`](../../../../../../../.cursor/rules/akos-inline-ratification.mdc),
using the 5-option enum:

1. **deterministic-fix-now** — author the canonical rationale block in
   the same commit (default for PWF-FM-01/02/03 when the rationale is
   simply absent or malformed).
2. **manual-fix-now** — author the rationale + close the underlying
   tracker reference (default for PWF-FM-04 when the tracker needs to
   be minted alongside).
3. **defer-OPS** — record an OPS_REGISTER row to author the rationale
   in a future commit (only acceptable for non-forward-only / pre-
   watershed reports per migration-grace posture).
4. **accept-as-canon** — operator ratifies that the rationale shape
   was intentionally non-standard (appends contra-precedent + decision
   row; rare).
5. **escalate-to-blocker-tracker** — the rationale gap is itself
   blocked on external operator-judgement; mints
   `_blockers/pwf-rationale-<slug>-tracker.md` per
   [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc).

When findings exceed 10, split the gates into 2 `AskQuestion` batches
per [inline-ratify-craft](../../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md)
Principle 5 batching guidance.

## 7. Migration posture

Reports authored before 2026-05-19 are **not** retroactively required
to backfill structural rationale. The discipline is forward-only from
D-IH-86-CX (2026-05-25). Specifically:

- **Pre-watershed reports**: validator emits INFO findings only;
  closures never blocked.
- **Forward reports** (≥ 2026-05-19): structural rationale required;
  INFO at ramp / FAIL at promotion per §4.1.
- **Amended reports** (verdict_history v2+): when an amendment lands
  for a pre-watershed report, the amendment SHOULD opt into the
  structural shape; doing so is encouraged but not mandatory.

The first amended-with-structural-rationale report is the Wave R
closure UAT itself: amended in Commit 3-c per the parent workspace
plan, with `verdict_history` recording the v1 PWF-without-rationale
shape and v2 supplying the structural rationale per this canonical.
That amendment closes the PWF-FM-01-CLASS-MISSING finding the
validator currently catches.

## 8. Specialty mint contract (per RULE 5 of the cursor rule)

This canonical mint follows the same 15-surface contract that the
Wave M INTER_WAVE_REGRESSION + Wave N INDEX_INTEGRITY precedent
established for every new Quality Fabric specialty:

| # | Surface | Path |
|:--|:---|:---|
| 1 | Canonical doctrine | `People/canonicals/PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md` (this file) |
| 2 | Pydantic chassis | `akos/hlk_pwf_governance.py` |
| 3 | Validator | `scripts/validate_pwf_governance.py` |
| 4 | Runbook | `scripts/validate_pwf_governance.py` (validator IS runbook — check-class only) |
| 5 | Cursor rule | `.cursor/rules/akos-pwf-governance.mdc` |
| 6 | Skill | `.cursor/skills/pwf-governance-craft/SKILL.md` |
| 7 | Paired SOP | `People/canonicals/SOP-PEOPLE_PWF_GOVERNANCE_001.md` |
| 8 | Pattern registry row | `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` row `pattern_pwf_governance_discipline` |
| 9 | PRECEDENCE.md row | canonical + mirror rows for this doctrine |
| 10 | Quality Fabric §6 row | `HOLISTIKA_QUALITY_FABRIC.md` §6 specialty list extended |
| 11 | CHANGELOG.md entry | `[Unreleased]` entry citing D-IH-86-CX |
| 12 | process_list.csv row | `hol_peopl_dtp_pwf_governance_001` |
| 13 | `validate_hlk.py` umbrella | dispatcher row + count update |
| 14 | `verification-profiles.json` `pre_commit` step | `validate_pwf_governance_self_test` |
| 15 | `scripts/release-gate.py` advisory wiring | `run_pwf_governance_validation` |

All 15 surfaces land in the same atomic commit (Commit 3-a per the
parent workspace plan) — the specialty is operationally complete
before being advertised.

## 9. Cross-references

- Parent meta-canonical: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) — the doctrine this specialty extends.
- Content-axis sibling: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) — the classification axis; PWF governance is the content axis. Compose multiplicatively.
- Cadence-axis sibling: [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md) — DIM-06 covers UAT class completeness; this canonical extends with content completeness.
- Index-axis sibling: [`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md) — 11th specialty; this is the 12th.
- Paired cursor rule: [`.cursor/rules/akos-pwf-governance.mdc`](../../../../../../../.cursor/rules/akos-pwf-governance.mdc) (the mechanical drift-gate companion).
- Paired skill: [`.cursor/skills/pwf-governance-craft/SKILL.md`](../../../../../../../.cursor/skills/pwf-governance-craft/SKILL.md) (the *how* layer).
- Paired SOP: [`SOP-PEOPLE_PWF_GOVERNANCE_001.md`](SOP-PEOPLE_PWF_GOVERNANCE_001.md) — AC-HUMAN + AC-AUTOMATION acceptance criteria.
- Disposition rule: [`.cursor/rules/akos-inline-ratification.mdc`](../../../../../../../.cursor/rules/akos-inline-ratification.mdc) — 5-option enum for findings disposition.
- Escalation rule: [`.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) — `escalate-to-blocker-tracker` class shape.
- Pydantic SSOT: [`akos/hlk_pwf_governance.py`](../../../../../../../akos/hlk_pwf_governance.py).
- Validator: [`scripts/validate_pwf_governance.py`](../../../../../../../scripts/validate_pwf_governance.py).
- Tests: [`tests/test_validate_pwf_governance.py`](../../../../../../../tests/test_validate_pwf_governance.py).

## 10. Decision lineage

- **D-IH-86-CW** (Wave R+1 Commit 1; 2026-05-24): UAT_DISCIPLINE
  charter → active promotion + the Wave R UAT amendment that exposed
  PWF-without-rationale as a recurring failure mode worth its own
  specialty mint.
- **D-IH-86-CX** (Wave R+1 Commit 3-a; 2026-05-25): this canonical's
  mint; codifies the 5-class followup taxonomy + structural rationale
  shape + INFO→FAIL ramp + 15-surface specialty contract.

### 10.1 Field-test window

The 12th specialty enters a 3-wave field-test window per
`field_test_window` frontmatter (forward-charter pointer; lands in
`UAT_DISCIPLINE.md`-style §10 promotion log once this canonical
promotes from `charter` → `active` after Wave T close at the earliest):

- FTW opens: 2026-05-25 (Wave R+1 close).
- FTW observation wave 1: Wave S close.
- FTW observation wave 2: Wave T close.
- FTW observation wave 3: Wave U close.
- FTW closes: Wave U close — at which point this canonical promotes
  to `active`, the validator promotes from INFO → FAIL ramp, and the
  cursor rule's RULE 4 flips from "advisory" to "binding".
