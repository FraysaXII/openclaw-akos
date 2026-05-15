---
language: en
status: scaffold
authored: 2026-05-15
---

# Pending GOI mint — recruiter intelligence target (`TODO[OPERATOR-goi-recruiter-001]`)

The canonical [`INTELLIGENCEOPS_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv) row **`IO-REC-PLACEHOLDER-001`** keeps `target_id` as **`TODO[OPERATOR-goi-recruiter-001]`** until the operator mints a concrete GOI row and replaces the placeholder **without inventing `goi_*` / `poi_*` IDs in automation** (per governance).

## Clears when

1. Operator adds or selects the governed **`goi_*` identifier** in the appropriate GOI register / workflow your process requires.
2. Operator updates **`INTELLIGENCEOPS_REGISTER.csv`** `target_id` for `IO-REC-PLACEHOLDER-001` (and any dependent paths) to that minted ID.
3. Validators: `validate_intelligenceops_register.py` + `validate_hlk.py` PASS on the resulting row set.

## Stub linkage (already wired)

- **`linked_sop_path`**: [`SOP-RECRUITER_ONBOARDING_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/People%20Operations/canonicals/SOP-RECRUITER_ONBOARDING_001.md)
- **`linked_runbook_path`**: [`scripts/peopl_recruiter_onboarding_checklist_stub.py`](../../../../../scripts/peopl_recruiter_onboarding_checklist_stub.py)
- **`process_list.csv`**: `tbi_peopl_dtp_recruiter_onboarding_001`
