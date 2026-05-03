---
language: en
status: closed
initiative: 53-graphrag-poc-closure
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 53 — GraphRAG PoC closure (closes I46 P3-P7)

**Folder:** `docs/wip/planning/53-graphrag-poc-closure/`

**Status:** **Closed (2026-05-03)** on the no-ship path. P0-P2 audit + P3 NO-FIRE governance event + P4 NO-SHIP verdict (`D-IH-46-Decision-P3-NO-SHIP-2026-05-03`) + P5 SKIPPED + P6 verification + P7 closure UAT all executed. Live A/B forwarded as **OPS-53-1** (likely shared with **OPS-52-1**) to next AKOS_RECORD_LIVE cycle. Release-gate **PASS** (8/8). Cassettes, scaffold, and CSV+POLICY infrastructure all preserved ship-ready.

**Authoritative Cursor plan:** `~/.cursor/plans/i50–i56_madeira_kb_completion_87cc767e.plan.md` §"Initiative 53".

**Origin:**

- [I46 master-roadmap](../46-neo4j-strategic-posture/master-roadmap.md) P3-P7 (Open since 2026-05-01); D-IH-46-A through G ratified.
- I46 P3 scaffold landed (`scripts/graphrag_poc.py`, `config/graphrag/golden_queries.json`, 14 tests; 2026-05-01) but **live A/B execution deferred** to operator-funded $20 envelope (R-46-1) — see [`46-neo4j-strategic-posture/reports/p3-graphrag-poc-scaffold-2026-05-01.md`](../46-neo4j-strategic-posture/reports/p3-graphrag-poc-scaffold-2026-05-01.md).
- I46 P5 scaffold landed (`retrieval_mode` column on SKILL_REGISTRY; `pol_neo4j_graph_rag_eligibility` POLICY row; `intent.py` dispatch; 2026-05-01) but **decision-flip deferred** until P3 A/B numbers are available.
- I46 P6 + P7 partly executed (drift canary, adversarial probes scaffolded; cassettes folder exists).
- **R-46-1 still in force:** operator-funded ~$20 envelope for the LightRAG-style hybrid PoC; cap embedding cost via `nomic-embed-text` (Ollama, $0).

## Outcome

(a) Drive the bounded PoC against `SKILL-MADEIRA-LOOKUP-V1` on the 20 multi-hop golden queries already authored at I46 P3, A/B vs current `hlk_role + hlk_search` chain;
(b) produce concrete cost / latency / accuracy numbers in `reports/graphrag-poc-results-YYYY-MM-DD.md`;
(c) ship-or-no-ship verdict logged as `D-IH-46-Decision-P3-YYYY-MM-DD`;
(d) conditional P5 ship of `retrieval_mode=graph_rag` flip on `SKILL-MADEIRA-LOOKUP-V1` + `pol_neo4j_graph_rag_eligibility` enforcement;
(e) close I46 master-roadmap.

**Bidirectional contract with I52:** if PoC live A/B executes, the multi-judge roster scores the accuracy axis. If only dispatcher-validation runs (no live API), the no-ship path is the honest outcome — same pattern as I52 P3 calibration burn.

## Asset classification

