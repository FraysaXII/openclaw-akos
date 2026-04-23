# Evidence matrix — Initiative 16

| Gate | Artifact | Evidence |
|------|----------|----------|
| CSV SSOT | `FINOPS_VENDOR_REGISTER.csv` | Git + `validate_finops_vendor_register.py` |
| Process baseline | `process_list.csv` | `thi_finan_ws_4`, `thi_finan_dtp_303`–`307`; `validate_hlk.py` |
| Vault SOP | `SOP-HLK_FINOPS_VENDOR_REGISTER_MAINTENANCE_001.md` | v3.0 Finance / Business Controller |
| Mirror DDL | `scripts/sql/i16_phase3_staging/*_up.sql` | Staging pack; operator apply |
| Sync contract | `sync_compliance_mirrors_from_csv.py --finops-vendor-register-only` | Generated upsert SQL |
| Precedence | `PRECEDENCE.md` | Canonical + mirrored rows |
| SQL intent | `sql-proposal-stack-20260417.md` §7 | Operator documentation |
| ERP | `HLK_ERP_FRONTEND_HANDOFF_FINOPS_MIRROR.md` | Server-only consumption |
