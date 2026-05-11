---
language: en
role_owner: PMO
purpose: dated rollback snapshots
audience: rollback / audit only
---

# `_archive/` — dated rollback snapshots (inbound)

Same convention as the outbound archive: one sub-folder per archive event, named `<YYYY-MM-DD>-<reason>/`. Each archive sub-folder contains the full pre-event state of whatever was archived.

## When to archive in inbound engagements

- Pre- / post-mandate-phase shift (e.g., `<YYYY-MM-DD>-pre-drafting-phase/` snapshots the intake/discovery state before drafting starts).
- Pre- / post-scope-renegotiation (when the adviser firm proposes a scope amendment and the prior scope retains diagnostic value).
- Pre- / post-counterparty-substitution (if a new adviser firm replaces the original; preserves the original mandate for closure).

## Conventions

- Folder name: `<YYYY-MM-DD>-<reason-slug>/` — date-prefix sorts chronologically.
- Folder contents: a sub-tree mirroring the archived part of the engagement (e.g., `_archive/2026-MM-DD-pre-drafting/01-our-pack/scope-of-mandate.es.md`).
- Include a per-event `README.md` describing what changed and why.
- **Never** rewrite history inside an archive folder — archives are immutable after creation.

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- Outbound archive counterpart: [`../../Clients/_engagement-template/_archive/README.md`](../../Clients/_engagement-template/_archive/README.md)
