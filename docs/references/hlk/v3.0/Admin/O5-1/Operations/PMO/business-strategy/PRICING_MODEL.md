---
status: active
role_owner: Business Controller + Founder
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_pricing_model
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: pricing_model
authority: Founder + Business Controller
last_review: 2026-04-30
deck_bound: true
deck_slides_consumed: ["10-business-model"]
---

# Pricing model — service rates, KiRBe SaaS, partner revenue share

## What this answers

What does it cost to engage Holística, in three currencies of value: service engagements, KiRBe SaaS subscriptions, partner revenue share.

## 1. Three price schedules (one company, three pricing surfaces)

### 1.1 Service rate card (engagements)

We do **not** sell day-rate consulting. Engagements are scoped, fixed-price packages keyed to outcomes.

| Engagement | Outcome | Price band (EUR, recommended) | Duration | Frequency we expect |
|:---|:---|:---|:---|:---|
| **Strategic Audit** | Mapped operating system + 90-day roadmap + 1 SOP draft | TODO[OPERATOR-pricing-audit] (band: €4 000 - €8 000) | 2 - 3 weeks | Most common entry point |
| **Operating System Build** | Designed operating system + 5 SOPs + 2 process automations + handoff documentation | TODO[OPERATOR-pricing-osys] (band: €15 000 - €40 000) | 6 - 10 weeks | After audit, when client commits |
| **Software Sprint** | One delivered piece of software (web feature, internal tool, KiRBe extension, Shopify app, etc.) | TODO[OPERATOR-pricing-sprint] (band: €8 000 - €25 000) per sprint | 2 - 6 weeks | Recurring; can be a retainer |
| **Embedded Engineering** | Holística engineer(s) embedded in client team for capacity | TODO[OPERATOR-pricing-embed] (band: €18 000 - €30 000 / month / engineer) | Monthly retainer, 3-month minimum | Channel-only initially (Websitz pattern); rare direct |

> **Why fixed-price not day-rate.** Day-rate maximises argument over hours and prevents productisation. Fixed-price aligns the client with the outcome and lets us reuse internal tooling without giving away margin.

### 1.2 KiRBe SaaS — 3-tier hybrid (subscription + metered overage)

Per 2026 SaaS pricing research: 3 tiers (not 4-5) is the converting structure; usage-based pricing grows revenue 8 pp faster than flat; value-based pricing at 10-12 % of customer value beats cost-plus by 20-30 %.

| Tier | Target | Price band (EUR / month) | Includes | Metered overage |
|:---|:---|:---|:---|:---|
| **Starter** | Solo founders / small teams (1 - 5 seats) | TODO[OPERATOR-kirbe-starter] (band: €49 - €99 / month) | 1 organisation, 5 seats, 50 GB knowledge, 5 000 queries / month | €0.01 - €0.05 / query above quota |
| **Team** | Growing teams (5 - 25 seats) | TODO[OPERATOR-kirbe-team] (band: €299 - €599 / month) | 1 organisation, 25 seats, 500 GB, 100 000 queries / month, audit log, role-based access | €0.005 - €0.02 / query above quota |
| **Business** | Established orgs (25 - 100 seats) | TODO[OPERATOR-kirbe-biz] (band: €1 500 - €4 000 / month) | Multi-organisation, 100 seats, 5 TB, 1 M queries / month, SSO, full audit trail, dedicated support | Custom |
| **Enterprise** | ≥ 100 seats / regulated industries | Custom (call) | Unlimited seats, custom SLA, on-premise option, custom integrations | Custom |

> **Pricing anchors**. Median SaaS user-month is €29; we anchor Starter / Team above that because we sell governed retrieval, not generic search. Value-based price = 10-12 % of the customer's annual labour cost saved by KiRBe; this calibrates Business + Enterprise.

### 1.3 Partner revenue share

For partner-channel engagements (Websitz, Rushly-class collaborations) where Holística delivers software for the partner's end client.

