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

### 3.6 Figma — visual SSOT for high-stakes deliverables

**Rule.** Figma is the **canonical visual source of truth** for any deliverable where layout decisions matter (decks, dossiers, pitch decks, partner-facing pitches, design libraries). Markdown / YAML remains the **content** SSOT; Figma owns **layout**. Drift between the two follows the rule documented in each deliverable's master roadmap.

**Why a SOP entry.** Figma joins Supabase + GitHub repos as a tool that produces canonical artifacts the rest of the AKOS stack consumes. Without a SOP entry, every operator/agent makes ad-hoc decisions about which file goes where, which team owns it, and how to cite it. With this SOP entry, those decisions are pre-resolved.

**Canonical invocation surface (Figma MCP).**

| Purpose | Tool |
|:---|:---|
| Identify the authenticated user + available teams | `whoami` |
| Create a new file in a chosen team / project | `create_new_file` |
| Read frame metadata + structure | `get_metadata` |
| Read a frame as a screenshot for visual review | `get_screenshot` |
| Execute Plugin API JS to mutate the file (create / refine frames, components, variables) | `use_figma` (always preceded by loading the `figma-use` skill) |
| Capture a web/HTML page into Figma as a layout reference | `generate_figma_design` (always preceded by loading the `figma-generate-design` skill) |
| Inspect / write Code Connect mappings | `get_code_connect_*` / `add_code_connect_map` / `send_code_connect_mappings` |

**Pinned skills.** Two skills MUST be loaded before specific tool calls and the skill name passed to the tool's `skillNames` parameter:

- Before any `use_figma` call: load `figma-use`. Without it, common Plugin API failure modes (font-loading order, layout-mode-mismatch, color-range, page-context reset) are uncaught.
- Before any `use_figma` call that builds or updates a multi-section view (deck, page, modal): also load `figma-generate-design`.

**Team workspace policy.** Files for company-facing deliverables (decks, dossiers, brand libraries) go in the team workspace identified in [`FIGMA_FILES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/FIGMA_FILES_REGISTRY.md). Files for ad-hoc explorations may live in a personal team / drafts; **explorations promoted to canonical require a row in the files registry**.

**File naming convention.** `<Org> - <Artifact name> (<context>)`. Example: `Holistika Research - Company Dossier (ENISA 2026)`. Spaces are allowed; avoid emoji because the Figma MCP tools sometimes echo names into JSON without normalization.

**Page + frame naming.** Within a file, the canonical page name follows `<Artifact slug> v<version>`. Example: `Company Dossier v1`. Frames inside follow `<NN> · <Section name>` so they sort numerically and read as a deck (e.g. `01 · Cover`, `06 · Tracción / Proof`, `14 · Siguiente paso`).

**Drift handling rule.** Per the I28/I29 master roadmaps:

1. Markdown / YAML SSOT (`deck_slides.yaml`, etc.) wins for **content**.
2. Figma wins for **visual layout** decisions made directly on the canvas.
3. HTML preview is fast iteration, never SSOT.
4. PDF is disposable, re-exported.
5. Any Figma copy edit that diverges from the YAML must be backported to the YAML before the consuming initiative closes.

**Cross-references**: [`FIGMA_FILES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/FIGMA_FILES_REGISTRY.md) — registry of all canonical Figma files; [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md) §"Output 1" — when a topic produces a Figma deliverable, the manifest carries `paths.figma_url` and (optionally) `paths.deck_yaml` to bind content + visual SSOT.

### 3.7 External design skill bundles — Impeccable as a consumer of brand SSOT

**Rule.** External design / UX skill bundles installed under `.cursor/skills/` (today: Impeccable Style; future: equivalent bundles) are treated as **skill consumers**, not as parallel sources of brand truth. Brand contracts always live in `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/`. The bundle's project-context file (e.g. Impeccable's `.impeccable.md`) is a **thin redirect** to those canonical files; it never duplicates voice / visual / jargon-audit content.

**Why.** Impeccable installs a `/teach` command that auto-writes a project-context file with brand voice, audience, anti-references, etc. Running `/teach` against the AKOS workspace would silently duplicate `BRAND_VOICE_FOUNDATION.md` + `BRAND_VISUAL_PATTERNS.md` + `BRAND_DO_DONT.md` + `BRAND_SPANISH_PATTERNS.md` + `BRAND_JARGON_AUDIT.md`, creating a parallel source that will drift the moment the operator updates one but not the other. The bridge-file pattern preserves Impeccable's command surface while keeping the brand SSOT canonical.

**Installation.** Per the upstream docs (`https://impeccable.style/`), Impeccable installs as a `.cursor/skills/` bundle:

