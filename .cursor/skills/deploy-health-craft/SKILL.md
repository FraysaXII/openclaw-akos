---
name: deploy-health-craft
description: Use when verifying that a consumer repo tracked in REPOSITORY_REGISTRY.csv deploys + renders correctly after meaningful changes. Codifies the craft for the 4-step CICD smoke checklist (deploy status check + build log inspection on failure + multi-viewport visual smoke + build-time optimisation) + the Failure-N catalogue + new-failure-addition rhythm. Triggers on deploy health, CICD smoke, Vercel deploy, Render deploy, build log inspection, multi-viewport smoke, build-time optimisation, Failure-N catalogue, deploy regression, hosting platform MCP. Pairs with .cursor/rules/akos-deploy-health.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT
authored: 2026-05-24
---

# Deploy-Health Craft

> Codified at I86 Wave R close (drain7) to operationalise the I66 P5 + I68 P5/P7 precedent. The craft turns deploy verification from manual visual hunt into structured 4-step checklist + a growing Failure-N catalogue. Ratified by D-IH-86-CT.

## When to use this skill

Read this skill at the start of any operator turn that touches a consumer repo tracked in [`REPOSITORY_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/REPOSITORY_REGISTRY.csv), before authoring a sibling-repo PR, and before closing any wave that includes sibling-repo work.

This skill assumes you have already read [`akos-deploy-health.mdc`](../../../.cursor/rules/akos-deploy-health.mdc).

## Core principles

### Principle 1 — Always check deploy status FIRST

Before any other turn-work on a consumer repo, poll the hosting platform's MCP for the last 5 deployments. Three or more consecutive terminal-error states usually means a code regression that's blocking everyone, not a transient infra issue. Don't author new commits on top of broken deploys without acknowledging the breakage.

Platform → tool mapping:

- **Vercel**: `list_deployments(teamId, projectId, limit=5)`.
- **Render**: `list_deploys(serviceId, limit=5)`.
- **Other** (GitHub Pages, Cloudflare, AWS): document polling tool when added.

### Principle 2 — Build log inspection on failure

If the most recent deploy is terminal-error, fetch + parse the build log:

- **Vercel**: `get_deployment_build_logs(teamId, idOrUrl, limit=400)`.
- **Render**: `list_logs(serviceId, deployId, limit=400)`.

Look in the **last ~30 events** for the actual error trail. First events are typically clone + dep-install warnings (noise). See §"Failure-N catalogue" for known patterns.

### Principle 3 — Multi-viewport visual smoke (after successful deploy)

Run the browser-use subagent against 5 standard viewports:

- 375 × 667 (iPhone SE) — narrowest mobile.
- 414 × 896 (iPhone 11/12/13/14/15) — wider mobile.
- 768 × 1024 (iPad portrait) — tablet.
- 1280 × 800 (desktop default) — most-common laptop.
- 1920 × 1080 (wide desktop) — large monitor.

Subagent prompt should explicitly enumerate:

1. Pages or routes to load + key elements to verify.
2. Locale switching where applicable.
3. Console errors / 404s.
4. Mobile-specific overflow / overlap / illegibility checks.
5. Auth state (preview deployments may need session credentials).

Report format: HIGH / MEDIUM / LOW severity with actionable remediation per finding.

### Principle 4 — Build-time optimisation gates

Operator's stated target: < 2 min per preview build for typical frontend repos. If exceeded, profile the build log timestamps + apply targeted optimisations:

- **Observability source-map upload**: non-blocking + skip on previews; production only.
- **Stale build cache**: ensure cache restored across deploys ("fresh dependency install" line = cache miss).
- **Static prerender of dynamic routes**: lazy-init singleton pattern (Failure 3 fix).
- **Framework-level**: Turbopack opt-in (Next.js 14+); Vite for SPAs; SWC over Babel.

### Principle 5 — Failure-N catalogue is craft-shaped; add new patterns

The Failure-N catalogue in the parent rule grows with each incident. When a new failure mode is encountered:

1. Reproduce it in the build log.
2. Add a new `### Failure N — <one-line title>` section to the parent rule body.
3. Each entry specifies: symptom + root cause + canonical fix + framework-applicability.
4. Reference any reusable template files by path, not by full content.
5. Update the relevant initiative's ChangeLog entry with a back-reference.

Speculative failure entries (e.g., "Failure 6 awaits P3 confirmation") are allowed; promote to "confirmed" on first observation in real CI.

## Failure-N catalogue summary (per parent rule body)

| # | Title | Framework | Severity |
|:--|:---|:---|:---|
| 1 | Duplicate `declare global { interface Window }` | TypeScript | HIGH |
| 2 | Observability SDK CLI fails build on transient API error | Any with source-map upload | MEDIUM |
| 3 | Static prerender fails on data-source-dependent route | Next.js / Remix / SvelteKit | HIGH |
| 4 | Mobile navbar overflow / no hamburger | Web frontends | MEDIUM |
| 5 | Sticky secondary header overlapping primary navbar | Web frontends | MEDIUM |
| 6 (speculative) | Visual-regression false positive on font subpixel | Playwright VR | LOW |
| 7 (speculative) | Render auto-deploy timeout on cold-start | Render workers | MEDIUM |

Full per-failure detail lives in the parent rule body §"Common build failures + canonical fixes".

## Pre-flight checklist (every consumer-repo turn)

1. Polled hosting platform MCP for last 5 deploys.
2. No 3+ consecutive terminal-error states (or, if yes, acknowledged the blocker).
3. If most-recent failed: build log fetched + last ~30 events inspected against Failure-N catalogue.
4. After successful deploy: multi-viewport visual smoke triggered (via browser-use).
5. Build-time profiled if > 2 min.
6. Findings filed at HIGH / MEDIUM / LOW with actionable remediation.
7. New failure modes added to parent rule + ChangeLog cross-referenced.

## Anti-patterns

- **AP1 — Skip the deploy status check.** Authoring on top of broken deploys; rework + operator confusion.
- **AP2 — Read whole build log linearly.** Wastes time; the error is in the last 30 events.
- **AP3 — Single-viewport smoke.** Mobile overflow + sticky overlap go unnoticed; ship-blocking issues post-deploy.
- **AP4 — Accept > 2 min build as normal.** Sets bad baseline; future builds degrade further.
- **AP5 — Don't catalogue new failures.** Same pattern hits another agent later; rediscovery cost.

## Cross-references

- Parent rule: [`akos-deploy-health.mdc`](../../../.cursor/rules/akos-deploy-health.mdc).
- Repo registry: [`REPOSITORY_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/REPOSITORY_REGISTRY.csv).
- Sister rule: [`akos-techops-discipline.mdc`](../../../.cursor/rules/akos-techops-discipline.mdc) (TECHOPS mechanical layer).
- Worked example: I68 P7 InfraMonitor module v0 + I66 P5 build-fix incident.
- Ratifying decision: D-IH-86-CT (this skill mint).
