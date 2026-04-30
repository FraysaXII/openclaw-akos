---
status: active
role_owner: Business Controller + Founder
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_unit_economics
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: unit_economics
authority: Founder + Business Controller
last_review: 2026-04-30
deck_bound: true
deck_slides_consumed: ["12-roadmap"]
---

# Unit economics — LTV / CAC / payback per channel × ICP

## What this answers

For each combination of channel × ICP (from `CHANNEL_STRATEGY.md`), what's the customer acquisition cost (CAC), the lifetime value (LTV), the payback period, and the gross margin assumption — plus the 2026 benchmarks we calibrate against.

## 2026 benchmarks (research-grounded)

Internal benchmarks for the four operating zones per 2026 SaaS data:

| Zone | LTV : CAC | What it means | Action |
|:---|:---|:---|:---|
| **Danger** | < 1.5 : 1 | High bankruptcy risk | Focus on pricing + churn, not acquisition |
| **Sustainable** | 2.0 - 2.9 : 1 | Healthy for bootstrapped | Slow growth; profitable |
| **Growth-ready** | 3.0 - 4.5 : 1 | Venture-scale ready | Increase paid acquisition |
| **Elite** | ≥ 5.0 : 1 | Highly efficient | Increase marketing spend immediately |

Holística targets **sustainable to growth-ready** (2 - 4 : 1 LTV:CAC) given the bootstrapped posture. For SaaS specifically, the benchmark CAC payback is **12 - 18 months**; for PLG with sub-€5 k ACV, **3 - 6 months**.

## Channel × ICP unit economics matrix

> Numbers are research-grounded directional estimates. Founder narrows to actuals as data accumulates per `STRATEGY_DECISION_LOG.md`.

### Service engagements (Channel 1: Founder-led + ICP 1: Pyme tecnológica)

| Metric | Value / band |
|:---|:---|
| ACV (annual contract value) | €4 000 - €40 000 (Strategic Audit through Operating System Build; assume avg €15 000 first engagement, with 50 % expansion to a second engagement) |
| Effective annual customer value | €15 000 + 50 % × €15 000 = €22 500 (year 1) |
| Customer lifespan | 1 - 3 years (consulting-style) |
| LTV (gross) | TODO[OPERATOR-le-svc1] (band: €22 500 × 2 years × 70 % gross margin = €31 500) |
| CAC | €100 - €500 |
| **LTV : CAC** | **63 : 1 to 315 : 1** (extreme; benefits from low founder-CAC) |
| Payback period | < 1 month (audit deposit covers CAC immediately) |
| Gross margin | ~70 % (founder + 1 engineer time on a fixed-price audit) |

> **Reality check**. The 63 : 1 ratio is unrealistic at scale; it reflects the founder-CAC dominance which compresses fast as the founder hits time-cap. Actual sustainable LTV : CAC for Channel 1 is closer to **8 - 15 : 1** once founder time is fully loaded as a cost.

### Partner-channel engagements (Channel 2: Partner B2B + ICP 2)

| Metric | Value / band |
|:---|:---|
| ACV per engagement | €15 000 - €100 000 (Holística share, after partner-share deducted) |
| Customer lifespan | 1 - 2 years (engagement-recurring, sometimes annual retainer) |
| LTV (gross) | TODO[OPERATOR-le-pb2b] (band: €40 000 × 1.5 years × 65 % gross margin = €39 000) |
| CAC | ~€0 (partner runs the relationship) |
| **LTV : CAC** | **Effectively unbounded** — channel CAC measured per *partner relationship*, not per engagement |
| CAC per partner relationship | €1 000 - €3 000 (founder time + occasional partner-event travel) |
| Engagements per partner per year | 2 - 6 (target) |
| Effective LTV per partner | TODO[OPERATOR-le-pb2bp] (band: 4 engagements × €40 000 × 65 % = €104 000 / year / partner) |
| Payback period | 1 - 2 engagements per partner |
| Gross margin | ~65 % (after partner-share) |

### KiRBe SaaS — Starter tier (Channel 3 + ICP 3)

| Metric | Value / band |
|:---|:---|
| ARPA (avg revenue per account, monthly) | TODO[OPERATOR-le-saas-s] (band: €49 - €99 / month / org; mid-band €70 / month) |
| Annual revenue / account | €840 |
| Monthly churn rate (target) | < 5 % (industry healthy band: 2 - 5 % / month for SMB SaaS) |
| Customer lifespan (= 1 / churn) | 20 + months |
| Gross margin | 75 - 80 % (compute + infra costs ~20 - 25 %) |
| LTV (gross × lifespan) | €840 × 1.7 years × 78 % ≈ **€1 100** |
| CAC | €50 - €300 (paid + content + onboarding) |
| **LTV : CAC** | **3.5 - 22 : 1** (sustainable to elite) |
| Payback period | **3 - 6 months** (PLG canonical band) |

