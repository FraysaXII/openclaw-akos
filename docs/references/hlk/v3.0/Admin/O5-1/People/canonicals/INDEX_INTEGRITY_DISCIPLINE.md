---
title: Index Integrity Discipline
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
last_review_decision_id: D-IH-86-CD
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-CD
  - D-IH-86-CE
  - D-IH-86-CF
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - UAT_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
linked_cursor_rules:
  - .cursor/rules/akos-index-integrity.mdc
  - .cursor/rules/akos-planning-traceability.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-inter-wave-regression.mdc
  - .cursor/rules/akos-docs-config-sync.mdc
  - .cursor/rules/akos-inline-ratification.mdc
linked_skills:
  - .cursor/skills/index-integrity-craft/SKILL.md
  - .cursor/skills/inline-ratify-craft/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
forward_charters:
  - process_list.csv row hol_peopl_dtp_index_integrity_001
  - PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_index_integrity_discipline
  - paired runbook scripts/baseline_index_sweep.py (Wave N P3)
  - paired validator scripts/validate_index_freshness.py (Wave N P3)
  - .cursor/rules/akos-index-integrity.mdc (mechanical drift gate companion)
  - .cursor/skills/index-integrity-craft/SKILL.md (the *how* layer)
---

# Index Integrity Discipline

> The People-area canonical that names the cadence and content of index-
> freshness sweeps performed at every wave-close gate AND at every
> canonical-CSV mint. Eleventh specialty instantiation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) (per
> D-IH-86-CD) and sister to [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md);
> codifies `compose_INDEX(governance) -> 8-dimension index-freshness sweep
> + deterministic-fix runbook + INFO→FAIL drift ramp`.

## 1. Purpose

Every Holistika collaborator (human, agent, AIC) reads **baseline index
documents** first to orient themselves before doing substantive work.
The planning README tells them what initiatives exist. PRECEDENCE.md
tells them which assets are canonical vs mirrored. CHANGELOG.md tells
them what shipped recently. INITIATIVE_DEPENDENCIES.md tells them what
gates what. USER_GUIDE.md HLK Operator Model tells them how many roles
and processes are active. ARCHITECTURE.md HLK Registry tells them which
canonical CSVs exist. Dashboards render the current operational state.

When any of these index documents falls out of sync with its source-of-
truth (the canonical CSV or the filesystem), every downstream
collaborator inherits the drift. They draft against stale counts. They
forget to update PRECEDENCE when a new CSV ships. They cite an
initiative as "active" that was closed three waves ago. The cost is
compounding: drift compounds because every wave that doesn't catch it
adds new drift on top.

This canonical names that **index integrity is itself a discipline** —
not a one-off chore but a recurring cadence with a paired runbook + a
paired validator + a paired cursor rule + a paired skill. The 8
dimensions below name what to check; the runbook fixes what is fixable
deterministically; the validator catches drift before commit; the
operator scratchpad records what was fixed and what was deferred.

## 2. The 8 dimensions

Every sweep runs the following 8 probes:

