---
language: en
status: active
initiative: 51-persona-calibration-cleanup
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 51 — Decision log

Four decisions seeded with defaults per the cursor plan; operator-ratified at greenlight 2026-05-03.

## D-IH-51-A — Rebalance vs per-persona target band

**Decision (default):** **Per-persona `target_difficulty_band` column.** Add a new optional column to `PERSONA_SCENARIO_REGISTRY.csv` capturing each persona's target band (e.g., `40/40/10/10` baseline; or `30/40/20/10` for a persona where `hard` matters more). Calibrator computes drift against the persona's own target rather than the global default.

**Alternative considered:** Move scenarios across personas to rebalance the global distribution.

**Rationale:** Least disruptive to scenario authors (no scenario relocation; no cassette re-record cost; preserves provenance and historical PASS/FAIL trail). Some personas have inherent calibration profiles that diverge from the global default — formalizing that via a column is more honest than forcing artificial rebalancing.

**Reversibility:** Medium — column is optional with NULL default; can be removed if approach proves unhelpful. Existing persona rows fall through to the global D-IH-47-C 40/40/10/10 target.

**Operator answer (2026-05-03 plan iteration):** Per-persona target band.

---

## D-IH-51-B — Flake-threshold formalization

**Decision (default):** **Formalize as POLICY row.** Add `POL-EVAL-FLAKE-THRESHOLD-V1` to `POLICY_REGISTER.csv` with new `flake_threshold` `policy_class` extending `akos/hlk_policy_register_csv.py::VALID_POLICY_CLASSES`. Default text: `min_consecutive_failures=3` (3 consecutive Tier-B FAIL → auto-quarantine candidate).

**Alternative considered:** Operator-judgement path (no POLICY row; quarantine remains manual).

**Rationale:** Symmetry with I47 P12 `judge_threshold` and I50 P2 `cost_ceiling` runtime-envelope rows. Flake quarantine becomes auditable + queryable + tunable per quarterly review, not buried in tribal knowledge.

**Reversibility:** High — POLICY row can be deprecated; manual quarantine path stays available.

---

## D-IH-51-C — `--hard-fail-on-drift` placement

**Decision (default):** **`eval_tier_b_weekly` profile only.** Pre-commit stays warn-only to preserve operator agency (rapid iteration can transiently exceed ±5pp without indicating a real regression).

**Rationale:** Tier-B weekly is the right cadence for hard-fail drift detection — it's the operator-aware regression cycle, not the per-keystroke pre-commit cycle. Pre-commit warn-only matches the existing brand-voice-lint pattern (warn at pre-commit; hard-fail at release-gate).

**Reversibility:** High — flag is per-profile and per-invocation; can be moved to pre-commit later.

---

## D-IH-51-D — Mirror reseed cadence

**Decision (default):** **After every CSV tranche edit.** Documented in a follow-on or new SOP (probably `SOP-HLK_PERSONA_SCENARIO_MIRROR_001` if surface area justifies; otherwise a section under `SOP-META_PROCESS_MGMT_001`).

**Rationale:** PERSONA_SCENARIO_REGISTRY edits are infrequent (operator-gated per row) so the cadence is naturally bounded. Forcing mirror reseed after every tranche keeps the bidirectional contract tight and surfaces drift early.

**Reversibility:** High — cadence is operator-driven; can move to scheduled job later if frequency justifies it.

---

## Decisions made during execution

### 2026-05-03 — P5 D-IH-51-C executed; --hard-fail-on-drift wired to eval_tier_b_weekly only

I51/P5 lands the `calibration-drift-gate` job in
`.github/workflows/eval-tier-b.yml` (runs after the matrix `tier-b`
job, single invocation per workflow). The job invokes
`py scripts/calibrate_scenarios.py --hard-fail-on-drift` against the
per-persona `target_difficulty_band` values produced in P3, exits
non-zero on any persona outside ±5pp of its own band, and uploads the
resulting `calibration-baseline-*.{md,json}` as a 90-day-retention
artifact. The script already supported `--hard-fail-on-drift`
(I47/P10) so this phase is wiring + governance, not new code.

Pre-commit stays warn-only by design: there is no
`.pre-commit-config.yaml` calibration hook today and we are
**deliberately not adding one** — D-IH-51-C scope explicitly bounds
the hard-fail surface to the weekly Tier-B profile so operators can
iterate freely on `target_difficulty_band` without per-keystroke
gating.

Local dry-run verification:
`py scripts/calibrate_scenarios.py --hard-fail-on-drift --quiet` →
exit 0 (0 / 17 personas outside tolerance; matches P3 closure state).

Phase report: [`reports/p5-ci-tightening-2026-05-03.md`](reports/p5-ci-tightening-2026-05-03.md).

