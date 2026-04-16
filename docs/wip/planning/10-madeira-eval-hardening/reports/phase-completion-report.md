# Phase completion report — Initiative 10 (Madeira Path B+C, eval harness)

**Date:** 2026-04-15  
**Status:** closed on `main` (post-push verification on this date).

## Scope delivered (decision log → artifacts)

| ID | Outcome |
|:---|:--------|
| **D-B** | `config/openclaw.json.example`: `agents.defaults.sandbox.mode: strict`, `tools.exec.host: sandbox`; `akos.models` `SandboxDefaults` / `ExecConfig.host` default `sandbox`; USER_GUIDE / SECURITY / `scripts/doctor.py` Windows Docker/WSL guidance. |
| **D-C** | Orchestrator and Architect `alsoAllow` drop `web_search` / `web_fetch`; Architect keeps `browser`; prompts and USER_GUIDE research spine. |
| **D-UI** | `gateway.controlUi` removed from SSOT; optional `GatewayConfig.controlUi` in models where applicable. |
| **D-EVAL** | `akos/eval_harness.py`, `tests/evals/suites/pathc-research-spine/`, `scripts/run-evals.py` (`list` / `run`, `--trials`, rubric + dry-run), `LangfuseTraceContext` / `trace_eval_outcome` eval metadata including `research_surface`; `tests/test_eval_harness.py`; `py scripts/test.py evals`; optional `AKOS_EVAL_RUBRIC=1` in `scripts/release-gate.py`. |

## Deferred / non-goals (roadmap appendices)

- **Tier B live evals:** Still operator/gateway-worker scoped; `run-evals.py --mode live` remains a stub path for CI (see `tests/evals/README.md`).
- **Appendix D (lanes α–η):** Codenames stay outside repo SSOT per master-roadmap.

## Verification (governed matrix subset)

Executed from repo root after final doc updates:

- `py scripts/test.py all` — PASS  
- `py scripts/release-gate.py` — PASS  

Full matrix remains as in [`DEVELOPER_CHECKLIST.md`](../../../../../DEVELOPER_CHECKLIST.md) (inventory verify, drift, browser-smoke with Playwright, `test_api`, HLK validators when assets change).
