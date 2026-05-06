<!--
  AKOS template — pull-request template for Holistika-tracked external repos.
  Rendered by scripts/bless_external_repo.py into <repo>/.github/PULL_REQUEST_TEMPLATE.md.
  Placeholders: {{REPO_SLUG}}, {{REPO_CLASS}}, {{PRIMARY_OWNER_ROLE}}, {{VAULT_DOC_ROOT}}.
  Last revision: 2026-05-06.
-->

<!--
  {{REPO_SLUG}} pull request — repo class {{REPO_CLASS}}, primary owner {{PRIMARY_OWNER_ROLE}}.
  Be small. Be focused. Cite the AKOS decision when governance-relevant.
  See CONTRIBUTING.md and EXTERNAL_REPO_CONTRACT.md at the repo root.
-->

## Summary

<!-- What does this PR do, in 1–3 sentences? -->

## Why

<!-- What problem does it solve, or what user/operator outcome does it enable? -->

## AKOS linkage

- **Decision id** (if applicable): `D-IH-XX-Y`
- **Initiative folder** (if applicable): `docs/wip/planning/<NN-slug>/` in AKOS
- **Mirror impact**:
  - [ ] None — no `compliance.*_mirror` schema touched
  - [ ] Read-only consumption (new view / query, no schema change)
  - [ ] New column / row consumed (links the AKOS PR that minted it)
  - [ ] Operator SQL gate engaged for migration

## Surface impact

<!-- Operator vs showcase vs both? Any new route, env var, secret, or feature flag? -->

- Routes touched:
- New env vars / secrets:
- Feature flags:

## Checklist

- [ ] Local lint / typecheck / test gates pass (see `CONTRIBUTING.md`)
- [ ] Brand-jargon scan green on any external-shipping prose
- [ ] No invented HLK IDs locally
- [ ] No HLK CSV authoring locally
- [ ] Operator SQL gate respected for any schema change
- [ ] Security headers / CSP untouched OR change explicitly justified

## Screenshots / recordings (UI changes)

<!-- Drop before/after; for flows, attach a short GIF or Loom. -->

## Deployment notes

<!-- Anything the operator should know at deploy time. -->

## Rollback plan

<!-- One sentence: how do we get back to a known-good state if this misbehaves in production? -->
