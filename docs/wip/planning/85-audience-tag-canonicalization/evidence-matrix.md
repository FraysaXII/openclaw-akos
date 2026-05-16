---
initiative_id: I85
language: en
last_review: 2026-05-16
---

# I85 — Evidence matrix

I86 D-IH-86-D mechanical cross-check before sibling closure verifies the rows below + `validate_hlk` + release-gate PASS.

| Phase | Deliverable | Verification | Artefact |
|:---|:---|:---|:---|
| **P0** | Initiative folder + 6 planning files + INIT/DEC/OPS rows + INITIATIVE_DEPENDENCIES + planning README | `py scripts/validate_hlk.py` PASS; `py scripts/verify.py pre_commit` PASS | This commit; `files-modified.csv` rows phase=P0 |
| **P1** | `AUDIENCE_REGISTRY.csv` (8 seed rows) + `akos/hlk_audience_csv.py` + `scripts/validate_audience_registry.py` + `tests/test_audience_registry.py` + `CANONICAL_REGISTRY.csv` 2 rows + `SOP-AUDIENCE_TAG_GOVERNANCE_001.md` at `status: review` | `pytest tests/test_audience_registry.py` GREEN; `validate_hlk` PASS; CANONICAL_REGISTRY validator PASS | `reports/p1-canonical-mint-uat-<date>.md` |
| **P2** | `scripts/audience_tag_assets.py` + `scripts/validate_audience_tags.py`; tranche dry-runs + operator-approved tag applies for advops/decks + advops/dossiers + touchpoint-kit/emails | Drift gate GREEN post-sweep; tranche reports show operator approval per file-class; `validate_hlk` PASS | `reports/p2-tranche-<tranche-id>-uat-<date>.md` (3 reports) |
| **P3** | `BASELINE_REALITY.md` carries `audience: [J-OP]`; `BRAND_BASELINE_REALITY_MATRIX.md` §"Multi-audience composition recipe" present; Impeccable bridge re-runs green | Impeccable `/audit BASELINE_REALITY.md` outputs no missing-frontmatter finding; matrix §recipe present + cross-references registered | `reports/p3-bridge-matrix-update-<date>.md` |
| **P4 (closure)** | Release-gate 8/8 PASS; UAT report; CHANGELOG; SOP `review → active`; INITIATIVE_REGISTRY flip `active → closed` | `py scripts/release-gate.py` 8/8; `py scripts/validate_hlk.py` PASS; UAT report sections per shape table; I86 D-IH-86-D mechanical cross-check PASS | `reports/uat-i85-closure-<date>.md` |

## I86 mechanical cross-check (D-IH-86-D) ordered list

Before flipping `INIT-OPENCLAW_AKOS-85` to `status: closed`, closure UAT must demonstrate:

1. All four phases above show rows in `files-modified.csv` with `change_kind` matching deliverable.
2. `validate_hlk.py` PASS in P4 transcript.
3. `release-gate.py` 8/8 PASS in P4 transcript.
4. `pytest tests/test_audience_registry.py` GREEN.
5. SOP+runbook pair both present (per `akos-executable-process-catalog.mdc` Rule 1): `SOP-AUDIENCE_TAG_GOVERNANCE_001.md` + `scripts/audience_tag_assets.py`.
6. UAT report at `reports/uat-i85-closure-<date>.md` with row outcomes per phase table.
7. `BASELINE_REALITY.md` Impeccable audit re-run shows finding #7+#8+#9 cleared.
8. I81 P1 evidence pack consumes `audience_tags_coverage` column (cross-initiative wire intact).
9. R-IH-85-1..5 status reviewed; any remaining `Open` items forwarded as fresh OPS rows.
