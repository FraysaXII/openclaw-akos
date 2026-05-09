---
language: en
status: active
role_owner: Legal Counsel
area: Legal
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_legal
  - topic_trademark
artifact_role: canonical
intellectual_kind: legal_brief
authority: Founder + Legal Counsel + filing agent
last_review: 2026-05-09
ssot: true
linked_initiative: I66
linked_decisions:
  - D-IH-66-A
  - D-IH-66-C
  - D-IH-66-H
  - D-IH-66-U
linked_canonicals:
  - BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md
  - BRAND_ARCHITECTURE.md
  - BRAND_LOGO_SYSTEM.md
  - BRAND_ABBREVIATIONS.md
---

# TRADEMARK_FILING_STRATEGY_2026-05 — Per-mark filing strategy + ready-to-sign forms

> **Operator-gated document.** This is the **filing strategy + clearance worklist + ready-to-sign filing forms** for the seven Holistika trademarks (umbrella + three sub-marks + four product marks). Per [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) §3, the architectural decisions are frozen; this document operationalises them into actionable filings. The actual submission to EUIPO + OEPM is **operator-driven** with counsel; the agent's role ends at "ready-to-sign" form preparation per D-IH-66-H.

## 1. Purpose and scope

This document is the **input package for counsel + filing agent**. It contains:

1. Per-mark **clearance worklist** (the searches counsel must run before filing).
2. Per-mark **filing strategy decision** (EUIPO vs OEPM vs both; word-only vs word-and-design; class scope rationale).
3. **Ready-to-sign filing forms** populated with the frozen filing strings + applicant data + class scope (§5 — EUIPO TM-1 form template + OEPM equivalent template).
4. **Operator-handoff matrix** — what counsel needs from the operator before filing day.

Out of scope: actual filing submission (counsel + filing-agent driven post-handoff); opposition response (operator + counsel post-filing); renewal calendar (governed by [`SOP-LEGAL_TRADEMARK_MONITORING_001`](SOP-LEGAL_TRADEMARK_MONITORING_001.md), I66 P3).

## 2. Mark inventory

Per [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) §2, the seven active marks for this filing wave:

| # | Mark | Form | Frozen filing string | Visual canonical (design mark) |
|:---:|:---|:---|:---|:---|
| M1 | Holistika (umbrella, word) | wordmark | `Holistika` | — |
| M1d | Holistika (umbrella, design) | designmark | — | `HOLÍSTIKA Research` (with diacritic on Í; per BRAND_LOGO_SYSTEM.md §2.2) |
| M2 | Holistika R&S (sub-mark, word) | wordmark | `Holistika R&S` | — |
| M3 | Think Big (sub-mark, word) | wordmark | `Think Big` | — |
| M4 | HLK Tech Lab (sub-mark, word) | wordmark | `HLK Tech Lab` | — |
| M5 | MADEIRA (product, word) | wordmark | `MADEIRA` | — |
| M5a | MADEIRA Agent (product variant, word) | wordmark | `MADEIRA Agent` | — |
| M5d | MADEIRA (product, design) | designmark | — | per BRAND_LOGO_SYSTEM.md product-mark rules |
| M6 | KiRBe (product, word) | wordmark | `KiRBe` (mixed-case) | optional — defer to next filing wave |
| M7 | ENVOY (product, word) | wordmark | `ENVOY` | — |

**Deferred** (per BRAND_HIERARCHY §2.3): InfraMonitor, Financial Analyst — defensive domain reservation only; no filings until commercial validation.

## 3. Per-mark clearance worklist

For each mark M1–M7, counsel runs the following clearance sequence **before** filing:

### Standard clearance template (apply to each mark)

