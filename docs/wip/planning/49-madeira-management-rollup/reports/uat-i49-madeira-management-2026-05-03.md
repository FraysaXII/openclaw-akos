---
language: en
status: active
initiative: 49-madeira-management-rollup
report_kind: uat
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-03
---

# Initiative 49 — Closure UAT (MADEIRA management verdict rollup)

> **Outcome: PASS with documented amber follow-ups.** Three-light verdict at closure: Conversational AMBER (snapshot mode), Operator GREEN, Surface GREEN. Live-mode emit + monthly Tier-3 lift the conversational lane to GREEN per cadence in `MADEIRA_HARDENING_CONSOLIDATED_PLAN.md` Part H.
>
> Plan anchor: [`master-roadmap.md`](../master-roadmap.md). Doctrine anchors: [SOP-MADEIRA_VERDICT_AND_CADENCE_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_VERDICT_AND_CADENCE_001.md), [SOP-MADEIRA_INCIDENT_RESPONSE_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_INCIDENT_RESPONSE_001.md), [SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md), [SOP-MADEIRA_UX_REVIEW_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_UX_REVIEW_001.md).

## 1. Phase results matrix

| Phase | Scope | Status | Evidence |
|:---|:---|:---|:---|
| P0 | Initiative folder + 6 governance artefacts + cursor rule scaffold + WIP README row | PASS | `master-roadmap.md`, `decision-log.md`, `evidence-matrix.md`, `risk-register.md`, `asset-classification.md`, `scenario-taxonomy.md`, `.cursor/rules/akos-madeira-management.mdc`, `docs/wip/planning/README.md` row 49 |
| P1 | MADEIRA program index page consolidating 9 initiatives | PASS | [`madeira-program-index.md`](../madeira-program-index.md) |
| P2 | `priority_score` + `safety_lane` + `release_blocking` columns + coverage matrix sort | PASS | `PERSONA_SCENARIO_REGISTRY.csv`, `akos/hlk_persona_scenario_priority.py`, `scripts/recalculate_persona_scenario_priorities.py`, `scripts/calibrate_scenarios.py --write-priority-scores`, `tests/test_priority_score.py`, `tests/test_persona_scenario_registry.py`, `tests/test_eval_persona_calibration.py`, `supabase/migrations/20260503120000_i49_persona_scenario_registry_priority_columns.sql`, `docs/wip/planning/17-madeira-cursor-mode-parity/coverage-matrix.md` |
| P3 | Three-light GO/NO-GO doctrine + cadence in `MADEIRA_HARDENING_CONSOLIDATED_PLAN.md` Part H | PASS | Part H added; `docs/USER_GUIDE.md` §24.2.1 cross-link |
| P4 | `doctor.py --docker-sandbox` precheck; Tier-3 / Playwright preflight env | PASS | `akos/docker_engine_probe.py`, `scripts/doctor.py`, `scripts/browser-smoke.py` env `AKOS_REQUIRE_DOCKER_PREFLIGHT=1`, `tests/test_doctor.py`, `docs/uat/dashboard_smoke.md`, `docs/uat/madeira_use_case_matrix.md` |
| P5 | `process_list.csv` tranche: 1 workstream + 6 process rows under `env_tech_prj_3` | PASS | `process_list.csv` with `env_tech_ws_madeira_quality` + `env_tech_dtp_madeira_{verdict,dossier,incident,lifecycle,telemetry,uxreview}`; `validate_hlk.py` OVERALL PASS at 1100 process rows; deck/governance counts updated |
| P6 | Four v3.0 vault SOPs with bidirectional dossier reference contract | PASS | `SOP-MADEIRA_VERDICT_AND_CADENCE_001.md`, `SOP-MADEIRA_INCIDENT_RESPONSE_001.md`, `SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md`, `SOP-MADEIRA_UX_REVIEW_001.md`; `validate_hlk_vault_links.py` PASS; vault `index.md` cross-links added |
| P7 | Three repo operator guides + cross-links | PASS | [`madeira_operator_quickstart.md`](../../../guides/madeira_operator_quickstart.md), [`madeira_contributor.md`](../../../guides/madeira_contributor.md), [`madeira_dossier_workflow.md`](../../../guides/madeira_dossier_workflow.md); `docs/README.md`, `CONTRIBUTING.md`, `docs/guides/first_time_contributor.md` cross-links |
| P8 | Cursor rule finalised with full doctrine + globs | PASS | [`.cursor/rules/akos-madeira-management.mdc`](../../../../.cursor/rules/akos-madeira-management.mdc) |
| P9 | `--filter madeira` flag + Section 1 specialisation (3-light verdict) | PASS | `scripts/render_uat_dossier.py`, `akos/dossier/run.py` (`flavor`+`skill_id`), `akos/dossier/sections.py::Section01ExecutiveSummaryMadeira`, `akos/dossier/madeira_preset.py`, `tests/test_dossier_madeira_flavor.py`, `docs/wip/planning/48-operator-dossier/dossier-section-spec.md` extension |
| P10 | Anti-flake / quarantine policy + `lifecycle_status` enum extension | PASS | `akos/hlk_persona_scenario_csv.py` (`quarantined`), `scripts/quarantine_scenario.py`, Section 4 quarantine table, `tests/test_scenario_quarantine.py`, decision-log D-IH-49-C |
| P11 | Telemetry → registry feedback loop (proposals only) | PASS | `scripts/promote_telemetry_to_scenario.py`, `tests/test_telemetry_promotion.py` |
| P12 | Cost ceiling extension in Section 8 + offline brand voice fast-lint | PASS | `akos/dossier/sections.py::Section08OperationalHealth` MADEIRA cost rollup block, `akos/dossier/sources.py::gather_madeira_cost_rollup`, `scripts/lint_brand_voice_offline.py`, `config/verification-profiles.json` step `brand_voice_lint_smoke`, `tests/test_brand_voice_lint.py` |
| P13 | Langfuse MADEIRA saved-view dashboard + walkthrough guide | PASS | [`madeira_langfuse_dashboard.md`](../../../guides/madeira_langfuse_dashboard.md) |
| P14 | `/impeccable shape` artefact for `static/madeira_control.html` | PASS | [`impeccable-shape-madeira-control-2026-05-03.md`](impeccable-shape-madeira-control-2026-05-03.md) |
| P15 | `/impeccable craft` redesign + a11y + i18n (en/es/fr) | PASS | `static/madeira_control.html` (rewritten), [`impeccable-critique-madeira-control-2026-05-03.md`](impeccable-critique-madeira-control-2026-05-03.md), `tests/test_madeira_control_a11y.py`, `tests/test_madeira_control_i18n.py` |
| P16 | Surface UX subsection in dossier Section 8 (flavor='madeira') | PASS | `akos/dossier/sources.py::gather_madeira_surface_signals`, Section 8 `MADEIRA Surface UX` block; `tests/test_dossier_madeira_flavor.py` (Section 8 cases) |
| P17 | Closure: tests, UAT, CHANGELOG, WIP_DASHBOARD, first MADEIRA dossier emit | THIS REPORT | Evidence below |

