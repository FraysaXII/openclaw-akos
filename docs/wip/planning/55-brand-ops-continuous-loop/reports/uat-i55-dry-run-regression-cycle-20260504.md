---
language: en
status: active
initiative: 55-brand-ops-continuous-loop
report_kind: uat
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-04
related_ops: OPS-55-1
---

# OPS-55-1 — Dry-run regression-to-advisor cycle (Initiative 55 L1–L4 baseline)

First end-to-end exercise of the regression → review → improve → maybe-send loop tooling shipped at I55 P6 + P7 (2026-05-03). This is **dry-run only**: no proposal file written; no advisor SMTP send; no `last-sent` baseline updated. Purpose: prove the rails carry signal correctly and establish the first manifest as the "last-sent" baseline candidate for future cycles.

Closes the loop-tooling-validation portion of **OPS-55-1**; remaining sub-tasks (P3 SOP-META `thi_mkt_dtp_NN` tranche, P4 ALTER, P5 composer finalize) stay forwarded.

## Three-lights summary

| Light | Signal | Status | Detail |
|:------|:-------|:------:|:-------|
| **Conversational** | Tier-A cassette replay | green | 6 / 6 cassettes PASS in 2.2s across 5 skills (`SKILL-ARCHITECT-PLAN-V1`, `SKILL-EXECUTOR-RUN-V1`, `SKILL-MADEIRA-LOOKUP-V1` × 2, `SKILL-SHARED-LOCALE-DETECT-V1`, `SKILL-VERIFIER-CHECK-V1`); overall PASS |
| **Operator** | Diff first-cycle behavior | green | `is_first_cycle: true` correctly recorded; all five families (cite_counts / scenario_deltas / judge_axes / endpoint_cost / brand_voice) emit `status: new`; baseline=null; structured manifest hash captured |
| **Surface** | Propose dispatcher contract | green | `--dry-run` (default) AND `--force-proposal --allow-first-cycle --dry-run` (demo) both emit valid decision JSON; `proposal_path: null` enforces dry-run discipline; threshold parser resolved POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1 fields cleanly |

Combined verdict: **dry-run clean; loop tooling functions end-to-end; baseline manifest established for next cycle**.

## Host environment

| Field | Value |
|:------|:------|
| Run timestamp (dossier) | `uat-dossier-20260504T174458Z` |
| Run timestamp (eval replay) | `2026-05-04T17:44:49Z` |
| Python interpreter | `3.14.2` (free-threading) |
| Eval runner | [`scripts/eval.py`](../../../../scripts/eval.py) `--mode replay --tier A` |
| Dossier renderer | [`scripts/render_uat_dossier.py`](../../../../scripts/render_uat_dossier.py) `--mode snapshot --format all --filter madeira --quiet` |
| Diff | [`scripts/regression_artifact_diff.py`](../../../../scripts/regression_artifact_diff.py) `--current artifacts/uat-dossier/uat-dossier-20260504T174458Z/manifest.json` |
| Propose (default) | [`scripts/propose_advisor_update.py`](../../../../scripts/propose_advisor_update.py) `--use-defaults --dry-run` |
| Propose (demo) | `--use-defaults --force-proposal --allow-first-cycle --dry-run` |
| FastAPI gateway | `127.0.0.1:8420` PID 18880 (live) |
| OpenClaw gateway | `127.0.0.1:18789` PID 10820 (live) |

## L1 — Tier-A cassette replay

```text
$ py scripts/eval.py --mode replay --tier A
# AKOS Eval Scorecard (v2)

- generated_at: 2026-05-04T17:44:49Z
- modes_run: replay
- overall_status: PASS
- elapsed_ms: 2244
- rows: 6

| mode   | skill_id                      | status | failures |
|:-------|:------------------------------|:-------|:---------|
| replay | SKILL-ARCHITECT-PLAN-V1       | PASS   |          |
| replay | SKILL-EXECUTOR-RUN-V1         | PASS   |          |
| replay | SKILL-MADEIRA-LOOKUP-V1       | PASS   |          |
| replay | SKILL-MADEIRA-LOOKUP-V1       | PASS   |          |
| replay | SKILL-SHARED-LOCALE-DETECT-V1 | PASS   |          |
| replay | SKILL-VERIFIER-CHECK-V1       | PASS   |          |
```

