---
name: Collaborator Share Craft
description: >-
  Use when authoring, running, dispositioning findings from, or wiring
  up the collaborator-share discipline in this AKOS workspace.
  Codifies the craft for picking the right (share_pattern,
  share_overlay, methodology_readiness) triple per the 4-base +
  1-overlay architecture (deep_partner_65_35 / bd_intro_only /
  joint_venture_aventure / consulting_direct base + bd_commission_overlay
  stackable; per D-IH-86-EJ Wave R+2 rewrite), authoring all 5 CSV
  rows (SHARE_REGISTRY 20 cols + overlay rows) in a single commit,
  computing settlements per pattern + overlay without arithmetic
  errors, and dispositioning commercial deviations
  (market_rate_excursion / share_split_deviation / bill_mode_deviation
  / overlay_pct_deviation) without producing benefits-pool drift,
  partner-narrative collapse, or the 35% compromise failure mode.
  Triggers on phrases like collaborator share, SHARE_REGISTRY, share
  pattern, share overlay, methodology readiness, 65/35 split, TRUE-
  MARGIN, partner overlap, market-rate excursion, overlay-pct
  deviation, CS-NN finding (CS-01..CS-09), settlement statement,
  Aïsha share, Websitz share, BD commission, consulting direct,
  joint venture, validate_collaborator_share.py,
  collaborator_share_calculate.py. Pairs with
  .cursor/rules/akos-collaborator-share.mdc (the WHEN); this skill is
  the HOW.
---

# Collaborator Share Craft

## Why this skill exists

The cursor rule `akos-collaborator-share.mdc` and the canonical
`COLLABORATOR_SHARE_DOCTRINE.md` tell you **when** to apply the
discipline and **what** the 4 base patterns + 1 overlay + 9 checks
are (per D-IH-86-EJ Wave R+2 doctrine rewrite, 2026-05-26). This
skill tells you **how** to apply them well — how to resolve the
load-bearing `(share_pattern, share_overlay, methodology_readiness)`
triple under operator pressure, how to author the 5 CSV rows (including
the new 20-column SHARE_REGISTRY shape + overlay rows) in the right
order, how to compute settlements per base pattern + overlay slice
without arithmetic errors, and how to disposition commercial
deviations without breaking the partner narrative OR collapsing into
the "35% compromise" failure mode the operator named verbatim at the
2026-05-22 framing.

Read this skill before authoring a new `COLLABORATOR_SHARE_REGISTRY`
row OR running a settlement OR ratifying a commercial deviation OR
wiring up a sibling specialty mint that should inherit the
COLLABORATOR_SHARE mint pattern (Wave R+1 P2c-a + Wave R+2 doctrine
rewrite worked examples).

## Principle 1 — Resolve the `(share_pattern, share_overlay, methodology_readiness)` triple BEFORE drafting any row

The single most load-bearing decision in this discipline is the triple
choice. CS-03, CS-04, and CS-09 all branch on it; pick wrong and the
validator passes the wrong invariant audit silently, producing
incorrect settlement math the operator may not catch until the
collaborator disputes the final-close statement — OR forces the "35%
compromise" failure mode where the partner share is fixed at 35% before
the collaborator can possibly deliver commensurate methodology value.

Decision tree:

```
Q1 (operational shape): Is there a collaborator party operationally
    delivering on the engagement (not just intro/BD)?

  NO  → base = consulting_direct
        Skip to Q3 (overlay axis).

  YES → Q2 (methodology fit): What is the operational collaborator's
        methodology_readiness vs Holistika's stack?

    methodology_trained:
      Q2a: Symmetric peer JV (both bring substantial methodology stacks;
           cross-recognized)?
        YES → base = joint_venture_aventure   (default 50/50; no overlay)
        NO  → base = deep_partner_65_35       (default 65/35; overlay OK)

    methodology_in_progress:
      Q2b: Mentoring clause + share_override_decision_id authored?
        YES → base = deep_partner_65_35       (with mentoring clause)
        NO  → base = consulting_direct        (skip to Q3)

    methodology_naive OR methodology_not_applicable:
      base = bd_intro_only                    (default 85/15; no overlay)
      OR
      base = consulting_direct                (skip to Q3)
      NEVER deep_partner_65_35 here (CS-09 FAIL — "35% compromise" prevention)
      NEVER joint_venture_aventure here (CS-09 FAIL — peer-equivalence required)

Q3 (overlay axis; only fires when base is consulting_direct OR deep_partner_65_35):
    Is there a separate intro/BD party who brought the deal but is NOT
    operating on it?

  NO  → no overlay row.

  YES → mint overlay row(s):
        share_overlay = bd_commission_overlay
        overlay party's methodology_readiness ∈ {methodology_naive,
          methodology_not_applicable}   (CS-09 enforces; trained/in-progress
                                          BD parties should be deep_partner
                                          base rows, not overlay slices)
        bd_commission_pct: default 15; deviation needs
          overlay_pct_deviation override row + ratifying decision.
```

