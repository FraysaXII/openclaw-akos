---
intellectual_kind: mint_gate_packet
authored: 2026-06-15
status: operator_ratified_2026-06-15
ratified_by: operator
ratified_at: 2026-06-15
execution_tranche: T1-cap-GCI
execution_status: committed_2026-06-15
decision_id: D-IH-76-Q
prerequisite: capability-registry-semantic-review-2026-06-15.md + post-sweep gap analysis
gate_type: canonical_csv_mint
decision_proposed: D-IH-76-CAP-GCI
operator_pre_authorization: D-IH-76-CAP full GCI bundle 2026-06-15
---

# Mint gate packet — capability governance tranche (GCI / T1-cap)

> **Plain language:** This tranche makes the “what Holistika can do” map **trustworthy for v3.2 closed alpha** — linking alpha claims (CAP-M01..M30) to vault capability rows, filling in which runtime delivers each one, expanding implementation proof, and tightening the validator so hollow FKs cannot pass silently again.

## Summary counts

| Artifact | Change |
|:---|:---|
| `CAPABILITY_REGISTRY.csv` | +4 rows; amend 18 substrate FKs; +1 column `alpha_inventory_refs`; v3.2 refresh on touched rows |
| `AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` | +23 rows |
| `CAPABILITY_ALPHA_CROSSWALK.csv` | **New** dimension (36 edges) — justified M:N alpha↔vault |
| `CANONICAL_RELATIONSHIP_REGISTRY.csv` | +1 triple schema row (capability,maps,alpha_inventory_seed) optional |
| `akos/hlk_capability_registry_csv.py` | +`alpha_inventory_refs` field |
| `scripts/validate_capability_registry.py` | FAIL empty substrate on active Applied AI & MADEIRA |
| `DECISION_REGISTER.csv` | +1 `D-IH-76-CAP-GCI` |

## A. New capability rows (4 net-new)

| capability_id | Plain name | lifecycle | l1_domain | substrate |
|:---|:---|:---|:---|:---|
| `CAP-MADEIRA-INTERACTION-MODE-PARITY` | Five MADEIRA interaction modes | active | Applied AI & MADEIRA | SUBS-ANYSPHERE-CURSOR-SDK |
| `CAP-MADEIRA-TOOL-CATEGORY-RBAC` | Tool category RBAC (16 cats) | active | Applied AI & MADEIRA | SUBS-HOLISTIKA-OPENCLAW |
| `CAP-MADEIRA-RESEARCH-CENTER-SURFACE` | Research Center operator UI | active | Applied AI & MADEIRA | SUBS-HOLISTIKA-LLAMAINDEX-WORKER |
| `CAP-MADEIRA-CONTEXT-ECONOMICS` | Metered context (cache/compaction/postprocess) | **planned** | Applied AI & MADEIRA | SUBS-HOLISTIKA-OPENCLAW |

Originating process IDs: derived from matrix owner initiatives (MADEIRA SOPs / hol_peopl / env_tech process stubs) — full IDs in execution commit.

## B. Substrate backfill (18 amendments)

See semantic review table — all FKs resolve to existing `SUBSTRATE_REGISTRY` rows post-T1b.

## C. Schema extension

**Column:** `alpha_inventory_refs` on `CAPABILITY_REGISTRY.csv`  
**Format:** semicolon-delimited `CAP-M01`..`CAP-M30` refs (reverse index from crosswalk primary edges)  
**Rationale:** Reuses main registry per operator preference; crosswalk CSV holds M:N supplements only.

## D. Crosswalk dimension (new)

**Path:** `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_ALPHA_CROSSWALK.csv`  
**Source draft:** `docs/wip/intelligence/.../wip/CAPABILITY_ALPHA_CROSSWALK.csv` (36 rows)  
**Why not registry-only:** 12 alpha seeds map to 2+ vault rows (e.g. M01 → conversational + agentic ops).

## E. ACIM expansion (+23 rows)

Coverage target: every CAP-M row with maturity Built/Partial except M27 (post-α2). Each row binds `AIC-MADEIRA-ON-CURSOR` or `AIC-CURSOR-BORROWED` with `tool_catalog_ref` pointing to validator script or rule path.

## F. Validator ramp (GCI-04)

On same commit:

```text
IF lifecycle_status=active AND l1_domain='Applied AI & MADEIRA' AND substrate_id empty → FAIL
```

Other domains: remain allowed empty at α0.

## G. Out of scope (this tranche)

- T2 `akos/postprocess.py` implementation (spec ratified; separate tranche)
- `MADEIRA_AIC_PER_TASK_REGISTRY` column extensions (ratified for T2)
- OpenClaw H3–H5 hardening (after T2)
- CAP-M27 vault row
- Bulk substrate backfill for all 99 rows

## Verification matrix

```powershell
py scripts/validate_capability_registry.py
py scripts/validate_aic_capability_implementation_matrix.py
py scripts/validate_hlk.py
py scripts/verify.py pre_commit_fast
```

## Evidence bundle

| Report | Path |
|:---|:---|
| Pre-sweep | `reports/capability-registry-gap-analysis-pre-sweep-2026-06-15.md` |
| Semantic review | `reports/capability-registry-semantic-review-2026-06-15.md` |
| Post-sweep | `reports/capability-registry-gap-analysis-post-sweep-2026-06-15.md` |
| Crosswalk draft | `wip/CAPABILITY_ALPHA_CROSSWALK.csv` |
