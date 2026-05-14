---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-13
target_initiative: I73 (candidate)
target_phase: Discovery → Plan-Author → P0 charter
classification: fact
ssot: false
---

# I73 kickoff — Discovery + Plan-Author + P0 charter (People Operations + Learning curriculum)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat.**
>
> **Hold gate**: do not run until I72 P0 has shipped + the founder has committed to either hiring a People Operations Lead OR formally taking the role + the founder has committed to a Holistik Researcher cohort hiring window. If you run earlier, the agent will surface hard dependencies.

## --- BEGIN PROMPT ---

```
Goal: Drive INIT-OPENCLAW_AKOS-73 (People Operations + Learning curriculum) from "candidate" to
"active P0 charter shipped on main", in the same inline-AskQuestion style as the I70 transcript.

CRITICAL — PLAN SCOPE (binding; non-negotiable):
The Cursor plan you mint MUST cover the ENTIRE I73 INITIATIVE (P0 through P6, all 4 strands A/B/C/D)
in ONE file at .cursor/plans/i73-people-operations-and-learning-curriculum_<8hex>.plan.md. The
reference shape is the I70 plan at .cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md
— ONE strategic plan covering 17 phases, drilled-down through 5 regression rounds. That is the
SOTA bar. DO NOT mint phase-scoped files (e.g. i73_p1_*.plan.md) or strand-scoped files. Filename
has NO phase or strand prefix. Regression rounds (Round 1 / Round 2 / ...) drill into depth ON
THE SAME FILE.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/_candidates/i73-people-operations-and-learning-curriculum.md (lift)
- docs/wip/planning/_templates/initiative-planning-prompts.md (generic prompt trio)

Internal canonicals to read:
- docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_AREA_RESTRUCTURE.md
- docs/references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md
  (especially section 5 quarterly review cadence; load-bearing for Strand B Ethics+Learning
  inseparability operationalization)
- docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md (anchor for
  curriculum-versioning conundrum C-73-2)
- DECISION_REGISTER.csv rows: D-IH-70-Q (People area restructure), D-IH-70-AA (Talent monolith
  hard-removal + 4 sub-roles), D-IH-70-M (Holistik Researcher = role row + cohort tag).
- baseline_organisation.csv rows for People area (verify the 4 sub-roles landed at I70 P8.3).

External research targets (cite at least 3 with URLs):
- "Learning & Development curriculum design for early-stage companies" — best practices on
  pillar-based vs role-based curricula.
- "AI ethics training programs" — academic + industry templates (e.g. Stanford HAI, Anthropic
  policy team, Mozilla's Responsible Computing Challenge).
- "People Operations playbooks" — modern startup HR (e.g. Gitlab Handbook, Buffer Open Salaries,
  Stripe Atlas, Sequoia's People Operations Playbook).
- Optional: "researcher cohort onboarding" (e.g. lab onboarding rituals; PhD program orientation).

Step 1 — Discovery (per generic Prompt 1):
- Surface every architectural conundrum from the candidate (C-73-1 through C-73-5).
- C-73-1 (cohort size for first Holistik Researcher cohort) is PLANNING-TIME architectural, not
  execution-time. The founder must ratify pre-charter.
- C-73-2 (curriculum-versioning vs methodology-versioning anchor cadence) is also pre-charter;
  cross-link to I71 D-IH-71-E review-stamp dimension if landed.
- Produce / update i73 candidate with "Discovery findings" section before promoting.
- One AskQuestion batch: confirm PROMOTE next-step.

Step 2 — Plan-Author (per generic Prompt 2):
- Author .cursor/plans/i73-people-operations-and-learning-curriculum_<8hex>.plan.md
- Author docs/wip/planning/73-people-operations-and-learning-curriculum/master-roadmap.md
- Author docs/wip/planning/73-people-operations-and-learning-curriculum/reports/p0-charter-<date>.md
- git mv the candidate to promoted-candidate-<date>.md

Step 3 — Mint registry rows (one atomic commit):
- DECISION_REGISTER.csv: D-IH-73-A (Learning charter + curriculum), D-IH-73-B (Ethics+Learning
  quarterly co-review SOP), D-IH-73-C (4 People Ops SOPs), D-IH-73-D (Compliance/Ethics boundary),
  D-IH-73-E (first cohort UAT placeholder), plus charter row.
- INITIATIVE_REGISTRY.csv: row INIT-OPENCLAW_AKOS-73 with status=active.
- OPS_REGISTER.csv: rows OPS-73-1 through OPS-73-4, status=open.

Step 4 — Cross-link surfaces:
- WORKSPACE_BLUEPRINT_HOLISTIKA.md: cross-link Learning curriculum + Ethics+Learning quarterly review.
- BRAND_VOICE_FOUNDATION.md: refresh slot to add "we become unethical when we unlearn" as a
  brand differentiator (Strand B authoring; not yet at P0).
- CHANGELOG.md [Unreleased] / Added: charter entry.

Verification before commit (run all; STOP at first FAIL):
- py scripts/validate_decision_register.py
- py scripts/validate_initiative_registry.py
- py scripts/validate_ops_register.py
- py scripts/validate_hlk.py
- py scripts/validate_master_roadmap_frontmatter.py
- py scripts/validate_hlk_vault_links.py
- py scripts/render_operator_inbox.py

Commit message:
"i73 p0 inline charter + registries + workspace cross-links (people operations + learning)"
Push only after final AskQuestion ratifies.

DECISION DISCIPLINE (binding):
- C-73-1 cohort size: NEVER ship a Learning charter without the cohort size ratified. If the
  founder hasn't committed yet, STOP at discovery and write a stop-and-clarify report.
- C-73-3 Ethics-leads-vs-co-leads: pre-charter ratify (planning-time architectural).

OPERATOR NOTES (optional context; paste your latest thoughts here):
[paste-here]
```

## --- END PROMPT ---

## Initiative-specific guidance

- **Cross-coordinate with I75 (Research area governance) at C-73-2 + C-73-4**: the KM Officer curriculum (I75 Strand B) and the Holistik Researcher curriculum (I73 Strand A) cross-reference each other. Best practice is to draft I73 P1 with explicit "cross-coordinate at I75 P4" hooks, even before I75 promotes.
- **The Ethics+Learning thesis** ("we become unethical when we unlearn") is a **brand differentiator**, not just an internal slogan. Strand B authoring lands its operational expression; brand-voice register integrates it (post-I71 Pack A1 ship).
- **People Ops vs FINOPS payroll boundary** (C-73-4) is genuine — the agent should cite `FINOPS_COUNTERPARTY_REGISTER` and decide cleanly: People Ops = process; FINOPS = ledger.

## After P0 ships

P1 (Learning charter + Holistik Researcher curriculum) is the heaviest phase; budget accordingly. Same prompt structure per phase.
