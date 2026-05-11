---
language: en
role_owner: PMO
purpose: rendered branded PDFs for distribution
audience: customer + partner + non-technical readers via Drive sync
---

# `_exports/` — rendered branded PDFs

This sub-folder holds **branded PDFs** rendered deterministically from the canonical markdowns in [`../01-operator-pack/`](../01-operator-pack/) and [`../02-customer-pack/`](../02-customer-pack/). The PDFs are **tracked in git** (per the 2026-05-11 `.gitignore` policy reversal; promoted to workspace doctrine in [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §5) so non-technical readers consume them directly via Google Drive sync.

## Tracking policy

| Asset class | Git policy | Rationale |
|:---|:---|:---|
| Branded PDFs (`*.pdf`) | **Tracked** | Drive readers consume PDFs directly; tracking means non-technical collaborators see the latest version via folder-sync |
| `render-manifest.json` | **Tracked** | Audit trail; sha256 over every rendered PDF; lets a verifier confirm a Drive PDF matches a git commit |
| Markdown sidecars (`*.md`) | **Ignored** | Render-time duplicates of canonical sources in `01-operator-pack/` + `02-customer-pack/`; drift risk |

The pattern in [`/.gitignore`](../../../../../../../../.gitignore) for `_exports/*` under Think Big/Clients/ implements this allowlist policy.

## Per-engagement README expectations

When using this template, the copied `_exports/README.md` lists the actual PDFs in a table:

```markdown
| File | Audience | Source markdown |
|:---|:---|:---|
| `proposal.fr.pdf` | operator + partner | `01-operator-pack/proposal.fr.md` |
| `proposal.customer.fr.pdf` | customer (pricing-free) | `02-customer-pack/proposal.customer.fr.md` |
| ... | ... | ... |
| `render-manifest.json` | audit trail | sha256 of each source-md ↔ rendered-pdf pair |
```

## Regenerating

Use an engagement-specific render script under `scripts/render_<slug>_engagement_pdfs.py` (precedent: [`scripts/render_suez_engagement_pdfs.py`](../../../../../../../../scripts/render_suez_engagement_pdfs.py)). Optional flags: `--smoke` (verify sources only); `--only <surface>` (single surface).

After regenerating, commit the changed PDFs + manifest. The sha256 entries in `render-manifest.json` are the audit anchor — if a markdown edit lands without a matching PDF re-render, `git diff` on the manifest surfaces it.

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- File-tracking doctrine: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §5
- Reference engagement: [`../../2026-suez-webuy/_exports/`](../../2026-suez-webuy/_exports/) — canonical example with seven PDFs + manifest
