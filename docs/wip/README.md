# Work-in-progress documentation (`docs/wip`)

This tree holds **non-canonical** drafts: planning copies, proposals, and interpretation-layer syntheses. **Canonical** Holistika knowledge remains under [`docs/references/hlk/v3.0/`](../references/hlk/v3.0/) and [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`](../references/hlk/compliance/) per [PRECEDENCE.md](../references/hlk/compliance/PRECEDENCE.md).

## Layout

| Path | Purpose |
|------|---------|
| `intelligence/` | **Tier 1 WIP (Research-area-owned)** per [WORKSPACE_BLUEPRINT_HOLISTIKA §17](../references/hlk/v3.0/Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) + **D-IH-70-O** (3-tier WIP topology). Cross-area research, engagement intelligence folders (e.g. `2026-05-10-suez-webuy-procure-to-pay/`), substrate-audit folders, KM drafts, ontology proposals. Curated by KM Officer. See [`intelligence/README.md`](intelligence/README.md). |
| `planning/NN-<initiative-slug>/` | **Tier 2 WIP (PMO-owned)** per blueprint §17. Execution roadmaps and phase reports (see [`.cursor/rules/akos-planning-traceability.mdc`](../../.cursor/rules/akos-planning-traceability.mdc)). **Reading order / "what went before":** [`planning/README.md`](planning/README.md) (numbered index). Examples: `01-akos-full-roadmap/`, `02-hlk-on-akos-madeira/`, `03-hlk-km-knowledge-base/`, `04-holistika-company-formation/`, `05-hlk-vault-envoy-repos/`. |
| `planning/99-proposals/` | Ad-hoc or comparative **`.plan.md`** artifacts (tooling experiments, model comparisons). Not initiative roadmaps. |
| `hlk-km/` | **DEPRECATED** per **D-IH-86-CY-D** (2026-05-25); superseded by `intelligence/`. The 5 stub files inside remain in place to preserve Trello-card linkage. New cross-area research lands under `intelligence/`. See [`hlk-km/README.md`](hlk-km/README.md) for the deprecation notice + stub inventory + Trello-card crosswalk. |
| `<area>/<role>/wip/` (under `docs/references/hlk/v3.0/`) | **Tier 3 WIP (role-owned)** per blueprint §17. Role-internal drafts before crossing into Tier 1 or Tier 2. |

## Rules

- Do not treat files here as SSOT for compliance CSVs or runtime inventory.
- When moving files, update inbound links from `docs/references/hlk/...` and registry tables.
- New initiatives: create `planning/NN-<kebab-slug>/` (next free `NN` from [planning/README.md](planning/README.md)) with `master-roadmap.md` rather than dumping files at the root of `docs/wip/`.
- **Initiative closure:** If a Cursor plan or `master-roadmap.md` promised **browser / WebChat / Langfuse UI / Docker** UAT, record dated **`reports/uat-*.md`** outcome tables (PASS / SKIP / N/A) or explicit skips—**not** only “run the DEVELOPER_CHECKLIST gates.” Full contract: [`.cursor/rules/akos-planning-traceability.mdc`](../../.cursor/rules/akos-planning-traceability.mdc). Patch-history notes: [planning/99-proposals/cursor-rules-uat-evidence-instructions.md](planning/99-proposals/cursor-rules-uat-evidence-instructions.md).
