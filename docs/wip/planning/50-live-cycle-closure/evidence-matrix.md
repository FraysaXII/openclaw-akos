---
language: en
status: active
initiative: 50-live-cycle-closure
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 50 — Evidence matrix

Structured observations that justified this initiative before and during execution.

| ID | Observation | Source | Impact |
|:---|:------------|:-------|:-------|
| E1 | Five I49 wave commits sit on local `main` ahead of `origin/main`; not yet visible to remote consumers | `git status` 2026-05-03 | P1 must publish before I51 baseline is stable |
| E2 | `config/eval/model-prices.json` `_last_reviewed` = 2026-05-01; supplier pricing changes ~quarterly per the file's own header note | [`config/eval/model-prices.json`](../../../../config/eval/model-prices.json) `_note` | P2 refresh needed to keep cost surfaces honest |
| E3 | No `POL-EVAL-COST-CEILING-*` rows exist in `POLICY_REGISTER.csv`; only `judge_threshold` policy_class is live; cost ceilings live as env vars only | Grep on canonical CSV (no matches) | D-IH-50-A formalization decision |
| E4 | First **live** `--filter madeira` dossier has never been emitted; only snapshot-mode and offline runs exist | I49 closure UAT [`reports/uat-i49-madeira-management-2026-05-03.md`](../49-madeira-management-rollup/reports/uat-i49-madeira-management-2026-05-03.md) §"Three-light verdict" | P3 first live emit needed |
| E5 | First Tier-B controlled cell run has never executed; matrix is wired from I47 P14 but offline-default | I47 closure UAT [`reports/uat-i47-user-centric-uat-2026-05-02.md`](../47-user-centric-uat/reports/uat-i47-user-centric-uat-2026-05-02.md) §"OPS follow-ups" | P4 smoke needed |
| E6 | `scripts/promote_telemetry_to_scenario.py` shipped at I49 P11 but has never been operator-merged end-to-end | I49 P11 report | P5 first promotion run needed |
| E7 | I47 OPS-47-9 (`compliance.persona_scenario_registry_mirror` empty) and OPS-47-1/2 (push, PR open) outstanding | I47 closure UAT operator follow-ups table | I50/P1 closes OPS-47-1/2; I51/P1 closes OPS-47-9 |
| E8 | `tests/test_model_prices.py` does not exist; `model-prices.json` has no schema test | Glob check | P2 ships the test |

## Three-light verdict — first live MADEIRA dossier emit (P3, 2026-05-03)

| Lane | Signal | Basis |
|:---|:---:|:---|
| **Conversational** | **GREEN** | Sections 3–6 status roll-up (eval health PASS; persona/calibration PASS; adversarial 15/15 PASS; recovery 15/15 PASS, real chaos PLANNED-no-fail) |
| **Operator** | **GREEN** | Section 8 Operational health PASS (0 cost-ceiling breaches; agent_memory triggers fired = 0; promotion_gate_pass_count null but no failures) |
| **Surface** | **GREEN** | Section 8 `madeira_surface_ship=GREEN` (basis: latest Impeccable critique declares ship verdict; from I49 wave D craft critique 2026-05-03) |
| **Ship verdict** | **GO** | All three lights GREEN |

| Cost guard | Value |
|:---|:---|
| `MAX_DOSSIER_USD` envelope | **$5.00** (D-IH-50-B; sourced from `POL-EVAL-COST-CEILING-DOSSIER-V1`) |
| Actual `cost_total_usd` | **$0.0000** (no live judge invocations; `compliance.eval_run` rows_total=0 since first Tier-B fires in P4) |
| Spend headroom | 100% remaining |
| Cost-cap raise fired? | **NO** — `aggregate_dossier_cost_under_cap` did not raise |

| Artifact | Path |
|:---|:---|
| Local dossier | `artifacts/uat-dossier/uat-dossier-20260503T164343Z/dossier.md` (gitignored per `.gitignore` line 116) |
| Manifest SHA-256 | `1db895e31f0c02ee469f0a65f4bc51be73ed95c56a2d3fa43ac244fc39f68a4f` |
| Run ID | `dossier-c3d5c001e610` |
| Git SHA at emit | `b2bfd8702e2229cb22ef769d54c4c4695ab272ac` (I50 P2 commit) |
| Mode | `live` |
| Filter | `flavor=madeira`, `skill_id=skill_madeira_lookup_v1`, 5 personas, 7 initiatives |
| `compliance.dossier_run` write | **skipped** (no Supabase service-role configured in operator env; manifest captured locally) |