### KiRBe SaaS — Team tier (Channel 3 + ICP 3)

| Metric | Value / band |
|:---|:---|
| ARPA (monthly) | TODO[OPERATOR-le-saas-t] (band: €299 - €599; mid-band €400) |
| Annual revenue / account | €4 800 |
| Monthly churn rate (target) | < 3 % |
| Customer lifespan | 33 + months |
| Gross margin | 78 % |
| LTV (gross) | €4 800 × 2.7 years × 78 % ≈ **€10 100** |
| CAC | €500 - €2 500 (more onboarding, longer sales cycle) |
| **LTV : CAC** | **4 - 20 : 1** |
| Payback period | **6 - 12 months** |

### KiRBe SaaS — Business tier (Channel 3 + ICP 3)

| Metric | Value / band |
|:---|:---|
| ARPA (monthly) | TODO[OPERATOR-le-saas-b] (band: €1 500 - €4 000; mid-band €2 500) |
| Annual revenue / account | €30 000 |
| Monthly churn rate (target) | < 2 % |
| Customer lifespan | 50 + months |
| Gross margin | 80 % |
| LTV (gross) | €30 000 × 4.2 years × 80 % ≈ **€100 800** |
| CAC | €5 000 - €15 000 (founder-led + custom onboarding + integration) |
| **LTV : CAC** | **6 - 20 : 1** |
| Payback period | **12 - 18 months** |

## Aggregate (24-month rolling target)

> **TODO[OPERATOR-le-aggregate]** — confirm or refine the 24-month target table. Bands below are research-grounded directional estimates per `MARKET_THESIS.md` §3 SOM band.

| Stream | Target (24-month) | LTV : CAC target | Notes |
|:---|:---|:---|:---|
| Service engagements (Channel 1 + 2) | 30 - 60 closed | 4 - 8 : 1 (loaded) | Founder time as cost |
| KiRBe Starter | 30 - 80 paying | ≥ 3 : 1 | PLG efficiency |
| KiRBe Team | 5 - 15 paying | ≥ 4 : 1 | Onboarding investment |
| KiRBe Business | 1 - 3 paying | ≥ 6 : 1 | Founder-led + integration cost |
| **Total ARR** | TODO[OPERATOR-le-arr] (band: €300 k - €800 k by month 24) | n/a | Mix of one-time service revenue + recurring SaaS |

## Model sensitivities (the variables that matter most)

1. **KiRBe Team-tier ARPA**. Each €100 / month change in ARPA changes Team-tier LTV by ~€2 500. Drives the gross profit picture more than any other lever.
2. **Service-engagement gross margin**. If founder time is loaded at €5 000 / month opportunity cost, gross margin drops from 70 % to ~50 %. Critical for the bootstrapped scenario.
3. **Monthly churn rate on KiRBe**. 2 % vs 5 % monthly churn changes lifespan from 50 months to 20 months — 2.5× LTV swing.

## What this means for the deck

Slide 12 (Roadmap) anchors phase milestones on unit-economics targets:

- 0 - 6 months: prove unit economics at small scale (3 audits + 1 partner engagement + 5 KiRBe Starter accounts; LTV : CAC ≥ 3 : 1 across the mix).
- 6 - 12 months: scale the channels with healthy unit economics (5 - 10 KiRBe B2B, 2 partner integrations recurring, 2 - 3 engineers).
- 12 - 24 months: KiRBe SaaS dominates revenue mix (≥ 60 %), with service work as expansion arm.

## Deck-bound facts

```
slide_id: 12-roadmap
unit_economics_anchor:
  phase_0_6:
    target_ltv_cac: ">= 3:1"
    target_signed: "3 audits + 1 partner engagement + first 5 KiRBe Starter accounts"
  phase_6_12:
    target_ltv_cac: ">= 4:1"
    target_arr_band: "TODO[OPERATOR-le-arr]"
  phase_12_24:
    target_ltv_cac: ">= 5:1"
    target_saas_share: "60% recurring SaaS revenue or higher"
```

## Cross-references

- [`PRICING_MODEL.md`](PRICING_MODEL.md) — pricing × volume × margin = unit economics
- [`CHANNEL_STRATEGY.md`](CHANNEL_STRATEGY.md) — CAC bands per channel
- [`BOOTSTRAPPING_PLAN.md`](BOOTSTRAPPING_PLAN.md) — burn rate × unit economics = runway
- [`INVESTMENT_THESIS.md`](INVESTMENT_THESIS.md) — when LTV:CAC > 5:1 the equation flips toward "raise to scale"
