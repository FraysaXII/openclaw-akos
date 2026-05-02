-- Initiative 49 — persona_scenario_registry mirror: priority / safety columns
--
-- Mirrors PERSONA_SCENARIO_REGISTRY.csv fields added in D-IH-49-A.

ALTER TABLE compliance.persona_scenario_registry_mirror
  ADD COLUMN IF NOT EXISTS priority_score TEXT;

ALTER TABLE compliance.persona_scenario_registry_mirror
  ADD COLUMN IF NOT EXISTS safety_lane TEXT;

ALTER TABLE compliance.persona_scenario_registry_mirror
  ADD COLUMN IF NOT EXISTS release_blocking TEXT;

COMMENT ON COLUMN compliance.persona_scenario_registry_mirror.priority_score IS
  'I49 deterministic RICE-style score from akos.hlk_persona_scenario_priority; CSV string fixed to 6 decimal places.';
COMMENT ON COLUMN compliance.persona_scenario_registry_mirror.safety_lane IS
  'I49 operator flag true|false|null — pinned backlog lane for Tier-3 safety UCs.';
COMMENT ON COLUMN compliance.persona_scenario_registry_mirror.release_blocking IS
  'I49 operator flag true|false|null — active scenarios that gate release verdict.';

CREATE INDEX IF NOT EXISTS persona_scenario_registry_mirror_priority_idx
  ON compliance.persona_scenario_registry_mirror (priority_score DESC NULLS LAST);
