---
language: en
intellectual_kind: migration_proposal
sharing_label: internal_only
status: resolved
authored: 2026-05-29
last_review: 2026-06-10
parent_wave: I86 Wave R+5
ratifying_decisions:
  - D-IH-75-G
---

# Legacy Research tree migration — status + remaining gated moves

**Source tree (legacy):** `docs/references/hlk/v3.0/Admin/O5-1/Research/`
**Target topology:** `docs/references/hlk/v3.0/Research/<discipline>/` (area harmonization per Wave R+5 plan + the lifecycle doctrine)

## Status update (D-IH-75-G, 2026-05-29)

The Research-area logic change (CORPINT lifecycle elevated to the spine; disciplines reframed as
crafts; cross-area joins made first-class) **resolved the technique-folder half of this proposal a
different way** than the original "migrate the folders" plan:

- The six technique folders under `Admin/O5-1/Research/` were **empty husks** (one `.gitkeep` each,
  never populated since the 2026-04-01 scaffold). They were **DELETED**, not moved.
- The discipline sub-areas were **built new** directly under the disciplines as capability-seeded
  index READMEs (`Research/Methodology/{Pillars,Techniques,Deep-Research}/` +
  `Research/Intelligence/{HUMINT,OSINT,Matrix}/`). Migrating empty husks would have achieved nothing
  and re-imported the rejected "tools-shed" taxonomy.

So the technique-folder rows in the original proposal are **closed (resolved-by-rebuild)**. What
remains below is the **markdown + SSOT-CSV** migration, which is genuinely gated.

## Already at top-level `Research/` (no move needed)

Area README + area charter + the new `RESEARCH_LIFECYCLE_DOCTRINE.md` + the four discipline charters
+ discipline indexes + technique sub-area indexes + `RESEARCH_ACTION_DISCIPLINE.md` +
`RESEARCH_RADAR_DISCIPLINE.md` + `GOI_POI_STANCE_DOCTRINE.md`.

## REMAINING moves — gated; NO `git mv` until operator confirms

> **Why gated.** Moving these is not free: the **IntelligenceOps register is an SSOT CSV** (its path
> change must update `PRECEDENCE.md` + `validate_intelligenceops_register.py` +
> `validate_compliance_schema_drift.py` + `akos/hlk_research_radar.py` FIELDNAMES references + the
> Supabase mirror emit — all in one commit), and the **SOP moves ripple into cursor-rule globs**
> (`akos-research-action.mdc` + `akos-research-radar.mdc` both glob the legacy `Admin/O5-1/Research/...`
> SOP paths) + PRECEDENCE rows 117–120. Bundling this into the area-logic build would have risked a
> broken-link / stale-glob regression. It is therefore a clean, self-contained follow-up commit.

| Legacy path | Proposed destination | Ripple to update in the SAME commit |
|:---|:---|:---|
| `Admin/O5-1/Research/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md` | `Research/canonicals/` | inbound links only |
| `Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md` | `Research/Methodology/canonicals/` | I75 master-roadmap `linked_canonicals`; PRECEDENCE |
| `Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md` | `Research/Methodology/canonicals/` | `akos-research-action.mdc` glob; PRECEDENCE row 118 |
| `Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md` | `Research/Methodology/canonicals/` | `akos-research-radar.mdc`; PRECEDENCE row 120 |
| `Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` | `Research/Methodology/canonicals/` | I75 `linked_canonicals`; PRECEDENCE |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_ELICITATION_DISCIPLINE_001.md` | `Research/Intelligence/canonicals/` | inbound links; Intelligence index |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_INTELLIGENCE_REPORT_001.md` | `Research/Intelligence/canonicals/` | inbound links; Intelligence index |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md` | `Research/Intelligence/canonicals/` | inbound links |
| `Admin/O5-1/Research/Intelligence/canonicals/SOP-RESEARCH_ENGAGEMENT_TRIGGER_001.md` | `Research/Intelligence/canonicals/` | adapter-registry handoff SOP refs; PRECEDENCE row 54 |
| `Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` | `Research/Intelligence/canonicals/dimensions/` | **SSOT path change** — PRECEDENCE row 55 + `validate_intelligenceops_register.py` + `validate_compliance_schema_drift.py` + `akos/hlk_research_radar.py` + `scripts/research_radar_sweep.py` + Supabase mirror emit |

## Post-move cleanup (same confirmed commit)

1. Remove the empty `Admin/O5-1/Research/` tree once all files moved.
2. Grep-replace inbound links from `Admin/O5-1/Research/` → `Research/` across vault + wip + the two cursor-rule globs.
3. Update `PRECEDENCE.md` rows 54, 55, 117–120 to the new paths.
4. Re-run `py scripts/validate_hlk.py` + `py scripts/validate_compliance_schema_drift.py` + `py scripts/research_radar_sweep.py`.

## Operator decision requested (remaining moves only)

- [x] **Approve remaining moves as-is** — executed 2026-06-10 (OPS-86-26 closure; operator Q1=B).
- [ ] **Approve the markdown SOP moves now, defer the SSOT-CSV register move** — superseded by full-bundle ratification.
- [ ] **Amend** — reply with path corrections before any mv.
