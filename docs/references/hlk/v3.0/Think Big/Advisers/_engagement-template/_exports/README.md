---
language: en
role_owner: PMO
purpose: rendered branded PDFs for distribution
audience: adviser counterparty + non-technical readers via Drive sync
---

# `_exports/` — rendered branded PDFs (inbound)

This sub-folder holds **branded PDFs** rendered from the canonical markdowns in [`../01-our-pack/`](../01-our-pack/). The PDFs are tracked in git per the workspace doctrine in [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §5.

## Tracking policy

Same as the outbound `_exports/` (per [`Think Big/Clients/_engagement-template/_exports/README.md`](../../../Clients/_engagement-template/_exports/README.md)):

| Asset class | Git policy | Rationale |
|:---|:---|:---|
| Branded PDFs (`*.pdf`) | **Tracked** | Adviser counterparty + Drive readers consume PDFs directly |
| `render-manifest.json` | **Tracked** | sha256 audit trail per source-md ↔ rendered-pdf pair |
| Markdown sidecars (`*.md`) | **Ignored** | Render-time duplicates of canonical sources in `01-our-pack/`; drift risk |

Note: inbound `_exports/` typically renders OUR-pack material (scope of mandate, KYC pack, context brief) since those are the materials Holistika hands off. Adviser-pack material (`02-adviser-pack/`) is received already-rendered by the adviser firm and stored as source — Holistika does not re-render adviser-authored documents.

## `.gitignore` invariant

The pattern for `Think Big/Advisers/*/_exports/` mirrors the outbound pattern when active inbound engagements land tracked PDFs. The invariant is encoded centrally in [`/.gitignore`](../../../../../../../../.gitignore) (extended in P13.5 when the first inbound engagement folder lands).

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- File-tracking doctrine: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §5
- Outbound `_exports/` counterpart: [`../../../Clients/_engagement-template/_exports/README.md`](../../../Clients/_engagement-template/_exports/README.md)
