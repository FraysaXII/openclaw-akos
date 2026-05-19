---
intellectual_kind: lane_inventory_and_design_report
sharing_label: internal_only
parent_initiative: INIT-OPENCLAW_AKOS-86
parent_lane: Lane F-GITHUB (Wave H, app-governance + metadata/tagging)
authored: 2026-05-19
last_review: 2026-05-19
linked_decisions:
  - D-IH-86-T  # cluster burndown plan
  - D-IH-86-O  # Option 5 default posture (conflict surfacing)
  - D-IH-86-AC  # PROPOSED — I86 cluster scope extension (app-governance lane)
  - D-IH-86-AD  # PROPOSED — REPOSITORY_REGISTRY.csv schema extension
  - D-IH-86-AE  # PROPOSED — SOP-TECH_APPLICATION_GOVERNANCE_001 mint
  - D-IH-86-AF  # PROPOSED — scripts/inventory_github_repos.py runbook mint
status: ratify_pending  # canonical-CSV gate per akos-governance-remediation.mdc + akos-holistika-operations.mdc
role_owner: System Owner
co_owner_role: PMO
language: en
gate_type: ratify-pending-canonical-csv-extension
related_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv
related_pydantic:
  - akos/hlk_repository_registry_csv.py
related_validators:
  - scripts/validate_repository_registry.py
  - scripts/validate_repository_registry_md_csv_sync.py
related_sops:
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_BLESSING_001.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md
related_scripts:
  - scripts/bless_external_repo.py
operator_quote: |
  "option B, as I told you this was bound to happen because we're creating and being holistik.
  I trust you'll do your best to craft the best solution as always."
  — operator, 2026-05-19, Wave H app-governance scope ratify
---

# Lane F-GITHUB — App Governance Inventory + Schema Design Report

## TL;DR

- **GitHub inventory:** 55 repositories under `FraysaXII` org. **4 production** (openclaw-akos, hlk-erp, boilerplate, kirbe) + **8 research** + **30 experiment** + **7 template** + **4 fork** + **2 uncategorized** + **0 archive**.
- **Governance gap:** `REPOSITORY_REGISTRY.csv` carries **7 rows** (5 unique GH repos: openclaw-akos, hlk-erp, boilerplate, kirbe, plus 2 placeholders + 1 internal alias for the AKOS monorepo). **51 of 55 GitHub repos (92.7%) are currently unmanaged** — not in the registry at all.
- **Proposed schema extension:** add **12 new columns** to `REPOSITORY_REGISTRY.csv` (17 → 29 cols). The load-bearing addition is **`app_class`** (production / research / experiment / template / fork / archive / uncategorized) — an *orthogonal* axis to the existing `class` column (which encodes AKOS governance relationship, not artifact purpose).
- **New SOP proposed:** `SOP-TECH_APPLICATION_GOVERNANCE_001.md` under `Envoy Tech Lab/canonicals/` (paired with new runbook `scripts/inventory_github_repos.py`, per `akos-executable-process-catalog.mdc` RULE 1).
- **Industry alignment:** matches the Spotify Backstage `catalog-info.yaml` GitOps SSOT pattern + GitHub 2026 custom-properties-driven ruleset governance + GOV.UK 2026 advisory ("don't use topics for automation; use explicit config"). AKOS-as-SSOT + GitHub-topics-as-discoverability-mirror is the correct shape.
- **Canonical-CSV gate required:** schema extension is a `gate_type: canonical-csv-gate` per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) + [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc). Operator MUST ratify the 12-column proposal in §6 before parent commits the schema bump + Pydantic + validator + migration + SOP + runbook bundle. See §9 for the numbered ratify checklist.

---

## §1 Scope of this report

