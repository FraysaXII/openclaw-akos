---
intellectual_kind: research_prong_synthesis
parent_pack: research-p6-data-fam-2026-06-04
prong: C
authored: 2026-06-04
---

# Prong C — P6 execution risks and sequencing

## Risks

| Risk | Mitigation |
|:---|:---|
| Double-mint with I91 | Charter: I93 = family CAP only; document in decision-log |
| 35 unmapped processes block P6 | Umbrella mint does **not** require full mapping — area batches follow |
| Mirror DDL scope creep | P6 = parity **check** + forward charter rows; DDL tranche can be P6b |
| Operator CSV fatigue | Single coordinated tranche: 7+7+7 rows in one approval packet |
| Probe false positives | Start with COMPLIANCE-MIRROR only; INFO ramp per D-IH-86-BN pattern |

## Recommended execution order (Composer tranche)

1. `akos/hlk_dataops_quality.py` — add `DATA_FAM_PROBE_PROFILES`
2. `scripts/dataops_quality_check.py` — `--data-fam` flag
3. CAPABILITY_REGISTRY — 7 rows
4. CAPABILITY_CONFIDENCE_REGISTRY — 7 rows
5. process_list — 7 umbrella rows
6. Tests + `validate_hlk.py`
7. Synthesis charter + operator CSV approval gate

## Sub-tranches (post-umbrella)

| Batch | Areas | Est. processes |
|:---|:---|---:|
| P6-Tech | Tech | 6 unmapped |
| P6-Ops | Operations | 5 |
| P6-Research | Research | 9 |
| P6-People | People | 7 |
| P6-MKT | Marketing | 11 |
| P6-Finance | Finance | 1 |
| P6-Legal | Legal | 3 |
