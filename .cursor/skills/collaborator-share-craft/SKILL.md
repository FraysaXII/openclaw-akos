---
name: Collaborator Share Craft
description: >-
  Use when authoring, running, dispositioning findings from, or wiring
  up the collaborator-share discipline in this AKOS workspace.
  Codifies the craft for picking the right share_pattern
  (deep_partner_65_35 / orchestration_broker_thin_margin / custom),
  authoring all 5 CSV rows in a single commit, computing settlements
  per pattern, and dispositioning commercial deviations without
  producing benefits-pool drift or partner-narrative collapse.
  Triggers on phrases like collaborator share, SHARE_REGISTRY, share
  pattern, 65/35 split, TRUE-MARGIN, partner overlap, market-rate
  excursion, CS-NN finding, settlement statement, Aïsha share,
  Websitz share, orchestration broker, thin margin, custom commercial,
  validate_collaborator_share.py, collaborator_share_calculate.py.
  Pairs with .cursor/rules/akos-collaborator-share.mdc (the WHEN); this
  skill is the HOW.
---

# Collaborator Share Craft

## Why this skill exists

The cursor rule `akos-collaborator-share.mdc` and the canonical
`COLLABORATOR_SHARE_DOCTRINE.md` tell you **when** to apply the
discipline and **what** the 3 patterns + 8 checks are. This skill tells
you **how** to apply them well — how to pick the right `share_pattern`
under operator pressure, how to author the 5 CSV rows in the right
order, how to compute settlements per pattern without arithmetic
errors, and how to disposition commercial deviations without breaking
the partner narrative.

Read this skill before authoring a new `COLLABORATOR_SHARE_REGISTRY`
row OR running a settlement OR ratifying a commercial deviation OR
wiring up a sibling specialty mint that should inherit the
COLLABORATOR_SHARE mint pattern (Wave R+1 P2c-a worked example).

## Principle 1 — Pick `share_pattern` BEFORE drafting any row

The single most load-bearing decision in this discipline is the
`share_pattern` choice. CS-03 and CS-04 branch on it; pick wrong and
the validator passes the wrong invariant audit silently, producing
incorrect settlement math the operator may not catch until the
collaborator disputes the final-close statement.

Decision tree:

```
Q1: Does Holistika contribute a full methodology + machinery + execution
    stack as the value of its share, with the collaborator bringing the
    deal + operating the process under a B2B partner narrative?

  YES → share_pattern = deep_partner_65_35
        (Websitz / Rushly shape; 65/35 per-row split with services in-kind)

  NO → Q2: Does Holistika orchestrate as a thin-margin broker (~6% of
           revenue), with multiple billed collaborators (founder + ≥ 1
           partner-class) sharing the bulk of revenue?

    YES → share_pattern = orchestration_broker_thin_margin
          (SUEZ POC shape; ≥ 2 rows per engagement; across-rows sum-to-100)

    NO → share_pattern = custom
         (mandatory override decision FK naming the commercial shape)
```

Worked decision examples:

- **SUEZ POC** (2026-05-25 framing: *"holistika has 6%"*) →
  `orchestration_broker_thin_margin`.
- **Websitz / Rushly extension** (mkt agency themselves; MKTOPS overlap) →
  `deep_partner_65_35` + `clause_partner_marketing_agency_overlap` in-kind row.
- **Flagship investor-relevant discount deal** (operator wants lighthouse
  case study; commercially priced at 50/50) → `custom` with override
  decision row.
- **Aïsha-on-SUEZ-continuity slice** → NOT a standalone share_pattern;
  Aïsha appears as one row inside the SUEZ engagement's
  orchestration_broker rows.

When unclear, halt and re-read the doctrine §2.3 + §3 worked examples
BEFORE posting any `AskQuestion` to the operator. Re-reading takes 5
minutes; reverting a mis-authored 5-CSV commit takes 30+.

## Principle 2 — Author the 5 CSV rows in dependency order, in ONE commit

