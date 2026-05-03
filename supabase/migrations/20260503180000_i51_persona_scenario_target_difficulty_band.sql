-- Initiative 51 P3 (D-IH-51-A) — persona_scenario_registry mirror:
-- target_difficulty_band column.
--
-- Mirrors PERSONA_SCENARIO_REGISTRY.csv field added in I51 P3 to formalize
-- per-persona calibration targets (closes R-47-2). Format is the literal
-- "<trivial>/<moderate>/<hard>/<impossible>" pp-string emitted by the CSV
-- (e.g., "15/40/35/10"); empty = fall through to the global D-IH-47-C
-- 40/40/10/10 default.
--
-- Per-persona consistency (every row of a given persona must share the same
-- target_difficulty_band value) is enforced by
-- scripts/validate_persona_scenario_registry.py — not by a column constraint
-- here, because mirror state always projects from CSV and the operator
-- workflow (CSV edit → mirror reseed) makes the validator the canonical
-- enforcement point.

ALTER TABLE compliance.persona_scenario_registry_mirror
  ADD COLUMN IF NOT EXISTS target_difficulty_band TEXT;

COMMENT ON COLUMN compliance.persona_scenario_registry_mirror.target_difficulty_band IS
  'I51 P3 D-IH-51-A — per-persona override of the global D-IH-47-C 40/40/10/10 calibration target. Format "<trivial>/<moderate>/<hard>/<impossible>" pp summing to 100; empty = global default fall-through. Per-persona consistency enforced by scripts/validate_persona_scenario_registry.py.';
