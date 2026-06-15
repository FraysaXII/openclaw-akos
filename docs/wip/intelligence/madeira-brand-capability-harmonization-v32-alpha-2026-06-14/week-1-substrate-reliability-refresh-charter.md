# Substrate reliability refresh — tranche R1 charter

> Renamed from "Week-1" per `agent-run-timing-doctrine.md`: agent runs are **minutes**; human calendar review dates live on carryover index only.

---
intellectual_kind: research_refresh_charter
authored: 2026-06-15
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
operator_authorize: 2026-06-15 ("start week-1 refresh" → interpreted as **refresh tranche R1**)
agent_run_budget: 5-15 min per execution block
human_calendar_mint_review: carryover CO-MBH-W1 next_review_date
spine: I76 MADEIRA v3.2 closed alpha (no new initiative)
---

# Substrate reliability refresh — tranche R1 charter

## Decision this refresh feeds (Stage 1)

**D-MBH-W1-01:** What must be true in vault registries before we mint SUBSTRATE / DATA_CONTRACT / PROOF_ADAPTER rows for agent runtimes — and which methods belong in the α0 portfolio besides OpenClaw-local?

Downstream artifact: [`mint-gate-packet-draft-2026-06-15.md`](mint-gate-packet-draft-2026-06-15.md) → operator AskQuestion ratify → Stage 6 CSV tranche.

## Scope

| In scope | Out of scope |
|:---|:---|
| Windows OpenClaw scheduled-task + gateway reliability (post-reboot evidence) | Canonical CSV commit without ratify gate |
| Portable runtime comparison (LangGraph self-host, LlamaIndex worker, Cursor SDK posture) | Full LangGraph production deploy |
| PROOF_ADAPTER binding for gateway repair + check-only | α0 cohort recruitment |
| Upstream vs AKOS adapter boundary | Forking OpenClaw gateway |
| Multi-method portfolio (primary + hardening + B-path + evaluation spike) | Vault folder rename to v3.2 |

## Prongs (this refresh)

| Prong | File | Question |
|:---|:---|:---|
| **P-I** | `prong-synthesis-P-I-substrate-reliability.md` | What broke, who owns the fix, what we mint |

## Verification (R1+R2 close)

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv
```

## Tranche T1b gate (after R1+R2 research complete)

Operator ratifies mint-gate packet → AIC executes CSV tranche (SUBSTRATE gaps, DC-HOL-SUBSTRATE-ADAPTER-001, PROOF_ADAPTER gateway rows).
