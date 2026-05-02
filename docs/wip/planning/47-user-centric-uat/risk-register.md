---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 47 — Risk Register

14 risks identified during planning (8 original + 6 from RICE-driven scope expansion 2026-05-02). Severity is L / M / H; likelihood same scale.

## Active risks

### R-47-1 — 350 scenarios = ballooning maintenance (M / H)
**Trigger:** Scenarios drift; nobody updates them; the library becomes a graveyard of stale tests.

**Mitigation:** P0 calibration framework re-runs every 90 days; auto-stale alarm at 90d (mirrors I45 P2 cassette staleness); per-tier scenario count cap; persona-id can be deprecated en masse if the persona retires from PERSONA_REGISTRY (cascade via FK).

**Rollback:** Mark scenarios `lifecycle_status=deprecated` in CSV; validator skips replay; cassettes stay for forensic reference.

### R-47-2 — Difficulty calibration is subjective (M / M)
**Trigger:** Operator argues "scenario X is hard" but meta-eval classifies it as moderate.

**Mitigation:** Meta-eval (`scripts/calibrate_scenarios.py`) is deterministic: every scenario runs through current AKOS at P0 + P10 + P15; difficulty class auto-assigned from observed pass/fail/escalate. Operator override is allowed via CSV edit but logged in decision-log.

**Rollback:** N/A.

### R-47-3 — Tier B cost explosion with 16-persona matrix (M / H)
**Trigger:** Weekly run × 16 personas × 2 model tiers × 4 scenario classes × 3 judge axes = 384 cells; each cell could cost ~$0.50 if unbounded; ~$200/run unmitigated.

**Mitigation:** Per-persona spend cap (`MAX_PERSONA_USD` env; default $5/persona); Tier-3 personas excluded from default weekly run (workflow_dispatch only); judge cost-cap per scenario (`--judge-cost-cap` default $0.01); cassette replay (no live LLM) is the default mode.

**Rollback:** Pause workflow via `gh workflow disable eval-tier-b`.

### R-47-4 — Persona impersonation scenarios accidentally legitimize attack vectors (L / H)
**Trigger:** A real-looking adversarial probe gets externalized (e.g., quoted in a deck) and people think "Holistika has a known impersonation vulnerability".

**Mitigation:** All adversarial persona cassettes are SYNTHETIC; no real founder/customer/advisor identities; `lint_cassette_pii.py` extension catches real names + extends to "real-looking persona profile" detection (e.g., a probe naming a real Spanish investor).

**Rollback:** `git filter-repo` (operator-side per I26 SOP).

### R-47-5 — Cross-axis stress reveals huge classification gaps (L / H — but this IS the point)
**Trigger:** P10 calibration reports 70% of cross-axis scenarios fail (vs target 40% hard).

**Mitigation:** This is the EXPECTED outcome of building a challenging test set. Per D-IH-47-C target: 40% hard scenarios are "fail-on-first-naive-run" by design. Failing cross-axis tests reveals where the 6-axis routing needs investment in I48+. P15 closure will INTENTIONALLY surface these as a "next initiative scope" feed.

**Rollback:** N/A.

### R-47-6 — Recovery scenarios mock the wrong failure mode (L / M)
**Trigger:** Our `NEO4J_URI=invalid` mock doesn't match how Aura actually fails (e.g., real Aura times out vs immediately rejects).

**Mitigation:** P9 specifies the 6 mock paths explicitly; each mock validated in P15 by manually breaking the dependency and re-running. Plus the 1 opt-in real-chaos scenario per D-IH-47-L catches the divergence class explicitly.

**Rollback:** Synthetic mocks are CSV-driven; edit CSV to align with observed failure mode.

### R-47-7 — Tech debt P13 surfaces deeper bugs than 4 items (M / M)
**Trigger:** Fixing `sync_hlk_neo4j.py` 6-dim writes reveals that the projection model has a bug in one of the 6 axis-6 build functions (e.g., `build_persona_graph` produces malformed nodes).

**Mitigation:** Each P13 item gets isolated commit + report; if a 5th item surfaces, it gets evidence-matrix row + decision: include now (extend P13) or defer to I48. Operator chooses.

**Rollback:** Per-item commits revertable.

### R-47-8 — Agent memory trigger watcher fires false positive (L / M)
**Trigger:** I46 P4 ADR Trigger 2 (conversation depth ≥10% MADEIRA traces with skills_invoked ≥4 in 7d window) misfires because Madeira UAT runs spike skills_invoked counts artificially.

**Mitigation:** Operator can dismiss with audit-trailed reason (R-45-9 pattern); 7-day rolling window prevents flap; UAT runs auto-tagged so they're excluded from the rolling window.

**Rollback:** Tune trigger thresholds in I46 P4 ADR (operator decision-log update).

