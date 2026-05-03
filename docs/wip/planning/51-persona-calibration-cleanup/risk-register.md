---
language: en
status: active
initiative: 51-persona-calibration-cleanup
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 51 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|:---|:-----|:-----------|:-------|:-----------|:-------|
| R-51-1 | Rebalance ripples through ~50 cassettes; cassette re-record cost | Med (if D-IH-51-A=rebalance) / Low (if D-IH-51-A=column) | Cost / Sched | Default chooses **per-persona target_difficulty_band column** path (D-IH-51-A) — no scenario relocation; no cassette re-record; no historical PASS/FAIL trail loss | Open |
| R-51-2 | Flake-threshold POLICY creates new operator-approval cadence | Low | Governance | Gate decision at P4 with explicit decision; can defer to operator-judgement path; reversible POLICY deprecation | Open |
| R-51-3 | Mirror reseed exposes drift between CSV and an unknown stale `compliance.persona_scenario_registry_mirror` state | Low | Sched | First-emit reseed is idempotent (UPSERT on `scenario_id`); row-count parity check at end of P1; abort if delta > 5% | Open |
| R-51-4 | `--hard-fail-on-drift` causes false positives during legitimate scaffold-row addition (e.g., P5 telemetry promotions) | Med | Sched | Pre-commit stays warn-only (D-IH-51-C); hard-fail only on weekly Tier-B which is operator-aware; ramp-up period of 2 weekly cycles before flag becomes blocking | Open |
| R-51-5 | OPS-50-1 cassette wiring is more work than fits in I51 P3 | Med | Scope | Bound P3 to highest-leverage cells (top 3 personas × 1 difficulty class each); remainder carries forward as new OPS-51-N | Open |