1. Download the latest bundle ZIP from `https://impeccable.style/` (or `git clone https://github.com/pbakaus/impeccable && cp -r impeccable/dist/cursor/.cursor your-project/`).
2. Extract into the repo root so `.cursor/skills/` contains the Impeccable folders (e.g. `audit/`, `polish/`, `critique/`, `teach/`, `animate/`, ~23 commands total).
3. Verify the bundle does **not** overwrite any existing AKOS rule under `.cursor/rules/akos-*.mdc`. If a conflict appears, AKOS rules win — see precedence below.

**Pre-requisites on the operator workstation.**

- Cursor with Agent Skills enabled (Settings → Beta → Rules → Agent Skills toggle on).
- Cursor on the Nightly channel (the bundle is calibrated to skill features in Nightly as of 2026-Q1).

**Bridge files (canonical contract).** Impeccable's loader at `.cursor/skills/impeccable/scripts/load-context.mjs` reads two files at the repo root before every command: `PRODUCT.md` (audience, voice, anti-references) and `DESIGN.md` (visual identity, tokens, layout). Instead of running `/impeccable teach` and accepting its auto-generated content, the operator hand-writes both as **thin redirects** to the canonical brand SSOT:

- [`PRODUCT.md`](../../../../../../../PRODUCT.md) — points at `BRAND_VOICE_FOUNDATION.md`, `BRAND_DO_DONT.md`, `BRAND_REGISTER_MATRIX.md`, `BRAND_SPANISH_PATTERNS.md`, `BRAND_JARGON_AUDIT.md`. Contains a one-page summary derived from those files plus an explicit AKOS-precedence rule.
- [`DESIGN.md`](../../../../../../../DESIGN.md) — points at `BRAND_VISUAL_PATTERNS.md` and the deck-specific [`deck-visual-system.md`](../../../../_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md). Contains a token snapshot, typography snapshot, layout-primitive list, and visual anti-patterns — all sourced from the canonical files.

Both bridges include a **non-negotiable AKOS-precedence rule** at the bottom: when Impeccable suggestions conflict with `.cursor/rules/akos-*.mdc`, the AKOS rule wins.

**Canonical command surface.** The 23-command Impeccable bundle ships many commands; the AKOS-canonical four are:

| Command | Use |
|:---|:---|
| `/critique <path>` | Full design review with persona tests + browser overlay anti-pattern detection. Best first pass. |
| `/audit <path>` | Technical quality (accessibility, performance, responsive, theming). Useful before shipping. |
| `/polish <path>` | Targeted, surgical fixes (alignment, kerning, hardcoded color → token, missing hover state, etc.). Targeted diffs, not rewrites. |
| `/teach` | Reserved — **do not run interactively**. The bridge file above replaces its output. |

Other Impeccable commands (`/animate`, `/distill`, `/colorize`, etc.) may be used ad-hoc; they remain governed by AKOS rules below.

**Precedence rule (AKOS wins).** If an Impeccable command's output conflicts with `.cursor/rules/akos-*.mdc` (governance, planning traceability, asset classification, jargon audit, etc.), the AKOS rule wins. The bridge file declares this explicitly. In practice this means:

- Impeccable can suggest copy edits, but copy must pass `BRAND_JARGON_AUDIT.md` §4 before commit.
- Impeccable can suggest token replacements (hex → CSS var); the token names must come from `BRAND_VISUAL_PATTERNS.md` §1.
- Impeccable can suggest layout / motion changes; phase commits still scope per the planning traceability rule.

**Drift safeguard.** A test (`tests/test_impeccable_bridge.py`) asserts:

- `PRODUCT.md` exists at the repo root, points at all five canonical brand files (`BRAND_VOICE_FOUNDATION.md`, `BRAND_DO_DONT.md`, `BRAND_REGISTER_MATRIX.md`, `BRAND_SPANISH_PATTERNS.md`, `BRAND_JARGON_AUDIT.md`), and contains the non-negotiable AKOS-precedence rule.
- `DESIGN.md` exists at the repo root, points at `BRAND_VISUAL_PATTERNS.md` and `deck-visual-system.md`, and contains the AKOS-precedence rule.
- Neither bridge contains hardcoded hex colors that would imply duplicated brand-token content (only HSL token names from the canonical visual file).

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
| 1.1 | 2026-04-30 | Initiative 29 P2 — added §3.6 Figma (visual SSOT, MCP tools, file naming, drift handling) + §3.7 External design skill bundles (Impeccable Style as a consumer of brand SSOT, bridge-file pattern, AKOS-precedence rule). Cross-references new [`FIGMA_FILES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/FIGMA_FILES_REGISTRY.md). |
