---
language: en
status: closed
initiative: 47-user-centric-uat
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 47 — User-centric UAT modernisation

**Folder:** `docs/wip/planning/47-user-centric-uat/`
**Status:** Closed (2026-05-02; all 16 phases shipped; 134 new tests; 326 scenarios; UAT report at [`reports/uat-i47-user-centric-uat-2026-05-02.md`](reports/uat-i47-user-centric-uat-2026-05-02.md))
**Authoritative Cursor plan:** `~/.cursor/plans/i47_user-centric_uat_a51d490f.plan.md`
**Predecessor:** [Initiative 45 — Live Eval Harness Modernisation](../45-live-eval-harness/master-roadmap.md) (closed 2026-05-01) and [Initiative 46 — Neo4j Strategic Posture](../46-neo4j-strategic-posture/master-roadmap.md) (closed 2026-05-01).
**Sister initiative scope (RICE-expanded 2026-05-02):** absorbs 4 originally-out-of-scope items into in-scope.

## Outcome

Build a persona-driven UAT scenario library that exercises the I45/I46 eval harness against challenging real-world queries (operator + 15 external personas from PERSONA_REGISTRY), with calibrated difficulty distribution (40% hard / 40% moderate / 10% trivial / 10% impossible-by-design), per-persona scorecard, persona-conditioned MADEIRA prompts (NEW per RICE A; user-mandated), LLM-as-judge 3-axis scoring (NEW per RICE B), tenant_id joint-axis prep (NEW per RICE C), hybrid synthetic+opt-in-real chaos scenarios (NEW per RICE D), and clean up the 4 real tech-debt items the I46 UAT surfaced.

The phrase that triggered this initiative: *"make sure the next UAT is thorough and user centric. imagine myself using this system, then imagine another persona. Be sure the testings are not passing easy to predict scenarios, but actually challenging scenarios, like benchmarkers do, tailor other scenario to us"* (operator, 2026-05-02 02:53 CET).

## Why now

- **The I46 UAT proved the eval harness works** but exposed a structural shortfall: every cassette assumes operator voice/intent/vocabulary. We have **zero scenarios** for what an investor-cold persona experiences when DM-ing Holistika, what an ENISA advisor sees, what a new hire sees on first MADEIRA contact.
- **Real bugs surfaced** by the I46 UAT (drift canary caught only-4-of-10-dimensions sync bug; sync emits empty string for boolean) deserve a tracked closure cycle, not loose follow-ups.
- **GraphRAG conditional ship (I46 P5)** depends on persona-aware routing — without per-persona scenarios there's no way to validate `retrieval_mode=graph_rag` doesn't degrade the operator-shaped flow.
- **Initiative 34 (multi-tenant) prep** wants persona+tenant joint-axis exposed in PERSONA_SCENARIO_REGISTRY now (0.25w) vs ~3w retrofit later.
- **2026 benchmark discipline** (LongMemEval, MASEval, Promptfoo, HELM-style calibration) is increasingly the standard for "your evals are credible". Our current substring rubric + canary-2 thresholds are minimum viable; this initiative lifts to benchmark-credible.

## Scope decisions

| In scope (post-RICE-expansion 2026-05-02) | Out of scope |
|:---|:---|
| All 16 PERSONA_REGISTRY archetypes (tiered: 4 deep / 8 medium / 4 light) | Building actual product UI surfaces |
| ~350 scenarios total (~250 persona + ~100 cross-cutting) | Public benchmark scoring (LongMemEval public leaderboard); adapt patterns instead |
| Calibrated difficulty distribution (target 40/40/10/10 within ±5%) | Persona-specific UI per agent (operator console stays generic) |
| Per-persona scorecard via `ScoreRow.persona_id` | I34 multi-tenant runtime (only the persona+tenant joint-axis schema is prepped here) |
| Adversarial persona scenarios (impersonation; indirect injection; tier-jumping; cross-persona leakage) | Inspect AI / DeepEval adoption (D-IH-45-A holds) |
| Recovery scenarios (synthetic by default + 1 opt-in real-chaos per D-IH-47-L) | New CI runner (existing eval-tier-b.yml matrix dim-extension is sufficient) |
| Tech debt cleanup (4 items from I46 UAT) | |
| Multi-persona Tier B matrix on existing GH Action | |
| Difficulty-calibration meta-eval | |
| Persona-conditioned MADEIRA prompts (NEW per RICE A; user-mandated) | |
| Live LLM-graded eval / 3-axis judge (NEW per RICE B) | |
| Tenant_id joint-axis prep (NEW per RICE C; 0.25w vs 3w retrofit) | |
| Hybrid chaos: synthetic default + 1 opt-in real-chaos (NEW per RICE D) | |

