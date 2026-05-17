---
title: SOP - Research Substrate Audit Cadence
language: en
intellectual_kind: research-area-canonical-sop
sop_id: SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Research Lead
  - KM Officer
  - System Owner
last_review: 2026-05-17
last_review_by: Research Lead
last_review_decision_id: D-IH-84-H
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-84-A
  - D-IH-84-G
  - D-IH-84-H
status: review
register: internal
linked_canonicals:
  - SUBSTRATE_LANDSCAPE_DOCTRINE.md
  - SUBSTRATE_REGISTRY.csv
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - PRECEDENCE.md
  - confidence_levels.md
  - source_taxonomy.md
linked_runbooks:
  - scripts/peopl_research_substrate_audit_cadence.py
linked_processes:
  - env_tech_dtp_substrate_landscape_mtnce_001
companion_to:
  - SUBSTRATE_LANDSCAPE_DOCTRINE.md
cadence: scheduled
cadence_schedule: quarterly
cadence_secondary: event_triggered
cadence_secondary_trigger: material substrate event (GA transition, major version bump, regulatory enforcement date, sunset / migration to deprecated)
---

# SOP - Research Substrate Audit Cadence

## Purpose

Operationalise the continuous Research-area substrate-audit discipline that the [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](SUBSTRATE_LANDSCAPE_DOCTRINE.md) names. Research is the **meta-discipline** that audits which substrates earn the right to canonical status (per `D-IH-84-G` discipline-of-disciplines posture applied recursively to Research-area). This SOP defines how that audit happens on a cadence the substrate landscape's velocity demands: who audits, who reviews, what gets registered, what gets superseded, where evidence lives, and how cross-area handoff fires when material change accrues.

Paired with the runbook [`scripts/peopl_research_substrate_audit_cadence.py`](../../../../../../../scripts/peopl_research_substrate_audit_cadence.py) per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (every executable SOP carries a paired executable runbook). Either Research Lead (or KM Officer + Founder interim per `D-IH-84-H` pre-Research-Director hire) can run the audit via this SOP, or the runbook fires off-cadence on a material-substrate-event trigger. Both surfaces are SSOT for the same process.

The supersession context: this SOP + paired runbook **replace** the I12 + I13 vendor-handoff Madeira-research-request lineage (per [`master-roadmap.md`](../../../../../../../docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) §1 + §10) with an internal Research-area continuous discipline that produces dated quarterly substrate-audit reports under `docs/wip/intelligence/substrate-audit-YYYY-QN/` per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) section 17 Tier-1 WIP convention.

## Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 section 5 (every executable process catalog entry must declare both acceptance paths):

