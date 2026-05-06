---
language: en
status: active
initiative: 58-cycle-2-multi-track-forward
report_kind: phase-report
phase: A.0
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-05
---

# I58 A.0 — G-58-1 pre-flight script + first invocation (2026-05-05)

## Outcome

A.0 substrate **shipped**: new [`scripts/preflight_g58_1.py`](../../../../scripts/preflight_g58_1.py) (216 LOC) + 14 regression tests in [`tests/test_preflight_g58_1.py`](../../../../tests/test_preflight_g58_1.py) (all PASS). First live invocation in this AKOS environment returns **4 / 11 prerequisites met → G-58-1 NO-FIRE**, identical in shape to the I57 P4 forward state but with three additional `OK` rows (Supabase URL literal, alias-seam canonical names, alarm script presence) thanks to the long-lived block P0 wrote into `~/.openclaw/.env`.

Per D-IH-58-B, this means **A.1, A.2, A.3, A.4 forward as OPS-58-1** for this cycle. A.5 stays gated on A.3.

## Artifact: `scripts/preflight_g58_1.py`

Read-only script that:

1. Loads `~/.openclaw/.env` into `os.environ` via `akos.io.bootstrap_openclaw_process_env()` (the canonical entry-point used by `serve-api.py` and the eval harness CLI).
2. Evaluates 11 deterministic checks against the loaded environment.
3. Prints a stable-shape table (13 lines: 1 header + 1 separator + 11 data rows) + a one-line verdict.
4. Returns 0 (G-58-1 GREEN) or 1 (G-58-1 NO-FIRE); reserves 2 for script-internal failure.

The script never authors secret values (D-IH-58-F / D-IH-17 invariance) — it only reads `os.environ`. Operator pastes values into the empty placeholders P0 wrote into `~/.openclaw/.env`.

### The 11 checks

| # | Prerequisite | Required | Failure mode |
|:-:|:-------------|:---------|:-------------|
| 1 | `AKOS_RECORD_LIVE` | `=1` (truthy: `1`/`true`/`yes` case-insensitive) | `0` is rejected — operator can't accidentally fire the cycle |
| 2 | `ANTHROPIC_API_KEY` | set; non-empty | unset or whitespace-only |
| 3 | `OPENAI_API_KEY` | set; non-empty | unset or whitespace-only |
| 4 | `SUPABASE_URL` | set; non-empty | unset (P0 wrote literal value `https://swrmqpelgoblaquequzb.supabase.co`) |
| 5 | `SUPABASE_SERVICE_ROLE_KEY` | set; non-empty (operator-pasted; service-role JWT, not anon) | unset or whitespace-only |
| 6 | `MAX_DOSSIER_USD` | set; integer; positive; ≤50 (D-IH-57-G ceiling) | unset, non-integer, non-positive, or above ceiling |
| 7 | `VLLM_RUNPOD_URL` OR `RUNPOD_ENDPOINT_URL` | at least one set (D-IH-58-G alias seam) | both unset |
| 8 | `VLLM_SHADOW_URL` OR `KALAVAI_ENDPOINT_URL` | at least one set (D-IH-58-G alias seam) | both unset |
| 9 | `AKOS_JUDGE_ROSTER` | set; contains both `anthropic` AND `openai` provider entries | unset or single-provider |
| 10 | `AKOS_GRAPHRAG_POC_LIVE` | `=1` (truthy) — A.3 only | unset or non-truthy (A.3 falls back to dry-run) |
| 11 | `scripts/endpoint_envelope_alarm.py` | present (abort-at-$40 wired at invocation time) | script missing |

### Test coverage (14 tests, all PASS)

