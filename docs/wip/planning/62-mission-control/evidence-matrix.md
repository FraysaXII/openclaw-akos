---
language: en
status: active
initiative: 62-mission-control
report_kind: evidence-matrix
last_review: 2026-05-06
---

> **Superseded hosts (2026-06-13):** Live hosts are **`holistikaresearch.com` only** — see [I96 P-G1](../../96-research-data-plane-and-research-center/reports/subdomains-registry-reconciliation-proposal-2026-06-13.md).

# I62 Evidence Matrix

Findings from the [I32 ERP architecture audit](../32-holistik-ops-maturation/reports/erp-architecture-audit-2026-04-30.md) and operator showcase ask, mapped to specific I62 phase work.

## I32 P8 audit deltas

| ID | Finding | Resolved by | Status |
|:---|:---|:---|:---|
| Δ1 | Adopt language frontmatter on every canonical Markdown | I62 P0 + P11.3 (CONTRIBUTING.md adds the rule) | Pending |
| Δ2 | Adopt `akos-mirror.mdc` cursor rule (Q10 supersession) | Already shipped in `hlk-erp/.cursor/rules/akos-mirror.mdc` (verified 2026-05-06) | Closed |
| Δ3 | Replace `other_documentation/kirbe/` with pointer file | Out of scope for I62 (separate hygiene initiative) | Deferred |
| Δ4 | Replace `other_documentation/hlk/documentation-hlk/` with pointer file | Out of scope for I62 (separate hygiene initiative) | Deferred |
| Δ5 | ERP screens read mirrors via Supabase views, not from `lib/types.ts` | I62 P2.3 (new `erp.*` views) + P2.5 (delete `lib/data.ts`) + P6 (repoint existing routes) | Pending |
| Δ6 | Adopt the 5-axis integration spec (persona filter, distance-band column, channel-tag join) | I62 P5 + P6 (new rooms apply the pattern) | Pending |

## ERP repository state findings (2026-05-06 audit)

| Finding | Evidence | Resolution |
|:---|:---|:---|
| No auth | `components/user-nav.tsx` hard-codes `"Admin" / admin@holistikaresearch.com`; no `middleware.ts` | I62 P1.1 + P1.2 (Supabase Auth, sign-in pages, callback) |
| No RBAC | Sign-in flow doesn't exist; nothing gates routes | I62 P1.3 + P1.4 (`holistika_ops.user_role_mapping`, `policy.ts`, `requireLevel`) |
| Mock data | `lib/data.ts` is 2706 lines of static processes seeded inline | I62 P2.5 (delete after P6 repointing complete) |
| `@supabase/supabase-js` installed but unused | `package.json` line 46 | I62 P2.1 (split clients server/browser/admin) |
| 7 themes declared but no persistence | `app/layout.tsx` line 40 lists 7 themes; no per-user persistence | I62 P7.5 (`user_preferences.theme`) |
| Hardcoded marketing numbers on Project MADEIRA page | `app/tech-lab/project-madeira/page.tsx` lines 65-79 ("99.9% Uptime", "10x Faster", "SOC 2 Compliant") | I62 P6 (replace with honest numbers from `erp.vw_mission_control_today`) |
| 2 trivial smoke tests only | `__tests__/smoke/app-layout.spec.tsx`, `__tests__/guards/providers.spec.ts` | I62 P9.1 (Playwright e2e + axe-core, 70% line coverage budget) |
| No `lint-staged` rules wired | `package.json` line 94 has empty `"lint-staged": {}` | I62 P9.5 (wire ESLint + Prettier + jargon lint into pre-commit) |
| No CI pipeline | No `.github/workflows/` | I62 P9.8 (`.github/workflows/ci.yml`) |
| No security headers | No `next.config.js` headers() | I62 P9.6 (CSP / HSTS / X-Frame / etc.) |
| No error monitoring | No Sentry, no Datadog | I62 P8.2 (`@sentry/nextjs`) |
| No health endpoints | No `/api/health`, no `/api/ready` | I62 P8.3 |
| No status page | No public surface | I62 P8.4 (`/status` route + `status.holistikaresearch.com` rewrite) |

## Operator showcase ask 2026-05-06

| Ask | Resolution |
|:---|:---|
| "I want to show off my erp but the data is fake. If we fill it with real data, we need that logic & decisions to be well designed." | I62 P3 (demo mode) + P2 (real data wiring) + decision register D-IH-62-* covering 18 design decisions |
| "It may be my own team that uses the erp, it may not need to see EVERYTHING." | I62 P1 (RBAC) — D-IH-62-B mapping to AKOS access_level 0-6 |
| "I'd like people to land on an easy subdomain to showcase. I can do any custom subdomain in vercel — so we need governance over those too." | I62 P0 (new canonical `SUBDOMAINS_REGISTRY.md`) + D-IH-62-P (subdomain layout) |
| "I like the use of `holistika_ops`, but what schema will the view tables live in? I think we have an erp schema." | I62 P2.3 (new `erp.*` schema) + D-IH-62-Q (read-side schema discipline) |
| "You've got my Sentry MCP installed, amongst several others. If you need more MCPs let me know." | D-IH-62-R (no new MCP requests; full toolchain inventory in master-roadmap "MCP integration" section) |
| "Plan for everything, not optional, actual best effort everywhere even add topics I didn't think about previously, like per example authentication" | 12 phases covering 30+ topics including auth, audit log, GDPR, DR, perf, a11y, i18n, security headers, demo mode, time-travel, AI assist |

## I59 ride-along closures

I59 closed [`OPS-58-3`](../59-hlk-governance-clean-slate/) with the rubric calibration fix; I62 inherits the now-clean PERSONA_SCENARIO ground truth and uses it in `erp.vw_three_lights_status` for the conversational light. No new evidence row needed; downstream-consumer.

## Cross-repo health snapshot

`compliance.repo_health_snapshot_mirror` 2026-04-30 reports `hlk-erp` at:
- `has_external_repo_contract`: true (✓; verified at planning time).
- `has_akos_mirror_cursor_rule`: true (✓; `.cursor/rules/akos-mirror.mdc`).
- `language_frontmatter_compliance_pct`: 0% (Δ1 deferred).
- `brand_jargon_violation_count`: 23 (most are in `other_documentation/**` snapshots; will reduce as Δ3 + Δ4 land out-of-scope to I62).

Post-I62 expectations:
- `has_mission_control`: true (NEW column; added in P11 to repo_health_snapshot schema as part of `validate_subdomains_registry.py` extension).
- `language_frontmatter_compliance_pct`: ≥ 50% (rises as new I62 routes ship with frontmatter).
- `brand_jargon_violation_count`: ≤ 10 (operator surfaces unrestricted; showcase + marketing CI-gated to 0).
