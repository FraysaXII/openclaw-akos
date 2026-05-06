---
language: en
report_kind: harmonisation_proposal
phase: P8
status: closed
closed_at: 2026-05-06
initiative: I59 — HLK governance promotion + clean slate cycle
---

# I59 P8 — Process_list harmonisation proposal

> **Per D-IH-59-L / D-IH-59-M:** no `process_list.csv` rows are minted in I59.
> This report is a **proposal** only. Minting happens in I60 with per-tranche
> operator approval (G-60-N gates).

## 1. Current state

`process_list.csv` contains 1,100 rows across all programs. The existing
hierarchy already covers MADEIRA engineering processes (`env_tech_dtp_*`),
operational excellence (`thi_opera_*`), HLK data governance (`thi_data_*`),
marketing (`thi_mkt_*`), finance (`thi_finan_*`), and legal (`thi_legal_*`).

The new `INITIATIVE_REGISTRY.csv` (47 rows from I59 P3) has a nullable
`manifests_processes` FK column ready to receive semicolon-delimited
`process_list.csv` `item_id` references per **D-IH-59-G**.

## 2. Recommended new process_list rows (I60 candidate)

### PMO tranche (6 rows)

| Proposed `item_id` | `item_name` | `parent_id` | `role_owner` |
| --- | --- | --- | --- |
| `thi_pmo_dtp_initiative_governance` | Initiative governance lifecycle | `hlk_prog_think_big_pmo` | PMO |
| `thi_pmo_dtp_cycle_coordination` | Coordinating-cycle planning and closure | `hlk_prog_think_big_pmo` | PMO |
| `thi_pmo_dtp_governance_dimension_authoring` | HLK compliance dimension authoring | `hlk_prog_think_big_pmo` | PMO |
| `thi_pmo_dtp_status_audit` | Initiative status audit and taxonomy apply | `hlk_prog_think_big_pmo` | PMO |
| `thi_pmo_dtp_freshness_canary` | Active initiative freshness canary | `hlk_prog_think_big_pmo` | PMO |
| `thi_pmo_dtp_operator_inbox_triage` | Operator Action Inbox triage | `hlk_prog_think_big_pmo` | PMO |

### Tech tranche (5 rows)

| Proposed `item_id` | `item_name` | `parent_id` | `role_owner` |
| --- | --- | --- | --- |
| `env_tech_dtp_compliance_dimension_seed` | Compliance dimension CSV seed + validator | `env_tech_prj_4` | AI Engineer |
| `env_tech_dtp_supabase_mirror_emit_runbook` | Supabase compliance mirror emit | `env_tech_prj_4` | AI Engineer |
| `env_tech_dtp_release_gate_run` | Release gate full suite | `env_tech_prj_4` | AI Engineer |
| `env_tech_dtp_validate_hlk_run` | HLK canonical vault validation | `env_tech_prj_4` | AI Engineer |
| `env_tech_dtp_browser_smoke_run` | Browser smoke test (Playwright) | `env_tech_prj_4` | AI Engineer |

### Operations tranche (3 rows)

| Proposed `item_id` | `item_name` | `parent_id` | `role_owner` |
| --- | --- | --- | --- |
| `hol_ops_dtp_decision_logging` | Decision logging (D-IH-XX-Y lifecycle) | `hol_ops_pgf_1` | System Owner |
| `hol_ops_dtp_uat_authoring` | UAT / phase closure report authoring | `hol_ops_pgf_1` | System Owner |
| `hol_ops_dtp_evidence_matrix_authoring` | Evidence matrix capture | `hol_ops_pgf_1` | System Owner |

### FinOps tranche (1 row)

| Proposed `item_id` | `item_name` | `parent_id` | `role_owner` |
| --- | --- | --- | --- |
| `thi_finops_dtp_envelope_alarm_run` | Endpoint envelope alarm monitoring | `thi_finan_prj_1` | System Owner |

### Marketing/Brand tranche (0 new rows)

Existing `thi_mkt_*` rows already cover brand authoring. No new rows needed.

