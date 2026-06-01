# GATE #1 — Registry mint proposal (I90 P0)

> **APPLIED 2026-06-01** — operator approved full package via AskQuestion. `validate_hlk` OVERALL PASS after `decision_class` fix on D-IH-90-E,G,K,L,S (`process` → `execution`). Per **D-IH-90-V** + plan §12 GATE #1.

## 1 — INITIATIVE_REGISTRY.csv (3 append rows)

| initiative_id | folder_path | title | status | inception_decision_id | program_anchors | notes |
|:---|:---|:---|:---|:---|:---|:---|
| INIT-OPENCLAW_AKOS-90 | docs/wip/planning/90-routing-and-wiring/ | I90 — Routing & Wiring (Ordnance) | active | D-IH-90-A | PRJ-HOL-PGF-2026;PRJ-HOL-OPS-2026 | Cluster tranche A ordnance; I86 sibling |
| INIT-OPENCLAW_AKOS-91 | docs/wip/planning/91-enterprise-graph-store-coverage/ | I91 — Enterprise Graph & Store-Coverage Mapping | active | D-IH-91-A | PRJ-HOL-PGF-2026;PRJ-HOL-DAT-2026 | Neo4j + coverage matrix; follows I90 P2 |
| INIT-OPENCLAW_AKOS-92 | docs/wip/planning/92-hlk-erp-reassess-dashboard/ | I92 — HLK-ERP Reassess & Dashboard | active | D-IH-92-A | PRJ-HOL-PGF-2026;PRJ-HOL-OPS-2026 | ERP panels + reassess; parallel after I90 P1 |

Common columns: `repo_slug=openclaw-akos`, `owner_role=PMO`, `inception_date=2026-06-01`, `last_review=2026-06-01`, `cadence=event_driven`, `gated_on=`, `operator_action=`, `manifests_processes=` (empty at P0), `linked_topic_ids=`, `methodology_version_at_review=v3.1`.

**Note:** `D-IH-91-A` and `D-IH-92-A` are **inception decisions for I91/I92** — minted at this GATE so INIT rows FK-resolve; full decision sets (B..I / B..G) land at I91/I92 P0 commits per plan §10.

## 2 — DECISION_REGISTER.csv (append — I90 charter set)

Append **D-IH-90-A** through **D-IH-90-V** (22 rows) with `initiating_initiative_id=INIT-OPENCLAW_AKOS-90`, `decision_class` mix architecture/process, `status=active`, `reversibility=low` (except D-IH-90-Q forward-charter → `medium`), `decision_log_path=docs/wip/planning/90-routing-and-wiring/decision-log.md`, summaries from [`decision-log.md`](../decision-log.md).

Also append **minimal inception rows**:

| decision_id | title | initiating_initiative_id |
|:---|:---|:---|
| D-IH-91-A | Charter I91 enterprise graph + store-coverage initiative | INIT-OPENCLAW_AKOS-91 |
| D-IH-92-A | Charter I92 HLK-ERP reassess + dashboard initiative | INIT-OPENCLAW_AKOS-92 |

## 3 — OPS_REGISTER.csv (proposed status edits)

| ops_id | Current | Proposed | Rationale |
|:---|:---|:---|:---|
| OPS-86-3 | open | **done** | `program_anchors` column + migration + validator shipped |
| OPS-86-16 | open | **done** | `artifact_class_registry_mirror` exists in Supabase + emit + validator |
| OPS-86-17 | open | **done** | `component_primitive_registry_mirror` exists + emit + validator |
| OPS-86-23 | open | open | Refresh notes only (DIM-04 stale list) — separate note edit |
| OPS-86-26 | open | open | No change at P0 |

## 4 — docs/wip/planning/README.md

Add index rows **90**, **91**, **92** pointing to new folders (mirror style of row 89).

## 5 — Post-approval verification commands

```powershell
py scripts/validate_hlk.py
py scripts/validate_initiative_registry.py
py scripts/validate_decision_register.py
py scripts/validate_ops_register.py
```

## 6 — I86 coordinator note (non-CSV)

Append one line to I86 `INITIATIVE_REGISTRY` **notes** cell: *"I90/I91/I92 routing cluster chartered 2026-06-01 (D-IH-90-A)."* — optional same commit.