- **`acceptance_criteria_human`**: a human (Research Lead, KM Officer, Founder, or an AIC role_owner per the I76 forward-charter F1-F5 framings) can execute every step in this SOP without invoking the paired runbook, by reading the canonicals it references and authoring the dated quarterly report manually under `docs/wip/intelligence/substrate-audit-YYYY-QN/`. The audit cycle completes successfully when (a) all 5 audit elements per section 3 ship; (b) [`SUBSTRATE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) `last_audit_date` columns are updated for any row touched; (c) cross-area handoff fires per section 6 if material change accrues.
- **`acceptance_criteria_automation`**: the paired runbook [`scripts/peopl_research_substrate_audit_cadence.py`](../../../../../../../scripts/peopl_research_substrate_audit_cadence.py) fires unattended (cron / event-trigger / dispatch-script) and (a) `--staleness-check` returns exit 0 when no row's `last_audit_date` is > 90 days old; (b) `--uat-mode <quarterly-report-path>` returns exit 0 when the freshly-committed quarterly report parses cleanly + cross-references resolve; (c) `--emit-delta <prior-q-path> <current-q-path>` produces a parsable Markdown delta report.

Both paths satisfy the same acceptance contract; neither is privileged.

## Scope

**In scope.** The audit cycle that produces:

- A dated quarterly substrate-audit report at `docs/wip/intelligence/substrate-audit-YYYY-QN/YYYY-QN-substrate-audit.md` per the 5-element structure in section 3 below.
- Per-substrate updates to [`SUBSTRATE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) (`last_audit_date`, `status`, `akos_integration_state`, and any other row-attribute drift).
- Optional new substrate-row mints when net-new substrates warrant canonical status (operator-gated canonical-CSV gate per [`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers" pattern + [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance" canonical-CSV gates).
- Optional supporting Tier-1 WIP threads under the same dated folder (competitive layer; regulatory + ToS; past-PoC translation) per the founder-directive 2026-05-16 four-thread audit pattern.
- Cross-area handoff per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) when material substrate change pings the Tech-Lab [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) or People-side [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) canonicals.

**Out of scope.** Architectural-shape ratification decisions on substrate baseline (`D-IH-84-B`), AIC framing (`D-IH-84-C`), MADEIRA productization (`D-IH-84-D`), KiRBe framework narrowing (`D-IH-84-E`). Those are operator-gated initiative-level decisions; this SOP produces the evidence those decisions ratify against, not the ratifications themselves. Also out of scope: ratifying which substrates promote to canonical row status (canonical-CSV gate per [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc); operator-gated even when the audit recommends).

## Inputs

- [`SUBSTRATE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) - the canonical state-of-record (18 rows as of 2026-Q2; 18-column schema per `D-IH-84-F`).
- [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](SUBSTRATE_LANDSCAPE_DOCTRINE.md) - the Research-area canonical this SOP operationalises.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) - the Tech-Lab canonical; the substrate audit consults this for the operational "how" companion.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) - the People canonical; the substrate audit consults this for the agentic "why-and-what" companion.
- The prior quarter's audit report at `docs/wip/intelligence/substrate-audit-YYYY-QN/YYYY-QN-substrate-audit.md` (or the founding Q2 2026 baseline at `docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`) - establishes the delta baseline for `--emit-delta` runs.
- [`confidence_levels.md`](../../../People/Compliance/canonicals/confidence_levels.md) - the A1-B2-C3-D4 confidence taxonomy for per-row attribute claims.
- [`source_taxonomy.md`](../../../People/Compliance/canonicals/source_taxonomy.md) - the source-class vocabulary for evidence citations.
- External research substrate sources: vendor docs, GitHub repos, regulatory texts (per `[ext]` flag discipline used in the founding 2026-Q2 audit).

## Steps

### 1. Schedule the cycle

Two cadence triggers:

- **Scheduled (primary).** Quarterly per `D-IH-84-H` ratification; aligned with calendar quarters (audit windows: Q1 = Feb-Mar; Q2 = May-Jun; Q3 = Aug-Sep; Q4 = Nov-Dec). The owning role (Research Lead, or KM Officer + Founder interim) schedules the audit window 2 weeks before quarter-close to allow execution + cross-area handoff before the next quarter.
- **Event-triggered (secondary).** Material substrate event: vendor GA transition (e.g., Cursor SDK GA), major version bump (e.g., LangChain v0.4), regulatory enforcement date (e.g., EU AI Act 2026-08-02 high-risk), substrate sunset / migration to deprecated, or cross-area breakthrough propagation ping from Tech Lab (AGENTIC_FRAMEWORK_LANDSCAPE.md extension) / People (HOLISTIKA_AGENTIC_DOCTRINE.md revision). Off-cycle audit fires per same SOP flow but may be scoped to the triggering substrate only.

The audit cycle ID is `substrate-audit-YYYY-QN` (per WORKSPACE_BLUEPRINT_HOLISTIKA section 17 Tier-1 WIP convention); off-cycle audits append a suffix (e.g., `substrate-audit-2026-Q3-off-cycle-cursor-ga`).

### 2. Open the working folder

Create or confirm the folder `docs/wip/intelligence/substrate-audit-YYYY-QN/` exists. Per the prior-cycle convention, the folder carries a `README.md` with thread index + scope frontmatter; subsequent files land under the same folder. Per [`PRECEDENCE.md`](../../../People/Compliance/canonicals/PRECEDENCE.md) classification: Tier-1 WIP working space; access_level: 5; not canonical until rows promote.

### 3. Execute the 5-element audit

Per [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](SUBSTRATE_LANDSCAPE_DOCTRINE.md) section 3 (the 5-element audit shape) - each cycle produces:

