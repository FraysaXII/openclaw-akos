-- I95 EG-2 (D-IH-95-G / DB-03): kirbe.kirbe_organizations already had policies {kirbe_orgs_read,kirbe_orgs_write}
-- but RLS was never enabled, leaving the policies inert (policy_exists_rls_disabled ERROR).
-- Applied to remote MasterData (swrmqpelgoblaquequzb) via MCP apply_migration on 2026-06-07.
-- Enabling activates the existing access model and clears the last security ERROR.
ALTER TABLE kirbe.kirbe_organizations ENABLE ROW LEVEL SECURITY;
