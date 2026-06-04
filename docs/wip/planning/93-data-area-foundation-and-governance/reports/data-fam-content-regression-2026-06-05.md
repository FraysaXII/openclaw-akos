---
intellectual_kind: regression_report
initiative: I93
phase: P6-followup
authored: 2026-06-05
verdict: remediated_pre_commit
research_pack: reports/research-data-fam-content-regression-2026-06-05/
---

# DATA-FAM content regression — seven umbrella families (2026-06-05)

## Scope

**Content-quality** review (not mechanical validators alone) of the seven P6 DATA-FAM
umbrella capabilities (`D-IH-93-F`), their CAP/CONF/process rows, contract registry
coverage, probe profiles, operator mirror path, and cross-area map narrative.

| # | DATA-FAM code | CAP row | Process row |
|:---|:---|:---|:---|
| 1 | COMPLIANCE-MIRROR | CAP-HOL-DATA-FAM-COMPLIANCE-MIRROR-001 | hol_data_dtp_datafam_compliance_mirror_001 |
| 2 | CANONICAL-CSV | CAP-HOL-DATA-FAM-CANONICAL-CSV-001 | hol_data_dtp_datafam_canonical_csv_001 |
| 3 | ENGAGEMENT-FACT | CAP-HOL-DATA-FAM-ENGAGEMENT-FACT-001 | hol_data_dtp_datafam_engagement_fact_001 |
| 4 | TELEMETRY-OBS | CAP-HOL-DATA-FAM-TELEMETRY-OBS-001 | hol_data_dtp_datafam_telemetry_obs_001 |
| 5 | GTM-CRM | CAP-HOL-DATA-FAM-GTM-CRM-001 | hol_data_dtp_datafam_gtm_crm_001 |
| 6 | KM-TOPIC | CAP-HOL-DATA-FAM-KM-TOPIC-001 | hol_data_dtp_datafam_km_topic_001 |
| 7 | AIC-RUNTIME | CAP-HOL-DATA-FAM-AIC-RUNTIME-001 | hol_data_dtp_datafam_aic_runtime_001 |

**Quality bar:** `DATAOPS_DISCIPLINE.md` §2 dimensions, `DATA_CATALOG_INTEGRATION_POSTURE.md`
§5–§9 governed-claim bar, data-mesh federated product ownership (Dehghani 2020; DAMA-DMBOK
maturity lens per Irish G2G advice note 2024).

## Internal evidence sweep

| Check | Result |
|:---|:---|
| CAP ↔ CONF pairing (7 rows each) | Aligned — seed_v1_unrated CONF rows present |
| `DATA_FAM_PROBE_PROFILES` in `akos/hlk_dataops_quality.py` | Seven keys match cross-area map § probe table |
| `dataops_quality_check.py --data-fam COMPLIANCE-MIRROR` | PASS (DDL+emit symbols; live row parity still operator-pending) |
| `cross-area-data-map-2026-06-04.md` OPS-86-15 table | **Was stale** — claimed DDL/emit absent post-P6 |
| `DATA_CONTRACT_REGISTRY.csv` | **Was thin** — 4 rows for 7 families; mirror row still said "DDL not minted" |
| `process_list` ENGAGEMENT-FACT automation column | **Wrong runbook** — cited `bi_integration_readiness_check.py` instead of engagement validators |
| Mirror upsert operator path | **Was `/tmp`** — not discoverable on Windows (`C:\tmp` unreliable) |

## External refinement (light)

| Source | Use |
|:---|:---|
| [Data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html) | Seven families = domain **data products**; global rules in DATA contracts, not one mega-migration per area |
| [DAMA-DMBOK maturity](https://atlan.com/dama-dmbok-framework/) | Contract-per-surface is L2 computational governance before L3 catalog export |
| OpenMetadata ODCS git-stored contracts (industry pattern, P2b research) | Each family should have ≥1 contract row or explicit forward-declaration — anti gap-theatre per posture §9 |

## Findings

| ID | Severity | Finding |
|:---|:---|:---|
| FAM-CQ-01 | **Blocker** | Operator upsert path hardcoded to `/tmp/ops8615-upsert.sql` — file not found on Windows |
| FAM-CQ-02 | **Major** | `cross-area-data-map` OPS-86-15 table contradicted P6 migration (still "No" DDL) |
| FAM-CQ-03 | **Major** | `DC-HOL-COMPLIANCE-MIRROR-001` notes claimed mirror DDL not minted (false post-P6) |
| FAM-CQ-04 | **Major** | Only 4/7 DATA-FAM families had contract rows — governed-claim bar §9 gap-theatre risk |
| FAM-CQ-05 | **Major** | ENGAGEMENT-FACT contract/process ignored P7 `canonical_engagement_code` reconciliation |
| FAM-CQ-06 | **Medium** | ENGAGEMENT-FACT process row paired wrong runbook (BI readiness vs engagement registry) |
| FAM-CQ-07 | **Minor** | UAT + verification docs cited `C:\tmp\` path |

## Remediation applied (2026-06-05)

| ID | Fix |
|:---|:---|
| FAM-CQ-01 | Default `--ops8615-gap-mirrors-only` output → `docs/wip/planning/93-.../artifacts/ops8615-mirror-upsert.sql`; `artifacts/README.md`; `.gitignore` for `*.sql` |
| FAM-CQ-02 | Refreshed OPS-86-15 table + status in `cross-area-data-map-2026-06-04.md` |
| FAM-CQ-03 | Updated `DC-HOL-COMPLIANCE-MIRROR-001` notes + decision id D-IH-93-F |
| FAM-CQ-04 | Added `DC-HOL-CANONICAL-CSV-SSOT-001`, `DC-HOL-TELEMETRY-OBS-001`, `DC-HOL-KM-TOPIC-001`, `DC-HOL-AIC-RUNTIME-001` |
| FAM-CQ-05 | Updated `DC-HOL-SUEZ-ENG-FACT-001` semantics for ENG-* codes + Websitz row |
| FAM-CQ-06 | `process_list` ENGAGEMENT-FACT automation → `validate_engagement_model_registry.py` + `validate_hlk.py` |
| FAM-CQ-07 | UAT, p6 verification, master-roadmap paths → repo-local artifacts path |

## Post-remediation verification

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only
py scripts/validate_data_contract_registry.py
py scripts/validate_hlk.py
py -m pytest tests/test_ops8615_mirror_emit.py tests/test_dataops_quality_check.py -q
```

## Residual follow-ups (not blockers)

| Item | Owner | Tracker |
|:---|:---|:---|
| Live mirror row parity (0 rows until SQL Editor) | Operator | `p6-supabase-verification-2026-06-04.md` |
| CONF registry still seed_v1_unrated for all 7 CAPs | Capability Curator | I82 quarterly review |
| 35 unmapped processes in cross-area map | CDO area batches | `cross-area-data-map` § P6 mint checklist |
| `engagement_registry_mirror` column for `canonical_engagement_code` | Forward DDL | P7 decision-log |

## Verdict

**Ready for commit** — content drift remediated; operator mirror SQL path is repo-discoverable.
