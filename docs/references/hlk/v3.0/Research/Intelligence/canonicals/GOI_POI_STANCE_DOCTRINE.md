---
language: en
status: active
canonical: true
role_owner: Research Analyst + Compliance
classification: way_of_working + selling_point
intellectual_kind: doctrine_canonical
ssot: true
authored: 2026-05-13
last_review: 2026-05-13
---

# GOI/POI STANCE DOCTRINE — Allies / Neutrals / Enemies

> Authored I70 P8.5 (§8.17) per `D-IH-70-AD` (operator ratification 2026-05-13). Codifies the operator's v2.7 intelligence-ops framing as a v3.1 governance dimension on `GOI_POI_REGISTER.csv`. This is the v3.1 methodology versioning event continuing from D-IH-70-Z (Marketing M3 schema extension) + D-IH-70-AA (People area restructure) — same chat, same day, same hard-remove + extend pattern.

## 1. Why this canonical exists

The operator's v2.7 corpus (Research & Logic legacy) framed external relationships through a single behavioural axis: **how we engage based on whether the counterpart is on our side, neutral, or against us**. That axis was prose-only in v2.7. v3.0 captured `distance_band` (proximity in the social graph) but not stance (posture of the relationship). v3.1 adds `stance` as a first-class column on `GOI_POI_REGISTER.csv` so every existing IntelligenceOps query can score relationship posture independently of distance.

Original v2.7 framing (operator quote, ratification 2026-05-13):

> *"to the allies, you give them free — or very discounted, or price-diluted — added value; to the neutrals, you give value × revenue in the best way you can / no beta / no alpha; to the enemies, you never let them pay you, and if they do, make the project valuable enough to warrant sharing our capabilities."*

The doctrine answers a different question than `distance_band`:

| dimension | question it answers | source |
|:---|:---|:---|
| `distance_band` (N1-N4) | how far is this entity from us in the social graph? | I31 P2.2 (D-IH-31-G) |
| **`stance`** (ally/neutral/enemy/unknown) | **what is the posture of the relationship — for us, against us, or indifferent?** | **I70 P8.5 (D-IH-70-AD)** |
| `related_party` (true/false/empty) | does SOC disclosure require an explicit conflict-of-interest flag? | P13.4 (D-W13-D) |

A row can be N1-distance + ally (close + on our side; e.g. EFA partner-lead), or N1-distance + enemy (close + against us; e.g. a former collaborator who became a competitive intelligence target), or N4-distance + neutral (remote + indifferent; e.g. a benchmark research entity). Each axis is independent.

## 2. The four stance values

### 2.1 `ally`

The counterpart is on our side. Definition: their success amplifies ours; their failure degrades ours; the relationship is mutually-reinforcing.

**Engagement-posture rule.** Free, discounted, or price-diluted added value. Beta/alpha access permitted. Sharing of methodology and capabilities is the default; we hold back only what protects the brand-positioning thesis (BRAND_DISCIPLINE_ONTOLOGY.md).

**Concrete examples (current rows).**
- `GOI-PRT-EFA-2026` + `POI-PRT-EFA-LEAD-2026` — partner; co-branded; EFA's success on the SUEZ engagement = our first-customer landing.
- `GOI-ADV-ENTITY-2026` + child POI rows — third-party adviser firm; our successful ENISA pack lands them a positive reference.
- `GOI-LEG-CONST-2026` — Spanish legal counsel; our successful incorporation is their billable repeat-engagement.
- `GOI-CUS-ASES-2026` — family-owned client (related_party=true); operator's family success = operator's success.

### 2.2 `neutral`

The counterpart is indifferent. Definition: a transactional relationship; their success and ours are decoupled; the engagement is value × revenue with neither side optimising for the other's growth.

**Engagement-posture rule.** Value × revenue in the best way we can. **No beta access; no alpha access.** No early-feature drops. We deliver the contracted scope at the contracted SLA tier (SLA_MATRIX.md). We do not over-invest narrative or methodology coaching beyond what the engagement specifies.

**Concrete examples (current rows).**
- `GOI-CUS-SUEZ-2026` + `POI-CUS-SUEZ-LEAD-2026` — first-customer SaaS-grade engagement; bridged through partner; transactional posture per Tier 2 SLA.
- `GOI-BNK-INC-2026` + `POI-BNK-DESK-LEAD-2026` — constitution-desk bank; commercial supplier of incorporation services; transactional.
- `GOI-INV-ENISA-2026` — Spanish state-backed startup investor; uniform-criteria public lender; we are a candidate, not a special case.
- `GOI-SUP-SHGPU-2026` — GPU/cloud supplier candidate in negotiation; could ramp to ally if cobranding lands or to enemy if predatory pricing emerges.

### 2.3 `enemy`

