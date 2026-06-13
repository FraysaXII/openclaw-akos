---
template_id: uat-closure
template_version: 1.0
introduced_by: INIT-OPENCLAW_AKOS-86 Wave J (D-IH-86-AS — UAT quality-bar canonization 2026-05-20)
applies_to: Closure UAT for any initiative >=5 phases OR touching a canonical CSV OR shipping sibling-repo work; full-fidelity post-2026-05-19 bar
audience: J-OP
status: active
authored: 2026-05-20
language: en
---

# `uat-closure-template.md` — Reusable closure-UAT shape (post-2026-05-19 bar)

> **Template intent.** Clone this file to `docs/wip/planning/<NN-initiative>/reports/uat-<NN>-closure-<YYYY-MM-DD>.md` (or `uat-<NN>-<topic>-<YYYY-MM-DD>.md` for non-closure topics). Replace tokens; preserve section ordering; preserve operator-UX optimisations (TL;DR table at top + reproducible-command evidence + sign-off checklist at bottom). Pair with `_templates/uat-impeccable-template.md` v1.0 when the UAT exercises Impeccable consumption (per-surface findings table); this template is the **structural superset** for all closure UAT.

## Why this template exists

Three problems the prior template family did not solve:

1. **Insufficient verdict accountability.** Pre-2026-05-19 UAT reports used `status:` enum (`shipped` / `in_progress` / etc.) but did not carry `verdict:` (`PASS` / `PASS-WITH-FOLLOWUP` / `FAIL`) at the **frontmatter** level. Result: closures were ambiguous about whether the gate truly cleared. The I85 + I87 closure UAT shape (Wave B / Wave C of Bundle D push, 2026-05-19) introduced explicit `verdict:` + `closure_decision_source:` frontmatter — this template binds it as the new bar.
2. **Insufficient mechanical evidence.** Earlier reports listed test names without **counts** + **outputs**, deferring rigour to operator memory. The I87 §3 pattern (`pytest -m openclaw_runtime: 20 passed, 0 failed, 0 skipped, 13 warnings`) and the §3 `git log` evidence proof binds quantitative verification at the report level — readers can reproduce the exact verification themselves.
3. **Insufficient audit trail when browser UAT is in scope.** The 2026 Playwright-MCP + PageBolt-MCP audit-trail pattern (cited §"External research" below) names that **API logs alone cannot prove what an operator saw on screen**. This template binds **screenshot + sha256 + timestamp** evidence for any closure where browser UAT is in scope per `akos-planning-traceability.mdc` §"UAT evidence contract".

## External research grounding (per applied-research-discipline.mdc RULE 2)

This template's quality bar is grounded in:

