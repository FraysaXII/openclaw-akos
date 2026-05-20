---
intellectual_kind: operator_landing_page
sharing_label: internal_only
parent_initiative: INIT-OPENCLAW_AKOS-86
wave_id: I
lane_id: I-A
authored: 2026-05-19
last_review: 2026-05-19
last_review_by: System Owner
methodology_version_at_review: v3.1
linked_decisions:
  - D-IH-86-AG  # Wave I composition
  - D-IH-86-AH  # Dual-surface routing
  - D-IH-86-AL  # Operator landing page pattern
status: active
language: en
role_owner: System Owner
co_owner_role: PMO
audience: J-OP
access_level: 3
purpose: single-pane operator landing for AKOS visibility (Wave I Lane I-A deliverable per D-IH-86-AG); answers operator scratchpad L66 day-to-day "where am I" question
---

# AKOS Operator Landing — 2026-05-19

> Generated as Wave I Lane I-A deliverable per **D-IH-86-AG**. Per **D-IH-86-AH** this landing is the **AKOS-markdown side** of the dual-surface routing; the **ERP browser side** lands when Lane I-D ships the [I65 planning panel](../../65-akos-planning-workspace-panel/master-roadmap.md). Doctrine for "when to open which" is Lane I-B's `OPERATIONAL_COHESION_DOCTRINE.md` (pending mint).

> **Audience:** J-OP (Wave I scope per **D-IH-86-AJ**). Wave J+ extends incrementally to J-AIC + J-IN + J-CU + J-PT + J-AD + J-RC + J-CO per audience activation cadence.

---

## If you have 30 seconds — what needs me now?

The "next action" surfaces. Open these first when you sit down at the repo.

| Surface | Path | What it gives | Status |
|:---|:---|:---|:---:|
| **Operator Action Inbox** | [`docs/wip/planning/OPERATOR_INBOX.md`](../../OPERATOR_INBOX.md) | RICE-ranked OPS tasks needing operator/mixed action (auto-rendered from `OPS_REGISTER.csv` where status=open AND owner_class IN operator/mixed) | live (auto) |
| **Review-stamp inbox** | [`docs/wip/planning/REVIEW_STAMP_INBOX.md`](../../REVIEW_STAMP_INBOX.md) | Stale or missing review stamps on mirrored governance CSVs (sidecar to OPERATOR_INBOX) | live |
| **I86 cluster burndown plan** | [`docs/wip/planning/86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md`](../../86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md) | Current wave lens — 5 active siblings + 3 blocker-trackers + 9 OPS rows; **most recent wave**: Wave I CHARTER landed `117a3cc` 2026-05-19 | live |

---

## If you have 5 minutes — where are the initiatives?

The "portfolio status" surfaces. Open these to triangulate across folders.

| Surface | Path | What it gives | Status |
|:---|:---|:---|:---:|
| **WIP Dashboard** | [`docs/wip/planning/WIP_DASHBOARD.md`](../../WIP_DASHBOARD.md) | Initiative portfolio status across ~70 folders, grouped by `InitiativeStatus` taxonomy (Active / Continuous / Program Lines / Gated / Closed / Archived / Unknown) | live (auto on initiative change) |
| **Planning README** | [`docs/wip/planning/README.md`](../../README.md) | Initiative index with one-line blurbs (hand-curated narrative summaries per initiative) | live |
| **I86 master-roadmap** | [`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`](../../86-initiative-cluster-execution-coordinator/master-roadmap.md) | Ten-sibling checklist + Wave H/I closure history + wave-composition tables | live |
| **I86 cluster burndown inventory** | [`docs/wip/planning/86-initiative-cluster-execution-coordinator/cluster-burndown-inventory.md`](../../86-initiative-cluster-execution-coordinator/cluster-burndown-inventory.md) | Inventory of every cluster-burndown row with status + RICE + forward-charter linkage | live |
| **Operator scratchpad** | [`docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md`](../../86-initiative-cluster-execution-coordinator/operator-scratchpad.md) | Free-form operator thought capture; drained at wave closure into formal artifacts per **D-IH-86-U** | live |

---

## If you have 15 minutes — deeper context

The "ground truth" surfaces. Open these when you need to verify or extend doctrine.

