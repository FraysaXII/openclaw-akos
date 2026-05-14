---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-14
target_initiative: I72 (gated_operator → activation via this charter session)
target_phase: Discovery → Plan-Author → P0 charter (3 super-strands)
classification: fact
ssot: false
---

# I72 kickoff — Discovery + Plan-Author + P0 charter (Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat (Plan mode preferred).**
>
> **Scope correction (2026-05-14):** I72 was already minted at I70 closure with a **broader scope than the original `_candidates/i72-marketing-area-governance.md` candidate** — see `INITIATIVE_REGISTRY.csv` row 58: `INIT-OPENCLAW_AKOS-72` titled "Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion", folder `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/`, status `gated_operator`, `inception_decision_id: D-IH-70-AC`. The forward-charter from `D-IH-70-AC` (P8.5 GOI class hunt) explicitly hands three deferrals to I72: business-developer-collaborator persona row under existing partner class; competitor-intelligence-target IntelligenceOps register schema; regulator (ENISA) / media (PR Manager) / recruiter onboarding patterns. **Do not mint a fresh INIT row** — verify and activate the existing one. The candidate file covers only the Marketing super-strand; the agent must absorb its scope as **Strand A** of a broader I72 (Strand B = Persona Registry; Strand C = IntelligenceOps Register Expansion).
>
> **Hold gate (corrected; supersedes prior wording):**
>
> - I72 **P0–P3 can run NOW** (no I71 hard dependency for charter, sub-area charters, ENGAGEMENT_TEMPLATE_REGISTRY, promotion-machine SOP, persona-registry expansion, IntelligenceOps register expansion).
> - I72 **P4 (RevOps activation)** is **hard-gated on I71 P5 Pack A4** (`validate_render_ownership.py`) — not on I71 P2 (which ships Packs A2 + A3).
>
> The agent should pre-allocate this in the master-roadmap's "Dependencies" section. Earlier wording in this kickoff conflated "I71 P2" with "I71 P5"; the I72 candidate text was always correct that the dependency is on Pack A4 specifically.

## --- BEGIN PROMPT ---

