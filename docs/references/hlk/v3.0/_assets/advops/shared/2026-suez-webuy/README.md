---
language: en
status: redirect_stub
last_review: 2026-05-10
---

# SUEZ WeBuy engagement — moved

This folder previously held the SUEZ WeBuy engagement artefacts (proposal, deck, CDC feasibility shape, discovery questionnaire, customer-pack, internal companions). As of 2026-05-10, all engagement-scoped artefacts live under the canonical client-engagement home in the **Think Big** vault:

> [`docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/`](../../../../../Think%20Big/Clients/2026-suez-webuy/)

The new layout is audience-segmented:

| Folder | Contents |
|:---|:---|
| `00-internal/` | Internal-only companions (objection bank, counterparty brief, checkpoints) |
| `01-operator-pack/` | Operator-and-collaborator pack (proposal, deck, CDC feasibility shape, discovery questionnaire, README) |
| `02-customer-pack/` | Customer-facing pack (proposal.customer.fr.md, tarification.customer.fr.md, deck.customer.fr.md) |
| `_external_marks/` | Partner / guest brand assets used in co-branded surfaces |
| `_archive/` | Dated snapshots of prior versions (pre-EFA-collaboration baseline preserved at `_archive/2026-05-10-pre-efa-collab/`) |
| `_exports/` | Rendered PDFs (regenerated from markdown; not committed to git) |

## Why this folder remains as a stub

The migration to `Think Big/Clients/` happens in tandem with the canonical workspace blueprint (`WORKSPACE_BLUEPRINT_HOLISTIKA.md` under `Admin/O5-1/Operations/PMO/`, drafted in track P13 of the SUEZ delivery + workspace blueprint plan). Until all back-references in intelligence checkpoints, render manifests, and cross-program documentation re-point to the new path, this stub redirects readers without breaking historical links.

This stub is scheduled for removal in P13 closing canonical (after all back-references are audited).

## What stays in `_assets/advops/shared/`

The `_assets/advops/shared/` folder remains the canonical home for **shared cross-engagement assets** (decks, email signatures, engagement playbook, onboarding kit, press kit, proposal template, sequence templates) that are **not** scoped to a single client engagement. Those continue to live where they are; only client-scoped artefacts moved to `Think Big/Clients/`.

## Canonical reference

The folder shape is governed by:

- [`docs/references/hlk/v3.0/Think Big/README.md`](../../../../../Think%20Big/README.md) — defines the Think Big vault purpose
- [`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) — the PMO hub that indexes client engagements
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` (P13.1) — the engagement-types matrix and folder-shape spec

End of stub.
