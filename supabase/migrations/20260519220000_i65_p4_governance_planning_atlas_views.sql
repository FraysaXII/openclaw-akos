-- I65 P4 — governance.planning_decisions_view + planning_ops_view
--
-- Per docs/wip/planning/65-akos-planning-workspace-panel/reports/sql-proposal-i65-p4-2026-05-19.md
-- (operator inline-ratify Option A at 2026-05-19; closure decision D-IH-86-AQ).
--
-- Powers I65 P4 atlas/queue routes shipped under I86 Wave I Lane I-D (Option C):
--   /operator/planning/decisions  -> governance.planning_decisions_view
--   /operator/planning/operations -> governance.planning_ops_view
--
-- D-IH-65-A: governance.* schema is approved for view-shaped projections; first
--            instantiated by 20260508010100_i65_p1_governance_planning_workspace.sql.
-- D-IH-65-D: SECURITY INVOKER (PostgreSQL default for views) — service_role reads
--            via hlk-erp planning fetcher; authenticated/anon callers see zero rows
--            because the underlying mirror tables (compliance.decision_register_mirror
--            + compliance.ops_register_mirror + compliance.initiative_registry_mirror)
--            all carry RLS-deny policies for non-service_role principals.
--
-- Route layer (requireLevel(4)) is the operator gate; this DDL adds zero new
-- attack surface beyond what the existing planning_workspace_view already exposes.

-- =============================================================================
-- governance.planning_decisions_view
--   Cross-initiative decision atlas. Joined view for /operator/planning/decisions.
-- =============================================================================

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
  'I65 P4 — cross-initiative decision atlas. Joined view for /operator/planning/decisions; live computed from decision_register_mirror + initiative_registry_mirror; SECURITY INVOKER inherits mirror RLS.';

GRANT SELECT ON governance.planning_decisions_view TO authenticated, service_role;

-- =============================================================================
-- governance.planning_ops_view
--   Cross-initiative ops queue, RICE-rankable. Joined view for /operator/planning/operations.
-- =============================================================================

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
  'I65 P4 — cross-initiative ops queue. Joined view for /operator/planning/operations; RICE-ranked at query time via ORDER BY rice_score DESC NULLS LAST; SECURITY INVOKER inherits mirror RLS.';

GRANT SELECT ON governance.planning_ops_view TO authenticated, service_role;

NOTIFY pgrst, 'reload schema';
