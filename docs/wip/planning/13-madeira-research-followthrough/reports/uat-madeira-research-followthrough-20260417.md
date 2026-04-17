# UAT — Initiative 13 MADEIRA research follow-through

**Date:** 2026-04-17  
**Scope:** Automated verification + qualitative WebChat spot-check (optional).

SOC: no API keys, bearer tokens, or full prompts.

## Summary

| Area | Result | Notes |
|:-----|:-------|:------|
| Intent golden + regex tests | **PASS** | `py -m pytest tests/test_intent.py tests/test_intent_golden.py -v` |
| Prompt contracts | **PASS** | `py -m pytest tests/validate_prompts.py -v` |
| `intent_benchmark.py` | **PASS** | Routing table produced; embedding path when Ollama up |
| Full repo gates | **PASS** | See phase 4 execution (`release-gate`, etc.) |

## Qualitative WebChat (before / after)

| Step | Before | After | Notes |
|:-----|:-------|:------|:------|
| Escalation copy mentions Orchestrator + dashboard + Path 3 | N/A (prior copy) | **PASS (spec)** | `_ROUTE_MESSAGES` + `MADEIRA_BASE.md` / overlay |
| Operator paths 1–4 in Madeira prompt | Partial | **PASS (spec)** | `prompts/base/MADEIRA_BASE.md` |
| Live WebChat transcript review | — | **SKIP** | Not run in this session; operators may repeat scenarios from [`docs/uat/hlk_admin_smoke.md`](../../../uat/hlk_admin_smoke.md) |

Cross-reference: [`doc-accuracy-20260417.md`](doc-accuracy-20260417.md), [`intent-benchmark-20260417-after.md`](intent-benchmark-20260417-after.md).
