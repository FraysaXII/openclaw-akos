# Holistika -- Shopify Bundle + Cart App: Product Requirements Document

**Document owner**: Fayçal, Holistika Administrator
**Version**: 1.1
**Date**: 2026-03-17 (enriched 2026-03-17)
**Source**: Meeting transcript 16-03-2026 (Holistika x Websitz x EFA), online market research, Annex gap analysis
**Status**: Draft -- pending Websitz review

---

## 1. Executive Summary

Holistika will build an all-in-one Shopify app that combines a fully customizable **cart drawer** with an advanced **bundle engine** and an **actionable analytics dashboard**. No existing Shopify app unifies these three capabilities at the quality level the market demands. Websitz provides product direction, UX benchmarking, and community-driven distribution. EFA/Faceline serves as early validation partner.

The app targets Shopify merchants of all sizes, from beginners to Shopify Plus enterprises, with a recurring subscription model (15/35/50 EUR tiers + Shopify Plus premium). The MVP must be ready for beta testing within ~1.5 months.

---

## 2. Partnership Roles

| Party | Representative(s) | Responsibilities |
|-------|-------------------|-----------------|
| **Holistika** | Fayçal | Technical build, infrastructure, AI/data, compliance, backend, admin tooling |
| **Websitz** | Mathias (ads/strategy), Ethan (Shopify) | Product ownership, UX direction, marketing, community distribution, tracking expertise |
| **EFA / Faceline** | Issa | Early adopter, B2B use case validation, market feedback |

### Governance

- Weekly coordination calls (group chat to be created)
- Holistika holds technical equity; joint entity to be formalized later
- Revenue split tracked automatically via Holistika's Stripe + PostgreSQL admin dashboard

---

## 3. Problem Statement

Shopify merchants face fragmented tooling:

1. **Cart optimization apps** (e.g., Monster Upsell) offer strong drawer customization but lack bundle capabilities.
2. **Bundle apps** (e.g., Fast Bundle, Wayne Bundle, Bundler) offer product bundling but lack cart drawer integration.
3. **All existing apps** have weak analytics dashboards that justify subscription cost rather than helping merchants optimize strategy.
4. **Merchants pay for 2-3 separate apps** ($12-35/month each) to get fragmented functionality, increasing total cost and creating integration headaches.

Merchants need a single app that handles bundles, cart drawer, and performance analytics in one place with superior UX.

---

## 4. Product Vision

A single Shopify app that is the definitive tool for **bundle creation**, **cart drawer optimization**, and **performance analytics** -- enabling merchants to increase AOV (Average Order Value), reduce cart abandonment, and make data-driven offer decisions.

### Success Metrics

- Shopify App Store rating >= 4.7 (matching Monster Upsell)
- 1,000+ installs within first 3 months of public launch
- MRR (Monthly Recurring Revenue) trajectory toward profitability within 6 months
- Merchant retention rate > 85% after trial conversion

---

## 5. Functional Requirements

### 5.1 Module A: Cart Drawer (Slide Cart)

The cart drawer is the primary conversion surface. It must match or exceed Monster Upsell's capabilities.

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| CD-01 | Slide-in drawer (not full-page cart) | P0 | Opens from the side without page navigation. Uses Shopify AJAX Cart API (`/cart.js`, `/cart/add.js`, `/cart/update.js`). |
| CD-02 | Multi-goal progress bars | P0 | Multiple stacked goals (e.g., free shipping at $50, free gift at $100). Visual progress indicator that turns green on unlock. |
| CD-03 | Order bumps (one-click upsells) | P0 | Checkbox-style product additions. Merchant configures placement: above CTA, below CTA, between line items. |
| CD-04 | Subscribe/subscription options | P1 | Integration point for subscription apps (e.g., Recharge, Bold Subscriptions). Display subscribe toggle per line item. |
| CD-05 | In-cart bundle display | P0 | Bundles created in Module B render natively inside the drawer with proper pricing and component breakdown. |
| CD-06 | Payment badges | P1 | Display Klarna, Alma, Afterpay, custom uploaded logos. Configurable text (e.g., "Pay in 3 installments from X EUR/month"). |
| CD-07 | Custom text below CTA | P1 | Editable text area for satisfaction guarantees, return policy, trust signals. |
| CD-08 | Banner slot above cart | P1 | Configurable banner with text, background color, optional countdown timer. |
| CD-09 | Sticky cart on product pages | P1 | Fixed bar (bottom or top of viewport) that follows scroll. Shows cart summary and quick-add CTA. |
| CD-10 | Configurable upsell placement | P0 | Drag-and-drop or dropdown to position upsell blocks above/below CTA, between items, at cart top/bottom. |
| CD-11 | Free gift unlock | P0 | When cart total exceeds threshold, a gift product is automatically added or offered. Progress bar transitions from partial to green. |
| CD-12 | Responsive design | P0 | Must render correctly on all screen sizes. Horizontal bundles preferred on mobile per Mathias's feedback. |
| CD-13 | Custom CSS/styling | P1 | Merchants can override colors, fonts, spacing to match their brand. |
| CD-14 | Mobile-first 375px baseline grid | P0 | All cart drawer layouts must be fully functional at 375px viewport width. Dominant traffic from social media ads is mobile. (Source: Annex ref 12, Oxify 2026) |
| CD-15 | Maximum 2-3 upsell suggestions per session | P0 | Cart drawer algorithmically limits upsell/cross-sell items to 2-3. Exceeding this triggers decision paralysis and depresses conversion. Merchant-configurable cap. (Source: Annex ref 13, Growth Suite 2026) |
| CD-16 | Upsell price ceiling (30% of cart) | P1 | Dynamically priced upsell suggestions must default to below 30% of total cart value. Configurable per merchant. (Source: Annex ref 13, Growth Suite 2026) |
| CD-17 | No URL redirect on add-to-cart | P0 | Adding a product to cart must never navigate to a new page. Drawer opens in-place, maintaining user context on product/collection page. (Source: Annex ref 12, Oxify 2026) |

