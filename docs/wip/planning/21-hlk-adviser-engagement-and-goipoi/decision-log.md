# Initiative 21 — Decision log

## D-CH-1 — Handoff shape

**Question:** Single unified handoff package vs per-discipline split vs unified-with-sections.

**Decision:** **Option C** — single unified package owned by Legal Counsel (today) with **explicit per-discipline sections** (Legal / Fiscal / IP / Banking / Certification / Notary), **plus** the External Adviser Engagement plane (ADVOPS) that establishes per-discipline ownership in `process_list.csv` and `ADVISER_ENGAGEMENT_DISCIPLINES.csv`. New disciplines extend the plane without forking the package.

**Rationale:** Operator wanted invariance and scalability like MKTOPS/FINOPS/OPS/TECHOPS. One reading entrypoint for advisers; deterministic per-row ownership via the disciplines CSV; future disciplines or programs reuse the structure without contamination.

## D-CH-2 — Privacy / redaction posture

**Question:** Already-pushed transcripts contain real names and private-org references on a public repo. Redact in place vs `git filter-repo` vs private submodule vs stay public.

**Decision:** **Redact-forward** via the GOI/POI dimension. Raw transcripts already in commit history accepted as-is; **future** commits use redacted markdown that references `POI-*`/`GOI-*` only. **Full history rewrite (`git filter-repo` + force-push) deferred** with an explicit re-evaluation trigger.

**Re-evaluation trigger:** A `restricted` POI is later identified in commit history without a corresponding row in `GOI_POI_REGISTER.csv` flagged for public reference, **or** counsel issues a privilege-protection demand.

## D-CH-3 — GOI/POI canonical authority

**Decision:** `docs/references/hlk/compliance/GOI_POI_REGISTER.csv` is SSOT. Markdown views (e.g. PMO hub stakeholder index, vault fact pattern) become **derived/manual** views that reference `ref_id`s. Mirror lives in `compliance.goipoi_register_mirror` (RLS deny `anon`/`authenticated`, `service_role` only).

**Rationale:** DAMA-pure SSOT, validator-gated, deterministic substitution.

## D-CH-4 — Open questions canonical authority

**Decision:** `ADVISER_OPEN_QUESTIONS.csv` is SSOT; vault `FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md` becomes a derived human view (manual rendering acceptable in P4; an optional `scripts/render_adviser_handoff.py` is a future improvement, not a P4 deliverable).

**Rationale:** Single-source for question state, owners, evidence, GOI/POI cross-references.

## D-CH-5 — Filed instruments canonical authority

**Decision:** `FOUNDER_FILED_INSTRUMENTS.csv` is SSOT; vault `FOUNDER_FILED_INSTRUMENT_REGISTER.md` becomes a derived view.

**Rationale:** Same DAMA reasoning; ties counsel handoff to validated structured data.

## D-CH-6 — ID schemes

**Decision:**

- POI: `POI-<class3>-<slug>-<YYYY>` (e.g. `POI-BNK-DESK-LEAD-2026`).
- GOI: `GOI-<class3>-<slug>-<YYYY>` (e.g. `GOI-ADV-ENTITY-2026`).
- Open questions: `Q-<DISC3>-<NNN>` per program (e.g. `Q-LEG-001`, `Q-FIS-001`).
- Filed instruments: `INST-<DISC3>-<slug>-<YYYY>` (e.g. `INST-LEG-ESCRITURA-2026`).

**Rationale:** Stable, sortable, human-readable, easily greppable; aligns with `process_list.csv` slug discipline.

## D-CH-7 — Sensitivity bands and sharing labels

**Decision:** Bands `public` / `internal` / `confidential` / `restricted` mapped to sharing labels (`counsel_ok`, `internal_only`, `counsel_and_named_counterparty`). Public entities (`is_public_entity = true`) skip obfuscation.

## D-CH-8 — Engagement-keyed registers (invariance for scale)

**Decision:** All new registers include `program_id` (e.g. `PRJ-HOL-FOUNDING-2026`) so future engagements reuse the same structures without contamination. New disciplines or programs do **not** require new schemas — only new rows.

**Rationale:** Matches the FINOPS counterparty register pattern (one CSV, many counterparties); avoids the trap of one-table-per-engagement.
