# OPS-86-15 mirror batches (auto-generated manifest)

source_git_sha: 989d32884dd76319879d729f2d2dc486293828b1

Apply in numeric order. **Preferred:** `pwsh -File scripts/apply_mirror_batches.ps1 -Preset ops8615` (linked `supabase db query --linked -f`). **Alternative:** psql per file. SQL Editor OK for 01–02 and 05 only.

| order | file | mirror | expected rows |
| --- | --- | --- | ---: |
| 01 | `01-aic_registry.sql` | `compliance.aic_registry_mirror` | 5 |
| 02 | `02-audience_registry.sql` | `compliance.audience_registry_mirror` | 9 |
| 03 | `03-capability_registry.sql` | `compliance.capability_registry_mirror` | 1119 |
| 04 | `04-capability_confidence_registry.sql` | `compliance.capability_confidence_registry_mirror` | 1119 |
| 05 | `05-country_work_calendar.sql` | `compliance.country_work_calendar_mirror` | 2 |