The counterpart is against us (actively or structurally). Definition: their success degrades ours; they are an audit subject of our IntelligenceOps practice; engaging them costs more than their revenue contribution can repay.

**Engagement-posture rule.** **Never let them pay you.** If they do (e.g. via a procurement channel that masks identity), the project must be valuable enough to warrant sharing our capabilities — i.e. the dollar amount must justify the risk that our deliverable becomes their training data. Default: refuse the engagement; document the entity in `GOI_POI_REGISTER.csv` for future IntelligenceOps queries.

**Concrete examples.**
- *(none in current corpus; competitor-intelligence-target rows will land in I72 IntelligenceOps register expansion.)*

### 2.4 `unknown`

Default for new rows pending operator ratification. Empty string is also accepted as backwards-compatible default for legacy rows that pre-date v3.1.

## 3. Stance vs distance: independence rule

Stance and distance are **orthogonal**. The operator's working surface frequently shifts one without the other:

- Distance can shrink (N3 → N1) when a chain of warm intros lands; stance does not change automatically.
- Stance can flip (neutral → enemy) when a counterpart breaches confidentiality; distance does not change.
- A new ally row often starts at N3-N4 distance; the relationship-posture is established first, the proximity follows.

Validators in `scripts/validate_goipoi_register.py` check each axis independently. Cross-axis sanity rules (e.g., "an N2 ally must declare bridge_via to a closer ally") are deferred to I72 IntelligenceOps register expansion if usage signals demand them.

## 4. Workflow: assigning + updating stance

### 4.1 New row: assign at row-creation time

Operator (or agent on operator's behalf with explicit ratify) sets stance to one of {ally, neutral, enemy} at row-creation time. `unknown` is the default for rows where stance has not yet been ratified.

### 4.2 Existing row: re-assess at quarterly cadence

Same cadence as `distance_band` re-assessment per `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` §4.X. A stance change is a recordable event in `DECISION_REGISTER.csv` if it crosses the ally↔neutral or neutral↔enemy boundary.

### 4.3 Engagement-posture cross-check

Before any new commercial proposal lands, the operator (or PMO on operator's behalf) verifies the counterpart's stance row is current. The proposal's pricing/scope/IP-sharing posture is derived from §2.1-§2.3 above:

- Ally: free/discounted/share-capabilities posture default.
- Neutral: value × revenue posture default; SLA_MATRIX.md tier-mapping applies.
- Enemy: refuse-or-premium-priced-with-capability-sharing-disclosure posture.

## 5. Schema cross-references

| Concern | Lives in |
|:---|:---|
| Stance column SSOT | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv` (column `stance`) |
| Pydantic FIELDNAMES | `akos/hlk_goipoi_csv.py` (last entry in `GOIPOI_REGISTER_FIELDNAMES`) |
| Validator | `scripts/validate_goipoi_register.py` (constant `STANCES`) |
| Mirror DDL | `supabase/migrations/20260513150000_i70_p85_goipoi_stance_and_class_enum_extension.sql` (CHECK constraint `goipoi_register_mirror_stance_check`) |
| Doctrine (this doc) | `docs/references/hlk/v3.0/Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md` |

## 6. Ratification log

| date | event | decision_id | summary |
|:---|:---|:---|:---|
| 2026-05-13 | Stance column landing as v3.1 schema extension | `D-IH-70-AD` | Operator-ratified single-column design (no bidirectional split for the v3.1 cycle); enum `ally/neutral/enemy/unknown`; backwards-compatible empty default; engagement-posture rules codified in §2 of this doc. |

## 7. Future evolution (deferred to I72+)

- **Bidirectional stance** (their-stance-toward-us vs our-stance-toward-them) when concrete divergence cases land.
- **Stance-distance cross-axis sanity rules** in the validator if operator's quarterly re-assessment surfaces patterns that warrant enforcement.
- **Engagement-posture rule machine-execution**: a future SOP could derive proposal-posture defaults from the stance column and the SLA tier mapping automatically.

## 8. Cross-references

- `D-IH-70-AC` (P8.5 GOI class regression hunt — sister event)
- `D-IH-70-AD` (this doctrine's ratifying decision)
- `D-IH-70-Z` (P8.2 Marketing M3 + sub_area/status schema extension — first v3.1 methodology versioning event)
- `D-IH-70-AA` (P8.3 People area restructure — sister versioning event)
- `D-IH-31-G` (I31 P2.2 distance_band — orthogonal dimension; established 2026-04-30)
- `D-W13-D` (P13.4 related_party — orthogonal disclosure flag; established 2026-05-11)
- `INTELLIGENCE_DISCIPLINE_CHARTER.md` — parent canonical (Research/Intelligence area)
- `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` — sister SOP governing GOI/POI maintenance discipline
- `GOI_POI_REGISTER.csv` — target dimension CSV
- v2.7 Research & Logic corpus — historical source of the ally/neutral/enemy framing
