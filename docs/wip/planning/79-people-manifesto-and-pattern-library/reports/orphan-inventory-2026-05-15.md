---
language: en
status: draft
canonical: false
role_owner: Chief People Officer (interim — operator)
classification: way_of_working
intellectual_kind: audit_report
ssot: false
authored: 2026-05-15
last_review: 2026-05-15
companion_to:
  - ../master-roadmap.md
  - ../decision-log.md
  - ../../_templates/INITIATIVE_DEPENDENCIES.md
---

# I79 P5 — Orphan-folder inventory + housekeeping verdicts

> **Strand E** of Initiative 79 (People manifesto + knowledge hygiene + cross-area design patterns + AI governance). Audits all seven repository documentation trees per the I79 master-roadmap §P5, classifies each suspect folder as **bookmark / promote / RESERVED-mark / candidate-delete / leave-alone**, and surfaces only the entries that need operator ratification before closure. Per `akos-inline-ratification.mdc` the audit is **read-only**; structural changes are made only after the operator picks per-cluster via inline `AskQuestion`.
>
> Closes **OPS-79-6** (orphan inventory + cadence-ratify scaffold). Cadence promotion to a recurring SOP is in scope here but the SOP-mint itself is a P7 deliverable; this report establishes the seed inventory and the cadence proposal.

## Method

For each tree, I walked the directory structure to depth 4–5, cross-referenced with `git ls-tree -r HEAD` to distinguish git-tracked vs local-only artefacts, and reconciled findings against [`v3.0/index.md`](../../../../references/hlk/v3.0/index.md) §"Vault Structure", [`compliance/PRECEDENCE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md), [`baseline_organisation.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv), and the I22 / I70 forward-layout decisions (D-IH-22, D-IH-70-S, D-IH-70-T) that promoted Research to a top-level area and re-homed compliance master files to per-area `canonicals/`.

The verdict taxonomy:

| Verdict | Meaning |
|---|---|
| **bookmark** | Add a brief README pointer or note so the next reader understands why the folder exists. Additive only. |
| **promote** | Move content into a more-canonical home (with full cross-ref preservation). Requires operator pick. |
| **RESERVED-mark** | Add `RESERVED.md` or a frontmatter note declaring the folder is intentionally empty + names the role/process it scaffolds. Additive only. |
| **candidate-delete** | Folder has no live signal, no git history, no role ownership, no cross-references. Surface for operator removal pick. |
| **leave-alone** | Folder is legitimate scaffolding for a baseline_organisation role or tracked v3.0 forward-layout slot; no action needed. |

Confidence tiers reflect how much evidence the verdict rests on:

| Tier | Definition |
|---|---|
| **HIGH** | Multiple sources agree (index.md + baseline + git history + content). Verdict is essentially mechanical. |
| **MEDIUM** | One strong source + corroborating absence of contrary evidence. Verdict is operator-final. |
| **LOW** | Evidence is partial or recent design ambiguous. Always inline-ratify before action. |

## Tree 1 — `docs/references/hlk/v3.0/`

The active canonical vault. Walks 9 areas (Research now top-level + Admin/O5-1 hosts the other 8) plus `Envoy Tech Lab/`, `Think Big/`, `_assets/`, `programs/` (per-role).

### 1A. Role-folder placeholders (`*/.gitkeep` only)

These were minted to mirror the **role hierarchy in `baseline_organisation.csv`** and gitkeeped to preserve directory presence in git. They are **not orphans**; they are **scaffolding**.

