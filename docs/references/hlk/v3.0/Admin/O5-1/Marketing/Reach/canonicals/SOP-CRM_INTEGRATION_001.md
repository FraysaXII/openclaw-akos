---
language: en
status: review
canonical: true
role_owner: RevOps Lead
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-O
methodology_version_at_review: v3.0
companion_to:
  - REACH_AREA_CHARTER.md
  - dimensions/CRM_ADAPTER_REGISTRY.csv
  - ../../../Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md
---

# SOP-CRM_INTEGRATION_001 — Multi-CRM adapter integration via Normalized Adapter Pattern

> Authored I72 P9 per `D-IH-72-A` (P0 charter), `D-IH-72-O` (GTM/CRM scope = AKOS-internal SSOT + HubSpot adapter shim + multi-CRM Normalized Adapter Pattern + active/inactive/planned/experimental/deprecated metadata per Truto/Unified.to/Apideck consensus 2026), `D-IH-72-L` (Strand D charter). Codifies how Holistika integrates multiple CRM platforms behind a uniform normalized API per industry-standard pattern.

## 1. Purpose

Establish the Normalized Adapter Pattern as the integration discipline for `CRM_ADAPTER_REGISTRY.csv` rows so:

1. **AKOS-internal `holistika_ops` adapter** stays the SSOT seed (status=active; first_party_internal kind; always_on flag).
2. **External CRM adapters** mount as normalized shims behind a uniform API (HubSpot + Salesforce planned; Attio experimental; 7 others inactive).
3. **Lifecycle metadata** drives operator-visible status (active/inactive/planned/experimental/deprecated) per D-IH-72-O.
4. **Cross-area handoffs** between Marketing/Reach (capture inbound) + RevOps (revenue spine) flow through the active adapter row.

## 2. Scope

In scope: All CRM_ADAPTER_REGISTRY.csv rows. Out of scope: per-vendor SDK details (covered by per-adapter implementation; this SOP is the integration discipline contract).

## 3. Steps

### 3.1 Normalized API surface

Define the Holistika-internal CRM API: contact CRUD + deal CRUD + activity log + custom fields. All adapters expose this API; per-vendor calls translate via the adapter shim.

### 3.2 Adapter activation flow

To activate a planned adapter (e.g., HubSpot):

1. Implement the shim per `akos.hlk_adapter_registry_csv` ADAPTER_REGISTRY_FIELDNAMES contract.
2. Update the CRM_ADAPTER_REGISTRY.csv row: status=`planned` → `experimental` (gated_operator) → `active` (gated_release_gate or always_on).
3. Validate via `py scripts/validate_adapter_registries.py`.
4. Operator ratifies activation via AskQuestion in commit author chat.

### 3.3 Adapter deactivation flow

Reverse: status=`active` → `inactive` (operator-flipped) OR `deprecated` (irreversible). Document rationale in `notes` cell + create `D-IH-*-CLOSURE` decision row.

### 3.4 Cross-area handoff

When a CRM adapter is active, Marketing/Reach (PERSONA-* qualified leads) + RevOps (engagement-template promotion) consume from the adapter; RevOps Lead reviews adapter health quarterly per `SOP-REVOPS_QBR_001.md`.

## 4. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **AC-HUMAN**: RevOps Lead executes activation/deactivation flow manually using only this SOP body; CSV-as-SSOT discipline preserved.
- **AC-AUTOMATION**: `validate_adapter_registries.py` PASS on CRM_ADAPTER_REGISTRY.csv with all 11 vendor rows.

## 5. Failure modes

- **Vendor API breaking change**: flip status=`active` → `inactive` (operator-gated); fix adapter; re-activate.
- **Authentication / rate-limit collapse**: temporary feature_flag=`gated_operator`; resume when vendor recovers.
- **Multi-CRM customer wants both adapters live**: both adapters can be `active` simultaneously; downstream consumer (RevOps QBR) reconciles.

## 6. Cross-references

- Parent area charter: [`REACH_AREA_CHARTER.md`](REACH_AREA_CHARTER.md).
- Sister area charter: [`REVOPS_AREA_CHARTER.md`](../../../Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md).
- Adapter rows: `CRM_ADAPTER_REGISTRY.csv` (11 vendor rows: 1 active + 7 inactive + 2 planned + 1 experimental).
- akos SSOT: [`akos/hlk_adapter_registry_csv.py`](../../../../../../akos/hlk_adapter_registry_csv.py).
- Validator: [`scripts/validate_adapter_registries.py`](../../../../../../scripts/validate_adapter_registries.py).
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 2 (active/inactive metadata) + Rule 4 (DAMA-DMBOK alignment).
- Decisions: D-IH-72-A, D-IH-72-O, D-IH-72-T, D-IH-72-L, D-IH-72-W (feature-flag pattern).
