---
language: en
status: active
initiative: 48-operator-dossier
report_kind: dossier-section-spec
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# Initiative 48 — Dossier section specification

> Per D-IH-48-D, the dossier emits 12 sections in fixed order (executive summary first → appendix last). Per D-IH-48-E, each section declares its data source(s) + refresh policy + page budget. This file is the **section contract** consumed by `akos/dossier/sections.py` (P1) — when this file changes, the section subclasses must update.

## Section design rules

Each section subclass implements 4 methods:

1. **`gather(mode: str, filter: DossierFilter | None) -> SectionData`** — fetch the data the section needs, respecting mode (snapshot reads cache; live re-runs CLI; tier-b runs Tier B).
2. **`render_markdown(data: SectionData) -> str`** — emit the markdown body (between BEGIN_AUTO/END_AUTO markers per the I32 P10 pattern).
3. **`render_html(data: SectionData) -> str`** — emit the HTML body (wrapped in `<details>` per D-IH-48-I; default-open status varies per section; appendix default-collapsed).
4. **`metrics_for_trend(data: SectionData) -> dict[str, float | int]`** — emit the per-section metrics that go into `compliance.dossier_run.section_metrics` JSONB for sparkline computation (P7).

## The 12 sections

### Section 1 — Executive summary

| Field | Value |
|:---|:---|
| Source(s) | All section roll-ups (post-aggregation; this section is computed last but rendered first) |
| Refresh policy | Always re-aggregated (cheap; in-memory) |
| Page budget (PDF) | 1 |
| Default `<details>` state (HTML) | open |
| Trend metrics emitted | `overall_status` (PASS/FAIL bool), `pass_count`, `fail_count`, `skip_count`, `cost_total_usd` |
| Markdown shape | Title + 1-line outcome verdict + table with per-section status (12 rows: section_name / status / data_age / outstanding_count) + 3-bullet "Operator action queue" derived from R-48-12 priorities |
| Failure mode | If any section reports FAIL, executive summary outcome = FAIL |

### Section 2 — Schema + governance

| Field | Value |
|:---|:---|
| Source(s) | `py scripts/validate_hlk.py` stdout |
| Refresh policy | Re-run if cache >12h |
| Page budget (PDF) | 1 |
| Default `<details>` state | open |
| Trend metrics | `validate_hlk_pass`, `total_topics`, `total_skills`, `total_policies`, `total_personas`, `total_scenarios`, `pre_existing_failures_count` |
| Markdown shape | Counts table (topics / skills / policies / personas / scenarios / cells / repos) + per-validator status table + Known operator-local config issues callout (the `tests/validate_configs.py::TestOpenclawConfig` failures from I47 P15 closure UAT) |
| Failure mode | FAIL when `validate_hlk` exit code ≠ 0 |

### Section 3 — Eval health

| Field | Value |
|:---|:---|
| Source(s) | `py scripts/eval.py --mode all --json` (snapshot: read latest run from `compliance.eval_run` if ≤12h fresh; live: re-run) |
| Refresh policy | Re-run if cache >12h |
| Page budget (PDF) | 2 |
| Default `<details>` state | open |
| Trend metrics | `eval_overall_status`, per-skill `pass_count`, per-skill `delta_pp`, per-skill `cost_usd`, `judge_score_brand_voice_mean`, `judge_score_citation_mean`, `judge_score_persona_fit_mean` |
| Markdown shape | Embed `Scorecard.to_markdown()` verbatim (E7) — includes per-skill canary table + smoke probes + rubric suites + per-persona breakdown (I47 P10) + LLM-judge axes (I47 P12) |
| Failure mode | FAIL when `overall_status='fail'` OR any skill regresses >5pp vs baseline |

### Section 4 — Persona library + calibration