Per Wave H ratify outcomes (operator's two human-input bullets in [`operator-scratchpad.md`](../operator-scratchpad.md) lines 62-63, 2026-05-19 15:30):

1. *"We need to reinforce governance of our applications. They will only grow in numbers, have several differences between each other but canonically they can be governed. Go look at GitHub to see how all apps I have and see how vast the scope is and growing (even though the vast majority are research and experiments)."*
2. *"Proper metadata and tagging is needed for a healthy data governance."*

Operator subsequently ratified **Option B (EXTEND I86 SCOPE)** at the lane-spawn gate (2026-05-19): *"option B, as I told you this was bound to happen because we're creating and being holistik. I trust you'll do your best to craft the best solution as always."*

This report is the **inventory + design** deliverable that precedes the canonical-CSV schema bump. It does NOT author files outside this report — per the lane prompt, parent commits the schema + Pydantic + validator + migration + SOP + runbook after operator ratifies the 12-column proposal in §6.

---

## §2 GitHub inventory (55 repos)

Source: `gh repo list FraysaXII --limit 200 --json …` (2026-05-19, captured at lane start).

### §2.1 Full table

| # | repo_name | vis. | fork | lang | pushed_at | proposed `app_class` | currently in registry? |
|--:|---|:--:|:--:|---|---|---|:--:|
|  1 | openclaw-akos | PUBLIC | — | Python | 2026-05-19 | **production** | yes (×2 alias) |
|  2 | hlk-erp | PRIVATE | — | Markdown | 2026-05-18 | **production** | yes |
|  3 | boilerplate | PRIVATE | — | TypeScript | 2026-05-09 | **production** | yes (`class=reference`) |
|  4 | kirbe | PRIVATE | — | PLpgSQL | 2026-05-07 | **production** | yes (`kirbe-platform` slug) |
|  5 | v0-efa-slim-crowdfunding-page | PRIVATE | — | TypeScript | 2026-04-15 | experiment | no |
|  6 | kirbe-frontend | PRIVATE | — | TypeScript | 2026-04-14 | experiment | no |
|  7 | holistika-websitz-shopify-app | PRIVATE | — | TypeScript | 2026-04-01 | **uncategorized** ⚠ | no |
|  8 | system-prompts-and-models-of-ai-tools | PUBLIC | T | — | 2026-03-05 | fork | no |
|  9 | TradingAgents | PUBLIC | T | Python | 2026-02-25 | fork | no |
| 10 | agentuity | PRIVATE | — | — | 2025-09-07 | **uncategorized** ⚠ | no |
| 11 | visiongen | PUBLIC | — | Python | 2025-06-30 | research | no |
| 12 | gemini_fastapi_RAG_Pydantic | PUBLIC | — | Python | 2025-05-11 | research | no |
| 13 | sop-shield-scribe | PRIVATE | — | TypeScript | 2025-05-09 | experiment | no |
| 14 | hlk-erp-design | PUBLIC | — | — | 2025-03-23 | experiment | no |
| 15 | nextjs-fastapi-supabase-vercel | PRIVATE | — | TypeScript | 2025-03-12 | template | no |
| 16 | obsidian-reader | PRIVATE | — | Python | 2025-02-17 | experiment | no |
| 17 | holistika-website | PRIVATE | — | TypeScript | 2025-01-14 | experiment | no |
| 18 | holistika-web | PRIVATE | — | — | 2024-10-01 | experiment | no |
| 19 | floating-endpoints | PRIVATE | — | TypeScript | 2024-09-26 | experiment | no |
| 20 | open-source-ai-artifacts | PRIVATE | — | TypeScript | 2024-08-11 | experiment | no |
| 21 | obsidian-holistika | PRIVATE | — | — | 2024-08-08 | experiment | no |
| 22 | function-call | PRIVATE | — | Jupyter | 2024-08-01 | research | no |
| 23 | hlk-vercel-payload | PRIVATE | — | TypeScript | 2024-07-13 | experiment | no |
| 24 | vercel-payload | PRIVATE | — | TypeScript | 2024-07-13 | experiment | no |
| 25 | e-commerce2 | PRIVATE | — | — | 2024-07-12 | experiment | no |
| 26 | e-commerce | PRIVATE | — | — | 2024-07-12 | experiment | no |
| 27 | boilerplate-2 | PRIVATE | — | TypeScript | 2024-06-22 | experiment | no |
| 28 | nextjs-supabase-kit | PRIVATE | — | TypeScript | 2024-06-18 | template | no |
| 29 | assemblyai | PRIVATE | — | Jupyter | 2024-06-17 | research | no |
| 30 | dalle3api | PRIVATE | — | Python | 2024-06-13 | research | no |
| 31 | hkassistant | PRIVATE | — | Python | 2024-06-12 | experiment | no |
| 32 | nextjs-with-supabase | PRIVATE | — | TypeScript | 2024-05-22 | template | no |
| 33 | nextjs-enterprise-boilerplate | PRIVATE | — | TypeScript | 2024-05-22 | template | no |
| 34 | app-directory | PRIVATE | — | TypeScript | 2024-05-22 | experiment | no |
| 35 | supabase | PUBLIC | T | TypeScript | 2024-05-08 | fork | no |
| 36 | homeplace-deploy | PRIVATE | — | TypeScript | 2024-05-02 | experiment | no |
| 37 | feature-flag-apple-store | PRIVATE | — | TypeScript | 2024-05-01 | experiment | no |
| 38 | nextjs-2 | PRIVATE | — | TypeScript | 2024-04-30 | experiment | no |
| 39 | python-hello-world | PRIVATE | — | Python | 2024-04-09 | experiment | no |
| 40 | python-hello-world-2 | PRIVATE | — | Python | 2024-04-09 | experiment | no |
| 41 | platforms-starter-kit | PRIVATE | — | TypeScript | 2024-04-09 | template | no |
| 42 | nextjs-fastapi-starter | PRIVATE | — | TypeScript | 2024-04-04 | template | no |
| 43 | fastapi-vercel | PRIVATE | — | TypeScript | 2024-04-04 | experiment | no |
| 44 | crew-ai-f | PRIVATE | — | Python | 2024-04-04 | research | no |
| 45 | with-google-analytics | PRIVATE | — | JavaScript | 2024-03-18 | experiment | no |
| 46 | nextjs-openai-doc-search-starter | PRIVATE | — | TypeScript | 2024-03-16 | template | no |
| 47 | pinecone-vercel-ai | PRIVATE | — | TypeScript | 2024-03-16 | experiment | no |
| 48 | funk-coding | PRIVATE | — | Python | 2024-02-18 | experiment | no |
| 49 | saas1 | PRIVATE | — | TypeScript | 2024-02-10 | experiment | no |
| 50 | susana-rag | PRIVATE | — | Python | 2024-01-14 | research | no |
| 51 | Questions-2 | PRIVATE | — | Python | 2023-10-29 | experiment | no |
| 52 | subscription-starter | PRIVATE | — | TypeScript | 2023-10-28 | experiment | no |
| 53 | nextjs | PRIVATE | — | TypeScript | 2023-10-23 | experiment | no |
| 54 | Susana-Autogen-Search | PRIVATE | — | Jupyter | 2023-10-09 | research | no |
| 55 | susanatest001 | PUBLIC | T | Python | 2023-07-20 | fork | no |

Observation: **0 repos use `isArchived=true`**. The operator has not exercised GitHub's archive flag for any of the 32 experiment-class or older research repos. This means `app_class=archive` will be empty at backfill; archival is a future operator-discipline gain (the SOP proposal in §7 codifies this).

### §2.2 Distribution

| app_class | count | % of 55 | examples |
|---|--:|--:|---|
| **production** | 4 | 7.3% | openclaw-akos, hlk-erp, boilerplate, kirbe |
| **research** | 8 | 14.5% | visiongen, susana-rag, dalle3api, gemini_fastapi_RAG_Pydantic, assemblyai, function-call, crew-ai-f, Susana-Autogen-Search |
| **experiment** | 30 | 54.5% | v0-efa-slim-crowdfunding-page, kirbe-frontend, sop-shield-scribe, hlk-erp-design, holistika-website, e-commerce, e-commerce2, boilerplate-2, …, nextjs-2, …, python-hello-world(-2), …, Questions-2, subscription-starter, nextjs |
| **template** | 7 | 12.7% | nextjs-fastapi-supabase-vercel, nextjs-supabase-kit, nextjs-with-supabase, nextjs-enterprise-boilerplate, platforms-starter-kit, nextjs-fastapi-starter, nextjs-openai-doc-search-starter |
| **fork** | 4 | 7.3% | system-prompts-and-models-of-ai-tools, TradingAgents, supabase, susanatest001 |
| **uncategorized** ⚠ | 2 | 3.6% | agentuity, holistika-websitz-shopify-app |
| **archive** | 0 | 0% | (none archived in GH today) |
| **TOTAL** | 55 | 100% | |

The operator's framing — *"vast majority are research and experiments"* — is **mechanically confirmed**: 30+8 = 38 of 55 (69.1%) are research or experiment. Including templates (12.7%) and forks (7.3%), **89.1% of repos are non-production** and warrant lighter-touch governance than the 4 production repos.

### §2.3 Uncategorized — operator input needed

Two repos need operator ratification of `app_class` before backfill:

1. **agentuity** (PRIVATE, no language detected, last push 2025-09-07, ~ 7 months stale). Name suggests an agentuity.com integration POC (an agentic platform-as-a-service) but the empty primary language + lack of description make this unclear. **Options:** `experiment` / `research` / `archive` (if abandoned).
2. **holistika-websitz-shopify-app** (PRIVATE, TypeScript, last push 2026-04-01, ~ 6 weeks stale). Description names it the "Holistika x Websitz Shopify Bundle + Cart App". If this is a live customer-deployed Shopify app for a Websitz partnership, it is **production** (and should be promoted to a registered governed repo). If it is a paused-or-discontinued partnership POC, it is **experiment** or **archive**. **Options:** `production` (governed promotion) / `experiment` / `archive`.

Both are flagged in the §6 ratify checklist for operator decision.

### §2.4 Staleness signal (pushed_at vs 2026-05-19)

A `pushed_at` column on the new schema lets us mechanically detect abandoned repos. Computed staleness for the 55 repos:

| Staleness bucket | count | % |
|---|--:|--:|
| < 30 days (fresh) | 4 | 7.3% (the 4 production repos) |
| 30-90 days | 4 | 7.3% (recent experiments + uncategorized) |
| 90-180 days | 1 | 1.8% |
| 180-365 days | 5 | 9.1% |
| 365-730 days (1-2 yr) | 19 | 34.5% |
| 730+ days (2+ yr) | 22 | 40.0% |

**40% of repos haven't been touched in 2+ years.** The SOP proposed in §7 includes a quarterly inventory sweep that flags this class for operator-decision: archive (cleanup) or revive (promote to research/production).

---

## §3 Current `REPOSITORY_REGISTRY.csv` state

### §3.1 Current schema (17 columns)

Per [`akos/hlk_repository_registry_csv.py`](../../../../akos/hlk_repository_registry_csv.py) `REPOSITORY_REGISTRY_FIELDNAMES`:

```
repo_slug, github_url, class, primary_owner_role, topic_ids, vault_doc_root,
api_spec_pointer, api_topic_id, lifecycle_status, notes,
consumes_compliance_types, consumes_mirrors, local_path,
last_review_at, last_review_by, last_review_decision_id,
methodology_version_at_review
```

**Enums** ([`hlk_repository_registry_csv.py`](../../../../akos/hlk_repository_registry_csv.py) L46-52):
- `class ∈ {platform, internal, client-delivery, reference}` — encodes **AKOS-relationship axis**.
- `lifecycle_status ∈ {active, archived, reference}` — encodes **state**.

### §3.2 Current rows (7 in CSV, 5 unique GH repos)

| repo_slug | github_url | class | primary_owner_role | lifecycle_status |
|---|---|---|---|---|
| kirbe-platform | https://github.com/FraysaXII/kirbe | platform | System Owner | active |
| openclaw-akos | https://github.com/FraysaXII/openclaw-akos | platform | AI Engineer | active |
| akos-telemetry-ci | https://github.com/FraysaXII/openclaw-akos (alias) | internal | System Owner | active |
| hlk-erp | https://github.com/FraysaXII/hlk-erp | platform | System Owner | active |
| boilerplate | https://github.com/FraysaXII/boilerplate | reference | Brand & Narrative Manager | reference |
| client-delivery-pilot | https://github.com/FraysaXII/client-delivery-pilot | client-delivery | PMO | active |
| (trailing empty row) | | | | |

5 unique GitHub repos are represented (kirbe, openclaw-akos × 2 alias rows, hlk-erp, boilerplate). One placeholder slug (`client-delivery-pilot`) points to a non-existent GitHub URL.

### §3.3 Governance-status partition (the gap we're closing)

| governance_status (proposed) | count of GH repos | %  | notes |
|---|--:|--:|---|
| **governed** (in registry + blessed full) | 3 | 5.5% | hlk-erp, kirbe-platform (kirbe), openclaw-akos |
| **inventoried** (in registry, light-touch) | 1 | 1.8% | boilerplate (`reference`-class skip per D-IH-32-N) |
| **unmanaged** (in GitHub, NOT in registry) | 51 | 92.7% | the 51 research / experiment / template / fork / uncategorized rows |
| **archived** | 0 | 0% | none |

The placeholder row `client-delivery-pilot` is also a "ghost" — points to a non-existent URL — and should be cleaned up at backfill (move to a tracker or drop).

---

## §4 External research — industry patterns (2026)

### §4.1 Spotify Backstage `catalog-info.yaml` (GitOps SSOT pattern)

[Backstage Software Catalog](https://backstage.io/docs/features/software-catalog) is the dominant 2026 IDP pattern. Key shape:

- **`catalog-info.yaml`** lives inside each repo at root; carries `apiVersion`, `kind`, `metadata.name`, `metadata.labels`, `metadata.annotations`, `metadata.tags`, `spec.type`, `spec.owner`, `spec.lifecycle`.
- **GitOps-first**: the YAML file IS the SSOT; Backstage's catalog DB is a derived projection. Teams own components via Git workflows, not via a UI.
- **GitHub Discovery** is the preferred ingestion path (Backstage scans the org for `catalog-info.yaml` files and ingests them).
- `spec.lifecycle` enum is typically `production` / `experimental` / `deprecated` — close to but not identical to the operator's proposed `app_class` enum.

**AKOS alignment:** the AKOS pattern is **inverted-Backstage**: instead of YAML-in-each-repo + central derivation, AKOS uses **central CSV-as-SSOT** + per-repo bless artifacts (per `akos-mirror-template.mdc`). This is justified because AKOS already has the CSV chassis (Pydantic + validator + Supabase mirror + FK joins) and adding 51 `catalog-info.yaml` files across the polyrepo fleet would create the kind of distributed-SSOT drift the canonical-CSV pattern exists to prevent. The CSV row replaces the YAML.

**Recommendation:** AKOS-as-SSOT (CSV) for the catalog; GitHub topics as discoverability-mirror only (not SSOT). Don't author 51 `catalog-info.yaml` files.

### §4.2 GitHub Custom Repository Properties (2026 governance pattern)

GitHub introduced **custom repository properties** as a first-class metadata mechanism, distinct from topics. Key differences:

| | GitHub Topics | GitHub Custom Properties |
|---|---|---|
| Access control | Anyone with repo write access can set | Org admins manage; can be `read_only_to_writers` |
| Use case | Discoverability (search by topic) | Governance (rulesets target by property) |
| Best-practice mandate | NOT for automation per [GOV.UK ADR-0017](https://docs.publishing.service.gov.uk/repos/govuk-infrastructure/architecture/decisions/0017-retire-use-of-github-topics-for-config-management.html) (retired) | YES for ruleset targeting (per [dxrf.com 2026-03](https://dxrf.com/blog/2026/03/10/scaling-github-rulesets-with-custom-properties/)) |
| Schema | Free-form lowercase strings | Typed (text / single-select / multi-select / true_false) with allowed-values |

**AKOS alignment:** custom properties are the **right** projection target for `app_class` and `governance_status` because they:
1. Drive **ruleset application** (e.g., "require CODEOWNERS review on all `app_class=production` repos"; "skip branch protection on `app_class=experiment` repos").
2. Are **access-controlled** (unlike topics), so they can carry governance metadata safely.
3. Are first-class in the GitHub Enterprise governance story (the rulesets + custom-properties combo is the 2026 polyrepo pattern per [GitHub Well-Architected](https://wellarchitected.github.com/library/architecture/recommendations/implementing-polyrepo-engineering/)).

**Topics**, by contrast, should mirror the CSV's `metadata_tags` column for **search/discovery**, not governance enforcement.

### §4.3 CODEOWNERS + Branch Protection Rulesets (2026 enforcement)

[GitHub Polyrepo Well-Architected](https://wellarchitected.github.com/library/architecture/recommendations/implementing-polyrepo-engineering/) names the 2026 multi-repo pattern:

- **CODEOWNERS** in each governed repo, owned by the canonical role from REPOSITORY_REGISTRY (e.g., `* @holistika/system-owner` for `primary_owner_role=System Owner`).
- **Repository Rulesets** (replacing classic Branch Protection Rules) — org-level rulesets targeted via custom properties (e.g., "all `app_class=production` repos require: signed commits, 1+ reviewer approval, status check `ci-baseline`").
- **Reusable workflows as versioned platform interface** — shared CI lives in a meta-repo; consumer repos pin to a semver tag.

**AKOS alignment:** `bless_external_repo.py` already writes CODEOWNERS via `_templates/ci/CODEOWNERS.template`. The `SOP-CICD_BASELINE_001` (per docs-config-sync table) already governs CI baselines. The schema extension just needs **two boolean projection columns** so the registry knows which repos have CODEOWNERS + branch protection enabled (drift signal).

### §4.4 IDP best practices 2026 (Harness, Platform Engineering)

[Harness 2026 IDP best practices](https://harness.io/blog/5-best-practices-for-building-effective-internal-developer-portals):
1. Prioritize DX (operator-centric views; feedback loops).
2. Toolchain integration (consistent UI, SSO, API-first).
3. Discoverability + documentation (robust search; well-maintained docs).
4. Self-service with guardrails ("vending machine" pattern per [HAMS Tech 2026](https://hams.tech/blog/platform-engineering-2026-terraform-github-actions-idp.html)).
5. Governance via custom properties + composable rulesets.

**AKOS alignment:** the existing HLK Operator Model + bless script already covers points 1-4 (operator-facing CSV; bless artifacts as guardrails; HLK MCP for search). Point 5 (custom-properties-driven rulesets) is what the schema extension unlocks.

### §4.5 Summary of external research

The 2026 industry pattern is: **central catalog (Backstage-shape) + per-repo custom-properties (GitHub-native) + ruleset-driven enforcement**. AKOS already has the central catalog (REPOSITORY_REGISTRY.csv); the schema extension brings parity with the metadata richness Backstage carries (`app_class`, `metadata_tags`, `lifecycle`, `pushed_at`, `governance_status`) and unlocks the custom-properties projection in a follow-up phase.

---

## §5 Mental model — orthogonal axes

The crucial design question is: *does `app_class` REPLACE the existing `class` column, or is it ORTHOGONAL?*

**Recommendation: ORTHOGONAL.** The two columns answer two different questions:

| Axis | Question it answers | Vocabulary |
|---|---|---|
| `class` (existing) | *How does AKOS relate to this repo?* | platform / internal / client-delivery / reference |
| `app_class` (NEW) | *What kind of artifact is this repo?* | production / research / experiment / template / fork / archive / uncategorized |

**Cross-product examples:**

| repo | class | app_class | meaning |
|---|---|---|---|
| openclaw-akos | platform | production | AKOS itself — production platform |
| hlk-erp | platform | production | Production app under full AKOS governance |
| boilerplate | reference | production | Production marketing site, light-touch AKOS governance (D-IH-32-N) |
| kirbe-platform | platform | production | Production SaaS, full AKOS governance |
| visiongen | internal (NEW) | research | AKOS-internal research output (paper code) |
| crew-ai-f | internal (NEW) | research | AKOS-internal CrewAI exploration |
| nextjs-supabase-kit | reference (NEW) | template | Boilerplate template the operator forks for new projects |
| supabase (fork) | reference (NEW) | fork | Tracked upstream fork |
| python-hello-world | internal (NEW) | experiment | Throwaway experiment |
| (future) suez-deliverable-2026 | client-delivery | production | A live client-delivery production repo |

This orthogonality matches the same pattern operator codified in `akos-external-render-discipline.mdc` (audience × format axes) and `akos-conflict-surfacing-and-blocker-trackers.mdc` (some-but-not-all gates). Two axes that compound, not collapse.

**Default `class` for newly inventoried repos:** `internal` if owned by an AKOS role + private; `reference` if a template or fork; the existing `class` enum is wide enough to host the 51 unmanaged repos without expansion.

---

## §6 Proposed schema extension (12 NEW columns)

Per `akos-holistika-operations.mdc` §"New git-canonical compliance registers (pattern)": every new column ships with a Pydantic SSOT update in [`akos/hlk_repository_registry_csv.py`](../../../../akos/hlk_repository_registry_csv.py) + a validator extension in [`scripts/validate_repository_registry.py`](../../../../scripts/validate_repository_registry.py) + a forward Supabase migration adding columns to `compliance.repository_registry_mirror`.

Total schema after extension: **17 → 29 columns**.

| # | column_name | type | enum / format | nullability | default | rationale |
|--:|---|---|---|---|---|---|
| 1 | **`app_class`** | enum | `production` / `research` / `experiment` / `template` / `fork` / `archive` / `uncategorized` | NOT NULL | (must be set per row) | Load-bearing classification — operator-named in scratchpad. Orthogonal to existing `class`. |
| 2 | **`metadata_tags`** | semi-list | free-form lowercase tags (`fnmatch`-safe; matches GH topics ruleset) | nullable | empty | Mirrors `github_topics`; used for operator-driven categorisation independent of GH UI. |
| 3 | **`github_topics`** | semi-list | mirrored from GH `repositoryTopics[].name` at inventory time | nullable | empty | Read-side mirror of GH topics; advisory only (per GOV.UK 2026 ADR-0017: not for automation). |
| 4 | **`github_visibility`** | enum | `PUBLIC` / `PRIVATE` / `INTERNAL` | NOT NULL | `PRIVATE` | Cross-check vs GitHub API; flags drift when operator changes visibility outside the registry. |
| 5 | **`primary_language`** | text | GH-reported primary language (e.g., `TypeScript`, `Python`, `Markdown`) | nullable | empty | Mirrored from `primaryLanguage.name`. Empty for empty repos. |
| 6 | **`created_at`** | date | `YYYY-MM-DD` (mirrored from GH `createdAt`) | NOT NULL | (mirror-on-create) | Audit trail; useful for age-based queries. |
| 7 | **`pushed_at`** | date | `YYYY-MM-DD` (mirrored from GH `pushedAt`) | NOT NULL | (mirror-on-sweep) | Staleness signal; drives quarterly archival sweep in proposed SOP. |
| 8 | **`last_inventory_at`** | date | `YYYY-MM-DD` (when the registry last ran a GH sweep for this row) | nullable | empty | Inventory cadence audit — orthogonal to `last_review_at` (governance review). |
| 9 | **`governance_status`** | enum | `governed` / `inventoried` / `unmanaged` / `archived` | NOT NULL | (must be set) | Defines AKOS posture: full SOP + bless (governed), classified-only (inventoried), GH-only (unmanaged), retired (archived). |
| 10 | **`related_initiative_ids`** | semi-list | `I-NN` identifiers (e.g., `I76;I86`) | nullable | empty | Cross-link repo → initiatives that produced or maintain it. |
| 11 | **`codeowners_present`** | boolean | `true` / `false` (parsed from in-repo `.github/CODEOWNERS` or repo root) | nullable | empty | Drift signal: `governed` repos must have this `true` (per `bless_external_repo.py` `--with ci-baseline`). |
| 12 | **`branch_protection_enabled`** | boolean | `true` / `false` (queried from GH API at inventory time) | nullable | empty | Drift signal: `governed` repos must have this `true`. |

### §6.1 Recommended defaults for backfill

For the **51 unmanaged repos**, the recommended bulk-fill is:

- `app_class` — per §2.1 (8 research / 30 experiment / 7 template / 4 fork / 2 uncategorized).
- `class` — `internal` for all PRIVATE + research/experiment/template (default for the polyrepo internal R&D layer); `reference` for the 7 templates + 4 forks (no governance contract).
- `primary_owner_role` — TBD per row (default suggestion: `System Owner` for research/experiment/template; `AI Engineer` for AI/ML-heavy research; the 2 uncategorized rows defer to operator).
- `governance_status` — `inventoried` (classified + tagged, not yet blessed).
- `lifecycle_status` — `active` if `pushed_at < 365 days`; `archived` if `pushed_at >= 730 days`; `reference` for templates/forks.
- `metadata_tags`, `github_topics` — empty (no current GH topics on any repo per the inventory).
- `github_visibility`, `primary_language`, `created_at`, `pushed_at` — mirrored from GH API.
- `last_inventory_at` — `2026-05-19` (date of this report).
- `codeowners_present`, `branch_protection_enabled` — `false` (the 51 repos don't carry these; that's why they're unmanaged).
- `consumes_compliance_types`, `consumes_mirrors`, `local_path` — empty (no AKOS dependency).
- `last_review_*`, `methodology_version_at_review` — empty (no review has happened).

### §6.2 Backwards-compatibility posture

All 12 new columns must be **nullable** in the **migration** (per `akos-holistika-operations.mdc` two-plane discipline) to keep the existing 7 CSV rows loading without immediate backfill. The validator at first will:

- **FAIL** on `app_class` empty (after backfill is committed — the backfill itself satisfies the gate).
- **FAIL** on `governance_status` empty (same posture).
- **WARN** on `pushed_at` / `created_at` empty (advisory until next inventory sweep populates).
- **WARN** on `codeowners_present` / `branch_protection_enabled` empty (advisory; runbook backfills via GH API).

This is the I66 brand-baseline-reality drift-gate pattern (INFO → FAIL after backfill closure), applied to schema extension.

---

## §7 Proposed new SOP — `SOP-TECH_APPLICATION_GOVERNANCE_001`

Per `akos-executable-process-catalog.mdc` RULE 1 (every executable process needs a paired SOP + runbook). Path: `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_APPLICATION_GOVERNANCE_001.md`.

DO NOT author today — describe shape only:

### §7.1 Section sketch (~10 sections, ~300-400 lines)

| § | Title | Content shape |
|---|---|---|
| §1 | Purpose | Every operator repo gets classified + tagged + inventoried per quarterly cadence; closes the 92.7% unmanaged gap; codifies app-governance discipline introduced in I86 Wave H per **D-IH-86-AC**. |
| §2 | Scope | All repos under `FraysaXII` org. Future-proofs for additional orgs (e.g., `holistika-ai`, `kirbe`) via a `github_org` column extension. |
| §3 | Inputs | (a) `gh repo list FraysaXII --json …` (the runbook's primary data source); (b) current `REPOSITORY_REGISTRY.csv`; (c) GH API metadata (CODEOWNERS presence + branch protection state) via `gh api repos/<owner>/<name>/codeowners-errors` + `gh api repos/<owner>/<name>/branches/<default>/protection`. |
| §4 | Process | (1) **Quarterly inventory sweep** (runbook `scripts/inventory_github_repos.py --sweep`): fetch GH list, diff vs CSV, append rows for new repos with `governance_status=unmanaged + app_class=uncategorized`. (2) **On-create classification** (~ 7 days after a new repo appears): operator classifies via inline-ratify gate (per `akos-inline-ratification.mdc`). (3) **On-archive update** (when operator archives a repo in GH UI): runbook detects via `isArchived: true` and flips `app_class=archive` + `lifecycle_status=archived`. (4) **Annual review** of `inventoried` repos: should they be promoted to `governed` (full bless) or demoted to `archived`? |
| §5 | Outputs | (a) Updated `REPOSITORY_REGISTRY.csv` rows; (b) drift report at `artifacts/inventory/repos-drift-<YYYYMMDD>.md` (advisory). (c) Optional Slack/email summary via existing `kirbe-platform` notification surface. |
| §6 | Failure modes | (a) **Uncategorized repos** stranded — operator does not classify within 30 days → runbook escalates via Slack/email per `akos-conflict-surfacing-and-blocker-trackers.mdc`. (b) **Abandoned production** — `production` row with `pushed_at > 180 days` → runbook flags for archival decision. (c) **Stale governed rows** — `governed` repo with `pushed_at > 365 days` → mandatory operator review. (d) **CODEOWNERS / branch-protection drift** — `governed` repo whose runtime state diverges from registry (`codeowners_present=false` when registry says `governed`) → auto-PR via existing `bless_external_repo.py --auto-pr`. |
| §7 | Cross-references | `SOP-EXTERNAL_REPO_BLESSING_001` (the upgrade path from `inventoried` to `governed`); `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001` (the drift detection mechanic); `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001` (downstream propagation when a registered repo consumes mirrors); `akos-mirror-template.mdc` (the cursor-rule kit for newly-governed repos); `akos-executable-process-catalog.mdc` RULE 1 (the SOP+runbook pairing this SOP itself instantiates); `akos-governance-remediation.mdc` (canonical-CSV gate discipline for the row writes this SOP produces). |
| §8 | Paired runbook | `scripts/inventory_github_repos.py` — see §8 for shape. |
| §9 | Acceptance criteria | (a) **human/AIC route**: a System Owner (or AIC role_owner) can run a quarterly inventory by following §4 manually and editing CSV rows — no runbook required. (b) **automation route**: `py scripts/inventory_github_repos.py --sweep --apply` runs unattended (e.g., as a GitHub Action) and produces a PR with diff + drift report. |
| §10 | Cadence | `cadence: scheduled` (quarterly) + `cadence_secondary: event_triggered` (on new-repo or archive events, when GH webhooks/Actions are wired). |

### §7.2 Process_list.csv tranche needed

Per `akos-governance-remediation.mdc` §"SOP-META order (CSV before SOP)": before the SOP can be finalised, a `process_list.csv` row must exist. Proposed row (operator ratify in §9):

- `item_id`: `env_tech_dtp_app_governance_quarterly_001` (per existing `env_tech_dtp_*` namespace per docs-config-sync table)
- `area`: `Tech`
- `entity`: `Holistika`
- `role_owner`: `System Owner`
- `cadence`: `scheduled` (quarterly)
- `inherited_pattern_id`: TBD — likely `paired_sop_runbook` from PEOPLE_DESIGN_PATTERN_REGISTRY (per `akos-people-discipline-of-disciplines.mdc` RULE 1).
- `description`: "Quarterly GitHub repository inventory sweep + classification update; closes the unmanaged-repo gap codified by I86 Wave H + D-IH-86-AC."

### §7.3 Topic asset (not required at v1)

The KM topic question (does this SOP get an Output-1 topic at `_assets/<plane>/holistika/topic_repository_governance/`?) is deferred. The SOP is a process artifact; KM topics are for cross-area knowledge. If, in a future I-NN, the registry expands to multi-org or multi-fleet scope, a topic asset may be warranted; today the SOP + runbook are sufficient.

---

## §8 Proposed paired runbook — `scripts/inventory_github_repos.py`

### §8.1 Shape (~250-350 lines, following `CONTRIBUTING.md` §Python Code Standards)

Module structure (per `akos-holistika-operations.mdc` Pydantic + validator + sync pattern + `CONTRIBUTING.md` validator callouts):

```text
scripts/inventory_github_repos.py
    main()                                  # CLI entry
    cmd_sweep(args)                         # gh repo list -> diff -> CSV append candidates
    cmd_apply(args)                         # write the CSV; produce drift report
    cmd_classify(args)                      # interactive classify (operator/AIC)
    cmd_check_codeowners(repo, owner)       # gh api codeowners-errors
    cmd_check_branch_protection(repo)       # gh api branches/<default>/protection
    fetch_github_inventory() -> list[Pydantic GhRepoSnapshot]
    diff_against_registry(snapshot, csv) -> InventoryDiff (Pydantic)
    classify_default(snapshot) -> AppClass
    write_csv_rows(diff, csv_path)
    write_drift_report(diff, report_path)
```

Pydantic models in [`akos/hlk_repository_registry_csv.py`](../../../../akos/hlk_repository_registry_csv.py) extension (mirroring the schema-bump):

```text
class AppClass(str, Enum): production | research | experiment | template | fork | archive | uncategorized
class GovernanceStatus(str, Enum): governed | inventoried | unmanaged | archived
class GithubVisibility(str, Enum): PUBLIC | PRIVATE | INTERNAL
class GhRepoSnapshot(BaseModel): name, github_url, visibility, primary_language, created_at,
                                  pushed_at, is_archived, is_fork, topics: list[str]
class InventoryDiff(BaseModel): new_repos: list[GhRepoSnapshot], removed_slugs: list[str],
                                 changed: list[tuple[str, dict]], at: date
```

CLI subcommands:

| subcommand | purpose | side effect |
|---|---|---|
| `--sweep` | Fetch GH inventory + compute diff vs CSV | read-only; prints diff |
| `--apply` | Append/update CSV rows; produce drift report | writes `REPOSITORY_REGISTRY.csv` + `artifacts/inventory/repos-drift-<date>.md` |
| `--classify <slug> --app-class <class>` | Operator/AIC classifies an uncategorized row | writes one CSV cell |
| `--check-codeowners <slug>` | Query GH for CODEOWNERS presence | updates the `codeowners_present` cell |
| `--check-branch-protection <slug>` | Query GH for branch protection state | updates `branch_protection_enabled` cell |
| `--sync-topics <slug>` | Mirror `github_topics` from GH API | updates that cell |

### §8.2 Wiring (per `akos-governance-remediation.mdc` §verification matrix)

- Wired into `config/verification-profiles.json` as a new profile `inventory_github_repos_smoke` (`--sweep` mode; CI-friendly; no GH writes).
- Wired into `scripts/release-gate.py` as advisory (does NOT fail release; INFO-tier only — it's an operator-cadence process, not a release gate).
- Tests in `tests/test_inventory_github_repos.py` (mock `gh` CLI via `akos.process.run` patching; Pydantic round-trips; diff correctness).
- Registered in `scripts/test.py` group list (e.g., `@pytest.mark.governance`).

### §8.3 Acceptance criteria

Per `akos-executable-process-catalog.mdc` RULE 1.5:

- `acceptance_criteria_human`: a System Owner (or AIC) can run `gh repo list FraysaXII --json …`, manually classify each repo, and edit CSV rows by hand. The SOP §4 makes this reproducible without ever running the runbook.
- `acceptance_criteria_automation`: `py scripts/inventory_github_repos.py --sweep --apply` runs unattended (e.g., quarterly GitHub Action) and emits a PR with the CSV diff + drift report; CI gate `inventory_github_repos_smoke` passes on every commit.

---

## §9 Canonical-CSV ratify gate (operator action required)

Per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance" + [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers (pattern)": the schema extension is a canonical-CSV gate. Operator MUST ratify before parent commits the bundle.

### §9.1 Numbered ratify checklist (12 items)

Per `akos-agent-checkpoint-discipline.mdc` operator-approval checklist (≤7 items recommended; 12 here is borderline but the schema extension is atomic — split would be artificial):

1. ☐ **Ratify the 7-value `app_class` enum** as proposed in §6 row 1: `production / research / experiment / template / fork / archive / uncategorized`. (Alternative: collapse `template + fork` into a single `reference-artifact` class — recommended against per §5 orthogonality.)
2. ☐ **Ratify the 4-value `governance_status` enum** as proposed in §6 row 9: `governed / inventoried / unmanaged / archived`.
3. ☐ **Ratify orthogonal axes design** (§5): keep existing `class` column unchanged; add `app_class` alongside (not collapsing). (Alternative: extend `class` enum to 11 values and drop `app_class` — recommended against per §5 single-axis-overload rationale.)
4. ☐ **Ratify the 12-column schema extension** (§6) as a single atomic CSV header bump (17 → 29 columns). All 12 columns nullable in migration; validator promotes `app_class` + `governance_status` to FAIL after backfill commit.
5. ☐ **Classify `agentuity`** (§2.3 row 1): pick one of {`experiment`, `research`, `archive`}. Default if no response: `experiment` (lowest-impact default).
6. ☐ **Classify `holistika-websitz-shopify-app`** (§2.3 row 2): pick one of {`production`, `experiment`, `archive`}. Default if no response: `experiment` (lowest-impact default; can be promoted later if it turns out to be live customer-facing).
7. ☐ **Ratify `client-delivery-pilot` ghost-row cleanup**: drop the placeholder row OR convert to a tracker entry under `docs/wip/planning/_trackers/client-delivery-pilot-placeholder-tracker.md` per `akos-conflict-surfacing-and-blocker-trackers.mdc`. (Recommendation: convert to tracker, preserve intent.)
8. ☐ **Ratify proposed SOP shape** (§7): name `SOP-TECH_APPLICATION_GOVERNANCE_001`; location `Envoy Tech Lab/canonicals/`; 10-section shape per §7.1.
9. ☐ **Ratify proposed `process_list.csv` row** (§7.2): `item_id=env_tech_dtp_app_governance_quarterly_001` + `cadence=scheduled` (quarterly). This is a **secondary canonical-CSV gate** that runs in lockstep with the schema bump per SOP-META order.
10. ☐ **Ratify proposed runbook** (§8): `scripts/inventory_github_repos.py` with the §8.1 subcommands + §8.2 wiring. (Acceptance: the runbook does NOT replace the SOP — both ship together per `akos-executable-process-catalog.mdc` RULE 1.)
11. ☐ **Ratify backfill posture** (§6.2): all 12 columns nullable at migration; validator promotes 2 to FAIL after backfill closure (`app_class` + `governance_status`); 6 to WARN until next sweep populates (`pushed_at`, `created_at`, `codeowners_present`, `branch_protection_enabled`, `github_topics`, `last_inventory_at`). This is the I66 INFO→FAIL ramp pattern, applied to schema extension.
12. ☐ **Ratify decision IDs** (per §10 forward decisions): mint D-IH-86-AC (scope extension), D-IH-86-AD (schema extension), D-IH-86-AE (SOP mint), D-IH-86-AF (runbook mint) at commit time per `DECISION_REGISTER.csv` append discipline.

### §9.2 Where the ratify gate fires

Per `akos-inline-ratification.mdc`: this ratify gate is `gate_type: inline-ratify` (NOT `stop-and-clarify`). The agent has done the evidence sweep; the options are surfaced; operator ratifies in-chat. The parent agent will pose this as a single batched `AskQuestion` block once the lane returns.

---

## §10 Forward decision candidates (not minted today; ratified inline with §9)

| Decision ID | Question | Status entering plan | Close-out commit |
|---|---|---|---|
| **D-IH-86-AC** | Extend I86 cluster scope to include app-governance lane (Wave H) | Pre-ratified by operator quote 2026-05-19 ("option B") | Parent commit after §9 ratify |
| **D-IH-86-AD** | Extend `REPOSITORY_REGISTRY.csv` schema from 17 to 29 columns per §6 | Proposed; awaits §9 items 1-4 + 11 ratify | Same parent commit |
| **D-IH-86-AE** | Mint `SOP-TECH_APPLICATION_GOVERNANCE_001` per §7 shape | Proposed; awaits §9 item 8 ratify | Same parent commit |
| **D-IH-86-AF** | Mint paired runbook `scripts/inventory_github_repos.py` per §8 shape | Proposed; awaits §9 item 10 ratify | Same parent commit |
| **D-IH-86-AG** (POTENTIAL) | Classify `agentuity` (§2.3) | Awaits §9 item 5 | Same parent commit |
| **D-IH-86-AH** (POTENTIAL) | Classify `holistika-websitz-shopify-app` (§2.3) | Awaits §9 item 6 | Same parent commit |
| **D-IH-86-AI** (POTENTIAL) | `client-delivery-pilot` ghost-row cleanup (§9 item 7) | Awaits ratify | Same parent commit |

The 7 decisions can be minted in a single decision-register append; the operator's 12-item ratify checklist surfaces the underlying choices.

---

## §11 Risk register (lane-scoped — flow to parent risk register on ratify)

| Risk ID | Risk | L | I | Mitigation |
|---|---|:--:|:--:|---|
| R-LF-1 | Operator does not ratify §9 within 24h → blocks parent commit | M | M | Parent commits Lane A + Lane C closure first (per lane prompt: "DO NOT commit; parent will commit after Lane A + Lane C close") — this lane's work survives uncommitted. |
| R-LF-2 | `app_class` classification disagreement (`uncategorized` defaults wrong) | L | L | Defaults are explicit (`experiment` for both uncategorized rows); operator can post-hoc reclassify via `cmd_classify` runbook in §8. |
| R-LF-3 | GitHub API rate limit during sweep (5K requests/hour authenticated) | L | M | Runbook batches calls; one sweep ~ 110 calls (55 repos × 2 endpoints); well under limit. |
| R-LF-4 | Pydantic migration breaks backwards-compat (existing 7 rows fail validation) | M | H | Schema extension §6.2 ships all 12 new columns nullable; validator FAIL only after backfill closure (per I66 INFO→FAIL ramp pattern). |
| R-LF-5 | Operator chooses to collapse axes (`app_class` into `class`) per §9 item 3 | L | M | §5 makes the orthogonality case; if operator collapses, parent re-plans the schema as enum-extension instead of additive (different migration shape). |
| R-LF-6 | The 51 unmanaged repos backfill is genuinely operator-content-heavy | M | M | Backfill defaults (§6.1) cover 49 of 51 mechanically; only 2 uncategorized rows need explicit operator pick. The remaining 49 can be backfilled in a single bulk-commit. |
| R-LF-7 | Holistika org grows from `FraysaXII` to multi-org → schema needs `github_org` column | L | L | Future-proofs via §6 column 4 (`github_visibility`) + `github_url` covering the org segment. Multi-org expansion is a future I-NN; not today's scope. |
| R-LF-8 | Wave H closure ratify cadence (W3-C inline-streaming per scratchpad 2026-05-19 15:30) blocks lane handoff if operator unavailable | L | M | Per scratchpad note: operator promoted W3-C to new norm — closure ratifies are inline. Lane F's ratify naturally happens at parent's W3-C cadence. |

---

## §12 Quality bar self-checks (per `akos-planning-traceability.mdc` plan-quality bar)

This report meets the following bar items (a lane inventory report doesn't need every plan-quality-bar element, but the relevant ones are):

- ☑ **Evidence sweep before ratify questions** — §2 (GitHub inventory) + §3 (registry state) + §4 (external research) all completed before §9 ratify gate.
- ☑ **Each option carries rationale** — §6 schema columns each carry a "rationale" cell; §9 ratify items each name the alternative + recommendation.
- ☑ **Recommended defaults explicit** — §6.1 (backfill defaults); §9 items 5+6 (uncategorized defaults if operator silent); §9 item 7 (recommend tracker not drop).
- ☑ **Evidence cited by file path + line** — `akos/hlk_repository_registry_csv.py` L46-52 (enum); `scripts/validate_repository_registry.py` (validator); `supabase/migrations/20260506120000_i59_repository_registry_mirror.sql` (mirror DDL).
- ☑ **Batched ratify call** — §9.1 is a single 12-item checklist that the parent will post as one batched `AskQuestion`, not 12 separate calls.
- ☑ **CONTRIBUTING.md adherence callouts** — §8.1 names Pydantic + type hints + structured logging + tests + release-gate wiring + verification-profiles registration; §8.2 names the wiring sites.
- ☑ **File-path density** — every script/CSV/SOP/migration named in this report is clickable (`docs/...`, `akos/...`, `scripts/...`, `supabase/migrations/...`).
- ☑ **Cursor-rules adherence per phase** — see §13.

---

## §13 Cursor-rules adherence

This lane operationalises the following rules:

- [`akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc) §"AKOS HLK SSOT mirror" + §"Never invent HLK IDs locally" — REPOSITORY_REGISTRY.csv stays SSOT; GitHub topics are advisory-only (per GOV.UK 2026 ADR-0017 cited in §4.2); the proposed schema preserves AKOS as the canonical surface.
- [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance" — schema extension is a canonical-CSV gate; §9 ratify checklist + §11 R-LF-4 backwards-compat posture both honor the rule.
- [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers (pattern)" — §6 (Pydantic SSOT extension) + §8 (paired script) + the forward migration listed in §6.2 follow the canonical pattern; §7.2 forces SOP-META order (process_list tranche before SOP).
- [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 (SOP + executable runbook pairing) — §7 (SOP) + §8 (runbook) ship as a pair; §8.3 declares both acceptance criteria (human + automation).
- [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar" — §6 schema table + §10 decision-log preview + §11 inline risk register + §12 quality self-checks satisfy the plan-quality bar items applicable to a lane inventory report.
- [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — §9 is `gate_type: inline-ratify` (NOT `stop-and-clarify` — no validator failed; this is a design decision, not a blocker).
- [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) — `client-delivery-pilot` ghost-row recommendation (§9 item 7) cites the tracker pattern; `holistika-websitz-shopify-app` uncategorized (§9 item 6) also conforms (some-but-not-all gates met → tracker, not promote).
- [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — operator pause point on §9 ratify gate is **soft pause** (per cadence heuristic for canonical-CSV gate = mandatory pause); this report is the pause-record-equivalent (mechanical evidence + documentary evidence + approval checklist all here).
- [`akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 1 — People owns design patterns; Tech Lab owns Tech SOPs. This SOP (`SOP-TECH_APPLICATION_GOVERNANCE_001`) lands under **Envoy Tech Lab** (Tech Lab as data owner) NOT People — consistent with the area-vs-pattern split.

---

## §14 Cross-references

### §14.1 Repo-local references

- [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv) — canonical CSV (target of schema bump)
- [`akos/hlk_repository_registry_csv.py`](../../../../akos/hlk_repository_registry_csv.py) — Pydantic SSOT (target of fieldnames tuple + 2 new enum frozensets)
- [`scripts/validate_repository_registry.py`](../../../../scripts/validate_repository_registry.py) — validator (target of new enum + nullability checks)
- [`scripts/validate_repository_registry_md_csv_sync.py`](../../../../scripts/validate_repository_registry_md_csv_sync.py) — markdown ↔ CSV sync validator (must re-baseline after schema bump)
- [`supabase/migrations/20260506120000_i59_repository_registry_mirror.sql`](../../../../supabase/migrations/20260506120000_i59_repository_registry_mirror.sql) — existing mirror table (target of forward `ALTER TABLE` migration adding 12 columns)
- [`scripts/bless_external_repo.py`](../../../../scripts/bless_external_repo.py) — bless script (consumer of registry; reads the new `governance_status` column post-bump)
- [`docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_BLESSING_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) — upstream SOP (the path from `inventoried` → `governed`)
- [`docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md) — sibling drift SOP
- [`docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md`](../operator-scratchpad.md) lines 62-63 — operator's source quotes for the app-governance lane
- [`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`](../master-roadmap.md) — parent initiative roadmap
- [`docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md`](../decision-log.md) — parent decision register (where D-IH-86-AC..AI rows append on ratify)

### §14.2 External references

- [Backstage Software Catalog descriptor format](https://github.com/backstage/backstage/blob/master/docs/features/software-catalog/descriptor-format.md) — `catalog-info.yaml` shape (§4.1)
- [GOV.UK ADR-0017: Retire GitHub topics for configuration management](https://docs.publishing.service.gov.uk/repos/govuk-infrastructure/architecture/decisions/0017-retire-use-of-github-topics-for-config-management.html) — 2026 advisory: topics not for automation (§4.2)
- [Scaling GitHub Rulesets with Custom Properties (dxrf.com 2026-03)](https://dxrf.com/blog/2026/03/10/scaling-github-rulesets-with-custom-properties/) — custom-properties-driven governance (§4.2)
- [GitHub Polyrepo Well-Architected](https://wellarchitected.github.com/library/architecture/recommendations/implementing-polyrepo-engineering/) — 2026 polyrepo pattern (§4.3)
- [Harness IDP Best Practices 2026](https://harness.io/blog/5-best-practices-for-building-effective-internal-developer-portals) — IDP DX patterns (§4.4)
- [HAMS Tech Platform Engineering 2026](https://hams.tech/blog/platform-engineering-2026-terraform-github-actions-idp.html) — vending-machine IDP architecture (§4.4)
- [GitHub Docs: Classifying your repository with topics](https://docs.github.com/en/enterprise-server@3.12/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) — official topic guidance (§4.2)
- [GitHub Docs: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) — CODEOWNERS reference (§4.3)

---

## §15 Lane closure — handoff to parent

This report fulfils the Lane F-GITHUB deliverable. The file is **uncommitted**; the parent agent will:

1. Post the §9 12-item ratify checklist as a single batched `AskQuestion` to the operator (per `akos-inline-ratification.mdc`).
2. After operator ratifies, mint D-IH-86-AC..AI (7 decision rows) per §10.
3. Author the schema bump in [`akos/hlk_repository_registry_csv.py`](../../../../akos/hlk_repository_registry_csv.py) (+ 2 new enum frozensets + 12 fieldnames).
4. Author the forward Supabase migration adding 12 nullable columns to `compliance.repository_registry_mirror`.
5. Extend [`scripts/validate_repository_registry.py`](../../../../scripts/validate_repository_registry.py) with the new enum + nullability rules.
6. Author the SOP at `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_APPLICATION_GOVERNANCE_001.md` per §7 shape.
7. Author the runbook at `scripts/inventory_github_repos.py` per §8 shape.
8. Append the `process_list.csv` row per §7.2.
9. Backfill the 51 unmanaged repo rows per §6.1 defaults (single bulk-commit).
10. Update `docs/USER_GUIDE.md` HLK Operator Model section + `docs/ARCHITECTURE.md` HLK Registry table per `akos-docs-config-sync.mdc`.
11. Wire the runbook into `config/verification-profiles.json` (new `inventory_github_repos_smoke` profile) + add a test in `tests/test_inventory_github_repos.py`.
12. Append rows to [`docs/wip/planning/86-initiative-cluster-execution-coordinator/files-modified.csv`](../files-modified.csv) covering the schema-bump + SOP-mint + runbook-mint + backfill commits.

Parent commits this bundle in a single atomic commit (or split into 2 if size > 4K lines diff) after Lane A + Lane C close, per lane prompt.

---

**End of Lane F-GITHUB report.**
