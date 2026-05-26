---
tranche_id: wave-r-plus-2-doctrine-rewrite-collaborator-share-4-base-1-overlay
tranche_class: internal_governance
tranche_title: COLLABORATOR_SHARE_DOCTRINE.md full rewrite — 3-pattern enum replaced by 4-base + 1-overlay shape per operator Q1=a_full_rewrite_now ratify (post-transcript substrate)
audiences_named:
  - J-OP
  - J-AIC
  - J-PT
channels_named: []
scenarios_named:
  - operator_consuming_corrected_doctrine_authoring_new_share_registry_row
  - aic_role_owner_running_synthesis_sweep_on_engagement_class_tranche_with_corrected_share_pattern_resolution
  - future_collaborator_reading_engagement_specific_settlement_statement_with_corrected_commercial_shape_narrative_jpt_secondary
  - operator_inline_ratify_resolution_picking_among_4_base_patterns_plus_optional_overlay_at_engagement_charter
brand_register: internal-corpint
ratifying_decisions:
  - D-IH-86-EJ
  - D-IH-86-EK
  - D-IH-86-EL
  - D-IH-86-EM
  - D-IH-86-EN
  - D-IH-86-DA
  - D-IH-86-DB
  - D-IH-86-DC
  - D-IH-86-DD
  - D-IH-86-DE
  - D-IH-86-EA
  - D-IH-86-EB
  - D-IH-86-EC
  - D-IH-86-ED
  - D-IH-86-EE
erp_surface_citations: []
is_atomic_commit: false
closing_loop_test: py scripts/validate_collaborator_share.py PASS (CS-01..CS-09; 5 CSVs with corrected SUEZ rows + retained Aïsha-row-as-bd-commission-overlay) + py scripts/collaborator_share_calculate.py --self-test PASS + py scripts/synthesis_before_tranche_check.py --check-charter docs/wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-2-doctrine-rewrite-collaborator-share-4-base-1-overlay.md PASS + py scripts/synthesis_before_tranche_check.py --self-test PASS + py scripts/validate_decision_register.py PASS (5 supersede + 5 new = 10 amended rows) + py scripts/validate_hlk.py OVERALL PASS + py -m pytest tests/test_hlk_collaborator_share.py tests/test_validate_collaborator_share.py -v PASS (target 75+ tests; up from 37 base + 20 enum-amendment) + grep VALID_SHARE_PATTERNS in akos/hlk_collaborator_share.py shows exactly 4 base + grep VALID_SHARE_OVERLAYS shows exactly 1 entry + grep orchestration_broker_thin_margin in any non-superseded canonical returns ZERO results (proving full removal from active doctrine)
recipient_fallback_channel: doctrine is J-OP-primary so no external recipient fallback applies; J-PT-secondary collaborator-facing settlement statements continue to live in engagement folders per per-engagement application of the rewritten doctrine (Drive distribution if any happens via per-engagement workflow not this commit)
reversibility_class: medium
reversibility_rationale: Doctrine rewrite (Commits 1-4) is fully reversible via git revert — no irreversible commitments embedded in the markdown / Pydantic / validator / governance authoring layer. SHARE_REGISTRY row correction (Commit 5) for SUEZ is medium-reversibility — the existing rows are status=draft (un-signed with collaborators) so correction does not break a signed commitment; correcting from `orchestration_broker_thin_margin` (incorrect) to `consulting_direct + bd_commission_overlay` (transcript-substantiated correct shape) is itself the act of preserving integrity. Supabase mirror DDL amendment (Commit 6) is reversible via rollback section (forward-migration carries an explicit rollback); however applying the forward migration to a populated remote table is medium-cost (operator-side operation; not auto-executed by this commit). D-IH-86-DF supersede (active-promotion based on wrong shape) is one-way at the DECISION_REGISTER row level — supersede row stays in history; the prior promotion's narrative effects (HOLISTIKA_QUALITY_FABRIC §6 13th-specialty row status flip) need explicit re-application after the corrected SUEZ encoding satisfies Stage 1 gate (deferred to next session per Q1=b ratify). Closing-loop verification confirms reversibility via fully-passing test suite + zero residual `orchestration_broker_thin_margin` references in active doctrine.
---

