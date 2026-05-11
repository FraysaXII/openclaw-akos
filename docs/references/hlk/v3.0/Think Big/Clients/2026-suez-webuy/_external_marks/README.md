---
language: en
status: active
last_review: 2026-05-10
---

# External marks — partner / guest brand assets for SUEZ engagement

This folder holds the brand assets used for the **guest** in the co-branded SUEZ engagement, per [`BRAND_COBRANDING_PATTERN.md`](../../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md). Holistika is the host (its assets live in the canonical brand-asset folder); EFA Académie is the guest (its assets live here, scoped to this engagement).

## Inventory

| File | Use |
|:---|:---|
| `efa-academie-logo.png` | EFA Académie full-color logo (transparent background). Source for the host-card guest-side, after mono-flattening per BRAND_COBRANDING_PATTERN.md §3.3. |
| `efa-academie-logo-on-white.png` | EFA Académie logo composed on white background. Reserved for surfaces where transparent backgrounds are not supported (e.g. legacy email signatures). Not used in the current PDF render pipeline. |

## Mono-flattening (per BRAND_COBRANDING_PATTERN.md §3.3)

The render pipeline applies the mono-flattening transform at composition time (CSS-only, via `filter: grayscale(1) contrast(1.05) brightness(0.9)` or equivalent) so the logo asset itself stays in its native form here. Operators who want to preview the flattened look without running the render can use the same filter in any image viewer.

The flattened tone matches Holistika's foreground charcoal `hsl(220 12% 18%)` on light surfaces.

## Color-bridge accent

The single warm-cream accent borrowed from the EFA palette for the host-card guest-side bottom-edge hairline is approximated as `hsl(35 25% 88%)` — see BRAND_COBRANDING_PATTERN.md §3.1 for tonal-compatibility tests. The exact hex is hard-coded in [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) at the host-card CSS block; this folder does **not** carry the accent value (the value is governance, not asset).

## Polarity-flip readiness

If a future engagement places EFA Académie as host (e.g. for an EFA-customer artefact where Holistika is the introduced guest), this folder structure becomes the EFA-side host directory. The polarity-flip is per-artefact, not per-engagement, so this folder may carry both host and guest assets for different artefacts within the same engagement lifecycle.

## Provenance

These logo assets were provided by the EFA partner lead during the proposal-briefing turn (`[EFA-T2]` per `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/efa-redacted.md`). Their use here is scoped to the SUEZ engagement under the host/guest pattern; broader use (e.g. on Holistika's marketing site, on press kits) requires explicit approval from the partner lead per the collaboration governance.

End.
