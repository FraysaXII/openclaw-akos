---
name: research-radar-craft
description: Use when maintaining IntelligenceOps register freshness, running research_radar_sweep.py, or authoring per-target volatility_class / staleness_days / staleness_posture / next_verify_by before Research Action govern. Never hardcode a global cadence. Triggers on research radar, INTELLIGENCEOPS_REGISTER freshness, volatility_class, staleness_posture, research_radar_sweep, validate_research_radar, RESEARCH_RADAR_DISCIPLINE. Pairs with akos-research-radar.mdc.
---

# Research Radar Craft

16th Quality Fabric specialty (D-IH-86-FG). Radar surfaces **which**
IntelligenceOps (and optional substrate) targets are STALE or DUE before
govern — cadence is **per row**, not calendar folklore.

## Pre-flight

1. Read charter `docs/wip/intelligence/research-radar-2026-05-29/charter-2026-05-29.md`.
2. Set `volatility_class` then `staleness_days` (or leave empty to use class default from `VOLATILITY_DEFAULT_STALENESS_DAYS`).
3. Set `staleness_posture` (`block_govern` vs `cite_and_flag`).
4. Compute `next_verify_by` from `last_review_at` + resolved days.
5. Run `py scripts/research_radar_sweep.py` before Research Action govern.

## Anti-patterns

- Uniform 90-day staleness on every row without target judgment.
- Writing "quarterly sweep" in prose instead of per-row `next_verify_by`.
- Skipping register extension when only authoring doctrine.
