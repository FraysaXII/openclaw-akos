---
language: en
status: applied
initiative: 63-external-repo-governance-codification
report_kind: csv-proposal
last_review: 2026-05-06
---

# CSV proposal — 2026-05-06 (REVISED 2026-05-07, applied)

> **Status: APPLIED 2026-05-07.** This report has been superseded by the
> canonical edits it proposed. It remains as the audit artefact gating the
> change. See `../decision-log.md` (D-IH-63-D, D-IH-63-E) for the operator
> approval trace.

## 0. Revision history

| Date | Revision | Author |
|:---|:---|:---|
| 2026-05-06 | v1 — initial proposal (had wrong schema for `process_list.csv`) | I63 P3 |
| 2026-05-07 | v2 — schema corrected, DevOPS/System Owner split, item_id harmonised to SOP-* | I63 P4 |

## 1. `REPOSITORY_REGISTRY.csv` — three new columns

### Proposed schema delta

Existing header (canonical):

```
repo_slug,github_url,class,primary_owner_role,topic_ids,vault_doc_root,api_spec_pointer,api_topic_id,lifecycle_status,notes
```

Append three columns at the end:

| Column | Type | Vocabulary | Default | Purpose |
|:---|:---|:---|:---|:---|
| `consumes_compliance_types` | string | `yes` / `no` | `no` | Marks repos that import generated TypeScript types from AKOS canonical CSVs (drives `regen_consumer_types.py`). |
| `consumes_mirrors` | string (semicolon-separated) | mirror names without `.csv` (e.g. `PERSONA_REGISTRY;SKILL_REGISTRY`) | _empty_ | Lists which canonical mirrors the repo consumes (drives `notify_consumers_of_canonical_change.py`). Semicolons (not commas) so the CSV doesn't fight with the field separator. |
| `local_path` | string | repo-relative path from `${REPO_ROOT}/..` | _empty_ | Local working-tree path so AKOS scripts can resolve the consumer without `--repo-path` overrides every time. |

### Row updates (existing slugs)

| repo_slug | consumes_compliance_types | consumes_mirrors | local_path |
|:---|:---|:---|:---|
| `kirbe-platform` | `yes` | `SOURCING_REGISTRY;POLICY_REGISTRY` | `root_cd/kirbe` |
| `openclaw-akos` | `no` | _empty_ | `cd_shadow/openclaw-akos` |
| `akos-telemetry-ci` | `no` | _empty_ | _empty_ |
| `hlk-erp` | `yes` | `PERSONA_REGISTRY;CHANNEL_REGISTRY;SOURCING_REGISTRY;SKILL_REGISTRY;POLICY_REGISTRY;PROGRAM_REGISTRY;TOPIC_REGISTRY;FOUNDER_FILED_INSTRUMENTS;FINOPS_COUNTERPARTY;COMPONENT_SERVICE_MATRIX;baseline_organisation;process_list;DECISION_REGISTER;OPS_REGISTER;INITIATIVE_REGISTRY;CYCLE_REGISTER` | `root_cd/hlk-erp` |
| `boilerplate` | `no` | _empty_ | `root_cd/boilerplate` |
| `client-delivery-pilot` | `no` | _empty_ | _empty_ |

### Backwards-compatibility statement

The bless scaffolder (`scripts/bless_external_repo.py`) already reads these
columns defensively: missing columns yield `consumes_compliance_types=False`,
`consumes_mirrors=()`, `local_path=""`. Header extension + row annotation is
**purely additive**.

> **Naming note.** v1 of this report used `path`; revised to `local_path` to
> avoid collision with Python's `pathlib.Path` import shadowing patterns in
> consumer scripts and to make the column self-describing.

## 2. `process_list.csv` — three new rows (HARMONISED)

### Schema reality (v1 had this wrong)

Real `process_list.csv` header (21 columns):

```
type, orientation, entity, area, role_parent_1, role_owner,
item_parent_2, item_parent_2_id, item_parent_1, item_parent_1_id,
item_name, item_id, item_granularity, time_hours_par,
description, instructions, addundum_extras, confidence,
count_name, frequency, quality
```

There is **no `plane`, no `sop_id`, no `trigger`, no `artefact`** column.
v1's proposal used a fictional shape; v2 below uses the real schema.

### Naming harmonisation

