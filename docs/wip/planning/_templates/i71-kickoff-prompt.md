---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-14
target_initiative: INIT-OPENCLAW_AKOS-71
target_phase: P2 (Packs A2 + A3 + Addition 11 + Tier 1 Vale sibling)
classification: fact
ssot: false
---

# I71 kickoff — P2 execution (Packs A2 + A3 + Addition 11 + Tier 1 Vale sibling)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat (Plan or Agent mode).**

## I71 status (as of 2026-05-14)

| Phase | Title | Status | Anchor |
|:---|:---|:---|:---|
| **P0** | Charter + WORKSPACE §18 + Strand C scope | **SHIPPED** | commits `e129bac` + `eb4c1b4`; 5 D-IH-71-A..E rows; 3 OPS-71-* rows. |
| **P1** | Pack A1 (Brand voice register expansion — chassis edition) | **SHIPPED** 2026-05-14 | commit `bdfc413`; `akos/brand_voice_register.py` Pydantic chassis (16 models, 6 parsers); 3 new canonicals (`BRAND_ENGLISH_PATTERNS.md`, `BRAND_LLM_TONE_TELLS.md`, `_validators/README.md`); `_validators/register-pack.yml` operator override; 6 D-IH-71-F..K rows; 28-case test suite; release-gate row updated in-place. |
| **P2** | **THIS PHASE** — Packs A2 + A3 + Addition 11 + Tier 1 Vale sibling | pending | Authoritative scope below. |
| P3 | Strand C1 (release-taxonomy SOP) | pending | OPS-71-2. |
| P4 | Strand C2 (review-stamp dimension; Supabase migration) | pending | OPS-71-3. |
| P5 | Pack A4 (render ownership) + Strand B hardening | pending | Gates I72 P4 (RevOps activation). |
| P6 | Closing UAT + INITIATIVE_REGISTRY closure | pending | OPS-71-1. |

I71 P1 strategic review (2026-05-14, post-ship) folded **Tier 1 — Vale sibling** into P2 scope and minted **I78 candidate** (Tier 2 LLM-as-judge advisory layer) as forward-charter; Tier 3 (writer-facing inline UX) remains parked behind a team-scale trigger. See [`docs/wip/planning/_candidates/i78-brand-voice-llm-judge.md`](../_candidates/i78-brand-voice-llm-judge.md) for the forward-charter design and [I71 master-roadmap §P2](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) for the canonical P2 scope.

## --- BEGIN PROMPT ---