Worked decision examples:

- **SUEZ POC corrected at Wave R+2 Commit 5** (per D-IH-86-EL re-read of
  13/05 transcript: Aïsha intro'd the deal but operates downstream
  separately from SUEZ; Holistika delivers SUEZ directly) →
  `consulting_direct + bd_commission_overlay`. Base row: Holistika 85%,
  `methodology_trained`. Overlay row: Aïsha-Holistika-link 15%,
  `methodology_not_applicable`. This SUPERSEDES the prior
  `orchestration_broker_thin_margin` classification (D-IH-86-EG) which
  was wrong.
- **Websitz / Rushly extension** (mkt agency themselves; MKTOPS overlap;
  Bricelle is methodology-trained and operates inside the engagement) →
  `deep_partner_65_35` + `clause_partner_marketing_agency_overlap`
  in-kind row. No overlay.
- **A pure intro-no-operations partnership** (someone hands Holistika a
  Fortune-500 contract on a silver platter and walks away) →
  `bd_intro_only`. 85/15 per-row default. No overlay (the base IS the
  BD shape).
- **A future peer-JV with a sister consultancy** (e.g., a CDP-specialist
  consultancy that brings their stack and Holistika brings the
  CORPINT/strategic-research stack on a co-delivered engagement) →
  `joint_venture_aventure`. 50/50 per-row default. No overlay.
- **A flagship discount lighthouse deal** where the commercial shape is
  truly bespoke → still pick the closest base + use a
  `share_override_decision_id` row to ratify the deviation; do NOT fall
  back to a generic `custom` value (the prior 3-shape doctrine had
  `custom` as escape valve; the 4-base + 1-overlay rewrite covers the
  space without it).

When unclear, halt and re-read the doctrine §2.3 + §2.4 + §3 worked
examples BEFORE posting any `AskQuestion` to the operator. Re-reading
takes 5 minutes; reverting a mis-authored 5-CSV commit takes 30+ and
risks the "35% compromise" failure mode landing on disk.

### The "35% compromise" failure mode (verbatim operator framing 2026-05-22)

*"i don't lie ... we lose value if we don't have things ready because in
reality A was correct"* — operator, 2026-05-22.

The structural failure this decision tree prevents: a
`methodology_naive` collaborator placed on `deep_partner_65_35`
produces a partnership where Holistika carries 100% of the methodology
burden (training the partner up to be operational; covering knowledge
gaps in live engagement; absorbing rework when the partner misapplies
the stack) but the partner's share has already been locked at 35% as
if they brought commensurate value. The collaborator over time becomes
visibly under-delivering relative to share, the partnership goes sour,
and Holistika ends up either eating the compromise (35% paid out for
~10% delivered) OR renegotiating mid-flight (relationship damage). CS-09
makes this mis-pairing impossible to commit silently — the validator
forces resolution at authoring time.

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
   agencies, `clause_mentoring_methodology_in_progress` when the
   methodology_readiness gating per CS-09 calls for an in-flight
   training clause).
3. **`HOLISTIKA_VENDOR_SERVICES_BILLED.csv`** — 10 rows (one per service
   class per doctrine §2.2 defaults). Mark deviations with
   `bill_mode_decision_id`. Even all-default engagements get all 10
   rows authored — the audit trail is the value.
