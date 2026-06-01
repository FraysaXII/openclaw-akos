---
initiative_id: INIT-OPENCLAW_AKOS-91
title: "I91 — Enterprise Graph & Store-Coverage Mapping"
status: active
owner_role: PMO
inception: 2026-06-01
last_review: 2026-06-01
linked_decisions:
  - D-IH-91-A
language: en
linked_initiatives:
  - INIT-OPENCLAW_AKOS-90
  - INIT-OPENCLAW_AKOS-86
  - INIT-OPENCLAW_AKOS-07
program_anchors: PRJ-HOL-PGF-2026;PRJ-HOL-DAT-2026
---

# I91 — Enterprise Graph & Store-Coverage

> **Plan SSOT:** [`routing_and_wiring_788b66e3.plan.md`](file:///c:/Users/Shadow/.cursor/plans/routing_and_wiring_788b66e3.plan.md) §4 I91. **Prerequisite initiative:** [I07 Neo4j graph projection](../07-hlk-neo4j-graph-projection/master-roadmap.md) (closed; reuse scripts + explorer). **Coordinator:** [I86](../86-initiative-cluster-execution-coordinator/master-roadmap.md). **Routing ordnance:** [I90](../90-routing-and-wiring/master-roadmap.md).

## 0 — Purpose

Map **which Holistika stores** (git CSVs, Supabase mirrors, Neo4j graph, vault markdown, sibling repos) cover **which enterprise surfaces**, harden the graph projection path, and produce an operator-maintainable **store-coverage matrix** for cluster planning.

## 1 — Phase at a glance

| Phase | Purpose | Gate |
|:---|:---|:---|
| **P0** | Charter + store inventory + coverage matrix skeleton | — |
| **P1** | Neo4j connectivity preflight + `sync_hlk_neo4j.py` smoke | Operator `NEO4J_*` in `~/.openclaw/.env` |
| **P2** | Store-coverage matrix v1 (CSV + report) | — |
| **P3** | Graph explorer / MCP regression vs I07 baseline | Browser or API evidence optional |
| **P4** | Handoff to I92 ERP reassess (dashboard data joins) | I90 P3 + I91 P2 |

## 2 — Phase dependency

```mermaid
flowchart LR
  P0[P0 Charter]
  P1[P1 Neo4jPreflight]
  P2[P2 CoverageMatrix]
  P3[P3 GraphRegression]
  P4[P4 ERPHandoff]
  I90[I90 RuleRewire]

  I90 --> P0
  P0 --> P1
  P1 --> P2
  P2 --> P3
  P3 --> P4
```

## 3 — P0 — Charter (current)

**Deliverables (this expansion):**

- This `master-roadmap.md` (replaces GATE #1 stub).
- Forward: `decision-log.md`, `risk-register.md`, `files-modified.csv` on first material commit.

**Pre-flight 2026-06-01:** Neo4j driver not configured in agent session; P1 blocked until operator supplies credentials or runs sync locally per I07 D1.

**Verification (no graph required):**

```powershell
py scripts/validate_hlk.py
# When NEO4J_* present:
py scripts/sync_hlk_neo4j.py --dry-run
```

## 4 — Mechanical anchors (reuse, do not re-derive)

| Asset | Path |
|:---|:---|
| Sync runbook | [`scripts/sync_hlk_neo4j.py`](../../../scripts/sync_hlk_neo4j.py) |
| Graph MCP | [`scripts/hlk_graph_mcp_server.py`](../../../scripts/hlk_graph_mcp_server.py) |
| Explorer UI | [`static/hlk_graph_explorer.html`](../../../static/hlk_graph_explorer.html) |
| Vault links validator | [`scripts/validate_hlk_vault_links.py`](../../../scripts/validate_hlk_vault_links.py) |
| I07 closure UAT | [`../07-hlk-neo4j-graph-projection/reports/`](../07-hlk-neo4j-graph-projection/reports/) |

## 5 — Closure criteria (forward)

- Store-coverage matrix v1 checked into `reports/store-coverage-matrix-<date>.md` (or canonical CSV if promoted later).
- Neo4j sync smoke PASS with operator credentials (or documented SKIP with reason).
- I92 master-roadmap cites coverage matrix rows for ERP panel data sources.

## 6 — Cross-references

- [`docs/ARCHITECTURE.md`](../../../docs/ARCHITECTURE.md) — HLK graph + compliance mirror sections.
- [`akos-research-area.mdc`](../../../.cursor/rules/akos-research-area.mdc) — Research area map when coverage touches Intelligence surfaces.
