---
intellectual_kind: decision_brief
ops_id: OPS-86-19
initiative_id: INIT-OPENCLAW_AKOS-86
parent_initiative: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
status: pending_operator
linked_decisions:
  - D-IH-86-CR
  - D-IH-86-BU
linked_packet: ../composer-packets/packet-ops-86-19-dataops-activation.md
language: en
---

# Decision brief — OPS-86-19 (DataOps doctrine activation)

## Question

What is the **minimum activation bundle** to flip `DATAOPS_DISCIPLINE.md` from `charter` → `active` and resolve the eight `thi_data_*` DIM-05 placeholders?

## Evidence

- Tracker: [`_trackers/dataops-activation-tracker.md`](../../_trackers/dataops-activation-tracker.md) — 8 rows documented as intentional placeholders (D-IH-86-CR contra-precedent).
- Parent canonical: [`DATAOPS_DISCIPLINE.md`](../../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/DATAOPS_DISCIPLINE.md).
- I91 coordination: store-coverage validator (Phase E) composes with DataOps quality dimensions — no duplicate doctrine (D-IH-91-I).

## Minimum bundle (P3c execution)

1. Successor decision row (e.g. `D-IH-86-BU-V2` or `D-IH-90-AA`) recording `charter` → `active`.
2. `SOP-TECH_DATAOPS_QUALITY_001.md` + `scripts/dataops_quality_check.py` + `akos/hlk_dataops_quality.py` + tests + `pre_commit` self-test.
3. Review each `thi_data_*` row: **rewrite** `linked_sop` / runbook pointers OR **remove** if redundant post-activation.
4. `process_list.csv` tranche — **PAUSE POINT #6** (operator gate).

## Options

| Option | Summary |
|:---|:---|
| **A — Full bundle at P3c** (recommended) | All four threads in one gated commit after P3a ratification. |
| **B — Runbook-only first** | Ship `dataops_quality_check.py` at INFO; defer SOP + process_list to Wave follow-up. |
| **C — Defer until I91 Phase E** | Wait for `validate_canonical_store_coverage.py` — delays DIM-05 clearance unnecessarily. |

## Recommendation

**Option A** at P3c — P3a only frames; Composer fleet must not flip doctrine status in P3b.

## Sufficiency test

Activation is sufficient when `py scripts/dataops_quality_check.py --self-test` PASS and regression sweep DIM-05 no longer lists `thi_data_*` as unpaired (or lists them with `accept-as-canon` decision cite).
