---
title: Synthesis Before Tranche Discipline
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
last_review: 2026-05-25
last_review_by: Founder/CEO
last_review_at: 2026-05-25
last_review_decision_id: D-IH-86-EA
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-EA
  - D-IH-86-EB
  - D-IH-86-EC
  - D-IH-86-ED
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - INDEX_INTEGRITY_DISCIPLINE.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - UAT_DISCIPLINE.md
  - PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md
  - COLLABORATOR_SHARE_DOCTRINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
linked_cursor_rules:
  - .cursor/rules/akos-synthesis-before-tranche.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-index-integrity.mdc
  - .cursor/rules/akos-inter-wave-regression.mdc
  - .cursor/rules/akos-planning-traceability.mdc
  - .cursor/rules/akos-inline-ratification.mdc
  - .cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc
linked_skills:
  - .cursor/skills/synthesis-before-tranche-craft/SKILL.md
  - .cursor/skills/inline-ratify-craft/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - INDEX_INTEGRITY_DISCIPLINE.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
forward_charters:
  - process_list.csv row hol_peopl_dtp_synthesis_before_tranche_001 (Commit 2c-b)
  - PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_synthesis_before_tranche_discipline (Commit 2c-b)
  - paired runbook scripts/synthesis_before_tranche_check.py (Commit 2b)
  - paired validator scripts/validate_synthesis_before_tranche.py (Commit 2b)
  - .cursor/rules/akos-synthesis-before-tranche.mdc (Commit 2c-a)
  - .cursor/skills/synthesis-before-tranche-craft/SKILL.md (Commit 2c-a)
  - SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md paired with runbook per akos-executable-process-catalog.mdc Rule 1 (Commit 2c-a)
  - first worked example application: this canonical's own mint (recursive self-application; reports/synthesis-specialty-14-mint-2026-05-25.md)
  - second worked example application: SUEZ POC FULL KIT (Commit 4)
  - third worked example application: I82 P1 capability registry mint (Commit 3)
---

# Synthesis Before Tranche Discipline