1. **EUIPO eSearch** at <https://euipo.europa.eu/eSearch/> — search exact + 1-edit-distance + phonetic similarity for `<filing string>`. Document hits in classes overlapping the target Nice scope (§4 below).
2. **OEPM Sitadex** at <https://sitadex.oepm.es/sitadex/> — same search, same documentation.
3. **WIPO Madrid Monitor** at <https://www3.wipo.int/madrid/monitor/> — international register search (catches Madrid-Protocol filings that may extend into EU/Spain).
4. **EU corporate-register cross-reference** — confirm no operating Spanish/EU company holds the wordmark in a conflicting industry (light search; not exhaustive).
5. **Domain-name cross-reference** — confirm primary `.com` and `.eu` domains are either owned by Holistika or free of obvious-conflict-holders.
6. **Common-law usage scan** — Google search for `<filing string>` + industry-context keywords; document any commercial usage in a similar Nice class.

Per-mark output: a `clearance-<mark-slug>-2026-05.md` filed alongside this strategy doc under `_assets/legal/trademark-clearance/` (folder created P4 follow-up; out-of-scope-for-this-commit unless counsel runs the searches before commit).

### Per-mark clearance highlights (pre-counsel-search expectations; from BRAND_HIERARCHY §2)

| Mark | Pre-search collision expectation | Filing-day risk |
|:---|:---|:---|
| **Holistika (M1, M1d)** | Low. The K-spelling is non-standard for Spanish/Portuguese context; the diacritic-Í wordmark is distinctive. | **Low risk.** Standard registration likely; opposition window unlikely to produce material conflicts. |
| **Holistika R&S (M2)** | Low. R&S as a paired wordmark has industry-specific meaning (Research & Strategy) but the paired form with Holistika is novel. | **Low risk.** |
| **Think Big (M3)** | **HIGH.** "Think Big" is generic; widely used in motivational/business literature; multiple prior registrations likely in EUIPO. | **High risk in EU.** Filing OEPM (national-Spain) with **narrow Nice 35 + 42 scope** as the strategic decision. EU-wide brand protection via use-in-trade only. |
| **HLK Tech Lab (M4)** | Medium. "HLK" + "Tech Lab" paired; "HLK" alone is a 3-letter combination with possible prior uses; the paired form should distinguish. | **Medium risk.** EUIPO opposition window monitored. |
| **MADEIRA (M5, M5a, M5d)** | **VERY HIGH.** MADEIRA is a Portuguese island, wine region, wood type. Multiple prior registrations across food/beverage/tourism Nice classes. | **High risk in Nice 33/32/30/39/41/43/44.** Strategic decision per BRAND_HIERARCHY §2.3: file in **Nice 9 + 42 ONLY** (computer software + SaaS). This is the narrowest possible scope but matches actual product use. |
| **KiRBe (M6)** | Low. Mixed-case; novel construction; unlikely prior uses. | **Low risk.** |
| **ENVOY (M7)** | **HIGH.** Used by other tech companies (Envoy Proxy is open-source; Envoy real-estate is registered in some markets). | **Medium-to-high risk.** EUIPO + OEPM opposition windows actively monitored. Counsel may recommend coexistence agreement if conflict surfaces. |

## 4. Per-mark filing strategy decision

| Mark | EUIPO | OEPM | Nice classes | Word | Design | Filing-day decision |
|:---|:---:|:---:|:---|:---:|:---:|:---|
| Holistika (M1) | ✅ | ✅ | 35, 41, 42 | ✅ | — | EUIPO + OEPM both jurisdictions; 3-class scope captures consulting (35), research/training (41), software/SaaS (42). |
| Holistika design (M1d) | ✅ | ✅ | 35, 41, 42 | — | ✅ | Filed alongside M1 as separate design-mark applications; same class scope. |
| Holistika R&S (M2) | ✅ | ➖ | 35, 42 | ✅ | — | EUIPO only; EU-wide. Spain protection cascades. |
| Think Big (M3) | ❌ | ✅ | 35, 42 | ✅ | — | OEPM-only (national Spain); narrow Nice scope; explicit decision to NOT file EUIPO due to high-collision risk. EU-wide brand protection via use-in-trade. |
| HLK Tech Lab (M4) | ✅ | ➖ | 35, 42 | ✅ | — | EUIPO only; EU-wide. |
| MADEIRA (M5) | ✅ | ✅ | 9, 42 | ✅ | — | EUIPO + OEPM both; **only Nice 9 + 42** (collision-driven narrow scope). |
| MADEIRA Agent (M5a) | ✅ | ✅ | 9, 42 | ✅ | — | Filed alongside M5; same class scope. |
| MADEIRA design (M5d) | ✅ | ✅ | 9, 42 | — | ✅ | Filed alongside M5; same class scope. |
| KiRBe (M6) | ✅ | ✅ | 9, 42 | ✅ | optional | EUIPO + OEPM both. Design-mark filing optional; defer if budget tight. |
| ENVOY (M7) | ✅ | ✅ | 9, 42 | ✅ | — | EUIPO + OEPM both. Counsel pre-files coexistence-agreement template in case opposition surfaces. |