| Field | Value |
|:---|:---|
| Source(s) | `py scripts/eval.py --calibrate` + `compliance.persona_scenario_registry_mirror` row count (when reseeded per I47 OPS-47-9) |
| Refresh policy | Read latest `artifacts/calibration/calibration-baseline-*.json` ≤24h; else re-run |
| Page budget (PDF) | 2 |
| Default `<details>` state | open |
| Trend metrics | `total_scenarios`, `total_personas`, `overall_within_tolerance` (bool), `personas_outside_tolerance_count`, per-persona `total_count` + `within_tolerance` |
| Markdown shape | Calibration distribution table (17 rows: __overall__ + 16 personas + OPERATOR pseudo) + within-tolerance flag per row + visual emphasis on `__overall__ YES/NO` + per-persona drift summary |
| Failure mode | WARN (not FAIL) when ≥1 persona outside ±5pp tolerance per D-IH-47-C; FAIL only when `__overall__` outside tolerance |

### Section 5 — Adversarial coverage

| Field | Value |
|:---|:---|
| Source(s) | `py scripts/eval.py --mode adversarial --json` (replay-only by default; tier-b adds live LLM judge) |
| Refresh policy | Re-run if cache >24h |
| Page budget (PDF) | 1 |
| Default `<details>` state | open |
| Trend metrics | `adversarial_pass_count`, `adversarial_fail_count`, per-category counts (impersonation / injection / context / tier-jumping / leakage), `pii_linter_clean` (bool), `cost_usd` |
| Markdown shape | Per-category counts table (5 rows; from I47 P7 categories) + recent-fail table (last 5 FAIL probes; with persona_id + scenario_id + reason) + `lint_cassette_pii.py` clean status |
| Failure mode | FAIL when any P7 cassette does NOT REFUSE (since all 30 expect REFUSE per I47 P7) |

### Section 6 — Recovery + chaos