## 2. Verification matrix outcomes

| Gate | Result | Evidence |
|:---|:---|:---|
| `py scripts/validate_hlk.py` | OVERALL PASS | 1100 process rows; 326 scenarios; vault frontmatter clean |
| `py scripts/validate_persona_scenario_registry.py` | PASS | `quarantined` accepted; `priority_score` validated |
| `py scripts/validate_hlk_vault_links.py` | PASS | Internal `.md` links resolve including 4 new SOP cross-links from `index.md` |
| `py -m pytest tests/test_priority_score.py tests/test_persona_scenario_registry.py tests/test_eval_persona_calibration.py tests/test_doctor.py tests/test_validate_hlk_dispatcher.py tests/test_sync_compliance_mirrors_from_csv.py tests/test_holistik_ops_axis_graph.py tests/test_company_deck.py` | 106 passed | P2 + P5 regression coverage |
| `py -m pytest tests/test_dossier_madeira_flavor.py tests/test_dossier_run.py tests/test_dossier_sections.py tests/test_dossier_run_writer.py` | passed | P9 + P12 + P16 dossier coverage |
| `py -m pytest tests/test_scenario_quarantine.py tests/test_telemetry_promotion.py tests/test_brand_voice_lint.py` | passed | P10 + P11 + P12 ops coverage |
| `py -m pytest tests/test_madeira_control_a11y.py tests/test_madeira_control_i18n.py` | passed | P15 surface coverage |
| `py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format md --quiet` | DOSSIER EMITTED (overall FAIL is expected snapshot signal — Section 3/5/7 placeholders; three lights still computed) | [`artifacts/uat-dossier/uat-dossier-20260502T232643Z/dossier.md`](../../../../artifacts/uat-dossier/uat-dossier-20260502T232643Z/dossier.md) |

## 3. Three-light verdict at closure

| Lane | Signal | Reason |
|:---|:---|:---|
| Conversational | AMBER | Snapshot mode placeholders for Sections 3/5/7. Run `py scripts/render_uat_dossier.py --filter madeira --mode live --format all` after the next weekly cadence to lift this lane to GREEN. |
| Operator | GREEN | Section 8 cost rollup envelope nominal; promotion gate count pending (snapshot). |
| Surface | GREEN | `gather_madeira_surface_signals` parses the P15 critique artefact: verdict ship. |

GO is gated on the conversational lane reaching GREEN under live mode and monthly Tier-3 cadence per Part H thresholds.

## 4. Operator follow-ups

- Run live-mode dossier weekly per cadence; first run after merge.
- Monthly Tier-3 UAT verdict for top-10 priority-ranked scenarios per `coverage-matrix.md` `I49_review_order`.
- Apply the I49 Supabase migration when MasterData is reconnected.
- Quarterly UX deep audit per [SOP-MADEIRA_UX_REVIEW_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_UX_REVIEW_001.md).
