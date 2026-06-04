---
intellectual_kind: research_prong_synthesis
parent_pack: research-p6-data-fam-2026-06-04
prong: A
authored: 2026-06-04
---

# Prong A — Internal evidence for P6 DATA-FAM tranche

## What P6 must deliver (roadmap binding)

1. **Seven umbrella capabilities** — `CAP-HOL-DATA-FAM-*-001` in `CAPABILITY_REGISTRY.csv`
2. **Seven confidence seeds** — matching `CONF-*` in `CAPABILITY_CONFIDENCE_REGISTRY.csv`
3. **Seven process rows** — `hol_data_dtp_datafam_*` under `thi_data_prj_1` with `pattern_dataops_discipline`
4. **Probe wiring** — `DATA_FAM_PROBE_PROFILES` + `--data-fam` on `dataops_quality_check.py`
5. **First live probe** — mirror parity (closes OPS-86-15 gap for 5 CSVs)
6. **Cross-area map** — 115 classified; **35 unmapped** → area sub-tranches (not blocking umbrella mint)

## Seven families (from I90 + cross-area map)

| Family | Processes (classified) | Primary probe cluster |
|:---|---:|:---|
| DATA-FAM-COMPLIANCE-MIRROR | 12 | DATA-01,02,03 |
| DATA-FAM-CANONICAL-CSV | 44 | DATA-01,05,07 + validate_hlk |
| DATA-FAM-ENGAGEMENT-FACT | 18 | DATA-01,07 + engagement validators |
| DATA-FAM-TELEMETRY-OBS | 8 | DATA-04,07 + techops |
| DATA-FAM-GTM-CRM | 5 | DATA-03,04 + finops |
| DATA-FAM-KM-TOPIC | 7 | DATA-06 + KM manifests |
| DATA-FAM-AIC-RUNTIME | 5 | DATA-06,07 + MADEIRA |

## Dependencies satisfied by P5c

- BI/integration plane minted (`D-IH-93-I`, `D-IH-93-J`)
- `AREA_BI_PROFILE.csv` — areas declare consumption before P6 probes claim ENGAGEMENT-FACT health
- Contract registry operating model live (P2b)

## I91 coordination rule

| I93 owns | I91 owns |
|:---|:---|
| Family-level CAP+CONF umbrella rows | Store inventory + Neo4j graph projection |
| `--data-fam` probe profiles on DataOps | Graph coverage milestones |

Do **not** duplicate I91 graph CAP rows in P6 tranche.

## Operator gate (non-negotiable)

`process_list.csv` + `CAPABILITY_REGISTRY.csv` + `CAPABILITY_CONFIDENCE_REGISTRY.csv` edits require **explicit operator approval** per baseline governance — P6 is canonical-CSV class.
