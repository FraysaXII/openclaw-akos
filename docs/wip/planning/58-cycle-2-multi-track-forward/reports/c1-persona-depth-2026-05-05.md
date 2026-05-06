---
language: en
status: deferred
initiative: 58-cycle-2-multi-track-forward
phase: C.1
report_kind: deferral
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-05
---

# I58 C.1 — Persona calibration depth (1/16 → ≥4/16) — DEFERRED to OPS-58-1

**Date**: 2026-05-05
**Phase**: I58 C.1 (KM polish track)
**Phase ref**: cycle_2_multi-track_forward_(i58)_769da1a3.plan.md → todo `c1_persona_depth`
**Verdict**: **DEFERRED — no fire required at I58 closure**

---

## 1. Decision

**C.1 is deferred** to the operator-funded OPS-58-1 window. The I58 plan explicitly authorises this:

> "C.1 Raise persona calibration coverage from 1/16 → ≥4/16. Defer entirely if A.1 alignment already ≥80% on ≥2/3 axes." — I58 master roadmap §"Phase summary"

> "If the live cycle hasn't fired by closure time, it re-forwards as OPS-58-1; engineering closure is not blocked on operator funding." — I58 master roadmap §"Posture (decided)"

## 2. Rationale

C.1 is a **conditional follow-up** to A.1 (multi-judge calibration burn). It only makes operational sense after A.1 produces real alignment numbers; running it in advance would burn dossier budget on persona depth that may not be needed (the cheapest outcome — A.1 alignment ≥80% on ≥2/3 axes — skips C.1 entirely).

Because A.1 forwarded as OPS-58-1 (operator-funded; agent context cannot run live API calls — see [`a1-a4-live-cycle-forward-2026-05-05.md`](a1-a4-live-cycle-forward-2026-05-05.md)), C.1 has no input data and must defer with it.

## 3. Conditions for fire

C.1 fires only if **all three** are true after OPS-58-1 completes:

1. A.1 ran successfully and produced a calibration artifact under `artifacts/judge-calibration/`.
2. Alignment was **<80% on ≥2/3 axes** (i.e., the cheapest outcome did **not** materialise).
3. Operator approves the additional budget (~$10 incremental for 3 more persona burns).

If any of those is false, C.1 stays in this deferred state and folds into the I58 closure as "deferred follow-up — no action required."

## 4. When OPS-58-1 fires

When the operator funds and runs OPS-58-1:

1. Re-read `artifacts/judge-calibration/<latest>.json` for axis-by-axis alignment percentages.
2. If the trigger condition (§3 #2) holds, run:

   ```powershell
   py scripts/judge_calibration_burn.py --n 50 --persona <next_persona_id> --target-pp 80
   py scripts/judge_calibration_burn.py --n 50 --persona <next_persona_id_2> --target-pp 80
   py scripts/judge_calibration_burn.py --n 50 --persona <next_persona_id_3> --target-pp 80
   ```

   to bring coverage from 1/16 to ≥4/16.
3. Capture all four artifacts under `artifacts/judge-calibration/` with JSON sidecars.
4. If alignment still <80% on any axis, draft `POL-EVAL-JUDGE-THRESHOLD-*` recalibration row in [`POLICY_REGISTER.csv`](../../../references/hlk/compliance/dimensions/POLICY_REGISTER.csv).
5. Update this report from `status: deferred` to `status: completed` (or to `closed` if no recalibration needed).

## 5. Engineering closure deliverables (this commit)

1. This deferral report.

That's it for C.1 at I58 closure time. No code changes; no canonical CSV touched; no test re-runs needed (C.1 is a budget-only burn, not an engineering deliverable).

## 6. Governance

- **Asset classification**: this report is a workspace planning artifact (reference-only).
- **Commit discipline**: this report folds into the **D.1 + D.2 + E.0** engineering-hygiene-and-closure commit batch (per the I58 plan's "Phase D is independent housekeeping" + Phase E is closure UAT). C.1 alone produces no scope-bearing change.
- **Brand-jargon audit**: not applicable — internal planning prose.

## 7. Roll-up

- **I58 todo**: `c1_persona_depth` → **completed (deferred)** per the I58 plan's explicit authorization.
- **Cycle progress**: P0, A.0-A.5 (OPS-58-1), B.1-B.4 (all four strategy initiatives closed engineering-side), C.1 (deferred to OPS-58-1) complete. Remaining: D.1 (archive I05/I20), D.2 (RunPod alias seam), E.0 (closure UAT).
- **Next action**: proceed to D.1 (archive I05/I20).

---

**Author**: Agent (Cursor / I58 C.1 step)
**Reviewer**: Operator (implicit, via I58 plan's deferral authorization)
**Status**: I58 C.1 DEFERRED to OPS-58-1; no closure blocker.
