---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 47 — Evidence Matrix

| ID | Observation | Source | Impact | Resolved by |
|:---|:------------|:-------|:-------|:------------|
| **E1** | The I46 UAT (browser + Supabase MCP + CLI) demonstrated all I45/I46 surfaces working but every cassette assumed operator voice/intent/vocabulary. Zero scenarios for non-operator personas. | I46 P7 closure UAT | Cannot validate persona-conditioned routing (I46 P5 conditional GraphRAG ship) or product-surface readiness | P2-P5 (operator + 15 external persona scenario libraries) |
| **E2** | Drift canary (I46 P2) caught real bug: `scripts/sync_hlk_neo4j.py:sync_csv_graph()` only writes Role/Process/Program/Topic (4 dimensions); Persona/Channel/Sourcing/Skill/TouchpointKitCell/Policy (6 axis-6 dimensions added in I32 P5/P6) are projected by `akos.hlk_graph_model` but never sent to Neo4j. | I46 UAT terminal output: 5 dimensions show `csv=N neo4j=0 [DRIFT]` | MADEIRA's optional graph traversal (per `agent-capabilities.json`) cannot use the axis-6 nodes; I46 P5 GraphRAG conditional ship would consume the missing data | P13 item 1 (extend sync_csv_graph to call all 10 dimension build functions) |
| **E3** | `scripts/sync_compliance_mirrors_from_csv.py` emits empty string `''` for boolean columns. The first INSERT against `compliance.skill_registry_mirror.tools_required_waived` (BOOLEAN) failed with `22P02: invalid input syntax for type boolean: ""`. | I46 P7 operator-applied step | Operator had to hand-write UPDATE statements via MCP execute_sql; sync script unusable for tables with bool columns | P13 item 2 (schema introspection or per-column override map; emit `true`/`false`) |
| **E4** | The `compliance.eval_run` mirror DDL exists (I45 P4 migration) but no code writes to it. The append-only history slot is currently inert. | Read of `akos/eval_harness/v2.py` (no `INSERT INTO compliance.eval_run` calls) | We can't query rolling cost / latency / regression patterns over time; defeats the purpose of P4's "symmetric to compliance.validation_runs" goal | P13 item 4 (`scripts/eval.py` writes per-row after each `--mode all` run) |
| **E5** | I46 P4 ADR (`AGENT_MEMORY_DEFERRED_ADR.md`) names 3 trigger conditions but no automated watcher emits when any fires. Trigger detection is operator-judgement-only. | Read of ADR + grep `agent_memory_trigger` returns zero matches in scripts/ | Trigger-fired-but-undetected is the core "deferred but never reopened" failure mode | P13 item 3 (`scripts/agent_memory_trigger_watcher.py` cron-ready; emits heads-up when any trigger fires) |
| **E6** | Substring rubric (`contains` / `forbidden` lists in I45 P1 `score_rubric_task`) catches token leakage but misses paraphrased jargon, missing citations, persona-register mismatch. | Read of `akos/eval_harness/__init__.py:score_rubric_task` (substring-only) | Tier B regression detection has a glass ceiling; persona-fit/brand-voice/citation discipline are unscored | P12 (LLM-as-judge 3-axis scoring per D-IH-47-J) |
| **E7** | All 16 PERSONA_REGISTRY archetypes exist in CSV with `typical_languages` + `typical_distance_band` + `intro_artifact_path` metadata, but no eval surface consumes them. The persona dimension is registry-only; never exercised. | Read of `PERSONA_REGISTRY.csv` (16 rows, fully populated; cross-coupled to `topic_persona_registry`) | Personas are governance-canonical but eval-invisible; registry-evaluator triangle is missing the persona vertex | P1-P5 (PERSONA_SCENARIO_REGISTRY.csv joins persona × skill × scenario) |
| **E8** | I46 P5 conditional GraphRAG ship adds `retrieval_mode` column to SKILL_REGISTRY (operator activates per skill if PoC ships). Activation needs persona-aware regression coverage; without I47 there's no way to test "did graph_rag retrieval improve investor-cold persona response without breaking operator persona response". | Read of I46 P5 phase report | I46 P5 ship-or-no-ship decision (D-IH-46-Decision-P3) is harder to make with only operator-shaped cassettes | P3-P5 + P10 + P11 (per-persona scorecard + persona-conditioned MADEIRA prompts) |
| **E9** | Initiative 34 (multi-tenant) is the next major initiative per planning README. Adding `tenant_id` to PERSONA_SCENARIO_REGISTRY at design-time is 0.25 weeks; retrofitting later is ~3 weeks (cassette regeneration + mirror re-migration + cross-product fan-out). | Cursor plan §"What this is NOT" + AgentMarketCap 2026 multi-tenant patterns | Late retrofit risk: I34 stalls on cassette migration; or worse, ships without per-tenant scenario coverage | P1 (`tenant_id` NULL-default column from day 1 per D-IH-47-K) |
| **E10** | The 6 default recovery scenarios in P9 use synthetic mocks (env vars; timestamp injection). The I46 UAT lesson — Aura password truncation — was a real-vs-mocked-API divergence (the mock said HTTP 401; the real Aura HTTP API also said HTTP 401, but the operator's actual password vs intended-password gap was invisible to the mock). | I46 D-IH-32-Q diagnosis report | Pure-synthetic CI cannot catch this class; pure-real chaos is operationally risky | P9 (hybrid: synthetic default + 1 opt-in real-chaos per D-IH-47-L) |
| **E11** | OpenClaw Control SPA at gateway `:18789` displays 5 agents (HLK Orchestrator/Architect/Executor/Verifier + Madeira) and 52 skills. The 5 agents match `SKILL_REGISTRY.csv:agents_supported`; the 52 skills are OpenClaw runtime plugins (different layer). The persona dimension is NOT exposed in the gateway UI. | I46 P7 browser UAT screenshots | Operator cannot switch personas in the live gateway today; I47 fixes the eval surface but UI is operator-side product work (out of I47 scope) | P10 + P11 expose per-persona scorecard via CLI; product UI deferred |
| **E12** | The I46 P7 closure caught the OVERLAY_HLK_GRAPH addition pushing MADEIRA_PROMPT.standard.md to 20324 chars (over the 20000 bootstrapMaxChars limit) and shrunk the doctrine pointer note to 80 chars. | I46 P7 commit message | Persona overlays (P11) face the same risk; need explicit length test in `assemble-prompts.py` | P11 (per-persona length test asserting MADEIRA_PROMPT stays ≤19500 chars under any overlay; R-47-9 mitigation) |

## Cross-references to other initiatives

- **Initiative 31 P2** — built `PERSONA_REGISTRY.csv` (the 16-row registry I47 builds scenarios for)
- **Initiative 32 P5/P6** — built the 6 axis-6 dimensions (E2 source: sync_hlk_neo4j doesn't write them yet)
- **Initiative 32 P9** — built per-skill canary surface that I47 P10 extends with `persona_id`
- **Initiative 45 P1-P8** — eval harness foundation; I47 builds on every phase
- **Initiative 45 P5** — adversarial cassette pattern; I47 P7 extends with persona context + tier-jumping + cross-persona leakage
- **Initiative 46 P2** — drift canary (E2 source)
- **Initiative 46 P4** — agent memory ADR (E5 source — trigger watcher gap)
- **Initiative 46 P5** — conditional GraphRAG ship (E8 dependency)
- **Initiative 46 P7** — closure UAT (E1, E11, E12 source)
- **Initiative 34 (future)** — multi-tenant runtime (E9 dependency target)
- **Initiative 49 (future)** — multi-judge consensus + public benchmark adoption (D-DEFER-47-α/γ targets)