| Field | v2 value | Why |
|:---|:---|:---|
| `entity` | `HLK Tech Lab` | Matches existing tech SOP rows (lines 316-320 of `process_list.csv`); `Envoy Tech Lab` is a brand label (Area Owner in SOP frontmatter), not a canonical entity. |
| `area` | `Tech` | Existing convention. |
| `role_parent_1` | `CTO` | Canonical: DevOPS and System Owner both report to CTO (`baseline_organisation.csv` lines 51-53). |
| `role_owner` | **split: `DevOPS` for blessing+drift, `System Owner` for schema-propagation** | Operator decision D-IH-63-E. DevOPS owns CI/CD + drift loops per its baseline description; System Owner owns infra + data governance, aligning with cross-repo schema propagation. |
| `item_parent_2` / `item_parent_1` | `HLK Infrastructure and DevOPS` / id `env_tech_prj_4` | Existing parent grouping for tech ops processes. This is where the "DevOps" concept lives in the canonical schema — there is no separate `plane` column. |
| `item_id` | `SOP-<NAME>_001` | Harmonised to canonical SOP-class convention: `item_id` IS the SOP filename (matches `SOP-MCP_SERVER_DEFINITION`, `SOP-ENVOYLAB_REFACTOR_ARCHITECTURE_001`, etc.). Drops the v1 `PROC-` prefix. |
| `addundum_extras` | `SOP` | Marks SOP-class rows. |
| `confidence` / `count_name` / `quality` | `2 / 1 / 3` | Matches existing tech SOP rows. |

### Final v2 rows

```csv
Internal,Employee,HLK Tech Lab,Tech,CTO,DevOPS,HLK Infrastructure and DevOPS,env_tech_prj_4,HLK Infrastructure and DevOPS,env_tech_prj_4,External repo blessing,SOP-EXTERNAL_REPO_BLESSING_001,process,,Apply standard governance + CI/CD + observability artefacts to a Holistika-tracked external repo using scripts/bless_external_repo.py.,,SOP,2,1,medium,3
Internal,Employee,HLK Tech Lab,Tech,CTO,DevOPS,HLK Infrastructure and DevOPS,env_tech_prj_4,HLK Infrastructure and DevOPS,env_tech_prj_4,External repo drift remediation,SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001,process,,Detect and auto-remediate drift between AKOS canonical templates and the consumer copies via the auto-PR loop (release-gate + scripts/bless_external_repo.py --auto-pr).,,SOP,2,1,high,3
Internal,Employee,HLK Tech Lab,Tech,CTO,System Owner,HLK Infrastructure and DevOPS,env_tech_prj_4,HLK Infrastructure and DevOPS,env_tech_prj_4,Cross-repo schema propagation,SOP-CROSS_REPO_SCHEMA_PROPAGATION_001,process,,Notify consumers of AKOS canonical CSV changes and regenerate downstream TypeScript types via scripts/notify_consumers_of_canonical_change.py + scripts/regen_consumer_types.py.,,SOP,2,1,medium,3
```

### Resolved questions (from v1 §"Open questions for the operator")

1. **`role_owner`** — RESOLVED: split. DevOPS owns blessing + drift; System Owner owns schema-propagation. (D-IH-63-E)
2. **`item_id` shape** — RESOLVED: `SOP-<NAME>_001` matching canonical SOP-class convention.
3. **`area` / `plane`** — RESOLVED: `area=Tech`; the "DevOps" concept lives at `item_parent_2 = HLK Infrastructure and DevOPS`. There is no `plane` column in canonical `process_list.csv`.
4. **`baseline_organisation.csv`** — CONFIRMED: no companion edit needed. `DevOPS` (org_039) and `System Owner` (org_038) already exist.

## 3. SOP cross-link expectations

After the rows are minted, the three SOPs at `status: review` flip to
`status: active` and bump `Version: 0.1` → `Version: 1.0`. The
`.cursor/rules/akos-mirror-template.mdc` already references the SOPs (Track O);
no rule edit is needed beyond confirming the references resolve.

## 4. Validation hooks (run after applying)

```pwsh
py scripts/validate_hlk.py
py scripts/validate_hlk_km_manifests.py
py scripts/validate_initiative_registry.py
py scripts/release-gate.py
py -m pytest tests/test_governance_moat_metrics.py -v
```

The bless scaffolder + posture checks already pass on the current
`REPOSITORY_REGISTRY.csv` shape; the schema delta is purely additive.

## 5. Decision

- **D-IH-63-D** (CSV approval) — operator approved 2026-05-06 with the
  harmonisation feedback that drove this v2.
- **D-IH-63-E** (role_owner split) — operator selected DevOPS for
  blessing+drift, System Owner for schema-propagation.

Both recorded in [`../decision-log.md`](../decision-log.md).
