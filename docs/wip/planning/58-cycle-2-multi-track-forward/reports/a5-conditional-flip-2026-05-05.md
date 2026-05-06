---
language: en
status: skipped
initiative: 58-cycle-2-multi-track-forward
report_kind: phase-report
phase: A.5
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-05
---

# I58 A.5 — Conditional I46 P5 flip + POLICY clone (SKIPPED this cycle, 2026-05-05)

## Outcome

A.5 is **SKIPPED this cycle** because A.3 (GraphRAG A/B) did not fire — A.0 returned G-58-1 NO-FIRE (4 / 11 prerequisites met) and A.1 → A.4 forwarded as OPS-58-1. Per D-IH-58-C ("GraphRAG NO-SHIP is a closure event, not a failure"), no-fire ⇒ no-flip; I46 P5 stays deferred with the infrastructure preserved ship-ready by I53 P6.

This is the documented expected behavior: A.5 is gated on **A.3 = GO**, not on A.3 firing at all. A non-fire of A.3 is equivalent to a deferred verdict; A.5 stays armed for the next cycle when OPS-58-1 fires.

## Trigger contract (re-affirmed from D-IH-58-C + D-IH-46-E)

A.5 fires **if and only if** A.3 returns a single-bar GO at the D-IH-46-E non-additive bar:

- ≥3pp accuracy lift, OR
- ≥30% latency reduction, OR
- ≥40% cost reduction.

NO-SHIP at A.3 (none of the three bars hit) keeps A.5 SKIPPED per D-IH-58-C; I46 P5 stays deferred. **No mid-bar negotiation** per D-IH-46-E.

## What A.5 ships when triggered (gated commit shape)

When OPS-58-1 fires and A.3 returns GO, A.5 is one commit with three coordinated edits + one mirror reseed SQL stub:

### Edit 1 — `SKILL_REGISTRY.csv` `retrieval_mode` flip

[`docs/references/hlk/compliance/dimensions/SKILL_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv)

Flip `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode` from `vector_only` to:

- `graph_rag` if A.3 hit the bar with single-mode GraphRAG (graph-only retrieval), OR
- `hybrid` if A.3 hit the bar with vector+graph hybrid retrieval (the typical winning configuration per [I53 P1 audit](../53-graphrag-poc-closure/reports/p1-golden-set-audit-2026-05-03.md)).

The choice between `graph_rag` and `hybrid` is recorded in `D-IH-46-Decision-P3-2026-MM-DD` (the same decision-log entry that captures the A.3 verdict, written to BOTH I46 and I53 decision-logs).

### Edit 2 — Clone new `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-V1` POLICY row

[`docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv`](../../../references/hlk/compliance/dimensions/POLICY_REGISTER.csv)

New row (cloned from the I46 P5 conditional-ship infrastructure preserved by I53 P6):

```csv
policy_id,policy_class,owner_role,policy_text,...
POL-NEO4J-GRAPH-RAG-ELIGIBILITY-V1,graph_rag_eligibility,System Owner,"GraphRAG is eligible for SKILL-MADEIRA-LOOKUP-V1 when A.3 verdict GO at D-IH-46-E non-additive bar; eligibility re-evaluates per cycle.",...
```

The `policy_class=graph_rag_eligibility` enum value is already in `akos.hlk_policy_register_csv` per [I46 P5 conditional-ship infrastructure](../46-neo4j-strategic-posture/master-roadmap.md#p5-conditional-graphrag-ship); no parser change needed.

### Edit 3 — Stage mirror reseed SQL stub

`artifacts/sql/mirror-batches/<YYYYMMDD>/i58-a5-graphrag-go-skill-policy-flip.sql` (gitignored under `artifacts/`):

- One UPDATE statement on `compliance.skill_registry_mirror` for the `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode` change.
- One INSERT on `compliance.policy_register_mirror` for the new POLICY row.

Operator applies via `npx supabase db query --linked --file <stub>` per the I22a P7 pattern.

### Re-run validation

```powershell
py scripts/validate_hlk.py
py scripts/verify.py compliance_mirror_emit
```

Both must PASS post-edit; the new POLICY row counts up by 1 (current 33 + 1 = 34); the SKILL row count stays at 5.

### Capture

`reports/a5-i46-p5-flip-2026-MM-DD.md` with the verdict-mode chosen (`graph_rag` vs `hybrid`), the SQL stub path + sha256, the post-edit validator counts, and the cross-link to the A.3 decision-log row.

## Why A.5 is not a new initiative

The infrastructure was preserved ship-ready by [I53 P6](../53-graphrag-poc-closure/master-roadmap.md): the `retrieval_mode` column already exists on `SKILL_REGISTRY.csv`, the `policy_class=graph_rag_eligibility` enum is already in the parser, and the mirror reseed SQL pattern is established by I22a P7. A.5 is a **single small commit** that lands when (and only when) the upstream verdict justifies it. Per the asset classification, it is "out-of-scope unless GO; spawned as small follow-on, not a new initiative".

## Verification (A.5 SKIPPED state)

| Check | Result |
|:------|:-------|
| A.3 verdict captured? | NO (A.3 forwarded; no live run this cycle) |
| `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode` current value | `vector_only` (unchanged from I53 P6 ship-ready state) |
| `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-V1` POLICY row present? | NO (per `validate_hlk.py` POLICY_REGISTER count = 33) |
| I46 P5 deferred state preserved? | YES (no edit landed; matches [I53 P5 SKIPPED state](../53-graphrag-poc-closure/master-roadmap.md)) |
| `validate_hlk.py` POLICY_REGISTER count | 33 (unchanged; expected 34 only after A.5 fires on GO) |

## Cross-references

- A.0 evidence (G-58-1 NO-FIRE state): [`a0-env-preflight-2026-05-05.md`](a0-env-preflight-2026-05-05.md)
- A.1 → A.4 forward: [`a1-a4-live-cycle-forward-2026-05-05.md`](a1-a4-live-cycle-forward-2026-05-05.md)
- D-IH-58-C (NO-SHIP closure event semantics): [`decision-log.md`](../decision-log.md#d-ih-58-c--graphrag-no-ship-is-a-closure-event-not-a-failure)
- D-IH-46-E (non-additive bar): [`../46-neo4j-strategic-posture/decision-log.md`](../46-neo4j-strategic-posture/decision-log.md)
- I46 P5 conditional ship infrastructure: [`../46-neo4j-strategic-posture/master-roadmap.md`](../46-neo4j-strategic-posture/master-roadmap.md)
- I53 P6 closure (preserved ship-ready): [`../53-graphrag-poc-closure/master-roadmap.md`](../53-graphrag-poc-closure/master-roadmap.md)
