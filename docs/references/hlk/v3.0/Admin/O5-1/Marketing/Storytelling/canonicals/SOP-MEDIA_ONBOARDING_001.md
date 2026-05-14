---
language: en
status: review
canonical: true
role_owner: Brand & Narrative Manager
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: Brand & Narrative Manager
last_review_decision_id: D-IH-72-J
methodology_version_at_review: v3.0
companion_to:
  - STORYTELLING_AREA_CHARTER.md
  - ../../../Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
  - ../../../Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md
---

# SOP-MEDIA_ONBOARDING_001 — Media counterparty onboarding contract

> Authored I72 P6 per `D-IH-72-A` (P0 charter) + `D-IH-72-H` (sibling INTELLIGENCEOPS_REGISTER canonical) + `D-IH-72-J` (media-counterparty-onboarding = Storytelling charter cross-link + IntelligenceOps register row both). Codifies how Holistika onboards a media counterparty (journalist, podcaster, conference programme committee) and tracks the relationship for systematic story-yield + accurate-quote outcomes. Cross-link from `INTELLIGENCEOPS_REGISTER.csv` row with `target_class=media`.

## 1. Purpose

Establish a uniform onboarding contract for media counterparties so Holistika:

1. **Defaults to acknowledgment-then-vet**: per the existing PERSONA-PRESS pattern (`Brand Manager handles; Founder vetoes if topic is sensitive`).
2. **Builds reliability incrementally**: starts at C (default for unknown media counterparty); upgrades to B after 2+ accurate quotes published.
3. **Generates story-yield artifacts**: every onboarded media counterparty produces a per-engagement record under `docs/wip/research/media/<slug>-engagement-record.md`.
4. **Cross-links to Storytelling charter**: ensures the story-yield discipline of `STORYTELLING_AREA_CHARTER.md` informs and is informed by media engagement records.

## 2. Scope

In scope:
- Any target in `INTELLIGENCEOPS_REGISTER.csv` with `target_class=media`.
- Any new media counterparty inbound (PR pitch, interview request) or outbound (Holistika-initiated story placement).
- Cross-area relationships: Brand Manager owns; Founder vetoes sensitive topics; Storytelling charter consumes outputs.

Out of scope:
- Per-story content authoring (covered by Storytelling area canonicals).
- Brand-voice register checks (covered by Brand area + I71 P1 Pack A1 brand-voice register).
- Press-release authoring (covered by future PR SOP — not in I72 scope).

## 3. Inputs

- The media counterparty's inbound message (PR pitch, interview request) OR Holistika-initiated outreach context.
- The media counterparty's GOI row in `GOI_POI_REGISTER.csv` (when minted; new counterparties may arrive without a GOI row — onboarding cycle creates one).
- The Storytelling area's current case-study pipeline (`STORYTELLING_AREA_CHARTER.md`).
- The PERSONA-PRESS persona row in `PERSONA_REGISTRY.csv`.

## 4. Steps

### 4.1 Acknowledgment (T+0 to T+48h)

Brand Manager acknowledges the inbound (or initiates outreach):

1. **Inbound case**: send acknowledgment per PERSONA-PRESS playbook within 48h; ask 2-3 qualifying questions (topic specificity, timeline, publication context, reach signal).
2. **Outbound case**: send personalized outreach citing specific past work the journalist/podcaster covered; propose 2-3 angles relevant to current Storytelling pipeline.

### 4.2 Vetting (T+48h to T+7d)

1. **Topic sensitivity check**: classify inbound as routine / nuanced / sensitive. Sensitive topics escalate to Founder per PERSONA-PRESS gating.
2. **Reach + reliability signal scan**: lookup the publication / podcast / event in publicly available editorial-quality + audience-reach signals. Flag low-reach + low-reliability sources for de-prioritization.
3. **Cross-area conflict check**: does the media counterparty have prior contact with a competitor or with any GOI/POI marked `enemy` per `GOI_POI_STANCE_DOCTRINE.md`? If yes, escalate.

