---
language: en
role_owner: PMO
purpose: operator-only notes for an inbound adviser engagement
audience: operator + agent only
---

# `00-internal/` — operator-only notes for inbound engagements

This sub-folder holds **operator-only** notes for an inbound adviser engagement: decision memos, GOI/POI cross-link tables, intake-stage observations, redaction-safe context summaries.

The inbound folder is a **unified entry point**, not a content store — the canonical content lives in role-owner SOPs and CSV registers under `Admin/O5-1/People/Legal/` and `compliance/`. This `00-internal/` README documents the entry-point cross-links.

## Audience

Operator + agents reading prose. Never the adviser firm. Never an external reader.

## Typical contents

- `goipoi-cross-links.md` — single table mapping every `GOI-ADV-*` / `POI-LEG-*` / `POI-BNK-*` / `POI-ADV-*` row in [`GOI_POI_REGISTER.csv`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) that touches this engagement, with `program_id`, `role_owner`, `process_item_id` columns and one-line context
- `decision-memo-<YYYY-MM-DD>-<topic>.md` — operator decisions that land in the engagement but stay internal
- `intake-observations.md` — pre-mandate intake notes; what we know about the adviser firm's intake process, their typical response times, their billing posture
- `mandate-phase-tracker.md` — `intake → discovery → drafting → filing → closure` progression with timestamps and key artifacts per phase

## Conventions

- Cross-link to GOI/POI rows via `ref_id`, never real names.
- Cross-link to canonical Admin SOPs under `Admin/O5-1/People/Legal/`, `Admin/O5-1/People/Compliance/`, `Admin/O5-1/Operations/PMO/` — do NOT duplicate content.
- Cross-link to the relevant `advops/` CSVs (`advops/ADVISER_OPEN_QUESTIONS.csv`, `advops/ADVISER_ENGAGEMENT_DISCIPLINES.csv`, `advops/FILED_INSTRUMENTS.csv` — all relocated I81 P2 T2/T3).

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- ADVOPS SOP: [`../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
- GOI/POI register: [`../../../../compliance/dimensions/GOI_POI_REGISTER.csv`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv)
