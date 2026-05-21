---
title: Inter-Wave Regression Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - PMO
  - System Owner
last_review: 2026-05-21
last_review_by: Founder/CEO
last_review_at: 2026-05-21
last_review_decision_id: D-IH-86-BK
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BK
  - D-IH-86-BL
  - D-IH-86-BM
  - D-IH-86-BN
  - D-IH-86-BP
  - D-IH-86-BQ
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
linked_cursor_rules:
  - .cursor/rules/akos-inter-wave-regression.mdc
  - .cursor/rules/akos-planning-traceability.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-inline-ratification.mdc
  - .cursor/rules/akos-agent-checkpoint-discipline.mdc
linked_skills:
  - .cursor/skills/inline-ratify-craft/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
forward_charters:
  - process_list.csv row hol_peopl_dtp_inter_wave_regression_001
  - PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_inter_wave_regression_discipline
  - paired runbook scripts/inter_wave_regression_sweep.py (P2)
  - .cursor/rules/akos-inter-wave-regression.mdc (mechanical drift gate companion)
---

# Inter-Wave Regression Discipline

> The People-area canonical that names the cadence and content of regression
> sweeps performed at every wave-close gate. Tenth specialty instantiation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) (per D-IH-86-BM)
> and sister to [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md); codifies
> `compose_REGRESSION(audience, channel, scenario, brand, governance, wave_closing)`
> -> 12-dimension regression sweep + per-finding inline-ratify gate.

## 1. Purpose

I86 has executed 12 waves so far (A through L). Each wave landed a coherent
substantive deliverable: A (cluster coordinator + cross-cutting D-IH-86-A..N),
B (Bundle B Lane I-A through I-F closure plumbing), C (Bundle C governance
hygiene), D (Bundle D Wave B + Wave C UAT bar + impeccable template), E
(Wave D + Wave E external-render doctrine + 6-surface enum), F (Wave F
brand-baseline-reality + locale orthography drift gate FAIL promotion), G
(Wave G CICD + observability), H (Wave H Lane D cluster burndown plus
Research Head Discipline), I (Wave I founding canonicals: Quality Fabric
+ UAT Discipline + 5-axis compose), J (Wave J Quality Fabric regression
G1..G5 + Cursor rule mint), K (Wave K UAT 11-class promotion + Vercel
deploy-evidence hotfix), L (Wave L output-architecture mechanical hardening
+ Supabase mirroring).

Across those 12 waves, the operator surfaced four classes of regression that
the per-wave plan-quality-bar at `akos-planning-traceability.mdc` did not
mechanically catch:

1. **Doctrine drift** - prior wave's canonical contradicted by a later wave's
   canonical without explicit supersedes / reconciliation lineage. Example:
   I85 closure-criteria-PASS-table vs I87 substrate-test-coverage-with-counts
   diverged before being reconciled at I88.
2. **Mechanical drift** - validator threshold silently relaxed across waves
   (charter / FAIL / INFO ramp without operator-explicit ratification).
   Example: D-IH-86-AY 11-class UAT promotion implicit until Wave K
   surfaced it as a gap.
3. **Inheritance drift** - sister area / sibling repo not informed when a
   People-area pattern is minted, so the inheritance is invisible. Example:
   Wave H minted RESEARCH_HEAD_DISCIPLINE.md but cross-area-breakthrough
   announcement only fired one wave later.
4. **Carryover blast-radius drift** - a forward-charter from a prior wave
   accumulated dependencies across subsequent waves and was no longer
   plausibly closeable in a single follow-up wave. Example: D-IH-86-AY 11
   -class UAT promotion required Wave K + Wave L + Wave M-equivalent
   carryovers before promotion bar cleared.

The pattern this canonical names: **every wave-close MUST execute an explicit
12-dimension regression sweep against the closing wave's deliverables AND
all prior waves' decisions, before the closing wave's UAT report is
finalized**. The sweep surfaces gaps. The gaps surface as inline-ratify
gates per `akos-inline-ratification.mdc`. The operator ratifies which
gaps rework-now (this wave), which forward-charter (next wave), which
defer (OPS row), which intentionally accept (decision row). The sweep
itself is mechanical (runbook); the disposition is human-in-the-loop.

This canonical answers the operator's standing concern (per D-IH-86-BK):
**how do we stop the regression-noticing pattern from being one-off per
agent + one-off per chat, and make it a wave-close discipline that future
agents inherit by default?**

## 2. The 12 regression dimensions

