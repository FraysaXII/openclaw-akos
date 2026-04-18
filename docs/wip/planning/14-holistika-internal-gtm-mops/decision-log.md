# Decision log — Initiative 14 (Holistika internal GTM / marketing ops)

| ID | Question | Options | Decision | Status |
|----|----------|---------|----------|--------|
| D-GTM-0-1 | North-star metric (90 days) | Qualified meetings / pipeline $ / inbound SQLs | **Deferred** — record in [`reports/phase-0-charter.md`](reports/phase-0-charter.md) when chosen | open |
| D-GTM-0-2 | Primary segment for first proof | Innovators / agencies / SME operational excellence | **Deferred** — charter | open |
| D-GTM-1-1 | Merge `process_list.csv` tranche from [`candidates/process_list_tranche_holistika_internal.csv`](candidates/process_list_tranche_holistika_internal.csv) | Approve + `py scripts/merge_process_list_tranche.py --write` / reject / revise | **Merged** 2026-04-17 — `holistika_gtm_dtp_001`–`003`; `validate_hlk.py` PASS | done |
| D-GTM-3-1 | Supabase DDL (mirrors, `holistika_ops`, deprecations) | Approve written `reports/sql-proposal-*.md` then apply via migrations | **Pending** — see [`reports/sql-proposal-stack-20260417.md`](reports/sql-proposal-stack-20260417.md) | blocked |
| D-GTM-A3 | CSV → mirror upsert SQL | Manual paste / CI / [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py) | **Script added** — run `--output` after B1 DDL on staging; not a substitute for operator SQL gate | done |
