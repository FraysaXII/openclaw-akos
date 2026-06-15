---
intellectual_kind: research_synthesis_prong
prong_id: P-D
prong_topic: Model management finops and token economy
authored: 2026-06-14
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
control_confidence: Euclid
---

# Prong P-D — Model management, finops, token economy

## Load-bearing finding

Holistika has **registers for commercial finops** (counterparties, pricing tiers, rev-rec) and **operating doctrine for model seats** (Opus thinking / Composer execution — `model-selection-2026-05-28`). What alpha requires is **closed-loop token economics**: every MADEIRA task class maps to model policy, budget envelope, and observable cost — linked to infonomics (I97) so data/context spend is valued, not just API lines.

External: model-agnostic gateways (LiteLLM, Portkey) centralize rate limits, cost allocation, credential rotation (SRC-MBH-EXT-005, 004). Langfuse attributes cost per trace but does not enforce budgets (SRC-MBH-EXT-018) — pair with gateway for hard caps.

## Model management layers

| Layer | Holistika SSOT | Alpha requirement |
|:---|:---|:---|
| **Catalog** | `config/openclaw.json.example` full inventory | No profile-only shrink |
| **Seat routing** | AIC_REGISTRY + two-seat guide | Per-task registry columns |
| **Provider billing** | FINOPS_COUNTERPARTY_REGISTER | Map API keys → cohort |
| **Unit economics** | PRICING_TIER_REGISTRY | Alpha pricing hypothesis |
| **Data value** | I97 infonomics charter | Context token ≈ data asset consumption |

## Token economy design principles (research)

1. **Attribute before optimize** — Langfuse trace IDs on every MADEIRA session; tag `alpha_cohort`, `scenario`, `mode`.
2. **Cache as finops lever** — P-B findings; report `cached_tokens` in dossier Section 1 extension.
3. **Model routing is product policy** — cheap seat for mechanical tranches; thinking seat for ratify packets only (already doctrine; enforce in registry).
4. **Infonomics link** — Deloitte + arXiv (SRC-MBH-EXT-016, 017): data value is context-dependent; KiRBe ingest cost should appear in research-center freshness strip narrative.

## Gaps

| Gap | Priority |
|:---|:---|
| MADEIRA_AIC_PER_TASK_REGISTRY lacks `model_policy`, `budget_class`, `cache_policy` columns | P0 for alpha |
| No alpha cohort cost dashboard | P1 — Langfuse dashboard + export |
| Token spend not tied to DATA_CONTRACT consumers | P1 — I97 × I96 join |
| Gateway abstraction not documented in vault | P2 — AGENTIC_FRAMEWORK_LANDSCAPE §4 |

## Ranked insights

1. **Observability without gateway = attribution without enforcement** — RANK 1
2. **Infonomics completes finops for context-heavy MADEIRA** — RANK 1
3. **Two-seat routing is already token economy; make it measurable** — RANK 2
