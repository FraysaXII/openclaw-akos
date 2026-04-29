# SOP — HLK Tooling Standards (v1.0)

**Document owner**: System Owner
**Process anchor**: `thi_tech_dtp_312`
**Version**: 1.0
**Date**: 2026-04-29
**Status**: Active
**Cursor rules**: [`akos-holistika-operations.mdc`](.cursor/rules/akos-holistika-operations.mdc), [`akos-docs-config-sync.mdc`](.cursor/rules/akos-docs-config-sync.mdc)

---

## 1. Purpose

This SOP codifies the **canonical command-line invocation** for every external tool the AKOS workspace depends on, and the **canonical reference format** for any external GitHub repository the operator/agents may cite. It exists because:

1. Documentation drift (different SOPs/README files invoking the same CLI under bare `<tool>` vs `npx <tool>` vs `pip install <tool>` vs Studio-only) creates "it works on my machine" failures and slows onboarding.
2. Cross-repo references that point at local filesystem paths (e.g. `c:\Users\Shadow\cd_shadow\root_cd\boilerplate`) break the moment the workspace is cloned to a different host or a teammate; they should always degrade to a portable GitHub URL with a local-clone hint.

A single SOP reference replaces ad-hoc text across every README/CONTRIBUTING/checklist.

## 2. Scope

| In scope | Out of scope |
|:---|:---|
| Supabase CLI invocation | Supabase Dashboard click-paths (operator runbook) |
| External GitHub repo citations from inside this AKOS repo | Internal AKOS code references (covered by [`PRECEDENCE.md`](../../../../compliance/PRECEDENCE.md)) |
| Mermaid CLI (`mmdc`) invocation | Mermaid syntax (covered by `.mcp.json` figma plugin) |
| Pandoc / pypandoc rendering | Word / LibreOffice manual operator finishing (covered by individual export scripts) |
| Python entrypoints (`py scripts/...`) | Python virtualenv management (covered by [`CONTRIBUTING.md`](../../../../../../../CONTRIBUTING.md)) |

## 3. Standards

### 3.1 Supabase CLI — `npx supabase ...` (canonical)

**Rule.** Every Supabase CLI invocation in this repo MUST use `npx supabase` (or, equivalently, `npm run supabase --`). Never bare `supabase`.

**Why.**

- `supabase` is pinned as a `devDependency` in [`package.json`](../../../../../../../package.json) (`"supabase": "^2.93.1"`). `npx supabase` resolves to the **pinned** local binary under `node_modules/.bin/`.
- Bare `supabase` resolves only when the operator has a globally-installed CLI. The global version typically drifts from the pinned version — different teammates run different CLI behaviours against the same migration ledger. That is precisely the "harmonize" problem this SOP closes.
- `npx supabase` is reproducible across operator workstations, CI runners, and ephemeral dev environments. It needs no global install (Node.js + npm only).
- `npm run supabase -- <subcommand>` is a synonym (uses the `"supabase": "supabase"` script alias in `package.json`). Either form is acceptable; **`npx supabase` is the documented default** because it has fewer characters and works without the `--` separator.

**Reference invocations** (canonical; copy-paste these in docs/SOPs):

| Purpose | Canonical command |
|:---|:---|
| Authenticate the local CLI to a Supabase account | `npx supabase login` |
| Link the local repo to a remote project | `npx supabase link --project-ref <PROJECT_REF>` |
| Inspect the remote migration ledger | `npx supabase migration list` |
| Create a new migration file with a timestamp prefix | `npx supabase migration new <short_description>` |
| Apply pending **schema** migrations from `supabase/migrations/` to the remote | `npx supabase db push` |
| Reconcile the remote schema back into a new migration file | `npx supabase db pull` |
| Repair the migration ledger after manual intervention | `npx supabase migration repair --status <reverted\|applied> <version>` |
| Generate TypeScript types from the live schema | `npx supabase gen types typescript --linked > types/supabase.ts` |

