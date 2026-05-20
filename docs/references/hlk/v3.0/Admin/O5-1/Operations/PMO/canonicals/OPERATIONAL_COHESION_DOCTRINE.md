---
intellectual_kind: doctrine
sharing_label: internal_only
doctrine_id: OPERATIONAL_COHESION_DOCTRINE_001
role_owner: PMO
co_owner_role: System Owner
area: Operations
entity: Holistika
audience: J-OP
access_level: 3
status: active
added_at: 2026-05-19
last_review_at: 2026-05-19
last_review_by: Founder/CEO
methodology_version_at_review: v3.1
last_review_decision_id: D-IH-86-AM
linked_decisions:
  - D-IH-86-AG
  - D-IH-86-AH
  - D-IH-86-AJ
  - D-IH-86-AM
  - D-IH-86-AN
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv
paired_runbook: scripts/render_operational_cohesion_index.py
governance_rules:
  - akos-external-render-discipline.mdc
  - akos-holistika-operations.mdc
  - akos-planning-traceability.mdc
  - akos-executable-process-catalog.mdc
language: en
---

# Holistika Operational Cohesion Doctrine

> Per **D-IH-86-AH** dual-surface routing: AKOS-markdown SSOT + ERP-browser UX coexist intentionally; this doctrine names *when to open which* per audience class. Per **D-IH-86-AJ** forward-compat for all 8 audience codes in [`AUDIENCE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) — Wave I ships the J-OP slice end-to-end (operator + cleared AICs per registry definition); Wave J+ extends incrementally to the seven external audiences.

## §1 — Purpose

The Holistika OS has unified its SSOT layer in canonical CSVs (per [`PRECEDENCE.md`](../../../../People/Compliance/canonicals/PRECEDENCE.md) and the two-plane discipline of [`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc)), yet the operator-facing UX layer is **intentionally bifurcated**: planning happens in AKOS-markdown, daily ops happens in the HLK-ERP browser, external delivery happens through rendered PDFs / Web / Mail, and agent runtime happens through the OpenClaw FastAPI dashboard. Before this doctrine, no contract named *which* surface to open *when* — operator scratchpad L66 surfaced the lived pain ("I don't always know where I am") and Lane VISIBILITY-SWEEP §5 confirmed the gap mechanically (nothing ≤30 days answered "open this first for AKOS vs ERP vs external").

This doctrine codifies the routing contract. After this commit, every operator, every cleared AIC, and every cleared collaborator can answer the same question deterministically: *given what I'm doing right now, which surface should I open?* The §4 routing matrix is the load-bearing deliverable; the rest of the doctrine establishes the surface-class taxonomy that the matrix operates on.

## §2 — Scope

In scope — the 4 surface classes Holistika operates today:

- **AKOS-markdown** — the planning + governance SSOT under [`docs/wip/planning/`](../../../../../../../docs/wip/planning/) + [`docs/references/hlk/`](../../../../../../../docs/references/hlk/) (governed by [`akos-planning-traceability.mdc`](../../../../../../../.cursor/rules/akos-planning-traceability.mdc)).
- **ERP-browser** — the operator-facing Next.js panels under sibling [`hlk-erp/`](https://github.com/FraysaXII/hlk-erp) repo (governed by [`HLK_ERP_ARCHITECTURE.md`](HLK_ERP_ARCHITECTURE.md)).
- **External-render** — PDF / Web / Mail / Slide / Broadcast / ERP surfaces for non-cleared audiences (governed by [`akos-external-render-discipline.mdc`](../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) 6-surface enum).
- **OpenClaw runtime** — agent dashboard at `127.0.0.1:18789` + WebChat + FastAPI control plane (governed by AKOS runtime contract per [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc)).

Out of scope:

- Physical infrastructure (Render / Vercel / Supabase deploy posture — owned by [`akos-deploy-health.mdc`](../../../../../../../.cursor/rules/akos-deploy-health.mdc)).
- Brand / marketing surfaces beyond the external-render trail (owned by Brand canonicals).
- The data plane itself — canonical CSVs are surface-agnostic SSOT; this doctrine routes operators to *views* of that plane, not to alternative SSOTs.
- Per-engagement folder structure (owned by [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](WORKSPACE_BLUEPRINT_HOLISTIKA.md) §1 four-channel persistence + §6 engagement folder shape).

## §3 — Surface inventory and ownership

Per-surface contract, mirroring [`HLK_ERP_ARCHITECTURE.md`](HLK_ERP_ARCHITECTURE.md) §4 panel inventory and Lane VISIBILITY-SWEEP §2.1 catalogue. The `Audience served` column uses [`AUDIENCE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) codes; per registry semantics, the J-OP code covers operator + cleared agents + cleared AICs (no separate AIC code).

| Surface | Class | Path / route | Render mechanism | Role owner | Audience served | Notes |
|:---|:---|:---|:---|:---|:---|:---|
| WIP Dashboard | AKOS-markdown | [`docs/wip/planning/WIP_DASHBOARD.md`](../../../../../../../docs/wip/planning/WIP_DASHBOARD.md) | [`render_wip_dashboard.py`](../../../../../../../scripts/render_wip_dashboard.py) (auto) | PMO | J-OP | Initiative portfolio status snapshot |
| Operator Inbox | AKOS-markdown | [`docs/wip/planning/OPERATOR_INBOX.md`](../../../../../../../docs/wip/planning/OPERATOR_INBOX.md) | [`render_operator_inbox.py`](../../../../../../../scripts/render_operator_inbox.py) (auto) | PMO | J-OP | RICE-ranked OPS tasks |
| Operator landing | AKOS-markdown | `docs/wip/planning/dashboards/<YYYY-MM-DD>/index.md` | manual (dated snapshot) | System Owner | J-OP | Single-pane "where am I"; introduced Lane I-A per D-IH-86-AL |
| Cluster burndown | AKOS-markdown | `docs/wip/planning/86-initiative-cluster-execution-coordinator/cluster-burndown-*.md` | manual | PMO | J-OP | Active wave lens |
| Master-roadmaps | AKOS-markdown | `docs/wip/planning/<NN-slug>/master-roadmap.md` | manual | role_owner per initiative | J-OP | Per-initiative phase detail |
| Mission Control | ERP-browser | `hlk-erp/.../mission-control/` (forward-charter) | Next.js + Supabase views | System Owner | J-OP | I62 closed per D-IH-86-AK for SQL views; UI mocked-data forward-chartered to I-NN-MISSION-CONTROL-UI |
| Planning panel | ERP-browser | `hlk-erp/.../operator/planning/` (Lane I-D scope) | Next.js + AKOS planning data | System Owner | J-OP | I65 fast-track Wave I Lane I-D |
| Governance panels | ERP-browser | `hlk-erp/.../operator/governance/external-repos/` (I64) | Next.js | DevOPS | J-OP | I64 spec v2 promoted; implementation pending |
| Program rollup | ERP-browser | `hlk-erp/.../program-rollup/` (I89) | Next.js + Supabase view | System Owner | J-OP and partial J-IN | I89 P0 in-progress |
| Investor dossier | External-render | `artifacts/exports/*-investor-*.pdf` | [`render_dossier.py`](../../../../../../../scripts/render_dossier.py) + [`export_company_deck_pdf.py`](../../../../../../../scripts/export_company_deck_pdf.py) | Founder/CEO + CFO | J-IN | Wave F render-trail discipline applies |
| ENISA dossier | External-render | `artifacts/exports/*-enisa-*.pdf` | [`render_dossier.py`](../../../../../../../scripts/render_dossier.py) | Compliance | J-ENISA | Sealed sha256 manifest mandatory |
| Customer pitches | External-render | per-engagement `_assets/.../{deck,dossier}.pdf` | [`render_dossier.py`](../../../../../../../scripts/render_dossier.py) + `build_company_deck.py` | Brand + CRO | J-CU | Per-engagement scope |
| Partner kits | External-render | per-engagement folder | [`render_dossier.py`](../../../../../../../scripts/render_dossier.py) | Brand + CRO | J-PT | Per-engagement scope |
| Adviser handoffs | External-render | `_assets/advops/.../handoff_*.pdf` | [`export_adviser_handoff.py`](../../../../../../../scripts/export_adviser_handoff.py) | PMO + Legal | J-AD | Pre / post-NDA distinction per [`akos-adviser-engagement.mdc`](../../../../../../../.cursor/rules/akos-adviser-engagement.mdc) |
| Broadcast / presentations | External-render | `docs/presentations/<engagement>/index.html` | [`render_impeccable_uat.py`](../../../../../../../scripts/render_impeccable_uat.py) + manual | Brand | J-IN + J-CU + J-PT | HTML deck variant on stable URL |
| OpenClaw dashboard | OpenClaw runtime | `http://127.0.0.1:18789` (local) | FastAPI + WebChat | System Owner | J-OP | Agent health; not portfolio |
| WebChat | OpenClaw runtime | `http://127.0.0.1:18789/webchat` | FastAPI | System Owner | J-OP | Madeira conversation surface |

When [`RENDERING_PIPELINE_REGISTRY.csv`](../../../Envoy%20Tech%20Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv) holds rows not appearing here, that is by design — the registry is the per-pipeline contract; this table is the per-surface contract; the join is `Render mechanism` column ↔ `pipeline_id`.

## §4 — Routing matrix (the load-bearing deliverable)

The "when to open which" matrix. Rows = operator intent; columns = surface class; cells = primary surface recommendation, with secondary alternatives when both serve.

| Operator intent | AKOS-markdown | ERP-browser | External-render | OpenClaw runtime |
|:---|:---:|:---:|:---:|:---:|
| **What needs me now?** | OPERATOR_INBOX **primary** | Mission Control panel (forward-charter) secondary | — | — |
| **Where am I in the current wave?** | Operator landing → cluster burndown **primary** | Planning panel (Lane I-D) secondary | — | — |
| **What's the status of initiative I-NN?** | WIP_DASHBOARD **primary**; master-roadmap secondary | Governance panel (I64) when shipped | — | — |
| **What did we decide on X?** | `DECISION_REGISTER.csv` **primary**; per-initiative `decision-log.md` secondary | — | — | — |
| **Authoring / editing / refactoring governance content** | AKOS-markdown SSOT **primary (mandatory)** | — | — | — |
| **Reviewing process / role / engagement-model rows** | `process_list.csv` / `baseline_organisation.csv` / `ENGAGEMENT_MODEL_REGISTRY.csv` **primary** | ERP panels when shipped (read-projection) | — | — |
| **Agent health check** | — | — | — | OpenClaw dashboard **primary** |
| **Madeira conversation / methodology check** | — | — | — | WebChat **primary** |
| **Show me to an investor** | — | — | Investor dossier PDF **primary** + broadcast HTML secondary | — |
| **Show me to a customer SME** | — | ERP customer-portal (forward-charter) when shipped | Customer dossier PDF **primary** + mail outreach | — |
| **Show me to a partner** | — | — | Partner kit PDF **primary** + broadcast HTML | — |
| **Show me to an adviser (pre-NDA)** | — | — | Adviser handoff PDF (pre-NDA variant) **primary** + mail | — |
| **Show me to an adviser (post-NDA)** | — | ERP advops adviser-rollup (I89 P1+) when shipped | Adviser handoff PDF (post-NDA variant) **primary** | — |
| **Show me to ENISA** | — | — | ENISA dossier PDF **primary** (sealed sha256 manifest mandatory) | — |
| **Show me to a recruiter (pending I75)** | — | — | Recruiter deck PDF (forward-charter) | — |
| **Show me to a collaborator (pending I74)** | — | — | Collaborator kit (forward-charter) | — |

**Reading the matrix.** "Primary" = the recommended first hop for that intent. "Secondary" = an acceptable alternative when the primary is unavailable, or when the secondary offers an affordance the primary lacks (e.g., ERP panel for interactive filtering vs markdown for full-text grep).

**Authoring vs reading distinction — non-negotiable.** AKOS-markdown is the SSOT for **authoring** every governance artifact. ERP-browser is a **read-projection** of that SSOT for operator UX (interactive panels, filtering, drawer-based affordances). External-render is the **audience-rendered projection** for non-cleared recipients. OpenClaw runtime is the **agent-side projection** for runtime ops. Operators must never author governance content in ERP-browser as the source of truth — that would create drift. ERP-browser writes back to AKOS-markdown via Supabase mirror sync per [`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc) two-plane discipline.

## §5 — Audience-class extension contract

Wave I ships the J-OP slice of the matrix end-to-end (operator + cleared agents + cleared AICs per [`AUDIENCE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) J-OP definition). Per **D-IH-86-AJ** Q4=D full-audience-spectrum scope, Wave J+ extends the matrix to the seven external audience codes incrementally, in this order:

- **J-IN** (investor) — primary surface class = External-render (PDFs + broadcast HTML); ERP investor-rollup is forward-charter (post-I89). Activation trigger = first investor outreach campaign.
- **J-CU** (customer SME) — primary surface class = External-render (PDFs + Mail); ERP customer-portal is forward-charter. Activation trigger = first commercial engagement at Holistika sub-mark scale (per [`engagement-model-registry`](../../../People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) `eng_model_hourly_consultant` / `eng_model_milestone_consultant`).
- **J-PT** (partner) — primary surface class = External-render (PDFs); ERP partner-portal is forward-charter. Activation trigger = first co-delivery or referral partnership.
- **J-AD** (advisor) — primary surface class = External-render (handoff PDFs); ERP advops adviser-rollup ships I89 P1+. Activation already underway per [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md).
- **J-ENISA** (regulator) — primary surface class = External-render (sealed PDFs); no ERP variant planned (regulator never gets an interactive surface). Activation already underway via founding-2026 dossier work.
- **J-RC** (recruiter) — pending I75 activation; AUDIENCE_REGISTRY status currently `inactive`. Surface class will be External-render (PDFs + Broadcast).
- **J-CO** (collaborator) — pending I74 activation; AUDIENCE_REGISTRY status currently `planned`. Surface class will be External-render (PDFs + Broadcast + Web).

Per **D-IH-86-AJ**, each Wave J+ extension is mechanical (row addition to §4 + row addition to §3 inventory), not architectural — this doctrine does not require restructure when a new audience activates; only the per-audience matrix row gets populated.

## §6 — Cohesion gates (what keeps surfaces in sync)

The 4 surface classes share the same SSOT but project to it differently; without mechanical gates, the projections drift. The following gates keep them aligned:

| Gate | Mechanism | Cadence | Owner |
|:---|:---|:---|:---|
| AKOS-markdown ↔ Supabase mirror | [`sync_compliance_mirrors_from_csv.py`](../../../../../../../scripts/sync_compliance_mirrors_from_csv.py) + `compliance_mirror_emit` profile | per canonical-CSV change | System Owner |
| External-render trail | [`validate_external_render_trail.py`](../../../../../../../scripts/validate_external_render_trail.py) `--strict --strict-freshness` (FAIL gate) | release-gate every commit | Brand + System Owner |
| Canonical freshness | [`validate_canonical_enrichment_freshness.py`](../../../../../../../scripts/validate_canonical_enrichment_freshness.py) 3/30/90-day INFO advisory | release-gate every commit | role_owner per canonical |
| BBR dual-register | [`validate_brand_baseline_reality_drift.py`](../../../../../../../scripts/validate_brand_baseline_reality_drift.py) FAIL on external-leak | release-gate every commit | Brand & Narrative Manager |
| ERP-browser ← Supabase view | Next.js consumes Supabase RLS views; no manual sync | per ERP deploy | System Owner |
| OpenClaw runtime ← config | [`verify_openclaw_inventory.py`](../../../../../../../scripts/legacy/verify_openclaw_inventory.py) | release-gate every commit | System Owner |
| Operator landing snapshot | manual regen per material visibility shift | event-triggered (Wave closure / new canonical mint / new audience activation) | System Owner |
| Cohesion quarterly review | this doctrine + paired runbook [`render_operational_cohesion_index.py`](../../../../../../../scripts/render_operational_cohesion_index.py) | quarterly per `process_list.csv` row `ops_pmo_dtp_cohesion_quarterly_001` | PMO + System Owner |

## §7 — Anti-patterns

The following are explicitly prohibited under this doctrine; reviewers should reject PRs that introduce them:

- **Authoring governance content in ERP-browser as source of truth.** Creates drift; violates the two-plane discipline of [`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc).
- **Publishing AKOS-markdown to external audiences without a render trail.** Violates [`akos-external-render-discipline.mdc`](../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) RULE 1 6-surface canonical enum.
- **Routing operators to the OpenClaw dashboard for portfolio status.** Category error; OpenClaw is agent runtime, not initiative status. The right surface is WIP_DASHBOARD / OPERATOR_INBOX / cluster burndown.
- **Forking decision SSOT into per-surface registries.** Violates [`akos-mirror-template.mdc`](../../../../../../../.cursor/rules/akos-mirror-template.mdc); `DECISION_REGISTER.csv` is canonical and downstream surfaces must FK-resolve into it, never duplicate it.
- **Treating WIP_DASHBOARD and OPERATOR_INBOX as duplicative.** They serve different intents per §4 (portfolio status vs RICE-ranked tasks); both stay.
- **Adding a new audience class without extending §5 routing.** Extension drift; the per-audience row addition to §3 inventory + §4 matrix is mandatory at audience-activation time.
- **Conflating "operator runtime" with "agent runtime".** OpenClaw dashboard surfaces *agent* health; operator runtime is the ERP-browser. Surface-class is determined by what *runs there*, not by who *opens it*.
- **Renaming surfaces in §3 inventory without updating the paired runbook.** The runbook validates per-surface paths exist; rename without runbook update breaks the cohesion gate.

## §8 — Paired runbook contract

The paired runbook [`scripts/render_operational_cohesion_index.py`](../../../../../../../scripts/render_operational_cohesion_index.py) implements the executable half of this doctrine per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 (every executable process needs a paired human-readable SOP / doctrine):

- **`validate` subcommand (default; load-bearing)** — self-consistency check against this doctrine. Specifically:
  1. Every path in this doctrine's `linked_canonicals:` frontmatter resolves to an existing file on disk.
  2. Every `J-*` audience code appearing in §3 inventory + §4 matrix + §5 extension matches a row in [`AUDIENCE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) `audience_code` column.
  3. Every `governance_rules:` entry resolves to an existing file under `.cursor/rules/`.
  4. Exit 0 on all-pass; exit 1 on any failure with a per-line error report.

- **`index` subcommand (optional; v1 emits a derived stub)** — emits an audience-pivoted routing index to `artifacts/cohesion/index-<YYYYMMDD>.md` for landing-page consumption.

- **`--dry-run` flag** — both subcommands accept it; no file writes.

CI invokes `validate` per release-gate. The runbook is registered with the [`ops_pmo_dtp_cohesion_quarterly_001`](../../../../People/Compliance/canonicals/process_list.csv) row's `acceptance_criteria_automation` field (per D-IH-86-AN).

## §9 — Forward-charters (Wave J+ scope)

The following are explicit forward-charters this doctrine creates; they are not Wave I scope:

- **Per-audience routing-matrix row population** (J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO) as each audience activates per §5 trigger conditions.
- **ERP-browser variant rows** in §3 inventory as panels ship (Lane I-D I65 planning panel; I89 program rollup; I64 governance panels; future Mission Control UI per I-NN-MISSION-CONTROL-UI candidate).
- **Wave I Lane I-C audit findings** may surface new surfaces or rename existing ones; doctrine `last_review_at:` advances accordingly.
- **`PEOPLE_DESIGN_PATTERN_REGISTRY.csv` row mint** if the cross-area surface-class routing pattern proves reusable (e.g., other discipline-of-disciplines areas adopt the 4-class surface abstraction). Candidate pattern name: `pattern_surface_class_routing_per_audience`.
- **Cohesion validator promotion to FAIL** if drift becomes a recurring class of finding; today the runbook is paired-runbook-only (not a release-gate FAIL gate) — promotion would mirror the I66 INFO → FAIL ramp pattern.

## §10 — Cross-references

- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](WORKSPACE_BLUEPRINT_HOLISTIKA.md) — four-channel persistence + engagement folder shape (this doctrine's substrate).
- [`HLK_ERP_ARCHITECTURE.md`](HLK_ERP_ARCHITECTURE.md) — ERP-browser surface architecture (this doctrine's read-projection contract).
- [`AUDIENCE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) — audience-class SSOT (this doctrine's §4 + §5 column source).
- [`RENDERING_PIPELINE_REGISTRY.csv`](../../../Envoy%20Tech%20Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv) — per-pipeline render contracts (this doctrine's §3 mechanism column).
- [`akos-external-render-discipline.mdc`](../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) — external-render trail discipline (this doctrine's §6 row).
- [`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc) — two-plane Supabase + SSOT discipline (this doctrine's §4 authoring constraint).
- [`akos-planning-traceability.mdc`](../../../../../../../.cursor/rules/akos-planning-traceability.mdc) — initiative discipline (this doctrine emerged from I86 Wave I Lane I-B; charter decision D-IH-86-AG).
- [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 — paired-SOP / paired-runbook discipline (this doctrine + `render_operational_cohesion_index.py` is the worked example).
- Wave I composition: [`master-roadmap.md`](../../../../../../wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md) §1.7 Lane I-B.
- Evidence: [`lane-visibility-sweep-2026-05-19.md`](../../../../../../wip/planning/86-initiative-cluster-execution-coordinator/reports/lane-visibility-sweep-2026-05-19.md) §5 cohesion + §6 Option D source material.
