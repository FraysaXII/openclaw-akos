---
template_id: uat-impeccable
template_version: 1.0
introduced_by: INIT-OPENCLAW_AKOS-77 (P3; D-IH-77-CLOSURE)
applies_to: Any UAT exercising Impeccable Style skill (.cursor/skills/impeccable/) consumption of refreshed bridge files (PRODUCT.md + DESIGN.md + BASELINE_REALITY.md)
audience: J-OP (operator-only; this report is consumed by founder + future BrandOps Lead)
status: active
authored: 2026-05-16
language: en
---

# `uat-impeccable-template.md` — Reusable Impeccable UAT shape

> **Template intent.** Clone this file to `docs/wip/planning/<NN-initiative>/reports/uat-impeccable-<topic>-<YYYYMMDD>.md`. Replace `<NN-initiative>`, `<topic>`, `<YYYYMMDD>`, and any `<placeholder>` token with concrete content. Keep section headings + ordering; vary content; preserve operator-UX optimizations (scannable summary at top + per-surface deep-section + closure checklist at bottom).

## Why this template exists

The Impeccable skill is the design-time companion to the Pack A1 voice validator: Pack A1 catches voice drift after rendering; Impeccable prevents drift at draft-time by consuming the refreshed brand bridges. Every UAT exercising Impeccable's consumption of refreshed bridges (or new bridge content; or a new sub-mark surface) follows the same shape so per-UAT reports are quickly comparable across initiatives. The template encodes the Q3 C decision (I77 P3 inline-ratify): full critique paste + classification + reusable scaffold.

## Required frontmatter (replace before commit)

```yaml
---
uat_id: uat-impeccable-<topic>-<YYYYMMDD>
initiative: INIT-OPENCLAW_AKOS-<NN>
phase: P<N>
status: shipped | in_progress | superseded
shipped_date: <YYYY-MM-DD>
operator_review_date: <YYYY-MM-DD> | pending
surfaces_audited: <count>
surfaces_skipped: <count>
findings_brand_aligned: <count>
findings_brand_drift: <count>
findings_neutral: <count>
overall_verdict: PASS | PASS-WITH-FOLLOWUP | FAIL
language: en
---
```

## Section 1 — Operator-readable executive summary (J-OP optimized)

> **One-paragraph TL;DR.** What was tested, against which bridges, what the verdict is, what follow-up (if any) is queued. Read in < 30 seconds; the operator decides whether to read the rest based on this.

| Dimension | Result |
|:---|:---|
| **Verdict** | PASS / PASS-WITH-FOLLOWUP / FAIL |
| **Bridges consumed** | PRODUCT.md ✓ / DESIGN.md ✓ / BASELINE_REALITY.md ✓ / nudge-cleared ✓ |
| **Surfaces audited** | `<count>` |
| **Surfaces skipped** | `<count>` (reason: external sibling repo / locale-confound / etc.) |
| **Findings** | `<N>` brand-aligned · `<N>` brand-drift · `<N>` neutral |
| **Follow-up** | `<one-line-summary>` or `none` |

## Section 2 — Surface inventory (what we tested)

| ID | Surface path | Audience(s) | Locale | Status | Findings count |
|:---|:---|:---|:---:|:---:|:---:|
| S-1 | `<path/to/surface>` | J-XX + J-YY | en/es/fr | **AUDITED** | `<N>` |
| S-2 | `<path/to/surface>` | J-XX | en | **AUDITED** | `<N>` |
| S-3 | `<path/to/external/surface>` | J-XX | en | **SKIPPED** (external sibling) | n/a |

**Surface coverage rationale**: explain why these surfaces (single sentence each). Bias toward multi-audience surfaces (BASELINE_REALITY gate signal); flag sibling-repo surfaces as SKIP with explicit forward-pointer to the next bless cycle.

## Section 3 — Per-surface deep audits

For each AUDITED surface, render one sub-section using the structure below. Skip SKIPPED surfaces (cite them in §4 with reason).

### S-N — `<surface display name>`

**Surface metadata**

- **Path**: `<full repo path>`
- **Surface type**: page / deck-slide / dossier-prose / config / bridge-file / other
- **Audience(s)**: J-XX (per BASELINE_REALITY.md row + surface frontmatter `audience:` value)
- **Locale**: `<en|es|fr|mixed>`
- **Last brand-review**: `<YYYY-MM-DD>` (per surface frontmatter or git blame on the last brand-affecting commit)
- **Bridges relevant**: PRODUCT.md / DESIGN.md / BASELINE_REALITY.md / none

**Audit scope** — what Impeccable would check on this surface (cite the relevant SKILL.md command):

- `/critique` (identify weaknesses + suggest improvements) — for prose-heavy surfaces.
- `/audit` (quality + UX heuristic audit) — for component surfaces.
- `/polish` (small refinements) — for near-final surfaces.
- Brand-DNA cross-check against the 18 brand canonicals via the 3 refreshed bridges.

**Findings table** (classify each finding):

| # | Finding | Class | Canonical reference | Severity |
|:---:|:---|:---:|:---|:---:|
| 1 | Surface uses "X" terminology consistent with `BRAND_VOICE_FOUNDATION.md` §2 | **brand-aligned** | `BRAND_VOICE_FOUNDATION.md` §2 | n/a |
| 2 | Surface leaks internal-register token "elicitation" into J-CU prose (line 47) | **brand-drift** | `BRAND_BASELINE_REALITY_MATRIX.md` §3 | high |
| 3 | Surface uses default OKLCH grey instead of brand-charcoal | **neutral** (within tolerance per `BRAND_VISUAL_PATTERNS.md` §"Neutral palette") | `BRAND_VISUAL_PATTERNS.md` §4 | low |