| Field | Value |
|:---|:---|
| Source(s) | `py scripts/recovery_chaos_runner.py --scenario neo4j-password-rotation --dry-run` + last `artifacts/chaos/*.json` |
| Refresh policy | Read existing chaos artifact (newest); never auto-trigger live chaos |
| Page budget (PDF) | 1 |
| Default `<details>` state | collapsed (only opens when there's actionable content) |
| Trend metrics | `synthetic_recovery_pass_count` (out of 15), `real_chaos_last_run_status` (REFUSED / PLANNED / EXECUTED / null), `real_chaos_gates_passed` (bool when last run attempted) |
| Markdown shape | 16 P9 scenario states (15 synthetic + 1 real-chaos) — each row reports last observed outcome; safety gate state for real-chaos (4 gates: env opt-in / forbidden-host / operator confirmation / Aura key) |
| Failure mode | FAIL when synthetic recovery scenario expected REFUSE/ESCALATE but observed PASS (over-permissive) |

### Section 7 — Drift canaries

| Field | Value |
|:---|:---|
| Source(s) | `py scripts/graphrag_drift_canary.py --json` + Supabase mirror staleness query (per-mirror `MAX(synced_at)` across all `compliance.*_mirror` tables) |
| Refresh policy | Re-run if cache >24h |
| Page budget (PDF) | 1 |
| Default `<details>` state | open (high-signal section) |
| Trend metrics | `drift_canary_total_drift`, per-dimension `csv_count` + `neo4j_count` + `drift_delta`, `mirror_oldest_age_seconds`, `mirrors_stale_count` (>7d) |
| Markdown shape | 10-dimension drift table (Role / Process / Program / Topic / Persona / Channel / Sourcing / Skill / TouchpointKitCell / Policy) + Supabase mirror staleness table (16 mirrors) |
| Failure mode | FAIL when any drift > tolerance (default 1) OR any mirror >14d stale |

### Section 8 — Operational health

| Field | Value |
|:---|:---|
| Source(s) | `py scripts/agent_memory_trigger_watcher.py --json` + cost ceiling state from `compliance.eval_run` (sum cost_usd over last 7d per skill vs `POL-EVAL-COST-CEILING-*` ceilings) + promotion gate state per skill (`py scripts/eval.py promote --skill X --json` for each skill) |
| Refresh policy | Re-run trigger watcher; query mirror; promotion gate per skill (5 invocations; ~2s each) |
| Page budget (PDF) | 1 |
| Default `<details>` state | collapsed (only opens when there's actionable content) |
| Trend metrics | `agent_memory_triggers_fired` (count of FIRED), `cost_ceiling_breaches_count`, `promotion_gate_pass_count` (out of 5 skills) |
| Markdown shape | 3 trigger states (multi-tenant / conversation depth / compliance ask) + per-skill cost roll-up vs ceiling + per-skill promotion gate verdict |
| Failure mode | FAIL when any trigger FIRED OR any cost ceiling breached OR <2 of 5 skills meet promotion gate |

### Section 9 — External repo health

| Field | Value |
|:---|:---|
| Source(s) | `docs/references/hlk/compliance/REPO_HEALTH_SNAPSHOT.csv` (last weekly snapshot per repo) |
| Refresh policy | Read CSV (cheap; no re-run) |
| Page budget (PDF) | 1 |
| Default `<details>` state | collapsed (only relevant for cross-repo audits) |
| Trend metrics | per-repo `contract_present` (bool), `mirror_rule_present` (bool), `language_frontmatter_compliance_pct`, `brand_jargon_violations_count` |
| Markdown shape | 3-row table (boilerplate / hlk-erp / kirbe) with last weekly snapshot data + 4-consecutive-week regression alarm (per I32 P7) |
| Failure mode | WARN (not FAIL) when 4-consecutive-week regression detected (triggers I42 cross-repo CI integration) |

### Section 10 — Open governance debt

| Field | Value |
|:---|:---|
| Source(s) | All active initiative `master-roadmap.md` files; parse OPS-* tables; cross-reference open issues |
| Refresh policy | Re-aggregated each run (cheap; reads markdown files) |
| Page budget (PDF) | 1 |
| Default `<details>` state | open (operator action source) |
| Trend metrics | `open_ops_count_total`, per-initiative `open_ops_count`, `oldest_open_ops_age_days` |
| Markdown shape | Top 10 open OPS-* items sorted by initiative number ascending (most-recent initiatives first per `WIP_DASHBOARD` ordering) + total count + oldest-open-age callout |
| Failure mode | WARN (not FAIL) when any OPS-* item >90d old |

### Section 11 — Trend lines (P7)

| Field | Value |
|:---|:---|
| Source(s) | `compliance.dossier_run` last N runs (N=10 default; configurable via `--trend-window`) |
| Refresh policy | Always queried (cheap) |
| Page budget (PDF) | 2 (sparklines per metric) |
| Default `<details>` state | open |
| Trend metrics | (this section emits NO trend metrics; it CONSUMES them from prior runs) |
| Markdown shape | 4 sparkline metrics: `eval_pass_rate` (Section 3) / `calibration_drift_count` (Section 4) / `drift_canary_total` (Section 7) / `cost_total_usd` (Section 1 + Section 8); each as inline SVG + delta-vs-last-run text |
| Failure mode | INFO-only (sparklines are diagnostic; never the failure cause) |
| Special | When <2 prior runs exist, emit "INSUFFICIENT-DATA placeholder" instead of sparkline (P7-A3) |

### Section 12 — Appendix

| Field | Value |
|:---|:---|
| Source(s) | All section manifest data + run config + git_sha + UTC timestamp + sha256 hashes |
| Refresh policy | Always emitted (computed at end of run) |
| Page budget (PDF) | 1 |
| Default `<details>` state | collapsed (operator drill-down only) |
| Trend metrics | `manifest_sha256`, `git_sha`, `run_duration_seconds` |
| Markdown shape | Run config table (mode + format + filters + git_sha + UTC + duration) + per-section data source paths + sha256 manifest + raw artifact paths under `artifacts/uat-dossier/uat-dossier-<UTC>/` |
| Failure mode | INFO-only |

## Section ordering invariant

Per D-IH-48-D, sections render in this order regardless of mode/filter:

```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12
```

Tests assert this ordering in `tests/test_dossier_run.py::test_section_order_matches_spec`.

## Per-section staleness cache contract (D-IH-48-E)

| Section | Default staleness threshold | Rationale |
|:-------:|:---------------------------:|:----------|
| 1 (Executive summary) | 0 (always re-aggregated) | Cheap; needs current data |
| 2 (Schema + governance) | 12h | `validate_hlk` is fast (~5s); but vault changes accumulate |
| 3 (Eval health) | 12h | `eval --mode all` is ~30s but reads mirror; cache-eligible |
| 4 (Persona library) | 24h | Calibration is ~3s; library rarely changes |
| 5 (Adversarial) | 24h | Replay-only is fast; live LLM is slow + expensive |
| 6 (Recovery + chaos) | NEVER auto-refresh | Chaos NEVER auto-runs; reads last artifact |
| 7 (Drift canaries) | 24h | `graphrag_drift_canary` is ~5s but Neo4j round-trip; cache-eligible |
| 8 (Operational health) | 12h | Mirror queries cheap; promotion gate per skill ~10s |
| 9 (External repo health) | 7d | REPO_HEALTH_SNAPSHOT is weekly cadence |
| 10 (Open governance debt) | 0 (always re-parse) | Cheap; reads markdown files |
| 11 (Trend lines) | 0 (always re-query) | Mirror query is cheap |
| 12 (Appendix) | 0 (always emitted) | Computed at end of run |

Operator can override staleness via `--max-staleness-hours <N>` flag at CLI time (applies to all sections).

## Mode behavior matrix

| Section | snapshot mode | live mode | tier-b mode |
|:-------:|:-------------:|:---------:|:-----------:|
| 1 | re-aggregate from cached sections | re-aggregate from re-run sections | re-aggregate from tier-b sections |
| 2 | read cache if fresh; else PLACEHOLDER | re-run | re-run |
| 3 | read cache if fresh; else PLACEHOLDER | re-run --mode all | re-run --tier B --mode all |
| 4 | read cache if fresh; else PLACEHOLDER | re-run --calibrate | re-run --calibrate |
| 5 | read cache if fresh; else PLACEHOLDER | re-run --mode adversarial | re-run --tier B --mode adversarial |
| 6 | read latest chaos artifact | dry-run gate-check + read latest artifact | same as live (chaos NEVER auto-runs in tier-b either) |
| 7 | read cache if fresh; else PLACEHOLDER | re-run drift canary | re-run drift canary |
| 8 | read cache if fresh; else PLACEHOLDER | re-run trigger watcher + per-skill promotion | re-run trigger watcher + per-skill promotion |
| 9 | read CSV (no cache; cheap) | read CSV | read CSV |
| 10 | always re-parse markdown | always re-parse markdown | always re-parse markdown |
| 11 | always query mirror | always query mirror | always query mirror |
| 12 | always emit at end of run | always emit at end of run | always emit at end of run |

## PLACEHOLDER text contract

When a section's source CLI fails (R-48-1) OR cache is stale + mode forbids re-run, emit:

```
> ⚠ STALE / UNAVAILABLE — last refreshed Nh ago (cache hit) OR CLI exit code N
> Run `py scripts/render_uat_dossier.py --mode live` to refresh this section
```

This makes incomplete data visible without crashing the dossier (R-48-1 graceful degradation).

## Cross-references

- D-IH-48-D (section ordering)
- D-IH-48-E (per-section staleness)
- D-IH-48-F (trend storage substrate)
- D-IH-48-I (HTML interactivity scope: native `<details>`)
- I32 P10 `render_wip_dashboard.py` BEGIN_AUTO/END_AUTO marker convention (reused for sections that mix auto-render with operator commentary)
- I47 P15 closure UAT report (E4 — section template source)
