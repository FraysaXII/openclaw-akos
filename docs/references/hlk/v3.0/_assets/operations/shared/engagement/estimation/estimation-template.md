---
status: active
classification: canonical
access_level: 4
language: en
register: external
artifact_kind: estimation_template
role_owner: Project Manager
area: Operations
entity: Holistika
governance:
  - SOP-ENG_ESTIMATION_DISCIPLINE_001
last_review: 2026-05-10
---

# Engagement estimation worksheet template

> Copy this file's example `scope.yaml` block into the engagement's working space (`docs/wip/intelligence/<YYYY-MM-DD>-<slug>/scope.yaml`) and fill it in. Then run:
>
> ```
> py scripts/estimate_engagement.py \
>     --scope docs/wip/intelligence/<slug>/scope.yaml \
>     --out docs/wip/intelligence/<slug>/commercial-schedule.md
> ```

## 1. Choose your method ids

Pick from the canonical 12-method library in `SOP-ENG_ESTIMATION_DISCIPLINE_001` §3:

* `discovery_kickoff`, `discovery_interviews`, `discovery_synthesis`
* `design_workshop`, `design_specification`
* `build_prototype_excel`, `build_webapp`, `build_integration_study`
* `transfer_training`, `transfer_documentation`
* `close_review`
* `ongoing_support_month`

Each method comes with min/par/max effort hours and a default role mix. Override the role mix only when the engagement's reality forces it (e.g. drop a non-applicable role for an automation-only scope).

## 2. Choose your multipliers

Pick zero or more from `MULTIPLIERS` in `SOP-ENG_ESTIMATION_DISCIPLINE_001` §5:

* `enterprise_premium` (× 1.20) — counterparty has formal procurement / DSI / legal-counsel chain.
* `bridge_entity` (× 1.10) — reached via a partner bridge.
* `locale_uplift_fr` (× 1.20) — French market vs Madrid SME baseline.
* `first_of_kind` (× 1.15) — engagement archetype is new to Holistika.
* `repeat_counterparty` (× 0.90) — repeat business.

Multipliers compound on **price only**, not on effort.

## 3. `scope.yaml` shape

```yaml
engagement_slug: 2026-mm-dd-counterparty-slug
counterparty_label: Anonymised counterparty label (used in the rendered headings)
country_code: FR
start_date: 2026-mm-dd
notes: |
  One or two sentences capturing the engagement framing.
  Renders into the commercial-schedule.md notes section.
packages:
  - package_id: WP-1-discovery
    method_id: discovery_kickoff
    label: Optional override of the default method label
    multiplier_ids:
      - enterprise_premium
      - locale_uplift_fr
  - package_id: WP-2-design
    method_id: design_specification
    role_mix_override:
      Tech Lead: 0.6
      Project Manager: 0.4
    multiplier_ids:
      - enterprise_premium
      - locale_uplift_fr
      - first_of_kind
  - package_id: WP-3-build
    method_id: build_webapp
    multiplier_ids:
      - enterprise_premium
      - locale_uplift_fr
      - first_of_kind
  - package_id: WP-4-transfer
    method_id: transfer_training
    multiplier_ids:
      - enterprise_premium
      - locale_uplift_fr
  - package_id: WP-5-close
    method_id: close_review
    multiplier_ids:
      - enterprise_premium
```

## 4. Output

`commercial-schedule.md` will contain:

* A per-package table — effort hours, blended rate, cost pre-multiplier, multiplier factor, cost final, duration in working days. All values are min/par/max triangles; PERT-expected values are shown in the Totals block.
* A Totals block — aggregate effort, cost, and duration (with PERT-expected for each).
* A Mermaid Gantt — sequential schedule from `start_date`, skipping weekends, public-holiday-aware.
* Optional notes (from the `notes` field in `scope.yaml`).

## 5. Operator review checklist

* [ ] Each package's role mix is plausible for this engagement's shape (no Brand Manager on a pure automation scope, no AI Engineer on a pure brand scope).
* [ ] Multipliers are justified (an `enterprise_premium` should pair with a counterparty graded enterprise in `GOI_POI_REGISTER.csv`).
* [ ] The par-cost is within the counterparty's plausible budget band (validated against `source-grade.csv` budget signals).
* [ ] The par-duration is consistent with the counterparty's stated urgency (Q-1 in the elicitation plan).
* [ ] PERT-expected vs par gap < 15% per package; if larger, the operator notes the risk in the proposal cover.

## 6. Cross-references

* `SOP-ENG_ESTIMATION_DISCIPLINE_001.md` — canonical SOP.
* `akos/engagement_estimation.py` — math.
* `scripts/estimate_engagement.py` — CLI.
* `tests/test_engagement_estimation.py` — gates.
