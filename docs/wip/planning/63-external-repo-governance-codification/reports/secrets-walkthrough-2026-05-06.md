---
language: en
status: applied-partial
initiative: 63-external-repo-governance-codification
report_kind: operator-walkthrough
last_review: 2026-05-07
supersedes: none
superseded_by_partial: reports/secrets-mcp-application-2026-05-07.md
---

> **Update 2026-05-07.** A subsequent MCP-side run captured the actual reach of automation in [`secrets-mcp-application-2026-05-07.md`](secrets-mcp-application-2026-05-07.md). Use that report's "Updated operator checklist" — it reduces the work to 4 browser tabs (~10 min). The detail below is preserved for reference.

# GitHub repo secrets walkthrough — 2026-05-07

Operator-facing checklist for setting the GitHub repository secrets that
the External Repo Bless Pattern automation depends on. **Do this once
per secret per repo.** None of these are required to land code; they
unlock the continuous loops (rotation reminders, drift auto-PR, Sentry
release upload, canonical-change Slack pings).

This report assumes the operator has admin access to the FraysaXII org
and the three target repos (`openclaw-akos`, `hlk-erp`, `kirbe`).

## Quick legend

- **Required** = the loop will warn or fail until set.
- **Optional** = enables a nice-to-have feature; absence is benign.
- **Repo-level** = set in `Settings → Secrets and variables → Actions →
  New repository secret` of that specific repo.
- **Org-level** = set once at the FraysaXII org and shared across repos.

## 1. Slack webhook (`SLACK_WEBHOOK_URL`) — **Required for K3 + L9**

**Repo:** `openclaw-akos` (org-level if you want hlk-erp + kirbe to also
post bless events).
**Type:** Repo-level (or org-level — we recommend org-level here).

### Provision

1. Go to `https://api.slack.com/apps` → "Create New App" → "From scratch".
2. Name: `Holistika Bless Bot`. Workspace: your Holistika workspace.
3. Sidebar → "Incoming Webhooks" → toggle ON.
4. "Add New Webhook to Workspace" → choose channel (e.g. `#governance`).
5. Copy the webhook URL (`https://hooks.slack.com/services/T.../B.../...`).

### Set in GitHub

```text
Repo: openclaw-akos
Settings → Secrets and variables → Actions → New repository secret
Name:  SLACK_WEBHOOK_URL
Value: <paste the webhook URL>
```

### Verify

```pwsh
# From AKOS local checkout, after secret is set:
py scripts/secret_rotation_reminders.py --pretend-today 2026-06-01 --slack
# Should post a message to #governance summarizing rotation status.
```

## 2. Sentry — `SENTRY_DSN` per repo + `SENTRY_AUTH_TOKEN` org-level

### Provision Sentry projects

1. https://sentry.io → "Create Project" → Next.js platform → name it
   `hlk-erp` (slug `hlk-erp`).
2. Repeat for `kirbe`.
3. **Sentry → Project → Settings → Client Keys (DSN)** → copy the DSN.
4. Each DSN looks like `https://abc123@o4506...ingest.us.sentry.io/4506...`.

### Set DSN per repo

```text
Repo: hlk-erp
Settings → Secrets and variables → Actions → New repository secret
Name:  NEXT_PUBLIC_SENTRY_DSN
Value: <hlk-erp DSN>
```

```text
Repo: hlk-erp (Vercel project too — same env var name)
Vercel → Project → Settings → Environment Variables
Name:  NEXT_PUBLIC_SENTRY_DSN
Value: <hlk-erp DSN>
Environments: Production, Preview, Development
```

(repeat both for `kirbe`.)

### Set auth token org-level (for source-map upload during release)

1. https://sentry.io → User Settings → Auth Tokens → "Create New Token".
2. Scopes: `project:releases`, `project:read`. Save the token.
3. Add as **org-level** secret in GitHub:

```text
Org: FraysaXII
Settings → Secrets and variables → Actions → New organization secret
Name:        SENTRY_AUTH_TOKEN
Value:       <token>
Repository access: Selected (hlk-erp, kirbe)
```

4. Also add as **org-level** variable (not secret) for `SENTRY_ORG`:

```text
Org: FraysaXII
Settings → Secrets and variables → Actions → Variables → New
Name:  SENTRY_ORG
Value: <your sentry org slug>
```

### Verify