```
Goal: (a) extend the existing I71 strategic plan with full P2 detail (regression-round-grade, in
the same .cursor/plans/ file — see SCOPE GUARDRAIL below), then (b) execute I71 P2 (Packs A2 + A3 +
Addition 11 + Tier 1 Vale sibling) as one atomic commit per phase OR a single combined P2 commit
(operator chooses at inline-ratify gate; Pack A1 precedent shipped as one combined commit).

CRITICAL — PLAN SCOPE (binding; non-negotiable):
The Cursor plan you author/extend MUST be the SINGLE INITIATIVE-SCOPED I71 plan covering ALL phases
(P0 SHIPPED, P1 SHIPPED, P2 active, P3-P6 pending). The reference shape is the I70 plan at
.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md — ONE strategic plan
covering 17 phases, drilled-down through 5 regression rounds, ~4 300 lines.

KNOWN HISTORICAL DIVERGENCE: The I71 P1 plan landed as a phase-scoped file at
.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md (738 lines, 3 regression rounds,
P1-only). That file STAYS in place as a historical artifact (P1 already shipped); do NOT re-author
or move it. Going forward (P2+), the canonical I71 plan lives at:
  .cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_<8hex>.plan.md  (initiative-scoped)

If that initiative-scoped file does not yet exist, MINT it now in Step 1 and absorb the P1 plan's
chassis narrative as Round 1 of P1's section (with cross-link to the historical phase-scoped
file). If it already exists, EXTEND it with P2 detail as a new regression round.

Either way: ONE file going forward. Phase-scoped files (i71_p2_*.plan.md, i71_a2_*.plan.md, etc.)
are forbidden.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md
  (authoritative phase-by-phase scope; especially §P2 which now folds Tier 1 Vale)
- docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p0-charter-2026-05-13.md
- docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-pack-a1-2026-05-14.md
  (if authored; the I71 P1 phase report capturing Round 2 + Round 3 ratifications)
- .cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md (historical; lift P1 chassis
  narrative as Round 1 of P1 section in the new initiative-scoped plan)
- akos/brand_voice_register.py (Pydantic chassis from P1; A2/A3 extend it with Gantt + multilingual
  models)
- scripts/validate_brand_voice_register.py (P1 thin CLI; A2/A3 ship sibling thin CLIs on the same
  chassis)
- docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_GANTT_DISCIPLINE.md
  (Pack A2 source; 5-level confidence ladder + 4-quadrant audience matrix)
- docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_MULTILINGUAL_CONTRACT.md
  (Pack A3 source; D-IH-70-P 3-file pattern)
- docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/register-pack.yml
  (P1 YAML operator override; A2/A3 add gantt-pack.yml + multilingual-pack.yml siblings)
- docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/README.md
  (P1 _validators/ index; A2/A3 register their packs here)
- docs/wip/planning/_candidates/i78-brand-voice-llm-judge.md
  (Tier 2 forward-charter context; Tier 1 Vale lives in this P2 scope, not in I78)
- Vale documentation at https://vale.sh/docs/ (Tier 1 Vale sibling: read 'Concepts', 'Styles',
  'Vocabularies', 'Sequence Checks'; Vale is the open-source NLP+POS-tagging linter the I71 P1
  strategic review identified as the deterministic-NLP gap-closer)

Step 1 — Initiative-scoped plan minting / extension:

If .cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_<8hex>.plan.md does NOT exist:
  - MINT it. Frontmatter: name "I71 — CI/CD Discipline and AIOps Baseline Maturity", overview
    1-paragraph summary, todos[] one entry per phase (P0/P1 status: completed; P2 status:
    in_progress; P3-P6 status: pending), isProject: false.
  - Body sections (match I70 plan shape):
    - Operating story (lift from master-roadmap §"Operating story"; refine).
    - Phase status table (lift from master-roadmap; mark P0 + P1 SHIPPED with commit SHAs;
      P2 in_progress).
    - Per-phase decomposition with the 4-section pattern (SCOPE / PREREQUISITES / DELIVERABLES /
      VERIFICATION) for ALL phases P0 through P6, not just P2. P0 + P1 sections summarize what
      shipped (lift from p0-charter-2026-05-13.md + the historical P1 phase-scoped plan as Round 1).
      P2 section is the new regression round; P3-P6 sections preview the work.
    - Conundrums (carry over from master-roadmap §Conundrums; mark C-71-1 RESOLVED at P1 inline-
      ratify with D-IH-71-F verdict; surface new C-71-Vale-* conundrums for Tier 1 Vale design).
    - Decision preview (D-IH-71-F..K MINTED 2026-05-14 at P1; D-IH-71-L..R + CLOSURE pending).
    - Risk register (top 5; carry over from master-roadmap).
    - Cross-references.

If .cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_<8hex>.plan.md EXISTS:
  - EXTEND its P2 section as a new regression round. Operator-quote the I71 P1 strategic review
    insight that surfaced Tier 1 Vale fold-in. Add the SCOPE / PREREQUISITES / DELIVERABLES /
    VERIFICATION 4-section pattern for P2.

Step 2 — P2 execution (Packs A2 + A3 + Addition 11 + Tier 1 Vale sibling):

SCOPE:

A2 — Brand Gantt confidence ladder enforcement:
- New scripts/validate_brand_gantt_confidence.py thin CLI on akos/brand_voice_register.py chassis.
- Extend chassis with GanttConfidenceRule + AudienceQuadrantRule Pydantic models if not already
  there; reuse existing AudienceQuadrant Literal from P1.
- Walk Gantt artifact prose (per BRAND_GANTT_DISCIPLINE.md §2 Variant A/B/C/D × audience-formality
  × data-maturity matrix) and detect:
    a. Confidence cells outside the 5-level ladder
    b. Variant assignment that doesn't match audience-formality dimension
    c. Confidence inflation (cells claim higher confidence than data-maturity supports)
- New gantt-pack.yml at docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/
  with same operator-override structure as register-pack.yml.

A3 — Brand multilingual locale-suffix enforcement:
- New scripts/validate_brand_multilingual.py thin CLI on akos/brand_voice_register.py chassis.
- Extend chassis with LocaleSuffixRule + ReadmeTriadRule Pydantic models.
- Walk engagement folders (Think Big/Clients/* and Advisers/*) and detect:
    a. Engagement README.md missing the 5-line pointer pattern per D-IH-70-P
    b. Engagement with README.md but missing README.fr.md OR README.en.md (per BRAND_MULTILINGUAL_
       CONTRACT.md 3-file pattern)
    c. Per-locale frontmatter cohesion (language: en in README.en.md, language: fr in README.fr.md)
- New multilingual-pack.yml sibling.

Addition 11 — Localised number / currency / date formats (Tier-3 fold-in from P1 Round 3):
- Author BRAND_LOCALISED_FORMATS.md canonical at docs/references/hlk/v3.0/Admin/O5-1/Marketing/
  Brand/canonicals/ (per-locale rules: en uses 1,234.56 / FR uses 1 234,56 / ES uses 1.234,56;
  EUR symbol position; date formats per locale).
- Extend akos/brand_voice_register.py chassis with NumberFormatRule + CurrencyFormatRule +
  DateFormatRule Pydantic models.
- Surface via either A2's validator (Gantt confidence cells often carry money/dates) or a sibling
  validate_brand_localised_formats.py — pick at design time based on size/scope.

Tier 1 — Vale sibling (deterministic-NLP layer; folded in 2026-05-14):
- Translate brand canonicals into Vale's .ini format via a one-time generator script:
    scripts/generate_vale_styles.py
  Reads docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/*.md, emits
    .vale/styles/Holistika/*.yml + Vocab/Holistika.txt + Vocab/Holistika-rejected.txt
- .vale.ini config at repo root (or under tools/.vale.ini); MinAlertLevel = warning during P2,
  promotable to error after operator UAT.
- CI integration: new release-gate.py row "Brand voice (Vale sibling; deterministic-NLP layer)";
  runs alongside existing regex chassis. The two are complementary: regex catches named
  violations (T-3-delve-into); Vale catches grammar patterns (any superlative-adjective in a
  customer-facing slide H1).
- Tests at tests/test_vale_styles_generator.py confirming generator output is deterministic and
  Vale-syntax-valid.

PREREQUISITES:
- I71 P1 SHIPPED 2026-05-14 (commit bdfc413; verified by INITIATIVE_REGISTRY.csv row
  INIT-OPENCLAW_AKOS-71 status=active with Pack A1 noted in row 57 notes).
- akos/brand_voice_register.py exists with chassis from P1; tests/test_validate_brand_voice_
  register_expansion.py exists.
- Vale binary installable on operator's host (operator confirms or skips CI integration if not).

DELIVERABLES (one combined P2 commit OR one commit per pack — operator decides at inline-ratify):
- scripts/validate_brand_gantt_confidence.py + gantt-pack.yml + tests
- scripts/validate_brand_multilingual.py + multilingual-pack.yml + tests
- BRAND_LOCALISED_FORMATS.md + chassis extension (3 new Pydantic models) + validator wiring + tests
- scripts/generate_vale_styles.py + .vale.ini + .vale/styles/Holistika/*.yml + Vocab/*.txt +
  release-gate row + tests
- CHANGELOG entry under [Unreleased] / Added covering all 4 deliverables
- 4 new D-IH-71-* rows: D-IH-71-L (A2 ratification), D-IH-71-M (A3 ratification), D-IH-71-N
  (Addition 11 ratification), and D-IH-71-Vale (Tier 1 Vale sibling architecture ratification —
  operator picks the row letter)
- OPS-71-1 notes appended ("P2 packs A2/A3 + Addition 11 + Tier 1 Vale shipped"); status stays
  open until P5 closes the strand
- Phase report at docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/
  p2-pack-a2-a3-addition-11-vale-2026-MM-DD.md

VERIFICATION before commit (run all; STOP at first FAIL):
- py -m pytest tests/test_validate_brand_gantt_confidence.py -v
- py -m pytest tests/test_validate_brand_multilingual.py -v
- py -m pytest tests/test_vale_styles_generator.py -v
- py scripts/validate_brand_gantt_confidence.py --pack-path canonicals/_validators/gantt-pack.yml
- py scripts/validate_brand_multilingual.py --pack-path canonicals/_validators/multilingual-pack.yml
- vale --config=.vale.ini docs/  (or skip if Vale not installed; report SKIP)
- py scripts/release-gate.py
- py scripts/validate_hlk.py
- py scripts/validate_decision_register.py
- py scripts/validate_initiative_registry.py
- py scripts/validate_ops_register.py
- py scripts/validate_canonical_registry.py (BRAND_LOCALISED_FORMATS.md is a new canonical;
  must register)

INLINE-RATIFY GATES (per .cursor/rules/akos-inline-ratification.mdc):
- C-71-2 (Pack A3 SUEZ vs general-engagement strictness): warn-until-2-bilingual vs strict-day-1.
  Default = warn; ratify at execution time.
- New C-71-Vale-1 (Vale config posture): MinAlertLevel = warning during P2 vs error from day 1.
  Default = warning; promote to error after 30-day UAT.
- New C-71-Vale-2 (Vale Vocab strategy): generate per-canonical-file Vocab vs single
  Holistika.txt/Holistika-rejected.txt pair? Default = single pair (simpler); per-canonical only
  if rule cardinality forces.
- A2/A3/Addition-11 commit posture: one combined P2 commit (Pack A1 precedent) OR three sub-phase
  commits (P2.1/P2.2/P2.3)? Default = one combined commit.

COMMIT MESSAGE (combined commit option):
"i71 p2 packs a2 + a3 + addition 11 + tier 1 vale sibling (gantt confidence + multilingual locale
+ localised formats + deterministic NLP layer)"

OR three sub-phase messages (per-pack option):
- "i71 p2.1 pack a2 brand gantt confidence ladder (5-level + 4-quadrant audience matrix)"
- "i71 p2.2 pack a3 brand multilingual locale-suffix (3-file pattern + per-locale frontmatter)"
- "i71 p2.3 addition 11 + tier 1 vale sibling (localised formats + deterministic NLP layer)"

Push to origin/main only after operator inline-ratifies (one final AskQuestion: "commit + push?").

OPERATOR NOTES (optional context; paste your latest thoughts here):
[paste-here]
```

