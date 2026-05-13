---
language: en
Item Name: External repository blessing
Item Number: SOP-EXTERNAL_REPO_BLESSING_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Envoy Tech Lab
Associated Workstream: Cross-repo governance + DX
Version: 1.0
Revision Date: 2026-05-07
status: active
process_id: SOP-EXTERNAL_REPO_BLESSING_001
role_owner: DevOPS
---

## Purpose

Define the **canonical procedure** for granting a Holistika-tracked external
repository the AKOS governance + CI/CD + observability kit. The procedure
preserves the AKOS Single Source of Truth (HLK doctrine, canonical CSVs,
brand register) while giving every consumer repo a deterministic,
drift-detectable copy of the artefacts that govern its day-to-day work.

This SOP is the human-readable companion to the executable scaffolder
[`scripts/bless_external_repo.py`](../../../../../../../scripts/bless_external_repo.py),
the contract template at
[`Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md`](../../../../Envoy%20Tech%20Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md),
and the mirror rule template at `.cursor/rules/akos-mirror-template.mdc`.

## Preconditions

1. The repo is registered in
   [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv`](../../../../../compliance/REPOSITORY_REGISTRY.csv)
   with `class != reference` (per D-IH-32-N reference repos receive only the
   light-touch contract, not the full bless kit).
2. The operator has a working tree of the consumer repo on the local
   filesystem (path resolvable from the `path` column of
   `REPOSITORY_REGISTRY.csv`, or supplied via `--repo-path`).
3. AKOS itself has the bless artefacts in place under
   `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/`.

## Inputs

- Consumer repo slug (`--repo-slug <slug>`).
- Consumer repo working-tree path (`--repo-path <abs-path>` or registry).
- Optional opt-in feature flags (`--with sentry`, `--with slack`,
  `--with postman`, `--with sbom`, `--with semgrep`, `--with codecov`,
  `--with semantic-release`, `--with browser-smoke`).

## Steps

### 1. Plan + dry-run

```pwsh
py scripts/bless_external_repo.py --repo-slug <slug> --repo-path <abs-path> --dry-run
```

Review the planned actions. The script reports per-artefact:

- `WROTE` / `DRY_WROTE` — would create or update.
- `SKIPPED_UNCHANGED` — already aligned to template.
- `SKIPPED_PRESENT` — file already exists; safe to keep.
- `REFUSED_HAND_EDIT` — file diverged from last bless; rerun with `--force`
  only after operator review.

### 2. Apply

```pwsh
py scripts/bless_external_repo.py --repo-slug <slug> --repo-path <abs-path>
```

The script writes (stack-aware, idempotent):

- `.cursor/rules/akos-mirror.mdc` (verbatim of AKOS template) +
  `.cursor/rules/.akos-mirror.sha256` (drift marker).
- `EXTERNAL_REPO_CONTRACT.md` (rendered with slug + class + owner + vault root).
- `CONTRIBUTING.md` (root, rendered).
- `.github/PULL_REQUEST_TEMPLATE.md`.
- `.gitattributes` (only when missing).
- CI/CD baseline: `.github/workflows/ci.yml`, `dependabot.yml`, `CODEOWNERS`,
  `docs/runbooks/branch-protection.md`.
- Issue templates: `bug.yml`, `feature.yml`, `governance.yml`.
- `LICENSE` (proprietary marker by default).

### 3. Commit + push (consumer-side)

The operator commits the bless artefacts inside the consumer repo with a
governance-tagged Conventional Commit:

```
chore(governance): bless against AKOS template (2026-05-06)

AKOS-decision: D-IH-<NN>-Y     # link if a specific decision motivated the bless
AKOS-initiative: 63-external-repo-governance-codification
```

### 4. Branch protection

Run `py scripts/configure_branch_protection.py --repo-slug <slug>` to ensure
`main` requires reviews ≥ 1, status checks (`lint` / `typecheck` / `audit` /
`unit` / `build`), conversation resolution, no force-push, no deletion.

### 5. Snapshot capture

`py scripts/snapshot_external_repos.py` writes a row into
`REPO_HEALTH_SNAPSHOT.csv` capturing the post-bless state (contract
presence, mirror sha256 match, CI workflow presence, secret rotation oldest
age). Re-run weekly.

## Drift handling (steady state)

- Nightly `py scripts/bless_external_repo.py --repo-slug <slug> --auto-pr`
  detects drift and opens a PR in the consumer when `gh` CLI is available.
- See companion SOP `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md`.

## Reference repos (light touch)

When `class=reference`, only `EXTERNAL_REPO_CONTRACT.md` is light-touch
applied; the full kit is intentionally not pushed (per D-IH-32-N). The
release-gate posture check skips reference repos.

## Verification

```pwsh
py scripts/release-gate.py
py -m pytest tests/test_bless_external_repo.py tests/test_external_repo_automation.py -v
```

## Related

- `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md`
- `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`
- `docs/USER_GUIDE.md` §24.13
- `EXTERNAL_REPO_CONTRACT_TEMPLATE.md`