**Total filing count**: ~10 applications across EUIPO + OEPM.

## 5. Ready-to-sign filing forms (templates populated with frozen strings)

> **Important**: these are **data-populated templates**, not legal advice. The filing-agent's official EUIPO TM-1 form / OEPM equivalent form (PDF/online portal) is the authoritative submission surface. Counsel transcribes the data below into that surface. Counsel is responsible for: (a) confirming Nice class names against the current Nice Classification edition (currently 12-2024); (b) confirming applicant entity details against the corporate register (Holistika Research SL); (c) confirming filing-day fees per the current EUIPO/OEPM fee schedule; (d) executing the actual submission.

### 5.1 EUIPO TM-1 form data (per mark)

**Common applicant block** (used for every EUIPO filing):

| Field | Value |
|:---|:---|
| Applicant name | `Holistika Research SL` |
| Applicant type | Legal entity (Sociedad Limitada) |
| Country of incorporation | Spain |
| Address | `[OPERATOR-PROVIDE: registered address per Registro Mercantil de Madrid]` |
| NIF / CIF | `[OPERATOR-PROVIDE: tax identification]` |
| Representative | `[OPERATOR-PROVIDE: filing-agent firm name + EUIPO ID number]` |
| Language of proceedings | English (with Spanish as second language for cascade to OEPM) |

**Per-mark data**:

#### M1 — Holistika (wordmark)

| Field | Value |
|:---|:---|
| Mark type | Word mark |
| Reproduction | `Holistika` |
| Goods/services (Nice 35) | Business consulting; business strategy advisory; business research; market research; business management consultancy. |
| Goods/services (Nice 41) | Education; training; provision of training; arranging and conducting of seminars and workshops; publication of texts. |
| Goods/services (Nice 42) | Scientific and technological services; software development; software-as-a-service (SaaS); design and development of computer hardware and software; cloud computing services. |

#### M1d — Holistika (design mark)

| Field | Value |
|:---|:---|
| Mark type | Figurative (design) mark |
| Reproduction | `[OPERATOR-PROVIDE: HOLÍSTIKA Research wordmark SVG/PNG file per BRAND_LOGO_SYSTEM.md §2.2; recommended file format per EUIPO ≤ 2 MB JPEG/PNG]` |
| Description of mark | Stylised wordmark `HOLÍSTIKA Research` with diacritic on Í; canonical brand wordmark of Holistika Research SL. |
| Goods/services | Same as M1 (Nice 35, 41, 42). |

#### M2 — Holistika R&S (wordmark)

| Field | Value |
|:---|:---|
| Mark type | Word mark |
| Reproduction | `Holistika R&S` |
| Goods/services (Nice 35) | Business consulting (research-focused); strategic advisory services. |
| Goods/services (Nice 42) | Scientific research; technology research; research and development services. |

#### M3 — Think Big (wordmark — OEPM-only filing per §4)

This mark is **NOT** filed at EUIPO. See §5.2 for OEPM-only filing data.

#### M4 — HLK Tech Lab (wordmark)

