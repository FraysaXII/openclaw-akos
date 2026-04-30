---
status: closed
initiative: 30-deck-moat-surgery
report_kind: uat-closure
program_id: shared
plane: ops
authority: Founder
last_review: 2026-04-30
---

# UAT closure — Initiative 30 (Deck moat surgery)

**Date:** 2026-04-30
**Scope:** P0 bootstrap + P1 MADEIRA artifact + P2 joint-equity channel + P3 governance moat + P4 deck restructure + P5 rebuild & verify + P6 tests & closure.
**Closes:** the operator-flagged "deck still feels services-biased" gap by injecting MADEIRA as the second product axis, joint-equity as a sixth channel, and quantified governance metrics as moat pillar 1.

---

## 1. Verification matrix

| Check | Command | Result | Evidence |
|---|---|---|---|
| Topic registry validator | `py scripts/validate_topic_registry.py` | **PASS** | 19 rows / 19 topics |
| HLK validator (full) | `py scripts/validate_hlk.py` | **PASS** | 12 programs / 1.093 processes / 65 roles / 19 topics |
| Vault link validator | `py scripts/validate_hlk_vault_links.py` | **PASS** | no broken internal `.md` links |
| KM manifest validator | `py scripts/validate_hlk_km_manifests.py` | **PASS** | 11/11 manifests |
| Business strategy tests | `py -m pytest tests/test_business_strategy.py` | **PASS** | 19 tests (15 from I29 + 4 from I30) |
| Company deck tests | `py -m pytest tests/test_company_deck.py` | **PASS** | 22 tests (16 from I28+I29 + 6 from I30) |
| Governance moat drift detector | `py -m pytest tests/test_governance_moat_metrics.py` | **PASS** | 5 tests; quoted metrics (19 topics / 1.093 processes / 65 roles / 11 KM manifests) match live counts |
| Sync deck-from-strategy `--check-only` | `py scripts/sync_deck_from_strategy.py` | **PASS** | 12 strategy files; 10 deck-bound (was 8); 9 TODO[OPERATOR-*] tokens in deck-bound blocks |
| Sync deck-from-strategy `--apply` | `py scripts/sync_deck_from_strategy.py --apply` | **REFUSED (rc=2, expected)** | Strategy artifacts retain TODO bands awaiting founder narrowing |
| Mirror reseed SQL staged | `py scripts/sync_compliance_mirrors_from_csv.py --topic-registry-only --out artifacts/sql/i30_topic_registry_business_strategy_upsert.sql` | **STAGED** | 27.520 bytes; operator applies via `npx supabase db push` or MCP `execute_sql` |
| HTML deck rebuild | `py scripts/build_company_deck.py` | **PASS** | 14 slides; html sha256 `5b1d40305b4e2413…` |
| PDF deck export | `py scripts/export_company_deck_pdf.py` | **PASS** | 14 pages; 69.565 bytes; pdf sha256 `3f4d99f35462b72c…` |
| Full pytest sweep (excl. pre-existing config failures) | `py -m pytest tests/ -q --ignore=tests/validate_configs.py` | **PASS** | 717 passed, 5 skipped, 6 warnings |

> **Pre-existing failures (NOT introduced by I30 — same posture as I29):** `tests/validate_configs.py::TestOpenclawConfig::test_validates_via_pydantic` and `test_agents_defaults_sandbox_strict` — relate to an AKOS sandbox-config drift unrelated to I30.

---

## 2. Phase-by-phase deliverables

### P0 — Bootstrap (COMPLETED)

- 5 standard artifacts in [`docs/wip/planning/30-deck-moat-surgery/`](..) (master-roadmap, decision-log with D-IH-30-A..F, asset-classification, evidence-matrix, risk-register).
- `reports/` subfolder created.

### P1 — MADEIRA Platform (COMPLETED)

