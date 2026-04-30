---
language: en
status: closed
initiative: 31-holistik-ops-discovery
report_kind: uat-closure
program_id: shared
plane: ops
authority: Founder
last_review: 2026-04-30
---

# UAT closure — Initiative 31 (Holistik Ops Discovery)

**Date:** 2026-04-30
**Scope:** P0 bootstrap + P1 localisation foundation + P2 people axes (persona + GOI/POI distance) + P3 channel touchpoint + P4 touchpoint kit + P5 outbound brief + sourcing register + P6 5-axis meta-doc + P7 tests + closure.
**Closes:** the operator-flagged "we're already operating multilingually across multiple channels and stakeholder types but the system doesn't reflect it" gap. Discovers and codifies the **5-axis Holistik Ops operating system** (Persona × Channel × Distance × Language × Artifact-class).

---

## 1. Verification matrix

| Check | Command | Result | Evidence |
|:------|:--------|:-------|:---------|
| Topic registry validator | `py scripts/validate_topic_registry.py` | **PASS** | 23 rows / 23 topics |
| HLK validator (full) | `py scripts/validate_hlk.py` | **PASS** | 12 programs / 1.093 processes / 65 roles / 23 topics / 6 GOI-POI / 16 personas / 10 channels / 1 vendor / 150 MD files with language |
| Vault link validator | `py scripts/validate_hlk_vault_links.py` | **PASS** | no broken internal `.md` links |
| KM manifest validator | `py scripts/validate_hlk_km_manifests.py` | **PASS** | 11/11 manifests |
| Persona registry validator | `py scripts/validate_persona_registry.py` | **PASS** | 16 personas |
| Channel touchpoint registry validator | `py scripts/validate_channel_touchpoint_registry.py` | **PASS** | 10 channels |
| Sourcing register validator | `py scripts/validate_sourcing_register.py` | **PASS** | 1 vendor (seed) |
| GOI/POI distance extension | `py scripts/validate_goipoi_register.py` | **PASS** | 6 rows, all backfilled to N1 |
| Language frontmatter validator | `py scripts/validate_hlk_language_frontmatter.py` | **PASS** | 150 files scanned, 0 missing language |
| New tests (5 suites) | `py -m pytest tests/test_persona_registry.py tests/test_channel_touchpoint_registry.py tests/test_sourcing_register.py tests/test_localisation_frontmatter.py tests/test_goipoi_distance_extension.py -q` | **PASS** | 39 tests |
| Full pytest sweep (excl. pre-existing config failures) | `py -m pytest tests/ -q --ignore=tests/validate_configs.py` | **PASS** | 757 passed, 5 skipped, 6 warnings |
| Mirror migration staged | `supabase/migrations/20260430210000_i31_goipoi_distance_extension_and_persona_registry.sql` | **STAGED** | DDL: GOI/POI ALTER + 3 new mirror tables (persona / channel touchpoint / sourcing) |
| Mirror reseed SQL staged | `artifacts/sql/i31_persona_channel_sourcing_topic_upsert.sql` | **STAGED** | Operator applies via `npx supabase db push` |
| GOVERNANCE_MOAT drift handled | I30 drift detector caught 19 → 23 topic growth mid-migration | **HANDLED** | Artifact + slide 11 + deck story updated; deck rebuilt clean |

> **Pre-existing failures (NOT introduced by I31 — same posture as I29 / I30):** `tests/validate_configs.py::TestOpenclawConfig::test_validates_via_pydantic` and `test_agents_defaults_sandbox_strict` — relate to an AKOS sandbox-config drift unrelated to I31.

---

## 2. Phase-by-phase deliverables

### P0 — Bootstrap (COMPLETED)

- 6 standard artifacts in [`docs/wip/planning/31-holistik-ops-discovery/`](..) (master-roadmap, decision-log with D-IH-31-A..H, asset-classification, evidence-matrix, risk-register, discovery-taxonomy).
- `reports/` subfolder created.

### P1 — Localisation foundation (COMPLETED)

- New canonical SOP: [`SOP-HLK_LOCALISATION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md).
- New canonical FR brand stub: [`BRAND_FRENCH_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_FRENCH_PATTERNS.md) (`status: stub`).
- New validator: [`scripts/validate_hlk_language_frontmatter.py`](../../../../scripts/validate_hlk_language_frontmatter.py) (hooked into `validate_hlk.py`).
- **Migration**: ~120 canonical Markdown files received `language: en` frontmatter (default); 2 I30 audience-canonical Spanish artifacts (MADEIRA_PLATFORM + GOVERNANCE_MOAT) preserved as `language: es` per D-IH-31-E.

### P2 — People axes (COMPLETED)

