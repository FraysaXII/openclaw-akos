---
name: Synthesis Before Tranche Craft
description: >-
  Use when authoring, running, dispositioning findings from, or wiring
  up the synthesis-before-tranche discipline in this AKOS workspace
  (14th Quality Fabric specialty). Codifies the craft for classifying
  a tranche's class (engagement / specialty_mint / internal_governance
  / canonical_csv_mint / brand_surface / external_deliverable), resolving
  the per-class fire-set, running the 10-dimension sweep BEFORE commit
  (not after), dispositioning findings via the 5-option enum, and citing
  the 3 ERP-engagement-governance surfaces (operator dashboard /
  customer dashboard / ERP workflow join) when engagement-class tranches
  fire SYN-06. Triggers on phrases like synthesis before tranche,
  pre-tranche review, scope creep, false scope, design intent,
  tranche-charter, ERP-engagement-governance UX, operator dashboard
  for client, recipient-fallback channel, SYN-NN finding,
  synthesis_complete, validate_synthesis_before_tranche.py,
  synthesis_before_tranche_check.py. Pairs with
  .cursor/rules/akos-synthesis-before-tranche.mdc (the WHEN); this
  skill is the HOW.
---

# Synthesis Before Tranche Craft

## Why this skill exists

The cursor rule `akos-synthesis-before-tranche.mdc` and the canonical
`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` tell you **when** the
discipline fires (in-scope tranche classes; trigger conditions; INFO→
FAIL ramp gates) and **what** the 10 dimensions + 6 tranche classes +
5-option disposition enum are. This skill tells you **how** to apply
them well — how to classify a tranche's class under pressure, how to
think about the 3 ERP-engagement-governance surfaces when SYN-06
fires, how to compose the disposition `AskQuestion` so the operator
can ratify in seconds, and how to avoid the false-scope-creep
anti-pattern the operator named verbatim at 2026-05-25 Q-A ratify:

> *"we need this kind of thinking to ensure we scale and don't find
> false scope creep that we knew was a logical tactical move and
> design from our part but we're not taking the full design in mind
> of these processes, why we're doing what we're doing."*

Read this skill before authoring any tranche-charter, running
`scripts/synthesis_before_tranche_check.py --check-charter`, or
dispositioning a finding from the runbook output.

## Principle 1 — Classify the tranche-class FIRST, before drafting any charter frontmatter

The single most load-bearing decision in this discipline is the
`tranche_class` choice. The 6 classes each carry a different
`DIMENSION_FIRE_RULES` always-fire + conditional-fire pair; picking
wrong means firing the wrong subset of dimensions, which means missing
the design-intent gaps the discipline was created to catch.

Decision tree:

```
Q1: Does the tranche ship value to a counterparty
    (customer / advisor / partner / ENISA / investor / recruiter /
    collaborator) via a deliverable, surface, or service?

  YES → Q1a: Is the deliverable an artifact you SEND to them
             (PDF / mail body / deck PDF) vs a surface they USE
             (operator dashboard / web page / portal)?

    SEND artifact → tranche_class = external_deliverable
                    (fires all 10 — the most exhaustive class)

    USE surface → Q1b: Is the surface engagement-scoped (a specific
                       counterparty uses it for a specific engagement)
                       vs general (all visitors / all users)?

      engagement-scoped → tranche_class = engagement
                          (fires all 10; SYN-06 ERP-surface citation
                          mandatory)

      general → tranche_class = brand_surface
                (fires 9; SYN-06 conditional only if engagement-scoped)

  NO → Q2: Does the tranche mint or modify a canonical CSV under
            docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/
            canonicals/?

    YES → tranche_class = canonical_csv_mint
          (fires 6 baseline; SYN-02 + SYN-03 + SYN-10 conditional
          when the CSV surfaces in dashboards or external rollups)

    NO → Q3: Does the tranche mint a new Quality Fabric specialty
              (doctrine + chassis + validator + runbook + rule +
              skill + SOP) per akos-quality-fabric.mdc RULE 7?

      YES → tranche_class = specialty_mint
            (fires 7; SYN-03 conditional when end-user scenarios
            apply — usually no, because specialties are
            agent-and-operator-facing)

      NO → tranche_class = internal_governance
            (fires 3 baseline; SYN-01/02/04/09 conditional when
            non-J-OP audience OR ≥ 3 files touched)
```

