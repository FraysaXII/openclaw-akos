# Decision log — Initiative 15 (HLK API lifecycle + component matrix)

**Status:** Execution tranche 2026-04-20  
**Canonical plan reference:** `.cursor/plans/hlk_api_lifecycle_governance_d63f9966.plan.md` (not edited during implementation)

## D-15-1 — Component matrix location

**Decision:** `COMPONENT_SERVICE_MATRIX.csv` lives under `docs/references/hlk/compliance/` as CTO-chain SSOT (not Envoy markdown).

## D-15-2 — Matriz ingest scope

**Decision:** Only the **components** sheet non-empty rows (97) were ingested; billing/date/helper sheets were out of scope. Source **`Matriz componentes.xlsx`** removed from repo after ingest; original retained by operators externally.

## D-15-3 — `component_id` stability

**Decision:** `comp_matriz_{sheet_row:05d}` keyed to Excel row number for traceability; `component_name` disambiguated with provider and row suffix on collision.

## D-15-4 — API workstream parentage

**Decision:** `env_tech_ws_api_1` uses duplicate parent pattern `env_tech_prj_4` / `env_tech_prj_4` (same as `env_tech_ws_s1`). Children of governance process use `item_parent_2` = workstream, `item_parent_1` = `env_tech_dtp_306`.

## D-15-5 — Matrix maintenance process parent

**Decision:** `env_tech_dtp_313` is child of **IT Catalog** (`env_tech_dtp_156`), not the API workstream.

## D-15-6 — Libraries and language versions SSOT

**Decision:** **Repo-derived default** (lockfiles and manifests) is the SSOT for library and language versions. **`COMPONENT_SERVICE_MATRIX.csv`** holds **exceptions only** (policy, vendor mandate, no-repo components). **No** separate Matriz libraries sheet ingest unless a concrete compliance or architecture driver is recorded in an initiative decision-log. **Forfeit rule:** no `repo_slug` and no approved exception ⇒ row is out of scope for the matrix. (Normative text also in `SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md` §A.3.)
