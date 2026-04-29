# Initiative 21 — Evidence matrix

Tracks the **provenance** of each open question / action / register row to its source artifact. Updated as transcripts are mined and CSVs are populated.

## Question-source mapping (seed)

| Q-id (target) | Discipline | Source | Path |
|:--------------|:-----------|:-------|:-----|
| Q-LEG-001 | Legal | §7.3 #1 | [`founder-incorporation-section7-structured-table.md`](../04-holistika-company-formation/reports/founder-incorporation-section7-structured-table.md) |
| Q-LEG-002 | Legal | §7.3 #2 | same |
| Q-LEG-003 | Legal | §7.3 #3 | same |
| Q-LEG-004 | Legal | §7.3 #4 | same |
| Q-LEG-005 | Legal | §7.3 #5 | same |
| Q-LEG-006 | Legal | §7.3 #6 | same |
| Q-LEG-007 | Legal | §7.3 #7 | same |
| Q-LEG-008 | Legal | §7.3 #8 | same |
| Q-LEG-009 | Legal | §7.3 #9 | same |
| Q-LEG-010 | Legal | 2026-08-04 ENISA kick-off (Part 1) | (post-redaction) `delete-legal-transcripts/<redacted>` |
| Q-LEG-011 | Legal | same | same |
| Q-LEG-012 | Legal | same | same |
| Q-FIS-001 | Fiscal | 2026-04-06 Fiscal pre-kick-off | (post-redaction) same folder |
| Q-FIS-002 | Fiscal | 2026-04-02 Alcance pre-kick-off | (post-redaction) same folder |
| Q-FIS-003 | Fiscal | 2026-08-04 ENISA kick-off (Part 2) | (post-redaction) same folder |

## GOI/POI seed mapping (target population in P1)

| Target ref_id | Class | Lens | Sensitivity | Source |
|:--------------|:------|:-----|:------------|:-------|
| `GOI-ADV-ENTITY-2026` | external_adviser | entity_readiness | internal | PMO hub stakeholder index |
| `GOI-BNK-INC-2026` | banking_channel | incorporation | confidential | PMO hub stakeholder index |
| `POI-BNK-DESK-LEAD-2026` | banking_channel | incorporation | confidential | 2026-08-04 ENISA kick-off (Part 1) |
| `POI-LEG-ENISA-LEAD-2026` | external_adviser | entity_readiness | internal | 2026-08-04 ENISA kick-off |
| `POI-LEG-FISCAL-LEAD-2026` | external_adviser | fiscal_readiness | internal | 2026-04-06 Fiscal pre-kick-off |

## Filed instruments seed (target population in P5)

| Target instrument_id | Type | Status | Source / link |
|:---------------------|:-----|:-------|:--------------|
| `INST-LEG-ESCRITURA-DRAFT-2026` | escritura de constitución | draft | Drive (off-repo) |

## Verification artifacts (target P9)

| Phase | Evidence target |
|:-----:|:----------------|
| P1 | `reports/p1-validate-goipoi.txt` (validator output) |
| P2 | `reports/p2-redaction-diff.md` (which files redacted, what `POI-*`/`GOI-*` ids substituted) |
| P3 | `reports/p3-advopps-plane.md` (cursor rule, disciplines CSV, plane SOP) |
| P4 | `reports/p4-questions-csv-migration.md` (Q-001..Q-012 → Q-LEG-* + Q-FIS-* mapping) |
| P5 | `reports/p5-filed-instruments-csv.md` |
| P6 | `reports/p6-km-manifest-validate.txt` |
| P7 | `reports/p7-export-smoke.md` (sample export markdown) |
| P9 | `reports/uat-adviser-handoff-<YYYYMMDD>.md` |
