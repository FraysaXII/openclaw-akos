---
authored: 2026-06-15
status: wip_spec
control_confidence: Keter
parent: context-economics-wip-spec-outline.md
tranche: T2_implementation_after_ratify
---

# Context economics — WIP specification (T0 expanded)

> **Functional name:** the rulebook for how MADEIRA spends context (tokens, cache, compaction, postprocessing) so the operator can read cost and trust on the surface — not inside three initiatives.  
> Closes **GAP-MBH-01** (cache/compaction) and **GAP-MBH-02** (postprocessing). Implementation remains **T2**; this spec is the T0 ratify target.

## 1. Problem statement (plain language)

Holistika already **ingests and trusts** research (source ledger, KiRBe, Research Center). What we do not yet **govern** is:

- Which parts of a prompt may be **cached** vs must stay dynamic
- When a long IDE session **compacts** without losing ratify decisions
- What the operator **sees** after the model speaks (brand lint, citations, PII gate)

Without this, α0 cannot claim **metered context** (BT-12 Option 6).

## 2. Scope boundary

| In scope (α0) | Out of scope (post-α0) |
|:---|:---|
| Cursor-local Scenario A prompt assembly contract | Full vault-wide prompt template registry |
| Research Center panel context budgets (read-only signals) | Real-time budget enforcement blocking sessions |
| Langfuse fields for cache + scenario tags | Multi-tenant cost allocation (Scenario D) |
| Minimal `akos/postprocess.py` hook for agent output | Full ENVOY channel render pipeline |

## 3. Prompt assembly contract

### 3.1 Layer stack (static → dynamic)

| Layer | Content | Cache | Owner |
|:---:|:---|:---:|:---|
| L0 | Mode + audience resolution (Quality Fabric) | No | I76 |
| L1 | System / doctrine slice (mode-aware) | **Yes** — breakpoint 1 | Cursor rules + vault slice |
| L2 | Tool schemas + MCP descriptors | **Yes** — breakpoint 2 | I79 MCP posture |
| L3 | KiRBe / vault retrieval chunk | Optional breakpoint 3 | I83 / I96 |
| L4 | Session memory + user turn + tool results | No | OpenClaw / adapter |

### 3.2 Rules

1. **Minimum cacheable prefix** ≥ provider minimum (typically 1024 tokens) before breakpoint 3.
2. **Doctrine changes** invalidate L1 cache (version tag in `MADEIRA_AIC_PER_TASK` row).
3. **Tool schema changes** invalidate L2 (inventory hash from `openclaw.json` or adapter equivalent).
4. Every assembled prompt logs `substrate_adapter_id` + `alpha_scenario` to Langfuse.

## 4. Compaction policy

Per **MADEIRA_AIC_PER_TASK_REGISTRY** extension (proposed columns):

| Column | Purpose |
|:---|:---|
| `max_turns_before_compact` | Task-class specific (research vs execution) |
| `compact_preserve_fields` | decision_id, source_id, ratify_outcome, carryover_id |
| `compact_drop_policy` | hash-dedupe tool stdout; never drop ledger citations |

**Default posture:** research-action sessions preserve **all source IDs**; execution tranches may compact tool noise after validator PASS.

## 5. Postprocessing pipeline (minimal α0)

Proposed module: `akos/postprocess.py` (T2) — ordered chain:

1. **Citation gate** — research surfaces must reference SRC-* or canonical path
2. **Brand lint** — `lint_brand_voice_offline.py` (existing)
3. **Secret/PII gate** — existing hooks; no new framework
4. **Channel truncate** — optional; ENVOY adapters only

Failure → surface to operator as **governed block**, not silent strip.

## 6. Telemetry + finops join

### Langfuse trace fields (extend existing reporter)

- `cache_read_tokens`, `cache_write_tokens`
- `alpha_scenario`, `alpha_cohort` (internal α0 = `scenario_a_internal`)
- `substrate_adapter_id` (FK to SUBSTRATE_REGISTRY post-mint)
- `economic_consumer` (BI-MADEIRA-DOSSIER proposal)

### Finops roll-up

Session cost → FINOPS counterparty via provider ID; cache savings → dossier **cost avoidance** line (not revenue).

Cross-link: `infonomics-substrate-join-2026-06-14.md` (DG-B).

## 7. Capability matrix linkage

| CAP ID | This spec closes |
|:---|:---|
| CAP-M16 | Prompt/cache boundary policy |
| CAP-M17 | Postprocessing pipeline |
| CAP-M18 | Compaction policy (partial; OpenClaw upstream for runtime) |
| CAP-M15 | Economic signal visible when joined to Research Center freshness strip |

## 8. Verification (T2 gate)

```powershell
py -m pytest tests/test_postprocess.py -v          # after module lands
py scripts/render_uat_dossier.py --filter madeira  # cost + cache line visible
py scripts/validate_research_action.py ...         # unchanged
```

## 9. Operator ratify target (T0 → T1)

Before T2 code: operator confirms layer stack + compaction preserve list + dossier cost line mockup.

**Carryover:** CO-MBH-001, CO-MBH-002 — **scheduled** until T2; spec satisfaction unblocks ratify gate.

## References

- Prong P-B synthesis; arXiv 2601.06007 (agentic cache boundaries)
- BT-12 Option 6 (metered context)
- `MADEIRA_AIC_PER_TASK_REGISTRY.csv` (extension proposal)