### R-47-9 (NEW from RICE A) — Persona overlay pushes MADEIRA_PROMPT past bootstrapMaxChars (M / H)
**Trigger:** A Tier-1 persona overlay grows past ~500 chars; `MADEIRA_PROMPT.standard.md` exceeds 20000 chars; `assemble-prompts.py` warns; `tests/validate_multimodel.py` fails (the I46 P7 lesson recurring).

**Mitigation:** P11 includes per-persona length test (`tests/test_persona_overlay_length.py` — NEW); CI test asserts `MADEIRA_PROMPT.standard.md` stays ≤19500 chars under any persona overlay (500-char headroom buffer); operator-authored overlay fragments must stay ≤500 chars (validator enforces).

**Rollback:** Trim the offending overlay; cassette regression remains green because per-persona tests anchor the contract.

### R-47-10 (NEW from RICE B) — LLM-judge sycophancy / drift between judge versions (M / M)
**Trigger:** Judge model (e.g., gpt-4o-mini) gets quietly upgraded by provider; judge_scores drift ±1 point on identical prompts; Tier B regression alerts spike with no real change.

**Mitigation:** Judge model is operator-pinned per D-IH-47-J (model_id captured in cassette + scorecard); ≥2 judge runs per scenario for variance estimation (operator-set via `--judge-runs`); baseline `judge_scores` frozen at P12 close; drift > ±1 point triggers re-baseline workflow (manual; logged).

**Rollback:** Restore prior judge model_id; replay cassettes.

### R-47-11 (NEW from RICE B) — LLM-judge cost runaway (L / M)
**Trigger:** A Tier B run with persona matrix triggers ~350 scenarios × 3 judge axes × 2 judge runs = ~2100 judge invocations; at $0.01/invocation = ~$21/run; weekly = ~$84/month.

**Mitigation:** Cost-cap `--judge-cost-cap` per scenario (default $0.01); rolls into I45 P4 per-skill cost accounting; Tier B per-persona spend cap covers it; Tier-3 personas excluded from default weekly run (~30% reduction).

**Rollback:** Lower cap; reduce judge runs to 1; exclude judge from default scorecard (`--no-judge`).

### R-47-12 (NEW from RICE C) — tenant_id NULL handling breaks downstream queries (L / M)
**Trigger:** Existing query `SELECT * FROM compliance.persona_scenario_registry_mirror WHERE persona_id='X'` returns NULL `tenant_id` rows; downstream code assumed string and crashes on NoneType.

**Mitigation:** Validator + mirror partial index on `WHERE tenant_id IS NOT NULL`; existing queries unchanged (don't filter on tenant_id); new tenant-aware queries opt in explicitly; Python akos contract default-handles NULL via `.get('tenant_id')` not `['tenant_id']`.

**Rollback:** Drop column (Supabase + CSV migration).

### R-47-13 (NEW from RICE D) — Real-chaos scenario damages live Aura instance (H / L)
**Trigger:** Operator runs `AKOS_REAL_CHAOS_OK=1` with `NEO4J_URI` pointing at the real MasterData instance instead of throwaway test instance; password rotation breaks live operations.

**Mitigation:** `AKOS_REAL_CHAOS_OK=1` env-gate + scenario uses dedicated throwaway test instance (NOT MasterData); operator confirms the test instance ID via interactive prompt before run; rotation includes restore-step with idempotent retry; scenario refuses to run if `NEO4J_URI` matches MasterData host.

**Rollback:** Restore-step rotates back to original credential; if restore fails, operator-side recovery via Aura console.

### R-47-14 (NEW from RICE A) — Persona-conditioned prompts diverge from MADEIRA_BASE doctrine (M / M)
**Trigger:** A persona overlay overrides a MADEIRA_BASE invariant (e.g., escalation path; citation rule; allowed tools list); response drifts from governance contract.

**Mitigation:** `assemble-prompts.py` test asserts every assembled MADEIRA prompt still contains the MADEIRA_BASE invariants (citation rule, escalation paths, allowed tools list); persona overlay can ADD context, not OVERRIDE invariants. Test enforces this structurally (overlay prepended/appended; never overwrites base body).

**Rollback:** Edit overlay; CI test catches the override on next run.

## Risks closed before P0

(None — initiative just opened.)

## Cross-references

- I26 service_role rotation pattern → R-47-3 cost ceiling enforcement model
- I32 P9 canary 5 → R-47-5 (failing-by-design) is the I47 equivalent
- I45 P5 R-45-4 (PII leak) → R-47-4 extends with "real-looking persona profile" lint
- I46 P4 ADR triggers → R-47-8 false positive scope
- I46 P7 OVERLAY shrink fix → R-47-9 same root cause class
