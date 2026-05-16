# I81 — Asset classification

Per [`PRECEDENCE.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md). Defines what each artefact touched by I81 is in the SSOT hierarchy.

## Canonical (edit here first; SSOT)

| Path | Phase | Action |
|:---|:---|:---|
| [`INITIATIVE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) | P0 | Append `INIT-OPENCLAW_AKOS-81` row (status=active) |
| [`DECISION_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | P0 | Append 5 rows for D-IH-81-A/B/C/E/H (P0 ratified) |
| [`OPS_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) | P0 | Append `OPS-81-1` charter-scaffold row |
| `compliance/` legacy root CSVs | P2 | Migrate to Initiative 22 forward-layout subfolders (`dimensions/` / `advops/` / `finops/` / `techops/`) per operator-approved tranche; update `PRECEDENCE.md` |
| `akos/hlk_planning_milestone.py` | P3 | Mint Pydantic SSOT for milestone schema (`MILESTONE_ID_PATTERN` regex; `Literal['planned','in_progress','closed','cancelled']` status enum) |
| `scripts/validate_planning_cross_refs.py` | P3 | Mint class-B drift validator (walks `_candidates/*.md` + `_templates/*.md` + active `<NN-slug>/master-roadmap.md`) |
| `tests/test_planning_cross_refs.py` | P3 | Mint pytest suite (`@pytest.mark.governance`; valid + invalid input pairs) |
| 40 SOP body files (across 11 areas) | P4-P8 | Retrofit per `pattern_sop_addendum_split`; ~28-36 paired-file outcomes expected |
| `.cursor/rules/akos-planning-traceability.mdc` | P3 | Extend §"Plan-quality bar" to require named-milestone convention |

## Canonical modifications (edit here in lockstep with canonical moves)

| Path | Phase | Action |
|:---|:---|:---|
| [`PRECEDENCE.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) | P2 | Update path anchors per tranche |
| Per-validator `Path` constants (`scripts/validate_*.py`) | P2 | Update in lockstep with `git mv` |
| [`scripts/sync_compliance_mirrors_from_csv.py`](../../../scripts/sync_compliance_mirrors_from_csv.py) | P2 | Update CSV→table mappings |
| [`scripts/validate_hlk.py`](../../../scripts/validate_hlk.py) | P3 | Wire in `validate_planning_cross_refs.py` |
| [`scripts/release-gate.py`](../../../scripts/release-gate.py) | P3 | Wire in new validator |
| [`config/verification-profiles.json`](../../../config/verification-profiles.json) | P3 | Add new validator to `pre_commit` profile |

## Mirrored / derived (regenerable; no direct authoring)

| Path | Action |
|:---|:---|
| `compliance.*_mirror` tables (Supabase) | Path moves in P2 re-mapped by `sync_compliance_mirrors_from_csv.py`; mirror emit profile re-runs |
| KM manifest FK paths | Updated by `validate_hlk_km_manifests.py` re-runs after each P2 tranche |
| `hlk-erp` panel route strings + API contracts | Updated per cross-repo schema propagation SOP per P2 tranche |

## Reference (planning-internal evidence; not SSOT)

| Path | Phase | Purpose |
|:---|:---|:---|
| `reports/i81/kb-integrity-audit-<date>.md` | P1 | Human-readable synthesis of integrity sprint |
| `reports/i81/kb-integrity-matrix-<date>.csv` | P1 | Machine-readable matrix (one row per `process_list.csv` executable row) |
| `reports/p3-class-b-regression-sweep-<date>.md` | P3 | One-shot historical baseline scan informing validator's rule set |
| `reports/p<NN>-uat-<date>.md` | P9 | Closure UAT report |

## Engineering surface (governed by [`CONTRIBUTING.md`](../../../CONTRIBUTING.md))

- `akos/hlk_planning_milestone.py` — Pydantic models; type hints; structured logging via `akos.log.setup_logging`.
- `scripts/validate_planning_cross_refs.py` — `pathlib.Path`; structured logging; subprocess via `akos.process.run` if shelling out.
- `tests/test_planning_cross_refs.py` — `@pytest.mark.governance`; registered in `scripts/test.py` group list; valid + invalid input pairs.

## Out of scope

- Net-new SOPs minted by other initiatives during I81 execution (those ship paired at mint time per I80 contract).
- Closed-initiative master-roadmaps + reports (frozen historical records per D-IH-81-J).
- Per-area register-specific jargon validators (D-IH-81-E — out of scope).
