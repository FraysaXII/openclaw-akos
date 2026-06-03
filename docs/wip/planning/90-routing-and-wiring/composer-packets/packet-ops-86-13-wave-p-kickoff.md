---
intellectual_kind: composer_bounded_packet
packet_id: I90-OPS-86-13-wave-p-kickoff
target_seat: Composer (execution)
owning_initiative: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
status: blocked_on_operator
blocked_on: reports/decisions/decision-ops-86-13-wave-p-kickoff-2026-06-01.md
---

# Composer packet — OPS-86-13 I82 P1 / I76 / I83 kickoff execution

## Objective

Execute ratified Wave P kickoff: close OPS-86-13 row + land I82 P1 tranche artifacts per pause-record checklist.

## Read first

- [`reports/decisions/decision-ops-86-13-wave-p-kickoff-2026-06-01.md`](../reports/decisions/decision-ops-86-13-wave-p-kickoff-2026-06-01.md)
- [`82-holistika-capability-doctrine/reports/p1-halt-pause-record-2026-05-21.md`](../../82-holistika-capability-doctrine/reports/p1-halt-pause-record-2026-05-21.md)

## Deliverables (P3c gated — **PAUSE POINT #6**)

| Location | Work |
|:---|:---|
| `docs/references/hlk/v3.0/.../canonicals/` | I82 P1 CSV tranche per ratified scope |
| `process_list.csv` | Operator-approved rows only |
| `76-madeira-elevation/` | P1–P3 forward execution if Option A/C ratified |
| `OPS_REGISTER.csv` | OPS-86-13 → `closed` |

## Validators

```powershell
py scripts/validate_hlk.py
py scripts/validate_process_list_pairing.py
```

## Acceptance

- Pause record checklist items updated PASS/N/A/DEFER.
- OPS-86-13 closed with `last_review_decision_id` pointing to ratifying row.

## Escalate to Opus if

- P1 tranche touches `baseline_organisation.csv` without prior GATE #1-style approval.
