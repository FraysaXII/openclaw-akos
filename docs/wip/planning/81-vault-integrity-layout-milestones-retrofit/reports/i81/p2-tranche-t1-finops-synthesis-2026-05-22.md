---
language: en
intellectual_kind: synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-22
last_review: 2026-05-22
status: review
verdict: PENDING-OPERATOR-WALK
closure_decision_source: agent_inline_default
ratifying_decisions:
  - D-IH-81-N
linked_runbooks:
  - scripts/validate_finops_counterparty_register.py
  - scripts/sync_compliance_mirrors_from_csv.py
  - scripts/stripe_set_billing_plane.py
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv
  - docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md
  - docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/SOP-FOUNDER_COMPANY_FUNDING_001.md
  - docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-FINOPS_BRIDGE_001.md
linked_initiatives:
  - INIT-OPENCLAW_AKOS-14
  - INIT-OPENCLAW_AKOS-16
  - INIT-OPENCLAW_AKOS-18
  - INIT-OPENCLAW_AKOS-19
  - INIT-OPENCLAW_AKOS-72
  - INIT-OPENCLAW_AKOS-81
external_references:
  - Stripe (2026). SaaS revenue recognition 101. https://stripe.com/en-gi/resources/more/a-guide-to-revenue-recognition-for-saas-businesses
  - Stripe (2026). Revenue recognition principles & best practices. https://stripe.com/guides/introduction-to-revenue-recognition
  - HighRock CPA (2026). SaaS Revenue Recognition ASC 606 — Founder Audit Guide.
  - NetSuite (2026). Revenue Recognition Complete Guide for SaaS.
  - Fractional CFO School (2026). CFO as a Service — What it Is, How it Works, Cost.
  - Level CFO (2026). Fractional CFO for SaaS & Software Startups — ARR, NRR, QSBS, Burn.
  - SaaS Fractional CFO UK (2026). Fractional CFO services menu.
  - Sincro (2026). Cómo constituir una sociedad en España en 2026.
  - Vademecum Legal (2026). Deducción IRPF por inversión en empresas de nueva o reciente creación.
  - AEAT Sede Electrónica (2026). Información sobre Haciendas Forales: Bizkaia + Gipuzkoa.
  - AEAT (2026). Modelo 720 — declaración informativa bienes en el extranjero.
  - Supplier.io / TealBook / Semarchy (2026). Vendor master data SSOT + governance.
---

# FINOPS End-to-End Synthesis — operator-engagement gate before I81 P2 Tranche T1

> Authored 2026-05-22 by Madeira (current AI O5-1) at operator request during Wave R lane D execution. The operator's framing verbatim: *"i'd really need yo to explain the end to end in plain terms but complete governed and true so i can know how far we are from our ideal finops scenario. Help me by challenging every aspect not only of T4 but any other, from as many points of view as you can. i have more knowledge in the head than what you can see minted or in the backlog so i need to be sure my methodology stands its ground every time and amend where it's not. or create what's lacking. of course, i'd need yo to research inwards and outwards to help me as my assistant and delegated expert"*.

This synthesis is the agent-side discharge of that framing. It is **not** a closure UAT and it is **not** a charter. It is a **gating governance synthesis** — the document the operator reads before consenting to advance I81 P2 Tranche T1 (`FINOPS_COUNTERPARTY_REGISTER.csv` → `finops/`), and the document Holistika reuses every time FINOPS doctrine is touched downstream. Decision row **D-IH-81-N** ratifies the synthesis itself (the methodology, the framing, the gap-list); concrete deltas raised here are forward-chartered as **OPS-81-FINOPS-1..N** rows for follow-up execution.

> **How to read this document.** Each section has a *Plain* sub-section (one paragraph) + a *Governed* sub-section (which canonical / Pydantic / process / mirror is the SSOT) + an *Ideal vs Current* gap call + a *Multi-perspective challenge*. The operator amends in-place; the agent appends each amendment to a §10 "Operator amendments" log so the synthesis stays auditable across iterations.

---

## 0. TL;DR — eight load-bearing claims, one paragraph each

1. **FINOPS is not one thing.** It is the join of five planes: counterparty metadata (vendors/customers/partners), revenue facts (Stripe + manual invoices), expense facts (vendor spend + founder reimbursements), capital facts (founder contributions, future investors, ENISA loan), and tax facts (IRPF, IRC, Modelo 720, R&D credits). Each plane has its own system of record; FINOPS is the contract that says how they join. Today only plane 1 (counterparty metadata) is canonically governed in git. Planes 2-5 are mostly off-repo or schema-only.

2. **CFO is a role we don't have yet.** Holistika today is operator + Madeira (AI O5-1). The Business Controller role exists in `baseline_organisation.csv` but is unactivated. Until that role is operator-assigned (founder dual-hat OR external CFOaaS contracted), FINOPS doctrine is **agent-readable + operator-executable**; it cannot yet be CFO-executable. This is the most consequential framing in the synthesis and it changes which gaps are "real" vs "deferred-by-design".

3. **The canonical counterparty register is a metadata SSOT, not a ledger.** `FINOPS_COUNTERPARTY_REGISTER.csv` carries vendor + customer + partner *master data* (name, type, billing model, segment, contract pointer, status). It never carries money. That separation is correct per ASC 606 / IFRS 15 + vendor-master-data industry pattern (Supplier.io, TealBook, Semarchy 2026), but Holistika has only **2 seed rows** in it today — the register exists architecturally without being *populated*. This is the highest-priority gap.

4. **Stripe is the payment truth, not the revenue truth.** Stripe FDW (`stripe_gtm` schema + `stripe_gtm_server`) gives read-only Postgres access to Stripe data; `holistika_ops.stripe_customer_link.finops_counterparty_id` bridges Stripe rows to register slugs. But Stripe payment-collected ≠ revenue-recognized. The 73% of SaaS companies under $10M ARR that record annual payments upfront (per HighRock 2026) is the failure mode this separation is meant to prevent. Holistika has the architecture; it does not yet have the recognition policy or the books.

5. **`finops.registered_fact` is the future ledger; today it is one table.** Initiative 19 P1 (2026-04-23) shipped the `finops.registered_fact` DDL — a single discriminated table for monetary facts joined to counterparty_id. It is RLS-locked to `service_role`. **Nothing has written to it yet.** Phase 2 (writers + UAT) is unscheduled. This is correct — we shouldn't write monetary amounts before entity formation + CFO alignment (gate `thi_finan_dtp_306`) — but it means FINOPS is "schema-ready, fact-empty" today.