4. **`COLLABORATOR_SHARE_REGISTRY.csv`** — author the SHARE_REGISTRY
   row(s) with the ratified `(share_pattern, share_overlay,
   methodology_readiness)` triple. The schema is **20 columns** (per
   Wave R+2 D-IH-86-EJ rewrite; up from 17). Per-pattern row counts:

   | `(share_pattern, share_overlay)` | Row count per engagement |
   |:---|:---|
   | `consulting_direct`, NULL | 1 base row |
   | `consulting_direct`, `bd_commission_overlay` | 1 base + 1 overlay = 2 rows |
   | `deep_partner_65_35`, NULL | 1 base row |
   | `deep_partner_65_35`, `bd_commission_overlay` | 1 base + 1 overlay = 2 rows |
   | `bd_intro_only`, NULL | 1 base row (overlay slot N/A) |
   | `joint_venture_aventure`, NULL | 1 base row per peer party (typically 2) |

   For overlay rows: `methodology_readiness` MUST be
   `methodology_naive` OR `methodology_not_applicable` (CS-09 FAILs
   trained/in-progress overlay parties — those should be deep_partner
   base rows). For `methodology_in_progress` base rows: requires
   ratifying `share_override_decision_id` row with mentoring-clause
   linkage (CS-09 WARN→FAIL gate).
5. **`COLLABORATOR_RATE_OVERRIDES.csv`** — append override rows for any
   `market_rate_excursion`, `share_split_deviation`,
   `bill_mode_deviation`, OR `overlay_pct_deviation` (NEW per D-IH-86-EJ;
   used when overlay default 15% needs deviation). All overrides FK to a
   DECISION_REGISTER row by `share_override_decision_id`.
6. **`DECISION_REGISTER.csv`** — append a row per ratified deviation OR
   per CS-09 methodology-pattern coherence override (e.g.,
   `methodology_in_progress` + `deep_partner_65_35` requires explicit
   decision row naming the mentoring clause + expected closure date for
   the in-progress training).

Bad (split across commits):

```
Commit A: SHARE_REGISTRY base row (consulting_direct)
  → CS-02 FAILs because VENDOR_SERVICES_BILLED roster missing AND
    overlay row's expected FK pair has no overlay row yet
Commit B: VENDOR_SERVICES_BILLED roster + overlay row + override row
  → late catch; main is broken between A and B
```

Good (single atomic commit):

```
git add path/to/all/5/csvs path/to/decision-register
git commit -m "Engagement-NN collaborator-share kit (share_pattern=consulting_direct + bd_commission_overlay; all 5 CSVs + 2 decision rows)"
  → CS-01..CS-09 all PASS at commit time
  → main is never in a broken state
```

## Principle 3 — Compute settlement math per base pattern + overlay, NOT by intuition

Each `share_pattern` has its own math; the `bd_commission_overlay`
stacks ON TOP of the base computation as a separate slice. Computing
one pattern's math under another pattern's assumptions is the second
most common failure mode after Principle 1.

The Wave R+2 doctrine rewrite (D-IH-86-EJ) unifies the math under a
single TRUE-MARGIN formula that applies across all 4 base patterns;
overlay slices are deducted at the engagement-revenue level BEFORE
TRUE-MARGIN computation (per D-IH-86-EJ §4.2 commercial-distribution
clarification).

### Unified TRUE-MARGIN formula (all 4 base patterns)

```
ENGAGEMENT_REVENUE = total commercial price agreed with customer

# Overlay slice (when present) is the FIRST deduction from revenue:
OVERLAY_SLICE = ENGAGEMENT_REVENUE × (overlay_row.share_pct / 100)
             (typically 15% when bd_commission_overlay default;
              overlay_pct_deviation row + decision required if ≠ 15%)

POST_OVERLAY_REVENUE = ENGAGEMENT_REVENUE - OVERLAY_SLICE

TRUE_MARGIN = POST_OVERLAY_REVENUE
            - founder_billed_time
            - collaborator_billed_time
            - direct_pass_through_project_costs
            - holistika_vendor_services_billed_against_project_per_log

# Then per-base split applies to TRUE_MARGIN:
Holistika-side  = TRUE_MARGIN × (base_row.holistika_share_pct / 100)
                + founder_billed_time
Collaborator-side = TRUE_MARGIN × (base_row.collaborator_share_pct / 100)
                  + collaborator_billed_time

Overlay party total = OVERLAY_SLICE
                    (no billed time; no methodology contribution; pure BD slice)
```

