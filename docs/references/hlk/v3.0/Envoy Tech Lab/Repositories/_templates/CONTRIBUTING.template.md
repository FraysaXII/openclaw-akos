<!--
  AKOS template — root CONTRIBUTING.md for Holistika-tracked external repos.
  Rendered by scripts/bless_external_repo.py into <repo>/CONTRIBUTING.md.
  Placeholders: {{REPO_SLUG}}, {{REPO_CLASS}}, {{PRIMARY_OWNER_ROLE}}, {{VAULT_DOC_ROOT}}.
  Last revision: 2026-05-06.
-->

# Contributing to {{REPO_SLUG}}

> Holistika-tracked repository — class **{{REPO_CLASS}}**, primary owner **{{PRIMARY_OWNER_ROLE}}**. AKOS is the single source of truth for HLK doctrine; this repository consumes those canonicals read-only.
>
> Read the [`EXTERNAL_REPO_CONTRACT.md`](EXTERNAL_REPO_CONTRACT.md) first — it pins the invariants this repo agrees to.

## Governance flow (read this first)

1. **AKOS wins on conflict.** If a doctrine statement here disagrees with the AKOS canonical, AKOS is correct. Open a PR to AKOS, not a workaround here.
2. **Never invent governed IDs locally.** Persona, channel, vendor, skill, cell, policy, program, topic, GOI/POI, process, org IDs are all minted in AKOS via PRs to the canonical CSVs in [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`](https://github.com/FraysaXII/openclaw-akos/tree/main/docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/).
3. **Brand-jargon scan applies to external prose.** Public READMEs, deployed pages, user-facing UI strings on showcase surfaces, generated dossiers/invoices/cover-emails must avoid the forbidden tokens listed in [`BRAND_JARGON_AUDIT.md`](https://github.com/FraysaXII/openclaw-akos/blob/main/docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) §4. Internal prose (developer comments, implementation notes) is unrestricted.
4. **Operator SQL gate.** No ad-hoc DDL/DML against production. Any schema change goes through the gate per [`operator-sql-gate.md`](https://github.com/FraysaXII/openclaw-akos/blob/main/docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md): proposal → operator approval → versioned migration.

## Branches

- `feature/*` — new functionality
- `fix/*` — bug fixes
- `chore/*` — non-functional housekeeping
- `release/*` — release preparation
- `hotfix/*` — production hotfixes

## Commit messages

[Conventional Commits](https://www.conventionalcommits.org/) only. When the change is governance-relevant, link the AKOS decision id in the body:

```
feat(area): short summary

Body explaining the why.

AKOS-decision: D-IH-XX-Y
AKOS-initiative: <NN-slug>
```

## Local gates

The exact commands depend on the repo stack — see the project's `package.json` / `pyproject.toml` and the README. The minimum bar:

- Lint / format
- Type-check (where applicable)
- Unit tests
- Brand-jargon scan on any external-shipping prose

## PR cadence

- Keep PRs small and focused. One concern per PR.
- Fill out the [PR template](.github/PULL_REQUEST_TEMPLATE.md).
- All status checks must be green before merge.

## Secrets

Never commit secrets. Use environment variables or the platform-native secret store. Rotation cadence in [`docs/runbooks/secrets-rotation.md`](docs/runbooks/secrets-rotation.md) (when present).

## When in doubt

- [`EXTERNAL_REPO_CONTRACT.md`](EXTERNAL_REPO_CONTRACT.md) — invariants for this repo
- [`.cursor/rules/akos-mirror.mdc`](.cursor/rules/akos-mirror.mdc) — always-loaded AKOS reminder
- AKOS [`USER_GUIDE.md`](https://github.com/FraysaXII/openclaw-akos/blob/main/docs/USER_GUIDE.md) §24.12, §24.13
- Open a `governance.yml` issue (it prompts for the linked AKOS canonical)
