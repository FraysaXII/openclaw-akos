---
status: active
role_owner: Business Controller + Founder
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_bootstrapping_plan
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: bootstrapping_plan
authority: Founder + Business Controller
last_review: 2026-04-30
deck_bound: true
deck_slides_consumed: ["12-roadmap", "13-enisa-fit"]
---

# Bootstrapping plan — runway, burn, break-even

## What this answers

Month-by-month cash position (personal + business), three scenarios (conservative / base / aggressive), the runway zone we're in (red / yellow / green / blue), and the break-even point under each scenario.

> **Format follows 2026 solo-founder runway model best practice**: split personal vs business expenses, three scenarios, zone-coloured runway forecast.

## 1. Operating principle

We run with **runway = months of cash on hand at current burn rate**. Below 6 months is a yellow zone; below 3 months is red. The plan shows when we hit each zone under each scenario, and the actions that fire at each transition.

## 2. Personal expense baseline (operator)

> **TODO[OPERATOR-runway-personal]** — confirm or refine. Bands below are placeholders the founder fills.

| Category | Monthly band (EUR) |
|:---|:---|
| Housing (rent + utilities) | TODO[OPERATOR] (band: €600 - €1 500) |
| Food + groceries | TODO[OPERATOR] (band: €300 - €600) |
| Transport | TODO[OPERATOR] (band: €0 - €200) |
| Health insurance + medical | TODO[OPERATOR] (band: €60 - €250) |
| Phone + internet | TODO[OPERATOR] (band: €40 - €100) |
| Personal subscriptions + tools | TODO[OPERATOR] (band: €50 - €200) |
| Discretionary (dining, leisure) | TODO[OPERATOR] (band: €100 - €500) |
| Savings / pension contribution | TODO[OPERATOR] (band: €0 - €500) |
| **Personal monthly total** | **TODO[OPERATOR-personal-total]** (band: €1 150 - €3 850; mid-band ~€2 500) |

## 3. Business expense baseline (Holística)

| Category | Monthly band (EUR) | Notes |
|:---|:---|:---|
| Infrastructure (hosting, databases, domains, monitoring) | €150 in idle, €300 - €500 in active use | Per `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md` |
| Software licences (Cursor, Figma, Linear/Notion, etc.) | €100 - €300 | |
| AI tooling (LLM API quota, embeddings, GPU hours when active) | €100 - €600 | Variable with KiRBe usage |
| Legal / fiscal / advisory | €100 - €500 (averaged; spiky around incorporation) | Per `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md` |
| Marketing (events, content, paid acquisition pilot) | €0 - €500 | Channel 5 + small Channel 3 paid pilot |
| Co-working / office | €0 - €250 | Optional |
| Insurance (professional / cyber) | €30 - €100 | |
| **Business monthly total (idle)** | TODO[OPERATOR-biz-idle] (band: €380 - €1 250; mid-band ~€800) | When no active engagements |
| **Business monthly total (active)** | TODO[OPERATOR-biz-active] (band: €580 - €2 250; mid-band ~€1 200) | When KiRBe + 1 - 2 active engagements |

## 4. Combined burn baseline

| Scenario | Monthly burn (EUR) | Description |
|:---|:---|:---|
| **Idle / minimum** | ~€2 880 - €5 100 (mid €3 300) | Personal mid + business idle |
| **Active / sustained** | ~€3 080 - €6 100 (mid €3 700) | Personal mid + business active |
| **Aggressive / hire-1** | ~€7 080 - €10 100 (mid €8 700) | + 1 senior engineer at €4 000 - €5 000 / month |

> **TODO[OPERATOR-burn-D1]** — confirm the mid-band burn that best reflects the founder's actual life. The deck consumes the mid-band as the baseline runway figure.

## 5. Cash on hand

> **TODO[OPERATOR-cash-D1]** — current cash position (personal + Holística initial capital, post-incorporation).

| Source | Amount (EUR) |
|:---|:---|
| Personal savings dedicated to runway | TODO[OPERATOR] |
| Holística initial capital (post-`Q-LEG-004` decision) | TODO[OPERATOR] (band: €1 - €3 000+ per `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`) |
| **Total cash on hand at month 0** | TODO[OPERATOR-cash-total] |

## 6. Three-scenario runway forecast

### Scenario A — Conservative

- Burn: €5 000 / month combined (personal mid + business idle + small contingency).
- Revenue: €0 / month (assumes no engagements close — purely defensive scenario).
- **Runway**: cash on hand ÷ €5 000.

