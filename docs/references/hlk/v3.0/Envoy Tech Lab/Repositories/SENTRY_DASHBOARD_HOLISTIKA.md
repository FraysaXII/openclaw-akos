---
language: en
status: review
intellectual_kind: operator_runbook
linked_initiative: I68
linked_decisions: D-IH-68-C, D-IH-68-G, D-IH-68-I
last_review: 2026-05-10
owner: System Owner
audience: System Owner, Tech Lead
access_level: 4
related_processes: env_tech_dtp_observability_dashboard_review (lands in I68 P5)
related_canonicals:
  - REPOSITORY_REGISTRY.csv
  - akos-deploy-health.mdc
related_validators:
  - scripts/validate_sentry_release_format.py
---

# SENTRY_DASHBOARD_HOLISTIKA

Operator runbook for the Holistika cross-repo Sentry dashboard. Captures the **canonical dashboard configuration** (markdown-as-config; operator pastes into Sentry UI dashboard editor) plus the **canonical release-format contract** the dashboard depends on.

> **Status note (2026-05-10).** Doc shipped at `status: review` in I68 P4. Promoted to `status: active` in I68 P8 closure once the operator has successfully pasted the dashboard config into the Sentry UI and confirmed all 3 platform repos show non-zero release events within 24h. Do not retire any local repo-level Sentry dashboards until the consolidated one is verified.

---

## 1. Why this doc exists, not a Sentry API automation

Per [D-IH-68-G interim posture](../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/decision-log.md): we **stay vendor-managed** on Sentry until monthly events exceed the free tier or €500/mo cost. That decision implies the dashboard is operator-curated in the Sentry UI, **not** programmatically managed via Sentry's API. Reasons:

1. **Vendor lock-in cost asymmetry.** A 30-line markdown-as-config block is portable across observability vendors (Sentry → Datadog → self-hosted Grafana) for ~30 minutes of operator re-paste work; Sentry-API-managed dashboards lock us into Sentry's REST schema with a multi-day extraction cost when the cost ceiling triggers a vendor migration.
2. **Free-tier API rate limits.** Sentry's dashboard API is rate-limited on free tier in ways that make sync-on-deploy unreliable.
3. **Operator attention is the dominant cost.** A markdown-as-config block the operator can read and amend is materially better than a TypeScript-coded dashboard the operator must deploy to mutate.

When monthly costs cross €500/mo OR Sentry events cross the free-tier ceiling, [D-IH-68-G](../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/decision-log.md) re-opens and the operator chooses between (a) Sentry paid tier + API-managed dashboards, (b) Datadog migration, (c) self-hosted Grafana + Loki + Tempo.

## 2. Canonical release-format contract (D-IH-68-I)

Every Holistika repo that emits Sentry events MUST tag releases with the format:

```
{repo_slug}@{sha_short}
```

where:

- `repo_slug` matches the [`REPOSITORY_REGISTRY.csv`](../../../compliance/REPOSITORY_REGISTRY.csv) `repo_slug` column (lowercase kebab-case `[a-z0-9][a-z0-9-]+[a-z0-9]`).
- `sha_short` is the 7-12 character lowercase hex git short-SHA of the deployed commit.

**Examples (the 3 active platform repos as of 2026-05-10):**

