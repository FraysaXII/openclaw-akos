---
name: PASS-WITH-FOLLOWUP Governance Craft
description: >-
  Use when authoring or amending a closure UAT report whose verdict is
  PASS-WITH-FOLLOWUP in this AKOS workspace. Codifies the craft for
  writing the verdict_followup_rationale block well — picking the right
  followup class, naming a falsifiable closure target, citing the right
  tracker, and surviving the FAIL ramp. Triggers on any phrase like
  PWF rationale, PASS-WITH-FOLLOWUP, verdict_followup_rationale,
  followup_class, closure_target, PWF-FM-01, PWF-FM-04, monitoring
  obligation, deferred work with tracker, convention-class followup,
  mechanical recovery, escalation to blocker tracker, or after
  validate_pwf_governance.py emits a finding. Pairs with
  .cursor/rules/akos-pwf-governance.mdc (the WHEN); this skill is the
  HOW.
---

# PASS-WITH-FOLLOWUP Governance Craft

## Why this skill exists

The cursor rule `akos-pwf-governance.mdc` and the canonical
`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md` tell you **when** the
PWF rationale block is required and **what** the 5 followup classes
are. This skill tells you **how** to author the block well, how to
pick the right class without forcing a square peg into a round hole,
how to disposition validator findings without creating governance
debt, and how to recognise the most common authoring anti-patterns.

Read this skill before writing the first `verdict_followup_rationale`
block in a session, OR before dispositioning any `PWF-FM-*` finding
the validator surfaces.

## Principle 1 — PASS-WITH-FOLLOWUP is not a softer PASS

The most common authoring failure is treating PWF as "PASS that we
felt slightly uneasy about". It is not. It is a **load-bearing
verdict** that says: *this closure crosses the line, AND we owe
ourselves named, dated followup work that we are tracking.*

Before writing PWF, ask:

- **Could this be PASS?** (Is the followup actually optional or
  cosmetic? If yes → PASS, no rationale needed.)
- **Could this be FAIL?** (Does the followup block downstream work?
  If yes → FAIL, do not paper over.)
