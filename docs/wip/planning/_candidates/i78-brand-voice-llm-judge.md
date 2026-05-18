---
candidate_id: I78
title: Brand-voice LLM-as-judge advisory layer (Tier 2 evolution from I71 P1 strategic review)
status: promoted_active
promotion_decision_id: D-IH-78-A
authored: 2026-05-14
last_review: 2026-05-17
parent_initiative: 71 (P1 strategic review forward-charter)
priority: 6 (candidate TRIGGER posture superseded for registry activation — bias-audit / strict-mode Strand D unchanged)
language: en
planning_traceability_folder: docs/wip/planning/78-brand-voice-llm-as-judge/master-roadmap.md
---

# I78 candidate — Brand-voice LLM-as-judge advisory layer

> **Promoted active (`promoted_active` frontmatter; registry `INIT-OPENCLAW_AKOS-78` per `D-IH-78-A` 2026-05-17).** This file remains the **deep scaffold** (strands, cost math, bias mitigation, §6 telemetry). Forward-charter from the I71 P1 Pack A1 strategic review session (operator-asked: *"do I have to put a never-ending list of words here? Are things like Grammarly LLM/AI terrain? Is it worth it? Costly? Overengineered? Popular?"*). The I71 agent's web-grounded answer mapped 2026 brand-voice tooling into four working patterns and three evolution tiers; **Tier 2 is this initiative**. Registry activation no longer waits on §6 signals — engineering backlog ships per [`../78-brand-voice-llm-as-judge/master-roadmap.md`](../78-brand-voice-llm-as-judge/master-roadmap.md). §6 remains **useful telemetry** for Strand D bias-audit + strict-mode promotion timing.

## 1. Operating story

I71 P1 Pack A1 shipped a **regex-based brand-voice validator** at the 2026 SOTA architecture bar. The architecture is what every credible 2026 brand-governance source describes (oleno.ai, markup.ai, contentmarketing.ai, prosemedia.com): machine-readable canonicals → linter → CI gate → per-rule operator override → operator-owner. We live on **layers 1-3** of the canonical "five-layer system" (Inputs / Instructions / Approvals / QA / Feedback) with strict-day-1 enforcement (`D-IH-71-F`). The current chassis catches **named violations with stable lexical signature** (32 LLM tone tells, 7 tic families, MBA-deck nouns).

What it doesn't catch: **paraphrased violations**. "Delve into" is a regex hit. "Drill down into" is the same brand violation but a different lexical surface. A 2026-current writer (or worse, a 2026 LLM) will produce paraphrases the regex can't see, and the only way to keep up is to maintain an ever-expanding word list — a treadmill that the I71 agent correctly identified as unsustainable.

The 2026 industry has moved past pure regex. The pattern is **rule-based linter + semantic LLM-as-judge in series**: rules catch the named violations cheaply and deterministically; the LLM-judge catches the paraphrases and suggests on-brand rewrites. Writer.com is the proprietary version (~$18-29/seat/month, vendor lock-in). DIY with Anthropic / OpenAI APIs is the open version (~$0.001-0.01/check, no lock-in). I78 is the DIY version, designed to plug into the existing Pack A1 chassis without disturbing it.

The cohering principle: **Pack A1 lives at the deterministic floor; I78 lives one layer up as advisory semantics**. The two run in series in the release-gate. Pack A1 fails fast and loud on named violations (strict-day-1 already). I78 fires only on prose Pack A1 didn't catch, returns a structured judgment (pass/fail, severity, reasoning, suggested rewrite), and runs in **soft mode** for the first 30 days while the operator catches its biases. Promotion to strict happens at an explicit ratification gate after the bias-audit cadence completes.

## 2. Why this is a separate initiative, not a Pack A5

The I71 agent's synthesis recommended this be a separate initiative for three structural reasons:

1. **Different decision posture.** Pack A1-A4 are deterministic regex / Vale rules — the rule **is** the decision. I78 introduces **non-determinism** (LLM-judge output), bias-audit cadence, prompt versioning, and per-locale judge tuning. That's a different governance shape and warrants its own charter.
2. **Different release cadence.** Pack A1-A4 ship behind I71 P1-P5. *Drafting posture:* I78 was framed as shipping after regex "pushback" signals so the operator could name concrete paraphrase gaps. **`D-IH-78-A` (2026-05-17)** superseded that **registry** gate — execution proceeds per [`master-roadmap.md`](../78-brand-voice-llm-as-judge/master-roadmap.md); §6 signals remain useful **telemetry** for phasing P1 work and for Strand D strict-mode promotion.
3. **Different cost surface.** Pack A1-A4 are free (Python + open-source + CI compute). I78 carries a per-call API cost ($10-50/month at our volume) that warrants explicit budget ratification.

