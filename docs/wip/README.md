# Work-in-progress documentation (`docs/wip`)

This tree holds **non-canonical** drafts: planning copies, proposals, and interpretation-layer syntheses. **Canonical** Holistika knowledge remains under [`docs/references/hlk/v3.0/`](../references/hlk/v3.0/) and [`docs/references/hlk/compliance/`](../references/hlk/compliance/) per [PRECEDENCE.md](../references/hlk/compliance/PRECEDENCE.md).

## Layout

| Path | Purpose |
|------|---------|
| `planning/<initiative-slug>/` | Execution roadmaps and phase reports (see [.cursor/rules/akos-planning-traceability.mdc](../../../.cursor/rules/akos-planning-traceability.mdc)). **Reading order / “what went before”:** [planning/README.md](planning/README.md) (numbered index). Examples: `akos-full-roadmap/`, `hlk-on-akos-madeira/`, `hlk-km-knowledge-base/`, `holistika-company-formation/`, `hlk-vault-envoy-repos/`. |
| `planning/_proposals/` | Ad-hoc or comparative **`.plan.md`** artifacts (tooling experiments, model comparisons). Not initiative roadmaps. |
| `hlk-km/` | HLK governed KM **wip syntheses** linked from the PMO Trello registry (`research-synthesis-*.md`). Promote to `v3.0/` per the founder governance lifecycle when stable. |

## Rules

- Do not treat files here as SSOT for compliance CSVs or runtime inventory.
- When moving files, update inbound links from `docs/references/hlk/...` and registry tables.
- New initiatives: create `planning/<kebab-slug>/` with `master-roadmap.md` rather than dumping files at the root of `docs/wip/`.
