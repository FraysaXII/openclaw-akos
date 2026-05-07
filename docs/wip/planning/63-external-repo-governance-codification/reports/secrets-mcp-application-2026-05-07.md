---
language: en
status: applied-partial
initiative: 63-external-repo-governance-codification
report_kind: secrets-mcp-application
last_review: 2026-05-07
---

# Secrets walkthrough — MCP application — 2026-05-07

Operator-approved attempt to operate the I63 secrets walkthrough end-to-end via MCPs. This report captures what landed, what was blocked at the auth layer, and a pruned operator checklist for the residual ~10-minute hands-on-keyboard work.

## TL;DR

| Outcome | Steps |
|:---|:---|
| **Works via MCP** | Sentry org/team discovery, Sentry DSN inspection, Slack channel discovery, GitHub repo-secret listing/setting (with current scopes). |
| **Blocked — needs operator UI** | Sentry **project creation** (account is member, not manager), all org-level token creation (Sentry auth token, Vercel token, GH PAT, Slack webhook). |
| **Blocked — needs scope upgrade** | GitHub **org-level** secret set (current token lacks `admin:org`). Either upgrade scope or set repo-level on each repo. |

Net effect: the walkthrough is reduced from "many steps with some automation" to "4 short browser tabs the operator must open, then I push values into GitHub via the gh CLI."

## What was attempted via MCP — full audit

### 1. Sentry MCP (`user-sentry`)

- `whoami` → authenticated as `Fayçal Njoya (fay.njoya@gmail.com)`, Sentry user `3230890`. Confirmed.
- `find_organizations` → org `holistika` (region `https://de.sentry.io`).
- `find_teams --organizationSlug holistika` → 1 team: `holistika` (id `4507325352378448`).
- `find_projects --organizationSlug holistika` → 4 existing projects: `boilerplate`, `boilerplate2`, `javascript-nextjs`, `python-fastapi`. **None match `hlk-erp` or `kirbe`.**
- `create_project --organizationSlug holistika --teamSlug holistika --name hlk-erp --platform javascript-nextjs` → **HTTP 403**: *"Your organization has disabled this feature for members."*
- `create_project --organizationSlug holistika --teamSlug holistika --name kirbe --platform python-fastapi` → **HTTP 403** (same reason).
- `find_dsns --projectSlug javascript-nextjs` → DSN read works (existing project has DSN `https://a701de23ecc8bee83b5b49c6e0104941@o4507325352312832.ingest.de.sentry.io/4507325354278992`); proves the DSN-discovery path works once projects exist.

**Resolution.** Operator must create the two projects in the Sentry UI as an org owner/manager. Steps unchanged from the original walkthrough §2.

### 2. Slack MCP (`plugin-slack-slack`)

- `slack_search_channels --query governance` → no matches.
- `slack_search_channels --query ops` → no matches.
- `slack_search_channels --query alerts` → no matches.
- `slack_search_channels --query holistika` → no matches.
- `slack_search_channels --query general` → 1 channel: `#general-openclaw-akos` (workspace `openclaw-akos.slack.com`).

**Resolution.** No `#governance` channel exists yet. Operator decision — either:

1. Use the existing `#general-openclaw-akos` channel (single-channel workspace), OR
2. Create a `#governance` channel before generating the webhook (cleaner separation; recommended).

Webhook URL itself **cannot** be created via MCP — Slack's Incoming Webhook flow requires the App Directory UI. Operator step preserved.

### 3. Vercel MCP (`user-vercel`)

The MCP exposes `list_projects`, `list_deployments`, `deploy_to_vercel`, etc. — **no `create_project` or `set_env_var` tools**. Token creation also requires UI. No automation path.

### 4. GitHub secret-set via gh CLI

- `gh auth status` → token scopes `gist, read:org, repo`. **Missing `admin:org`** — cannot set org-level secrets.
- `gh secret list --repo FraysaXII/openclaw-akos` → empty.
- `gh secret list --repo FraysaXII/hlk-erp` → empty.
- `gh secret list --repo FraysaXII/kirbe` → empty.

**Resolution.** Two options:

1. **Repo-level only.** Use the current `repo` scope. Each secret is set per-repo (`gh secret set NAME --repo FraysaXII/<repo>`). More secrets to maintain (3× duplication) but no scope upgrade.
2. **Upgrade the local gh token.** Run `gh auth refresh -h github.com -s admin:org,workflow` once; subsequent `gh secret set --org` calls work. Cleaner; recommended.

Recommended: option 2.

## Updated operator checklist (the residual ~10 minutes)

