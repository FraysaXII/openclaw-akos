---
status: active
role_owner: PMO
area: Operations / PMO
entity: Holistika Research
program_id: shared
plane: ops
topic_ids:
  - topic_strategy_decisions
parent_topic: topic_business_strategy
artifact_role: canonical
intellectual_kind: decision_log
authority: Founder + PMO
last_review: 2026-04-30
---

# Strategy Decision Log

> Material business-strategy decisions. One row per decision: id, date, scope, options considered, decision, rationale, trigger to revisit. Decisions made in other artifacts (`PRICING_MODEL.md`, `BOOTSTRAPPING_PLAN.md`, etc.) are summarised here so the founder has one chronological view.

## Decision table

| ID | Date | Scope | Options | Decision | Rationale | Revisit trigger |
|:---|:---|:---|:---|:---|:---|:---|
| `D-IH-29-STR-1` | 2026-04-30 | Strategy SSOT location | (a) `Operations/PMO/business-strategy/`; (b) `Finance/Business Controller/`; (c) shared `_assets/strategy/` | (a) PMO/business-strategy | PMO chain owns multi-discipline strategy; Finance owns the BOOTSTRAPPING_PLAN section but the parent is PMO; `_assets/` is for visual outputs not Markdown SSOT | A discipline becomes the dominant owner (e.g. CFO chain takes over) → migrate folder |
| `D-IH-29-STR-2` | 2026-04-30 | TODO[OPERATOR] pattern | (a) blank slots; (b) research-grounded bands + named TODO[OPERATOR-x]; (c) one giant TODO at top of each file | (b) | Founder needs context to decide; bands are research-grounded so the deck-sync script can use them as fallback values | Founder requests blank slots later (refactor to (a)) |
| `D-IH-29-STR-3` | 2026-04-30 | Service rate currency | (a) EUR; (b) USD; (c) dual | (a) EUR | Domiciled in Spain, ENISA narrative, Spanish adviser, EUR primary | First USD-billed engagement closes → revisit |
| `D-IH-29-STR-4` | 2026-04-30 | KiRBe pricing tier count | (a) 2 tiers; (b) 3 tiers + enterprise; (c) 4 tiers; (d) usage-only | (b) — 3 tiers + enterprise + metered overage | 2026 SaaS research: 3 tiers is the converting structure; >4 drops conversions ~30 %; hybrid (subscription + usage) outgrows flat by 8 pp | First 5 paying KiRBe customers reveal mismatch with tiering → revisit |
| `TODO[OPERATOR-D5]` | TODO | Capital social amount | (a) 1 EUR formación sucesiva; (b) 1 000-2 000 EUR; (c) ≥ 3 000 EUR | TODO | Operator decides per `BOOTSTRAPPING_PLAN.md` and `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md` | Notary signing date |
| `TODO[OPERATOR-D6]` | TODO | Whether to raise external capital in 0-12 months | (a) bootstrap-only; (b) ENISA loan only; (c) angel / pre-seed; (d) deferred | TODO | Operator decides per `INVESTMENT_THESIS.md` once `BOOTSTRAPPING_PLAN.md` shows runway position | First funded engagement OR runway < 6 months |
| `TODO[OPERATOR-D7]` | TODO | Founder personal monthly draw | (a) zero (live off savings); (b) minimum-viable (€1.5 - 2k / mo); (c) market-rate (€4 - 6k / mo deferred) | TODO | Operator decides per `BOOTSTRAPPING_PLAN.md` personal split | Cash flow positive OR external capital lands |

## How to add a row

1. Open this file.
2. Append a new row with a fresh `D-IH-29-STR-N` id (or another initiative id if outside I29).
3. Fill date, scope, options, decision, rationale, revisit trigger.
4. If the decision affects another artifact in this folder, link to it from the rationale column.
5. Commit per the I29 phase-scoped commit strategy.

## Cross-references

- [`README.md`](README.md) — folder index
- [`PRICING_MODEL.md`](PRICING_MODEL.md), [`BOOTSTRAPPING_PLAN.md`](BOOTSTRAPPING_PLAN.md), [`INVESTMENT_THESIS.md`](INVESTMENT_THESIS.md) — deeper detail on D4 / D5 / D6 / D7
- I29 master roadmap: [`docs/wip/planning/29-multi-phase-consolidation/master-roadmap.md`](../../../../../../wip/planning/29-multi-phase-consolidation/master-roadmap.md)
