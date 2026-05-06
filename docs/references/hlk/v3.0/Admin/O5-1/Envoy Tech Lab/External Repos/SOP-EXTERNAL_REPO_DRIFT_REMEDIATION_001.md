---
language: en
Item Name: External repository drift remediation
Item Number: SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Envoy Tech Lab
Associated Workstream: Cross-repo governance + DX
Version: 1.0
Revision Date: 2026-05-07
status: active
process_id: SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001
role_owner: DevOPS
---

## Purpose

Define how AKOS detects and remediates drift between the canonical AKOS
templates (under
`docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/`) and the
copies that live in blessed external repositories. Drift means a sha256
mismatch between the template and the consumer copy of bless-managed
artefacts.

## Scope

Bless-managed artefacts that produce drift signals:

- `.cursor/rules/akos-mirror.mdc` (verbatim copy; sha-stamped at
  `.cursor/rules/.akos-mirror.sha256`).
- `EXTERNAL_REPO_CONTRACT.md` (rendered from template; sha-stamped at
  `.github/.akos-bless/external_repo_contract.sha256`).
- `CONTRIBUTING.md`, `PULL_REQUEST_TEMPLATE.md`, CI/CD workflow files,
  issue templates, license.

## Detection

Two channels:

1. **Filesystem-level (offline)** — `scripts/check_external_repo_contract.py`
   compares sha256 of the AKOS template against the consumer's local copy
   when the consumer is reachable on disk. Wired into `release-gate.py`.

2. **Snapshot-level (weekly)** — `scripts/snapshot_external_repos.py` writes
   a row into `REPO_HEALTH_SNAPSHOT.csv` with `akos_mirror_sha256_match` set
   to `true`/`false`/`unknown`. The release-gate fails when contract
   presence is missing, sha256 mismatches, or contract review is older than
   90 days (`AKOS_EXTERNAL_REPO_FRESHNESS_DAYS` env var).

## Remediation paths

### Path A — operator-driven (preferred for ad-hoc drift)

```pwsh
py scripts/bless_external_repo.py --repo-slug <slug> --repo-path <abs-path>
```

The scaffolder REFUSES to overwrite hand-edited files unless `--force` is
passed; the operator first reviews the diff (`git diff` inside the
consumer), then either:

- Forces the realignment when the hand edit was unintentional, or
- Opens an AKOS PR to update the template when the consumer's edit is the
  better default.

### Path B — automated (preferred at steady state)

Nightly cron / GitHub Actions schedule on AKOS:

```pwsh
py scripts/bless_external_repo.py --repo-slug <slug> --auto-pr
```

The scaffolder detects sha256 drift on the mirror rule and opens a PR in
the consumer via `gh pr create`. The PR title is canonical
(`chore(governance): realign .cursor/rules/akos-mirror.mdc to AKOS template`),
so the script can detect already-open PRs and skip duplicate creation.

When `gh` CLI is unavailable the script logs `SKIPPED_NO_GH` and the
operator handles it via Path A.

## Hand-edit policy

A hand-edited bless-managed file is an **incident**, not a feature:

1. The operator opens a `governance.yml` issue in the consumer repo
   describing the rationale for the local edit.
2. If the rationale is sound, an AKOS PR updates the canonical template;
   the consumer realigns on the next nightly run.
3. If the rationale is local-only and intentional, the operator marks the
   file with `# AKOS-bless-exempt: <D-IH-XX-Y>` (top-of-file comment) and
   the bless scaffolder respects that flag on subsequent runs (future
   enhancement; today the operator runs `--force` after the AKOS PR lands).

## Reference repos

`class=reference` repos are skipped entirely by the bless flow per D-IH-32-N.
Drift detection does not apply to them.

## Verification

```pwsh
py scripts/check_external_repo_contract.py --freshness-days 90
py scripts/release-gate.py
```

## Related

- `SOP-EXTERNAL_REPO_BLESSING_001.md`
- `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`
- `docs/USER_GUIDE.md` §24.13