Every wave-close regression sweep probes each of these 12 dimensions
against (a) the closing wave's deliverables and (b) the prior wave's
ratified decisions. A finding fires when the probe surfaces a gap, drift,
or unaddressed promise.

| # | Dimension | What it probes | Probe heuristic |
|:--|:---|:---|:---|
| 1 | **decision_lineage** | Every D-IH-86-X decision row references an artifact that exists; every artifact carries a ratifying_decisions frontmatter pointing back. | FK-resolve DECISION_REGISTER decision_id <-> canonical frontmatter ratifying_decisions; bidirectional must hold. |
| 2 | **forward_charter_carryover** | Every prior wave's frontmatter forward_charters list either landed in a subsequent wave OR is in this wave's scope OR carries an OPS row + deferral decision. | Glob prior canonicals -> parse forward_charters -> resolve against subsequent waves' deliverables + OPS_REGISTER rows. |
| 3 | **validator_ramp_consistency** | INFO -> FAIL drift gate promotions are operator-explicit with decision rows; no silent threshold relaxation. | Diff verification-profiles.json + release-gate.py across the wave; surface any threshold change without paired decision row. |
| 4 | **canonical_csv_pair_completeness** | Every new canonical CSV register has paired Pydantic model + validator + Supabase mirror + PRECEDENCE row per `akos-holistika-operations.mdc`. | For each new CSV under canonicals/dimensions/, check akos/hlk_*_csv.py model + scripts/validate_*.py + supabase/migrations/ mirror + PRECEDENCE row. |
| 5 | **sop_runbook_pairing** | Every process_list.csv item_id has paired SOP at `<area>/<role>/canonicals/SOP-*.md` AND paired runbook `scripts/<purpose>.py` per `akos-executable-process-catalog.mdc` RULE 1. | FK-resolve process_list.csv item_id -> SOP path + runbook path; both AC-HUMAN + AC-AUTOMATION fields present. |
| 6 | **uat_report_class_completeness** | Every closed initiative's UAT report fires the right UAT classes per `compose_UAT` § `UAT_DISCIPLINE.md` §4. | For each INITIATIVE_REGISTRY status=closed row, read its reports/uat-*.md; verify §1 + §3.N for each class that compose_UAT says fires. |
| 7 | **render_trail_audience_match** | Every external-tagged artifact carries paired render trail per `akos-external-render-discipline.mdc` RULE 4. | Re-run `scripts/validate_external_render_trail.py --strict --strict-freshness`; FAIL surfaces any drift. |
| 8 | **brand_baseline_register_match** | Every public surface uses external register; no CORPINT-internal vocabulary leaks per `akos-brand-baseline-reality.mdc`. | Re-run `scripts/validate_brand_baseline_reality_drift.py`; FAIL surfaces any drift. |
| 9 | **cross_area_breakthrough_announcement** | Every new PEOPLE_DESIGN_PATTERN_REGISTRY row triggers an announcement per `SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`. | FK-resolve new pattern_id rows in this + prior wave -> announcement evidence under reports/cross-area-breakthrough-*.md. |
| 10 | **deploy_evidence_completeness** | Every sibling-repo touch carries deploy-verification evidence per `UAT_DISCIPLINE.md` §3.7 + `akos-quality-fabric.mdc` RULE 3. | For each Wave-N-P* row in files-modified.csv where repo != openclaw-akos, verify deploy_id + state=READY + HTTP 200 hero route in UAT report. |
| 11 | **cursor_rule_skill_pairing** | Every new cursor rule under `.cursor/rules/akos-*.mdc` is paired with a skill under `.cursor/skills/*/SKILL.md` when craft transmission is needed (per D-IH-80-E precedent). | For each new akos-*.mdc, inspect for craft-mention; if craft is named, verify paired skill exists OR forward-charter row exists. |
| 12 | **operator_scratchpad_continuity** | Every wave-close updates `docs/wip/intelligence/operator-scratchpad.md` with the wave's summary, gaps, and forward-pointers per `akos-agent-checkpoint-discipline.mdc` self-checkpoint cadence. | Read operator-scratchpad.md; verify last entry timestamp >= last wave-close commit timestamp; verify wave's decision IDs cited. |

Per-dimension findings table from a sweep run carries: `dimension_id`,
`finding_severity` (INFO / WARN / FAIL), `affected_artifacts` (list of
paths), `gap_summary` (1-2 sentences), `proposed_disposition` (rework-now
/ forward-charter / defer-OPS / accept). The operator ratifies the
disposition column at the inline-ratify gate (§6).