### 2026-05-03 — P4 D-IH-51-B executed; flake-threshold POLICY + bulk quarantine wired

I51/P4 lands the **`POL-EVAL-FLAKE-THRESHOLD-V1`** POLICY row
(policy_class=`flake_threshold`; default `min_consecutive_failures=3`)
plus the `quarantine_scenario.py --auto-from-flake-history` bulk mode.
POLICY_REGISTER: 29 → 30 rows. **G-51-2 is a runtime gate** (fires
on operator-driven bulk quarantine of live flake history); not fired
in this phase since no live flake-history was processed. Module-level
constants `FLAKE_QUARANTINE_NOTE_PREFIX="I51-FLAKE-QUARANTINE"`,
`DEFAULT_FLAKE_THRESHOLD=3`, and `FLAKE_POLICY_ID` formalized.
9 new tests in `tests/test_scenario_quarantine.py` (16 / 16 PASS).
Phase report:
[`reports/p4-flake-threshold-2026-05-03.md`](reports/p4-flake-threshold-2026-05-03.md).

### 2026-05-03 — P3 G-51-1 fired; D-IH-51-A executed (R-47-2 closes)

I51/P3 lands the per-persona `target_difficulty_band` column +
calibrator/validator/mirror wiring. **G-51-1 GREEN with 0 / 17 outliers**
(plan exit criterion was ≤ 2 personas outside tolerance). Four bands
were refined post-P2 against the verification loop
(CUSTOMER-SERVICE-PROSPECT, IDEA-PROPOSER, EXISTING-PARTNER,
RANDOM-INBOUND); see phase report for the P2-proposed → P3-final
table. **R-47-2 closes.**

**OPS-50-1** investigated: cassette dispatch is `(skill_id, probe_id)`-
keyed, not persona-keyed; `--persona` is a post-run filter. Wiring
persona-keyed cassettes belongs naturally inside I52's multi-judge
harness mode (avoids parallel cassette-layout churn). **Forwarded as
OPS-51-1**, scoped to I52 P3/P4.

**C-51-B** (per-persona target in calibration markdown) **closes**:
`render_calibration_markdown` now surfaces `t/m/h/i target` and
`source` (`persona`/`global`) columns.

Mirror DDL: `supabase/migrations/20260503180000_i51_persona_scenario_target_difficulty_band.sql`
(operator-applied via `mcp_supabase_apply_migration` or psql under
`service_role`; D-IH-51-D cadence applies). Phase report:
[`reports/p3-rebalance-2026-05-03.md`](reports/p3-rebalance-2026-05-03.md).

10 new tests in `tests/test_persona_scenario_registry.py` (33 / 33 PASS).

### 2026-05-03 — P2 calibration audit emitted (R-47-2 baseline + remediation plan)

I51/P2 lands the deterministic 13-outlier calibration audit:
[`reports/calibration-audit-2026-05-03.md`](reports/calibration-audit-2026-05-03.md).
Anchored to the calibration JSON
`artifacts/calibration/calibration-baseline-20260503T172852Z.json`
(`__overall__` PASS; 13 / 17 persona buckets outside ±5pp). Per-persona
`target_difficulty_band` proposals ratified for I51/P3 under G-51-1.
Two thin-N personas (CUSTOMER-SERVICE-PROSPECT, IDEA-PROPOSER; n=6 each)
flagged as the explicit candidates for the "≤ 2 personas may remain
outside tolerance" allowance at the P3 exit. Three carriers surfaced
(C-51-A USER_GUIDE doc surface, C-51-B calibration markdown render,
C-51-C persona-band-divergence policy). No CSV mutation; no operator
gate fire; mirror state unchanged. Phase report:
[`reports/p2-calibration-audit-2026-05-03.md`](reports/p2-calibration-audit-2026-05-03.md).

### 2026-05-03 — D-IH-51-D wired (P1 mirror-reseed emitter)

I51/P1 lands the `_emit_persona_scenario_registry_upserts()` emitter +
`--persona-scenario-registry-only` CLI mode in
`scripts/sync_compliance_mirrors_from_csv.py`. CSV row-count parity
verified at **329** (CSV header-anchored == `--count-only` ==
`INSERT` count in emitted SQL). This makes the D-IH-51-D cadence
("after every CSV tranche edit") mechanically executable: the operator
can now run `--persona-scenario-registry-only --output ...` and apply
under `service_role`. Phase report:
[`reports/p1-mirror-reseed-2026-05-03.md`](reports/p1-mirror-reseed-2026-05-03.md).
**Closes** OPS-47-9 on the data-plane side (one operator apply away
from full mirror parity).

_Append further phased ratifications below as they land._
