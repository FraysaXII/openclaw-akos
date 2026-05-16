# I82 — Asset classification

Per [`PRECEDENCE.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md). Defines what each artefact touched by I82 is in the SSOT hierarchy.

## Canonical (edit here first; SSOT)

| Path | Phase | Action |
|:---|:---|:---|
| [`INITIATIVE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) | P0 | Append `INIT-OPENCLAW_AKOS-82` row (status=active) |
| [`DECISION_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | P0 | Append 5 rows for D-IH-82-A/B/NAME/ARCHIVIST/SEQUENCE (P0 ratified) |
| [`OPS_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) | P0 | Append `OPS-82-1` charter-scaffold + live-UAT scheduling row |
| `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_CAPABILITY_DOCTRINE.md` (+ `.addendum.md`) | P0 followup | Mint paired body+addendum per `pattern_sop_addendum_split` |
| [`baseline_organisation.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) | P1 | **Operator gate** — Talent role activation tranche |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv` | P2 | Mint canonical + Pydantic SSOT (`akos/hlk_capability_registry_csv.py`) + validator (`scripts/validate_capability_registry.py`) + tests |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv` (+ paired `.addendum.md`) | P3 | Mint paired body+addendum |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/USE_CASE_ARCHIVE.csv` | P4 | Mint canonical + Pydantic SSOT (`akos/hlk_use_case_archive_csv.py`) + validator + tests + 5 seed POC rows |
| [`CANONICAL_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv) | P2-P4 | Append rows for each new canonical (registry + doctrine + 2 facet registries) |
| [`PRECEDENCE.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) | P2-P4 | Register canonical + mirror rows per minted registry |

## Canonical modifications (edit here in lockstep with cascading effects)

| Path | Phase | Action |
|:---|:---|:---|
| [`BRAND_BASELINE_REALITY_MATRIX.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) | P5 | Append §N "Capability messaging extension" with per-audience translation tables |
| [`scripts/validate_hlk.py`](../../../scripts/validate_hlk.py) | P2-P4 | Wire in new validators (capability + confidence + use-case) |
| [`scripts/release-gate.py`](../../../scripts/release-gate.py) | P2-P4 | Wire in new validators |
| [`config/verification-profiles.json`](../../../config/verification-profiles.json) | P2-P4 | Add new validators to `pre_commit` profile |
| [`process_list.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) | P1 | Optional accompaniment row(s) defining Talent upkeep mechanics (operator gate) |

## Mirrored / derived (regenerable; no direct authoring)

| Path | Action |
|:---|:---|
| `compliance.capability_registry_mirror` (Supabase) | Per P2 via `sync_compliance_mirrors_from_csv.py` |
| `compliance.capability_confidence_registry_mirror` (Supabase) | Per P3 |
| `compliance.use_case_archive_mirror` (Supabase) | Per P4 — RLS posture: `service_role` only; PII risk per redaction class |
| `hlk-erp` capability-surfacing panel + API routes | P6 forward-spec alignment |

## Reference (planning-internal evidence; not SSOT)

| Path | Phase | Purpose |
|:---|:---|:---|
| `reports/p0-doctrine-uat-<date>.md` | P0 followup | Operator review of doctrine prose |
| `reports/p2-capability-registry-uat-<date>.md` | P2 | Operator review of seed-row anchors against I81 P1 integrity matrix |
| `reports/p7-live-capability-surfacing-uat-<date>.md` | P7 | Live external-stakeholder rehearsal evidence (or waiver narrative) |

## Engineering surface (governed by [`CONTRIBUTING.md`](../../../CONTRIBUTING.md))

- `akos/hlk_capability_registry_csv.py` — Pydantic models; `Literal` enums; type hints.
- `akos/hlk_capability_confidence_registry_csv.py` — same standards.
- `akos/hlk_use_case_archive_csv.py` — same standards + `redaction_class` enum.
- `scripts/validate_capability_registry.py` — `pathlib.Path`; structured logging; FK resolution to `process_list.csv` + `SKILL_REGISTRY.csv`.
- `scripts/validate_capability_confidence_registry.py` — paired-file validation per `pattern_sop_addendum_split`.
- `scripts/validate_use_case_archive.py` — FK resolution to `CAPABILITY_REGISTRY.csv` + `ENGAGEMENT_REGISTRY.csv` (if exists) + redaction-class enum enforcement.
- `tests/test_capability_registry.py` + `tests/test_capability_confidence_registry.py` + `tests/test_use_case_archive.py` — `@pytest.mark.governance`; valid + invalid input pairs.

## Out of scope (forward-chartered)

- **AI Archivist + KiRBe ingestor system** — forward to I83 (Tech-area-led; consumes I82 P4 USE_CASE_ARCHIVE data layer).
- **Per-engagement capability rehearsal scripting** — out of doctrine scope; operator + Talent run rehearsals organically.
- **External branded landing page for capabilities** — Marketing/Brand future initiative; doctrine carries the rails (P5 eloquence extension), not the rendered page.