## --- END PROMPT ---

## What to expect from the agent

- The canonical initiative-scoped Cursor plan appears at `.cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_<8hex>.plan.md` if it didn't exist; otherwise it gets a new P2 regression round appended.
- Up to 4 inline `AskQuestion` rounds (C-71-2, C-71-Vale-1, C-71-Vale-2, commit-posture).
- One combined commit on `main` with message `i71 p2 packs a2 + a3 + addition 11 + tier 1 vale sibling ...` — OR three sub-phase commits per operator's commit-posture verdict.
- `OPS-71-1` notes updated; row stays `open` until P5 closes the validator-pack strand.

## If the agent gets stuck

- Vale not installable on the host: report SKIP for the Vale CI step, ship the generator + styles + Vocab files anyway (they're text artifacts; CI integration deferred to a follow-up commit).
- A2/A3 chassis extension breaks P1 chassis tests: `NOT VALID + VALIDATE CONSTRAINT` pattern doesn't apply here (Pydantic, not Postgres) — the agent should add the new models additively without changing existing model signatures, and run the full P1 test suite before commit.
- Validator failure: 5-line blocker report at `docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p2-blocker-<date>.md` per `.cursor/rules/akos-governance-remediation.mdc` `opt-stop-report` posture.

## After P2 ships, the next prompts

- **P3** — Strand C1 (release-taxonomy SOP authoring; closes `OPS-71-2`). ~1 day; one commit.
- **P4** — Strand C2 (review-stamp dimension; column-vs-table inline-ratify; Supabase migration; closes `OPS-71-3`). 2-3 days.
- **P5** — Pack A4 (render ownership) + Strand B hardening (MCP smoke). Unblocks I72 P4 (RevOps activation).
- **P6** — Closing UAT + INITIATIVE_REGISTRY closure.

Each subsequent phase extends the same initiative-scoped Cursor plan as a new regression round (per the SCOPE GUARDRAIL above). Lift this kickoff and swap the SCOPE block.
