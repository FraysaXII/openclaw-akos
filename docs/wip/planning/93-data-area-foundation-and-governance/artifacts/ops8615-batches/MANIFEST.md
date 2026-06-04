# OPS-86-15 mirror batches (auto-generated manifest)

source_git_sha: 7a529e6a3442f4f57332d3410122b593fb951b38

Apply in numeric order. Prefer **psql** for all files; SQL Editor is OK for 01–02 and 05 only.

| order | file | mirror | expected rows |
| --- | --- | --- | ---: |
| 01 | `01-aic_registry.sql` | `compliance.aic_registry_mirror` | 5 |
| 02 | `02-audience_registry.sql` | `compliance.audience_registry_mirror` | 9 |
| 03 | `03-capability_registry.sql` | `compliance.capability_registry_mirror` | 1119 |
| 04 | `04-capability_confidence_registry.sql` | `compliance.capability_confidence_registry_mirror` | 1119 |
| 05 | `05-country_work_calendar.sql` | `compliance.country_work_calendar_mirror` | 2 |
