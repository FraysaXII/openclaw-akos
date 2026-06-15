---
report_type: evaluation_spike
parent: langgraph-evaluation-spike-charter.md
authored: 2026-06-16
revised: 2026-06-16
verdict: PASS
ci_proof_run: https://github.com/FraysaXII/openclaw-akos/actions/runs/27520939620
ci_proof_at: 2026-06-16
substrate_id: SUBS-LANGGRAPH-OSS-SELFHOST
operator_ratify: full_recovery 2026-06-16
root_cause_source: SRC-MBH-EXT-040
---

# LangGraph OSS evaluation spike — closure report (2026-06-16, revised)

> **Functional name:** proof that a **second substrate method** (LangGraph OSS) can hit the same CAP-M outcome rows as OpenClaw for a bounded research-action loop — without replacing Scenario A primary.

## Verdict

**PASS** (re-closed 2026-06-16 after operator ratified re-close following green CI).

GitHub Actions **`langgraph-spike-smoke`** run [27520939620](https://github.com/FraysaXII/openclaw-akos/actions/runs/27520939620): real `langgraph` engine, fixture validation PASS, artifact **`langgraph-spike-evidence`** uploaded.

Prior mock-only PWF and interim FAIL are **superseded**.

## Root cause correction (2026-06-16)

| Prior (wrong) claim | Correct finding |
|:---|:---|
| "LangGraph blocked on Windows (orjson wheel)" | Shadow box runs **Python 3.14.2 only**; repo pins **3.13** (`.python-version`). **orjson has no 3.14 wheel** → `pip install langgraph` fails. LangGraph on Windows with 3.13 is **unproven here, not disproven**. |

Source: **SRC-MBH-EXT-040** (orjson PyPI + Python version RCA).

## Success criteria (charter)

| # | Criterion | Result |
|:---|:---|:---:|
| 1 | End-to-end run + evidence JSON | **PASS** — CI artifact `langgraph-spike-evidence` |
| 2 | CAP-M05 research-action on fixture | **PASS** — real graph + `validate_research_action.py` |
| 3 | CAP-M10 Langfuse `substrate_adapter_id` | **PWF** — metadata wired; CI used `--no-langfuse` |
| 4 | CAP-M21 MCP read posture node | **PASS** — read posture in real graph |
| 5 | Comparison note vs OpenClaw | **Done** — § below |

## How you observe proof (operator)

1. Push this recovery tranche to `main` (or open a PR).
2. GitHub → **Actions** → workflow **`langgraph-spike-smoke`**.
3. Green run → download artifact **`langgraph-spike-evidence`** → confirm `"engine": "langgraph"` and `"status": "PASS"`.
4. Manual re-run anytime: Actions → `langgraph-spike-smoke` → **Run workflow**.

Local Windows recovery (separate from CI): install **Python 3.13**, then `pip install -r requirements-langgraph-spike.txt` and run without `--require-langgraph` to confirm import.

## Run commands

```powershell
# Local (mock if langgraph not installed)
py scripts/langgraph_spike_run.py --json --write-artifact --no-langfuse

# CI / proof class (fails on mock)
py scripts/langgraph_spike_run.py --json --require-langgraph --no-langfuse
```

## OpenClaw vs LangGraph OSS (comparison)

| Dimension | OpenClaw (Scenario A primary) | LangGraph OSS spike |
|:---|:---|:---|
| **Dev install on shadow box** | Gateway + scheduled task; repair script | **Blocked today** — only Python 3.14 installed; need 3.13 for orjson/langgraph wheels |
| **CI proof** | `pre-commit-fast`, gateway check-only | **`langgraph-spike-smoke`** (ubuntu + 3.13 + real package) |
| **Cold start** | Post-reboot probe grace (~180s) | Real graph TBD after CI green |
| **Persistence** | Session via gateway | PostgresSaver required for prod; Memory/Sqlite in spike scope |
| **Capability parity** | CAP-M* via Cursor + gateway | Same **logical** loop; different `substrate_id` FK |

## Code + CI landed (recovery tranche)

| Path | Role |
|:---|:---|
| `akos/langgraph_spike/` | ingest → rate → synthesize → mcp_read |
| `scripts/langgraph_spike_run.py` | CLI; `--require-langgraph` for proof class |
| `requirements-langgraph-spike.txt` | Real package deps (3.11–3.13) |
| `.github/workflows/langgraph-spike-smoke.yml` | Observable proof gate |
| `tests/test_langgraph_spike.py` | Mock-safe + require-langgraph test |

## Follow-up (scheduled, not dropped)

1. PostgresSaver smoke (charter prod scope — separate carryover)
2. Promote `SUBS-LANGGRAPH-OSS-SELFHOST` from `candidate` → `pilot` (mint gate — operator CSV ratify)
3. FastAPI `/health` + `/run` wrapper (charter scope — not in spike)

Cross-ref: [`langgraph-evaluation-spike-charter.md`](../../intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/langgraph-evaluation-spike-charter.md)
