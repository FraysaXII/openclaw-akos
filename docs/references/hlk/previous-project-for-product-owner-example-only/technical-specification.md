# Holistika -- Technical Specification: Shopify Bundle + Cart App

**Document owner**: Fayçal, Holistika Administrator
**Version**: 1.1
**Date**: 2026-03-17 (enriched 2026-03-17)
**Status**: Draft -- pending feasibility validation (Week 1 sprint)

---

## 1. Architecture Overview

The app consists of three layers:

1. **Shopify Embedded App** -- the merchant-facing admin interface running inside Shopify Admin
2. **Storefront Extensions** -- JavaScript/Liquid injected into the merchant's storefront (cart drawer, bundles, sticky cart)
3. **Holistika Backend** -- PostgreSQL database, API layer, analytics engine, AI services, Stripe billing

```
┌─────────────────────────────────────────────────────────────┐
│                    Merchant's Shopify Store                  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Cart Drawer   │  │ Bundle       │  │ Sticky Cart       │  │
│  │ (Theme App    │  │ Display      │  │ (Theme App        │  │
│  │  Extension)   │  │ (Theme App   │  │  Extension)       │  │
│  │              │  │  Extension)   │  │                   │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘  │
│         │                 │                    │             │
│         ▼                 ▼                    ▼             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │          Shopify AJAX Cart API + cart_transform          │ │
│  │   /cart.js  /cart/add.js  /cart/update.js  /cart/change  │ │
│  └──────────────────────┬──────────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Shopify Admin (Embedded App)                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Polaris Web Components + App Bridge                 │    │
│  │  Routes: /setup /campaigns /bundles /analytics       │    │
│  └──────────────────────┬───────────────────────────────┘    │
└─────────────────────────┼───────────────────────────────────┘
                          │ HTTPS (Session Tokens)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Holistika Backend                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │ API Layer   │  │ Analytics    │  │ AI / Madeira      │   │
│  │ (Node.js)   │  │ Engine       │  │ (Post-MVP)        │   │
│  └──────┬──────┘  └──────┬───────┘  └────────┬──────────┘   │
│         │                │                    │              │
│         ▼                ▼                    ▼              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │          PostgreSQL (Row-Level Security)                 │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │          Stripe (Billing & Revenue Tracking)             │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Shopify App Stack

### 2.1 Framework

**Primary**: `@shopify/shopify-app-react-router` (recommended by Shopify as successor to Remix for new apps)

Shopify's current guidance (2025-2026):
- The `@shopify/shopify-app-remix` package (v4.2.0) is maintained but should migrate to React Router
- New apps should use `@shopify/shopify-app-react-router` directly
- Scaffolding: `npm init @shopify/app@latest`

### 2.2 UI Components

**Polaris Web Components** (framework-agnostic, GA since 2025):
- Loaded via CDN script tags -- no npm dependency for Polaris UI
- Custom HTML elements: `<s-page>`, `<s-button>`, `<s-modal>`, `<s-card>`, `<s-text>`, etc.
- Automatic design system updates from Shopify's CDN (no code changes needed)
- Covers all Shopify surfaces: App Home, Admin UI extensions, Checkout UI extensions

```html
<!-- Example: root.jsx loads -->
<script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
<script src="https://cdn.shopify.com/shopifycloud/polaris/latest/polaris.min.js"></script>
```

**Do NOT use**: Deprecated `@shopify/polaris` React library.

### 2.3 App Bridge

Required for embedded app behavior:
- Handles navigation events (`shopify:navigate`)
- Provides session token authentication
- Manages app lifecycle within Shopify Admin

### 2.4 Authentication

- **Session tokens** (mandatory for all embedded apps)
- **OAuth** for initial app installation flow
- Shopify handles the install/consent flow; we store the session in PostgreSQL

---

## 3. Shopify Functions: cart_transform

### 3.1 Overview

The `cart_transform` function is a Shopify Function that runs server-side to modify cart contents. This is the core mechanism for bundle pricing and presentation.

**Scaffold command**:
```bash
shopify app generate extension --template cart_transform
```

### 3.2 Capabilities

| Operation | Description | Availability |
|-----------|------------|-------------|
| `linesMerge` | Merge multiple cart lines into a single bundled line | All plans |
| `lineExpand` | Expand a bundled line to show individual components | All plans |
| `lineUpdate` | Override price, title, image on a cart line | **Dev stores + Shopify Plus only** |

### 3.3 Critical Constraints

1. **ONE `cart_transform` per store**: Only one app can register a `cart_transform` function per Shopify store. If a merchant has another bundle app using `cart_transform`, they must uninstall it first.
   - **Implication**: This is both a constraint and a moat. Once a merchant installs our app, switching costs are high.
   - **Marketing angle**: "Replace 2 apps with 1" messaging.

2. **`lineUpdate` restricted to Plus**: Price/title/image overrides on individual cart lines require Shopify Plus ($2,000+/month). This naturally gates our premium features.
   - **Implication**: Design the Plus tier around `lineUpdate` capabilities (custom bundle pricing display, image overrides, title customization).

3. **No nested bundles**: A bundle cannot contain another bundle.

4. **Selling plan conflict**: `lineExpand`, `linesMerge`, and `lineUpdate` operations are rejected if a selling plan (subscription) is present on the line item. Subscription integration must be carefully designed to avoid conflicts.

### 3.4 Data Storage Strategy

| Storage Method | Use Case | Security |
|---------------|---------|----------|
| **Metafields** | Fixed bundles (merchant-defined compositions) | Secure -- browser cannot modify |
| **Line item properties** | Mix-and-match bundles (buyer chooses components) | Requires validation -- browser can modify |

For mix-and-match bundles, the `cart_transform` function must validate line item properties against the store's actual product catalog to prevent manipulation.

### 3.5 API Version

Target: **2025-07 or higher** for full `cart_transform` function support.

### 3.6 Shopify Scripts Deprecation & Migration Context

**Critical external deadline**: Legacy Shopify Scripts permanently cease execution on **June 30, 2026** (source: BrainSpate / Shopify changelog). All custom checkout logic, discounting structures, and bundling mechanisms built on the Ruby-based Scripts engine must be migrated to Shopify Functions before that date.

**Impact on our app**: None -- our app is natively built on Shopify Functions / `cart_transform`. No migration is required. This is a **competitive advantage**: merchants currently using older bundle or cart apps that rely on Shopify Scripts will be forced to switch. Our app is a natural migration target.

**Implementation language options**:
- **JavaScript (recommended for MVP)**: Scaffolded by `shopify app generate extension`. Pragmatic, fast iteration, familiar to the team.
- **Rust / WebAssembly (optional, performance path)**: Compiles to `wasm32-unknown-unknown`. Achieves sub-5ms execution latency. Consider for V1.1+ if performance profiling shows JavaScript is a bottleneck during high-traffic events. Requires Rust toolchain and WebAssembly compilation pipeline in CI/CD.

**Architecture Migration Reference** (Legacy Shopify Scripts vs. 2026 Shopify Functions):

| Component | Legacy (Shopify Scripts -- deprecated) | 2026 Standard (Shopify Functions / cart\_transform) |
|-----------|---------------------------------------|---------------------------------------------------|
| **Execution environment** | Ruby-based scripts on Shopify servers | WebAssembly (Wasm) or JavaScript deployed via Shopify Functions |
| **Execution latency** | Slower, subject to throttling during high traffic | Sub-5ms (Wasm) or ~10-50ms (JS), natively integrated into Checkout Extensibility |
| **Inventory synchronization** | Prone to phantom stockouts; relies on async third-party apps | Native component expansion; individual SKUs deducted accurately at checkout |
| **Data storage / rules** | Hardcoded conditional logic within monolithic script files | Dynamic retrieval via MetafieldsSet mutations linked to the CartTransform object |
| **POS integration** | Limited to online storefronts; manual reconciliation for physical retail | Native support for dynamic bundles on Shopify POS with UI extension targets (2026) |

---

## 4. Storefront Components

### 4.1 Cart Drawer (Theme App Extension)

The cart drawer is a **Theme App Extension** that injects into the merchant's storefront theme.

**Technology**: Vanilla JavaScript + CSS (no heavy framework to minimize load impact)

**Integration points**:
- Hooks into Shopify's AJAX Cart API:
  - `GET /cart.js` -- read current cart state
  - `POST /cart/add.js` -- add items (order bumps, gift unlocks)
  - `POST /cart/update.js` -- update quantities
  - `POST /cart/change.js` -- change line item properties
- Listens for `cart:add` and `cart:change` custom events from the theme
- Emits custom GTM-compatible events (see Section 7)

**Performance target**: < 200ms added page load time. Achieved through:
- Lazy loading (drawer JS loads on first cart interaction, not on page load)
- CSS inlined for above-the-fold, deferred for drawer panel
- No external framework dependency (no React/Vue on storefront)
- Assets served from Shopify's CDN (automatically global)

#### 4.1.1 Design Constraints (Research-Backed)

The following behavioral constraints are derived from 2026 merchant data and UX research. They are mandatory design rules for the cart drawer implementation:

| Constraint | Rule | Rationale | Source |
|-----------|------|-----------|--------|
| **Mobile-first baseline grid** | 375px minimum viewport width | Dominant traffic from social media (Facebook/Instagram ads) is mobile. The drawer must be fully functional at 375px. | Annex ref 12 (Oxify 2026) |
| **Maximum upsell suggestions** | 2-3 items per drawer session | Exceeding 3 upsells triggers decision paralysis, depressing conversion rates. | Annex ref 13 (Growth Suite 2026) |
| **Upsell price ceiling** | Upsell items priced below 30% of total cart value | Higher-priced suggestions feel exploitative and increase cart abandonment. Configurable per merchant. | Annex ref 13 (Growth Suite 2026) |
| **No URL redirect on add-to-cart** | Adding a product to cart must NOT navigate to a new page | Maintaining the user's context on the product or collection page drastically reduces cart abandonment. Drawer opens in-place. | Annex ref 12 (Oxify 2026) |
| **Progress bar anchoring** | Free shipping and discount threshold progress bars must be visually prominent | Exploits the psychological anchoring effect, driving incremental AOV increases. 3.2X revenue multiplier for optimized drawers vs. 2.2X for basic cart pages. | Annex ref 14 (Appfox 2026) |

### 4.2 Bundle Display (Theme App Extension)

Renders on product pages and collection pages.

**Rendering approach**:
- App block that merchants place via Shopify's theme editor (drag and drop)
- Renders bundle options (vertical/horizontal layouts, swatches, gift unlocks)
- On selection, calls AJAX Cart API to add the bundle components with proper metafields/line item properties
- The `cart_transform` function then merges/expands the bundle server-side

### 4.3 Sticky Cart (Theme App Extension)

Fixed bar on product pages.

**Behavior**:
- Appears on scroll (configurable: after X pixels or when "Add to Cart" button leaves viewport)
- Shows: product name, price, quick-add button, cart item count
- Clicking opens the cart drawer (CD-01)

---

## 5. Holistika Backend Architecture

### 5.1 Database: PostgreSQL

**Existing infrastructure** -- already operational with row-level security (RLS).

#### Schema Design (Core Tables)

```
merchants
├── id (UUID, PK)
├── shopify_shop_domain (VARCHAR, unique)
├── shopify_access_token (VARCHAR, encrypted)
├── subscription_tier (ENUM: trial, starter, growth, pro, plus)
├── stripe_customer_id (VARCHAR)
├── installed_at (TIMESTAMP)
├── settings_json (JSONB)  -- global app settings
└── locale (VARCHAR)       -- merchant's preferred language