1. **Substrate landscape audit** - per-substrate structured rows refreshed against current state. Update `last_audit_date` for every row touched. Net-new substrates surfaced are recorded as candidates pending canonical row mint at the operator-gated CSV gate.
2. **Substrate scorecard** - per-substrate per-dimension scoring across the 6 governance dimensions (governance fit, operator-runtime maturity, cost, lock-in risk, AKOS-as-SSOT compatibility, MADEIRA elevation alignment). Methodology per the founding 2026-Q2 scorecard at [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md`](../../../../../../../docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md).
3. **Competitive-layer positioning** - per-competitor analysis of vendors whose products overlap or could displace Holistika's value proposition. Methodology per the founding 2026-Q2 analysis at [`docs/wip/intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md`](../../../../../../../docs/wip/intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md).
4. **Regulatory + ToS forecast** - per-regulatory-topic analysis of substrate-relevant law + contract surfaces. Methodology per the founding 2026-Q2 analysis at [`docs/wip/intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md`](../../../../../../../docs/wip/intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md). When material regulatory exposure is identified, recommend ADVOPS engagement per [`akos-adviser-engagement.mdc`](../../../../../../../.cursor/rules/akos-adviser-engagement.mdc) workflow.
5. **Past-PoC translation matrix** - per-prior-initiative analysis of substrate learnings translatable to current version. Methodology per the founding 2026-Q2 analysis at [`docs/wip/intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md`](../../../../../../../docs/wip/intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md).

Each element produces a stand-alone Tier-1 WIP file under the dated folder; the consolidated cycle report `YYYY-QN-substrate-audit.md` synthesises across the 5 elements.

### 4. Cross-reference SUBSTRATE_REGISTRY rows in the consolidated cycle report

The cycle report MUST cite SUBSTRATE_REGISTRY row IDs (FK to the canonical) for every substrate referenced. The paired runbook `--uat-mode` flag validates cross-reference resolution mechanically; ungrounded references are caught at the verification step (step 7).

### 5. Update SUBSTRATE_REGISTRY rows in place

Per the regular row-update pattern:

- **Row attribute drift** - any row whose attributes shifted (status change; new pricing tier; new tool protocol; new akos_integration_state) is updated in place with the new value AND the `last_audit_date` advanced to today's ISO date. This is a canonical-CSV edit gated per [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"Canonical CSV gates" - operator approval required before commit; the audit cycle prepares the diff but does not commit unilaterally.
- **New row mints** - net-new substrates that warrant canonical status are proposed via a per-row CSV diff + Pydantic-load proof via [`scripts/validate_substrate_registry.py`](../../../../../../../scripts/validate_substrate_registry.py). Operator-gated mint approval at the same canonical-CSV gate.
- **Status promotions / demotions** - `forecasted` → `candidate` → `pilot` → `active`; `active` → `deprecated`; `candidate` / `experimental` → `rejected` (per the founding-cycle Devin + Replit Agent reclassification precedent). All canonical-CSV-gated.

### 6. Cross-area handoff (when material change accrues)

When the audit produces material change to the canonical-state-of-record, fire the cross-area breakthrough propagation per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md). Material-change examples:

- A new substrate row mints with `akos_integration_state: pilot` or `in-production` (Tech Lab consumes for AGENTIC_FRAMEWORK_LANDSCAPE.md extension; People consumes for HOLISTIKA_AGENTIC_DOCTRINE.md cross-reference review if AIC framing implications surface).
- An existing substrate row demotes to `deprecated` (Tech Lab consumes for migration planning; affected initiatives consume for plan adjustments).
- An existing substrate row's `madeira_productization_role` or `aic_pattern_role` shifts (cross-area pings to I74, I76, I83 owning initiatives if active or post-charter).
- Net-new regulatory exposure surfaces (Marketing + Legal + Brand consume for brand-baseline-reality / dual-register / public-prose audit; ADVOPS engagement recommendation surfaces per the founding-cycle pattern).

Per the SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001 workflow: surface the propagation digest as Tier-2 WIP under the initiative folder, ping consuming areas, and record adoption decisions in their respective area registers.

### 7. Run paired runbook verification

Before the cycle's commit batch lands, run:

- `py scripts/peopl_research_substrate_audit_cadence.py --staleness-check` - confirm no SUBSTRATE_REGISTRY row's `last_audit_date` is > 90 days old (quarterly cadence boundary). Exits 0 PASS or 1 FAIL with structured row list.
- `py scripts/peopl_research_substrate_audit_cadence.py --uat-mode <quarterly-report-path>` - confirm the freshly-committed report parses cleanly + cross-references to SUBSTRATE_REGISTRY rows resolve. Exits 0 PASS or 1 FAIL with structured error report.
- `py scripts/validate_substrate_registry.py` - confirm the 18-column schema integrity + per-row Pydantic validation + status counts.
- `py scripts/validate_hlk.py` - umbrella sanity check covering all canonical-CSV gates.

Failures halt the cycle close; the audit author re-runs after correction.

### 8. Commit + close

Per [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"Commit and phase discipline" - one commit per logical scope, validators green before commit, files-modified.csv row(s) appended per [`akos-planning-traceability.mdc`](../../../../../../../.cursor/rules/akos-planning-traceability.mdc) §"Per-initiative file-changes CSV" 18-col schema (when the audit lands under an active initiative folder; when standalone, the chronicled-quarterly-audit pattern lives at the Tier-1 WIP folder + cross-references the cycle ID).

Author the cycle close note as `docs/wip/intelligence/substrate-audit-YYYY-QN/closure-note.md` (or commit-message body when minor cycle) declaring: cycle-ID, audit-date, owning-role, summary findings, registry deltas (rows touched + rows minted + rows demoted), cross-area handoffs fired, follow-on actions (if any). Cross-link to [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](SUBSTRATE_LANDSCAPE_DOCTRINE.md) for context.

## Outputs

Per cycle, the following artefacts MUST exist:

- **Cycle report.** `docs/wip/intelligence/substrate-audit-YYYY-QN/YYYY-QN-substrate-audit.md` - the consolidated 5-element audit synthesis.
- **Per-element Tier-1 WIP threads.** Stand-alone files for the audit / scorecard / competitive / regulatory / past-PoC elements when each element warrants standalone depth.
- **SUBSTRATE_REGISTRY.csv row updates.** `last_audit_date` advanced for every row touched; attribute drift propagated; net-new row mints proposed.
- **Cross-area handoff digests.** When material change fires per step 6; under the consuming-area folder per SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.
- **Closure note.** Short narrative summarising cycle outcomes; cross-linked from the cycle report.

Per cycle, the following are optional:

- **Off-cycle update reports** when material substrate events warrant intra-quarter updates.
- **ADVOPS engagement recommendations** when regulatory exposure surfaces (per the founding-cycle precedent at [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md`](../../../../../../../docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/advops-engagement-scoping-2026-05-17.md)).
- **New initiative charters** when the audit identifies a substrate transition warranting initiative-level scoping (e.g., a future I-NN dedicated to a specific substrate migration).