### 4.3 Onboarding (T+7d to T+14d)

1. **GOI row mint**: create or update the media counterparty's GOI row in `GOI_POI_REGISTER.csv` with `class=media` per D-IH-70-AC enum. Distance band starts at N3 (most media counterparties); upgrades when collaboration solidifies.
2. **INTELLIGENCEOPS_REGISTER row mint**: append a row with `target_class=media`, `cadence=event_triggered`, `source_type=HUMINT`, `reliability=C` (default). Output artifact path = `docs/wip/research/media/<slug>-engagement-record.md`.
3. **Engagement record draft**: create the engagement record artifact with onboarding context, qualifying answers, and intended next interaction.

### 4.4 First interaction (T+14d to T+30d)

1. **Conduct interview / send case-study material / fulfill quote request** per Brand Manager judgment.
2. **Update engagement record** with interaction transcript or summary + Founder vetoes recorded if any.
3. **Reliability tracking**: when the publication lands, compare published quotes/material to what Holistika provided. If accurate, increment a per-counterparty accurate-quote counter; at 2+ accurate quotes upgrade `reliability` from `C` to `B`.

### 4.5 Ongoing relationship management (per cadence)

The cadence stays `event_triggered` (fires when journalist reaches out OR Holistika has a new story to pitch). At each event-trigger:

1. Update the engagement record with the new interaction.
2. Refresh the INTELLIGENCEOPS_REGISTER row's audit-trail + reliability cells.
3. Cross-feed the Storytelling charter: any case-study yield from the media interaction informs `STORYTELLING_AREA_CHARTER.md` §5 process catalog.

## 5. Outputs

- Updated/created `GOI_POI_REGISTER.csv` row for the media counterparty.
- Updated/created `INTELLIGENCEOPS_REGISTER.csv` row.
- Per-engagement record under `docs/wip/research/media/<slug>-engagement-record.md`.
- 0+ case-study yield candidates for Storytelling charter.

## 6. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **`acceptance_criteria_human`**: Brand Manager runs §4.1-4.5 manually using only this SOP body; engagement record auditable; reliability progression documented and reviewable.
- **`acceptance_criteria_automation`**: `validate_intelligenceops_register.py` PASS on the updated row; `validate_hlk.py` PASS on GOI_POI_REGISTER changes.

## 7. Failure modes

- **Counterparty turns out to be off-brand or sensationalist**: deprioritize; document in engagement record; mark GOI row stance = `enemy` per `GOI_POI_STANCE_DOCTRINE.md` if relationship has gone adversarial.
- **Quote misrepresentation in published piece**: do NOT increment accurate-quote counter; flag for Founder review; consider stance reassessment.
- **High-reach low-reliability counterparty pitches**: invoke Founder veto pathway; default to acknowledgment-defer.
- **Cross-area conflict surfaces** (counterparty has prior favorable coverage of an `enemy` GOI): defer engagement; escalate to Founder.

## 8. Cross-references

- Parent area charter: [`STORYTELLING_AREA_CHARTER.md`](STORYTELLING_AREA_CHARTER.md) §5 (process catalog) + §3 (sub-area boundary).
- Sister SOP: [`SOP-REGULATOR_RELATIONSHIP_001.md`](../../../Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md) — generic intelligence-relationship pattern (regulator example).
- Persona row: PERSONA-PRESS in `PERSONA_REGISTRY.csv` (existing routing baseline).
- Doctrine: [`GOI_POI_STANCE_DOCTRINE.md`](../../../Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md) (D-IH-70-AD).
- Canonicals: [`dimensions/INTELLIGENCEOPS_REGISTER.csv`](../../../Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv), [`GOI_POI_REGISTER.csv`](../../../People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv).
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 1 + 3 + 4 + 5.
- Decisions: `D-IH-72-H` (sibling canonical), `D-IH-72-J` (this SOP + cross-link charter), `D-IH-70-AC` (forward-charter context), `D-IH-72-Q` (cadence taxonomy).
