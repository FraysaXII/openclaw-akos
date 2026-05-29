---
title: Research Radar Discipline
language: en
status: charter
canonical: true
role_owner: Research Director + KM Officer
classification: way_of_working
intellectual_kind: discipline_charter
access_level: 4
authored: 2026-05-29
last_review: 2026-05-29
last_review_by: Founder
last_review_decision_id: D-IH-86-FG
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-FG
  - D-IH-86-FH
  - D-IH-86-FI
linked_runbooks:
  - scripts/research_radar_sweep.py
  - scripts/validate_research_radar.py
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv
---

# Research Radar Discipline

## 1. Purpose

Research Radar is the **time dimension** the research apparatus was missing: a register-driven discipline that tracks **freshness** of volatile claims, intelligence targets, and substrate audit stamps — then surfaces a **prioritized re-verify queue** into Research Action **govern** stage 5.

Cadence and decay windows live **as data per row** on `INTELLIGENCEOPS_REGISTER.csv` and per-substrate profiles in `akos/hlk_research_radar.SUBSTRATE_VOLATILITY_PROFILES`. **No global schedule constant** (for example a hardcoded "every 90 days" or "quarterly") may appear in doctrine, runbook, or validator code.

## 2. Relationship to Research Action

| Discipline | Owns |
|:---|:---|
| **Research Action** | ingest → rate → rank → synthesize → **govern** → implement → test → iterate |
| **Research Radar** | freshness registers + sweep + stale-target queue feeding **govern** |

Radar is **not** a second ingest doctrine, not the substrate-audit SOP cadence, and not the MADEIRA GTM "research radar" product theme.

## 3. Register contract (INTELLIGENCEOPS extension)

Per `D-IH-86-FH`, four columns extend `INTELLIGENCEOPS_REGISTER.csv`:

| Column | Role |
|:---|:---|
| `volatility_class` | `fast` / `medium` / `slow` / `static` — default decay hint only |
| `staleness_days` | **Per-row integer** decay window for this target |
| `staleness_posture` | `cite_and_flag` / `block_govern` / `none` at govern stage when stale |
| `next_verify_by` | Date alarm; sweep surfaces when `today > next_verify_by` |

`volatility_class` supplies register defaults (`fast`≈30d, `medium`≈90d, `slow`≈365d, `static`=none) **overridable per row** via `staleness_days`.

## 4. Substrate subsume (D-IH-86-FI)

Substrate landscape freshness is swept via `SUBSTRATE_REGISTRY.last_audit_date` against `SUBSTRATE_VOLATILITY_PROFILES` (per `env_tech_dtp_substrate_landscape_mtnce_001` process row minted in Wave R+5 C1). This subsumes the missing process row gap documented in plan §0 without inventing a separate global audit calendar.

## 5. Operating loop

1. **Register** — maintain IntelligenceOps rows + substrate profiles with per-target `staleness_days`.
2. **Sweep** — `py scripts/research_radar_sweep.py [--include-substrate]`.
3. **Queue** — stale/DUE targets become input to Research Action govern (ranked re-verify options).
4. **Ratify** — inline-ratify per `akos-inline-ratification.mdc` when `staleness_posture=block_govern`.
5. **Iterate** — bump `last_review_at` + `next_verify_by` on the register row after verification.

## 6. Verification

```powershell
py scripts/validate_research_radar.py --self-test
py scripts/research_radar_sweep.py
py scripts/validate_intelligenceops_register.py
py scripts/validate_hlk.py
```

INFO ramp at mint per `D-IH-86-FG`; FAIL promotion gates on 3+ sweeps with zero chassis findings + operator-ratified successor decision.

## 7. Cross-references

- Charter: `docs/wip/intelligence/research-radar-2026-05-29/charter-2026-05-29.md`
- SOP: `SOP-RESEARCH_RADAR_001.md`
- Parent fabric: `HOLISTIKA_QUALITY_FABRIC.md` §6 (16th specialty row)