Folding I78 into I71 would either delay I71's closure or create a phase that's structurally different from its siblings. Cleaner: I78 stands on its own.

## 3. Strands

### Strand A — External research + bias audit corpus

| Topic | Why it matters | Source 2026 |
|:---|:---|:---|
| Anthropic + OpenAI judge-prompt best practices | Prompt engineering for evaluator models — position bias, verbosity bias, self-preference bias | Anthropic engineering blog "Building effective agents"; OpenAI evals cookbook 2026 |
| MLflow guidelines judges + Vale `sequence` checks | The deterministic-NLP middle layer (POS tagging, sequence checks) — included as Tier 1.5 in the architecture | Vale docs; MLflow Evaluator API |
| Bias categories in LLM-as-judge | Position, verbosity, self-preference, authority — the four documented failure modes | LMSYS chatbot arena papers; "LLM-as-a-Judge" survey papers |
| Caching strategies for judge calls | At ~50 prose surfaces × 4 locales × 10 commits/month, raw cost is ~$10/month; with content-hash caching and only-judge-changed-segments it drops to ~$2-5/month | Anthropic prompt caching docs; OpenAI batch API |
| Vendor lock-in posture | Same brand canonicals must drive every LLM provider (Anthropic / OpenAI / DeepSeek-R1 local) | I70 multi-provider doctrine; `config/openclaw.json.example` |

### Strand B — Implementation chassis

- **Module**: `akos/brand_voice_judge.py` — Pydantic models for `JudgeRequest`, `JudgeVerdict`, `JudgeBiasMitigation`, `JudgePromptVersion`. Plug into existing `akos/brand_voice_register.py` so the two share the same canonical-loading code.
- **Script**: `scripts/judge_brand_voice.py` — CLI thin layer. Reads brand canonicals as system prompt, prose under audit as user prompt, returns structured JSON. Caches by SHA256(prose + prompt-version) under `.akos-cache/judge/`.
- **Provider abstraction**: support Anthropic + OpenAI + local DeepSeek-R1 (RunPod) per `config/openclaw.json.example` provider list. Operator picks per session.
- **Soft / strict / advisory** modes via env vars (mirrors `AKOS_BRAND_VOICE_REGISTER_SOFT=1` pattern from Pack A1).
- **Release-gate integration**: new `[INFO]` row (advisory) for the first 30 days; promote to `[PASS]/[FAIL]` after ratification.

### Strand C — Bias mitigation + UAT cadence

- **30-day bias audit**: every judge call logged; operator reviews 1 sample/day and flags drift; biases catalogued in `BRAND_VOICE_JUDGE_BIAS_LOG.md` at `Marketing/Brand/canonicals/`.
- **Position bias test**: same prose, swap order — judge should not change verdict.
- **Verbosity bias test**: same content, longer surface form — judge should not over-penalize.
- **Self-preference test**: judge prose generated by Provider X with Provider Y as judge — should not converge to same provider's "voice".
- **Authority test**: judge same prose with anonymous header vs author-bylined — verdict should not depend on identity.

### Strand D — Promotion-to-strict cadence

- After 30 days of advisory-only operation: operator runs `scripts/judge_brand_voice.py --bias-audit-summary` to surface the four bias categories' false-positive / false-negative rates.
- Inline-ratify gate (D-IH-78-PROMOTE): "Promote judge to strict-mode? Per-locale? Per-surface? With which severity threshold?"
- Strict-mode lands as `[PASS]/[FAIL]` row in release-gate; soft-mode override preserved via `AKOS_BRAND_VOICE_JUDGE_SOFT=1`.

## 4. Phase scaffold

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P-1** (pre-charter) | A | External research + bias-mitigation corpus + cost math validation | — |
| **P0** | — | Charter + INITIATIVE / DECISION / OPS rows + master-roadmap; budget ratification | — |
| **P1** | B | `akos/brand_voice_judge.py` Pydantic chassis + `scripts/judge_brand_voice.py` CLI + provider abstraction (Anthropic + OpenAI + DeepSeek-R1) + content-hash caching | OPS-78-1 |
| **P2** | B | Release-gate `[INFO]` advisory row + WORKSPACE §18 cross-link + tests | OPS-78-2 |
| **P3** | C | 30-day bias audit launch: `BRAND_VOICE_JUDGE_BIAS_LOG.md` + 4 bias tests + daily sampling cadence | OPS-78-3 |
| **P4** | D | Promotion-to-strict ratification gate (D-IH-78-PROMOTE) + per-locale / per-surface tuning | OPS-78-4 |
| **P5** | — | Closing UAT + INITIATIVE_REGISTRY closure | — |