```
Goal: Drive INIT-OPENCLAW_AKOS-72 (Marketing Area Governance + Persona Registry + IntelligenceOps
Register Expansion) from "gated_operator" to "active P0 charter shipped on main", in the same
inline-AskQuestion style as the I70 plan-creation transcript. Three super-strands per the existing
INIT row title, NOT just Marketing.

PRECONDITION VERIFICATION (run BEFORE any other action; STOP at first FAIL):
- Read INITIATIVE_REGISTRY.csv row 58 — confirm INIT-OPENCLAW_AKOS-72 exists with:
    folder_path = docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/
    status = gated_operator
    inception_decision_id = D-IH-70-AC
    title contains "Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion"
- Read DECISION_REGISTER.csv row D-IH-70-AC — confirm the four forward-charter deferrals
  (business-developer-collaborator persona, competitor-intelligence-target schema,
  regulator-relationship roadmap, media-counterparty-onboarding pattern).
- If preconditions FAIL, write a 5-line stop-and-clarify report at
  docs/wip/planning/_candidates/i72-precondition-blocker-<date>.md and HALT.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/_candidates/i72-marketing-area-governance.md (Strand A scope; lift)
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
  (SMO baseline + Account Manager), D-IH-70-AC (P8.5 GOI hunt forward-charter; SUPER-STRAND
  scope source for Strand B + Strand C).
- For Strand B (Persona Registry expansion):
    docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv
    docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv
    scripts/validate_persona_registry.py
    scripts/validate_persona_scenario_registry.py
- For Strand C (IntelligenceOps Register Expansion):
    docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv
    docs/references/hlk/v3.0/Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md
    docs/references/hlk/v3.0/Research/Intelligence/canonicals/ (any IntelligenceOps SOPs migrated
    from I70 P4.5 wave 3 per D-IH-70-W)
    DECISION_REGISTER.csv: D-IH-70-AD (stance dimension)

External research targets (cite at least 4 with URLs in the discovery report):
- "RevOps maturity model" — best-in-class definitions (Forrester, SiriusDecisions, MOPSpalooza).
- "Engagement template" patterns — engagement-as-product literature; consulting-firm template libraries.
- Account-management vs customer-success boundary debates (industry consensus).
- M3 sub-area equivalents in agency/consulting world (storytelling vs PR vs thought-leadership).
- Persona registry / ICP modelling — modern B2B SaaS frameworks (e.g. Bowery Capital ICP scoring,
  HubSpot persona builder, 6sense ICP intelligence).
- IntelligenceOps register / regulator + media engagement playbooks — government-affairs canon
  (e.g. Public Affairs Council, ENISA-specific stakeholder-engagement guidance) + PR-relations
  canon (e.g. PRCA Code; Cision media-relations playbooks).

Step 1 — Discovery (per generic Prompt 1):
- Surface every architectural conundrum from the candidate (C-72-1 through C-72-5) PLUS new ones
  for Strand B + Strand C (e.g. C-72-6 through C-72-10):
    C-72-6 — Persona registry vs scenario registry boundary: business-developer-collaborator goes
      in PERSONA_REGISTRY.csv as a persona row OR in PERSONA_SCENARIO_REGISTRY.csv as a scenario
      row OR both? Default = both (persona row + scenario row); ratify pre-charter.
    C-72-7 — IntelligenceOps register: extend GOI_POI_REGISTER.csv with new schema columns
      (regulator_specific / media_specific / recruiter_specific fields) OR mint a sibling
      INTELLIGENCEOPS_REGISTER.csv? Default = sibling register; ratify pre-charter.
    C-72-8 — Regulator-relationship roadmap (ENISA): one canonical SOP at
      Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_ENISA.md OR a generic SOP that
      ENISA + future regulators inherit? Default = generic with ENISA worked-example; ratify
      pre-charter.
    C-72-9 — Media-counterparty-onboarding (PR Manager activation): does PR Manager activation
      live in I72 Strand A.1 (Storytelling charter) or Strand C (IntelligenceOps register)?
      Per D-IH-70-X, Storytelling AUTHORS (Marketing); per D-IH-70-AC, media is an
      IntelligenceOps register row. Default = both — Storytelling charter cross-links to
      IntelligenceOps register media row; ratify pre-charter.
    C-72-10 — Recruiter onboarding: same shape as media (Strand A.1 People/People-Ops collaboration?
      OR Strand C IntelligenceOps?). Recruiter is HR-adjacent; default = cross-link to I73 People
      Operations Lead activation; ratify pre-charter.
- Particularly important: ratify C-72-1 (template-promotion threshold: 3 vs 5 vs 7 engagements) at
  PLANNING TIME, not execution. This is architectural; the agent must NOT defer.
- Produce / update docs/wip/planning/_candidates/i72-marketing-area-governance.md with a
  "Discovery findings" section before promoting (the candidate is already 3-strand-reshaped per
  the 2026-05-14 amendment; the agent extends it with Discovery findings).
- One AskQuestion batch: confirm PROMOTE next-step.

Step 2 — Plan-Author (per generic Prompt 2):
- Author .cursor/plans/i72-marketing-area-governance-and-persona-registry-expansion_<8hex>.plan.md
- Author docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md
  (workspace mirror; folder slug per the existing INIT row).
- Author docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/reports/
  p0-charter-<date>.md.
- git mv docs/wip/planning/_candidates/i72-marketing-area-governance.md
        docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/promoted-candidate-<date>.md

Step 3 — Update / mint registry rows (one atomic commit; per generic Prompt 2):

INITIATIVE_REGISTRY.csv (row 58 — UPDATE, do NOT mint a fresh row):
  - status: gated_operator -> active
  - last_review: <today>
  - inception_decision_id: D-IH-70-AC (already set; do not change)
  - notes: append "P0 charter ratified <today> per <new charter D-IH-72 row>; 3 super-strands
    (Marketing / Persona Registry / IntelligenceOps Register Expansion). Master roadmap +
    P0 charter report shipped."

DECISION_REGISTER.csv (mint 7-9 new rows covering all 3 super-strands; one atomic commit):
  Strand A (Marketing) rows:
    - D-IH-72-A — Strand A.1 sub-area charter authoring (4 disciplines + Account Management).
    - D-IH-72-B — Strand A.2 engagement-template promotion machine architecture.
    - D-IH-72-C — Strand A.3 RevOps owner activation (gated on I71 P5 Pack A4).
  Strand B (Persona Registry) rows:
    - D-IH-72-D — Persona registry vs scenario registry boundary verdict (C-72-6).
    - D-IH-72-E — business-developer-collaborator persona row architecture.
  Strand C (IntelligenceOps Register Expansion) rows:
    - D-IH-72-F — IntelligenceOps register architecture (extend vs sibling per C-72-7).
    - D-IH-72-G — regulator-relationship roadmap shape (generic SOP + ENISA worked-example per C-72-8).
    - D-IH-72-H — media-counterparty-onboarding placement (Strand A.1 + C cross-link per C-72-9).
    - D-IH-72-I — recruiter onboarding cross-link to I73 (per C-72-10).
  Charter row:
    - D-IH-72-J (or named "D-IH-72-CHARTER") — I72 charter ratification (3 super-strands;
      activates INIT-OPENCLAW_AKOS-72 from gated_operator to active).
      decision_log_path = the new p0-charter-<date>.md
      supersedes_decision_id: (none; this is the activation decision)

OPS_REGISTER.csv (mint 6 new rows; one atomic commit):
  - OPS-72-1 — Strand A.2 ENGAGEMENT_TEMPLATE_REGISTRY full build + Supabase mirror + ERP panel
    (closure target P2). linked_decision_ids: D-IH-72-B.
  - OPS-72-2 — Strand A.2 SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001 + promotion-rule validator
    (closure target P3). linked_decision_ids: D-IH-72-B.
  - OPS-72-3 — Strand A.3 RevOps owner activation (closure target P4; gated on I71 P5 Pack A4).
    linked_decision_ids: D-IH-72-C.
  - OPS-72-4 — Strand B Persona Registry expansion (business-developer-collaborator persona row +
    any additional persona rows surfaced; closure target P5). linked_decision_ids: D-IH-72-D + D-IH-72-E.
  - OPS-72-5 — Strand C IntelligenceOps Register Expansion (schema for competitor-intelligence-target;
    regulator + media + recruiter onboarding patterns; closure target P6). linked_decision_ids:
    D-IH-72-F + D-IH-72-G + D-IH-72-H + D-IH-72-I.
  - OPS-72-6 — Strand A.1 5 sub-area charter authoring (closure target P1). linked_decision_ids: D-IH-72-A.

Step 4 — Cross-link surfaces:
- WORKSPACE_BLUEPRINT_HOLISTIKA.md section 16.3: link the PMO -> RevOps transition trigger to the
  new master-roadmap.
- HLK_ERP_ARCHITECTURE.md section 4: reserve op_revops_engagement_templates panel slot
  (Strand A.2) + op_intelligenceops_register panel slot (Strand C, if separate register chosen).
- I73 candidate cross-link: recruiter onboarding handoff per D-IH-72-I (update i73 cross-references
  if I73 is also being charted in parallel).
- I75 candidate cross-link: IntelligenceOps register cross-coordinates with I75 P2 Intelligence
  per-source-type SOPs (especially competitor_intelligence_target).
- CHANGELOG.md [Unreleased] / Added: charter entry mirroring the I71 P0 charter format.

Verification before commit (run all; STOP at first FAIL):
- py scripts/validate_decision_register.py
- py scripts/validate_initiative_registry.py
- py scripts/validate_ops_register.py
- py scripts/validate_hlk.py
- py scripts/validate_master_roadmap_frontmatter.py
- py scripts/validate_hlk_vault_links.py
- py scripts/validate_persona_registry.py (Strand B touches PERSONA_REGISTRY.csv only at P5; for
  P0 charter, just verify the validator passes pre-edit)
- py scripts/validate_canonical_registry.py (any new canonicals declared in P0 must be registered)
- py scripts/render_operator_inbox.py (refresh inbox after new OPS rows)

Commit message:
"i72 p0 inline charter + 3 super-strands activation (marketing area governance + persona registry +
intelligenceops register expansion) + registries + workspace cross-links"
Push to origin/main only after operator inline-ratifies (one final AskQuestion: "commit + push?").

DECISION DISCIPLINE (binding):
- NEVER use "OPERATOR PAUSE POINT". Always use "(inline-ratify gate at section X.Y)".
- Architectural decisions ratified at planning time, not deferred.
- For execution-time gates, pre-allocate the gate location in the plan.
- C-72-1 template-promotion threshold MUST be ratified pre-charter; do NOT defer to P2.
- C-72-6 through C-72-10 (Strand B + Strand C architectural choices) MUST be ratified pre-charter.

OPERATOR NOTES (optional context; paste your latest thoughts here):
[paste-here]
```