| Class | Paths | Rule |
|:------|:------|:-----|
| **New canonical (planning)** | `docs/wip/planning/53-graphrag-poc-closure/{master-roadmap,decision-log,asset-classification,evidence-matrix,risk-register}.md` + `reports/` | 6 standard artefacts |
| **Existing scripts (reused, hardened)** | [`scripts/graphrag_poc.py`](../../../scripts/graphrag_poc.py) (I46 P3 scaffold), [`scripts/graphrag_drift_canary.py`](../../../scripts/graphrag_drift_canary.py) | PoC + canary; this initiative drives them through real A/B exercise |
| **Existing canonical (vault, conditional flip)** | `retrieval_mode` column on [`SKILL_REGISTRY.csv`](../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv) (I46 P5 column already added) | Flip `SKILL-MADEIRA-LOOKUP-V1` row only if PoC ships |
| **Existing canonical (POLICY, conditional)** | `pol_neo4j_graph_rag_eligibility` row in [`POLICY_REGISTER.csv`](../../references/hlk/compliance/dimensions/POLICY_REGISTER.csv); `policy_class=graph_rag_eligibility` enum value | Already present (I46 P5); enforces eligibility on flip |
| **Existing canonical (router)** | [`akos/intent.py`](../../../akos/intent.py) | Already reads `retrieval_mode`; reversible |
| **Cassettes (operator-driven)** | `tests/evals/cassettes/graph_rag/<query_id>.jsonl` (20 cassettes via I45 P2 recorder) | Recorded via live PoC run; not authored |
| **Existing tests** | `tests/test_graphrag_poc.py` (I46 P3; 14 tests), `tests/test_graphrag_dispatcher.py` (if present), `tests/test_neo4j_graph_escape.py` (adversarial), `tests/test_neo4j_retrieval_mode.py` | This initiative may add a small number of tests if drift / canary findings demand |

## Phase plan (~5-7 op-days; ~$20 envelope per R-46-1)

| Phase | Focus |
|:-:|:----|
| **P0** | Bootstrap I53 folder + 6 artefacts; cross-link I46 P3-P7 reports; README row. |
| **P1** | **Pre-flight + golden-set audit:** Verify [`config/graphrag/golden_queries.json`](../../../config/graphrag/golden_queries.json) (20 queries; I46 P3) is governed; `py scripts/graphrag_poc.py --validate-config` PASS; document the I46 P3 cost-estimate refresh and the operator opt-in surface (`AKOS_GRAPHRAG_POC_LIVE=1` + provider env). |
| **P2** | **PoC infra audit:** Re-confirm `scripts/graphrag_poc.py --dry-run` lists planned execution + cost ceiling; verify the existing scaffold path is still wired; verify Neo4j connection knobs documented. |
| **P3** | **A/B run + report (operator-gated; G-53-1 input):** When operator opts in via `AKOS_GRAPHRAG_POC_LIVE=1`, run live A/B; emit `reports/graphrag-poc-results-YYYY-MM-DD.md` with cost / latency / accuracy delta per query class; multi-judge (I52) scores accuracy axis. Without operator opt-in, document the **no-fire** outcome as a governance event mirroring I52 P3 / P4 / P5 stub-mode pattern. |
| **P4** | **Ship/no-ship gate (G-53-1):** Per [D-IH-46-E](../46-neo4j-strategic-posture/decision-log.md): if **≥1** of (≥3pp accuracy lift OR ≥30% latency reduction OR ≥40% cost reduction): proceed P5. Else log `D-IH-46-Decision-P3-NO-SHIP` and skip to P7. **D-IH-53-C** explicitly forbids partial-credit ship. |
| **P5** | **Conditional ship (G-53-2 + G-53-3; conditional on P4):** Flip `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode = graph_rag` in [`SKILL_REGISTRY.csv`](../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv); confirm `pol_neo4j_graph_rag_eligibility` POLICY row covers the topic class; verify `akos/intent.py` dispatch on the new value; mirror reseed. |
| **P6** | **Test wiring + canaries:** Confirm `neo4j_governance_kg_drift_smoke` profile in [`config/verification-profiles.json`](../../../config/verification-profiles.json) wired to drift canary; adversarial probe (`tests/test_neo4j_graph_escape.py`) green; Neo4j drift canary row visible in [`WIP_DASHBOARD.md`](../WIP_DASHBOARD.md); `release_gate` idempotency proof preserved. |
| **P7** | **I46 + I53 closure UAT:** Flip I46 master-roadmap status to `Closed`; emit `reports/uat-i46-i53-graphrag-YYYY-MM-DD.md`; CHANGELOG entry; planning README rows for both I46 and I53 → `Closed (YYYY-MM-DD)`; WIP_DASHBOARD re-render. |

## Verification matrix