## Failure modes

| Failure | Detection | Remediation |
|:---|:---|:---|
| Audit cycle slips past quarter-close | Staleness check exit 1 (rows > 90 days) | Owning role schedules immediate catch-up cycle; per `R-IH-84-5` mitigation - interim owner (KM Officer + Founder) covers if Research Lead unavailable |
| Cycle report doesn't cite SUBSTRATE_REGISTRY rows | `--uat-mode` exit 1 | Audit author re-runs after adding row-ID citations |
| Substrate landscape moves faster than quarterly cadence | Per `R-IH-84-6` - off-cycle event-triggered audit | Trigger event-cadence run per step 1 secondary cadence; intra-quarter update report under same folder |
| Material substrate change misses cross-area handoff | Step 6 self-check at cycle close | Backfill cross-area digest per SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001 within 5 business days |
| New substrate proposed but operator gate doesn't fire | Audit shelves the proposal in cycle report; flags for next-cycle re-review | Operator scheduling concern, not SOP failure - audit cycle ships without the mint and re-proposes at next cycle |
| Pydantic validation fails on SUBSTRATE_REGISTRY edit | `validate_substrate_registry.py` exit 1 | Pre-commit gate per [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) verification matrix; correct the row + re-validate |

## Verification

Mechanical verification per step 7 above:

- `py scripts/peopl_research_substrate_audit_cadence.py --staleness-check` - exit 0 PASS
- `py scripts/peopl_research_substrate_audit_cadence.py --uat-mode <path>` - exit 0 PASS
- `py scripts/validate_substrate_registry.py` - exit 0 PASS
- `py scripts/validate_hlk.py` umbrella - exit 0 PASS
- `py scripts/release-gate.py` - exit 0 PASS

