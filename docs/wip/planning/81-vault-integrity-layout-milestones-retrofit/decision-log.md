# I81 — Decision log

Full rationale for every `D-IH-81-*` decision. Source-of-truth row lives in [`DECISION_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv); this file carries the human-readable narrative.

Cross-reference: [I81 master-roadmap §2](master-roadmap.md#2-charter-decisions-ratified-at-p0-agent-default-operator-skip-2026-05-16).

## P0 — ratified 2026-05-16 (`decision_source: agent_inline_default`; user confirmation 2026-05-16 evening: "answered all 18 questions; please continue")

### D-IH-81-A — Retrofit mode (continuous vs absorbed)

**Question:** Should the 40-SOP retrofit run as a continuous 5-8 day sprint or absorbed into per-area quarterly review?

**Options surveyed:**

- A: **Continuous** — single-initiative ~5-8 days; fastest closure; high context-switch risk.
- B: **Absorbed** — each area's role_owner retrofits during their existing quarterly canonical-review window. Slower aggregate closure but lower fatigue and better register-discipline preservation.

**Verdict:** **B — Absorbed.** Default per candidate §5 C-81-1. P4-P8 schedulable as parallel waves rather than forced linear sequence; allows role_owners to retrofit alongside other area work.

**Trade-off accepted:** I81 closure stretches across ≥ 2 quarterly cycles; mitigated by per-strand phase tracking (each P4-P8 phase closes when its strand is complete; the initiative closes when all five strands close).

### D-IH-81-B — No-addendum-needed threshold

**Question:** When does an SOP legitimately not need an addendum?

**Verdict:** Heuristic — body word-count ≥ 600 OR cross-area integration count ≥ 2 → addendum recommended. Below threshold: body-only acceptable; record `addendum_needed: false` in retrofit log. Per-pair author judgement is final (heuristic guides, doesn't gate).

**Expected outcome:** 10-30% of the 40 remaining SOPs end up body-only, narrowing actual paired-file count to ~28-36.

### D-IH-81-C — Author posture

**Question:** Each area's `role_owner` authors retrofits OR a single agent batch-retrofits all?

**Verdict:** **Each area's `role_owner` with agent assistance.** Preserves register-discipline expertise per area (Tech speaks tech; Marketing speaks brand-voice; Research speaks CORPINT; Compliance speaks classification-routing). Agent does mechanical scaffolding (split body → body + addendum.md; populate frontmatter; mint KNOWLEDGE_PAIRING row); role_owner reviews + signs off on register choices.

### D-IH-81-E — Per-area register-specific jargon-scan extension

**Question:** Should `validate_design_pattern_registry.py --jargon-scan` extend to non-People area canonicals (Marketing brand register; Tech framework register) using their own register-specific forbidden-token lists?

**Verdict:** **Out-of-scope for I81.** Per-area register-jargon is legitimate by design (the I79 doctrine explicitly carves out Tech jargon → Tech Lab; brand jargon → Marketing/Brand). Cross-area jargon contamination is a real risk but mechanical detection requires per-area forbidden-token list authoring upstream of the validator — that authoring is its own governance work, not I81 scope. Logged as future-gate candidate in P1 integrity report; no validator extension this run.

### D-IH-81-H — Named-milestone schema vocabulary

**Question:** What ID format for the named-milestone schema that replaces magic-number cross-references?

**Options surveyed:**

- A: `<I_ID>-<PURPOSE_SLUG>` — e.g., `I82-CAPABILITY-REGISTRY-MINT`. Simple, stable, no embedded sequence (phase position lives in frontmatter `milestones:` array, not the ID).
- B: `<I_ID>-M<NN>-<PURPOSE_SLUG>` — e.g., `I82-M02-CAPABILITY-REGISTRY-MINT`. Orderable but reintroduces magic numbers.
- C: `<I_ID>:<PURPOSE_SLUG>` — e.g., `I82:CAPABILITY-REGISTRY-MINT`. Colon awkward in markdown anchors.

**Verdict:** **A — `<I_ID>-<PURPOSE_SLUG>`.** Simplest stable form. `INITIATIVE_ID` matches `^I\d{2,3}$`; `PURPOSE_SLUG` is `UPPER-KEBAB-CASE`, ≤ 6 hyphenated tokens, semantically meaningful (not `PHASE-2`). Frontmatter `milestones:` array carries `id`, `phase` (informational `P\d+(\.\d+)?` mapping), `purpose` (1 sentence), `status` (`planned` / `in_progress` / `closed` / `cancelled`). Body headers retain `## P<N> — <name>` AND add `(milestone: I<NN>-<SLUG>)` parenthetical on first occurrence.

**Validation rule:** `scripts/validate_planning_cross_refs.py` (P3 deliverable) loads each plan's frontmatter `milestones:` and resolves every `I<NN>-<SLUG>` reference in body; fails loudly on unresolved IDs. Phase parenthetical drift (e.g., body says `(currently P2)` but frontmatter says `phase: P3`) is **warn-only** because the parenthetical is informational and the canonical ID is the FK.

**Finalisation:** If P3 migration of the first wave reveals corner cases, schema may be refined at P3 close.

## Deferred decisions (close at later phases)

| ID | Question | Owner | Close-out phase |
|:---|:---|:---|:---|
| D-IH-81-D | Forward-extension to non-SOP canonicals (registries + doctrines) | People Operations Lead | P9 |
| D-IH-81-F | Integrity matrix methodology + PASS threshold — what constitutes CLOSED-P1? | PMO + System Owner | P1 |
| D-IH-81-G | Layout migration wave plan — which root files move in which tranche; deprecation-alias policy | Data Architect + Compliance Officer | P2 (per-tranche) |
| D-IH-81-I | Validator wiring scope + strictness — `validate_hlk.py` umbrella + `release-gate.py` + `pre_commit` profile + transition-window allowlist | System Owner | P3 |
| D-IH-81-J | Closed-initiative frozen-reference policy — closed roadmaps never retroactively migrated | PMO | P3 |
