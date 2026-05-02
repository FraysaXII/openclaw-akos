---
language: en
status: active
---

# Operator-facing UAT Dossier outputs

Per-run artifact pack from `scripts/render_uat_dossier.py` (Initiative 48).

Files in this directory are gitignored except this README. Regenerate with:

```bash
py scripts/render_uat_dossier.py                              # snapshot mode (~10s; default)
py scripts/render_uat_dossier.py --mode live --format all     # live mode (~5min); md+pdf+html
py scripts/render_uat_dossier.py --persona PERSONA-INVESTOR-COLD --format md
```

Each run produces:

- `uat-dossier-<UTC>/dossier.md` — canonical markdown body (12 sections per `dossier-section-spec.md`)
- `uat-dossier-<UTC>/dossier.pdf` — brand-aligned PDF (P4; via `akos.hlk_pdf_render.render_pdf_branded`)
- `uat-dossier-<UTC>/dossier.html` — standalone styled HTML (P5; no JS / CDN)
- `uat-dossier-<UTC>/manifest.json` — sha256 + per-section metrics + run config + git_sha + UTC

Initiative reference: `docs/wip/planning/48-operator-dossier/`.

Cost discipline:

- `MAX_DOSSIER_USD` env caps spend (default $2/run; D-IH-48-L)
- `--mode tier-b` requires `AKOS_DOSSIER_TIER_B=1` env opt-in
