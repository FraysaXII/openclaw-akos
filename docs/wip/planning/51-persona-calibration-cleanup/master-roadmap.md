---
language: en
status: closed
initiative: 51-persona-calibration-cleanup
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 51 — Persona calibration cleanup

**Folder:** `docs/wip/planning/51-persona-calibration-cleanup/`

**Status:** Closed 2026-05-03. R-47-2 closes (13 / 17 → 0 / 17 outliers); OPS-47-9 + OPS-47-6 close; OPS-50-1 forwarded as OPS-51-1 to I52 P3/P4. Closure UAT: [`reports/uat-i51-persona-calibration-cleanup-2026-05-03.md`](reports/uat-i51-persona-calibration-cleanup-2026-05-03.md).

**Authoritative Cursor plan:** `~/.cursor/plans/i50–i56_madeira_kb_completion_87cc767e.plan.md` §"Initiative 51".

**Origin:**

- **R-47-2** (calibration drift) — I47 P10 baseline showed 13 of 17 personas outside ±5pp tolerance even though `__overall__` passes.
- **OPS-47-6** — calibration audit and remediation deferred from I47 closure.
- **OPS-47-9** — `compliance.persona_scenario_registry_mirror` was created at I47 P1 but has remained empty.
- **OPS-50-1** — Tier-B persona cassette population (carrier surfaced in I50 P4 closure).

## Outcome

Land mirror reseed; drive per-persona difficulty distribution back inside ±5pp tolerance; formalize the I49 quarantine policy with a flake-rate threshold (POLICY row); gate `--hard-fail-on-drift` for tightened CI on the weekly Tier-B profile only (pre-commit stays warn-only). Bidirectional contract: dossier Section 04 reflects post-cleanup balance and `quarantined_scenarios_count` once the loop runs end-to-end.

## Phase plan (~3-5 op-days)

| Phase | Deliverable |
|:--:|:----|
| **P0** | Six governance artefacts under this folder + planning README row |
| **P1** | **Mirror reseed (closes OPS-47-9):** add `_emit_persona_scenario_registry_upserts()` to [`scripts/sync_compliance_mirrors_from_csv.py`](../../../scripts/sync_compliance_mirrors_from_csv.py); reseed via `service_role`; verify CSV row-count == mirror row-count |
| **P2** | **Calibration audit:** run `py scripts/calibrate_scenarios.py` baseline; emit `reports/calibration-audit-YYYY-MM-DD.md` with the 13 outliers, drift direction (+/- per band), and proposed remediation per persona |
| **P3** | **Operator-chosen rebalance path (G-51-1; D-IH-51-A):** rebalance scenarios across personas OR add per-persona `target_difficulty_band` column; edit `PERSONA_SCENARIO_REGISTRY.csv`; re-run calibration; require ≤2 personas outside ±5pp at exit. ALSO closes OPS-50-1 (cassette wiring for hot-path personas) where it overlaps |
| **P4** | **Flake-threshold policy (D-IH-51-B):** either add `POL-EVAL-FLAKE-THRESHOLD-V1` row + `flake_threshold` `policy_class`, OR document operator-judgement path; extend `quarantine_scenario.py --auto-from-flake-history` |
| **P5** | **CI tightening (D-IH-51-C):** wire `--hard-fail-on-drift` (>5pp) into `eval_tier_b_weekly` profile; pre-commit stays warn-only to preserve operator agency |
| **P6** | **Closure:** pytest sweep; `dossier --filter madeira` re-emit; CHANGELOG entry; planning README row → **Closed (YYYY-MM-DD)**; WIP_DASHBOARD re-render |

## Verification matrix

| Check | Cadence |
|:------|:--------|
| `py scripts/validate_hlk.py` (PERSONA_SCENARIO_REGISTRY + POLICY_REGISTER) | Every commit |
| `py scripts/validate_persona_scenario_registry.py` | Every commit |
| `py scripts/eval.py --calibrate` distribution (per-persona, ±5pp at P3 exit) | P3 + P6 |
| `py scripts/eval.py --hard-fail-on-drift` smoke | New `eval_calibration_hard_fail` profile (P5) |
| Mirror row-count parity (CSV vs `compliance.persona_scenario_registry_mirror`) | P1 + P6 |
| `py -m pytest tests/test_persona_scenario_mirror_emit.py tests/test_eval_persona_calibration.py tests/test_scenario_quarantine.py -v` | Every commit |

## Operator approval gates

- **G-51-1** (P3) — Per-persona target band edits in `PERSONA_SCENARIO_REGISTRY.csv` (CSV gate per AKOS governance rule).
- **G-51-2** (P4, conditional) — New `flake_threshold` `policy_class` if D-IH-51-B chooses formalize path.

## Risks (R-51-1..2)

See [`risk-register.md`](risk-register.md). Two risks: rebalance ripple through cassettes (mitigation: prefer per-persona band column path); flake-threshold policy creating new operator-approval cadence (mitigation: gate decision at P4; reversible).

## Reporting artefacts

- `reports/p<N>-*-YYYY-MM-DD.md` per phase
- `reports/p1-mirror-reseed-YYYY-MM-DD.md` (P1)
- `reports/calibration-audit-YYYY-MM-DD.md` (P2)
- `reports/uat-i51-persona-calibration-cleanup-YYYY-MM-DD.md` (P6 closure)

## Cross-cutting

- Decision IDs: `D-IH-51-A` through `D-IH-51-D` (4 seeded; defaults documented in [`decision-log.md`](decision-log.md)).
- `language: en` frontmatter on all vault docs.
- WIP_DASHBOARD picks this row up automatically.
- CHANGELOG entry on closure (P6).

## What this is NOT

- A rewrite of the calibration metric (the 40/40/10/10 target stays per D-IH-47-C).
- An expansion of the scenario library beyond rows promoted in I50/P5.
- A change to LLM-judge thresholds (that's I52).
- A rewrite of the priority_score formula (I49 deterministic Reach × Impact / Effort stays).