## 5. Conundrums (open at candidate stage)

1. **C-78-1 — Provider posture**: single-provider (Anthropic only? cheapest? best?) vs multi-provider rotation (load-balance + bias dilution) vs operator-picks-per-session? Default = multi-provider rotation with Anthropic as default and DeepSeek-R1 local as fallback for offline scenarios. Ratify pre-P1.
2. **C-78-2 — Cost ceiling**: hard ceiling per month ($25? $50? $100?) with circuit-breaker, OR no ceiling but real-time cost monitor in `OPERATOR_INBOX.md`? Default = $50 hard ceiling + monitor. Ratify pre-P1.
3. **C-78-3 — Caching aggressiveness**: cache by exact prose hash only (safe; high miss rate) vs cache by canonical + prompt-version + prose-segment hash (aggressive; reuses across surfaces) vs cache by paragraph-level semantic hash (most aggressive; needs embeddings). Default = canonical + prompt-version + prose-segment hash. Ratify pre-P1.
4. **C-78-4 — Bias-audit promotion threshold**: false-positive rate <5% AND false-negative rate <10% AND no single-bias-category >2x baseline → promote? Or operator-judgment per-locale? Default = quantitative thresholds + operator-judgment override. Ratify pre-P3.
5. **C-78-5 — Locale fairness**: judge tuned on EN; FR/ES may have different bias profiles. Run separate bias audit per locale, OR single audit with locale dimension? Default = separate audit per locale (3 audits, 30 days each, can run in parallel). Ratify pre-P3.
6. **C-78-6 — Judge-prompt versioning**: when the judge prompt changes, do all cached verdicts invalidate (safe; expensive) OR only verdicts touching the changed canonical (cheaper; risk of stale judgments)? Default = full invalidation on judge-prompt version bump; rely on aggressive caching to absorb the re-run cost. Ratify pre-P1.
7. **C-78-7 — Inline-with-Pack-A1 vs sibling**: judge runs after Pack A1 only on prose Pack A1 passed (cheap; misses cases where regex's verdict was wrong) OR on every prose surface (expensive; redundant on Pack-A1-failed surfaces). Default = after Pack A1 only; expose `--judge-all-surfaces` flag for spot-audit. Ratify pre-P1.

## 6. Spin-out trigger conditions

> **Governance supersession:** Operator minted **`INIT-OPENCLAW_AKOS-78`** + **`D-IH-78-A`** (2026-05-17), activating the initiative **before** §6 signals fired. The bullets below remain **operational telemetry** — especially for bias-audit timing and P1 scope prioritisation — but they are **no longer** the INITIATIVE_REGISTRY promotion gate.

*Historical drafting posture:* this scaffold **did not** promote to active on a calendar trigger alone; it was framed as promoting when **the regex list visibly pushes back** — when the operator can articulate concrete paraphrase patterns the regex misses. Concrete signals:

- Operator adds a regex to `register-pack.yml` and notes "this took >20 min to think of all the variations" (the I71 agent's stated tipping point).
- A customer-visible artifact ships with a paraphrase that the regex didn't catch but the operator immediately recognizes as off-voice.
- Pack A2 (Gantt confidence) or Pack A3 (multilingual locale-suffix) hits the same regex-cardinality problem during their own ratification.
- I77 (Impeccable Brand-Bridge Refresh) closes and produces a per-bridge brand-voice expectation that the regex chassis can't represent without explosion of rule cardinality.

When **≥2** of these signals fire, prioritise P1 judge coverage toward the surfaced paraphrase classes and accelerate Strand C bias-audit prep — the regex chassis remains the deterministic SSOT **floor** either way.

## 7. Risk register (top 5)

| Risk | Severity | Mitigation |
|:---|:---:|:---|
| LLM-judge bias drifts the brand voice toward generic corporate style | Critical | Strand C 30-day bias audit; promotion-to-strict gates on quantitative thresholds; per-locale audit; operator-editable bias log. |
| Vendor lock-in via single provider | High | C-78-1 default = multi-provider rotation; akos/model_catalog.py SSOT for provider list; never hardcode a provider in judge prompt. |
| Cost spiral (judge fires on every commit, every surface) | High | C-78-2 default = $50 hard ceiling + circuit-breaker; C-78-3 aggressive caching; C-78-7 default = run after Pack A1 only. |
| Judge-prompt versioning drifts canonicals | Medium | C-78-6 default = full invalidation on prompt bump; canonical edits trigger judge re-run automatically; review-stamp dimension (I71 P4) tracks last-judge-version-at-review. |
| Premature promotion-to-strict erodes operator trust (false-positives block legitimate prose) | High | C-78-4 quantitative thresholds + 30-day audit; operator-judgment override; per-locale fairness gate; emergency soft-mode env preserved. |

## 8. Out of scope (this candidate; punt to follow-on initiatives)

- **Tier 3 — Writer-facing inline UX (Cursor extension / VS Code plug-in)**: parked behind a team-scale trigger (≥3 marketing writers concurrently). Today the workflow is operator + agent; CLI + CI gate is the right surface. When (if) Holistika has a content team, mint a separate initiative for inline UX. The judge backend from I78 P1 is reusable as-is.
- **Adoption of Acrolinx, Writer.com, or Grammarly Business**: explicitly rejected per I71 agent's strategic synthesis. Vendor lock-in (their rules in their system) breaks AKOS SSOT contract. Useful as drafting companions for a writer; bad as enforcement layers for the brand. Re-revisit only if the operator's posture on lock-in changes.
- **Tier 1 (Vale sibling integration)**: folded into I71 P2 scope, not I78. I71 P2 ships Vale alongside the regex chassis as a complementary deterministic-NLP layer (free, ~1 day).
- **Numeric brand-voice score as gate**: nice-to-have, not load-bearing. If operator wants per-surface confidence scores, mint a sibling I79 candidate for "Brand-voice score dashboard".

## 9. Cross-references

- **I71 P1 strategic review session** (2026-05-14): the conversation that generated this candidate. The I71 agent's 4-pattern × 3-tier synthesis is the design source. Web sources cited: Acrolinx, Writer.com, Grammarly Business, Vale (open-source), MLflow guidelines judges, Anthropic/OpenAI engineering blogs, oleno.ai, markup.ai, contentmarketing.ai, prosemedia.com.
- [`scripts/validate_brand_voice_register.py`](../../../../scripts/validate_brand_voice_register.py) — the regex chassis I78 plugs into.
- [`akos/brand_voice_register.py`](../../../../akos/brand_voice_register.py) — the Pydantic chassis I78 reuses for canonical loading.
- [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/register-pack.yml`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/register-pack.yml) — the per-rule operator override surface; I78 introduces a sibling `judge-pack.yml` for judge-side overrides (per-bias-category opt-out, per-locale tuning, per-surface scope).
- [`D-IH-71-F`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — strict-day-1 enforcement precedent for Pack A1; I78 deliberately does NOT inherit (advisory-first, then promote on quantitative gate).
- I71 master roadmap [Strand A Pack A1 anchor](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) — the chassis I78 plugs into.
- I71 master roadmap [P2 Tier 1 Vale fold-in](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) — the deterministic-NLP layer that runs alongside I78 (between Pack A1 regex and I78 LLM-judge).
- I77 (Impeccable Brand-Bridge Refresh) — concurrent brand-DNA initiative; I78 cross-runs on Impeccable bridge prose at I77 P1 ship.
- [`config/openclaw.json.example`](../../../../config/openclaw.json.example) — multi-provider SSOT (Anthropic + OpenAI + DeepSeek-R1 local + Ollama).
- [`akos/model_catalog.py`](../../../../akos/model_catalog.py) — provider catalog for Strand B provider abstraction.
- [`docs/wip/planning/_templates/initiative-planning-prompts.md`](../_templates/initiative-planning-prompts.md) — the right Discovery + Plan-Author entry point when I78 promotes.
- [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — the discipline I78's promotion-to-strict gates honor.

## 10. Operator notes

The I71 agent's web-grounded read in plain terms (verbatim transcription, edited for length): *"What we shipped is the rule-based half of the current best practice. The semantic half is exactly an evolution of this product, not a replacement. The architecture we just built is the load-bearing half. The other half plugs in next to it, not on top of it."* That framing is the entire reason I78 is a sibling initiative, not a Pack A5.

Registry activation already landed via **`D-IH-78-A`**. For **P1 execution**, the entry point remains [`docs/wip/planning/78-brand-voice-llm-as-judge/master-roadmap.md`](../78-brand-voice-llm-as-judge/master-roadmap.md) plus `docs/wip/planning/_templates/initiative-planning-prompts.md` Prompt 1 (Discovery) if you want a fresh chat — paste §6 signal evidence when available so the judge corpus targets observed paraphrase gaps first.