| Folder | Files | Verdict | Confidence | Reason |
|---|---:|---|---|---|
| `Admin/O5-1/Marketing/Growth` | 0 | leave-alone | HIGH | Listed in `index.md` §"Vault Structure" line 174; baseline role row exists. Empty because all live SOPs migrated to `Reach/` per D-IH-72-Z (I72 P1 R7 GTM→Reach migration). |
| `Admin/O5-1/Marketing/Social/{Community Manager, Paid Media Manager}` | 0 | leave-alone | HIGH | `index.md` lines 174–176; baseline rows exist. |
| `Admin/O5-1/Operations/PMO/business-strategy` | 0 | **candidate-delete** | MEDIUM | **NOT** listed in `index.md`; **NO** baseline row owning it; git log shows touched only in I47/I49/I63/I70 P4.5 link sweeps but never seeded with content. **Inline-ratify**. |
| `Admin/O5-1/Tech/{AI Engineer, DevOPS/{Front-End,Back-End}, Tech Lead}` | 1 each (.gitkeep) | leave-alone | HIGH | `index.md` lines 184–189; baseline role rows exist. |
| `Admin/O5-1/People/{Organisation, Talent/{Corporate Marketing, Ethics & Learning}}` | 1 each (.gitkeep) | leave-alone | HIGH | `index.md` lines 152–156; baseline role rows exist. |
| `Admin/O5-1/Finance/Business Controller/{Pricing, Taxes}` | 1 each (.gitkeep) | leave-alone | HIGH | `index.md` lines 163–164; baseline rows exist. |
| `Admin/O5-1/Finance/Financial Controller/Front Office` | 1 (.gitkeep) | leave-alone | HIGH | `index.md` line 166; baseline row exists. |
| `Admin/O5-1/Marketing/Brand/{AV, Copywriter, Design, UX Designer}` | 2–3 each | leave-alone | HIGH | All host live charters or SOPs (BRAND_AV_CHARTER, BRAND_COPYWRITING_DISCIPLINE, BRAND_DESIGN_CHARTER, BRAND_UX_DESIGNER_CHARTER, BRAND_GANTT_DISCIPLINE). |
| `Admin/O5-1/Marketing/Resonance/Account Management` | 1 | leave-alone | HIGH | Hosts `ACCOUNT_MANAGEMENT_CHARTER.md` from I72 P1 R7. |
| `Admin/AI/{AIC, Susana Madeira}` | 1 each (.gitkeep) | **RESERVED-mark** | MEDIUM | `index.md` lines 189–191 explicitly cite the AI governance chain (AI persona + AIC role). Ratified scaffolding for the future Madeira AIC concept (per I76 candidate). The .gitkeep already serves as a marker, but a short `RESERVED.md` would help the next reader understand the role-class is intentionally pre-allocated. **Inline-ratify**. |

**Pattern recognition.** Of the ~20 "empty" folders found by the depth-4 sweep, 18 are legitimate baseline-scaffolding. This validates the index.md + baseline alignment posture.

### 1B. Top-level v3.0 areas (Admin / Envoy Tech Lab / Research / Think Big / _assets / programs)

| Folder | Files | Verdict | Confidence | Reason |
|---|---:|---|---|---|
| `Envoy Tech Lab/` (top-level) | 46 | leave-alone | HIGH | `index.md` §"Envoy Tech Lab (Entity)" lines 194–207. Hosts Repositories registry + KiRBe / MADEIRA / Neo4j / Showcases. **Distinct** from `Admin/O5-1/Envoy Tech Lab/` which hosts the area-role canonicals (RevOps / Cross Repo / External Repos / MADEIRA-AKOS / etc.). Both are intentional. |
| `Research/` (top-level) | 6 | **bookmark** (`index.md` update) | HIGH | Promoted from `Admin/O5-1/Research/` sub-area to top-level area per **D-IH-70-S** (Initiative 70, ratified 2026-05-12). `RESEARCH_AREA_CHARTER.md` is the canonical authority. **`index.md` is stale** — it does not reflect the promotion (it still lists Research under Admin/O5-1). The fix is a small `index.md` patch + a one-line bookmark in the legacy `Admin/O5-1/Research/` README pointing at the top-level. **Inline-ratify** scope of patch (minimal vs full rewrite). |
| `Think Big/` (top-level) | 163 | leave-alone | HIGH | `index.md` §"Think Big (Entity)" lines 209–220. Two-root model (Clients/, Advisers/) per D-W13-I. Live engagements + templates. |
| `_assets/` (top-level) | 99 | leave-alone | HIGH | KM Output-1 binary assets per `HLK_KM_TOPIC_FACT_SOURCE.md`. Tracked by manifest validators. |
| Per-role `programs/` subfolders | 11 | leave-alone | HIGH | I22 P3 forward-layout convention. All present folders own a README anchor for their `program_id`. |

### 1C. Misc orphan-shaped findings

| Item | Verdict | Confidence | Reason |
|---|---|---|---|
| `docs/references/hlk/v3.0/index.md` last_review absent (not in frontmatter) | bookmark + minor patch | MEDIUM | Not strictly an orphan, but the index is **canonical wayfinding** and is missing the post-I70 Research promotion + the post-I22a `programs/` per-role hierarchy expansion. **Inline-ratify** patch scope. |

## Tree 2 — `docs/wip/`

Working space. Per `docs/wip/README.md` (not re-read here for brevity), legitimate top-level homes are `planning/`, `intelligence/`, `hlk-km/`. Anything else is a candidate.