**Two-plane reminder.** This SOP only standardises the **CLI invocation form**. The two-plane convention from [`supabase/migrations/README.md`](../../../../../../../supabase/migrations/README.md) — schema DDL goes through `supabase/migrations/`, large compliance-mirror DML stays out — is unchanged. For mirror data (e.g. `compliance.topic_registry_mirror` upserts) the canonical path is:

1. Generate via `py scripts/sync_compliance_mirrors_from_csv.py --<register>-only --out artifacts/sql/<file>.sql`.
2. Operator review: open `artifacts/sql/<file>.sql`, confirm the upserts match `dimensions/<REGISTRY>.csv`.
3. Apply via Supabase Studio SQL editor (paste + run) **or** via `psql` against the project connection string (retrieved from the Dashboard project page, never committed). The `user-supabase` MCP `execute_sql` tool is an authenticated alternative when available.
4. Verify with `py scripts/probe_compliance_mirror_drift.py --verify` (or the verify profile `compliance_mirror_drift_probe`) so canonical CSV row counts and live mirror row counts agree.

### 3.2 External GitHub repos — canonical reference format

**Rule.** Any reference to an external repository — including Holistika products at the `FraysaXII` GitHub org — MUST cite the repo by its `https://github.com/<org>/<repo>` URL via [`REPOSITORIES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md). Local filesystem paths are operator hints, never the SSOT.

**Canonical format** (use both lines together; the URL is the primary, the local-clone path is a non-binding hint):

```
Source: https://github.com/FraysaXII/<repo>
Local clone (this workstation): c:\Users\Shadow\cd_shadow\<container>\<repo> — operator-specific; not portable.
```

**The canonical registry is** [`REPOSITORIES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md). When citing an external repo from a doc / SOP / dossier:

1. **Always** point readers at the registry for the canonical row.
2. The `repo_slug` column is the stable identifier (e.g. `kirbe-platform`, `madeira-hlk-runtime`).
3. The `github_url` column is the canonical URL.
4. Add the local-clone path only as an **operator hint** (clearly marked as "this workstation"), never as the source-of-truth.