Classification key:
- **brand-aligned** = surface honors the canonical (no action needed).
- **brand-drift** = surface deviates from the canonical (action required; severity high/med/low).
- **neutral** = surface is within tolerance OR not covered by a canonical yet (forward-candidate for a future canonical addition).

**Impeccable command output paste** (verbatim if short; 3-7 line digest if very long):

```
<paste here>
```

When Impeccable was not invoked directly (e.g., agent-driven audit using the bridges + canonicals as proxy for the skill output), state that explicitly:

> *Note: Impeccable skill not invoked in this session. Audit performed by the agent applying the same canonical-consumption discipline (read 3 bridges → cross-reference 18 brand canonicals → classify findings). Real `/critique` invocation deferred to operator's preferred session.*

**Per-surface verdict**: PASS / PASS-WITH-FOLLOWUP / FAIL

## Section 4 — Skipped surfaces (with reason)

For each SKIPPED surface, one row:

| ID | Surface path | Reason | Forward-pointer |
|:---|:---|:---|:---|
| S-N | `<path>` | External sibling repo not present in this workspace | Next bless cycle per [`SOP-EXTERNAL_REPO_BLESSING_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) |
| S-N | `<path>` | Locale confound — Spanish surface, dual-register translation rules not yet applied to ES | Future I-NN initiative |

## Section 5 — Bridge consumption verification

This section confirms the three bridges (PRODUCT.md + DESIGN.md + BASELINE_REALITY.md) are loadable + cite the canonicals the audit referenced. Cross-references the `validate_impeccable_bridge_drift.py` gate output.

| Check | Result | Evidence |
|:---|:---:|:---|
| `validate_impeccable_bridge_drift.py` exits 0 | PASS | Coverage `<N>/<N>` brand canonicals cited by ≥ 1 bridge |
| `generate_impeccable_bridges.py --check` emits coverage report | PASS | Full per-canonical table shows correct citation routing |
| Audit findings referenced canonicals exist in CANONICAL_REGISTRY.csv | PASS | `<N>` canonical references found; `<N>` resolve cleanly |
| Multi-audience nudge (Impeccable v3.1 SKILL.md line 8) | CLEARED | BASELINE_REALITY.md present + non-empty + 7 J-* audience codes surfaced |

## Section 6 — Decisions ratified by this UAT

Any inline-ratify decisions made during the UAT session (per `akos-inline-ratification.mdc`):

- `D-IH-<NN>-<X>`: `<one-line summary>`. Closed at this UAT.

If none: state "No decisions ratified during this UAT."

## Section 7 — Follow-up queue

Numbered items capturing brand-drift remediation, neutral upgrades, and external-sibling UAT carryover. Each item has owner + target date + linked decision (if applicable).

| # | Action | Owner | Target | Linked |
|:---:|:---|:---|:---:|:---|
| 1 | Fix brand-drift finding #2 on S-1 (line 47 internal-register leak) | Brand Manager | next commit cycle | D-IH-<NN>-<X> |
| 2 | UAT external sibling S-3 in next bless cycle | System Owner | next bless cycle | — |

## Section 8 — Operator approval checklist

Reviewer should validate before this UAT closes the parent OPS row:

1. **Surface inventory matches charter** — surfaces audited cover the scope declared in the parent initiative's master-roadmap.
2. **No brand-drift left in HIGH severity** without a follow-up entry.
3. **Bridge consumption verified** — drift gate PASS; coverage report renders.
4. **Multi-audience nudge cleared** (when applicable).
5. **Follow-up queue assigned** — every drift finding has an owner + target.
6. **OPS row ready for closure** with `closed_at` + `closed_by` populated.
7. **(Optional) Operator invoked Impeccable directly** to spot-check at least one surface where the agent acted as a proxy.

## Section 9 — Cross-references

Each UAT report must cite (and link inline):

- The parent initiative's `master-roadmap.md`
- The relevant `decision-log.md` entries for any decisions ratified
- `BRAND_BASELINE_REALITY_MATRIX.md` (matrix the audit consulted)
- `BRAND_VOICE_FOUNDATION.md` + `BRAND_JARGON_AUDIT.md` (voice canon used in classification)
- `akos-planning-traceability.mdc` §"UAT evidence contract" (governing rule)
- `akos-brand-baseline-reality.mdc` (dual-register contract enforcing external-register on external surfaces)
- The 3 bridge files (PRODUCT.md + DESIGN.md + BASELINE_REALITY.md)
- The drift gate script (`scripts/validate_impeccable_bridge_drift.py`)

## Template usage notes

- **Section ordering is binding**: §1 executive summary first (J-OP optimization), §2 inventory, §3 deep audits, §4 skips, §5 verification, §6 decisions, §7 follow-up, §8 approval checklist, §9 cross-refs.
- **Section content is variable**: every section adapts to the surfaces in scope. A single-surface UAT may collapse §3 to one sub-section + §4 may be empty; a multi-surface UAT expands §3 with one sub-section per surface.
- **Naming convention**: `uat-impeccable-<topic>-<YYYYMMDD>.md` where `<topic>` is one of: `<surface-class>` (e.g., `bridge-refresh`, `deck-redesign`, `dashboard-chrome`), `all-surfaces` (broad sweep), or the surface ID itself (single-surface UAT).
- **Operator-UX optimizations**:
  - Section 1 must be readable in < 30 seconds.
  - Section 3 sub-sections must each be scannable in < 2 minutes.
  - All tables have ≤ 6 columns + ≤ 10 rows (split into multiple tables if needed).
  - Every cited canonical is a clickable markdown link.
  - No internal-register tokens (this report renders to J-OP only, but should still respect dual-register hygiene as practice).
- **Append-only after operator review**: once the operator reviews + approves, only the §7 follow-up queue and §6 decisions may be amended; the rest is frozen reference.