| # | Dimension code | Index document | Source-of-truth | Probe heuristic |
|:--|:---|:---|:---|:---|
| 1 | **IDX-01-PLANNING-README-INITIATIVE-COUNT** | [`docs/wip/planning/README.md`](../../../../../wip/planning/README.md) | Filesystem (NN- folders) + [`INITIATIVE_REGISTRY.csv`](../Compliance/canonicals/INITIATIVE_REGISTRY.csv) | Count of NN- folders ↔ count of rows in README initiative table ↔ active/closed status mentioned in README ↔ INITIATIVE_REGISTRY status column. Any mismatch is drift. |
| 2 | **IDX-02-PRECEDENCE-CSV-COVERAGE** | [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md) | Filesystem (every `*.csv` under `compliance/canonicals/` + `compliance/canonicals/dimensions/`) | Every CSV file must have a row in PRECEDENCE.md naming its canonical class + mirror class. Missing rows are gaps. Rows pointing to nonexistent files are drift. |
| 3 | **IDX-03-CHANGELOG-WAVE-COVERAGE** | [`CHANGELOG.md`](../../../../../../CHANGELOG.md) | Git log (most recent commit message wave letter) + I86 master-roadmap wave list | Most recent wave-closing commit (e.g., 'I86 Wave M.5' or 'I86 Wave N') must have at least one corresponding bullet under `[Unreleased]` or a recent release section. Multi-wave gap is drift. |
| 4 | **IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS** | [`INITIATIVE_DEPENDENCIES.md`](../Compliance/canonicals/INITIATIVE_DEPENDENCIES.md) | `INITIATIVE_REGISTRY.csv` (most recent active/closed row) | Last-update of INITIATIVE_DEPENDENCIES.md ↔ last new/closed initiative in registry (within 7 days). Stale > 7 days when registry changed = drift. |
| 5 | **IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS** | [`docs/USER_GUIDE.md`](../../../../../../USER_GUIDE.md) HLK Operator Model section | [`baseline_organisation.csv`](../Compliance/canonicals/baseline_organisation.csv) + [`process_list.csv`](../Compliance/canonicals/process_list.csv) | Any number stated in USER_GUIDE (e.g., "29 roles", "1088 processes") must match a deterministic count from the canonical CSV. Mismatch is drift. Conditional: fires only when canonical CSV row count changes. |
| 6 | **IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE** | [`docs/ARCHITECTURE.md`](../../../../../../ARCHITECTURE.md) HLK Registry section | Filesystem (every `*.csv` under `compliance/canonicals/dimensions/`) | Every dimension CSV mentioned in ARCHITECTURE HLK Registry table must exist on disk. Every dimension CSV on disk should have a row in the table. Conditional: fires only when dimensions/ folder gains/loses a CSV. |
| 7 | **IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY** | [`docs/wip/planning/README.md`](../../../../../wip/planning/README.md) initiative table | Filesystem (`docs/wip/planning/NN-*/` folders, excluding `_blockers/`, `_trackers/`, `_candidates/`, `_templates/`, `99-proposals/`, `_dashboards/`) | Every NN- folder must have a row in the README table. Every row must point to an existing folder. Bidirectional FK. |
| 8 | **IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT** | [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) §6 specialty materialisation table | Filesystem (every `*_DISCIPLINE.md` under `People/canonicals/`) + this canonical's frontmatter linked_canonicals | The §6 table row count ↔ count of specialty *_DISCIPLINE.md files. Mismatch is drift (new specialty minted but not yet rolled into the umbrella) OR gap (specialty named in §6 but file missing). |

6 dimensions (1-4, 7-8) are **baseline + always fire** at every sweep
trigger. 2 dimensions (5-6) are **conditional** — they fire only when the
relevant source-of-truth has changed (CSV row count delta for IDX-05;
dimensions/ folder delta for IDX-06). This split mirrors the
INTER_WAVE_REGRESSION 7-baseline + 5-conditional pattern (Wave M
precedent).

## 3. The compose_INDEX rule

The fabric's compose() rule, specialised for index integrity:

```
compose_INDEX(governance) -> 8-dimension sweep
  where:
    baseline_dimensions = {IDX-01, IDX-02, IDX-03, IDX-04, IDX-07, IDX-08}  # 6 always fire
    conditional_dimensions = {IDX-05, IDX-06}                                # fire on delta
    deterministic_fix_runbook = scripts/baseline_index_sweep.py --fix
    judgement_call_fix = inline-ratify per akos-inline-ratification.mdc
```

INDEX_INTEGRITY depends **only on the governance axis** — every
baseline index document is governance-bound (PRECEDENCE classifies it;
DECISION_REGISTER ratifies edits to it; INITIATIVE_REGISTRY tracks it).
The other 4 axes (audience, channel, scenario, brand) are not
load-bearing for index documents because the audience is always J-OP /
J-AIC (operator-internal), the channel is always read-from-repo, the
scenario is always orientation/lookup, and the brand axis is internal
register.

