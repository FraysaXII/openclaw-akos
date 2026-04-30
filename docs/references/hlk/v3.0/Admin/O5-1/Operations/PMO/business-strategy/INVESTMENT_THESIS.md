---
status: active
role_owner: Founder + PMO
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_investment_thesis
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: investment_thesis
authority: Founder
last_review: 2026-04-30
deck_bound: true
deck_slides_consumed: ["13-enisa-fit"]
---

# Investment thesis — if/when raise, what it buys

## What this answers

Whether external capital is on the table; if so, the amount band, the milestones it unlocks, the dilution band, comparable rounds in the EU SaaS ecosystem, and the alternatives we deliberately consider before raising.

## 1. Default posture

**Default**: bootstrap. We do not need to raise to ship the next 6 months of the roadmap. The thesis is operationally healthy at €4 - 5 k / month burn with founder-led pipeline + partner channel + KiRBe inbound seed.

This is the bootstrapped-Spanish-SME-SaaS posture. We're calibrated against the **2.0 - 2.9 LTV : CAC sustainable zone** per `UNIT_ECONOMICS.md` rather than the venture-scale **3.0 - 4.5 zone** that requires capital infusion to scale acquisition.

> **TODO[OPERATOR-invest-D1]** — confirm: bootstrap-only as default? Acceptable variants: (a) bootstrap-only; (b) bootstrap + ENISA loan opportunistic; (c) actively pursue pre-seed; (d) deferred decision until month 6.

## 2. When raising changes from "deferred" to "active"

Three triggers each independently flip the calculus:

1. **Channel 3 (KiRBe inbound) shows LTV : CAC ≥ 5 : 1 with > €5 k MRR.** Elite-zone unit economics at material scale → raising lets us spend on paid acquisition without breaking the equation.
2. **Customer or partner with strategic value** offers a structural advance (e.g. 12-month prepaid contract, distribution exclusive in a region) that materially shortens KiRBe time-to-product-market-fit.
3. **Cash position dips ≤ 6 months runway** (Yellow zone per `BOOTSTRAPPING_PLAN.md`) AND ENISA loan path is unavailable or insufficient.

## 3. If raising — round shape

If/when we raise, three credible rounds map to three sets of milestones:

### Pre-seed (€100 - €400 k)

- **Comparable EU pre-seed bands (2026)**: pre-product / early-traction Spanish + EU SaaS startups raised pre-seed at €150 - €500 k typical, €4 - €10 M post-money valuation.
- **What it unlocks**: 1 - 2 senior engineer hires for 12 - 18 months; KiRBe productisation push; first paid acquisition pilot.
- **Dilution band**: 8 - 15 %.
- **Investor profile**: angels + small Spanish / EU pre-seed funds (Bcombinator, Inveready, K Fund, etc.).
- **When**: months 6 - 12 if Channel 3 unit economics flip to growth-ready zone.

### Seed (€500 k - €2 M)

- **Comparable**: Spanish SaaS at seed raised €600 k - €2 M typical, €6 - €15 M post-money in 2026.
- **What it unlocks**: 4 - 6 hires; 2 - 3 markets; KiRBe enterprise tier capacity; founder time freed for strategy.
- **Dilution band**: 15 - 25 %.
- **Investor profile**: K Fund, Kibo, Bewater, Samaipata, JME Ventures.
- **When**: months 18 - 30 if KiRBe ARR ≥ €500 k.

### Series A (€3 - €8 M)

- **Comparable**: Spanish + EU SaaS Series A at €3 - €10 M typical, €15 - €40 M post-money.
- **What it unlocks**: full sales-led motion; international expansion (UK, FR, DE); platform investment.
- **Dilution band**: 18 - 28 %.
- **Investor profile**: Cathay Innovation, Atomico, Accel, Northzone (EU); Sequoia / GV (US).
- **When**: months 30 + if KiRBe ARR ≥ €1 M with healthy LTV:CAC ≥ 3:1.

> **TODO[OPERATOR-invest-D2]** — confirm or refine the round bands. Operator may stay vague ("we'll raise when it makes sense") or commit to pre-seed only / seed only.

## 4. Alternatives to equity capital we explicitly consider first

| Alternative | Pros | Cons | When |
|:---|:---|:---|:---|
| **ENISA loan** (Empresa Emergente) | Cheap (1 - 5 % rate band), no equity dilution, Spanish-government endorsement | Requires certification, repayable, capped amount (~€25 - €100 k) | Default first move per `BOOTSTRAPPING_PLAN.md` ENISA Plan B |
| **Customer prepay** (1-year subscription paid up front, often at discount) | No dilution, signals real demand | Requires existing customer relationship | When KiRBe Business tier signs first 1-2 customers |
| **Partner advance** (Partner pays 6 - 12 months of dedicated capacity in advance) | No dilution, locks in channel commitment | Only works at scale of partner | When partner pipeline has 4+ recurring engagements |
| **Revenue-based financing** (Capchase, Pipe, et al.) | No dilution, scales with MRR | Requires MRR ≥ €10 - €30 k / month, high effective cost | When KiRBe MRR ≥ €15 k |
| **EU grants** (Horizon Europe, EIC, NEOTEC, RED.es) | Non-dilutive, large sums | Heavy paperwork, multi-year cycles, restricted use-of-funds | Specific R&D / sector tracks; opportunistic |
| **Crowdfunding / equity crowdfunding** (Crowdcube, Seedrs) | Brand exposure, small-investor base | High cost, regulatory burden, dilution still | Rarely worth it under €500 k raise |

The decision tree: ENISA loan → Customer prepay → Partner advance → RBF → Equity capital. Equity is the **last** instrument considered, not the first.

## 5. What we'd never raise for

- To extend runway without unit-economic improvement (death-loop).
- To replicate a competitor's strategy.
- To buy a logo we don't need.
- To hire faster than the team's coordination capacity.

## 6. If raising — the deck variant we'd build

Slide 14 of the company dossier currently asks for ENISA-adviser confirmation. The **investor-deck variant** (out of scope for I29) would replace slide 14 with:

- The amount asked.
- The milestones unlocked.
- The dilution band.
- The current cash position + runway months.
- The 18-month plan post-raise.

That deck variant is built on demand from this artifact's data.

## 7. Founder-equity preservation rule

We deliberately retain ≥ 75 % founder equity through pre-seed. Below 75 % we revisit whether the raise is necessary or whether an alternative funds the same milestones.

## Deck-bound facts

```
slide_id: 13-enisa-fit
investment_posture: "TODO[OPERATOR-invest-D1] - default: bootstrap; ENISA loan as opportunistic non-dilutive instrument."
investment_decision_owner: "Founder per STRATEGY_DECISION_LOG D-IH-29-STR-D6."
use_of_funds_orientation: "Non-dilutive funding (ENISA + customer prepay) targeted first; equity capital reserved for post-month-12 if Channel 3 unit economics flip to growth-ready."
```

## Cross-references

- [`BOOTSTRAPPING_PLAN.md`](BOOTSTRAPPING_PLAN.md) — runway position triggers
- [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md) — when LTV:CAC ≥ 5:1 the equation flips
- [`STRATEGY_DECISION_LOG.md`](STRATEGY_DECISION_LOG.md) D-IH-29-STR-D6 (raise / not-raise)
- [`MARKET_THESIS.md`](MARKET_THESIS.md) §3 SOM band — investor calibration
