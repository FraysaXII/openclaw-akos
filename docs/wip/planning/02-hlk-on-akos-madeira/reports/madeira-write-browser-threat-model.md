# Madeira write / browser expansion — threat model (M0)

**Initiative:** `02-hlk-on-akos-madeira`  
**Date:** 2026-04-14  
**Links:** [phase-madeira-write-browser-plan.md](../phase-madeira-write-browser-plan.md), [MADEIRA_HARDENING_CONSOLIDATED_PLAN.md](../MADEIRA_HARDENING_CONSOLIDATED_PLAN.md)

---

## Scope

This document covers **incremental** widening from read-only Madeira toward Executor-led write/browser flows. Read-only closure remains the baseline record; expansion is additive and HITL-governed.

## Threats and mitigations

| Threat | Impact | Mitigation |
|:-------|:-------|:-----------|
| Prompt injection drives mutating tools on Madeira | Data loss, repo tampering, SOC incident | Gateway **deny** for `write`, `edit`, `apply_patch`, `exec`; no coarse `browser` on Madeira; only **read-only** observation tools (`browser_snapshot`, `browser_screenshot`) in template + `agent-capabilities.json`; mutating paths remain Executor + HITL per D-MWB-1 |
| Browser SSRF / internal network probe | Lateral movement from agent runtime | `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork: false` (unchanged); snapshot/screenshot still subject to gateway MCP policy |
| Capability drift between AKOS matrix and live `openclaw.json` | Silent tool widen | `scripts/bootstrap.py`, `scripts/check-drift.py`, `/agents/{id}/policy`, `scripts/doctor.py` gateway tool checks |
| Over-broad Langfuse metadata | Compliance / SOC exposure | `LangfuseTraceContext` + coercion in `akos/telemetry.py`; no transcripts or CSV payloads in metadata |
| Operator confusion on lanes | Weak UAT signal | Maintain ≥2 Lane B model notes in `madeira-readonly-hardening.md`; Langfuse tags for observability |

## HITL / UX note

Any future **write** or **navigate/click** browser class on Madeira must remain **off** unless a product decision revises D-MWB-1 with inventory tests and UAT. Operators escalate multi-step or mutating work through `execution_escalate` / Orchestrator → Executor with explicit approval gates.

## Verification

On changes to gateway SSOT: full matrix per [DEVELOPER_CHECKLIST.md](../../../../docs/DEVELOPER_CHECKLIST.md) (`verify_openclaw_inventory.py`, `check-drift.py`, `test.py all`, `pytest tests/test_api.py`, `release-gate.py`, `validate_hlk.py` when HLK assets change).
