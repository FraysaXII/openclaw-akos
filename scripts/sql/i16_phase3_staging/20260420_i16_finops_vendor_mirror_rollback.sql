-- Initiative 16 rollback — FINOPS vendor register mirror (operator use only)

DROP POLICY IF EXISTS finops_vendor_register_mirror_deny_authenticated ON compliance.finops_vendor_register_mirror;
DROP POLICY IF EXISTS finops_vendor_register_mirror_deny_anon ON compliance.finops_vendor_register_mirror;

DROP TABLE IF EXISTS compliance.finops_vendor_register_mirror;
