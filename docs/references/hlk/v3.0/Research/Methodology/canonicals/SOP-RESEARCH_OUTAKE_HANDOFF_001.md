---
title: SOP - Research Outake Handoff (SHARE lifecycle stage)
language: en
intellectual_kind: research-area-canonical-sop
sop_id: SOP-RESEARCH_OUTAKE_HANDOFF_001
access_level: 4
confidence_level: Euclid
source_taxonomy: holistika-internal-sop
authors:
  - Research Director
  - Lead Researcher
last_review: 2026-05-29
last_review_by: Founder
last_review_decision_id: D-IH-75-G
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-75-G
status: active
register: internal
linked_canonicals:
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
linked_runbooks: []
cadence: on_demand
---

# SOP — Research Outake Handoff (SHARE / OUTAKE)

## Purpose

Walk the **Research → Marketing/Brand → External-Render** handoff when an intelligence product
(brief, report, engagement pack, diagnostic output) must leave the internal CORPINT register and
reach a non-cleared audience. This SOP is Research-owned; it does **not** replace Marketing's
translation work or the render runbooks — it ensures Research delivers a **complete internal
package** so the sister areas can execute without guesswork.

Grounding: [`RESEARCH_LIFECYCLE_DOCTRINE.md`](../../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md) §6.1
(SHARE as a two-party join); decision `D-IH-75-G`.

## Scope

**In scope:** any Research-authored `.md` or structured pack under `docs/wip/intelligence/` or
`docs/references/hlk/v3.0/` tagged for external delivery (audience class other than J-OP only).

**Out of scope:** internal-only CORPINT briefs (J-OP audience only); raw source ledgers; operator
scratchpads; canonical CSV edits (those follow `akos-holistika-operations.mdc`).

## Inputs

| Input | Where it lives |
|:---|:---|
| Finished intelligence product (internal register) | `docs/wip/intelligence/<slug>/` or engagement folder |
| Source ledger (when governance-feeding) | `source-ledger.csv` per Research Action discipline |
| Audience tag(s) | Frontmatter `audience:` FK → `AUDIENCE_REGISTRY.csv` |
| Channel tag (when known) | Frontmatter `channel:` FK → `CHANNEL_TOUCHPOINT_REGISTRY.csv` |
| Access level + confidence | Frontmatter + `access_levels.md` / `confidence_levels.md` |

## Steps

### 1 — Confirm the product is SHARE-ready (Research)

1. Research Action loop stages **ingest → rate → rank → synthesize → govern** are complete for
   every source cited in the product (no "we'll add sources later").
2. Frontmatter carries resolvable `audience:` (one or more external classes when delivery is
   external).
3. Internal-register vocabulary is acceptable in the **source** `.md`; external delivery will use
   the translated register (see step 3).
4. PROTECT checks passed: no crown-jewel leakage; GOI/POI stance respected; access level matches
   content sensitivity (`access_levels.md`).

### 2 — Package the handoff artefact (Research)

Create or update **`outake-handoff-<YYYYMMDD>.md`** beside the product with:

| Field | Required content |
|:---|:---|
| `product_path` | Repo-relative path to the internal SSOT `.md` |
| `audience` | Semicolon-separated audience codes |
| `channel` | Channel code when known; `TBD` + inline-ratify if unknown |
| `objective` | One sentence: what decision/action the recipient should take |
| `language` | `es` / `fr` / `en` (working language for external prose) |
| `render_surfaces` | Which of pdf / web / mail / slide / erp / broadcast apply |
| `redaction_notes` | What was withheld and why (AL gate) |
| `linked_source_ledger` | Path to `source-ledger.csv` when applicable |
| `brand_register` | `internal` (handoff doc) / `external` (recipient-facing) |

### 3 — Surface the dual-register translation ask (Research → Marketing)

1. Flag every internal token that **must** translate before external render (see
   [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md)
   §3).
2. Do **not** pre-translate in the Research product unless the operator explicitly opts in — the
   translation step is Marketing/Brand's craft; Research supplies the internal SSOT + the
   handoff table above.
3. Record the handoff in the engagement's decision log or OPS row when the delivery gates a
   milestone.

### 4 — Surface the render-trail requirement (Research → External-Render)

Before any external send, confirm the six-surface contract per
`akos-external-render-discipline.mdc`:

1. Audience × channel × language × objective resolved (Surface 0 pre-flight).
2. Render artefact path named (PDF manifest, web URL, mail body policy, etc.).
3. If local render is blocked, file a row in
   `docs/wip/planning/_trackers/external-render-pending-tracker.md` — never attach raw `.md`
   to externals.

### 5 — Sign-off checklist (Research owner)

| # | Check | PASS / N/A |
|:--|:---|:---|
| 1 | Source ledger complete (when governance-feeding) | |
| 2 | Audience tag FK-resolves | |
| 3 | Access level matches content | |
| 4 | Handoff artefact written | |
| 5 | Translation table flagged for Marketing | |
| 6 | Render surfaces named | |
| 7 | PROTECT / redaction notes present when AL > internal | |

## Outputs

- `outake-handoff-<YYYYMMDD>.md` (internal; AL4)
- OPS or decision-log row when the handoff gates delivery
- Sister-area notification (Marketing/Brand + render owner when applicable)

## Failure modes

| Failure | Recovery |
|:---|:---|
| Missing audience tag | Halt SHARE; inline-ratify audience before handoff |
| Internal token in external render | Marketing drift gate FAIL — return to step 3 |
| No render trail | File render-pending tracker; do not send |
| Source ledger incomplete | Return to Research Action govern stage |

## Cross-references

- Lifecycle doctrine: [`RESEARCH_LIFECYCLE_DOCTRINE.md`](../../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md) §5–§6.1
- Dual register: [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md)
- Render discipline: `.cursor/rules/akos-external-render-discipline.mdc`
- Research Action: [`RESEARCH_ACTION_DISCIPLINE.md`](RESEARCH_ACTION_DISCIPLINE.md)
- Wave R+5 backlog item A3: `docs/wip/planning/86-initiative-cluster-execution-coordinator/research-rollout-backlog-2026-05-29.md`