## --- END PROMPT ---

## Initiative-specific guidance (read before launching)

- **Three super-strands, not one.** The existing INIT row title is the SSOT for scope; the candidate text was narrower because it was authored before the existing INIT row was discovered. The agent must absorb the candidate as **Strand A** of a broader I72 and add **Strand B** (Persona Registry expansion) + **Strand C** (IntelligenceOps Register Expansion) per `D-IH-70-AC` forward-charter.
- **Folder slug**: `72-marketing-area-governance-and-persona-registry-expansion/` (matches the existing INIT row's `folder_path`). Do not use the shorter form.
- **Hold-gate clarification**: I72 P0–P3 can run anytime; only P4 (Strand A.3 RevOps activation) hard-depends on **I71 P5** (Pack A4 = `validate_render_ownership.py`). Earlier wording in this kickoff said "I71 P2" — that was wrong.
- **`D-IH-70-AC` is the inception decision** for this initiative (already set in the registry row). The new charter row mints as a sibling activation decision; do not supersede `D-IH-70-AC`.
- **The 6 patterns from the previous-project annex (P2.4)** are **load-bearing inputs** to Strand A.2 (engagement-template promotion machine) — the agent must read them, not just cite them.
- **Cross-coordinate with I71 P1 outcomes**: the brand-voice register pack (Pack A1) has shipped; the agent should run `validate_brand_voice_register.py` strict mode on any new charter prose authored in this tranche.

## After P0 ships

P1 (4 sub-area charters + Account Management charter) — author one prompt per sub-area; same structure as the I71 per-phase prompt; lift SCOPE from the master-roadmap. P5 (Persona Registry expansion) and P6 (IntelligenceOps Register Expansion) are independent of Marketing P1–P3 and can run in parallel after P0 charter lands.
