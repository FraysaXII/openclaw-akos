# Branch protection — {{REPO_SLUG}}

> **Source of truth**: this file is rendered by `bless_external_repo.py`. Do not hand-edit; instead update the template at `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/ci/branch-protection-runbook.template.md` in AKOS.
>
> **Automation alternative**: `py scripts/configure_branch_protection.py --repo-slug {{REPO_SLUG}}` (Track K4) configures the protection programmatically and idempotently. The runbook below is the manual fallback.

## Required posture

`main` must be protected with:

| Setting | Value |
|:---|:---|
| Required reviewers | ≥ 1 |
| Dismiss stale approvals on push | ✓ |
| Require conversation resolution | ✓ |
| Required status checks (strict) | `lint`, `typecheck`, `audit`, `unit`, `build` (job names from `.github/workflows/ci.yml`) |
| Block force pushes | ✓ |
| Block deletions | ✓ |
| Allow merge commit | ✓ |
| Allow squash merge | ✓ |
| Allow rebase merge | ✗ (linear history is fine but not strict) |
| Restrict who can push to matching branches | Optional; recommended for `main` |

## Manual setup (one-time, when not using the configurator)

1. Open `https://github.com/<owner>/{{REPO_SLUG}}/settings/branches`.
2. Click **Add classic branch protection rule**.
3. Set **Branch name pattern** to `main`.
4. Tick:
    - Require a pull request before merging
    - Require approvals (set to 1)
    - Dismiss stale pull request approvals when new commits are pushed
    - Require conversation resolution before merging
    - Require status checks to pass before merging
    - Require branches to be up to date before merging
5. In the status-checks search, select each job from `.github/workflows/ci.yml`.
6. Tick **Do not allow bypassing the above settings**.
7. Save.

## Verification

```bash
gh api repos/<owner>/{{REPO_SLUG}}/branches/main/protection | jq '
  {
    required_reviews: .required_pull_request_reviews.required_approving_review_count,
    dismiss_stale: .required_pull_request_reviews.dismiss_stale_reviews,
    required_checks: [.required_status_checks.contexts[]],
    conversation_resolution: .required_conversation_resolution.enabled,
    block_force_push: (.allow_force_pushes.enabled == false)
  }'
```

The `release-gate.py` external-repo-CI-posture check (Track F) reads this same API and fails if the required job names are missing or the dismiss-stale flag is off.

## Audit trail

Every change to this runbook should be reflected back into the AKOS template (so future bless runs propagate). Open a PR to `openclaw-akos`.