### Per-base default splits (CS-04 anchors)

| Base pattern | holistika_share_pct | collaborator_share_pct | Anchor narrative |
|:---|---:|---:|:---|
| `consulting_direct` | 100 | 0 | Holistika delivers solo; no operational collaborator |
| `bd_intro_only` | 85 | 15 | Pure intro slice; no operational contribution by partner |
| `deep_partner_65_35` | 65 | 35 | Full methodology-enabled co-delivery |
| `joint_venture_aventure` | 50 | 50 | Symmetric peer JV; both bring methodology stacks |

Per-row split MUST sum to 100. CS-03 enforces across-rows sum-to-100
unified for all 4 base patterns; the Wave R+1 per-row-vs-across-rows
branching is collapsed in the rewrite (one base row per engagement
covering Holistika + the operational collaborator; overlay slice is a
SEPARATE row not counted in the base sum-to-100 invariant per
D-IH-86-EJ §6.3).

### Overlay slice details (when present)

The overlay row is computed FIRST off the top of revenue. It does NOT
participate in TRUE_MARGIN math. The overlay party (e.g., the BD intro
person) does not contribute billed time, methodology, or operational
work — pure commission slice.

```
OVERLAY_SLICE pays: overlay party's tax + any overhead on their side
                    (NOT deducted from anyone else's share)
```

### Worked numerical check (Principle 3 cross-validation)

**SUEZ POC re-classified per D-IH-86-EL** at €100k engagement revenue
with consulting_direct + bd_commission_overlay (Aïsha intro slice 15%;
SUEZ delivery direct by Holistika; founder billed 50h @ €200/h = €10k;
no other collaborator billed time; €5k direct pass-through):

```
ENGAGEMENT_REVENUE = €100,000
OVERLAY_SLICE     = €100,000 × 0.15 = €15,000    (→ Aïsha-Holistika-link)
POST_OVERLAY_REV  = €85,000
TRUE_MARGIN       = €85,000 - €10,000 (founder) - €5,000 (pass-through)
                  = €70,000
Holistika-side    = €70,000 × 1.00 (consulting_direct = 100% to Holistika)
                  + €10,000 (founder billed time)
                  = €80,000
Collaborator-side = €0 (consulting_direct has no operational collaborator)
Aïsha-side        = €15,000 (overlay slice)

Sum check: €80,000 + €0 + €15,000 + €5,000 (pass-through) = €100,000 ✓
```

If you author this as `deep_partner_65_35` instead, CS-09 FAILs
immediately because Aïsha's `methodology_readiness` is
`methodology_not_applicable` for the SUEZ delivery (she's not the
operational collaborator on SUEZ — she runs continuity downstream
independently). Pattern mismatch surfaces at the validator before any
math runs.

**Websitz/Rushly deep_partner** at €100k revenue with
`deep_partner_65_35` + no overlay (Bricelle is methodology_trained;
operates inside the engagement; founder billed 40h @ €200/h = €8k;
Bricelle billed 60h @ €150/h = €9k):

```
ENGAGEMENT_REVENUE = €100,000
OVERLAY_SLICE     = €0   (no overlay)
POST_OVERLAY_REV  = €100,000
TRUE_MARGIN       = €100,000 - €8,000 (founder) - €9,000 (Bricelle billed)
                  = €83,000
Holistika-side    = €83,000 × 0.65 + €8,000 = €53,950 + €8,000 = €61,950
Bricelle-side     = €83,000 × 0.35 + €9,000 = €29,050 + €9,000 = €38,050

Sum check: €61,950 + €38,050 = €100,000 ✓
```

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
   COLLABORATOR_SHARE_DOCTRINE.md v3.2 + D-IH-86-EJ Wave R+2 4-base +
   1-overlay rewrite + D-IH-86-EN methodology-pattern coherence"*).
3. A 2-3 sentence summary of the math (revenue, overlay slice deducted
   first if present, TRUE_MARGIN composition, base-pattern split).

### Settlement composition per (base, overlay) combination

For **`consulting_direct` + no overlay** (pure Holistika solo delivery):
- One settlement document; goes to Holistika finance only.
- Collaborator-side = €0; no external party receives a statement.

