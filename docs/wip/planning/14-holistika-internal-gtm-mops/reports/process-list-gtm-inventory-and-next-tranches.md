# `process_list.csv` — GTM inventory and next tranches

**Purpose:** Avoid duplicate `item_name` sprawl and align new rows with **existing** parents. Canonical file: [`docs/references/hlk/compliance/process_list.csv`](../../../../references/hlk/compliance/process_list.csv).

---

## 1. Anchor parents (already in CSV — do not recreate)

| Role | `item_id` | `item_name` (short) |
|------|-----------|---------------------|
| GTM strategy workstream | `thi_mkt_dtp_210` | Go-To-Market Strategy |
| Lead routing project | `thi_opera_dtp_288` | LEADS WEB Centralization and BD Routing |
| End-to-end lead flow | `thi_opera_dtp_289` | End-to-End Marketing Lead Flow |
| Event / analytics | `env_tech_dtp_243` | Event Taxonomy and Analytics Pipeline |

**Holistika internal GTM (Initiative 14) — merged rows:**

| `item_id` | `item_name` | `item_parent_1_id` | Notes |
|-----------|-------------|--------------------|--------|
| `holistika_gtm_dtp_001` | Holistika Internal GTM Proof Run (90-Day) | `thi_mkt_dtp_210` | Process |
| `holistika_gtm_dtp_002` | Agency Partner Proposal Intake and Fit Assessment | `thi_mkt_dtp_210` | Process |
| `holistika_gtm_dtp_003` | Inbound Response SLA (Holistika Services) | `thi_opera_dtp_289` | Process |

**Trello-derived clusters (`gtm_cl_*`, `gtm_ws_*`):** Large set under `gtm_ws_gtm_entity`, `gtm_ws_madeira_*`, etc. — **reference for scope**, not a prompt to duplicate Initiative 14 rows.

---

## 2. Enrichment strategy (not “more top-level processes”)

**Prefer:**

1. **Task**-level children under `holistika_gtm_dtp_001`–`003` when a checklist step needs a **unique** `item_id` for RACI or tooling.
2. **Instructions** / **SOP** depth before new rows.
3. New **process** rows only when a **distinct lifecycle** or owner boundary exists (operator judgment).

---

## 3. Candidate next tranche (operator approval before merge)

**Status:** Proposal only — **not** in `process_list.csv` until approved and validated.

### 3a. Research-team themes (2026 — candidate **processes**, not merged)

These mirror the unified Initiative 14 plan: **themes for inventory** only. Real `item_id` / parents must match CSV conventions (often under `thi_mkt_dtp_210` or `thi_opera_dtp_289`). **SOP-META:** CSV tranche before net-new v3.0 SOPs for new IDs.

| Theme | Intent | Suggested parent (draft) | Notes |
|-------|--------|--------------------------|--------|
| Lead scoring and SLA routing | Firmographic + behavioral scoring; route high-intent to BD | `thi_mkt_dtp_210` or `holistika_gtm_dtp_001` | Any **stricter** response time than [D-GTM-C1](../decision-log.md) (4 business hours) needs a **new decision-log row** |
| Multi-touch attribution / revenue facts | SQL-friendly facts in Postgres; fractional models later | `env_tech_dtp_243` + `holistika_gtm_dtp_001` | Tie to Wave E / [`event-attribution-blueprint-reference.md`](event-attribution-blueprint-reference.md) |
| Micro-events (exec roundtables, dinners) | Curated small-format events vs generic webinars | `thi_mkt_dtp_210` | Ops runbook; may reuse event taxonomy rows |
| Silver-medalist nurturing | Recycle near-miss leads or candidates | `holistika_gtm_dtp_001` or HR-adjacent parent | Split **GTM leads** vs **hiring** scope in tranche design |

**Sales / CS / partnership gaps** (existing plan): continue to use task children under `holistika_gtm_dtp_001`–`003` where possible before new process rows.

Suggested **task** children (examples; adjust names for global `item_name` uniqueness):

| Proposed `item_id` | `item_name` | `item_parent_1_id` | `item_granularity` | Rationale |
|--------------------|-------------|--------------------|--------------------|-----------|
| `holistika_gtm_task_001` | GTM proof run — Week 1 baseline metrics capture | `holistika_gtm_dtp_001` | task | Executable unit for 90-day proof |
| `holistika_gtm_task_002` | Partner intake — Legal screening gate | `holistika_gtm_dtp_002` | task | NDAs / DPAs before technical review |
| `holistika_gtm_task_003` | Inbound SLA — Tool failure escalation path | `holistika_gtm_dtp_003` | task | Distinct from weekly metrics review |

**Merge procedure:** Add rows to `candidates/process_list_tranche_holistika_internal.csv` (or new candidate file), run `py scripts/merge_process_list_tranche.py`, then `py scripts/validate_hlk.py` and update [`USER_GUIDE.md`](../../../../USER_GUIDE.md) HLK counts if required by governance.

---

## 4. What we are **not** doing here

- **No** parallel “GTM Strategy” workstream — `thi_mkt_dtp_210` remains parent.
- **No** duplicate SLA process — `holistika_gtm_dtp_003` is the Holistika-services SLA; generic marketing ops stay under existing MKT children.
- **No** new MADEIRA `gtm_cl_*` rows from this initiative without Trello/source traceability.

---

## 5. Verification

```bash
py scripts/validate_hlk.py
rg "holistika_gtm" docs/references/hlk/compliance/process_list.csv
```
