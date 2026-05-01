---
language: en
status: active
initiative: 45-live-eval-harness
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 45 — Risk Register

Risks identified during planning and at each phase boundary. Severity is **L** / **M** / **H**; likelihood is the same scale.

## Active risks

### R-45-1 — Cassettes go stale silently (M / H)
**Trigger:** A skill's underlying prompt or tool surface changes; cassettes still pass replay because they were recorded against the old behavior; we declare green CI on stale evidence.

**Mitigation:** Per-cassette frontmatter `last_recorded` field + 90-day staleness alarm in `scripts/eval.py replay` (warn at 60 days, fail at 90 unless `--allow-stale` flag passed). Mirrors the LiveBench-style awareness pattern documented in `tests/evals/README.md`.

**Rollback:** Cassettes are git-canonical → `git revert` or `git rm` recovers.

### R-45-2 — Test count temporarily drops as duplicates collapse (L / H)
**Trigger:** P1 unification merges 3 entry points into 1; some tests that exercised duplicate behavior get consolidated; pytest count drops by ~10-20.

**Mitigation:** P0 audit memo records the pre-merge test inventory; CHANGELOG documents the delta with explicit rationale; `tests/test_eval_harness_v2.py` adds new tests covering the unified surface.

**Rollback:** Phase-revert P1 commit; the 3 entry points return.

### R-45-3 — Tier B costs balloon on bad models (M / M)
**Trigger:** Operator adds a new flagship model to the matrix that has 10× the per-token cost of expectation; weekly run racks up unexpected spend.

**Mitigation:** Per-run kill switch: `MAX_TIER_B_USD` env var (default $5), enforced by `scripts/eval.py --mode rubric --tier B`. Monthly budget cap surfaced to `/metrics` endpoint; alert if MTD spend > 80% of cap.

**Rollback:** Pause the GitHub Action via `gh workflow disable eval-tier-b`.

### R-45-4 — Adversarial cassettes leak PII into git (L / H)
**Trigger:** A well-meaning recorder uses real user data (e.g., test trace from a customer session) when crafting adversarial probes.

**Mitigation:** P5 ships with explicit policy + `tests/evals/cassettes/.gitattributes` for redaction discipline; recorder script strips emails / phone / IP / customer-name patterns; CI lint check (`scripts/validate_cassette_no_pii.py`) on every commit touching `cassettes/`.

**Rollback:** `git filter-repo` (operator-side per I26 SOP-HLK_GOIPOI §6.1).

### R-45-5 — Routing changes (P3) break Madeira UX (M / H)
**Trigger:** `intent.py` refactor causes a regression in the embed+regex hybrid; an intent that used to route to MADEIRA now falls through to "ask Orchestrator".

**Mitigation:** I32 P9 canary 5 (orchestrator-fallback) is currently shape-only; P3 promotes it to hard-fail (`scripts/eval.py --mode canary --fail-on canary-5`). Pre-commit check via the unified harness blocks merge.

**Rollback:** Revert P3 commit; intent.py reverts to exemplar-only.

### R-45-6 — `tools_required` reconciliation (P3) breaks an external repo (KiRBe / hlk-erp) (M / M)
**Trigger:** Renaming a Cursor-style tool name to a gateway-style tool name in SKILL_REGISTRY is consumed by KiRBe/hlk-erp via the kirbe-sync-contract mirror.

**Mitigation:** P3 ships with a per-tool waiver column (`tools_required_waived` boolean); reconciliation is opt-in per skill, not big-bang. KiRBe/hlk-erp remain on the old names until they explicitly opt into the new ones.

**Rollback:** Set `tools_required_waived=true` for the affected skill; old name resumes.

### R-45-7 — `routing_condition` column added but no skill uses it for 4 weeks (L / L)
**Trigger:** Column is added in P3 but every existing skill defaults to empty (always-eligible); the new field becomes vestigial.

**Mitigation:** P7 promotion gate requires non-empty `routing_condition` for tenant promotion; this naturally drives adoption when I34 lands. In the interim, P3 ships 1 example (e.g., `risk_level == 'low'` for `SKILL-MADEIRA-LOOKUP-V1`).

**Rollback:** N/A (column drop is a Supabase + CSV migration).

### R-45-8 — `compliance.eval_run` mirror grows unbounded (L / M)
**Trigger:** Every CI run inserts ~5 rows (one per skill); over a year that's ~50,000 rows. Not catastrophic but unmanaged.

**Mitigation:** P4 migration includes a partial index on `(created_at)`; P8 closure adds a documented retention policy (`POLICY_REGISTER` row: keep 90 days hot, then archive — operator-side cron).

**Rollback:** Truncate table via operator SQL gate.

### R-45-9 — Promotion gate (P7) blocks a skill that should ship for ops reasons (M / L)
**Trigger:** A skill needs to land in production for an urgent customer commitment but lacks 14-day Tier B history.

**Mitigation:** `scripts/eval.py promote --override --reason "<text>"` is allowed but writes a high-visibility audit row to `compliance.eval_run` + sends a notification (operator-pasted Slack/email per I22 pattern). Override usage is reviewed at the next quarterly ops review.

**Rollback:** N/A (overrides are governed, not blocked).

### R-45-10 — Inspect AI / Promptfoo become obvious adoption candidates and we re-architect mid-stream (M / L)
**Trigger:** During P5 adversarial work, Promptfoo's vector library proves materially better than what we ship; we want to swap.

**Mitigation:** D-IH-45-A and D-IH-45-E both leave the door open; P5 cassettes are JSONL files independent of any framework, so swap-in is a renaming exercise, not a rewrite. Defer to I47.

**Rollback:** N/A.

### R-45-11 — Langfuse cost-scrape (P4) hits Langfuse rate limits (L / M)
**Trigger:** Pre-commit hook scrapes Langfuse for cost metrics; on busy CI days, Langfuse Cloud rate-limits us.

**Mitigation:** Cache scraped metrics for 5 minutes; switch to bulk API; failover to "no-cost-data" (warn but don't fail) if Langfuse is unreachable.

**Rollback:** Disable scrape via `EVAL_SCRAPE_LANGFUSE=0` env var.

### R-45-12 — Backwards-compat shims (P1) hide that consumers haven't migrated (L / M)
**Trigger:** Pre-commit / CI / external scripts keep calling `scripts/run-evals.py` and `scripts/eval_per_skill.py`; the deprecation warnings are ignored; a year later the shims stay forever.

**Mitigation:** Shims emit a deprecation warning to stderr; P8 closure adds a tracking row to a new "deprecation calendar" doc; quarterly review removes shims that are no longer hit (instrumented via shim-side counter).

**Rollback:** Restore shims by `git revert`.

## Risks closed before P0

(None — initiative just opened.)

## Cross-references

- I26 service_role rotation pattern → R-45-3 monthly budget cap (operator-side cron).
- I32 P9 canary 5 → R-45-5 (orchestrator-fallback) promotion to hard-fail.
- I22 operator-pasted SOP pattern → R-45-9 audit notification.
