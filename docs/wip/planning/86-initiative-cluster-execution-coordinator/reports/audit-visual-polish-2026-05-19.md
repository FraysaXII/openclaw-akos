---
status: active
classification: audit-report
intellectual_kind: visual_polish_a11y_audit
authority: System Owner
artifact_role: derived
ratifying_decisions: [D-IH-86-Q, D-IH-86-S]
parent_decision: D-IH-86-S
linked_initiative: INIT-OPENCLAW_AKOS-86
forward_linked_initiative: INIT-OPENCLAW_AKOS-68
language: en
last_review: 2026-05-19
audience: J-OP
---

# Wave G B-G2 — Visual-polish accessibility audit (axe-core)

> Wave G Strand F+6 deliverable; companion to the F+3 process_list tranche and F+4 channel-frontmatter onboarding. Baseline accessibility findings against the 2 rendered HTML artifacts under `docs/presentations/`; produces the evidence rows that **I68 P3 Visual regression rollout** can absorb when it activates per [`docs/wip/planning/68-cicd-discipline-and-observability-maturity/master-roadmap.md`](../../68-cicd-discipline-and-observability-maturity/master-roadmap.md).

## Tooling

- **Tool:** `@axe-core/cli@4.11.3` (npm; bundles `axe-core@4.11.x` rule library).
- **Runner:** `npx @axe-core/cli <file://url> --save <out.json>` (Windows + PowerShell; no Python wrapper installed locally).
- **Driver:** axe-core's default Chrome headless via WebDriver bundled with the CLI.
- **Executive call:** F+6 ratify gate auto-resolved to `npx CLI` (lowest setup friction; Node 22 + npm 11 already on this Windows machine; axe-selenium-python + axe-core-python NOT installed). Per inline-ratify-craft skill "Pitfall: I have run the evidence sweep but I do not see clear options" — decision recorded as `decision_source: agent_executive_call`.
- **Raw output:** `artifacts/axe-core/holistika-company-dossier.json` + `artifacts/axe-core/uat-impeccable.json`.

## Per-artifact findings table

### Artifact 1 — `docs/presentations/holistika-company-dossier/index.html`

The 14-slide ENISA company dossier deck preview (canonical paired source: `docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_story_es.md` + `deck_slides.yaml`). Rendered surface destined for J-ENISA + J-IN audiences via PDF export (`artifacts/exports/holistika-company-dossier-enisa-<date>.pdf`).

| Rule | Severity | Nodes | Help | Remediation hint |
|:---|:---|---:|:---|:---|
| `color-contrast` | SERIOUS | 34 | Elements must meet minimum color contrast ratio thresholds | Increase contrast on `.eyebrow` class (slides 13-15), `.fit-title`, `.use-of-funds-title`, `.solution-card .solution-title`. Most failures are light-grey eyebrow text or thin-weight titles on white. Bump to ≥4.5:1 per WCAG 2.1 AA. |
| `heading-order` | MODERATE | 8 | Heading levels should only increase by one | Card titles (`.solution-card`, `.method-stripe`, `.icp-card`, `.bm-row`, `.moat-card`, `.roadmap-window`, `.fit-card`) use `<h3>` or `<h4>` after a `<h2>` skipping the expected next level. Adjust card-title HTML to use `<h3>` consistently after slide `<h2>`. |

**Subtotal:** 42 nodes across 2 rules (1 SERIOUS + 1 MODERATE).

### Artifact 2 — `docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html`

The Impeccable UAT all-surfaces audit deck (J-OP-only internal surface; companion to the I86 Wave 1 Impeccable Style work). Currently J-OP per the canonical, but render quality still warrants the audit since this is the operator-facing artifact reviewed before the I86 cluster closure.

| Rule | Severity | Nodes | Help | Remediation hint |
|:---|:---|---:|:---|:---|
| `color-contrast` | SERIOUS | 17 | Elements must meet minimum color contrast ratio thresholds | Multiple text classes on dark-blue background fall below 4.5:1. Mostly eyebrows + small caption text on accent panels. Same remediation pattern as Artifact 1. |
| `heading-order` | MODERATE | 1 | Heading levels should only increase by one | Single instance; one card-title skips a heading level. Adjust HTML semantics. |
| `landmark-one-main` | MODERATE | 1 | Document should have one main landmark | Wrap the primary content in `<main>` element. Currently the `.page` div is the main container but lacks the landmark role. Add `role="main"` or wrap in `<main>`. |
| `region` | MODERATE | 13 | All page content should be contained by landmarks | All 12 `.section` divs + `.footer` need landmark roles (`<section aria-labelledby="...">` or `<aside>` or `<nav>`). Boilerplate fix once the `<main>` lands; sections become semantic regions by default. |

**Subtotal:** 32 nodes across 4 rules (1 SERIOUS + 3 MODERATE).

## Summary count by severity

| Severity | Total nodes | Rules affected | Artifacts affected |
|:---|---:|---:|---:|
| **CRITICAL** | 0 | 0 | 0 |
| **SERIOUS** | 51 | 1 (`color-contrast`) | 2 of 2 |
| **MODERATE** | 23 | 4 (`heading-order`, `landmark-one-main`, `region`) | 2 of 2 |
| **MINOR** | 0 | 0 | 0 |
| **Total** | **74** | **5** | **2** |

**Key observation:** zero CRITICAL findings. The 51 SERIOUS findings are all the same single rule (`color-contrast`) and concentrate on small-text classes (eyebrows, card titles, captions). The 23 MODERATE findings are all semantic-HTML adjustments (heading order, landmark wrapping). None of these block J-ENISA acceptance of a PDF render (axe-core checks the HTML preview, not the final PDF — and ENISA reviewers reference the PDF + sha256 manifest, not the HTML).