6. **Founder funding is documented but not lived.** `SOP-FOUNDER_COMPANY_FUNDING_001` + `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04` describe the capital-contribution / shareholder-loan / reimbursement decision matrix. The decision note recommends `EUR 1,000` operating buffer minimum + `~3x active monthly burn` as healthier target. The actual founder ledger (what's been spent, what's been reimbursed, what's a loan, what's a capital contribution) does not yet exist in any system Holistika owns. This becomes a real liability the moment entity formation closes.

7. **Spain tax surface is operator-aware but agent-blind.** Modelo 200 (IS), Modelo 720 (bienes extranjeros), Hacienda Foral Bizkaia / Gipuzkoa territoriality, IRPF deduction for `empresas de nueva o reciente creación` (50% up to €100K base, requires equity ≤ €400K), pluriactividad quota benefit, ENISA reporting obligation, R&D credit (`deducción I+D`) — none of these are encoded in any FINOPS-readable canonical. They live in [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md) as `Q-FIS-001`, `Q-LEG-004`, `Q-CRT-001` etc. Until those answers come back and get encoded as canonical doctrine, FINOPS planning is operator-head + adviser-routed, not agent-readable.

8. **The advisor/handoff path is in good shape; the post-handoff feedback loop is not.** ADVOPS plane (`hol_opera_ws_5`, `EXTERNAL_COUNSEL_HANDOFF_PACKAGE`, `ADVISER_OPEN_QUESTIONS.csv`, `FOUNDER_FILED_INSTRUMENTS.csv`, GOI/POI register, [`export_adviser_handoff.py`](../../../../../scripts/export_adviser_handoff.py)) is the most mature governance surface for the founder-incorporation phase. But there is **no canonical receiving slot for adviser answers** — when fiscal counsel answers `Q-FIS-001`, the answer becomes a memo in legal/ ; FINOPS doesn't pick it up unless the operator hand-routes. That's the failure mode T1 + downstream synthesis must close.

---

## 1. Plane inventory — what's actually in scope when we say "FINOPS"

### 1.1 The five planes

| # | Plane | What lives here | Today's system of record | Doctrine status |
|:--|:---|:---|:---|:---|
| 1 | **Counterparty metadata** | Vendors + customers + partners: name, type, billing model, segment, contract pointer, status, PCI/PHI/PII scope | `FINOPS_COUNTERPARTY_REGISTER.csv` (git) + `compliance.finops_counterparty_register_mirror` (Postgres) | Architectural complete (Initiative 18 closed 2026-04-23); populated with **2 seed rows** only |
| 2 | **Revenue facts** | What customers paid + what Holistika earned (recognized) | Stripe API (paid); **nowhere** (recognized) | Stripe FDW exists; ASC 606 / IFRS 15 recognition policy unauthored |
| 3 | **Expense facts** | What Holistika paid vendors + what the founder paid out of pocket | Vendor invoices (off-repo); founder receipts (off-repo); future `finops.registered_fact` | Schema exists (`finops.registered_fact`); zero writers; founder ledger does not exist |
| 4 | **Capital facts** | Founder capital contribution + founder shareholder loans + future ENISA loan + future investor SAFE/equity | Off-repo (notary deed pending); future `finops.registered_fact` + ENISA program filings | Authoring SOP exists (`SOP-FOUNDER_COMPANY_FUNDING_001`); no live ledger |
| 5 | **Tax facts** | IRPF + IRC + Modelo 720 + Modelo 200 + Hacienda Foral filings + R&D credit claims + ENISA reporting | AEAT + Hacienda Foral (when filed) | Operator-aware via [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md); zero canonical encoding |

### 1.2 What's *not* in scope (deliberately)

- **Card data + raw PCI** — never in git; never in mirrors; never in `finops.registered_fact`. Stays in Stripe.
- **Personal IRPF of the founder** — outside Holistika legal-entity scope; the founder's personal `EUR 150-500/month` operating-cost baseline is operator-private, captured in `FOUNDER_CAPITALIZATION_DECISION_NOTE` as a *working planning input, not an accounting fact*.
- **HR payroll** — not in scope until first hire. People Operations canonicals will own; FINOPS will consume via counterparty_type=employee row (forward-charter).

---

## 2. The counterparty register — plane 1 deep-dive (the immediate gating concern for T1)

### 2.1 Plain
The counterparty register is the canonical list of every commercial counterparty Holistika has — every vendor we buy from, every customer we sell to, every partner we share revenue with. Each row is one counterparty + classification metadata (what kind of counterparty, what billing model, what segment, who owns the relationship inside Holistika, where the contract is stored). It deliberately does not carry money — money lives in Stripe + future `finops.registered_fact`. The register is the *thing every other plane joins to*.

### 2.2 Governed
- **SSOT**: [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) — 22-column tuple per [`akos/hlk_finops_counterparty_csv.py`](../../../../../akos/hlk_finops_counterparty_csv.py) `FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES`.
- **Validator**: [`scripts/validate_finops_counterparty_register.py`](../../../../../scripts/validate_finops_counterparty_register.py) — FK to `process_list.csv`, `baseline_organisation.csv`, `COMPONENT_SERVICE_MATRIX.csv`, enum checks, status whitelist, duplicate-counterparty_id check.
- **Mirror**: `compliance.finops_counterparty_register_mirror` (Postgres; `service_role` writes; RLS deny anon/authenticated).
- **Sync runbook**: `py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only`.
- **SOP (human-facing)**: [`SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001`](../../../../references/hlk/v3.0/Admin/O5-1/Finance/Business%20Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md) (Business Controller-owned).
- **Process catalogue**: `thi_finan_ws_4` (FINOPS and counterparty economics workstream) — anchors `thi_finan_dtp_303` (register maintenance) → `dtp_304` (onboarding/offboarding) → `dtp_305` (data classification) → `dtp_306` (legal+entity readiness gate) → `dtp_307` (annual renewal review) → `dtp_309` (customer segment/revenue metadata) → `dtp_308` (Stripe FDW stewardship).
- **Bridge SOP**: [`SOP-FINOPS_BRIDGE_001`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-FINOPS_BRIDGE_001.md) — RevOps spine event-triggered handoff: engagement signed → counterparty validated → Stripe customer linked → `finops.registered_fact.engagement_id` backfill.

### 2.3 Ideal vs current

