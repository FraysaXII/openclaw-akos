---
intellectual_kind: ops_triage_tracker
sharing_label: internal_only
language: en
authored: 2026-06-04
last_review: 2026-06-04
status: active
role_owner: PMO
linked_decisions:
  - D-IH-90-AB
next_review_trigger: First 20 OPS rows dispositioned OR I86 cluster UAT close
---

# OPS_REGISTER open-row triage tracker (70 open)

Operator ratification 2026-06-04: **scope-extend** — triage remaining open OPS rows rather than parking until cluster UAT alone.

## Summary

| Bucket | Action | Target |
|:---|:---|:---|
| I86 cluster follow-ups | Close at cluster UAT | Wave coordinator |
| I59/I66 historical PMO seeds | Close or defer with forward pointer | PMO |
| I82 capability gaps | Link to I91 DATA coverage | Capability Curator |
| Eval harness (MADEIRA) | OPS-90-EVAL-1 (new) | AI Engineer |
| UX research SOP | Already forward-chartered | People |

## Triage batches (execute in order)

### Batch 1 — I90/I86 closure blockers (≤10 rows)

Close or attach evidence when cluster UAT mints:

- OPS-86-8, OPS-86-10, OPS-86-12 (verify current status in OPS_REGISTER.csv)
- OPS-86-24 (forward-only UAT baseline — observation row at UAT close)
- OPS-81-1 (hold until wave-close — resolve at I81 P9 or supersede)

### Batch 2 — Capability / DATA plane (≤15 rows)

Route to `data-area-capability-coverage-2026-06-04.md` phased plan.

### Batch 3 — Historical open rows (remaining ~45)

Mechanical pass: `py scripts/validate_ops_register.py` + per-row `status` flip with `linked_decision_ids`.

## New OPS rows to mint (this wave)

| Proposed ID | Summary | Owner | ETA |
|:---|:---|:---|:---|
| OPS-90-EVAL-1 | MADEIRA eval cassette harness green on Windows/py3.12 CI path | AI Engineer | 2026-06-11 |
| OPS-91-DATA-1 | I91 DATA-area capability coverage P1 (43 cadence-bound CAP+CONF) | Capability Curator | 2026-06-15 |
| OPS-91-DATA-2 | TECHOPS + UX charter→active promotion tranche | System Owner | 2026-06-15 |

## Verification

```text
py scripts/validate_ops_register.py
rg '^OPS-' docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv | wc
```
