---
language: en
status: active
initiative: 32-holistik-ops-maturation
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-04-30
---

# Initiative 32 — Asset classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md). Drift handling rule at the bottom.

## Canonical assets (edit here first)

### Planning artifacts

- `docs/wip/planning/32-holistik-ops-maturation/master-roadmap.md`
- `docs/wip/planning/32-holistik-ops-maturation/decision-log.md`
- `docs/wip/planning/32-holistik-ops-maturation/asset-classification.md` (this file)
- `docs/wip/planning/32-holistik-ops-maturation/evidence-matrix.md`
- `docs/wip/planning/32-holistik-ops-maturation/risk-register.md`

### New canonical CSVs (compliance dimensions)

- `docs/references/hlk/compliance/dimensions/SKILL_REGISTRY.csv` (P2; 5 seed rows)
- `docs/references/hlk/compliance/dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv` (P3; 8 seed rows mirroring `_assets/touchpoint-kit/`)
- `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` (P4; seed: every existing RLS rule + I26 quarterly service_role rotation + BRAND_JARGON_AUDIT redaction policy)
- `docs/references/hlk/compliance/REPO_HEALTH_SNAPSHOT.csv` (P8; 3 seed rows for boilerplate + hlk-erp + kirbe)

### New canonical templates

- `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md` (P8; cross-repo discipline seed)
- `.cursor/rules/akos-mirror-template.mdc` (P8; cursor rule template imported by external repos)

### New canonical akos contracts

- `akos/hlk_skill_registry_csv.py` (P2)
- `akos/hlk_touchpoint_kit_cell_csv.py` (P3)
- `akos/hlk_policy_register_csv.py` (P4)
- `akos/hlk_validation_run.py` (P1; operational mirror akos contract)
- `akos/hlk_repo_health_csv.py` (P8)

### New canonical scripts (validators + sync)

- `scripts/validate_skill_registry.py` (P2)
- `scripts/validate_touchpoint_kit_cells.py` (P3; with FS-drift invariant)
- `scripts/validate_policy_register.py` (P4)
- `scripts/validate_repo_health_snapshot.py` (P8)
- `scripts/snapshot_external_repos.py` (P8; pulls from local clones)
- `scripts/render_wip_dashboard.py` (P13)
- `scripts/eval_per_skill.py` (P12)

### Modified canonical (existing files)

- `scripts/validate_hlk.py` (P1; refactored to dispatcher + per-validator graph + `--json`)
- `scripts/sync_hlk_neo4j.py` (P6; extended with 6 new node-label MERGE blocks)
- `akos/hlk_graph_model.py` (P6; new `build_persona_graph`, `build_channel_graph`, `build_sourcing_graph`, `build_skill_graph`, `build_touchpoint_kit_cell_graph`, `build_policy_graph`)
- `akos/hlk_persona_registry_csv.py`, `akos/hlk_channel_touchpoint_registry_csv.py`, `akos/hlk_sourcing_register_csv.py` (P5; gain `topic_ids` field)
- `scripts/sync_compliance_mirrors_from_csv.py` (P2/P3/P4/P8; new `--skill-registry-only`, `--touchpoint-kit-cell-only`, `--policy-register-only`, `--repo-health-snapshot-only` flags)
- `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md` (P5; extended to 6 axes)
- `docs/references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv` (P5; +`topic_ids` column)
- `docs/references/hlk/compliance/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` (P5; +`topic_ids` column)
- `docs/references/hlk/compliance/dimensions/SOURCING_REGISTER.csv` (P5; +`topic_ids` column)
- `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv` (P2/P3/P4/P5; +4 rows: skill, touchpoint-kit-cell, policy, repo-health-snapshot)
- `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` (P11; +1 row for `boilerplate` as `class=reference`)
- `config/sync/kirbe-sync-contract.md` (P9; §2 rewrite to enumerate all 12 mirrors + new §11 cross-repo contract)
- `docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_KIRBE.md` (P9; +§11 language frontmatter discipline +§12 EXTERNAL_REPO_CONTRACT pointer +§13 cross-Neo4j note)
- `docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_HLK_ERP.md` (P10; +§10 EXTERNAL_REPO_CONTRACT pointer +§11 data-ssot rule supersession note)
- `docs/references/hlk/compliance/PRECEDENCE.md` (P1/P2/P3/P4/P8; new mirror rows)
- `docs/references/hlk/compliance/README.md` (P7; deprecation-alias map for GOI/POI move + localisation SOP move)
- `docs/references/hlk/v3.0/index.md` (P7; navigation update for both moved files)
- `docs/ARCHITECTURE.md` (P1/P2/P3/P4/P6/P8; mirror table + Neo4j section + cross-repo extraction section)
- `docs/USER_GUIDE.md` (P6/P12; new §"Neo4j projection — 6-axis Holistik Ops graph" + §"Skill drift canaries")
- `.cursor/rules/akos-docs-config-sync.mdc` (P2/P3/P4/P8; sync triggers for new artifacts)
- `.cursor/rules/akos-holistika-operations.mdc` (P5; topic_skill_registry, topic_touchpoint_kit_cell_registry, topic_policy_register, topic_repo_health_snapshot all registered under plane `ops`)
- `CHANGELOG.md` (P14; comprehensive entry)
- `config/verification-profiles.json` (P13; new `wip_dashboard_render_smoke` profile)

