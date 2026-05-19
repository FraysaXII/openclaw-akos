---
language: en
initiative_id: INIT-OPENCLAW_AKOS-78
---

# I78 — Decision log

| ID | Question | Decision |
|:---|:---|:---|
| **D-IH-78-A** | Should I78 remain TRIGGER-only without `INITIATIVE_REGISTRY` row? | **No** — operator directed mint **`INIT-OPENCLAW_AKOS-78`** as **`active`** (2026-05-17). Prior candidate posture waited on regex pushback signals; activation proceeds on execution track while **strict-mode / promotion-to-FAIL** gates remain bias-audit gated per [`_candidates/i78-brand-voice-llm-judge.md`](../_candidates/i78-brand-voice-llm-judge.md) Strand D. |
| **D-IH-78-CLOSURE** | Close I78 today at engineering-done (P1+P2) or wait for Strand C bias-audit + Strand D promotion-to-strict? | **Close at engineering-done** (Wave H lane-1, 2026-05-19) per [I86 cluster burndown plan §6 axis-2 pragmatic-closure executive call](../../86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md). P1 chassis ([`akos/brand_voice_judge.py`](../../../../akos/brand_voice_judge.py) — 7 Pydantic models + 7 type aliases) + P2 release-gate INFO advisory ([`scripts/judge_brand_voice.py --self-test`](../../../../scripts/judge_brand_voice.py)) shipped. P3 (Strand C bias audit) + P4 (Strand D `D-IH-78-PROMOTE`) + P5 (closure UAT) forward-chartered to a successor strict-mode-promotion follow-up that activates when (a) live LLM provider configured + (b) Strand C thresholds met per C-78-4. 3 executive calls recorded in [`reports/2026-05-19-closure.md`](reports/2026-05-19-closure.md) §2 (closure shape / provider scope / release-gate row category). Reversibility = single-diff at three sites; full operator override mechanism documented per §2. |

## Executive calls under D-IH-78-CLOSURE

The subagent stream (Wave H lane-1) cannot post `AskQuestion` to inline-ratify; instead each architectural choice is documented with the 4-line executive-call pattern per [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) + [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc):

1. **Closure shape — P1+P2-only with P3-P5 forward-chartered.** Operator override via reply ("reopen I78 — strand C live now" / "spin off successor initiative" / silent → default closed). Full trace at [`reports/2026-05-19-closure.md`](reports/2026-05-19-closure.md) §2.1.
2. **Provider scope — `mock`-only at P1+P2; live providers forward-chartered.** Operator override via authoring dispatch branches in `_live_provider_call` + adding API key bindings. Full trace §2.2.
3. **Release-gate row category — `INFO` advisory; not `PASS`/`FAIL`.** Operator override via single-line edit when `D-IH-78-PROMOTE` ratifies. Full trace §2.3.