# Wave R+2 — COLLABORATOR_SHARE_DOCTRINE.md full doctrine rewrite (4-base + 1-overlay shape)

## Purpose

Execute the 13th specialty COLLABORATOR_SHARE_DOCTRINE.md **full doctrine rewrite** ratified at the operator's `Q1=a_full_rewrite_now` ratification gate (post-meta-discussion 2026-05-25 + reinforced post-transcript 2026-05-26). Replace the existing 3-pattern enum (`deep_partner_65_35` / `orchestration_broker_thin_margin` / `custom`) — minted at Wave R+1 Commit 2b-ext per D-IH-86-DE — with an expanded **4-base + 1-overlay** shape that better reflects the operator's lived commercial reality across all engagement classes:

| Base pattern | Shape | Replaces |
|:---|:---|:---|
| **`bd_intro_only`** *(NEW)* | Pure deal-source (sales-style introduction); no execution; collaborator gets one-time finder's-fee % of contract value. Margins for Holistika: 85-95%. | Net-new shape; no prior pattern covered it. |
| **`joint_venture_aventure`** *(NEW)* | Co-venture where operator + collaborator co-create a deal-vehicle (legal entity OR contractual shared P&L); both parties take risk; margins split per per-venture agreement. | Net-new shape; orchestration_broker was misused for some JV-shape encodings. |
| **`consulting_direct`** *(NEW)* | Holistika prime-bills client directly; NO collaborator-share component in the SHARE_REGISTRY row. Solo execution by Holistika team. SUEZ POC actual shape per 2026-05-13 customer-meeting transcript substrate. | Net-new shape; orchestration_broker was misused for SUEZ encoding. |
| **`deep_partner_65_35`** *(RETAINED, refined)* | Existing pattern — Holistika contributes full methodology + machinery as value of 65% share; collaborator brings deal + operates process. Websitz/Rushly precedent. | Retained from D-IH-86-DE. |

