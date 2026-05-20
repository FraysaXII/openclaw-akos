---
candidate_id: I90
title: Visibility audit and per-audience routing — full 8 J-* spectrum dogfooded
status: candidate
authored: 2026-05-19
last_review: 2026-05-19
parent_initiatives: [86]
related_initiatives: [62, 64, 65, 70, 85, 89]
priority: 4
language: en
audience: J-OP
access_level: 3
parent_lane: I86 Wave I Lane I-C
charter_decisions:
  - D-IH-86-AO  # candidate mint
  - D-IH-86-AP  # activation criteria gate
forward_charter_authority: D-IH-86-AJ (Wave I full-audience-spectrum scope; J-OP + J-AIC ship in Wave I; J-IN/J-CU/J-PT/J-AD/J-ENISA/J-RC/J-CO forward-chartered)
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
---

# I90 candidate — Visibility audit and per-audience routing (full 8 J-* spectrum, dogfooded)

> **Spawned by I86 Wave I Lane I-C** per operator scratchpad L66 (visibility entry) → ratified D-IH-86-AG..AK 2026-05-19 → forward-chartered as candidate per **Option 5 default posture** (`akos-conflict-surfacing-and-blocker-trackers.mdc`). Activation gates not met today; this candidate preserves operator-intent visibility (the audit was *considered* during Wave I) without speculative-promotion debt. Sibling pattern: I85 candidate → I85 active (clean activation); contrast with I74 / I75 / I83 blocker-tracker shape (gated on external triggers).

## 1. Operating story

