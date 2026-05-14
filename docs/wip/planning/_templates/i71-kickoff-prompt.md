---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-13
target_initiative: INIT-OPENCLAW_AKOS-71
target_phase: P1 (Pack A1 — Brand voice register expansion)
classification: fact
ssot: false
---

# I71 kickoff — Cursor plan minting + P1 execution (Pack A1)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat (Plan or Agent mode). Optional: paste any operator notes after the operator-notes section.**

## --- BEGIN PROMPT ---

```
Goal: (a) author a Cursor plan for INIT-OPENCLAW_AKOS-71 from the existing workspace master-roadmap,
      then (b) execute I71 P1 (Pack A1 — Brand voice register expansion) as one atomic commit.

CRITICAL — PLAN SCOPE (binding; non-negotiable):
The Cursor plan you mint MUST cover the ENTIRE I71 INITIATIVE (P0 through P6) in ONE file at
.cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_<8hex>.plan.md. The reference
shape is the I70 plan at .cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md
— ONE strategic plan covering 17 phases, drilled-down through 5 regression rounds. That is the
SOTA bar. DO NOT mint a phase-scoped file (e.g. i71_p1_pack_a1_<8hex>.plan.md). DO NOT fragment
P1 / P2 / P3 / P4 / P5 / P6 into separate plan files. Filename has NO phase prefix.
Regression rounds (Round 1 / Round 2 / ...) drill into depth ON THE SAME FILE. If a phase needs
heavy detail, that detail goes IN the file under that phase's section, not in a sibling file.
A phase-scoped file like i71_p1_pack_a1_brand_voice_register_*.plan.md has appeared in the past
during I71 P1 execution; that is a documented divergence and corrected by this guardrail.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md
  (this is the authoritative phase-by-phase scope; lift it into the Cursor plan)
- docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p0-charter-2026-05-13.md
- docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_COPYWRITING_DISCIPLINE.md
  (the canonical that Pack A1 enforces; 7 tic families + 11 anti-pattern seeds)
- scripts/validate_brand_voice_register.py
  (the existing validator that Pack A1 extends)
- tests/test_validate_brand_voice_register.py (or sibling test module if present)

Step 1 — Cursor plan minting (small lift; don't over-author):
- Author .cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_<8hex>.plan.md
- Lift the master-roadmap content; expand each phase's todos with status flags:
    P0 status: completed (commit eb4c1b4 on main)
    P1 status: in_progress
    P2-P6 status: pending
- Frontmatter: name, overview (1 paragraph), todos[] (one per phase), isProject: false
- Don't duplicate prose verbatim; use cross-links to the master-roadmap

Step 2 — P1 execution (Pack A1 — Brand voice register expansion):
SCOPE:
- Extend scripts/validate_brand_voice_register.py with:
    a. 7 tic-family enforcement (per BRAND_COPYWRITING_DISCIPLINE.md section 2)
    b. Locale-aware register checks (FR/EN/ES per BRAND_REGISTER_MATRIX)
    c. Audience-matrix hooks (4 quadrants from BRAND_GANTT_DISCIPLINE)
    d. Storytelling-vs-Resonance boundary check per D-IH-70-X
- Add a YAML rule pack at:
    docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/register-pack.yml
- Add tests at:
    tests/test_validate_brand_voice_register_expansion.py
    (cover: 7 tic-family detections, locale variance, audience-matrix hits, boundary check)
- Wire into scripts/release-gate.py as a [PASS] row.

PREREQUISITES:
- I71 P0 closed (verified by INITIATIVE_REGISTRY.csv row INIT-OPENCLAW_AKOS-71 status=active and
  D-IH-71-A in DECISION_REGISTER.csv).
- BRAND_COPYWRITING_DISCIPLINE.md exists at federated path (verify; landed at I70 P5 commit 240c448).

DELIVERABLES (one atomic commit):
- Validator extension (scripts/validate_brand_voice_register.py).
- Rule-pack YAML (register-pack.yml).
- Test module (tests/test_validate_brand_voice_register_expansion.py).
- release-gate integration (scripts/release-gate.py edit).
- CHANGELOG entry under [Unreleased] / Added.
- Update OPS-71-1 row notes to "P1 Pack A1 shipped" but keep status=open until P5 closes the strand.

VERIFICATION before commit (run all; STOP at first FAIL):
- py -m pytest tests/test_validate_brand_voice_register_expansion.py -v
- py scripts/validate_brand_voice_register.py (strict mode) on the canonical brand path
- py scripts/release-gate.py
- py scripts/validate_hlk.py
- py scripts/validate_decision_register.py
- py scripts/validate_initiative_registry.py
- py scripts/validate_ops_register.py

INLINE-RATIFY GATE (per .cursor/rules/akos-inline-ratification.mdc):
- Conundrum C-71-1 (Pack A1 strictness ladder): soft-for-30-days vs strict-on-day-1.
- Surface AskQuestion BEFORE wiring release-gate; default = soft for first 30 days.
- Capture verdict as D-IH-71-F in DECISION_REGISTER.csv; decision_log_path =
    docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-pack-a1-2026-MM-DD.md

COMMIT MESSAGE:
"i71 p1 pack a1 brand voice register expansion (7 tic families + locale + audience + boundary)"
Push to origin/main only after operator inline-ratifies (one final AskQuestion: "commit + push?").

OPERATOR NOTES (optional context; paste your latest thoughts here):
[paste-here]
```

## --- END PROMPT ---

## What to expect from the agent

- Cursor plan file appears at `.cursor/plans/i71-...plan.md`; this is the source-of-truth for execution.
- One inline `AskQuestion` at the strictness-ladder gate (C-71-1).
- One commit on `main` with message `i71 p1 pack a1 ...`.
- `OPS-71-1` notes updated; row stays `open` until P5 closes the validator-pack strand.

## If the agent gets stuck

- Validator failure: it should write a 5-line blocker report at `docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-blocker-<date>.md` per `.cursor/rules/akos-governance-remediation.mdc` `opt-stop-report` posture.
- Conundrum it can't decide: it should surface a fresh `AskQuestion`, not improvise.

## After P1 ships, the next prompts

- **P2** — Pack A2 (Gantt confidence) + Pack A3 (multilingual locale-suffix). Same structure; substitute `BRAND_GANTT_DISCIPLINE.md` and `BRAND_MULTILINGUAL_CONTRACT.md` as canonicals.
- **P3** — Strand C1 release-taxonomy SOP authoring. Closes `OPS-71-2`.
- **P4** — Strand C2 review-stamp dimension. Closes `OPS-71-3`.
- **P5** — Pack A4 (render ownership) + Strand B hardening.
- **P6** — Closing UAT.

You can hand the same prompt structure to the agent for each phase, swapping the SCOPE block.
