---
tranche_id: i93-p6-data-fam
tranche_class: canonical_csv_mint
initiative: INIT-OPENCLAW_AKOS-93
authored: 2026-06-04
ratifying_decisions:
  - D-IH-93-F
  - D-IH-93-J
operator_ratification: P6-A + MIRROR-2 + I91 cross-initiative regression
reversibility: medium
---

# P6 tranche charter — DATA-FAM families + OPS-86-15 mirrors

## Scope

| In | Out |
|:---|:---|
| 7 DATA-FAM umbrella CAP+CONF+process rows | 35 unmapped area-batch processes |
| `DATA_FAM_PROBE_PROFILES` + `--data-fam` | Live Supabase DB connectivity probes |
| OPS-86-15 five mirror DDL + sync emit | I91 Neo4j P1 execution |

## Deliverables

1. `akos/hlk_dataops_quality.py` — profiles + OPS-86-15 mirror spec
2. `scripts/dataops_quality_check.py` — `--data-fam`; COMPLIANCE-MIRROR live repo parity probe
3. `supabase/migrations/20260604120000_i93_p6_ops8615_mirror_gap_closure.sql`
4. `scripts/sync_compliance_mirrors_from_csv.py` — five emitters + flags
5. CSV tranche: 7+7+7 rows
6. Regression reports: `i91-i93-cross-initiative-regression-2026-06-04.md`

## Verification

```powershell
py scripts/validate_hlk.py
py scripts/validate_capability_registry.py
py scripts/validate_capability_confidence_registry.py
py scripts/dataops_quality_check.py --self-test
py scripts/dataops_quality_check.py --data-fam COMPLIANCE-MIRROR
py -m pytest tests/test_dataops_quality_check.py tests/test_ops8615_mirror_emit.py -v
```

## Synthesis

Tranche class `canonical_csv_mint` — run `synthesis_before_tranche_check.py` before commit.
