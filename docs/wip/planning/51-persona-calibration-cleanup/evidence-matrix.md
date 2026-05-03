---
language: en
status: active
initiative: 51-persona-calibration-cleanup
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 51 — Evidence matrix

Structured observations that justified this initiative before and during execution.

| ID | Observation | Source | Impact |
|:---|:------------|:-------|:-------|
| E1 | I47 P10 baseline showed **13 of 17** personas outside ±5pp difficulty tolerance even though `__overall__` PASSes the 40/40/10/10 target | I47 closure UAT [`uat-i47-user-centric-uat-2026-05-02.md`](../47-user-centric-uat/reports/uat-i47-user-centric-uat-2026-05-02.md) §"Calibration" | Persona-level calibration cleanup needed; R-47-2 carrier |
| E2 | Section 4 of the I50/P3 first live MADEIRA dossier reports `personas_outside_tolerance_count: 13` at the new baseline (unchanged from I47 P10) | I50 P3 manifest [`reports/dossier-first-live-emit-2026-05-03.md`](../50-live-cycle-closure/reports/dossier-first-live-emit-2026-05-03.md) | I51 P3 must drive this to ≤2 |
| E3 | `compliance.persona_scenario_registry_mirror` was created at I47 P1 but has remained empty (`OPS-47-9`); reseed pathway never executed | I47 OPS-47-9 + Glob check on `sync_compliance_mirrors_from_csv.py` (no `_emit_persona_scenario_registry_upserts`) | I51 P1 ships the emitter |
| E4 | I49 P10 shipped `lifecycle_status=quarantined` enum + `scripts/quarantine_scenario.py` but quarantine **trigger conditions** are operator-judgement only — no flake-threshold formalism exists | I49 P10 report + Grep on POLICY_REGISTER (no `flake_threshold` `policy_class`) | I51 P4 formalizes (D-IH-51-B default) |
| E5 | I50/P4 Tier-B 2-cell smoke returned `rows_after_filter=0` because `tests/evals/cassettes/` has no persona-conditioned cassettes (16 files exist; all skill/adversarial-suite, not persona×difficulty) | [`reports/p4-tier-b-smoke-2026-05-03.md`](../50-live-cycle-closure/reports/p4-tier-b-smoke-2026-05-03.md) §"Why filtered cells returned 0 rows" | OPS-50-1 carrier — close in I51/P3 alongside calibration |
| E6 | `scripts/eval.py --calibrate` exists (I47 P10) but `--hard-fail-on-drift` flag does not | Grep on `scripts/eval.py` | I51 P5 wires the flag + new `eval_calibration_hard_fail` profile step |
| E7 | I49 P11 `scripts/promote_telemetry_to_scenario.py` runs end-to-end but doesn't (yet) feed into the calibration loop — the 3 scaffold rows merged in I50/P5 currently have **no calibration baseline** | I50 P5 report + scaffold lifecycle on the 3 new rows | I51 P3 must include the new rows in calibration audit |
| E8 | The 9 telemetry-promotion proposals (I50/P5) all targeted OPERATOR persona; investor/advisor/customer personas have no telemetry feed yet (no UI hookup, no MCP probe pipeline) | I50 P5 promotion run output | Out-of-scope for I51 (calibration cleanup, not data acquisition); flag for future initiative |
