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
last_review: 2026-05-26
last_review_by: Founder/CEO
last_review_decision_id: D-IH-86-EJ
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-DA
  - D-IH-86-DB
  - D-IH-86-DC
  - D-IH-86-DD
  - D-IH-86-DE  # superseded by D-IH-86-EJ (Wave R+2 rewrite)
  - D-IH-86-EJ  # 4-base + 1-overlay enum rewrite + CS-09 + methodology_readiness axis
  - D-IH-86-EK  # methodology_readiness + parallel_invoice_stream_indicator ratify
  - D-IH-86-EL  # SUEZ recommercialisation consulting_direct + bd_commission_overlay
  - D-IH-86-EM  # Stage-1 reset to charter pending re-active-promotion gate
  - D-IH-86-EN  # methodology_readiness x share_pattern coherence (CS-09 NEW)
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

## Inputs (with `(share_pattern, share_overlay, methodology_readiness)` triple routing)

For **every** trigger:

- `engagement_id` — slug matching the engagement folder under
  `docs/references/hlk/v3.0/Think Big/<Clients|Advisers>/<engagement-slug>/`.
- `collaborator_id` — FK to `GOI_POI_REGISTER.csv` (resolve before
  authoring; seed a new POI row first if the collaborator is new).
- `engagement_model_id` — FK to `ENGAGEMENT_MODEL_REGISTRY.csv`
  (typically `eng_model_percentage_collaborator` for `deep_partner_65_35`
  shape; `eng_model_consulting_direct` for `consulting_direct` shape;
  forward-charter per D-IH-73-J extension at successor commits).
- **`share_pattern`** — the base routing input per D-IH-86-EJ (4 base
  values; the Wave R+1 `orchestration_broker_thin_margin` value is
  superseded and decomposed into `consulting_direct + bd_commission_overlay`
  per D-IH-86-EL):
  - `consulting_direct` *(default for solo Holistika delivery)* — pick
    when Holistika delivers solo with no operational collaborator. Base
    split is 100/0. **Worked precedent post-D-IH-86-EL: SUEZ POC base.**
  - `bd_intro_only` — pick when the collaborator brought the deal but
    has no operational role on delivery. Base split is 85/15. Use ONLY
    when the BD partner does not require the
    `bd_commission_overlay` shape AND the deal cannot be classified as
    `consulting_direct` (e.g., the partner has a small ongoing
    relationship-management role).
  - `deep_partner_65_35` — pick when Holistika contributes a full
    methodology + machinery + execution stack as the value of its 65%
    share; collaborator brings methodology-readiness AND operates the
    process; B2B partner narrative applies. Base split 65/35. **Lived
    precedent: Websitz / Rushly engagement.**
  - `joint_venture_aventure` — pick when Holistika and the partner are
    symmetric peers; both bring methodology stacks; both have operational
    roles. Base split 50/50. **Worked precedent: Aventure-shape JV.**
- **`share_overlay`** — the overlay axis per D-IH-86-EJ (1 overlay value
  + null):
  - `null` *(default)* — no overlay party; settlement involves only the
    base pattern parties.
  - `bd_commission_overlay` — pick when a BD-intro partner takes a
    commission slice OFF THE TOP of revenue (default 15%) BEFORE the
    base TRUE_MARGIN math runs. Pairs ONLY with `consulting_direct` OR
    `deep_partner_65_35`; CS-09 FAILs other pairings (e.g.,
    `bd_intro_only + bd_commission_overlay` is redundant; `joint_venture_aventure
    + bd_commission_overlay` is incoherent). **Worked precedent
    post-D-IH-86-EL: SUEZ POC Aïsha intro slice.**
