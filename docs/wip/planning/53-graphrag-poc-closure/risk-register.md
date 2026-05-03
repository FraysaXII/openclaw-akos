---
language: en
status: active
initiative: 53-graphrag-poc-closure
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 53 — Risk register

## R-53-1 — Operator-funded $20 envelope insufficient for 20 cassette × 2 modes × judge scoring

**Severity:** High (blocks live A/B execution).

**Mitigation:** Cap embedding cost via `nomic-embed-text` (Ollama, $0); pre-flight cost estimate at P1 exit; abort and downscope if estimate >$25.

**Status:** Active; pre-flight estimate happens at P1.

---

## R-53-2 — PoC succeeds only marginally (just under one of the three bars)

**Severity:** Medium.

**Mitigation:** D-IH-53-C explicitly forbids partial-credit ship; defer to a future initiative if so. The no-ship path is well-documented.

**Status:** Open until P4 verdict logs; D-IH-53-C blocks accidental ship.

---

## R-53-3 — Adversarial graph-escape reveals systemic Neo4j projection gap

**Severity:** Critical.

**Mitigation:** I32 P5/P6 idempotency proof + drift canary (already live) is the floor; if escape works, file as Critical and block P5. Existing test `tests/test_neo4j_graph_escape.py` is the gate.

**Status:** Active.

---

## R-53-4 — Operator declines to opt into live A/B this cycle

**Severity:** Low (no-fire is a documented governance outcome, not a failure).

**Mitigation:** P3 reports the **no-fire** outcome as a governance event (mirrors I52 P3 / P4 / P5 stub-mode pattern); no-ship path documented; cassettes preserved for next cycle. I53 closes on the no-ship path. I46 closes alongside (its master-roadmap success criteria explicitly accept "documented decision-not-to-ship with PoC numbers" — and "PoC numbers" can include the no-fire governance event when no live run has occurred).

**Status:** Active; this is the most likely outcome given the operator's current execution stance.
