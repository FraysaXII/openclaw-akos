---
candidate_id: I72
title: Marketing Area Governance (renamed from I67 RevOps Discovery per Conundrum 12)
status: candidate
authored: 2026-05-12
parent_initiative: 70 (closing scaffold)
priority: 2
supersedes: I67 (RevOps Discovery)
---

# I72 candidate — Marketing Area Governance

## 1. Scope

Operationalizes the M3 Marketing redesign (per `MARKETING_AREA_M3_REDESIGN.md`; D-IH-70-T):
- Per-sub-area charters (Reach / Resonance / Storytelling / Experimentation; Brand already authored at I70 P5).
- Account Management charter at `Marketing/Resonance/Account Management/canonicals/`.
- Engagement-template promotion machine (RevOps owner; consumes the 6 patterns from previous-project annex per I70 P2.4).
- ENGAGEMENT_REGISTRY.csv full build (deferred from I70 P8 §8.1-§8.3 alongside P4.5 wave 2/3 CSV migration).
- M3 sub-area Marketing CSV updates (~10 baseline_organisation.csv role rows + ~10 process_list.csv ops processes).
- Acquisition-driven engagement template promotion: when 3+ engagements consume same template pattern, RevOps takes over template-iteration responsibility (per WORKSPACE_BLUEPRINT_HOLISTIKA §16.3 PMO -> RevOps transition trigger).

## 2. Why priority 2 (after I71)

- M3 sub-area charter authoring is author-only; can proceed in parallel with P4.5 wave 2/3.
- ENGAGEMENT_REGISTRY full build coordinates with P4.5 wave 2/3 CSV migration (atomic with compliance migration).
- RevOps owner activation depends on validator rule packs from I71 (validate_render_pipeline_owner_coverage.py).

## 3. Spin-out trigger conditions

- I70 closing UAT + v3.1 release flag.
- I71 P0 charter shipped (validator rule packs reserved).
- Founder approval to activate RevOps owner.

## 4. Cross-references

- I70 P8 commit `8f2559b` (MARKETING_AREA_M3_REDESIGN parent).
- I67 RevOps Discovery (superseded; rename per Conundrum 12 + D-IH-70-T).
- I70 P2.4 previous-project pattern annex (6 patterns inform engagement-template promotion machine).
- WORKSPACE_BLUEPRINT_HOLISTIKA §16.3 PMO -> RevOps transition trigger.
- D-IH-70-X (P2.5 sub-decision: Storytelling-authors / Resonance-consumes boundary).
- D-IH-70-R (P3 ratification: SMO vs Account Management distinction).
