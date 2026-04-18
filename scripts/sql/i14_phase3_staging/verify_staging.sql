-- Initiative 14 §8 — verification (run after DDL + mirror sync on staging)

SELECT COUNT(*) AS process_rows, MAX(synced_at) AS last_sync
FROM compliance.process_list_mirror;

SELECT COUNT(*) AS org_rows FROM compliance.baseline_organisation_mirror;

SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname IN ('compliance', 'holistika_ops')
ORDER BY schemaname, tablename;

-- Expect rowsecurity = true for the four mirror / holistika_ops tables
-- Spot-check Initiative 14 anchors (after sync from git):
-- SELECT item_id FROM compliance.process_list_mirror
-- WHERE item_id IN ('holistika_gtm_dtp_001','holistika_gtm_dtp_002','holistika_gtm_dtp_003');