| Repo | Release format | Source of `sha_short` |
|:---|:---|:---|
| [`boilerplate`](https://github.com/FraysaXII/boilerplate) | `boilerplate@74f9a95d` | `process.env.VERCEL_GIT_COMMIT_SHA?.slice(0, 8)` |
| [`hlk-erp`](https://github.com/FraysaXII/hlk-erp) | `hlk-erp@a3b1c92e` | `process.env.VERCEL_GIT_COMMIT_SHA?.slice(0, 8)` |
| [`kirbe-platform`](https://github.com/FraysaXII/kirbe-platform) | `kirbe-platform@5fe2d18b` | `os.environ['RENDER_GIT_COMMIT'][:8]` (Python FastAPI) |

**Why this exact format:**

- Cross-repo Sentry queries become unambiguous: `release:boilerplate@*` returns events for that repo only; `release:*@74f9a95d` returns the 1 deploy with that SHA across the fleet.
- Sentry's vendor-default release format `<package@semver>` is incompatible with rolling-deploy apps that don't have semver versions per build.
- The `@` separator is unambiguous: kebab-case repo_slugs may contain `-`, so `<repo>-<sha>` would be ambiguous.

The `release_template` Pydantic rule enforcing this format lives at [`akos/sentry_release.py`](../../../../../../akos/sentry_release.py) (`SentryReleaseFormatRule`); the validator at [`scripts/validate_sentry_release_format.py`](../../../../../../scripts/validate_sentry_release_format.py) scans each consumer repo's Sentry init code for the `release:` field and FAILs on drift.

## 3. Per-repo Sentry init code (the standard)

### 3.1 Next.js on Vercel (`boilerplate`, `hlk-erp`)

In `sentry.client.config.ts` and `sentry.server.config.ts`:

```ts
import * as Sentry from '@sentry/nextjs';

const REPO_SLUG = '<repo-slug>'; // boilerplate | hlk-erp | future class=platform Next.js repos
const SHA_SHORT = (process.env.VERCEL_GIT_COMMIT_SHA ?? 'unknown').slice(0, 8);

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  release: `${REPO_SLUG}@${SHA_SHORT}`,
  environment: process.env.VERCEL_ENV ?? 'development',
  tracesSampleRate: process.env.VERCEL_ENV === 'production' ? 1.0 : 0.0,
  enabled: process.env.VERCEL_ENV === 'production',
});
```

In `next.config.mjs` `withSentryConfig` options:

```ts
{
  silent: true,
  org: 'holistika',
  project: '<repo-slug>',
  // D-IH-68-C: skip source-map upload on preview builds (transient API errors
  // there should not block the build per akos-deploy-health.mdc Failure 2).
  sourcemaps: {
    disable: process.env.VERCEL_ENV !== 'production',
  },
}
```

### 3.2 Python FastAPI on Render (`kirbe-platform`)

In the FastAPI app init file:

```python
import os
import sentry_sdk

REPO_SLUG = "kirbe-platform"
SHA_SHORT = (os.environ.get("RENDER_GIT_COMMIT") or "unknown")[:8]
RENDER_SERVICE_TYPE = os.environ.get("RENDER_SERVICE_TYPE", "")
RENDER_GIT_BRANCH = os.environ.get("RENDER_GIT_BRANCH", "")

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    release=f"{REPO_SLUG}@{SHA_SHORT}",
    environment=RENDER_SERVICE_TYPE or "development",
    traces_sample_rate=1.0 if RENDER_GIT_BRANCH == "main" else 0.0,
    enabled=(RENDER_SERVICE_TYPE != "preview" and RENDER_GIT_BRANCH == "main"),
)
```

The Render-equivalent of Vercel's `VERCEL_ENV !== 'production'` skip-on-preview is `RENDER_SERVICE_TYPE != "preview"` AND `RENDER_GIT_BRANCH == "main"` (Render uses `RENDER_SERVICE_TYPE` per [Render docs](https://render.com/docs/environment-variables)).

## 4. Canonical dashboard configuration (operator pastes into Sentry UI)

Open Sentry → Dashboards → Create New → name the dashboard **"Holistika deploy-health (cross-repo)"** → switch to YAML editor → paste:

```yaml
# Sentry dashboard: Holistika deploy-health (cross-repo)
# Linked initiative: I68 (CICD discipline + observability maturity)
# Owner: System Owner; Audience: System Owner + Tech Lead
# Last review: 2026-05-10
widgets:
  - title: "Deploy success rate per repo (rolling 7d)"
    type: bar
    interval: 7d
    queries:
      - name: "boilerplate"
        conditions: 'release:boilerplate@* event.type:transaction'
        aggregation: failure_rate
      - name: "hlk-erp"
        conditions: 'release:hlk-erp@* event.type:transaction'
        aggregation: failure_rate
      - name: "kirbe-platform"
        conditions: 'release:kirbe-platform@* event.type:transaction'
        aggregation: failure_rate
  - title: "Deploy success rate per repo (rolling 30d)"
    type: bar
    interval: 30d
    queries:
      - name: "boilerplate"
        conditions: 'release:boilerplate@* event.type:transaction'
        aggregation: failure_rate
      - name: "hlk-erp"
        conditions: 'release:hlk-erp@* event.type:transaction'
        aggregation: failure_rate
      - name: "kirbe-platform"
        conditions: 'release:kirbe-platform@* event.type:transaction'
        aggregation: failure_rate
  - title: "Build-time trend per repo (rolling 30d)"
    type: line
    interval: 30d
    queries:
      - name: "boilerplate"
        conditions: 'release:boilerplate@* transaction.op:build'
        aggregation: p50(measurements.build_duration)
      - name: "hlk-erp"
        conditions: 'release:hlk-erp@* transaction.op:build'
        aggregation: p50(measurements.build_duration)
      - name: "kirbe-platform"
        conditions: 'release:kirbe-platform@* transaction.op:build'
        aggregation: p50(measurements.build_duration)
  - title: "Source-map upload health (rolling 7d)"
    type: number
    interval: 7d
    queries:
      - name: "All repos: artifacts uploaded"
        conditions: 'event.type:artifact_bundle'
        aggregation: count()
      - name: "All repos: artifact upload failures"
        conditions: 'event.type:artifact_bundle status:failed'
        aggregation: count()
  - title: "Release volume sparkline (rolling 30d)"
    type: line
    interval: 30d
    queries:
      - name: "All repos: distinct releases per day"
        conditions: '*'
        aggregation: count_unique(release)
  - title: "Error-rate by release (rolling 7d)"
    type: table
    interval: 7d
    queries:
      - name: "Top 10 releases by event count"
        conditions: 'event.type:error'
        aggregation: count()
        groupBy: [release]
        orderBy: count desc
        limit: 10
```

> **Operator note.** Sentry's dashboard YAML format is paste-and-tweak; Sentry will reject unknown widget types or invalid query syntax with a clear error. After paste, manually verify that all 3 platform repos appear in widget 1 with non-zero release events within 24h of the I68 P4 commits landing.

## 5. What's NOT in this dashboard (deliberate omissions)

- **No per-repo nested dashboards.** Each repo retains its own auto-Sentry dashboard for engineering deep-dives; this consolidated dashboard is for **operator deploy-health attention**, not engineering debugging.
- **No alerting rules.** Alerts are configured per repo via Sentry's alert rules UI; this dashboard is read-only.
- **No PR-level visual regression diffs.** Those live in Argos (per D-IH-68-A); this dashboard is Sentry-only.
- **No build-time alerts.** Build-time targets are encoded in [`REPOSITORY_REGISTRY.csv`](../../../compliance/REPOSITORY_REGISTRY.csv) `build_time_target_seconds` (column lands in I68 P5 PAUSE POINT #3) and surfaced in the InfraMonitor → InfraHealth module (lands in I68 P7) — not in Sentry.

## 6. Migration plan when D-IH-68-G re-opens (cost ceiling crossed)

If/when monthly Sentry events exceed free tier OR €500/mo cost:

1. Operator re-opens [D-IH-68-G in `decision-log.md`](../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/decision-log.md).
2. Three options re-evaluated:
   a. **Sentry paid tier** + this dashboard kept as-is (lowest migration cost; locks vendor for another cycle).
   b. **Datadog migration** + this dashboard re-pasted into Datadog dashboard YAML (medium migration cost; equivalent observability surface).
   c. **Self-hosted Grafana + Loki + Tempo** + this dashboard re-pasted into Grafana JSON (highest migration cost; best long-term cost ceiling; requires self-hosting expertise).
3. Migration prioritises preserving the cross-repo deploy-health view; per-repo engineering deep-dives can stay in Sentry during a phased migration.

## 7. Cross-references

- [I68 master roadmap](../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/master-roadmap.md) §P4 (this doc's parent phase).
- [I68 decision log](../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/decision-log.md) §D-IH-68-C / D-IH-68-G / D-IH-68-I.
- [`.cursor/rules/akos-deploy-health.mdc`](../../../../../../.cursor/rules/akos-deploy-health.mdc) §"Step 1 — Deploy status check" (this dashboard operationalises that step at fleet scale).
- [`scripts/validate_sentry_release_format.py`](../../../../../../scripts/validate_sentry_release_format.py) (validator that enforces the §2 release-format contract).
- [`akos/sentry_release.py`](../../../../../../akos/sentry_release.py) (Pydantic models that are the SSOT for the release-format regex).
