---
language: en
report_kind: phase_closure
phase: P4
status: closed
closed_at: 2026-05-06
initiative: I59 — HLK governance promotion + clean slate cycle
---

# I59 P4 — Operator Action Inbox SSOT (closure)

## Outcome

P4 closes successfully. The Operator Action Inbox is live at
`docs/wip/planning/OPERATOR_INBOX.md`, auto-rendered from
`docs/references/hlk/compliance/OPS_REGISTER.csv` (the SSOT seeded in P3).
Re-renders are deterministic and a soft INFO row in `release-gate.py` flags
drift without blocking the verdict.

## What shipped

### Renderer

`scripts/render_operator_inbox.py` — new script following the same shape as
`render_wip_dashboard.py`:

- Reads `OPS_REGISTER.csv` and filters `status='open' AND owner_class IN
  ('operator', 'mixed')` per **D-IH-59-A** governance promotion + the I59 plan
  §P4.
- FK-joins `originating_initiative_id` against `INITIATIVE_REGISTRY.csv` for
  the initiative title and `owner_role` against `baseline_organisation.csv`
  for the human-readable role label.
- Sorts by `rice_score DESC` (negative-key sort with `ops_action_id`
  tie-break for determinism); rows missing a numeric RICE land at the bottom
  in their natural order so they remain visible.
- Emits a deterministic block between `<!-- BEGIN AUTO -->` and
  `<!-- END AUTO -->` markers in `OPERATOR_INBOX.md`. Hand-written content
  outside the markers is preserved across re-renders.
- `--check-only` re-renders to memory and exits 1 if the on-disk file would
  change — this is what the release-gate hook uses.

### Inbox surface

`docs/wip/planning/OPERATOR_INBOX.md` — newly created. Frontmatter is
`status: continuous` with a `continuous_rationale` explaining the
auto-rendering contract. The inbox currently contains 22 open
operator/mixed-owned rows from the P3 seed; once the operator triages these
and assigns RICE / closes superseded items, the table tightens to the genuine
high-leverage backlog.

### Release-gate hook

`scripts/release-gate.py` gained a soft INFO row (non-blocking) that calls
`render_operator_inbox.py --check-only`. When the inbox is stale, the gate
emits `[INFO] Operator inbox stale — re-run scripts/render_operator_inbox.py`
without changing the PASS/FAIL verdict. This mirrors the `render_wip_dashboard`
pattern (the dashboard is rendered eagerly via `validate_hlk.py`'s test suite;
the inbox has its own renderer for visibility).

### Tests

`tests/test_render_operator_inbox.py` — 8 tests covering filter correctness,
RICE descending sort, FK joins on initiative title and role label,
determinism (sha256 stable), the empty-no-actions branch, the
missing-CSV-files graceful branch, and pipe-character escaping. All pass.

## Verification

| #   | Check                                                       | Result                              |
| --- | ----------------------------------------------------------- | ----------------------------------- |
| 1   | `py scripts/render_operator_inbox.py`                       | wrote OPERATOR_INBOX.md (22 rows)   |
| 2   | `py scripts/render_operator_inbox.py --check-only` (×2)     | PASS: operator inbox up to date     |
| 3   | `py -m pytest tests/test_render_operator_inbox.py -q`       | 8 / 8 passed                        |
| 4   | `py scripts/validate_hlk.py`                                | OVERALL: PASS (regression check)    |

## Linkage to predecessors / successors

- Reads `OPS_REGISTER.csv` (seeded in P3.7) and `INITIATIVE_REGISTRY.csv`
  (seeded in P3.6).
- **P5** (cycle staleness canary) reuses the release-gate INFO-row pattern.
- **P6** (OPS-58-3 fix) flips one row in `OPS_REGISTER.csv` from `open` →
  `closed`; the next inbox re-render drops it.
- **P10** (closure UAT) verifies inbox determinism under `--strict`.

## Decisions captured

No new D-IH-59-* decisions in P4. The phase implements the design from
**D-IH-59-A** (governance promotion) + plan §P4 verbatim.

## Forward work

- Operator triage of the 22 P3-seeded rows: assign RICE scores, close
  superseded items, retitle the placeholder titles (`(seed; needs operator
  triage)`) to one-line descriptions. This is the first thing the operator
  does after I59 closes.
- When the operator dashboard surface lands (future cycle), it can render the
  same view as a live SQL query against `compliance.ops_register_mirror` —
  the markdown surface and the dashboard view share one SSOT.
