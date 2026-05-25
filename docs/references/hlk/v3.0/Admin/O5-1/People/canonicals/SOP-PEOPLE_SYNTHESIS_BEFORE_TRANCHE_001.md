---
title: SOP — People Synthesis Before Tranche
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001
access_level: 5
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Founder/CEO
co_authors:
  - PMO
  - People Operations Lead
last_review: 2026-05-25
last_review_by: Founder/CEO
last_review_decision_id: D-IH-86-EA
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-EA
  - D-IH-86-EB
  - D-IH-86-EC
  - D-IH-86-ED
  - D-IH-86-EE
status: charter
register: internal
linked_canonicals:
  - SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - INDEX_INTEGRITY_DISCIPLINE.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - UAT_DISCIPLINE.md
  - COLLABORATOR_SHARE_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/process_list.csv
  - ../Compliance/canonicals/DECISION_REGISTER.csv
  - ../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
linked_runbooks:
  - scripts/synthesis_before_tranche_check.py
  - scripts/validate_synthesis_before_tranche.py
linked_processes:
  - hol_peopl_dtp_synthesis_before_tranche_001
cadence: event_triggered
cadence_trigger: tranche-charter authored OR tranche pre-commit OR wave-charter OR engagement charter OR specialty mint OR canonical CSV mint OR brand surface deploy OR external deliverable ship
cadence_secondary: scheduled
cadence_secondary_schedule: pre_commit self-test (always-on)
---

# SOP — People Synthesis Before Tranche

## Purpose

