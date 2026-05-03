---
language: en
status: closed
initiative: 50-live-cycle-closure
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 50 — Live cycle closure + cost SSOT truth-up

**Folder:** `docs/wip/planning/50-live-cycle-closure/`

**Status:** **Closed (2026-05-03).** All seven phases delivered; release-gate PASS across all 8 gates; 1571 tests PASS; MADEIRA SHIP verdict GO. Closure UAT: [`reports/uat-i50-live-cycle-closure-2026-05-03.md`](reports/uat-i50-live-cycle-closure-2026-05-03.md).

**Authoritative Cursor plan:** `~/.cursor/plans/i50–i56_madeira_kb_completion_87cc767e.plan.md` (master roadmap I50–I56).

**Cross-references:**

- Predecessor: [Initiative 49 — MADEIRA management and verdict rollup](../49-madeira-management-rollup/master-roadmap.md) (Closed 2026-05-03; five wave commits sit on `main` ahead of `origin/main`).
- Sister chain: I51 (persona calibration cleanup) → I52 (multi-model judge + RunPod cost) → I53 (GraphRAG PoC closure).
- Parallel tracks: [I54](../54-surface-test-hardening/) (depends on I50); [I55](../55-brand-ops-continuous-loop/) (depends on I50 + I52 P6).
- Operator follow-ups carried forward: I47 OPS-47-1/2/9 (push, mirror reseed scaffold).

## Outcome

Land governance folder; operator follow-through on I49 (push, drift, tests); refresh pricing + decide cost-ceiling formalization from 2026-Q2 public research; emit first **live** MADEIRA dossier with spend cap; run **Tier-B** smoke; run **telemetry promotion** loop once with operator-merge; close with UAT + CHANGELOG + planning table + WIP_DASHBOARD. Bidirectional contract: opens runway for I51 (clean baseline) and I54 (clean drift) in parallel.

## Phase plan (~5–7 op-days)

| Phase | Deliverable |
|:--:|:----|
| **P0** | Six governance artefacts in this folder + README row added to [`docs/wip/planning/README.md`](../README.md) |
| **P1** | I49 commits pushed to `origin/main`; `check-drift` clean; six MADEIRA-related test suites green |
| **P2** | `model-prices.json` refreshed for 2026-Q2; FINOPS counterparty notes aligned where eval suppliers map; D-IH-50-A logged with chosen path; `tests/test_model_prices.py` shipped and green |
| **P3** | First live `--filter madeira` dossier emit honoring `MAX_DOSSIER_USD=5`; three-light verdict captured in evidence-matrix |
| **P4** | First Tier-B controlled cell run (2-cell smoke; `AKOS_TIER_B_ENABLED=true`); outcome captured |
| **P5** | Telemetry promotion run; 1–3 scaffold scenarios merged via operator review (or explicit zero-merged decision-log row) |
| **P6** | Closure UAT report; `CHANGELOG.md` entry; planning README row → **Closed (YYYY-MM-DD)**; WIP_DASHBOARD re-render |

## Verification matrix

| Check | Cadence |
|:------|:--------|
| `py scripts/validate_hlk.py` | Every commit |
| `py scripts/check-drift.py` | P1 + P6 |
| `py -m pytest tests/test_model_prices.py -v` | After P2 |
| `py -m pytest tests/test_dossier_madeira_flavor.py tests/test_madeira_control_a11y.py tests/test_madeira_control_i18n.py tests/test_brand_voice_lint.py tests/test_telemetry_promotion.py tests/test_scenario_quarantine.py -v` | P1 + P6 |
| `py scripts/render_uat_dossier.py --filter madeira --mode live` honors `MAX_DOSSIER_USD=5` | P3 |
| Tier-B smoke (`AKOS_TIER_B_ENABLED=true`) | P4 |
| `py scripts/release-gate.py` | P6 |

## Operator approval gates

- **G-50-1** (P2) — Cost-ceiling formalization choice (D-IH-50-A) + `POL-EVAL-COST-CEILING-*` rows if path (i) selected.
- **G-50-2** (P5) — Each scaffold scenario merged from telemetry proposals (per-row gate per AKOS rule on `PERSONA_SCENARIO_REGISTRY.csv`).

## Risks

See [`risk-register.md`](risk-register.md). Six risks tracked (R-50-1..6) covering price regression, dossier overspend, Tier-B production regression, telemetry hallucination, FINOPS notes drift, push conflict.

## Reporting artefacts

- `reports/p<N>-*-YYYY-MM-DD.md` per phase
- `reports/dossier-first-live-emit-YYYY-MM-DD.md` (P3)
- `reports/p4-tier-b-smoke-YYYY-MM-DD.md` (P4)
- `reports/uat-i50-live-cycle-closure-YYYY-MM-DD.md` (P6 closure)

## Cross-cutting

- Decision IDs: `D-IH-50-A` through `D-IH-50-D` (4 seeded); operator-ratified at greenlight 2026-05-03.
- All vault docs carry `language: en` frontmatter.
- WIP_DASHBOARD picks this row up automatically.
- CHANGELOG entry on closure (P6).

## What this is NOT

- Multi-tenant runtime work (waits on I34).
- Live judge activation (that's I52).
- Persona calibration cleanup (that's I51).
- A new evaluation framework or dossier flavor (extends I47/I48/I49).