### 5.2 Module B: Bundles

The bundle engine must combine the best of Wayne Bundle (display options, gifts) with Fast Bundle (variety of bundle types).

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| BN-01 | Vertical bundle layout | P0 | Stacked product cards. |
| BN-02 | Horizontal bundle layout | P0 | Side-by-side product cards. |
| BN-03 | Color swatch integration | P1 | Display variant swatches (color, size) directly on bundle items. |
| BN-04 | Gift/unlock mechanics | P0 | Spend $X, unlock product Y. Visual indicator (lock icon -> unlocked). |
| BN-05 | Banner overlays | P1 | Promotional banner on top of bundle display (e.g., "Best Seller", "Save 30%"). |
| BN-06 | Volume-based campaigns | P0 | Buy more, save more. Tiered discounting (e.g., buy 2 save 10%, buy 3 save 20%). |
| BN-07 | Collection-based campaigns | P0 | Apply bundle rules to entire collections or specific products. |
| BN-08 | "Add to unlock" mechanics | P0 | Progress-based rewards tied to cart composition. |
| BN-09 | Design template library | P0 | Multiple pre-built "ultra-stylish" display templates. Minimum 6 templates at launch. |
| BN-10 | Mix-and-match bundles | P1 | Customers select N products from a collection to build their own bundle. |
| BN-11 | Frequently bought together | P1 | Algorithm-driven or manually curated product groupings displayed on product pages. |
| BN-12 | i18n / translation support | P0 | All user-facing text translatable. Holistika's programmatic i18n library supports 6+ European languages. |
| BN-13 | Campaign scheduling | P1 | Start/end dates for bundle campaigns. Auto-activate and deactivate. |

### 5.3 Module C: Analytics Dashboard

This is the primary competitive differentiator. Current competitors display 3-4 vanity metrics that justify the subscription but do not enable strategic decisions.

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| AN-01 | Per-bundle performance | P0 | Revenue, conversion rate, click-through rate, add-to-cart rate for each bundle/campaign. |
| AN-02 | Per-campaign performance | P0 | Same metrics aggregated by campaign (volume, gift unlock, etc.). |
| AN-03 | Daily / weekly / monthly views | P0 | Toggle between time granularities. |
| AN-04 | Best-seller identification | P0 | Rank bundles by performance. Highlight top/bottom performers. |
| AN-05 | Revenue attribution | P0 | Total revenue attributable to the app (upsells, bundles, order bumps). |
| AN-06 | Margin data | P1 | If merchant provides COGS, calculate and display gross margin per bundle. |
| AN-07 | Actionable recommendations | P1 | Text-based suggestions (e.g., "Bundle X outperforms Y by 40% -- consider promoting it"). |
| AN-08 | AI-powered insights | P2 | Trend analysis, pricing strategy suggestions via Holistika's Madeira agent. Post-MVP. |
| AN-09 | Export / reporting | P1 | CSV/PDF export of dashboard data. |
| AN-10 | GTM event exposure | P0 | Emit custom events for Google Tag Manager. Cart actions (add, remove, bump, bundle select) must be trackable. |

