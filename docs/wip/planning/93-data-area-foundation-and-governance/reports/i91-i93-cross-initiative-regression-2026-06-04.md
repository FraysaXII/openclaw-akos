---
intellectual_kind: regression_report
initiative: I93
feeds_phase: P6
authored: 2026-06-04
linked_initiatives:
  - INIT-OPENCLAW_AKOS-90
  - INIT-OPENCLAW_AKOS-91
  - INIT-OPENCLAW_AKOS-93
---

# I91 ↔ I93 cross-initiative regression (2026-06-04)

Operator ratification: **cross-initiative regression** before P6 mint (not passive COORD-1).

## I91 state (read-only sweep)

| Item | Finding | P6 action |
|:---|:---|:---|
| I91 roadmap | P0 charter only; P1 blocked on `NEO4J_*` | No Neo4j mint in P6 |
| Store-coverage matrix | Not yet v1 in repo | I93 publishes cross-area map; I91 P2 should **cite** it |
| DATA-FAM P1 (I90) | Was "next" for 43 cadence CAP rows | **Folded into I93 P6** per D-IH-93-G — seven umbrellas first |
| Graph projection | I07 closed; reuse `sync_hlk_neo4j.py` | KM-TOPIC family probes reference graph path; no duplicate CAP |

## Scope split (binding for cluster)

| Owner | Owns | Must not |
|:---|:---|:---|
| **I93 P6** | 7 `CAP-HOL-DATA-FAM-*-001` + CONF + process umbrellas; OPS-86-15 mirror DDL+emit; `--data-fam` probes | Neo4j sync smoke; store-coverage matrix v1 |
| **I91** | Store inventory; coverage matrix v1; graph regression | Re-mint family CAP rows |

## Lessons written back

1. **I91 master-roadmap** — add P6 coordination note (this regression + I93 cross-area map SSOT).
2. **I90 data-area-capability-coverage** — P6 executes family row from table § "Proposed DATA capability taxonomy".
3. **OPS-86-15** — MIRROR-2 closes five CSV gap in P6 (was forward-chartered to mixed owner).

## Verdict

**Proceed with P6-A mint** — no double-mint risk if I91 limits P1 to cadence backfill without family CAP IDs.
