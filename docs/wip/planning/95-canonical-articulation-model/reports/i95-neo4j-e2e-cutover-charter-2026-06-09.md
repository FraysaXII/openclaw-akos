---
report_type: neo4j-e2e-charter
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L4-HCAM-P2-Neo4j
authored: 2026-06-09
authored_by: Thinking seat (Opus) → execution seat mint
ratifying_decisions:
  - D-IH-95-C
  - D-IH-95-F
status: charter-only
blocked_on:
  - NEO4J_credentials
  - dual_emit_code
  - semantic_council_gate
---

# I95 Neo4j — Full e2e cutover execution charter (2026-06-09)

**Operator intent:** All-out e2e — NOT spec-only. Assessments/plans/intent exist; live graph mutation required after gates clear.

---

## What exists today (spec / additive only)

| Artifact | Role |
|:---|:---|
| [`akos/hlk_graph_articulation.py`](../../../../akos/hlk_graph_articulation.py) | 13 legacy → 6 unified verb edges; `COMPETENCY_QUESTIONS` Cypher specs; `assert_edge_coverage()`. **Does not mutate live graph.** |
| [`scripts/sync_hlk_neo4j.py`](../../../../scripts/sync_hlk_neo4j.py) | Still emits **legacy** edges via `hlk_graph_model.py` only — **no dual-emit, no unified mode flag** |
| I91 preflight | [`p1-neo4j-preflight-blocked-2026-06-01.md`](../../91-enterprise-graph-store-coverage/reports/p1-neo4j-preflight-blocked-2026-06-01.md) — `BLOCKED-ENV` |

---

## Full cutover phases

| Phase | Deliverable | Gate |
|:---|:---|:---|
| **N0** | Operator provides `NEO4J_URI` + `NEO4J_PASSWORD` in `~/.openclaw/.env` (or CI secrets) | I91 preflight clears |
| **N1** | Implement `--unified` / dual-emit in `hlk_graph_model` + `sync_hlk_neo4j` | Unit tests + `assert_edge_coverage()` |
| **N2** | Dry-run parity: CSV node/edge counts vs legacy projection | `sync_hlk_neo4j.py --dry-run` PASS |
| **N3** | One dual-emit sync cycle to Aura | Semantic Council sign-off (**D-IH-95-F**) |
| **N4** | Run CQ1–CQ5 against live Neo4j; capture evidence | Operator UAT row per competency question |
| **N5** | Flip consumers (graph MCP, explorer) to unified edge labels | Browser/API smoke |
| **N6** | Retire legacy edge emission; update parity assertions | Rollback = re-run legacy sync from tagged commit |
| **N7** | Closure: update I91 + I95 P2 status; link to area-completeness v3 | Closure UAT |

---

## Secrets checklist

| Secret | Location | Required for |
|:---|:---|:---|
| `NEO4J_URI` | `~/.openclaw/.env` or CI | N0–N7 — use `neo4j+s://`, not `bolt://` |
| `NEO4J_PASSWORD` | `~/.openclaw/.env` or CI | N0–N7 — from Aura credentials file or clone (Free tier) |
| `NEO4J_USERNAME` | same | Always lowercase `neo4j` on Aura Free (no `CREATE USER`) |

**Credential recovery (Aura Free):** [`i95-neo4j-credential-recovery-2026-06-09.md`](i95-neo4j-credential-recovery-2026-06-09.md) — clone instance or browser password test; paid-tier `CREATE USER` is appendix-only.

**Preflight command (after secrets set):**

```powershell
py scripts/sync_hlk_neo4j.py --dry-run
```

---

## Rollback posture

1. Tag commit immediately before N3 live sync (`git tag neo4j-pre-unified-<date>`).
2. Rollback = re-run legacy sync from tagged commit (no unified flag).
3. Keep dual-emit window until CQ1–5 green + operator UAT sign-off.
4. Document rollback in initiative `decision-log.md` before N3.

---

## Blockers (what prevents "all out" today)

1. **No Neo4j credentials** — I91 P1 `BLOCKED-ENV`.
2. **No dual-emit implementation** — articulation module is migration map only; sync script unchanged.
3. **D-IH-95-F / Semantic Council gate** — cutover explicitly gated.
4. **CQ1–CQ3 may fail on first live run** — unified Cypher assumes `Capability`, `Engagement`, `REALIZES`, `ASSIGNED_TO` nodes; legacy graph is Role/Process-heavy — may need **entity catalog projection** tranche first.
5. **Master-seq dependency** — operator chose Mirror → L3 → L2 → L1 → Neo4j; prod mirror apply still **PENDING-OPERATOR**.

---

## Credential-free work (can proceed now)

```powershell
py -c "from akos.hlk_graph_articulation import assert_edge_coverage; assert_edge_coverage()"
py scripts/validate_canonical_articulation.py
py -m pytest tests/test_validate_canonical_articulation.py -v
```

---

## Cross-references

- I91 blocked preflight: [`p1-neo4j-preflight-blocked-2026-06-01.md`](../../91-enterprise-graph-store-coverage/reports/p1-neo4j-preflight-blocked-2026-06-01.md)
- Operator ratification: [`i95-round2-operator-ratification-2026-06-09.md`](i95-round2-operator-ratification-2026-06-09.md)
- L2 graph bearer edge (pending): [`i95-l2-state-audit-2026-06-09.md`](i95-l2-state-audit-2026-06-09.md)
