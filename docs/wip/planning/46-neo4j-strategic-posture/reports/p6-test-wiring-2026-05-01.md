---
language: en
status: active
intellectual_kind: phase_report
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# I46 P6 — Test wiring (graph-escape + cassette dir scaffold + WIP health surface)

**Phase:** P6 (depends on I45 P2 + P5; closes the test-wiring layer for I46)
**Closes:** I46 P6 + R-46-2 mitigation (graph-escape probes guard against GraphRAG hallucinations) + evidence-matrix E11 (Neo4j drift surfaced in WIP_DASHBOARD).
**Date:** 2026-05-01

## Actions

1. **3 graph-escape adversarial cassettes** under `tests/evals/cassettes/adversarial/SKILL-MADEIRA-LOOKUP-V1/`:
   - `ge_simple_role_id_lookup.jsonl` — "Look up the role 'System Owner'" (must stay on CSV path)
   - `ge_persona_id_direct.jsonl` — "What is PERSONA-INVESTOR-COLD?" (direct dimension lookup)
   - `ge_process_item_id_direct.jsonl` — "Show me process item env_tech_prj_2" (direct id lookup)
   - Each `forbidden_in_response` extends the standard JARGON_TOKENS list with `["graph_rag", "neo4j"]` — verifying classify_request doesn't leak graph-mode tokens into responses for simple direct lookups
   - All target SKILL-MADEIRA-LOOKUP-V1 (highest-traffic skill; most likely to be over-eagerly routed once GraphRAG ships)

2. **GraphRAG cassette directory scaffold** at `tests/evals/cassettes/graph_rag/`:
   - Directory present with `README.md` (`status: scaffold`)
   - README documents the activation flow (operator runs P3 PoC → records ship in decision-log → records initial cassettes via `eval.py record --kind live_llm`)
   - Empty of cassettes today (no skill is `retrieval_mode='graph_rag'` yet)
   - When populated, `py scripts/eval.py --mode replay` picks them up automatically (I45 P2 dispatcher routes by `probe_kind`)

3. **WIP_DASHBOARD operational health surface** (hand-written; below auto-render markers so re-renders preserve it):
   - 5 live signals with operator-runs commands:
     - Neo4j governance KG drift (I46 P2): `py scripts/graphrag_drift_canary.py`
     - Eval harness Tier A smoke (I45 P6): `py scripts/eval.py --mode all`
     - Cassette PII linter (I45 P5; R-45-4): `py scripts/lint_cassette_pii.py`
     - Adversarial floor (I45 P5): `py scripts/eval.py --mode adversarial`
     - Skill promotion gate (I45 P7): `py scripts/eval.py promote --skill <id>`
   - "operator-recorded" Last-green column = operator updates manually after each run

4. **10 new tests** in `tests/test_neo4j_graph_escape.py`:
   - Graph-escape cassettes (4 tests): 3 ge_* probes shipped + target MADEIRA-LOOKUP + forbid graph_rag/neo4j tokens + all replay PASS
   - GraphRAG cassette dir scaffold (3 tests): dir + README present + activation flow documented + language frontmatter
   - WIP_DASHBOARD operational health surface (3 tests): drift canary pointer + eval/PII/adversarial pointers + hand-written section OUTSIDE auto-render markers (drift detector)

## Verification

- `py scripts/eval.py --mode adversarial`: **15/15 PASS** (12 from I45 P5 + 3 new graph-escape from I46 P6); overall PASS
- `py scripts/lint_cassette_pii.py`: **21 cassettes scanned, 0 PII findings**; PASS
- `py scripts/render_wip_dashboard.py`: deterministic sha256 stable; auto-section unchanged; hand-written "Operational health" section preserved (verified by `test_wip_dashboard_auto_section_unchanged_after_p6`)
- `tests/test_neo4j_graph_escape.py`: **10/10 PASS** in 0.9s
- Cross-suite regression: `tests/test_eval_adversarial.py` + `test_neo4j_graph_escape.py` + `test_neo4j_retrieval_mode.py` + `test_neo4j_usecase_a_hardening.py`: **55/55 PASS** in 4.5s

## What this does NOT do (operator-pending)

- **No live GraphRAG cassettes recorded yet** — the cassette directory is scaffold; live cassettes land when operator runs P3 PoC and ships at least one skill. Documented in the directory's README.
- **No router-side `retrieval_mode` honour** — when the first skill activates, `akos.skill_router` needs an extension. Out of P6 scope; lands as a P5 follow-up commit when the activation happens.
- **No automated WIP_DASHBOARD health-signal capture** — operators run the 5 signals on demand and update "Last green" manually. Automation could be added later (out of I46 scope).

## Risks resolved

- **R-46-2 (GraphRAG hallucinations leak into MADEIRA answers)**: foundation in place. The 3 graph-escape probes verify simple direct lookups STAY on CSV path even when classify_request output mentions graph terms. When GraphRAG ships, these probes detect over-eager graph routing as a regression.

## Operator-applied steps

1. Add `eval_harness_smoke` (I45 P6) and `neo4j_governance_kg_drift_smoke` (I46 P2) profiles to `pre_commit` profile in `verification-profiles.json` if you want per-commit enforcement of these signals (operator decision per the doctrine `NEO4J_STRATEGY.md` §"Operator-known gotchas" warns about CI cost ceilings).
2. After running each WIP_DASHBOARD operational-health command, edit the "Last green" column with the date and the result. (Could be auto-rendered in a follow-up I46 P7+ if desired.)

## Next phase

P7 — Closure. Full pytest sweep + UAT report covering all 8 phases + CHANGELOG entry + WIP_DASHBOARD re-render + I46 closure assertion. Hand-off note documents the operator follow-ups (P3 PoC live run, P5 conditional ship if PoC passes, P4 ADR trigger watch, recurring Neo4j drift canary cron).
