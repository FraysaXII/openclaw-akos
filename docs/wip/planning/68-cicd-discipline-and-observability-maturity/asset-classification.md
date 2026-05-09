---
linked_initiative: I68
last_review: 2026-05-09
governed_by: docs/references/hlk/compliance/PRECEDENCE.md
---

# I68 Asset Classification

Per `PRECEDENCE.md`, every asset I68 will touch is classified canonical / mirrored / reference. Edits flow canonical-first; mirrored derivations resync; reference-only docs are read.

## Canonical (edit here first)

| Asset | Why canonical |
|:---|:---|
| [`.cursor/rules/akos-deploy-health.mdc`](../../../../.cursor/rules/akos-deploy-health.mdc) | Discipline-layer canonical; I68 extends with new failure patterns + tooling references discovered in P1+. |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORY_REGISTRY.csv` | Source of truth for consumer-repo + hosting-platform mapping. P5 extends with `build_time_target_seconds` + `ci_baseline_version` columns. |
| `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-CICD_BASELINE_001.md` (NEW, P5) | Per-consumer-repo baseline CI workflow definition + the version that's currently active. |
| `docs/references/hlk/compliance/process_list.csv` | New rows for ongoing CICD-discipline + observability-monitoring + visual-regression-triage processes (P5/P6/P8). |

## Mirrored / derived

| Asset | Where it derives from |
|:---|:---|
| Per-consumer-repo `.github/workflows/*.yml` (CI) | Mirrors the SOP-CICD_BASELINE_001 baseline plus per-repo customisations. Drift detected by `check_external_repo_ci_posture.py` (extended in P5). |
| Per-consumer-repo `playwright.config.ts` | Mirrors a shared template (added in P2). |
| Per-consumer-repo Sentry config (`sentry.client.config.ts`, `sentry.server.config.ts`, `next.config.mjs` `withSentryConfig`) | Mirrors the canonical pattern documented in P4. |
| Argos / Percy / Chromatic baseline storage | Vendor cloud; not in git; correlated via release SHA. |
| Sentry release records | Vendor cloud; correlated via D-IH-68-I cross-repo strategy. |
| InfraMonitor v0 dashboard data layer | Reads from Vercel API + Sentry API + GitHub Actions API; stateless aggregator. |

## Reference-only (read; do not edit here)

- I66 master-roadmap + decision-log (motivation context).
- I63 bless-pattern documentation + scaffolder script (consumer-repo registry foundation).
- Vercel + Render + Sentry vendor docs.
- Visual-regression vendor docs (Argos / Percy / Chromatic / Lost Pixel — for P1 research).
