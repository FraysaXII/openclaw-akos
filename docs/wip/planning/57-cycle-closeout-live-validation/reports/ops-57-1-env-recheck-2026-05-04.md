---
language: en
status: forwarded
initiative: 57-cycle-closeout-live-validation
report_kind: ops-recheck
phase: P4-followup
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-04
---

# OPS-57-1 — environment recheck + operator-action gap (2026-05-04, post-closure)

## Outcome

**OPS-57-1 remains forwarded.** A second pass through the [G-57-1 pre-flight checklist](../master-roadmap.md#operator-approval-gates) in this AKOS environment finds **0 / 11 prerequisites met** — identical to the I57 P4 forward state. The agent cannot execute the `AKOS_RECORD_LIVE` window from this environment because:

1. None of the four required provider keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `RUNPOD_API_KEY`, `KALAVAI_ENDPOINT`) are loaded in the current shell.
2. None of the two required Supabase env vars (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`) are loaded.
3. The cycle-control flags (`AKOS_RECORD_LIVE=1`, `AKOS_GRAPHRAG_POC_LIVE=1`, `AKOS_JUDGE_ROSTER`, `MAX_DOSSIER_USD=50`) are not set.
4. There is no `.env` file at the repo root from which the gateway / scripts could load these on startup.

This is **not a regression** — it matches what the I57 P4 forward report already documented. This recheck confirms the gap is stable and that no operator action has occurred between I57 closure and this follow-up cycle.

## Pre-flight checklist (recheck 2026-05-04, post-closure)

| Prerequisite | Required | Available in this environment | Source of truth |
|:-------------|:--------:|:-----------------------------:|:----------------|
| `AKOS_RECORD_LIVE=1` | YES | NO (empty) | `os.environ.get("AKOS_RECORD_LIVE")` |
| `ANTHROPIC_API_KEY` | YES | NO (unset) | `os.environ.get("ANTHROPIC_API_KEY")` |
| `OPENAI_API_KEY` | YES | NO (unset) | `os.environ.get("OPENAI_API_KEY")` |
| `SUPABASE_URL` | YES | NO (unset) | `os.environ.get("SUPABASE_URL")` |
| `SUPABASE_SERVICE_ROLE_KEY` | YES | NO (unset) | `os.environ.get("SUPABASE_SERVICE_ROLE_KEY")` |
| `MAX_DOSSIER_USD=50` | YES | NO (unset; default ceiling not asserted) | `os.environ.get("MAX_DOSSIER_USD")` |
| `RUNPOD_ENDPOINT_URL` | YES | NO (unset) | `os.environ.get("RUNPOD_ENDPOINT_URL")` |
| `KALAVAI_ENDPOINT_URL` | YES | NO (unset) | `os.environ.get("KALAVAI_ENDPOINT_URL")` |
| `AKOS_JUDGE_ROSTER` | YES | NO (unset; `judge_calibration_burn.py` aborts pre-flight with the exact env var requirement) | `os.environ.get("AKOS_JUDGE_ROSTER")` |
| `AKOS_GRAPHRAG_POC_LIVE=1` | YES (P4 (c) only) | NO (unset; `graphrag_poc.py` defaults to dry-run) | `os.environ.get("AKOS_GRAPHRAG_POC_LIVE")` |
| `endpoint_envelope_alarm.py` abort threshold $40 wired | YES | YES (script exists; threshold is configured at invocation time, no env precondition) | [`scripts/endpoint_envelope_alarm.py`](../../../../scripts/endpoint_envelope_alarm.py) |
| `.env` at repo root with above values | OPTIONAL — not required if vars are exported in the calling shell | NO `.env` present | `Test-Path .env` |

**Result: 0 / 11 prerequisites met (1 of 11 is "script-side ready" — `endpoint_envelope_alarm.py` exists; the remaining 10 are env-bound and would require operator action).**

Per [R-57-7](../master-roadmap.md#risks-r-57-1-through-7) (`AKOS_RECORD_LIVE prerequisites missing at sitting time`) the documented response is "abort pre-flight via G-57-1 checklist; reschedule the window". This recheck is that abort + reschedule cycle re-fired with no new evidence.

## Why the agent cannot self-load the missing keys

- **Provider keys are off-repo identity material.** They live in the operator's secret store (or environment-local `.env` outside the repo per `.gitignore`); the agent has no read path to that store and no permission to fabricate them.
- **Supabase service-role key is a privileged write credential.** Even if the agent could somehow read it, executing the live cycle from a non-operator context would violate the one-operator-per-cycle audit assumption that `compliance.eval_run` mirror parity depends on.
- **Spend authorization is an operator decision.** The ~$30-50 envelope under `MAX_DOSSIER_USD=50` (per [D-IH-57-G](../master-roadmap.md#d-ih-57-g--cost-ceiling-envelope-for-the-live-cycle)) is the operator's budget call; auto-firing it would breach [G-57-1](../master-roadmap.md#operator-approval-gates).

This is the documented design boundary, not a missing capability — the I57 P4 forward existed precisely because the live cycle is operator-initiated by definition.

## What the operator can do to fire OPS-57-1

The full runbook lives in [`p4-live-cycle-forward-2026-05-04.md`](p4-live-cycle-forward-2026-05-04.md) §"Operator runbook". In short:

1. **Load env**: export all 10 missing env vars (provider keys + Supabase + cycle flags + cost ceiling) into a single shell session.
2. **Restart gateway** with that env: `py scripts/serve-api.py --no-graph-explorer` and confirm `/health` returns the loaded provider list (Anthropic + OpenAI active, Supabase URL set).
3. **Run [G-57-1](../master-roadmap.md#operator-approval-gates) pre-flight**: confirm `endpoint_envelope_alarm.py` is wired to abort at $40, confirm budget intent in YAML or commit message.
4. **Fire the four sub-steps** under one envelope:
   - **P4 (a)** — `py scripts/judge_calibration_burn.py --live --persona founder --n 50`.
   - **P4 (b)** — record-mode cassette dispatch via the standard Madeira cassette flow under `AKOS_RECORD_LIVE=1`.
   - **P4 (c)** — `py scripts/graphrag_poc.py --live --golden-set` (only if `AKOS_GRAPHRAG_POC_LIVE=1`).
   - **P4 (d)** — `py scripts/render_uat_dossier.py --filter madeira --mode live` and capture the manifest sha256.
5. **Capture outcomes** in `reports/uat-akos-record-live-cycle-<DATE>.md` per the I57 master-roadmap success metrics.

If the operator wants the agent to drive steps 1–5 from inside this session, the operator must first load the env vars into the shell that runs the agent, then re-prompt; the agent will pick up the loaded env via `os.environ` and re-evaluate this checklist.

## Verification (recheck only — no live cycle fired)

| Check | Command | Result |
|:------|:--------|:-------|
| Env var probe | PowerShell `[System.Environment]::GetEnvironmentVariable($name)` for all 11 vars | **0 / 11 set** (matches I57 P4 forward report) |
| `.env` presence | `Test-Path .env` | **`False`** (no .env file at repo root) |
| Engineering substrate intact | (see [`p4-live-cycle-forward-2026-05-04.md`](p4-live-cycle-forward-2026-05-04.md) §"Engineering substrate verified") | All four scripts (`judge_calibration_burn.py`, `graphrag_poc.py`, `render_uat_dossier.py`, `endpoint_envelope_alarm.py`) present and `--help`-clean. No regression since I57 closure. |

## Cross-references

- I57 P4 forward (the original OPS-57-1 ticket): [`p4-live-cycle-forward-2026-05-04.md`](p4-live-cycle-forward-2026-05-04.md) — full runbook + per-step success criteria.
- I57 P6 closure UAT (which preserved OPS-57-1 as the forward residual): [`uat-i57-cycle-closeout-2026-05-04.md`](uat-i57-cycle-closeout-2026-05-04.md).
- D-IH-57-G (cost ceiling): [`../master-roadmap.md#d-ih-57-g--cost-ceiling-envelope-for-the-live-cycle`](../master-roadmap.md#d-ih-57-g--cost-ceiling-envelope-for-the-live-cycle).
- G-57-1 (operator approval gate): [`../master-roadmap.md#operator-approval-gates`](../master-roadmap.md#operator-approval-gates).