## 4. Cadence

Default cadence: **every wave-close** (sweep_trigger = `wave_close`) +
**every canonical-CSV mint** (sweep_trigger = `canonical_csv_mint`).
Exceptions:

- **Chore-only commits** (typo fixes, link-rot fixes, formatting): exempt
  entirely.
- **Multi-commit waves**: sweep at wave-close only, not per-commit.
- **Canonical-CSV-mint cadence**: a mint that adds < 3 rows to an
  existing CSV MAY skip the sweep if the affected dimensions are
  conditional (IDX-05, IDX-06) and the operator records the skip
  explicitly in the operator-scratchpad.
- **Pre-commit self-test** (sweep_trigger = `pre_commit_self_test`):
  always-on, zero-cost, validates Pydantic fixtures only (not real
  index drift). Wired into `release-gate.py` per D-IH-86-CD.

No other exemptions. "We're in a hurry" / "we'll do it next wave" are
NOT exemptions per the operator's 2026-05-21 framing.

## 5. Drift gate INFO → FAIL ramp

Per D-IH-86-CD, the validator [`scripts/validate_index_freshness.py`](../../../../../../../scripts/validate_index_freshness.py)
runs at **INFO** during the Wave N backfill window (planning README,
PRECEDENCE, CHANGELOG, INITIATIVE_DEPENDENCIES, dashboards, USER_GUIDE,
ARCHITECTURE all need their backfill commits before FAIL is reasonable).

Promotion to **FAIL** requires:

1. Wave N N.4 backfill commit lands all 7 baseline index documents in
   sync with their source-of-truth.
2. One full sweep (sweep_trigger = `wave_close` at Wave N close) emits
   `drift_count == 0 AND gap_count == 0` (skip/blocked allowed).
3. Operator-explicit ratification of the FAIL promotion in
   DECISION_REGISTER (`D-IH-86-CD` rationale or a successor row).

Until promotion to FAIL, the validator emits INFO findings that the
operator reviews via the wave-close UAT report's mechanical-evidence
section.

## 6. Findings disposition via inline-ratify 5-option enum

Every drift/gap/blocked finding from the sweep is dispositioned via an
inline `AskQuestion` gate per [`akos-inline-ratification.mdc`](../../../../../../../.cursor/rules/akos-inline-ratification.mdc) +
the paired [`inline-ratify-craft`](../../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md) skill,
using the 5-option enum:

1. **deterministic-fix-now** — invoke `scripts/baseline_index_sweep.py
   --fix --dimension <IDX-NN>` to repair the drift mechanically (default
   for drift findings on IDX-01, IDX-02, IDX-07, IDX-08 which have
   deterministic-fix paths).
2. **manual-fix-now** — operator or agent edits the index document by
   hand to repair the drift (default for drift findings on IDX-03, IDX-04,
   IDX-05, IDX-06 which involve narrative prose the runbook cannot
   safely auto-edit).
3. **defer-OPS** — record the finding as an OPS_REGISTER row for next
   wave (default for low-severity gap findings + skip findings).
4. **accept-as-canon** — operator ratifies the drift was deliberate (e.g.,
   the README intentionally lags the registry until the next manual
   sweep); appends a contra-precedent note + decision row.
5. **escalate-to-blocker-tracker** — cannot be dispositioned in-chat;
   mints `_blockers/<slug>-tracker.md` per [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc).

When findings exceed 10, the agent splits the gates into 2
`AskQuestion` batches (inline-ratify-craft Principle 5 batching).
Time-box recovery: 24h+ operator silence + clean validators +
reversible dispositions auto-default to the recommended option;
irreversible dispositions never auto-default.

## 7. The paired runbook contract

