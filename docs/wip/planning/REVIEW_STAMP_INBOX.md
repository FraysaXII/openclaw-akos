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

_Last rendered: 2026-06-01 UTC (validate_review_stamps.py)._ 

## Invalid decision references (error)

_No advisories at this severity._

## Stale rows (warning; review window exceeded)

_No advisories at this severity._

## Missing review stamps (info; backfill recommended)

_No advisories at this severity._

<!-- END REVIEW-STAMP-AUTO -->

## Cross-references

- Design doc: [`p4-design-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-design-2026-05-14.md).
- Phase report: [`p4-strand-c2-review-stamp-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-strand-c2-review-stamp-2026-05-14.md).
- SQL proposal (audit trail): [`sql-proposal-p4-review-stamp-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/sql-proposal-p4-review-stamp-2026-05-14.md).
- Sibling inbox (OPS): [`OPERATOR_INBOX.md`](OPERATOR_INBOX.md).