Operationalise the synthesis-before-tranche discipline named in
[`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md).
For every tranche of work that approaches commit-time
(engagement / specialty_mint / internal_governance with non-J-OP
audience / canonical_csv_mint / brand_surface / external_deliverable),
the People area runs a deterministic 7-step workflow that classifies
the tranche, resolves the per-class dimension fire-set, runs the
synthesis sweep, dispositions findings, files forward-pointers, and
updates the operator-scratchpad before the tranche's atomic commit
lands.

The SOP is the **human-or-AIC-readable contract**; the paired runbook
[`scripts/synthesis_before_tranche_check.py`](../../../../../../scripts/synthesis_before_tranche_check.py)
+ validator
[`scripts/validate_synthesis_before_tranche.py`](../../../../../../scripts/validate_synthesis_before_tranche.py)
are the **agent-readable executable contract** per
[`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
Rule 1 (paired SOP+runbook). Both surfaces are SSOT for the same
process. The cursor rule
[`akos-synthesis-before-tranche.mdc`](../../../../../../.cursor/rules/akos-synthesis-before-tranche.mdc)
governs *when* this SOP fires; the paired skill
[`.cursor/skills/synthesis-before-tranche-craft/SKILL.md`](../../../../../../.cursor/skills/synthesis-before-tranche-craft/SKILL.md)
codifies *how* to apply it well.

## Scope

In-scope tranches (per cursor rule "When this rule applies"):

- All 6 tranche classes per `VALID_TRANCHE_CLASSES`:
  **engagement**, **specialty_mint**, **internal_governance** (non-J-OP
  audience OR ≥ 3 files), **canonical_csv_mint**, **brand_surface**,
  **external_deliverable**.
- Tranches with ≥ 5 files in one commit OR touching any canonical CSV.
- Tranches carrying a `tranche_class:` frontmatter tag in a master-
  roadmap, candidate, or `.tranche-charter.md` file.
- Operator-requested on-demand sweeps.

Out of scope (per
[`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md)
§9):

- Chore-only commits (typos, link-rot, formatting, CHANGELOG-only).
- Per-engagement WIP synthesis under `docs/wip/intelligence/`.
- Internal helper modules with no audience/channel/scenario impact.
- Pre-2026-05-25 already-shipped tranches (forward-only discipline).

## Roles

| Role | Responsibility |
|:---|:---|
| **Founder/CEO** (interim primary actor; current operator) | Author tranche-charter; classify tranche-class via inline-ratify when unclear; ratify finding dispositions; co-sign the synthesis report. |
| **PMO** (current standing role) | Co-sign cluster-coordinator tranches (e.g., I86 wave-close charters); maintain the synthesis report index under `docs/wip/planning/<initiative>/reports/`. |
| **People Operations Lead** (current standing role) | Maintain the cursor rule + skill + this SOP + doctrine in sync as the discipline matures from charter → active → promoted; review per-tranche-class fire rules quarterly. |
| **AIC role_owner** (per `akos-people-discipline-of-disciplines.mdc` Rule 1) | An AIC operating in PMO or People Operations role may execute this SOP exactly like a human (AC-HUMAN side); MUST honor the 5-option disposition enum + cannot auto-default irreversible findings. |

## Inputs

- The tranche's draft files (NOT yet committed).
- (When available) a tranche-charter file at
  `docs/wip/planning/<initiative>/charters/<tranche-slug>.tranche-charter.md`
  with YAML frontmatter conforming to `SynthesisTrancheCharter` Pydantic
  schema.
- (When inline-CLI mode) the tranche_id + tranche_class + audiences +
  ratifying_decisions + reversibility + closing_loop_test as CLI args.
- The parent initiative's master-roadmap + decision-log for cross-
  reference.
- Operator-scratchpad current state for continuity context.

## Steps

### Step 1 — Classify the tranche-class (AC-HUMAN entry point)

Walk Principle 1 decision tree from
[`.cursor/skills/synthesis-before-tranche-craft/SKILL.md`](../../../../../../.cursor/skills/synthesis-before-tranche-craft/SKILL.md):

- Does the tranche ship value to a counterparty via a deliverable,
  surface, or service? If yes → external_deliverable OR engagement OR
  brand_surface (per sub-tree).
- Does it mint or modify a canonical CSV? → canonical_csv_mint.
- Does it mint a new Quality Fabric specialty? → specialty_mint.
- Otherwise → internal_governance.

When unclear, post an inline-ratify `AskQuestion` per
[`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc)
+ paired
[`inline-ratify-craft`](../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md)
skill: present 2-3 candidate tranche-classes with rationale; ratify
explicitly before drafting the tranche-charter frontmatter.

**Output of Step 1:** explicit `tranche_class` value drawn from
`VALID_TRANCHE_CLASSES` frozen-set.

### Step 2 — Draft the tranche-charter

Author a tranche-charter file at
`docs/wip/planning/<initiative>/charters/<tranche-slug>.tranche-charter.md`
(or inline as `--tranche-id` + `--tranche-class` + ancillary CLI args
when no persistent charter file is warranted). Frontmatter MUST
conform to `SynthesisTrancheCharter`:

```yaml
---
tranche_id: <unique-tranche-slug>           # e.g., "i86-wave-rplus1-p3-commit-2c-a"
tranche_class: <one-of-6-classes>            # from Step 1
tranche_title: <readable title>
audiences_named: [<audience-tags>]           # e.g., [J-OP, J-AIC] or [J-CU, J-CO]
channels_named: [<channel-tags>]             # optional; from CHANNEL_TOUCHPOINT_REGISTRY
scenarios_named: [<scenario-slugs>]          # optional; from PERSONA_SCENARIO_REGISTRY
brand_register_per_audience:                 # required when audiences include non-J-OP
  <audience-tag>: <internal-corpint OR translated-external OR custom-with-rationale>
ratifying_decisions: [<D-IH-NN-X>, ...]      # required (SYN-05)
erp_surfaces_named:                          # required for engagement class; recommended for others
  - operator_dashboard: <path-or-N/A>
  - customer_dashboard: <path-or-N/A>
  - erp_workflow_join: <path-or-N/A>
reversibility_class: <low | medium | high>   # required (SYN-08)
reversibility_rationale: <one-line>
closing_loop_test: <one-line>                # required (SYN-09)
recipient_fallback_channel: <one-line>       # required for external surface tranches
---
```

When a field is genuinely N/A for the tranche-class, set it to the
empty list / N/A explicitly with a one-line rationale; never leave
required-for-class fields unset.

### Step 3 — Run the synthesis sweep

Invoke the runbook:

```sh
py scripts/synthesis_before_tranche_check.py --check-charter <path>
```

OR (inline mode):

```sh
py scripts/synthesis_before_tranche_check.py \
  --tranche-id <slug> --tranche-class <class> \
  --audiences <J-OP,J-CU,...> \
  --ratifying-decisions <D-IH-NN-X,...> \
  --reversibility <low|medium|high> \
  --closing-loop-test "<text>" \
  --emit-report
```

The runbook dispatches the per-tranche-class fire-set (resolved via
`akos.hlk_synthesis_before_tranche.resolve_fire_set(tranche_class,
conditional_triggers=True)`) and emits a synthesis report at
`docs/wip/planning/<initiative>/reports/synthesis-<tranche-id>-<YYYY-MM-DD>.md`
when `--emit-report` is passed.

**Inspect the findings table.** Each row carries:
- Dimension code (SYN-NN-NAME)
- Finding status (PASS / WARN / FAIL / INFO / N/A)
- Finding text (per-dimension probe explanation)
- Recommended disposition + reversibility class

### Step 4 — Disposition findings via inline-ratify

For every WARN / FAIL / INFO finding, walk
[`.cursor/skills/synthesis-before-tranche-craft/SKILL.md`](../../../../../../.cursor/skills/synthesis-before-tranche-craft/SKILL.md)
Principle 4 composition pattern and post a batched `AskQuestion`:

- ≤ 10 findings → one batched `AskQuestion`.
- 11-20 findings → split into 2 batches.
- > 20 findings → halt and propose splitting the tranche per
  [`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md)
  §6 bandwidth-recovery pattern.

The 5-option disposition enum (per
[`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md)
§6 + `D-IH-86-EC`):

1. **scope-complete** — extend the tranche scope; re-run sweep; commit when clean.
2. **scope-extend** — file forward-pointer; commit this tranche as-is.
3. **scope-narrow** — narrow tranche scope; defer removed scope.
4. **defer-OPS** — low-priority gap; OPS_REGISTER row.
5. **escalate-to-blocker-tracker** — mint `_blockers/<slug>-tracker.md`.

Time-box recovery applies only to reversible dispositions per
[`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc)
§"Time-box recovery". Irreversible dispositions NEVER auto-default —
halt and escalate per
[`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc).

### Step 5 — Apply ratified scope adjustments

Apply the ratified `scope-complete` and `scope-narrow` adjustments to
the tranche's draft files. Re-run Step 3 to confirm
`synthesis_complete == true` (no FAIL findings + WARN findings either
ratified `scope-extend` with pointer or `defer-OPS` with tracker
entry).

### Step 6 — File forward-pointers + update operator-scratchpad

For every `scope-extend` ratify, file ONE of (per skill Principle 5):

- OPS_REGISTER row in
  `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/OPS_REGISTER.csv`
  with named owner + ETA.
- Tracker file at `docs/wip/planning/_trackers/<slug>-tracker.md`.
- Candidate file at `docs/wip/planning/_candidates/i-nn-<slug>.md`
  when extension is initiative-sized.

For every `escalate-to-blocker-tracker` ratify, mint the tracker file
per
[`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc)
§"Blocker-tracker file shape".

Update the operator-scratchpad (per skill Principle 6) with:
- Tranche ID + class + classification rationale.
- Synthesis sweep verdict + finding counts + disposition summary.
- Decision IDs minted.
- Forward-pointer paths filed.
- Next-tranche forward-pointer.

### Step 7 — Commit the tranche atomically

Land the tranche files + synthesis report + scratchpad update + (when
applicable) OPS_REGISTER + tracker + candidate file in ONE atomic
commit. The commit message MUST cite:

- Tranche ID + class.
- Synthesis verdict (PASS / PASS-WITH-FOLLOWUP / FAIL).
- Ratifying decision IDs.
- Disposition summary (e.g., "5 findings: 3 scope-complete + 2
  scope-extend with OPS pointers").

The tranche's UAT verdict line (when a UAT report applies) fills in
ONLY AFTER Step 7 — synthesis-before is the design pre-flight; UAT is
the post-commit verdict.

## Outputs

- Synthesis report markdown at
  `docs/wip/planning/<initiative>/reports/synthesis-<tranche-id>-<YYYY-MM-DD>.md`.
- Tranche-charter file at
  `docs/wip/planning/<initiative>/charters/<tranche-slug>.tranche-charter.md`
  (when persistent).
- Forward-pointer artifacts (OPS_REGISTER rows / tracker files /
  candidate files) per ratified dispositions.
- Operator-scratchpad entry per Step 6.
- Atomic tranche commit per Step 7.
- (Indirect) Updated DECISION_REGISTER rows when novel ratifying
  decisions or disposition decisions are minted.

## Verification

| Verification check | Tool / surface |
|:---|:---|
| Pydantic chassis intact (10-dim enum + 6-class enum + 5-option enum + 3-reversibility enum + per-class fire rules) | `py scripts/validate_synthesis_before_tranche.py --self-test` (always-on; pre_commit profile) |
| Runbook dispatch coverage (10 probes mapped to 10 dimensions) | `py scripts/synthesis_before_tranche_check.py --self-test` (always-on; pre_commit profile) |
| Tranche-charter parses to `SynthesisTrancheCharter` | `py scripts/synthesis_before_tranche_check.py --check-charter <path>` |
| Synthesis report generated cleanly with per-dimension findings | Inspect `reports/synthesis-<tranche-id>-<YYYY-MM-DD>.md` |
| `synthesis_complete == true` before commit | Synthesis report §Summary line |
| Per-finding disposition recorded with decision ID | Synthesis report §Findings + DECISION_REGISTER append |
| Forward-pointer artifact filed for every scope-extend ratify | OPS_REGISTER append OR tracker file OR candidate file |
| Operator-scratchpad updated before commit | `docs/wip/intelligence/operator-scratchpad.md` last entry timestamp |

## Acceptance criteria

### AC-HUMAN (per `akos-executable-process-catalog.mdc` Rule 1 §5)

A human OR an AIC role_owner (PMO interim; COO when activated) CAN
execute the synthesis sweep + dispose findings following this SOP
without invoking the runbook by:

1. Reading the tranche-charter (or drafting one if absent).
2. Walking Steps 1-7 in order, with the per-dimension fire-rule
   reference table from
   [`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md)
   §2 open.
3. Authoring the synthesis report markdown by hand per the per-
   dimension worked examples in the doctrine §11 + the paired skill.
4. Posting the disposition `AskQuestion` batch per skill Principle 4.
5. Filing forward-pointers + scratchpad entry per Step 6.
6. Committing per Step 7.

The runbook is the automation surface; the SOP IS the readable
contract that an AIC OR a human follows without it.

### AC-AUTOMATION (per `akos-executable-process-catalog.mdc` Rule 1 §5)

The runbook
[`scripts/synthesis_before_tranche_check.py`](../../../../../../scripts/synthesis_before_tranche_check.py)
fires unattended at:

- `--self-test` mode in pre_commit + release-gate (always-on; ~3s
  combined with validator).
- `--check-charter <path>` mode when invoked by an agent or the
  operator with a charter file.
- `--tranche-id <slug> --tranche-class <class> [--audiences ...]
  [--ratifying-decisions ...] [--reversibility ...] [--closing-loop-
  test ...]` inline-CLI mode for ad-hoc sweeps without a charter
  file.
- `--emit-report` toggles persistent synthesis-report markdown output
  to `--reports-dir` (default
  `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/`).

Both AC-HUMAN and AC-AUTOMATION acceptance are required for the
discipline to satisfy
[`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
Rule 1.

## Per-tranche-class step routing

| Tranche class | Step 1 default | Step 2 frontmatter focus | Step 3 fire-set count | Step 4 typical finding density |
|:---|:---|---:|---:|---:|
| **engagement** | classify via Q1a/Q1b sub-tree | erp_surfaces_named MANDATORY; recipient_fallback_channel MANDATORY | 10 | 5-10 |
| **specialty_mint** | recursive self-application | ratifying_decisions for the specialty's D-IH-NN-X quartet | 7 baseline + SYN-03 conditional | 3-7 |
| **internal_governance** | check non-J-OP audience trigger | minimum frontmatter; brand_register N/A when J-OP-only | 3 baseline + 4 conditional | 1-4 |
| **canonical_csv_mint** | check dashboard surfacing trigger | ratifying_decisions + closing_loop_test (validator self-test) | 6 baseline + 3 conditional | 3-7 |
| **brand_surface** | check engagement-scoping trigger | brand_register_per_audience MANDATORY | 9 baseline + SYN-06 conditional | 4-8 |
| **external_deliverable** | always all-10 | erp_surfaces_named for engagement-deliverables; recipient_fallback_channel MANDATORY | 10 | 6-12 |

## ERP-engagement-governance UX shape (primary worked example per Q-A ratify)

When the tranche class is `engagement` (or `brand_surface` /
`canonical_csv_mint` with engagement scope), SYN-06 fires the 3-
surface citation requirement. The operator's verbatim framing at
2026-05-25 Q-A:

> *"the main goal is to properly govern our engagements via cleverly
> crafting erp workflow and UX just like i want my dashboard they
> would also like to have it (even if they don't log so much or see
> it that much and i send them info via traditional means or drives)"*

The 3 surfaces (per
[`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md)
§11) are:

