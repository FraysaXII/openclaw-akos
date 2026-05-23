---
language: en
status: continuous
continuous_rationale: Auto-rendered review-stamp inbox (I71 P4) — re-renders from canonical CSVs on every validate_review_stamps.py run; never hand-edit between markers.
---

# Review-stamp inbox (I71 P4 — sidecar to OPERATOR_INBOX.md)

> **SSOT** is the four canonical CSVs that carry review-stamp columns
> (`process_list.csv`, `DECISION_REGISTER.csv`, `INITIATIVE_REGISTRY.csv`, `OPS_REGISTER.csv`).
> This file is auto-rendered by `scripts/validate_review_stamps.py` on every run.
> The dated section between the BEGIN/END markers is replaced wholesale; never hand-edit between them.
> Operator backfills review stamps in the canonical CSVs; subsequent runs drop backfilled rows from this inbox.

## Cadence

- **Stale window**: 180 days (6 months) per `D-IH-71-Q` default.
- **Missing-stamp grace**: rows authored within 30 days don't surface (operator review can wait until the row settles).
- **Invalid-decision-ref**: surfaces immediately as an `error` advisory (data integrity).

<!-- BEGIN REVIEW-STAMP-AUTO -->

_Last rendered: 2026-05-23 UTC (validate_review_stamps.py)._ 

## Invalid decision references (error)

| Canonical | Row PK | Detail |
|:---|:---|:---|
| `decision_register` | `D-IH-82-S` | last_review_decision_id='AIC-CURSOR-SDK-PROGRAMMATIC (forecasted; SUBS-ANYSPHERE-CURSOR-SDK). Seed MADEIRA_AIC_PER_TASK with 3 demonstrator rows for AIC-MADEIRA-ON-CURSOR (code-authoring + doctrine-curation + uat-verification; all operator-inline dispatcher + read-and-write RBAC). Resolves Wave-Q-vs-Wave-R coordination risk from operator-scratchpad point 6. Amends OPS-86-11 scope (Wave R no longer mints AIC_REGISTRY but still mints AGENTIC_TOOLING_OBSERVATIONS + AIC_INTERACTION_PATTERNS_REGISTRY).' not present in DECISION_REGISTER.csv decision_id column |
| `ops_register` | `OPS-86-14` | last_review_decision_id='System Owner' not present in DECISION_REGISTER.csv decision_id column |

## Stale rows (warning; review window exceeded)

_No advisories at this severity._

## Missing review stamps (info; backfill recommended)

| Canonical | Row PK | Detail |
|:---|:---|:---|
| `ops_register` | `OPS-86-14` | last_review_at empty; operator backfill recommended |

<!-- END REVIEW-STAMP-AUTO -->

## Cross-references

- Design doc: [`p4-design-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-design-2026-05-14.md).
- Phase report: [`p4-strand-c2-review-stamp-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-strand-c2-review-stamp-2026-05-14.md).
- SQL proposal (audit trail): [`sql-proposal-p4-review-stamp-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/sql-proposal-p4-review-stamp-2026-05-14.md).
- Sibling inbox (OPS): [`OPERATOR_INBOX.md`](OPERATOR_INBOX.md).
