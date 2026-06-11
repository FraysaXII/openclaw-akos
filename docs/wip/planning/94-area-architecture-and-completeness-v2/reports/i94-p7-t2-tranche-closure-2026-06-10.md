---
authored: 2026-06-10
tranche: I94-P7-AREA09-T2
parent_initiative: INIT-OPENCLAW_AKOS-94
operator_gate: ratified_option_a
linked_preview: i94-p7-t2-process-list-preview-2026-06-10.md
ratifying_decisions:
  - D-IH-94-A
status: completed
---

# I94 P7 T2 — AREA-09 process_list pairing tranche closure (2026-06-10)

## Summary

| Signal | Before P7 T2 | After P7 T2 |
|:---|:---|:---|
| Operations process rows (`granularity=process`) | 53 | 53 |
| Paired (`sop_path` + `runbook_path` both set) | 12 | **32** |
| Unpaired | 41 | **21** |
| P7 T2 rows applied | — | **20** |
| TBI RevOps SOPs minted (Option A) | — | **3** |

Operator gate: **Option A** — pair all 20 rows; mint 3 TBI SOPs in same wave before CSV tranche ([`i94-p7-t2-process-list-preview-2026-06-10.md`](i94-p7-t2-process-list-preview-2026-06-10.md), batch2 Q1-A).

## process_id list (20 rows)

| # | process_id | handoff class |
|---:|:---|:---|
| 1 | `hol_opera_dtp_310` | OPS-LOCAL-DO |
| 2 | `thi_opera_dtp_201` | OPS-LOCAL-DO |
| 3 | `thi_opera_dtp_220` | OPS-LOCAL-DO |
| 4 | `hol_opera_dtp_300` | OPS-LOCAL-DO |
| 5 | `thi_opera_dtp_250` | OPS-LOCAL-DO |
| 6 | `hol_opera_dtp_148` | OPS-TRIG-COMPLIANCE |
| 7 | `hol_opera_dtp_103` | OPS-TRIG-COMPLIANCE |
| 8 | `tbi_ops_dtp_revops_revenue_rollup_001` | OPS-TRIG-FINOPS |
| 9 | `tbi_ops_dtp_revops_persona_audit_001` | OPS-TRIG-RESEARCH |
| 10 | `tbi_ops_dtp_revops_crm_sync_001` | OPS-LOCAL-DO |
| 11 | `tbi_ops_dtp_revops_regulator_checkpoint_001` | OPS-TRIG-RESEARCH |
| 12 | `tbi_ops_dtp_revops_media_review_001` | OPS-TRIG-RESEARCH |
| 13 | `thi_opera_dtp_288` | OPS-TRIG-FINOPS |
| 14 | `hol_ops_dtp_71` | OPS-LOCAL-DO |
| 15 | `hol_eng_prc_estimation_001` | OPS-LOCAL-DO |
| 16 | `thi_opera_dtp_97` | OPS-LOCAL-DO |
| 17 | `thi_opera_dtp_121` | OPS-LOCAL-DO |
| 18 | `thi_opera_dtp_129` | OPS-LOCAL-DO |
| 19 | `hol_opera_dtp_312` | OPS-TRIG-COMPLIANCE |
| 20 | `hol_ops_pis_3` | OPS-TRIG-COMPLIANCE |

## Handoff class breakdown (P7 T2)

| Class | Rows |
|:---|---:|
| OPS-LOCAL-DO | 11 |
| OPS-TRIG-COMPLIANCE | 4 |
| OPS-TRIG-FINOPS | 2 |
| OPS-TRIG-RESEARCH | 3 |

## TBI SOPs minted (Option A)

| process_id | SOP |
|:---|:---|
| `tbi_ops_dtp_revops_crm_sync_001` | `SOP-REVOPS_CRM_SYNC_001.md` |
| `tbi_ops_dtp_revops_regulator_checkpoint_001` | `SOP-REVOPS_REGULATOR_CHECKPOINT_001.md` |
| `tbi_ops_dtp_revops_media_review_001` | `SOP-REVOPS_MEDIA_REVIEW_001.md` |

## Script + CSV

- Extended [`scripts/i94_area09_process_list_tranche.py`](../../../../scripts/i94_area09_process_list_tranche.py) — `P7_T2_PAIRINGS` dict (idempotent; merges with P3 `PAIRINGS`)
- Applied via operator-ratified write to [`process_list.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv)

## Evidence

```powershell
py scripts/validate_hlk.py
py scripts/validate_process_list_pairing.py
py scripts/validate_area_completeness.py --area Operations --matrix
```

**`validate_hlk.py`:**

```
OVERALL: PASS
```

**`validate_process_list_pairing.py`:**

```
PASS
```

**`validate_area_completeness.py --area Operations --matrix`:**

```
Operations | delivery_capacity | 13 | 2 | 0 | 1 | 93% | 10/10 | COMPLETE
Operations AREA-09-PAIRED-SOP-RUNBOOK partial (medium): paired processes=32/53
```

## Next

Per [`i94-operations-master-sweep-design-2026-06-10.md`](i94-operations-master-sweep-design-2026-06-10.md):

- **P8 T3** — ~21 remaining unpaired rows (or retire/merge inline-ratify)
- **Or P5/P6 first** — I88 solo-operator wiring + P6 UAT PWF on AREA-09 cliff (recommended sequence in P4 wave synthesis)

## Cross-references

- Preview packet: [`i94-p7-t2-process-list-preview-2026-06-10.md`](i94-p7-t2-process-list-preview-2026-06-10.md)
- P3 tranche evidence: [`i94-p3-area09-process-list-tranche-2026-06-10.md`](i94-p3-area09-process-list-tranche-2026-06-10.md)
- P4 session doctrine: [`i94-p4-session-doctrine-2026-06-10.md`](i94-p4-session-doctrine-2026-06-10.md)
- Cross-area map: [`i94-operations-cross-area-execution-map-2026-06-10.md`](i94-operations-cross-area-execution-map-2026-06-10.md)
