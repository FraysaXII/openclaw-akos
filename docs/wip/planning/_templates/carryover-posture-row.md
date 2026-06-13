# Carryover posture row template (I98 P0)

Copy into `decision-log.md`, scope-overlap trackers, or [`carryover-posture-index.md`](../_trackers/carryover-posture-index.md).

**Rule:** bare "deferred" is banned in new artifacts — use **`scheduled`** or another posture from [`akos/planning/carryover_posture.py`](../../../akos/planning/carryover_posture.py).

---

## Scheduled (evidence-gated — **not dropped**)

```yaml
posture: scheduled
item_id: D-IH-NN-X          # or OPS-NN-Y / deliverable slug
target_initiative: INIT-OPENCLAW_AKOS-NN
target_phase: P6
activation_trigger: "One sentence — what must be true before work starts"
owner_role: Operator
next_review_trigger: "Phase entry OR YYYY-MM-DD OR named govern session"
discoverability_path: docs/wip/planning/NN-slug/decision-log.md#D-IH-NN-X
legacy_label: deferred      # optional — only when backfilling old prose
```

---

## Forward charter

```yaml
posture: forward_charter
item_id: OPS-NN-Y
successor_ref: docs/wip/planning/_candidates/i-nn-slug.md
activation_trigger: "TRIGGER condition or successor initiative P0"
discoverability_path: docs/wip/planning/_blockers/iNN-promotion-blocker-tracker.md
owner_role: PMO
next_review_trigger: "Successor P0 entry OR YYYY-MM-DD"
```

---

## Overlap pending

```yaml
posture: overlap_pending
item_id: D-IH-NN-D
scope_overlap_tracker: docs/wip/planning/_trackers/i96-i97-infonomics-scope-overlap-tracker.md
ratify_phase: I97 P5
tracked_siblings:
  - INIT-OPENCLAW_AKOS-96
discoverability_path: docs/wip/planning/_trackers/i96-i97-infonomics-scope-overlap-tracker.md
owner_role: Operator
next_review_trigger: "Ratify phase entry OR govern session date"
```

---

## Blocked

```yaml
posture: blocked
item_id: I83-promotion
blocker_tracker: docs/wip/planning/_blockers/i83-promotion-blocker-tracker.md
resolution_conditions:
  - "Criterion 1 from tracker §3"
next_review_trigger: "I86 Wave closes OR operator re-opens candidate"
discoverability_path: docs/wip/planning/_blockers/i83-promotion-blocker-tracker.md
owner_role: PMO
```

---

## Dropped (explicitly out of scope)

```yaml
posture: dropped
item_id: deliverable-slug
drop_rationale: "Why we are not doing this"
reversibility: low | medium | high
supersedes_or_replaces: optional-note
```

---

## Monitoring (PWF follow-up)

```yaml
posture: monitoring
item_id: uat-iNN-topic-YYYYMMDD
followup_class: monitoring-obligation
closure_target: "Wave R+2 or named phase"
linked_uat_path: docs/wip/planning/NN-slug/reports/uat-iNN-2026-06-12.md
owner_role: System Owner
next_review_trigger: "Closure target date OR next UAT amendment"
```

---

## Index table row (markdown)

| index_id | posture | item_id | target / successor | activation_trigger | next_review | owner | discoverability_path |
|:---|:---|:---|:---|:---|:---|:---|:---|
| CO-98-001 | scheduled | D-IH-97-E | I97 P6 | P5 govern ratify | I97 P5 entry | Operator | `97-.../decision-log.md#D-IH-97-E` |
