---
language: en
status: proposal
initiative: 65-akos-planning-workspace-panel
report_kind: sql-proposal
authored: 2026-05-19
last_review: 2026-05-19
parent_lane: I86 Wave I Lane I-D
linked_decisions: [D-IH-65-A, D-IH-65-D]
---

# SQL proposal — I65 P4 governance views (Decision Atlas + Ops Queue)

> **Inline-ratify gate** per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate". Pure read-only views in the **already-approved** `governance.*` schema (D-IH-65-A). No new tables, no new RLS policies, no new PII surfaces. Same `SECURITY INVOKER` posture as `governance.planning_workspace_view` shipped in [`20260508010100_i65_p1_governance_planning_workspace.sql`](../../../../supabase/migrations/20260508010100_i65_p1_governance_planning_workspace.sql).

## 1. Scope

Two new views power the I65 P4 routes (`/operator/planning/decisions` Decision Atlas + `/operator/planning/operations` Ops Queue) shipped under I86 Wave I Lane I-D Option C:

1. `governance.planning_decisions_view` — every row in `compliance.decision_register_mirror` joined with parent initiative metadata, for cross-initiative decision browsing + class/status filters.
2. `governance.planning_ops_view` — every row in `compliance.ops_register_mirror` joined with parent initiative metadata, RICE-ranked, for cross-initiative ops queue.

**Reports Stream** (`/operator/planning/reports`) needs **no DB view** — markdown lives at GitHub per D-IH-65-B; the existing `lib/planning/github-reader.ts` lists per-initiative `reports/` folders via cached Contents API calls.

## 2. Proposed DDL

```sql
-- I65 P4 — governance.planning_decisions_view + planning_ops_view
-- D-IH-65-A: governance.* schema is approved for view-shaped projections.
-- D-IH-65-D: SECURITY INVOKER — service_role reads via hlk-erp planning fetcher;
--           authenticated/anon are denied at the underlying mirror RLS.

CREATE OR REPLACE VIEW governance.planning_decisions_view AS
SELECT
  d.decision_id,
  d.title,
  d.initiating_initiative_id,
  d.linked_initiative_ids,
  d.linked_ops_action_ids,
  d.decision_class,
  d.status                       AS decision_status,
  d.reversibility,
  d.decided_at,
  d.decision_log_path,
  d.supersedes_decision_id,
  d.summary,
  d.notes                        AS decision_notes,
  i.title                        AS initiative_title,
  i.status                       AS initiative_status,
  i.folder_path                  AS initiative_folder_path,
  i.owner_role                   AS initiative_owner_role,
  d.synced_at
FROM compliance.decision_register_mirror d
LEFT JOIN compliance.initiative_registry_mirror i
  ON i.initiative_id = d.initiating_initiative_id;

COMMENT ON VIEW governance.planning_decisions_view IS
  'I65 P4 — cross-initiative decision atlas. Joined view for /operator/planning/decisions; live computed from decision_register_mirror + initiative_registry_mirror.';

GRANT SELECT ON governance.planning_decisions_view TO authenticated, service_role;


CREATE OR REPLACE VIEW governance.planning_ops_view AS
SELECT
  o.ops_action_id,
  o.title,
  o.originating_initiative_id,
  o.forwarded_to_initiative_id,
  o.owner_class,
  o.owner_role,
  o.status                       AS ops_status,
  o.rice_reach,
  o.rice_impact,
  o.rice_confidence_pct,
  o.rice_effort_person_weeks,
  o.rice_score,
  o.gate_id,
  o.linked_decision_ids,
  o.summary,
  o.operator_runbook_path,
  o.evidence_path,
  o.opened_at,
  o.closed_at,
  o.notes                        AS ops_notes,
  i.title                        AS initiative_title,
  i.status                       AS initiative_status,
  i.folder_path                  AS initiative_folder_path,
  o.synced_at
FROM compliance.ops_register_mirror o
LEFT JOIN compliance.initiative_registry_mirror i
  ON i.initiative_id = o.originating_initiative_id;

COMMENT ON VIEW governance.planning_ops_view IS
  'I65 P4 — cross-initiative ops queue. Joined view for /operator/planning/operations; RICE-ranked at query time via ORDER BY rice_score DESC.';

GRANT SELECT ON governance.planning_ops_view TO authenticated, service_role;

NOTIFY pgrst, 'reload schema';
```

## 3. Security posture

- **No new tables**. Both views read from existing mirrors that already deny `authenticated` + `anon` reads via RLS.
- **`SECURITY INVOKER`** (PostgreSQL default for views) — RLS of the underlying mirrors is honoured. `authenticated` / `anon` callers get zero rows; `service_role` (hlk-erp planning fetcher) gets full rows.
- **Operator gate** = `requireLevel(4)` at the route layer (already enforced for `/planning/*`).
- **No PII / financial / counterparty data**. Decisions + ops are governance metadata.

## 4. Rollback

```sql
DROP VIEW IF EXISTS governance.planning_decisions_view;
DROP VIEW IF EXISTS governance.planning_ops_view;
```

Both views are stateless (no data of their own); rollback is a single transaction. No mirror data is mutated.

## 5. Inline-ratify shape

Three options for operator approval:

| Option | Shape | Rationale |
|:---|:---|:---|
| **A** (recommended) | Both views as proposed (decisions + ops) | Mirrors the existing `planning_workspace_view` pattern; minimal scope; matches the I65 P4 plan; live computed (no materialisation cost). |
| **B** | Decisions view only (defer ops view) | Reduces SQL footprint; ops queue could reuse `planning_workspace_view` with a UI-side ranking pass. Trade-off: ops queue UI loses RICE-ranked cross-initiative listing without a view, requiring a heavier client-side filter+sort over all rows. |
| **C** | Materialised views (instead of regular views) | Lower query latency for atlas/queue at scale (>10k decisions). Trade-off: needs a refresh strategy (cron / trigger); not justified at current registry size (~330 decisions, ~30 ops); over-engineering. |

## 6. Verification

- `py scripts/verify.py compliance_mirror_emit` — unaffected (mirror tables unchanged).
- Post-apply: `SELECT * FROM governance.planning_decisions_view LIMIT 5;` (manual SELECT via MCP or `serve-api`).
- hlk-erp Playwright e2e: `pnpm test:e2e -- --grep planning-atlas-stream-queue` (P4 verification per master-roadmap).

## 7. Cross-references

- Sister view: [`governance.planning_workspace_view`](../../../../supabase/migrations/20260508010100_i65_p1_governance_planning_workspace.sql) (same shape; same security posture).
- Mirror tables: [`compliance.decision_register_mirror`](../../../../supabase/migrations/20260508010000_i65_p1_decision_register_mirror.sql) + [`compliance.ops_register_mirror`](../../../../supabase/migrations/20260506120200_i59_ops_register_mirror.sql).
- Master-roadmap §"P4 Atlas + Queue + Stream": [`master-roadmap.md`](../master-roadmap.md).
- Cursor rule: [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate".