| Concern | Ideal state | Current state | Gap class |
|:---|:---|:---|:---|
| Population | Every vendor + customer + partner Holistika has touched in 2026 is a row | 2 seed rows | **CRITICAL — backfill** |
| Onboarding pattern | New vendor signed → row added same-day before invoice posts | No new vendor has been formally onboarded; ad-hoc | Doctrine-ready, not exercised |
| Renewal review cadence | Annual sweep (`thi_finan_dtp_307`) | Never run (nothing to sweep) | Blocked-on-population |
| Sensitivity classification | Every row carries `pci_phi_pii_scope` ∈ {none, pii, phi, pci} | Both seed rows have `none`; no PCI/PHI-bearing counterparty exists yet | OK by construction |
| Mirror sync | Every CSV commit triggers operator-mediated mirror sync | DDL exists; mirror has 2 rows matching CSV | OK — operator-discipline-enforced |
| AIC consumption | Madeira reads register row to validate engagement before drafting any FINOPS-touching artifact | Madeira reads register only when validators force-resolve FKs | Pattern-exists, not-exercised |

### 2.4 Multi-perspective challenge

- **CFO perspective (hypothetical, since role unactivated)**: "Where is the vendor concentration analysis? Two rows is not a register; it's a placeholder. I need to see at minimum the recurring SaaS spend (OpenAI, Anthropic, Stripe, Cloudflare, Vercel, Render, Supabase, GitHub, Cal.com, Resend, Sentry, Langfuse — every dollar-bearing service Madeira invokes) before I can sign off on a budget."
- **Auditor perspective**: "Where is the dual-control? CSV-as-SSOT + git history is a *log*, not a *control*. Who approves a new vendor row? Today the answer is 'whoever has commit access', i.e. the founder. That's fine for AL5 pre-CFO; it breaks the moment you onboard external collaborators."
- **Founder perspective**: "I have a list in my head of every service I've signed up for. Why is that list not in the register?" → Answer: because the inventory pass hasn't happened. This is the OPS-81-FINOPS-1 the synthesis is going to forward-charter.
- **AIC / agent perspective (Madeira)**: "The bridge SOP-FINOPS_BRIDGE_001 tells me to check the register before authoring engagement artifacts. The register has 2 seed rows. So either every engagement I touch trips the bridge gate (because the counterparty isn't registered) or I silently bypass. I bypass. That's a discipline gap I should surface."
- **Investor / ENISA perspective**: "Show me your vendor list. Show me your customer list. Show me your concentration risk. Show me your unit economics." → All three answers route to the counterparty register. Until populated, all three are unanswerable.
- **Legal counsel perspective**: "Every counterparty needs a contract pointer. Every contract pointer needs a renewal date. Every renewal date needs a sweep. The register is the join surface for `FOUNDER_FILED_INSTRUMENTS.csv`." → Today no FOUNDER_FILED_INSTRUMENTS row has a counterparty_id back-reference because nothing has been filed yet.
- **Customer perspective (future)**: "When Holistika invoices me, who in Holistika is accountable for the relationship?" → Today: the founder, by default. Register `role_owner` cell encodes this; it's empty for customers because there are no customer rows yet.

### 2.5 What T1 actually changes (and doesn't)

T1 moves `FINOPS_COUNTERPARTY_REGISTER.csv` from `compliance/canonicals/` to `compliance/canonicals/finops/`, mints the `finops/` plane subdirectory per I22 forward layout, updates ~12 consumer surfaces (validators, PRECEDENCE, CANONICAL_REGISTRY, README, SOP cross-references, USER_GUIDE, ARCHITECTURE, vault index, migration manifest, files-modified.csv), and adds the deprecation alias for one initiative cycle.

T1 does **not**:
- Add rows to the register.
- Change the schema.
- Touch Postgres (mirror table name stays `compliance.finops_counterparty_register_mirror`).
- Touch Stripe.
- Touch `finops.registered_fact`.
- Address any of the §2.3 gaps above.

T1 is **layout hygiene**. The substantive doctrine work this synthesis surfaces is forward-chartered to OPS rows (§9).

---

## 3. Revenue plane — Stripe truth vs recognition truth

### 3.1 Plain
Stripe knows what customers paid. It does not know what Holistika earned. "Paid" and "earned" are different concepts; the gap between them is called *deferred revenue* (collected but not yet earned), and getting it wrong is the most common SaaS accounting failure (73% of <$10M ARR SaaS companies per HighRock 2026). For Holistika today this is zero-risk because there are zero customers. For Holistika in 6 months when KiRBe SaaS goes live, this becomes the most consequential FINOPS doctrine call to make.

### 3.2 Governed
- **Payment truth**: Stripe API + Stripe FDW (`stripe_gtm` schema; foreign tables behind `stripe_gtm_server`).
- **Routing**: [`scripts/stripe_set_billing_plane.py`](../../../../../scripts/stripe_set_billing_plane.py) sets `metadata.hlk_billing_plane = 'kirbe' | 'holistika_company'` on Stripe customers; webhook router (`supabase/functions/stripe-webhook-handler/`) dispatches based on the metadata.
- **Two-plane bridge**: `holistika_ops.stripe_customer_link.finops_counterparty_id` (company plane); `kirbe.subscription` (product plane).
- **Process catalogue**: `thi_finan_dtp_261` (KiRBe Stripe Billing Activation + Reconciliation); `thi_finan_dtp_308` (Stripe FDW stewardship); `thi_finan_dtp_301` (Revenue share automation — partnerships).
- **Future ledger**: `finops.registered_fact` will eventually carry recognized revenue facts joined to `counterparty_id` + `stripe_customer_id` + `stripe_subscription_id` + `engagement_id`. Phase 2 writers unscheduled.
- **Pricing doctrine**: `thi_finan_dtp_125`/`126` (Budget Scope + Pricing Definition); `thi_finan_dtp_203` (Subscription Pricing Strategy — trial/starter/growth/pro/plus/consultant tiers; competitive benchmark; revenue-split for partnerships).
- **Lead-to-revenue spine**: `thi_finan_dtp_271` (BID Lead-to-Contract Revenue Chain — lead → product/workstream IDs → contract → revenue tables → finance handoff).

### 3.3 Ideal vs current