The 6 cassettes cover the 5 SKILL_REGISTRY rows currently in scope; the duplicate `SKILL-MADEIRA-LOOKUP-V1` row is the two cassettes for that skill (`hlk_search.jsonl`, `lookup_role.jsonl`). The earlier plan referenced "21 cassettes" — that count was carried from the I32 pre-rationalization wave; today's eval surface is 6 cassettes / 5 skills (see `py scripts/eval.py list`).

## L1 — Snapshot dossier render

Rendered 5 artifacts under `artifacts/uat-dossier/uat-dossier-20260504T174458Z/`:

- `dossier.md` — markdown long-form
- `dossier.html` — branded HTML
- `dossier.pdf` — WeasyPrint PDF
- `dossier-console.html` — operator console (per-section panels with raw prompts/answers/citations)
- `manifest.json` — the canonical input to `regression_artifact_diff.py`

Filter: `madeira` (Section 1 three-light surface; Section 2 cite-counts; Section 4 persona library + judge axes; Section 8 operational health; Section 11 trends).

Three-lights from this cycle's manifest:

| Light | Value |
|:------|:------|
| `light_conversational` | `AMBER` |
| `light_operator` | `GREEN` |
| `light_surface` | `GREEN` |
| `madeira_ship_go` | `false` |

Overall status: **FAIL** (expected on a fresh snapshot without the I52 multi-judge calibration burn or full live cassettes; this is the cosmetic conversational AMBER + ship-go=false combination on the snapshot mode). The dossier itself reaching **FAIL** is the loop's job to detect — and the diff captures it correctly.

## L3 — First-cycle regression diff

`regression_artifact_diff.py` ran without `--last-sent`, so `is_first_cycle: true` and every entry returns `status: new` with `delta: null`. Output JSON: `artifacts/uat-dossier/uat-dossier-20260504T174458Z/regression-diff-firstcycle.json`.

Summary block (from the diff record):

| Family | Fields compared | Fields changed | Notes |
|:-------|:---------------:|:--------------:|:------|
| `cite_counts` | 4 | 4 | total_scenarios / total_personas / total_topics / total_skills all `new` |
| `scenario_deltas` | 3 | 3 | total_scenarios / personas_outside_tolerance_count / quarantined_scenarios_count `new` |
| `judge_axes` | 7 | 4 | judge_axis_fail_brand_voice / citation / persona_fit + judge_worst_axis_fail_count `new` |
| `endpoint_cost` | — | — | empty in snapshot mode (no live endpoint probe) |
| `brand_voice` | — | 4 | light_conversational / light_operator / light_surface / madeira_ship_go captured |
| `files` | 4 | 4 | All 4 dossier files (`dossier.md`, `dossier.html`, `dossier-console.html`, `manifest.json`) recorded with `status: new` and sha256 |

## L4 — Propose dispatcher (default `--dry-run`)

```text
$ py scripts/propose_advisor_update.py --diff <…>/regression-diff-firstcycle.json --use-defaults --dry-run

  thresholds:        min_changed_scenarios=3, min_judge_axis_movement_pp=2,
                     min_register_rows_added=1, min_files_changed=2
  evaluation.metrics: {changed_scenarios=0, judge_axis_movement_pp=0.0,
                       register_rows_added=0, files_changed=4}
  evaluation.trips:  [["min_files_changed", 4, 2]]
  is_first_cycle:    true
  should_propose:    true        # threshold tripped naturally
  forced:            false
  first_cycle_explicit: false    # not relevant since should_propose already true
  proposal_path:     null        # dry-run; would write proposal-advisor-send-2026-05-04.md
```

**Insight for OPS-55-1 threshold tuning:** on a first cycle where every dossier file is `status: new`, `min_files_changed=2` will *always* trip — this is by design (the I55 P6 author chose to count new files as material). If the operator wants first-cycle silence to be the default, two clean options live in the existing POLICY surface (no code change required):

