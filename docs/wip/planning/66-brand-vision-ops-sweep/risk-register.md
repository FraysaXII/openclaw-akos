---
language: en
status: charter
initiative: 66-brand-vision-ops-sweep
report_kind: risk-register
last_review: 2026-05-08
---

# I66 Risk Register

10 risks tracked across the 5.5-week initiative. Each row: ID · risk · likelihood · impact · mitigation · owner · trigger.

## R-IH-66-1 — Trademark clearance returns blocking conflict on a primary mark

- **Likelihood.** Medium (3/5). Holistika as a registered mark may already exist in non-relevant Nice classes; MADEIRA likely conflicts (it's also a wine region + a Portuguese island; high collision in classes 33 + 39 + 41).
- **Impact.** High (4/5). A blocked mark forces a brand rename mid-initiative or an asymmetric launch (file in EUIPO with one mark, OEPM with another).
- **Mitigation.**
  - P4 clearance reports per mark per jurisdiction; results shared in pause #5 before any filings.
  - Escape hatch: if MADEIRA conflicts in primary classes, file as MADEIRA Agent stylized in Class 9 + 42 only (software / SaaS), never in 33 (wines) or 39 (transport) or 41 (entertainment); accept the trademark posture is "MADEIRA Agent" not "MADEIRA".
  - Document escape decision in DECISION_REGISTER as D-IH-66-CONFLICT-* if triggered.
- **Owner.** Founder + Legal Counsel.
- **Trigger.** P4 clearance result for any of the 5 marks shows a blocking conflict in the target Nice class.

## R-IH-66-2 — Voice canon enrichment over-fits to operator's recorded conversations

- **Likelihood.** Medium-High (4/5). The 20 transcripts are operator-led; collaborator + customer voice is under-sampled.
- **Impact.** Medium (3/5). BRAND_SPANISH_PATTERNS becomes "how the operator speaks" instead of "how Holistika speaks across audiences" — Tier-2 sub-mark voice integrity erodes.
- **Mitigation.**
  - P1 transcript curation explicitly tags speaker role per turn (operator / collaborator / customer / advisor / interviewer).
  - Voice patterns extracted only when ≥2 turns from ≥2 distinct speakers exhibit the same pattern; single-occurrence operator-isms flagged as "operator-pattern" not "brand-pattern."
  - P1 deliverable includes a "voice-patterns under-evidenced" addendum listing patterns where evidence is thin and operator should be skeptical.
- **Owner.** Voice Lead (founder for I66; future BrandOps role).
- **Trigger.** P1 voice synthesis shows >50% of patterns drawn from operator-only speakers.

## R-IH-66-3 — Drift gates produce false positives from rendered DOM scanning

- **Likelihood.** Medium (3/5). `validate_brand_jargon.py` scans DOM; rich text editors, third-party widgets, and code blocks may legitimately contain forbidden tokens.
- **Impact.** Low-Medium (2/5). Failing CI on a false positive blocks deploys; operator frustration; pressure to disable the gate.
- **Mitigation.**
  - Allow-list per gate at the file or selector level (e.g., `/dashboard/**/*` — operator-only legacy area; out of scope per D-IH-66-H).
  - Drift-gate output includes precise file + line + selector for every match; not just "found."
  - P2 deliberate-drift demo verifies the gate fires only on true positives in declared scope.
- **Owner.** Repo Hygiene Operator.
- **Trigger.** ≥2 false positives from `validate_brand_jargon.py` in the first week post-P2.

## R-IH-66-4 — Calendar slip: 5.5 weeks → 7+ weeks

- **Likelihood.** Medium-High (4/5). I66 has more deliverables than I64 + I65 combined.
- **Impact.** Medium (3/5). Operator capacity is the constraint; trademark filings have external timing pressure (EU classes 35 + 42 are competitive; rivals filing first preempts).
- **Mitigation.**
  - Parallelism: P2, P3, P4 run in parallel after P1.
  - Operator pauses are short-cycle (each ≤30 min) so operator throughput doesn't bottleneck.
  - Phase-effort estimates include buffer; agent self-checkpoints catch slip early (≤2 days behind triggers a re-plan, not a silent grind).
  - Cuts list pre-defined: BRAND_LOGO_SYSTEM full audit could descope to "primary mark only" if calendar pressure mounts.
- **Owner.** Founder + System Owner.
- **Trigger.** Cumulative phase slip ≥3 days at any pause point.

## R-IH-66-5 — HUMINT framework leakage to external prose

- **Likelihood.** Medium (3/5). 4 SOPs in IntelligenceOps + per-deck `.objections.md` + `.counterparty-brief.md` companions all draw from internal-only register; mistakes happen.
- **Impact.** High (4/5). Brand collapse if a customer-facing artifact uses HUMINT vocabulary ("counterparty," "elicitation," "reliability grading") instead of the external CORPINT-research register ("client," "discovery interview," "source confidence").
- **Mitigation.**
  - `BRAND_BASELINE_REALITY_MATRIX.md` ships dual-register columns; external column is canonical for external prose.
  - `validate_brand_baseline_reality_drift.py` + new cursor rule `akos-brand-baseline-reality.mdc` enforce external-prose-only-cites-external-register.
  - All deck `.objections.md` + `.counterparty-brief.md` files marked frontmatter `register: internal-only; access_level: 5`.
  - `docs/wip/intelligence/` working-space access_level: 5 enforced via `governance.engagement_intelligence_view` RLS.
  - Operator UAT pause #6 + #7 explicitly checks public surfaces for forbidden internal vocabulary.
- **Owner.** Founder + future BrandOps Lead.
- **Trigger.** Any external-facing artifact (manifesto, deck, press kit, founder bio, dossier) contains a token from the internal-only column without a corresponding external-translation row.

## R-IH-66-6 — Methodology track-record evidence triggers attribution claim

- **Likelihood.** Low-Medium (2/5). Anonymized case study (50K€ → 7 venues) is recognizable to anyone who knows the operator's history.
- **Impact.** High (4/5). If an investor / advisor probes and operator can't substantiate ownership claim or has IP concerns, brand credibility damage.
- **Mitigation.**
  - All public materials use anonymized phrasing per D-IH-66-Q ("in a prior co-founder role I built a fitness-franchise from concept to 7 venues...").
  - Verifiable references behind NDA flag explicit in materials.
  - Cleared advisor / investor materials may include the literal name with operator approval per engagement (operator-discretion gate, not agent-automatic).
  - `FOUNDER_BIO.md` per-audience FAQ has a dedicated entry: "Q: What's an example of your prior work? A: [anonymized]. Specific references available under NDA."
- **Owner.** Founder.
- **Trigger.** External feedback ("can you tell me more about that fitness venue?") that suggests over-clear identification.

## R-IH-66-7 — Boilerplate i18n drift between EN / ES / FR

- **Likelihood.** Medium (3/5). 5 manifestos × 3 languages + new pages × 3 languages = ~30 translation units; humans miss things.
- **Impact.** Medium (3/5). FR or ES surface gets stale; brand voice breaks per locale; native speakers lose trust.
- **Mitigation.**
  - P5 includes EN/ES/FR parity check in CI (next-intl validator already exists; extend to assert no missing keys).
  - `validate_brand_voice_register.py` (P2) explicitly parses each locale.
  - Per-language voice canonical (BRAND_SPANISH_PATTERNS + BRAND_FRENCH_PATTERNS) gives translators a brand-coherence reference.
- **Owner.** Voice Lead.
- **Trigger.** `next-intl` validation reports missing keys after P5.

## R-IH-66-8 — Operator pause fatigue / under-reads at pauses

- **Likelihood.** Medium-High (4/5). 8 pause points × 5.5 weeks = ~1.5 pauses per week sustained for >5 weeks.
- **Impact.** Medium (3/5). Pauses become rubber-stamp; drift slips through.
- **Mitigation.**
  - Pause records use a templated checklist (operator ticks specific items, not just signs).
  - Pause #4 (CSV gate) + #6 (live review) + #7 (template suite) + #8 (drift gate) get specifically high-attention treatment per the rule.
  - Agent self-checkpoint reports surface "what changed since last pause" up-front so operator's 30-min review focuses on diffs not full re-reads.
- **Owner.** Founder.
- **Trigger.** Operator pause record is signed without items ticked, or pause record is single-line ("approved").

## R-IH-66-9 — Trademark filing strategy collides with EU branding rules

- **Likelihood.** Low-Medium (2/5). The accent on "Í" in HOLÍSTIKA Research wordmark may complicate filings; some jurisdictions require Latin-1 only.
- **Impact.** Medium-High (4/5). Filing rejected; refile delays + extra fees.
- **Mitigation.**
  - P4 clearance includes filing-format validation per jurisdiction.
  - Filing strategy may file two versions (with + without diacritic) per jurisdiction; cost is fee × 2 per mark, manageable.
  - BRAND_LOGO_SYSTEM rule "stylized-vs-prose split" already permits both versions; trademark filings target the stylized canonical (with diacritic) for design protection + the plain "HOLISTIKA" wordmark for word protection.
- **Owner.** Legal Counsel.
- **Trigger.** EUIPO or OEPM filing-format guidance excludes diacritic in word marks for the target class.

## R-IH-66-10 — I67 scaffold under-specified; next agent jumps to opinions

- **Likelihood.** Medium (3/5). Research-first scaffolds are designed to be "near-empty"; they reward agents who can sit with ambiguity but punish agents who over-fit fast.
- **Impact.** Medium-High (3/5). I67 produces a confident-sounding plan that's not grounded in operator-specific funnel data; operator wastes a cycle revising.
- **Mitigation.**
  - `AGENT_INSTRUCTIONS.md` in I67 scaffold has six binding mandates including: do not lock tooling / pricing / channels without operator approval; treat scaffold as VERSION 0; challenge every starting hypothesis.
  - `starting-hypotheses.md` is deliberately a tree of `[UNKNOWN]` markers, not opinions; signals "fill in by research."
  - First operator pause in I67 is BEFORE any phase scoping; agent reports research findings + proposed phases together; operator approves both.
- **Owner.** Founder + future BrandOps Lead.
- **Trigger.** I67 first agent submission includes phases without research-citation footers.

## Risk monitoring cadence

- All 10 risks reviewed at every operator pause point (one row per pause record).
- Triggered risks promote to OPS_REGISTER as `risk-mitigation-*` rows.
- I66 closure (P8) re-rates each risk; closed risks marked "Closed"; persistent risks (e.g., R-IH-66-5 HUMINT leakage) inherit into BrandOps continuous register.