For **`consulting_direct` + `bd_commission_overlay`** (SUEZ shape post-EL):
- TWO settlement documents:
  1. Overlay-party statement → BD-intro partner (e.g., Aïsha) receives
     ONLY their overlay slice line item; their statement does NOT
     reference TRUE_MARGIN or post-overlay math (it's none of their
     business — they're paid off-the-top regardless).
  2. Holistika-internal statement → captures TRUE_MARGIN composition +
     base 100/0 split + founder billed time addback.
- Cite both the base pattern AND the overlay pairing in each statement
  header.

For **`bd_intro_only` + no overlay**:
- TWO settlement documents:
  1. Collaborator statement → 15% share of TRUE_MARGIN line item;
     no billed time addback (intro-only collaborators are not
     operational).
  2. Holistika-internal statement → 85% TRUE_MARGIN share + founder
     billed time addback.

For **`deep_partner_65_35` + no overlay** (Websitz/Rushly shape):
- TWO settlement documents:
  1. Collaborator statement → their billed time line + their 35%
     TRUE_MARGIN share line. Total = sum.
  2. Holistika-internal statement → founder billed time + 65%
     TRUE_MARGIN share.

For **`deep_partner_65_35` + `bd_commission_overlay`** (rare; methodology-trained
partner + separate BD-intro slice):
- THREE settlement documents:
  1. Overlay-party statement (BD intro slice off-the-top).
  2. Operational collaborator statement (billed time + 35% post-overlay
     TRUE_MARGIN).
  3. Holistika-internal statement (founder billed time + 65%
     post-overlay TRUE_MARGIN).

For **`joint_venture_aventure` + no overlay** (peer JV — Aventure shape):
- TWO settlement documents:
  1. JV-peer statement (their billed time + 50% TRUE_MARGIN share).
  2. Holistika-internal statement (founder billed time + 50%
     TRUE_MARGIN share).

For any combination involving `methodology_in_progress` on the
operational collaborator row:
- ALSO attach the operator-ratified mentoring-clause line item from
  PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv showing the in-kind methodology
  training Holistika is providing as part of the engagement (so the
  collaborator understands why their 35% isn't actually free — methodology
  training is the implicit Holistika contribution being amortised across
  the engagement).

The collaborator's confidence in the math comes from the reproducible
audit trail (5 CSVs + DECISION_REGISTER + settlement Markdown +
doctrine version + methodology-readiness rationale where applicable),
not from operator assertion.

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

1. ✓ `(share_pattern, share_overlay, methodology_readiness)` triple
   resolved via inline-ratify (NOT defaulted silently). All 3 axes
   ratified explicitly per Principle 1 decision tree.
2. ✓ Doctrine §2.3 (4 base patterns) + §2.4 (methodology_readiness
   axis) + §3 worked examples (SUEZ post-EL, Websitz, hypothetical
   bd_intro_only) re-read if unclear.
3. ✓ Overlay-base pairing valid (`bd_commission_overlay` pairs ONLY
   with `consulting_direct` or `deep_partner_65_35`; CS-09 enforces).
4. ✓ Methodology-pattern coherence checked: `methodology_naive` +
   `deep_partner_65_35` triggers CS-09 FAIL (35% compromise failure
   mode); requires either base downgrade to `consulting_direct` OR
   methodology upgrade to `methodology_in_progress` with mentoring
   clause.
5. ✓ All 5 CSVs touched in the same commit (or N/A noted in commit
   message for CSVs that don't change).
6. ✓ SHARE_REGISTRY row count matches `(share_pattern, share_overlay)`:
   1 base row for solo base + overlay none; 1 base + 1 overlay row when
   overlay paired.
7. ✓ Cross-CSV FKs resolve (grepped the FK target file before commit).
8. ✓ DECISION_REGISTER row authored for every override
   (`market_rate_excursion` / `share_split_deviation` /
   `overlay_pct_deviation` / `bill_mode_deviation` /
   `methodology_pattern_coherence_override`).
9. ✓ `py scripts/validate_collaborator_share.py` PASS for CS-01..CS-09
   (or known WARN findings explained in commit message).
10. ✓ Settlement Markdown emitted per Principle 5 composition rules
    (1/2/3 statements depending on `(base, overlay)` combination); each
    statement names doctrine version + the (base, overlay,
    methodology_readiness) triple in the header.
11. ✓ `parallel_invoice_stream_indicator` set correctly on each row
    (true when the row-holder issues their own invoice to the customer
    directly per D-IH-86-EK; false when they invoice Holistika
    internally).
12. ✓ operator-scratchpad entry appended naming engagement_id, the
    full triple, decision IDs (D-IH-86-EJ + any EL/successor for
    SUEZ-shape recommercialisation).
13. ✓ Mirror sync run (`--collaborator-share-only`) if CSV rows changed
    (new columns: `share_overlay`, `methodology_readiness`,
    `parallel_invoice_stream_indicator`, `overlay_pct_deviation`).
14. ✓ External-render trail set up if settlement Markdown going to
    collaborator OR investor audience (per
    `akos-external-render-discipline.mdc`).

## Anti-patterns (recovery patterns)

- **Anti-pattern: silently default to `deep_partner_65_35`** — most
  common failure for `consulting_direct` or `bd_intro_only` engagements
  where the BD partner is not actually operational on delivery.
  Recovery: re-resolve the `(share_pattern, share_overlay,
  methodology_readiness)` triple per Principle 1; rebuild SHARE_REGISTRY
  rows with the correct pattern; rerun CS-03 + CS-04 + CS-08 + CS-09;
  amend the engagement-folder settlement if already issued. The SUEZ
  POC pre-D-IH-86-EL state is the worked precedent for this recovery
  (originally minted as `orchestration_broker_thin_margin` with 4 rows;
  recommercialised to `consulting_direct + bd_commission_overlay` with
  2 rows).
- **Anti-pattern: the "35% compromise" — pair `methodology_naive`
  collaborator with `deep_partner_65_35`** — the most insidious failure
  mode the Wave R+2 rewrite is designed to prevent. The collaborator
  walks away with 35% but Holistika carries the full methodology load
  (because the collaborator can't apply it independently). CS-09 FAILs
  this immediately. Recovery: either (a) downgrade the base to
  `consulting_direct` and use `bd_commission_overlay` for the
  collaborator's intro slice (their actual value-add); OR (b) upgrade
  the collaborator to `methodology_in_progress` and add a mentoring
  clause to PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv showing the in-kind
  training Holistika provides during the engagement (which justifies
  why the 35% is now "fair" — they're learning, not just executing).
- **Anti-pattern: forget overlay row authoring when `share_overlay` is
  set** — the overlay slice is a SEPARATE SHARE_REGISTRY row, not a
  field on the base row. Forgetting the overlay row means CS-09 FAILs
  on overlay-base pairing (no overlay row found for the declared
  `share_overlay` value). Recovery: author the overlay row with the
  overlay-party as `collaborator_id`, the overlay-party's
  `methodology_readiness` as `methodology_not_applicable` (overlay
  parties are not operational), and `parallel_invoice_stream_indicator`
  per the overlay-party's invoicing arrangement.
- **Anti-pattern: bill founder time AND claim 65% Holistika share**
  (double-dip on `deep_partner_65_35`) — Recovery: the unified
  TRUE-MARGIN formula already handles this correctly
  (`founder_billed_time` is subtracted from POST_OVERLAY_REVENUE before
  the base split, then added back to Holistika-side total). The error
  appears when the operator manually computes without using the
  runbook. Always run `py scripts/collaborator_share_calculate.py` for
  settlement math; never hand-compute.
- **Anti-pattern: forget the VENDOR_SERVICES_BILLED roster** — the
  10-row roster is mandatory even when all 10 are in-kind defaults. The
  audit trail (which Holistika services were considered AND in-kind
  vs billed) IS the artifact. Recovery: author all 10 rows in a
  follow-up commit; never bypass the roster.
- **Anti-pattern: deviate `overlay_pct_deviation` without a decision
  row** — the default overlay percentage is 15% per D-IH-86-EJ §4.2;
  deviating up (e.g., 20% to a deeply-relational BD partner) or down
  (e.g., 10% to reflect lower intro-effort) requires an
  `overlay_pct_deviation` override row in COLLABORATOR_RATE_OVERRIDES.csv
  + a DECISION_REGISTER row naming the rationale. Silent deviation
  fails CS-08 immediately. Recovery: author both rows in the same
  commit as the SHARE_REGISTRY overlay row.

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