## Asset classification (per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Paths | Rule |
|:------|:------|:-----|
| **New canonical (planning)** | `docs/wip/planning/47-user-centric-uat/{master-roadmap,decision-log,asset-classification,evidence-matrix,risk-register,scenario-taxonomy}.md` + `reports/` | 6 standard artifacts (5 + scenario-taxonomy) |
| **New canonical (registry)** | `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv` (P1) | The DAMA-canonical scenario library; mirrored to Supabase |
| **New canonical (vault)** | `prompts/overlays/PERSONA_OVERLAY.md` (P11; D-IH-47-I) | Template for persona-conditioned MADEIRA prompt fragments |
| **New canonical (per-persona overlays)** | `prompts/personas/<persona_id>/MADEIRA_HINTS.md` (P11; ≥4 Tier-1 personas at close) | Lazy-loaded fragments; soft-fail to base prompt if missing |
| **New canonical (POLICY rows)** | `POL-EVAL-JUDGE-THRESHOLD-{BRAND_VOICE,CITATION,PERSONA_FIT}` (P12; D-IH-47-J) | LLM-judge per-axis pass thresholds |
| **New mirrored / derived** | `compliance.persona_scenario_registry_mirror` (P1) + extended `compliance.eval_run` with `persona_id` + `difficulty_class` columns (P10) | Standard governance posture |
| **New mirrored / derived** | `tests/evals/cassettes/persona/<persona_id>/<scenario_id>.jsonl` (~350 cassettes) | Recorded; not authored; replay-driven by P10 dispatcher |
| **New scripts** | `scripts/calibrate_scenarios.py`, `scripts/agent_memory_trigger_watcher.py`, extended `scripts/eval.py` (P10/P11/P12 flags) | Operator + CI surfaces |
| **New CI** | Extended `.github/workflows/eval-tier-b.yml` with 4-D matrix (P14) | Per-persona spend cap |

## Phase plan (16 phases, ~9 week elapsed time)

| # | Phase | Output | Dependency |
|:--:|:------|:-------|:-----------|
| P0 | Bootstrap + scenario taxonomy + calibration framework | This folder + 6 artifacts + scenario-taxonomy.md | — |
| P1 | PERSONA_SCENARIO_REGISTRY.csv schema (incl. `tenant_id`) + akos contract + validator + mirror DDL | New canonical CSV + Supabase migration | P0 |
| P2 | Operator persona scenario library | ~25 scenarios | P1 |
| P3 | Tier-1 external personas (4 × ~25) | 100 scenarios | P1 |
| P4 | Tier-2 external personas (8 × ~10) | 80 scenarios | P1 |
| P5 | Tier-3 external personas (4 × ~5) | 20 scenarios | P1 |
| P6 | Cross-axis stress scenarios | ~25 scenarios | P1 |
| P7 | Adversarial persona scenarios | ~30 scenarios | P1 + I45 P5 |
| P8 | Benchmark adapters | ~30 scenarios (LongMemEval-LIGHT + MASEval-LIGHT + Promptfoo subset) | P1 |
| P9 | Recovery / degraded-state scenarios | ~15 synthetic + 1 opt-in real-chaos per D-IH-47-L | P1 |
| P10 | Per-persona scorecard + difficulty meta-eval | `ScoreRow.persona_id`/`difficulty_class`/`scenario_class`/`judge_scores` + `--persona`/`--calibrate` CLI flags | P1 + I45 P1 |
| P11 (NEW) | Persona-conditioned MADEIRA prompts | `PERSONA_OVERLAY.md` + per-persona fragments + `assemble-prompts --persona` flag | P10 |
| P12 (NEW) | LLM-as-judge 3-axis scoring | `judge.py` + 3 POLICY_REGISTER rows + cost-cap CLI | P10 |
| P13 | Tech debt cleanup (4 items from I46 UAT) | sync_hlk_neo4j 6-dim writes; sync_compliance bool fix; agent_memory_trigger_watcher; eval_run live writes | P10 |
| P14 | Tier B GH Action 4-D matrix extension | `model_tier × persona × scenario_class × judge_axis` matrix + per-persona spend cap | P10 + P12 + I45 P6 |
| P15 | Tests + UAT + closure | Full pytest sweep + UAT report + CHANGELOG + WIP_DASHBOARD | All |

