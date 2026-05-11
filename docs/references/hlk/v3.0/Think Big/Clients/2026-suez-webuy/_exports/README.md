---
language: en
role_owner: PMO
purpose: distribution
---

# `_exports/` — branded PDFs for distribution

This folder holds branded PDFs rendered from the canonical markdowns in [`01-operator-pack/`](../01-operator-pack/) and [`02-customer-pack/`](../02-customer-pack/). The PDFs are tracked in git (and synced via Google Drive) so non-technical readers can open them directly without running the render pipeline.

## What's in here

| File | Audience | Source markdown |
|:---|:---|:---|
| `cdc-feasibility-shape.fr.pdf` | operator + EFA partner lead | `01-operator-pack/cdc-feasibility-shape.fr.md` |
| `discovery-questionnaire.fr.pdf` | operator + EFA partner lead | `01-operator-pack/discovery-questionnaire.fr.md` |
| `proposal.fr.pdf` | operator + EFA partner lead (carries internal tarification annex) | `01-operator-pack/proposal.fr.md` |
| `deck-suez-webuy.fr.pdf` | operator + EFA partner lead | `01-operator-pack/deck-suez-webuy.fr.md` |
| `proposal.customer.fr.pdf` | SUEZ (customer) — pricing-free | `02-customer-pack/proposal.customer.fr.md` |
| `tarification.customer.fr.pdf` | SUEZ (customer) — separate annex | `02-customer-pack/tarification.customer.fr.md` |
| `deck.customer.fr.pdf` | SUEZ (customer) | `02-customer-pack/deck.customer.fr.md` |
| `render-manifest.json` | audit trail | sha256 of each source md ↔ rendered PDF pair |

## Tracking policy

- **PDFs (`*.pdf`)** — tracked in git. The repo is shared with non-technical readers via git + Google Drive sync, and most stakeholders consume PDFs, not markdown.
- **`render-manifest.json`** — tracked in git. Records sha256 of each source-md ↔ rendered-pdf pair so any drift between the canonical markdown and the published PDF is observable in `git diff`.
- **Markdown sidecars (`*.md`)** — gitignored. They are render-time duplicates of the canonical sources in `01-operator-pack/` + `02-customer-pack/`; tracking them creates drift risk.

## Regenerating

```
py scripts/render_suez_engagement_pdfs.py
```

Optional flags: `--smoke` (verify sources only, no render), `--only <surface>` (single surface).

After regenerating, commit the changed PDFs + manifest. The sha256 entries in `render-manifest.json` are the audit anchor — if a markdown edit lands without a matching PDF re-render, `git diff` on the manifest surfaces it.

End.
