---
language: en
Item Name: Cross-repo canonical schema propagation
Item Number: SOP-CROSS_REPO_SCHEMA_PROPAGATION_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Envoy Tech Lab
Associated Workstream: Cross-repo governance + DX
Version: 1.0
Revision Date: 2026-05-07
status: active
process_id: SOP-CROSS_REPO_SCHEMA_PROPAGATION_001
role_owner: System Owner
---

## Purpose

When an AKOS canonical CSV (PERSONA, CHANNEL, SOURCING, SKILL, POLICY,
PROGRAM, TOPIC, GOI/POI, FOUNDER_FILED_INSTRUMENTS, FINOPS_COUNTERPARTY,
COMPONENT_SERVICE_MATRIX, baseline_organisation, process_list, …) gains a
new column, this SOP defines the propagation flow that keeps every
consumer repo (e.g. `hlk-erp`, future `kirbe-platform`) statically typed
against AKOS without invented IDs and without manual hand-editing.

## Scope

The flow applies to repos in
[`REPOSITORY_REGISTRY.csv`](../../../../../compliance/REPOSITORY_REGISTRY.csv)
where `consumes_compliance_types=yes`. The repo's `consumes_mirrors`
column lists which canonical CSVs that repo statically types against (the
`.csv` filename minus the suffix; e.g.
`PERSONA_REGISTRY,SKILL_REGISTRY`).

These columns are introduced by Initiative
[I63](../../../../../../wip/planning/63-external-repo-governance-codification/master-roadmap.md)
P3 / P4 (operator-gated) — `bless_external_repo.py` and
`regen_consumer_types.py` already read them defensively (default
`consumes_compliance_types=False`, empty `consumes_mirrors`), so this SOP
is forward-compatible during the I63 charter ship.

## Triggers

- A push to `main` of `openclaw-akos` that modifies any file under
  `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/*.csv`.
- Equivalently: an operator-applied DML migration that mints rows in a
  `compliance.*_mirror` table (when the schema deltas surface in CSV form).

## Steps — automated path

### 1. AKOS-side regeneration

```pwsh
py scripts/regen_consumer_types.py
```

For every consuming repo with a resolvable local path:

- Reads `consumes_mirrors` from `REPOSITORY_REGISTRY.csv`.
- Emits TypeScript interfaces from each consumed CSV's headers into
  `<repo>/lib/types/akos-mirrors.generated.ts`.
- Detects drift via sha256; writes only when content differs.

When run with `--auto-pr` and `gh` CLI is available, the script opens a
`chore(types): regenerate AKOS mirror types` PR in the consumer.

### 2. Notify consumers

```pwsh
py scripts/notify_consumers_of_canonical_change.py --changed PERSONA_REGISTRY,SKILL_REGISTRY --open-issue
```

For every consumer whose `consumes_mirrors` intersects the changed CSVs:

- Posts a Slack notification (when `SLACK_OPS_WEBHOOK` is set).
- Opens an issue in the consumer (when `--open-issue` and `gh` CLI
  available); idempotent on title.

### 3. Consumer-side merge

The consumer reviews the regenerated `akos-mirrors.generated.ts`, runs its
local lint/type/test suite, and merges. The interface is `string | null`
across the board — strict enough to surface unknown columns, loose enough
to never break a CI run on column reorder.

## Steps — manual path

When `gh` CLI is not available or the consumer has chosen to handle
notifications manually, the operator:

1. Opens a `governance.yml` issue in the consumer (referencing the AKOS
   PR that minted the change).
2. Pulls AKOS, runs `regen_consumer_types.py --repo-slug <slug>` against
   AKOS, copies the regenerated types into the consumer, opens a normal PR.

## Type-safety contract

- All emitted interfaces use `string | null` for every column. Consumers
  refine specific columns in their own `.d.ts` files when they need
  literal types or enums.
- The interface name is `AkosMirror_<MIRROR_NAME>` (e.g.
  `AkosMirror_PERSONA_REGISTRY`).
- The `// AUTO-GENERATED` header at the top of
  `akos-mirrors.generated.ts` carries the regen command for traceability.

## Drift detection

The nightly snapshot run captures `akos_mirror_sha256_match` per consumer
in `REPO_HEALTH_SNAPSHOT.csv`. Mismatch is a posture-check FAIL.

The consumer's CI also fails when its own typecheck breaks against the
regenerated types — surfaced through the standard lint/typecheck job in
the bless-rendered `.github/workflows/ci.yml`.

## Verification

```pwsh
py scripts/regen_consumer_types.py --dry-run
py -m pytest tests/test_external_repo_automation.py -v
```

## Related

- `SOP-EXTERNAL_REPO_BLESSING_001.md`
- `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md`
- I63 charter:
  `docs/wip/planning/63-external-repo-governance-codification/master-roadmap.md`
- I63 CSV proposal:
  `docs/wip/planning/63-external-repo-governance-codification/reports/csv-proposal-2026-05-06.md`
