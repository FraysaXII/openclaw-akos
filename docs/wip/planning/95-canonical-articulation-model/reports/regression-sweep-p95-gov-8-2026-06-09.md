# Regression sweep — Wave-GOV close — 2026-06-09

**Report ID:** `regression-sweep-2026-06-09`  
**Swept by:** agent:inter_wave_regression_sweep  
**Wave closing:** Wave-GOV  

## Counts

| Verdict | Count |
| --- | --- |
| clean | 0 |
| drift | 0 |
| gap | 8 |
| blocked | 0 |
| skip | 0 |
| **TOTAL** | **8** |

## Findings

| Dimension | Surface | Verdict | Severity | Proposed action | Notes |
| --- | --- | --- | --- | --- | --- |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=aic_capability_implementation_matrix; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=aic; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ARTIFACT_CLASS_REGISTRY.csv` | gap | medium | mint missing components: scripts-validator, supabase-mirror-migration | slug=artifact_class; missing_components=scripts-validator,supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=audience; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/BUILDOUT_BACKLOG.csv` | gap | medium | mint missing components: supabase-mirror-migration, PRECEDENCE-entry | slug=buildout_backlog; missing_components=supabase-mirror-migration,PRECEDENCE-entry |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CANONICAL_GOVERNANCE_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration, PRECEDENCE-entry | slug=canonical_governance; missing_components=supabase-mirror-migration,PRECEDENCE-entry |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=capability_confidence; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=channel_touchpoint; missing_components=supabase-mirror-migration |

---

Per `akos-inter-wave-regression.mdc` RULE 3: every non-clean finding
MUST become one `AskQuestion` option set at P4 (inline-ratify gate).
