# Holistika -- Project Timeline: Shopify Bundle + Cart App

**Document owner**: Fayçal, Holistika Administrator
**Version**: 1.1
**Date**: 2026-03-17 (enriched 2026-03-17)
**Status**: Draft -- pending Websitz alignment
**Start date**: Week of 2026-03-23 (post API feasibility kick-off)
**External deadline**: Shopify Scripts sunset June 30, 2026 -- creates migration window (see below)

---

## Timeline Summary

| Phase | Duration | Dates (estimated) | Key Deliverable |
|-------|---------|-------------------|-----------------|
| Phase 0: Feasibility | 1 week | Mar 23 - Mar 29 | API validation, dev store, scaffold |
| Phase 1: Core Build | 4 weeks | Mar 30 - Apr 26 | Cart drawer + bundles + basic analytics |
| Phase 2: MVP Polish | 2 weeks | Apr 27 - May 10 | UX refinement, onboarding, templates |
| Phase 3: Closed Beta | 2 weeks | May 11 - May 24 | Testing on Websitz client stores |
| Phase 4: Community Launch | 3 weeks | May 25 - Jun 14 | Business Brothers, Hype Labs, Shopify App Store |
| Phase 5: Content & Growth | Ongoing | Jun 15+ | Tutorials, case studies, paid ads |
| Phase 6: V1.1 (AI + Post-MVP) | 4-6 weeks | Jul - Aug 2026 | AI recommendations, post-purchase, Plus features |

**Target**: Live on Shopify App Store by late May / early June 2026 (pre-summer, as committed in the meeting).

**External market event**: Shopify Scripts permanently cease execution on **June 30, 2026**. Legacy bundle/cart apps built on the deprecated Ruby Scripts engine will stop working. Our launch window (late May / early June) positions us to capture displaced merchants during the forced migration period. This is a strategic tailwind that amplifies our community launch (Phase 4) timing. Content strategy should include a "migration guide" to target these merchants explicitly.

---

## Phase 0: Feasibility & Setup (1 week)

**Dates**: March 23 - March 29, 2026
**Owner**: Holistika (Fayçal)

### Milestones

| # | Milestone | Due | Owner | Status |
|---|-----------|-----|-------|--------|
| 0.1 | Shopify Partner account active | Mar 23 | Holistika | Not started |
| 0.2 | Development store created | Mar 23 | Holistika | Not started |
| 0.3 | App scaffolded (`@shopify/shopify-app-react-router`) | Mar 24 | Holistika | Not started |
| 0.4 | `cart_transform` function deployed to dev store | Mar 25 | Holistika | Not started |
| 0.5 | AJAX Cart API integration tested (add, update, change) | Mar 26 | Holistika | Not started |
| 0.6 | Theme App Extension rendering on storefront | Mar 26 | Holistika | Not started |
| 0.7 | Polaris web components rendering in admin | Mar 27 | Holistika | Not started |
| 0.8 | PostgreSQL connection confirmed from app server | Mar 27 | Holistika | Not started |
| 0.9 | Session token auth flow working end-to-end | Mar 28 | Holistika | Not started |
| 0.10 | Feasibility report: GO / NO-GO decision | Mar 29 | Holistika | Not started |

### Deliverables

- Working app shell deployed to dev store
- `cart_transform` function modifying cart behavior
- Theme extension rendering a placeholder component on storefront
- Written feasibility assessment (blockers, risks, adjusted timeline if needed)

### Dependencies

- Shopify Partner account (may already exist from prior work)
- Access to Monster Upsell back-office via FA Slim store (Mathias to confirm)

---

## Phase 1: Core Build (4 weeks)

**Dates**: March 30 - April 26, 2026
**Owner**: Holistika (Fayçal) with Websitz UX input

### Week 1 (Mar 30 - Apr 5): Cart Drawer Foundation

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 1.1 | Cart drawer component (slide-in from right) | Apr 1 | Holistika |
| 1.2 | AJAX Cart API integration (real-time cart state) | Apr 2 | Holistika |
| 1.3 | Line item display (product image, name, qty, price) | Apr 3 | Holistika |
| 1.4 | Multi-goal progress bar (1 goal working) | Apr 4 | Holistika |
| 1.5 | Basic styling controls in admin (colors, fonts) | Apr 5 | Holistika |

