# Postman collection — {{REPO_SLUG}}

> **Source of truth**: this collection (`{{REPO_SLUG}}.postman_collection.json`).
> Maintained via the **Postman MCP** from inside Cursor; do not hand-edit unless a quick fix is needed.

## What this collection covers

The canonical entry-points required by the AKOS CI/CD posture check:

- `GET /api/health` — liveness probe
- `GET /api/ready` — readiness probe (DB / downstream check)
- `GET /api/status` — public status payload

Add additional folders for domain endpoints as the API surface grows. Keep auth
in environment variables, not in the collection.

## Maintenance flow (Postman MCP)

From a Cursor session in this repo:

1. Open the Postman MCP and select the workspace that owns this collection.
2. Pull the latest version: it overwrites `{{REPO_SLUG}}.postman_collection.json`.
3. Commit the change with a `chore(postman): refresh collection` message.
4. Newman re-runs automatically on the next push (`.github/workflows/newman.yml`).

To **add** an endpoint:

1. Add the request in Postman (UI or via the MCP).
2. Pull the collection back into this repo as in the flow above.
3. Update any environment variables in `.github/workflows/newman.yml` if needed.

## Local execution

```bash
npx newman run postman/{{REPO_SLUG}}.postman_collection.json \
  --env-var "baseUrl=http://localhost:3000"
```

## Why a JSON-in-repo source of truth

- CI can run it without a Postman account.
- The diff is reviewable in PRs.
- Drift between staging and production is detectable: Newman runs the same
  collection against multiple base URLs.

## Cross-references

- `EXTERNAL_REPO_CONTRACT.md` — the governance contract for this repo
- AKOS [`USER_GUIDE.md`](https://github.com/FraysaXII/openclaw-akos/blob/main/docs/USER_GUIDE.md) §24.13 — bless flow
- `.github/workflows/newman.yml` — CI runner
