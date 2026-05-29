---
language: en
intellectual_kind: migration_proposal
sharing_label: internal_only
status: pending_operator_confirmation
authored: 2026-05-29
parent_wave: I86 Wave R+5 C4
ratifying_decisions: []
---

# Legacy Research tree migration — proposed mapping (NO git mv until operator confirms)

**Source tree (legacy):** `docs/references/hlk/v3.0/Admin/O5-1/Research/`  
**Target topology:** `docs/references/hlk/v3.0/Research/<discipline>/` (area harmonization per Wave R+5 plan §6)

**STOP:** No `git mv` has been executed for this table. Operator confirmation required.

## Already at top-level `Research/` (do not move; update cross-links only)

| Path | Notes |
|:---|:---|
| `Research/README.md` | Area anchor (delivered C0) |
| `Research/canonicals/RESEARCH_AREA_CHARTER.md` | Area charter |
| `Research/Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md` | Discipline charter |
| `Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md` | Doctrine (15th QF specialty) |
| `Research/Methodology/canonicals/RESEARCH_RADAR_DISCIPLINE.md` | Doctrine (16th QF specialty; C1) |
| `Research/Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md` | Discipline charter |
| `Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md` | Doctrine |
| `Research/Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md` | Discipline charter |
| `Research/Validation/canonicals/VALIDATION_DISCIPLINE_CHARTER.md` | Discipline charter |

## Proposed moves from `Admin/O5-1/Research/` → top-level `Research/`

| Legacy path | Proposed destination | Conflict / merge note |
|:---|:---|:---|
| `Admin/O5-1/Research/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md` | `Research/canonicals/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md` | No conflict |
| `Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md` | `Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md` | No conflict |
| `Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md` | `Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md` | Pair with existing `RESEARCH_ACTION_DISCIPLINE.md` |
| `Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md` | `Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md` | Pair with `RESEARCH_RADAR_DISCIPLINE.md` |
| `Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` | `Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` | No conflict |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_ELICITATION_DISCIPLINE_001.md` | `Research/Intelligence/canonicals/SOP-IO_ELICITATION_DISCIPLINE_001.md` | No conflict |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_INTELLIGENCE_REPORT_001.md` | `Research/Intelligence/canonicals/SOP-IO_INTELLIGENCE_REPORT_001.md` | No conflict |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md` | `Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md` | No conflict |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-RESEARCH_ENGAGEMENT_TRIGGER_001.md` | `Research/Intelligence/canonicals/SOP-RESEARCH_ENGAGEMENT_TRIGGER_001.md` | No conflict |
| `Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` | `Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` | **SSOT after move** — update PRECEDENCE + validators + mirror emit paths in same commit |
| `Admin/O5-1/Research/Methodology Pillars/.gitkeep` | `Research/Methodology/Pillars/.gitkeep` | Rename folder (drop "Methodology " prefix space) |
| `Admin/O5-1/Research/Deep Research/.gitkeep` | `Research/Deep Research/.gitkeep` | No conflict |
| `Admin/O5-1/Research/HUMINT Techniques/.gitkeep` | `Research/HUMINT Techniques/.gitkeep` | No conflict |
| `Admin/O5-1/Research/Intelligence Matrix/.gitkeep` | `Research/Intelligence Matrix/.gitkeep` | No conflict |
| `Admin/O5-1/Research/OSINT Operations/.gitkeep` | `Research/OSINT Operations/.gitkeep` | No conflict |
| `Admin/O5-1/Research/Research Techniques/.gitkeep` | `Research/Research Techniques/.gitkeep` | No conflict |

## Post-move cleanup (same confirmed commit)

1. Remove empty `Admin/O5-1/Research/` tree after all files moved.
2. Grep-replace inbound links from `Admin/O5-1/Research/` → `Research/` across vault + wip + `akos/` FIELDNAMES paths if any.
3. Update `PRECEDENCE.md` rows that cite legacy paths.
4. Re-run `py scripts/validate_hlk.py` + `py scripts/validate_compliance_schema_drift.py`.

## Operator decision requested

- [ ] **Approve mapping as-is** — execute git mv in a follow-up commit.
- [ ] **Amend mapping** — reply with path corrections before any mv.
