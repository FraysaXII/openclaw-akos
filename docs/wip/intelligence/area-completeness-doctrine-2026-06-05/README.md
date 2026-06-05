---
intellectual_kind: research_action_index
parent_initiative: INIT-OPENCLAW_AKOS-93
related_initiatives: [88, 86]
authored: 2026-06-05
status: active
language: en
---

# Research action — area-completeness doctrine (2026-06-05)

> **Named decision D-AREA-DEF:** before driving the remaining five O5-1 areas to closure,
> should Holistika amend the definition of "an area" and/or the 14-component completeness
> bar — and if so, how? Governed by `RESEARCH_ACTION_DISCIPLINE.md` (8-stage loop) +
> `akos-research-action.mdc` RULE 1 (mandatory source ledger).

## Folder index

| File | Stage | What it holds |
|:---|:---|:---|
| [`research-action-pack.md`](research-action-pack.md) | control | Named decision + 8-stage loop + prong plan |
| [`source-ledger.csv`](source-ledger.csv) | 1–2 ingest/rate | **117 sources** (55 internal + 62 external), 13-field canonical schema, validator PASS |
| [`baseline-state-2026-06-05.md`](baseline-state-2026-06-05.md) | 3 rank/topography | Matrix refresh + full-picture regression + per-area topography |
| [`prong-a-internal-doctrine.md`](prong-a-internal-doctrine.md) | 4 synthesize | How WE define area + completeness today |
| [`prong-b-external-maturity.md`](prong-b-external-maturity.md) | 4 synthesize | Industry maturity/governance models (DAMA/DCAM/CMMI/COBIT/ISO) |
| [`prong-c-domain-boundaries.md`](prong-c-domain-boundaries.md) | 4 synthesize | What an area *is* (DDD/Team Topologies/Data Mesh/Wardley/Golden Paths) |
| [`prong-d-completeness-value.md`](prong-d-completeness-value.md) | 4 synthesize | What "complete"/"value-ranked" means (DQ dims/DoD-AC/WSJF/GQM/OKR) |
| [`master-synthesis.md`](master-synthesis.md) | 4–5 synthesize/govern | **Definitional regression + ranked option set for D-AREA-DEF** |

## Source ledger at a glance

- **117 sources**; 8 topic clusters; `control_confidence` = {Safe: 61, Euclid: 56}.
- **55 internal** (`SRC-AREA-INT-*`, CORPINT) — every canonical/validator/decision bearing on area + completeness.
- **62 external** (`SRC-AREA-EXT-*`, OSINT) — DAMA-DMBOK, DCAM, CMMI, COBIT, ISO/IEC 38500,
  DDD bounded contexts, Team Topologies, Data Mesh, Wardley, Golden Paths, DoD/DoR/AC, WSJF,
  GQM, OKR, maturity-model design theory (Becker/Pöppelbuß/Mettler).
- Validate: `py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/area-completeness-doctrine-2026-06-05/source-ledger.csv`

## Headline result (full detail in master-synthesis §1–3)

The 14-component bar is a sound **artifact-presence Definition-of-Done** with a rare strength
(**determinism / intersubjective verifiability**), but the field says a governance-maturity
model should also be **leveled, criticality-weighted, boundary-defined, per-area-tiered, and
outcome-aware** — five axes the current flat bar collapses. Recommendation: **1B + 2A + 3B +
4B** (weight + boundary criterion + DoD/AC + tiered threshold), keeping determinism and not
invalidating the Data/Finance closures.

## Status

Stages 1–4 complete; **Stage 5 (govern) is the operator AskQuestion gate** (Step 7 of the
instruction). Stage 6 (implement — amend `AREA_GOVERNANCE_DISCIPLINE.md` /
`hlk_area_completeness.py`) is **gated** on the operator's pick. Then options A (Finance F4 →
I88) and D (5-area sweep) proceed against the upgraded bar.