### ADVOPS tranche (0 new rows)

Existing adviser engagement processes under `hol_peopl_prj_1` suffice. No new
rows needed.

**Total proposed:** 15 new rows across 4 program areas. Each area becomes one
G-60-N gate at I60 minting time.

## 3. Per-initiative manifests_processes mapping (sample)

| Initiative | Status | Candidate `manifests_processes` |
| --- | --- | --- |
| I59 (governance clean slate) | active | `thi_pmo_dtp_initiative_governance;thi_pmo_dtp_governance_dimension_authoring` |
| I58 (cycle 2 multi-track) | closed | `thi_pmo_dtp_cycle_coordination` |
| I57 (cycle closeout) | closed | `thi_pmo_dtp_cycle_coordination` |
| I08 (Python runtime) | program_line | `env_tech_dtp_release_gate_run;env_tech_dtp_browser_smoke_run` |
| I03 (KM knowledge base) | active | `thi_pmo_dtp_governance_dimension_authoring` |
| I04 (company formation) | program_line | (none — external-process by nature) |
| I55 (brand ops loop) | continuous | `thi_pmo_dtp_operator_inbox_triage` |
| Archived/closed-legacy | closed | (leave NULL — no retroactive enrolment) |

The full per-initiative mapping (47 rows) should be completed by the operator
during I60, row by row, as each tranche is approved. The `manifests_processes`
column is nullable by design (**D-IH-59-F**).

## 4. Folder / role / artifact recommendations

### Folders

Current `docs/wip/planning/<NN>-<slug>/` convention is good — keep it.
`WIP_DASHBOARD.md` / `OPERATOR_INBOX.md` / `README.md` stay at
`docs/wip/planning/` root. No subfolder restructure recommended.

### Roles

No new `baseline_organisation.csv` roles needed. Existing roles (Founder,
System Owner, PMO, Brand Manager, AI Engineer, Marketing Manager, Legal
Counsel) cover all `owner_role` FKs across the new dimensions. If
cross-functional split ownership is needed in the future, add
`engineering_owner_role` / `business_owner_role` columns via ALTER TABLE on
`INITIATIVE_REGISTRY` — non-breaking extension.

### Repo artifacts

The six per-initiative artefacts (master-roadmap.md, decision-log.md,
asset-classification.md, evidence-matrix.md, risk-register.md, reports/) are
codified by `SOP-INITIATIVE_GOVERNANCE_001.md`. No new artifact-types
proposed. The CSV layer is the only structural addition.

### Cross-repo onboarding

When a new Holistika-tracked repo is added:

1. Operator adds a row to `REPOSITORY_REGISTRY.csv`.
2. Operator copies `.cursor/rules/akos-mirror.mdc` to the new repo.
3. Initiatives in that repo append rows to `INITIATIVE_REGISTRY.csv` with the
   new `repo_slug`.

## 5. Upstream/downstream design choice

**Recommendation: upstream only (initiative → process).**

- `INITIATIVE_REGISTRY.manifests_processes` (semicolon-list FK →
  `process_list.csv`) is the upstream link: the initiative declares which
  processes it implements.
- No new column on `process_list.csv` for the downstream link. The downstream
  view is a SQL query against `compliance.initiative_registry_mirror
  .manifests_processes`, not a denormalised column. This avoids sync drift.

## 6. I60 candidate scope handoff

See `docs/wip/planning/_candidates/i60-process-list-harmonisation.md`
(created below as part of P8 closure).

## 7. I61 candidate (optional, low-priority)

Deeper artifact-process mapping — model each artifact-type as a `dtp_*` row.
Currently **not recommended**: keeps process_list lean. Revisit only if a
future cycle surfaces a real need.

## Cross-references

- SOP (draft): `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md`
- Decision: D-IH-59-L (process_list mints deferred to I60)
- Decision: D-IH-59-M (mint authority chain: SOP-META + role_owner + tranche)
- Decision: D-IH-59-G (manifests_processes column on INITIATIVE_REGISTRY)
