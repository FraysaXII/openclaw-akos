---
language: en
role_owner: PMO
purpose: operator-only briefs + counterparty intel + objection bank
audience: operator + agent only
---

# `00-internal/` — operator-only companions

This sub-folder holds **operator-only** material that supports the engagement but is not shared with the counterparty: objection banks, counterparty briefs, internal review notes, redacted intelligence transcripts, decision memos.

## Audience

Operator + agents reading prose. Never the customer. Never the partner counterparty.

## Typical contents

- `<engagement-slug>.objections.md` — objection bank: anticipated counterparty objections + responses; pre-meeting prep
- `<engagement-slug>.counterparty-brief.md` — what we know about the counterparty (their roles, processes, pain, prior moves); cross-links to GOI/POI rows
- `decision-memo-<YYYY-MM-DD>-<topic>.md` — operator decision notes that landed in the engagement but stay internal
- intelligence cross-links: pointers to `docs/wip/intelligence/<engagement-slug>/` for redacted research synthesis

## Conventions

- File names follow `<slug>.<purpose>.<lang>.md` where useful (`<engagement-slug>.objections.fr.md`).
- Cross-link to GOI/POI rows via `ref_id` (`GOI-CUS-SUEZ-2026`), not real names.
- Cross-link to canonical Admin SOPs under `Admin/O5-1/<area>/<role>/` rather than copying content.
- Reference engagement: [`../../2026-suez-webuy/00-internal/`](../../2026-suez-webuy/00-internal/) — illustrative shape (objection bank + counterparty brief pattern).

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- Blueprint §4: [`../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md)
