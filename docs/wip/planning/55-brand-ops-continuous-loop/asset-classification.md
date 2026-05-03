---
language: en
status: active
initiative: 55-brand-ops-continuous-loop
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 55 — Asset classification

Per [`PRECEDENCE.md`](../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (edit here first)

- [`docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv`](../../references/hlk/compliance/dimensions/POLICY_REGISTER.csv) — adds `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` row at I55 P7; new `policy_class=update_threshold` enum value.
- *(Operator-pending, OPS-55-1):* `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md`, `BRAND_REGISTER_MATRIX.md`, `BRAND_DO_DONT.md` — Wave-2 Section 2 fill.
- *(Operator-pending, OPS-55-1):* `docs/references/hlk/compliance/process_list.csv` — tranche `thi_mkt_dtp_NN` "Communication methodology maintenance".
- *(Operator-pending, OPS-55-1):* `docs/references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv` — 3 new nullable columns.

## Mirrored / derived

- *(Operator-pending, OPS-55-1):* `compliance.goipoi_register_mirror` — ALTER for 3 new columns via Supabase MCP `apply_migration`.

## Reference-only (do not edit)

- [`docs/wip/planning/24-hlk-communication-methodology/`](../24-hlk-communication-methodology/) — I24 doctrine; I55 closes I24's *capability* once Wave-2 fills land.
- [`docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml`](../22a-i22-post-closure-followups/operator-answers-wave2.yaml) — operator-fill input; not edited by I55 directly (operator fills, then `wave2_backfill.py` reads).

## Code (no canonical-status edits)

- *(I55 P6 — ships this cycle):* `scripts/regression_artifact_diff.py` — new; structural diff between current dossier/cover-email artifact vs last-sent artifact.
- *(I55 P6 — ships this cycle):* `scripts/propose_advisor_update.py` — new; emits a send proposal when material change ≥ POLICY threshold.
- *(I55 P5 — operator-pending):* `scripts/compose_adviser_message.py` — finalize 4-layer composer.
- *(I55 P6 — ships this cycle):* extension of `scripts/validate_policy_register.py` to recognize `policy_class=update_threshold`.
- [`scripts/wave2_backfill.py`](../../../scripts/wave2_backfill.py) — already exists; not edited by I55.

## Tests (ships this cycle)

- *(I55 P6):* `tests/test_regression_artifact_diff.py` — material-change detector contract.
- *(I55 P6):* `tests/test_propose_advisor_update.py` — proposal-trigger semantics.
- *(I55 P7):* tests assert `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` row + `policy_class=update_threshold` enum value.

## Config (ships this cycle)

- [`config/verification-profiles.json`](../../../config/verification-profiles.json) — new `regression_loop_smoke` profile.

## Reports (governance + per-fire + closure)

- I55 P0-P8 phase reports.
- *(operator-driven, per fire):* `reports/uat-adviser-send-N-YYYY-MM-DD.md` — N increments per G-24-3 fire.
- *(continuous):* `reports/loop-history.md` — cumulative one-line-per-cycle log (D-IH-55-E).
- *(closure of I24 capability):* `reports/uat-i24-capability-closure-YYYY-MM-DD.md` — written when P1-P5 land (operator-pending).
- *(this cycle):* `reports/uat-i55-loop-tooling-closure-2026-05-03.md` — partial-capability closure (P6 + P7 + governance only).
