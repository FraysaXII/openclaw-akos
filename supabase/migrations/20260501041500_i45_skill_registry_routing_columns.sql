-- Initiative 45 P3 — Add routing_condition + tools_required_waived to
-- compliance.skill_registry_mirror.
--
-- Per D-IH-45-A: SKILL_REGISTRY becomes the routing-decision substrate (not
-- just the metadata catalog). The 4-field minimum registry contract from the
-- Abstract Algorithms 2026 piece (skill_id, input_schema, routing_condition,
-- eval_hook) requires routing_condition; we add it now (input_schema lands in
-- I47 if needed). tools_required_waived closes R-45-6 by letting a skill
-- explicitly opt out of the tools_required vs agent-capabilities.json
-- reconciliation warning (see scripts/validate_skill_registry.py).
--
-- Both columns are nullable / default empty for back-compat with the existing
-- 5 rows (most have routing_condition explicitly populated by I45 P3 reseed,
-- but defensive nullable keeps replays of older mirror data safe).

ALTER TABLE compliance.skill_registry_mirror
  ADD COLUMN IF NOT EXISTS routing_condition       TEXT,
  ADD COLUMN IF NOT EXISTS tools_required_waived   BOOLEAN NOT NULL DEFAULT false;

COMMENT ON COLUMN compliance.skill_registry_mirror.routing_condition IS
  'I45 P3: empty | intent_in=R1;R2 | intent=R | agent=A. Empty = always-eligible.';
COMMENT ON COLUMN compliance.skill_registry_mirror.tools_required_waived IS
  'I45 P3 (R-45-6): true = skip the tools_required vs agent-capabilities.json reconciliation warning.';

CREATE INDEX IF NOT EXISTS skill_registry_mirror_routing_condition_idx
  ON compliance.skill_registry_mirror (routing_condition)
  WHERE routing_condition IS NOT NULL AND routing_condition <> '';