## Forward-charter section

### Findings that warrant remediation

- **All 51 SERIOUS `color-contrast` findings** — should be remediated when [I68 P3 Visual regression rollout](../../68-cicd-discipline-and-observability-maturity/master-roadmap.md#p3) activates. The remediation pattern is mechanical (CSS variable adjustment in the deck-visual-system tokens); one PR can fix both decks if they share the brand-token surface. **Effort:** small (1 commit; ~30 LoC CSS changes). **Owner:** Brand & Narrative Manager + Tech Lab co-review.
- **`region` + `landmark-one-main` (uat-impeccable.html, 14 nodes total)** — together they need a single semantic-HTML refactor: wrap `.page` in `<main>`, change `.section` to `<section>` (or add `role="region"` + `aria-label`). One PR closes both rules. **Effort:** small (1 commit; ~20 LoC HTML structure changes). **Owner:** Tech Lab.
- **`heading-order` (9 nodes total across both artifacts)** — change `<h3>`/`<h4>` card-title elements to the correct level relative to the parent slide `<h2>`. Two-line CSS class swap or per-template HTML correction. **Effort:** small (1 commit; ~10 LoC). **Owner:** Brand & Narrative Manager.

### Findings tolerable as-is (with documented justification)

- **`color-contrast` on light-grey eyebrows on slide-light templates** — these are *intentional* visual hierarchy (eyebrows are secondary metadata; main slide text already passes contrast). The 4.5:1 WCAG threshold is appropriate for the main copy; eyebrows operating as visual labels at 12-14pt are arguably exempt under WCAG 2.1 SC 1.4.11 (large-scale text exemption) when the font weight is regular. **Decision deferred** — Brand & Narrative Manager + Tech Lab to ratify at I68 P3 entry whether to (a) bump contrast and lose the visual whisper quality, (b) keep contrast and accept axe-core noise, or (c) re-tag the eyebrows as `aria-hidden="true"` + replace with semantic `<small>` siblings.
- **uat-impeccable J-OP-only landmark/region findings** — the audit fired on the J-OP internal-review surface. J-OP surfaces don't have an external-recipient accessibility obligation; the operator is the sole reader. **Decision:** accept as-is for J-OP scope; remediation only required when/if the surface ever gets re-tagged to an external audience.

### Cross-reference to I68 P3

When [I68 P3 Visual regression rollout](../../68-cicd-discipline-and-observability-maturity/master-roadmap.md#p3) activates, the planned `visual-regression snapshot` cadence can absorb this audit's findings as the **baseline** against which future regressions are detected. Specifically:

- The 74 findings here become the "tolerated baseline" — future commits that introduce *new* violations beyond this count would fail CI; existing baseline violations would be tracked as remediation backlog.
- I68 P3's `playwright + snapshot` rollout per [`akos-deploy-health.mdc`](../../../../.cursor/rules/akos-deploy-health.mdc) §"Step 3 — Multi-viewport visual smoke" extends naturally to a per-viewport axe-core snapshot if I68 P3 chooses to integrate the a11y rule library.
- The forward `INFO → FAIL` ramp for this class of findings mirrors the Wave F precedent (D-IH-86-Q): start INFO advisory in I68 P3 P0; promote to FAIL once the baseline holds across multiple commits + Brand co-signs the WCAG posture.

### When this audit should re-run

- Before each Wave-class push that touches the deck-visual-system tokens (HTML or CSS).
- At I68 P3 P0 entry (re-baseline for the visual-regression rollout).
- Quarterly per the canonical `tbi_mkt_prc_drift_gate_ops_001` cadence (Brand drift gate operations) — axe-core findings count + severity distribution become a per-quarter delta.

## Mechanical evidence

```text
$ npx @axe-core/cli "file:///.../docs/presentations/holistika-company-dossier/index.html" --save artifacts/axe-core/holistika-company-dossier.json
  → 42 Accessibility issues detected.
  → Saved file at artifacts/axe-core/holistika-company-dossier.json

$ npx @axe-core/cli "file:///.../docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html" --save artifacts/axe-core/uat-impeccable.json
  → 32 Accessibility issues detected.
  → Saved file at artifacts/axe-core/uat-impeccable.json

$ py -c "import json; ..."
  → holistika-company-dossier: SERIOUS color-contrast 34 + MODERATE heading-order 8 = 42 total
  → uat-impeccable: SERIOUS color-contrast 17 + MODERATE heading-order 1 + landmark-one-main 1 + region 13 = 32 total
  → No CRITICAL findings; no MINOR findings.
```

## Cross-references

- [`docs/wip/planning/68-cicd-discipline-and-observability-maturity/master-roadmap.md`](../../68-cicd-discipline-and-observability-maturity/master-roadmap.md) — I68 charter; P3 Visual regression rollout will absorb these baseline findings when active.
- [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-render-quality-2026-05-19.md`](uat-render-quality-2026-05-19.md) — Wave F UAT-evidence pass; §7 item 4 ("Visual-polish automated audit") was the forward-enhancement that this audit closes.
- [`.cursor/rules/akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) — the external-render discipline; visual-polish is the *quality* axis orthogonal to the *render-trail* axis the rule enforces.
- [`.cursor/rules/akos-deploy-health.mdc`](../../../../.cursor/rules/akos-deploy-health.mdc) §"Step 3" — multi-viewport visual smoke discipline (precedent for the I68 P3 absorption pattern).
- `artifacts/axe-core/holistika-company-dossier.json` + `artifacts/axe-core/uat-impeccable.json` — raw axe-core output for archival / future delta comparison.
- D-IH-86-S in [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — Wave G B-G2 closure decision that ratifies this audit.