campaigns
├── id (UUID, PK)
├── merchant_id (FK -> merchants)
├── type (ENUM: volume, add_to_unlock, one_click_upsell, buy_x_get_y)
├── name (VARCHAR)
├── config_json (JSONB)   -- rules, thresholds, products, discounts
├── status (ENUM: draft, active, paused, ended)
├── starts_at (TIMESTAMP, nullable)
├── ends_at (TIMESTAMP, nullable)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

bundles
├── id (UUID, PK)
├── merchant_id (FK -> merchants)
├── campaign_id (FK -> campaigns, nullable)
├── name (VARCHAR)
├── layout (ENUM: vertical, horizontal)
├── template_id (VARCHAR)  -- references design template
├── products_json (JSONB)  -- product IDs, variants, quantities, discount rules
├── gift_product_id (VARCHAR, nullable)
├── gift_threshold (DECIMAL, nullable)
├── status (ENUM: draft, active, paused)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

cart_configs
├── id (UUID, PK)
├── merchant_id (FK -> merchants, unique)
├── drawer_enabled (BOOLEAN)
├── sticky_cart_enabled (BOOLEAN)
├── multi_goals_json (JSONB)    -- array of {type, threshold, reward}
├── order_bumps_json (JSONB)    -- array of {product_id, placement, text}
├── payment_badges_json (JSONB) -- array of {provider, logo_url}
├── banner_json (JSONB)         -- {text, bg_color, countdown_end}
├── custom_text (TEXT)
├── styling_json (JSONB)        -- CSS overrides
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

