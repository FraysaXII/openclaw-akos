---
language: en
status: active
role_owner: PMO
program_id: ENG-SUEZ-WEBUY-2026
engagement_class: client_led_with_partner_introduction
host_brand: Holistika Research
guest_brand: EFA Académie
collaboration_since: 2025-10
last_review: 2026-05-10
---

# SUEZ — WeBuy procure-to-pay automation (engagement folder)

This is the canonical engagement folder for the SUEZ WeBuy procure-to-pay automation. It is co-presented by Holistika Research (host) and EFA Académie (guest, collaboration partner since October 2025), per the host/guest pattern in [`BRAND_COBRANDING_PATTERN.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md).

## Folder layout

| Sub-folder | Contents | Audience |
|:---|:---|:---|
| [`00-internal/`](00-internal/) | Objection bank, counterparty brief, checkpoints, internal review notes | operator + agent only |
| [`01-operator-pack/`](01-operator-pack/) | Operator-and-collaborator pack: proposal, deck, CDC feasibility shape, discovery questionnaire | operator + EFA partner lead |
| [`02-customer-pack/`](02-customer-pack/) | Customer-facing pack: pricing-free proposal, deck, separate tarification annex | SUEZ (customer) |
| [`_external_marks/`](_external_marks/) | EFA Académie brand assets used in co-branded surfaces (logos, palette references) | render pipeline |
| [`_archive/`](_archive/) | Dated snapshots of prior versions (rollback only) | rollback only |
| [`_exports/`](_exports/) | Rendered PDFs (generated from markdown; not committed to git) | distribution |

## Intelligence inflows (Option A hybrid: intelligence stays in wip)

The intelligence base for this engagement lives in:

> [`docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/`](../../../../../wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/)

It carries: extracts of source documents, redacted EFA-side intelligence (`efa-redacted.md`), voice corpus (`voice-corpus.md`), discovery questionnaire pre-meeting plan, scope, and dated checkpoints (P12.0–P12.9 cycle).

Per [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md), intelligence-stage artefacts remain under `wip/intelligence/` until they are crystallized into engagement-pack artefacts; the engagement README cross-links the live intel base.

## Brand posture (per BRAND_COBRANDING_PATTERN.md)

- **Host:** Holistika Research (Holistika light variant palette; Inter typeface; teal + amber accents).
- **Guest:** EFA Académie. Logo at 0.7× host scale, mono-flattened to host foreground charcoal on the slide-02 host-card. Color-bridge accent: a single warm-cream tone borrowed from the EFA Académie print materials, used once on the guest-card bottom-edge hairline.
- **Cover-strip:** 4-field (Programme / Date / Discipline / `En collaboration avec` → `EFA Académie`).
- **Polarity-flip clause** in effect for any future EFA-hosted artefacts.

## Decision register cross-link

Engagement-scoped decisions D-12-1..D-12-17 live in the SUEZ delivery + workspace blueprint plan and are summarized in the closing checkpoint at `00-internal/checkpoints/p12-efa-collaboration-formalization-2026-05-10.md` (filed at P12.9).

## GOI / POI rows

- `GOI-CUS-SUEZ-2026` — customer organisation (SUEZ procurement scope)
- `POI-CUS-SUEZ-LEAD-2026` — customer-side lead contact
- `GOI-PRT-EFA-2026` — partner organisation (EFA Académie)
- `POI-PRT-EFA-LEAD-2026` — partner lead (also incumbent operator of the WeBuy process; two-hat posture per `efa-redacted.md` §3)

Notes on these rows are updated at P12.6 (notes-only; class enum stays `partner` per D-12-7).

## Render pipeline

PDFs are generated from the markdowns in this folder by [`scripts/render_suez_engagement_pdfs.py`](../../../../../../scripts/render_suez_engagement_pdfs.py). The script's `SOURCES` dict points to the audience sub-folders here. Rendered output lands in [`_exports/`](_exports/), which is in `.gitignore` patterns.

## Status

Currently in proposal stage (pre-discovery-meeting). Phase plan in track P12 of the SUEZ delivery + workspace blueprint plan.

End.