- **`methodology_readiness`** — the collaborator-capability axis per
  D-IH-86-EK + CS-09 gating per D-IH-86-EN (4 values):
  - `methodology_trained` — collaborator has internalised Holistika
    methodology + can operate independently. Pairs cleanly with
    `deep_partner_65_35` (full 35% justified) OR `joint_venture_aventure`
    (symmetric peer).
  - `methodology_in_progress` — collaborator is being trained mid-engagement.
    Pairs with `deep_partner_65_35` ONLY IF a mentoring clause from
    `PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv` is attached
    (`clause_mentoring_methodology_in_progress` or equivalent) showing
    the in-kind methodology training Holistika provides during the
    engagement. Otherwise CS-09 WARN.
  - `methodology_naive` — collaborator has NOT internalised methodology
    + cannot operate independently. CS-09 FAILs the pairing with
    `deep_partner_65_35` (the "35% compromise" failure mode: collaborator
    walks away with 35% but Holistika carries the full methodology
    load). Required pairings: `consulting_direct + bd_commission_overlay`
    (BD-only role) OR `bd_intro_only` (small ongoing role).
  - `methodology_not_applicable` — used for overlay rows
    (`bd_commission_overlay` parties are not operational; methodology
    doesn't apply). The base row's `methodology_readiness` is what CS-09
    audits; the overlay row's is documentary only.
- **`parallel_invoice_stream_indicator`** (boolean, per row) — set true
  when the row-holder issues their own invoice directly to the
  customer; false when they invoice Holistika internally for downstream
  remittance.

### Triple resolution decision matrix (operator quick-reference)

| Operational shape | Methodology fit | Recommended triple |
|:---|:---|:---|
| Holistika solo + BD intro | n/a | `consulting_direct + bd_commission_overlay + methodology_not_applicable` (overlay row) + `methodology_trained` (base Holistika row) |
| Holistika solo, no BD | n/a | `consulting_direct + null + methodology_trained` |
| Partner-operated, trained partner | trained | `deep_partner_65_35 + null + methodology_trained` |
| Partner-operated, training in progress | in_progress | `deep_partner_65_35 + null + methodology_in_progress` + mentoring clause |
| Partner-operated, naive partner | naive | **CS-09 FAIL** — re-classify to `consulting_direct + bd_commission_overlay` OR upgrade methodology to `in_progress` |
| Symmetric peer JV | trained both sides | `joint_venture_aventure + null + methodology_trained` |
| Small ongoing partner role | n/a operational | `bd_intro_only + null + methodology_not_applicable` |

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

### Step 1 — Resolve the `(share_pattern, share_overlay, methodology_readiness)` triple BEFORE drafting any CSV row

Inline-ratify gate per `akos-inline-ratification.mdc`: post a 3-question
`AskQuestion` (one per axis) OR a single composite question with 5-7
ranked combinations + recommended default based on the engagement's
operational shape + methodology fit. The triple is LOAD-BEARING — the
wrong combination cascades into CS-03/CS-04/CS-08/CS-09 producing
incorrect settlement math OR a CS-09 FAIL the agent will have to
unwind.

Decision sequence (mirrors the Principle 1 decision tree in
[`collaborator-share-craft`](../../../../../../.cursor/skills/collaborator-share-craft/SKILL.md)):

1. **Q1 — Operational shape**: who actually executes the delivery
   work on this engagement? Solo Holistika → `consulting_direct`.
   Partner operates the process → `deep_partner_65_35` OR
   `joint_venture_aventure`. Partner only made the intro / has small
   ongoing role → `bd_intro_only`.
2. **Q2 — Methodology fit** (only material when partner is operational):
   is the partner methodology_trained / in_progress / naive? If naive +
   `deep_partner_65_35` selected → STOP, re-classify to
   `consulting_direct + bd_commission_overlay` to avoid the "35%
   compromise" failure mode (CS-09 will FAIL the original framing).
3. **Q3 — Overlay axis**: is there a BD-intro party taking a slice off
   the top? If yes → `share_overlay = bd_commission_overlay` (requires
   `consulting_direct` or `deep_partner_65_35` base; CS-09 enforces).
   If no → `null`.

Worked examples:

- **SUEZ POC** (post-D-IH-86-EL) → `(consulting_direct,
  bd_commission_overlay, methodology_trained)` for the base Holistika
  row + `(consulting_direct, bd_commission_overlay,
  methodology_not_applicable)` for the Aïsha overlay row. Pre-EL state
  was `orchestration_broker_thin_margin` with 4 rows; reclassification
  surfaced because Aïsha is the BD-intro party and SUEZ delivery is
  Holistika-direct.
- **Websitz / Rushly extension** → `(deep_partner_65_35, null,
  methodology_trained)`. Bricelle is methodology_trained + operates
  the process. MKTOPS overlap handled via
  `clause_partner_marketing_agency_overlap`.
- **Hypothetical methodology_in_progress partner** → `(deep_partner_65_35,
  null, methodology_in_progress)` + attach
  `clause_mentoring_methodology_in_progress` to
  PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv showing the in-kind training.
  CS-09 PASS conditional on the mentoring clause being present.
- **methodology_naive partner attempted on deep_partner_65_35** → CS-09
  FAIL immediately. STOP — re-classify to `(consulting_direct,
  bd_commission_overlay, methodology_not_applicable)` for the partner
  (their actual value-add is the intro slice, not co-delivery).

If unclear after walking Q1-Q3, halt and re-read the doctrine §2.3 +
§2.4 (methodology_readiness axis NEW per D-IH-86-EK) + §3 worked
examples + §6.3 (CS-09 details) before authoring.

### Step 2 — Author the canonical CSV rows

Append rows to the 5 CSVs in this order (FKs resolve forward to back):

1. `COLLABORATOR_MARKET_RATE_REFERENCE.csv` — seed row for the
   collaborator's `role_class × region × experience_band` if missing.
2. `PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv` — append any new clause
   patterns the engagement surfaces (typically reuses existing rows).
   When `share_pattern = deep_partner_65_35` AND
   `methodology_readiness = methodology_in_progress`, attach
   `clause_mentoring_methodology_in_progress` to the engagement
   showing the in-kind training Holistika provides during the
   engagement window. CS-09 expects this clause as the WARN-clearance
   path for the in-progress methodology state.
3. `HOLISTIKA_VENDOR_SERVICES_BILLED.csv` — author 10 rows (one per
   service class per doctrine §2.2 defaults); flag any deviations with
   `bill_mode_decision_id`.
4. `COLLABORATOR_SHARE_REGISTRY.csv` — author the SHARE_REGISTRY
   row(s) per the `(share_pattern, share_overlay)` combination:
   - `consulting_direct + null` → 1 row (Holistika).
   - `consulting_direct + bd_commission_overlay` → 2 rows: base
     Holistika row + overlay row for the BD party. The overlay row
     carries `share_pattern = consulting_direct`,
     `share_overlay = bd_commission_overlay`,
     `methodology_readiness = methodology_not_applicable`, and an
     `overlay_pct_deviation` value if the operator ratified a
     non-default % (default = 15%).
   - `bd_intro_only + null` → 2 rows: base Holistika row +
     small-ongoing-role partner row.
   - `deep_partner_65_35 + null` → 2 rows: Holistika row + collaborator
     row; per-row splits sum to 100.
   - `deep_partner_65_35 + bd_commission_overlay` → 3 rows: Holistika
     base + collaborator base + overlay row.
   - `joint_venture_aventure + null` → 2 rows summing 50/50.
   - **Methodology readiness per row**: the BASE rows carry the
     operationally-relevant `methodology_readiness` value (CS-09
     audits these). Overlay rows carry `methodology_not_applicable`
     (documentary only).
   - **Parallel invoice stream indicator per row**: set true when
     that party invoices the customer directly; false when they
     invoice Holistika downstream. Per D-IH-86-EK this is a per-row
     boolean; do not collapse across rows.
5. `COLLABORATOR_RATE_OVERRIDES.csv` — append override rows for any:
   - `market_rate_excursion` (rate >25% above/below
     `COLLABORATOR_MARKET_RATE_REFERENCE.csv`); requires
     `override_decision_id` FK.
   - `share_split_deviation` (split outside the base-pattern anchor);
     requires `override_decision_id` FK.
   - `bill_mode_deviation` (vendor service billing flag flipped from
     default); requires `bill_mode_decision_id` on the corresponding
     `HOLISTIKA_VENDOR_SERVICES_BILLED.csv` row (NOT on the override
     row — the deviation lives at the bill row).
   - `overlay_pct_deviation` (overlay party slice ≠ default 15%);
     stored as a row field on the overlay SHARE_REGISTRY row, NOT
     in this CSV; this CSV captures the ratifying decision lineage
     when the deviation is large.

For each row authored, the agent confirms FK resolution against the
target canonical BEFORE the commit (`Grep` against the FK target file).
The 5-CSV authoring is ONE atomic commit; intermediate states FAIL
CS-02.

### Step 3 — Run the validator self-test + full sweep

```
py scripts/validate_collaborator_share.py --self-test    # MUST exit 0
py scripts/validate_collaborator_share.py                # full sweep
py scripts/collaborator_share_calculate.py --self-test   # MUST exit 0
```

The self-test verifies the 9 CS-NN checks load + return well-formed
`CollaboratorShareAuditRow` Pydantic models per D-IH-86-EJ + EN. If
FAIL, the validator is broken — halt and fix before continuing.

The full sweep emits per-row findings. Expected outcomes per
`(share_pattern, share_overlay)` combination:

- **`consulting_direct + null`** (Holistika solo):
  - CS-03 PASS (single base row carries 100% Holistika; trivial sum).
  - CS-04 PASS (no collaborator → no market-rate audit triggers).
  - CS-08 PASS (`share_pattern` and `share_overlay` enum members valid).
  - CS-09 PASS (no overlay; methodology_readiness on base row is documentary).
- **`consulting_direct + bd_commission_overlay`** (SUEZ post-EL shape):
  - CS-03 PASS (overlay slice is OFF THE TOP; base row still 100%
    Holistika after overlay deduction; across-rows sum-to-100 unifies
    base + overlay = 100% of post-overlay revenue).
  - CS-04 PASS (no collaborator co-delivery → no market-rate audit).
  - CS-08 PASS.
  - CS-09 PASS conditional on: (a) overlay pairing valid
    (`consulting_direct + bd_commission_overlay` IS in
    `VALID_OVERLAY_BASE_PAIRINGS`); (b) overlay row carries
    `methodology_readiness = methodology_not_applicable`; (c) base row's
    methodology is anything except naive (no naive co-delivery hazard
    on consulting_direct base).
- **`bd_intro_only + null`** (small ongoing role):
  - CS-03 PASS (across-rows sum-to-100; default 85/15).
  - CS-04 WARN if collaborator row deviates from 15 anchor without
    override row.
  - CS-08 PASS. CS-09 PASS (no overlay; methodology_readiness on
    partner row is documentary).
- **`deep_partner_65_35 + null`** (Websitz / Rushly shape):
  - CS-03 PASS (per-row sum-to-100; 65/35 default).
  - CS-04 PASS if rates within ±25% of reference OR override row exists.
  - CS-08 PASS.
  - CS-09 PASS conditional on `methodology_readiness IN
    {methodology_trained, methodology_in_progress}`. If
    `methodology_naive` → CS-09 **FAIL** with the "35% compromise"
    finding — STOP, re-classify, do not commit.
  - CS-09 WARN if `methodology_in_progress` AND no mentoring clause
    attached.
- **`deep_partner_65_35 + bd_commission_overlay`** (deep partner +
  separate BD intro):
  - Same as above + overlay row CS-09 check (overlay pairing IS in
    `VALID_OVERLAY_BASE_PAIRINGS`; overlay row methodology must be
    `methodology_not_applicable`).
- **`joint_venture_aventure + null`** (Aventure-shape):
  - CS-03 PASS (across-rows sum-to-100; default 50/50).
  - CS-04 PASS if rates within band OR override.
  - CS-08 PASS.
  - CS-09 PASS conditional on `methodology_readiness =
    methodology_trained` on both rows (symmetric peer JVs assume
    both sides are trained).

If any CS-09 FAIL surfaces, the agent does NOT commit the row(s).
Instead: post an `AskQuestion` walking the operator through the
re-classification (typical path: `deep_partner_65_35 + methodology_naive`
→ `consulting_direct + bd_commission_overlay + methodology_not_applicable`
on the BD party + `methodology_trained` on the Holistika base row).

### Step 4 — Compute the settlement (charter / milestone / final modes)

```
py scripts/collaborator_share_calculate.py \
  --engagement <id> \
  --mode <charter|milestone|final> \
  [--share-pattern <base-pattern>] \
  [--share-overlay <overlay-or-none>]
```

The runbook reads the 5 CSVs + the engagement folder's billed-hours
roster, applies the **unified TRUE-MARGIN formula** (D-IH-86-EJ),
allocates per-row splits across all 4 base patterns + optional overlay,
emits advisory notes, and writes a Markdown settlement statement under
`docs/references/hlk/v3.0/Think Big/<Clients|Advisers>/<engagement-slug>/settlement-<mode>-<YYYY-MM-DD>.md`.

**Unified TRUE-MARGIN formula** (applies to ALL 4 base patterns; the
Wave R+1 per-pattern formulas were collapsed into one in the rewrite
per D-IH-86-EJ):

```
TRUE-MARGIN = invoiced_revenue
            − billed_direct_costs   (per VENDOR_SERVICES_BILLED bill_mode=billed rows)
            − overlay_amount        (if share_overlay != null; OFF THE TOP)

per-row payout = row.share_pct × (TRUE-MARGIN − in_kind_imputed_value)
                                where in_kind_imputed_value is captured but does
                                NOT reduce TRUE-MARGIN (it's documentary)
```

**Composition per `(share_pattern, share_overlay)`**:

- **`consulting_direct + null`** → 1 base row; Holistika carries
  100% of TRUE-MARGIN.
- **`consulting_direct + bd_commission_overlay`** → 1 overlay row
  (paid OFF THE TOP at `overlay_pct` or `overlay_pct_deviation`) +
  1 base row carrying 100% of remaining TRUE-MARGIN. Settlement
  statement names the overlay party + the base party explicitly.
- **`bd_intro_only + null`** → 2 base rows (Holistika + BD party);
  default 85/15 split of TRUE-MARGIN.
- **`deep_partner_65_35 + null`** → 2 base rows (Holistika + partner);
  default 65/35 per-row split of TRUE-MARGIN.
- **`deep_partner_65_35 + bd_commission_overlay`** → 1 overlay row +
  2 base rows (65/35 of remaining TRUE-MARGIN). Used when a third-
  party BD introduced the deal that landed as a deep partnership.
- **`joint_venture_aventure + null`** → 2 base rows (symmetric);
  default 50/50 split of TRUE-MARGIN.

**Parallel invoice stream indicator**: when any row carries
`parallel_invoice_stream_indicator = true`, the runbook emits an
advisory note in the settlement statement reminding the operator that
the row's `share_pct × TRUE-MARGIN` is the **commission slice**, NOT
the row-holder's total revenue from the engagement (the row-holder
also invoices the customer directly under a parallel contract).

