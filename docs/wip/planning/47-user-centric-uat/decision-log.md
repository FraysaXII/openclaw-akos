---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 47 — Decision Log

12 decisions seeded with default positions per the cursor plan (8 original + 4 from RICE-driven scope expansion). User pre-ratified at greenlight (2026-05-02 03:25 CET).

## D-IH-47-A — PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT

**Decision:** New canonical CSV at `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv`. Cassettes are mirrored/derived from CSV rows. Validator enforces FK to PERSONA_REGISTRY.csv + SKILL_REGISTRY.csv.

**Alternatives considered:**
- Cassettes-only (no governance CSV; faster but loses queryable surface; cannot run `WHERE persona_id=X AND difficulty_class=hard` queries)

**Rationale:** Symmetry with I32 P2 SKILL_REGISTRY pattern. DAMA discipline. Enables Supabase-side analytics on scenario coverage per persona/skill/difficulty.

**Reversibility:** Low (DAMA conventions don't reverse cleanly).

---

## D-IH-47-B — Tiered persona coverage (4 deep / 8 medium / 4 light)

**Decision:** Tier-1 (4 personas × 25 scenarios = 100), Tier-2 (8 × 10 = 80), Tier-3 (4 × 5 = 20). Plus 25 operator scenarios = 225 persona-scenarios. Plus ~100 cross-cutting (cross-axis, adversarial, benchmark, recovery) = ~350 total.

**Tier-1 personas** (highest strategic value): `PERSONA-INVESTOR-COLD`, `PERSONA-INVESTOR-WARM`, `PERSONA-ADVISOR-REFERRAL`, `PERSONA-CUSTOMER-KIRBE-PROSPECT`.

**Tier-2 personas**: `PERSONA-ADVISOR-COLD`, `PERSONA-PARTNER-JOINT-EQUITY`, `PERSONA-PARTNER-SUBCONTRACT`, `PERSONA-TALENT-INBOUND`, `PERSONA-VENDOR-OUTBOUND`, `PERSONA-VENDOR-INBOUND`, `PERSONA-EXISTING-CUSTOMER`, `PERSONA-EXISTING-PARTNER`.

**Tier-3 personas** (long-tail; lighter coverage): `PERSONA-PRESS`, `PERSONA-IDEA-PROPOSER`, `PERSONA-RANDOM-INBOUND`, `PERSONA-CUSTOMER-SERVICE-PROSPECT`.

**Alternatives considered:**
- Flat 15 each (240 total; simpler but ignores strategic weight; under-tests investor-cold which is highest-value strategic)
- All-Tier-1 (16 × 25 = 400; too heavy)

**Rationale:** Cost-aware coverage. Tier-1 personas drive most measurement value (investor + advisor + customer prospects = sales-relevant); Tier-3 personas are coverage completeness with low signal.

**Reversibility:** High (per-persona scenario count is just a CSV row count).

---

## D-IH-47-C — Difficulty calibration target: 40/40/10/10

**Decision:** Target distribution measured by P10 meta-eval:
- **40% Hard** — fails first naive prompt run; needs grounding/multi-step retrieval/persona context
- **40% Moderate** — passes after persona context applied
- **10% Trivial** — passes naive first run (sanity floor; ensures we still test happy path)
- **10% Impossible-by-design** — system MUST refuse/escalate (e.g., "what's the weather in Madrid")

Meta-eval is deterministic: every scenario runs through current AKOS at P0 + P10 + P15; difficulty class auto-assigned from observed pass/fail/escalate behavior. Operator overrides via CSV edit if classification disagrees.

**Alternatives considered:**
- 60% Hard / 30% Moderate / 10% Impossible (very aggressive; risks false negatives where system "fails" on subjective grounding)
- 30% Hard / 50% Moderate / 20% Trivial (conservative; less informative)

**Rationale:** 40/40/10/10 mirrors HELM-style benchmark distribution. Hard scenarios are where the value is; trivial floor ensures we still catch happy-path regressions; impossible-by-design tests refusal discipline.

**Reversibility:** Trivial — change targets in P0 calibration framework + re-classify.

---

## D-IH-47-D — Benchmark adapters: 3 LIGHT adapters

**Decision:** 3 benchmark-pattern adapters totalling ~30 scenarios:
1. **LongMemEval-LIGHT** (10 scenarios): tests whether system correctly REFUSES retrospective queries (since use-case C agent memory is deferred per I46 P4 ADR). Validates "what did we tell you 6 weeks ago" routes to "we don't have memory yet; here's the deferral context".
2. **MASEval-LIGHT** (10 scenarios): whole-MAS scenarios where the test asserts the FULL agent chain (intent → router → skill → response) not just per-component.
3. **Promptfoo curated subset** (10 scenarios): from Promptfoo's vector library, curated for our threat surface (excludes vectors that don't apply to read-only governance assistant).