| Field | Value |
|:---|:---|
| Mark type | Word mark |
| Reproduction | `HLK Tech Lab` |
| Goods/services (Nice 35) | Business consulting (technology-focused); IT consultancy. |
| Goods/services (Nice 42) | Software development; design and development of artificial-intelligence systems; cloud computing services; software-as-a-service (SaaS). |

#### M5 — MADEIRA (wordmark — narrow Nice scope)

| Field | Value |
|:---|:---|
| Mark type | Word mark |
| Reproduction | `MADEIRA` |
| Goods/services (Nice 9) | Computer software; downloadable software; software platforms; agent-based software systems. |
| Goods/services (Nice 42) | Software-as-a-service (SaaS); software development; provision of online non-downloadable software; cloud computing services. |
| Disclaimer / limitation | **Filing intentionally excludes** Nice 33 (wines), 32 (beers), 30 (food), 39 (transport), 41 (entertainment as it relates to Madeira Island tourism), 43 (hospitality), 44 (medical). The applicant claims **no rights in the geographic name "Madeira"** as it relates to wine, food, tourism, or any geographic-origin context. |

#### M5a — MADEIRA Agent (wordmark)

| Field | Value |
|:---|:---|
| Mark type | Word mark |
| Reproduction | `MADEIRA Agent` |
| Goods/services | Same as M5 (Nice 9 + 42, with same disclaimer). |

#### M5d — MADEIRA (design mark)

| Field | Value |
|:---|:---|
| Mark type | Figurative (design) mark |
| Reproduction | `[OPERATOR-PROVIDE: MADEIRA wordmark SVG/PNG per BRAND_LOGO_SYSTEM.md product-mark rules]` |
| Goods/services | Same as M5. |

#### M6 — KiRBe (wordmark)

| Field | Value |
|:---|:---|
| Mark type | Word mark |
| Reproduction | `KiRBe` (mixed-case) |
| Goods/services (Nice 9) | Computer software; downloadable software; knowledge-management software; database-management software. |
| Goods/services (Nice 42) | Software-as-a-service; provision of database services; software development. |

#### M7 — ENVOY (wordmark)

| Field | Value |
|:---|:---|
| Mark type | Word mark |
| Reproduction | `ENVOY` |
| Goods/services (Nice 9) | Computer software; downloadable software; software adapters and connectors; integration software. |
| Goods/services (Nice 42) | Software-as-a-service; software development; provision of integration services. |

### 5.2 OEPM (Spain national) form data (per mark)

OEPM accepts filings in Spanish. Counsel translates the goods/services blocks into Spanish per the current Nice Classification (12-2024) Spanish-language designation list.

**Common applicant block**:

| Field | Value |
|:---|:---|
| Solicitante | `Holistika Research SL` |
| Forma jurídica | Sociedad Limitada |
| Domicilio | `[OPERATOR-PROVIDE: domicilio social registrado]` |
| NIF | `[OPERATOR-PROVIDE]` |
| Representante | `[OPERATOR-PROVIDE: agente de la propiedad industrial]` |

**Per-mark data** (same Nice scope as EUIPO unless noted; Spanish goods/services translation):

- **M1 / M1d Holistika** — clases 35, 41, 42; misma cobertura que EUIPO.
- **M3 Think Big (OEPM-only)** — clases 35, 42. Rótulo: `Think Big`. Servicios (clase 35): consultoría empresarial; asesoría estratégica de negocios. Servicios (clase 42): servicios científicos y tecnológicos; desarrollo de software; servicios de software como servicio (SaaS).
- **M5 / M5a / M5d MADEIRA** — clases 9, 42 únicamente; con limitación expresa: *"El solicitante no reivindica derechos sobre el nombre geográfico Madeira en su sentido geográfico ni en relación con vinos, productos alimentarios, turismo, hostelería, transporte ni servicios médicos."*
- **M6 KiRBe** — clases 9, 42.
- **M7 ENVOY** — clases 9, 42.

(Holistika R&S M2 + HLK Tech Lab M4 do **not** file OEPM separately — protection cascades from EUIPO.)

## 6. Counsel handoff checklist

The filing agent / counsel needs the following before filing day. Items in **bold** require operator action.

