---
language: en
status: charter
initiative: 63-external-repo-governance-codification
report_kind: asset-classification
last_review: 2026-05-06
---

# Asset classification — Initiative 63

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md).

| Asset | Class | Authority | Notes |
|:---|:---|:---|:---|
| `process_list.csv` (3 new rows: blessing, drift remediation, schema propagation) | **Canonical** (proposed, not yet minted) | Founder + System Owner | Operator-gated edit; this ship produces the proposal report only. |
| `REPOSITORY_REGISTRY.csv` (3 new columns) | **Canonical** (proposed) | Founder + System Owner | Same gate as above. |
| `SOP-EXTERNAL_REPO_BLESSING_001.md` | **Canonical** (drafted, `status: review`) | Founder + System Owner | Promotion to `active` gated by P3-P5. |
| `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md` | **Canonical** (drafted, `status: review`) | Founder + System Owner | Same. |
| `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md` | **Canonical** (drafted, `status: review`) | Founder + System Owner | Same. |
| `_assets/techops/SOP-EXTERNAL_REPO_*.manifest.md` | **Canonical** (KM manifest stub) | Founder + System Owner | Stub only; topic backfill at P5. |
| This charter folder (`master-roadmap.md`, `decision-log.md`, `asset-classification.md`, `evidence-matrix.md`, `risk-register.md`, `reports/csv-proposal-2026-05-06.md`) | **Reference-only** | Initiative owner | Workspace-only; not load-bearing for runtime. |
| External Repo Bless Pattern automation (the 9 scripts + 12 templates) | **Mirrored / derived** | System Owner | Already shipped under I62 sibling; not re-classified here. |
