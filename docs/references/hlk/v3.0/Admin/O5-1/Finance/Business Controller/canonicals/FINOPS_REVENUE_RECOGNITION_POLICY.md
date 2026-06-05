---
title: FINOPS Revenue Recognition Policy
language: en
intellectual_kind: finance-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Business Controller
co_authors:
  - CFO
last_review: 2026-06-05
last_review_by: Business Controller
last_review_at: 2026-06-05
last_review_decision_id: D-IH-88-E
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-81-N
  - D-IH-81-P
  - D-IH-88-E
status: active
register: internal
linked_canonicals:
  - ../../Governance/canonicals/FINOPS_DISCIPLINE.md
  - ../../canonicals/FINANCE_AREA_CHARTER.md
  - ../../Governance/canonicals/dimensions/PRICING_TIER_REGISTRY.csv
  - ../../Governance/canonicals/dimensions/FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv
  - ../../../Operations/PMO/canonicals/business-strategy/PRICING_MODEL.md
  - ../../../People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv
linked_runbooks:
  - scripts/validate_pricing_tier_registry.py
  - scripts/validate_finops_ledger.py
companion_to:
  - ../../Governance/canonicals/FINOPS_DISCIPLINE.md
---

# FINOPS Revenue Recognition Policy

> **Plane 2 SSOT** for Holistika revenue recognition posture. Minted at
> FINANCE-AREA-FULL **F2a** per **D-IH-88-E**; closes **OPS-81-5** and pairs
> with `PRICING_TIER_REGISTRY.csv` (**OPS-81-6**). Commercial narrative remains
> in PMO `PRICING_MODEL.md`; this policy owns **recognition timing** and
> **performance-obligation mapping**.

## 1. Accounting framework

Holistika recognises revenue under **IFRS 15** (five-step model), applied in a
**Spain GAAP-equivalent** posture for the operating entity. Evidence grounding:
**EXT-04** (KPMG ASC 606 / IFRS 15 handbook 2025) for policy structure;
internal charter gates (**D-IH-81-N**, **D-IH-81-P**) for internal-first
ratification before external CFOaaS review at scale.

| Step | Holistika application |
|:---|:---|
| 1 Contract | Engagement registry + Stripe subscription / invoice objects |
| 2 Performance obligations | `FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv` |
| 3 Transaction price | PMO pricing bands + registry tier; no production amounts in git |
| 4 Allocation | Single PO default for KiRBe tiers; split when metered overage billed |
| 5 Recognition | Ratable (over time) or upon acceptance (point in time) per §3 |

## 2. Scope

| In scope | Out of scope |
|:---|:---|
| KiRBe SaaS tiers (`PRICING_TIER_REGISTRY`) | Tax filing calendar (F2b) |
| Service engagements (fixed-price packages) | Full ERP general ledger |
| Partner revenue share | Production monetary amounts in git (`thi_finan_dtp_306` gate) |
| Deferred revenue on annual prepay | Ad-hoc spreadsheets |

## 3. Performance obligation table

Each obligation ID must exist in
[`FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv`](../../Governance/canonicals/dimensions/FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv)
and be referenced by at least one pricing tier where applicable.

### 3.1 PO-FIN-HOL-PLATFORM-ACCESS

**Pattern:** over time. **Trigger:** customer has access to KiRBe for the
subscription period. **Tiers:** `PT-FIN-HOL-STARTER`, `PT-FIN-HOL-GROWTH`,
`PT-FIN-HOL-PRO`, `PT-FIN-HOL-PLUS`.

### 3.2 PO-FIN-HOL-METERED-USAGE

**Pattern:** over time. **Trigger:** query usage above tier quota in the
billing period. **Tiers:** any KiRBe tier with metered overage per PMO
`PRICING_MODEL.md` §1.2.

### 3.3 PO-FIN-HOL-SERVICE-OUTCOME

**Pattern:** point in time (or over time when SOW spans multiple milestones).
**Trigger:** documented acceptance of scoped outcome. **Tiers:**
`PT-FIN-HOL-CONSULTANT` and service rate-card engagements.

### 3.4 PO-FIN-HOL-PARTNER-REVSHARE

**Pattern:** over time. **Trigger:** end-client revenue event with probable
collectability; Holistika share per engagement model. **Join:**
`DC-HOL-REVOPS-FINOPS-ENGAGEMENT-001`.

### 3.5 PO-FIN-HOL-TRIAL-ACCESS

**Pattern:** over time (zero transaction price). **Trigger:** trial period
active; **no revenue** until conversion to a paid tier.

## 4. Deferred revenue and annual prepay

When `billing_cadence=annual_prepay` (e.g. `PT-FIN-HOL-PLUS`):

1. Invoice / charge creates a **contract liability** (deferred revenue).
2. Recognition follows **straight-line** ratable release over the prepay term.
3. Refunds and pro-ration: reverse deferred balance for unused period per
   Stripe credit-note event; log lineage on `finops.registered_fact` at F3.

## 5. Refunds and pro-ration

- **Subscription cancel mid-term:** stop recognition; true-up deferred balance.
- **Service engagement:** only recognised amounts subject to acceptance;
  refunds adjust the period of reversal, not prior closed periods without error.
- **Partner share:** adjust Holistika share when end-client refund confirmed.

## 6. Cross-area contracts

Producer-consumer obligations for monetary surfaces are declared in
`DATA_CONTRACT_REGISTRY` DC-HOL-FINOPS-* rows (FIN-05). Consumers must not
book against orphan Stripe customers — `finops_counterparty_id` spine required.

## 7. Verification

```powershell
py scripts/validate_pricing_tier_registry.py
py scripts/validate_data_contract_registry.py
py scripts/validate_finops_ledger.py
```

## 8. Promotion history

| Date | Status | Decision |
|:---|:---|:---|
| 2026-06-05 | charter → **active** | D-IH-88-E (F2a mint) |