| Partner shape | Holística share | Partner share | Notes |
|:---|:---|:---|:---|
| **Sub-contracted delivery** (partner sells, Holística delivers) | 65 - 75 % | 25 - 35 % | Holística carries delivery risk; partner carries client relationship |
| **Joint delivery** (both names on the contract) | 50 % | 50 % | Used when both sides bring real capacity |
| **Holística-led, partner-introduced** (partner refers, Holística closes + delivers) | 85 - 90 % | 10 - 15 % (referral fee) | Standard SaaS-style channel referral |
| **KiRBe reseller** (partner sells KiRBe to their book; Holística supplies platform + ops) | 70 - 80 % platform | 20 - 30 % reseller margin | Future state; not active today |

> **TODO[OPERATOR-partner-share]** — confirm the 65 / 50 / 85 splits or refine. Current Websitz arrangement is operator-confirmed at one of these tiers; future partnerships use this schedule as a starting point.

## 2. Why pricing matters strategically

- **Service rates anchor the brand**. €5 000 audit, not €1 500. Below a band the client treats us like a freelancer; above a band like classic consulting. We price in the upper-mid SME band to land "premium product agency".
- **KiRBe pricing anchors the SaaS thesis**. Below €49 / month we look like a personal tool; above €1 000 / month we anchor the B2B-platform identity.
- **Partner share funds the channel**. < 10 % to the partner kills the channel; > 35 % kills our margin. The 25-35 % standard reflects 2026 SaaS partner-channel norms.

## 3. Anti-patterns we explicitly avoid

- **Free tier on KiRBe SaaS**. We don't have the engineering bandwidth to support a free tier with 100 + waste-class users; the Starter tier at €49+ is the floor.
- **Discounting service rates**. Volume discount on service hours signals weakness. If a client wants more for less, we restructure scope, not price.
- **Paid pilots disguised as POCs**. If we're going to deliver real software, we charge for it. Pure exploratory POCs are a separate "Strategic Audit" engagement.

## 4. Discounting policy (when it's allowed)

- **Strategic clients** (visible logo, future-partner potential, regulator relationship): up to 20 % off service rates first engagement, never on KiRBe SaaS.
- **Multi-engagement bundle** (audit + ops-build pre-committed): up to 15 % off bundled price.
- **Annual KiRBe billing**: standard 15 - 20 % off vs monthly.

## 5. Open questions for the founder

> **TODO[OPERATOR-pricing-D1]** — Confirm or refine the four service-rate bands above (audit, osys, sprint, embed). Acceptable: bands stay; or single recommended numbers; or pricing-by-package-name (e.g. "Holistika Audit €4 800") with no bands.
>
> **TODO[OPERATOR-pricing-D2]** — Confirm or refine the three KiRBe SaaS tier prices. Acceptable: 3-tier specific numbers, or the bands above.
>
> **TODO[OPERATOR-pricing-D3]** — Confirm partner revenue-share standard schedule.
>
> **TODO[OPERATOR-pricing-D4]** — Decide whether we publish prices on the public site (yes / partial / no). 2026 norm: SaaS publishes; service stays "Contact us" or "Starting from".

## Deck-bound facts

```
slide_id: 10-business-model
today_pricing_summary: "Engagements estructurados con precio cerrado por entregable - de auditoria estrategica a sprint de software. Nada de tarifa diaria."
tomorrow_pricing_summary: "KiRBe SaaS B2B con tres niveles + extensiones por uso. Subscripcion mensual o anual; canal de partner con margen de reseller."
bridge_pricing_summary: "El servicio paga el desarrollo del producto; el producto paga el equipo a medida que escala."
service_price_floor: "TODO[OPERATOR-pricing-D1]"
saas_tier_count: 3
saas_starter_floor: "TODO[OPERATOR-pricing-D2]"
partner_revshare_default: "TODO[OPERATOR-pricing-D3]"
```

## Cross-references

- [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md) — pricing × volume × margin = unit economics
- [`CHANNEL_STRATEGY.md`](CHANNEL_STRATEGY.md) — partner share funds the channel hypothesis
- [`COMPETITIVE_LANDSCAPE.md`](COMPETITIVE_LANDSCAPE.md) §"Why we don't price by day-rate"
- [`STRATEGY_DECISION_LOG.md`](STRATEGY_DECISION_LOG.md) D-IH-29-STR-4 (3-tier choice rationale)
