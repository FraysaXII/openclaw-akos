---
title: SOP — People Collaborator Share
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_COLLABORATOR_SHARE_001
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Founder/CEO
co_authors:
  - PMO
  - People Operations Lead
  - Legal Counsel
last_review: 2026-05-25
last_review_by: Founder/CEO
last_review_decision_id: D-IH-86-DA
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-DA
  - D-IH-86-DB
  - D-IH-86-DC
  - D-IH-86-DD
  - D-IH-86-DE
status: charter
register: internal
linked_canonicals:
  - COLLABORATOR_SHARE_DOCTRINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - ../People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/process_list.csv
  - ../Compliance/canonicals/DECISION_REGISTER.csv
  - ../Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv
linked_runbooks:
  - scripts/collaborator_share_calculate.py
  - scripts/validate_collaborator_share.py
  - scripts/sync_compliance_mirrors_from_csv.py
linked_processes:
  - hol_peopl_dtp_collaborator_share_001
cadence: event_triggered
cadence_trigger: engagement charter OR milestone close OR final close OR commercial deviation
cadence_secondary: scheduled
cadence_secondary_schedule: quarterly cross-engagement audit
---

# SOP — People Collaborator Share

## Purpose

Operationalise the collaborator-share discipline named in
[`COLLABORATOR_SHARE_DOCTRINE.md`](COLLABORATOR_SHARE_DOCTRINE.md). For
every engagement involving a strategic collaborator (deal-source,
operator-of-the-process, or paired GTM partner), the People area runs a
deterministic 6-step workflow to author the SHARE_REGISTRY row + the
VENDOR_SERVICES_BILLED roster + (when applicable) the RATE_OVERRIDES /
PARTNER_OVERLAP_EXCLUSION_CLAUSES rows, then computes settlement at
each milestone + final close.

Paired with runbook
[`scripts/collaborator_share_calculate.py`](../../../../../../scripts/collaborator_share_calculate.py)
+ validator
[`scripts/validate_collaborator_share.py`](../../../../../../scripts/validate_collaborator_share.py)
+ sync emit
[`scripts/sync_compliance_mirrors_from_csv.py --collaborator-share-only`](../../../../../../scripts/sync_compliance_mirrors_from_csv.py)
per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1. Either the Founder/CEO + People Operations Lead — or an AIC
role_owner per [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc)
forward — executes via this SOP, OR the runbook fires on demand at the
trigger moment. Both surfaces are SSOT for the same process.

## Scope

In scope:

- Engagement charter time (new engagement with a strategic collaborator
  opens): author SHARE_REGISTRY + VENDOR_SERVICES_BILLED + seed
  MARKET_RATE_REFERENCE row if missing.
- Engagement milestone close: recompute current benefits estimate via
  runbook; share transparently with collaborator.
- Engagement final close: emit settlement statement; obtain collaborator
  sign-off; archive engagement-folder companion files.
- Per-engagement commercial deviation: inline-ratify + RATE_OVERRIDES
  row + DECISION_REGISTER row.
- Quarterly cross-engagement audit: validator across all engagements;
  operator dispositions findings via inline-ratify.

Out of scope:

- Cap-table-bearing partnerships (equity instead of revenue share) —
  use `eng_model_investor_advisor` engagement model instead per
  [`ENGAGEMENT_MODEL_REGISTRY.csv`](../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv).
- Pure milestone-class consulting with no collaborator party — use
  `eng_model_milestone_consultant` engagement model (Bâtard 2020
  precedent; `D-IH-73-I`) instead.
- Internal Holistika team compensation — covered by employment
  contracts + payroll, not this SOP.

## Inputs (with `share_pattern` routing)

For **every** trigger:

- `engagement_id` — slug matching the engagement folder under
  `docs/references/hlk/v3.0/Think Big/<Clients|Advisers>/<engagement-slug>/`.
- `collaborator_id` — FK to `GOI_POI_REGISTER.csv` (resolve before
  authoring; seed a new POI row first if the collaborator is new).
- `engagement_model_id` — FK to `ENGAGEMENT_MODEL_REGISTRY.csv`
  (typically `eng_model_percentage_collaborator` for `deep_partner_65_35`
  shape; `eng_model_orchestration_broker` for `orchestration_broker_thin_margin`
  shape — forward-charter per D-IH-73-J extension at Commit 3).
