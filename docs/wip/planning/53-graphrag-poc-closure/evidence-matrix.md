---
language: en
status: active
initiative: 53-graphrag-poc-closure
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 53 — Evidence matrix

| ID | Observation | Source | Impact |
|:---|:------------|:-------|:-------|
| E1 | I46 P3 scaffold landed 2026-05-01: `scripts/graphrag_poc.py` (3 modes: --validate-config, --dry-run, live-with-AKOS_GRAPHRAG_POC_LIVE=1), `config/graphrag/golden_queries.json` (20 queries), 14 tests | [`46-neo4j-strategic-posture/reports/p3-graphrag-poc-scaffold-2026-05-01.md`](../46-neo4j-strategic-posture/reports/p3-graphrag-poc-scaffold-2026-05-01.md) | I53 P1-P2 audit, not re-author |
| E2 | I46 P5 conditional-ship infrastructure landed 2026-05-01: `retrieval_mode` column on SKILL_REGISTRY.csv; `pol_neo4j_graph_rag_eligibility` POLICY row; `policy_class=graph_rag_eligibility` enum value; `akos/intent.py` reads `retrieval_mode` from registry | [`46-neo4j-strategic-posture/reports/p5-conditional-graphrag-ship-2026-05-01.md`](../46-neo4j-strategic-posture/reports/p5-conditional-graphrag-ship-2026-05-01.md) | I53 P5 is a CSV-row flip, not a column add |
| E3 | I46 P6 test wiring + canaries landed 2026-05-01: `tests/test_neo4j_graph_escape.py`, `tests/test_neo4j_retrieval_mode.py`, `scripts/graphrag_drift_canary.py`, `tests/evals/cassettes/graph_rag/` folder | [`46-neo4j-strategic-posture/reports/p6-test-wiring-2026-05-01.md`](../46-neo4j-strategic-posture/reports/p6-test-wiring-2026-05-01.md) | I53 P6 is verification, not authoring |
| E4 | R-46-1 still in force: $20 envelope operator-funded; PoC LIVE mode is currently a SCAFFOLD that prints execution plan when env var is set, not a real `neo4j-graphrag-python` indexing loop | [`46-neo4j-strategic-posture/reports/p3-graphrag-poc-scaffold-2026-05-01.md`](../46-neo4j-strategic-posture/reports/p3-graphrag-poc-scaffold-2026-05-01.md) §"What this does NOT do" | I53 P3 either drives the live A/B (operator opt-in) or documents the no-fire outcome |
| E5 | I52 closure 2026-05-03 ships multi-judge roster (`prompts/judge/JUDGE_ROSTER_V1.md`) with N=2 consensus default and `MAX_JUDGE_USD_PER_RUN=$15` envelope; `score_response_live` no longer raises NotImplementedError when `AKOS_JUDGE_ROSTER` is set | I52 P8 closure UAT | D-IH-53-A re-uses this roster for PoC accuracy scoring |
| E6 | OPS-52-1 forwarded from I52 P3: real-API multi-judge calibration burn deferred to next AKOS_RECORD_LIVE cycle (operator-funded API spend) | [`52-multi-model-judge-and-cost-discipline/reports/p3-calibration-burn-2026-05-03.md`](../52-multi-model-judge-and-cost-discipline/reports/p3-calibration-burn-2026-05-03.md) | If I53 P3 fires live, OPS-52-1 closes alongside it (one operator-funded cycle for both) |
| E7 | I46 master-roadmap status `active` since 2026-05-01; closure path through I53 P7 | [`46-neo4j-strategic-posture/master-roadmap.md`](../46-neo4j-strategic-posture/master-roadmap.md) | I53 closes I46 |
| E8 | The operator's stated stance from the master-roadmap session: "Master roadmap: Initiatives 50–56 ... Don't stop until you have completed all the to-dos" — supports executing all non-live phases regardless of operator opt-in to $20 spend | I50-I56 master roadmap message | I53 executes P0-P2 + P6-P7 (audit + closure) on the no-fire path; P3-P5 honestly reflect the gating |
