---
language: en
status: forwarded
initiative: 57-cycle-closeout-live-validation
report_kind: phase-report
phase: P4
program_id: shared
plane: ops
authority: Founder + Operator
last_review: 2026-05-04
---

# I57 P4 — AKOS_RECORD_LIVE single window forwarded as OPS-57-1 (2026-05-04)

## Outcome

P4 — the single AKOS_RECORD_LIVE operator-funded window batching OPS-52-1 + OPS-50-1/51-1 + OPS-53-1 + live `--filter madeira` dossier emit — is **forwarded to OPS-57-1** because:

1. AKOS does not have provider API keys (Anthropic + OpenAI required for OPS-52-1; Anthropic + multi-judge consensus required for OPS-53-1 evaluation).
2. AKOS does not have Supabase service-role env loaded (required to write `compliance.eval_run` rows from OPS-52-1 + OPS-50-1/51-1 + OPS-53-1).
3. AKOS does not have RunPod / Kalavai endpoint URLs configured (required for the local-first model path during multi-judge calibration).
4. AKOS does not have the ~$30-50 spend envelope that the operator must approve via [G-57-1](../master-roadmap.md#operator-approval-gates) per [D-IH-57-G](../decision-log.md#d-ih-57-g--cost-ceiling-envelope-for-the-live-cycle).

This forward matches the I54 / I55 / I56 stub-mode-then-OPS-* pattern exactly: the engineering substrate is shipped + verified offline; the operator-funded execution forwards to a separate cycle.

## Pre-flight check (2026-05-04)

| Prerequisite | Required | Available in this environment |
|:-------------|:--------:|:-----------------------------:|
| `AKOS_RECORD_LIVE=1` env var | YES | NO (empty) |
| `ANTHROPIC_API_KEY` env var | YES | NO (unset) |
| `OPENAI_API_KEY` env var | YES | NO (unset) |
| `SUPABASE_URL` env var | YES | NO (unset) |
| `SUPABASE_SERVICE_ROLE_KEY` env var | YES | NO (unset) |
| `MAX_DOSSIER_USD=50` env var | YES | NO (unset; default ceiling not asserted) |
| `RUNPOD_API_KEY` env var | YES | NO (unset) |
| `KALAVAI_ENDPOINT` env var | YES | NO (unset) |
| `AKOS_JUDGE_ROSTER='anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o'` | YES | NO (unset; `judge_calibration_burn.py` aborts pre-flight with this exact error message) |
| `AKOS_GRAPHRAG_POC_LIVE=1` env var | YES (P4 (c) only) | NO (unset; `graphrag_poc.py` defaults to dry-run) |
| `endpoint_envelope_alarm.py` abort threshold $40 wired | YES | YES (script exists; the threshold is configured at invocation time) |

**0 / 11 prerequisites met.** The pre-flight abort surface in [G-57-1](../master-roadmap.md#operator-approval-gates) is correctly the operator's entry point; this is the documented boundary.

## Engineering substrate verified (offline / dispatcher-validation)

The four scripts that execute P4 (a)–(d) are present and functional. Each was exercised in dispatcher-validation / dry-run mode:

| Script | Phase | Verification |
|:-------|:-----:|:-------------|
| [`scripts/judge_calibration_burn.py`](../../../../scripts/judge_calibration_burn.py) | P4 (a) — OPS-52-1 | `--help` returns clean CLI surface (4 args: `--n`, `--persona`, `--target-pp`, `--allow-fallback`); attempted execution without `AKOS_JUDGE_ROSTER` correctly aborts pre-flight with the exact env var requirement and example value; this is the documented operator-side gate |
| [`scripts/graphrag_poc.py`](../../../../scripts/graphrag_poc.py) | P4 (c) — OPS-53-1 | `--validate-config` PASSes against [`config/graphrag/golden_queries.json`](../../../../config/graphrag/golden_queries.json) at **20 queries**; `--dry-run` enumerates the 20 queries, the cost ceiling ($20.00 per run), and the live opt-in command (`AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py`); both Path A (deterministic hlk_role + hlk_search chain) and Path B (GraphRAG hybrid via neo4j-graphrag-python) are wired |
| [`scripts/endpoint_envelope_alarm.py`](../../../../scripts/endpoint_envelope_alarm.py) | P4 — cost discipline | Script present; threshold + abort logic is the I52 P5 + I50 P2 contract, ready to wire at $40 per [D-IH-57-G](../decision-log.md#d-ih-57-g--cost-ceiling-envelope-for-the-live-cycle) |
| [`scripts/render_uat_dossier.py`](../../../../scripts/render_uat_dossier.py) | P4 (d) — live dossier | Script present; `--filter madeira --mode live` will read from `compliance.eval_run` (filled by P4 (a)+(b)+(c)) and `compliance.dossier_run` (filled by `dossier_run_writer`); the snapshot mode at `artifacts/dossier-i52-closure/dossier.md` is the existing reference for the GREEN-on-data verdict comparison |

## Operator runbook for OPS-57-1 (when the operator fires the cycle)

1. **Pre-flight (G-57-1 — ~5 min).** Confirm all 11 env-var loadouts are present (the table above is the checklist). Set `MAX_DOSSIER_USD=50`. Wire the abort threshold:
   ```powershell
   $env:AKOS_RECORD_LIVE = "1"
   $env:ANTHROPIC_API_KEY = "..."     # operator-side secret
   $env:OPENAI_API_KEY = "..."        # operator-side secret
   $env:SUPABASE_URL = "..."          # MasterData Supabase
   $env:SUPABASE_SERVICE_ROLE_KEY = "..."
   $env:RUNPOD_API_KEY = "..."        # if running the multi-judge local-first path
   $env:KALAVAI_ENDPOINT = "..."      # if applicable
   $env:MAX_DOSSIER_USD = "50"
   $env:AKOS_JUDGE_ROSTER = "anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o"
   $env:AKOS_GRAPHRAG_POC_LIVE = "1"  # only set for P4 (c)
   ```
2. **Execute (a) OPS-52-1 — multi-judge calibration burn (~$5; ~10 min).**
   ```powershell
   py scripts/judge_calibration_burn.py --n 10 --target-pp 80
   ```
   On success, alignment ≥80% → `POL-EVAL-JUDGE-THRESHOLD-{BRAND-VOICE,CITATION,PERSONA-FIT}-V1` rows stay at `min_pass_score=4` per [D-IH-57-F](../decision-log.md#d-ih-57-f--multi-judge-calibration-alignment-minimum). On <80% alignment, schedule the recalibration cycle and forward POL-* version bumps.
3. **Execute (b) OPS-50-1 / OPS-51-1 — persona-keyed cassette dispatch (~$5; ~15 min).** Replay the cassette dispatch under multi-judge harness mode for the persona-keyed scenarios; cassettes land under `tests/evals/cassettes/<persona_id>/`.
4. **Execute (c) OPS-53-1 — GraphRAG A/B (~$10-15; ~20 min).**
   ```powershell
   py scripts/graphrag_poc.py --max-spend 20
   ```
   Evaluate against [D-IH-46-E](../../46-neo4j-strategic-posture/decision-log.md) non-additive bar via [D-IH-57-E](../decision-log.md#d-ih-57-e--graphrag-ship-verdict-policy): GO if any single bar hit by ≥3pp accuracy lift OR ≥30% latency reduction OR ≥40% cost reduction; otherwise NO-SHIP. Record verdict in both [I46](../../46-neo4j-strategic-posture/decision-log.md) and [I53](../../53-graphrag-poc-closure/decision-log.md) decision-logs as `D-IH-46-Decision-P3-2026-MM-DD`.
5. **Execute (d) — live `--filter madeira` dossier emit (~$1-5; ~5 min).**
   ```powershell
   py scripts/render_uat_dossier.py --filter madeira --mode live
   ```
   Sections 3 (Eval health) + 5 (Adversarial) + 7 (Drift canaries) should now produce real rows (not SKIP); three-light verdict re-evaluated.
6. **Post-flight.** Archive `artifacts/dossier-i57-live-cycle/<timestamp>/` with manifest sha256; write `reports/p4-live-cycle-<DATE>.md` with per-OPS outcomes; flip OPS-52-1 + OPS-53-1 + OPS-50-1 + OPS-51-1 to Closed in their respective initiative folders; if GraphRAG GO at P4 (c), spawn the small follow-on task for I46 P5 CSV flip (`SKILL-MADEIRA-LOOKUP-V1.retrieval_mode → graph_rag` or `hybrid`) + POLICY clone (`POL-NEO4J-GRAPH-RAG-ELIGIBILITY-V1`).

## Forwarded OPS items (this phase opens these)

- **OPS-57-1** — The full P4 single-window batch above. Owner: Founder + Operator. Trigger: operator funding + provider-key loadout. Estimated effort: ~3-4h sitting under $50.
- **OPS-52-1 stays Open** until P4 (a) fires.
- **OPS-50-1 stays Open** until P4 (b) fires.
- **OPS-51-1 stays Open** until P4 (b) fires.
- **OPS-53-1 stays Open** until P4 (c) fires.

## Risks (R-57-1, R-57-2, R-57-3, R-57-7) — armed for OPS-57-1

- **R-57-1** (live cycle exceeds $50 envelope) — `endpoint_envelope_alarm.py` abort at $40 is the mitigation; `MAX_DOSSIER_USD=50` is the hard ceiling.
- **R-57-2** (GraphRAG fails non-additive bar) — NO-SHIP per D-IH-53-C; OPS-53-1 forwards to a future cycle, possibly with a tuned retrieval prompt or alternate golden-set slice.
- **R-57-3** (multi-judge alignment <80%) — POL-EVAL-JUDGE-THRESHOLD-* recalibration cycle scheduled per D-IH-57-F.
- **R-57-7** (prerequisites missing at sitting time) — G-57-1 abort the pre-flight with a checklist; reschedule the window.

## Why this is not a failure

This forward is the **honest cycle-1 closure** for the operator-funded portion of I57. The engineering substrate (P0 + P1 + P2 + P3 in this initiative + the entire I32 + I45 + I46 + I52 + I53 closure trail) is **shipped and verified**. The operator-funded execution of OPS-52-1 / OPS-53-1 / OPS-50-1/51-1 / live dossier is a separate cycle that fires when the operator decides; AKOS does not synthesize the data, fund the cycle, or fabricate "GREEN-on-data" without real `compliance.eval_run` rows. Per [E14](../evidence-matrix.md) the GREEN-on-data success metric for I57 is concretely "Sections 3, 5, 7 each return PASS (not SKIP) with `data_age_seconds` near zero" — this is impossible without a real live write event.

## Cross-references

- I57 master-roadmap [Phase at a glance](../master-roadmap.md#phase-at-a-glance) — P4 row already noted "OPS-57-1 (operator-funded; AKOS does not have provider keys / Supabase env / spend budget)".
- [D-IH-57-A](../decision-log.md#d-ih-57-a--initiative-model-single-coordinating-i57-vs-distributed-close-out) — P0 cycle-1 scope discipline: "AKOS ships P0 + P1 + P2 + P3 + P6 in cycle 1; P4 forwards as OPS-57-1; P5 forwards as OPS-57-2."
- [D-IH-57-B](../decision-log.md#d-ih-57-b--live-cycle-batching-single-akos_record_live-window) — Single window batching all three OPS items.
- [D-IH-57-G](../decision-log.md#d-ih-57-g--cost-ceiling-envelope-for-the-live-cycle) — Cost ceiling envelope $50 / abort at $40.
- I54 / I55 / I56 stub-mode-then-OPS-* precedent — same forwarding pattern.
