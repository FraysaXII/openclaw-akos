---
language: en
status: review
canonical: true
role_owner: Compliance
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: Compliance
last_review_decision_id: D-IH-72-I
methodology_version_at_review: v3.0
companion_to:
  - dimensions/INTELLIGENCEOPS_REGISTER.csv
  - SOP-IO_INTELLIGENCE_REPORT_001.md
  - SOP-IO_ELICITATION_DISCIPLINE_001.md
  - ../../People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md
---

# SOP-REGULATOR_RELATIONSHIP_001 — Regulator-relationship operating contract

> Authored I72 P6 per `D-IH-72-A` (P0 charter) + `D-IH-72-H` (sibling INTELLIGENCEOPS_REGISTER canonical) + `D-IH-72-I` (regulator-relationship roadmap = generic SOP + ENISA worked-example annex). Codifies how Holistika maintains a deterministic intelligence-collection contract with regulators (public bodies whose criteria, decisions, or correspondence shape Holistika's runway). Generic body applies to any regulator; ENISA worked example in §10 annex is the live concrete instance per `D-IH-70-AC` GOI/POI hunt seed.

## 1. Purpose

Establish a uniform contract for relationship management with regulator-class targets in `INTELLIGENCEOPS_REGISTER.csv`:

1. **Distance-band trajectory**: explicit posture for moving from N3-N4 (cold; reading public criteria only) → N2 (bridged via adviser firm or public consultation comment) → N1 (direct correspondence).
2. **Cadence discipline**: per-cycle review; refresh evidence pack on schedule; surface regulator decisions promptly.
3. **Reliability progression**: starts at C (fairly reliable; OSINT public criteria); upgrades to B (usually reliable; via bridge HUMINT) and to A (completely reliable; direct correspondence).
4. **Stance discipline**: regulators stay `neutral` until concrete posture emerges (loan approved/denied; license granted/revoked; investigation closed/escalated). Stance assessment is a deliberate act, not an assumption.
5. **Output artifact discipline**: every regulator engagement produces an evidence-pack updated artifact under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/<REGULATOR>_EVIDENCE_PACK_*.md` per ENISA precedent.

## 2. Scope

In scope:
- Any target in `INTELLIGENCEOPS_REGISTER.csv` with `target_class=regulator`.
- The regulator's GOI row in `GOI_POI_REGISTER.csv` (entity-side; `class=investor` or future `class=regulator` enum if minted).
- Cross-area relationships: Compliance owns; PMO observes; CFO consumes outputs for capital-readiness decisions.

Out of scope:
- Per-regulator certification SOPs (e.g., ISO 27001 vs ENISA participative-loan vs SOC 2 — each gets its own certification SOP, this SOP is the GENERIC relationship-management contract).
- Certification deliverable authoring (covered by the per-regulator certification SOP).

## 3. Inputs

- The regulator's row in `INTELLIGENCEOPS_REGISTER.csv` (target_id, cadence, source_type, reliability, output_artifact, responsible_role).
- The regulator's row in `GOI_POI_REGISTER.csv` (distance_band, bridge_via, stance, voice_register, language_preference).
- The regulator's public-criteria document (when one exists); the regulator's published decisions (when published); the regulator's contact channels (public + bridged via adviser firm).
- Relevant `process_list.csv` rows under `Compliance` ownership.

## 4. Steps

### 4.1 Pre-cycle assembly (T-7 days from cadence trigger)

The role_owner (Compliance) assembles:

1. **Public-criteria delta**: did the regulator publish updated criteria since last cycle?
2. **Bridge HUMINT**: any new signals from the bridge (adviser firm, peer founder, public consultation responses)?
3. **Internal-status delta**: did Holistika's status against the regulator's criteria materially change since last cycle?

### 4.2 Cycle execution (T-0)

1. **Refresh evidence pack**: update the per-regulator evidence pack artifact under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/<REGULATOR>_EVIDENCE_PACK_*.md` reflecting the deltas from §4.1.
2. **Update INTELLIGENCEOPS_REGISTER.csv row**: refresh `last_review_at` + `last_review_by` + `last_review_decision_id` + the reliability cell if source-grade has shifted.
3. **Surface stance reassessment**: if a concrete decision (loan approved/denied; license granted/revoked) has landed since last cycle, update the GOI_POI_REGISTER `stance` cell from `neutral` to `ally` or `enemy` per `GOI_POI_STANCE_DOCTRINE.md` (D-IH-70-AD). Stance changes are operator-gated.
4. **Distance-band trajectory check**: if direct correspondence has been initiated since last cycle, update GOI_POI_REGISTER `distance_band` from N2 to N1 + clear `bridge_via` cell.

### 4.3 Post-cycle handoff (T+7 days)

1. **CFO briefing**: surface any capital-readiness implications from the cycle update. Inputs into the next QBR per `SOP-REVOPS_QBR_001.md` (Operations/RevOps/canonicals/).
2. **PMO observation**: log cycle outcome to `PMO_HUB_LOG.md` (or successor) as an observable event.

## 5. Outputs

- Updated evidence-pack artifact under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/<REGULATOR>_EVIDENCE_PACK_*.md`.
- Refreshed `INTELLIGENCEOPS_REGISTER.csv` row (audit-trail columns + reliability cell as appropriate).
- 0+ stance / distance changes in `GOI_POI_REGISTER.csv` (operator-gated).
- 0+ decision rows in `DECISION_REGISTER.csv` for stance reassessments.

## 6. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **`acceptance_criteria_human`**: Compliance role_owner runs the §4 cycle manually using only this SOP body; evidence pack refresh is auditable; reliability + distance + stance reassessments documented and reviewable.
- **`acceptance_criteria_automation`**: `validate_intelligenceops_register.py` PASS on the updated row (audit-trail + lifecycle_status); `validate_hlk.py` PASS on the GOI_POI_REGISTER stance/distance changes.

## 7. Failure modes

- **Public criteria document not yet published**: skip §4.2.1 evidence-pack refresh; document in cycle notes; resume next cycle.
- **Bridge HUMINT inconsistent across sources**: lower reliability cell from B to C until reconciled; flag for next cycle.
- **Concrete decision arrives outside cycle**: trigger ad-hoc cycle (cadence flips temporarily to `event_triggered`); update register row + propose stance reassessment.
- **Operator unavailable for stance reassessment**: keep stance=`neutral`; defer to next cycle.

## 8. Failure escalation

If the regulator's decision is genuinely adversarial (license denied, sanctions, investigation), escalate per `SOP-IO_INTELLIGENCE_REPORT_001.md` §5 escalation matrix + invoke executive-layer review (Founder + CMO + COO when activated).

## 9. Cross-references

- Sibling Intelligence SOPs: [`SOP-IO_INTELLIGENCE_REPORT_001.md`](SOP-IO_INTELLIGENCE_REPORT_001.md) (per-cycle intelligence reporting standard) + [`SOP-IO_ELICITATION_DISCIPLINE_001.md`](SOP-IO_ELICITATION_DISCIPLINE_001.md) (HUMINT elicitation hygiene).
- Cross-area sister SOP: `SOP-REVOPS_QBR_001.md` (Operations/RevOps/canonicals/) — regulator decisions feed forward-pipeline confidence calibration at QBR cadence.
- Doctrine: [`GOI_POI_STANCE_DOCTRINE.md`](../../../../Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md) (D-IH-70-AD).
- Canonical: [`dimensions/INTELLIGENCEOPS_REGISTER.csv`](dimensions/INTELLIGENCEOPS_REGISTER.csv).
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 1 + 3 + 4 + 5.
- Decisions: `D-IH-72-H` (sibling canonical), `D-IH-72-I` (this SOP charter), `D-IH-70-AC` (forward-charter context), `D-IH-72-Q` (cadence taxonomy).

## 10. ENISA worked-example annex

Per `D-IH-72-I`, ENISA (Empresa Nacional de Innovación SA — Spanish state-backed startup capital provider) is the live worked example.

### 10.1 ENISA register row context

- `register_id`: `IO-REG-ENISA-2026-001`
- `target_id`: `GOI-INV-ENISA-2026` (organisation; investor class; public entity)
- `cadence`: `scheduled` (per certification cycle; typically annual or per loan-application window)
- `source_type`: `hybrid` (OSINT public criteria + HUMINT via adviser bridge)
- `reliability`: `B` (usually reliable; will upgrade to `A` once direct correspondence at N1 begins)
- `output_artifact`: [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md)
- `responsible_role`: Compliance
- `lifecycle_status`: `active`
- Bridge: `GOI-ADV-ENTITY-2026` (third-party startup-certification adviser firm)
- Distance: N2 (bridged); collapses to N1 once direct ENISA correspondence begins
- Stance: `neutral` (we are a candidate; ENISA is a public lender bound by uniform criteria; stance reassessment will trigger when a loan decision lands)

### 10.2 ENISA cycle calendar

- **T-90 days** before submission window: Compliance runs §4.1 pre-cycle assembly; checks ENISA's published criteria for delta vs prior cycle.
- **T-30 days** before submission window: §4.2.1 evidence-pack refresh; CFO + PMO review.
- **T-0 (submission window opens)**: ENISA submission via the bridged adviser firm; record submission date in evidence pack.
- **T+post-decision**: §4.2.3 stance reassessment.

### 10.3 ENISA stance flip rules

- **If ENISA approves a participative loan** → stance flips from `neutral` to `ally` (mutual interest established; ENISA becomes a stakeholder in Holistika's success).
- **If ENISA denies a participative loan with constructive feedback** → stance stays `neutral`; cycle restarts with feedback incorporated.
- **If ENISA denies with structural objections** (e.g., sector mismatch, revenue trajectory mismatch) → stance stays `neutral` but next-cycle posture re-evaluates whether to continue ENISA pursuit or de-prioritize.
- **If ENISA closes participation channel** (e.g., scheme discontinued or eligibility changed retroactively) → mark register row `lifecycle_status=deprecated`; archive evidence pack; record `D-IH-*-CLOSURE` decision.

### 10.4 ENISA-specific failure modes

- **Bridged adviser firm unresponsive**: temporarily lower `reliability` to `C`; surface to operator via `AskQuestion` whether to switch bridge or initiate direct contact at higher cost.
- **ENISA criteria document amended mid-cycle**: invoke ad-hoc evidence-pack refresh; cadence flips temporarily to `event_triggered`.
- **Public consultation period opens**: opportunity to bridge HUMINT directly; update register row source_type to add direct-OSINT layer.