Open these four tabs once. Paste the values back into chat. I'll run the corresponding `gh secret set` commands.

### Tab 1 — Sentry: create the two projects (4 min)

1. Open <https://holistika.sentry.io/projects/>. You need org-owner or manager role.
2. *Create Project* → platform `Next.js` → name `hlk-erp` → team `holistika` → Create.
3. *Create Project* → platform `Python (FastAPI)` → name `kirbe` → team `holistika` → Create.
4. After each: *Settings → Client Keys (DSN)* → copy the DSN.

Paste back: `hlk-erp DSN`, `kirbe DSN`. I run:

```pwsh
gh secret set NEXT_PUBLIC_SENTRY_DSN --repo FraysaXII/hlk-erp --body "<hlk-erp dsn>"
gh secret set SENTRY_DSN --repo FraysaXII/kirbe --body "<kirbe dsn>"
```

### Tab 2 — Sentry: auth token (1 min)

1. Open <https://holistika.sentry.io/settings/account/api/auth-tokens/>.
2. *Create New Token* → scopes `project:releases`, `project:read` → Create.
3. Copy the token (shows once).

Paste back. I run (with `admin:org` scope after `gh auth refresh`):

```pwsh
gh secret set SENTRY_AUTH_TOKEN --org FraysaXII --visibility selected --repos hlk-erp,kirbe,openclaw-akos --body "<token>"
gh variable set SENTRY_ORG --org FraysaXII --visibility all --body "holistika"
```

### Tab 3 — Slack webhook (3 min)

1. Open <https://api.slack.com/apps?new_app=1>. *Create New App → From scratch*.
2. Name: `Holistika Bless Bot`. Workspace: `openclaw-akos`.
3. Sidebar → *Incoming Webhooks* → toggle ON.
4. *Add New Webhook to Workspace* → choose `#general-openclaw-akos` (or `#governance` if you create it first) → Authorize.
5. Copy the webhook URL (`https://hooks.slack.com/services/T.../B.../...`).

Paste back. I run:

```pwsh
gh secret set SLACK_WEBHOOK_URL --org FraysaXII --visibility selected --repos hlk-erp,kirbe,openclaw-akos --body "<webhook>"
```

### Tab 4 — GitHub fine-grained PAT (3 min)

1. Open <https://github.com/settings/personal-access-tokens/new>.
2. Resource owner: `FraysaXII` org (you may need to enable fine-grained PATs at org level first).
3. Repository access: *Only select repositories* → `hlk-erp`, `kirbe`, `boilerplate`.
4. Permissions:
   - Contents: Read and write
   - Pull requests: Read and write
   - Metadata: Read (auto-enabled)
5. Expiration: 90 days.
6. Copy the token (`github_pat_...`).

Paste back. I run:

```pwsh
gh secret set GH_PAT_AUTOPR --repo FraysaXII/openclaw-akos --body "<token>"
```

### Optional — Vercel token + Codecov

These are deferred until the L6 hands-off provisioning loop (`scripts/provision_vercel_project.py`) is run for real. Today's Vercel deploys still use the user-bound deploy hooks; nothing breaks without a token.

If you want to set them now anyway:

- Vercel token: <https://vercel.com/account/settings/tokens> → Create → paste back → `gh secret set VERCEL_TOKEN --repo FraysaXII/openclaw-akos --body "<token>"`.
- Codecov per-repo: <https://codecov.io> → enable repo → copy upload token → `gh secret set CODECOV_TOKEN --repo FraysaXII/<repo> --body "<token>"`.

## Rotation log seeded

When the operator pastes a value back, it will be set with `last_rotated = 2026-05-07`. The corresponding [`secrets-rotation.md`](../../../../../kirbe/docs/runbooks/secrets-rotation.md) runbooks (kirbe + hlk-erp) and [`.github/.akos-bless/secret_rotation_metadata.json`](../../../../../kirbe/.github/.akos-bless/secret_rotation_metadata.json) files seeded in Phase 4 of this session reflect that.

## Trace

- Operator approval: user response on 2026-05-07.
- MCP servers used: `user-sentry`, `plugin-slack-slack`, `user-supabase` (for Phase 2), and `gh` CLI (shell).
- See updated frontmatter on [`secrets-walkthrough-2026-05-06.md`](secrets-walkthrough-2026-05-06.md): `status: applied-partial` with footer pointer to this report.

## Decision

Logged as **D-IH-63-G** in [`../decision-log.md`](../decision-log.md): "MCP-side automation is bounded by Sentry member-tier permissions and the absence of a Slack webhook MCP. Net result: 4 hands-on browser steps, 4 `gh secret set` invocations after."
