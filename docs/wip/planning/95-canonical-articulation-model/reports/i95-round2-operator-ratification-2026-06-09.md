---
report_type: operator-ratification
parent_initiative: INIT-OPENCLAW_AKOS-95
phase: P95-R2-post-ratification
authored: 2026-06-09
authored_by: Thinking seat (Opus) → execution seat mint
closure_decision_source: operator_explicit
ratifying_decisions:
  - D-IH-95-G
  - D-IH-95-H
  - D-IH-95-I
  - D-IH-95-J
status: ratified
---

# I95 Round-2 — Operator ratification capture (2026-06-09)

**Initiative:** INIT-OPENCLAW_AKOS-95 (Canonical Articulation Model)  
**Context:** Post-AskQuestion ratification after GOV-8 closure @ `1bc2d1d`. Deep thinking-seat research: [`a568f6c9-05f8-4109-b653-545539443362`](agent-transcript).

---

## Binding operator choices

| Lane | Operator choice | Nuance |
|:---|:---|:---|
| **L1 EG** | **A** | EG-2 API exposure doc + `config.toml` reconcile |
| **L2** | **A if not done** | Operator asked: "didn't we do that already?" — **VERIFY** foundation schema + D+F+L pilot collapse state before recommending execution |
| **L3** | **All bundles** | Wants TRP-038/045–047/021 AND engagement cluster AND TRP-030/036 unblock — parallel/multitask with **research first per bundle** |
| **Neo4j** | **All out e2e** | NOT spec-only — full cutover; operator says assessments/plans/intent exist |
| **Hygiene** | **B then C** | Re-scan vault for 74th CSV, then charter amend + CS strict audit/fix — **research + brainstorm first** |
| **Master seq** | **A all-out** | Mirror → L3 → L2 → L1 → Neo4j but **no spec-only** lanes; each lane: research → AskQuestion → brainstorm → research → detailed thinking charter before Composer execution |

---

## Master sequence (ratified vs adjusted)

### Ratified literal order

Mirror → L3 → L2 → L1 → Neo4j — **no spec-only** lanes.

### Adjusted order (post L2 state audit — recommended)

L2 collapse is **DONE** @ 2026-06-08 (D-IH-95-I). Do **not** re-run collapse.

| Step | Lane | Mode |
|:---|:---|:---|
| 1 | **Mirror** | Operator walkthrough Steps 0–4 (GOV-5/7 prod apply) |
| 2 | **L3 A+B** | Research → AskQuestion Q2 → tranche-4 bindings commit |
| 3 | **L3 C** | Research charter only → CSV gate for TRP-030/036 |
| 4 | **L1 EG** | `SUPABASE_API_EXPOSURE.md` + `config.toml` reconcile (operator ratified A) |
| 5 | **L2 follow-ups** | Rating cadence + TRP-014 + mirror backlog (not re-collapse) |
| 6 | **Neo4j** | Dual-emit implementation → Council sign-off → CQ1–5 live UAT |
| 7 | **Hygiene B→C** | Charter 73 amend → CS research/brainstorm per Q4 |

---

## Per-lane execution contract

Each lane follows: **research → AskQuestion → brainstorm → research → detailed thinking charter → Composer execution**.

Hard gates before lane execution:

- **L2:** AskQuestion Q1 (skip collapse vs re-run) — audit says **skip**
- **Neo4j:** AskQuestion Q3 (credentials + cutover posture)
- **L3:** AskQuestion Q2 (parallel phasing)
- **Hygiene C:** AskQuestion Q4 (scope after B charter amend)

---

## Cross-references

- L2 state audit: [`i95-l2-state-audit-2026-06-09.md`](i95-l2-state-audit-2026-06-09.md)
- L3 parallel bundles: [`i95-l3-parallel-bundles-charter-2026-06-09.md`](i95-l3-parallel-bundles-charter-2026-06-09.md)
- Neo4j e2e cutover: [`i95-neo4j-e2e-cutover-charter-2026-06-09.md`](i95-neo4j-e2e-cutover-charter-2026-06-09.md)
- Hygiene B→C: [`i95-hygiene-research-2026-06-09.md`](i95-hygiene-research-2026-06-09.md)
- Prior synthesis (L2 section stale — superseded): [`i95-round2-lanes-research-synthesis-2026-06-09.md`](i95-round2-lanes-research-synthesis-2026-06-09.md)
- Mirror walkthrough: [`operator-mirror-apply-walkthrough-2026-06-09.md`](operator-mirror-apply-walkthrough-2026-06-09.md)