## 3. Compose_REGRESSION - the rule that picks the depth

Per the 5-axis Quality Fabric architecture in `HOLISTIKA_QUALITY_FABRIC.md`
§5, this canonical instantiates the regression specialty. The
`compose_REGRESSION` rule extends the parent `compose_UAT` shape with a
sixth coordinate (`wave_closing`) and emits a 12-dimension sweep:

```
def compose_REGRESSION(audience, channel, scenario, brand, governance, wave_closing):
    dimensions = []
    # baseline dimensions (always fire at every wave-close):
    dimensions += [decision_lineage, forward_charter_carryover,
                   validator_ramp_consistency, canonical_csv_pair_completeness,
                   sop_runbook_pairing, uat_report_class_completeness,
                   operator_scratchpad_continuity]
    # axis-conditional dimensions:
    if audience.has_external_tag(): dimensions += [render_trail_audience_match]
    if brand.fires_branded_surface(): dimensions += [brand_baseline_register_match]
    if scenario.has_new_pattern_mint(): dimensions += [cross_area_breakthrough_announcement]
    if channel.touches_sibling_repo(): dimensions += [deploy_evidence_completeness]
    if governance.minted_new_cursor_rule(): dimensions += [cursor_rule_skill_pairing]
    return dimensions  # 7 baseline + up to 5 conditional = 12 total
```

The 7 baseline dimensions fire every wave-close regardless of axis state -
they are the structural integrity checks any wave can drift on. The 5
conditional dimensions fire only when the corresponding axis is active in
the closing wave's deliverables. In practice, every multi-deliverable wave
fires 9-12 dimensions; only narrowly-scoped chore waves fire fewer.

Multiplicative-AND verdict rule from the parent fabric applies: the wave
cannot close with a clean regression verdict unless **every** fired
dimension PASSes (or every WARN/FAIL is dispositioned via inline-ratify per
§6).

## 4. Cadence rule

**Default cadence:** every wave-close. Concretely, the sweep runs after the
last substantive commit of a wave AND before the wave's UAT report
verdict line is filled in. The sweep output (regression-sweep-`<wave>`-
`<date>`.md) is a §3.3 row in the wave's UAT report under the regression
class.

**Exception 1 (chore-only waves).** When a wave touches only sibling-repo
infrastructure (e.g., wrangler config bump, no canonical CSVs, no SOPs,
no decisions besides infrastructure-bump rows), the sweep MAY skip the 5
conditional dimensions and run only the 7 baseline ones. The skipped
dimensions get N/A-with-reason rows in the sweep report.

**Exception 2 (multi-wave initiatives with continuous closure).** When an
initiative spans 5+ waves with daily-cadence wave closes (rare; I86 is
the precedent at 12 waves), the sweep MAY run only on every 3rd wave-
close PROVIDED the operator-explicit ratification is recorded as a
decision row. Skipped waves still file an UAT report; the sweep row in
those reports says "deferred to wave-N+3 per D-IH-NN-X".

**Exception 3 (single-commit waves).** Trivial single-commit chore waves
(typo fixes, link-rot fixes, formatting normalisations) are exempt from
the sweep entirely. The wave's UAT report (if any) records the exemption.

No other exemptions. In particular, "we're in a hurry" / "we'll do it next
wave" / "the operator wants to ship now" are NOT exemptions; per the
operator's verbatim framing on 2026-05-21: *"the regression-noticing
pattern needs to be wave-close-baseline, not agent-discretion-baseline."*

## 5. Depth posture

Three depth tiers, picked per dimension:

- **Tier 1 (mechanical-only).** The dimension is fully encoded as a
  runbook probe + drift gate; the operator never sees individual findings
  unless the gate fires. Examples: dimension 7 (render trail) -
  `validate_external_render_trail.py --strict --strict-freshness` is the
  whole story; dimension 8 (brand baseline register) -
  `validate_brand_baseline_reality_drift.py` is the whole story.

- **Tier 2 (mechanical-surface + operator-disposition).** The dimension's
  probe runs mechanically + emits a findings table; the operator ratifies
  the disposition column at the inline-ratify gate. Examples: dimensions
  1, 2, 4, 5, 6, 9, 10, 11, 12. This is the default tier for new
  dimensions until they harden enough to drop to Tier 1.

- **Tier 3 (operator-walk-required).** The dimension cannot be fully
  mechanised; the operator-walk produces the evidence + the
  disposition. Examples: future dimensions like "MADEIRA persona-walk
  finds the canonical reads correctly to the named persona" (when
  MADEIRA is active per I76).

