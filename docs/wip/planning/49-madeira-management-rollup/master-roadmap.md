---
language: en
status: closed
initiative: 49-madeira-management-rollup
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 49 — MADEIRA management and verdict rollup

**Folder:** `docs/wip/planning/49-madeira-management-rollup/`

**Status:** **Closed (2026-05-03).** All 18 phases delivered; closure UAT [`reports/uat-i49-madeira-management-2026-05-03.md`](reports/uat-i49-madeira-management-2026-05-03.md).

**Cross-references:**

- MADEIRA hardened program baseline: [`../02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](../02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md) (Part H: verdict and cadence, post-P3)
- Persona-driven UAT library: [`../47-user-centric-uat/master-roadmap.md`](../47-user-centric-uat/master-roadmap.md)
- Operator dossier aggregator: [`../48-operator-dossier/master-roadmap.md`](../48-operator-dossier/master-roadmap.md)
- Program index: [`madeira-program-index.md`](madeira-program-index.md)

## Outcome

Ship canonical **process**, **vault SOP**, and **repo guide** tiers for repeatable MADEIRA governance; extend `PERSONA_SCENARIO_REGISTRY` with priority ranking and optional quarantine; add `--filter madeira` to [`scripts/render_uat_dossier.py`](../../../scripts/render_uat_dossier.py); redesign [`static/madeira_control.html`](../../../static/madeira_control.html) with a11y and i18n; wire Docker preflight, telemetry proposals, offline brand lint, Langfuse observability docs, dossier Surface UX rollup, closure UAT.

## Phase map (18 phases)

| Phase | Deliverable |
|:--:|:---|
| P0 | Six governance artefacts and cursor rule scaffold |
| P1 | `madeira-program-index.md` |
| P2 | `priority_score`, `safety_lane`, `release_blocking` columns + calibration |
| P3 | Part H verdict and cadence in consolidated plan |
| P4 | `doctor.py --docker-sandbox` |
| P5 | `process_list` workstream + six processes |
| P6 | Four v3.0 SOP-MADEIRA files |
| P7 | Three `docs/guides/madeira_*.md` |
| P8 | Finalize `akos-madeira-management.mdc` |
| P9 | Dossier `--filter madeira` + Section 1 three-light verdict |
| P10 | `quarantined` lifecycle + `quarantine_scenario.py` |
| P11 | `promote_telemetry_to_scenario.py` |
| P12 | Section 8 MADEIRA cost rollup + `lint_brand_voice_offline.py` |
| P13 | `madeira_langfuse_dashboard.md` |
| P14 | Impeccable shape report |
| P15 | Impeccable craft redesign of control plane |
| P16 | Dossier Section 8 Surface UX sub-section (madeira flavor) |
| P17 | Closure: tests, UAT, CHANGELOG, WIP_DASHBOARD, dossier emission |

See [`asset-classification.md`](asset-classification.md) for canonical boundaries.

## Verification matrix

| Check | Cadence |
|:------|:--------|
| `py scripts/validate_hlk.py` | Every commit touching compliance or vault |
| `py scripts/verify.py pre_commit` | Every commit |
| `py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format md` | P9+ |

## Risks

See [`risk-register.md`](risk-register.md).

