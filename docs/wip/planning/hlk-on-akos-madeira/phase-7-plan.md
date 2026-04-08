# Phase 7 Plan: Gateway and GPU Recovery Hardening (Workspace Traceability)

**Source plan**: Cursor plan `gateway_gpu_hardening_e41370d0` (2026-04-03); **not** edited in-repo — this file is the workspace mirror for execution traceability only.

**Status**: Complete — see `reports/phase-7-report.md` (full governed matrix still operator-run on target hardware).

**Program mapping**: Continuation of Phase 6 runtime remediation — Windows supervision, env-file contract clarity, GPU operator unblock runbooks.

---

## Objectives

1. **Freeze runtime contract** — `config/openclaw.json.example`, `config/environments/dev-local.json`, `scripts/legacy/verify_openclaw_inventory.py`, and docs agree on local default `ollama/deepseek-r1:14b` with `ollama/qwen3:8b` fallback; runtime does not read `*.env.example` as a source of truth.
2. **Harden Windows gateway recovery** — One supported AKOS path (`py scripts/doctor.py --repair-gateway` / `recover_gateway_service`) clears orphan listeners on `18789` after `gateway stop` and restarts via upstream OpenClaw commands.
3. **Simplify profile UX (operator-facing)** — Treat environment overlays as SSOT implementation detail; operators copy **real** `config/environments/<profile>.env` only; bootstrap seeds `~/.openclaw/.env` from `RUNTIME_ENV_PLACEHOLDERS`, not from example files.
4. **Ship GPU unblock runbooks** — Exact RunPod balance and Shadow Nova-policy checklists in `docs/uat/gpu_provider_unblock_checklist.md` with cross-links from UAT/SOP/README where appropriate.
5. **Close with governed validation** — Extend unit tests for runtime parsing/recovery; document full verification matrix in the phase report (browser UAT remains operator-evidenced).

## Asset classification

| Class | Assets |
|:------|:-------|
| Canonical | `config/openclaw.json.example`, `config/environments/*.json`, real `config/environments/*.env`, `akos/runtime.py`, `scripts/bootstrap.py`, `scripts/switch-model.py`, `scripts/doctor.py`, `scripts/legacy/verify_openclaw_inventory.py` |
| Mirrored | `~/.openclaw/openclaw.json`, `~/.openclaw/.env`, Windows Scheduled Task, RunPod/Shadow live resources |
| Reference-only | Upstream OpenClaw/Shadow/OpenStack public docs |

## Governed verification matrix (closeout)

1. `py scripts/legacy/verify_openclaw_inventory.py`
2. `py scripts/check-drift.py`
3. `py scripts/test.py all`
4. `py scripts/browser-smoke.py --playwright`
5. `py -m pytest tests/test_api.py -v`
6. `py scripts/release-gate.py`
7. `py scripts/validate_hlk.py` when HLK canonical CSVs are in scope

## Non-goals

- Replacing the environment overlay system (kept as internal SSOT glue).
- Building a second Windows service framework outside upstream OpenClaw supervision.
