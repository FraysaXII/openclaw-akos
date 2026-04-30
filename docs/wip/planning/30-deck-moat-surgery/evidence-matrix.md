# Initiative 30 — Evidence matrix

Maps every claim made by this initiative to its source of truth. Each row is something a reader (founder, advisor, certifier, investor) might challenge — the matrix points at the artifact that backs it.

| Claim | Source | Verifiable how |
|:------|:-------|:---------------|
| MADEIRA is a first-class internal concept | [`SOP-MADEIRA_HLK_ERP_SHOWCASE_004.md`](../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_HLK_ERP_SHOWCASE_004.md), [`SOP-MADEIRA_ENVOYTECH_SHOWCASE_002.md`](../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_ENVOYTECH_SHOWCASE_002.md), [`platform/README.md`](../../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/platform/README.md) | `rg "MADEIRA" docs/references/hlk/` returns 10+ files |
| MADEIRA is referenced from KIR program onboarding | [`programs/PRJ-HOL-KIR-2026/README.md`](../../references/hlk/v3.0/Admin/O5-1/People/programs/PRJ-HOL-KIR-2026/README.md) | Read the file; MADEIRA is named in the role narrative |
| MADEIRA is in the Think Big section | [`Think Big/README.md`](../../references/hlk/v3.0/Think%20Big/README.md) | Read the file |
| Joint-equity demand is real (not aspirational) | [`POC_TO_COMMERCIAL_MAP.csv`](../../references/hlk/compliance/dimensions/POC_TO_COMMERCIAL_MAP.csv) rows `POC-WEBSITZ-SHOPIFY-2026` (`engagement_type=partner_subcontracted`) and `POC-RUSHLY-SCAFFOLD-2026` (`engagement_type=partner_design_phase`) | Open the CSV; both rows describe partner-anchored deliveries with revenue band still TODO[OPERATOR-x] (the bands are confidential, not absent) |
| Holistika has 17 governed topics | [`TOPIC_REGISTRY.csv`](../../references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv) | `py scripts/validate_topic_registry.py` reports row count (will become 19 after I30 P1+P3) |
| Holistika has 1,093 governed processes | [`process_list.csv`](../../references/hlk/compliance/process_list.csv) | `py scripts/sync_compliance_mirrors_from_csv.py --count-only` reports `process_list_rows=1093` |
| Holistika has 65 governed roles | [`baseline_organisation.csv`](../../references/hlk/compliance/baseline_organisation.csv) | `py scripts/sync_compliance_mirrors_from_csv.py --count-only` reports `baseline_organisation_rows=65` |
| Holistika has 11 KM Output 1 manifests | KM manifests under `docs/references/hlk/v3.0/_assets/` matching `*.manifest.md` | `py scripts/validate_hlk_km_manifests.py` reports `OVERALL: PASS` over 11 manifests |
| Three layers of validators (artifact / FK / mirror drift) | `scripts/validate_hlk.py` (artifact), `scripts/validate_program_id_consistency.py` (FK), `scripts/probe_compliance_mirror_drift.py` (mirror) | Run each; each exits 0 |
| Jargon-audit gate on every external deliverable | [`scripts/build_company_deck.py`](../../../scripts/build_company_deck.py) raises if any forbidden token reaches slide copy | Read the script; the gate is implemented |
| Deterministic build pipeline (HTML + PDF reproducible from YAML) | `build_company_deck.py` + `export_company_deck_pdf.py` | Re-run both; output sha256 matches manifest |
| Same architecture entrega web, ERP, SaaS, partner apps | `POC_TO_COMMERCIAL_MAP.csv` rows + the 5 capability cards in slide 06 | Read the CSV + slide 06 in the deck |
| Descale without impact (1-commit program teardown) | The `program_id` axis in `compliance/` + `_assets/<plane>/<program_id>/<topic_id>/` layout (Initiative 22) | A program shutdown is "delete the row in `PROGRAM_REGISTRY.csv` + delete the folder under `_assets/<plane>/<program_id>/`"; rerun `validate_hlk` to confirm no orphan FKs |

## How a reader audits the deck

1. Open `deck_slides.yaml` and walk slide 06 cards. Cross-check each `card-*` against `POC_TO_COMMERCIAL_MAP.csv` (or, for `card-madeira`, against `MADEIRA_PLATFORM.md`).
2. Open slide 11 pillar 1 and cross-check the four numbers against the live `py scripts/validate_hlk.py` output.
3. Open slide 09 ICP 2 ("Partner B2B + joint-equity") and cross-check against `CHANNEL_STRATEGY.md` Channel 2 + Channel 6.
4. Open slide 12 and cross-check the 12-24m bullet against `MADEIRA_PLATFORM.md` §"Commercial path".
5. Re-run `py scripts/sync_deck_from_strategy.py` — it tells the reader exactly which strategy artifacts feed which slides.