This canonical lands all 12 dimensions at Tier 2 except dimensions 7 + 8
which land at Tier 1 (the underlying drift gates already exist + are at
FAIL strictness). Promotion from Tier 2 -> Tier 1 happens when the
dimension's findings count drops to zero across 3+ consecutive wave-
closes AND the operator-explicit ratification is recorded as a decision
row.

## 6. Inline-ratify integration

The regression sweep is mechanically deterministic; the disposition of each
WARN/FAIL finding is operator-ratified inline per
`akos-inline-ratification.mdc` + the paired
[`inline-ratify-craft`](../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md)
skill.

**Default 5-option enum per finding** (codified at D-IH-86-BL):

1. **rework-now** - the agent fixes the gap in this wave before the wave
   closes. Default for FAIL severity on baseline dimensions.
2. **forward-charter-next-wave** - the agent mints a candidate-shaped
   forward-charter file under `docs/wip/planning/_candidates/` or a
   tracker file under `_trackers/`; fix lands in the next wave. Default
   for WARN severity on conditional dimensions.
3. **defer-OPS** - the agent appends a row to
   [`OPS_REGISTER.csv`](../Compliance/canonicals/OPS_REGISTER.csv) with
   a named owner + ETA; the gap is not blocking the wave-close. Default
   for INFO severity.
4. **accept-as-canon** - the operator ratifies that the finding is
   actually intentional (the "drift" was a deliberate evolution); the
   agent appends a decision row codifying the acceptance + adds a
   contra-precedent row to the affected canonical's frontmatter
   `last_review_decision_id`.
5. **escalate-to-blocker-tracker** - the finding cannot be
   dispositioned in-chat (e.g., requires external research, requires
   I-team input, requires legal review); the agent mints a blocker-
   tracker under `_blockers/` per
   `akos-conflict-surfacing-and-blocker-trackers.mdc`. Rare.

The single `AskQuestion` batch posts one question per finding (each carrying
the 5-option enum + a recommended-default per the dispositions above + a
one-clause rationale per option), batched up to the inline-ratify-craft
prompt-length cap. When the prompt would exceed 10 questions, the agent
splits the gates into 2 batches (per inline-ratify-craft Principle 5
batching guidance).

**Time-box recovery** applies per `akos-inline-ratification.mdc` Time-box
section: 24h+ operator silence + clean validators + reversible dispositions
auto-default to the recommended option (decision row tagged
`closure_decision_source: agent_inline_default`). Irreversible dispositions
(rework-now touching canonical CSVs; accept-as-canon flipping a frontmatter
flag; escalate-to-blocker-tracker creating durable blocker state) NEVER
auto-default; they halt and escalate.

## 7. Drift gate

The runbook `scripts/inter_wave_regression_sweep.py` (Wave M P2) is the
mechanical implementation. CLI surface:

```
py scripts/inter_wave_regression_sweep.py \
  --wave-closing <wave-letter> \
  [--prior-waves <comma-list>] \
  [--baseline-only] \
  [--output reports/regression-sweep-<date>.md] \
  [--strict]
```

Behaviour:

- Runs 12 `_probe_dimension_N` functions (or 7 with `--baseline-only`).
- Emits a Markdown report with a per-dimension findings table + summary
  counts (FAIL / WARN / INFO / N/A).
- Exit code 0 (PASS) when all dimensions report 0 FAIL findings; exit
  code 1 (FAIL) otherwise.
- `--strict` mode treats WARN as FAIL (forward-charter posture).
- The validator self-test step
  `validate_inter_wave_regression_self_test` (Wave M P2.4) wires the
  runbook's `--self-test` mode into `config/verification-profiles.json`
  `pre_commit` profile + `scripts/release-gate.py`
  `run_inter_wave_regression_self_test`. The self-test verifies the 12
  probe functions exist + return well-formed `RegressionFindingRow`
  Pydantic models; it does NOT run a full sweep at every pre_commit
  (which would be too expensive). The full sweep runs at wave-close
  only.

**Drift posture ramp** (per `D-IH-86-BN`):

- **Wave M (this wave):** self-test step lands at PASS; full sweep
  runs once for Wave L deliverables; findings dispositioned inline.
- **Wave M+1..M+2:** full sweep runs at each wave-close; self-test
  step stays PASS; findings count tracked.
- **Wave M+3 or later (operator-explicit promotion):** sweep promoted
  to release-gate INFO advisory at every wave-close commit; eventually
  FAIL when findings count <= 2 across 3+ consecutive waves.