> The People-area canonical that names the cadence and content of
> **synthesis-before-tranche** sweeps performed before any tranche of
> work ships. Fourteenth specialty instantiation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) (per
> `D-IH-86-EA`) and sister to
> [`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md) +
> [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md);
> codifies `compose_SYNTHESIS(audience, channel, scenario, brand,
> governance, tranche_scope) → 10-dimension synthesis sweep + per-axis
> design citation + ERP-engagement-governance UX shape derivation`.
>
> Codifies the operator's verbatim framing 2026-05-25 (Q-A response,
> mid-architecture session before 13th specialty closure commit):
>
> *"the main goal is to properly govern our engagements via cleverly
> crafting erp workflow and UX just like i want my dashboard they would
> also like to have it (even if they don't log so much or see it that
> much and i send them info via traditional means or drives) we need
> this kind of thinking to ensure we scale and don't find false scope
> creep that we knew was a logical tactical move and design from our
> part but we're not taking the full design in mind of these processes,
> why we're doing what we're doing"*

## 1. Purpose

A tranche of work — a wave that closes; a kit that ships; an engagement
phase that commits; a canonical CSV that mints; a brand surface that
deploys — represents a **commitment**. Once the commit lands, the
tranche's scope is what was shipped; rolling back is expensive and
sometimes irreversible.

Without a synthesis-before-tranche pass, the agent and operator
discover, mid-tranche or post-tranche, that the tranche's scope was
unintentionally narrow — that the design intent the operator carried
in their head was richer than the design the tranche actually
materialised. The operator names this as *"false scope creep that we
knew was a logical tactical move and design from our part but we're
not taking the full design in mind"*: the tranche IS a legitimate
tactical move; the failure is at the design layer, where the full
intent was not surfaced before the tranche's scope was frozen.

This canonical names that **synthesis is itself a discipline** — not
a one-off retrospective but a recurring cadence applied **before**
every meaningful tranche of work ships. The 10 dimensions below name
what the synthesis pass MUST surface; the paired runbook emits the
synthesis report; the validator catches missing dimensions before
commit; the operator scratchpad records what was synthesised and
what was deferred.

The discipline catches scope-creep at the **design layer** (before
commitment) rather than at the **execution layer** (after commitment).
That's the load-bearing claim — and the difference between a
governance system that scales and one that requires the founder to
catch every miss in retrospect.

## 2. The 10 dimensions

Every synthesis sweep emits findings against the following 10 probes.
Each probe answers a specific question about whether the tranche's
design intent is fully surfaced **before** the tranche commits:

| # | Dimension code | Question the dimension answers | Axis it touches |
|:--|:---|:---|:---|
| 1 | **SYN-01-AUDIENCE-COMPLETENESS** | Has the tranche named every audience class touched by the tranche's output? (operator dashboard reader / customer dashboard reader / ERP back-office consumer / mail recipient / etc.) | Audience |
| 2 | **SYN-02-CHANNEL-COVERAGE** | Has the tranche named every channel through which the tranche's output reaches each named audience? (web dashboard / email / PDF attachment / Slack DM / etc.) | Channel |
| 3 | **SYN-03-SCENARIO-INVENTORY** | Has the tranche named all scenarios the audience-channel pairs will be in when consuming the output? (first-look scenario / re-visit scenario / empty-state / error-state / mobile vs desktop / etc.) | Scenario |
| 4 | **SYN-04-BRAND-REGISTER-CITATION** | Has the tranche cited which brand register applies per audience? (internal CORPINT vs external translated; voice traits cited; visual identity surface cited) | Brand |
| 5 | **SYN-05-GOVERNANCE-RATIFICATION-LINEAGE** | Has the tranche cited which D-IH-NN-X decisions ratify the design intent? (per-axis ratifications + composite tranche-mint decision) | Governance |
| 6 | **SYN-06-ERP-SURFACE-CITATION** | For engagement-class tranches: has the tranche named which of the 3 ERP-engagement-governance surfaces it lives in? (operator dashboard / customer dashboard / ERP workflow join) | All 5 (engagement-class composite) |
| 7 | **SYN-07-TRANCHE-ATOMICITY** | Is the tranche scoped as ONE atomic commit (or one operator-readable artifact)? Does the tranche land as one decision-point the operator can ratify / revert in one action? | Governance |
| 8 | **SYN-08-REVERSIBILITY-DECLARATION** | Has the tranche declared its reversibility class (low / medium / high) with the rationale for the class? Has irreversibility been flagged to the operator before commit? | Governance |
| 9 | **SYN-09-CLOSING-LOOP-TEST** | Has the tranche named the self-test / field-test / observability signal that confirms the tranche works as designed post-ship? | Governance |
| 10 | **SYN-10-RECIPIENT-FALLBACK-CHANNEL** | Has the tranche named the traditional-means fallback (PDF attachment / shared drive / mail body / Loom video / phone call) for recipients who don't access the primary surface? *"even if they don't log so much or see it that much"* | Channel + Audience |

**Dimension firing per tranche-class** (per `D-IH-86-EC` ratification):

| Tranche class | Always-fire dimensions | Conditional dimensions |
|:---|:---|:---|
| **engagement** (e.g., SUEZ POC FULL KIT; Websitz handoff pack; per-engagement settlement) | SYN-01, 02, 03, 04, 05, 06, 07, 08, 09, 10 (all 10 fire) | none |
| **specialty_mint** (e.g., this canonical's own mint; future 15th specialty) | SYN-01, 02, 04, 05, 07, 08, 09 (7 fire) | SYN-03 (fires only when the specialty has end-user-facing scenarios); SYN-06 + SYN-10 skip (no engagement) |
| **internal_governance** (e.g., wave-close UAT; decision-register append; PRECEDENCE update) | SYN-05, 07, 08 (3 fire) | SYN-01, 02, 04, 09 (fire only when the internal-governance artifact has a non-J-OP audience or operator-readable surface) |
| **canonical_csv_mint** (e.g., new dimension CSV; row append to existing CSV) | SYN-01, 04, 05, 07, 08, 09 (6 fire) | SYN-02, 03, 10 (fire only when CSV rows surface in operator/customer-facing dashboards) |
| **brand_surface** (e.g., website page; deck slide; PDF dossier) | SYN-01, 02, 03, 04, 05, 07, 08, 09, 10 (9 fire) | SYN-06 (fires only when the brand surface is engagement-scoped) |
| **external_deliverable** (e.g., investor dossier; ENISA evidence; advisor handoff pack) | all 10 fire | none |

This split mirrors the precedent from sister disciplines:
INTER_WAVE_REGRESSION 7-baseline + 5-conditional;
INDEX_INTEGRITY 6-baseline + 2-conditional; SYNTHESIS_BEFORE_TRANCHE
has variable firing because the tranche-class determines which axes
are load-bearing.

## 3. The compose_SYNTHESIS rule

The fabric's compose() rule, specialised for synthesis-before-tranche:

```
compose_SYNTHESIS(audience, channel, scenario, brand, governance,
                  tranche_scope) -> 10-dimension synthesis sweep
  where:
    tranche_class       = classify_tranche(tranche_scope)
    fire_set            = dimension_firing_rules[tranche_class]
    findings            = [run_probe(dim) for dim in fire_set]
    report_path         = reports/synthesis-<tranche-id>-<date>.md
    disposition_gate    = inline-ratify per akos-inline-ratification.mdc
                         (5-option enum; see §6)
```

SYNTHESIS_BEFORE_TRANCHE composes across **all 5 axes** of the fabric.
Unlike INDEX_INTEGRITY (governance-only composition) or
INTER_WAVE_REGRESSION (governance-only), this discipline pulls audience
+ channel + scenario + brand + governance because tranche scope CAN
affect any axis. The discipline is the fabric's most-broadly-composing
specialty.

The composition is also **temporal**: the sweep runs BEFORE the tranche
commits, not after. INTER_WAVE_REGRESSION and INDEX_INTEGRITY both run
at wave-close (after commit); SYNTHESIS_BEFORE_TRANCHE runs at
tranche-charter time (before commit). This temporal ordering is what
makes the discipline catch design-gaps at the design layer.

## 4. Cadence

Default cadence: **before every meaningful tranche ships**. The
"meaningful tranche" definition is the operative threshold (per
`D-IH-86-EA` ratification):

A tranche is "meaningful" — and therefore in scope for this discipline
— when **any** of:

- The tranche is one of the 6 tranche classes in §2 (engagement /
  specialty_mint / internal_governance with non-J-OP audience /
  canonical_csv_mint / brand_surface / external_deliverable).
- The tranche ships ≥ 5 files in one commit OR touches a canonical
  CSV.
- The tranche carries a `tranche_class:` frontmatter tag in a
  master-roadmap or candidate file.
- The operator explicitly requests a synthesis pass (on_demand
  cadence).

Exceptions:

- **Chore-only commits** (typo fixes, link-rot fixes, formatting,
  CHANGELOG-only edits): exempt entirely.
- **Internal-governance with J-OP-only audience and < 3 files**:
  exempt; the synthesis dimensions reduce to SYN-05/07/08 which the
  commit message itself captures.
- **Pre-commit self-test** (sweep_trigger = `pre_commit_self_test`):
  always-on, zero-cost; validates Pydantic fixtures only (not real
  tranche-scope drift). Wired into `release-gate.py` per
  `D-IH-86-EA`.
- **Hot-fix commits** (urgent production fix; e.g., the Wave R+1 P3
  Commit 1 hygiene precedent): operator may invoke the
  `--hotfix-bypass` flag with a one-sentence rationale that lands in
  the next operator-scratchpad drain entry. Bypass logs as a
  superseded-on-record skip; not silent.

No other exemptions. The operator's 2026-05-25 framing explicitly
rejected the "we're moving fast, we'll synthesise next tranche"
posture — that posture IS the failure mode this discipline catches.

## 5. Drift gate INFO → FAIL ramp

Per `D-IH-86-ED`, the validator
[`scripts/validate_synthesis_before_tranche.py`](../../../../../../../scripts/validate_synthesis_before_tranche.py)
launches at **INFO** during the Wave R+1 P3 + Wave S backfill window.
Broad-fire posture (per Q-3 auto-default at 14th-specialty meta-ratify
gate): the validator fires at every commit touching any of the 6
tranche-class triggers, emits findings, but does not block CI.

Promotion to **FAIL** requires (Stage 2 gate):

1. ≥ 3 worked examples applied the discipline cleanly: (i) this
   canonical's own mint (specialty_mint class; recursive self-
   application); (ii) SUEZ POC FULL KIT (engagement class; Commit 4);
   (iii) I82 P1 capability registry mint (canonical_csv_mint class;
   Commit 3).
2. Two consecutive subsequent tranches (next 2 commits in scope) emit
   `synthesis_complete == true` with zero FAIL-severity findings.
3. Validator FAIL promotion ratified by operator-explicit decision
   (`D-IH-86-EA` successor row, e.g., `D-IH-86-EF`-shape).
4. SYN-04 / SYN-05 / SYN-08 remain at FAIL ramp permanently (these
   are mandatory-citation dimensions; missing citation always fails).
5. SYN-01 / SYN-02 / SYN-03 / SYN-06 / SYN-09 / SYN-10 remain at WARN
   forever (these are completeness dimensions that judgement may
   legitimately defer; WARN surfaces them without blocking).
6. SYN-07 (atomicity) remains at FAIL ramp permanently (atomicity is
   binary; non-atomic tranches are not meaningful tranches under the
   doctrine).

Until promotion, the validator emits INFO findings that the operator
reviews via the wave-close UAT report's mechanical-evidence section
OR the tranche-pre-commit checkpoint.

## 6. Findings disposition via inline-ratify 5-option enum

Per `D-IH-86-EC`, every WARN or FAIL finding from the sweep is
dispositioned via an inline `AskQuestion` gate per
[`akos-inline-ratification.mdc`](../../../../../../../.cursor/rules/akos-inline-ratification.mdc)
+ the paired
[`inline-ratify-craft`](../../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md)
skill, using the 5-option enum:

1. **scope-complete** — finding represents missing scope that should
   be added BEFORE the tranche commits; the agent extends the tranche
   scope to include the missing dimension and re-runs the synthesis
   sweep. Default for WARN findings on always-fire dimensions when
   the operator's prior framing makes the missing scope load-bearing.
2. **scope-extend** — finding represents adjacent scope that should
   be added to a FOLLOW-UP tranche (not this one); the agent files an
   OPS_REGISTER row or a forward-charter pointer and commits THIS
   tranche as-is with the scope-extension explicitly named. Default
   for WARN findings on conditional dimensions when adding to this
   tranche would over-burden it.
3. **scope-narrow** — finding represents scope creep INTO this
   tranche that should be REMOVED; the agent narrows the tranche's
   scope to the synthesis-validated minimum. Default for FAIL
   findings on SYN-07 atomicity when the tranche is non-atomic.
4. **defer-OPS** — finding represents low-priority gap that defers
   indefinitely with a tracker row. Default for INFO findings.
5. **escalate-to-blocker-tracker** — finding cannot be dispositioned
   in-chat; mints
   `docs/wip/planning/_blockers/<slug>-tracker.md` per
   [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc).
   Default for findings that require operator-time the inline-ratify
   window does not allow.

When findings exceed 10, the agent splits the gates into 2
`AskQuestion` batches (inline-ratify-craft Principle 5 batching).
Time-box recovery: 24h+ operator silence + clean validators +
reversible dispositions auto-default to the recommended option.
Irreversible dispositions (`scope-narrow` on a tranche that already
shipped a partial; commercial-share decisions; brand-canon edits with
sibling-repo carry-overs) NEVER auto-default — halt and escalate per
[`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc).

