---
title: I90 P4b — Preview slice prep (mechanical gate)
last_review: 2026-06-14
audience: J-OP;J-AIC
status: in_progress
carryover_posture: scheduled
activation_trigger: Gateway + hlk-erp Preview deploy reachable (CO-90-001)
linked_decisions:
  - D-IH-90-AF
verdict: BLOCKED-ENV
---

# P4b prep — mechanical proof path (2026-06-14)

**Carryover posture:** scheduled (not dropped) — `CO-90-001`. P4a+ singularity tranche committed (`32521d2f`).

## Prerequisites satisfied

| Gate | Result |
|:---|:---|
| P4c+ vault + DATA contracts landed | **PASS** — commit `32521d2f` |
| PRECEDENCE rows for evidence registries | **PASS** — index backfill this session |
| `lab_platform_registry_reconcile.py --self-test` | **PASS** (8 Vercel rows) |
| `run_automated_uat_evidence_sweep.py --self-test` | **PASS** (exit 0) |
| `validate_hlk.py` | **PASS** (pre-commit on P4c+ tranche) |

## Blocked on environment (browser experiential slice)

| Step | Result | Notes |
|:---|:---|:---|
| AKOS gateway / dashboard smoke | **SKIP** (14/14) | `browser-smoke.py --playwright` — gateway unreachable |
| hlk-erp Preview deploy | **Not run** | Requires Vercel Preview + operator auth |
| Browser manifest `browser_experiential` | **Not run** | Target: `artifacts/uat-screenshots/i96-preview-*` |

**Verdict:** `BLOCKED-ENV` — not a doctrine gap; local gateway down blocks steps 1 and 4 of the critical path in [`evidence-class-gate-phase-b-preview-slice-2026-06-14.md`](evidence-class-gate-phase-b-preview-slice-2026-06-14.md).

## Operator unblock checklist

1. Start AKOS gateway (or confirm `openclaw.json` listener healthy).
2. Confirm hlk-erp Preview URL from `VERCEL_PROJECT_SETTINGS_REGISTRY.csv` row for consumer repo.
3. Re-run deploy-health craft steps 1–4 on Preview host.
4. Capture browser journey → `artifacts/uat-screenshots/i96-preview-evidence-gate-2026-06-14/` with `MANIFEST.json`.
5. Close supplement with `evidence_class: browser_experiential` + `evidence_proof_ref` path.

## Commands (when unblocked)

```powershell
py scripts/browser-smoke.py --playwright
py scripts/lab_platform_registry_reconcile.py
py scripts/run_automated_uat_evidence_sweep.py
```

## Cross-references

- Singularity ratification: [`evidence-class-gate-singularity-ratification-2026-06-14.md`](evidence-class-gate-singularity-ratification-2026-06-14.md)
- I96 production UAT context: `docs/wip/planning/96-research-data-plane-and-research-center/reports/uat-i96-research-center-production-2026-06-14.md`