This is the same INFO -> FAIL ramp pattern used by
`validate_brand_baseline_reality_drift.py` (I66 P2 -> P7) and
`validate_external_render_trail.py` (Wave E -> Wave F D-IH-86-Q
promotion). The ramp is the load-bearing pattern; the bar gets tighter
as the doctrine matures, never looser.

## 8. Cross-references

- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md)
  (5-axis compose() architecture; this canonical is the 10th specialty
  instantiation per `D-IH-86-BM`).
- Sister canonicals under People:
  [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) (the 9th specialty; same shape
  with different verb),
  [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md),
  [`RESEARCH_HEAD_DISCIPLINE.md`](RESEARCH_HEAD_DISCIPLINE.md),
  [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md).
- Paired cursor rule: [`akos-inter-wave-regression.mdc`](../../../../../../.cursor/rules/akos-inter-wave-regression.mdc)
  (mints at this wave's P1.2; 4 RULES + when-not-applies + self-discipline
  + cross-references).
- Paired SOP at charter status:
  [`SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md`](SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md)
  (mints at this wave's P1.3; promotes to active when runbook hardens at
  Wave M+3 or later per D-IH-86-BN ramp).
- Paired runbook: [`scripts/inter_wave_regression_sweep.py`](../../../../../../scripts/inter_wave_regression_sweep.py)
  (mints at this wave's P2.2; Pydantic-typed findings via
  [`akos/hlk_inter_wave_regression.py`](../../../../../../akos/hlk_inter_wave_regression.py)).
- Process catalog row:
  [`process_list.csv`](../Compliance/canonicals/process_list.csv)
  `hol_peopl_dtp_inter_wave_regression_001` (mints at P1.7).
- Pattern registry row:
  [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv)
  `pattern_inter_wave_regression_discipline` (mints at P1.5; class
  `inter_wave_regression_cadence`).
- Sister cursor rules whose dimensions this discipline probes:
  [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc)
  (UAT quality bar; dimension 6),
  [`akos-quality-fabric.mdc`](../../../../../../.cursor/rules/akos-quality-fabric.mdc)
  (parent fabric; multiplicative-AND verdict rule),
  [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc)
  (dimension dispositions via inline-ratify; §6),
  [`akos-agent-checkpoint-discipline.mdc`](../../../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc)
  (operator-scratchpad continuity; dimension 12),
  [`akos-holistika-operations.mdc`](../../../../../../.cursor/rules/akos-holistika-operations.mdc)
  (canonical-CSV pair completeness; dimension 4),
  [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
  (SOP+runbook pairing; dimension 5),
  [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc)
  (render trail audience match; dimension 7),
  [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)
  (brand baseline register match; dimension 8),
  [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc)
  (escalation option; §6 option 5).
- External research grounding (per
  `akos-applied-research-discipline.mdc` RULE 2 - novel framing requires
  external citation):
  - **IEEE 829-2008** (Standard for Software and System Test
    Documentation) + **ISTQB Foundation Level Syllabus** -
    underpins the 12-dimension probe taxonomy as a structured-regression
    discipline (test-process structure; test-design technique catalogue).
  - **Continuous Delivery 2010** (Humble + Farley, "deployment pipeline
    + commit-stage automation") - inter-wave regression sweep mirrors
    the commit-stage gate concept at wave-cadence rather than commit-
    cadence.
  - **Toyota Production System "andon cord"** (Liker, "The Toyota Way",
    2004) - any worker can halt the line when defects surface; the
    inline-ratify 5-option enum is the operator's andon cord at every
    wave-close.
  - **Google SRE Workbook 2018** (chapter on "Production Readiness
    Reviews") - the wave-close PRR analog; 12-dimension sweep is the
    PRR checklist at wave granularity.
- Decision lineage: D-IH-86-BK (this canonical's mint),
  D-IH-86-BL (5-option enum codification at §6),
  D-IH-86-BM (10th-specialty-instantiation tagging),
  D-IH-86-BN (INFO -> FAIL ramp gating),
  D-IH-86-BP (cursor-rule + SOP pairing at P1.2 + P1.3),
  D-IH-86-BQ (Pydantic + Literal enum 12->13 extension at P1.6),
  D-IH-86-BO (P2 closure self-test step landing per `D-IH-86-BN` ramp
  Wave M tier; deferred to P2.5 for ratification).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md
@.cursor/rules/akos-inter-wave-regression.mdc
@.cursor/rules/akos-planning-traceability.mdc