Worked decision examples:

- **This rule's mint (Commit 2c-a)** → `specialty_mint` (recursive
  self-application). Fires 7 dimensions: SYN-01 (J-OP + J-AIC named),
  SYN-02 (cursor + repo channel), SYN-04 (internal CORPINT register;
  no translation needed), SYN-05 (D-IH-86-EA..EE), SYN-07 (atomic
  4-commit-kit per `akos-quality-fabric.mdc` RULE 7), SYN-08
  (reversibility medium; rule + skill + SOP are reversible by `git
  revert`; PRECEDENCE + DECISION_REGISTER + process_list edits at
  Commit 2c-b less so), SYN-09 (validator + runbook self-test in
  pre_commit + this skill's pre-flight checklist).
- **SUEZ POC FULL KIT (Commit 4 target)** → `external_deliverable`
  (mail + PDF dossier + Excel attachment ship to SUEZ rep). Fires all
  10. SYN-06 conditional but recommended (the operator framing
  explicitly names the ERP-engagement-governance UX shape).
- **I82 P1 capability registry mint (Commit 3 target)** →
  `canonical_csv_mint`. Fires 6 baseline. SYN-10 conditional but
  recommended (capabilities surface in the operator dashboard
  eventually).
- **Wave-close commit landing a single SOP edit + CHANGELOG entry +
  files-modified row** → `internal_governance` (3-file scope; J-OP-
  only audience). Fires 3 baseline only.
- **A new `_candidates/i-nn-foo.md` file** → out of scope (under §9
  exception 4: per-engagement WIP synthesis or candidate-stage scope
  sheets).

When unclear, halt and re-read the doctrine §4 + §11 BEFORE posting
any `AskQuestion`. Re-reading takes 5 minutes; re-running a sweep
under the wrong class takes 30+ AND surfaces wrong findings the
operator has to manually correct.

## Principle 2 — Run synthesis BEFORE the tranche commits, not after

The defining temporal posture of this discipline (vs sister disciplines
INDEX_INTEGRITY + INTER_WAVE_REGRESSION which run after-commit) is the
pre-tranche cadence. Synthesis is design-layer pre-flight; UAT + index-
sweep + regression-sweep are post-commit signals. Doing them in the
wrong order is the most expensive failure mode.

Bad (synthesis-after):

```
1. Author tranche files
2. Commit
3. UAT verdict fills in
4. Realize SYN-06 ERP-surface was never named for the engagement
5. Amend the engagement folder + UAT report + commit-amend OR
   ship as-is and accept the design debt
```

Good (synthesis-before):

```
1. Classify tranche-class
2. Draft tranche-charter frontmatter
3. Run scripts/synthesis_before_tranche_check.py --check-charter <path>
4. Inspect findings; dispose via inline-ratify AskQuestion
5. Apply ratified scope adjustments to tranche files
6. Commit; UAT verdict fills in cleanly
```

The discipline's value is in the order of operations. Skipping step 3
defeats the discipline.

## Principle 3 — When SYN-06 fires, walk the 3 ERP-engagement-governance surfaces explicitly

SYN-06 is the ERP-engagement-governance UX surface citation. It fires
mandatorily for `engagement` class tranches and conditionally for
`brand_surface` + `canonical_csv_mint` tranches when the artifact
eventually surfaces in a dashboard. The 3 surfaces (per
`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` §11) are:

### Surface 1 — Operator dashboard (Holistika-side)

The dashboard the operator uses to govern the engagement. Lives in
HLK-ERP under `/operator/<engagement-slug>/`. Holds: counterparty
brief; objections brief; commercial schedule; settlement statements;
tranche progress; risk flags; AIC delegations. Built first because
the operator is the always-on actor; collaborators may not use the
dashboard but the operator always does.

### Surface 2 — Customer dashboard (counterparty-side)

The dashboard the counterparty uses to consume the engagement. Lives
in HLK-ERP under `/customer/<engagement-slug>/` OR in the
counterparty's own ERP via integration. Holds: read-only views of
engagement progress; milestone deliverables; settlement summaries;
status updates; AI-assisted summaries when the counterparty doesn't
log in often.

**Recipient-fallback (SYN-10):** the customer dashboard MUST have a
traditional-means counterpart (email summary; PDF report; SMS update)
for counterparties who *"don't log so much or see it that much"*.
Citing the surface alone is not enough; the fallback channel is the
load-bearing claim per the operator's 2026-05-25 framing.

### Surface 3 — ERP workflow join

The workflow logic that joins operator-side governance to customer-
side consumption. Lives in HLK-ERP `app/workflows/<engagement-class>/`
+ the runbook scripts that fire on tranche close events. Holds: state
transitions; webhook dispatches; data joins (operator dashboard ↔
customer dashboard ↔ external systems); audit trails.

### Worked example (SUEZ POC SYN-06 inventory)

For the SUEZ POC engagement (`tranche_class: engagement`; FULL KIT
Commit 4 target), SYN-06 fires mandatorily. The 3 surfaces:

| Surface | SUEZ-POC-specific shape |
|:---|:---|
| **Operator dashboard** | `/operator/suez-poc/` carrying counterparty brief + Aïsha continuity-role briefing + commercial-schedule (`orchestration_broker_thin_margin`) + tranche progress (libellé generator + parc engins + PO normalisation) + Aïsha delegation status. |
| **Customer dashboard** | `/customer/suez-poc/` carrying Phase 1/2/3 milestone status + libellé generator output samples + parc engins lookup widget + Aïsha contact card. Recipient-fallback per SYN-10: email summaries to SUEZ rep on every milestone close + PDF architecture addendum on every Phase transition + Loom video for Phase 1 walkthrough. |
| **ERP workflow join** | `app/workflows/engagement-suez/` firing on Aïsha continuity tasks + sync to SUEZ CTO office replicability checklist + commercial settlement events into `finops.registered_fact`. |

Naming the 3 surfaces explicitly in the engagement-tranche-charter
frontmatter is the SYN-06 satisfaction; not naming them is the
SYN-06 FAIL the discipline catches BEFORE commit.

## Principle 4 — Compose the disposition AskQuestion so the operator can ratify in seconds, not minutes

Bad (raw finding-by-finding):

```
AskQuestion: SYN-04 brand-register-citation WARN finding. What to do?
  Options:
    1. fix
    2. defer
```

Good (per-finding rationale + recommended default per severity class):

```
AskQuestion: SUEZ FULL KIT synthesis sweep (engagement class; all 10 dims fired).
  3 FAIL + 2 WARN + 1 INFO surfaced; full report at
  reports/synthesis-suez-full-kit-2026-05-26.md.

  Finding #1: SYN-04 brand-register-citation FAIL — engagement-charter
    frontmatter missing audience-class-to-brand-register mapping.
    Recommended: scope-complete — add `brand_register_per_audience:`
    mapping `J-CU.suez-rep: translated-external` + `J-CO.aisha: internal-
    corpint-with-AL3-restriction` to the engagement-tranche-charter
    frontmatter (5-line edit; reversible). Ratify?
    [scope-complete (recommended) / scope-extend / defer-OPS]

  Finding #2: SYN-06 ERP-surface-citation FAIL — operator-dashboard +
    customer-dashboard surfaces named but ERP-workflow-join not cited.
    Recommended: scope-complete — add §"ERP workflow join" subsection
    naming app/workflows/engagement-suez/ + sync-to-SUEZ-CTO-office
    handoff per Aïsha-continuity-role (10-line edit; reversible). Ratify?
    [scope-complete (recommended) / scope-narrow / defer-OPS]

  ... (one option-set per finding; batch all in single AskQuestion call
       when total ≤ 10 findings; split into 2 batches when 11-20)
```

Each finding gets: severity class explicit + recommended default
(rationale embedded inline) + a 3-option subset of the 5-option enum
chosen per the finding's reversibility class.

When findings exceed 20, halt and propose splitting the tranche per
`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` §6 bandwidth-recovery pattern.

## Principle 5 — When `scope-extend` is the disposition, file the forward-pointer in the same chat

`scope-extend` is the safety valve that keeps tranches atomic without
losing the extended scope. But "extend later" with no follow-up
pointer is the silent-debt-accumulation anti-pattern. When ratifying
`scope-extend`, file ONE of:

1. **OPS_REGISTER row** — for operator-class follow-ups with a named
   owner + ETA. Append to
   `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/OPS_REGISTER.csv`.
2. **Tracker file** — for scope that needs more than a one-liner.
   Mint `docs/wip/planning/_trackers/<slug>-tracker.md` per the
   tracker template in
   [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../rules/akos-conflict-surfacing-and-blocker-trackers.mdc)
   §"Scope-overlap-tracker file shape" (adapt to scope-extend
   shape).
3. **`_candidates/` file** — for scope that's initiative-sized. Mint
   `docs/wip/planning/_candidates/i-nn-<slug>.md` with 3-paragraph
   scope sheet.

The pointer is filed in the SAME chat that dispositions the finding,
not deferred to the next session. Deferred pointer-filing is the
shape of the false-scope-creep the discipline catches.

## Principle 6 — Update operator-scratchpad BEFORE the tranche commits

The operator-scratchpad continuity dimension (this rule's RULE 1
sister discipline INTER_WAVE_REGRESSION dimension 12) is implicitly
enforced by SYN-05 (governance ratification lineage). Before any
in-scope tranche commits, the scratchpad MUST carry:

- Tranche ID + tranche class + classification rationale (one line).
- Synthesis sweep verdict (PASS / PASS-WITH-FOLLOWUP / FAIL) with
  finding count + disposition summary.
- Decision IDs minted at the tranche (D-IH-NN-X for ratifying
  decisions; D-IH-NN-Y for disposition decisions when novel).
- Forward-pointers filed (OPS row IDs; tracker paths; candidate file
  paths).
- Next-tranche forward-pointer (the next tranche-charter's slug +
  expected tranche-class).

The scratchpad entry is the operator's audit trail of synthesis
discipline application; it's also the next-session-continuity surface
when chat rolls over.

## Pre-flight checklist (walk mentally before posting any tranche-charter)

1. ✓ `tranche_class` resolved via Principle 1 decision tree (NOT
   defaulted silently).
2. ✓ Tranche-charter frontmatter drafted with: `tranche_id`,
   `tranche_class`, `tranche_title`, `audiences_named[]`,
   `channels_named[]` (if applicable), `scenarios_named[]` (if
   applicable), `brand_register_per_audience` (if non-J-OP-only),
   `ratifying_decisions[]`, `erp_surfaces_named[]` (if engagement
   class), `reversibility_class` + rationale, `closing_loop_test`,
   `recipient_fallback_channel` (if external surface).
3. ✓ `scripts/synthesis_before_tranche_check.py --check-charter
   <path>` invoked; findings table inspected.
4. ✓ Per-finding disposition mapped to one of 5 enum options with
   per-severity-class recommended default.
5. ✓ `AskQuestion` batch posted with one option-set per finding;
   total findings ≤ 10 per batch.
6. ✓ For every `scope-extend` ratify, the forward-pointer is filed in
   the same chat.
7. ✓ For every `scope-narrow` ratify, the removed scope is named in
   the synthesis report's SYN-07 row.
8. ✓ For every `escalate-to-blocker-tracker` ratify, the tracker file
   is minted in the same chat.
9. ✓ operator-scratchpad entry appended with tranche_id, class,
   verdict, decisions, forward-pointers.
10. ✓ Tranche commit assembled; UAT verdict line drafted ONLY AFTER
    synthesis sweep verdict is PASS or PASS-WITH-FOLLOWUP.

## Anti-patterns (recovery patterns)

- **Anti-pattern: classify silently** — most common failure when
  agent under pressure defaults to `internal_governance` for a tranche
  that's actually `engagement` or `external_deliverable`. Recovery:
  re-run synthesis under correct class; expect more findings; re-
  dispose.
- **Anti-pattern: synthesis-after-commit** — same shape as the
  operator's "false scope creep" framing. Recovery: amend the tranche
  if reversibility allows; OR file the post-hoc synthesis report as
  evidence-only and forward-charter the next tranche to apply
  synthesis-before.
- **Anti-pattern: SYN-06 cite operator-dashboard only, forget
  customer-dashboard + ERP-workflow-join** — partial citation passes
  the validator at INFO ramp but misses the operator's full design
  intent. Recovery: walk the 3 surfaces per Principle 3 worked
  example; amend the tranche-charter.
- **Anti-pattern: ratify `scope-extend` without filing forward-pointer**
  — the silent-debt-accumulation shape. Recovery: file the pointer
  retroactively in the same chat; never let the disposition close
  without the pointer.
- **Anti-pattern: post the `AskQuestion` with one finding per call**
  — exhausts the operator's bandwidth + breaks the batching guidance.
  Recovery: re-compose into ≤ 10 findings per call; split into 2
  calls when 11-20.
- **Anti-pattern: defer the operator-scratchpad entry to next session**
  — breaks the continuity audit trail. Recovery: write the entry
  before the commit; never let "I'll catch up next session" rationale
  win.

## Recovery pattern: tranche-charter retroactive backfill

When a pre-2026-05-25 tranche needs to be re-validated under this
discipline (e.g., I86 cluster wave-close UATs), the retroactive
backfill pattern:

1. Mint a `tranche-charter` retroactive file at
   `docs/wip/planning/<initiative>/charters/<tranche-slug>.tranche-charter.md`
   capturing the tranche's as-shipped scope using current canonical
   tag values.
2. Run `--check-charter` against the retroactive file.
3. Document findings as RETRO-class (no commit changes).
4. File any high-severity findings as forward-charters for the next
   in-scope tranche to inherit + remediate.

Per `SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` §9 migration posture, the
discipline is forward-only from this rule's mint commit; retroactive
backfill is OPTIONAL and used only when the operator explicitly
requests it.

## Cross-references

- Doctrine: [`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md).
- Cursor rule: [`akos-synthesis-before-tranche.mdc`](../../rules/akos-synthesis-before-tranche.mdc) — the *when* layer.
- Paired SOP: [`SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md).
- Runbook: [`scripts/synthesis_before_tranche_check.py`](../../../scripts/synthesis_before_tranche_check.py).
- Validator: [`scripts/validate_synthesis_before_tranche.py`](../../../scripts/validate_synthesis_before_tranche.py).
- Pydantic chassis: [`akos/hlk_synthesis_before_tranche.py`](../../../akos/hlk_synthesis_before_tranche.py).
- Sister skill: [`inline-ratify-craft`](../inline-ratify-craft/SKILL.md) — disposition `AskQuestion` craft per Principle 4.
- Sister skill: [`index-integrity-craft`](../index-integrity-craft/SKILL.md) — Wave N specialty mint precedent for pre-flight checklist shape.
- Sister skill: [`collaborator-share-craft`](../collaborator-share-craft/SKILL.md) — Wave R+1 13th specialty mint precedent for per-pattern decision-tree shape.
- Sister discipline doctrines: [`INDEX_INTEGRITY_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md), [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md), [`UAT_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md), [`COLLABORATOR_SHARE_DOCTRINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md).
