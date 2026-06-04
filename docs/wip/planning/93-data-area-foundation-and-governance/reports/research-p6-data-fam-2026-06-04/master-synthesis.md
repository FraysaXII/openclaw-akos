---
intellectual_kind: research_master_synthesis
initiative: I93
pack_id: research-p6-data-fam-2026-06-04
authored: 2026-06-04
control_confidence_level: Safe
feeds_phase: P6
---

# Master synthesis — P6 DATA-FAM families + probe wiring

## Executive summary

P6 mints **seven named data products** (DATA-FAM umbrellas) as capability + confidence +
process rows, and wires **family-scoped DataOps probes** — starting with **compliance mirror
parity**. The **115/35** cross-area map is the engineering backlog; it does **not** block the
umbrella tranche. **I91** keeps graph-store scope; **I93** owns family CAP rows only.

P5c (BI plane + multi-area consumption) is a **hard prerequisite** — complete before P6 execution.

## Recommended P6 bundle (for operator ratification)

| Step | Deliverable |
|:---|:---|
| 1 | `DATA_FAM_PROBE_PROFILES` in `akos/hlk_dataops_quality.py` |
| 2 | `dataops_quality_check.py --data-fam COMPLIANCE-MIRROR` (first live probe) |
| 3 | Seven `CAP-HOL-DATA-FAM-*-001` rows |
| 4 | Seven `CONF-*` seeds (paired) |
| 5 | Seven `hol_data_dtp_datafam_*` process rows |
| 6 | `reports/p6-data-fam.tranche-charter.md` + synthesis PASS |

## Options for operator

| ID | Scope |
|:---|:---|
| **P6-A** | Full bundle above in **one CSV approval tranche** |
| **P6-B** | Umbrella CAP/CONF/process only; probes in **P6b** follow-up |
| **P6-C** | Umbrella + COMPLIANCE-MIRROR probe only; other families INFO-ramp |
| **P6-D** | Defer P6; run **area batch P6-Tech** first (6 unmapped) before umbrellas |

## I91 coordination

| Choice | Meaning |
|:---|:---|
| **COORD-1** | I93 family CAP rows only; I91 unchanged (recommended) |
| **COORD-2** | Joint charter with I91 before any P6 commit |

## Mirror DDL

| Choice | Meaning |
|:---|:---|
| **MIRROR-1** | P6 = parity **check** only; DDL emit tranche = P6b (recommended) |
| **MIRROR-2** | P6 includes DDL for all five gap CSVs (larger scope) |

---

*Ratification via AskQuestion in session — execution seat proceeds on chosen bundle only.*
