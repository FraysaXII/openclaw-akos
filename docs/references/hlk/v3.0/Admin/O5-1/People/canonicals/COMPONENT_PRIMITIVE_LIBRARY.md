---
intellectual_kind: discipline_charter
sharing_label: internal_only
authored: 2026-05-20
last_review: 2026-05-20
last_review_by: Founder
last_review_decision_id: D-IH-86-BB
methodology_version_at_review: v3.1
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - OUTPUT_TYPE_LIBRARY.md
  - ARTIFACT_CLASS_LIBRARY.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - BRAND_BASELINE_REALITY_MATRIX.md
  - BRAND_DO_DONT.md
linked_canonical_csvs:
  - dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv
  - dimensions/ARTIFACT_CLASS_REGISTRY.csv
  - dimensions/OUTPUT_TYPE_REGISTRY.csv
  - dimensions/AUDIENCE_REGISTRY.csv
  - dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
status: active
role_owner: Brand & Narrative Manager
co_owner_role: System Owner
language: en
audience: J-OP
---

# Component Primitive Library — Layer 3 of the 4-layer hierarchy

> **Layer 3 of the 4-layer output architecture** sitting beneath the 5-axis [Holistika Quality Fabric](HOLISTIKA_QUALITY_FABRIC.md). This library names the **granular primitives** that compose every Holistika output — greeting, hook, body, CTA, signature, slide-hero, slide-compare, mermaid-flowchart, mermaid-gantt, data-table, form-field, dashboard-card, navbar, sidebar, empty-state, loading-state, error-state, evidence-block, methodology-note, confidentiality-block, cover-page, executive-summary, context-anchor, slide-progress, slide-appendix.
>
> **This is the Shadcn-depth layer.** Just as [Shadcn](https://ui.shadcn.com/docs) gives developers full control over button + dialog + form + dropdown primitives — open code, predictable composition, beautiful defaults — this library gives Holistika authors the same control over message and document primitives. **A creative user reaches their highest output quality when each primitive has been researched in depth + has variants to choose from + has a clear rationale for each variant choice.**
>
> Per [NextUI/HeroUI design principles](https://nextui.org/docs/guide/design-principles): simplicity + modular design + customization + consistent API + accessibility + slots. Same shape applied to message-and-document primitives, not just UI elements.
>
> **Forward-charter:** this library ships as a skeleton at I86 Wave K (D-IH-86-BB) with one fully-worked Shadcn-depth exemplar (CP-CTA below). The other 24 primitives mature when the corresponding artifact-class doctrine page lands and demands them.

## 1. The 25 component primitives

The canonical inventory lives in [`COMPONENT_PRIMITIVE_REGISTRY.csv`](Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv). Quick orientation:

| Kind | Primitives |
|:---|:---|
| **Prose** | CP-EXECUTIVE-SUMMARY · CP-CONTEXT-ANCHOR · CP-HOOK · CP-GREETING · CP-BODY · CP-CTA *(also interactive)* · CP-EVIDENCE-BLOCK *(also visual)* · CP-METHODOLOGY-NOTE · CP-CONFIDENTIALITY-BLOCK · CP-SIGNATURE *(also visual)* |
| **Visual** | CP-COVER-PAGE · CP-SLIDE-HERO · CP-SLIDE-COMPARE · CP-SLIDE-PROGRESS · CP-SLIDE-APPENDIX · CP-DIAGRAM-MERMAID-FLOWCHART · CP-DIAGRAM-MERMAID-GANTT · CP-DATA-TABLE *(also interactive)* · CP-DASHBOARD-CARD *(also interactive)* · CP-EMPTY-STATE · CP-LOADING-STATE · CP-ERROR-STATE *(also prose)* |
| **Interactive** | CP-FORM-FIELD · CP-NAV-NAVBAR · CP-NAV-SIDEBAR |

Status: 25 active.

## 2. Doctrine-page contract (per primitive — Shadcn shape)

Each primitive's doctrine page contains the same 9 sections (see §3 below for the CP-CTA worked example). The contract is borrowed from Shadcn's component documentation pattern:

1. **Anatomy** — the structural slots that compose this primitive (per [HeroUI slots](https://nextui.org/docs/guide/design-principles)).
2. **Variants** — the named alternatives + when to use each.
3. **Composition** — which artifact_classes this primitive composes into (FK to ARTIFACT_CLASS_REGISTRY).
4. **Research** — the discipline-specific research dimensions (per [RESEARCH_HEAD_DISCIPLINE.md](RESEARCH_HEAD_DISCIPLINE.md) — both internal-pattern + external-precedent).
5. **Accessibility** — non-negotiables before publish.
6. **Brand** — which brand canonicals constrain this primitive.
7. **Code-or-prose templates** — the open-code or open-prose templates the author can copy + customise (per Shadcn Open Code principle).
8. **Worked exemplars** — pointers to the best instances of this primitive shipped so far.
9. **Anti-patterns** — common failures the discipline of this primitive has surfaced.

## 3. Worked Shadcn-depth example — CP-CTA

### 3.1 Anatomy

```
[CP-CTA]
├── Container (scaffold)
├── Label slot       ← the action verb + object
├── Icon slot        ← optional; left or right of label
├── Loading-state    ← optional; replaces label during async
├── Disabled-state   ← optional; visual + a11y signal
└── Helper-text slot ← optional; below container, explains what happens
```

The 6 slots compose any CTA variant. Variants are named combinations of slot states.

### 3.2 Variants — when to use each

| Variant | Slots active | When to use | Example label |
|:---|:---|:---|:---|
| `cta-prose-only` | Label only | Mail body where button rendering is unreliable; J-ENISA where formality demands it; conversational DMs where a button is anti-pattern | "Reply to this email if you'd like to schedule a deeper conversation." |
| `cta-link-styled` | Label + container as inline link | Secondary CTAs in dense prose; non-primary actions in dashboards | "Read the methodology note →" |
| `cta-button-primary` | Label + container as filled button | Primary action in mail / web / slide; the one button per surface | "Schedule a 30-min call" |
| `cta-button-secondary` | Label + container as outlined or ghost button | Alternate path next to a primary; never alone | "Forward to your team" |
| `cta-stack-primary-plus-secondary` | Two buttons: primary + secondary | Web dashboards where two paths are genuinely paired | "Approve" + "Decline" |
| `cta-cal-com-embedded` | Embedded scheduler iframe + label fallback | High-friction-removal for J-IN / J-PT discovery calls; use when the audience is willing to schedule on first contact | "Pick a slot below" + Cal.com embed |
| `cta-form-submit` | Label + form-state-aware container (loading + disabled when invalid) | Web forms; submit action of CP-FORM-FIELD groupings | "Send my response" |
| `cta-toast-action` | Label + container as toast-action button | Recovery action after error or async success | "Retry" / "Undo" |

### 3.3 Composition

CP-CTA is summoned into:

| Artifact class | Typical variant(s) | Audience-gated variants |
|:---|:---|:---|
| AC-COVER-EMAIL | `cta-button-primary` (default); `cta-cal-com-embedded` (J-IN); `cta-prose-only` (J-ENISA) | See [Artifact Class Library §3.3](ARTIFACT_CLASS_LIBRARY.md#33-component-primitive-inventory) for full audience matrix. |
| AC-INTRO-MESSAGE | `cta-prose-only` (DM-bound; never buttons in WhatsApp/LinkedIn) | J-CU/J-PT → qualifying-question-as-CTA-anti-pattern; J-AD → discovery-call-anchor as CTA |
| AC-DECK-FOUNDING | `cta-prose-only` on closing slide | J-IN → "Investor inquiry: investors@holistikaresearch.com" |
| AC-DECK-ENGAGEMENT | `cta-prose-only` on next-steps slide | J-CU/J-PT → "Engagement go/no-go discussion: scheduled X" |
| AC-OPERATOR-INBOX | `cta-button-primary` per row action; `cta-stack-primary-plus-secondary` for ratify/decline | J-OP → operator-confidence-pairing |
| AC-WIP-DASHBOARD | `cta-link-styled` per inline action | J-OP → low-friction navigation |

### 3.4 Research — internal patterns + external precedents

**Internal patterns** Holistika has converged on:

- **One primary CTA per surface.** Validated by [`docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/cover_email_es.md`](../../../../../_assets/advops/PRJ-HOL-FOUNDING-2026/cover_email_es.md) and decided in I66 brand-vision-ops sweep (D-IH-66-N).
- **CTA selection scales with audience friction.** J-ENISA = prose-only (formal), J-AD = button + confidentiality block, J-CU = button + Cal.com embed, J-IN = Cal.com embed (highest priority for friction removal).
- **Channel binds variant.** DM channels (LinkedIn / WhatsApp) ban buttons; mail allows buttons + Cal.com; web allows full stack.

**External precedents** (per [akos-applied-research-discipline.mdc](../../../../../../../../.cursor/rules/akos-applied-research-discipline.mdc) RULE 2):

- [Shadcn Button](https://ui.shadcn.com/docs/components/button) — variant taxonomy: default, destructive, outline, secondary, ghost, link. Holistika's variant set is a superset (we add Cal.com embed + form-submit + toast-action because our artifact classes extend beyond pure UI).
- [Stripe's CTA design playbook](https://stripe.com) — one button per surface; AAA contrast; loading state always present.
- [Linear's commanding-button discipline](https://linear.app) — clear action verb + object; no ambiguous "Submit" or "OK".
- [BasecampForms' email button pattern](https://www.basecamp.com) — bullet-proof email button HTML (table-based for Outlook); Holistika uses the same pattern for `cta-button-primary` in mail.

### 3.5 Accessibility

| Bar | Check |
|:---|:---|
| **Label** | Action verb + object. "Click here" is anti-pattern; "Schedule a 30-min call" is correct. Per WCAG 2.4.4 link-purpose rule. |
| **Color contrast** | Filled button: foreground vs background ≥ 4.5:1 (text) or 3:1 (large text). Outlined button: foreground vs background ≥ 4.5:1 + outline vs background ≥ 3:1. Brand palette has pre-certified pairs. |
| **Focus ring** | Visible 2px focus ring on `:focus-visible`; ring-offset distinct from button. |
| **Keyboard activation** | Space + Enter both trigger; for cta-cal-com-embedded the iframe is keyboard-traversable. |
| **Disabled state** | `aria-disabled="true"` + visual signal (opacity 0.6 + cursor not-allowed); does NOT remove from tab order (so screen readers can read why disabled). |
| **Loading state** | `aria-busy="true"` + visible spinner replaces label OR appended right of label; label updated to past-tense ("Sending...") for screen reader announcement. |
| **Touch target** | ≥ 44×44 CSS px on mobile per WCAG 2.5.5. |
| **Animation** | Respects `prefers-reduced-motion: reduce`; loading spinner pauses + becomes static when reduced. |

### 3.6 Brand

- **Primary button:** brand primary color background (`brand-primary-600`); white text; border-radius per design system (8px desktop / 12px mobile per [BRAND_BASELINE_REALITY_MATRIX.md](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md)); type-scale `text-base font-semibold`; padding `12px 24px` (mobile: `16px 24px` for touch).
- **Secondary button:** transparent background; brand primary border; brand primary text; same border-radius + type-scale + padding.
- **Link-styled CTA:** brand primary color text; underline on hover/focus; arrow `→` glyph for forward-action.
- **Cal.com embed:** Cal.com's brand wrapped in Holistika's outer container (background neutral-1; border 1px neutral-2); never iframe-naked.
- **Per [akos-brand-baseline-reality.mdc](../../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)**: external CTAs use external-register vocabulary ("Schedule a research consultation"); internal CTAs (J-OP) may use internal-register ("Run intelligence collection on counterparty X").

### 3.7 Code-or-prose templates (Open Code)

**Mail bullet-proof button** (table-based for Outlook compatibility — copy + edit per channel doctrine):

```html
<table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
  <tr>
    <td align="center" bgcolor="#005DAF" style="border-radius: 8px;">
      <a href="https://cal.com/holistika/30min"
         style="display: inline-block; padding: 12px 24px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 16px; font-weight: 600; color: #ffffff; text-decoration: none; border-radius: 8px;">
        Schedule a 30-min call
      </a>
    </td>
  </tr>
</table>
```

**DM cta-prose-only** (LinkedIn / WhatsApp — copy + edit per channel doctrine):

```
If this resonates, happy to share a 15-min slot to walk through the methodology — pick a time that works: cal.com/holistika/discovery
```

**Web React component** (forward-charter — full Shadcn-style implementation in `boilerplate/components/ui/cta.tsx` per `I-NN-OUTPUT-ARCHITECTURE` P5):

```tsx
import { Button } from "@/components/ui/button";

export function CTAButtonPrimary({ href, label, loading, ...props }) {
  return (
    <Button
      asChild
      variant="default"
      size="lg"
      className="font-semibold"
      aria-busy={loading}
      {...props}
    >
      <a href={href}>{loading ? "Sending..." : label}</a>
    </Button>
  );
}
```

### 3.8 Worked exemplars

- **`docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/cover_email_es.md`** — uses `cta-button-primary` in mail context for ENISA cover email.
- **(Forward-charter)** — exemplars per audience × channel × variant matrix to mature per `I-NN-OUTPUT-ARCHITECTURE` P5.

### 3.9 Anti-patterns

- **Stacked-primary-CTAs.** Two filled buttons of equal weight side-by-side. Choice paralysis. Solution: one primary + one secondary OR pick the one that matters most.
- **The "Click here" label.** WCAG violation + zero context for screen reader users. Solution: action-verb-plus-object label.
- **Channel-mismatch variant.** A `cta-button-primary` in a LinkedIn DM (rendered as raw URL or stripped). Solution: DM channels mandate `cta-prose-only`.
- **The CTA-without-context.** A button at the end of a 30-second-read body with no rationale for why the recipient should click. Solution: CTA paired with the body's evidence — body answers "why click?", CTA executes the click.
- **The Cal.com-friction-mismatch.** Embedding Cal.com for a J-RC recruiter cold-outreach where the recipient hasn't agreed to a call yet. Solution: layered CTAs by audience-friction profile (J-IN warmest = Cal.com; J-RC coldest = reply-to-this-email).
- **The non-AAA contrast.** Brand-color button on a brand-color tinted background. Solution: brand palette has pre-certified contrast pairs; never hand-pick.
- **The disabled-without-tooltip.** Disabled button with no `aria-describedby` explaining why. Solution: `<button disabled aria-describedby="cta-disabled-reason">` + adjacent `<p id="cta-disabled-reason">Sign in to continue</p>`.

## 4. Forward-charter — primitive doctrine pages still to mature

Priority order (per `I-NN-OUTPUT-ARCHITECTURE` P5):

1. **CP-COVER-PAGE** (drives every sealed-deliverable opening).
2. **CP-SIGNATURE** (touched by every external-delivery prose artifact).
3. **CP-EXECUTIVE-SUMMARY** (the TLDR primitive — leverage compounds across dossiers + decks + UAT reports).
4. **CP-DIAGRAM-MERMAID-FLOWCHART + CP-DIAGRAM-MERMAID-GANTT** (already partially covered by [akos-planning-traceability.mdc](../../../../../../../../.cursor/rules/akos-planning-traceability.mdc) plan-quality bar; migrate to library shape).
5. **CP-EVIDENCE-BLOCK + CP-METHODOLOGY-NOTE** (per [RESEARCH_HEAD_DISCIPLINE.md](RESEARCH_HEAD_DISCIPLINE.md)).
6. **CP-DATA-TABLE + CP-FORM-FIELD + CP-DASHBOARD-CARD + CP-NAV-NAVBAR + CP-NAV-SIDEBAR + CP-EMPTY-STATE + CP-LOADING-STATE + CP-ERROR-STATE** (the dashboard family — matures with ERP panel implementations per Initiative 81).
7. **CP-SLIDE-HERO + CP-SLIDE-COMPARE + CP-SLIDE-PROGRESS + CP-SLIDE-APPENDIX** (the deck family — matures with `I-NN-OUTPUT-ARCHITECTURE` P5).
8. Remaining 7 primitives — backfill incrementally per first-production-instance.

## 5. Cross-references

- [HOLISTIKA_QUALITY_FABRIC.md](HOLISTIKA_QUALITY_FABRIC.md) — the 5-axis meta-doctrine.
- [OUTPUT_TYPE_LIBRARY.md](OUTPUT_TYPE_LIBRARY.md) — Layer 1 (shape).
- [ARTIFACT_CLASS_LIBRARY.md](ARTIFACT_CLASS_LIBRARY.md) — Layer 2 (purpose).
- [`COMPONENT_PRIMITIVE_REGISTRY.csv`](Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv) — canonical inventory.
- [Shadcn Button](https://ui.shadcn.com/docs/components/button) — external precedent for variant taxonomy.
- [HeroUI Design Principles](https://nextui.org/docs/guide/design-principles) — external precedent for slot-based composition.
- [`I-NN-OUTPUT-ARCHITECTURE`](../../../../../../wip/planning/_candidates/i-nn-output-architecture.md) — the candidate initiative that matures every primitive doctrine page.
- [akos-applied-research-discipline.mdc](../../../../../../../../.cursor/rules/akos-applied-research-discipline.mdc) — RULE 2 internal-pattern + external-precedent research applied per primitive.
- D-IH-86-BB — ratifying decision (4-layer architecture, 2026-05-20).
