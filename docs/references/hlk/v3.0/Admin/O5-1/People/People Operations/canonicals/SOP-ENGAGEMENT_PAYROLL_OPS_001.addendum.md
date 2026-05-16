---
language: en
status: active
canonical: true
role_owner: People Operations Lead
co_owner_role: Business Controller
area: People
entity: Holistika
intellectual_kind: sop-addendum
authored: 2026-05-16
last_review: 2026-05-16
last_review_by: People Operations Lead
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-73-E
  - D-IH-73-J
  - D-IH-73-M
  - D-IH-80-D
parent_sop: SOP-ENGAGEMENT_PAYROLL_OPS_001.md
companion_to:
  - SOP-ENGAGEMENT_PAYROLL_OPS_001.md
ssot: true
---

# SOP-ENGAGEMENT_PAYROLL_OPS_001 — Addendum (FINOPS integration architecture + Stripe metadata routing + Ethics automation posture)

> Access level 5. Authored at I80 P5 (D-IH-80-D Option B retrofit pilot, 2026-05-16). The body executor needs to know *what* to do for outsourced SOC review and percentage payout reconciliation; this addendum carries the FINOPS integration architecture, Stripe metadata routing detail, Ethics automation posture matrix, and economic rationale for caps/thresholds that Business Controller / FINOPS Lead / Ethics Advisor reference.

## A. The "no second SSOT" rule — why FINOPS owns counterparty economics

Per [`akos-holistika-operations.mdc`](../../../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"FINOPS / FINOPS_COUNTERPARTY_REGISTER", monetary identifiers and economic terms for engagement payouts MUST live in [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) — never duplicated in People canonicals. This is the structural rule that prevents counterparty drift across People + FINOPS + RevOps.

The architecture:

- **`ENGAGEMENT_REGISTRY.csv`** (Compliance/canonicals/dimensions/) — instance registry; carries `engagement_id` + `engagement_model_id` (FK to People class registry) + `finops_counterparty_id` (FK to FINOPS counterparty register).
- **`FINOPS_COUNTERPARTY_REGISTER.csv`** (Compliance/canonicals/) — monetary SSOT; carries `counterparty_id` + payment cadence + payment method + Stripe customer ID + tax-form requirements + jurisdiction.
- **`finops.registered_fact`** (Supabase operational table) — fact ledger; one row per monetary event tied to a `counterparty_id`.

When People Ops needs to know payment cadence for an engagement: read `ENGAGEMENT_REGISTRY.engagement_id` → follow `finops_counterparty_id` FK → read FINOPS register row. Never hard-code payment cadence in People canonicals; never duplicate FINOPS columns.

## B. Stripe metadata routing for percentage collaborator payouts (D-IH-73-J)

When a deal closes for a `eng_model_percentage_collaborator` engagement, the Stripe metadata layer (`hlk_billing_plane`) must route the revenue event correctly. The mechanism:

- The originating Stripe customer (the customer paying Holistika) is the upstream metadata source; the revenue event lands in `holistika_ops.stripe_customer_link` → `finops.registered_fact`.
- The `finops.registered_fact` row carries the originating `stripe_customer_id` + the revenue amount + the engagement_id (joined via the deal-pipeline metadata).
- The percentage payout calculation reads the `engagement_id` → follows to `engagement_model_id=eng_model_percentage_collaborator` → reads the engagement instance's `collaborator_share_pct:` field (in the engagement README's frontmatter, audit-trailed; FINOPS does not store this).
- The runbook computes the share + creates a payout-side `finops.registered_fact` row tied to the collaborator's `finops_counterparty_id`.

Audit cross-reference: every percentage-collaborator payout has TWO `finops.registered_fact` rows (revenue inbound + payout outbound) joined by the `engagement_id` metadata. Quarterly Business Controller reconciliation confirms the join integrity.

## C. €400/mo cap for outsourced helper class — economic rationale

The body §4.3 references "€400/mo cap compliance where applicable." The auditor-facing rationale:

The cap exists to enforce two structural constraints:

1. **Methodology exposure boundary.** An outsourced helper engaged at >€400/mo of total exposure either has substantial methodology access (which violates `D-IH-73-E` work-product-only doctrine) OR has been mis-classified (should be `hourly_consultant` or `milestone_consultant`). The cap is a forcing function for re-classification at the threshold.
2. **Quarterly review tractability.** SOC review per `D-IH-73-M` happens quarterly across all outsourced helpers; capping monthly exposure caps quarterly exposure (~€1,200/quarter); People Operations Lead can review 10 helpers in a sitting (~€12K/quarter total exposure across the class). Higher caps would compress the review cadence beyond practical bandwidth.

When an engagement legitimately requires >€400/mo of outsourced-helper-class work, the operator-approved exception process is:
1. Re-classify to `hourly_consultant` or `milestone_consultant` (different SOC posture; cap does not apply).
2. Or split into multiple outsourced-helper engagements each within cap (rare; only when the work genuinely segments).
3. Or operator-approved exception with explicit `D-IH-NN-X` decision row + quarterly review intensity increase.

## D. Ethics automation posture matrix

The body §6 references "Ethics if automation posture conflicts arise" pointing to [`ETHICAL_AUTOMATION_POSTURE.md`](../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md). The matrix detail:

| Engagement class | Automation posture | Ethics review cadence |
|:---|:---|:---|
| `hourly_consultant` | full-trust automation OK; consultant runs scripts on AKOS scope | Annual; ad-hoc on script-class change |
| `milestone_consultant` | scoped automation OK per milestone | Annual |
| `percentage_collaborator` | full-trust automation; share-aware automations need review | Annual; ad-hoc on share-aware automation introduction |
| `apprentice_learner` | restricted automation; no scripts that affect canonicals | Quarterly |
| `investor_advisor` | restricted automation; cap-table or financial scripts forbidden | Annual; ad-hoc on advisor-led financial automation |
| `outsourced_helper` | no automation; work-product-only delivery | Quarterly per `D-IH-73-M` |
| `operator_self` | full automation | Continuous (operator self-audit) |

When an engagement's automation posture conflicts with the matrix (e.g., outsourced helper requests script execution access), the engagement is paused; Ethics review per [`ETHICAL_AGENTIC_BOUNDARIES.md`](../../canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) §6 escalation procedure.

## E. Operator framing decisions encoded

- **D-IH-73-E** (I73 P3) — outsourced-helper work-product-only doctrine.
- **D-IH-73-J** (I73 P5) — percentage collaborator payout reconciliation procedure.
- **D-IH-73-M** (I73 P5) — quarterly SOC review cadence for outsourced-helper class.
- **D-IH-80-D** (I80 P0) — body/addendum split retrofit pilot.

## F. Cross-references

- Body file: [`SOP-ENGAGEMENT_PAYROLL_OPS_001.md`](SOP-ENGAGEMENT_PAYROLL_OPS_001.md).
- FINOPS architecture rule: [`akos-holistika-operations.mdc`](../../../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"FINOPS counterparty integration".
- FINOPS register: [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv).
- Ethics automation posture: [`ETHICAL_AUTOMATION_POSTURE.md`](../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md).
- Pattern provenance: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md #pattern-sop-addendum-split`](../../canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split).
- I80 retrofit charter: [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../../../../../../wip/planning/80-i79-lessons-learned/master-roadmap.md) §"P5".
