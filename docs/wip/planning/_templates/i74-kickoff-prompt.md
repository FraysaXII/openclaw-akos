---
language: en
status: dormant
authored: 2026-05-13
last_review: 2026-05-13
target_initiative: I74 (candidate, dormant by design)
target_phase: TRIGGER-2 watch + (later) Discovery + Plan-Author + P0 charter
classification: fact
ssot: false
---

# I74 kickoff — TRIGGER-2 watch + (later) Discovery (Brand-tooling productization)

> **DO NOT RUN this prompt today.** I74 is dormant by design. The trigger gate is **TRIGGER-2**: ≥2 external orgs request AKOS doctrine consumption without source-fork. **Today: 0 such requests.** Productizing speculatively before the trigger fires is the explicitly-flagged Critical risk in the candidate's risk register.

## Trigger watch (run quarterly; ~5 minutes)

Check these signals:

1. **Inbound requests log** (operator-maintained, e.g. CRM / inbox folder / `docs/wip/intelligence/external-interest/`). Is there an entry from an org (not Holistika, not its sister-businesses) asking how to consume the brand discipline / render pipeline / validators?
2. **Cited-by signal**: any external talk, blog, or paper citing `BRAND_COPYWRITING_DISCIPLINE.md`, `BRAND_GANTT_DISCIPLINE.md`, `BRAND_MULTILINGUAL_CONTRACT.md`, or the public render artifacts (SUEZ deck, Asesoría)?
3. **Recruiter / advisor signal**: is anyone pitching Holistika that they want to license the methodology?

If **≥2 signals from distinct orgs** within a 6-month rolling window, **TRIGGER-2 has fired**. Open the kickoff prompt below.

## Pre-trigger readiness checklist (do this NOW so you're ready when the trigger fires)

