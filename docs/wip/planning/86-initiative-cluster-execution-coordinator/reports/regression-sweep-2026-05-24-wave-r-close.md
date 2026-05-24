# Regression sweep — Wave-R close — 2026-05-24

**Report ID:** `regression-sweep-2026-05-24`  
**Swept by:** agent:inter_wave_regression_sweep  
**Wave closing:** Wave-R  

## Counts

| Verdict | Count |
| --- | --- |
| clean | 6 |
| drift | 1 |
| gap | 39 |
| blocked | 0 |
| skip | 0 |
| **TOTAL** | **46** |

## Findings

| Dimension | Surface | Verdict | Severity | Proposed action | Notes |
| --- | --- | --- | --- | --- | --- |
| DIM-01-DECISION-LINEAGE | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` | clean | low |  | 400 decisions in register; all ratifying_decisions: frontmatter values FK-resolve (reverse-FK advisory sweep deferred to operator review) |
| DIM-02-FORWARD-CHARTER-CARRYOVER | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/MKTOPS_DISCIPLINE.md` | gap | low | land 'scripts/mktops_campaign_quality_check.py (paired runbook; same gate)' in a subsequent canonical OR mint a _candidates/ file for it OR file an OPS_REGISTER row | forward_charters: item 'scripts/mktops_campaign_quality_check.py (paired runbook; same gate)' has no observable carryover signal (no _candidates/ match, no OPS row) |
| DIM-02-FORWARD-CHARTER-CARRYOVER | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md` | gap | low | land 'SOP-PEOPLE_UAT_GOVERNANCE_001.md (paired SOP + addendum + runbook validate_uat_report.py)' in a subsequent canonical OR mint a _candidates/ file for it OR file an OPS_REGISTER row | forward_charters: item 'SOP-PEOPLE_UAT_GOVERNANCE_001.md (paired SOP + addendum + runbook validate_uat_report.py)' has no observable carryover signal (no _candidates/ match, no OPS row) |
| DIM-02-FORWARD-CHARTER-CARRYOVER | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md` | gap | low | land 'process_list.csv row hol_peopl_dtp_uat_governance_001' in a subsequent canonical OR mint a _candidates/ file for it OR file an OPS_REGISTER row | forward_charters: item 'process_list.csv row hol_peopl_dtp_uat_governance_001' has no observable carryover signal (no _candidates/ match, no OPS row) |
| DIM-02-FORWARD-CHARTER-CARRYOVER | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md` | gap | low | land 'PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_uat_class_taxonomy' in a subsequent canonical OR mint a _candidates/ file for it OR file an OPS_REGISTER row | forward_charters: item 'PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_uat_class_taxonomy' has no observable carryover signal (no _candidates/ match, no OPS row) |
| DIM-03-VALIDATOR-RAMP-CONSISTENCY | `verification-profiles.json;release-gate.py` | drift | medium | verify each promotion/relaxation cites a decision row in DECISION_REGISTER.csv with rationale | prior_sha=26dd13f; promotions_observed=1; relaxations_observed=0 |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=aic_capability_implementation_matrix; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=aic; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ARTIFACT_CLASS_REGISTRY.csv` | gap | medium | mint missing components: scripts-validator, supabase-mirror-migration | slug=artifact_class; missing_components=scripts-validator,supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=audience; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=capability_confidence; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=capability; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` | gap | medium | mint missing components: supabase-mirror-migration | slug=channel_touchpoint; missing_components=supabase-mirror-migration |
| DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv` | gap | medium | mint missing components: scripts-validator, supabase-mirror-migration | slug=component_primitive; missing_components=scripts-validator,supabase-mirror-migration |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:thi_marke_dtp_109` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['marke'] |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:hol_ops_pdiu_6` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['pdiu'] |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:SOP-ETL_MACROECON_INGESTION_001` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['macroecon', 'ingestion'] |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:gtm_ws_team_growth` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['team', 'growth'] |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:gtm_ws_ops_control` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['control'] |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:gtm_cl_028e05b3126789` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['028e05b3126789'] |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:gtm_cl_0370bec6e882ca` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['0370bec6e882ca'] |
| DIM-05-SOP-RUNBOOK-PAIRING | `process_list:gtm_cl_04ec26ad9a99ef` | gap | low | mint paired SOP under <area>/<role>/canonicals/ AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1 | no SOP or runbook token-match for item_id; tokens=['04ec26ad9a99ef'] |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `INITIATIVE_REGISTRY:INIT-OPENCLAW_AKOS-02` | gap | medium | mint reports/uat-*.md for closed initiative INIT-OPENCLAW_AKOS-02 | closed initiative INIT-OPENCLAW_AKOS-02 has no UAT report under 02-hlk-on-akos-madeira/reports/ |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `docs/wip/planning/07-hlk-neo4j-graph-projection/reports/uat-graph-explorer-browser-20260415.md` | gap | low | add §1 (closure summary) AND §3 (mechanical evidence) sections per UAT_DISCIPLINE.md §4 | UAT report for closed init INIT-OPENCLAW_AKOS-07 missing required class sections |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `docs/wip/planning/10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md` | gap | low | add §1 (closure summary) AND §3 (mechanical evidence) sections per UAT_DISCIPLINE.md §4 | UAT report for closed init INIT-OPENCLAW_AKOS-10 missing required class sections |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `INITIATIVE_REGISTRY:INIT-OPENCLAW_AKOS-15` | gap | medium | mint reports/uat-*.md for closed initiative INIT-OPENCLAW_AKOS-15 | closed initiative INIT-OPENCLAW_AKOS-15 has no UAT report under 15-hlk-api-lifecycle-governance/reports/ |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `docs/wip/planning/17-madeira-cursor-mode-parity/reports/uat-madeira-uc-20260425.md` | gap | low | add §1 (closure summary) AND §3 (mechanical evidence) sections per UAT_DISCIPLINE.md §4 | UAT report for closed init INIT-OPENCLAW_AKOS-17 missing required class sections |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `docs/wip/planning/18-hlk-finops-counterparty-stripe/reports/uat-stripe-finops-reconcile-20260423.md` | gap | low | add §1 (closure summary) AND §3 (mechanical evidence) sections per UAT_DISCIPLINE.md §4 | UAT report for closed init INIT-OPENCLAW_AKOS-18 missing required class sections |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `docs/wip/planning/22a-i22-post-closure-followups/reports/uat-i24-supabase-apply-20260504.md` | gap | low | add §1 (closure summary) AND §3 (mechanical evidence) sections per UAT_DISCIPLINE.md §4 | UAT report for closed init INIT-OPENCLAW_AKOS-22A missing required class sections |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `INITIATIVE_REGISTRY:INIT-OPENCLAW_AKOS-58` | gap | medium | mint reports/uat-*.md for closed initiative INIT-OPENCLAW_AKOS-58 | closed initiative INIT-OPENCLAW_AKOS-58 has no UAT report under 58-cycle-2-multi-track-forward/reports/ |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `INITIATIVE_REGISTRY:INIT-OPENCLAW_AKOS-70` | gap | medium | mint reports/uat-*.md for closed initiative INIT-OPENCLAW_AKOS-70 | closed initiative INIT-OPENCLAW_AKOS-70 has no UAT report under 70-holistika-os-self-governance/reports/ |
| DIM-06-UAT-REPORT-CLASS-COMPLETENESS | `INITIATIVE_REGISTRY:INIT-OPENCLAW_AKOS-71` | gap | medium | mint reports/uat-*.md for closed initiative INIT-OPENCLAW_AKOS-71 | closed initiative INIT-OPENCLAW_AKOS-71 has no UAT report under 71-cicd-discipline-and-aiops-baseline-maturity/reports/ |
| DIM-07-RENDER-TRAIL-AUDIENCE-MATCH | `scripts/validate_external_render_trail.py` | clean | low |  | --strict --strict-freshness PASS |
| DIM-08-BRAND-BASELINE-REGISTER-MATCH | `scripts/validate_brand_baseline_reality_drift.py` | clean | low |  | brand-baseline drift validator PASS |
| DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv` | clean | low |  | 21 pattern_ids; all observed in at least one breakthrough digest body |
| DIM-10-DEPLOY-EVIDENCE-COMPLETENESS | `docs/wip/planning/68-cicd-discipline-and-observability-maturity/files-modified.csv` | gap | medium | mint reports/uat-*.md with deploy_id + state=READY + HTTP 200 hero route evidence for the sibling-repo touches | sibling-repo row(s) exist but no UAT report under reports/ |
| DIM-10-DEPLOY-EVIDENCE-COMPLETENESS | `docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/files-modified.csv` | gap | medium | mint reports/uat-*.md with deploy_id + state=READY + HTTP 200 hero route evidence for the sibling-repo touches | sibling-repo row(s) exist but no UAT report under reports/ |
| DIM-10-DEPLOY-EVIDENCE-COMPLETENESS | `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/files-modified.csv` | gap | medium | mint reports/uat-*.md with deploy_id + state=READY + HTTP 200 hero route evidence for the sibling-repo touches | sibling-repo row(s) exist but no UAT report under reports/ |
| DIM-10-DEPLOY-EVIDENCE-COMPLETENESS | `docs/wip/planning/73-people-operations-and-learning-curriculum/reports` | gap | low | add deploy_id + state=READY + HTTP 200 hero-route evidence to the UAT report | UAT present but no deploy/state/HTTP-200 evidence tokens found |
| DIM-11-CURSOR-RULE-SKILL-PAIRING | `.cursor/rules/akos-applied-research-discipline.mdc` | gap | low | mint paired skill under .cursor/skills/ OR file forward-charter candidate per D-IH-80-E precedent | rule body mentions craft/skill but no paired SKILL.md or _candidates/ match for token 'appliedresearchdiscipline' |
| DIM-11-CURSOR-RULE-SKILL-PAIRING | `.cursor/rules/akos-brand-baseline-reality.mdc` | gap | low | mint paired skill under .cursor/skills/ OR file forward-charter candidate per D-IH-80-E precedent | rule body mentions craft/skill but no paired SKILL.md or _candidates/ match for token 'brandbaselinereality' |
| DIM-11-CURSOR-RULE-SKILL-PAIRING | `.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc` | gap | low | mint paired skill under .cursor/skills/ OR file forward-charter candidate per D-IH-80-E precedent | rule body mentions craft/skill but no paired SKILL.md or _candidates/ match for token 'conflictsurfacingandblockertrackers' |
| DIM-11-CURSOR-RULE-SKILL-PAIRING | `.cursor/rules/akos-deploy-health.mdc` | gap | low | mint paired skill under .cursor/skills/ OR file forward-charter candidate per D-IH-80-E precedent | rule body mentions craft/skill but no paired SKILL.md or _candidates/ match for token 'deployhealth' |
| DIM-11-CURSOR-RULE-SKILL-PAIRING | `.cursor/rules/akos-docs-config-sync.mdc` | gap | low | mint paired skill under .cursor/skills/ OR file forward-charter candidate per D-IH-80-E precedent | rule body mentions craft/skill but no paired SKILL.md or _candidates/ match for token 'docsconfigsync' |
| DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY | `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` | clean | low |  | last_entry_date=2026-05-24; HEAD_date=2026-05-24; continuity OK |
| DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/` | clean | low |  | roles=70; process_owners=45; orphan_processes=0; ghost_roles=0 |

---

Per `akos-inter-wave-regression.mdc` RULE 3: every non-clean finding
MUST become one `AskQuestion` option set at P4 (inline-ratify gate).