The runbook [`scripts/baseline_index_sweep.py`](../../../../../../../scripts/baseline_index_sweep.py)
implements the 8 probes + 4 deterministic-fix paths. Modes:

- `--self-test`: validates Pydantic fixtures only; ~50ms; wired into
  `release-gate.py` + `pre_commit` profile.
- `--check`: runs all 8 probes; emits findings; exit 0 (always — INFO
  posture during Wave N backfill window).
- `--fix --dimension <IDX-NN>`: deterministic-fix path for the named
  dimension; runs the probe, applies the fix, re-runs the probe,
  asserts fresh. Supported dimensions: IDX-01 (rewrite README initiative
  table from filesystem + registry), IDX-02 (append missing PRECEDENCE
  rows from filesystem scan), IDX-07 (rewrite README initiative table
  from filesystem), IDX-08 (rewrite Quality Fabric §6 table from
  filesystem). Other dimensions require manual fix (no deterministic
  path exists today).
- `--sweep-trigger <trigger> --output <path>`: full sweep at one of
  the 4 cadence triggers; emits markdown + JSON.

The runbook respects `compose_INDEX(governance)` — it reads governance-
axis canonicals only (no audience / channel / scenario / brand inputs)
and does not modify any artifact outside the 8 named indexes (no
collateral edits).

## 8. The paired SOP contract

