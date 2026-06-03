---
intellectual_kind: composer_bounded_packet
packet_id: I90-OPS-86-19-dataops-activation
target_seat: Composer (execution)
owning_initiative: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
status: blocked_on_operator
blocked_on: reports/decisions/decision-ops-86-19-dataops-activation-2026-06-01.md
execution_phase: P3c
---

# Composer packet — OPS-86-19 DataOps activation (P3c gated)

## Objective

Flip DataOps doctrine to `active` + ship SOP+runbook pair + resolve eight `thi_data_*` rows.

## Read first

- [`reports/decisions/decision-ops-86-19-dataops-activation-2026-06-01.md`](../reports/decisions/decision-ops-86-19-dataops-activation-2026-06-01.md)
- [`_trackers/dataops-activation-tracker.md`](../../_trackers/dataops-activation-tracker.md)
- [`DATAOPS_DISCIPLINE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/DATAOPS_DISCIPLINE.md)

## Deliverables

| Path | Work |
|:---|:---|
| `SOP-TECH_DATAOPS_QUALITY_001.md` | AC-HUMAN surface |
| `scripts/dataops_quality_check.py` | 7-dimension sweep + `--self-test` |
| `akos/hlk_dataops_quality.py` | Pydantic SSOT |
| `DATAOPS_DISCIPLINE.md` | `status: active` + `last_review_decision_id` |
| `process_list.csv` | **Operator gate** — tranche only |
| `DECISION_REGISTER.csv` | Promotion decision row |

## Validators

```powershell
py scripts/dataops_quality_check.py --self-test
py scripts/validate_hlk.py
py scripts/validate_process_list_pairing.py
```

## Acceptance

- All 8 `thi_data_*` rows have SOP+runbook paths OR documented removal rationale in OPS-86-19 notes.
- `dataops-activation-tracker.md` → `status: closed`.

## Escalate to Opus if

- I91 Phase E store-coverage validator conflicts with DataOps dimension numbering.