After the next push to hlk-erp `main`, the Sentry release workflow
(in `.github/workflows/`) should upload a sourcemap and create a
release. Check `https://sentry.io → hlk-erp → Releases`.

If the env is missing on a future bless run,
`scripts/check_external_repo_ci_posture.py --auto-fix` opens a tracking
issue in the affected repo titled "Sentry environment configuration
required".

## 3. Vercel token (`VERCEL_TOKEN`) — **Optional, enables L6 hands-off provisioning**

**Repo:** `openclaw-akos` (or local-only if you only run the script
manually).

### Provision

1. https://vercel.com → Account Settings → Tokens → "Create".
2. Scope: full account access (or limit to a team).
3. Copy the token.

### Set

```text
Repo: openclaw-akos
Settings → Secrets and variables → Actions → New repository secret
Name:  VERCEL_TOKEN
Value: <token>
```

### Verify

```pwsh
# Local check — operator-side (token comes from ~/.openclaw/.env):
py scripts/provision_vercel_project.py --slug hlk-erp --dry-run
# Should report what would be provisioned without changing anything.
```

## 4. GitHub auto-PR PAT (`GH_PAT_AUTOPR`) — **Required for K2 drift auto-PR**

**Repo:** `openclaw-akos`.

### Why we need a PAT and not GITHUB_TOKEN

GitHub Actions' built-in `GITHUB_TOKEN` cannot trigger workflows in
*other* repos (the bless `--auto-pr` runs in AKOS but pushes to
hlk-erp / kirbe). We need a fine-grained PAT scoped to consumer repos.

### Provision

**Recommended: fine-grained PAT (scoped, expirable).**

1. https://github.com/settings/personal-access-tokens/new
2. Resource owner: FraysaXII org (you may need org admin to enable
   fine-grained PATs first).
3. Repository access: "Only select repositories" → check `hlk-erp`,
   `kirbe`, `boilerplate`.
4. Permissions:
   - Contents: Read and write
   - Pull requests: Read and write
   - Metadata: Read
5. Expiration: 90 days (rotate per the secret_rotation_reminders loop).
6. Copy the token (starts with `github_pat_...`).

### Set

```text
Repo: openclaw-akos
Settings → Secrets and variables → Actions → New repository secret
Name:  GH_PAT_AUTOPR
Value: <token>
```

### Verify

```pwsh
# Local check (operator runs from AKOS):
py scripts/bless_external_repo.py --repo hlk-erp --dry-run
# If --auto-pr is later added, the script will use $GH_PAT_AUTOPR.
```

## 5. Codecov per repo (`CODECOV_TOKEN`) — **Optional**

Per-repo. Only if you want coverage reports.

1. https://codecov.io → log in with GitHub → enable repo.
2. Copy the upload token.
3. Set in repo: `Settings → Secrets → Actions → CODECOV_TOKEN`.

## Order of operations recommendation

The `secret_rotation_reminders.py` loop already tracks ages but it
assumes secrets *exist*. Start with **(1) Slack** because it's the
notification channel for everything else. Then **(2) Sentry** since
hlk-erp + kirbe are in production. Then **(4) GH_PAT_AUTOPR** to flip
on the drift auto-PR loop. **(3) Vercel** and **(5) Codecov** are
nice-to-have.

## Rotation cadence (locked into the secret_rotation_reminders loop)

| Secret | Rotation cadence | Notification window |
|:---|:---|:---|
| `SLACK_WEBHOOK_URL` | 365 days | warn @ 30d, fail @ 0d |
| `SENTRY_AUTH_TOKEN` | 90 days | warn @ 14d, fail @ 0d |
| `VERCEL_TOKEN` | 365 days | warn @ 30d, fail @ 0d |
| `GH_PAT_AUTOPR` | 90 days | warn @ 14d, fail @ 0d |
| `CODECOV_TOKEN` | never | n/a (Codecov tokens don't expire) |
| `NEXT_PUBLIC_SENTRY_DSN` | never | n/a (DSNs are public-safe) |

The reminder script reads these from `secret_rotation_metadata.json`
in each blessed repo's `.github/.akos-bless/` folder. Update the
"created_at" date there when you rotate; the reminder picks it up.

## Trace

Recorded in [`../decision-log.md`](../decision-log.md) once the operator
confirms each secret is set, as **D-IH-63-G** (or per-secret if
preferred).
