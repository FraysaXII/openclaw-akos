# Research Backlog — Trello Registry (canonical index)

**Document owner**: PMO  
**Version**: 1.2  
**Date**: 2026-04-08  
**Status**: Final  

---

## Purpose

Canonical mapping from **external Trello board** `67697e19c67277de7ae1a85c` to Holistika **topic_id** candidates and **role_owner** hints. **Trello is not SSOT**; card descriptions and checklists are not copied here as authoritative prose. This file is the governed index for traceability and promotion planning.

**Board export:** Governed imports live under [imports/](imports/); use the **primary** export slice (card ids starting with `676993` for Research Material playlist cards, `676992` for MADEIRA list cards in the same file) when refreshing this table. See [imports/README.md](imports/README.md) for dual-export notes.

## Status values

| Status | Meaning |
|--------|---------|
| `candidate` | Not yet in wip synthesis |
| `in_wip` | Work in `docs/wip/` |
| `promoted_v3` | Case or SOP in `v3.0/` |
| `deferred` | Explicitly parked |

## Registry

Ids below were reconciled to the primary slice [imports/trello_board_67697e19_primary.json](imports/trello_board_67697e19_primary.json) (Research Material / MADEIRA lists).

| trello_card_id | list (typical) | card name | suggested topic_id | suggested role_owner | status | notes |
|----------------|----------------|-----------|-------------------|----------------------|--------|-------|
| 67699325c36ae35b88747a30 | Research Material | Research Material | topic_research_pipeline | Holistik Researcher | in_wip | Pipeline checklist: process, channels, MADEIRA, scrape, data governance, KMS UI — [wip synthesis](../../../../../../../wip/hlk-km/research-synthesis-research-pipeline.md) |
| 676993277253135f01d5d95e | Research Material | Office Automation | topic_office_automation | PMO | candidate | YouTube playlist link on card |
| 676993287efead30a968408e | Research Material | People | topic_people_research | CPO | candidate | Playlist |
| 676993288a2d6fa5d743649e | Research Material | Security & Intelligence | topic_security_intelligence | Holistik Researcher | candidate | Playlist |
| 67699329fefb5c8b58d8a9d9 | Research Material | Design | topic_design_research | Brand Manager | candidate | Playlist |
| 67699329d8c0958ff8311f6e | Research Material | System Design | topic_system_design_research | Tech Lead | candidate | Playlist |
| 676993295672e3a8c21169ea | Research Material | Content & Channel Strategy | topic_content_channel_strategy | Growth Manager | candidate | Playlist |
| 6769932a916c78afe2611081 | Research Material | Macro Economists & Investments | topic_macro_investment_research | Business Controller | in_wip | [wip synthesis](../../../../../../../wip/hlk-km/research-synthesis-macro-investment.md) |
| 6769932a2e14f16f0004e6cd | Research Material | AI | topic_ai_landscape_research | AI Engineer | in_wip | [wip synthesis](../../../../../../../wip/hlk-km/research-synthesis-ai-landscape.md) |
| 6769932b297f4ab43c8b53d7 | Research Material | Politics | topic_politics_research | Holistik Researcher | candidate | Playlist |
| 6769932b3b3baacaa104a7ef | Research Material | Social | topic_social_research | Holistik Researcher | candidate | Playlist |
| 6769932b21a84a9e94c642fa | Research Material | Logic | topic_logic_research | Compliance | candidate | Playlist |
| 6769932ce223d38514d3fc5c | Research Material | Legal | topic_legal_research | Legal Counsel | in_wip | [wip synthesis](../../../../../../../wip/hlk-km/research-synthesis-legal-research.md) |
| 6769932c0ecd2c833c05ab04 | Research Material | UX - Customer Relationship | topic_ux_crm_research | UX Designer | candidate | Playlist |
| 676992d120f3b43df103aac7 | MADEIRA Project | Research - Topics on Radar | topic_madeira_research_radar | Product Owner | in_wip | Nested checklists — [wip synthesis](../../../../../../../wip/hlk-km/research-synthesis-madeira-radar.md) |
| 676992dcb64b6e72a6a4b0d3 | MADEIRA Project | PMO - Product Owner - Product Timeline | topic_madeira_product_timeline | Product Owner | candidate | Planning phase checklist items map to process candidates |

## Maintenance

1. On board change, update rows; never delete history without a decision log entry in `docs/wip/planning/03-hlk-km-knowledge-base/reports/`.  
2. When a topic promotes to v3.0, set `promoted_v3` and link the knowledge index path.  
3. New `process_list.csv` rows require operator approval per governance rules.

## Related

- [HLK_KM_TOPIC_FACT_SOURCE.md](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md)  
- [master-roadmap.md](../../../../../../../../wip/planning/03-hlk-km-knowledge-base/master-roadmap.md)  
- [imports/README.md](imports/README.md)  