### Scenario B — Base

- Burn: €4 000 / month combined.
- Revenue: 1 audit closed every 6 weeks (€5 000 average); 1 KiRBe Starter signup / month from month 6 onwards.
- **Net burn**: €4 000 - €3 500 = ~€500 / month from month 6 onwards.
- **Break-even**: month 9 - 12 (when steady-state revenue ≥ burn).

### Scenario C — Aggressive

- Burn: €4 500 / month combined for months 0-6, ramping to €8 700 from month 7 with 1 engineer hire.
- Revenue: 2 audits / month + 1 partner engagement / quarter + KiRBe ramp to 5 paying accounts by month 12.
- **Break-even**: month 14 - 18 (engineer hire pushes break-even later but unlocks growth).

> **TODO[OPERATOR-scenario-D1]** — operator picks which scenario is the planning baseline.

## 7. Zone table (runway health)

| Months of runway | Zone | Action |
|:---|:---|:---|
| **< 3** | Red | Stop hiring, freeze infra spend, offer Q4 audits at discount, raise emergency line |
| **4 - 6** | Yellow | No new fixed costs, push pipeline, prepare optional fundraising deck |
| **7 - 12** | Green | Execute plan; option to invest in 1 engineer hire if pipeline supports |
| **≥ 12** | Blue | Investment phase: engineer hire, paid acquisition pilot, strategic move |

## 8. ENISA-trigger scenarios

ENISA / Empresa Emergente certification + the optional ENISA loan path materially affect runway. Two scenarios below:

### ENISA Plan A — certification only (no loan)

- Outcome: Empresa Emergente status + tax / labour benefits (€0 - €5 000 / year saved depending on payroll).
- Runway impact: marginal (tax savings, not cash injection).
- Operator decision: pursue regardless if pipeline supports the cost.

### ENISA Plan B — certification + loan

- Outcome: Empresa Emergente + ENISA-loan typically €25 000 - €100 000 at favourable terms.
- Runway impact: extends runway 6 - 24 months depending on draw amount.
- Operator decision: pursue if Scenario A or B above shows < 6 months runway by month 6.

> **TODO[OPERATOR-enisa-D1]** — choose Plan A or Plan B; informs the deck's slide 13 use-of-funds language.

## 9. ENISA cash-trigger summary

| Trigger | Action |
|:---|:---|
| Cash position ≤ 6 months runway | Submit ENISA loan application + confirm one alternative funding path (partner advance, customer prepay) |
| First paid KiRBe customer signed | Confirm Scenario B trajectory; revisit hire decision |
| First partner engagement signed > €25 000 | Reduces Scenario A risk; consider modest hiring |

## 10. What goes in the deck

Slide 12 (Roadmap) phase 0-6 anchors on the runway position in the chosen scenario; slide 13 (use of funds) reads from this artifact's mid-band burn × scenario × ENISA-plan to populate the four-line use-of-funds list with **proportional bands** (e.g. ~40 % productización, ~30 % hire, ~20 % infra, ~10 % asesoría).

## Deck-bound facts

```
slide_id: 12-roadmap
phase_0_6_runway:
  baseline_scenario: "TODO[OPERATOR-scenario-D1]"
  baseline_runway_months: "TODO[OPERATOR-cash-D1] / TODO[OPERATOR-burn-D1] (typically 6-15 months at base scenario)"
  break_even_target: "month 9-12 (Scenario B) | month 14-18 (Scenario C with engineer hire)"

slide_id: 13-enisa-fit
use_of_funds_split_recommendation:
  productization_kirbe: "~40%"
  hiring_spain: "~30%"
  infrastructure_observability: "~20%"
  legal_fiscal_certification: "~10%"
funds_label: "Reparto recomendado interno; band, no figure final."
funds_decision_owner: "TODO[OPERATOR-enisa-D1]"
```

## Cross-references

- [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md) — burn × revenue per channel = runway forecast inputs
- [`INVESTMENT_THESIS.md`](INVESTMENT_THESIS.md) — when bootstrapping is insufficient, raise
- [`FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`](../../../Finance/Business%20Controller/Taxes/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md) — pre-incorporation cost framing
- [`STRATEGY_DECISION_LOG.md`](STRATEGY_DECISION_LOG.md) D-IH-29-STR-7 (founder personal draw decision)
