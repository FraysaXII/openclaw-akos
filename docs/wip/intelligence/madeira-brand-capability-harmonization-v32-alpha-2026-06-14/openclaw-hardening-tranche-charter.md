---
authored: 2026-06-15
initiative: I87/I90
parent: prong-synthesis-P-I-substrate-reliability.md
status: scheduled
---

# OpenClaw hardening tranche — post R1 refresh

> **Functional name:** make the **primary Windows adapter** more deterministic without forking OpenClaw. Pairs with SOP §4.6; feeds mint gate PROOF_ADAPTER rows.

## Motivation

Upstream issues (SRC-MBH-EXT-027..030) + post-reboot evidence show **timing** and **probe semantics** dominate PASS/FAIL. AKOS can harden without waiting for upstream release.

## Proposed mechanical changes (AIC)

| # | Change | File |
|:---:|:---|:---|
| H1 | Increase RPC probe timeout on Windows during check-only wait loop (20s → 45s) | `akos/runtime.py` |
| H2 | Treat HTTP 200 on `/` as sufficient for warm path when RPC still in channel-connect grace | `akos/runtime.py` |
| H3 | Log repair outcome summary to Langfuse (trace id in JSON artifact) | `scripts/openclaw_gateway_repair.py` |
| H4 | `openclaw --version` pin check in repair preflight; warn if below known fix release | `akos/runtime.py` |
| H5 | Document upstream issue IDs in SOP §4.6 cross-links | SOP touch |

## Verification

```powershell
py -m pytest tests/test_runtime_contract.py -v
py scripts/openclaw_gateway_repair.py --check-only --json
```

## Proof binding (mint gate)

- `proof-openclaw-check-only-post-reboot` — must PASS within 180s after simulated reboot (manual UAT note)
- Langfuse trace optional until H3 lands

## Operator role

None for execution. Ratify tranche start if you want H1–H5 in one commit vs split H3/H4 to Week-3.

**Posture:** **Scheduled** — starts after mint tranche T1b ratify unless you say "execute hardening now."