The SOP [`SOP-PEOPLE_INDEX_INTEGRITY_001.md`](SOP-PEOPLE_INDEX_INTEGRITY_001.md)
is the human-facing operator-readable counterpart per
[`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1. AC-HUMAN acceptance: any human or AIC role_owner (PMO interim;
COO when activated per I76) can run the sweep + dispose the findings
following the SOP without invoking the runbook. AC-AUTOMATION
acceptance: the runbook fires unattended at wave-close +
canonical-CSV-mint cadence.

## 9. When this canonical applies

This canonical applies whenever **any** of:

- A wave inside a multi-wave coordinator initiative closes (I86 precedent;
  future analogous coordinators).
- A new row lands in any canonical CSV under
  `compliance/canonicals/dimensions/` or in the top-level
  `compliance/canonicals/` (INITIATIVE_REGISTRY, OPS_REGISTER,
  DECISION_REGISTER, baseline_organisation, process_list,
  REPOSITORY_REGISTRY, CYCLE_REGISTER).
- A new `docs/wip/planning/NN-<slug>/` folder is created.
- A new `*_DISCIPLINE.md` specialty canonical is minted under
  `People/canonicals/`.
- The operator explicitly requests a sweep (on_demand cadence).

It does **not** apply to:

- Chore-only commits (typo fixes, link-rot fixes, formatting).
- Pure runtime infrastructure code (no impact on baseline indexes).
- Per-engagement WIP synthesis under `docs/wip/intelligence/` (governed
  by the brand-baseline-reality discipline, not this one).

## 10. Migration posture (charter → active)

This canonical lands at **`status: charter`** at mint time (D-IH-86-CD,
2026-05-21). Charter status means: the architecture is ratified;
implementation is phased; FAIL promotion is forward-chartered to a
ratifying decision at Wave N close.

Promotion to **`status: active`** requires:

1. Wave N N.4 backfill commit closes all baseline-index drift.
2. One full sweep at Wave N close emits `drift_count == 0 AND
   gap_count == 0`.
3. Validator FAIL promotion ratified by operator-explicit decision
   (D-IH-86-CD rationale or successor row).
4. Two consecutive subsequent wave-closes (Wave O + Wave P) emit clean
   sweeps without operator intervention — proves the discipline is
   self-sustaining, not propped up by the mint commit.
5. Operator-explicit ratification of the promotion.

## 11. Cross-references

- Sister canonicals under People:
  [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) §6
  materialisation table — this canonical is the 11th specialty row
  (added at this mint per `D-IH-86-CD`).
  [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md)
  — sister discipline; INTER_WAVE_REGRESSION sweeps governance
  artifacts at wave-close, INDEX_INTEGRITY sweeps baseline indexes at
  wave-close + canonical-CSV mint. The two compose: a clean
  INTER_WAVE_REGRESSION sweep does NOT prove index freshness; a clean
  INDEX_INTEGRITY sweep does NOT prove wave-deliverable integrity.
  [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) — closure UAT class that
  hosts index-freshness evidence as a mechanical row.
- Per-axis SSOT registries: [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md),
  [`INITIATIVE_REGISTRY.csv`](../Compliance/canonicals/INITIATIVE_REGISTRY.csv),
  [`DECISION_REGISTER.csv`](../Compliance/canonicals/DECISION_REGISTER.csv),
  [`OPS_REGISTER.csv`](../Compliance/canonicals/OPS_REGISTER.csv),
  [`baseline_organisation.csv`](../Compliance/canonicals/baseline_organisation.csv),
  [`process_list.csv`](../Compliance/canonicals/process_list.csv),
  [`INITIATIVE_DEPENDENCIES.md`](../Compliance/canonicals/INITIATIVE_DEPENDENCIES.md),
  [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv).
- Cursor rules: [`akos-index-integrity.mdc`](../../../../../../../.cursor/rules/akos-index-integrity.mdc)
  (this canonical's mechanical companion),
  [`akos-quality-fabric.mdc`](../../../../../../../.cursor/rules/akos-quality-fabric.mdc)
  (parent fabric rule),
  [`akos-inter-wave-regression.mdc`](../../../../../../../.cursor/rules/akos-inter-wave-regression.mdc)
  (sister discipline rule),
  [`akos-docs-config-sync.mdc`](../../../../../../../.cursor/rules/akos-docs-config-sync.mdc)
  (sync-contract rule that documents what to update when canonicals
  change — INDEX_INTEGRITY is the mechanical enforcement of that rule's
  contracts),
  [`akos-inline-ratification.mdc`](../../../../../../../.cursor/rules/akos-inline-ratification.mdc)
  (findings disposition).
- Skill: [`index-integrity-craft`](../../../../../../../.cursor/skills/index-integrity-craft/SKILL.md)
  — the *how* layer paired with this canonical's *what* layer.
- Governance lineage: D-IH-86-CD (canonical mint + INFO ramp; operator-
  ratified 2026-05-21), D-IH-86-CE (8-dimension probe set ratification),
  D-IH-86-CF (paired SOP+runbook gate per akos-executable-process-
  catalog.mdc Rule 1).

## 12. External research grounding

Per [`akos-applied-research-discipline.mdc`](../../../../../../../.cursor/rules/akos-applied-research-discipline.mdc)
RULE 2 (novel framings require external citation): the INDEX_INTEGRITY
discipline is grounded in three external practices that converge on the
same insight:

- **DAMA-DMBOK 2.0 §"Reference & Master Data Management"** (RMDM
  knowledge area) — names data quality as a continuous discipline, not
  a one-off project. Baseline indexes are reference data about the
  governance state; they degrade unless actively maintained.
- **Site Reliability Engineering (Beyer et al., O'Reilly 2016)
  §"Toil reduction"** — the practice of identifying manual maintenance
  work that can be eliminated by deterministic tooling. The
  `baseline_index_sweep.py --fix` paths are the toil-reduction
  application of this principle to documentation indexes.
- **Continuous Documentation movement (GitBook 2024; Write the Docs
  conference 2025 talks)** — the practice of treating documentation as
  code that can be tested, validated, and automatically updated. The
  INFO→FAIL ramp on `validate_index_freshness.py` operationalises this.

These three external groundings + the internal precedent of the
INTER_WAVE_REGRESSION sweep (Wave M, 10th specialty) constitute the
authoring evidence for this canonical's novel framing — that index
integrity is itself a discipline worth a paired runbook + validator +
cursor rule + skill quartet.

@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md