### Moved canonical (file-system relocation)

- `GOI_POI_REGISTER.csv`: from `docs/references/hlk/compliance/` to `docs/references/hlk/compliance/dimensions/` (P7; deprecation alias for one initiative cycle)
- `SOP-HLK_LOCALISATION_001.md`: from `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/` to `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/` (P7; cross-references both ways)

## Mirrored / derived assets

### New Postgres mirrors (DDL ships in I32)

- `compliance.validation_runs` (P1; operational mirror, server-only, RLS deny `anon` and `authenticated`; same pattern as `finops.registered_fact`)
- `compliance.skill_registry_mirror` (P2; canonical CSV → mirror)
- `compliance.touchpoint_kit_cell_mirror` (P3; canonical CSV → mirror)
- `compliance.policy_register_mirror` (P4; canonical CSV → mirror)
- `compliance.repo_health_snapshot_mirror` (P8; operational mirror, server-only)

### Modified Postgres mirrors

- `compliance.persona_registry_mirror`, `compliance.channel_touchpoint_registry_mirror`, `compliance.sourcing_register_mirror` (P5; additive ALTER for `topic_ids` column)
- `compliance.goipoi_register_mirror` (P7; no schema change; only canonical CSV path moves; `sync_compliance_mirrors_from_csv.py --goipoi-register-only` reads new path)

### Mirror reseed bundle (operator-applied)

- `artifacts/sql/i32_skill_touchpoint_policy_topic_repohealth_upsert.sql` (P14; staged for operator)

### Neo4j projection extension (mirrored read index)

- 6 new node labels: `:Persona`, `:Channel`, `:Sourcing`, `:Skill`, `:TouchpointKitCell`, `:Policy` (P6; constraints + range indexes per HLK governance pattern)
- 6+ new edge types: `:ROUTES_FROM_PERSONA`, `:ROUTES_VIA_CHANNEL`, `:VENDOR_AT_DISTANCE`, `:CONSUMES_AXIS`, `:LIVES_IN_CELL`, `:GOVERNED_BY_POLICY`, `:UNDER_TOPIC` (P6; for axis 6 propagation across all dimensions)

### Cross-repo handoff bundles (in I32 reports/)

- `reports/erp-handoff-bundle-2026-MM-DD/` (folder, P10; 7 files: 00-README + 01-mirror-schema-map + 02-five-axis-integration-spec + 03-operator-sql-gate-pointer + 04-localisation-policy-pointer + 05-changelog-snippet + 06-team-sota-pointer)
- `reports/external-repo-seed-prs/` (folder, P8/P9/P10/P11; 9 files: 3 .patch + 6 cover-emails EN+ES per repo)

### WIP dashboard

- `docs/wip/planning/WIP_DASHBOARD.md` (P13; auto-rendered between `<!-- BEGIN AUTO -->` / `<!-- END AUTO -->` markers from each initiative master-roadmap's frontmatter)

## Reference-only assets

- I32 phase reports under `docs/wip/planning/32-holistik-ops-maturation/reports/`
- External repos themselves (`boilerplate`, `hlk-erp`, `kirbe`): tracked via `REPOSITORIES_REGISTRY.md` rows; **github remote is SSOT for their source code**, this repo is SSOT for their HLK doctrine consumption only
- Embedded Obsidian snapshot in boilerplate at `app/dashboard/applications/kms/obsidian-holistika-main/`: explicitly NOT canonical per D-IH-32-N; live Obsidian-anchored vault is `docs/references/hlk/v3.0/` in this repo

## Drift handling rule

If canonical and mirrored assets disagree:

1. **Canonical wins.**
2. Investigate translation or propagation drift (was the sync script extended? did the validator catch it? did an operator hand-edit the mirror?).
3. Resync runtime / mirror from canonical via `scripts/sync_compliance_mirrors_from_csv.py --<artifact>-only`.
4. Document the incident in the I32 phase report and write a `compliance.validation_runs` row with `drift_detected=true` (the new operational mirror from P1 is exactly the surface for this).

For Neo4j drift: re-run `scripts/sync_hlk_neo4j.py` against the configured instance. Constraint violations (uniqueness on `Persona.persona_id` etc.) are surfaced by the script and block the sync.

For external-repo drift: `compliance.repo_health_snapshot_mirror` is the surface. If a snapshot row shows a drop in `language_frontmatter_compliance_pct` or a spike in `brand_jargon_violations` or `has_external_repo_contract=false`, open a follow-up report under the relevant initiative folder.