CS-02 verifies cross-CSV FK integrity. Authoring rows in the wrong
order means the validator FAILs on the intermediate state and the
operator has to commit-amend. Author in this order in a SINGLE atomic
commit:

1. **`COLLABORATOR_MARKET_RATE_REFERENCE.csv`** — seed the collaborator's
   `role_class × region × experience_band` row if missing. Cite the
   rate source (URL when public; industry survey name when private).
2. **`PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv`** — append any new clause
   patterns the engagement surfaces. Reuses existing rows most of the
   time (e.g., `clause_partner_marketing_agency_overlap` for marketing
   agencies).
3. **`HOLISTIKA_VENDOR_SERVICES_BILLED.csv`** — 10 rows (one per service
   class per doctrine §2.2 defaults). Mark deviations with
   `bill_mode_decision_id`. Even all-default engagements get all 10
   rows authored — the audit trail is the value.
4. **`COLLABORATOR_SHARE_REGISTRY.csv`** — author the SHARE_REGISTRY
   row(s) with the ratified `share_pattern`. For
   `orchestration_broker_thin_margin`, author MULTIPLE rows (one per
   collaborator + one for Holistika-corporate) per the doctrine §3.2
   worked example.
5. **`COLLABORATOR_RATE_OVERRIDES.csv`** — append override rows for any
   `market_rate_excursion` OR `share_split_deviation` OR (mandatory)
   any `custom`-pattern row's `share_override_decision_id` lineage.
6. **`DECISION_REGISTER.csv`** — append a row per ratified deviation OR
   per `custom`-pattern lineage.

Bad (split across commits):

```
Commit A: SHARE_REGISTRY row
  → CS-02 FAILs because VENDOR_SERVICES_BILLED roster missing
Commit B: VENDOR_SERVICES_BILLED roster
  → late catch; main is broken between A and B
```

Good (single atomic commit):

```
git add path/to/all/5/csvs path/to/decision-register
git commit -m "Engagement-NN collaborator-share kit (share_pattern=...; all 5 CSVs + decision)"
  → CS-01..CS-08 all PASS at commit time
  → main is never in a broken state
```

## Principle 3 — Compute settlement math per pattern, NOT by intuition

Each `share_pattern` has its own math. Computing one pattern's math
under another pattern's assumptions is the second most common failure
mode after Principle 1.

### `deep_partner_65_35` math

```
BENEFITS = REVENUE - (founder_billed_time
                    + collaborator_billed_time
                    + direct_pass_through_project_costs
                    + holistika_vendor_services_billed_against_project_per_log)

Holistika-side = BENEFITS × 0.65 + founder_billed_time
Collaborator-side = BENEFITS × 0.35 + collaborator_billed_time
```

The collaborator's TOTAL is their 35% share PLUS their billed time
(billed-time is NOT subtracted from their share — it's a transparent
line item ABOVE the share computation).

### `orchestration_broker_thin_margin` math

```
For each row r:
  row_revenue_slice = REVENUE × (r.holistika_share_pct + r.collaborator_share_pct) / 100

Across-rows-per-engagement:
  Σ (r.holistika_share_pct + r.collaborator_share_pct) for all r in engagement = 100
```

Costs are tracked separately (for tax/accounting) but NOT subtracted
inside the share math. Each row's slice IS that row-holder's revenue;
they pay their own taxes + costs against it.

### `custom` math

NO automated math. The runbook emits a MANUAL placeholder pointing at
the override decision row. The operator authors the math by hand in
the engagement folder, citing the decision row's
`commercial_strategy_rationale`.

### Worked numerical check (Principle 3 cross-validation)

For an `orchestration_broker_thin_margin` engagement at €100k revenue with
the §3.2 worked example layout:

| Row | holistika_pct | collab_pct | Row revenue |
|:---|---:|---:|---:|
| Holistika corp | 6 | 0 | €6,000 |
| Aïsha | 0 | 30 | €30,000 |
| Founder | 0 | 24 | €24,000 |
| Exec collab 1 | 0 | 20 | €20,000 |
| Exec collab 2 | 0 | 20 | €20,000 |
| **Sum check** | **6** | **94** | **€100,000** |