- **Could this be PENDING-OPERATOR-WALK?** (Is the gap waiting on
  operator input that hasn't arrived? If yes → PENDING, not PWF.)

PWF is the residue when (a) the closure substantively cleared and
(b) followup is real but not blocking. Use it sparingly and
honestly.

## Principle 2 — The 5 followup classes are NOT interchangeable

Each class encodes a different operational expectation. Mis-classifying
trains future readers (and validators) to ignore the rationale field.

| Class | When to use | Worked example |
|:---|:---|:---|
| `monitoring-obligation` | The work IS done; you owe yourself observation cadence to confirm it stays done. | "FX cache cron registered; followup = monitor 3 consecutive runs for staleness." |
| `deferred-work-with-tracker` | Concrete work was scoped-out of this closure with a successor target. **Tracker file MANDATORY.** | "B-2c shipped pipeline; per-product cost-allocation rules deferred to OPS-81-23 tracker." |
| `convention-class-followup` | Refinement to doctrine / conventions surfaced during the closure; non-blocking; informs future versions. | "UAT bar landed; observed Wave R amendment surfaces FTW-01 → next-cycle convention refinement." |
| `mechanical-recovery-with-eta` | A known reversible regression is in flight with a fix coming inside a bounded window. | "Vercel deploy recovered at hotfix sha 7a3b9c; followup = monitor 24h then mark cleared." |
| `escalation-to-blocker-tracker` | Closure clearance is real but downstream work hinges on operator judgement or external dep. **Blocker tracker MANDATORY.** | "Bundle B-2 shipped; advisory R7 pending operator novel framing → tracker `_blockers/r7-advisory-tracker.md`." |

If you cannot fit your followup into one of these, the verdict is
probably wrong. Re-read Principle 1.

## Principle 3 — Closure targets must be falsifiable

`closure_target` is the load-bearing field. A vague closure target
trains future agents to ignore the rationale.

Bad:

```yaml
closure_target: when we have time
closure_target: next quarter
closure_target: TBD
```

Good:

```yaml
closure_target: Wave T close
closure_target: 2026-06-30
closure_target: OPS-86-23 closed
closure_target: D-IH-86-CY ratified
closure_target: FTW-PWF-01 closes (3 wave-close observations)
```

Date-shaped, OPS-shaped, Decision-shaped, Wave-shaped, FTW-shaped —
any of these are falsifiable. "When we have time" is not.

## Principle 4 — Tracker paths must exist or be co-minted

For `deferred-work-with-tracker` + `escalation-to-blocker-tracker`,
the `tracker_path` field is REQUIRED. The validator's
`PWF-FM-04-TRACKER-PATH-INVALID` finding catches dangling pointers
(paths that don't exist + paths that don't follow the
`_trackers/` or `_blockers/` convention).

Two patterns work:

1. **Mint the tracker first** (e.g., as part of the disposition sweep
   that generated the followup), then cite its path in the rationale.
2. **Co-mint the tracker in the same commit** as the UAT report.

NEVER cite a tracker path you intend to author "later" — that is
PWF-FM-04 by construction, and the validator catches it.

## Principle 5 — Owner must resolve to a real role

The `owner` field carries an FK-style obligation: the value should
resolve to a `role_owner` in `baseline_organisation.csv`, OR be an
AIC-prefixed role (`AIC:PMO`, `AIC:SystemOwner`) per the People DoD
discipline (`akos-people-discipline-of-disciplines.mdc`).

`owner: agent` is **always wrong** — agents do not own followups; they
execute under role-class supervision per `D-IH-72-S`. Use
`AIC:<role>` instead.

## Principle 6 — Disposition validator findings via inline-ratify

When `validate_pwf_governance.py --report <path>` emits findings the
agent cannot deterministically fix in the same session (e.g., a
malformed tracker_path where the operator must choose between minting
the tracker or downgrading to convention-class), surface as an
`AskQuestion` per `akos-inline-ratification.mdc` using the 5-option
enum from the canonical §6:

```text
AskQuestion: PWF-FM-04-TRACKER-PATH-INVALID on Wave R UAT —
recommended deterministic-fix-now (mint
docs/wip/planning/_trackers/wave-r-followup-tracker.md +
update tracker_path). Alternatives:
  - manual-fix-now (operator names different tracker path)
  - defer-OPS (pre-watershed; INFO-only)
  - accept-as-canon (operator ratifies tracker-less variant + appends
    contra-precedent decision)
  - escalate-to-blocker-tracker (rationale gap blocked on operator
    novel framing)
```

NEVER silently fill the field with a plausible-looking path the
operator never ratified.

## Principle 7 — Compose multiplicatively with UAT_DISCIPLINE

PWF governance is the **content axis**; UAT_DISCIPLINE is the
**classification axis**. A closure UAT clears governance only when
**both** validators pass. Run both at authoring time:

```powershell
py scripts/validate_uat_report.py --report <path> --strict --strict-freshness
py scripts/validate_pwf_governance.py --report <path> --strict
```

If only one passes, the closure is **not** governance-ready. Do not
ship the commit until both clear.

## Worked example — full rationale block for a deferred-work case

```yaml
verdict: PASS-WITH-FOLLOWUP
verdict_followup_rationale:
  followup_class: deferred-work-with-tracker
  closure_target: OPS-86-23 closed
  owner: AIC:PMO
  tracker_path: docs/wip/planning/_trackers/dim-10-deploy-state-backfill-tracker.md
  closure_decision_id_target: D-IH-86-CY
  notes: >-
    OPS-86-23 (DIM-10 deploy state backfill) is in flight; this Wave R
    closure does NOT block on its completion. Tracker carries per-row
    backfill state for I68/I71/I72/I73 sibling-repo deploy_id +
    deploy_state tokens; resolves Wave T at the earliest.
```

This block satisfies every PWF-FM-* check + reads cleanly to a future
J-OP / J-AIC auditor at 0 cost of context.

## Worked example — full rationale block for a monitoring-obligation case

```yaml
verdict: PASS-WITH-FOLLOWUP
verdict_followup_rationale:
  followup_class: monitoring-obligation
  closure_target: FTW-PWF-01 closes (3 wave-close observations)
  owner: AIC:SystemOwner
  notes: >-
    FX rate cache cron registered + first run succeeded. Followup is
    pure observation — monitor 3 consecutive daily 15:30 UTC runs for
    staleness; if all clean, FTW closes and verdict promotes to PASS
    on the next regression sweep.
```

Note: `tracker_path` omitted (not required for monitoring-obligation).
`closure_decision_id_target` omitted (no decision will close the FTW;
the FTW closing IS the closure signal).

## Anti-patterns (don't do these)

- **PWF as soft-PASS** — see Principle 1.
- **Class-mismatch** — using `convention-class-followup` for what is
  actually `deferred-work-with-tracker` (the latter REQUIRES a tracker;
  using the former dodges the obligation).
- **Vague closure targets** — see Principle 3.
- **Phantom trackers** — see Principle 4.
- **`owner: agent`** — see Principle 5.
- **Silent finding auto-fix** — see Principle 6.
- **Skipping the dual-validator run** — see Principle 7.

## Pre-flight checklist (walk mentally before posting the UAT commit)

1. Could this be PASS / FAIL / PENDING instead? (Principle 1)
2. Which of the 5 classes fits? (Principle 2)
3. Is `closure_target` falsifiable? (Principle 3)
4. If class requires tracker, does the path exist? (Principle 4)
5. Does `owner` resolve to a real role? (Principle 5)
6. Did `validate_pwf_governance.py --report <path> --strict` exit 0?
7. Did `validate_uat_report.py --report <path> --strict --strict-freshness` exit 0?

All 7 = green → safe to commit. Any red → stop and disposition.

## Cross-references

- Parent canonical: [`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md).
- Cursor rule: [`akos-pwf-governance.mdc`](../rules/akos-pwf-governance.mdc) — the WHEN.
- Paired SOP: [`SOP-PEOPLE_PWF_GOVERNANCE_001.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_PWF_GOVERNANCE_001.md).
- Content-axis sibling skill: [`uat-discipline-craft`](../skills/uat-discipline-craft/SKILL.md) — classification axis.
- Findings disposition skill: [`inline-ratify-craft`](../skills/inline-ratify-craft/SKILL.md).
- Validator: [`scripts/validate_pwf_governance.py`](../../scripts/validate_pwf_governance.py).
- Pydantic SSOT: [`akos/hlk_pwf_governance.py`](../../akos/hlk_pwf_governance.py).
