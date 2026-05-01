---
language: en
status: active
initiative: 45-live-eval-harness
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 45 — Decision Log

Seven decisions seeded with default positions per the cursor plan; ratified by operator at greenlight (2026-05-01 04:30 CET).

## D-IH-45-A — Build on existing `akos/eval_harness`; do not adopt Inspect AI in I45

**Decision:** Stay native. Extend `akos/eval_harness` into a v2 module; do not introduce Inspect AI as the I45 entry point.

**Alternatives considered:**
- Adopt **Inspect AI** as a complementary CI runner (MIT licensed, unlimited free tier, parallel suite execution). Strong fit for Tier B; would require porting our manifest schema or running suites in parallel with our own. Rejected for I45 to avoid two-runner cognitive load during the initial unification; revisit at I47 if Tier B coverage demands it.
- Adopt **DeepEval** as a scoring backend (50+ research-backed metrics, Apache-2.0). Useful for downstream scoring but doesn't solve the unification problem; orthogonal — could be added inside `--mode rubric` if a future use-case demands the metric breadth.

**Rationale:** We already shipped `akos/eval_harness` in I10 with Tier A/B split, manifest schema, optional Langfuse reporter, and `eval_rubric_governance_suites` integration. The drift is in the *entry-point surface* (3 scripts), not the harness internals. Native unification keeps the single Cursor agent surface coherent.

**Reversibility:** High. Inspect AI can be added as a parallel runner in a later initiative without touching I45 deliverables.

---

## D-IH-45-B — Cassettes are git-canonical, not Langfuse Datasets

**Decision:** Replay cassettes live in `tests/evals/cassettes/<skill_id>/*.jsonl` and are checked into the repo. They are reviewable in PRs, signed by `last_recorded` + `recorded_by` frontmatter, and version-controlled alongside the `SKILL_REGISTRY` rows they exercise.

**Alternatives considered:**
- Store as **Langfuse Datasets** (queryable, server-side, cross-team visible). Rejected because: (a) introduces a runtime dependency for CI (Langfuse must be reachable), (b) cassette diffs are no longer in PRs, (c) external-repo consumers can't replay without Langfuse credentials.

**Rationale:** AKOS treats CSV vault as SSOT; cassettes follow the same posture (in-repo, diffable, no external runtime needed for replay). Langfuse remains the live-trace observatory; cassettes are the offline replay corpus.

**Reversibility:** Medium. Could mirror cassettes to Langfuse Datasets later as a derived view.

---

## D-IH-45-C — Tier B cadence: weekly + on-demand

**Decision:** Tier B (live LLM regression) runs once per week on a scheduled GitHub Action, plus on-demand via `gh workflow run eval-tier-b`. Model matrix is 1 cheap (e.g., Ollama-local nomic) + 1 flagship (operator-set in `.github/workflows/eval-tier-b.yml`).

**Alternatives considered:**
- **Nightly** (4× weekly cost). Justified only if regression detection latency matters more than spend; currently it doesn't.
- **Per-PR** (10×+ cost). Tightest feedback loop but cost-prohibitive at our scale; gated behind `[skip eval-tier-b]` PR-label semantics if ever adopted.

**Rationale:** Weekly cadence matches our release-gate rhythm; on-demand handles the urgent "did this PR regress?" case without baseline GitHub Action cost.

**Reversibility:** Trivial — change `cron` schedule + matrix.

---

## D-IH-45-D — Cost regression: hard-fail at >20% increase

**Decision:** When a skill's average `usd_estimate` per run regresses >20% vs the rolling 4-week baseline, CI hard-fails (blocks merge). Soft-warn between 10-20%. No-op below 10%.

**Alternatives considered:**
- **Warn-only** at all thresholds with monthly digest. Less protective; a chatty model upgrade could drift cost 50% before anyone notices.
- **Hard-fail at 10%**. Too noisy given LLM-pricing volatility (provider price changes can swing 5-15% in a single billing period).

**Rationale:** 20% threshold matches the Anthropic / OpenAI typical price-revision magnitude; lower thresholds would cry wolf on provider-side changes; higher thresholds would let actual regressions hide.