| Stackable overlay | Shape | When |
|:---|:---|:---|
| **`bd_commission_overlay`** *(NEW)* | Stackable concept (NOT a base pattern). Adds N% (operator-defined; typical 10-15%) of Holistika's net margin to a collaborator who brought the deal but isn't operating it. Can stack on `consulting_direct` / `deep_partner_65_35` / `joint_venture_aventure` (NOT on `bd_intro_only` — BD intro IS the deal). | When deal-sourcing partner is structurally different from execution-operator party (the operator's *"15% of business development that i give to people when they don't work but just come and give us a project"* framing). |

| Removed pattern | Reason |
|:---|:---|
| **`orchestration_broker_thin_margin`** *(REMOVED)* | Per operator framing 2026-05-22: this enum was an **architectural invention** by the agent at Wave R+1, NOT a real operator-codified commercial pattern. The original encoding force-fit the SUEZ deal into a 3-way revenue split with Holistika at 6%, but the 2026-05-13 customer-meeting transcript substantiates that SUEZ is `consulting_direct` (Holistika prime-bills) + `bd_commission_overlay` (Aïsha-via-EFA-intro stacked) — NOT a 3-way revenue split. Full removal preserves doctrinal integrity; supersede chain in Commit 5 documents the architectural-invention mistake as durable lesson. |

Per the operator's verbatim framing (transcript-supported, 2026-05-22):

> *"I would nevver acceeptt sh holistik wwork for notthing. … what abot 15% of business development that i give to people when they don't work but just come and give us a projett and woork as business devveloppeerr/account mgr at lleast forr the beginning, getting their share over the margin so that they have an incenticce to bbring goood deals?"*

> *"yeah, ew need to get paid from oor own proojject like any consultancy does, and be lever so that the nmbers are cleverly crafted to sit oor interests."*

And per the 2026-05-13 SUEZ customer-meeting transcript substrate (load-bearing):

- Aïsha is positioned as **continuity operator post-project**, NOT as commercial party in the meeting — operator's verbatim *"Il s'est plus facile parce que c'est Aïsha qui fait ça, mais on voulait le dire au cas où il y a d'autres personnes"*.
- SUEZ commercial shape is **Holistika prime-bills SUEZ directly** — operator's verbatim positioning *"j'avais commencé à créer ma propre compagnie [Holistika]"* + *"si le fait d'avoir un prestataire extérieur, comme fait sale, permet peut-être de dynamiser le sujet, pourquoi pas, ça peut être intéressant"* — customer recognizes external-prestation B2B vendor posture.
- No 3-way revenue split is visible anywhere in the meeting.

### Methodology-readiness axis (NEW; §2.5 of rewritten doctrine)

Beyond the share_pattern enum, the rewrite introduces a **methodology-readiness axis** as a separate scoring dimension on the SHARE_REGISTRY row:

| `methodology_readiness` value | What it means | Impact on share math |
|:---|:---|:---|
| **`methodology_trained`** | Collaborator can execute Holistika methodology unsupervised | More services contributed in-kind by collaborator; lower Holistika billed-against-project |
| **`methodology_in_progress`** | Collaborator being trained on Holistika methodology | Mixed mode; partial services billed; partial in-kind |
| **`methodology_naive`** | Collaborator needs Holistika to handhold the methodology | More Holistika services billed against project; affects `bd_commission_overlay` % calibration |
| **`methodology_not_applicable`** | Pattern doesn't require methodology engagement (e.g., `bd_intro_only` pure-intro) | No methodology axis impact on math |

This axis IS load-bearing for the operator's *"if I compromise for that 35%, we lose value if we don't have things ready"* concern — the methodology-readiness scoring makes the methodology IP explicit + audit-trail-bearing instead of implicit (which is how the value erosion was happening per operator's prior framing).

## Scope (in scope for this multi-commit tranche; 7 commits expected)

### Commit 1 — Doctrine canonical rewrite (~30min)

1. **Demote `COLLABORATOR_SHARE_DOCTRINE.md` frontmatter** `status: charter` (already charter; reconfirm post-amendment).
2. **Amend §2.3** — replace 3-pattern enum table with 4-base + 1-overlay table per the matrix at top of this charter.
3. **NEW §2.5** — methodology-readiness axis: 4-value enum + per-pattern impact table + worked example.
4. **Amend §3 worked examples** — restructure:
   - **§3.1** `deep_partner_65_35` Websitz lived precedent (RETAINED + refined for clarity).
   - **§3.2** `joint_venture_aventure` (NEW; forward-charter placeholder for first lived precedent).
   - **§3.3** `consulting_direct + bd_commission_overlay` SUEZ POC (CORRECTED from prior §3.2 orchestration_broker fiction; cites 2026-05-13 transcript verbatim quotes).
   - **§3.4** `bd_intro_only` (NEW; light worked example).
   - **§3.5** `custom` (RETAINED; minor refinement).
   - **§3.6** Stacking overlay worked example: `consulting_direct + bd_commission_overlay` math walkthrough for Aïsha-on-SUEZ (TRUE-MARGIN with 15% overlay applied on Holistika net margin → Aïsha gets her overlay-share on top of any per-hour billed continuity work she does post-project via VENDOR_SERVICES_BILLED rate).
5. **Amend §6** — CS-03/CS-04 4-way branching table + NEW CS-09 (overlay-base coherence check: every row with overlay must have valid base pattern + overlay-allowed-on-base matrix enforced).
6. **Amend §11 decision lineage** — supersede D-IH-86-DE (3-value enum); supersede D-IH-86-DF (active-promotion based on wrong shape); supersede D-IH-86-EG/EH/EI partially per SUEZ recommercialization (preserve EH artifact-shape; rewrite EG commercial-architecture; preserve EI atomicity); add **D-IH-86-EJ** (this rewrite ratification) + **D-IH-86-EK** (methodology-readiness axis mint) + **D-IH-86-EL** (4-base + 1-overlay shape mint) + **D-IH-86-EM** (CS-09 overlay-base-coherence mint) + **D-IH-86-EN** (SUEZ recommercialization to `consulting_direct + bd_commission_overlay`).
7. **Amend frontmatter** `ratifying_decisions` to add the 5 new D-IH-86-EJ..EN rows; `last_review_at` to 2026-05-26; `methodology_version_at_review` v3.2.

### Commit 2 — Pydantic chassis update (~45min)

8. **`akos/hlk_collaborator_share.py`**:
   - `VALID_SHARE_PATTERNS`: replace 3-value frozenset with 4-base frozenset (`bd_intro_only` / `joint_venture_aventure` / `consulting_direct` / `deep_partner_65_35`).
   - NEW `VALID_SHARE_OVERLAYS`: 1-value frozenset (`bd_commission_overlay`); document extensibility.
   - NEW `VALID_METHODOLOGY_READINESS`: 4-value frozenset.
   - NEW `OVERLAY_ALLOWED_BASES`: dict[str, frozenset[str]] mapping overlay → set of base patterns it can stack on.
   - Remove `ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT` constant (no longer used).
   - Extend `CollaboratorShareRegistryRow` model: add `share_overlay: str | None` (optional; FK to VALID_SHARE_OVERLAYS); add `overlay_pct: float | None` (operator-defined %; 0-100); add `methodology_readiness: str` (FK to VALID_METHODOLOGY_READINESS; default `methodology_trained`).
   - Extend `COLLABORATOR_SHARE_REGISTRY_FIELDNAMES` tuple: add 3 columns (`share_overlay`, `overlay_pct`, `methodology_readiness`) — total fieldnames count 17 → 20.
   - Refactor per-pattern helper functions: `compute_split_per_pattern(share_pattern, ...)` branches 4 ways; `check_overlay_allowed(base_pattern, overlay) -> bool`; `compute_overlay_amount(net_margin_amount, overlay_pct) -> float`.
9. **`tests/test_hlk_collaborator_share.py`**:
   - Extend tests for 4 new patterns + overlay coherence + methodology readiness.
   - Target: +30 tests (37 → 67+); per-pattern Pydantic validation + overlay-allowed-on-base matrix tests + methodology_readiness enum tests.

### Commit 3 — Validator + runbook update (~30min)

10. **`scripts/validate_collaborator_share.py`**:
    - Update CS-08 enum check: extend to validate `share_overlay` + `methodology_readiness` against new frozensets.
    - NEW CS-09 (overlay-base coherence): every row with non-empty `share_overlay` must (a) have a valid base `share_pattern`, AND (b) the overlay must be allowed on the base per `OVERLAY_ALLOWED_BASES`, AND (c) `overlay_pct` must be in 0-100 range, AND (d) carry a `share_override_decision_id` (overlays always require ratification per doctrine).
    - Update CS-03/CS-04 4-way branching: per-pattern invariant enforcement updated for 4 base patterns (no `orchestration_broker_thin_margin` branch; `consulting_direct` has NO per-row split check since Holistika prime-bills; `bd_intro_only` has finder's-fee % within 5-20% advisory band).
11. **`scripts/collaborator_share_calculate.py`** settlement-math per-pattern branching:
    - `deep_partner_65_35`: existing TRUE-MARGIN per §2.
    - `bd_intro_only`: REVENUE × collaborator_share_pct (where collaborator_share_pct = finder's fee %; typical 5-20%).
    - `joint_venture_aventure`: per-venture-agreement; runbook emits MANUAL placeholder pointing at decision row.
    - `consulting_direct`: Holistika net margin = REVENUE - founder_billed_time - direct_pass_through - VENDOR_SERVICES_BILLED_billed; collaborator_share_pct = 0 unless overlay applied.
    - Overlay calculation: when `share_overlay = bd_commission_overlay`, compute `overlay_amount = holistika_net_margin × overlay_pct / 100`; add to collaborator's row; deduct from Holistika's row.
12. **`tests/test_validate_collaborator_share.py`** + **`tests/test_collaborator_share_calculate.py`**:
    - Per-pattern math tests + overlay stacking tests + CS-09 coherence tests.

### Commit 4 — Governance authoring layer (~30min)

13. **`.cursor/rules/akos-collaborator-share.mdc`**:
    - **RULE 1** (resolve share_pattern BEFORE drafting): expand decision tree to 4-base + 1-overlay path; add methodology-readiness sub-decision.
    - **RULE 3** (validator CS-01..CS-09): extend table with CS-09 overlay-base coherence; CS-08 covers all 3 new enums (pattern + overlay + methodology).
    - **RULE 5** (INFO→FAIL ramp): extend coverage requirement to ≥ 2 of the 4 base patterns exercised + ≥ 1 overlay-stacked engagement.
    - **NEW RULE 6** (overlay stacking discipline): when authoring an overlay-stacked row, the inline-ratify gate MUST surface (a) which base pattern + (b) why the overlay applies (deal-source-partner ≠ execution-operator) + (c) the overlay_pct + (d) the ratifying decision row narrative.
14. **`.cursor/skills/collaborator-share-craft/SKILL.md`**:
    - **Principle 1** (pick share_pattern FIRST): rewrite decision tree to 4-base + 1-overlay; add worked decision examples for SUEZ + bd_intro_only mini-example + a hypothetical JV-aventure mini-example.
    - **Principle 2** (5-CSV order): unchanged (atomic co-mint contract holds).
    - NEW worked-example section §3 walkthrough: SUEZ as `consulting_direct + bd_commission_overlay` math (Aïsha overlay slice + post-project continuity hours billed separately via VENDOR_SERVICES_BILLED).
15. **`SOP-PEOPLE_COLLABORATOR_SHARE_001.md`**:
    - Steps 1-3 updated for 4-base + 1-overlay resolution flow.
    - AC-HUMAN + AC-AUTOMATION acceptance unchanged in shape.
    - New step (Step 4.5) on methodology-readiness scoring at engagement-charter time.

### Commit 5 — Registries + supersede decisions + CHANGELOG (~30min)

16. **`DECISION_REGISTER.csv` supersede + new rows** (~10 row amendments):
    - SUPERSEDE rows: D-IH-86-DE (3-value enum); D-IH-86-DF (active-promotion based on wrong shape — re-promote at next gate per Q1=b); D-IH-86-EG (orchestration_broker 6/47/47 commercial-architecture); preserve D-IH-86-EH (artifact-shape — still valid); preserve D-IH-86-EI (commit atomicity — orthogonal to commercial encoding).
    - NEW rows: D-IH-86-EJ (this doctrine rewrite); D-IH-86-EK (methodology-readiness axis); D-IH-86-EL (4-base + 1-overlay shape); D-IH-86-EM (CS-09 overlay-base coherence); D-IH-86-EN (SUEZ recommercialization narrative).
17. **`COLLABORATOR_SHARE_REGISTRY.csv` SUEZ row correction**:
    - DELETE 3 prior orchestration_broker rows for ENG-SUEZ-WEBUY-2026 (Holistika 6 + Founder 47 + EFA 47).
    - RETAIN Aïsha row but flip pattern: was `deep_partner_65_35`; becomes `consulting_direct + bd_commission_overlay` with `overlay_pct = 15` (operator's *"15% of business development"* framing); status preserved as `draft` pending SUEZ commercial-close.
    - ADD 1 new row for ENG-SUEZ-WEBUY-2026: `share_pattern = consulting_direct`, `collaborator_id = HOLISTIKA-CORPORATE`, `holistika_share_pct = 100`, `collaborator_share_pct = 0`, `methodology_readiness = methodology_trained` (Holistika executes its own methodology).
    - Add `share_override_decision_id = D-IH-86-EN` to the Aïsha overlay row.
    - Net row count: ENG-SUEZ-WEBUY-2026 goes from 4 rows → 2 rows (one Holistika prime + one Aïsha overlay).
18. **`HOLISTIKA_VENDOR_SERVICES_BILLED.csv`** — re-verify SUEZ 10 rows; `consulting_direct + bd_commission_overlay` shape inherits the same default bill_mode per service class as `deep_partner_65_35`; no changes expected.
19. **`HOLISTIKA_QUALITY_FABRIC.md` §6 13th-specialty row reconfirm**:
    - Status: `charter` (was promoted to `active` at Commit 4 per D-IH-86-DF; now reverted because the worked-example #1 substrate was wrong; Stage 1 active-promotion deferred to next session when corrected SUEZ encoding satisfies Stage 1 gate cleanly).
    - linked_canonicals + ratifying_decisions amended to include EJ..EN.
20. **`PRECEDENCE.md` re-check** — 5 CSVs + doctrine + SOP rows; no path changes expected; verify decision_id columns reference EJ..EN where applicable.
21. **`CHANGELOG.md`** — comprehensive Wave R+2 entry under `[Unreleased]` documenting the full rewrite + supersede chain + corrected SUEZ encoding.

### Commit 6 — Supabase mirror DDL forward migration (~20min)

22. **`supabase/migrations/<timestamp>_i86_waveRplus2_collaborator_share_enum_amend.sql`**:
    - `ALTER TABLE compliance.collaborator_share_registry_mirror DROP CONSTRAINT IF EXISTS chk_share_pattern;`
    - `ALTER TABLE compliance.collaborator_share_registry_mirror ADD CONSTRAINT chk_share_pattern CHECK (share_pattern IN ('bd_intro_only', 'joint_venture_aventure', 'consulting_direct', 'deep_partner_65_35'));`
    - `ALTER TABLE compliance.collaborator_share_registry_mirror ADD COLUMN share_overlay TEXT NULL CHECK (share_overlay IS NULL OR share_overlay IN ('bd_commission_overlay'));`
    - `ALTER TABLE compliance.collaborator_share_registry_mirror ADD COLUMN overlay_pct NUMERIC(5,2) NULL CHECK (overlay_pct IS NULL OR (overlay_pct >= 0 AND overlay_pct <= 100));`
    - `ALTER TABLE compliance.collaborator_share_registry_mirror ADD COLUMN methodology_readiness TEXT NOT NULL DEFAULT 'methodology_trained' CHECK (methodology_readiness IN ('methodology_trained', 'methodology_in_progress', 'methodology_naive', 'methodology_not_applicable'));`
    - Rollback section documents reverse migration.
    - Filename timestamp uses 2026-05-26 ISO.

### Commit 7 — Closing-loop verification (~20min)

23. **Full validator + test suite execution**:
    - `py scripts/validate_collaborator_share.py` PASS (CS-01..CS-09; corrected SUEZ rows).
    - `py scripts/synthesis_before_tranche_check.py --check-charter <this charter>` PASS (internal_governance fire-set; baseline 3 + conditional 1 SYN-01 per J-PT secondary).
    - `py scripts/validate_decision_register.py` PASS (10 amended rows; 433 → 443).
    - `py scripts/validate_hlk.py` OVERALL PASS.
    - `py -m pytest tests/test_hlk_collaborator_share.py tests/test_validate_collaborator_share.py tests/test_collaborator_share_calculate.py -v` ALL PASS (target 75+).
    - `py scripts/synthesis_before_tranche_check.py --self-test` PASS (recursive self-test of 14th specialty still holds).
24. **`files-modified.csv`** — 30+ rows appended (per-commit attribution).
25. **`operator-scratchpad.md`** — drain entry summarising the rewrite + supersede chain + corrected SUEZ encoding + forward-pointer to next session SUEZ ship lane.

## Out of scope for this tranche (forward-charters)

- **SUEZ engagement-folder updates** beyond SHARE_REGISTRY row correction — cover-email rewrite + use-case-demo authoring + render + send pack assembly land next session per Q1=b ratify.
- **`joint_venture_aventure` first lived precedent** — no JV-aventure engagement exists yet; §3.2 carries a forward-charter placeholder pending a real instance.
- **`bd_intro_only` first lived precedent** — likewise; §3.4 carries a forward-charter placeholder. Operator's verbatim *"15% of business development"* concept materialises as overlay on existing patterns first; pure `bd_intro_only` first lived precedent waits for an actual finder's-fee-only deal.
- **14th specialty Stage 1 active-promotion** — independent timeline; not affected by this rewrite (the 14th specialty 3-of-3 worked-example gate was met cleanly at Commit 4; the 13th specialty's worked-example #1 needs re-validation post-correction in next session).
- **Investor stability dossier** — parallel non-blocking; lands at separate commit per Q-C ratify.
- **Methodology-readiness CSV register** — the axis is encoded as a SHARE_REGISTRY column at this rewrite; a separate `METHODOLOGY_READINESS_REFERENCE.csv` reference table (analogous to `COLLABORATOR_MARKET_RATE_REFERENCE`) is forward-charter for a future expansion when more lived patterns emerge.
- **Removal of orchestration_broker_thin_margin from akos/hlk_collaborator_share.py docstring narrative** — the docstring comments at L72-86 reference the removed pattern; they're updated as part of Commit 2 chassis rewrite (not a separate commit).

## Decision lineage table

| Decision ID | Purpose | Status at this tranche | Reversibility |
|:---|:---|:---|:---|
| D-IH-86-DE | 3-pattern share_pattern enum (deep_partner / orchestration_broker / custom) | SUPERSEDED by D-IH-86-EJ | one-way at register level; narrative effect reversible via re-supersede |
| D-IH-86-DF | 13th specialty Stage 1 active-promotion (based on wrong SUEZ encoding) | SUPERSEDED by D-IH-86-EN (re-promote after corrected encoding in next session) | high reversibility via successor row |
| D-IH-86-EG | SUEZ orchestration_broker 6/47/47 commercial-architecture interim-defaults | SUPERSEDED by D-IH-86-EN | high — interim rows status=draft so no signed commitment to reverse |
| D-IH-86-EH | SUEZ POC FULL KIT artifact shape (cover-mail + arch-addendum + render extension) | PRESERVED — artifact shape orthogonal to commercial encoding | medium |
| D-IH-86-EI | SUEZ commit atomicity ratification | PRESERVED — orthogonal to commercial encoding | medium |
| D-IH-86-EJ | NEW: This rewrite ratification (replace 3-pattern enum with 4-base + 1-overlay shape) | active at Commit 1 | medium — full revert via git revert + supersede |
| D-IH-86-EK | NEW: Methodology-readiness axis mint | active at Commit 1 | medium |
| D-IH-86-EL | NEW: 4-base + 1-overlay shape mint (the architectural delta) | active at Commit 1 | medium |
| D-IH-86-EM | NEW: CS-09 overlay-base coherence validator mint | active at Commit 3 | medium |
| D-IH-86-EN | NEW: SUEZ recommercialization to consulting_direct + bd_commission_overlay | active at Commit 5 | high — SHARE_REGISTRY status=draft preserves reversibility |

## Closing-loop test (SYN-09)

The tranche is verified PASS when ALL of:

1. `py scripts/validate_collaborator_share.py` PASS — all 9 checks (CS-01..CS-09); 5 CSVs with corrected SUEZ rows (2 rows for SUEZ + Aïsha overlay).
2. `py scripts/collaborator_share_calculate.py --self-test` PASS (per-pattern math branching + overlay stacking computed correctly).
3. `py scripts/synthesis_before_tranche_check.py --check-charter <this charter>` PASS (internal_governance fire-set: baseline SYN-05/07/08 + conditional SYN-01 per J-PT secondary; ≥ 3 PASS, ≤ 1 WARN/INFO acceptable per D-IH-86-ED broad-fire INFO ramp).
4. `py scripts/synthesis_before_tranche_check.py --self-test` PASS (14th specialty recursive self-test still holds).
5. `py scripts/validate_decision_register.py` PASS (10 amended rows: 5 supersede + 5 new).
6. `py scripts/validate_hlk.py` OVERALL PASS.
7. `py -m pytest tests/test_hlk_collaborator_share.py tests/test_validate_collaborator_share.py tests/test_collaborator_share_calculate.py -v` ALL PASS (target 75+ tests).
8. Grep `VALID_SHARE_PATTERNS` in `akos/hlk_collaborator_share.py` shows exactly 4 base entries (no `orchestration_broker_thin_margin`).
9. Grep `VALID_SHARE_OVERLAYS` in `akos/hlk_collaborator_share.py` shows exactly 1 entry (`bd_commission_overlay`).
10. Grep `orchestration_broker_thin_margin` in any non-superseded canonical (excluding DECISION_REGISTER supersede rows + CHANGELOG historical entries) returns ZERO results — proving full removal from active doctrine.

## Cross-references

- Pre-existing doctrine: [`COLLABORATOR_SHARE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md) (status: charter; this tranche rewrites it).
- Pre-existing Pydantic chassis: [`akos/hlk_collaborator_share.py`](../../../../akos/hlk_collaborator_share.py) (566 lines; this tranche extends to ~750+ lines).
- Pre-existing validator: [`scripts/validate_collaborator_share.py`](../../../../scripts/validate_collaborator_share.py) (CS-01..CS-08; this tranche adds CS-09).
- Pre-existing runbook: [`scripts/collaborator_share_calculate.py`](../../../../scripts/collaborator_share_calculate.py) (this tranche extends per-pattern math branching).
- Pre-existing cursor rule: [`.cursor/rules/akos-collaborator-share.mdc`](../../../../.cursor/rules/akos-collaborator-share.mdc) (RULE 1..5; this tranche adds RULE 6).
- Pre-existing skill: [`.cursor/skills/collaborator-share-craft/SKILL.md`](../../../../.cursor/skills/collaborator-share-craft/SKILL.md) (this tranche rewrites Principle 1 decision tree + adds worked-example).
- Pre-existing SOP: [`SOP-PEOPLE_COLLABORATOR_SHARE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_COLLABORATOR_SHARE_001.md) (this tranche updates Steps 1-3 + adds Step 4.5).
- Pre-existing Supabase mirror: [`supabase/migrations/20260525000000_i86_waveRplus1_commit2b_collaborator_share_mirrors.sql`](../../../../supabase/migrations/20260525000000_i86_waveRplus1_commit2b_collaborator_share_mirrors.sql) (this tranche adds forward-migration at Commit 6).
- 14th specialty parent doctrine: [`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md) (this tranche-charter runs through the 14th specialty synthesis sweep as a worked example reinforcing the 14th's coverage gates).
- Quality Fabric §6 row for 13th specialty: [`HOLISTIKA_QUALITY_FABRIC.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md) §6 (this tranche reverts status to charter pending Stage 1 re-promotion at next session).
- Prior session's wrong-encoding tranche: [`wave-r-plus-1-commit-4-suez-poc-full-kit.md`](wave-r-plus-1-commit-4-suez-poc-full-kit.md) (SUEZ POC FULL KIT; recorded the architectural-invention mistake; this tranche corrects).
- Operator-scratchpad source-grounding entries: L1577-1750+ in [`operator-scratchpad.md`](../operator-scratchpad.md) (2026-05-22 EFA-substrate drain + 2026-05-26 transcript-substrate drain).
- 2026-05-13 SUEZ customer-meeting transcript: [`docs/.../2026-suez-webuy/00-internal/source-materials/transcripts/2026-05-13-suez-customer-meeting.mp3.md`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/2026-05-13-suez-customer-meeting.mp3.md) (load-bearing substrate for SUEZ commercial-shape correction).
- Inline-ratify ratify gates: post-meta-discussion 2026-05-25 (`Q1=a_full_rewrite_now` for full rewrite scope); post-transcript 2026-05-26 (`Q1=b_doctrine_first_suez_after` for lane priority; `Q2=c_two_deep_demos` for next-session demo depth).