analytics_events
├── id (UUID, PK)
├── merchant_id (FK -> merchants)
├── event_type (ENUM: drawer_open, bundle_view, bundle_add, bump_add,
│               gift_unlock, checkout_start, purchase_complete)
├── campaign_id (FK -> campaigns, nullable)
├── bundle_id (FK -> bundles, nullable)
├── cart_total (DECIMAL)
├── revenue_attributed (DECIMAL, nullable)
├── metadata_json (JSONB)
├── created_at (TIMESTAMP)
└── session_id (VARCHAR)   -- anonymous session tracking

design_templates
├── id (VARCHAR, PK)      -- e.g., "minimal-horizontal", "bold-vertical"
├── name (VARCHAR)
├── category (ENUM: bundle, cart_drawer, sticky_cart)
├── preview_image_url (VARCHAR)
├── css_template (TEXT)
├── html_template (TEXT)
├── is_premium (BOOLEAN)
└── created_at (TIMESTAMP)
```

**Row-Level Security**: Each query is scoped to the authenticated merchant's `merchant_id`. No cross-tenant data access is possible at the database level.

### 5.2 API Layer

**Runtime**: Node.js (aligns with Shopify's ecosystem and `@shopify/shopify-app-react-router`)

**API endpoints** (RESTful):

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/campaigns` | List merchant's campaigns |
| POST | `/api/campaigns` | Create campaign |
| PUT | `/api/campaigns/:id` | Update campaign |
| DELETE | `/api/campaigns/:id` | Delete campaign |
| GET | `/api/bundles` | List merchant's bundles |
| POST | `/api/bundles` | Create bundle |
| PUT | `/api/bundles/:id` | Update bundle |
| DELETE | `/api/bundles/:id` | Delete bundle |
| GET | `/api/cart-config` | Get merchant's cart drawer configuration |
| PUT | `/api/cart-config` | Update cart drawer configuration |
| GET | `/api/analytics` | Query analytics (params: date_range, granularity, campaign_id, bundle_id) |
| POST | `/api/analytics/events` | Ingest analytics event from storefront |
| GET | `/api/templates` | List available design templates |
| GET | `/api/merchant/settings` | Get merchant settings |
| PUT | `/api/merchant/settings` | Update merchant settings |

