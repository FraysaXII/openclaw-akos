---
language: en
status: applied
initiative: 63-external-repo-governance-codification
report_kind: dry-run-evidence
last_review: 2026-05-07
---

# Dry-run evidence — End-to-end loop validation

**Date:** 2026-05-07
**Scope:** Walk every continuous loop end-to-end against the live
hlk-erp + kirbe checkouts in safe-default mode. No side effects.
Captures actual stdout for the audit trail.

## 1. Bless scaffolder — `scripts/bless_external_repo.py --repo-slug hlk-erp --dry-run`

Outcome: **OK overall** — all 17 blessed files report
`SKIPPED_UNCHANGED` or `SKIPPED_PRESENT`. No drift detected.

```
[INFO] blessing hlk-erp at C:\Users\Shadow\cd_shadow\root_cd\hlk-erp (class=platform, dry_run=True, force=False, auto_pr=False)

  bless: hlk-erp
  ----------------------------------------
  [SKIPPED_UNCHANGED] akos-mirror.mdc
  [SKIPPED_UNCHANGED] EXTERNAL_REPO_CONTRACT.md
  [SKIPPED_UNCHANGED] CONTRIBUTING.md
  [SKIPPED_UNCHANGED] PULL_REQUEST_TEMPLATE.md
  [SKIPPED_PRESENT] .gitattributes
  [SKIPPED_PRESENT] ci.yml
  [SKIPPED_PRESENT] dependabot.yml
  [SKIPPED_PRESENT] CODEOWNERS
  [SKIPPED_PRESENT] branch-protection.md
  [SKIPPED_PRESENT] dependabot-auto-merge.yml
  [SKIPPED_PRESENT] lint-staged.config.json
  [SKIPPED_PRESENT] commitlint.config.cjs
  [SKIPPED_PRESENT] husky-pre-commit
  [SKIPPED_PRESENT] ISSUE_TEMPLATE/{bug,feature,governance}.yml
  [SKIPPED_PRESENT] LICENSE
  [OK] overall
```

Interpretation: hlk-erp is fully blessed and in sync with the AKOS
canonical templates. Re-running the bless command would be a no-op.

## 2. CI/CD posture — `scripts/check_external_repo_ci_posture.py --repo-slug hlk-erp --skip-live`

Outcome: **PASS (6 checks)**.

```
  CI/CD posture
  ----------------------------------------

  hlk-erp (platform)
    [PASS] presence.ci_yml.jobs: required tokens satisfied by jobs=
           ['lint-typecheck', 'unit', 'build', 'audit', 'e2e', 'lighthouse']
    [PASS] presence.dependabot:
    [PASS] presence.codeowners:
    [PASS] license_present:
    [PASS] secret_rotation_freshness: 14 secret(s) tracked; oldest 22d
    [SKIPPED] live_checks: --skip-live

[INFO] CI/CD posture: OK (6 checks)
```

Interpretation: Every static governance check is green. Live checks
(Sentry / Slack live probes) are skipped here because they require
the external secrets walked through in
[`secrets-walkthrough-2026-05-06.md`](secrets-walkthrough-2026-05-06.md).

## 3. Secret rotation reminders — `scripts/secret_rotation_reminders.py --warn-days 30 --fail-days 90`

Outcome: **PASS for hlk-erp**, **WARN for kirbe-platform** (missing
rotation runbook).

```
  # Secret rotation reminders


  ## Approaching (30-90d)

  - kirbe-platform — WARN: docs/runbooks/secrets-rotation.md missing
    (bless writes a template; fill in last_rotated dates)


  ## Healthy

  - hlk-erp — PASS: 14 secret(s) tracked; oldest 22d


  ## Skipped

  - client-delivery-pilot — no resolvable local path
```

Interpretation: hlk-erp's secrets are within rotation window. kirbe
needs the secrets-rotation.md runbook populated with `last_rotated`
dates per secret — bless writes the template; the operator fills in.
Operator action: edit `kirbe/docs/runbooks/secrets-rotation.md` per
the template comments.