**Repos in scope** (current; sourced from [`REPOSITORIES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md)):

| repo_slug | github_url | class | role |
|:---|:---|:---|:---|
| `kirbe-platform` | `https://github.com/FraysaXII/kirbe` | platform | KiRBe SaaS — knowledge-management productisation |
| `madeira-hlk-runtime` | `https://github.com/FraysaXII/openclaw-akos` | platform | This monorepo (AKOS / vault / methodology) |
| `akos-telemetry-ci` | `https://github.com/FraysaXII/openclaw-akos` | internal | Same monorepo; `internal` class for telemetry/CI evidence |
| `client-delivery-pilot` | `https://github.com/<org>/<client-project-repo>` | client-delivery | Operator-confirmed per engagement |

**Repos worth promoting to the registry** (currently referenced in this SOP and in `BRAND_VISUAL_PATTERNS.md` / `dossier_es.md` Apéndice C; pending row addition by the operator):

- `holistika-research-boilerplate` → `https://github.com/FraysaXII/<boilerplate>` — Next.js 14 marketing + intake site; **canonical brand-visual source**.
- `hlk-erp` → `https://github.com/FraysaXII/<hlk-erp>` — internal ERP shell.
- `holistika-websitz-shopify-bundles` → `https://github.com/FraysaXII/<use-case-1>` — Shopify cart-bundle B2B partner app.
- `rushly-saas-scaffold` → `https://github.com/FraysaXII/<use-case-2>` — Rushly partner SaaS scaffold (design phase).

> **TODO[OPERATOR]** — promote these four placeholder rows into [`REPOSITORIES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) with the actual `<repo>` slugs once decided. Until then, [`BRAND_VISUAL_PATTERNS.md`](../../Marketing/Brand/BRAND_VISUAL_PATTERNS.md) cites the local clone path as an explicit operator-workstation hint and points here for the canonical contract.

### 3.3 Mermaid CLI — `npx -y -p @mermaid-js/mermaid-cli mmdc ...`

**Rule.** Diagram rendering MUST use either:

1. The shared script: `py scripts/render_km_diagrams.py [--all] [--update-manifest]` (preferred — handles font, theme, mmdc resolution, sha256 stamping).
2. Direct invocation: `npx -y -p @mermaid-js/mermaid-cli mmdc -i <input.mmd> -o <output.png>` (when the script is not the right tool, e.g. one-off ad-hoc diagram outside `_assets/`).

The pinned version contract lives in [`CONTRIBUTING.md`](../../../../../../../CONTRIBUTING.md) §"Mermaid CLI install" (Initiative 26 P1). Bare `mmdc` is permitted **only** after `npm install -g @mermaid-js/mermaid-cli` and only on operator workstations; it is **not** the canonical doc form.

### 3.4 Pandoc / pypandoc — `pypandoc_binary` (canonical pip-only path)

**Rule.** PDF/DOCX rendering paths in [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) try `WeasyPrint → fpdf2 → pandoc` (PDF) and `pandoc → pypandoc` (DOCX). For zero-system-install, the canonical pip path is:

```
py -m pip install --only-binary=:all: -r requirements-export.txt
```

This pulls `pypandoc_binary` (which bundles pandoc as a wheel). Bare `pandoc` is a fallback only.

### 3.5 Python entrypoints — `py scripts/...` on Windows, `python3 scripts/...` on POSIX

**Rule.** All Python script invocations in **operator-facing docs** on Windows use `py` (the Windows launcher); on POSIX use `python3`. CI uses whatever the matrix dictates. When mentioned in a cross-platform doc, use `py` and add a footnote: "POSIX equivalent: `python3 ...`".

## 4. Enforcement

### 4.1 Drift safeguards

- **Cursor rule guardrail.** [`akos-docs-config-sync.mdc`](.cursor/rules/akos-docs-config-sync.mdc) gains a row mentioning this SOP so any new doc that introduces bare `supabase ...` triggers a sync prompt.
- **Lint hint.** Operators or future automation (Initiative 28+) can grep for the anti-patterns:

```powershell
rg -n -P "(?<!npx )(?<!`)\bsupabase (login|link|migration|db push|db pull|migration list|migration new|migration repair)\b" docs/ supabase/ CONTRIBUTING.md
```

A non-empty result indicates drift from §3.1.

### 4.2 Updating this SOP

Edit this file directly when:

1. A new external CLI is added to the AKOS workflow.
2. The pinned Supabase CLI major version changes.
3. `REPOSITORIES_REGISTRY.md` adds a row that any vault doc currently references via local path.

After editing, run:

```powershell
py scripts/validate_hlk.py
py scripts/validate_hlk_vault_links.py
```

## 5. Cross-references

- [`supabase/README.md`](../../../../../../../supabase/README.md) — Supabase CLI quick card (operator runbook).
- [`supabase/migrations/README.md`](../../../../../../../supabase/migrations/README.md) — migration ledger parity rules.
- [`CONTRIBUTING.md`](../../../../../../../CONTRIBUTING.md) — onboarding + dependency install instructions.
- [`docs/DEVELOPER_CHECKLIST.md`](../../../../../../../docs/DEVELOPER_CHECKLIST.md) — verify-step matrix.
- [`docs/ARCHITECTURE.md`](../../../../../../../docs/ARCHITECTURE.md) §"Supabase migration plane".
- [`REPOSITORIES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) — canonical external-repo SSOT.
- [`PRECEDENCE.md`](../../../../compliance/PRECEDENCE.md) — overall compliance ranking.
- [`operator-sql-gate.md`](../../../../../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) — break-glass DDL SOP referenced from `supabase/README.md`.

## 6. Change log

| Version | Date | Change |
|:---|:---|:---|
| 1.0 | 2026-04-29 | Initial SOP — canonical `npx supabase` invocation + canonical GitHub repo reference format + cursor rule sync trigger. Created during Initiative 27 follow-up (post-merge harmonization request from operator). |