| Concern | Ideal | Current | Gap class |
|:---|:---|:---|:---|
| Revenue recognition policy | Authored, accountant-reviewed, encoded as canonical doctrine | None | **CRITICAL — author** |
| ASC 606 / IFRS 15 stance | Holistika commits to IFRS 15 (Spain GAAP-equivalent) explicitly | Not declared | Author-blocker |
| Performance obligations taxonomy | Per pricing-tier (trial/starter/growth/pro/plus/consultant + consulting engagement) carries explicit performance obligations + recognition schedule (ratable / on-delivery / on-milestone) | Tiers exist (`dtp_203`); recognition schedule does not | Author-blocker |
| Deferred revenue handling | Annual prepayments recorded as liability, recognized monthly | No customer; no deferred revenue yet | Doctrine-needed-before-first-sale |
| Revenue-share automation | Stripe dashboards + Postgres views show partner shares deterministically (`thi_finan_dtp_301`) | Nothing wired; no partners yet | Architecture-ready |
| FDW privilege hardening | `stripe_gtm_server` is operator-only; `service_role` only for materialised views; no browser/anon exposure (`thi_finan_dtp_308`) | Posture documented; access review never run | Posture-OK-by-construction; never audited |
| MRR/ARR/churn reporting | Per-plane (KiRBe SaaS vs Holistika company) dashboards refreshed monthly | Zero customers → zero MRR | Blocked-on-customer |

### 3.4 Multi-perspective challenge

- **CFO perspective**: "What's your billing model per pricing tier? Where is the customer success motion? Who handles deferred revenue at the end of period? Where do refunds land in the ledger?" → All open.
- **Auditor perspective**: "Show me how a $12,000 annual subscription is recognized monthly (Stripe vs books). Show me your evidence chain from invoice → bank → revenue ledger → tax declaration." → No chain exists yet because no invoice exists yet.
- **Stripe perspective**: "We give you the rev-rec product (Stripe Revenue Recognition) for $2/$0.05 per invoice + monthly fee. Use it or don't." → Holistika decision: not until customer count justifies it (forward-charter).
- **Investor / ENISA perspective**: "Show me your projected MRR-to-Year-3, your contribution margin, your CAC payback." → Currently lives in operator head + business plan draft; not yet in any canonical or model in repo.
- **AIC perspective**: "When I draft a customer engagement contract, I need to know what performance obligations attach. The pricing-tier doctrine doesn't define them." → Surface that drives `dtp_203` expansion.
- **Customer perspective**: "If I prepay annually, do I get a discount? Refund policy? Upgrade pro-ration?" → Open.

### 3.5 What the canonical answer set might look like

> **Note — this is a sketch for operator critique, not a proposed ratification.** It exists so the operator has something concrete to push back on.

