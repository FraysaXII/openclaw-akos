---
language: en
status: draft
audience: Operator (boilerplate is reference-only; no team)
delivery_method: short note alongside the patch
---

**Subject:** [Holistika Ops] boilerplate — light-touch reference registration (1 file)

Hi,

Quick light-touch registration for the boilerplate repo as part of Initiative 32 P11 (D-IH-32-N).

**1 file to land** — `EXTERNAL_REPO_CONTRACT.md` at the repo root. That's it. The boilerplate repo has no `.cursor/rules/` directory so no cursor rule mirror is shipped — by design, per D-IH-32-N (light-touch reference-only).

**What this changes:** boilerplate is now `class=reference` in `REPOSITORIES_REGISTRY.md` and tracked by the weekly `REPO_HEALTH_SNAPSHOT.csv` (it shows up with `has_external_repo_contract=true` after the file lands). No SSOT obligation. Brand assets (Holistika logo SVG, hero gradient) stay as visual reference per `BRAND_VISUAL_PATTERNS.md` in AKOS.

**The embedded Obsidian snapshot at** `app/dashboard/applications/kms/obsidian-holistika-main/` **stays as historical archive** — explicitly NOT canonical. Initiative 43 (deferred) will replace it with a pointer to AKOS `docs/references/hlk/v3.0/` once the operator migrates personal Obsidian workflow off boilerplate fully.

No further action needed.

— Holistika AKOS governance
