---
language: en
status: active
canonical: true
role_owner: People Operations Manager
co_owner_role: Compliance Officer
area: People
entity: Holistika
intellectual_kind: sop-addendum
authored: 2026-05-16
last_review: 2026-05-16
last_review_by: People Operations Manager
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-73-D
  - D-IH-73-N
  - D-IH-80-D
parent_sop: SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md
companion_to:
  - SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md
ssot: true
---

# SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001 — Addendum (FINOPS + Compliance + Legal cross-area depth)

> Access level 5. Authored at I80 P5 (D-IH-80-D Option B retrofit pilot, 2026-05-16) as the fourth instantiation of `pattern_sop_addendum_split`. The body executor needs to know *what* to maintain and *when*; this addendum carries the cross-area depth — FINOPS counterparty linkage, Compliance access-level routing, Legal IP-clause matrix, and the operator-side ratifications that shaped the 7-class taxonomy — that auditors / FINOPS Lead / Legal Counsel / System Owner reference.

## A. The 7-class taxonomy — operator framing rationale (D-IH-73-D)

The 7 engagement classes (`eng_model_hourly_consultant` / `eng_model_milestone_consultant` / `eng_model_percentage_collaborator` / `eng_model_apprentice_learner` / `eng_model_investor_advisor` / `eng_model_outsourced_helper` / `eng_model_operator_self`) were ratified at I73 P1 inline-ratify gate per `D-IH-73-D`. The rationale for the cardinality and the choice of these specific classes lives at this level, not in the body executor's reading path.

**Why 7 classes and not 5 or 12.** The operator's framing at I73 was that engagement classes need to be discriminable along four orthogonal axes simultaneously: retribution pattern (hourly / milestone / percentage / equity / fixed) × SOC posture (full-trust / scoped / methodology-restricted) × IP clause class (work-product-only / shared-methodology / IP-contributor) × knowledge-access level (1-5). Five classes would have collapsed `outsourced_helper` into `hourly_consultant` (losing the SOC-restricted-helper distinction); twelve classes would have produced rows that differ only on a single axis cell (over-fragmentation that hurts the FK targeting downstream). Seven is the smallest count that preserves discriminability across all four axes.

**Why these specific 7 and not different 7.** Each class corresponds to a real engagement shape Holistika has executed (or is forward-charter for I-NN). The historical_examples cell in each row anchors the class against a concrete engagement instance, not an abstract pattern. New classes are added only when an engagement shape arises that does not fit any existing class along any of the four axes; the canonical-CSV gate (operator approval before commit) ensures this discipline.

## B. ENGAGEMENT_REGISTRY FK posture (D-IH-73-N)

The `engagement_model_id` column on [`ENGAGEMENT_REGISTRY.csv`](../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) is **nullable until UAT**. The auditor-facing rationale:

- Historical engagements pre-dating I73 do not have a clean class assignment; backfilling them all at once would create false-confidence rows. The nullable column lets new engagements take the FK while historical engagements remain explicit-null until reviewed.
- The operator-approved backfill cadence (per `D-IH-73-N`) is one historical-engagement-batch per quarter; UAT confirms the FK assignment via review of the engagement README + audit trail.
- After the I73 P-followup UAT closes, the column becomes NOT NULL; new engagement rows fail to commit if the FK is missing.

System Owner's quarterly audit cross-references the `ENGAGEMENT_REGISTRY.csv` rows against the registry FK target slugs to detect drift between People-side classification and PMO-side instance ownership. Mismatches surface as findings with a one-quarter remediation window.

## C. FINOPS counterparty linkage — no second SSOT

Per [`akos-holistika-operations.mdc`](../../../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"FINOPS / FINOPS_COUNTERPARTY_REGISTER", monetary identifiers for engagement payouts live in [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) — not duplicated in the engagement model registry.

The link mechanism: each engagement instance row in `ENGAGEMENT_REGISTRY.csv` carries a `finops_counterparty_id:` field (FK to `FINOPS_COUNTERPARTY_REGISTER.csv`). The `ENGAGEMENT_MODEL_REGISTRY.csv` row defines the *class* posture (e.g., percentage-collaborator means revenue-share payout); the FINOPS register defines the *instance* posture (which counterparty + which Stripe customer + which payout cadence). Cross-area integrity is: `ENGAGEMENT_REGISTRY.engagement_model_id` → `ENGAGEMENT_MODEL_REGISTRY` (class posture) AND `ENGAGEMENT_REGISTRY.finops_counterparty_id` → `FINOPS_COUNTERPARTY_REGISTER` (monetary posture).

When auditing payroll-adjacent engagements (per `SOP-ENGAGEMENT_PAYROLL_OPS_001.md`), the auditor reads the engagement instance row, follows the class FK to the model registry for posture, follows the FINOPS FK to the counterparty register for payout. No third SSOT is needed; the joint key carries all dimensions.

## D. Cross-area integration matrix

| Consuming canonical | What it reads from this registry | What it pings back |
|:---|:---|:---|
| `ENGAGEMENT_REGISTRY.csv` | `engagement_model_id` FK target list | Backfill cadence per `D-IH-73-N` |
| `FINOPS_COUNTERPARTY_REGISTER.csv` | Class-posture for counterparty payout-shape verification | None directly; PMO reconciles quarterly |
| `BASELINE_ORGANISATION.csv` | `role_owner` field validation (must be valid baseline role) | None |
| Stripe metadata layer (`hlk_billing_plane`) | Class-posture for routing payout to correct Stripe customer + product line | Mirror sync confirmation per quarter |
| Workspace folder skeleton (`WORKSPACE_BLUEPRINT_HOLISTIKA.md`) | Class-posture for selecting `_engagement-template/` shape | None |
| Legal templates (`Templates/Legal/`) | Class-posture for selecting NDA + IP-clause + retribution-clause variants | None |

## E. Operator framing decisions encoded

- **D-IH-73-D** (I73 P1) — 7-class taxonomy ratified.
- **D-IH-73-E** (I73 P3) — outsourced-helper work-product-only doctrine.
- **D-IH-73-M** (I73 P5) — quarterly SOC review cadence for outsourced-helper class.
- **D-IH-73-N** (I73 P-followup) — `engagement_model_id` nullable-until-UAT FK posture on `ENGAGEMENT_REGISTRY.csv`.
- **D-IH-80-D** (I80 P0) — body/addendum split retrofit pilot Option B; this addendum is the third file (after the I80 P2 stakeholder lenses pair and the I80 P4 agentic-ops + cross-area-breakthrough pair) to instantiate the pattern.

## F. Cross-references

- Body file: [`SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md`](SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md).
- Class FK target: [`ENGAGEMENT_MODEL_REGISTRY.csv`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv).
- Instance registry: [`ENGAGEMENT_REGISTRY.csv`](../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv).
- Monetary SSOT: [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv).
- Pattern provenance: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md #pattern-sop-addendum-split`](../../canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split).
- I80 retrofit charter: [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../../../../../../wip/planning/80-i79-lessons-learned/master-roadmap.md) §"P5 — I73 lifecycle SOP retrofit pilot".