- A canonical [`FINOPS_REVENUE_RECOGNITION_POLICY.md`](#) (proposed) at `Finance/Business Controller/canonicals/`:
  - declares **IFRS 15** (Spain GAAP-equivalent) as the recognition standard.
  - lists every pricing tier from `dtp_203` with **performance obligations** + **recognition schedule** (ratable / point-in-time / milestone).
  - states **annual prepay treatment** explicitly (deferred liability, monthly recognition).
  - declares Stripe Revenue Recognition product **out of scope until X customers** with operator-discretion override.
- A `validate_revenue_recognition_policy.py` that checks every active pricing tier in a future `PRICING_TIER_REGISTRY.csv` has a paired performance-obligation row.
- A `process_list.csv` row `thi_finan_dtp_310 Revenue recognition policy maintenance` paired with the SOP.
- A forward-chartered Phase 2 of I19 to actually write recognized facts to `finops.registered_fact`.

---

## 4. Expense plane — vendor spend + founder reimbursements

### 4.1 Plain
Two distinct flows: (a) Holistika as a legal entity pays vendors (mostly SaaS subscriptions today); (b) the founder pays out of pocket and gets reimbursed (or contributes capital, or makes a loan). Today both flows are off-repo; the second flow has a SOP (`SOP-FOUNDER_COMPANY_FUNDING_001`) but no live ledger; the first flow has a register schema waiting for population.

### 4.2 Governed
- **Vendor spend**: counterparty rows (`counterparty_type=vendor` + `billing_model={subscription, usage, one_time, ...}`) → invoices off-repo → future `finops.registered_fact` writes.
- **Founder funding paths**: `SOP-FOUNDER_COMPANY_FUNDING_001` defines three paths: capital contribution / shareholder loan / reimbursement.
- **Capitalization posture**: [`FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04`](../../../../references/hlk/v3.0/Admin/O5-1/Finance/Business%20Controller/canonicals/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md) — recommend EUR 1,000 minimum + 3× active monthly burn as healthier target.
- **Operating baseline**: founder-described `EUR 150/month idle` to `EUR 300-500/month active` recurring infra (working planning input, not accounting fact).
- **Open question routing**: `Q-FIS-002` in `ADVISER_OPEN_QUESTIONS.csv` (Founder-funded infrastructure handling: tax treatment + bookkeeping path pre vs post incorporation).

### 4.3 Ideal vs current

| Concern | Ideal | Current | Gap class |
|:---|:---|:---|:---|
| Vendor spend register coverage | Every recurring SaaS subscription registered as counterparty row + monthly recurring amount captured (post-Phase C) | Register has 2 seed rows; no subscriptions registered | **CRITICAL — backfill** |
| Founder out-of-pocket ledger | Every founder receipt classified (capital / loan / reimbursement) + filed with date + amount + business purpose | No ledger exists; receipts in operator-private storage | **Author-blocker** (need entity formation first) |
| Capital contribution amount | Set per `FOUNDER_CAPITALIZATION_DECISION_NOTE` heuristic at incorporation | Pending notary deed (`Q-LEG-004`) | Blocked-on-incorporation |
| Pluriactividad treatment | Operator's `cotización` decision encoded in canonical doctrine | `Q-FIS-001` open at adviser | Blocked-on-adviser |
| Reimbursement workflow | SOP step-by-step + evidence pack + accountant-reviewed | SOP exists at draft maturity (v0.1); never run | Doctrine-ready, not exercised |
| Vendor PII/PCI scope | Each vendor row's `pci_phi_pii_scope` reflects actual data the vendor processes (e.g. OpenAI = pii if customer transcripts; Stripe = pci) | No vendor rows | Blocked-on-population |

### 4.4 Multi-perspective challenge

- **CFO perspective**: "Why are we treating every founder out-of-pocket spend as undifferentiated? It matters whether €500 of OpenAI usage is (a) capital contribution to be returned via dividend, (b) shareholder loan with interest, or (c) reimbursement. The IRC consequences differ. The cap-table consequences differ."
- **Spanish fiscal counsel perspective**: "Founder loans are a *related-party transaction*. They need market-rate interest documentation OR they get reclassified. Capital contributions don't generate IRPF deduction for the founder unless `empresas de nueva o reciente creación` rules apply (50% deduction up to €100K base, equity ≤ €400K). Reimbursements need invoice + business-purpose evidence."
- **Auditor perspective**: "Show me dual-control on every founder spend that exceeds €X. Today X is unbounded because there's no policy."
- **Cap-table perspective**: "Every capital contribution changes the cap table. Today the cap table is 100% founder. The moment a contribution becomes a SAFE-with-discount or convertible-loan-to-equity, cap-table tracking becomes a live concern."
- **R&D credit perspective**: "Founder time + founder out-of-pocket spend on R&D-eligible work may be claimable under `deducción I+D` (varies by Hacienda Foral). Today none of that time/spend is being categorised."

---

## 5. Capital + tax plane — the off-repo surface

### 5.1 Plain
Capital lives at the notary registry (escritura de constitución, capital contributions, future SAFE notes). Tax lives at AEAT (or Hacienda Foral Bizkaia / Gipuzkoa for territoriality-applicable scenarios). Both surfaces are external systems of record. Holistika's job is to **reference + cross-link**, not to duplicate. The synthesis question is: what canonical / register / doctrine should Holistika own to keep this surface legible?

### 5.2 Governed
- **Filed instruments**: [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FOUNDER_FILED_INSTRUMENTS.csv) — per-discipline (legal / fiscal / IP / banking / certification / notary) instrument-by-instrument registry. 1 row today: `INST-LEG-ESCRITURA-DRAFT-2026` (draft).
- **Open questions**: [`ADVISER_OPEN_QUESTIONS.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_OPEN_QUESTIONS.csv) — 12 rows across disciplines; all open.
- **Adviser engagement disciplines**: [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv) — discipline-id + canonical_role + default_process_item_id lookup.
- **GOI/POI**: [`GOI_POI_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/GOI_POI_REGISTER.csv) — every private adviser/entity by ref_id; identity mapping off-repo per [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md).
- **Handoff export**: [`scripts/export_adviser_handoff.py`](../../../../../scripts/export_adviser_handoff.py) (Initiative 21 P7) builds the per-discipline handoff package.
- **Process catalogue**: `hol_opera_ws_5` (External Adviser Engagement workstream) + `hol_opera_dtp_311..312`, `hol_peopl_dtp_303..304`, `thi_legal_dtp_304`.
- **Plane SOP**: [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md).
- **Founder fact pattern**: [`FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md) — WS-A through WS-D map.

### 5.3 Ideal vs current

| Concern | Ideal | Current | Gap class |
|:---|:---|:---|:---|
| Adviser answer encoding | Each `Q-XXX-NNN` close-out generates a canonical artifact (memo or doctrine update) that downstream agents can read | `Q-XXX-NNN` closes as `status=answered` + free-text note; canonical encoding manual | **Architectural gap** — no receiving slot |
| Tax filing calendar | Every Spanish tax filing (Modelo 200 IS, Modelo 720 if applicable, Modelo 202 IS payments-on-account, IRPF withholding, IVA TMS, Modelo 130 if autónomo path, Modelo 036/037 census) has a calendar entry + paired SOP + paired runbook | Calendar non-existent; no SOPs for any | **Architectural gap** — calendar pattern needed |
| Pluriactividad strategy | Encoded as canonical position with `Q-FIS-001` answer | `Q-FIS-001` open | Blocked-on-adviser |
| Hacienda Foral vs AEAT routing | Operator's territoriality + foral applicability documented (Bizkaia/Gipuzkoa/Common) | Operator-head; no canonical | **Author-now-needed** — even pre-incorporation |
| R&D credit posture | `deducción I+D` eligibility + evidence requirements per Hacienda | Not authored | Blocked-on-CFO+counsel |
| ENISA reporting | Activity report cadence + responsibility (`Q-CRT-001`) | Open | Blocked-on-adviser |
| Capital instrument register | Every cap-table-affecting instrument (capital contribution, founder loan, future SAFE, future equity grant, future ENISA loan) carries instrument_id + amount + date + counterparty | Only `INST-LEG-ESCRITURA-DRAFT-2026` row exists; no money-amount field on FOUNDER_FILED_INSTRUMENTS | **Schema gap** — money-amount field absent by design (off-repo today); reconsider post-incorporation |
| Modelo 720 trigger | Operator alerted if foreign-account aggregate exceeds €50K threshold | No alerting mechanism | Operator-vigilance-only |

### 5.4 Multi-perspective challenge

- **External fiscal counsel perspective**: "You're asking me to answer 12 questions in one engagement. That's a complex retainer. Show me your prioritization: which answers gate what filings." → `ADVISER_OPEN_QUESTIONS.csv` has `target_date` column (mostly `before_signing` or `tbd`); operator/Madeira should curate a tighter priority order.
- **Auditor perspective**: "Where is the version-controlled accountant-reviewed financial policy?" → Doesn't exist yet. `SOP-FOUNDER_COMPANY_FUNDING_001` says "does not replace accountant sign-off on jurisdiction-specific tax treatment" — explicitly deferring.
- **ENISA perspective**: "Your business plan + market analysis is due to the certification adviser per `Q-CRT-002` `target_date=asap`. Where is it?" → Open question.
- **Hacienda perspective (hypothetical)**: "What's your tax residency, foral applicability, IAE classification, CNAE classification? What are you planning to declare in your first Modelo 036?" → Pending `Q-LEG-001` (objeto social + CNAE codes) + `Q-BNK-001` (CNAE/IAE alignment).
- **Founder perspective**: "How do I keep an eye on this without becoming the bookkeeper?" → That's the CFOaaS / fractional CFO question. The synthesis recommends activating a CFOaaS engagement as the load-bearing answer (§7).

---

## 6. The CFO question — who runs FINOPS at Holistika?

### 6.1 Plain
FINOPS doctrine is *operator-readable + agent-executable* today because the operator + Madeira are doing the work. That works for the metadata layer (counterparty register, schema, SOPs). It does not work for the **judgment layer** (revenue recognition policy, capital structure, tax strategy, vendor concentration analysis, board reporting). Industry consensus (Fractional CFO School 2026, Level CFO 2026, SaaS Fractional CFO UK 2026) is that pre-seed/seed-stage SaaS companies activate **fractional CFO / CFOaaS** at the moment two of the following are true: (a) first customer revenue starts flowing, (b) first external capital comes in, (c) tax filings become non-trivial, (d) board / investor reporting cadence kicks in.

### 6.2 Industry CFOaaS model (external grounding)

Per Fractional CFO School (2026), CFOaaS pricing is tiered:

| Tier | Monthly cost | Scope |
|:---|:---|:---|
| Essentials | $2,000-$3,500 | Bookkeeping oversight + monthly close + basic reporting |
| Growth | $3,500-$6,000 | + financial modeling + fundraising prep + board reporting |
| Strategic | $6,000-$10,000 | + investor relations + M&A prep + complex tax structuring |

Compared to a full-time CFO at $200K-$400K+/year. SaaS-specific CFOaaS providers focus on: MRR/ARR waterfall, NRR/GRR, CAC/LTV/payback, Rule of 40 / Magic Number / burn multiple, ASC 606 rev-rec, fundraising modeling, board reporting (per Level CFO + SaaS Fractional CFO UK, 2026).

### 6.3 Ideal vs current

| Concern | Ideal | Current | Gap class |
|:---|:---|:---|:---|
| CFO function presence | CFOaaS Essentials tier activated at incorporation, scales to Growth at first revenue | Business Controller role unactivated; operator+Madeira covering | **Architectural gap** — activation pending |
| Pre-CFO posture documentation | Canonical doctrine names operator+Madeira as interim FINOPS owners with explicit handoff conditions to CFOaaS | Implicit in `baseline_organisation.csv` (Business Controller role exists, unfilled); no canonical position | **Author-now-needed** |
| CFOaaS selection criteria | Documented evaluation rubric: Spain-fluent, SaaS-fluent, ENISA-fluent, bilingual EN+ES | Not authored | Author-when-ready |
| Bridge handoff plan | When CFOaaS activates, this synthesis + `SOP-FOUNDER_COMPANY_FUNDING_001` + `FOUNDER_CAPITALIZATION_DECISION_NOTE` form the onboarding pack | Pack assembled by happy accident (these are the right artifacts); never assembled deliberately | Trivial-to-close |

### 6.4 Multi-perspective challenge

- **Founder perspective**: "I don't want to hire a full-time CFO at this stage." → Aligned with industry consensus + this synthesis.
- **CFOaaS firm perspective (hypothetical)**: "Your books are basically empty. Where do I start?" → Right starting point: counterparty register backfill (§2.5) + revenue recognition policy authoring (§3.5) + first close (when first revenue arrives) + tax compliance calendar (§5.3).
- **AIC perspective**: "If I delegate FINOPS tasks to an external CFOaaS, what do they see?" → They see the AKOS repo (read-only or via export); they get the SOP package; they get the operator-scratchpad drain; they get the GOI/POI ref_id for themselves and start in the ADVOPS plane.
- **Investor perspective**: "Why isn't there a CFO?" → Stage-appropriate; CFOaaS is the answer. Document the answer.
- **Auditor perspective**: "Who signs off on the books?" → Today: operator. Post-CFOaaS: CFOaaS firm + operator.

---

## 7. The ideal-state architecture — what "FINOPS-mature Holistika" looks like

> **Note — this is the agent's hypothesis for operator critique. The operator's head knows things the agent doesn't. Amend liberally.**

### 7.1 Canonical surface (when mature)

```
docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/
  FINOPS_COUNTERPARTY_REGISTER.csv         # vendor/customer/partner metadata
  FINOPS_REVENUE_RECOGNITION_POLICY.md     # IFRS 15 + per-tier perf-obligations
  PRICING_TIER_REGISTRY.csv                # per-tier with perf-obligations FK
  FINOPS_TAX_CALENDAR.csv                  # Modelo 200/720/036/etc. with cadence
  FINOPS_CAPITAL_INSTRUMENTS_REGISTER.csv  # founder/SAFE/equity/ENISA loan
  FINOPS_VENDOR_SPEND_CATEGORIES.csv       # OPEX taxonomy
  FINOPS_REVENUE_SHARE_AGREEMENTS.csv      # partnerships
  FINOPS_REIMBURSEMENT_REGISTER.csv        # founder OPEX reimbursements
```

### 7.2 Pydantic + validator chassis (when mature)

```
akos/hlk_finops_counterparty_csv.py            # exists
akos/hlk_finops_revenue_recognition.py         # forward
akos/hlk_pricing_tier_csv.py                   # forward
akos/hlk_finops_tax_calendar_csv.py            # forward
akos/hlk_finops_capital_instruments_csv.py     # forward
akos/hlk_finops_reimbursement_csv.py           # forward
scripts/validate_finops_*.py                   # one per CSV; umbrella in validate_hlk.py
scripts/validate_finops_cross_consistency.py   # cross-CSV (pricing tier ↔ recognition policy ↔ revenue share)
```

### 7.3 Postgres surface (when mature)

```
schema compliance:
  finops_counterparty_register_mirror          # exists
  finops_tax_calendar_mirror                   # forward
  finops_capital_instruments_mirror            # forward
  pricing_tier_mirror                          # forward

schema finops:
  registered_fact                              # exists (empty)
  recognition_schedule                         # forward (joins to registered_fact + pricing_tier)
  revenue_share_distribution                   # forward
  vendor_spend_fact                            # forward
  reimbursement_fact                           # forward

schema holistika_ops:
  lead_intake                                  # exists
  stripe_customer_link                         # exists
  billing_account                              # exists (KiRBe routing)

schema stripe_gtm (FDW):
  customer, subscription, invoice, charge, ... # exists (read-only via stripe_gtm_server)
```

### 7.4 SOP + runbook surface (when mature)

| Process | SOP | Runbook |
|:---|:---|:---|
| Counterparty register maintenance (`thi_finan_dtp_303`) | `SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001` ✅ | `scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only` ✅ |
| Counterparty onboarding/offboarding (`dtp_304`) | ✅ (procedure section) | New: `scripts/finops_counterparty_onboard.py` (forward) |
| Counterparty data classification review (`dtp_305`) | ✅ (procedure section) | Reuses validate_finops_counterparty_register.py |
| Legal+entity readiness gate (`dtp_306`) | ✅ (procedure section) | Manual operator gate |
| Annual counterparty renewal review (`dtp_307`) | ✅ (procedure section) | New: `scripts/finops_counterparty_renewal_sweep.py` (forward) |
| Stripe FDW stewardship (`dtp_308`) | ✅ | `scripts/stripe_set_billing_plane.py` + manual review |
| Counterparty segment+revenue metadata (`dtp_309`) | ✅ (procedure section) | Reuses validate_finops_counterparty_register.py |
| Revenue recognition policy (forward `dtp_310`) | New (§3.5) | Stripe Revenue Recognition export → validate against policy |
| Tax calendar management (forward `dtp_311`) | New | Scheduled reminder + per-Modelo checklist |
| Capital instrument registration (forward `dtp_312`) | New + cross-link to legal SOP-FOUNDER_ENTITY_FORMATION_001 | Manual operator |
| Founder reimbursement processing (forward `dtp_313`) | New + cross-link to SOP-FOUNDER_COMPANY_FUNDING_001 | Manual + validator |

### 7.5 Drift gates (when mature)

- `validate_finops_counterparty_register.py` ✅
- `validate_finops_cross_consistency.py` (forward) — every pricing tier has a perf-obligation; every counterparty type customer has a revenue_model; every counterparty type vendor has a service_category
- `validate_finops_tax_calendar.py` (forward) — every Modelo has paired SOP + cadence + responsible role
- `validate_finops_capital_instruments.py` (forward) — every cap-table-affecting instrument is filed within X days of execution

---

## 8. Gap call — where Holistika is today vs ideal (per §7)

> Severity scale: **CRITICAL** (immediate operator concern) / **HIGH** (next-quarter target) / **MEDIUM** (next-year target) / **LOW** (post-Series A target).

| Plane | Concern | Severity | Owner | Forward-charter |
|:---|:---|:---|:---|:---|
| 1 (Counterparty) | Register population (vendor inventory pass) | **CRITICAL** | Operator + Madeira | OPS-81-FINOPS-1 |
| 1 (Counterparty) | Customer rows (when first customer signs) | HIGH | Business Controller (CFOaaS when active) | OPS-81-FINOPS-2 |
| 1 (Counterparty) | Renewal review cadence first-run | MEDIUM | Business Controller | OPS-81-FINOPS-3 |
| 2 (Revenue) | Revenue recognition policy authoring | **CRITICAL** (before first sale) | Business Controller + accountant | OPS-81-FINOPS-4 |
| 2 (Revenue) | Pricing tier performance-obligation mapping | HIGH | Business Controller + Product | OPS-81-FINOPS-5 |
| 2 (Revenue) | Stripe Revenue Recognition product activation | MEDIUM (post-first-customer) | CFOaaS | OPS-81-FINOPS-6 |
| 3 (Expense) | Vendor spend ledger writers (`finops.registered_fact`) | HIGH (post-incorporation) | CFOaaS | OPS-81-FINOPS-7 |
| 3 (Expense) | Founder reimbursement workflow first-run | HIGH | CFOaaS + operator | OPS-81-FINOPS-8 |
| 3 (Expense) | Founder out-of-pocket categorization (capital/loan/reimbursement) | **CRITICAL** | Fiscal counsel (`Q-FIS-002`) | OPS-81-FINOPS-9 |
| 4 (Capital) | Capital instruments register (cap-table) authoring | HIGH (post-incorporation) | Legal Counsel + CFOaaS | OPS-81-FINOPS-10 |
| 4 (Capital) | Founder capital contribution amount + IRPF deduction strategy | HIGH | Legal Counsel + fiscal counsel | OPS-81-FINOPS-11 |
| 5 (Tax) | Tax filing calendar authoring | **CRITICAL** | Fiscal counsel | OPS-81-FINOPS-12 |
| 5 (Tax) | Hacienda Foral vs AEAT territoriality documentation | HIGH | Operator (head knowledge) → canonical | OPS-81-FINOPS-13 |
| 5 (Tax) | R&D credit eligibility assessment | MEDIUM | Fiscal counsel + accountant | OPS-81-FINOPS-14 |
| 5 (Tax) | ENISA activity reporting cadence | HIGH | Compliance (`Q-CRT-001`) | OPS-81-FINOPS-15 |
| 6 (CFO) | CFOaaS engagement activation | HIGH (when 2 of 4 triggers fire — see §6.1) | Operator | OPS-81-FINOPS-16 |
| 6 (CFO) | Pre-CFO posture canonical | MEDIUM | Madeira author + operator ratify | OPS-81-FINOPS-17 |
| Cross | Adviser answer encoding pattern (the `Q-XXX` → canonical artifact slot) | **CRITICAL** | Madeira author + operator ratify | OPS-81-FINOPS-18 |
| Cross | Brand register on FINOPS prose | LOW | Anti-jargon discipline already applies | n/a |

---

## 9. Forward-charter set (proposed OPS rows)

> These rows are **proposed**, not minted. Operator engagement at the §10 ratify gate decides which mint, which combine, which defer, which reject.

Critical-severity rows (mint at next FINOPS push window):

- **OPS-81-FINOPS-1** — Vendor inventory pass (populate counterparty register with every recurring SaaS spend Holistika has signed up for).
- **OPS-81-FINOPS-4** — Revenue recognition policy doctrine authoring (IFRS 15 declaration + per-tier perf-obligation mapping + deferred revenue treatment).
- **OPS-81-FINOPS-9** — Founder out-of-pocket categorization first-pass (every receipt classified capital / loan / reimbursement) — gated on fiscal counsel answer `Q-FIS-002`.
- **OPS-81-FINOPS-12** — Spain tax filing calendar authoring (Modelo 200 / 720 / 036 / IS payments-on-account / IRPF withholding / IVA).
- **OPS-81-FINOPS-18** — Adviser answer encoding pattern doctrine (the slot every `Q-XXX-NNN` closes into).

High-severity rows (mint at next-quarter window):

- **OPS-81-FINOPS-2** — Customer row protocol (when first customer signs).
- **OPS-81-FINOPS-5** — Pricing-tier perf-obligation mapping.
- **OPS-81-FINOPS-7** — Vendor spend ledger writers (`finops.registered_fact` Phase 2).
- **OPS-81-FINOPS-8** — Founder reimbursement workflow first-run.
- **OPS-81-FINOPS-10** — Capital instruments register (cap-table) — depends on entity formation.
- **OPS-81-FINOPS-11** — Founder capital contribution amount + IRPF deduction strategy.
- **OPS-81-FINOPS-13** — Hacienda Foral vs AEAT territoriality canonical.
- **OPS-81-FINOPS-15** — ENISA activity reporting cadence (gated on `Q-CRT-001`).
- **OPS-81-FINOPS-16** — CFOaaS engagement activation (when 2 of 4 triggers fire).

Medium / Low (mint when context warrants):

- OPS-81-FINOPS-3, OPS-81-FINOPS-6, OPS-81-FINOPS-14, OPS-81-FINOPS-17.

---

## 10. Operator engagement gate (inline-ratify surface)

This synthesis exists so the operator can read it, push back, amend it, and ratify the doctrine deltas. Specific decisions the operator needs to make before I81 P2 Tranche T1 (`FINOPS_COUNTERPARTY_REGISTER.csv` → `finops/`) advances:

### Decision A — does this synthesis describe Holistika FINOPS truthfully?

- Option A1 — **Yes, ratify as-written.** Mint **D-IH-81-N** with this synthesis as the ratifying evidence. Forward-charter §9 OPS rows for downstream execution.
- Option A2 — **Yes with amendments.** Operator surfaces specific factual corrections + framings; agent rewrites the affected sections; re-ratifies a v2 synthesis.
- Option A3 — **No, fundamentally misframed.** Operator surfaces the misframing + agent restarts the synthesis from corrected premises.

### Decision B — which OPS rows mint now vs defer?

Operator picks per-row from §9. Default if silent ≥ 24h: mint the 5 CRITICAL rows + defer the rest until next FINOPS push window.

### Decision C — does T1 proceed in the same push window after A+B, or is T1 itself contingent on operator-led FINOPS work first?

- Option C1 — **T1 proceeds immediately after A+B.** Layout migration is orthogonal to substantive FINOPS doctrine; the synthesis cleared the operator's "I need to understand the end-to-end before any FINOPS-touching work" gate, T1 is mechanical, OK to ship.
- Option C2 — **T1 deferred until the 5 CRITICAL OPS rows ship.** Layout migration before substantive doctrine work would be cart-before-horse.
- Option C3 — **T1 deferred until operator-led work (e.g. populate vendor inventory in operator-scratchpad) catches up to a minimum threshold.**

### Decision D — CFOaaS engagement activation timing

- Option D1 — Activate at entity formation close + first-customer-signed simultaneity.
- Option D2 — Activate at entity formation close immediately (don't wait for first customer).
- Option D3 — Activate now, pre-formation, as `_pre-formation_engagement` (CFOaaS firms typically resist but some accommodate).
- Option D4 — Defer indefinitely; operator + Madeira continue covering until further notice.

---

## 11. Cross-references

### Internal precedent
- Parent initiative: I81 master-roadmap.
- Sister tranche reports: [`p2-tranche-t4-verification-2026-05-22.md`](p2-tranche-t4-verification-2026-05-22.md).
- Predecessor doctrine: I14 (Holistika internal GTM/MOPS), I16 (FINOPS vendor SSOT, superseded by I18), **I18** (FINOPS counterparty SSOT + Stripe FDW, **closed 2026-04-23**), **I19** (FINOPS ledger Phase 1 — `finops.registered_fact` DDL applied 2026-04-23, Phase 2 unscheduled), I72 (RevOps spine + `SOP-FINOPS_BRIDGE_001`).
- Adviser engagement parent: I21 (adviser engagement + GOI/POI), I22 (forward layout convention + program folders).
- Founder funding doctrine: [`SOP-FOUNDER_COMPANY_FUNDING_001`](../../../../references/hlk/v3.0/Admin/O5-1/Finance/Business%20Controller/canonicals/SOP-FOUNDER_COMPANY_FUNDING_001.md) + [`FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04`](../../../../references/hlk/v3.0/Admin/O5-1/Finance/Business%20Controller/canonicals/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md).
- Tax doctrine open questions: [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md) §Fiscal + §Banking + §Certification.

### External grounding (per akos-applied-research-discipline.mdc RULE 2)
- **Stripe (2026), SaaS revenue recognition 101.** — load-bearing source for ASC 606 / IFRS 15 5-step model + the 73%-mis-recognition statistic.
- **Stripe (2026), Revenue recognition principles & best practices.** — corroborating source.
- **HighRock CPA (2026), SaaS Revenue Recognition ASC 606 Founder Audit Guide.** — founder-perspective framing of the same rules.
- **NetSuite (2026), Revenue Recognition for Software and SaaS.** — alternative platform framing (validates the 5-step framing is industry-universal, not Stripe-specific).
- **Fractional CFO School (2026), CFO as a Service Cost Guide.** — load-bearing source for the CFOaaS tiered-pricing model + activation triggers.
- **Level CFO (2026), Fractional CFO for SaaS & Software Startups.** — SaaS-specific CFOaaS metric coverage (MRR/ARR/NRR/CAC/LTV/payback/Rule-of-40/Magic-Number/burn-multiple/ASC 606).
- **SaaS Fractional CFO UK (2026), Fractional CFO services menu.** — UK/EU-region peer of the US Level CFO model.
- **Sincro (2026), Cómo constituir una sociedad en España en 2026.** — Spain-specific incorporation cost + IS deductibility.
- **Vademecum Legal (2026), Deducción IRPF por inversión en empresas de nueva o reciente creación.** — IRPF 50%-deduction rule + equity ceiling.
- **AEAT Sede Electrónica (2026) — Haciendas Forales Bizkaia + Gipuzkoa.** — Foral Modelo 200 reference.
- **AEAT (2026) — Modelo 720.** — foreign-asset declaration trigger.
- **Supplier.io / TealBook / Semarchy (2026).** — vendor master data SSOT industry pattern (deduplication, hierarchy mapping, audit trails, SOC2/SOX alignment).

### Governing rules
- [`akos-holistika-operations.mdc`](../../../../../.cursor/rules/akos-holistika-operations.mdc) §"FINOPS" — load-bearing posture rule for this synthesis.
- [`akos-applied-research-discipline.mdc`](../../../../../.cursor/rules/akos-applied-research-discipline.mdc) RULE 2 — external-source grounding for novel framings.
- [`akos-executable-process-catalog.mdc`](../../../../../.cursor/rules/akos-executable-process-catalog.mdc) — SOP+runbook pairing applies to every forward-chartered §9 row.
- [`akos-inline-ratification.mdc`](../../../../../.cursor/rules/akos-inline-ratification.mdc) — §10 surfaces as the inline-ratify gate.
- [`akos-quality-fabric.mdc`](../../../../../.cursor/rules/akos-quality-fabric.mdc) — synthesis audience axis = J-OP; brand register = internal CORPINT OK; channel axis = J-OP-internal (no render trail required).
- [`akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc) — synthesis is not a closure UAT; quality bar applies on its terms (research grounding + multi-perspective challenge + ideal-vs-current gap).