| Surface | Path | What it gives |
|:---|:---|:---|
| **HLK ERP architecture** | [`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) | ERP panel inventory + mirror → view → panel triplet pattern |
| **PRECEDENCE ledger** | [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) | Canonical-vs-mirror-vs-reference classification across HLK assets |
| **DECISION REGISTER** | [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | Full decision log (~328 rows; most recent D-IH-86-AL Wave I Lane I-A landing pattern) |
| **INITIATIVE REGISTRY** | [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) | Initiative status truth (SSOT for `status:` flag synced from each folder's `master-roadmap.md` frontmatter) |
| **OPS REGISTER** | [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) | Full OPS action log (SSOT for `OPERATOR_INBOX.md`) |
| **USER_GUIDE** | [`docs/USER_GUIDE.md`](../../../USER_GUIDE.md) | Operator quick reference (commands, profiles, workflows) |
| **ARCHITECTURE** | [`docs/ARCHITECTURE.md`](../../../ARCHITECTURE.md) | System-level architecture (control plane, execution layer, data plane) |

---

## Cross-area canonicals (Lane E freshness gate)

Cross-area doctrinal SSOTs gated by `scripts/validate_canonical_enrichment_freshness.py` per **D-IH-86-AB** (3-day / 30-day / 90-day staleness tiers).

| Area | Canonical SSOT |
|:---|:---|
| **Marketing / Brand** | [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) |
| **People** | [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md) |
| **People — Agentic** | [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) |
| **Research** | [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md) |
| **Tech / System Owner** | [`docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) |
| **Operations / PMO** | [`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) |

To check freshness across all area canonicals:

```powershell
py scripts/validate_canonical_enrichment_freshness.py
```

For Wave H closure context (148 surfaces scanned; ~22 stale missing review-frontmatter), see the validator output directly.

---

## Runtime surfaces (separate from planning SSOT)

These are **runtime** — agent/server health and live UX — not portfolio/governance.

| Surface | Where | Notes |
|:---|:---|:---|
| **OpenClaw control dashboard** | `http://127.0.0.1:18789` (local) | Agent health + WebChat; runtime not portfolio. Started via `py scripts/serve-api.py` or `scripts/openclaw.py up`. |
| **HLK-ERP browser** | sibling repo [`hlk-erp`](https://github.com/FraysaXII/hlk-erp) | Operator-facing UX surface; v1 panels mostly reserved per [`HLK_ERP_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md); I65 planning panel lands in Wave I Lane I-D. |
| **Boilerplate** | sibling repo [`boilerplate`](https://github.com/FraysaXII/boilerplate) → `holistikaresearch.com` | Public marketing DOM; **reference-only** per D-IH-32-N. Not an operator surface. |

---

## Freshness signal

This landing is regenerated **per dated snapshot** — folder pattern `docs/wip/planning/dashboards/YYYY-MM-DD/index.md`. Today's snapshot is `2026-05-19/`. The page itself is static markdown; the **WIP_DASHBOARD** + **OPERATOR_INBOX** it points to are auto-regenerated when initiative folders change (run `py scripts/render_wip_dashboard.py` + `py scripts/render_operator_inbox.py`).

**Snapshot trigger:** mint a new dated folder when a material visibility shift lands (e.g., Lane I-B doctrine mint, Wave I closure, new wave charter, new operator-facing surface). The dated-folder pattern preserves historical snapshots without churn on the SSOT artifacts.

For cross-area canonical freshness numbers (148 surfaces; ~22 stale missing review-frontmatter as of 2026-05-19), run:

```powershell
py scripts/validate_canonical_enrichment_freshness.py
```

---

## Where this landing fits in the visibility doctrine

Per the Lane VISIBILITY-SWEEP four-axis parse (operator scratchpad L66, 2026-05-19):

| Axis | Operator question | This landing's contribution |
|:---|:---|:---|
| **1 — AKOS internal** | "where how what it gives" — day-to-day, which artifact tells me initiative/wave/OPS status? | **Primary axis.** This landing is the single pane of glass that links WIP Dashboard + Operator Inbox + cluster burndown + cross-area canonicals with "what it gives" annotations. |
| **2 — HLK external** | Which J-* audiences have real shipped surfaces vs markdown-only vault? | **Out of scope this wave.** Wave I bounded to J-OP per **D-IH-86-AJ**; J-IN + J-CU + J-PT + J-AD + J-RC + J-CO extend in Wave J+. |
| **3 — HLK-ERP status** | What landed in `hlk-erp` vs what is still charter/spec? | **Pointer only.** This landing names the ERP browser as a runtime surface (separate); the ERP-browser side of dual-surface routing ships when Lane I-D delivers I65. |
| **4 — Operational cohesion** | One narrative tying AKOS planning, ERP panels, boilerplate/web, registers, render pipelines? | **Lane I-B territory.** This landing is the AKOS-markdown side; the cross-surface routing matrix lands in `OPERATIONAL_COHESION_DOCTRINE.md` (pending). |

---

## Cross-references

- **Evidence base (parent of this landing):** [`reports/lane-visibility-sweep-2026-05-19.md`](../../86-initiative-cluster-execution-coordinator/reports/lane-visibility-sweep-2026-05-19.md) — full four-axis parse + §2.1 inventory table sourced here verbatim
- **Wave I CHARTER:** [`master-roadmap.md`](../../86-initiative-cluster-execution-coordinator/master-roadmap.md) §1.7 — five-lane composition (I-A through I-E)
- **Wave I CHARTER decisions:** D-IH-86-AG (composition) + D-IH-86-AH (dual-surface routing) + D-IH-86-AI (I65 fast-track) + D-IH-86-AJ (audience scope) + D-IH-86-AK (wave-execution mode)
- **This lane's decision:** **D-IH-86-AL** — operator-landing-page pattern at `docs/wip/planning/dashboards/<YYYY-MM-DD>/index.md`
- **Doctrine that names "when to open AKOS-markdown vs ERP-browser":** **pending** Lane I-B (`OPERATIONAL_COHESION_DOCTRINE.md` mint scheduled for the next commit)
- **ERP-browser side of dual-surface routing:** **pending** Lane I-D (I65 fast-track to `/operator/planning/` route in `hlk-erp` sibling)

---

*This landing is the AKOS-markdown side of the dual-surface routing per **D-IH-86-AH**. The ERP-browser side ships when Lane I-D delivers I65 (`/operator/planning/` route).*
