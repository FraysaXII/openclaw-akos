---
source_id: topic_enisa_evidence
output_type: 1
title: "Topic — ENISA evidence pack (Founder Incorporation)"
created: 2026-04-29
revised: 2026-04-29
author_role: Compliance
topic_ids:
  - topic_enisa_evidence
program_id: PRJ-HOL-FOUNDING-2026
plane: advops
summary: >
  KM Topic-Fact-Source manifest for the ENISA evidence pack used in the
  startup-certification track of founder incorporation. Facts cite the
  canonical CSVs (GOI_POI_REGISTER for adviser/banking counterparties,
  ADVISER_OPEN_QUESTIONS for outstanding questions, FOUNDER_FILED_INSTRUMENTS
  for filed/draft instruments) and the redacted transcripts under business-
  intent/. Depends on topic_external_adviser_handoff (Initiative 21) for the
  ADVOPS plane scaffolding.
paths:
  raster: ./topic_enisa_evidence.png
  svg: ./topic_enisa_evidence.svg
  mermaid: ./topic_enisa_evidence.mmd
  excalidraw: null
access_level: 2
confidence: Safe
artifact_role: canonical
intellectual_kind: evidence_pack
related_process_ids:
  - hol_opera_ws_5
  - thi_legal_dtp_304
  - hol_peopl_dtp_303
file_sha256: "635bb9240c418b56497f64415adcec853e1f3a47a366656b4c066e62cfcb1724"
---

# Manifest: topic_enisa_evidence

KM Topic-Fact-Source bundle for the **ENISA evidence pack** scoped to program `PRJ-HOL-FOUNDING-2026`.

Schema: [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md).

Companion narrative (Output 2): [`topic_enisa_evidence.md`](./topic_enisa_evidence.md).
Source-of-truth (Mermaid): [`topic_enisa_evidence.mmd`](./topic_enisa_evidence.mmd).
Renderer: `py scripts/render_km_diagrams.py docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/topic_enisa_evidence.mmd`.

Topic edge: `topic_enisa_evidence` `depends_on=topic_external_adviser_handoff` per `TOPIC_REGISTRY.csv` (Initiative 25 P6).

The vault doc [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../../Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md) is the **derived narrative view**; canonical facts live in the CSV registers.
