---
source_id: topic_kirbe_billing_plane_routing
output_type: 1
title: "Topic — KiRBe billing-plane routing (KiRBe SaaS platform)"
created: 2026-04-29
revised: 2026-04-29
author_role: System Owner
topic_ids:
  - topic_kirbe_billing_plane_routing
program_id: PRJ-HOL-KIR-2026
plane: techops
summary: >
  KM Topic-Fact-Source manifest for KiRBe billing-plane routing — how Stripe webhook
  payloads route between the KiRBe product plane (kirbe.* schema) and the Holistika
  company plane (holistika_ops.* schema), and how counterparty enrichment joins
  through FINOPS_COUNTERPARTY_REGISTER.csv. First non-founder Topic asset under the
  Initiative 22 plane × program × topic layout — validates the convention at N=2
  programs (Initiative 23 P6).
paths:
  raster: ./topic_kirbe_billing_plane_routing.png
  svg: ./topic_kirbe_billing_plane_routing.svg
  mermaid: ./topic_kirbe_billing_plane_routing.mmd
  excalidraw: null
access_level: 2
confidence: Safe
artifact_role: canonical
intellectual_kind: architecture
related_process_ids:
  - env_tech_prj_2
  - thi_finan_dtp_261
  - thi_finan_dtp_308
  - thi_finan_dtp_309
file_sha256: "779e9f8e616b4e41f4113727bbdf8f8a46173df4addabfc277ff89af3caacbf6"
---

# Manifest: topic_kirbe_billing_plane_routing

KM Topic-Fact-Source bundle for the **KiRBe billing-plane routing** topic, scoped to program `PRJ-HOL-KIR-2026`. First non-founder topic under the Initiative 22 plane × program × topic layout convention; proves the layout at N=2 programs.

Schema: [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md).

Companion narrative (Output 2): [`topic_kirbe_billing_plane_routing.md`](./topic_kirbe_billing_plane_routing.md).
Source-of-truth (Mermaid): [`topic_kirbe_billing_plane_routing.mmd`](./topic_kirbe_billing_plane_routing.mmd).
Renderer: `py scripts/render_km_diagrams.py docs/references/hlk/v3.0/_assets/techops/PRJ-HOL-KIR-2026/topic_kirbe_billing_plane_routing/topic_kirbe_billing_plane_routing.mmd`.
