# Regression sweep — Wave-L close — 2026-05-21

**Report ID:** `regression-sweep-2026-05-21`  
**Swept by:** agent:inter_wave_regression_sweep  
**Wave closing:** Wave-L  

## Counts

| Verdict | Count |
| --- | --- |
| clean | 7 |
| drift | 15 |
| gap | 4 |
| blocked | 0 |
| skip | 3 |
| **TOTAL** | **29** |

## Findings

| Dimension | Surface | Verdict | Severity | Proposed action | Notes |
| --- | --- | --- | --- | --- | --- |
| DIM-01-CLOSING-WAVE-SURFACES | `git-log:Wave-L` | clean | low |  | 23 files touched across 2 commits; all present |
| DIM-02-SIBLING-INITIATIVE-STATUS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` | clean | low |  | all status enum values valid; FK sweep skipped (Supabase MCP not invoked in self-test) |
| DIM-03-I86-COORDINATOR-STATE | `docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md` | clean | low |  | last_review=2026-05-17; days_since=4 |
| DIM-04-QUALITY-FABRIC-SPECIALTIES | `HOLISTIKA_QUALITY_FABRIC.md::DATAOPS_DISCIPLINE.md` | gap | medium | mint DATAOPS_DISCIPLINE.md or update fabric to drop the reference | §6 references DATAOPS_DISCIPLINE.md but file not found under canonicals/ |
| DIM-04-QUALITY-FABRIC-SPECIALTIES | `HOLISTIKA_QUALITY_FABRIC.md::MKTOPS_DISCIPLINE.md` | gap | medium | mint MKTOPS_DISCIPLINE.md or update fabric to drop the reference | §6 references MKTOPS_DISCIPLINE.md but file not found under canonicals/ |
| DIM-04-QUALITY-FABRIC-SPECIALTIES | `HOLISTIKA_QUALITY_FABRIC.md::TECHOPS_DISCIPLINE.md` | gap | medium | mint TECHOPS_DISCIPLINE.md or update fabric to drop the reference | §6 references TECHOPS_DISCIPLINE.md but file not found under canonicals/ |
| DIM-04-QUALITY-FABRIC-SPECIALTIES | `HOLISTIKA_QUALITY_FABRIC.md::UX_DISCIPLINE.md` | gap | medium | mint UX_DISCIPLINE.md or update fabric to drop the reference | §6 references UX_DISCIPLINE.md but file not found under canonicals/ |
| DIM-05-FORWARD-CHARTER-GATES | `docs/wip/planning/_candidates` | clean | low |  | no candidates exceed 90-day staleness threshold |
| DIM-06-SIBLING-REPO-DEPLOY-POSTURE | `sibling-repos:hlk-erp;boilerplate;kirbe-platform` | skip | low | re-probe with Vercel/Render MCP at P3 sweep with --mcp flag | MCP probes deferred to live sweep; runbook smoke-tested without external deps |
| DIM-07-RENDER-PENDING-TRACKER | `docs/wip/planning/_trackers/external-render-pending-tracker.md` | clean | low |  | approx_pending_rows=4; last_review=2026-05-19 |
| DIM-08-PRE-EXISTING-RELEASE-GATE-FAILS | `scripts/release-gate.py` | skip | low | invoke release-gate --dry-run at P3 sweep (deferred to live run) | self-test path defers release-gate invocation to avoid recursion / runtime cost |
| DIM-09-CURSOR-RULES-DRIFT | `.cursor/rules/` | clean | low |  | 18 akos-*.mdc rules present; deep parity check deferred to P3 sweep |
| DIM-10-SKILLS-DRIFT | `.cursor/skills/` | clean | low |  | 3 SKILL.md files present; deep parity deferred to P3 sweep |
| DIM-11-UNTRACKED-FILES-AUDIT | `.cursor/rules/akos-deploy-health.mdc` | drift | low | stage + commit OR add to .gitignore (bucket=.cursor/) | untracked/modified file in classification bucket=.cursor/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `.cursor/rules/akos-docs-config-sync.mdc` | drift | low | stage + commit OR add to .gitignore (bucket=.cursor/) | untracked/modified file in classification bucket=.cursor/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `.cursor/rules/akos-madeira-management.mdc` | drift | low | stage + commit OR add to .gitignore (bucket=.cursor/) | untracked/modified file in classification bucket=.cursor/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `.cursor/rules/akos-quality-fabric.mdc` | drift | low | stage + commit OR add to .gitignore (bucket=.cursor/) | untracked/modified file in classification bucket=.cursor/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `akos/hlk_design_pattern_csv.py` | drift | low | stage + commit OR add to .gitignore (bucket=akos/) | untracked/modified file in classification bucket=akos/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `config/verification-profiles.json` | drift | low | stage + commit OR add to .gitignore (bucket=other) | untracked/modified file in classification bucket=other |
| DIM-11-UNTRACKED-FILES-AUDIT | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` | drift | low | stage + commit OR add to .gitignore (bucket=docs/) | untracked/modified file in classification bucket=docs/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv` | drift | low | stage + commit OR add to .gitignore (bucket=docs/) | untracked/modified file in classification bucket=docs/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv` | drift | low | stage + commit OR add to .gitignore (bucket=docs/) | untracked/modified file in classification bucket=docs/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md` | drift | low | stage + commit OR add to .gitignore (bucket=docs/) | untracked/modified file in classification bucket=docs/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `docs/wip/planning/86-initiative-cluster-execution-coordinator/files-modified.csv` | drift | low | stage + commit OR add to .gitignore (bucket=docs/) | untracked/modified file in classification bucket=docs/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `scripts/release-gate.py` | drift | low | stage + commit OR add to .gitignore (bucket=scripts/) | untracked/modified file in classification bucket=scripts/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `tests/test_design_pattern_registry.py` | drift | low | stage + commit OR add to .gitignore (bucket=other) | untracked/modified file in classification bucket=other |
| DIM-11-UNTRACKED-FILES-AUDIT | `.cursor/rules/akos-inter-wave-regression.mdc` | drift | low | stage + commit OR add to .gitignore (bucket=.cursor/) | untracked/modified file in classification bucket=.cursor/ |
| DIM-11-UNTRACKED-FILES-AUDIT | `akos/hlk_inter_wave_regression.py` | drift | low | stage + commit OR add to .gitignore (bucket=akos/) | untracked/modified file in classification bucket=akos/ |
| DIM-12-CANONICAL-CSV-MIRROR-PARITY | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals` | skip | low | invoke `py scripts/verify.py compliance_mirror_emit` at live P3 sweep | 34 canonical CSVs found; live mirror parity deferred to MCP-enabled run |

---

Per `akos-inter-wave-regression.mdc` RULE 3: every non-clean finding
MUST become one `AskQuestion` option set at P4 (inline-ratify gate).