### Surface 1 — Operator dashboard (Holistika-side)

`/operator/<engagement-slug>/` in HLK-ERP. Holds: counterparty brief;
objections brief; commercial schedule; settlement statements; tranche
progress; risk flags; AIC delegations.

### Surface 2 — Customer dashboard (counterparty-side)

`/customer/<engagement-slug>/` in HLK-ERP OR integrated into
counterparty's own ERP. Holds: read-only views; milestone deliverables;
settlement summaries; status updates; AI-assisted summaries.

**Recipient-fallback (SYN-10):** customer dashboard MUST carry a
traditional-means counterpart (email summary; PDF report; SMS update)
for counterparties who don't log often. Operator framing: *"even if
they don't log so much or see it that much and i send them info via
traditional means or drives"*.

### Surface 3 — ERP workflow join

`app/workflows/<engagement-class>/` + runbook scripts firing on
tranche close events. Holds: state transitions; webhook dispatches;
data joins; audit trails.

### SUEZ POC worked example (Commit 4 target)

For the SUEZ POC engagement (`tranche_class: engagement`; commercial
shape `orchestration_broker_thin_margin` per Aïsha continuity row +
founder + ≥ 1 exec collab; per
[`COLLABORATOR_SHARE_DOCTRINE.md`](COLLABORATOR_SHARE_DOCTRINE.md)
§3.2), SYN-06 fires mandatorily. The 3 surfaces:

| Surface | SUEZ-POC-specific shape |
|:---|:---|
| Operator dashboard | `/operator/suez-poc/` carrying counterparty brief + Aïsha continuity-role briefing + commercial-schedule + tranche progress (libellé generator + parc engins + PO normalisation) + Aïsha delegation status. |
| Customer dashboard | `/customer/suez-poc/` carrying Phase 1/2/3 milestone status + libellé generator output samples + parc engins lookup widget + Aïsha contact card. **Recipient-fallback per SYN-10:** email summaries to SUEZ rep on every milestone close + PDF architecture addendum on every Phase transition + Loom video for Phase 1 walkthrough. |
| ERP workflow join | `app/workflows/engagement-suez/` firing on Aïsha continuity tasks + sync to SUEZ CTO office replicability checklist + commercial settlement events into `finops.registered_fact`. |

Naming the 3 surfaces explicitly in the SUEZ engagement-tranche-charter
frontmatter (Commit 4) IS the SYN-06 satisfaction. Failing to name
them is the FAIL the discipline catches BEFORE the SUEZ FULL KIT
commits.

## Cadence

- **pre_commit (always-on)** — `--self-test` mode of validator +
  runbook runs at every `py scripts/verify.py pre_commit` invocation
  via `validate_synthesis_before_tranche_self_test` +
  `synthesis_before_tranche_check_self_test` steps in
  [`config/verification-profiles.json`](../../../../../../config/verification-profiles.json).
  Cost ~3s combined. Ensures the chassis is always intact.