- **`share_pattern`** — the routing input per D-IH-86-DE:
  - `deep_partner_65_35` *(default for backward-compatibility)* — pick when
    Holistika contributes a full methodology + machinery + execution stack
    as the value of its 65% share; collaborator brings the deal +
    operates the process; B2B partner narrative applies. **Lived precedent:
    Websitz / Rushly engagement.**
  - `orchestration_broker_thin_margin` — pick when Holistika orchestrates
    a deal as a thin-margin broker (~6%); multiple billed collaborators
    (founder + ≥ 1 partner-class) share the bulk of revenue. **First
    instantiation: SUEZ POC at Commit 3.**
  - `custom` — pick when neither pattern fits; requires mandatory
    `share_override_decision_id` FK to a DECISION_REGISTER row that
    names the commercial shape narratively.

For **charter-time** trigger:

- Founder + collaborator hourly rates (charter-time best estimate; revised
  at milestone closes).
- VENDOR_SERVICES_BILLED roster — typically 10 rows seeded from the
  doctrine §2.2 default-in-kind table; deviations require
  `bill_mode_decision_id`.
- Any partner-overlap-exclusion clause IDs (e.g.,
  `clause_partner_marketing_agency_overlap` if collaborator has MKTOPS
  overlap).

For **milestone-close** trigger:

- Updated billed-hours (founder + collaborator).
- Updated direct-pass-through costs.
- Updated revenue (when partial invoicing).

For **commercial-deviation** trigger:

- The proposed deviation (rate excursion OR share-split deviation).
- The commercial-strategy rationale (1-3 sentences).
- The reversibility classification (reversible / irreversible).

## Steps (AC-HUMAN; AIC consumes same steps)

### Step 1 — Resolve the `share_pattern` BEFORE drafting any CSV row

Inline-ratify gate per `akos-inline-ratification.mdc`: post an
`AskQuestion` with the three `share_pattern` options + recommended
default based on the engagement's commercial shape. Decisions of
which pattern applies are LOAD-BEARING — the wrong choice cascades into
CS-03 + CS-04 producing the wrong invariant audit. Worked example:

- **SUEZ POC** → `orchestration_broker_thin_margin` (thin Holistika
  margin + multiple billed collaborators).
- **Websitz / Rushly extension** → `deep_partner_65_35` (Holistika brings
  full methodology + machinery; partner is a marketing agency themselves
  with MKTOPS overlap → MKTOPS in-kind via
  `clause_partner_marketing_agency_overlap`).
- **Flagship investor-customer discount deal** → `custom` (commercially
  priced below default 65/35; override decision row names the strategic
  rationale).

If unclear, halt and re-read the doctrine §2.3 + §3 worked examples
before authoring.

### Step 2 — Author the canonical CSV rows

Append rows to the 5 CSVs in this order (FKs resolve forward to back):

1. `COLLABORATOR_MARKET_RATE_REFERENCE.csv` — seed row for the
   collaborator's `role_class × region × experience_band` if missing.
2. `PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv` — append any new clause
   patterns the engagement surfaces (typically reuses existing rows).
3. `HOLISTIKA_VENDOR_SERVICES_BILLED.csv` — author 10 rows (one per
   service class per doctrine §2.2 defaults); flag any deviations with
   `bill_mode_decision_id`.
4. `COLLABORATOR_SHARE_REGISTRY.csv` — author the SHARE_REGISTRY row
   with the ratified `share_pattern`. For `orchestration_broker_thin_margin`,
   author MULTIPLE rows (one per collaborator + one for Holistika-corporate)
   per the §3.2 worked example.
5. `COLLABORATOR_RATE_OVERRIDES.csv` — append override rows for any
   `market_rate_excursion` OR `share_split_deviation` OR (mandatory)
   any `custom` pattern row's `share_override_decision_id` lineage.

For each row authored, the agent confirms FK resolution against the
target canonical BEFORE the commit (`Grep` against the FK target file).

### Step 3 — Run the validator self-test + full sweep

```
py scripts/validate_collaborator_share.py --self-test    # MUST exit 0
py scripts/validate_collaborator_share.py                # full sweep
py scripts/collaborator_share_calculate.py --self-test   # MUST exit 0
```

The self-test verifies the 8 CS-NN checks load + return well-formed
`CollaboratorShareAuditRow` Pydantic models. If FAIL, the validator is
broken — halt and fix before continuing.

The full sweep emits per-row findings. Expected outcomes per
`share_pattern`:

- **deep_partner_65_35**: per-row sum-to-100 invariant holds (CS-03
  PASS); rates within ±25% of reference OR override row exists (CS-04
  PASS or WARN).
- **orchestration_broker_thin_margin**: across-rows sum-to-100 invariant
  per `engagement_id` holds (CS-03 PASS); Holistika-total in ~6% band
  (CS-04 advisory PASS).
