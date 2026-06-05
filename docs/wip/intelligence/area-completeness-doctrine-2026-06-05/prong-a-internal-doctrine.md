---
intellectual_kind: research_prong
prong: A
topic_cluster: internal_area_doctrine
authored: 2026-06-05
status: active
language: en
---

# Prong A — How WE define "area" and "completeness" today

> Internal evidence-sweep (`SRC-AREA-INT-01..55`). What the repo already says, so the
> external prongs measure a *real* gap rather than a strawman.

## A.1 What "an area" is, in current doctrine

The current definition is **structural-organisational**, not boundary-theoretic. An O5-1
area is "a folder tree under `Admin/O5-1/` with role/sub-area structure" (`SRC-AREA-INT-01`
AREA-01) whose membership is defined by **role roots** in `baseline_organisation.csv`
(`SRC-AREA-INT-12`, AREA-05) and **processes** in `process_list.csv` (`SRC-AREA-INT-13`,
AREA-04). The seven scored areas are frozen in code (`SRC-AREA-INT-02`): Data, Tech,
Finance, Marketing, Operations, People, Research. People mints the *pattern*
(`pattern_area_buildout`, `SRC-AREA-INT-14`); each area inherits the shape (`SRC-AREA-INT-10`).

**Gap:** the doctrine never states a **boundary criterion** — *why* these seven, *where* one
ends, *when* a sub-area (e.g. Brand inside Marketing; Envoy Tech Lab inside Tech) should be
its own area. The only worked boundary precedent is `PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY.md`
(`SRC-AREA-INT-54`) — a single sub-area split, not a general rule.

## A.2 What "completeness" means today

Completeness = **a flat 14-component checklist** (`SRC-AREA-INT-01`) scored by a conservative
heuristic (`SRC-AREA-INT-03`) into `pass/partial/gap/skip/blocked` (`SRC-AREA-INT-02`). The
matrix score is `pass ÷ scored`; the I93 reference bar is **88% + zero unexpected gaps**
(`SRC-AREA-INT-43`, `SRC-AREA-INT-45`). Closure tolerates residual partials via
PASS-WITH-FOLLOWUP (`SRC-AREA-INT-26`) — Data closed at 92% (`SRC-AREA-INT-40`).

**Three structural observations:**

1. **Flat count, no weights.** Every component is 1 point. The discipline has *no* notion
   that AREA-02 (charter) might matter more than AREA-11 (rule+skill). This is the most
   visible delta from every external maturity model (Prong B).
2. **We already weight elsewhere.** The repo *has* value-weighting machinery —
   `INTENT_RANKED_REGRESSION` ICS (`SRC-AREA-INT-27`) and `confidence_levels.md`
   Safe/Euclid/Keter (`SRC-AREA-INT-20`) — but area completeness does not use it. There is
   internal precedent to weight; it simply has not been applied here.
3. **Sibling bars are richer.** UAT (11 sections + verdict, `SRC-AREA-INT-22`), inter-wave
   (13 dims, `SRC-AREA-INT-23`), synthesis-before-tranche (10 dims with **per-class fire-sets**,
   `SRC-AREA-INT-25`) all already do **conditional dimensions** — a dimension fires only for
   relevant tranche classes. Area completeness fires all 14 for all 7 areas flatly.

## A.3 The alternative lens already in the repo

I88's **10-pillar Holistika ReOps lens** (`SRC-AREA-INT-49`, `SRC-AREA-INT-50`) — Boulton's
8 ops pillars + Brand + UX — is a *second*, competing decomposition of "what an area must
have." It is richer on **outcome/value** (pillar dimensions like Strategy, Brand, UX) where
the 14-component bar is richer on **artifact presence** (charter, README, CSV, mirror). The
two have never been reconciled. This is the strongest internal signal that the 14 components
are an *artifact-completeness* checklist, not a *capability/value-completeness* model.

## A.4 What Prong A establishes for the decision

- `def-area`: current boundary = "folder + roles + processes"; **no boundary criterion** exists.
- `def-complete`: current = flat artifact checklist; **value/outcome axis absent**.
- `def-components`: 14 artifact-presence checks; candidate missing dimensions already implied
  by sibling disciplines (data-quality `SRC-AREA-INT-30`, reliability `SRC-AREA-INT-31`,
  UX `SRC-AREA-INT-33`) and by the 10-pillar lens.
- `def-threshold`: 88% flat + PWF; the AREA-09 pairing-cliff (`F-TOPO-3`) caps everyone.