```text
test_evaluate_checks_returns_exactly_11_results   PASS
test_clean_env_reports_all_misses                  PASS
test_full_env_returns_zero                         PASS
test_main_returns_one_on_any_miss                  PASS
test_max_dossier_usd_above_ceiling_fails           PASS
test_max_dossier_usd_non_integer_fails             PASS
test_max_dossier_usd_within_ceiling_passes         PASS
test_runpod_alias_seam_resolves_either_name        PASS  <- D-IH-58-G alias seam
test_kalavai_alias_seam_resolves_either_name       PASS  <- D-IH-58-G alias seam
test_runpod_both_unset_fails                       PASS
test_truthy_parsing_rejects_zero                   PASS
test_judge_roster_requires_both_providers          PASS
test_judge_roster_truthy_with_both_providers       PASS
test_render_table_lists_all_eleven                 PASS
```

Pytest summary: `14 passed in 0.15s`. Test count delta: +14 (target ≥1770 at E.0 closure).

## First live invocation (2026-05-05, AKOS environment)

```text
  G-58-1 pre-flight check (Initiative 58 Phase A / OPS-58-1)
  D-IH-58-B + D-IH-58-F + D-IH-58-G inherit D-IH-57-G envelope

  Prerequisite                             Status   Detail
  ---------------------------------------  -------  ------
  AKOS_RECORD_LIVE                         MISS     value=None
  ANTHROPIC_API_KEY                        MISS     unset / empty
  OPENAI_API_KEY                           MISS     unset / empty
  SUPABASE_URL                             OK       set
  SUPABASE_SERVICE_ROLE_KEY                MISS     unset / empty
  MAX_DOSSIER_USD                          MISS     unset
  VLLM_RUNPOD_URL or RUNPOD_ENDPOINT_URL   OK       VLLM_RUNPOD_URL set
  VLLM_SHADOW_URL or KALAVAI_ENDPOINT_URL  OK       VLLM_SHADOW_URL set
  AKOS_JUDGE_ROSTER                        MISS     unset
  AKOS_GRAPHRAG_POC_LIVE                   MISS     value=None
  endpoint_envelope_alarm.py               OK       present: scripts/endpoint_envelope_alarm.py

  Result: 4 / 11 prerequisites met
  G-58-1 NO-FIRE — reschedule the window per R-58-1 + R-58-cycle2-A.
```

**Comparison to I57 P4 forward (2026-05-04):**

| Metric | I57 P4 forward | I58 A.0 first run | Delta |
|:-------|:--------------:|:-----------------:|:-----:|
| Prerequisites met | 0 / 11 (1 of 11 was script-side ready) | 4 / 11 | **+3 OK rows** |
| Supabase URL | unset | OK (P0 literal value) | improved |
| RunPod / Kalavai URLs | unset | OK (canonical `VLLM_*` names) | improved |
| Alarm script present | implicit only | OK (explicit check row) | surfaced |
| Operator-paste prerequisites missing | 11 | 7 | reduced by 4 |

The improvement is structural, not data: P0 supplied the Supabase URL literal value (per D-IH-58-F: agent writes structure) and the alias seam (D-IH-58-G) means the existing `VLLM_RUNPOD_URL` + `VLLM_SHADOW_URL` already satisfy checks 7 and 8 without operator action. The 7 remaining MISS rows are all operator-paste-required and intentionally so (provider keys + Supabase service-role + Phase A flags + judge roster + cost ceiling).

## Forward consequences for A.1–A.4

Per D-IH-58-B + R-58-1 documented response, A.1 → A.4 forward as **OPS-58-1**. The runbook is OPS-57-1's verbatim (per D-IH-58-A coordinating-initiative model):