- **tranche-charter (event-triggered)** — full sweep runs once when a
  new tranche-charter is authored OR an in-scope tranche approaches
  commit.
- **tranche pre-commit (event-triggered)** — full sweep runs immediately
  BEFORE the tranche's atomic commit (the design-layer pre-flight).
  This is the load-bearing cadence — the discipline's value comes
  from running here, not after.
- **on-demand (operator request)** — full sweep runs when the
  operator explicitly requests an audit of a past tranche or a sweep
  of a candidate-stage scope.

## Cross-references

- Parent doctrine: [`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md).
- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).
- Sister disciplines:
  [`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md) (post-commit baseline-index freshness),
  [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md) (post-commit inter-wave regression),
  [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) (post-commit acceptance evidence),
  [`COLLABORATOR_SHARE_DOCTRINE.md`](COLLABORATOR_SHARE_DOCTRINE.md) (engagement-economic axis; 13th specialty).
- Cursor rule: [`akos-synthesis-before-tranche.mdc`](../../../../../../.cursor/rules/akos-synthesis-before-tranche.mdc) — the *when* layer.
- Paired skill: [`.cursor/skills/synthesis-before-tranche-craft/SKILL.md`](../../../../../../.cursor/skills/synthesis-before-tranche-craft/SKILL.md) — the *how* layer.
- Paired runbook: [`scripts/synthesis_before_tranche_check.py`](../../../../../../scripts/synthesis_before_tranche_check.py).
- Paired validator: [`scripts/validate_synthesis_before_tranche.py`](../../../../../../scripts/validate_synthesis_before_tranche.py).
- Pydantic chassis: [`akos/hlk_synthesis_before_tranche.py`](../../../../../../akos/hlk_synthesis_before_tranche.py).
- Process catalog (forward-charter; lands at Commit 2c-b):
  `hol_peopl_dtp_synthesis_before_tranche_001`.
- Pattern registry row (forward-charter; lands at Commit 2c-b):
  `pattern_synthesis_before_tranche_discipline`.
- Decision lineage: D-IH-86-EA (doctrine mint + INFO ramp), D-IH-86-EB (10-dimension probe set), D-IH-86-EC (5-option disposition enum + per-tranche-class firing), D-IH-86-ED (INFO→FAIL ramp + broad-fire cadence), D-IH-86-EE (paired SOP+runbook gate; ratified at the cursor rule's mint commit alongside this SOP).
