---
language: en
status: active
initiative: 32-holistik-ops-maturation
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-04-30
---

# Initiative 32 — Decision log

| ID | Date | Decision | Rationale | Status |
|:---|:-----|:---------|:----------|:-------|
| **D-IH-32-A** | 2026-04-30 | Promote Topic to **axis 6** of Holistik Ops (after Persona, Channel, Distance, Language, Artifact-class). | Topic Registry is canonical since Initiative 25; promoting to axis removes the "guess the topic" failure mode in routing. The HOLISTIK_OPS_DISCOVERY.md doctrine and the 5 dimension CSVs all already implicitly carry topic; making it explicit lets skills route on `(persona × channel × topic)` cells. | **Approved** |
| **D-IH-32-B** | 2026-04-30 | Add `compliance/dimensions/SKILL_REGISTRY.csv` as the **7th canonical dimension**. | Skill-shaped artifacts live in 4 unaligned places today (`prompts/base/`, `.cursor/skills/`, `config/workspace-scaffold/<agent>/IDENTITY.md`, `config/agent-capabilities.json`). Multiagentic decomposition has no SSOT. Promoting skill to a governed CSV makes it a queryable asset that doubles as the MADEIRA-SaaS productisation substrate. | **Approved** |
| **D-IH-32-C** | 2026-04-30 | Add `compliance/dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv`. | The I31 touchpoint-kit is filesystem-only (8 cells under `_assets/touchpoint-kit/`). Runtime cannot query "all `(persona × channel × language)` cells". Cell registry + FS-drift validator closes the gap. | **Approved** |
| **D-IH-32-D** | 2026-04-30 | Move `GOI_POI_REGISTER.csv` from `compliance/` to `compliance/dimensions/`. Keep one-cycle deprecation alias. | Last canonical knowledge dimension still at root; closes the I22 forward-layout convention gap. | **Approved** |
| **D-IH-32-E** | 2026-04-30 | Move `SOP-HLK_LOCALISATION_001.md` from `Tech/System Owner/` to `Marketing/Brand/`. Validator stays in Tech (where script lives); SOP moves to its policy owner; cross-reference both ways. | Brand owns voice; Tech owns the validator script. Cleaner role split. | **Approved** |
| **D-IH-32-F** | 2026-04-30 | Split `scripts/validate_hlk.py` into a **dispatcher + per-validator graph** with structured JSON report and a new `compliance.validation_runs` operational mirror. Backward-compatible CLI is non-negotiable. | Audit-grade history. Required before adding 3 new dimensions piles on a single binary. | **Approved** |
| **D-IH-32-G** | 2026-04-30 | KiRBe sync contract is **frozen** until I32-P9. Communicate to KiRBe team in P0 (freeze memo). | Avoids parallel divergence while the canonical mirror set grows from 3 (current §2) to 12 (true canonical set). | **Approved** |
| **D-IH-32-H** | 2026-04-30 | ERP prod-readiness gates 1-3 (auth, tenancy RLS, rollback runbook) ship as **Initiative 33**, not as part of I32. I32 ships only the read-side handoff bundle. | I32 stays in ops governance. Prod is a different risk profile. |  **Approved** |
| **D-IH-32-I** | 2026-04-30 | Skills **lazy-load** (Cursor pattern), not eager-load. Each agent prompt carries 1-2 line skill descriptions; full body loads only when invoked. | Avoids prompt bloat. Aligns with the existing Cursor `agent_skills` block pattern. | **Approved** |
| **D-IH-32-J** | 2026-04-30 | Skill registry has `tenant_scope` column from day 1. Validator enforces `^shared$` as the only valid value until a future MADEIRA-SaaS initiative opens tenant scopes. | Day-1 tenant-aware schema; zero migration cost when MADEIRA-SaaS productises. | **Approved** |
| **D-IH-32-K** | 2026-04-30 | External repos (`boilerplate`, `hlk-erp`, `kirbe`) governed via a **one-way EXTERNAL_REPO_CONTRACT.md** seed at their root + a small `.cursor/rules/akos-mirror.mdc` cursor rule that imports AKOS HLK doctrine without copying it. AKOS stays SSOT; external repos consume; nothing flows from external to AKOS as authoring. | Closes the "MADEIRA-Cursor deployed in every repo but uninformed by AKOS doctrine" gap (E12). | **Approved** |
| **D-IH-32-L** | 2026-04-30 | Cross-repo extraction is **pull-based**. AKOS reads external repo state into `compliance/REPO_HEALTH_SNAPSHOT.csv` (mirror, ingested by `scripts/snapshot_external_repos.py`). KiRBe and ERP push nothing to AKOS authoring surfaces. Snapshot cadence: weekly (cron) + on-demand. | Same governance pattern as Stripe FDW (read projection, external is authoritative for source code). | **Approved** |
| **D-IH-32-M** | 2026-04-30 | Neo4j projection extends to `:Persona`, `:Channel`, `:Sourcing`, `:Skill`, `:TouchpointKitCell`, `:Policy` nodes plus cross-axis typed edges. **Single AKOS Neo4j instance is canonical for governance.** KiRBe's local Neo4j (per its `60-graphdb-neo4j.mdc`) is a separate operational graph for vault search and stays independent. No cross-instance merge. | Closes E15 (one initiative behind). KiRBe's vault graph and AKOS governance graph have different shapes and audiences; merging would couple them. | **Approved** |
| **D-IH-32-N** | 2026-04-30 | Boilerplate registered as `repo_class=reference` in `REPOSITORIES_REGISTRY.md` (light-touch). No SSOT obligation; embedded Obsidian vault snapshot at `app/dashboard/applications/kms/obsidian-holistika-main/` explicitly **NOT canonical** (the AKOS `docs/references/hlk/v3.0/` tree is the live Obsidian-anchored SSOT). Brand assets remain visual reference per `BRAND_VISUAL_PATTERNS.md`. | Boilerplate is the marketing/web boilerplate with its own Supabase, Pinecone, n8n, RAG plan. Useful as visual reference + future patterns informer. Not part of the active vault. | **Approved** |
| **D-IH-32-O** | 2026-04-30 | **R-32-2 gate is HARD**: I31 mirror reseed has NOT been applied yet. P0 will pause at P0-A6 after creating the initiative folder; operator runs `npx supabase db push` for the 4 outstanding I31 surfaces and confirms via `py scripts/probe_compliance_mirror_drift.py --verify`. Only then does P1 start. No skipping. | Operator answer 2026-04-30 to question i31_reseed: chose `no_apply_now`. Avoids R-32-2 collision risk completely. | **Approved** |
| **D-IH-32-P** | 2026-04-30 | External-repo PR delivery format: **patches + bilingual cover-email drafts** (one per team), EN + ES siblings per `SOP-HLK_LOCALISATION_001.md` D-IH-31-A audience-canonical rule. Operator forwards the emails. P9-A8, P10-A11, P11-A6 ship the email drafts. | Operator answer 2026-04-30 to question external_repo_pr_mode: chose `patches_plus_email`. KiRBe and ERP team leads work in ES; engineering threads happen in EN. | **Approved** |
| **D-IH-32-Q** | 2026-04-30 | Neo4j P6 closes ONLY when **live sync succeeds against the configured Neo4j instance**. Dry-run-clean is necessary but not sufficient. P6-A8 (idempotent re-sync) must execute against the live instance and report the 6 new node label counts matching CSV row counts before P6 acceptance closes. | Operator answer 2026-04-30 to question neo4j_live_or_dry: chose `block_until_live`. Highest assurance posture. | **Approved** |