1. **Raise `min_files_changed`** in [`POLICY_REGISTER.csv`](../../../../docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv) row `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` `policy_text` to `999` (the documented suppression value) so file-count alone never trips.
2. **Add `is_first_cycle` gating** to `evaluate_thresholds()` in `propose_advisor_update.py` (small code change; would require a new test asserting first-cycle silence-by-default unless `--allow-first-cycle`).

Recommended: defer until the operator sees one or two real cycles run (after Phase H persona_scenario mirror back-fill produces real baselines). Documented as a tuning candidate; **no change made in this cycle**.

## L4 — Propose dispatcher (demo `--force-proposal --allow-first-cycle --dry-run`)

```text
$ py scripts/propose_advisor_update.py --diff <…>/regression-diff-firstcycle.json \
      --use-defaults --force-proposal --allow-first-cycle --dry-run

  forced:            true        # --force-proposal
  first_cycle_explicit: false    # threshold already tripped, so --allow-first-cycle is moot
  should_propose:    true
  proposal_path:     null        # dry-run still in force
  decision JSON returns valid render_proposal_md() input shape
```

Both flags surface in the decision JSON; render path validated by tests `test_render_proposal_md_*` in [`tests/test_propose_advisor_update.py`](../../../../tests/test_propose_advisor_update.py).

## Live-LLM cost projection footer

When the operator promotes this cycle to **Tier-B live regression** (cassettes recorded with `AKOS_RECORD_LIVE=1`), the spend envelope splits into two unit families per **D-IH-52-E** (no mixed-unit ceilings):

| Provider class | Unit | Per-cycle estimate | Source / ceiling |
|:----|:----|:----|:----|
| Per-token APIs (e.g. OpenAI / Anthropic) | USD per 1K input + 1K output tokens | ~$0.05–$0.15 across 6 cassettes (Tier-B; small dialogues) | `POL-EVAL-COST-CEILING-PER-TOKEN-*-V1` rows; `MAX_TIER_B_USD` env default $5/run |
| Per-GPU-hour endpoints (e.g. RunPod, Kalavai) | USD per GPU-hour | ~$0.10–$0.40 per cycle (5–15 minutes of endpoint warm-time) | `POL-EVAL-COST-CEILING-ENDPOINT-*-V1` rows; `config/eval/endpoint-prices.json`; `scripts/endpoint_cost_probe.py` enforces ceiling |

`scripts/endpoint_envelope_alarm.py` halts the run if either ceiling is breached. `MAX_TIER_B_USD=5.0` is the global kill-switch; the per-class ceilings are tighter than this in practice.

For *this* dry-run cycle: **$0.00 spent** — Tier-A cassette replay is fully offline; dossier snapshot is offline; diff + propose are pure-Python.

## D-IH-55-H — Loop history establishes baseline

Per the loop telemetry contract in **D-IH-55-E** (silence is also signal), this cycle gets logged. Decision log entry [D-IH-55-H](../decision-log.md) records that 2026-05-04 establishes the baseline manifest. The `manifest.json` written under `artifacts/uat-dossier/uat-dossier-20260504T174458Z/` is the candidate `--last-sent` for the next cycle's `regression_artifact_diff.py --last-sent <…>` invocation; on that run, `is_first_cycle` flips to `false` and the threshold logic runs against real deltas.

## Cross-references

- I55 master-roadmap: [docs/wip/planning/55-brand-ops-continuous-loop/master-roadmap.md](../master-roadmap.md)
- I55 decision log: [decision-log.md](../decision-log.md)
- Threshold POLICY: `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` in [`POLICY_REGISTER.csv`](../../../../docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv)
- I55 P6 closure: [reports/p6-regression-loop-tooling-2026-05-03.md](p6-regression-loop-tooling-2026-05-03.md)
- I55 P7 closure: [reports/p7-threshold-policy-2026-05-03.md](p7-threshold-policy-2026-05-03.md)
- SOP: [`SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md)
