---
language: en
status: charter
initiative: 63-external-repo-governance-codification
report_kind: risk-register
last_review: 2026-05-06
---

# Risk register — Initiative 63

| Risk | Likelihood | Impact | Mitigation | Owner |
|:---|:---|:---|:---|:---|
| `process_list.csv` proposal stalls at operator review (P3) | Medium | Medium | The bless scaffolder reads the proposed columns defensively (defaults to `False` / empty). The pattern ships and works without canonical mint. | System Owner |
| New SOPs land at `status: review` but never get promoted to `active` | Medium | Low | Charter explicitly notes this is acceptable until process_list rows are minted. SOPs at `review` are still readable; they just don't get the cursor-rule pointer. | System Owner |
| Column names chosen in P3 differ from defensive defaults in `bless_external_repo.py` | Low | Medium | `load_registry()` already maps column names by `csv.DictReader`; renames at P4 require a one-line edit. Tests cover both scenarios. | Initiative owner |
| KM manifest stubs created at P2 reference unminted SOPs and break `validate_hlk_km_manifests.py` | Low | Medium | Stubs explicitly mark the SOPs as `status: review`; the validator already tolerates that. | System Owner |
| Mirror-rule extension at P6 lands before SOPs are `active` | Low | Low | P6 explicitly waits on P5; charter calls this out. | Initiative owner |
| New columns in `REPOSITORY_REGISTRY.csv` break the snapshot writer | Low | Medium | `snapshot_external_repos.py` already uses `DictWriter` with explicit fieldnames from `akos.hlk_repo_health_csv`; new registry columns don't propagate to the snapshot automatically. Future column additions to the snapshot are tracked in I63 P4 evidence. | System Owner |
