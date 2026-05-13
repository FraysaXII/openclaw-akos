---
language: en
intellectual_kind: SOP
status: review
version: v0.9.0
last_review: 2026-05-10
owner: System Owner
audience: System Owner, Tech Lead
access_level: 4
linked_initiative: I68
linked_decisions: D-IH-68-A, D-IH-68-B, D-IH-68-C, D-IH-68-D, D-IH-68-E, D-IH-68-G, D-IH-68-I, D-IH-68-J
related_processes: env_tech_dtp_cicd_baseline_maintenance (lands in I68 P5 PAUSE POINT #3); env_tech_dtp_observability_dashboard_review (same); env_tech_dtp_visual_regression_triage (same)
related_canonicals:
  - REPOSITORY_REGISTRY.csv
  - SENTRY_DASHBOARD_HOLISTIKA.md
  - playwright.config.ts.tmpl
related_validators:
  - scripts/validate_playwright_baseline.py
  - scripts/validate_sentry_release_format.py
  - scripts/validate_cicd_baseline.py
cursor_rules:
  - akos-deploy-health.mdc
  - akos-governance-remediation.mdc
  - akos-mirror-template.mdc
  - akos-docs-config-sync.mdc
  - akos-planning-traceability.mdc
---

# SOP — CICD Baseline (v0.9.0, status: review)

**Document owner**: System Owner.
**Process anchor**: `env_tech_dtp_cicd_baseline_maintenance` (canonical row added in I68 P5 PAUSE POINT #3 — canonical CSV gate).
**Status**: `review` at land time (I68 P5); promoted to `active` (`v1.0.0`) in I68 P8 closure once at least one `class=platform` consumer-repo PR has shipped a workflow generated from the canonical template at [`_templates/github-workflows/ci-baseline.yml.tmpl`](../../../../../Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl) and [`scripts/check_external_repo_ci_posture.py`](../../../../../../../scripts/check_external_repo_ci_posture.py) reports it healthy.

> **Why this SOP exists.** The I66 P5 build-fix incident catalogued in [I66 P5 reports](../../../../../../../wip/planning/66-brand-vision-ops-sweep/reports/) showed 16 of 20 boilerplate deployments ERROR with 5 sequential failure modes — every failure was solvable post-hoc but a multi-viewport visual regression + per-repo deploy telemetry + build-time discipline + per-class CI baseline would have caught most pre-merge or pre-deploy. This SOP codifies that baseline so the next consumer repo blessed via [`scripts/bless_external_repo.py`](../../../../../../../scripts/bless_external_repo.py) inherits the discipline automatically.

---

## 1. Purpose

This SOP defines the **canonical CI/CD baseline** every Holistika consumer repo (governed via [`REPOSITORY_REGISTRY.csv`](../../../../../compliance/REPOSITORY_REGISTRY.csv)) must carry, broken down by `class` (per the existing `class` column: `platform` / `reference` / `internal` / `client-delivery`).

It exists because, before I68:

1. **CI configuration drifted** between sibling repos. `boilerplate` had Lighthouse + visual smoke; `hlk-erp` had only lint + type; `kirbe-platform` had a custom Render-only workflow. Cross-repo issues (e.g. brand-jargon drift in deck templates ↔ boilerplate prose) needed three different debug sessions.
2. **Visual regression was reactive**, not pre-merge. The I66 P5 incident is the worked example.
3. **Deploy telemetry was inconsistent.** Sentry was wired in `boilerplate` but production-only on a non-canonical sample-rate; `hlk-erp` had no Sentry at all; `kirbe-platform` had a Render-side log dump but no error-grouping.
4. **Build-time discipline was unowned.** Operator targets ("preview build < 2 min" in casual conversation) had no per-repo enforcement; targets like `boilerplate@< 2 min` and `kirbe-platform@< 5 min` lived in head-canon, not in `REPOSITORY_REGISTRY.csv`.

This SOP closes all four gaps.

## 2. Scope

| In scope | Out of scope |
|:---|:---|
| `class=platform` consumer repos (kirbe-platform, hlk-erp, openclaw-akos) | `class=client-delivery` repos (defined when first such repo blesses) |
| `class=reference` consumer repos (boilerplate) | Sibling-repo working tree changes from the AKOS workspace (operator does these via [`bless_external_repo.py`](../../../../../../../scripts/bless_external_repo.py) `--with ci-baseline` per §6) |
| `class=internal` consumer repos (akos-telemetry-ci) | Per-repo *engineering* deep dives (live in repo-local CI files; this SOP only enforces the baseline) |
| Per-repo per-class baseline check matrix (§3) | Per-repo Sentry alert *rules* (live in Sentry UI per repo) |
| Per-class workflow templates + Render YAML stub (§4) | Per-repo build-time *optimisation* targets (live in `REPOSITORY_REGISTRY.csv build_time_target_seconds`) |
| Vercel preview-protection bypass pattern (§5) | Per-repo Vercel project configuration (operator-managed in Vercel UI) |
| Render preview-protection equivalent + cold-start pattern (§5) | Per-repo Render service configuration (operator-managed in Render UI) |
| Per-repo opt-out matrix (§7; D-IH-68-J) | Disabling the entire baseline for a repo (no opt-out at the SOP level — class downgrade required) |

## 3. Per-class baseline check matrix

Every consumer repo's CI must run the checks marked ✓ for its `class`. Per-repo opt-outs are encoded in [`REPOSITORY_REGISTRY.csv ci_baseline_optouts`](../../../../../compliance/REPOSITORY_REGISTRY.csv) (column lands in I68 P5 PAUSE POINT #3 — canonical CSV gate); the validator at [`scripts/validate_cicd_baseline.py`](../../../../../../../scripts/validate_cicd_baseline.py) enforces this matrix.

| Check | platform | reference | internal | client-delivery | Per-check opt-out string |
|:---|:---:|:---:|:---:|:---:|:---|
| `lint` (eslint / pyflakes / equivalent) | ✓ | ✓ | ✓ | ✓ (TBD when first lands) | `lint` |
| `typecheck` (`tsc --noEmit` / `mypy` / equivalent) | ✓ | ✓ | ✓ | ✓ (TBD) | `typecheck` |
| `unit-test` (`vitest` / `jest` / `pytest`) | ✓ | ✓ | ✓ | ✓ (TBD) | `unit-test` |
| `playwright-smoke` (5 viewports per [I68 P2 canonical template](../../../../../Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl)) | ✓ | ✓ | ✗ | ✓ (TBD) | `playwright-smoke` + per-viewport `playwright-viewport-<name>` |
| `visual-regression` (Argos PR comment per D-IH-68-A) | ✓ | ✓ | ✗ | ✓ (TBD) | `visual-regression` |
| `lighthouse` (perf + a11y per akos-deploy-health §"Step 4") | ✓ | ✓ | ✗ | ✓ (TBD) | `lighthouse` |
| `brand-jargon` (boilerplate is the brand surface; platform repos that ship public prose carry this) | ✓ | ✓ (full set) | ✗ | ✓ (TBD) | `brand-jargon` |
| `brand-voice-register` | ✓ (where applicable) | ✓ | ✗ | ✓ (TBD) | `brand-voice-register` |
| `sentry-release-format` (per [SENTRY_DASHBOARD_HOLISTIKA.md §2](../../../../../Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md) + D-IH-68-I) | ✓ | ✓ | ✗ | ✓ (TBD) | `sentry-release-format` |
| `sentry-skip-on-preview` (D-IH-68-C) | ✓ | ✓ | ✗ | ✓ (TBD) | `sentry-skip-on-preview` |
| `build-time-target` (assert preview build under `build_time_target_seconds`) | ✓ | ✓ | ✗ | ✓ (TBD) | `build-time-target` |

Notes on the matrix:

- **`class=internal` repos** (e.g. `akos-telemetry-ci`) ship without a rendered surface and skip every visual / brand / observability check. They get the lint + typecheck + unit-test floor only.
- **`class=reference` (boilerplate)** carries every check at its strictest setting because boilerplate IS the brand surface — every brand-jargon hit in boilerplate is a defect, not a flake.
- **`class=client-delivery`** is reserved; first such repo defines the per-check expectation in a successor SOP version (`v1.1.0`).
- **Per-repo opt-out via `ci_baseline_optouts` JSON-array column** (e.g. `["lighthouse","brand-jargon"]`) is allowed but every opt-out must carry a justification entry in the repo's `BASELINE_REALITY.md` (mirror file maintained per [`.cursor/rules/akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) per I66 P2). Open-ended "we don't want to" is rejected by [`scripts/validate_cicd_baseline.py`](../../../../../../../scripts/validate_cicd_baseline.py); concrete operator-justification strings are required.

## 4. Workflow templates

### 4.1 GitHub Actions canonical template (Vercel + Render)

Located at [`docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl`](../../../../../Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl). The template:

- Uses GitHub Actions matrix strategy for Node versions (Node 20 + 22 by default; per-repo `package.json engines.node` narrows the matrix).
- Pulls Playwright config from the consumer repo's `playwright.config.ts` (which mirrors the I68 P2 canonical template).
- Validates the Sentry release-format via `npx --yes @holistika/cicd-baseline-cli validate-sentry-release` (the CLI wraps the AKOS Pydantic validator; first-class npm package candidate but ships as `npx --yes` for now to avoid distribution complexity).
- Posts a single PR-comment summary table aggregating every check's status, with a click-through to the failing job log.

Operators install the template into a consumer repo via:

```sh
py scripts/bless_external_repo.py --repo-slug <slug> --with ci-baseline
```

(Extension to `bless_external_repo.py` lands in I68 P5 PAUSE POINT #3 — canonical CSV gate alongside the column bumps.)

### 4.2 Render YAML stub (kirbe-platform-class)

Located at [`docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/render/render-baseline.yaml.tmpl`](../../../../../Envoy Tech Lab/Repositories/_templates/render/render-baseline.yaml.tmpl). The stub documents:

- **Build-cache pattern.** `buildCommand` ends with the canonical `--cache-from` invocation (Docker BuildKit layer cache); `buildFilter.paths` declares which file changes invalidate the cache.
- **Healthcheck pattern.** `healthCheckPath` always points at `/health` (Holistika convention), which returns `{"status": "ok", "release": "<repo>@<sha>"}` per the same release-format contract from [SENTRY_DASHBOARD_HOLISTIKA.md §2](../../../../../Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md).
- **Cold-start pattern.** `numInstances >= 1` for production services (no scale-to-zero; cold-starts are the dominant tail-latency contributor on Render's free + starter tiers).
- **Auto-deploy filter.** Only `branch=main` triggers production deploys; preview deploys land on `preview-*` branches with `previewsEnabled: true`.

The stub is **operator-edited per service**; the validator at [`scripts/validate_cicd_baseline.py`](../../../../../../../scripts/validate_cicd_baseline.py) reads it as a contract reference, not as a rigid mirror (Render YAMLs vary too much per service for sha256-stamped mirroring).

## 5. Per-platform preview-protection bypass

### 5.1 Vercel (Next.js)

Vercel preview deployments are protected by Vercel Authentication when a project enables the feature. Playwright (and any external pre-merge check) bypass the protection by sending the `x-vercel-protection-bypass` header with `VERCEL_AUTOMATION_BYPASS_SECRET` per [Vercel's official docs](https://vercel.com/docs/security/deployment-protection). The CI workflow template at [`ci-baseline.yml.tmpl`](../../../../../Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl) reads the secret from `secrets.VERCEL_AUTOMATION_BYPASS_SECRET`; the `playwright/auth.setup.ts` file (mirrored from the I68 P3 boilerplate canary) captures `storageState` by sending the header in a one-off authentication request before the smoke spec runs.

The header is also documented in [SENTRY_DASHBOARD_HOLISTIKA.md §3.1](../../../../../Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md) for operator transparency.

### 5.2 Render (FastAPI Python or Next.js Node)

Render preview environments do not have an equivalent vendor-managed authentication wall today. Operator-side discipline:

- Preview branches are deployed under `preview-*` branch names with `previewsEnabled: true`; they are environment-scoped (no production data access; no production Sentry events).
- The release-format `<repo>@<sha>` distinguishes preview vs production events in Sentry; combined with `tracesSampleRate: 0.0` on preview, this avoids preview-noise polluting the cross-repo dashboard.
- If/when Render adds an authentication-bypass secret (tracked as an internal operator OPS issue), this section gets a §5.2.1 update.

## 6. Operator-driven adoption flow (`bless_external_repo.py --with ci-baseline`)

Once the canonical CSV column bumps land at I68 P5 PAUSE POINT #3, the operator runs:

```sh
py scripts/bless_external_repo.py --repo-slug <slug> --with ci-baseline
```

The flag (additive to existing `--with` flags from the I63 bless infrastructure):

1. Reads the consumer repo's `class` from [`REPOSITORY_REGISTRY.csv`](../../../../../compliance/REPOSITORY_REGISTRY.csv).
2. Looks up the per-class check matrix from §3 of this SOP (parsed at runtime from the SOP's frontmatter `related_validators` + the `## 3` table).
3. Stamps the canonical workflow template `ci-baseline.yml.tmpl` into the consumer repo's `.github/workflows/ci-baseline.yml`, sha256-tagging the resulting file per the existing bless pattern.
4. (For `class=platform` Render repos) stamps `render-baseline.yaml.tmpl` into the consumer repo's `render.yaml` (or appends to it if the repo already carries one).
5. Sets the `ci_baseline_version` column for the row to the SOP's frontmatter `version` (initially `v0.9.0`; bumped to `v1.0.0` in I68 P8 closure).
6. Sets `build_time_target_seconds` from the per-class default (Vercel Next.js → 120s; Render Python+Node → 300s; static → 60s) unless the operator passes `--build-time-target <seconds>`.
7. Initialises `ci_baseline_optouts` to `[]` (empty JSON array); operator amends post-bless when needed.
8. Stamps a sha256 of the resulting `ci-baseline.yml` into [`REPOSITORY_REGISTRY.csv`](../../../../../compliance/REPOSITORY_REGISTRY.csv) so [`scripts/check_external_repo_ci_posture.py`](../../../../../../../scripts/check_external_repo_ci_posture.py) can detect drift.

## 7. Per-repo opt-out matrix (D-IH-68-J)

Encoded in [`REPOSITORY_REGISTRY.csv ci_baseline_optouts`](../../../../../compliance/REPOSITORY_REGISTRY.csv) as a JSON-array column (column lands in I68 P5 PAUSE POINT #3 — canonical CSV gate per [`.cursor/rules/akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc)). Allowed values are the per-check opt-out strings from §3 plus the per-viewport opt-out strings from [I68 P2 Playwright baseline §"Per-repo opt-out"](../../../../../Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl).

Examples:

| Repo | `ci_baseline_optouts` | Why |
|:---|:---|:---|
| `kirbe-platform` | `["lighthouse","brand-jargon","brand-voice-register"]` | Backend-heavy FastAPI; no rendered brand surface |
| `boilerplate` | `[]` (no opt-outs) | Brand surface; full strict baseline |
| `hlk-erp` | `["playwright-viewport-iphone-se","playwright-viewport-iphone-11"]` | Operator-internal surface; full mobile coverage not required at v0 (revisit in I68 P8) |
| `akos-telemetry-ci` | (column unused; `class=internal` skips most checks per matrix) | Internal repo |

The validator at [`scripts/validate_cicd_baseline.py`](../../../../../../../scripts/validate_cicd_baseline.py) honours opt-outs but **requires a corresponding justification entry in the repo's `BASELINE_REALITY.md`** (or, until that mirror exists per repo, in the repo's `README.md` "CI Baseline" section). Empty justification → validator FAIL with operator-actionable message.

## 8. Verification

- [`scripts/validate_cicd_baseline.py`](../../../../../../../scripts/validate_cicd_baseline.py) (forward-compatible: tolerates missing `ci_baseline_version` / `build_time_target_seconds` / `ci_baseline_optouts` columns until P5 CSV gate lands).
- [`scripts/check_external_repo_ci_posture.py`](../../../../../../../scripts/check_external_repo_ci_posture.py) (existing I63 script; extended in I68 P5 to cross-check each `class=platform` repo's `.github/workflows/ci-baseline.yml` sha256 against the `REPOSITORY_REGISTRY.csv` recorded sha).
- [`scripts/release-gate.py`](../../../../../../../scripts/release-gate.py) wires `validate_cicd_baseline` after `validate_sentry_release_format` per the same I68-cluster ordering convention used in P2 + P4.
- Per-class smoke: every `class=platform` consumer repo, after a successful `bless_external_repo.py --with ci-baseline`, must show a green workflow run on its next PR; failure → revert the `--with ci-baseline` flag and triage.

## 9. Change-control

This SOP body is the canonical source of truth for the baseline. Changes follow the standard SOP-META workflow per [`SOP-META_PROCESS_MGMT_001.md`](../../Tech/System Owner/SOP-MADEIRA_INCIDENT_RESPONSE_001.md):

1. Open a successor decision (e.g. `D-IH-NN-X`) in the relevant initiative's `decision-log.md` describing the addition / removal / opt-out.
2. Update §3 matrix or §7 opt-out matrix here.
3. Bump frontmatter `version` (semver: minor for adds + non-breaking opt-out additions; major for breaking changes that require existing repo PRs to update).
4. Open per-repo PRs to update their `.github/workflows/ci-baseline.yml` if the workflow template content changed.
5. Update [`scripts/check_external_repo_ci_posture.py`](../../../../../../../scripts/check_external_repo_ci_posture.py) to expect the new sha256.

## 10. Cross-references

- [I68 master roadmap](../../../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/master-roadmap.md) §P5 (this SOP's parent phase).
- [I68 decision log](../../../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/decision-log.md) §D-IH-68-D (per-class baseline) + §D-IH-68-J (per-repo opt-outs).
- [SENTRY_DASHBOARD_HOLISTIKA.md](../../../../../Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md) (the Sentry-specific operator runbook this SOP cites).
- [Playwright canonical template](../../../../../Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl) (the Playwright-specific canonical config this SOP cites).
- [`.cursor/rules/akos-deploy-health.mdc`](../../../../../../../.cursor/rules/akos-deploy-health.mdc) (operator deploy-health rule this SOP operationalises at fleet scale).
- [`.cursor/rules/akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) (governs the §3 matrix + §7 opt-out + §6 bless-flow per the canonical CSV gate).
- [`.cursor/rules/akos-mirror-template.mdc`](../../../../../../../.cursor/rules/akos-mirror-template.mdc) (governs the AKOS-template-as-SSOT + sibling-repo-mirrors model used in §4).