Sanity check: 6 + 94 = 100. Σ row_revenue_slice = €100,000. Both
invariants hold; CS-03 PASS.

If you author this as `deep_partner_65_35` instead, CS-03 FAILs on
every row (per-row sum 6+0=6 ≠ 100; 0+30=30 ≠ 100; etc.). Pattern
mismatch surfaces immediately at the validator.

## Principle 4 — Disposition commercial deviations via inline-ratify, not silently

When the operator proposes a deviation (rate excursion, share-split
deviation, bill_mode deviation), surface as `AskQuestion` BEFORE
authoring the override row. The 5-option enum from the cursor rule
RULE 4 applies.

Bad (silent authoring):

```
# Operator: "let's give Aïsha 40% on this one"
# Agent: silently authors SHARE_REGISTRY row with 60/40 split
# Validator FAILs CS-03 on the 60/40 split (no override row)
# Operator surprised; commit rejected; rework needed
```

Good (inline-ratify):

```
AskQuestion: Aïsha share-split deviation from 65/35 → 60/40 on engagement-NN.
  Options:
    1. ratify-as-proposed (recommended — operator-named strategic rationale: ...)
       → author override row + DECISION_REGISTER row + commit
    2. ratify-with-amendment (e.g., 62/38 as intermediate)
    3. defer-to-next-milestone (charter-time stays 65/35; revisit at MS-1)
    4. reject-keep-default (65/35 stays)
    5. escalate-to-blocker-tracker (more time than the inline-ratify window)
```

Time-box recovery: reversible deviations (`bill_mode_deviation`,
expired rate override) auto-default to recommended option after 24h+
silence + clean validators. Irreversible deviations (commercial
share-split signed by collaborator; `custom`-pattern narrative
committed to engagement folder) NEVER auto-default — halt and escalate
per `akos-governance-remediation.mdc`.

## Principle 5 — Share settlement with collaborator + cite doctrine version

When emailing or DM-ing the collaborator the settlement statement,
attach:

1. The Markdown settlement file (or the PDF if rendering applies per
   `akos-external-render-discipline.mdc`).
2. The doctrine version reference (e.g., *"computed per
   COLLABORATOR_SHARE_DOCTRINE.md at version v3.1 + D-IH-86-DE
   `share_pattern` extension"*).
3. A 2-3 sentence summary of the math (revenue, costs subtracted or
   not per pattern, per-row split).

For `deep_partner_65_35`: the collaborator receives one line item for
their billed time + one for their 35% share. Total = sum.

For `orchestration_broker_thin_margin`: each row-holder receives their
own row's slice; the collaborator sees ONLY their slice (not the full
engagement-level revenue allocation) — no benefits-pool calculation
needed.

For `custom`: cite the override decision row's
`commercial_strategy_rationale` verbatim in the settlement Markdown
header so the collaborator understands the bespoke math.

The collaborator's confidence in the math comes from the reproducible
audit trail (5 CSVs + DECISION_REGISTER + settlement Markdown +
doctrine version), not from operator assertion.

## Principle 6 — Wire mirror sync after every commit touching the 5 CSVs

The Supabase mirror DDL at
`supabase/migrations/20260525000000_i86_waveRplus1_commit2b_collaborator_share_mirrors.sql`
carries CHECK constraints matching the Pydantic enums. When the
canonical CSVs change, the mirror needs INSERT statements regenerated:

```
py scripts/sync_compliance_mirrors_from_csv.py --collaborator-share-only
```

This emits SQL UPSERTs to `artifacts/sql/` per the
[`akos-holistika-operations.mdc`](../../rules/akos-holistika-operations.mdc)
two-plane discipline (DDL via `supabase/migrations/`; DML via
`compliance_mirror_emit` profile). Operator reviews + applies in
batches; never commits large `INSERT` mirror batches as migration
files.

## Pre-flight checklist (walk mentally before any SHARE_REGISTRY commit)

