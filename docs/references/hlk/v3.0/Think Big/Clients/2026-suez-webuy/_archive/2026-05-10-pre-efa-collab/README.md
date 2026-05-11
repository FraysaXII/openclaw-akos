---
language: en
status: archive
archive_date: 2026-05-10
archive_reason: Pre-EFA-collaboration-framing baseline preserved before P12 voice-fidelity gate and customer-pack updates
---

# Archive — pre-EFA-collaboration baseline (2026-05-10)

This snapshot captures the SUEZ engagement markdown files **before** the P12 cycle of the SUEZ delivery + workspace blueprint plan introduced:

- The volume hot-fix from `~20/month` to `20-50/day` with FTE-equivalent anchor (D-12-13).
- The litige reframe to value-prop spine (D-12-15), including the 5th feature card on the litige module, the three commitment KPIs, and the triadic pull-quote.
- The four new intro slides (02-05) on the customer deck, with EFA host-card on slide 02, network-claim retirement on slide 03, *Deux récits, une seule discipline* on slide 04, and *How we work today* on slide 05; renumbering of existing slides 02-09 to 06-13; `slide_count: 13`.
- The Continuité opérationnelle section (proposal §3 new) with two postures (operator-led / Holistika-led) and tarification-deferred clause.
- The cover-strip 4-field extension (`En collaboration avec EFA Académie`) on customer-pack surfaces.
- The EFA-since-October-2025 date correction across all dated phrasings.
- The redaction of internal filename leaks (`.fr.md`), internal taxonomy (`Cellule`, `SERVICE_OFFERING_CATALOG`), and explicit CDC article citations (per D-12-17 external-prose discretion).

## What this snapshot contains

The 10 markdowns in this directory are byte-identical copies of the files at the source location `docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/` immediately before the P12 cycle ran (timestamp 2026-05-10).

## How to roll back

If the operator decides to revert the SUEZ engagement to this baseline:

1. Delete or move the live versions in `00-internal/`, `01-operator-pack/`, and `02-customer-pack/`.
2. Copy the snapshot files in this directory into the corresponding audience folders (audience mapping below).
3. Re-run [`scripts/render_suez_engagement_pdfs.py`](../../../../../../../../scripts/render_suez_engagement_pdfs.py); rendered PDFs in `_exports/` regenerate from the rolled-back markdown.

## Audience mapping for rollback

| Snapshot file | Restore to |
|:---|:---|
| `deck-suez-webuy.objections.md` | `00-internal/` |
| `deck-suez-webuy.counterparty-brief.md` | `00-internal/` |
| `proposal.fr.md` | `01-operator-pack/` |
| `deck-suez-webuy.fr.md` | `01-operator-pack/` |
| `cdc-feasibility-shape.fr.md` | `01-operator-pack/` |
| `discovery-questionnaire.fr.md` | `01-operator-pack/` |
| `README.md` | `01-operator-pack/` (operator-pack README; not the engagement-level README at the parent folder) |
| `proposal.customer.fr.md` | `02-customer-pack/` |
| `tarification.customer.fr.md` | `02-customer-pack/` |
| `deck.customer.fr.md` | `02-customer-pack/` |

## Why version-history lives here, not in git history

Git history is the canonical version log; this archive does not replace it. The archive serves a different purpose: it gives the operator a **single coherent point-in-time snapshot** that can be restored as a unit, without having to identify and revert the right cluster of git commits. This is especially useful when:

- A future P12-equivalent phase needs to compare *current* vs *pre-P12* on a single artefact.
- The operator wants to audit "what changed in P12" without reading commit-by-commit.
- A rollback is needed urgently (e.g. a customer meeting reveals the new framing did not land) and the operator prefers a one-step restore.

PDFs are not archived; they regenerate deterministically from the markdown via the render pipeline.

End of archive README.
