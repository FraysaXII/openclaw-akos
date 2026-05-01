---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-pointer
program_id: shared
plane: ops
authority: Brand Manager + System Owner
last_review: 2026-04-30
audience: ERP team engineering
---

# Localisation policy — pointer

The canonical localisation policy was relocated in Initiative 32 P7 (D-IH-32-E):

- **New canonical path:** `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_LOCALISATION_001.md`
- **Legacy path:** `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-HLK_LOCALISATION_001.md` (no longer exists)

GitHub link: `https://github.com/FraysaXII/openclaw-akos/blob/main/docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_LOCALISATION_001.md`

## Why the move

Brand Manager owns the policy (voice, locale strategy, audience-canonical exception per D-IH-31-A). Tech / System Owner kept ownership of the validator script (`scripts/validate_hlk_language_frontmatter.py`) because the executor lives in code. The SOP cross-references the validator; the validator does not load the SOP. Two-way pointer relationship preserved.

## What ERP needs to do

1. Adopt `language: en | es | fr` frontmatter on every new canonical Markdown file in the ERP repo.
2. The audience-canonical exception (D-IH-31-A) applies to single-locale-targeted ERP screens (e.g., Spanish founder-incorporation dashboard).
3. AKOS-side `validate_hlk_language_frontmatter.py` does not scan the ERP repo (cross-repo); the AKOS-side `compliance.repo_health_snapshot_mirror` reports `language_frontmatter_compliance_pct` as a non-blocking signal.

## Cross-references

- D-IH-31-A (audience-canonical default) in `docs/wip/planning/31-holistik-ops-discovery/decision-log.md`
- D-IH-32-E (relocation rationale) in `docs/wip/planning/32-holistik-ops-maturation/decision-log.md`
- ERP architecture audit (sibling): recommends 100% language-frontmatter adoption on a non-blocking timeline
