---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P1
phase_name: Engagement folders + GOI/POI rows
recorded_at: 2026-05-10
---

# P1 — Engagement folders + GOI/POI self-checkpoint

## Folders created

* `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/` (with `extracts/`, `checkpoints/` subfolders + `README.md`).
* `docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/` (with `README.md`).

## GOI/POI rows appended (4)

| ref_id | entity_kind | class | distance_band | bridge_via |
|:---|:---|:---|:---|:---|
| `GOI-PRT-EFA-2026` | organisation | partner | N1 | — |
| `POI-PRT-EFA-LEAD-2026` | person | partner | N1 | — |
| `GOI-CUS-SUEZ-2026` | organisation | client_org | N2 | `GOI-PRT-EFA-2026` |
| `POI-CUS-SUEZ-LEAD-2026` | person | client_org | N2 | `POI-PRT-EFA-LEAD-2026` |

* Real entity names + identity mappings kept off-repo per redaction discipline.
* Class abbreviations follow existing register convention (`PRT` = partner, `CUS` = customer; matches `ADV` = adviser, `BNK` = banking_channel in the seed rows).

## Pointer placeholder

`docs/wip/planning/_candidates/customer-engagements-2026.md` — one-page pointer listing in-flight customer engagements. Promotes to a chartered initiative only when ≥ 2 engagements are simultaneously in flight.

## Verification

```
py scripts/validate_goipoi_register.py
==> Rows validated: 10
==> PASS
```

## Next

P2 — Internal counterparty brief + elicitation plan + source grading.
