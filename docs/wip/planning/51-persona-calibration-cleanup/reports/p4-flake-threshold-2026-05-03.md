---
language: en
initiative: 51-persona-calibration-cleanup
phase: P4
report_kind: phase-report
status: completed
date: 2026-05-03
authority: Founder
last_review: 2026-05-03
decision_executed: D-IH-51-B
gate_evaluated: G-51-2
closes: []
---

# I51 / P4 — D-IH-51-B flake-threshold POLICY + `--auto-from-flake-history`

## Outcome

D-IH-51-B default executed: **`POL-EVAL-FLAKE-THRESHOLD-V1`** added to
`POLICY_REGISTER.csv` with `policy_class=flake_threshold` and
`policy_text="min_consecutive_failures=3"`. `quarantine_scenario.py` extended
with **`--auto-from-flake-history <path.json>`** mode that reads the threshold
from the new POLICY row and bulk-quarantines scenarios whose
`consecutive_failures` count meets or exceeds it. Operator-judgement single-
row path (`--scenario-id` + `--reason`) preserved. **G-51-2 not fired** in this
phase: no live flake-history input was processed (the carrier was
infrastructure / governance, not a quarantine event), and the canonical CSV is
unchanged with respect to scenario lifecycle.

## Carrier closes / forwards

- **D-IH-51-B (flake-threshold formalization)** — executed default path:
  POLICY row + `policy_class=flake_threshold` extension to
  `VALID_POLICY_CLASSES`. Symmetric with I47/P12 `judge_threshold` and I50/P2
  `cost_ceiling` runtime-envelope POLICY rows.
- **C-51-C (persona-band-divergence policy)** — no pressure: post-I51/P3
  aggregate is 40.18/40.80/11.04/7.98 (well within global tolerance). No
  enforcement action needed in P4. Re-inspect at I51/P6 closure.

## Deliverables

### POLICY row

`docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` (29 → 30 rows):

```text
POL-EVAL-FLAKE-THRESHOLD-V1,flake_threshold,compliance,
  persona_scenario_registry_mirror,
  "Persona scenario auto-quarantine threshold:
   min_consecutive_failures=3. Scenarios with >=3 consecutive
   Tier-B FAILs across distinct runs are quarantine candidates per
   scripts/quarantine_scenario.py --auto-from-flake-history. ...",
  continuous, System Owner, 2026-05-03, 2026-08-03, topic_policy_register,
  "I51 P4 + D-IH-51-B. ..."
```

### Field contract

`akos/hlk_policy_register_csv.py`:

- `VALID_POLICY_CLASSES` extended with `"flake_threshold"`. The class joins
  `cost_ceiling` and `judge_threshold` as runtime-envelope POLICY rows that
  encode an enforcement number in `policy_text` (parsed by the consumer).

### Script extension

`scripts/quarantine_scenario.py`:

- New module-level constants: `FLAKE_QUARANTINE_NOTE_PREFIX="I51-FLAKE-QUARANTINE"`,
  `DEFAULT_FLAKE_THRESHOLD=3`, `FLAKE_POLICY_ID="POL-EVAL-FLAKE-THRESHOLD-V1"`,
  `_THRESHOLD_TOKEN_RE` (compiled regex matching `min_consecutive_failures=N`).
- New helpers:
  - `_read_flake_threshold(policy_csv)` returns `(threshold, source)` where
    source is `"policy"` if the POLICY row was found and parsed, else
    `"default"`. Header-drift on `POLICY_REGISTER.csv` triggers fall-through
    to default. Threshold values < 1 ignored (defensive).
  - `_load_flake_history(path)` reads + validates the operator-curated JSON.
    Schema: list of objects, each with `scenario_id` (non-empty string) and
    `consecutive_failures` (int ≥ 0). Other keys (e.g., `last_run_iso`)
    accepted but unused. UTF-8-sig safe (BOM tolerance).
  - `auto_quarantine_from_flake_history(csv_path, history, *, threshold,
    today, dry_run)` mutates rows with `consecutive_failures ≥ threshold`,
    sets `lifecycle_status=quarantined`, appends a dated note prefixed
    `I51-FLAKE-QUARANTINE` carrying the offending count and threshold +
    `POL-EVAL-FLAKE-THRESHOLD-V1` reference. Returns a summary dict with
    `threshold`, `candidates`, `quarantined`, `skipped_already_quarantined`,
    `not_found`, `no_change_below_threshold`.
