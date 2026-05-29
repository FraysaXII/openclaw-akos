---
intellectual_kind: topic_registry_promotion_staging
sharing_label: internal_only
status: promoted_operator_gate_cleared_2026-05-29
authored: 2026-05-29
last_review: 2026-05-29
ratifying_decisions:
  - D-IH-75-G
gate: canonical-CSV — operator promotes rows into TOPIC_REGISTRY.csv; do NOT commit this file as SSOT
source_index: docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md
target_csv: docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv
---

# TOPIC_REGISTRY promotion staging (D2 — Trello → topic_id)

> **Gate:** These rows are **staged only**. Promotion into `TOPIC_REGISTRY.csv` requires the
> operator canonical-CSV gate per `akos-governance-remediation.mdc`. After promotion: mint
> matching `.manifest.md` under `_assets/` per Initiative 25 convention.

## Rows ready for promotion (status `candidate` in Trello index; not yet in TOPIC_REGISTRY)

Copy-paste block for operator review (18-column schema):

```csv
topic_id,title,topic_class,lifecycle_status,primary_owner_role,program_id,plane,parent_topic,related_topics,depends_on,subsumes,subsumed_by,manifest_path,notes,last_review_at,last_review_by,last_review_decision_id,methodology_version_at_review
topic_office_automation,Office Automation research playlist,methodology_map,candidate,PMO,shared,shared,,,,,,docs/wip/intelligence/topic-office-automation/topic_office_automation.manifest.md,Trello 676993277253135f01d5d95e; manifest forward-charter,2026-05-29,PMO,D-IH-75-G,v3.2
topic_people_research,People research playlist,methodology_map,candidate,CPO,shared,shared,,,,,,docs/wip/intelligence/topic-people-research/topic_people_research.manifest.md,Trello 676993287efead30a968408e,2026-05-29,PMO,D-IH-75-G,v3.2
topic_security_intelligence,Security & Intelligence research playlist,methodology_map,candidate,Holistik Researcher,shared,shared,,,,,,docs/wip/intelligence/topic-security-intelligence/topic_security_intelligence.manifest.md,Trello 676993288a2d6fa5d743649e,2026-05-29,PMO,D-IH-75-G,v3.2
topic_design_research,Design research playlist,methodology_map,candidate,Brand Manager,shared,shared,,,,,,docs/wip/intelligence/topic-design-research/topic_design_research.manifest.md,Trello 67699329fefb5c8b58d8a9d9,2026-05-29,PMO,D-IH-75-G,v3.2
topic_system_design_research,System Design research playlist,methodology_map,candidate,Tech Lead,shared,shared,,,,,,docs/wip/intelligence/topic-system-design-research/topic_system_design_research.manifest.md,Trello 67699329d8c0958ff8311f6e,2026-05-29,PMO,D-IH-75-G,v3.2
topic_content_channel_strategy,Content & Channel Strategy research playlist,methodology_map,candidate,Growth Manager,shared,shared,,,,,,docs/wip/intelligence/topic-content-channel-strategy/topic_content_channel_strategy.manifest.md,Trello 676993295672e3a8c21169ea,2026-05-29,PMO,D-IH-75-G,v3.2
topic_politics_research,Politics research playlist,methodology_map,candidate,Holistik Researcher,shared,shared,,,,,,docs/wip/intelligence/topic-politics-research/topic_politics_research.manifest.md,Trello 6769932b297f4ab43c8b53d7,2026-05-29,PMO,D-IH-75-G,v3.2
topic_social_research,Social research playlist,methodology_map,candidate,Holistik Researcher,shared,shared,,,,,,docs/wip/intelligence/topic-social-research/topic_social_research.manifest.md,Trello 6769932b3b3baacaa104a7ef,2026-05-29,PMO,D-IH-75-G,v3.2
topic_logic_research,Logic research playlist,methodology_map,candidate,Compliance,shared,shared,,,,,,docs/wip/intelligence/topic-logic-research/topic_logic_research.manifest.md,Trello 6769932b21a84a9e94c642fa,2026-05-29,PMO,D-IH-75-G,v3.2
topic_ux_crm_research,UX - Customer Relationship research playlist,methodology_map,candidate,UX Designer,shared,shared,,,,,,docs/wip/intelligence/topic-ux-crm-research/topic_ux_crm_research.manifest.md,Trello 6769932c0ecd2c833c05ab04,2026-05-29,PMO,D-IH-75-G,v3.2
topic_madeira_product_timeline,MADEIRA Product Timeline (PMO checklist),methodology_map,candidate,Product Owner,PRJ-HOL-INF-2026,techops,,topic_madeira_research_radar,,,,docs/wip/intelligence/topic-madeira-product-timeline/topic_madeira_product_timeline.manifest.md,Trello 676992dcb64b6e72a6a4b0d3,2026-05-29,PMO,D-IH-75-G,v3.2
```

## Already in WIP (promote when manifest + operator gate ready)

| topic_id | Trello status | WIP synthesis path |
|:---|:---|:---|
| `topic_research_pipeline` | in_wip | `docs/wip/intelligence/topic-research-pipeline/` |
| `topic_macro_investment_research` | in_wip | `docs/wip/intelligence/topic-macro-investment-research/` |
| `topic_ai_landscape_research` | in_wip | `docs/wip/intelligence/topic-ai-landscape-research/` |
| `topic_legal_research` | in_wip | `docs/wip/intelligence/topic-legal-research/` |
| `topic_madeira_research_radar` | in_wip | `docs/wip/intelligence/topic-madeira-research-radar/` |

## Verification after operator promotion

```powershell
py scripts/validate_hlk.py
py scripts/validate_hlk_km_manifests.py
```