**Alternatives considered:**
- Just MASEval (lighter; misses memory-trigger validation)
- All 3 + HELM-adapted (heavier; HELM is broad-spectrum; not aligned with our agent shape)
- Adopt actual public benchmark scoring (rejected per RICE — low value vs effort; defer to I49)

**Rationale:** Adapt-pattern not adopt-leaderboard keeps us internal-scored and lightweight while gaining benchmark discipline.

**Reversibility:** High (each adapter is its own ~10 cassettes).

---

## D-IH-47-E — Recovery scenarios via synthetic mocks (default)

**Decision:** Recovery scenarios (P9) use synthetic mocks (env vars + timestamp injection) by default. The 6 base recovery scenarios all use safe mocks. Plus 1 opt-in real-chaos scenario per D-IH-47-L (separate decision).

**Alternatives considered:**
- All-synthetic (no real chaos; misses real-vs-mocked-API divergence)
- All-real chaos (operator-side risk; could affect real Aura operations)

**Rationale:** Synthetic mocks are cheap, repeatable, CI-safe. Real-chaos catches the kind of bug the I46 password-truncation lesson illustrates (where the mock doesn't match real behavior). Hybrid is the safe compromise.

**Reversibility:** Trivial.

---

## D-IH-47-F — Per-persona scorecard wiring on `ScoreRow`

**Decision:** Extend `ScoreRow` (in `akos/eval_harness/v2.py`) with `persona_id`, `difficulty_class`, `scenario_class`, `judge_scores: dict` fields. Aggregator emits per-persona section in markdown scorecard. New `--persona <id>` and `--calibrate` and `--difficulty <class>` CLI flags.

**Alternatives considered:**
- Separate `PersonaScorecard` dataclass (purer separation; more boilerplate; harder to write meta-eval against)

**Rationale:** Lower friction; existing ScoreRow consumers don't break (new fields default to None); meta-eval aggregator can sort by any new field.

**Reversibility:** Medium (touches public ScoreRow contract).

---

## D-IH-47-G — Tech debt scope: 4 items in P13 (originally P11)

**Decision:** All 4 items from I46 UAT cleaned up in P13 (renumbered after RICE expansion):
1. `scripts/sync_hlk_neo4j.py` 6-dimension write extension (drift canary caught it only writes 4 of 10)
2. `scripts/sync_compliance_mirrors_from_csv.py` boolean emit fix (`true`/`false` not `''`)
3. Agent memory trigger watcher (cron-ready script per I46 P4 ADR triggers)
4. `compliance.eval_run` live writes wiring (DDL exists from I45 P4; data flow now lands)

**Alternatives considered:**
- Split off `eval_run` writes to I48 (lighter P13; defers cross-coupling)
- Defer all 4 to I48 (separate cleanup initiative; cleaner I47 closure)

**Rationale:** Single-initiative closure pattern matches operator preference (greenlight question 2). Tech debt is from the I46 UAT cycle; I47 is the I47-UAT cycle; cleanest to close them together.

**Reversibility:** N/A.

---

## D-IH-47-H — Multi-persona run cadence: extend Tier B (P14)

**Decision:** Extend the existing `.github/workflows/eval-tier-b.yml` with a `persona` matrix dimension. Each weekly run executes the full scenario library per persona × model_tier × scenario_class × judge_axis (4-D matrix per P12). Per-persona spend cap enforced. Tier-3 personas excluded from default weekly run (only on-demand via `workflow_dispatch`).

**Alternatives considered:**
- New `eval-tier-c.yml` for persona runs (cleaner separation; more YAML to maintain; redundant secrets)

**Rationale:** Single workflow keeps secrets management simple. Matrix dimensions are the GH Actions idiom.

**Reversibility:** Trivial.

---

## D-IH-47-I (NEW from RICE A) — Persona-conditioned MADEIRA prompts

**Decision:** Build a persona-aware prompt overlay layer:
- New canonical template: `prompts/overlays/PERSONA_OVERLAY.md` (the framework)
- Per-persona override fragments: `prompts/personas/<persona_id>/MADEIRA_HINTS.md` (operator-authored short hints; ≤500 chars each)
- Lazy-loaded by `scripts/assemble-prompts.py` when called with new `--persona <id>` flag
- Soft-fails to base prompt if persona overlay missing (back-compat for unconditioned calls)
- New regression test asserts `MADEIRA_PROMPT.standard.md` stays ≤19500 chars under any persona overlay (per the I46 P7 bootstrapMaxChars lesson)

**Alternatives considered:**
- Bake all persona awareness into `MADEIRA_BASE.md` directly (simpler; risks bootstrapMaxChars overflow per the I46 P7 lesson)
- Per-persona FULL prompt files (heavy; loses MADEIRA_BASE invariants)

**Rationale (RICE A: Reach High × Impact High × Confidence Med-High / Effort 1.5-2w = HIGH):** Without persona-conditioning, scenarios test only routing (correct route picked) not response quality (correct register/citation/persona-fit). User mandate. Effort 1.5-2 weeks; pays off across all subsequent persona scenarios.

**Reversibility:** High (overlay is opt-in; remove `--persona` flag and base prompt is unchanged).

---

## D-IH-47-J (NEW from RICE B) — Live LLM-graded eval (3-axis judge)

**Decision:** New `akos/eval_harness/judge.py` module with `score_response(response, scenario, persona) → JudgeResult`. 3-axis judge rubric per scenario response:
1. **Brand-voice fidelity** — judge model scores 1-5 on adherence to BRAND_VOICE_FOUNDATION + BRAND_JARGON_AUDIT
2. **Citation discipline** — every claim cites a canonical path (`docs/references/hlk/...`); 1-5
3. **Persona-fit** — response register matches persona's `typical_languages` + `typical_distance_band` from PERSONA_REGISTRY; 1-5

`ScoreRow.judge_scores: dict[str, int]` (3 keys). Cost-capped at $0.01/scenario by default (operator override via `--judge-cost-cap`). Judge model = cheaper of Tier B matrix (operator-pinned). 3 new POLICY_REGISTER rows (`POL-EVAL-JUDGE-THRESHOLD-{BRAND_VOICE,CITATION,PERSONA_FIT}`) set the PASS threshold per axis (default ≥4/5).

**Alternatives considered:**
- Just brand-voice axis (cheaper; less coverage)
- Multi-judge consensus (heavier; defer to I49)
- No LLM-judge (rejected per RICE — substring rubric misses tone/register/citation discipline)

**Rationale (RICE B: Reach High × Impact Very-High × Confidence Med / Effort 1.5w = HIGH):** Substring rubric (I45 P1) catches `forbidden` token leakage but misses paraphrased jargon, missing citations, persona-register mismatch. LLM-judge captures these. Worth the cost given it gates Tier B promotion decisions.

**Reversibility:** Medium (judge_scores are additive; existing scorecard consumers see them as optional).

---

## D-IH-47-K (NEW from RICE C) — Tenant_id joint-axis prep

**Decision:** Add `tenant_id` column (NULL default; back-compat) to PERSONA_SCENARIO_REGISTRY.csv at P1 schema-design time. Mirror gets `(persona_id, tenant_id)` composite index. Validator accepts NULL + future tenant string.

**Alternatives considered:**
- Defer entirely until I34 multi-tenant lands (~3w retrofit risk; persona × scenario × tenant cross-product breaks if schema not designed for it from day 1)

**Rationale (RICE C: Reach High × Impact High × Confidence High / Effort 0.25w = VERY HIGH):** 0.25w now vs ~3w retrofit later. The schema discipline (NULL = "shared scenario applies to all tenants"; non-NULL = "tenant-scoped scenario") is well-understood. Massive future-proofing for tiny effort.

**Reversibility:** Trivial (drop column).

---

## D-IH-47-L (NEW from RICE D) — Hybrid chaos: synthetic + 1 opt-in real

**Decision:** P9 ships 6 synthetic-mock recovery scenarios + 1 OPTIONAL real-chaos scenario gated behind `AKOS_REAL_CHAOS_OK=1` env (default OFF). Real-chaos scenario:
- Operates on a throwaway test instance (NOT MasterData)
- Rotates NEO4J_PASSWORD on the test instance → runs drift canary → asserts detection → restores credential
- Operator must confirm test instance ID before run (interactive prompt)
- Never runs in default CI; operator-side opt-in only

**Alternatives considered:**
- All-synthetic (cheaper; doesn't catch real-vs-mocked-API divergence — the lesson from I46 password-truncation)
- All-real chaos (operator-side risk; could affect real operations)

**Rationale (RICE D: Reach Med × Impact Med × Confidence Med-Low / Effort 1w + ongoing risk = MED):** Hybrid keeps default CI safe and cheap; the 1 opt-in real-chaos catches the rare-but-painful class of bug where the mock and real API diverge. Throwaway test instance + interactive confirmation cap blast radius.

**Reversibility:** High (just don't run with `AKOS_REAL_CHAOS_OK=1`).

---

## Decisions deferred (out of I47 scope, candidates for I48+)

- **D-DEFER-47-α** — Public benchmark leaderboard submission (LongMemEval / MASEval). RICE-skipped: low value vs effort; revisit at I49.
- **D-DEFER-47-β** — Inspect AI / DeepEval adoption. D-IH-45-A holds; revisit at I49.
- **D-DEFER-47-γ** — Multi-judge consensus (≥3 judges per scenario for variance reduction). Single judge in P12; multi-judge at I49 if drift surfaces.
- **D-DEFER-47-δ** — Persona-specific UI for non-operator agents. Product team scope; not in I47.
- **D-DEFER-47-ε** — Multi-tenant scenario forking (per-tenant cassette fan-out). Schema prepped (D-IH-47-K); runtime lands in I34.
