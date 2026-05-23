---
language: en
status: active
role_owner: PMO
co_owner_role: Compliance; Legal Counsel
area: PMO
entity: Holistika Research SL
plane: advops
program_id: PRJ-HOL-FOUNDING-2026
program_label: "Holistika Research SL — Programa de fundación 2026"
engagement_slug_consuming: 2026-holistika-incorporation
authored: 2026-05-18
last_review: 2026-05-18
intellectual_kind: program_asset_bucket_anchor
sharing_label: internal_only
linked_canonicals:
  - FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md
  - EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md
  - TOPIC_PMO_CLIENT_DELIVERY_HUB.md
  - SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md
  - ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md
---

# `_assets/advops/2026-holistika-incorporation/` — Program asset bucket

> **What this folder is.** The **program-level asset bucket** for the founder-incorporation program `PRJ-HOL-FOUNDING-2026`. It holds the **rendered external collateral** (dossiers, deck slides + visual systems, adviser-handoff topic visuals, ENISA evidence topic visuals, cover emails) produced *for* this program — not the canonical SOPs or CSV registers that govern them. The canonical content lives in role-owner SOPs under `Admin/O5-1/<area>/<role>/canonicals/` and the CSV registers under `Admin/O5-1/People/Compliance/canonicals/`; this folder is the **derived-artifact bucket** that the operator hands to advisers / regulators.

## Why two slugs (program_id vs engagement_slug)

This program operates under **two slugs** that coexist intentionally and serve different governance purposes. **Per D-IH-89-H (2026-05-18, operator-override of D-IH-89-G)**: the ADVOPS plane uses the **engagement-slug as the asset-bucket dirname** (external register; what humans and Obsidian see when navigating the vault) while the **program_id stays in frontmatter** (internal register / SSOT; what FK joins and PMO portfolio rollup use).

| Slug | Domain | Where it lives | Used by |
|:---|:---|:---|:---|
| `PRJ-HOL-FOUNDING-2026` | **Program identifier** — PMO portfolio key | `Admin/O5-1/Operations/PMO/canonicals/TOPIC_PMO_CLIENT_DELIVERY_HUB.md`; frontmatter `program_id:` field across all program-attributed canonicals; `dimensions/PROGRAM_REGISTRY.csv`; `dimensions/TOPIC_REGISTRY.csv` `program_id` column | PMO portfolio rollup; Legal / Finance / Compliance canonical attribution; KM Output-1 topic-asset anchoring; cross-CSV FK joins (GOI_POI, FILED_INSTRUMENTS, ADVISER_OPEN_QUESTIONS) |
| `2026-holistika-incorporation` | **Engagement slug** — human-readable inbound adviser engagement label AND the dirname for the asset bucket (ADVOPS plane only) | `Think Big/Advisers/2026-holistika-incorporation/` engagement folder; **`_assets/advops/2026-holistika-incorporation/`** (this folder); `engagement_slug:` frontmatter field; `engagement_slug_consuming:` field on this README | Inbound adviser engagement bundle (`00-internal/`, `01-our-pack/`, `02-adviser-pack/`, `_archive/`, `_exports/`) per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §4; external-facing navigation in Obsidian graph + GitHub tree views |

**Plane convention (post-D-IH-89-H).** The I22 forward layout convention (`_assets/<plane>/<program_id>/<topic_id>/`) is amended for the ADVOPS plane: ADVOPS produces external-register collateral, so its asset bucket dirname uses engagement-slug. All other planes (techops, marketing, finops, etc.) continue to use program_id as the bucket dirname. The PROGRAM_ID consistency validator (`scripts/validate_program_id_consistency.py`) and the dossier renderer (`scripts/render_dossier.py`) both look up the program_id via the bucket README's `program_id:` frontmatter when the dirname doesn't match the `PRJ-HOL-*` pattern.

**Why this split.** Operators and advisers navigate the vault visually (file browser, Obsidian graph, GitHub tree). The engagement-slug `2026-holistika-incorporation/` is immediately legible — "this is the 2026 Holistika incorporation engagement". The internal program_id `PRJ-HOL-FOUNDING-2026` is a system identifier (PMO-defined, FK-stable, never changes) and lives in the frontmatter where validators + scripts read it.

## External register discipline (BBR posture)