**Authentication**: All API calls authenticated via Shopify session tokens. The token is validated against Shopify's API, and the `shop` domain is extracted to scope database queries.

### 5.3 Stripe Integration

Holistika's Stripe integration handles:
- **Subscription billing**: App subscription charges (15/35/50 EUR tiers) via Shopify's Billing API (preferred) or Stripe as fallback
- **Revenue tracking**: Internal dashboard for Holistika/Websitz revenue split
- **Ambassador commissions**: Automated payout tracking (V1.3)

**Note**: Shopify's Billing API is the recommended method for charging merchants (Shopify takes a commission but handles all billing UI). Stripe is used for internal revenue management and the admin dashboard.

### 5.4 Capacity

Already validated:
- 100M users/month throughput
- 500K concurrent API calls
- PostgreSQL with connection pooling
- Global CDN for static assets (Next.js deployment)

For the Shopify app specifically, expected load at 5,000 merchants:
- ~50K API calls/hour (campaign/config reads)
- ~500K analytics events/day (cart interactions)
- Well within existing capacity

---

## 6. Deployment Architecture

### 6.1 Environments

| Environment | Purpose | URL Pattern |
|------------|---------|-------------|
| Development (Basic) | Local development + primary dev store | `localhost:3000` + ngrok tunnel -> `hlk-app-store.myshopify.com` |
| Development (Plus) | `lineUpdate` and Plus-exclusive feature testing | `localhost:3000` + ngrok tunnel -> `holistika-app-store-plus.myshopify.com` |
| Staging | QA testing with real Shopify data | `staging.app.holistika.io` |
| Production | Live merchants | `app.holistika.io` |