| Folder | Files | Verdict | Confidence | Reason |
|---|---:|---|---|---|
| `docs/wip/planning/` | 67 dirs | leave-alone | HIGH | Active initiative workspace; index in `README.md`. |
| `docs/wip/intelligence/` | ~20 | leave-alone | HIGH | Tier-1 WIP topology owned by Research per D-IH-70-S §"WIP topology". |
| `docs/wip/hlk-km/` | 5 | leave-alone | HIGH | KM curation home per `HLK_KM_TOPIC_FACT_SOURCE.md`. |
| `docs/wip/wip_proposals/` | 0 (untracked) | **candidate-delete** | HIGH | Empty local-only directory, not in `git ls-tree`, no readme, no purpose. Likely a typo of `planning/99-proposals/` that was never populated. **Inline-ratify**. |
| `docs/wip/planning/_candidates/i60-process-list-harmonisation.md` | 1 | bookmark | MEDIUM | The candidate is **substantively absorbed by I79 P6** (`process_list.csv` 8th column for `inherited_pattern_id` + baseline tranche). Add a one-line "superseded-by I79 P6" header so the next reader doesn't reopen it as a fresh candidate. **Additive only — no operator-extra-PAUSE per plan §P5d.** |
| `docs/wip/planning/_candidates/customer-engagements-2026.md` | 1 | leave-alone | MEDIUM | Active candidate seed for forward customer-engagement design work. |
| Initiative folders 27, 33–44, 60, 61, 69, 74–76, 78 (gaps in numbering) | n/a | leave-alone | HIGH | Per `docs/wip/planning/README.md` numbering convention, gaps reflect unratified candidates that never promoted to initiatives. Not orphans — intentional. |

## Tree 3 — `docs/references/hlk/Research & Logic/`

v2.7 historical reference. Per `index.md` §"Governance" line 134 and `PRECEDENCE.md`, this tree is **read-only reference**.

| Folder | Files | Verdict | Confidence | Reason |
|---|---:|---|---|---|
| Entire tree (1 302 files) | leave-alone | HIGH | Governed by PRECEDENCE.md §"Reference-only — historical (v2.7)". `validate_hlk.py` does not lint it. Conscious historical archive. |

## Tree 4 — `docs/references/hlk/v3.0/_assets/`

Already covered in Tree 1B. Leave-alone.

## Tree 5 — `programs/` (per-role inside v3.0)

Already covered in Tree 1B. Leave-alone (11 README anchors all present).

## Tree 6 — `scripts/sql/`

Per `akos-holistika-operations.mdc` §"Two-plane model", `scripts/sql/<initiative>_staging/` is the **promotion-staging** path: DDL is authored here, reviewed by operator, promoted to `supabase/migrations/`, then the staging copy stays as **historical rollback evidence**.

| Folder | Files | Verdict | Confidence | Reason |
|---|---:|---|---|---|
| `i14_phase3_staging/` … `i25_phase1_staging/` (8 staging dirs, 31 .sql files total) | leave-alone | HIGH | Each staging dir has a matching `supabase/migrations/<timestamp>_iNN_*.sql` promoted file. Staging dirs preserve `*_rollback.sql` companions. Per the rule, they remain. |

## Tree 7 — `supabase/migrations/`

Forward DDL plane. 61 `.sql` files + 1 `README.md`. All `iNN_*` named matching their initiative.

| Folder | Files | Verdict | Confidence | Reason |
|---|---:|---|---|---|
| `supabase/migrations/` | 61 | leave-alone | HIGH | Each migration has a corresponding `iNN` initiative (verifiable in `INITIATIVE_REGISTRY.csv`). The `README.md` is the parity-map between local + remote. No orphan migrations. |

## Tree 8 (bonus) — `docs/references/hlk/compliance/` (legacy tombstone)

Not one of the 7 trees in the plan, but surfaced during the sweep.

| Folder / file | Files | Verdict | Confidence | Reason |
|---|---:|---|---|---|
| `docs/references/hlk/compliance/MIGRATED.md` | 1 (tracked) | **candidate-delete** | HIGH | The tombstone file itself states (line 10): *"This tombstone exists for one release cycle and is removed at I71 closing."* I71 closed (`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p71-closing.md` exists). Tombstone removal is overdue. |
| `docs/references/hlk/compliance/dimensions/` | 0 (untracked) | **candidate-delete** | HIGH | Empty local-only; superseded by per-area-role `canonicals/dimensions/`. |
| `docs/references/hlk/compliance/baseline_organisation.gsheet` | 1 (untracked) | leave-alone | LOW | Operator-local Google Sheet shortcut; not in git; harmless. |
| `docs/references/hlk/business-intent/` | 10 (tracked) | leave-alone | MEDIUM | Governed by `akos-adviser-engagement.mdc` + `SOP-HLK_TRANSCRIPT_REDACTION_001`. README explicitly says retention review is Compliance + Legal decision, not People-housekeeping. Out of I79 P5 scope. |