**Methodology readiness in the settlement**: each per-row payout line
includes the row's `methodology_readiness` as a documentary annotation
(e.g., `Aïsha (methodology_trained)`, `Hugo (methodology_not_applicable)`)
so the audit trail captures why the row earned what it earned.

**Advisory notes engine** emits per-row hints when:
(a) default-anchor mismatch (row split deviates from pattern default
without an override row);
(b) overlay-base pairing invalid (CS-09 also FAILs);
(c) methodology-readiness eligibility mismatch (CS-09 also FAILs);
(d) market-rate band excursion (>±25%) without override row;
(e) bill_mode deviation without `bill_mode_decision_id`.

For `custom` patterns (deferred per D-IH-86-EJ §2.3 narrative), the
runbook would emit a MANUAL placeholder pointing at the override
decision row — operator authors the math by hand. `custom` is NOT in
the 4-base + 1-overlay enum today; it is a forward-charter pointer for
a future enum extension when a non-fitting commercial shape arises.

### Step 5 — Share the settlement with the collaborator (transparency cadence)

Per the doctrine §10 Self-discipline Rule 5, the agent attaches the
settlement Markdown + the relevant doctrine version reference when
emailing or DM-ing the collaborator. The collaborator's confidence in
the math comes from the reproducible audit trail, not from operator
assertion.

