# Phase 1 — process_list tranche report

**Date:** 2026-04-17

## Candidate file

[`../candidates/process_list_tranche_holistika_internal.csv`](../candidates/process_list_tranche_holistika_internal.csv)

## Rows merged (operator execution)

| `item_id` | `item_name` |
|-----------|-------------|
| `holistika_gtm_dtp_001` | Holistika Internal GTM Proof Run (90-Day) |
| `holistika_gtm_dtp_002` | Agency Partner Proposal Intake and Fit Assessment |
| `holistika_gtm_dtp_003` | Inbound Response SLA (Holistika Services) |

## Tooling

- `py scripts/merge_process_list_tranche.py --candidate <path> [--write]`
- Gate: `py scripts/validate_hlk.py` (**PASS** after merge)

## baseline_organisation.csv

No changes in this tranche (existing roles only).