- New canonical: [`PERSONA_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv) (16 archetype rows).
- New `akos/hlk_persona_registry_csv.py` field contract.
- New `scripts/validate_persona_registry.py` validator.
- GOI/POI distance extension: [`GOI_POI_REGISTER.csv`](../../../references/hlk/compliance/GOI_POI_REGISTER.csv) gains `distance_band` + `bridge_via` + `distance_assessed_date`; 6 existing rows backfilled to N1.
- [`scripts/validate_goipoi_register.py`](../../../../scripts/validate_goipoi_register.py) gains 4 invariants.
- [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §4.9 distance-assessment subsection added.
- [`scripts/render_pmo_hub.py`](../../../../scripts/render_pmo_hub.py) extended; PMO hub auto-render now includes `distance` + `bridge_via` columns.

### P3 — Channel touchpoint registry (COMPLETED)

- New canonical: [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv) (10 touchpoint rows).
- New `akos/hlk_channel_touchpoint_registry_csv.py` field contract.
- New `scripts/validate_channel_touchpoint_registry.py` validator.

### P4 — Touchpoint kit (COMPLETED)

- New folder [`docs/references/hlk/v3.0/_assets/touchpoint-kit/`](../../../references/hlk/v3.0/_assets/touchpoint-kit/) with README + 15 templates across 8 highest-leverage cells × locales × in-file N-distance variants.

### P5 — Outbound brief + sourcing register (COMPLETED)

- New canonical templates: [`TEMPLATE_OUTBOUND_BRIEF_en.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_en.md) + ES + FR variants (FR variant is the first real exercise of the locale-derivation pipeline).
- New canonical CSV: [`SOURCING_REGISTER.csv`](../../../references/hlk/compliance/dimensions/SOURCING_REGISTER.csv) (1 seed row; operator fills as engagements happen).
- New `akos/hlk_sourcing_register_csv.py` field contract.
- New `scripts/validate_sourcing_register.py` validator.

### P6 — Holistik Ops Discovery meta-doc (COMPLETED)

- New canonical: [`HOLISTIK_OPS_DISCOVERY.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md) — the 5-axis operating system meta-pattern document with cross-axis routing flow + decomposability property + descale-without-impact corollary + **reach-map property** + future hooks.

### P7 — Tests + closure (COMPLETED — this report)

- 5 new test suites (39 tests covering all 5 axes).
- Extended `tests/test_sync_compliance_mirrors_from_csv.py` (new row count assertions).
- CHANGELOG entry shipped.
- This UAT report.
- Mirror migration staged at `supabase/migrations/20260430210000_i31_goipoi_distance_extension_and_persona_registry.sql`.
- Mirror reseed SQL staged at `artifacts/sql/i31_persona_channel_sourcing_topic_upsert.sql`.

---

## 3. Operator follow-up queue

The 11 founder decision markers from I29 + I30 remain open. **No new TODO[OPERATOR-x] markers** were added by I31 in deck-bound surfaces (the persona registry's `intro_artifact_path` markers are operator-fillable but they don't gate the deck). Specific I31 operator follow-ups:

| Item | Action |
|:-----|:-------|
| GOI/POI distance backfill confirmation | Confirm or adjust the 6 backfilled-to-N1 distances; ~5 min review |
| Mirror migration apply | Run `npx supabase db push` after PR merge per [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.1 |
| Mirror reseed | Apply [`artifacts/sql/i31_persona_channel_sourcing_topic_upsert.sql`](../../../../artifacts/sql/i31_persona_channel_sourcing_topic_upsert.sql) |
| Verify mirror counts | `py scripts/probe_compliance_mirror_drift.py --verify` after apply — confirm `persona_registry_mirror=16`, `channel_touchpoint_registry_mirror=10`, `sourcing_register_mirror=1`, `goipoi_register_mirror=6 with distance schema` |
| Persona seed list confirmation | Trim / expand the 16 archetypes per founder review |
| Channel seed list confirmation | Trim / expand the 10 touchpoints per founder review |
| Touchpoint-kit seed cell prioritisation | Are the 8 seeded combinations the right ones? Trivial to add/swap |
| FR brand-voice rules authoring | Defer to first FR external deliverable |
| First quarterly distance re-assessment | Last business day of Q3 2026 (per SOP-HLK_GOIPOI §4.9 cadence) |

---

## 4. Cursor-rules hygiene

- [x] [`akos-docs-config-sync.mdc`](../../../../.cursor/rules/akos-docs-config-sync.mdc) — sync-trigger rows already cover the new artifact patterns added here (CSVs in `dimensions/`, SOPs under `Admin/O5-1/`). **CONFIRMED.**
- [x] [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — every new artifact follows the standard frontmatter contract (status, role_owner, area, entity, plane, topic_ids, parent_topic, artifact_role, intellectual_kind, authority, last_review). All canonical MDs declare `language:` per the new SOP. **CONFIRMED.**
- [x] [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — every founder-decision in I31 is captured as either a TODO[OPERATOR-x] marker or a §3 follow-up item; `validate_hlk` blocks PR merge while invariants fail. **CONFIRMED.**
- [x] [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) — `topic_persona_registry`, `topic_channel_touchpoint_registry`, `topic_sourcing_register`, `topic_holistik_ops_discovery` all registered under plane `ops`. **CONFIRMED.**

---

## 5. Closure assertion

Initiative 31 is **CLOSED** as of 2026-04-30. All P0-P7 deliverables shipped.

The 5-axis Holistik Ops operating system is now governed:

- **Axis 1 (Persona).** 16 archetypes in `PERSONA_REGISTRY.csv` with cross-references to channels and topics.
- **Axis 2 (Channel).** 10 touchpoints in `CHANNEL_TOUCHPOINT_REGISTRY.csv` with cross-references to personas and topics.
- **Axis 3 (Distance).** Live on every named individual in `GOI_POI_REGISTER.csv` (N1-N4 + bridge_via FK + assessed_date); reach-map queryable as a costly-signal asset.
- **Axis 4 (Language).** Every canonical Markdown declares `language:` per `SOP-HLK_LOCALISATION_001.md`; brand voice rules per locale (EN active, ES active, FR stub).
- **Axis 5 (Artifact-class).** Touchpoint kit seeded; outbound brief template proven across EN+ES+FR; meta-doc anchors the system.

The descale-without-impact corollary holds: any axis (persona, channel, distance band, language, artifact-class) can be added or retired with a single CSV / file edit; FK validators block orphan references at PR time.

— Founder + PMO