## 7. The paired runbook contract

The runbook
[`scripts/synthesis_before_tranche_check.py`](../../../../../../../scripts/synthesis_before_tranche_check.py)
implements the 10 probes + emits the synthesis report. Modes:

- `--self-test`: validates Pydantic fixtures only; ~50ms; wired into
  `release-gate.py` + `pre_commit` profile.
- `--check --tranche-class <class> --tranche-id <slug>`: runs the
  applicable probes for the named tranche class; emits findings to
  stdout + writes report to
  `reports/synthesis-<tranche-id>-<YYYY-MM-DD>.md`.
- `--check-from-frontmatter <path>`: reads tranche metadata from a
  master-roadmap or candidate file frontmatter; runs the applicable
  probes; same report output. Convenience mode for in-flight commits.
- `--list-dimensions`: emits the 10 dimensions + per-tranche-class
  firing rules as a human-readable table.

The runbook respects `compose_SYNTHESIS(audience, channel, scenario,
brand, governance, tranche_scope)` — it reads all 5 axes' canonicals
when the tranche-class warrants and emits per-axis findings without
attempting to auto-fix (synthesis is judgement-class work; auto-fix
would defeat the purpose).

## 8. The paired SOP contract

The SOP
[`SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md`](SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md)
is the human-facing operator-readable counterpart per
[`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1. AC-HUMAN acceptance: any human or AIC role_owner (PMO interim;
COO when activated per I76) can run the synthesis sweep + dispose
findings following the SOP without invoking the runbook (the SOP
walks the 10 questions one by one). AC-AUTOMATION acceptance: the
runbook fires unattended at pre-commit hook + tranche-charter
trigger + on-demand operator invocation.

## 9. When this canonical applies

This canonical applies whenever **any** of:

- A tranche of work approaches commit-time and the tranche meets the
  "meaningful tranche" threshold in §4.
- A new wave-charter (or wave-close commit when the wave introduces
  a new tranche-class).
- An engagement charters or commits a phase (e.g., a customer-
  engagement Phase 0 charter, an advisor-engagement handoff-pack).
- A canonical CSV mints OR a row appends with audience-axis impact
  (e.g., AUDIENCE_REGISTRY append surfacing in operator dashboards).
- A specialty canonical mints (every specialty mint is a tranche).
- A brand surface deploys (web page, deck slide, dossier render).
- An external deliverable ships (investor dossier, ENISA evidence,
  advisor handoff pack).
- The operator explicitly requests a synthesis pass (on_demand
  cadence).

It does **not** apply to:

- Chore-only commits (typo fixes, link-rot fixes, formatting,
  CHANGELOG-only edits).
- Per-engagement WIP synthesis under `docs/wip/intelligence/`
  (governed by the brand-baseline-reality discipline, not this one).
- Internal helper modules with no audience/channel/scenario impact.
- Pre-2026-05-25 tranches that have already shipped — the discipline
  is forward-only from this mint commit, not retroactive.

## 10. Migration posture (charter → active)

This canonical lands at **`status: charter`** at mint time
(`D-IH-86-EA`, 2026-05-25). Charter status means: the architecture is
ratified; implementation is phased; FAIL promotion is forward-
chartered to a ratifying decision after the 3-worked-example
threshold per §5 Stage 2.

Promotion to **`status: active`** requires:

1. This canonical's own mint successfully applies the discipline
   recursively (specialty_mint class; first worked example).
2. SUEZ POC FULL KIT successfully applies the discipline
   (engagement class; second worked example; Commit 4 target).
3. I82 P1 capability registry mint successfully applies the
   discipline (canonical_csv_mint class; third worked example;
   Commit 3 target).
4. Operator-explicit ratification of active promotion in a
   successor decision row (`D-IH-86-EF` or successor).
5. Validator FAIL promotion ratified at the same gate per §5
   Stage 2.

The recursive self-application requirement is intentional and load-
bearing: if the discipline can't be applied to its own mint, it can't
be applied to engagement work either. Recursive self-application is
the credibility floor.

## 11. ERP-engagement-governance UX shape (engagement-class worked example)

Per the operator's Q-D ratify (2026-05-25), this canonical folds in
the ERP-engagement-governance UX design layer as its primary
engagement-class worked example. Every engagement-class tranche
inherits the 3-surface design substrate:

### 11.1 The 3 ERP-engagement-governance surfaces

1. **Operator dashboard** (Holistika-side; J-OP audience; access
   level 4-5) — surfaces the engagement's current state, pending
   ratifications, settlement preview, collaborator share view,
   ERP-workflow blockers, and operator-action queue. The
   surface the operator wants for themselves *"just like i want my
   dashboard"*.

2. **Customer dashboard** (counterparty-side; J-CU / J-PT / J-AD
   audience depending on engagement model; access level 3) — surfaces
   the customer's view of the same engagement: their commitment
   tracker, their settlement statement, their open questions, their
   next-step queue. The mirrored surface *"they would also like to
   have it"* — exists as design SSOT REGARDLESS of customer login
   frequency. *"even if they don't log so much or see it that much"*.

3. **ERP workflow join** (back-office plane; J-OP + J-AIC audience;
   access level 5) — surfaces the canonical FK joins between
   engagement-level data (`process_list.csv` rows owned by the
   engagement; collaborator-share rows; settlement rows;
   intelligence rows) and the cross-engagement portfolio view
   (Madeira aggregate; FINOPS rollup; INTELLIGENCEOPS portfolio).
   The data layer that makes the dashboards live.

### 11.2 Tranche → surface mapping (engagement-class)

For every engagement-class tranche, SYN-06-ERP-SURFACE-CITATION
requires explicit naming of which of the 3 surfaces the tranche's
output lives in. The doctrine REJECTS the "we'll figure out the
surface later" posture — the surface IS the design decision.

Worked example (SUEZ POC FULL KIT, Commit 4 target):

| Tranche deliverable | Primary surface | Secondary surface (fallback per SYN-10) |
|:---|:---|:---|
| Cobranded cover mail FR | none (channel: CHAN-EMAIL-OUTBOUND) | n/a (mail IS the channel) |
| Architecture-addendum PDF (2 pages) | none (channel: CHAN-PDF-DOWNLOAD attachment to cover mail) | shared drive folder per CHAN-DRIVE-SHARE |
| Excel + Power Query libellé generator | none (channel: CHAN-FILE-ATTACH; Microsoft Power Platform substrate) | shared drive folder per CHAN-DRIVE-SHARE |
| Loom video (60-90s) | Operator dashboard (Holistika-side build log) + Customer dashboard (customer-facing demo) | mail + drive fallback |
| Settlement statement (post-engagement) | Customer dashboard + Operator dashboard (mirrored views) | PDF emailed via CHAN-EMAIL-OUTBOUND |
| Capability registry rows (per I82 P1) | ERP workflow join (back-office FK to engagement_id) | none — back-office plane only |

### 11.3 Tranche → surface mapping (non-engagement classes)

Non-engagement-class tranches (specialty_mint, internal_governance,
canonical_csv_mint) SKIP SYN-06 entirely. The 3 ERP-engagement-
governance surfaces are engagement-specific; applying them to
governance-internal work would be over-fitting the doctrine.

The 14th specialty's own mint (recursive worked example) skips SYN-06
for this reason — the mint is a specialty_mint, not an engagement.
The skip is recorded explicitly in the synthesis report's SYN-06
finding row as "N/A — specialty_mint class does not have engagement-
governance surfaces".

## 12. Cross-references

- **Sister canonicals under People:**
  [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) §6
  materialisation table — this canonical is the 14th specialty row
  (added at this mint per `D-IH-86-EA`).
  [`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md)
  — sister discipline; INDEX_INTEGRITY runs AT or AFTER tranche-
  close (wave-close cadence); SYNTHESIS_BEFORE_TRANCHE runs BEFORE
  tranche-commit. The two compose: a clean SYNTHESIS_BEFORE_TRANCHE
  sweep does NOT prove tranche-close index freshness; a clean
  INDEX_INTEGRITY sweep does NOT prove pre-tranche design synthesis.
  [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md)
  — sister discipline; INTER_WAVE_REGRESSION runs at every wave-
  close (after commit); SYNTHESIS_BEFORE_TRANCHE runs at every
  tranche-charter (before commit). Both compose with the 5-axis
  fabric but at opposite temporal phases of the work lifecycle.
  [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) — closure UAT class that
  hosts synthesis-report evidence as a mechanical row inside the
  pre-commit checkpoint section.
  [`COLLABORATOR_SHARE_DOCTRINE.md`](COLLABORATOR_SHARE_DOCTRINE.md)
  — sister specialty (13th); SHARE_REGISTRY mints are tranches that
  pass through SYNTHESIS_BEFORE_TRANCHE (canonical_csv_mint class)
  with SYN-04 brand-register + SYN-05 governance lineage citing
  D-IH-86-DA/B/C/D/E quintet.
