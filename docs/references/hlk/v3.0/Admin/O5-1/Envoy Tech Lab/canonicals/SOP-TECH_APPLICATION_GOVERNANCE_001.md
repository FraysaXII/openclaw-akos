---
intellectual_kind: sop
sharing_label: internal_only
sop_id: SOP-TECH_APPLICATION_GOVERNANCE_001
role_owner: System Owner
co_owner_role: PMO
area: Tech
entity: Holistika
audience: J-OP
access_level: 3
status: active
added_at: 2026-05-19
last_review_at: 2026-05-19
last_review_by: Founder/CEO
methodology_version_at_review: v3.1
last_review_decision_id: D-IH-86-AE
linked_decisions:
  - D-IH-86-AC
  - D-IH-86-AD
  - D-IH-86-AE
  - D-IH-86-AF
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_BLESSING_001.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md
paired_runbook: scripts/inventory_github_repos.py
governance_rules:
  - akos-executable-process-catalog.mdc
  - akos-holistika-operations.mdc
  - akos-governance-remediation.mdc
language: en
---

# SOP-TECH_APPLICATION_GOVERNANCE_001 — Application Governance

Inventory + classify + monitor every repository under the operator's GitHub org
so the fleet is governed by category instead of by name-recognition. Pairs with
the runbook [`scripts/inventory_github_repos.py`](../../../../../../../../scripts/inventory_github_repos.py)
per [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1 (paired SOP + executable runbook).

## §1 Purpose

Holistika's polyrepo footprint has grown to **55 repositories** under the
`FraysaXII` org, of which only **4 are production** (`openclaw-akos`, `hlk-erp`,
`boilerplate`, `kirbe`); the remaining **51 are research / experiment / template /
fork / uncategorized**. Lane F-GITHUB report (2026-05-19) confirmed that
**92.7% of the GitHub footprint is currently unmanaged** by
[`REPOSITORY_REGISTRY.csv`](../../../../People/Compliance/canonicals/REPOSITORY_REGISTRY.csv).

This SOP codifies the discipline that closes that gap: every repository in the
org gets classified (`app_class`), tagged (`metadata_tags`), inventoried
(`last_inventory_at`), and assigned a governance posture (`governance_status`).
Production repos receive full [`SOP-EXTERNAL_REPO_BLESSING_001`](../External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md)
treatment; research / experiment / template / fork repos receive light-touch
inventory only.

Drives the I86 Wave H schema extension (17 → 29 columns) per **D-IH-86-AC**
(scope) + **D-IH-86-AD** (12-column extension). Mints the cadence that prevents
the gap from re-opening.

## §2 Scope

All repositories under the `FraysaXII` GitHub organisation (current scope; the
schema preserves a hook for a future `github_org` column when Holistika expands
to a second org like `holistika-ai` or `kirbe`).

| Governance posture | `app_class` typical values | What this SOP requires |
|---|---|---|
| **`governed`** | `production` | Full bless contract — CODEOWNERS + branch protection + AKOS mirror rule + EXTERNAL_REPO_CONTRACT.md. Tracked by [`SOP-EXTERNAL_REPO_BLESSING_001`](../External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) + [`SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001`](../External%20Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md). |
| **`inventoried`** | `research` / `experiment` / `template` / `fork` | Classification + tagging + quarterly inventory sweep — no bless contract. The registry row exists; SOP coverage is light-touch. |
| **`unmanaged`** | (transient — should not persist after sweep) | The state of a repo before the runbook discovers it. The sweep promotes to `inventoried` automatically with default `app_class=uncategorized`. |
| **`archived`** | `archive` | Retired repo (GH `isArchived=true` OR operator explicit). Registry row preserved for audit; no review cadence. |

The four production-class repos (`openclaw-akos`, `hlk-erp`, `boilerplate`,
`kirbe`) remain governed by their existing bless contracts; this SOP adds the
fleet-wide classification + inventory cadence the bless contracts did not
themselves cover.

## §3 Inputs

1. **`gh repo list FraysaXII --limit 200 --json …`** — primary data source for
   the inventory sweep. The runbook calls this through [`akos.process.run`](../../../../../../../../akos/process.py)
   and parses the JSON into Pydantic snapshots. Required fields:
   `name`, `url`, `visibility`, `isArchived`, `isFork`, `primaryLanguage`,
   `createdAt`, `pushedAt`, `repositoryTopics`.
2. **Current [`REPOSITORY_REGISTRY.csv`](../../../../People/Compliance/canonicals/REPOSITORY_REGISTRY.csv)**
   state — the registry the sweep diffs against. Loaded via
   [`akos.hlk_repository_registry_csv.REPOSITORY_REGISTRY_FIELDNAMES`](../../../../../../../../akos/hlk_repository_registry_csv.py)
   to guarantee the 29-column schema.
3. **GitHub API per-repo metadata** — `gh api repos/<owner>/<name>/codeowners-errors`
   + `gh api repos/<owner>/<name>/branches/<default>/protection` for the
   `codeowners_present` + `branch_protection_enabled` drift signals on `governed`
   rows. Other rows skip these calls (light-touch).
4. **Operator classification input** — for any `app_class=uncategorized` row the
   sweep produces, operator (or AIC role_owner) decides the final class via
   inline-ratify gate per [`akos-inline-ratification.mdc`](../../../../../../../../.cursor/rules/akos-inline-ratification.mdc).

## §4 Process

### §4.1 Quarterly inventory sweep (default cadence)

Runbook: `py scripts/inventory_github_repos.py sweep`.

1. Fetch `gh repo list FraysaXII --limit 200 --json …` and parse to Pydantic
   snapshots.
2. Load the current registry rows from canonical CSV via the SSOT tuple.
3. Compute three sets:
   - **New repos** (in GH, not in CSV) → propose `governance_status=inventoried`
     + `app_class=uncategorized` (operator classifies later via §4.2).
   - **Ghost rows** (in CSV, not in GH) → flag for operator inspection
     (placeholder rows like `client-delivery-pilot` per Lane F report §3.2).
   - **Changed metadata** (visibility flipped, language updated, pushed_at
     newer) → propose `last_inventory_at` bump + field refresh.
4. Write the drift report at `artifacts/inventory/repo-inventory-<YYYYMMDD>.md`
   with one section per category.
5. Do NOT write to canonical CSV during `sweep` — write happens in `classify`
   (per-row, after operator ratifies) or by Lane F-AUTHOR-2 backfill commit
   (bulk, after CSV gate clears).

### §4.2 On-create classification (event-triggered)

When a new repo appears in the org (sweep detects), operator or AIC role_owner
classifies it within 30 days. Runbook: `py scripts/inventory_github_repos.py
classify --repo <name> --app-class <value>`.

Classification options:

- `production` — promote via §4.3 (full bless flow, not this SOP's scope).
- `research` — AKOS-internal R&D output (paper code, framework exploration).
- `experiment` — throwaway / POC / spike — lowest-touch.
- `template` — boilerplate the operator forks for new projects.
- `fork` — tracked upstream fork (no AKOS contract).
- `archive` — retire immediately (operator decision: never worth pursuing).

Default if operator doesn't classify within 30 days: `experiment` (lowest-impact
default; can be promoted later). Escalation per
[`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc):
a blocker-tracker entry under `docs/wip/planning/_blockers/` captures the
operator-intent if classification is genuinely stalled.

### §4.3 Promotion to `governed` (cross-SOP handoff)

When operator decides an `inventoried` repo should become `governed` (full
production bless), the path is [`SOP-EXTERNAL_REPO_BLESSING_001`](../External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md)
§3-§6. This SOP just sets the entry condition: a row must already exist in the
registry with `governance_status=inventoried` before bless can fire.

After bless, the row's `governance_status` flips `inventoried → governed` +
`app_class` flips `(whatever) → production` + `codeowners_present=true` +
`branch_protection_enabled=true` (the bless flow writes all four cells via the
runbook's `classify` subcommand).

### §4.4 On-archive update (event-triggered)

When operator archives a repo in the GH UI (`isArchived=true`), the next
quarterly sweep detects the flip and proposes
`app_class=archive` + `governance_status=archived` + `lifecycle_status=archived`.
Operator ratifies via `classify` subcommand or the Lane F-AUTHOR-2 batch flow.

### §4.5 Annual review of `inventoried` repos

Once per year (Q1 default), operator reviews each `inventoried` row:

- **Promote to `governed`** if the repo is being actively maintained + warrants
  CODEOWNERS + branch protection.
- **Demote to `archive`** if the repo has been dormant > 2 years (per Lane F
  report §2.4 staleness signal).
- **Keep `inventoried`** if status quo is correct.

The annual review is operator-driven; the runbook produces a summary via
`audit` subcommand but doesn't auto-decide.

## §5 Outputs

1. **Updated [`REPOSITORY_REGISTRY.csv`](../../../../People/Compliance/canonicals/REPOSITORY_REGISTRY.csv)
   rows** — one row per repo in the org, 29 columns each, validated by
   [`scripts/validate_repository_registry.py`](../../../../../../../../scripts/validate_repository_registry.py)
   (advisory until backfill closure; FAIL after `--strict-app-class` flips on
   per D-IH-86-AD INFO→FAIL ramp).
2. **Drift report** at `artifacts/inventory/repo-inventory-<YYYYMMDD>.md` —
   markdown summary per sweep with sections: new repos, ghost rows, changed
   metadata, staleness candidates. Advisory; not committed to git.
3. **Cross-reference into [`REPO_HEALTH_SNAPSHOT.csv`](../../../../People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv)**
   when a `governed` row is touched — the existing weekly snapshot picks up the
   new `codeowners_present` + `branch_protection_enabled` cells naturally.

## §6 Failure modes

| # | Failure mode | Symptom | Remediation |
|--:|---|---|---|
| 1 | **Uncategorized stranded** | Newly-discovered repo sits at `app_class=uncategorized` for >30 days | Operator escalation per `akos-conflict-surfacing-and-blocker-trackers.mdc`; tracker entry under `docs/wip/planning/_blockers/` flags the stall. |
| 2 | **Abandoned production drift** | `production` row with `pushed_at > 180 days` | Runbook flags in `sweep` output; operator reviews — either revive (recent commit) or demote (`production → archive`). |
| 3 | **Stale governed rows** | `governed` repo whose `pushed_at > 365 days` | Mandatory operator review at annual cadence; default action: demote `governed → inventoried` and remove bless contract. |
| 4 | **Orphan ghost rows** | Registry row points at a non-existent GitHub URL (e.g. placeholder `client-delivery-pilot`) | Convert to a tracker entry under `docs/wip/planning/_trackers/` per `akos-conflict-surfacing-and-blocker-trackers.mdc` Option 5, OR drop with operator approval + decision row. |
| 5 | **CODEOWNERS missing on governed** | `governance_status=governed` AND `codeowners_present=false` | Auto-PR via [`scripts/bless_external_repo.py`](../../../../../../../../scripts/bless_external_repo.py) `--with ci-baseline` writes the canonical CODEOWNERS template. |
| 6 | **Branch protection disabled on governed** | `governance_status=governed` AND `branch_protection_enabled=false` | Operator-only fix (the GH API requires admin token); runbook surfaces the gap, operator enables protection in the GH UI. |
| 7 | **GitHub API rate limit** | Sweep batched calls exceed 5K req/hour authenticated quota | Runbook batches per-repo metadata calls only for `governed` rows (sweep itself is one call for the list). At 55 repos × 2 per-repo calls = ~110 calls per sweep — well under the limit. |

## §7 Cross-references

- [`SOP-EXTERNAL_REPO_BLESSING_001`](../External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md)
  — the path from `governance_status=inventoried` to `governance_status=governed`.
  This SOP is the precursor; that SOP is the upgrade flow.
- [`SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001`](../External%20Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md)
  — handles `governed` row drift (sha256 mismatches against AKOS templates) via
  auto-PR loop. Out of scope for this SOP, which is fleet-wide inventory.
- [`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001`](../Cross%20Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md)
  — when a `governed` repo consumes canonical mirrors, schema propagation
  notifications fire automatically. This SOP just ensures the `consumes_*`
  columns are populated on `governed` rows.
- [`akos-mirror-template.mdc`](../../../../../../../../.cursor/rules/akos-mirror-template.mdc)
  — AKOS-as-SSOT discipline; this SOP keeps `REPOSITORY_REGISTRY.csv` as the
  canonical authoring surface (GitHub topics are advisory mirror only, per
  Lane F report §4.2 GOV.UK ADR-0017 citation).
- [`akos-holistika-operations.mdc`](../../../../../../../../.cursor/rules/akos-holistika-operations.mdc)
  §"New git-canonical compliance registers (pattern)" — the canonical pattern
  this SOP's paired runbook follows (Pydantic SSOT + validator + Supabase
  mirror).
- [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
  RULE 1 — the pairing-rule this SOP + runbook instantiate.
- [`akos-governance-remediation.mdc`](../../../../../../../../.cursor/rules/akos-governance-remediation.mdc)
  §"HLK compliance governance" — canonical-CSV gate discipline for the row
  writes this SOP authorises.
- Lane F-GITHUB inventory report:
  [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/lane-f-app-governance-inventory-2026-05-19.md`](../../../../../../wip/planning/86-initiative-cluster-execution-coordinator/reports/lane-f-app-governance-inventory-2026-05-19.md)
  — the inventory + design report that grounds this SOP.

## §8 Paired runbook

[`scripts/inventory_github_repos.py`](../../../../../../../../scripts/inventory_github_repos.py)
implements the executable side of this SOP per
[`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1. Subcommands:

| Subcommand | Purpose | Side effects |
|---|---|---|
| `sweep` | Fetch GH inventory + diff vs registry + write drift report | Read-only for canonical CSV; writes `artifacts/inventory/repo-inventory-<YYYYMMDD>.md`. |
| `classify --repo <slug> --app-class <value>` | Set `app_class` on one row | Writes one cell in `REPOSITORY_REGISTRY.csv` via Pydantic round-trip (validates before write). |
| `audit` | Run validator with `--strict-app-class` | Read-only; surfaces missing `app_class` / `governance_status` cells. |
| `--dry-run` | Available on all subcommands | Prints planned writes without performing them. |

Per RULE 1.5 acceptance criteria:

- **Human/AIC route** (`acceptance_criteria_human`): a System Owner (or AIC
  role_owner) can run `gh repo list FraysaXII --json …`, classify each repo
  manually, and edit CSV cells by hand. The SOP §4 steps are reproducible
  without ever invoking the runbook.
- **Automation route** (`acceptance_criteria_automation`): `py scripts/inventory_github_repos.py
  sweep` runs unattended (e.g., quarterly GitHub Action) and produces a drift
  report; the operator can then dispatch `classify` per row or batch.

## §9 Cadence

- **Primary cadence:** `scheduled` (quarterly). Q1 / Q2 / Q3 / Q4 default sweep
  at end-of-quarter; the runbook can be wired to a GitHub Action when the
  org-level CI surface exists.
- **Secondary cadence:** `event_triggered`. New-repo events (sweep detects a
  GitHub repo not yet in the registry); on-archive events (sweep detects
  `isArchived=true` flip).
- **Per-engagement trigger:** when blessing a new sibling repo via
  [`SOP-EXTERNAL_REPO_BLESSING_001`](../External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md),
  the inventory sweep runs first to confirm the repo exists in GH and to
  populate its `created_at` / `pushed_at` / `primary_language` cells.
- **Operator-on-demand:** `py scripts/inventory_github_repos.py sweep --dry-run`
  produces the drift report without writes. Useful before any large refactor
  or org-level migration.

The cadence is registered in [`process_list.csv`](../../../../People/Compliance/canonicals/process_list.csv)
as `cadence: scheduled` + `cadence_secondary: event_triggered` (Lane F-AUTHOR-2
appends the row at backfill commit per §7.2 of the Lane F report). The
`item_id` is `env_tech_dtp_app_governance_quarterly_001` per the
`env_tech_dtp_*` namespace.

## §10 Anti-patterns

The following patterns are explicitly forbidden because they re-open the
governance gap this SOP exists to close:

1. **Manual CSV edit without `gh repo list` cross-check.** Operator editing
   `REPOSITORY_REGISTRY.csv` directly without first running `sweep --dry-run`
   risks duplicating a repo under two slugs, or registering a slug that doesn't
   match the GH `name` cell. Always sweep first; classify second.
2. **Bypassing the runbook for a `governed` promotion.** The path from
   `inventoried` to `governed` MUST go through
   [`SOP-EXTERNAL_REPO_BLESSING_001`](../External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md).
   Hand-editing `governance_status=governed` without authoring CODEOWNERS +
   enabling branch protection + writing EXTERNAL_REPO_CONTRACT.md fakes the
   contract and breaks the drift-remediation loop.
3. **Classification by guess instead of inventory evidence.** The Lane F report
   §2.1 inventory table is the canonical evidence base for the first backfill;
   classifications should be defensible against the `pushed_at` + `primary_language`
   + repo description signals, not invented from memory.
4. **Dropping ghost rows without a tracker.** When a registry row points at a
   non-existent GitHub URL, the right move is to convert to a tracker entry
   (per `akos-conflict-surfacing-and-blocker-trackers.mdc` Option 5), not
   silently delete. The tracker preserves the operator-intent that originally
   placed the row.
5. **Auto-default for `production`.** The `experiment` auto-default is safe
   because experiments don't carry contracts; `production` is never the
   auto-default because the bless flow is operator-discretionary. A repo that
   should be `production` but isn't classified surfaces as `uncategorized`,
   not auto-promoted.
6. **Skipping the annual review.** `inventoried` rows are NOT permanent. Without
   the annual review, the registry accumulates dormant entries that are neither
   `governed` nor `archived` and the staleness signal goes unused. The annual
   review is the doctrine; the SOP isn't complete without it.