- **custom**: CS-03 + CS-04 skipped; CS-02 verifies the mandatory
  `share_override_decision_id` FK resolves.

### Step 4 — Compute the settlement (charter / milestone / final modes)

```
py scripts/collaborator_share_calculate.py \
  --engagement <id> \
  --mode <charter|milestone|final> \
  [--share-pattern <pattern>]
```

The runbook reads the 5 CSVs + the engagement folder's billed-hours
roster, branches on `share_pattern`, and emits a Markdown settlement
statement under
`docs/references/hlk/v3.0/Think Big/<Clients|Advisers>/<engagement-slug>/settlement-<mode>-<YYYY-MM-DD>.md`.

For `custom` patterns, the runbook emits a MANUAL placeholder pointing
at the override decision row — operator authors the math by hand
inside the engagement folder.

### Step 5 — Share the settlement with the collaborator (transparency cadence)

Per the doctrine §10 Self-discipline Rule 5, the agent attaches the
settlement Markdown + the relevant doctrine version reference when
emailing or DM-ing the collaborator. The collaborator's confidence in
the math comes from the reproducible audit trail, not from operator
assertion.

For `deep_partner_65_35` shape, transparency cadence is at each
milestone close + at final close. For `orchestration_broker_thin_margin`,
each row-holder receives their own row's slice at the same cadence
(no benefits-pool calculation to share; each collaborator's slice IS
their slice). For `custom`, cadence is per the override decision row's
commercial narrative.

### Step 6 — Update operator-scratchpad + sync mirrors

After every material commit touching the 5 CSVs:

1. Append a one-paragraph entry to
   `docs/wip/intelligence/operator-scratchpad.md` naming: engagement_id,
   `share_pattern`, ratifying decision IDs, any drift or override rows.
2. Run `py scripts/sync_compliance_mirrors_from_csv.py --collaborator-share-only`
   to regenerate the Supabase mirror INSERT statements.
3. Commit the mirror SQL artifacts per
   [`akos-holistika-operations.mdc`](../../../../../../.cursor/rules/akos-holistika-operations.mdc)
   two-plane discipline (DDL via `supabase/migrations/`; DML via
   `compliance_mirror_emit`).

## Outputs

- Updated rows across the 5 collaborator-share CSVs.
- `settlement-<mode>-<YYYY-MM-DD>.md` under engagement folder.
- DECISION_REGISTER.csv rows for each `share_split_deviation` /
  `market_rate_excursion` / `bill_mode_deviation` / custom-pattern
  override.
- Updated operator-scratchpad entry.
- Mirror INSERT SQL artifacts under `artifacts/sql/` per the sync emit.
- Engagement-folder companion files (signed copy of settlement; PDF
  export when external rendering required per
  [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc)).

## Acceptance criteria

### AC-HUMAN