1. Operator pastes 7 missing values into `~/.openclaw/.env`:
   - `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
   - `MAX_DOSSIER_USD=50` (or lower per D-IH-57-G ceiling)
   - `AKOS_JUDGE_ROSTER=anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o`
   - `AKOS_RECORD_LIVE=1` (uncomment the existing line)
   - `AKOS_GRAPHRAG_POC_LIVE=1` (uncomment the existing line)
2. Operator runs `py scripts/preflight_g58_1.py` again. Expected: `Result: 11 / 11 prerequisites met. G-58-1 GREEN.`
3. Operator restarts gateway with the new env: `py scripts/serve-api.py --no-graph-explorer`. Confirms `/health` returns Anthropic + OpenAI active and Supabase URL set.
4. Operator wires `endpoint_envelope_alarm.py --abort-at 40` and fires A.1 → A.2 → A.3 → A.4 in sequence:
   - A.1: `py scripts/judge_calibration_burn.py --live --persona founder --n 50 --target-pp 80`
   - A.2: persona-keyed cassette dispatch under multi-judge harness for ≥2 personas (record-mode under `AKOS_RECORD_LIVE=1`)
   - A.3: `py scripts/graphrag_poc.py --live --max-spend 20 --golden-set`
   - A.4: `py scripts/render_uat_dossier.py --filter madeira --mode live`
5. Operator captures outcomes in `reports/a1-judge-burn-2026-MM-DD.md`, `reports/a2-cassettes-2026-MM-DD.md`, `reports/a3-graphrag-2026-MM-DD.md`, `reports/a4-live-dossier-2026-MM-DD.md` per the I58 master-roadmap success metrics.

If the operator does not fire by E.0, A.* re-forwards with this runbook unchanged.

## Why the agent cannot self-load the missing keys

Identical to I57: provider keys are off-repo identity material; Supabase service-role is a privileged write credential that must originate from an operator context for `compliance.eval_run` audit parity; spend authorization is an operator decision. Per D-IH-58-F (D-IH-17 invariance) the agent never authors secret values. This is the documented design boundary, not a missing capability.

## Verification (A.0 only — substrate ready)

| Check | Command | Result |
|:------|:--------|:-------|
| Script exists, `--help`-clean | `py scripts/preflight_g58_1.py --help` (currently no flags) | n/a — script accepts argv but doesn't parse flags yet (reserved for future `--json` / `--fail-soft`) |
| Script runs without import errors | `py scripts/preflight_g58_1.py` | PASS (exits 1 = NO-FIRE; expected) |
| Regression tests | `py -m pytest tests/test_preflight_g58_1.py -v` | **14 passed in 0.15s** |
| HLK validator | `py scripts/validate_hlk.py` | PASS (159 frontmatter / 0 errors) |
| Vault links | `py scripts/validate_hlk_vault_links.py` | PASS |
| Dashboard determinism | `py scripts/render_wip_dashboard.py --check-only` | PASS (sha256 stable) |

## Cross-references

- I57 P4 forward (the OPS-57-1 origin runbook): [`p4-live-cycle-forward-2026-05-04.md`](../57-cycle-closeout-live-validation/reports/p4-live-cycle-forward-2026-05-04.md)
- I57 OPS-57-1 env recheck (the 0/11 baseline): [`ops-57-1-env-recheck-2026-05-04.md`](../57-cycle-closeout-live-validation/reports/ops-57-1-env-recheck-2026-05-04.md)
- D-IH-58-B (OPS-57-1 inside Phase A): [`decision-log.md`](../decision-log.md#d-ih-58-b--ops-57-1-fires-inside-i58-phase-a-not-detached)
- D-IH-58-F (env enrichment is operator-driven): [`decision-log.md`](../decision-log.md#d-ih-58-f--openclawenv-enrichment-is-operator-driven-d-ih-17-invariance)
- D-IH-58-G (RunPod/Kalavai alias seam): [`decision-log.md`](../decision-log.md#d-ih-58-g--runpodkalavai-env-var-alias-seam-no-rename)
- D-IH-57-G (cost ceiling envelope): [`../57-cycle-closeout-live-validation/decision-log.md`](../57-cycle-closeout-live-validation/decision-log.md#d-ih-57-g--cost-ceiling-envelope-for-the-live-cycle)
- R-58-1 (live cycle exceeds envelope): [`risk-register.md`](../risk-register.md)
- R-58-cycle2-A (first five-track coordinating initiative): [`risk-register.md`](../risk-register.md#cycle-2-specific-risks)