Profile wiring: `substrate_audit_smoke` profile in [`config/verification-profiles.json`](../../../../../../../config/verification-profiles.json) runs the staleness-check + the dedicated test suite (`tests/test_peopl_research_substrate_audit_cadence.py`). Operator can invoke via `py scripts/verify.py substrate_audit_smoke`.

Qualitative verification:

- Cycle report carries the 5-element structure
- All cited SUBSTRATE_REGISTRY rows resolve to actual canonical rows
- Cross-area handoff digests landed where material change accrued
- Methodology-portability axis (per SUBSTRATE_LANDSCAPE_DOCTRINE section 4 principle 1) is honored - no substrate-induced canonical migration without explicit operator gate
- Brand-baseline-reality dual-register held when audit prose references customer-facing copy per [`akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)

## Cross-references

- [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](SUBSTRATE_LANDSCAPE_DOCTRINE.md) - paired Research-area canonical (this SOP operationalises its cadence).
- [`SUBSTRATE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) - canonical state-of-record; this SOP updates rows + proposes mints.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) - Tech-Lab canonical; consumes substrate-audit outputs via cross-area handoff.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) - People canonical; consumes substrate-audit outputs when AIC framing implications surface.
- [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) - cross-area handoff workflow this SOP fires per step 6.
- [`SOP-META_PROCESS_MGMT_001.md`](../../../People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md) - SOP-META ordering (process_list row before SOP status:active); this SOP stays at `status: review` until process_list row `env_tech_dtp_substrate_landscape_mtnce_001` mints.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) section 17 - Tier-1 WIP folder convention this SOP follows for `substrate-audit-YYYY-QN/` placement.
- [`scripts/peopl_research_substrate_audit_cadence.py`](../../../../../../../scripts/peopl_research_substrate_audit_cadence.py) - paired runbook.
- [`tests/test_peopl_research_substrate_audit_cadence.py`](../../../../../../../tests/test_peopl_research_substrate_audit_cadence.py) - test coverage for the paired runbook CLI modes.
- [`config/verification-profiles.json`](../../../../../../../config/verification-profiles.json) - `substrate_audit_smoke` profile wiring.
- [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 - paired SOP+runbook pattern this SOP follows.
- [`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers" - canonical-CSV gate pattern for SUBSTRATE_REGISTRY mints + edits.
- [`akos-adviser-engagement.mdc`](../../../../../../../.cursor/rules/akos-adviser-engagement.mdc) - ADVOPS workflow when audit surfaces regulatory exposure.
- [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md`](../../../../../../../docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) - I84 master-roadmap; this SOP is the P6 deliverable (paired with the doctrine canonical).
- [`docs/wip/planning/_candidates/i75-research-area-governance.md`](../../../../../../../docs/wip/planning/_candidates/i75-research-area-governance.md) Strand C - Research-Director hire + KM Officer + Founder interim ownership posture this SOP inherits.

## Status

**status: review** per master-roadmap section 3 P6 + SOP-META ordering rule (per [`SOP-META_PROCESS_MGMT_001.md`](../../../People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md) sections 4.2-4.3). Promotes to **status: active** after the process_list.csv row `env_tech_dtp_substrate_landscape_mtnce_001` is minted (operator-gated canonical-CSV gate tranche; not in this commit). Promotion authorisation: Founder + Research Lead (or KM Officer + Founder interim per `D-IH-84-H`).

## Provenance

Authored at I84 Wave A2 (parallel-to-P4-foreground gate per I86 successor-pickup) 2026-05-17. Paired with the doctrine canonical [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](SUBSTRATE_LANDSCAPE_DOCTRINE.md) and the runbook [`scripts/peopl_research_substrate_audit_cadence.py`](../../../../../../../scripts/peopl_research_substrate_audit_cadence.py). First execution cycle: 2026-Q2 audit landing at [`docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`](../../../../../../../docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md) (the founding-cycle baseline). Owner pre-Research-Director: KM Officer + Founder interim per `D-IH-84-H`. Owner post-Research-Director: Research Lead.
