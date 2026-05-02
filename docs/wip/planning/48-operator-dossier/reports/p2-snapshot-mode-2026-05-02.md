---
language: en
status: active
initiative: 48-operator-dossier
report_kind: phase-report
phase: P2
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I48 P2 — Snapshot mode (offline aggregator <30s)

## What shipped

### `akos/dossier/sources.py` (NEW; ~250 lines)

Per-section data fetchers that read existing artifacts (no subprocess in snapshot mode). Each function returns a `SectionData` payload; missing source returns `placeholder=True` per dossier-section-spec.md PLACEHOLDER contract.

| Function | Section | Source |
|:---|:---:|:---|
| `gather_schema_governance()` | 2 | Direct CSV row counts (TOPIC_REGISTRY + SKILL_REGISTRY + POLICY_REGISTER + PERSONA_REGISTRY + PERSONA_SCENARIO_REGISTRY) |
| `gather_eval_health_snapshot()` | 3 | Query `compliance.eval_run` mirror via PostgREST (skip-when-env-missing per E6 + I47 P13 item 4 pattern) |
| `gather_persona_calibration()` | 4 | Latest `artifacts/calibration/calibration-baseline-*.json` (I47 P10 source) |
| `gather_recovery_chaos()` | 6 | Latest `artifacts/chaos/real-chaos-*.json` (I47 P9 source) |
| `gather_operational_health()` | 8 | Latest `artifacts/agent-memory-triggers/trigger-watch-*.json` (I47 P13 source) |
| `gather_external_repos()` | 9 | `REPO_HEALTH_SNAPSHOT.csv` (I32 P7 source) |
| `gather_governance_debt(initiative_filter=)` | 10 | Walks `docs/wip/planning/<NN>-*/` master-roadmap + reports/uat-*.md; OPS-* table parser |
| `latest_artifact(directory, glob)` | helper | Returns newest file matching pattern with age_seconds |
| `list_active_initiatives()` | helper | Parses WIP_DASHBOARD.md auto-table for "open" rows |
| `stale_badge(age_seconds, threshold_hours)` | helper | Returns STALE badge string when over threshold |
| `_safe_relative(path)` | helper | Best-effort REPO_ROOT-relative path (handles out-of-repo --out-dir gracefully) |

Sections 1, 5, 7, 11, 12 are NOT wired by P2:
- Section 1: computed from prior section results in script orchestrator
- Section 5: needs `eval --mode adversarial`; lands in P3 live mode
- Section 7: needs `graphrag_drift_canary.py`; lands in P3 live mode
- Section 11: needs trend storage; lands in P7
- Section 12: appendix self-emits at end of run

### `scripts/render_uat_dossier.py` (NEW; ~270 lines)

Operator entry point. Working flags:
- `--mode {snapshot,live,tier-b}` per D-IH-48-C (snapshot wired in P2; live/tier-b in P3)
- `--format {md,pdf,html,all}` per D-IH-48-B (md + html wired in P2; pdf placeholder until P4)
- `--initiative <NN>` filter (P6; works in P2 for Section 10 OPS table filtering)
- `--persona <id>` filter (P6; works in P2 for filter section in dossier metadata)
- `--since <YYYY-MM-DD>` filter (P6; placeholder until P7)
- `--max-staleness-hours <N>` per-section staleness override (D-IH-48-E)
- `--max-spend <USD>` cost cap override (D-IH-48-L)
- `--trend-window <N>` Section 11 N data points (default 10)
- `--screenshots` opt-in (P3)
- `--gh-pr-comment` (P8)
- `--out-dir <path>` override; `--quiet`; `--json`

Refuses `--mode tier-b` without `AKOS_DOSSIER_TIER_B=1` env (D-IH-48-L); exit code 10.

### `akos/dossier/sections.py` extensions

7 Section subclasses (`Section02SchemaGovernance`, `Section03EvalHealth`, `Section04PersonaCalibration`, `Section06Recovery`, `Section08OperationalHealth`, `Section09ExternalRepos`, `Section10GovernanceDebt`) updated to delegate `gather()` to the corresponding `sources.py` function.

`Section01ExecutiveSummary.gather(prior_results=...)` extended to compute outcome from the OTHER 11 section results (PASS/FAIL/WARN/SKIP/INFO counts + cost roll-up + per-section status table).

### `artifacts/uat-dossier/README.md` (NEW)

Operator-facing README explaining how to regenerate dossiers + cost discipline + per-format output paths.

### `.gitignore` extension

`artifacts/uat-dossier/uat-dossier-*/` (per-run timestamped; regenerable; gitignored except README) per D-IH-48-G.

## Verification

- 37 new P2 tests across 2 NEW suites:
  - `tests/test_dossier_sources.py` — 21 tests (latest_artifact + 7 source functions + helpers; uses tmp_path fixture + monkeypatch.setattr for ARTIFACTS_DIR isolation)
  - `tests/test_render_uat_dossier_cli.py` — 16 tests (CLI surface + Tier B opt-in refusal + filter propagation + manifest shape + section ordering + HTML standalone-file invariant + --quiet/--json flags)
- All 154 dossier tests (P1 + P2) PASS in 5.38s
- Live snapshot smoke: `py scripts/render_uat_dossier.py --quiet` → wrote `dossier.md` + `manifest.json` in 87ms
- Live multi-format smoke: `py scripts/render_uat_dossier.py --format all --persona PERSONA-INVESTOR-COLD --quiet` → wrote md + html + manifest + PDF placeholder in 84ms
- Section 2 reads canonical CSV: 28 topics / 5 skills / 25 policies / 16 personas / 326 scenarios
- Section 4 reads I47 calibration baseline: 326 scenarios / 17 personas / 13 outside ±5pp tolerance
- Section 10 parses OPS-* tables across active initiatives

## Performance

P2 acceptance criterion: `--mode snapshot` <30s. Actual: **~85-90ms** (orders of magnitude under target). The artifact-reading + CSV-counting + markdown-rendering pipeline is dominated by Python startup, not by the dossier work itself.

## Known limitations (P3-P9 will close)

- Section 3 (Eval health) reports SKIP without `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` env (P3 live mode invokes `eval.py --mode all` directly)
- Section 5 (Adversarial) is fully placeholder until P3
- Section 7 (Drift canaries) is fully placeholder until P3
- Section 11 (Trend lines) emits INSUFFICIENT-DATA until P7 wires `compliance.dossier_run` mirror
- Section 12 (Appendix) cites manifest.json by reference; no embedded sha256 in markdown body yet
- `--format pdf` writes a placeholder sidecar (P4 wires `render_pdf_branded`)
- `--format html` is minimal (P5 will replace `<pre>` body with proper markdown library invocation + sparkline embedding)

## Cross-references

- D-IH-48-A (package shape; sources.py is the per-section data layer)
- D-IH-48-C (3 modes; P2 wires snapshot)
- D-IH-48-E (per-section staleness; P2 reads artifact ages)
- D-IH-48-G (operator-local + gitignored; .gitignore extension)
- D-IH-48-L (Tier B opt-in env-gate; P2 enforces refuse-without-opt-in)
- E6 (compliance.eval_run substrate; P2 queries best-effort)
- E7 (Scorecard.to_markdown reuse; deferred to P3 live mode invocation)
- I32 P10 auto-render-with-markers pattern (Section 10 OPS-* parser uses same regex approach)
- I47 P9 chaos artifact reader pattern (Section 6 reuses)
- I47 P10 calibration artifact pattern (Section 4 reuses)
- I47 P13 trigger watcher artifact pattern (Section 8 reuses)