**Reversibility:** Trivial — POLICY_REGISTER row's threshold is one column.

---

## D-IH-45-E — Adversarial scope: prompt injection + brand jargon + PII (the 3 that map to existing `alerts.json`)

**Decision:** I45 P5 ships adversarial cassettes for exactly 3 vectors:
1. **Prompt injection** — probes that try to make MADEIRA execute unauthorized tools or reveal system prompt.
2. **Brand jargon leakage** — probes designed to elicit forbidden tokens from `BRAND_JARGON_AUDIT.md` §4.
3. **PII extraction** — probes that try to make MADEIRA echo back synthetic PII planted in earlier turns.

**Alternatives considered:**
- **Promptfoo's full 500-vector suite** (broader coverage). Rejected: maintenance burden, false-positive rate against our governed prompt surface, vector overlap with our 3 chosen surfaces.
- **OWASP LLM Top 10 full coverage**. Rejected for I45; some (e.g., supply-chain attacks) are infrastructure-not-prompt and belong in a separate security initiative.

**Rationale:** The 3 chosen vectors map 1:1 to existing `config/eval/alerts.json` Madeira alerts (`madeira_internal_tool_leak`, `madeira_pseudo_hlk_path_leak`, `madeira_suspect_uuid_hallucination`). Closing the loop on what we already alert on is higher-value than adding broad-but-unreviewed Promptfoo vectors.

**Reversibility:** High. Adversarial cassettes are additive; expanding to Promptfoo's full suite is just `cassettes/adversarial/promptfoo_*` files.

---

## D-IH-45-F — Skill promotion gate: enforced by `scripts/eval.py promote`, not honour

**Decision:** A skill cannot be flipped from `tenant_scope='shared'` to a tenant-specific scope without `py scripts/eval.py promote --skill <id>` returning exit 0. The script enforces 4 criteria (3 green Tier A across both model tiers, 1 green Tier B within 14 days, 1 green adversarial cassette pass, non-empty `routing_condition`).

**Alternatives considered:**
- **Documented checklist in CONTRIBUTING.md**. Rejected: relies on operator discipline; the entire I45 framing is "stop relying on operator discipline".
- **Fully automated promotion** (no operator approval). Rejected: production-impacting changes always require operator-in-the-loop per the AKOS safety posture.

**Rationale:** Promotion gate is a hybrid — automated *eligibility check*, manual *trigger*. Matches `scripts/release-gate.py` pattern from I26.

**Reversibility:** N/A (would require explicit deactivation, which is itself a governed change).

---

## D-IH-45-G — Per-skill cost ceiling lives in POLICY_REGISTER, not eval-baseline JSON

**Decision:** Cost ceilings (e.g., "SKILL-MADEIRA-LOOKUP-V1 must average ≤$0.005/run") are governed via new POLICY_REGISTER rows with `policy_class=cost_ceiling`. Eval-baseline JSON files keep accuracy baselines only.

**Alternatives considered:**
- **Co-locate cost ceiling in `config/eval-baselines/skill_*.json`**. Rejected: cost is a *policy* (governable, auditable, versioned via POLICY_REGISTER mirror) not a *baseline* (statistical).

**Rationale:** Symmetry with I32 P4 — POLICY_REGISTER is the canonical home for governed thresholds; eval-baselines is statistical reference. Adding `cost_ceiling` rows lets the FinOps + System Owner roles co-sign cost policies independently of the eval team's baseline freeze cadence.

**Reversibility:** High. Migration would be a column rename + mirror DDL.

---

## Decisions deferred (out of I45 scope, candidates for I47+)

- **D-DEFER-45-α** — Full Promptfoo suite adoption (see D-IH-45-E alternative).
- **D-DEFER-45-β** — Inspect AI as parallel runner (see D-IH-45-A alternative).
- **D-DEFER-45-γ** — Public eval leaderboard surface.
- **D-DEFER-45-δ** — Auto-promotion of skills based purely on metrics (no operator approval).
- **D-DEFER-45-ε** — Per-tenant eval scorecards (waits on Initiative 34 multi-tenancy).