Transparency cadence per `(share_pattern, share_overlay)`:

- **`consulting_direct + null`** — no collaborator to share with;
  settlement is internal documentation only (audit trail for Holistika
  finance + future operator references).
- **`consulting_direct + bd_commission_overlay`** — overlay party
  receives **their overlay slice only** at milestone-close + final-
  close cadence. The base TRUE-MARGIN figure is **not** shared with
  the overlay party (they have no claim to it; commission is OFF THE
  TOP). The overlay party's settlement shows: invoiced revenue ×
  overlay_pct = their payout. Per SUEZ POC (D-IH-86-EL), the BD party
  gets their commission per stage close; Holistika retains the rest.
- **`bd_intro_only + null`** — BD party receives their slice
  (default 15%) at each milestone close. Holistika carries the base.
- **`deep_partner_65_35 + null`** — deep partner receives their slice
  at each milestone close + at final close, with FULL TRUE-MARGIN
  transparency (the partner is co-delivering; opaque math erodes
  partner trust per §10 Rule 5).
- **`deep_partner_65_35 + bd_commission_overlay`** — overlay party
  receives their overlay slice (as above); deep partner receives
  their 35% of remaining TRUE-MARGIN with FULL transparency on the
  remaining-after-overlay base figure (the partner sees the overlay
  deduction line so they understand the base).
