---
intellectual_kind: composer_bounded_packet
packet_id: I90-OPS-86-9-qf-runbooks
target_seat: Composer (execution)
owning_initiative: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
status: ready
---

# Composer packet — OPS-86-9 TechOps runbook (P3b no-gate)

## Objective

Ship `scripts/techops_reliability_check.py` + Pydantic chassis + tests + `pre_commit` self-test per QF specialty pattern.

## Read first

- [`reports/decisions/decision-ops-86-9-qf-runbooks-2026-06-01.md`](../reports/decisions/decision-ops-86-9-qf-runbooks-2026-06-01.md)
- [`TECHOPS_DISCIPLINE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/TECHOPS_DISCIPLINE.md)
- Precedent: [`scripts/validate_inter_wave_regression.py`](../../../../scripts/validate_inter_wave_regression.py) self-test wiring

## Deliverables

| Path | Work |
|:---|:---|
| `akos/hlk_techops_reliability.py` | Frozen models; 7-dimension probe enum |
| `scripts/techops_reliability_check.py` | `--self-test` + full sweep CLI |
| `tests/test_techops_reliability_check.py` | Valid + invalid fixtures |
| `config/verification-profiles.json` | `pre_commit` step (INFO) |
| `scripts/release-gate.py` | Advisory hook |

## Do NOT (this packet)

- Mint `scripts/mktops_campaign_quality_check.py` (OPS-86-25 park).
- Flip `DATAOPS_DISCIPLINE.md` status (OPS-86-19 / P3c).
- Mint `SOP-PEOPLE_UX_RESEARCH_001` (forward-charter).

## Acceptance

- `py scripts/techops_reliability_check.py --self-test` exit 0.
- `py scripts/verify.py pre_commit` PASS.
- Update OPS-86-9 notes: TechOps thread complete; MKTOPS/UX parked.

## Escalate to Opus if

- Probe set needs new canonical CSV column (schema gate).