1. ✓ `share_pattern` resolved via inline-ratify (NOT defaulted silently).
2. ✓ Doctrine §2.3 + §3 worked examples re-read if unclear.
3. ✓ All 5 CSVs touched in the same commit (or N/A noted in commit
   message for CSVs that don't change).
4. ✓ Cross-CSV FKs resolve (grepped the FK target file before commit).
5. ✓ DECISION_REGISTER row authored for every override / custom-pattern
   lineage.
6. ✓ `py scripts/validate_collaborator_share.py` PASS (or known WARN
   findings explained in commit message).
7. ✓ Settlement Markdown emitted if at milestone/final-close trigger.
8. ✓ operator-scratchpad entry appended naming engagement_id,
   share_pattern, decision IDs.
9. ✓ Mirror sync run (`--collaborator-share-only`) if CSV rows changed.
10. ✓ External-render trail set up if settlement Markdown going to
    collaborator OR investor audience (per
    `akos-external-render-discipline.mdc`).

## Anti-patterns (recovery patterns)

- **Anti-pattern: silently default to `deep_partner_65_35`** — most
  common failure for orchestration-broker engagements. Recovery: rebuild
  the SHARE_REGISTRY rows with the correct pattern; rerun CS-03 + CS-04;
  amend the engagement-folder settlement if already issued.
- **Anti-pattern: bill founder time AND claim 65% Holistika share**
  (double-dip on `deep_partner_65_35`) — Recovery: the doctrine §2 TRUE-
  MARGIN formula already handles this correctly (`founder_billed_time`
  is subtracted from REVENUE before the 65/35 split, then added back
  to Holistika-side total). The error appears when the operator
  manually computes without using the runbook. Always run the runbook
  for settlement math.
- **Anti-pattern: forget the VENDOR_SERVICES_BILLED roster** — the
  10-row roster is mandatory even when all 10 are in-kind defaults. The
  audit trail (which Holistika services were considered AND in-kind
  vs billed) IS the artifact. Recovery: author all 10 rows in a
  follow-up commit; never bypass the roster.
- **Anti-pattern: settle a `custom`-pattern engagement without citing the
  override decision row** — the override decision narrative IS the
  commercial-shape SSOT for custom patterns. Recovery: amend the
  settlement Markdown to cite the decision row's
  `commercial_strategy_rationale` verbatim.

## Cross-references

- Doctrine: [`COLLABORATOR_SHARE_DOCTRINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md).
- Cursor rule: [`akos-collaborator-share.mdc`](../../rules/akos-collaborator-share.mdc) — the *when* layer.
- Paired SOP: [`SOP-PEOPLE_COLLABORATOR_SHARE_001.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_COLLABORATOR_SHARE_001.md).
- Runbook: [`scripts/collaborator_share_calculate.py`](../../../scripts/collaborator_share_calculate.py).
- Validator: [`scripts/validate_collaborator_share.py`](../../../scripts/validate_collaborator_share.py).
- Sync emit: [`scripts/sync_compliance_mirrors_from_csv.py --collaborator-share-only`](../../../scripts/sync_compliance_mirrors_from_csv.py).
- Pydantic chassis: [`akos/hlk_collaborator_share.py`](../../../akos/hlk_collaborator_share.py).
- Supabase mirror DDL: [`supabase/migrations/20260525000000_i86_waveRplus1_commit2b_collaborator_share_mirrors.sql`](../../../supabase/migrations/20260525000000_i86_waveRplus1_commit2b_collaborator_share_mirrors.sql).
- Sister skill: [`inline-ratify-craft`](../inline-ratify-craft/SKILL.md) — disposition `AskQuestion` craft for Principle 1 + Principle 4 gates.
- Sister skill: [`index-integrity-craft`](../index-integrity-craft/SKILL.md) — Wave N specialty mint precedent for pre-flight checklist shape.
- Sister discipline doctrines: [`INDEX_INTEGRITY_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md), [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md), [`UAT_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md).
