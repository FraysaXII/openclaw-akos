---
language: en
initiative: 55-brand-ops-continuous-loop
report_kind: phase-report
phase: P7
status: completed
date: 2026-05-03
authority: I55 P7 master-roadmap (G-55-loop-1)
---

# I55 P7 — Material-change threshold POLICY (G-55-loop-1)

## Scope

Per the I55 master-roadmap, this phase wires the threshold POLICY that the I55 P6 tooling depends on. Without this row in `POLICY_REGISTER.csv`, `scripts/propose_advisor_update.py` falls back to `--use-defaults` (CI-friendly) but cannot resolve a real operator-tuned threshold. P7 makes the operator-tunable surface canonical.

## Deliverables

### 1. New `policy_class` enum value: `update_threshold`

Added to `akos/hlk_policy_register_csv.py::VALID_POLICY_CLASSES`. Mirrors the existing pattern of `cost_ceiling` (I50 P2), `judge_threshold` (I47 P12), and `flake_threshold` (I51 P4) — each is a runtime-envelope POLICY where `policy_text` encodes operator-tuned thresholds as space/comma/semicolon-separated `key=value` tokens.

### 2. New POLICY row: `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1`

Appended to `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv`:

| Field | Value |
|:------|:------|
| `policy_id` | `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` |
| `policy_class` | `update_threshold` |
| `applies_to_schema` | `*` |
| `applies_to_table` | `*` |
| `policy_text` | `min_changed_scenarios=3 min_judge_axis_movement_pp=2 min_register_rows_added=1 min_files_changed=2` (+ doctrine prose; D-IH-55-D defaults) |
| `cadence` | `continuous` |
| `owner_role` | `Brand Manager` |
| `last_review` | `2026-05-03` |
| `next_review` | `2026-08-03` |
| `topic_ids` | `topic_policy_register` |
| `notes` | I55 P7 + G-55-loop-1 + D-IH-55-D rationale |

### 3. New test row: `tests/test_policy_register.py::test_seed_includes_i55_advisor_update_threshold`

Asserts:

- `update_threshold` is in `VALID_POLICY_CLASSES`.
- At least one POLICY row uses the new class.
- The advisor row exists with the expected `policy_id`.
- The four well-known threshold tokens (`min_changed_scenarios=`, `min_judge_axis_movement_pp=`, `min_register_rows_added=`, `min_files_changed=`) are present in `policy_text`.
- The I55 P6 parser (`propose_advisor_update._parse_policy_text`) extracts all four keys as numeric values.

This test locks in the contract between the POLICY row and the script — if either is edited in isolation, the test fails fast.

## Verification

| Gate | Command | Result |
|:-----|:--------|:------:|
| Policy register tests | `py -m pytest tests/test_policy_register.py -v` | **16 passed** (incl. new `test_seed_includes_i55_advisor_update_threshold`) |
| HLK validator | `py scripts/validate_hlk.py` | **PASS** (POLICY_REGISTER ok; new row resolves owner_role + topic_ids) |
| End-to-end POLICY lookup | `py scripts/propose_advisor_update.py --diff diff.json --dry-run` (no `--use-defaults`) | OK — reads `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` from the CSV; thresholds match the `policy_text` token values |
| I55 P6 unit tests | `py -m pytest tests/test_regression_artifact_diff.py tests/test_propose_advisor_update.py -v` | **34 passed** (regression — no break vs P6) |

## Decisions reaffirmed

- **D-IH-55-D conservative defaults** — encoded both in code (`DEFAULT_THRESHOLDS`) and in the POLICY row. The two stay in sync deliberately: code defaults serve the `--use-defaults` CI path; POLICY row serves the operator-tunable production path.
- **Owner = Brand Manager** — the threshold governs *when* an advisor message is proposed, which is brand/communications territory. Business Controller co-owns at the loop level (cost discipline of regression cycles), but the canonical owner of the threshold itself is Brand.
- **`update_threshold` as a separate enum value, not a `cost_ceiling` extension** — distinguishes "how much spend before halting" (I50 P2) from "how much change before proposing" (I55 P7). They are different cost surfaces with different units (USD/run vs. count of changed rows). Mixing them violates D-IH-52-E (per-token vs per-GPU-hour separation generalisation).
- **`min_files_changed=2` included** despite not being in the original D-IH-55-D defaults — see I55 decision-log "P6 tooling shape decisions" entry. The tooling test suite locks both the field set and the parser; the POLICY row's `policy_text` is the canonical source.

## What does NOT ship in this phase

- The Wave-2 brand voice content that drives `register_rows_added` (P1, P2 — operator-pending; OPS-55-1).
- The I24 P1 SOP + process_list tranche that the threshold POLICY references in spirit (P3 — G-24-2 operator-pending; OPS-55-1).

These are unblocked from a *tooling* standpoint by P6 + P7, but remain operator-pending from a *content* standpoint.

## Cross-references

- [I55 master-roadmap](../master-roadmap.md)
- [I55 P6 phase report](p6-regression-loop-tooling-2026-05-03.md)
- `akos/hlk_policy_register_csv.py` — enum extended
- `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` — POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1 row added
- `tests/test_policy_register.py::test_seed_includes_i55_advisor_update_threshold` — contract lock