[`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) (Lane I-B mint, 2026-05-19) names the **routing matrix** (§4) and the **per-audience extension contract** (§5) for all 8 J-\* codes in [`AUDIENCE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv). Wave I ships the **J-OP slice end-to-end** (operator + cleared agents + cleared AICs per registry semantics — no separate J-AIC code today; the registry's J-OP definition covers the AIC class) but the seven external audience rows in §5 (J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO) are **forward-chartered** with extension being mechanical (row addition to §3 inventory + §4 matrix) rather than architectural.

**Without this audit**, the doctrine's per-audience routing claims stay theoretical — they pass `validate` (`render_operational_cohesion_index.py`) on linked-canonical and J-\* code resolution, but no one has verified that the *promised surface* for J-IN actually exists, renders, and reaches the recipient with the expected register / format / channel triplet. Lane VISIBILITY-SWEEP §3.3 already flagged this drift mechanically (registry promised vs shipped by audience class).

**With this audit**, every audience row in the routing matrix carries an evidenced status: which surfaces ship today, which are forward-chartered, which have render-trail gaps, which exist as drift between AKOS-markdown SSOT and the rendered artifact. The audit's output becomes the **load-bearing evidence base** for Wave J+ extension work — naming what each audience actually receives versus what the doctrine claims it should.

## 2. Why activation is gated (D-IH-86-AP)

Per Option 5 default posture: speculatively chartering this audit today would create the same shape as the I74 / I75 reverted-promotion lineage (`D-IH-86-F` / `D-IH-86-G` precedent). The audit needs three concrete preconditions before it can produce *evidenced* findings rather than theoretical inventory:

### 2.1 Activation criteria (all three required; AND-gate)

| # | Criterion | Why required | Source of truth |
|:---:|:---|:---|:---|
| **A1** | **I65 ERP planning panel completion** (Lane I-D delivery: `/operator/planning/` route live in `hlk-erp` reading from Supabase mirror tables) | The audit must verify the **J-OP + J-AIC ERP-browser column** of the routing matrix has actual *implemented* surfaces, not just `HLK_ERP_ARCHITECTURE.md` §4 spec rows marked `reserved (P10.5)`. Without I65 shipped, the J-OP audit row stays in *spec-vs-reality* limbo. | `INITIATIVE_REGISTRY.csv` row I65 `status: closed` + `closure_decision_id` set + ERP browser MCP UAT in `docs/wip/planning/65-akos-planning-workspace-panel/reports/uat-i65-*.md` |
| **A2** | **≥ 1 customer engagement in flight** (J-CU activation per [`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) §5 J-CU activation trigger: *"first commercial engagement at Holistika sub-mark scale"*) | Without a real customer engagement, the J-CU row's audit is theoretical (no proposal PDF, no mail-render trail, no ERP customer-portal use case to dogfood). The audit must **inspect a real engagement folder** under `docs/references/hlk/v3.0/Think Big/Clients/<engagement-slug>/` to evidence the J-CU column. | `_assets/advops/<plane>/<program>/<engagement>/manifest.md` exists with `audience: J-CU` and rendered surfaces present |
| **A3** | **≥ 1 investor engagement in flight** (J-IN activation per [`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) §5 J-IN activation trigger: *"first investor outreach campaign"*) | Same logic as A2 for the J-IN column. The 2026-04-29 ENISA dossier work (`PRJ-HOL-FOUNDING-2026`) is regulator-class (J-ENISA), not investor-class (J-IN); investor surfaces remain partial per Lane VISIBILITY-SWEEP §3.1 ("partial — deck HTML/PDF pipeline exists; investor-specific surfaces vary by engagement"). | An engagement folder under `_assets/advops/founder-filed/` or `_assets/investor-relations/` with `audience: J-IN` frontmatter and rendered investor dossier PDF + manifest |

### 2.2 Why AND-gate (not OR-gate)

The audit's *value* is the cross-audience routing inventory — a single-audience evidence pass would produce a partial matrix, which is the same shape as the current Lane VISIBILITY-SWEEP report (already shipped in Wave I CHARTER). The AND-gate ensures the audit produces **comprehensive routing-truth** per the doctrine's full-spectrum scope (D-IH-86-AJ).

### 2.3 What happens if an activation criterion lingers

Per Option 5 default posture's tracker hygiene rule: when a single criterion blocks for > 90 days, this candidate's status transitions to **`blocker-tracker`** (folder move from `_candidates/` to `_blockers/`) per `akos-conflict-surfacing-and-blocker-trackers.mdc` §"Blocker-tracker file shape". Until then, the candidate-shape is correct because the activation criteria are *expected to clear within Wave J+ pacing* (I65 lands in Wave I; first customer / investor engagements anchor Wave J+ per master-roadmap Wave dependency diagram).

## 3. Forward-charter scope (when promoted)

When all three A1+A2+A3 gates clear, this candidate promotes to active with the following minimal shape:

### 3.1 Audit deliverables

1. **Per-audience routing-matrix evidence pass** — for each J-\* code, populate the [`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) §4 routing-matrix row with: shipped surface paths, render mechanism verification, audience-tag frontmatter coverage, BBR drift-gate status, render-trail status, ERP-browser column status (live route URL or `reserved`).
2. **Drift findings register** — every row that fails one of (a) shipped vs spec; (b) audience-tag coverage; (c) render-trail; (d) BBR external-register translation; (e) ERP-browser implementation. Findings file under `reports/audit-findings-<YYYY-MM-DD>.md`.
3. **Top-N gap fix forward-charter** — RICE-ranked list of audit findings; gap fixes that warrant standalone initiatives forward-chartered as `I-NN-<slug>` candidates in `_candidates/`; minor fixes folded into existing OPS rows or absorbed into I86 / I89 follow-up.
4. **`OPERATIONAL_COHESION_DOCTRINE.md` last_review_at: bump** — doctrine's freshness tier resets to `fresh` on audit completion; per-audience row content updated based on findings.
5. **(Conditional) `unified_operator_dashboard_render` orchestrator** — per `D-IH-86-AL` forward-charter, if the audit confirms multiple render scripts produce the operator-facing landing page, mint a `RENDERING_PIPELINE_REGISTRY.csv` row + paired runbook. Conditional because today's landing page is single-script-per-section (no orchestrator needed).

### 3.2 Phase shape (provisional; ratified at P0 charter)

| Phase | Effort | Deliverable | Gate |
|:---|:---|:---|:---|
| P0 — Charter | 0.5d | Inline-ratify open conundrums (audit cadence: one-shot vs quarterly; per-audience evidence depth: surface-path-only vs full-render-trail; deliverable register: standalone CSV vs doctrine §4 row updates); mint INITIATIVE_REGISTRY + DECISION_REGISTER rows | operator approval |
| P1 — Per-audience evidence pass | 3-5d | Per-audience evidence sweep across §4 routing matrix; one report per audience (8 audiences × 1 report each, batched into 2-3 sweep reports for AKOS internal, external delivery, ERP-browser) | inline-ratify per audience batch |
| P2 — Drift findings register | 1d | `reports/audit-findings-<YYYY-MM-DD>.md` with RICE-ranked findings; cross-link to existing OPS / DECISION rows | operator approval (canonical-CSV-gate if findings produce new `OPS_REGISTER.csv` / new candidate stubs) |
| P3 — Doctrine sync + closure | 1d | [`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) per-audience rows updated; `last_review_at` bumped; closure decision ratified; CHANGELOG entry | operator approval |
| **Total** | **~5-7d** | | |

### 3.3 Open conundrums (resolve at P0 charter via inline-ratify)

| ID | Question | Default verdict | Decision target |
|:---|:---|:---|:---|
| C-90-1 | Audit cadence: one-shot at activation, or quarterly cadence registered as `process_list.csv` row paired with runbook? | One-shot at activation; quarterly cadence forward-chartered to a successor I-NN if drift becomes recurring | D-IH-90-A |
| C-90-2 | Per-audience evidence depth: surface-path-only inventory vs full-render-trail (sha256 manifest verification per audience surface) | Full-render-trail for J-IN / J-ENISA / J-AD (high-stakes external delivery); surface-path-only for J-OP / J-AIC / J-PT / J-CU / J-RC / J-CO at v1 | D-IH-90-B |
| C-90-3 | Findings register: standalone canonical CSV vs doctrine §4 row updates only | Doctrine §4 row updates only at v1 (no new register); findings file at `reports/audit-findings-<YYYY-MM-DD>.md` is the per-run evidence | D-IH-90-C |
| C-90-4 | Cross-area coordination: should this audit ride alongside [I85](i85-audience-tag-canonicalization.md) closure work or stay separate? | Separate (I85 closes the *tagging* mechanic; I90 audits the *routing-matrix* per-audience reality — different governance axis, less coupling) | D-IH-90-D |
| C-90-5 | Audit owner role: PMO + System Owner co-own (matches I86 Wave I Lane I-B doctrine ownership), or Brand & Narrative Manager + System Owner (audience-class authority + render-trail authority)? | PMO + System Owner co-own; Brand & Narrative Manager consulted on J-IN / J-CU / J-PT / J-RC audience-class questions | D-IH-90-E |

## 4. Cross-references and wiring

- **Origin**: I86 Wave I CHARTER `D-IH-86-AG` (Wave I composition Q1=E sweep-recommended combo) + `D-IH-86-AJ` (Q4=D full-audience-spectrum scope) + Lane VISIBILITY-SWEEP §3 (HLK external visibility audit; partial across audiences).
- **Doctrine to audit**: [`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) §4 routing matrix + §5 per-audience extension contract — the audit populates the per-audience rows with evidenced status.
- **Lane VISIBILITY-SWEEP evidence carry-forward**: [`reports/lane-visibility-sweep-2026-05-19.md`](../86-initiative-cluster-execution-coordinator/reports/lane-visibility-sweep-2026-05-19.md) §3 HLK external visibility (already names registry vs shipped drift); the audit deepens this per-audience.
- **Sibling registry to consume**: [`AUDIENCE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) (I85 closed; SSOT for J-\* codes + activation triggers); [`RENDERING_PIPELINE_REGISTRY.csv`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv) (per-pipeline render contracts).
- **ERP-side dependency**: I65 Lane I-D delivery (this Wave I) ships `/operator/planning/` — required precondition A1.
- **Paired drift gate to consume**: [`scripts/validate_external_render_trail.py`](../../../../scripts/validate_external_render_trail.py) `--strict --strict-freshness` (FAIL gate; Wave F closure); [`scripts/validate_audience_tags.py`](../../../../scripts/validate_audience_tags.py) (I85 P3 closure); [`scripts/validate_brand_baseline_reality_drift.py`](../../../../scripts/validate_brand_baseline_reality_drift.py) (I66 closure); [`scripts/render_operational_cohesion_index.py`](../../../../scripts/render_operational_cohesion_index.py) (Lane I-B mint; `validate` subcommand).
- **Forward-charter ascendants**: when audit findings warrant standalone initiatives, mint `I-NN-<slug>` candidates in `_candidates/` (potential names: `I-NN-investor-surface-rollout`, `I-NN-customer-portal-erp-implementation`, `I-NN-recruiter-deck-rollout` once J-RC activates per I75); when findings are minor, fold into existing OPS rows.
- **Governing rules**: [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) (Option 5 default posture; this candidate's authoring contract) + [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) (audience × channel × format triplet; the audit's structural lens) + [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) (initiative discipline + UAT-evidence contract; audit findings live in `reports/`) + [`akos-applied-research-discipline.mdc`](../../../../.cursor/rules/akos-applied-research-discipline.mdc) (the audit's research-sweep posture per Wave H Lane D mint).

## 5. Files this candidate will mint (when promoted)

When promoted to active, the initiative folder `docs/wip/planning/90-visibility-audit-and-routing/` will mint the standard 6 governance artefacts (master-roadmap.md / decision-log.md / asset-classification.md / evidence-matrix.md / risk-register.md / files-modified.csv) plus:

- **NEW** `reports/audit-findings-<YYYY-MM-DD>.md` (P2 deliverable)
- **NEW** per-audience evidence reports (P1 deliverables; 2-3 batched files)
- **MODIFIED** [`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) per-audience rows (P3 sync)
- **MODIFIED** [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) (registry append at promotion + closure decision at P3)
- **MODIFIED** [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) (D-IH-90-A..E + closure)
- **CONDITIONAL** new `_candidates/I-NN-<slug>.md` files for any audit findings that warrant standalone initiatives (per scope §3.1 item 3)

## 6. Promotion criteria (to active initiative folder under `docs/wip/planning/90-visibility-audit-and-routing/`)

All three required (per D-IH-86-AP):

1. **A1**: I65 closed in `INITIATIVE_REGISTRY.csv` + ERP UAT report present.
2. **A2**: ≥ 1 customer engagement in flight with rendered artefacts under `_assets/advops/**` (`audience: J-CU` frontmatter present).
3. **A3**: ≥ 1 investor engagement in flight with rendered artefacts under `_assets/advops/**` or `_assets/investor-relations/**` (`audience: J-IN` frontmatter present).

When A1 + A2 + A3 met simultaneously, the next operator scratchpad / inline-ratify gate may promote this candidate. Promotion authoring follows the standard candidate-to-active flow per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) (mint folder + 6 standard artefacts + INITIATIVE_REGISTRY append + master-roadmap.md per plan-quality bar for ≥ 5-phase initiatives — but this is a < 5-phase audit so the bar is the standard governance content requirements only).

## 7. Tracker review cadence

Per `akos-conflict-surfacing-and-blocker-trackers.mdc` candidate hygiene: this file's `last_review` is updated whenever any of the three activation criteria flips state (A1 closure, A2 first customer engagement, A3 first investor engagement) — at minimum at every Wave J+ boundary. If activation criteria linger > 90 days, this file moves to `_blockers/` per the rule's tracker-state-transition contract.