### 6.2 CI/CD

- Code repository (to be set up)
- Automated tests on push
- Staging deploy on PR merge to `develop`
- Production deploy on release tag to `main`
- Shopify CLI for extension deployment: `shopify app deploy`

### 6.3 Monitoring

- Application logs -> centralized logging
- Error tracking (Sentry or equivalent)
- Uptime monitoring (99.9% target)
- Performance metrics (API response times, storefront load impact)

---

## 7. GTM / Tracking Integration

### 7.1 Custom Events Emitted

The storefront components emit `dataLayer.push()` events for Google Tag Manager:

| Event Name | Trigger | Data |
|-----------|---------|------|
| `holistika_drawer_open` | Cart drawer slides open | `{ cart_total, item_count }` |
| `holistika_drawer_close` | Cart drawer closes | `{ cart_total, item_count }` |
| `holistika_bundle_view` | Bundle display becomes visible | `{ bundle_id, bundle_name, products }` |
| `holistika_bundle_add` | Bundle added to cart | `{ bundle_id, bundle_name, bundle_price, products }` |
| `holistika_bump_add` | Order bump checked/added | `{ product_id, product_name, price }` |
| `holistika_bump_remove` | Order bump unchecked/removed | `{ product_id, product_name }` |
| `holistika_gift_unlock` | Free gift threshold reached | `{ gift_product_id, threshold, cart_total }` |
| `holistika_goal_progress` | Progress bar updates | `{ goal_type, current_total, threshold, percentage }` |
| `holistika_goal_complete` | Progress bar goal reached | `{ goal_type, reward }` |
| `holistika_sticky_click` | Sticky cart CTA clicked | `{ product_id, action }` |

### 7.2 Server-Side Tracking Compatibility

Websitz uses Tape for server-side Shopify tracking. Our events:
- Are emitted to the `dataLayer` (standard GTM pattern)
- Include Shopify cart token for server-side correlation
- Do not require additional client-side scripts beyond GTM

### 7.3 Shopify Cart API State

All cart state changes flow through Shopify's AJAX Cart API, meaning:
- Shopify's own analytics capture cart events
- Our app augments with granular bundle/bump/goal events
- Server-side tracking tools (Tape) can correlate via cart token

---

## 8. i18n (Internationalization)

### 8.1 Approach

Holistika's existing programmatic translation library handles:
- **Admin UI text**: All labels, descriptions, tooltips translatable via JSON locale files
- **Storefront text**: Merchant-editable text (banner, CTA, progress bar labels) stored per-locale in `settings_json`
- **Tutorial videos**: French source, auto-translated audio/subtitles for 6+ languages

### 8.2 Supported Languages (Launch)

| Language | Code | Priority |
|---------|------|----------|
| English | `en` | Primary (global market) |
| French | `fr` | Primary (home market) |
| Spanish | `es` | Secondary |
| German | `de` | Secondary |
| Italian | `it` | Secondary |
| Portuguese | `pt` | Secondary |