- **Per-axis SSOT registries:**
  [`AUDIENCE_REGISTRY.csv`](../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv)
  (SYN-01 FK source),
  [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv)
  (SYN-02 + SYN-10 FK source),
  [`PERSONA_SCENARIO_REGISTRY.csv`](../../Marketing/Resonance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv)
  (SYN-03 FK source),
  [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md)
  (SYN-04 register source),
  [`DECISION_REGISTER.csv`](../Compliance/canonicals/DECISION_REGISTER.csv)
  (SYN-05 FK source),
  [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md)
  (SYN-08 reversibility class source),
  [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv)
  (this canonical's pattern row source).
- **Cursor rules:**
  [`akos-synthesis-before-tranche.mdc`](../../../../../../../.cursor/rules/akos-synthesis-before-tranche.mdc)
  (this canonical's mechanical companion; Commit 2c-a deliverable),
  [`akos-quality-fabric.mdc`](../../../../../../../.cursor/rules/akos-quality-fabric.mdc)
  (parent fabric rule),
  [`akos-index-integrity.mdc`](../../../../../../../.cursor/rules/akos-index-integrity.mdc)
  (sister discipline rule; INDEX_INTEGRITY),
  [`akos-inter-wave-regression.mdc`](../../../../../../../.cursor/rules/akos-inter-wave-regression.mdc)
  (sister discipline rule; INTER_WAVE_REGRESSION),
  [`akos-planning-traceability.mdc`](../../../../../../../.cursor/rules/akos-planning-traceability.mdc)
  (per-initiative file-changes CSV pattern that SYN-07 atomicity
  inherits from),
  [`akos-inline-ratification.mdc`](../../../../../../../.cursor/rules/akos-inline-ratification.mdc)
  (findings disposition),
  [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc)
  (escalate-to-blocker-tracker option in §6).
- **Skill:**
  [`synthesis-before-tranche-craft`](../../../../../../../.cursor/skills/synthesis-before-tranche-craft/SKILL.md)
  — the *how* layer paired with this canonical's *what* layer.
- **Governance lineage:**
  `D-IH-86-EA` (canonical mint + INFO ramp; operator-ratified
  2026-05-25 via the Q-D Q-A-folded auto-default at the
  meta-discussion sequencing gate),
  `D-IH-86-EB` (10-dimension probe set ratification),
  `D-IH-86-EC` (5-option disposition enum + per-tranche-class
  dimension firing rules),
  `D-IH-86-ED` (INFO→FAIL ramp posture + broad-fire cadence).
  `D-IH-86-EE` (paired SOP+runbook gate per `akos-executable-process-
  catalog.mdc` Rule 1; lands at Commit 2c-a).

## 13. External research grounding

Per [`akos-applied-research-discipline.mdc`](../../../../../../../.cursor/rules/akos-applied-research-discipline.mdc)
RULE 2 (novel framings require external citation): the
SYNTHESIS_BEFORE_TRANCHE discipline is grounded in four external
practices that converge on the same insight:

- **Design Sprint methodology (Knapp / Zeratsky / Kowitz at GV,
  Google Ventures 2016; "Sprint: How to Solve Big Problems and Test
  New Ideas in Just Five Days")** — the Monday-Tuesday phases
  ("understand" + "diverge") are the design-layer synthesis that
  precedes the commitment phase (Wednesday-Friday). The 14th
  specialty operationalises the same insight at the tranche layer:
  synthesis BEFORE the build. The doctrine extends Design Sprint by
  making the synthesis pass auditable (validator + report) rather
  than relying on facilitator memory.
- **DAMA-DMBOK 2.0 §"Data Governance" knowledge area** — names that
  data design decisions made in isolation create downstream debt
  across the data lifecycle. The 5-axis composition rule the fabric
  inherits is the data-governance application; the synthesis pass IS
  the data-governance review at the tranche level.
- **Bret Victor "Stop drawing dead fish" + "Inventing on Principle"
  (2012, 2013)** — the principle that design work happens in a
  feedback loop where the designer sees the consequences of the
  design BEFORE committing. The synthesis report is the analog of
  Victor's "see the consequences before committing" for governance
  tranches.
- **GitOps practice (Weaveworks 2017; "Guide to GitOps")** — every
  meaningful change is a Pull Request with explicit review; the PR
  description IS the synthesis the reviewer needs. The 14th
  specialty extends GitOps by codifying WHAT the synthesis must
  include (the 10 dimensions) rather than leaving it to PR-author
  discretion.

The synthesis methodology is also internally precedented:

- The I86 cluster's wave-by-wave UAT structure already runs a
  retrospective synthesis (post-wave); SYNTHESIS_BEFORE_TRANCHE
  shifts that synthesis to PRE-wave / PRE-tranche.
- The COLLABORATOR_SHARE 13th specialty's pre-flight checklist
  (in `collaborator-share-craft` skill) is a domain-specific
  instantiation of synthesis-before-tranche; the 14th specialty
  generalises that pattern to ALL tranche classes.
- The operator's verbatim framing 2026-05-25 names the discipline
  as a scale-enabler: *"we need this kind of thinking to ensure
  we scale"*. The doctrine codifies the framing.

@HOLISTIKA_QUALITY_FABRIC.md
@INDEX_INTEGRITY_DISCIPLINE.md
@INTER_WAVE_REGRESSION_DISCIPLINE.md
