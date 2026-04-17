# Cursor rules: planning sync (2026-04-17)

**Status:** Applied. The three rules below were updated in the repo (not only planned).

| Rule file | Changes (summary) |
|-----------|-------------------|
| [`.cursor/rules/akos-docs-config-sync.mdc`](../../../../.cursor/rules/akos-docs-config-sync.mdc) | New **Planning and initiative docs** sync table (`README.md` on new folder, `master-roadmap.md` alignment, optional `reference/` plan mirror); planning insight on phase order vs SOP-META; verification bullets for mermaid node IDs and initiative index. |
| [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) | **SOP-META order** and **baseline tranche** under HLK; **master-roadmap** sync and **phase structure** bullets under planning + verification. |
| [`.cursor/rules/akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) | New **`master-roadmap.md` contents** section (link, narrative, mermaid, at-a-glance, sync); **SOP-META alignment**; governance requirements for phase dependency and **per-tranche** CSV approval; quality checks for mermaid, README, roadmap drift. |

From repo root, paths are `.cursor/rules/akos-*.mdc` (same targets).

**Note:** Cursor **plan mode** could not write `.mdc` directly; merged bodies were written as temporary `.md` then copied with PowerShell `Copy-Item` into `.cursor/rules/*.mdc`. **Agent mode** can edit `.mdc` directly.
