-- Initiative 14 Wave B2 — OPTIONAL legacy public deprecation (maintenance window + backup first).
-- Adjust identifiers to match the target database. See deprecate-legacy-public-proposal.md

-- Example: legacy v2.4-shaped table name (quoted mixed-case)
-- ALTER TABLE IF EXISTS public."Process list" RENAME TO "Process list_deprecated_20260417";

-- Optional shim for apps still selecting from public name (uncomment and align columns to mirrors):
-- CREATE OR REPLACE VIEW public."Process list" AS
-- SELECT item_id, item_name, /* map columns as needed */ ...
-- FROM compliance.process_list_mirror;
