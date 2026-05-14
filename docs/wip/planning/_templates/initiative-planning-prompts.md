---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-13
role_owner: PMO
classification: fact
ssot: true
---

# Initiative-planning prompt trio (Discovery → Plan-Author → Pre-flight)

> **Purpose.** Three copy-pasteable prompts you hand to an agent (Cursor agent, Cloud Agent, or background subagent) so it drives an initiative from "loose idea in your head" to "ready-to-execute Cursor plan" in the **same inline-`AskQuestion` style as the I70 plan-creation transcript** (`.cursor/projects/.../agent-transcripts/72d2e675-...jsonl` — the one that "felt like speaking with the real MADEIRA").
>
> **Authority.** These prompts are the operational expression of three already-active Cursor rules:
>
> - [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — never write `OPERATOR PAUSE POINT`; surface options inline via `AskQuestion`.
> - [`.cursor/rules/akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — phase plan structure, UAT vs automated smoke discipline, `master-roadmap.md` mirror requirement.
> - [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — phase structure (scope / prerequisites / deliverables / verification); strict verification matrix as final gate.
>
> Use them in order — Prompt 1 produces the input to Prompt 2; Prompt 2 produces the input to Prompt 3.

## How to use

1. **Pick the initiative number.** Either an existing candidate (e.g. `i72-marketing-area-governance.md`) or a brand-new one — the prompts work for both.
2. **Paste Prompt 1** into a fresh Cursor chat (Plan mode preferred). Substitute `[INITIATIVE_TITLE]`, `[CANDIDATE_PATH]`, and `[INITIATIVE_NUMBER]`.
3. **Answer the inline `AskQuestion` calls** until the agent says discovery is complete.
4. **Paste Prompt 2** in the **same chat or a new one**. The discovery report is the bridge.
5. **Paste Prompt 3** before the agent starts P1+ execution.

If the agent ever skips an inline question or proposes a real-stop pause, **interrupt and quote the akos-inline-ratification rule.**

---

## Prompt 1 — Discovery + internal/external research + inline questions

```
Goal: Discovery for [INITIATIVE_TITLE] (number [INITIATIVE_NUMBER]).
Do NOT author a Cursor plan yet. ONLY discover, research, and surface options.

Rules in scope (read first, do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- .cursor/rules/akos-mirror-template.mdc

Inputs:
- Candidate scaffold (if any): [CANDIDATE_PATH] (e.g. docs/wip/planning/_candidates/i7N-<slug>.md).
- Operator's loose-thoughts dump (paste below): [OPERATOR_NOTES].

Discovery scope (do all five):

1. INTERNAL RESEARCH — this repo first, sibling repos second.
   - Read the candidate scaffold in full.
   - Grep for related decisions in DECISION_REGISTER.csv (any D-IH-* row whose summary or notes
     mentions the topic).
   - Read related initiatives' master-roadmap.md if cited (active stack: query
     INITIATIVE_REGISTRY.csv where status = active).
   - Read related canonicals: at minimum WORKSPACE_BLUEPRINT_HOLISTIKA.md (table of contents),
     HLK_ERP_ARCHITECTURE.md if ERP/panels are in scope, MARKETING_AREA_M3_REDESIGN.md / 
     PEOPLE_AREA_RESTRUCTURE.md / RESEARCH_AREA_CHARTER.md if those areas are in scope.
   - Read CANONICAL_REGISTRY.csv to confirm asset homes.
   - If sibling repos are in scope (hlk-erp, kirbe-platform, etc.), follow the
     EXTERNAL_REPO_CONTRACT.md cross-link discipline.

2. EXTERNAL RESEARCH — best practices, named patterns, cited prior art.
   - Run targeted web searches (with year suffix, e.g. "2026") on the topic.
   - Cite at least 3 named patterns from outside this repo (with URLs). Prefer engineering blogs,
     specs, and book chapters over slide decks.
   - For each pattern, note: what it solves, where it fits, what it does NOT solve, what
     license/IP posture it carries.
   - Highlight at least one "we'd be diverging from common practice IF we do X — is that
     deliberate?" point.

3. CONUNDRUM SURFACING — the architectural forks in the road.
   - List every architectural choice that has 2+ defensible answers.
   - For each, draft 2–4 ranked options with: rationale, cited evidence (internal or external),
     recommended default (with explicit reasoning).
   - Flag which conundrums must be ratified at planning time (architectural; not deferrable to
     execution) vs which can be deferred to inline-ratify gates during execution.

4. INLINE QUESTIONS — operator ratification round.
   - Surface conundrums via AskQuestion, batched up to 6 per call.
   - Each option label carries: rationale + (one-line citation OR file ref) + (recommended) suffix
     when applicable.
   - DO NOT proceed past unresolved architectural conundrums.
   - If the operator answers "I don't know yet" to a conundrum, ask a follow-up question
     decomposing it into sub-options. Don't move on with ambiguity.

5. DISCOVERY REPORT — the bridge to Prompt 2.
   - Author a markdown report at docs/wip/planning/_candidates/i[INITIATIVE_NUMBER]-<slug>-discovery.md
     (or update the candidate file in place if it exists; preserve the file).
   - Sections:
     a. Operating story (1–2 paragraphs; what the operator is actually trying to build, in
        their own framing, with the agent's clarifying language).
     b. Internal context map (table: artifact / what it does / how this initiative touches it).
     c. External pattern catalog (table: pattern / source / fit / divergence point).
     d. Conundrum index (table: ID / question / options / ratified verdict + decision_id placeholder).
     e. Recommended next step: PROMOTE (ready for Prompt 2), REFINE (more discovery needed),
        DEFER (operator should park it), or RECONSIDER (operator's framing has a flaw).
   - End with a single AskQuestion confirming the recommended next step.

Output: the discovery report. Do NOT modify INITIATIVE_REGISTRY, DECISION_REGISTER, or
OPS_REGISTER yet (those land at P0 in Prompt 2).
```

---

## Prompt 2 — Plan-Authoring + Cursor-plan minting

```
Goal: Author the Cursor plan for [INITIATIVE_TITLE] (number [INITIATIVE_NUMBER]).

CRITICAL — PLAN SCOPE (binding; non-negotiable):
The Cursor plan you author MUST cover the ENTIRE INITIATIVE (every phase: P0 through PN), in
ONE single .plan.md file. The reference shape is the I70 plan at
.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md — ONE strategic plan
covering 17 phases, drilled-down through 5 regression rounds, ~4 300 lines. That is the SOTA bar.

DO:
- Mint a SINGLE plan file at .cursor/plans/<initiative-slug>_<8hex>.plan.md (no phase suffix).
- Cover every phase of the initiative (P0 through PN) with full per-phase decomposition.
- Drill into depth via REGRESSION ROUNDS inside the same file (Round 1 / Round 2 / Round 3 ...).
  Each regression round narrative documents what expanded vs the prior round, captures verbatim
  operator feedback, and refines the existing sections — it does NOT spawn a new plan file.

DO NOT:
- Mint a phase-scoped plan file like i7N_p1_<thing>_<8hex>.plan.md, i7N_p2_<thing>_*.plan.md,
  i7N_strand_a_*.plan.md, etc. The filename has NO phase prefix or strand prefix.
- Fragment the initiative into multiple plan files (one per phase, one per strand). The whole
  initiative lives in ONE file. If a phase has heavy execution detail, that detail goes IN
  the file under that phase's section, not in a sibling file.
- Confuse the per-phase REPORT files (docs/wip/planning/<NN>-<slug>/reports/p<N>-*.md) with the
  Cursor plan. Reports are post-execution artifacts; the plan is the pre-execution strategic
  document. Both exist; they are NOT alternatives.

Phase-scoped plan files have appeared by accident in past sessions (e.g. i71_p1_pack_a1_*.plan.md
during I71 P1 execution). That is a divergence from the I70 reference shape and is corrected by
this guardrail. If you find yourself about to name a file with a phase prefix, STOP and consult
the operator.

Preconditions (verify before writing a single line of plan):
- Discovery report exists and ends with operator-confirmed PROMOTE next-step.
- All conundrums in the report are ratified OR explicitly tagged "deferred to execution-time
  inline-ratify gate" with the gate location pre-allocated.

Outputs (in order):
A. .cursor/plans/<initiative-slug>_<8hex>.plan.md — the authoritative Cursor plan, INITIATIVE-
   SCOPED, covering all phases (NOT a phase-scoped file).
B. docs/wip/planning/[INITIATIVE_NUMBER]-<slug>/master-roadmap.md — workspace mirror per
   .cursor/rules/akos-planning-traceability.mdc.
C. docs/wip/planning/[INITIATIVE_NUMBER]-<slug>/reports/p0-charter-<date>.md — ratification record.
D. New rows in DECISION_REGISTER.csv (D-IH-7N-A architecture/scope, D-IH-7N-B sibling, D-IH-7N-C
   charter ratification, plus any pre-execution-ratified conundrum decisions).
E. New row in INITIATIVE_REGISTRY.csv (status = active).
F. New rows in OPS_REGISTER.csv (one OPS-7N-K per execution strand).
G. WORKSPACE_BLUEPRINT_HOLISTIKA.md cross-link entry if the initiative authors a
   workspace-wide canonical.
H. CHANGELOG.md [Unreleased] / Added entry.

Cursor-plan structure (match the I70 plan shape; see
.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md):
- Frontmatter: name, overview (1 paragraph), todos[] (one entry per phase with status), isProject: false.
- "Operating story" — the answer to "Do you know where I'm trying to go?" (lift from discovery report,
  refine).
- "Phase status table" with: phase / title / status / commit (— at planning time) / notes.
- Per-phase decomposition with the four-section pattern from
  .cursor/rules/akos-governance-remediation.mdc:
    SCOPE — what this phase is and is NOT.
    PREREQUISITES — what must be true before this phase starts.
    DELIVERABLES — what files / rows / artifacts ship.
    VERIFICATION — what validators / tests / UAT confirm completion.
  PLUS for inline-ratify phases: gate location + question shape.
- "Conundrums" — every remaining open architectural question with 2–4 ranked options.
- "Decision preview" — D-IH-7N-* rows that will mint during execution, with one-line summary each.
- "Risk register" — top 5 risks with severity + mitigation.
- "Verification matrix" — the closing-UAT acceptance criteria checklist.
- "Cross-references" — every cited file/folder/decision/initiative.

Decision discipline (binding):
- NEVER use the phrase "OPERATOR PAUSE POINT". Always say "(inline-ratify gate at §X.Y)".
- Architectural decisions that affect what gets built must be ratified at planning time.
  If you're tempted to defer one, that's a signal the plan is incomplete; finish planning
  before declaring it ready.
- For every D-IH row you mint, populate decision_log_path so the validator can find it.
- For every OPS row you mint, set originating_initiative_id, owner_role, status: open, and
  closure target phase in the notes.
- For every INITIATIVE row you mint, set inception_decision_id (= D-IH-7N-C charter) and
  master roadmap path.

Verification before committing the plan tranche (run, do not skip):
- py scripts/validate_decision_register.py
- py scripts/validate_initiative_registry.py
- py scripts/validate_ops_register.py
- py scripts/validate_hlk.py
- py scripts/validate_master_roadmap_frontmatter.py
- py scripts/validate_hlk_vault_links.py
- py scripts/render_operator_inbox.py (refresh OPERATOR_INBOX.md)

Atomic commit discipline:
- ONE commit for the P0 tranche (all of A–H above).
- Commit message format: "i[INITIATIVE_NUMBER] p0 inline charter + registries + workspace cross-links"
- Push to origin/main only after the operator inline-ratifies.

End the chat with an AskQuestion confirming the operator wants to commit + push, OR delegate the
P1+ execution to a separate session.
```

---

## Prompt 3 — Pre-execution Pre-flight

```
Goal: Pre-flight check for [INITIATIVE_TITLE] (number [INITIATIVE_NUMBER]) before P1 execution begins.

Run all of the following sequentially. STOP at the first FAIL.

1. P0 landed on main:
   - git log --oneline -1 — confirm latest commit is the P0 charter commit.
   - INITIATIVE_REGISTRY.csv has the [INITIATIVE_NUMBER] row with status: active.
   - DECISION_REGISTER.csv has D-IH-7N-A, B, C (and any conundrum-ratified rows).
   - OPS_REGISTER.csv has at least one OPS-7N-K row, status: open.
   - master-roadmap.md exists at docs/wip/planning/[INITIATIVE_NUMBER]-<slug>/.
   - Cursor plan exists at .cursor/plans/<slug>_<8hex>.plan.md.

2. Validator matrix green (run all; report any FAIL or non-empty stderr):
   - py scripts/validate_hlk.py
   - py scripts/validate_decision_register.py
   - py scripts/validate_initiative_registry.py
   - py scripts/validate_ops_register.py
   - py scripts/validate_canonical_registry.py
   - py scripts/validate_compliance_schema_drift.py
   - py scripts/validate_hlk_vault_links.py
   - py scripts/release-gate.py (browser-smoke FAIL is a known carry-over; everything else must PASS)

3. No open architectural conundrums:
   - Read the plan's Conundrums section.
   - Every entry must be either (a) ratified with a D-IH row, or (b) explicitly tagged
     "execution-time inline-ratify gate at §X.Y" (no orphan question marks).

4. Operator alignment:
   - Surface a single AskQuestion: "P0 is shipped, validators are green, no open architectural
     conundrums. Confirm proceed to P1 execution? (yes / pause / re-plan)".
   - If "pause": stop. If "re-plan": jump back to Prompt 1 with a refined operator-notes block.

5. P1 kickoff:
   - Open the Cursor plan; locate the P1 todo entry; mark it in_progress.
   - Read the P1 SCOPE / PREREQUISITES section.
   - Begin execution; one atomic commit per phase; AskQuestion at every inline-ratify gate.

Reporting: if any step fails, STOP and write a 5-line blocker report at
docs/wip/planning/[INITIATIVE_NUMBER]-<slug>/reports/p0-pre-flight-blocker-<date>.md per the
opt-stop-report posture in .cursor/rules/akos-governance-remediation.mdc.
```

---

## Notes for the operator

- **Why three prompts and not one.** Discovery and Plan-Author are different cognitive modes; combining them is what produces the "OPERATOR PAUSE POINT" anti-pattern that I70 retired. Pre-flight is the cheap insurance that prevents P1 starting on a broken foundation.
- **Why inline `AskQuestion` and not a chat back-and-forth.** Structured options (with rationale + citations) compress 4–6 messages of free-form Q&A into one batched ratification. The I70 transcript closed 25 architectural decisions in a few minutes of operator wall-clock time using this pattern.
- **Where the prompts plug into the rules.** Prompt 1 enforces the inline-ratify rule + planning-traceability discovery shape. Prompt 2 enforces the phase structure + atomic-commit discipline + UAT vs automated smoke. Prompt 3 enforces the strict verification matrix.
- **Iterating on the prompts.** When you find a phrase that consistently produces the discovery output you want, edit this file. Cursor agents will read it on each session if you `@`-reference it.

## Cross-references

- I70 plan (the gold-standard reference shape): [`.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md`](../../../../.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md).
- Inline-ratify rule: [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc).
- Planning traceability rule: [`.cursor/rules/akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc).
- Governance remediation rule: [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc).
- External-repo mirror rule: [`.cursor/rules/akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc).
- Cursor docs on large-codebase planning: <https://docs.cursor.com/en/guides/advanced/large-codebases>.
