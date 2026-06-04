---
intellectual_kind: propagation_record
initiative: I93
phase: P8
authored: 2026-06-05
sop: SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001
---

# P8 — Cross-area breakthrough propagation record

## Trigger

I93 P0 minted `pattern_area_buildout`; P5c minted `pattern_sop_method_library`.
Both rows carry `last_review: 2026-06-04` in `PEOPLE_DESIGN_PATTERN_REGISTRY.csv`.

## Runbook execution

```text
py scripts/peopl_cross_area_breakthrough_announce.py --since 2026-06-04 -v
  INFO | registry rows in window: 2 of 31
  OVERALL PASS: 9 areas processed; 9 files written
```

## Digest outputs (SSOT path)

Per-area digests under I79 breakthrough folder (cross-initiative SSOT per SOP):

| Area token | Digest path |
|:---|:---|
| compliance | `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/breakthroughs/2026-06/compliance.md` |
| marketing | `.../marketing.md` |
| techlab | `.../techlab.md` |
| finance | `.../finance.md` |
| operations | `.../operations.md` |
| research | `.../research.md` |
| people | `.../people.md` |
| ethics | `.../ethics.md` |
| legal | `.../legal.md` |

## Patterns announced

1. **`pattern_area_buildout`** — 14-component bar; DATA is worked example (`DATA_AREA_CHARTER.md`).
2. **`pattern_sop_method_library`** — SOP-META §4.7 method variants (P5c).

## Consuming-area next action

Each area role-owner records **adopt-now / adopt-later / decline** in the digest
"Decision" line per SOP §2 step 3. I93 does not author consuming-area charters.