## Open questions (resolved in P0 dialogue or downstream phases)

- **Q1** Touchpoint-kit physical relocation now or defer? **Recommendation: defer (Initiative 35).** Decision: TBD-FOUNDER.
- **Q2** Skill registry granularity: per-skill (with `agents_supported` semicolon-list) or per-`(skill, agent)` pair? **Recommendation: per-skill** for parity with persona × channel pattern. Decision: TBD-FOUNDER.
- **Q3** `validation_runs` mirror class: operational or git-canonical JSON? **Recommendation: operational** (same pattern as `finops.registered_fact`). Decision: TBD; provisionally operational.
- **Q4** `policy_register.csv` scope: RLS only or all of RLS + service_role rotation + redaction? **Recommendation: all three.** Decision: TBD-COMPLIANCE.
- **Q5** Topic propagation to touchpoint-kit cells: now or later? **Recommendation: now**; cells already implicitly carry topic. Decision: TBD-PMO.
- **Q6** KiRBe consumption pattern: RLS read-only or versioned JSON snapshot? Decision: TBD-KIRBE-LEAD; resolved in P0 freeze memo dialogue.
- **Q7** REPO_HEALTH_SNAPSHOT cadence: weekly cron or on-PR webhook? **Recommendation: weekly + on-demand**; webhook is Initiative 42. Decision: TBD-AI-ENGINEER.
- **Q8** Neo4j extension scope: ship all 6 new node labels in P6 or stage by axis? **Recommendation: ship all 6 together**; projection is small + additive. Decision: TBD-AI-ENGINEER.
- **Q9** EXTERNAL_REPO_CONTRACT.md location: at each external repo root or under `docs/`? **Recommendation: at root**, alongside README.md. Decision: TBD-FOUNDER.
- **Q10** HLK-ERP `data-ssot.mdc` rule: rewrite or supersede via akos-mirror.mdc? **Recommendation: supersede** (less invasive; respects ERP team ownership). Decision: TBD-ERP-LEAD.

## Re-evaluation triggers (cross-initiative, persistent)

- **D-IH-32-N — boilerplate Obsidian snapshot retirement.** Triggered by: founder migrates personal Obsidian workflow off boilerplate fully. Action: Initiative 43 replaces snapshot with pointer to AKOS `docs/references/hlk/v3.0/`.
- **D-IH-32-Q — Neo4j live sync.** Triggered by: any future change to graph node labels or edge types. Action: re-run `py scripts/sync_hlk_neo4j.py` against configured instance; capture Cypher count outputs in the closing initiative's report.
- **D-IH-32-K — KiRBe-ERP-boilerplate cross-repo discipline.** Triggered by: 4 consecutive weeks of REPO_HEALTH_SNAPSHOT drift in any external repo. Action: Initiative 42 (cross-repo CI integration via GitHub Actions).
- **D-IH-32-J — `tenant_scope` validator strictness.** Triggered by: founder commits to MADEIRA-SaaS productisation window (`TODO[OPERATOR-madeira-saas-window]`). Action: Initiative 34 opens `tenant_scope` regex to allow `^tenant:[a-z0-9_-]+$`.
