---
language: en
role_owner: PMO
purpose: dated rollback snapshots
audience: rollback / audit only
---

# `_archive/` — dated rollback snapshots

This sub-folder holds **dated snapshots** of prior versions of engagement material. One sub-folder per archive event, named `<YYYY-MM-DD>-<reason>/`. Each archive sub-folder contains the full pre-event state of whatever was archived.

## When to archive

- Major reframe of the engagement (e.g., pre- / post-partner-onboarding, pre- / post-pivot, pre- / post-scope-change).
- Pre-customer-meeting snapshot (when a meeting drives substantive revisions and the prior version retains diagnostic value).
- Decision-point archival (when a key operator decision retires a prior approach and the prior approach should remain recoverable).

## Conventions

- Folder name: `<YYYY-MM-DD>-<reason-slug>/` — date-prefix sorts chronologically; reason slug is short ASCII-snake (e.g. `pre-efa-collab`, `pre-scope-pivot-2`).
- Folder contents: a sub-tree mirroring the archived part of the engagement (e.g., `_archive/2026-05-10-pre-efa-collab/01-operator-pack/proposal.fr.md`).
- Include a per-event `README.md` describing what changed and why (one sub-folder = one decision point).
- **Never** rewrite history inside an archive folder — archives are immutable after creation.

## What does NOT live here

- `_exports/` — rendered PDFs go in [`../_exports/`](../_exports/), not here. The archive holds source markdowns; the renderer can regenerate PDFs from any committed git SHA.
- Cross-engagement comparisons — those live under `docs/wip/intelligence/<engagement-slug>/checkpoints/`.

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- Reference engagement: [`../../2026-suez-webuy/_archive/2026-05-10-pre-efa-collab/`](../../2026-suez-webuy/_archive/2026-05-10-pre-efa-collab/) — canonical archive event (pre-EFA-collaboration snapshot)