## Verification matrix

| Check | Profile | Cadence |
|:------|:--------|:--------|
| `validate_hlk.py` (full vault incl. PERSONA_SCENARIO_REGISTRY) | `pre_commit` | Every commit |
| `validate_persona_scenario_registry.py` | `pre_commit` | Every commit |
| Per-persona scorecard `--mode all --persona <id>` | `pre_commit` | Every commit |
| Difficulty-calibration meta-eval `--calibrate` | `pre_commit` (warn-only) + weekly (hard-fail on >5% drift from target) | Daily |
| Cross-axis + adversarial + benchmark + recovery cassette replays | `pre_commit` | Every commit |
| Real-chaos opt-in (`AKOS_REAL_CHAOS_OK=1`) | manual P15 + operator-on-demand | Never automatic |
| Tier B 4-D matrix run | `eval_tier_b_weekly` | Weekly + on-demand |
| LLM-judge cost ceiling | `pre_commit` | Every commit |

## Success metrics (closure conditions)

- PERSONA_SCENARIO_REGISTRY.csv with ≥250 scenarios across all 16 personas; validator green
- Difficulty distribution measured by P10 calibration matches target (40/40/10/10) within ±5%
- Per-persona scorecard emits per persona (16 personas × at least 1 row each)
- Cross-axis + adversarial + benchmark + recovery suites all PASS
- 4 tech debt items closed (drift canary 0 drift; bool emit fixed; eval_run mirror has live data; trigger watcher has 1 emission test)
- Tier B persona matrix runs end-to-end against ≥1 persona with `AKOS_RECORD_LIVE=1`
- Live UAT demo: 16-persona scorecard rendered + calibration distribution + recovery scenario triggered + browser walkthrough
- ≥5 real bugs found by new scenarios that I45 P5 adversarial cassettes did NOT catch
- Persona-conditioned MADEIRA prompts shipped (RICE A); LLM-judge live (RICE B); tenant_id column live (RICE C); real-chaos opt-in works (RICE D)

## Risks + rollback

See [`risk-register.md`](risk-register.md). 14 risks tracked (8 original + 6 from RICE-expansion).

## Reporting artifacts

- `reports/p<N>-*-YYYY-MM-DD.md` per phase
- `reports/uat-i47-user-centric-uat-2026-05-XX.md` (P15 closure)
- `reports/calibration-baseline-2026-05-XX.md` (P0 + P10 difficulty meta-eval baseline)

## Cross-cutting

- Decision IDs: `D-IH-47-A` through `D-IH-47-L` (12 seeded; user pre-ratified at greenlight 2026-05-02 03:25 CET)
- All vault docs carry `language: en` frontmatter
- WIP_DASHBOARD picks this row up automatically
- CHANGELOG entry on closure (P15)

## What this is NOT

- Not a rewrite of I45/I46 (extension only)
- Not adopting a public benchmark leaderboard (adapt patterns; score internally)
- Not Inspect AI / DeepEval adoption (D-IH-45-A still holds)
- Not multi-tenant runtime work (only schema prep per D-IH-47-K)
- Not building product UI for non-operator personas (operator console only)
- Not a new CI runner (extends existing eval-tier-b.yml)