### 5.4 Onboarding

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| OB-01 | Step-by-step setup wizard | P0 | 3-step flow: (1) Activate cart drawer, (2) Create first campaign, (3) Review sticky cart. Modeled on Monster Upsell. |
| OB-02 | Tutorial video per step | P1 | Short embedded video. Produced in French, auto-translated to 6+ languages. |
| OB-03 | Pre-configured templates | P0 | "One-click apply" templates that give merchants a working setup immediately. |
| OB-04 | Onboarding email sequence | P1 | Drip emails post-install pushing merchants to tutorials and templates. |

### 5.5 Admin / Back-Office (Merchant-Facing)

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| AD-01 | Tab-based navigation | P0 | Cart Setup > Campaigns > Bundles > Sticky Cart > Analytics > Integrations. Clean, Monster Upsell-style organization. |
| AD-02 | Live preview | P1 | Real-time preview of cart drawer and bundle display as merchant configures options. |
| AD-03 | Granular styling controls | P0 | Text size, color, spacing, font. Per-section controls (banner, progress bar, CTA, badges). |
| AD-04 | Campaign management | P0 | Create, edit, pause, delete campaigns. 3 types: volume-based, add-to-unlock, one-click upsell. |
| AD-05 | Integration panel | P1 | Connect existing bundle apps (migration path). Connect subscription providers. |

### 5.6 Internal Admin (Holistika + Websitz)

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| IA-01 | Revenue dashboard | P1 | Total MRR, subscriber count, churn rate, revenue per tier. |
| IA-02 | Revenue split automation | P1 | Automatic calculation and display of Holistika/Websitz revenue shares based on agreed percentages. |
| IA-03 | Ambassador tracking | P2 | Commission tracking for ambassador/referral program. |
| IA-04 | User management | P1 | View merchant accounts, subscription status, support requests. |

---

## 6. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NF-01 | Page load impact | Cart drawer must add < 200ms to page load time |
| NF-02 | Concurrent users | Support 500K concurrent API calls (Holistika infra already supports this) |
| NF-03 | Uptime | 99.9% availability |
| NF-04 | Data privacy | Row-level security in PostgreSQL. No cross-merchant data leakage. GDPR-compliant. |
| NF-05 | AI Act compliance | Full traceability of any AI-generated recommendations (timestamp, model, context). Holistika's existing compliance framework. |
| NF-06 | Shopify App Store compliance | Pass all mandatory and category-specific Shopify review requirements. Session tokens, proper OAuth, no popup-dependent flows. |
| NF-07 | Lighthouse score | Storefront components must not degrade merchant's Lighthouse score by more than 2 points |
| NF-08 | Multi-language | UI available in English (primary), French, Spanish, German, Italian, Portuguese from day 1 |

---

## 7. Pricing Model

| Tier | Monthly Price (EUR) | Feature Scope |
|------|-------------------|---------------|
| Free Trial | 0 (14 days) | Full features, all tiers unlocked during trial |
| Starter | 15 | Cart drawer (basic config), up to 3 bundle campaigns, core analytics |
| Growth | 35 | Full cart drawer config, unlimited campaigns, full analytics, templates |
| Pro | 50 | Everything in Growth + advanced styling, AI recommendations, priority support |
| Shopify Plus | TBD | Everything in Pro + `lineUpdate` operations, combined offers, dedicated onboarding |
| Consultant | Custom | Websitz/Holistika team configures and optimizes the app on merchant's behalf |

### Pricing Rationale

