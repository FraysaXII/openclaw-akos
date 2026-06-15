# I90 gateway tranche — OpenClaw local recovery (CO-90-004)

**Date:** 2026-06-14  
**Initiative:** I90 routing and wiring  
**Verdict:** PASS (post-reboot recovery confirmed 2026-06-15)

Post-reboot: first single-attempt repairs failed; **2-attempt run** succeeded (~10.5 min) via warm path (`http_ready=true`, `rpc_ready=true`). Follow-up `--check-only` also **PASS**. Evidence: `artifacts/gateway-repair-post-reboot-2026-06-15.json`.

## Outcome

The local OpenClaw gateway repair path is now a **governed tranche** instead of ad-hoc shell retries:

1. **`akos/openclaw_config.py`** — normalizes operator-local `openclaw.json` for OpenClaw 2026.4.x (`strict`→`all`, `tools.exec.host` alignment with sandbox posture and Docker availability).
2. **`akos/runtime.py`** — warm-path skip when healthy; Windows scheduled-task stop; **130s** post-ready grace (OpenClaw channel-connect); **300s** recovery budget; AIC hints (no operator netstat/taskkill).
3. **`scripts/openclaw_gateway_repair.py`** — paired runbook wired to **SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001** §4.6; **two automated attempts**; operator RACI = escalate only.
4. **`scripts/bootstrap.py`** — uses shared normalizer before writing operator config.
5. **USER_GUIDE §17** — documents repair runbook + cold-start timing.

## Verification

| Gate | Result |
|:---|:---|
| `py -m pytest tests/test_openclaw_config.py tests/test_runtime_contract.py -v` | (run at tranche close) |
| `py scripts/openclaw_gateway_repair.py --json` | (run at tranche close) |
| `py scripts/verify.py pre_commit_fast` | (run at tranche close) |

## Carryover

- **CO-90-004** → **satisfied** 2026-06-15 (post-reboot 2-attempt repair + check-only PASS).
- **CO-MBH-005** → **satisfied** (closes with CO-90-004).

## Cross-references

- Substrate audit symptoms: `docs/wip/intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md`
- I87 SOP: `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` §4.6
- P4b PWF that opened CO-90-004: `reports/uat-i90-p4b-preview-evidence-gate-2026-06-14.md`