Additional languages added post-launch based on merchant demand.

---

## 9. Security

### 9.1 Data Protection

- **Row-Level Security (RLS)** in PostgreSQL: Every query is scoped to the authenticated merchant. No cross-tenant data access.
- **Encrypted tokens**: Shopify access tokens encrypted at rest in the database
- **Session tokens**: Shopify's session token mechanism (no long-lived API keys stored client-side)
- **HTTPS everywhere**: All API calls over TLS
- **No PII in analytics**: Analytics events use anonymous session IDs, not customer identifiers

### 9.2 Shopify App Store Compliance

Mandatory requirements:
- Session token authentication (no cookie-based auth)
- Proper OAuth flow with minimal permission scopes
- No popup-dependent essential functionality
- Factual information only in app listing
- Shopify checkout must not be bypassed
- Data deletion webhook handler (GDPR)

### 9.3 AI Act Compliance (Post-MVP)

When AI features are introduced (V1.1):
- Full traceability of every AI-generated recommendation (timestamp, model used, input context, output)
- Stored in Holistika's compliance log (already operational for Madeira)
- Merchants can audit AI recommendations affecting their store

---

## 10. Development Prerequisites

### 10.1 Required Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 18+ (LTS recommended) | Runtime |
| Shopify CLI | Latest | App scaffolding, extension generation, deployment |
| npm/yarn | Latest | Package management |
| PostgreSQL | 15+ | Database (already operational) |
| Rust toolchain (optional) | Latest stable | If `cart_transform` is written in Rust (alternative: JavaScript) |

### 10.2 Shopify Setup

1. **Shopify Dev Dashboard**: Active at `https://dev.shopify.com/dashboard/210423805/stores` (Holistika organization). Created by Fayçal Njoya.
2. **Primary dev store (Basic)**: `hlk-app-store.myshopify.com` -- general development and testing. Extended Variants enabled.
3. **Plus dev store**: `holistika-app-store-plus.myshopify.com` -- `lineUpdate` testing and Plus-exclusive feature validation. Extended Variants enabled.
4. **App registration**: Register app in Dev Dashboard to get API keys.
5. **Extension registration**: Register `cart_transform` function extension.

### 10.3 Scaffold Commands

```bash
# Create the app
npm init @shopify/app@latest -- --template remix

# Generate cart_transform extension
shopify app generate extension --template cart_transform --name holistika-bundles

# Generate theme app extension (for cart drawer, bundle display, sticky cart)
shopify app generate extension --template theme_app_extension --name holistika-storefront

# Start development server
shopify app dev
```

---

## 11. Testing Strategy

| Level | Tool | Coverage |
|-------|------|----------|
| Unit tests | Vitest / Jest | API handlers, data transformations, analytics calculations |
| Integration tests | Shopify CLI dev mode | cart_transform function behavior, AJAX Cart API interaction |
| E2E tests | Playwright / Cypress | Full merchant flows (install, configure, preview, checkout) |
| Performance tests | Lighthouse CI | Storefront load impact < 200ms, no Lighthouse score degradation > 2 points |
| Beta testing | Websitz client stores | Real merchant stores with real traffic |

---

## 12. Week 1 Feasibility Checklist

Before committing to the full build, validate in Week 1:

- [x] Shopify Dev Dashboard active and dev stores created (`hlk-app-store.myshopify.com` Basic + `holistika-app-store-plus.myshopify.com` Plus)
- [ ] App scaffolded with `@shopify/shopify-app-react-router`
- [ ] `cart_transform` function deployed to dev store and modifying cart behavior
- [ ] AJAX Cart API calls working (add, update, change) from custom JavaScript
- [ ] Theme App Extension rendering a basic component on the storefront
- [ ] Polaris web components rendering in embedded admin app
- [ ] PostgreSQL connection from app server confirmed
- [ ] Session token authentication flow working end-to-end
- [ ] Basic data round-trip: create campaign in admin -> stored in DB -> affects storefront behavior

If all items pass, proceed to full build. If any fail, document blockers and adjust timeline.