- **World Quality Report 2024** (cited in [Yuri Kan, "UAT Documentation: Complete Guide"](https://yrkan.com/blog/uat-documentation/)): organisations with structured UAT documentation report **38% fewer post-release defects + 52% fewer project escalations** than teams without formal documentation. The Acceptance-Criteria-Status table (this template §1) materialises that structure.
- **Standish Group CHAOS Report 2023**: inadequate user involvement is the **second most common cause of project failure (15% of failed IT projects)**. The §10 7-item operator sign-off checklist + per-row Target/Actual columns require the operator (or AIC role_owner) to actually engage — not rubber-stamp.
- **TestRail UAT guide** + **testomat.io UAT templates**: per-step `Step | Action | Expected | Pass/Fail | Comments` table is industry-standard; this template inherits it as the §2 closure-criteria pattern + §4 per-dimension findings table.
- **Playwright MCP introduction (playwright.dev/mcp)** + **PageBolt MCP audit pattern**: 2026 best practice for browser-based UAT pairs accessibility-snapshot execution (token-efficient; deterministic via element refs) with screenshot evidence at decision points (legal/audit-grade). This template binds that pattern in §3.4 for browser-walk evidence.

## Internal precedent grounding (per applied-research-discipline.mdc RULE 1)

This template's structural shape is grounded in:

- [`uat-i87-closure-2026-05-19.md`](../87-openclaw-operator-runtime-hardening/reports/uat-i87-closure-2026-05-19.md) — Bundle D Wave B closure pattern (§1 closure scope + §2 reproducible drill table + §3 substrate-test coverage + §5 D-IH-86-D mechanical cross-check + §6 closure registry edits + §7 risks closed + §8 closure verdict).
- [`uat-i85-closure-2026-05-19.md`](../85-audience-tag-canonicalization/reports/uat-i85-closure-2026-05-19.md) — Bundle D Wave C closure pattern (§1 closure-criteria verification with PASS-row table + §2 mechanical evidence with reproducible commands + §3 surface-tagging coverage list + §5 3-axis content-quality check).
- [`uat-impeccable-all-surfaces-2026-05-16.md`](../77-impeccable-brand-bridge-refresh/reports/uat-impeccable-all-surfaces-2026-05-16.md) — multi-surface UAT pattern with per-surface deep-section + verdict_history + remediation narrative (when an earlier version's verdict was overturned).
- [`uat-render-quality-2026-05-19.md`](../86-initiative-cluster-execution-coordinator/reports/uat-render-quality-2026-05-19.md) — multi-dimensional findings pattern (Orthography mechanical / Visual polish mechanical-ish / Naturalness operator-sign-off) + 7-item operator sign-off checklist.
- [`uat-i47-user-centric-uat-2026-05-02.md`](../47-user-centric-uat/reports/uat-i47-user-centric-uat-2026-05-02.md) — I47 was the foundational user-centric UAT modernisation initiative; persona-conditioned scenarios + calibration tolerance + cumulative test counts.
- [`docs/uat/i86-p3-persona-rollup-acceptance.md`](../../../uat/i86-p3-persona-rollup-acceptance.md) — Dimension-checklist pattern (A/B/C/D/E columns; self-attestable vs forward-chartered classification).

## Required frontmatter (replace before commit)

```yaml
---
report_type: closure-uat | uat-evidence | uat-amendment
intellectual_kind: uat_report | uat_evidence | closure_uat
parent_initiative: INIT-OPENCLAW_AKOS-<NN>
phase: P<N> | P<N>-followup | closure
sharing_label: internal_only
authored: <YYYY-MM-DD>
authored_by: <role_name e.g. System Owner | Brand & Narrative Manager | PMO>
last_review: <YYYY-MM-DD>
audience: J-OP
language: en
status: closed | shipped | review | superseded
verdict: PASS | PASS-WITH-FOLLOWUP | FAIL | PENDING-OPERATOR-WALK
closure_decision_source: agent_inline_default | operator_explicit | n/a
ratifying_decisions:
  - D-IH-<NN>-<X>
  - D-IH-<NN>-CLOSURE
linked_canonicals:
  - <canonical filename or path>
linked_runbooks:
  - <script path when SOP+runbook pair applies>
verdict_history:  # OPTIONAL — only for amended reports per impeccable-template precedent
  - <YYYY-MM-DD> PASS|FAIL — <one-line summary>
---
```

**Frontmatter contract notes.**

- `verdict` is **mandatory** at every commit. If a row is operator-pending, use `PENDING-OPERATOR-WALK` rather than omitting the field.
- `closure_decision_source: agent_inline_default` per `akos-inline-ratification.mdc` §"Time-box recovery" when operator skipped a ratify gate; `operator_explicit` when the operator answered the gate; `n/a` when no ratify gate fired.
- `ratifying_decisions:` must include the closure decision (when applicable) and every `D-IH-<NN>-<X>` row that this UAT evidences.
- `linked_runbooks:` is mandatory if the parent initiative shipped a SOP+runbook pair per `akos-executable-process-catalog.mdc` Rule 1.
- `verdict_history` is optional but **mandatory** if this UAT is an amendment of a prior version (per I77 P3-P4 amendment precedent).

## Section 1 — Closure summary (TL;DR; J-OP-optimised; <30s read)

> **One-paragraph TL;DR.** What was tested + verdict + follow-up (if any) + closure decision pointer. Read in <30 seconds.

| Dimension | Target | Actual | Status |
|:---|:---|:---|:---:|
| **Verdict** | PASS / PASS-WITH-FOLLOWUP | <verdict> | ✓ / ⏳ / ✗ |
| **Closure-criteria met** | <N>/<N> | <K>/<N> | ✓ / ⏳ / ✗ |
| **Mechanical gates green** | all | <K>/<N> | ✓ / ⏳ / ✗ |
| **Browser UAT evidence** | required / n/a | captured / pending / n/a | ✓ / ⏳ / N/A |
| **Risks closed** | <N> | <K> | ✓ / ⏳ / ✗ |
| **Operator sign-off** | required | yes / pending | ✓ / ⏳ |
| **Outstanding items** | 0 critical | <K> low / <K> medium / <K> high | ✓ / ⏳ / ✗ |

**Closure decision**: `D-IH-<NN>-CLOSURE` (or equivalent) — see §8 for full close-out + §9 for registry edits. Reversibility: **<low | medium | high>** (per decision row).

## Section 2 — Closure-criteria verification (master-roadmap §9 cross-check)

Per the parent initiative's master-roadmap §"Closure criteria", verify each row mechanically.

| # | Closure criterion | Verification command | Expected | Actual | Status |
|:---|:---|:---|:---|:---|:---:|
| 1 | <criterion 1> | `<reproducible cmd>` | <expected output> | <actual output / file path / count> | PASS / FAIL / SKIP |
| 2 | <criterion 2> | `<cmd>` | ... | ... | PASS / FAIL / SKIP |
| ... | | | | | |

**SKIP rows** must carry a one-clause reason in a footnote (e.g. *"SKIP — operator-credentials-only walkthrough; covered by §3.4 browser-evidence pattern"*).

## Section 3 — Mechanical evidence (reproducible)

### 3.1 Validator runs

Verbatim or near-verbatim output of every validator the closure depends on:

```text
py scripts/validate_<X>.py
  PASS|FAIL: <summary line; row counts; buckets>

py scripts/validate_hlk.py
  OVERALL: PASS|FAIL  (when HLK compliance assets are in scope)
```

### 3.2 Pytest output

```text
py -m pytest <markers or test files> -q
  <K> passed, <K> failed, <K> skipped, <K> warnings
```

When the parent initiative introduced a new pytest marker (per `akos-executable-process-catalog.mdc`), include the marker-specific run.

### 3.3 Build / lint output (when sibling-repo TSX or browser-relevant)

```text
npm run typecheck  (or: tsc --noEmit)
  <K> errors / clean

npm run lint
  <K> warnings / clean
```

### 3.4 Browser-evidence pattern (mandatory when browser UAT is in scope)

Per the 2026 Playwright-MCP + audit-trail pattern: capture **screenshot + accessibility-snapshot text + timestamp** at every decision point. Save under `artifacts/uat-screenshots/<initiative-slug>-<YYYY-MM-DD>/` with a `MANIFEST.md` sidecar.

| # | Step | Route | Expected element/state | Evidence path | Verdict |
|:---|:---|:---|:---|:---|:---:|
| 1 | Anonymous redirect at `/<protected-route>` | `/<route>` | 302 → `/sign-in` | `screenshots/<route>-anonymous-redirect.png` + accessibility-snapshot in `MANIFEST.md` | PASS |
| 2 | Authenticated render at `/<protected-route>` | `/<route>` | <expected element> | `screenshots/<route>-authenticated.png` | PASS / REVIEW-PENDING |

**Code-evidence fallback** (when operator credentials unavailable in agent session): cite the source file + line range that proves the component invariant statically. Mark verdict `CODE-EVIDENCE` not `PASS` to preserve the live-walk distinction.

```text
Component: components/planning/decision-timeline.tsx L34-L62
Invariant: status pill mapping covers all PlanningAtlasDecisionRow.status enum values
Evidence: const statusToTone: Record<PlanningStatus, ToneToken> = { active: 'success', ... } at L41-L48
```

## Section 4 — Per-dimension findings (when multi-dimensional)

For initiatives with multiple acceptance dimensions (e.g. data-layer + UI + auth + e2e), one column per dimension. Default to a single-dimension table when only one applies.

| # | Surface / dimension | Expected | Actual | Class | Severity |
|:---|:---|:---|:---|:---|:---:|
| 1 | <dim 1> | ... | ... | aligned / drift / neutral | n/a / low / med / high |

**Class key** — *aligned* = honors canonical / spec; *drift* = deviates (action required); *neutral* = within tolerance OR not yet covered by canonical (forward-candidate).

## Section 5 — D-IH-86-D mechanical cross-check (cluster sibling closures)

I86 cluster coordinator's D-IH-86-D contract (Wave B precedent) requires four signals at sibling closure. **All four must be ✓ before INITIATIVE_REGISTRY closure flip.**

| Signal | Source | Result |
|:---|:---|:---:|
| `release-gate.py` INFO advisory: parent initiative row green | [`config/verification-profiles.json`](../../../../config/verification-profiles.json) | ✓ / ✗ |
| `validate_hlk.py` OVERALL PASS | `py scripts/validate_hlk.py` | ✓ / ✗ |
| Paired-runbook contract honored (when SOP shipped) | SOP frontmatter `linked_runbooks:` populated AND scripts exist | ✓ / ✗ / N/A |
| UAT report present | This file | ✓ |

When any signal is N/A (e.g. initiative did not mint a SOP+runbook pair), state the reason explicitly. **Never use ✓ for an N/A row.**

## Section 6 — SOP + runbook pair (when applicable per akos-executable-process-catalog.mdc Rule 1)

Per Rule 1, every executable process registered in `process_list.csv` must have BOTH a paired human-readable SOP AND an agent-facing executable runbook. Cross-reference both here.

| Surface | Path | Status |
|:---|:---|:---:|
| Human-readable SOP | `docs/references/hlk/v3.0/<area>/<role>/canonicals/SOP-<NAME>_001.md` | active / review |
| Executable runbook (primary) | [`scripts/<name>.py`](../../../../scripts/<name>.py) | active |
| Executable runbook (secondary, if any) | [`scripts/<name2>.py`](../../../../scripts/<name2>.py) | active |
| `process_list.csv` row | `<area>_dtp_<purpose>_001` | active |
| AC-HUMAN | <one-line: how a role_owner can run via paired SOP without invoking the runbook> | satisfied |
| AC-AUTOMATION | <one-line: how the runbook fires unattended> | satisfied |

If the parent initiative did NOT mint a SOP+runbook pair, replace this section with a single sentence: *"Not applicable — this initiative did not introduce a new executable process row in `process_list.csv`."*

## Section 7 — Risk-register closure

Cross-reference every risk row in the parent's `risk-register.md` with status MITIGATED / NOT-TRIGGERED / DEFERRED.

| Risk ID | Risk summary | Status | Note |
|:---|:---|:---:|:---|
| R-IH-<NN>-1 | <summary> | MITIGATED | <how it was mitigated> |
| R-IH-<NN>-2 | <summary> | NOT-TRIGGERED | <why it didn't fire> |
| R-IH-<NN>-3 | <summary> | DEFERRED | <to which initiative + why> |

## Section 8 — Decision close-outs

For every `D-IH-<NN>-<X>` row in the parent's `decision-log.md`, name its activation status + reversibility.

- **D-IH-<NN>-A** — <one-line question>. **Activated** / **Superseded by D-IH-<NN>-Y** / **Closed**. Reversibility: **<low | medium | high>**.
- **D-IH-<NN>-B** — ...
- **D-IH-<NN>-CLOSURE** — All <K> phases shipped; UAT verdict <verdict>; `INIT-OPENCLAW_AKOS-<NN>` ratified `active → closed`. Reversibility: **<low | medium | high>**.

## Section 9 — Closure registry edits (mechanical)

Every closure flips state in canonical CSVs. Name the exact rows + the after-state.

- **INITIATIVE_REGISTRY**: `INIT-OPENCLAW_AKOS-<NN>` `status` flip `active` → `closed`; `closed_at` <YYYY-MM-DD>; `closure_decision_id` D-IH-<NN>-CLOSURE.
- **DECISION_REGISTER**: append `D-IH-<NN>-CLOSURE` (governance class; `decision_source` <agent_inline_default | operator_explicit>; reversibility <high | medium | low>).
- **OPS_REGISTER**: existing OPS-<NN>-<K> rows flip `status: open` → `status: closed` (when applicable; one bullet per OPS row).
- **Cluster coordinator master-roadmap §<X> sibling table**: <NN> row updated to closed (when initiative is in a cluster).
- **planning README** §"<NN-<NN>" table: <NN> row updated to closed.

## Section 9.5 — Carryover index propagation (required)

Per [`OPERATOR_STEERING_AND_CARRYOVER.md`](../../OPERATOR_STEERING_AND_CARRYOVER.md) rule 3: when this
closure may satisfy parked work tracked elsewhere, list each related row in
[`carryover-posture-index.md`](../_trackers/carryover-posture-index.md).

| Index row | Disposition | Evidence / link |
|:---|:---|:---|
| CO-NN-NNN | satisfied-here / superseded / unchanged / new-row | path or one-line note |

If none apply, state **N/A — no carryover index rows touched by this closure**.

## Section 10 — Verdict + 7-item operator sign-off checklist

**Verdict**: <PASS | PASS-WITH-FOLLOWUP | FAIL>

**Operator sign-off checklist (≤7 items; per `.cursor/rules/akos-agent-checkpoint-discipline.mdc` §"Operator pause point contract")**:

1. ⏳ **Closure-criteria all PASS** — §2 table shows every row PASS or operator-acknowledged SKIP. **Status: <verdict>**.
2. ⏳ **Mechanical evidence reproducible** — §3 commands re-run by operator yield same outputs. **Status: <yes / pending>**.
3. ⏳ **Browser UAT evidence captured (when in scope)** — §3.4 screenshots + accessibility-snapshots present at all decision points. **Status: <yes / n/a / pending>**.
4. ⏳ **D-IH-86-D mechanical cross-check four-signal PASS** (cluster siblings only) — §5 table all ✓. **Status: <yes / n/a>**.
5. ⏳ **SOP+runbook pair contract honored** (when applicable) — §6 SOP frontmatter + linked_runbooks resolved + AC-HUMAN + AC-AUTOMATION satisfied. **Status: <yes / n/a>**.
6. ⏳ **Risk + decision close-outs reflect repo state** — §7 + §8 cross-references audited; no risk left at trigger-imminent without DEFERRED forward-pointer. **Status: <yes>**.
7. ⏳ **CHANGELOG + files-modified.csv + master-roadmap last_review + DECISION_REGISTER closure row land in same commit wave as this UAT** — §9 entries committed atomically. **Status: <yes / pending>**.

When all 7 close ✓, the UAT report's `status:` flips to `closed` in frontmatter. Per `akos-inline-ratification.mdc` §"Time-box recovery", checklist items may auto-clear after 24h+ of operator silence + clean validators (reversible decisions only; irreversible items always require explicit operator ack).

## Section 11 — Cross-references

Every closure UAT must cite + link inline:

- Parent initiative master-roadmap: [`<NN-slug>/master-roadmap.md`](../master-roadmap.md).
- Parent decision log: [`<NN-slug>/decision-log.md`](../decision-log.md).
- Parent risk register: [`<NN-slug>/risk-register.md`](../risk-register.md).
- Parent files-modified: [`<NN-slug>/files-modified.csv`](../files-modified.csv).
- Cluster coordinator (when applicable): [`86-initiative-cluster-execution-coordinator/master-roadmap.md`](../../86-initiative-cluster-execution-coordinator/master-roadmap.md).
- Sibling-precedent UAT (cite the closest-shape closure UAT): e.g. [`uat-i85-closure-2026-05-19.md`](../../85-audience-tag-canonicalization/reports/uat-i85-closure-2026-05-19.md) or [`uat-i87-closure-2026-05-19.md`](../../87-openclaw-operator-runtime-hardening/reports/uat-i87-closure-2026-05-19.md).
- Governing rules: [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract" + §"UAT quality bar"; [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Verification matrix"; [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (when SOP+runbook pair); [`akos-applied-research-discipline.mdc`](../../../../.cursor/rules/akos-applied-research-discipline.mdc) RULE 3 (research enrichment subsection in wave-closure reports).
- External research base for this template's bar: [`docs/wip/planning/_templates/uat-closure-template.md`](uat-closure-template.md) §"External research grounding".

## Template usage notes

- **Section ordering is binding**: §1 closure summary first (J-OP <30s read), §2 closure-criteria, §3 mechanical evidence, §4 per-dimension findings (when applicable; collapse to one-row table when single-dimension), §5 D-IH-86-D cross-check (cluster siblings only; otherwise omit), §6 SOP+runbook (when applicable; otherwise one-line N/A), §7 risk closure, §8 decision close-outs, §9 registry edits, §10 verdict + sign-off checklist, §11 cross-references.
- **Section content is variable**: every section adapts to the initiative scope. A 1-3-phase initiative may collapse §4 + §5 + §6; a 5+-phase canonical-CSV-touching initiative populates every section fully.
- **Naming convention**: `uat-<NN>-closure-<YYYY-MM-DD>.md` for closure UAT; `uat-<NN>-<topic>-<YYYY-MM-DD>.md` for non-closure topics; `uat-<NN>-<topic>-browser-<YYYY-MM-DD>.md` when browser-evidence is the centerpiece.
- **Append-only after operator review**: once verdict closes PASS + operator signs §10 checklist, only §7 (risk closure carry-forward) and §8 (decision row reversal) may be amended; rest is frozen reference.
- **Reproducibility bar**: every PASS row in §2 + §3 carries a reproducible command. A reader without access to this session must be able to verify the verdict from the report alone.
- **Audit-trail bar**: when browser UAT is in scope per `akos-planning-traceability.mdc`, screenshot + sha256 + timestamp evidence is mandatory; absence = closure blocker per Wave B / Wave C precedent.
- **Sign-off finality**: per Yuri Kan's UAT documentation guide + the World Quality Report 2024, formal sign-off is what produces the 38%-fewer-defects + 52%-fewer-escalations outcome. The §10 checklist materialises that finality.