### Week 2 (Apr 6 - Apr 12): Cart Drawer Advanced Features

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 1.6 | Multi-goal progress bars (stacked, multiple goals) | Apr 7 | Holistika |
| 1.7 | Order bumps (checkbox upsells, configurable placement) | Apr 9 | Holistika |
| 1.8 | Free gift unlock (threshold + auto-add) | Apr 10 | Holistika |
| 1.9 | Banner slot above cart contents | Apr 11 | Holistika |
| 1.10 | Payment badges (Klarna, Alma, Afterpay) | Apr 12 | Holistika |

### Week 3 (Apr 13 - Apr 19): Bundle Engine

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 1.11 | Bundle data model (PostgreSQL schema) | Apr 13 | Holistika |
| 1.12 | `cart_transform` function: merge bundle lines | Apr 14 | Holistika |
| 1.13 | Vertical bundle layout on product page | Apr 15 | Holistika |
| 1.14 | Horizontal bundle layout on product page | Apr 16 | Holistika |
| 1.15 | Volume-based campaign (buy more, save more) | Apr 17 | Holistika |
| 1.16 | Add-to-unlock campaign | Apr 18 | Holistika |
| 1.17 | Gift/unlock mechanics (spend X, get Y free) | Apr 19 | Holistika |

### Week 4 (Apr 20 - Apr 26): Admin UI + Analytics Foundation

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 1.18 | Admin: tab-based navigation (Cart Setup / Campaigns / Bundles / Analytics) | Apr 21 | Holistika |
| 1.19 | Admin: campaign creation flow (CRUD) | Apr 22 | Holistika |
| 1.20 | Admin: bundle creation flow (CRUD) | Apr 23 | Holistika |
| 1.21 | Analytics event ingestion pipeline | Apr 24 | Holistika |
| 1.22 | Analytics dashboard: revenue attribution, per-bundle stats | Apr 25 | Holistika |
| 1.23 | Analytics dashboard: daily/weekly/monthly toggle | Apr 26 | Holistika |

### Week 4 Checkpoint

- Holistika demos full cart drawer + bundle + analytics flow to Websitz
- Websitz provides detailed UX feedback
- Adjust priorities for Phase 2 based on feedback

---

## Phase 2: MVP Polish (2 weeks)

**Dates**: April 27 - May 10, 2026
**Owner**: Holistika (build) + Websitz (UX review)

### Week 5 (Apr 27 - May 3): UX Refinement

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 2.1 | Sticky cart component (product pages) | Apr 28 | Holistika |
| 2.2 | Design template library (6+ templates) | Apr 30 | Holistika |
| 2.3 | Color swatch integration on bundles | May 1 | Holistika |
| 2.4 | Banner overlays on bundle displays | May 2 | Holistika |
| 2.5 | Custom CSS override capability | May 3 | Holistika |
| 2.6 | UX review session with Mathias | May 3 | Websitz |

### Week 6 (May 4 - May 10): Onboarding + i18n

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 2.7 | 3-step onboarding wizard | May 5 | Holistika |
| 2.8 | Pre-configured templates (15-20, niche-specific) | May 7 | Holistika + Websitz |
| 2.9 | i18n: English + French UI complete | May 8 | Holistika |
| 2.10 | i18n: Spanish, German, Italian, Portuguese | May 9 | Holistika |
| 2.11 | GTM event emission (all custom events) | May 9 | Holistika |
| 2.12 | Campaign scheduling (start/end dates) | May 10 | Holistika |
| 2.13 | Internal MVP sign-off | May 10 | Holistika + Websitz |

### MVP Definition of Done

All items from the Product Requirements acceptance criteria (Section 10 of `product-requirements.md`) must pass:
- [ ] App installs on Shopify dev store
- [ ] Cart drawer slides in without full page load
- [ ] Multi-goal progress bar functional
- [ ] Order bump configurable and functional
- [ ] 2 bundle layouts (vertical + horizontal) working
- [ ] Volume and add-to-unlock campaigns working
- [ ] Analytics shows per-bundle revenue and conversion data
- [ ] Onboarding wizard (3 steps) working
- [ ] 3+ bundle design templates available
- [ ] All text translatable via i18n
- [ ] GTM events firing on cart actions