| # | Item | Source / who provides |
|:---:|:---|:---|
| 1 | Frozen filing strings | This document §2 |
| 2 | Per-mark Nice classes + goods/services | This document §5 |
| 3 | Per-mark filing strategy (EUIPO/OEPM/both) | This document §4 |
| 4 | **Applicant address (registered SL address)** | Operator |
| 5 | **NIF / CIF** | Operator |
| 6 | **Representative entity (filing agent firm)** | Operator engages firm |
| 7 | **Power of attorney (signed)** | Operator → filing agent |
| 8 | **Logo / wordmark image files** (SVG + PNG; ≤ 2 MB) for design marks | Operator from `boilerplate/public/holistika-*` or `_assets/brand/` |
| 9 | Applicable Nice Classification edition | Filing agent (currently 12-2024) |
| 10 | Live EUIPO + OEPM fee schedule | Filing agent (validated on filing day per Official-Fee Rule §6 of BRAND_HIERARCHY) |
| 11 | **Operator-side budget approval** | Operator (provisional total: €5,500–€7,800 per BRAND_HIERARCHY §5) |
| 12 | **Counsel contract / engagement letter** | Operator + counsel |

## 7. Post-filing operations

After filings are submitted (out of P4 scope; tracked by counsel + Legal Counsel role per `SOP-LEGAL_TRADEMARK_MONITORING_001`):

1. **Examination phase** (EUIPO: 1-3 months; OEPM: 1-2 months). Examiner may issue formal/substantive objections; counsel responds.
2. **Publication phase** — opposition window opens (EUIPO: 3 months; OEPM: 2 months). Third parties may file oppositions.
3. **Opposition response** — if opposition filed, counsel-led response or coexistence-agreement negotiation. ENVOY (M7) is the highest-risk mark per §3.
4. **Registration grant** — typical timeline: 4-9 months from filing to grant.
5. **Renewal** — 10-year terms; first renewal due 10 years post-registration. Tracked by `SOP-LEGAL_TRADEMARK_MONITORING_001` quarterly cadence.

## 8. Cross-references

- [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) — architectural source-of-truth (D-IH-66-A) that this document operationalises.
- [`BRAND_LOGO_SYSTEM.md`](../../Marketing/Brand/BRAND_LOGO_SYSTEM.md) — visual canonicals for design marks.
- [`BRAND_ABBREVIATIONS.md`](../../Marketing/Brand/BRAND_ABBREVIATIONS.md) — short-form governance (HLK Tech Lab paired form).
- [`SOP-TRADEMARK_NAMING_GOVERNANCE_001.md`](SOP-TRADEMARK_NAMING_GOVERNANCE_001.md) — process for adding new sub-mark or product brands (created I66 P4).
- [`SOP-LEGAL_TRADEMARK_MONITORING_001.md`](SOP-LEGAL_TRADEMARK_MONITORING_001.md) — post-filing monitoring (created I66 P3).
- [`SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md`](SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md) — IP register maintenance (created I66 P3).
- I66 master-roadmap §"P4 — Trademark + legal templates".
- [D-IH-66-C](../../../../wip/planning/66-brand-vision-ops-sweep/decision-log.md#d-ih-66-c) — per-jurisdiction filing matrix.
- [D-IH-66-H](../../../../wip/planning/66-brand-vision-ops-sweep/decision-log.md#d-ih-66-h) — agent role ends at "ready-to-sign" (operator-driven submission).
- [D-IH-66-U](../../../../wip/planning/66-brand-vision-ops-sweep/decision-log.md#d-ih-66-u) — filing scope finalisation: 7 marks × ~2 jurisdictions = ~10 filings.

## 9. Maintenance

- **Annual review** alongside `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`.
- **Off-cycle review** when: new sub-mark or product brand introduced; mark refused/granted; opposition filed; renewal due; filing-fee schedule changes materially.
- **Authority for changes**: Founder (final) + Legal Counsel (drafts) + Brand Manager (visual + naming consistency).
