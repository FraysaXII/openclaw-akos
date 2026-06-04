---
audience: J-OP
last_review: 2026-06-04
linked_decisions:
  - D-IH-90-AA
  - D-IH-82-P
  - D-IH-86-BV
ratifying_research:
  - DAMA-DMBOK2 2024 revision Ch.13 (nine DQ dimensions + Currency)
  - RESEARCH_HEAD_DISCIPLINE.md §6 backfill protocol
status: research-synthesis
---

# DATA-area capability coverage — process_list → CAPABILITY_REGISTRY gap analysis

## Operator intent (verbatim framing, 2026-06-04)

Data must support everything Holistika does — governance is the key, and DAMA is the driver of the operator's vision across all initiatives (present and aspirational). The ~1,188-row process_list was always expected to need a matching capability plane; DataOps activation is the first executable wedge, not the finish line.

## Internal evidence sweep

| Signal | Count | Implication |
|:---|---:|:---|
| `process_list.csv` total rows | 1,188 | Full org process baseline |
| `item_granularity=process` | 440 | Executable processes needing capability FK |
| Formal `area=Data` processes | 6 | Under-scoped vs 161 data-tagged / MasterData rows |
| `CAPABILITY_REGISTRY.csv` rows | 1,103 | Wave Q seed from I81 matrix; not 1:1 with 440 processes |
| Cadence-bound processes (SOP+runbook bar) | 43 | Highest-priority capability candidates |
| DATAOPS active specialty | 1 | `env_tech_dtp_dataops_quality_001` umbrella |

### Process distribution by area (executable processes only)

| Area | Process count |
|:---|---:|
| Tech | 115 |
| Operations | 105 |
| Research | 71 |
| People | 64 |
| MKT | 56 |
| Finance | 16 |
| Legal | 6 |
| Data | 6 |
| Marketing | 1 |

**Load-bearing insight:** Data governance touches every area (FINOPS mirrors, compliance CSVs, engagement registers, MADEIRA telemetry) but only 6 rows carry `area=Data`. The DATA **plane** is cross-cutting — capability coverage must be **by data-product / mirror-family / probe lane**, not by org-chart area column alone.

## External research enrichment

| Source | Application |
|:---|:---|
| [DAMA DMBOK 2.0 Revision (2024)](https://dama.org/dama-dmbok-revision/) | Nine DQ dimensions (adds **Currency**); Ch.13 cross-links DQ to Metadata, RMDM, DII — maps to DATA-01..07 + forward DATA-08 metadata probe |
| DAMA Ch.13 improvement lifecycle | Justifies phased capability rollout: profile → measure → improve → monitor (matches I82 confidence registry + DataOps sweep cadence) |
| Holistika two-plane ops (akos-holistika-operations) | Git-canonical CSV (schema) + mirror DML (operational facts) — every mirror family is a DATA capability product |

## Proposed DATA capability taxonomy (7 families)

Maps 440 executable processes into governable DATA products without minting 440 CAP rows in one commit:

| Family code | DATA product | Example process clusters | Probe / runbook |
|:---|:---|:---|:---|
| **DATA-FAM-COMPLIANCE-MIRROR** | compliance.* mirrors | All `*_mirror` emit paths; FINOPS; GOI/POI; adapter registries | `dataops_quality_check.py --sweep` DATA-01..03 |
| **DATA-FAM-CANONICAL-CSV** | Git CSV SSOT | process_list, baseline_org, all dimensions/*.csv | validate_hlk.py + schema drift |
| **DATA-FAM-ENGAGEMENT-FACT** | Engagement operational facts | hol_eng_* ; SUEZ POC data products | Engagement CSV validators |
| **DATA-FAM-TELEMETRY-OBS** | Observability + eval facts | MADEIRA telemetry; Sentry; Langfuse | techops + eval harness |
| **DATA-FAM-GTM-CRM** | holistika_ops GTM plane | lead_intake; stripe links | FINOPS + GTM SOPs |
| **DATA-FAM-KM-TOPIC** | Topic-Fact-Source graph | TOPIC_REGISTRY; manifests | validate_hlk_km_manifests |
| **DATA-FAM-AIC-RUNTIME** | Agent runtime persistence | MADEIRA persistence vehicles | madeira_persistence_check |

Each family gets: 1 umbrella `process_list` row (if missing) + 1 CAP row + 1 CONF seed + 1 DATAOPS sweep profile extension.

## Phased execution (recommended)

| Phase | Scope | Rows | Gate |
|:---|:---|---:|:---|
| **P0 (done)** | DataOps QF specialty active | 1 | D-IH-90-AA ✓ |
| **P1 (next)** | Cadence-bound 43 processes → CAP+CONF backfill | 43 | Operator CSV tranche |
| **P2** | Mirror-family probes DATA-FAM-* | 7 families | I91 charter |
| **P3** | Remaining 397 processes by area batch | ~400 | Quarterly waves |
| **P4** | TECHOPS + UX + MKTOPS specialty promotions | 3 | Same tranche as P2 |

## Immediate actions (this session)

1. ✓ BT-06 enriched with DATA-as-substrate breakthrough (LOGIC_CHANGE_LOG)
2. ✓ CAP-HOL-DATAOPS-QUALITY-CHECK-001 + CONF seed
3. → OPS-91-1 tracker for 70 open OPS triage (operator ratified scope-extend)
4. → Forward charter `docs/wip/planning/_candidates/i91-data-area-capability-coverage.md`
5. → TECHOPS + UX promotion tranche (charter→active) bundled with I91 P2

## Cross-references

- I82 capability doctrine: `docs/wip/planning/82-holistika-capability-doctrine/master-roadmap.md`
- I90 P3c: `reports/p3c-dataops-activation-2026-06-04.md`
- DATAOPS_DISCIPLINE.md
- PRECEDENCE.md compliance mirror rows
