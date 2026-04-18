-- Initiative 14 Phase 3 — rollback (DESTRUCTIVE). Staging / operator-approved use only.

DROP POLICY IF EXISTS process_list_mirror_deny_authenticated ON compliance.process_list_mirror;
DROP POLICY IF EXISTS process_list_mirror_deny_anon ON compliance.process_list_mirror;
DROP POLICY IF EXISTS baseline_org_mirror_deny_authenticated ON compliance.baseline_organisation_mirror;
DROP POLICY IF EXISTS baseline_org_mirror_deny_anon ON compliance.baseline_organisation_mirror;
DROP POLICY IF EXISTS holistika_stripe_link_deny_authenticated ON holistika_ops.stripe_customer_link;
DROP POLICY IF EXISTS holistika_stripe_link_deny_anon ON holistika_ops.stripe_customer_link;
DROP POLICY IF EXISTS holistika_billing_deny_authenticated ON holistika_ops.billing_account;
DROP POLICY IF EXISTS holistika_billing_deny_anon ON holistika_ops.billing_account;

ALTER TABLE IF EXISTS compliance.process_list_mirror DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS compliance.baseline_organisation_mirror DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS holistika_ops.stripe_customer_link DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS holistika_ops.billing_account DISABLE ROW LEVEL SECURITY;

DROP TABLE IF EXISTS holistika_ops.billing_account CASCADE;
DROP TABLE IF EXISTS holistika_ops.stripe_customer_link CASCADE;
DROP SCHEMA IF EXISTS holistika_ops CASCADE;

DROP TABLE IF EXISTS compliance.process_list_mirror CASCADE;
DROP TABLE IF EXISTS compliance.baseline_organisation_mirror CASCADE;
DROP SCHEMA IF EXISTS compliance CASCADE;