- New CLI flag `--auto-from-flake-history <path.json>` mutually exclusive
  with `--scenario-id`. Single-row mode preserved (still requires
  `--reason` or `--release` when used).
- CLI prints a one-line summary plus per-scenario action lines; `not_found`
  entries surface on stderr.

### Tests

`tests/test_scenario_quarantine.py`: 9 new I51/P4 tests appended to the
existing 7 I49/P10 tests (16/16 PASS):

- `test_flake_threshold_resolves_from_policy`
- `test_flake_threshold_default_when_policy_missing`
- `test_flake_threshold_default_when_no_policy_file`
- `test_load_flake_history_validates_schema`
- `test_auto_quarantine_quarantines_above_threshold`
- `test_auto_quarantine_skips_already_quarantined`
- `test_auto_quarantine_dry_run_does_not_write`
- `test_auto_quarantine_reports_unknown_scenarios`
- `test_canonical_policy_register_has_flake_threshold_row`

## Verification

```text
$ py -m pytest tests/test_scenario_quarantine.py -v
16 passed in 0.30s

$ py scripts/check-drift.py
  No drift detected. Runtime matches repo state.

$ py scripts/sync_compliance_mirrors_from_csv.py --policy-register-only --count-only
source_git_sha=051a091...
policy_register_rows=30   # (was 29; +1 flake_threshold row)

$ py scripts/validate_hlk.py
  ... POLICY_REGISTER: PASS
  ... OVERALL: PASS

$ py scripts/quarantine_scenario.py \
    --auto-from-flake-history /tmp/i51-p4-flake.json \
    --dry-run
AUTO-QUARANTINE (dry-run): threshold=3 (policy); history_rows=4;
  candidates=3; quarantined=2; skipped_already_quarantined=0;
  not_found=1; below_threshold=1
  -> quarantined: SCN-OP-001-V1
  -> quarantined: SCN-OP-003-V1
  ?  not in registry: SCN-NONEXISTENT-V1
```

## Tier-B / governance impact

- **POLICY_REGISTER edit (canonical):** +1 row. Operator approval is on the
  plan-level greenlight (D-IH-51-B default explicitly ratified at
  greenlight 2026-05-03; the row is symmetric with the I47/P12 +
  I50/P2 runtime-envelope rows that received the same approval shape).
- **Mirror reseed cadence (D-IH-51-D)** applies to the
  `policy_register_mirror`. To apply:
  `py scripts/sync_compliance_mirrors_from_csv.py --policy-register-only
   --output ...` then operator review + `service_role` apply.
- **No PERSONA_SCENARIO_REGISTRY mutation** in this phase. The bulk
  quarantine path is wired but **not exercised** (no live flake-history
  data fed in). Carrier closes governance / infrastructure side; future
  Tier-B regression cycles can feed history into `--auto-from-flake-history`
  on demand.
- **No DDL changes.** `compliance.policy_register_mirror` already accepts
  arbitrary `policy_class` values as TEXT (validation is operator-side
  via `VALID_POLICY_CLASSES`).

## G-51-2 status

The plan defines G-51-2 as a **conditional** gate that fires when bulk
quarantine actually mutates lifecycle. **Not fired** here: the bulk path
exists and is tested, but no live flake-history was processed. When an
operator runs `--auto-from-flake-history` against a live CI artifact and
the script reports `quarantined > 0`, that operator action is the
G-51-2 fire — it's a runtime gate, not a phase gate.

## Closes

- (none — D-IH-51-B execution; carrier formalized, not yet exercised
  against live flake data.)

## Carriers state

- **C-51-A** (USER_GUIDE.md doc surface for `target_difficulty_band`) —
  forwards to I51/P6 closure.
- **C-51-B** — closed at I51/P3.
- **C-51-C** — no current pressure; re-inspect at I51/P6 closure.

## Operator next step

For Mirror reseed (per D-IH-51-D cadence):

```text
py scripts/sync_compliance_mirrors_from_csv.py --policy-register-only \
   --output /tmp/i51-p4-policy-mirror.sql
# Review + apply via mcp_supabase_apply_migration or psql / service_role.
```

For live flake auto-quarantine (when operator has flake-history JSON):

```text
py scripts/quarantine_scenario.py \
   --auto-from-flake-history <path.json> \
   --dry-run            # always check first
py scripts/quarantine_scenario.py \
   --auto-from-flake-history <path.json>
# Mirror reseed afterwards (D-IH-51-D cadence).
```