| Check | Cadence |
|:------|:--------|
| `py scripts/validate_hlk.py` (with conditional column / POLICY row) | Every commit |
| `py scripts/graphrag_poc.py --validate-config` (offline; 20-query golden set) | Every commit |
| `py scripts/graphrag_poc.py --dry-run` (offline; planned execution) | Every commit when scaffold present |
| `py -m pytest tests/test_graphrag_poc.py tests/test_neo4j_graph_escape.py tests/test_neo4j_retrieval_mode.py -v` | Every commit |
| `neo4j_governance_kg_drift_smoke` profile (Neo4j ≈ CSV row counts ±1) | Nightly + pre-commit |
| `release-gate` idempotency proof (`sync_hlk_neo4j` 2 consecutive runs identical) | Per release |
| Adversarial probe: graph-escape + citation spoofing | Every commit |
| Operator-driven live A/B: `AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py` | P3 (operator-funded $20 envelope) |

## Operator approval gates

- **G-53-1** (P4) — Ship/no-ship verdict on PoC outcome (depends on P3 live A/B run; if no live run, the gate **NO-FIRE**s and P5 is skipped on the no-ship path).
- **G-53-2** (P5, conditional) — Flip `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode = graph_rag` in SKILL_REGISTRY.
- **G-53-3** (P5, conditional) — Confirm `pol_neo4j_graph_rag_eligibility` enforcement on the topic class for `SKILL-MADEIRA-LOOKUP-V1`.

## Decisions seeded

- **D-IH-53-A** — Judge model used in PoC accuracy scoring: re-use I52 pinned roster (`anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o`).
- **D-IH-53-B** — 20-query selection criteria: 60% multi-hop / 40% single-hop; mix of OPERATOR + Tier-1 persona shapes (already encoded in I46 P3 `golden_queries.json`).
- **D-IH-53-C** — Trade-off thresholds: any one of the three I46 P5 bars qualifies; **non-additive** per D-IH-46-E (no partial-credit ship).
- **D-IH-53-D** — Rollback procedure: SKILL_REGISTRY `retrieval_mode=vector_only` flip + decision-log row; cassettes preserved.

## Risks

- **R-53-1** — Operator-funded $20 envelope insufficient for 20 cassette × 2 modes × judge scoring. Mitigation: cap embedding cost via `nomic-embed-text` (Ollama, $0); pre-flight cost estimate at P1 exit; abort and downscope if estimate >$25.
- **R-53-2** — PoC succeeds only marginally (just under one of the three bars). Mitigation: D-IH-53-C explicitly forbids partial-credit ship; defer to a future initiative if so.
- **R-53-3** — Adversarial graph-escape reveals systemic Neo4j projection gap. Mitigation: I32 P5/P6 idempotency proof + drift canary (already live) is the floor; if escape works, file as Critical and block P5.
- **R-53-4** — Operator declines to opt into live A/B this cycle. Mitigation: P3 reports the **no-fire** outcome as a governance event (mirrors I52 P3 / P4 / P5 stub-mode pattern); no-ship path documented; cassettes preserved for next cycle.

## Success metrics

- `reports/graphrag-poc-results-*.md` published with concrete numbers (cost / latency / accuracy delta per query class), OR explicit no-fire governance report.
- Ship/no-ship verdict logged as `D-IH-46-Decision-P3-YYYY-MM-DD` in [`46-neo4j-strategic-posture/decision-log.md`](../46-neo4j-strategic-posture/decision-log.md).
- I46 master-roadmap status flipped to `Closed`.
- If ship: 1 skill (`SKILL-MADEIRA-LOOKUP-V1`) running `retrieval_mode=graph_rag` end-to-end with adversarial probe green.
- If no-ship: explicit decision log + cassettes preserved for future re-evaluation.

## What this is NOT

- Microsoft GraphRAG full adoption (D-IH-46-A; D-DEFER-47-α stays deferred).
- Agent memory build (D-IH-46-B defers; trigger-gated ADR at I46 P4 already authored).
- Cross-skill expansion of GraphRAG (incremental; future initiative if PoC + ship succeed).
- A migration away from current vector path (rollback path is always available via `retrieval_mode` flip).
