---
language: en
initiative: 55-brand-ops-continuous-loop
report_kind: phase-report
phase: P6
status: completed
date: 2026-05-03
authority: I55 P6 master-roadmap
---

# I55 P6 — Regression-loop tooling (the new heart of I55)

## Scope

Per the I55 master-roadmap (and the operator reframing of 2026-05-03), this phase ships the operator-content-independent tooling that makes the regression-to-advisor loop work. The brand-voice / register-fill / SOP / ALTER phases (P1–P5) remain operator-pending and are forwarded as `OPS-55-1`.

## Deliverables

### 1. `scripts/regression_artifact_diff.py` (new)

Compares a *current* dossier `manifest.json` against the *last-sent* baseline `manifest.json` and emits a structured diff record across five families of signal:

| Family | Source | Fields tracked |
|:-------|:-------|:---------------|
| `cite_counts` | Section 02 | `total_scenarios`, `total_personas`, `total_topics`, `total_skills`, `total_policies` |
| `scenario_deltas` | Section 04 | `total_scenarios`, `personas_outside_tolerance_count`, `quarantined_scenarios_count` |
| `judge_axes` | Sections 03 + 04 (merged; 04 wins) | `judge_score_*_mean` × 3 axes; `judge_axis_fail_*` × 3; `judge_worst_axis_fail_count` |
| `endpoint_cost` | Section 08 | `madeira_endpoint_count`, `madeira_endpoint_worst_status`, `madeira_cost_ceiling_status`, `madeira_cost_total_usd`, `cost_ceiling_breaches_count` |
| `brand_voice` | Section 01 | `light_conversational`, `light_operator`, `light_surface`, `madeira_ship_go` |

Plus per-file sha256 status (`unchanged` / `changed` / `new` / `removed`).

First-cycle handling: if `--last-sent` is omitted or the file does not exist, every metric is reported as `new` and `is_first_cycle=True` is set in the record.

### 2. `scripts/propose_advisor_update.py` (new)

Reads the diff record + the `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` row from `POLICY_REGISTER.csv` (or `--use-defaults` for CI) and:

- Emits `proposal-advisor-send-YYYY-MM-DD.md` when any threshold tripped.
- Appends a `no` row to `loop-history.md` when no threshold tripped (D-IH-55-E both-signal-and-silence).
- `--force-proposal` overrides silence (R-55-5 mitigation: thresholds may be too tight).
- `--allow-first-cycle` emits a first-send proposal when no baseline exists.
- `--dry-run` computes the decision without writing files.

The script never inlines a real recipient email; only the GOI/POI `ref_id` (operator-supplied via `--recipient`) appears in the proposal markdown. R-55-2 mitigation: pre-commit grep-guard for SMTP-pattern catches accidental leaks.

### 3. `SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md` (new)

Located at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/`. Codifies the L1–L7 loop, the threshold POLICY semantics, and the per-fire G-24-3 IRREVERSIBLE doctrine. `status: review` (CSV-before-SOP per SOP-META: the `thi_mkt_dtp_NN` tranche row is operator-pending under G-24-2 / OPS-55-1 — the SOP can land in `review` because no new process_id is invented inside this SOP itself).

### 4. `regression_loop_smoke` verification profile (new)

Added to `config/verification-profiles.json` between `playwright_a11y_smoke` and `eval_harness_smoke`. Tier A only (no LLM cost; no SMTP). Runs the 34 unit tests covering:

- Diff record structure + field-status vocabulary (11 tests).
- Threshold parsing from `policy_text` (4 tests).
- `evaluate_thresholds` across the four metric families (8 tests).
- Proposal markdown rendering (3 tests).
- Loop-history append (2 tests).
- `main()` integration including dry-run, force, first-cycle (6 tests).

## Verification

| Gate | Command | Result |
|:-----|:--------|:------:|
| Unit tests | `py -m pytest tests/test_regression_artifact_diff.py tests/test_propose_advisor_update.py -v` | **34 passed** |
| Profile parse | `py -m pytest tests/test_verification_profiles.py -v` | **5 passed** |
| Real-data smoke (diff) | `py scripts/regression_artifact_diff.py --current artifacts/dossier-i52-closure/manifest.json --last-sent artifacts/dossier-i51-closure/manifest.json --out /tmp/smoke.json --quiet` | OK |
| Real-data smoke (propose) | `py scripts/propose_advisor_update.py --diff /tmp/smoke.json --use-defaults --dry-run` | `proposed=true` (`min_register_rows_added` + `min_files_changed` tripped — expected for I51→I52 closure delta) |

## Decisions reaffirmed

- **D-IH-55-D conservative defaults** — `min_changed_scenarios=3`, `min_judge_axis_movement_pp=2`, `min_register_rows_added=1`, `min_files_changed=2`. Encoded as `DEFAULT_THRESHOLDS` in `propose_advisor_update.py` and surfaced via `--use-defaults` for CI.
- **D-IH-55-E both-signal-and-silence** — `loop-history.md` is created on first run with header + first row; subsequent runs append. Both `proposed=YES` and `proposed=no` rows are recorded.
- **D-IH-55-B off-repo identity store** — proposal markdown carries only the GOI/POI `ref_id`. Recipient address never enters git. Pre-commit grep-guard already in place from I24 P0 doctrine.

## Operator-content-independent (ships in this cycle)

- Both new scripts: tooling only, no operator content.
- SOP: doctrine only, references existing CSV rows (no new process_id invented inside the SOP).
- Verification profile: tooling only.

## What does NOT ship in this cycle

- `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` POLICY row + new `update_threshold` policy_class enum value — **shipping next as I55 P7** in this same cycle.
- Wave-2 Section 2 / Section 3 fills (P1, P2) — operator-input gated; OPS-55-1.
- I24 P1 SOP finalization with process_list tranche (P3) — G-24-2 operator-pending; OPS-55-1.
- GOI_POI_REGISTER ALTER + Supabase mirror (P4) — G-24-1 operator-pending; OPS-55-1.
- `compose_adviser_message.py` finalization (P5) — depends on P1–P2 brand voice content; OPS-55-1.

## Cross-references

- [I55 master-roadmap](../master-roadmap.md)
- [`SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md)
- `scripts/regression_artifact_diff.py`
- `scripts/propose_advisor_update.py`
- `tests/test_regression_artifact_diff.py`
- `tests/test_propose_advisor_update.py`
- `config/verification-profiles.json` → `regression_loop_smoke`
