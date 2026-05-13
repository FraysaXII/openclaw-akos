-- Parity: scripts/sql/i70/20260513_p85_goipoi_stance_and_class_extension_up.sql (none — direct apply per I70 P8.5 atomic discipline)
-- I70 P8 §8.17 (P8.5) — extend goipoi_register_mirror with stance column + tighten class enum CHECK
--
-- Rationale (D-IH-70-AC + D-IH-70-AD, operator ratification 2026-05-13):
--   The P8.5 GOI class regression hunt produced 4 new class enum values + 1 new
--   ratify-by-deferring (business-developer-collaborator → I72 persona registry)
--   + 1 new schema dimension (stance: ally/neutral/enemy/unknown).
--
--   D-IH-70-AC ratifies the class enum extension (and pre-emptive additions for
--   recruiter / regulator / media counterpart rows that may not have concrete
--   instances today but will appear during normal operator engagement).
--
--   D-IH-70-AD is the *architectural* decision: a new `stance` column codifies
--   the operator's v2.7 ally/neutral/enemy doctrine ("to allies you give value;
--   to neutrals you give x for revenue without beta/alpha; to enemies, you
--   never let them pay you and if they do, make project valuable enough to
--   warrant sharing capabilities"). The column powers IntelligenceOps queries
--   that score relationship posture independently of distance_band. See
--   docs/references/hlk/v3.0/Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md
--   for the canonical doctrine.
--
--   Schema choice (single column, not bidirectional): the operator's v2.7
--   framing classifies entities mutually (one stance per row); engagement
--   posture rules infer what we offer to them based on this single value.
--   A bidirectional split (their stance toward us vs ours toward them) is
--   deferred until concrete divergence cases land; this is the v3.1
--   methodology versioning posture inherited from D-IH-70-Z + D-IH-70-AA.
--
-- Pattern follows 20260511030000_release_gate_hygiene_baseline_rates.sql for
-- additive nullable columns and 20260430210000_i31_goipoi_distance_extension*.sql
-- for the NOT VALID + VALIDATE CONSTRAINT enum guard.

-- Part 1 — stance column (additive, nullable, enum-checked)

ALTER TABLE compliance.goipoi_register_mirror
  ADD COLUMN IF NOT EXISTS stance TEXT;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'goipoi_register_mirror_stance_check'
  ) THEN
    ALTER TABLE compliance.goipoi_register_mirror
      ADD CONSTRAINT goipoi_register_mirror_stance_check
      CHECK (stance IS NULL OR stance = '' OR stance IN ('ally', 'neutral', 'enemy', 'unknown'))
      NOT VALID;

    ALTER TABLE compliance.goipoi_register_mirror
      VALIDATE CONSTRAINT goipoi_register_mirror_stance_check;
  END IF;
END $$;

-- Helpful covering index for "all allies" / "all enemies" governance queries.
CREATE INDEX IF NOT EXISTS goipoi_register_mirror_stance_idx
  ON compliance.goipoi_register_mirror (stance)
  WHERE stance IS NOT NULL AND stance <> '';

-- Part 2 — class enum CHECK (additive; widens to include new I70 P8.5 values)
--
-- The class column was previously plain TEXT with no constraint. Adding a
-- check now is a tightening that does not break any existing row because the
-- enum below is a strict superset of every value currently present in the
-- canonical CSV (verified at 2026-05-13: external_adviser, banking_channel,
-- client_org, partner — all present below).
--
-- The validator script scripts/validate_goipoi_register.py keeps the broader
-- list (Initiative 22 P4 extension) in lockstep; this CHECK reflects the
-- runtime guard that mirrors what the validator enforces at edit time.

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'goipoi_register_mirror_class_check'
  ) THEN
    ALTER TABLE compliance.goipoi_register_mirror
      ADD CONSTRAINT goipoi_register_mirror_class_check
      CHECK (class IS NULL OR class = '' OR class IN (
        -- Original Initiative 21 set
        'external_adviser', 'banking_channel', 'supplier', 'research_benchmark',
        'lead', 'client_org', 'collaborator', 'public_authority', 'other',
        -- Initiative 22 P4 extension (D-IH-5)
        'client', 'partner', 'investor', 'regulator', 'vendor', 'media',
        -- Initiative 70 P8.5 extension (D-IH-70-AC)
        'legal_counsel_external', 'supplier_infrastructure',
        'competitor_intelligence_target', 'recruiter'
      ))
      NOT VALID;

    ALTER TABLE compliance.goipoi_register_mirror
      VALIDATE CONSTRAINT goipoi_register_mirror_class_check;
  END IF;
END $$;
