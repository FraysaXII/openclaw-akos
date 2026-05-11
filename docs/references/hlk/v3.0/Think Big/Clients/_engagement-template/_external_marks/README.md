---
language: en
role_owner: Brand Manager
purpose: guest / partner brand assets for co-branded surfaces
audience: render pipeline (no human reader)
---

# `_external_marks/` — guest / partner brand assets

This sub-folder holds the **guest brand assets** (logos, color palettes, typography references) used by the renderer to compose co-branded surfaces. Host = Holistika brand assets stay in the Holistika brand canon (`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/`); only guest assets land here.

## When this folder has content

- Engagement involves co-branding posture per [`BRAND_COBRANDING_PATTERN.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md) (host / guest semantics).
- The `_external_marks/` folder of [`../../2026-suez-webuy/_external_marks/`](../../2026-suez-webuy/_external_marks/) is the canonical example: it holds `efa-academie-logo.png` + light / on-white variants for SUEZ-engagement co-branded surfaces.

## When this folder is empty

- **Type-5 internal-capacity engagements** (`<YYYY>-internal-<slug>/`) — no external counterparty to co-brand with; this folder typically stays empty (keep `.gitkeep` to preserve the folder).
- Engagements where Holistika delivers solo without a co-branded partner.

## Naming conventions

- `<partner-slug>-logo.<variant>.<format>` — e.g. `efa-academie-logo.png`, `efa-academie-logo-on-white.png`, `efa-academie-logo-light.png`.
- Vector formats (`.svg`) are preferred where available; PNG fallback for renderer compatibility.
- File names are redaction-safe: use partner brand name as displayed publicly (the partner controls their own public brand visibility).

## Cross-references

- Co-branding pattern: [`../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md)
- Brand architecture: [`../../../Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md)
- Reference engagement: [`../../2026-suez-webuy/_external_marks/`](../../2026-suez-webuy/_external_marks/) — canonical example