- New canonical artifact: [`MADEIRA_PLATFORM.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/MADEIRA_PLATFORM.md) (~5.700 chars) with 7 sections + deck-bound facts block.
- New topic row: `topic_madeira_platform` (parent `topic_business_strategy`, plane `ops`).
- 1 new `TODO[OPERATOR-madeira-saas-window]` marker (productization commit window: 6 / 12 / 18 months).

### P2 — Joint-equity channel (COMPLETED)

- [`CHANNEL_STRATEGY.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/CHANNEL_STRATEGY.md) Channel 6 added (~1.700 chars), following the established 5-channel format.
- 1 new `TODO[OPERATOR-channel6-equity-band]` marker.
- Slide-09 ICP block in deck-bound facts updated: ICP 2 renamed "Partner B2B + equidad conjunta".
- Channel matrix summary row added.

### P3 — Governance moat (COMPLETED)

- New canonical artifact: [`GOVERNANCE_MOAT.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/GOVERNANCE_MOAT.md) (~4.500 chars) with 6 sections + deck-bound facts block.
- 4 hero metrics quoted: **19 topics / 1.093 processes / 65 roles / 11 KM manifests**, all sourced from `validate_hlk`.
- Drift detector test (`tests/test_governance_moat_metrics.py`) referenced from the artifact body so future operators understand the parity contract.
- New topic row: `topic_governance_moat` (parent `topic_business_strategy`).

### P4 — Deck restructure (COMPLETED)

- 7 slides edited in [`deck_slides.yaml`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml): 04, 05, 06, 09, 10, 11, 12.
- Slide 06 capability grid restructured: 5 cards now read as **2 hero products (KiRBe + MADEIRA) + 2 demand signals (partner B2B + partner joint-equity) + 1 internal validation (web + ERP combined)**. `stat_grid` swapped to read "2 productos propios / 2 partners en demanda / 1.093 procesos / 2023".
- Slide 11 pillar 1 replaced with "Operación gobernada y medible" quoting the 4 governance metrics directly.
- Mirror narrative in [`deck_story_es.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_story_es.md) sections 04, 05, 06, 09, 10, 11, 12 updated to match.

### P5 — Rebuild + verify (COMPLETED)

