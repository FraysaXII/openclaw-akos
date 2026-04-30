---
status: active
role_owner: Founder + PMO
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_sales_motion
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: sales_motion
authority: Founder
last_review: 2026-04-30
deck_bound: true
deck_slides_consumed: []
---

# Sales motion — per ICP, how the deal actually closes

## What this answers

For each of the three ICPs, the discovery → qualification → proposal → close sequence; the cycle length band; the deal size band; and the most common objections by stage. Per 2026 SaaS GTM research: founder-led sales is the canonical motion until ~€1 M ARR; PLG works best for sub-€5 k ACV; sales-led for €25 k+ ACV with 80 - 100 day cycles.

## ICP 1 — Pyme tecnológica (cliente directo, servicio profesional)

**Deal size**: €4 000 - €40 000 per engagement (Strategic Audit through Operating System Build).
**Cycle length**: 4 - 8 weeks first conversation to signed.
**Motion**: Founder-led.

### Stages

| Stage | What happens | Time | Common objection |
|:---|:---|:---|:---|
| **Discovery** | Founder reaches out via LinkedIn / warm intro / inbound; 30-min discovery call to understand the operations problem | 1 - 2 weeks | "We're not ready / no budget" |
| **Qualification** | Free 60 - 90 min "operating-state" workshop call; map the chaos in real time; identify 2 - 3 candidate audit scopes | 1 - 2 weeks | "We can do this internally" |
| **Proposal** | Written audit proposal (1-page) with scope + price + timeline + outcomes | 1 week | "Why so expensive?" / "Can we do half?" |
| **Close** | Signature + 50 % deposit; first audit session within 2 weeks | < 1 week | "Let me check with co-founder" |

### Objection responses

- **"We're not ready"**: Offer a free 60-min discovery call only; convert when they hit a real pain trigger.
- **"We can do this internally"**: Show 2 - 3 case studies (slide 6 evidence) where similar SMEs tried internally, then engaged.
- **"Why so expensive?"**: Re-frame as productized engagement vs day-rate consulting; same outcome would cost €15 k+ at McKinsey-class.
- **"Half scope?"**: Decline politely; we don't deliver a useful audit at half scope. Offer the smaller "Strategic Audit" entry-point instead.

## ICP 2 — Partner B2B (canal indirecto, entrega gobernada)

**Deal size**: €15 000 - €100 000 per partner-led engagement (Holística delivers; partner owns relationship).
**Cycle length**: 2 - 6 weeks from partner intro to scope-signed (because the partner has already qualified the client).
**Motion**: Partner-led with Holística technical due diligence.

### Stages

| Stage | What happens | Time | Common objection |
|:---|:---|:---|:---|
| **Partner intro** | Partner sends a brief: "client X needs Y, can you deliver?" | < 1 week | (Partner has handled this) |
| **Technical scope** | Holística engineer + founder review the brief; estimate effort; propose architecture | 1 - 2 weeks | "Effort estimate too high" |
| **Joint proposal** | Partner + Holística draft joint scope; partner-share negotiated per `PRICING_MODEL.md` §1.3 | < 1 week | "Margin too thin for partner" |
| **Close** | Partner signs with end client; Holística sub-contracts | < 1 week | (Partner closes) |

### Objection responses

- **"Effort too high"**: Walk the architecture; show what corner-cutting buys (technical debt, brittle deploy, no audit). Partner respects depth.
- **"Margin thin"**: Stick to the schedule in `PRICING_MODEL.md`; sub-30 % partner share kills the channel.

## ICP 3 — Cliente SaaS (KiRBe direct, ingreso recurrente)

**Deal size**: Starter €49 - €99 / month / org → Business €1 500 - €4 000 / month / org.
**Cycle length**: < 1 week trial → paid (Starter); 2 - 8 weeks (Team); 6 - 16 weeks (Business / Enterprise).
**Motion**: Product-led growth (PLG) with founder-led for Business / Enterprise tier.

### Stages

| Stage | What happens | Time | Common objection |
|:---|:---|:---|:---|
| **Trial signup** | Self-serve via the public KiRBe site; 14-day free trial of Starter or Team | < 1 day | (Pre-objection: signing up is itself the test) |
| **Activation** | First content uploaded + first query; in-app onboarding | 1 - 7 days | "Search isn't finding what I want" |
| **Conversion** | Trial-to-paid: card on file; auto-charge at end of trial | < 1 week from trial | "Free is enough for me" |
| **Expansion** | Account grows: more seats, more knowledge, more queries; tier upgrade Starter → Team → Business | 3 - 12 months from first paid | "Why do we need to upgrade?" |
| **Enterprise close** (Business → Enterprise) | Founder-led; 2 - 4 calls; SOC 2 / on-premise / custom integration as upsell | 6 - 16 weeks | "Procurement will take time" |

### Objection responses (PLG-specific)

- **"Search isn't finding what I want"**: Most-common conversion blocker. Improve onboarding to include a "first-query coaching" moment in the first session.
- **"Free is enough"**: Quota cliff at end of trial does the work; if a free tier is ever introduced (we currently say no per `PRICING_MODEL.md` §3), introduce strict quota.
- **"Why upgrade?"**: Build in usage-based metering signals so the customer can see "you used 80 % of your query quota" → natural upgrade prompt.

## Cross-cutting: founder-led vs PLG split

Per 2026 GTM research, the ARR-band rule:

- **< €100 k ARR**: 100 % founder-led across all ICPs. Skip the sales hire.
- **€100 k - €500 k ARR**: Founder-led ICP 1 + ICP 2; PLG ramping for ICP 3.
- **€500 k - €1 M ARR**: First sales hire (BDR / SDR for ICP 1 outbound; partner manager for ICP 2; PLG mature for ICP 3).
- **≥ €1 M ARR**: Sales-led for Business / Enterprise tier; PLG for everything else.

We are currently in the **first band** (founder-led across all ICPs). Hire trigger is the second band.

## Sales-rituals checklist (operator runs weekly)

- **Monday**: Review pipeline (Notion / KiRBe internal). Identify 3 - 5 first conversations to initiate.
- **Wednesday**: Workshop or proposal call (max 2 per week as founder-led capacity).
- **Friday**: Update `STRATEGY_DECISION_LOG.md` with any closed / lost / postponed deal; update `POC_TO_COMMERCIAL_MAP.csv` with any new shipped engagement.

## Deck-bound facts

This artifact is currently informational; deck slides 9 (ICP) and 10 (business model) display the **outcome** of the motion, not the motion itself. When the deck pivots to "investor-only" variant, slide 9 expands to include cycle-length + deal-size bands per ICP.

```
slide_id: 09-market-icp (currently uses CHANNEL_STRATEGY signals; SALES_MOTION informs the underlying credibility but does not directly populate slide copy today)
slide_id: 10-business-model (currently uses PRICING_MODEL today/bridge/tomorrow framing; SALES_MOTION informs underlying credibility)
deck_bound_when: investor_variant
```

## Cross-references

- [`CHANNEL_STRATEGY.md`](CHANNEL_STRATEGY.md) — channel × motion is the full picture
- [`PRICING_MODEL.md`](PRICING_MODEL.md) — deal size bands
- [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md) — cycle length × close rate × deal size = unit economics