## 4. Type regen — `scripts/regen_consumer_types.py --repo-slug hlk-erp --dry-run`

Outcome: **DRY_WROTE** (would write
`hlk-erp/lib/types/akos-mirrors.generated.ts`).

```
[INFO] [dry-run] would update C:\Users\Shadow\cd_shadow\root_cd\hlk-erp\lib\types\akos-mirrors.generated.ts
  [DRY_WROTE] hlk-erp
```

Interpretation: When canonical CSVs change, this loop would regenerate
the TypeScript interfaces consumed by hlk-erp. The dry-run confirms
the file path resolution and template rendering work end-to-end. To
let it commit + open a PR automatically, set `GH_PAT_AUTOPR` per the
secrets walkthrough and add `--auto-pr`.

## 5. Canonical change broadcast — `scripts/notify_consumers_of_canonical_change.py --changed POLICY_REGISTRY --dry-run`

Outcome: **OK** — would post Slack with the consumer list.

```
[INFO] [dry-run] would post Slack:
*AKOS canonical mirror change* — `POLICY_REGISTRY`
• `hlk-erp` consumes: POLICY_REGISTRY
• `kirbe-platform` consumes: POLICY_REGISTRY
```

Interpretation: When a canonical CSV like `POLICY_REGISTRY.csv` is
edited in AKOS, this loop fans out a Slack notification listing every
consumer that imports that mirror. With `SLACK_WEBHOOK_URL` set, this
becomes the real broadcast.

## 6. Unblessed registry rows — `scripts/detect_unblessed_registry_rows.py`

Outcome: **2 BLESSED, 1 UNREACHABLE**.

```
  REPOSITORY_REGISTRY bless status
  ----------------------------------------
  [BLESSED] hlk-erp
  [BLESSED] kirbe-platform
  [UNREACHABLE] client-delivery-pilot  -> add `local_path` column value or pass --repo-path-map
```

Interpretation: `client-delivery-pilot` has no `local_path` set in
`REPOSITORY_REGISTRY.csv` because it's a placeholder for a future
client delivery repo (per its row notes). UNREACHABLE is the correct
state. When the engagement remote is known, edit the registry row to
populate `local_path` and re-run bless.

## 7. External repo contract — `scripts/check_external_repo_contract.py`

Outcome: **OK** — 2 repos validated, 3 skipped (AKOS-internal /
placeholder).

```
[INFO] skipping client-delivery-pilot (no local path or snapshot row; treat as placeholder)
[INFO] external repo contract: OK -- 2 repo(s) validated, 3 skipped (AKOS-internal / placeholder)
```

Interpretation: Both blessed repos pass the contract check (sha256
alignment + EXTERNAL_REPO_CONTRACT.md present + freshness within
`AKOS_EXTERNAL_REPO_FRESHNESS_DAYS`).

## Remediations applied during the dry-run

While exercising the loops, two small mismatches were caught and
fixed:

1. **`scripts/detect_unblessed_registry_rows.py`** — message updated
   from `add 'path' column` to `add 'local_path' column value` to
   match the canonical I63 P4 column rename.
2. **`scripts/bless_external_repo.py`** — verified that the I63
   column changes (semicolon separator for `consumes_mirrors`,
   `local_path` column rename) propagate correctly into RepoMeta.

These fixes were already covered by the earlier I63 P4 work; the
detect-unblessed message string was a documentation-only mismatch,
not a behavioural one.

## Summary

All six loops execute without errors in safe-default mode. No
production secrets were used; no PRs were opened; no Slack messages
were sent. The system is **ready for the operator to flip on the
external secrets** per the
[`secrets-walkthrough-2026-05-06.md`](secrets-walkthrough-2026-05-06.md)
report and run the loops live.

The lone open warning is `kirbe/docs/runbooks/secrets-rotation.md`
needs `last_rotated` dates populated in its bless-rendered template.
That's a one-edit operator action, not a code defect.
