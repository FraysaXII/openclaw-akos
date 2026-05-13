---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-13
target_initiative: I72 (candidate)
target_phase: Discovery → Plan-Author → P0 charter
classification: fact
ssot: false
---

# I72 kickoff — Discovery + Plan-Author + P0 charter (Marketing Area Governance)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat (Plan mode preferred).**
>
> **Hold gate**: do not run this prompt until I71 P2 has shipped (Pack A4 unblocks RevOps-activation Strand C). If you run it earlier, the agent will surface a hard dependency and pause.

## --- BEGIN PROMPT ---

```
Goal: Drive INIT-OPENCLAW_AKOS-72 (Marketing Area Governance) from "candidate" to "active P0 charter
shipped on main", in the same inline-AskQuestion style as the I70 plan-creation transcript.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/_candidates/i72-marketing-area-governance.md (candidate scaffold; lift)
- docs/wip/planning/_templates/initiative-planning-prompts.md (the generic Discovery + Plan-Author
  + Pre-flight prompt trio; this kickoff is the I72-specific composition)

Internal canonicals to read:
- docs/references/hlk/v3.0/Admin/O5-1/Marketing/canonicals/MARKETING_AREA_M3_REDESIGN.md
- docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  (sections 11-18; especially section 16.3 PMO -> RevOps transition trigger)
- docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
  (section 4 panel slots; reserve op_revops_engagement_templates)
- docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/checkpoints/
  p13.0b-previous-project-pattern-extraction.md (the 6 patterns informing template-promotion machine)
- DECISION_REGISTER.csv rows: D-IH-70-T (M3 redesign), D-IH-70-R (SMO vs Account Management),
  D-IH-70-X (Storytelling-authors / Resonance-consumes), D-IH-70-Z (sub_area + status), D-IH-70-AB
  (SMO baseline + Account Manager).

External research targets (cite at least 3 with URLs in the discovery report):
- "RevOps maturity model" — best-in-class definitions (Forrester, SiriusDecisions, MOPSpalooza).
- "Engagement template" patterns — engagement-as-product literature; consulting-firm template libraries.
- Account-management vs customer-success boundary debates (industry consensus).
- M3 sub-area equivalents in agency/consulting world (storytelling vs PR vs thought-leadership).

Step 1 — Discovery (per generic Prompt 1):
- Surface every architectural conundrum from the candidate (C-72-1 through C-72-5) plus any new ones
  you find in research.
- Particularly important: ratify C-72-1 (template-promotion threshold: 3 vs 5 vs 7 engagements) at
  PLANNING TIME, not execution. This is architectural; the agent must NOT defer.
- Produce / update docs/wip/planning/_candidates/i72-marketing-area-governance.md with a
  "Discovery findings" section before promoting.
- One AskQuestion batch: confirm PROMOTE next-step.

Step 2 — Plan-Author (per generic Prompt 2):
- Author .cursor/plans/i72-marketing-area-governance_<8hex>.plan.md
- Author docs/wip/planning/72-marketing-area-governance/master-roadmap.md (workspace mirror).
- Author docs/wip/planning/72-marketing-area-governance/reports/p0-charter-<date>.md.
- git mv docs/wip/planning/_candidates/i72-marketing-area-governance.md
        docs/wip/planning/72-marketing-area-governance/promoted-candidate-<date>.md

Step 3 — Mint registry rows (one atomic commit; per generic Prompt 2):
- DECISION_REGISTER.csv: D-IH-72-A (sub-area charter authoring), D-IH-72-B (template promotion
  machine), D-IH-72-C (RevOps activation), D-IH-72-D (any conundrum-ratified architectural row,
  e.g. C-72-1 threshold), plus the charter row at the end (use D-IH-72 charter convention).
- INITIATIVE_REGISTRY.csv: row INIT-OPENCLAW_AKOS-72 with status=active,
  inception_decision_id = D-IH-72 charter row, master_roadmap_path =
  docs/wip/planning/72-marketing-area-governance/.
- OPS_REGISTER.csv: rows OPS-72-1 (P2 ENGAGEMENT_TEMPLATE_REGISTRY), OPS-72-2 (P3 promotion SOP),
  OPS-72-3 (P4 RevOps activation), all status=open.

Step 4 — Cross-link surfaces:
- WORKSPACE_BLUEPRINT_HOLISTIKA.md section 16.3: link the PMO -> RevOps transition trigger to the
  new master-roadmap.
- HLK_ERP_ARCHITECTURE.md section 4: reserve op_revops_engagement_templates panel slot.
- CHANGELOG.md [Unreleased] / Added: charter entry mirroring the I71 P0 charter format.

Verification before commit (run all; STOP at first FAIL):
- py scripts/validate_decision_register.py
- py scripts/validate_initiative_registry.py
- py scripts/validate_ops_register.py
- py scripts/validate_hlk.py
- py scripts/validate_master_roadmap_frontmatter.py
- py scripts/validate_hlk_vault_links.py
- py scripts/render_operator_inbox.py (refresh inbox after new OPS rows)

Commit message:
"i72 p0 inline charter + registries + workspace cross-links (marketing area governance)"
Push to origin/main only after operator inline-ratifies (one final AskQuestion: "commit + push?").

DECISION DISCIPLINE (binding):
- NEVER use "OPERATOR PAUSE POINT". Always use "(inline-ratify gate at section X.Y)".
- Architectural decisions ratified at planning time, not deferred.
- For execution-time gates, pre-allocate the gate location in the plan.

OPERATOR NOTES (optional context; paste your latest thoughts here):
[paste-here]
```

## --- END PROMPT ---

## Initiative-specific guidance (read before launching)

- The candidate at `docs/wip/planning/_candidates/i72-marketing-area-governance.md` is already at depth-bar; the agent's job is to **research outside (best practices)**, **ratify the open conundrums** (especially C-72-1 threshold and C-72-2 Account-Management vs Customer-Success boundary), and **mint the P0 tranche**.
- Hard dependency: I71 P2 (Pack A4 render ownership) must ship before P4 RevOps activation can land. The agent should pre-allocate this in the master-roadmap's "Dependencies" section.
- The 6 patterns from the previous-project annex (P2.4) are **load-bearing inputs** to Strand B (engagement-template promotion machine) — the agent must read them, not just cite them.

## After P0 ships

P1 (4 sub-area charters + Account Management charter) — author one prompt per sub-area; same structure as the I71 per-phase prompt; lift SCOPE from the master-roadmap.