---

## Phase 3: Closed Beta (2 weeks)

**Dates**: May 11 - May 24, 2026
**Owner**: Websitz (testing) + Holistika (fixes)

### Week 7 (May 11 - May 17): Beta Deployment

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 3.1 | Deploy to 3-5 Websitz low-stakes client stores | May 12 | Websitz + Holistika |
| 3.2 | Deploy to FA Slim store (EFA/Issa) | May 12 | Holistika |
| 3.3 | Daily bug reports and feedback collection | Daily | Websitz |
| 3.4 | Critical bug fixes (< 24h turnaround) | Daily | Holistika |
| 3.5 | Tracking validation (GTM events verified by Websitz specialist) | May 15 | Websitz |
| 3.6 | Performance audit (Lighthouse impact < 2 points) | May 16 | Holistika |

### Week 8 (May 18 - May 24): Beta Iteration

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 3.7 | UX fixes based on beta feedback | May 20 | Holistika |
| 3.8 | Analytics dashboard validation (data accuracy) | May 21 | Holistika + Websitz |
| 3.9 | First case study drafted (beta store data) | May 22 | Websitz |
| 3.10 | First tutorial video recorded ("Set up cart drawer in 5 min") | May 23 | Websitz |
| 3.11 | Shopify App Store listing prepared (screenshots, description, metadata) | May 24 | Holistika + Websitz |
| 3.12 | Beta sign-off: GO for public launch | May 24 | Both |

### Beta Exit Criteria

- No critical bugs for 5 consecutive days
- Cart drawer renders correctly on all beta store themes
- At least 1 merchant reports measurable AOV increase
- Onboarding wizard completion rate > 80%
- Analytics data matches Shopify's own reporting (within 5% margin)

---

## Phase 4: Community Launch + App Store (3 weeks)

**Dates**: May 25 - June 14, 2026
**Owner**: Websitz (marketing) + Holistika (support)

### Week 9 (May 25 - May 31): Shopify App Store Submission

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 4.1 | Submit app to Shopify App Store for review | May 26 | Holistika |
| 4.2 | Respond to any Shopify review feedback | May 28-31 | Holistika |
| 4.3 | App approved and live on App Store | May 31 (target) | Shopify |
| 4.4 | Landing page live (app.holistika.io or equivalent) | May 28 | Holistika |
| 4.5 | Onboarding email sequence activated | May 28 | Holistika |

### Week 10 (Jun 1 - Jun 7): Community Soft Launch

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 4.6 | Business Brothers case study post | Jun 2 | Websitz |
| 4.7 | Hype Labs announcement post | Jun 3 | Websitz |
| 4.8 | Direct outreach to Websitz client base | Jun 2-7 | Websitz |
| 4.9 | First YouTube tutorial published | Jun 4 | Websitz |
| 4.10 | Monitor installs, support requests, feedback | Daily | Both |

### Week 11 (Jun 8 - Jun 14): Early Growth

| # | Milestone | Due | Owner |
|---|-----------|-----|-------|
| 4.11 | Collect first App Store reviews (target: 10+) | Jun 10 | Websitz |
| 4.12 | Second case study (community launch data) | Jun 12 | Websitz |
| 4.13 | Strategy guide PDF published | Jun 13 | Websitz |
| 4.14 | Growth metrics review (installs, conversions, retention) | Jun 14 | Both |
| 4.15 | Decide: proceed to paid ads or extend organic phase | Jun 14 | Both |

---

## Phase 5: Content & Growth Engine (Ongoing)

**Dates**: June 15, 2026 onward
**Owner**: Websitz (content) + Holistika (product, infrastructure)

### Monthly Cadence

| Activity | Frequency | Owner |
|---------|-----------|-------|
| Tutorial videos | 2-3 per week (Month 3-4), then 1-2 per week | Websitz |
| Strategy content (YouTube, blog) | 1 per week | Websitz |
| Template additions | 3-5 new templates per month | Holistika + Websitz |
| Community engagement | Daily | Both |
| App updates (bug fixes, minor features) | Bi-weekly releases | Holistika |
| Analytics review | Weekly | Both |
| Ambassador program operations | Monthly payouts, new ambassador onboarding | Holistika |

### Monthly Milestones (Months 3-6)

