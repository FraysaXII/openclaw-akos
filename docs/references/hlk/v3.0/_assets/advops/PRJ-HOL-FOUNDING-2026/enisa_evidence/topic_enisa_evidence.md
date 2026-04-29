# Topic: ENISA evidence pack (`PRJ-HOL-FOUNDING-2026`)

**source_id**: `topic_enisa_evidence`  
**topic_id**: `topic_enisa_evidence`  
**program_id**: `PRJ-HOL-FOUNDING-2026`  
**plane**: `advops`  
**primary_owner_role**: Compliance  
**access_level**: 2 (Internal Use)  
**output_type**: 2 (text — companion to `topic_enisa_evidence.manifest.md`)  
**Topic edge**: `depends_on=topic_external_adviser_handoff` (Initiative 25 P6).

## Scope

Evidence pack for the ENISA startup-certification track of founder incorporation. Captures what we know about the certification process, who is involved (adviser firm + ENISA-track lead), and what filings/questions are open. Reframes the operator-authored vault doc [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../../Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md) as a **derived narrative view** — facts and counterparty rows live in canonical CSVs.

## Facts

- **F-E-001** — Certification track operates via an external adviser firm (`GOI-ADV-ENTITY-2026`) with a dedicated ENISA-track lead contact (`POI-LEG-ENISA-LEAD-2026`). Source: `GOI_POI_REGISTER.csv`.
- **F-E-002** — Open questions in the ENISA track are tracked in `ADVISER_OPEN_QUESTIONS.csv` under discipline `CRT` (Startup Certification). Source: `ADVISER_OPEN_QUESTIONS.csv`, `ADVISER_ENGAGEMENT_DISCIPLINES.csv`.
- **F-E-003** — Filed/draft instruments related to certification are tracked in `FOUNDER_FILED_INSTRUMENTS.csv` under `discipline_id=startup_certification`. Source: `FOUNDER_FILED_INSTRUMENTS.csv`.
- **F-E-004** — Topic depends on `topic_external_adviser_handoff` (Initiative 21) which provides the ADVOPS plane router and the per-discipline lookup. Source: `TOPIC_REGISTRY.csv`.
- **F-E-005** — Process anchors: `hol_opera_ws_5` (External Adviser Engagement workstream), `thi_legal_dtp_304` (filed instruments register maintenance), `hol_peopl_dtp_303` (GOI/POI register maintenance). Source: `process_list.csv`.

## Sources

| `source_id` | `output_type` | `location` | Notes |
|:------------|:-------------:|:-----------|:------|
| `S-CSV-GOIPOI-2026` | 3 | `docs/references/hlk/compliance/GOI_POI_REGISTER.csv` | Adviser + ENISA lead identities (off-repo real names) |
| `S-CSV-DISC-2026` | 3 | `docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv` | Discipline `CRT` Startup Certification |
| `S-CSV-Q-2026` | 3 | `docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv` | Open questions filtered by `discipline_id=startup_certification` |
| `S-CSV-INST-2026` | 3 | `docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv` | Filed/draft instruments filtered by discipline |
| `S-VAULT-EVID-2026` | 2 | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md` | Operator-authored narrative; **derived view** post-Initiative 25 P6 |
| `S-VAULT-GOV-2026` | 2 | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md` | Document lifecycle for ENISA filings |
| `S-PROC-OPS-WS5` | 3 | `process_list.csv` (`hol_opera_ws_5`) | External Adviser Engagement workstream |

## Refresh hooks

- After any change to the canonical CSV rows tagged for ENISA (CRT discipline, ENISA POI, ADV-ENTITY GOI), refresh the Mermaid `.mmd` and re-render via `py scripts/render_km_diagrams.py … --update-manifest`.
- After any change to `topic_external_adviser_handoff` (parent dependency), review whether ENISA evidence still reflects the updated ADVOPS plane scaffolding.
- Validate via `py scripts/validate_hlk_km_manifests.py` and `py scripts/validate_topic_registry.py` before commit.

## Related

- Parent topic: [`topic_external_adviser_handoff`](../adviser_handoff/topic_external_adviser_handoff.md) — Wikilink: [[topic_external_adviser_handoff]].
- Vault narrative (derived view): [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../../Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md).
- Compliance maintenance SOP: [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../../Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md).
- Initiative 25 master roadmap: [`docs/wip/planning/25-hlk-topic-graph-and-km-scalability/master-roadmap.md`](../../../../../../wip/planning/25-hlk-topic-graph-and-km-scalability/master-roadmap.md).
- KM contract: [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md).