- **`joint_venture_aventure + null`** — both JV peers see the full
  settlement at every milestone (symmetric peer relationship; both
  sides have equal claim to the math).

For all patterns: when a row carries `parallel_invoice_stream_indicator
= true`, the settlement makes explicit that this slice is the
commission portion only and the row-holder's parallel direct invoicing
to the customer is separate (preventing accidental double-counting in
the partner's bookkeeping).

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
- **CS-03 FAIL on across-rows sum-to-100** → one or more SHARE_REGISTRY
  rows for the engagement are missing OR duplicated OR carry the wrong
  `share_pct`; recompute the per-engagement sum manually (base rows +
  overlay row), reconcile, then re-run the validator. CS-03 is unified
  across-rows post-D-IH-86-EJ (no longer per-row sum on
  deep_partner_65_35; this changed in Wave R+2).
- **CS-04 WARN on default-anchor mismatch** → row split deviates from
  the pattern default (consulting_direct=100; bd_intro_only=85/15;
  deep_partner_65_35=65/35; joint_venture_aventure=50/50) without an
  override row; either fix the split to the default OR author the
  override + DECISION_REGISTER row in the same commit.
- **CS-04 WARN on rate >25% above reference** → either seed the
  MARKET_RATE_REFERENCE row at a different rate (if the reference is
  stale) OR author the `market_rate_excursion` override row +
  DECISION_REGISTER row.
- **CS-08 FAIL on unknown `share_pattern` value** → typo in the
  CSV cell (must be exactly `consulting_direct` / `bd_intro_only` /
  `deep_partner_65_35` / `joint_venture_aventure`); fix the cell
  value, then re-run.
- **CS-08 FAIL on unknown `share_overlay` value** → typo in the CSV
  cell (must be exactly `bd_commission_overlay` OR empty/null); fix the
  cell value, then re-run.
- **CS-09 FAIL on invalid overlay-base pairing** → `share_overlay` is
  set on a row whose `share_pattern` is not in
  `VALID_OVERLAY_BASE_PAIRINGS` (the only valid pairings today are
  `consulting_direct + bd_commission_overlay` and
  `deep_partner_65_35 + bd_commission_overlay`); either remove the
  overlay OR re-classify the base pattern OR (rare) amend
  `VALID_OVERLAY_BASE_PAIRINGS` via operator inline-ratify gate +
  D-IH-86-EJ successor decision row before re-running.
- **CS-09 FAIL — "35% compromise" anti-pattern** → a row carries
  `share_pattern = deep_partner_65_35` AND `methodology_readiness =
  methodology_naive`. This is the load-bearing failure mode the rewrite
  exists to prevent (post-13/05 transcript framing per D-IH-86-EL +
  D-IH-86-EN). REMEDIATION: re-classify to `consulting_direct +
  bd_commission_overlay` with `methodology_not_applicable` on the
  overlay (BD party) row and `methodology_trained` on the Holistika
  base row. Do NOT silently lower the 35% share to compensate — that's
  the failure mode this check prevents. Re-author the 5-CSV bundle in
  one commit with the new pattern + DECISION_REGISTER row citing
  D-IH-86-EN as the gating decision.
- **CS-09 WARN — `methodology_in_progress` partner without mentoring
  clause** → attach `clause_mentoring_methodology_in_progress` to
  PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv + add a milestone-review row
  to the engagement folder for a re-evaluation at next close; this
  documents the methodology mentoring obligation.
- **Operator silence > 24h on a reversible disposition** → time-box
  recovery per `akos-inline-ratification.mdc` §"Time-box recovery";
  reversible (`bill_mode_deviation`, expired rate override) auto-defaults
  to recommended option; irreversible (commercial share-split deviation
  signed by collaborator, `share_pattern` re-classification) NEVER
  auto-defaults — halt and escalate.
- **Collaborator dispute on settlement math** → cite the doctrine
  version + the relevant CSV rows + the settlement Markdown; if the
  collaborator disputes the doctrine itself, escalate to operator
  inline-ratify gate to amend the doctrine + back-resolve the
  engagement with the amended math + a DECISION_REGISTER row naming
  the amendment lineage.
- **Settlement Markdown missing at engagement final-close commit** →
  release-gate INFO advisory while doctrine sits at charter (Stage-1
  reset per D-IH-86-EM); future promotion to FAIL gated on
  re-active-promotion decision row (D-IH-86-EO reserved) + the FAIL-ramp
  successor decision per Stage 2.

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
- Decision lineage:
  - D-IH-86-DA (doctrine mint + paired SOP gate).
  - D-IH-86-DB (TRUE-MARGIN formula; unified across all 4 base
    patterns post-EJ).
  - D-IH-86-DC (clause table schema).
  - D-IH-86-DD (Tier 1 WIP hygiene pre-requisite).
  - D-IH-86-DE (Wave R+1 3-shape `share_pattern` enum; **SUPERSEDED**
    by D-IH-86-EJ).
  - D-IH-86-DF (Wave R+1 Stage-1 active promotion; superseded by
    D-IH-86-EM Stage-1 reset to charter pending re-promotion).
  - D-IH-86-EJ (**Wave R+2 doctrine FULL REWRITE**: 4-base + 1-overlay
    enum + `share_overlay` axis + methodology-readiness axis + CS-09
    new + unified TRUE-MARGIN + CS-03 unified across-rows + CS-04
    composition-branching).
  - D-IH-86-EK (`methodology_readiness` 4-value axis +
    `parallel_invoice_stream_indicator` boolean per-row +
    CS-09 ratification).
  - D-IH-86-EL (SUEZ POC recommercialisation post-13/05 customer
    meeting: re-classified from `orchestration_broker_thin_margin` to
    `consulting_direct + bd_commission_overlay`; supersedes the Wave
    R+1 SUEZ rows).
  - D-IH-86-EM (Stage-1 status reset from `active` back to `charter`
    pending re-active-promotion gate against the rewritten doctrine).
  - D-IH-86-EN (methodology_readiness × share_pattern coherence
    gating; CS-09 "35% compromise" failure-mode prevention).
  - D-IH-86-EO (RESERVED; future Stage-1 re-active-promotion decision
    once 1+ engagement applies the rewritten doctrine end-to-end with
    CS-01..CS-09 PASS).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md
@.cursor/rules/akos-collaborator-share.mdc