This folder is governed by the dual-register contract per [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) §3 + cursor rule [`akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc):

- **Rendered prose** that this folder ships to external audiences (`dossier_*.md`, `deck/*.yaml`, `deck_slides.yaml`, `founder-filed/**/*.md`, `adviser-handoff/*.md`) **must not** carry internal-register tokens — including the `PRJ-HOL-*` program identifier itself. External prose refers to the program as "Holistika Research SL — Programa de fundación 2026" or by the entity name "Holistika Research SL".
- **Operator-side metadata** in this folder (frontmatter `program_id:`, manifest files, `.mmd` source-of-truth diagrams) may continue to use the internal `PRJ-HOL-*` identifier — those surfaces are not external-facing.
- **Companion files** with suffixes `.objections.md` or `.counterparty-brief.md` are intentionally exempt from the BBR validator and may carry the internal register (operator-private working surfaces).

The drift gate `scripts/validate_brand_baseline_reality_drift.py` enforces this contract automatically and runs under `pre_commit` profile per [`config/verification-profiles.json`](../../../../../../../config/verification-profiles.json) (FAIL since 2026-05-17 per D-IH-89-E).

## Folder shape

| Sub-folder | Topic | What lives here |
|:---|:---|:---|
| `enisa_evidence/` | `topic_enisa_evidence` | ENISA evaluator-facing evidence appendix (`dossier_es.md` is the prose SSOT) + topic visual (`topic_enisa_evidence.mmd` + `.svg`) + manifest + cover email (`cover_email_es.md`) |
| `enisa_company_dossier/` | `topic_enisa_dossier_es` | Visual deck companion for `enisa_evidence/`: structured slide data (`deck_slides.yaml`), prose narrative (`deck_story_es.md`), visual system spec (`deck-visual-system.md`), Figma cross-link (`figma-link.md`), cover email (`cover_email_company_dossier_es.md`) |
| `adviser_handoff/` | `topic_external_adviser_handoff` | Topic visual for external-adviser handoff (`.mmd` + `.svg`) + topic doc (`topic_external_adviser_handoff.md`) + manifest |

> **Note on file naming.** Sub-folder names use `snake_case` (`enisa_evidence`, `adviser_handoff`) to match the `topic_id` convention used in [`TOPIC_REGISTRY.csv`](../../../Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv). The BBR validator's adviser-surface glob set (per `scripts/validate_brand_baseline_reality_drift.py` lines 197-203) covers `**/deck/*.yaml`, `**/dossier_*.md`, `**/deck_slides.yaml`, `**/founder-filed/**/*.md`, `**/adviser-handoff/*.md` — i.e., it uses `adviser-handoff` with a hyphen. The current folder is named `adviser_handoff` with underscore; the validator therefore does NOT currently scan that folder. This is a tracked governance gap: see [`OPS-86-5` closure record](../../../../../../wip/planning/86-initiative-cluster-execution-coordinator/reports/ops-86-5-closure-evidence-2026-05-18.md) (either rename folder to `adviser-handoff` or extend validator glob to cover `adviser_handoff/`). I56 P5+ ADVOPS architecture harmonization (D-IH-89-I) will resolve this jointly with the broader post-I72 wiring.

> **Note on historical path references.** Documents authored before 2026-05-18 (closure records, UAT records, decision-log rows, files-modified CSV rows for prior commits, CHANGELOG history) reference this asset bucket at its pre-rename path `_assets/advops/PRJ-HOL-FOUNDING-2026/`. Those references are intentionally **not** rewritten — they record what was true on their date of authoring (audit-trail integrity). Active canonicals + scripts + tests were updated to the new path on 2026-05-18 per D-IH-89-H.

## Cross-area governance wiring

This folder is **cross-wired** with the following neighbours so that operators + advisers can navigate seamlessly between the canonical narrative (role-owner SOPs), the machine-readable registers (CSV canonicals), the engagement-level inbound bundle (Think Big/Advisers), and the rendered external collateral (this folder):

### Inbound engagement bundle (operator-side scaffold)

- [`Think Big/Advisers/2026-holistika-incorporation/`](../../../../Think%20Big/Advisers/2026-holistika-incorporation/README.md) — the **inbound engagement folder** for this program. Holds `00-internal/`, `01-our-pack/`, `02-adviser-pack/`, `_archive/`, `_exports/`. The legal-constitutor handoff bundle lives at `01-our-pack/legal-constitutor-handoff-2026-05-18.md`.

### Canonical SOPs + decision memos (role-owner narrative)

- [`FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`](../../../Admin/O5-1/People/Legal/canonicals/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md) — incorporation-program knowledge index (Legal-side narrative SSOT).
- [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../../Admin/O5-1/People/Legal/canonicals/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) — handoff doc for external counsel (binding ladder + sharing legend + per-discipline routing).
- [`FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md`](../../../Admin/O5-1/People/Legal/canonicals/FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md) — entity formation case memo.
- [`FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`](../../../Admin/O5-1/Finance/Business%20Controller/canonicals/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md) — capitalization posture.
- [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../Admin/O5-1/People/Legal/canonicals/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) — Branded House decision + trademark filing scope.
- [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../Admin/O5-1/People/Compliance/canonicals/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md) — ENISA evidence pack canonical.

### Plane SOPs (PMO ADVOPS)

- [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../Admin/O5-1/Operations/PMO/canonicals/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) — ADVOPS plane SOP (operator runbook).
- [`EXTERNAL_ADVISER_ROUTER.md`](../../../Admin/O5-1/Operations/PMO/canonicals/EXTERNAL_ADVISER_ROUTER.md) — discipline lookup / routing.
- [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../Admin/O5-1/Operations/PMO/canonicals/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) — PMO portfolio hub (the `PRJ-HOL-FOUNDING-2026` row lives here).

### Machine-readable canonical registers (CSV)

- [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../Admin/O5-1/People/Compliance/canonicals/advops/ADVISER_ENGAGEMENT_DISCIPLINES.csv) — adviser disciplines registry.
- [`ADVISER_OPEN_QUESTIONS.csv`](../../../Admin/O5-1/People/Compliance/canonicals/advops/ADVISER_OPEN_QUESTIONS.csv) — adviser-facing open questions (`Q-LEG-NNN`, `Q-FIS-NNN`, etc.).
- [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../Admin/O5-1/People/Compliance/canonicals/FOUNDER_FILED_INSTRUMENTS.csv) — legal / fiscal / IP / banking / certification / notary instruments register.
- [`GOI_POI_REGISTER.csv`](../../../Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv) — counterparty rows; filter `program_id = PRJ-HOL-FOUNDING-2026`.
- [`PROGRAM_REGISTRY.csv`](../../../Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv) — programs registry (the `PRJ-HOL-FOUNDING-2026` row).
- [`TOPIC_REGISTRY.csv`](../../../Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv) — topic registry; covers `topic_enisa_evidence`, `topic_enisa_dossier_es`, `topic_external_adviser_handoff`.

### Brand governance (external-register surfaces)

- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) — dual-register canonical (internal vocabulary vs external rendering).
- [`BRAND_JARGON_AUDIT.md`](../../../Admin/O5-1/Marketing/Brand/canonicals/BRAND_JARGON_AUDIT.md) §4.1 — forbidden tokens in external prose.
- [`BRAND_VOICE_FOUNDATION.md`](../../../Admin/O5-1/Marketing/Brand/canonicals/BRAND_VOICE_FOUNDATION.md) — voice canon for external-facing prose.

## Operator runbook (when editing files in this folder)

1. **Confirm asset class.** Is the file you're editing **rendered external prose** (in scope of BBR validator), **operator metadata** (manifest, frontmatter, mmd source), or **operator companion** (`.objections.md` / `.counterparty-brief.md` — exempt)? The rules differ.
2. **For rendered external prose.** Edit in the **external register**: refer to the program as "Holistika Research SL — Programa de fundación 2026" or the entity name "Holistika Research SL"; never paste `PRJ-HOL-` tokens; never paste `TODO[OPERATOR]` markers; never paste internal `D-IH-NN-X` decision IDs; never paste operator-internal sources or hash blocks.
3. **Run BBR validator before commit.** `py scripts/validate_brand_baseline_reality_drift.py` must PASS.
4. **For new sub-folders / new topic visuals.** Mint the topic_id in `TOPIC_REGISTRY.csv` *first*, then the manifest under the topic's sub-folder, then the visual (`.mmd` + `.svg` via `py scripts/render_km_diagrams.py <path-to-.mmd>`).
5. **For new rendered prose.** Reference the canonical SOP (in the role-owner `canonicals/` folder) as the SSOT; the rendered prose is the **derived view** for adviser / regulator consumption.

## Cross-references

- Engagement README (reciprocal): [`Think Big/Advisers/2026-holistika-incorporation/README.md`](../../../../Think%20Big/Advisers/2026-holistika-incorporation/README.md).
- ADVOPS plane cursor rule: [`akos-adviser-engagement.mdc`](../../../../../../../.cursor/rules/akos-adviser-engagement.mdc).
- BBR dual-register cursor rule: [`akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc).
- Initiative cluster context: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`](../../../../../../../docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md) (program-anchor governance + OPS-86-5 BBR triage).