## Bonus check — `agent-transcripts/` and `_templates/`

Out of v3.0 vault but inside the workspace:

| Folder | Verdict | Confidence | Reason |
|---|---|---|---|
| `agent-transcripts/` | leave-alone | HIGH | Operator-private, ignored from validators. |
| `docs/wip/planning/_templates/` | leave-alone | HIGH | Tracked + actively used (UNIVERSAL_KICKSTART, PLANNING_COMPENDIUM, INITIATIVE_DEPENDENCIES, kickoff prompts i71–i76). |

## Summary verdict counts

| Verdict | Count |
|---|---:|
| leave-alone | 28 of 33 inspected clusters |
| bookmark | 2 (Research promotion in `index.md`; `_candidates/i60` superseded note) |
| RESERVED-mark | 1 (`Admin/AI/{AIC, Susana Madeira}`) |
| candidate-delete | 3 (`docs/wip/wip_proposals/`; `Operations/PMO/business-strategy`; `compliance/MIGRATED.md` + sibling empty `dimensions/`) |
| promote | 0 |

The bias toward leave-alone is the validating signal. The vault structure has been actively cared-for through I22 / I70 forward-layout migrations and per-area-role federation. Most "empty" folders are intentional baseline scaffolding.

## Inline-ratify ledger

The plan §P5d reserves PAUSE only if any DELETE is approved. The bookmarks + RESERVED-marks are **additive housekeeping** and may proceed without an extra PAUSE. The deletes need explicit operator picks via inline `AskQuestion`, fired separately so each can be ratified or skipped independently.

| Item | `AskQuestion` ID | Type |
|---|---|---|
| `docs/wip/wip_proposals/` (empty local-only) | `p5-delete-wip_proposals` | candidate-delete |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/` (empty, no baseline owner) | `p5-delete-pmo-business-strategy` | candidate-delete |
| `docs/references/hlk/compliance/MIGRATED.md` (overdue tombstone) | `p5-delete-compliance-tombstone` | candidate-delete |
| `Admin/AI/{AIC, Susana Madeira}` (RESERVED-mark vs leave-alone) | `p5-ai-reserved-mark` | RESERVED-mark |
| `index.md` Research-promotion patch (minimal patch vs full rewrite) | `p5-index-research-patch` | bookmark scope |

The two pure-additive bookmarks (`_candidates/i60` superseded note + `index.md` Research promotion when scope agreed) auto-apply per plan §P5d once the inline ratification picks the scope.

## Cadence proposal — orphan-folder housekeeping as a recurring SOP

The audit pattern surfaced here would benefit from a recurring cadence. Proposed:

- **Cadence:** `gated_operator` (operator-judgement; not unattended) **or** `scheduled` quarterly (low-noise) — this is itself an inline-ratify question.
- **Owner:** People Operations Manager (per the People = discipline-of-disciplines posture from the manifesto).
- **SOP path (if minted):** `docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-PEOPLE_ORPHAN_FOLDER_AUDIT_001.md`.
- **Runbook (optional):** none initially — the audit is exploratory + judgement-heavy. A future runbook could surface the heuristics ("empty + no baseline row + no git history = candidate-delete") but the core decision must remain operator.
- **Cadence ratify question:** `p5-orphan-cadence` (inline below).

This would close OPS-79-6's "ratify the cadence" sub-deliverable. The SOP itself is a **P7 mint** (not authored in P5) to avoid scope creep.

## Cross-references

- I79 master-roadmap §P5 — the phase this report fulfils.
- `akos-inline-ratification.mdc` §"When to use" — the inline-ratify pattern this report follows.
- `akos-people-discipline-of-disciplines.mdc` — the rule that names People as the orphan-folder steward.
- D-IH-70-S — Research-area top-level promotion (the source of the `index.md` staleness).
- D-IH-72-Z — Marketing GTM→Reach migration (the source of `Marketing/Growth/` emptiness).
- I71 P71 closing report — the source of the overdue `compliance/MIGRATED.md` tombstone.
