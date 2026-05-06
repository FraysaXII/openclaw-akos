---
language: en
source_id: SOP-CROSS_REPO_SCHEMA_PROPAGATION_001
output_type: 1
title: "SOP — Cross-repo canonical schema propagation"
created: 2026-05-06
author_role: System Owner
topic_ids:
  - topic_holistik_ops_discovery
summary: >
  Propagate AKOS canonical CSV column changes to consuming external repos
  via TypeScript type regeneration plus Slack and gh-issue notifications,
  keeping consumers strictly typed against AKOS without invented IDs.
paths:
  sop: ../../Admin/O5-1/Envoy Tech Lab/Cross Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md
  excalidraw: null
access_level: 2
confidence: Safe
artifact_role: canonical
intellectual_kind: sop
related_process_ids:
  - PROC-CROSS_REPO_SCHEMA_PROPAGATION_001
file_sha256: ""
---
# Manifest: SOP-CROSS_REPO_SCHEMA_PROPAGATION_001

SOP authored in I63 P1 at `status: review`. Promotion to `status: active`
gated by I63 P3-P4 (canonical CSV mint of the three new
`REPOSITORY_REGISTRY.csv` columns and the three new `process_list.csv`
rows).

See [`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`](../../Admin/O5-1/Envoy%20Tech%20Lab/Cross%20Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md).