A human (or AIC role_owner) can execute every Step above without
invoking the runbook — by reading the doctrine §2 economic architecture
+ §2.3 share_pattern enum + §3 worked examples + §2.2 default bill_mode
table, manually authoring the 5 CSV rows by inspection, computing the
math by hand on a sheet of paper or in Excel (Excel + Power Query is
the operator's reference computation surface per the SUEZ POC kit),
and emitting the settlement Markdown by hand. The output follows the
same schema the runbook emits. Manual execution is tedious but
deterministic — for a typical 3-row `deep_partner_65_35` engagement,
expect 1-2hr of manual work vs ~5s of runbook execution.

### AC-AUTOMATION

The runbook `scripts/collaborator_share_calculate.py --engagement <id>
--mode <mode>` runs unattended (dispatch script invocation; future cron
at milestone-due-date triggers) and emits the same Markdown settlement
output. The validator `scripts/validate_collaborator_share.py` runs at
every `py scripts/verify.py pre_commit` invocation via
`validate_collaborator_share_self_test` step in
`config/verification-profiles.json`. The sync emit
`scripts/sync_compliance_mirrors_from_csv.py --collaborator-share-only`
runs on demand when the operator commits new rows to any of the 5 CSVs.

## Failure modes + remediation

- **Self-test FAIL** → validator or runbook is broken; halt; fix before
  any commit touching the 5 CSVs; never bypass the self-test.
- **CS-03 FAIL on `deep_partner_65_35` row without override** → either
  the row's split was authored incorrectly (fix to 65/35) OR the
  operator intends a commercial deviation (author the override row +
  DECISION_REGISTER row in the same commit; do not commit the SHARE_REGISTRY
  row standalone).
- **CS-03 across-rows-sum ≠ 100 on `orchestration_broker_thin_margin`** →
  one or more SHARE_REGISTRY rows for the engagement are missing OR
  duplicated; recompute the sum-across-rows manually, reconcile, then
  re-run the validator.
- **CS-08 FAIL on unknown `share_pattern` value** → typo in the CSV cell
  (must be exactly `deep_partner_65_35` / `orchestration_broker_thin_margin` /
  `custom`); fix the cell value, then re-run.
- **CS-04 WARN on rate >25% above reference** → either seed the
  MARKET_RATE_REFERENCE row at a different rate (if the reference is
  stale) OR author the `market_rate_excursion` override row +
  DECISION_REGISTER row.
- **Operator silence > 24h on a reversible disposition** → time-box
  recovery per `akos-inline-ratification.mdc` §"Time-box recovery";
  reversible (`bill_mode_deviation`, expired rate override) auto-defaults
  to recommended option; irreversible (commercial share-split deviation
  signed by collaborator) NEVER auto-defaults — halt and escalate.
- **Collaborator dispute on settlement math** → cite the doctrine
  version + the relevant CSV rows + the settlement Markdown; if the
  collaborator disputes the doctrine itself, escalate to operator
  inline-ratify gate to amend the doctrine + back-resolve the
  engagement with the amended math + a DECISION_REGISTER row naming
  the amendment lineage.
- **Settlement Markdown missing at engagement final-close commit** →
  release-gate INFO advisory while doctrine sits at charter; future
  promotion to FAIL gated on doctrine `status: active` promotion +
  explicit operator FAIL-ramp decision.

## Cross-references

- Doctrine: [`COLLABORATOR_SHARE_DOCTRINE.md`](COLLABORATOR_SHARE_DOCTRINE.md).
- Cursor rule: [`akos-collaborator-share.mdc`](../../../../../../.cursor/rules/akos-collaborator-share.mdc).
- Skill: [`collaborator-share-craft`](../../../../../../.cursor/skills/collaborator-share-craft/SKILL.md).
- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).
- Sister discipline SOPs: [`SOP-PEOPLE_INDEX_INTEGRITY_001.md`](SOP-PEOPLE_INDEX_INTEGRITY_001.md),
  [`SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md`](SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md).
- Runbook: [`scripts/collaborator_share_calculate.py`](../../../../../../scripts/collaborator_share_calculate.py).
- Validator: [`scripts/validate_collaborator_share.py`](../../../../../../scripts/validate_collaborator_share.py).
- Sync emit: [`scripts/sync_compliance_mirrors_from_csv.py --collaborator-share-only`](../../../../../../scripts/sync_compliance_mirrors_from_csv.py).
- Pydantic chassis: [`akos/hlk_collaborator_share.py`](../../../../../../akos/hlk_collaborator_share.py).
- 5 canonical CSVs:
  - [`../People Operations/canonicals/dimensions/COLLABORATOR_SHARE_REGISTRY.csv`](../People%20Operations/canonicals/dimensions/COLLABORATOR_SHARE_REGISTRY.csv)
  - [`../People Operations/canonicals/dimensions/HOLISTIKA_VENDOR_SERVICES_BILLED.csv`](../People%20Operations/canonicals/dimensions/HOLISTIKA_VENDOR_SERVICES_BILLED.csv)
  - [`../People Operations/canonicals/dimensions/PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv`](../People%20Operations/canonicals/dimensions/PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv)
  - [`../People Operations/canonicals/dimensions/COLLABORATOR_MARKET_RATE_REFERENCE.csv`](../People%20Operations/canonicals/dimensions/COLLABORATOR_MARKET_RATE_REFERENCE.csv)
  - [`../People Operations/canonicals/dimensions/COLLABORATOR_RATE_OVERRIDES.csv`](../People%20Operations/canonicals/dimensions/COLLABORATOR_RATE_OVERRIDES.csv)
- Process catalog: `hol_peopl_dtp_collaborator_share_001` in
  [`process_list.csv`](../Compliance/canonicals/process_list.csv) (lands
  in Commit 2c-b).
- Decision lineage: D-IH-86-DA (doctrine mint + paired SOP gate),
  D-IH-86-DB (TRUE-MARGIN benefits formula), D-IH-86-DC (clause
  table schema), D-IH-86-DD (Tier 1 WIP hygiene pre-requisite),
  D-IH-86-DE (`share_pattern` enum + CS-08 + CS-03/CS-04 per-pattern
  branching).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md
@.cursor/rules/akos-collaborator-share.mdc
