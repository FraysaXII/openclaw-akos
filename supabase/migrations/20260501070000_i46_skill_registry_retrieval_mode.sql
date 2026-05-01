-- Initiative 46 P5 — Add retrieval_mode column to compliance.skill_registry_mirror.
--
-- Per D-IH-46-A: SKILL_REGISTRY's retrieval_mode column drives whether a skill
-- routes through GraphRAG hybrid (use-case B) or stays on the current direct
-- chain. Empty default keeps all 5 existing skills back-compat. P3 PoC outcome
-- determines whether SKILL-MADEIRA-LOOKUP-V1 flips to retrieval_mode='graph_rag'
-- in P5 conditional ship.

ALTER TABLE compliance.skill_registry_mirror
  ADD COLUMN IF NOT EXISTS retrieval_mode TEXT;

COMMENT ON COLUMN compliance.skill_registry_mirror.retrieval_mode IS
  'I46 P5: empty (default) | vector_only | graph_rag | hybrid. Activates when I46 P3 PoC ships.';

CREATE INDEX IF NOT EXISTS skill_registry_mirror_retrieval_mode_idx
  ON compliance.skill_registry_mirror (retrieval_mode)
  WHERE retrieval_mode IS NOT NULL AND retrieval_mode <> '';
