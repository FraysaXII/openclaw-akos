---
tranche_id: i93-p7-hygiene
tranche_class: canonical_csv_mint
initiative: INIT-OPENCLAW_AKOS-93
authored: 2026-06-04
ratifying_decisions:
  - D-IH-93-E
reversibility: medium
---

# P7 tranche charter — component + engagement + transcript hygiene

## Scope (D-IH-93-E all four)

1. Component matrix privacy columns populated (`scripts/i93_p7_hygiene_apply.py`)
2. Engagement registry `canonical_engagement_code` + Websitz Shopify row
3. GOI partner rows (Websitz, Rushly)
4. USE_CASE_ARCHIVE +5 POC realisations
5. Transcript backfill tracker (27 rows)

## Verification

```powershell
py scripts/validate_component_service_matrix.py
py scripts/validate_use_case_archive.py
py scripts/validate_hlk.py
```
