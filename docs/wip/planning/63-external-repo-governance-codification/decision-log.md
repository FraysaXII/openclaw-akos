---
language: en
status: active
initiative: 63-external-repo-governance-codification
report_kind: decision-log
last_review: 2026-05-07
---

# Decision log — Initiative 63

Decisions land here as `D-IH-63-X` ids. Charter ships with three decisions
implicit in P0; new decisions are recorded as P1-P6 unfold.

## D-IH-63-A — Charter as a sibling initiative to I62

- **Date:** 2026-05-06
- **Decision:** Codify the External Repo Bless Pattern in a separate
  initiative folder (I63), not by overloading I62.
- **Rationale:** I62 is execution-shaped (Mission Control on hlk-erp). I63
  is governance-shaped (canonical CSVs + SOPs). Mixing the two would muddle
  scope and make the audit trail harder to read.
- **Alternative considered:** Fold this work into I62 as P12. Rejected
  because P12 would touch `process_list.csv` and v3.0 vault — unrelated to
  I62's outcome (operator surface).

## D-IH-63-B — SOPs land at `status: review` first, never `active` directly

- **Date:** 2026-05-06
- **Decision:** Author all three SOPs at `status: review` in this charter
  ship; promotion to `active` requires P3 operator approval and the
  corresponding `process_list.csv` row mint.
- **Rationale:** `SOP-META_PROCESS_MGMT_001.md` §4.2-4.3 says canonical
  CSV rows must exist before SOPs go active. We honour that here.
- **Implication:** The Cursor rule extension to point at the three SOPs
  (P6) waits until they're `active`.

## D-IH-63-C — CSV column proposal as a separate report, not a CSV edit

- **Date:** 2026-05-06
- **Decision:** Propose the three new `REPOSITORY_REGISTRY.csv` columns
  (`consumes_compliance_types`, `consumes_mirrors`, `path`) in a markdown
  report (`reports/csv-proposal-2026-05-06.md`) rather than minting them
  in this ship.
- **Rationale:** Canonical CSV edits require operator approval per the
  HLK governance rule. A markdown report is the correct artefact at the
  charter stage.
- **Implication:** The bless scaffolder already reads these columns
  defensively (defaults to `False` / empty), so the soft-rollout is
  forward-compatible.

## D-IH-63-D — Operator approval of CSV proposal v2 (revised schema + naming)

- **Date:** 2026-05-07
- **Decision:** Operator approves
  [`reports/csv-proposal-2026-05-06.md`](reports/csv-proposal-2026-05-06.md)
  with revisions: corrected `process_list.csv` schema (no fictional `plane`
  column), renamed `path` → `local_path` to avoid `pathlib.Path`
  shadowing, switched `consumes_mirrors` separator from `,` to `;` to
  avoid CSV field-separator collision, and harmonised `item_id` to
  canonical `SOP-<NAME>_001` shape (dropped `PROC-` prefix).
- **Rationale:** Operator review of v1 proposal flagged that the
  proposed schema didn't match the real `process_list.csv` header.
  Re-reading the canonical CSV revealed the correct 21-column shape and
  the existing `SOP-MCP_SERVER_DEFINITION` / `SOP-ENVOYLAB_REFACTOR_*`
  naming convention.
- **Trace:** Updated proposal report carries a v1 → v2 revision history
  table. Both versions remain in the audit trail.
- **Applied:** P4. CSVs edited at `docs/references/hlk/compliance/`.

## D-IH-63-E — `role_owner` split: DevOPS for blessing+drift, System Owner for schema-propagation

- **Date:** 2026-05-07
- **Decision:** The three new `process_list.csv` rows use a split
  `role_owner` assignment:
  - `SOP-EXTERNAL_REPO_BLESSING_001` → `DevOPS`
  - `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001` → `DevOPS`
  - `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001` → `System Owner`
- **Rationale:** `baseline_organisation.csv` (org_039) defines DevOPS
  as owning *"CI/CD, infrastructure, deployment pipelines, and
  operational tooling"* — which is exactly the bless and drift loops.
  System Owner (org_038) owns *"Infrastructure and Data Governance"*,
  aligning with the cross-repo data-schema propagation loop. Split
  ownership reflects the actual function rather than collapsing all
  three to one role.
- **Alternative considered:** Single owner = `System Owner` (v1
  proposal). Rejected because it under-credits DevOPS's existing
  canonical mandate over CI/CD and drift loops.
- **Implication:** Operator-side notifications from these processes
  will route to DevOPS for blessing+drift and to System Owner for
  schema propagation. No baseline_organisation.csv edit needed; both
  roles already exist.

## D-IH-63-F — KM manifest validator extended to honour `intellectual_kind: sop`

- **Date:** 2026-05-07
- **Decision:** `scripts/validate_hlk_km_manifests.py` extended so
  manifests with `intellectual_kind: sop` validate against
  `paths.sop:` rather than the visual-asset `paths.raster:` field.
- **Rationale:** SOP manifests document markdown SOPs, not visual
  diagrams. Forcing them through the raster validator was a category
  error — the v1 SOP manifests for I59 P9 already encountered this
  silently. The extension closes that gap and unblocks the three I63
  SOP manifests cleanly.
- **Trace:** `tests/` coverage and `OVERALL: PASS` on 16/16 manifests
  after the extension.

## D-IH-63-G — Bounded MCP automation for secrets walkthrough

- **Date:** 2026-05-07
- **Question:** Operate the I63 secrets walkthrough end-to-end via
  MCPs.
- **Decision:** Apply the parts that MCPs actually cover (Sentry org/
  team/DSN discovery, Slack channel discovery, GitHub repo-secret
  set/list via gh CLI). Defer the four user-bound flows (Sentry
  project creation, Sentry auth token creation, Vercel token
  creation, Slack webhook URL creation, GitHub fine-grained PAT
  creation) to a 4-tab, ~10-minute operator checklist captured in
  [`reports/secrets-mcp-application-2026-05-07.md`](reports/secrets-mcp-application-2026-05-07.md).
- **Rationale:** Sentry MCP `create_project` returned HTTP 403
  (account is org member, not manager). Slack MCP has no webhook-
  creation tool. Vercel MCP has no env-var or token tool. GitHub MCP
  is not installed. The current `gh` token has `gist`, `read:org`,
  `repo` — sufficient for repo-level secret-set, missing `admin:org`
  for org-level. Recommended: `gh auth refresh -h github.com -s
  admin:org,workflow` once before running org-level `gh secret set`
  commands.
- **Trace:** [`reports/secrets-mcp-application-2026-05-07.md`](reports/secrets-mcp-application-2026-05-07.md);
  [`reports/secrets-walkthrough-2026-05-06.md`](reports/secrets-walkthrough-2026-05-06.md)
  frontmatter flipped `applied → applied-partial` with pointer to the
  newer report.