| Month | Target Installs | Target MRR | Key Actions |
|-------|----------------|-----------|-------------|
| Month 3 (Jun) | 100-300 | 500-1,500 EUR | Community launch, first reviews |
| Month 4 (Jul) | 300-700 | 1,500-4,000 EUR | Start paid ads, ambassador program, 3 niche playbooks |
| Month 5 (Aug) | 700-1,200 | 4,000-8,000 EUR | Offer calculator tool, community platform launch |
| Month 6 (Sep) | 1,200-2,000 | 8,000-15,000 EUR | V1.1 features (AI), first evaluation of exit/funding options |

---

## Phase 6: V1.1 -- AI & Advanced Features (Months 4-6)

**Dates**: July - August 2026 (parallel to growth phase)
**Owner**: Holistika

### V1.1 Feature Milestones

| # | Feature | Target Date | Priority |
|---|---------|------------|----------|
| 6.1 | AI-powered product recommendations (Madeira integration) | Jul 15 | P1 |
| 6.2 | AI dashboard insights (trend analysis, optimization tips) | Jul 30 | P1 |
| 6.3 | Post-purchase upsell module | Aug 15 | P2 |
| 6.4 | Shopify Plus tier features (`lineUpdate`, combined offers) | Aug 30 | P2 |
| 6.5 | Ambassador program with automated commission tracking | Jul 30 | P2 |
| 6.6 | Bundle landing pages | Aug 15 | P2 |
| 6.7 | CSV/PDF analytics export | Jul 15 | P1 |

---

## Key Dependencies & Critical Path

```
Phase 0 (Feasibility)
    │
    ├── GO decision ──► Phase 1 (Core Build)
    │                       │
    │                       ├── Week 4 Checkpoint (demo to Websitz)
    │                       │
    │                       ▼
    │                   Phase 2 (MVP Polish)
    │                       │
    │                       ├── MVP Sign-off
    │                       │
    │                       ▼
    │                   Phase 3 (Beta)
    │                       │
    │                       ├── Beta Sign-off
    │                       │
    │                       ▼
    │                   Phase 4 (Launch)
    │                       │
    │                       ├── Shopify App Store approval (external dependency)
    │                       │
    │                       ▼
    │                   Phase 5 (Growth) ◄───► Phase 6 (V1.1) [parallel]
    │
    └── NO-GO decision ──► Reassess scope, adjust timeline, identify blockers
```

**Critical path items** (delays here delay everything):
1. Phase 0 feasibility (if `cart_transform` doesn't work as expected)
2. Shopify App Store review (external, typically 5-10 business days)
3. Week 4 checkpoint (if core build needs major rework)

---

## Communication Cadence

| Meeting | Frequency | Participants | Purpose |
|---------|-----------|-------------|---------|
| Dev standup | Daily (async, group chat) | Holistika | Share progress, flag blockers |
| Weekly sync | Weekly (video call) | Holistika + Websitz | Demo progress, align priorities, UX review |
| Monthly review | Monthly | Holistika + Websitz + EFA | Growth metrics, strategic decisions, roadmap planning |
| Ad-hoc | As needed | Any | Urgent issues, technical questions |

---

## Decision Log

| Date | Decision | Rationale | Decided By |
|------|---------|-----------|------------|
| 2026-03-16 | Focus on bundles + cart drawer, deprioritize post-purchase | Higher value per effort; merchants need conversions first | Websitz (Mathias) |
| 2026-03-16 | Recurring subscription model (not one-time) | Better for MRR, valuation, and long-term business | All |
| 2026-03-16 | Pricing at 15/35/50 EUR tiers | Competitive with market, doesn't exceed 50 EUR standard | Websitz (Mathias) |
| 2026-03-16 | Lemlist model for go-to-market | Proven organic growth strategy via templates + tutorials + community | Websitz (Mathias) |
| 2026-03-16 | Monster Upsell as UX benchmark | Best back-office config UX in the market | Websitz (Mathias) |
| 2026-03-16 | Analytics dashboard as key differentiator | Biggest gap in all competitors; merchants want strategic data | Websitz (Mathias) + Holistika |
| 2026-03-17 | Target Shopify App Store launch pre-summer 2026 | Market timing + Holistika development capacity | Holistika (Fayçal) |
