---
intellectual_kind: research_baseline
parent_initiative: INIT-OPENCLAW_AKOS-93
authored: 2026-06-05
status: active
language: en
sweep_id: area-completeness-2026-06-05
---

# Baseline state — area completeness + full-picture regression + topography (2026-06-05)

> Steps 1–3 of the operator's instruction: **update area-completeness parameters →
> regression over the full picture → per-area topography**. This is the *measured
> starting point* the definitional regression (Step 6) is run against. Evidence only;
> no canonical edits here.

## Step 1 — Area-completeness parameters refreshed (the bar as it stands)

`py scripts/validate_area_completeness.py --matrix` (sweep `area-completeness-2026-06-05`,
trigger `on_demand`). The bar is the **14-component** set AREA-01..14 (`SRC-AREA-INT-01`),
scored `pass / partial / gap / skip / blocked` (`SRC-AREA-INT-02`), score = pass ÷ scored.

| Area | pass | partial | gap | skip | score | At bar (≥88%)? |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Finance** | 12 | 2 | 0 | 0 | **93%** | ✅ |
| **Data** | 11 | 2 | 0 | 1 | **92%** | ✅ (closed I93) |
| People | 10 | 1 | 2 | 1 | 81% | ✗ |
| Marketing | 9 | 2 | 2 | 1 | 77% | ✗ |
| Operations | 8 | 2 | 3 | 1 | 69% | ✗ |
| Research | 7 | 3 | 3 | 1 | 65% | ✗ |
| Tech | 7 | 3 | 3 | 1 | 65% | ✗ |

**Open gaps by area** (the zero-backlog target set):

- **People** — AREA-02 area-charter (high; accept-as-canon candidate per gap tracker), AREA-13 README.
- **Marketing** — AREA-11 rule+skill, AREA-13 README; partials on AREA-09 (0/56 paired), AREA-12.
- **Operations** — AREA-03 discipline-charter, AREA-11 rule+skill, AREA-13 README; partials AREA-09 (0/105).
- **Research** — AREA-02 charter, AREA-03 discipline, AREA-13 README; partials AREA-08, AREA-09 (0/71), AREA-12.
- **Tech** — AREA-02 charter, AREA-03 discipline, AREA-13 README; partials AREA-09 (0/118), AREA-11, AREA-12.

**Parameter note (candidate finding F-PARAM-1):** the score is a **flat ratio** — all 14
components weighted equally, `skip` excluded from the denominator. A high-severity
AREA-02 charter gap costs the same one point as a low-severity AREA-11 rule+skill gap.
This is the single most consequential "parameter" the definitional regression interrogates
(see master-synthesis §D-threshold).

## Step 2 — Regression over the full picture

Two complementary sweeps (TIA safety-net + value layer per `SRC-AREA-INT-27`):

**(a) Intent-ranked regression** — `py scripts/intent_ranked_regression.py --rank`
(ICS = 3·intent + 2·time + 2·risk + 1·detection_gap; max 40):

| Rank | Surface | ICS | Verdict relevant to this research |
|:---:|:---|:---:|:---|
| 1 | S-06 Legal/fiscal existence artifacts | 36 ! | green (Finance F2b tax calendar) |
| 2 | S-04 FINOPS commercial substrate | 35 ! | green (F3 FINOPS-SPINE) |
| 3 | S-01 Governance SSOT integrity | 34 | green (validate_hlk PASS) |
| 4 | S-05 Release-gate composite | 32 | green |
| 5 | S-12 Schema drift (CSV/enum/DDL) | 32 | green (area_governance enum fixed) |
| **6** | **S-02 Area-completeness (7 areas)** | **31** | **the surface this research targets** |
| 7 | S-03 Structural regression | 29 | green |
| 8–12 | operator/brand/index/eval/runtime | 24–27 | n/a this cycle |

**(b) Mechanical safety net** — `validate_hlk.py` OVERALL PASS; `validate_research_action.py`
self-test PASS; area matrix deterministic across repeated probes. No new regressions
attributable to this session's diffs (all edits are additive evidence + the ledger).

**Full-picture verdict:** the existence-critical surfaces (S-06, S-04, S-01) are green;
**S-02 area-completeness is the highest-ICS surface with material open work** (5 areas
below bar). That is *why* re-examining the area definition before the 5-area sweep is the
correct sequencing — fixing the ruler before measuring five more things with it.

## Step 3 — Per-area topography

Structural mass per O5-1 area (md + csv files; sub-area folders; paired processes from the
AREA-09 probe). "Topography" = how built-out each area's tree actually is, independent of score.

| Area | md | csv | sub-areas | processes | Shape read |
|:---|:---:|:---:|:---:|:---:|:---|
| **People** | 103 | 47 | 9 | 67 | Densest — hosts Compliance/Legal/Ethics + all cross-area canonical CSVs; the "discipline of disciplines" |
| **Marketing** | 56 | 5 | 8 | 56 | Broad sub-area spread (Brand/Reach/Resonance); brand canon heavy |
| **Operations** | 52 | 5 | 5 | 105 | Highest process count (PMO/RevOps/SMO/IntelligenceOps); thin on discipline charters |
| **Data** | 24 | 5 | 4 | 17 | Lean but fully governed (Architecture/Governance); the I93 worked example |
| **Tech** | 22 | 0 | 4 | 118 | Highest process count, **zero area-local CSVs**, no charter — split across `Tech/` + `Envoy Tech Lab/` |
| **Envoy Tech Lab** | 18 | 2 | 5 | — | Second physical Tech home — the boundary ambiguity flagged below |
| **Finance** | 9 | 3 | 4 | 17 | Smallest but fully governed (F0–F3); newest worked example |
| **Research** | 9 | 1 | 8 | 71 | Many sub-areas, thin canon — charter + discipline gaps |

**Topography findings:**

- **F-TOPO-1 (boundary ambiguity, Tech).** Tech occupies **two physical roots** — `Tech/`
  and `Envoy Tech Lab/`. The matrix scores `Tech` only; `Envoy Tech Lab` mass is invisible
  to AREA-01. This is the exact failure DDD's bounded context (`SRC-AREA-EXT-24`) and Team
  Topologies' boundary clarity (`SRC-AREA-EXT-29`) warn against: one area, two unreconciled
  models. Feeds `def-area`.
- **F-TOPO-2 (mass ≠ maturity).** Operations (52 md / 105 processes) and Tech (118 processes)
  are the **most built-out by mass yet lowest-scoring** (69% / 65%). Conversely Finance
  (9 md) scores 93%. Confirms the bar measures *governance shape*, not *content volume* —
  consistent with capability-maturity being orthogonal to size (`SRC-AREA-EXT-07`).
- **F-TOPO-3 (process-pairing cliff).** AREA-09 paired-SOP-runbook is `partial` for **every**
  area (0 paired in Data/Finance up to 0/118 in Tech). The bar counts the component present
  but never `pass` — a systemic ceiling that caps every area near ~93% regardless of effort.
  Feeds `def-components` + `def-threshold`.

## Cross-references

- Ledger: [`source-ledger.csv`](source-ledger.csv) (117 sources)
- Subject: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md)
- Forward map: [`area-governance-gap-tracker-2026-06-05.csv`](../../planning/93-data-area-foundation-and-governance/_trackers/area-governance-gap-tracker-2026-06-05.csv)
- Next: [`master-synthesis.md`](master-synthesis.md) (the definitional regression + option set)
