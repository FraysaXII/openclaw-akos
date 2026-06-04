# Data area — v3.0 vault index

> O5-1 **Data** area under Admin. Charter:
> [`canonicals/DATA_AREA_CHARTER.md`](canonicals/DATA_AREA_CHARTER.md)
> (`inherited_pattern_id=pattern_area_buildout`, I93 P1).

## Sub-domains

| Sub-domain | Path | Purpose |
|:---|:---|:---|
| **Governance** | [`Governance/canonicals/`](Governance/canonicals/) | DataOps discipline, data-governance policy + contract standards (P2+), paired SOPs |
| **Architecture** | [`Architecture/canonicals/`](Architecture/canonicals/) | Three-tier data architecture doctrine (P3) |
| **Science** | [`Science/canonicals/`](Science/canonicals/) | Semantic / metrics layer (P3) |

## Key canonicals (P1)

| Artifact | Path |
|:---|:---|
| Area charter | [`canonicals/DATA_AREA_CHARTER.md`](canonicals/DATA_AREA_CHARTER.md) |
| DataOps discipline | [`Governance/canonicals/DATAOPS_DISCIPLINE.md`](Governance/canonicals/DATAOPS_DISCIPLINE.md) |
| DataOps quality SOP | [`Governance/canonicals/SOP-TECH_DATAOPS_QUALITY_001.md`](Governance/canonicals/SOP-TECH_DATAOPS_QUALITY_001.md) |

## Deprecation aliases (one cycle)

Legacy paths retain stubs only — do not edit:

- `People/canonicals/DATAOPS_DISCIPLINE.md` → Governance canonical above
- `Tech/System Owner/canonicals/SOP-TECH_DATAOPS_QUALITY_001.md` → Governance SOP above

## Programs

KiRBe program folders under `Governance/programs/` and `Architecture/programs/`
inherit engagement-folder doctrine from PMO; not expanded at P1.

## Verification

```powershell
py scripts/validate_area_completeness.py --matrix
py scripts/validate_hlk.py
```

Cross-area compliance SSOT remains under
[`People/Compliance/canonicals/`](../People/Compliance/canonicals/) per
[`PRECEDENCE.md`](../People/Compliance/canonicals/PRECEDENCE.md).