- [ ] I70 closed — **MET** 2026-05-13.
- [ ] I71 closed (validator packs A1–A4 are the source for `@holistika/akos-brand`) — pending.
- [ ] I72 closed (engagement-template patterns are part of the library scope) — pending.
- [ ] I73 closed (People Ops mature; not strict dependency but signals operator capacity) — pending.
- [ ] HLK Tech Lab capacity available (per `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16.3 transition trigger).
- [ ] I76 closed — `D-IH-76-A` AICs ratification is load-bearing for Strand C (`@holistika/madeira-agent`).
- [ ] `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` reviewed and license posture confirmed.

## Trigger-fired kickoff prompt (paste only when TRIGGER-2 has fired)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat — but ONLY when TRIGGER-2 has fired. Otherwise the agent will rightly refuse to proceed.**

## --- BEGIN PROMPT ---

```
Goal: Drive INIT-OPENCLAW_AKOS-74 (Brand-tooling productization) from "candidate, dormant" to
"active P0 charter shipped on main", in the same inline-AskQuestion style as the I70 transcript.

CRITICAL — PLAN SCOPE (binding; non-negotiable):
The Cursor plan you mint MUST cover the ENTIRE I74 INITIATIVE (P0 through P6, all 4 strands A/B/C/D)
in ONE file at .cursor/plans/i74-brand-tooling-productization_<8hex>.plan.md. The reference shape
is the I70 plan at .cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md — ONE
strategic plan covering 17 phases, drilled-down through 5 regression rounds. That is the SOTA
bar. DO NOT mint phase-scoped or strand-scoped files. Filename has NO phase or strand prefix.
Regression rounds (Round 1 / Round 2 / ...) drill into depth ON THE SAME FILE.

PRECONDITION VERIFICATION (run BEFORE any other action; STOP if any FAIL):
- Confirm TRIGGER-2 evidence: list at least 2 external-org requests with org name + date + ask.
  These must live in docs/wip/intelligence/external-interest/ or equivalent.
- Confirm I70 + I71 + I72 + I76 closed (INITIATIVE_REGISTRY.csv status = closed for each).
- Confirm BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md is current (last_review within 90 days).
- If any FAIL: write a 5-line blocker report at
  docs/wip/planning/_candidates/i74-trigger-blocker-<date>.md and STOP.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/_candidates/i74-brand-tooling-productization.md (lift)
- docs/wip/planning/_templates/initiative-planning-prompts.md (generic prompt trio)
- docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md
- docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
  (section 8 AKOS-complete-enough trigger gates MADEIRA productization)
- docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  (sections 15.2 + 16.3 — TRIGGER-2 + transition triggers)
- docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/STATUS.md
  (section 3 TRIGGER-2 details + Scenario B activation)

External research targets (cite at least 4 with URLs):
- Open-source library distribution channels (PyPI vs private indexes vs GitHub Packages).
- Methodology-as-a-product licensing precedents (e.g. Atlassian's Team Playbook, IDEO's Design
  Kit, BMG's Business Model Canvas open-source posture, Lean Startup canon).
- "Trademark + open methodology" splits — how do Atlassian / IDEO / BMG keep the brand while
  releasing the discipline?
- Multi-agent productization (for Strand C `@holistika/madeira-agent` cross-link to I76).
- Optional: "AI agent libraries" (LangGraph, AutoGen, CrewAI as comparables for `@holistika/madeira-agent`).

Step 1 — Discovery (per generic Prompt 1):
- Surface every architectural conundrum (C-74-1 through C-74-5).
- C-74-1 (library scope: validators-only vs validators+templates+SOPs) is pre-charter architectural.
- C-74-3 (MADEIRA gate criteria) MUST cross-link to I76 closure status; if I76 hasn't closed, the
  agent flags Strand C (P4) as conditional.
- One AskQuestion batch: confirm PROMOTE next-step.

Step 2 — Plan-Author (per generic Prompt 2):
- Author .cursor/plans/i74-brand-tooling-productization_<8hex>.plan.md
- Author docs/wip/planning/74-brand-tooling-productization/master-roadmap.md
- Author docs/wip/planning/74-brand-tooling-productization/reports/p0-charter-<date>.md
- git mv the candidate.

Step 3 — Mint registry rows (one atomic commit):
- DECISION_REGISTER.csv: D-IH-74-A (license + brand-mark separation), D-IH-74-B (akos-brand library),
  D-IH-74-C (akos-render package), D-IH-74-D (madeira-agent gated on I76 + AKOS-complete-enough),
  plus charter row.
- INITIATIVE_REGISTRY.csv: row INIT-OPENCLAW_AKOS-74 with status=active.
- OPS_REGISTER.csv: rows OPS-74-1 through OPS-74-4, status=open.

Step 4 — Cross-link surfaces:
- WORKSPACE_BLUEPRINT_HOLISTIKA.md sections 15.2 + 16.3: link the master-roadmap.
- HLK_ERP_ARCHITECTURE.md section 8: cross-link the AKOS-complete-enough trigger evidence.
- MADEIRA-AKOS/STATUS.md section 3: update Scenario B status from "deferred" to "active".
- CHANGELOG.md [Unreleased] / Added: charter entry.

Verification (same suite as I72/I73 kickoff):
- validate_decision_register, validate_initiative_registry, validate_ops_register, validate_hlk,
  validate_master_roadmap_frontmatter, validate_hlk_vault_links, render_operator_inbox.

Commit message:
"i74 p0 inline charter + registries + workspace cross-links (brand tooling productization;
TRIGGER-2 fired YYYY-MM-DD)"

OPERATOR NOTES (paste TRIGGER-2 evidence; paste any direct asks from external orgs):
[paste-here]
```

## --- END PROMPT ---

## Why this template is shaped differently

The other initiatives' templates assume "go now". I74's template assumes "wait" until the trigger fires, with the precondition-verification block as the agent's first action. This protects against the **Critical risk** in the candidate: speculative productization before TRIGGER-2 evidence wastes effort and may prejudice the architecture.

If TRIGGER-2 never fires, this template is a no-op forever. That's the desired posture.