- HTML deck: `docs/presentations/holistika-company-dossier/index.html` rebuilt; sha256 `5b1d40305b4e2413…`.
- PDF deck: `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf` re-exported; sha256 `3f4d99f35462b72c…`; 14 pages; 69.565 bytes.
- Mirror reseed SQL staged at `artifacts/sql/i30_topic_registry_business_strategy_upsert.sql` (27.520 bytes; git-ignored per .gitignore artifacts/sql/*.sql convention; operator applies via `npx supabase db push` or MCP `execute_sql`).
- All validators green at the new totals.

### P6 — Tests + closure (COMPLETED — this report)

- 4 new tests in `tests/test_business_strategy.py` (MADEIRA + GOVERNANCE_MOAT artifact presence, topic FK resolution, joint-equity channel + equity-band TODO, expected_children grown to 13).
- 6 new tests in `tests/test_company_deck.py` (MADEIRA on YAML + story, card-madeira list item, slide 11 governance metrics, slide 09 joint-equity, slide 10 MADEIRA in tomorrow tier, slide 12 MADEIRA in 12-24m phase, HTML deck carries MADEIRA after rebuild).
- New test suite `tests/test_governance_moat_metrics.py` (5 tests — drift detector with tolerance bands per D-IH-30-F).
- `tests/test_sync_compliance_mirrors_from_csv.py` updated `topic_registry_rows=17` → `topic_registry_rows=19`.
- CHANGELOG entry shipped.
- This UAT report.

---

## 3. Operator follow-up queue (TODO[OPERATOR-x] markers)

The strategy SSOT now carries **11 founder decision markers** (9 inherited from I29 P4 + 2 new from I30):

| Marker | File | Decision needed |
|---|---|---|
| `TODO[OPERATOR-bootstrap-personal]` | `BOOTSTRAPPING_PLAN.md` | Personal monthly draw band |
| `TODO[OPERATOR-bootstrap-burn]` | `BOOTSTRAPPING_PLAN.md` | Business burn band |
| `TODO[OPERATOR-bootstrap-runway]` | `BOOTSTRAPPING_PLAN.md` | Runway threshold for raise-vs-bootstrap decision |
| `TODO[OPERATOR-bootstrap-break-even]` | `BOOTSTRAPPING_PLAN.md` | Break-even month under base scenario |
| `TODO[OPERATOR-thesis-amount-band]` | `INVESTMENT_THESIS.md` | If/when raise: amount band + dilution range |
| `TODO[OPERATOR-pricing-service-rate]` | `PRICING_MODEL.md` | Service rate card concrete numbers |
| `TODO[OPERATOR-pricing-kirbe-tier]` | `PRICING_MODEL.md` | KiRBe SaaS tier prices |
| `TODO[OPERATOR-pricing-partner-share]` | `PRICING_MODEL.md` | Partner revenue share % per channel |
| `TODO[OPERATOR-unit-blended-cac]` | `UNIT_ECONOMICS.md` | Blended CAC target across the 5 channels |
| **`TODO[OPERATOR-madeira-saas-window]`** | `MADEIRA_PLATFORM.md` | **MADEIRA productization commit window: 6 / 12 / 18 months** |
| **`TODO[OPERATOR-channel6-equity-band]`** | `CHANNEL_STRATEGY.md` | **Joint-equity / revenue-share band for Channel 6** |

**Resolution path:** edit the artifact, replace the `TODO[OPERATOR-x]` token with the chosen value, re-run `py scripts/sync_deck_from_strategy.py --apply` (currently refuses with `rc=2` until at least the deck-bound TODOs are narrowed), verify HTML + PDF rebuild clean, log the decision in [`STRATEGY_DECISION_LOG.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/STRATEGY_DECISION_LOG.md).

**Mirror reseed:** apply [`artifacts/sql/i30_topic_registry_business_strategy_upsert.sql`](../../../../artifacts/sql/i30_topic_registry_business_strategy_upsert.sql) via `npx supabase db push` (preferred) or MCP `execute_sql` with `service_role`. After reseed, run `py scripts/probe_compliance_mirror_drift.py --verify` to confirm `topic_registry_mirror=19`.

---

## 4. Cursor-rules hygiene

- [x] [`akos-docs-config-sync.mdc`](../../../../.cursor/rules/akos-docs-config-sync.mdc) — no new sync triggers required (the I29 P2 triggers cover the artifact patterns added here: business-strategy/*.md, TOPIC_REGISTRY.csv, deck SSOT). **CONFIRMED.**
- [x] [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — both new strategy artifacts follow the standard frontmatter contract (status, role_owner, area, entity, program_id, plane, topic_ids, parent_topic, artifact_role, intellectual_kind, authority, last_review); `deck_bound` + `deck_slides_consumed` slots filled. **CONFIRMED.**
- [x] [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — every TODO[OPERATOR-x] is a tracked decision; STRATEGY_DECISION_LOG.md is the resolution surface; sync_deck_from_strategy.py refuses --apply while tokens remain. **CONFIRMED.**
- [x] [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) — `topic_madeira_platform` and `topic_governance_moat` registered under the correct plane (`ops`); both link back to the parent `topic_business_strategy`. **CONFIRMED.**

---

## 5. Closure assertion

Initiative 30 is **CLOSED** as of 2026-04-30. All P0-P6 deliverables shipped. The 11 founder decision markers and the mirror reseed are operator-side work captured in §3, not initiative scope.

The deck now reads as a 2-product company with 2 active partner demand signals + 1 internal validation, anchored on quantified governance — not a 5-card services factory. MADEIRA is named as the second product axis; joint-equity is named as the highest-demand channel; and the moat is replaced from qualitative claim to live-validator-backed metric.

The Figma backport (per D-IH-30-E) is queued for the next operator-scheduled session — until then, the YAML/Markdown SSOT carries the I30 edits and the Figma file at `https://www.figma.com/design/yiPav7BLxUulNFrrsoKJqW` stays on its I29 P1 frame copy.

— Founder + PMO