- Recurring subscriptions chosen over one-time pricing for MRR and valuation (Matt de Souza's app at ~40K EUR MRR received offers at 25M EUR valuation).
- Competitive benchmarks: Monster Upsell $12.99-$34.99, Fast Bundle ~$13.99-$29, Bundler free-$29.
- Our 15/35/50 EUR tiers are competitive while offering more combined value.
- 14-day free trial with full features maximizes adoption and reduces friction.

---

## 8. Dependencies and Constraints

| Dependency | Owner | Status |
|-----------|-------|--------|
| Shopify Dev Dashboard + dev stores | Holistika | **Done** -- `hlk-app-store.myshopify.com` (Basic) + `holistika-app-store-plus.myshopify.com` (Plus). Dev Dashboard at `dev.shopify.com/dashboard/210423805/stores`. |
| `cart_transform` function (1 per store limit) | Shopify API | Constraint -- merchants must uninstall competing bundle apps |
| `lineUpdate` restricted to Shopify Plus | Shopify API | Constraint -- gates our Plus tier features |
| Monster Upsell back-office access (via FA Slim store) | Websitz / EFA | Available -- Mathias confirmed |
| Websitz tracking specialist (GTM, Tape) | Websitz | Available for integration testing |
| OpenCloud integration | Holistika | In progress -- not blocking MVP |
| Shopify Scripts sunset (June 30, 2026) | Shopify | External deadline -- legacy Scripts permanently cease execution. Our app uses Shopify Functions natively, so no migration needed. This forces merchants off competitor apps built on Scripts, creating a migration window and acquisition opportunity. (Source: Annex ref 5, BrainSpate) |

---

## 9. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Shopify API changes break cart_transform | Low | High | Pin API version, monitor Shopify changelog, maintain buffer between Shopify updates and production deploys |
| Monster Upsell adds bundles before our launch | Medium | High | Speed to market. MVP in 1.5 months. Our analytics dashboard remains a differentiator regardless. |
| Slow adoption in first months | Medium | Medium | Freemium model + community launch (Business Brothers, Hype Labs) provides built-in initial user base |
| UX complexity overwhelms merchants | Medium | High | Strong onboarding (wizard + videos + templates). Lemlist-model tutorial content. |
| Revenue split disagreements | Low | High | Automate tracking from day 1 via Holistika admin dashboard. Formalize agreement before public launch. |
| **Shopify Scripts sunset creates forced migration** | **Opportunity** | **High (positive)** | Legacy Shopify Scripts cease execution June 30, 2026. Competitors built on Scripts will lose their installs. Our app is natively on Shopify Functions -- position as migration target. Create "migration guide" content to capture displaced merchants. (Source: Annex ref 5) |

---

## 10. Acceptance Criteria for MVP

The MVP is accepted for beta when:

1. A merchant can install the app on a Shopify dev store
2. The cart drawer slides in from the side without a full page load
3. At least 1 multi-goal progress bar is functional
4. At least 1 order bump is configurable and functional
5. At least 2 bundle display layouts (vertical + horizontal) are working
6. Volume-based and add-to-unlock campaigns can be created
7. The analytics dashboard shows per-bundle revenue and conversion data
8. The onboarding wizard walks through 3 setup steps
9. At least 3 bundle design templates are available
10. All text is translatable via i18n system
11. GTM-compatible events fire on cart actions

---

## 11. Post-MVP Roadmap

| Phase | Features | Timeline |
|-------|---------|----------|
| V1.1 | AI-powered recommendations (Madeira integration) | Month 3-4 |
| V1.2 | Post-purchase upsell module | Month 4-5 |
| V1.3 | Ambassador program with automated commission tracking | Month 4-5 |
| V1.4 | Advanced Shopify Plus features (lineUpdate, combined offers) | Month 5-6 |
| V2.0 | Full multi-channel analytics (Meta, Google, Klaviyo integration) | Month 6+ |

---

## Appendix A: Competitor Feature Matrix (Summary)

| Feature | Monster Upsell | Fast Bundle | Wayne Bundle | Bundler | **Our App** |
|---------|---------------|-------------|-------------|---------|------------|
| Cart drawer | Yes (excellent) | No | No | No | **Yes** |
| Bundles | No | Yes | Yes | Yes | **Yes** |
| Multi-goal progress | Yes | No | No | No | **Yes** |
| Order bumps | Yes | No | No | No | **Yes** |
| Design templates | Limited | Limited | Limited | Limited | **Extensive** |
| Analytics dashboard | Weak | Weak | Weak | Weak | **Strong** |
| AI recommendations | No | No | No | No | **Yes (V1.1)** |
| i18n multi-language | Partial | Partial | Partial | Partial | **Full (6+ langs)** |
| Onboarding tutorials | Basic | Basic | None | None | **Rich (Lemlist model)** |
| Price range | $12.99-$34.99 | $13.99-$29 | ~$15-$40 | Free-$29 | **15-50 EUR** |

---

## Appendix B: Glossary

- **AOV**: Average Order Value
- **CTA**: Call to Action
- **Drawer / Slide Cart**: A cart panel that slides in from the side of the screen without navigating to a new page
- **GTM**: Google Tag Manager
- **i18n**: Internationalization (multi-language support)
- **MRR**: Monthly Recurring Revenue
- **Order Bump**: A one-click addition to cart (checkbox-style) displayed near the checkout button
- **Sticky Cart**: A fixed bar on product pages that remains visible as the user scrolls
- **cart_transform**: Shopify Function API that modifies cart behavior (merging lines, expanding bundles, updating prices)
- **Madeira**: Holistika's LLM-based agent/operating system
- **OpenCloud**: AI model orchestration platform being integrated into Holistika's stack
