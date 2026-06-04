# Runbook — MS Demo Factory Method B (Portal + Browser)

> Paired with `SOP-DATA_MS_DEMO_FACTORY_001.md` · method `MS-DEMO-METHOD-B` ·
> registry `akos/hlk_ms_demo_methods.py`.

## When to use

- Licensing, environment creation, or canvas layout requires portal UI.
- Deliverable includes **screenshots** for customer-pack PDF (Method A export insufficient).
- Composio Browser Tool available; no Power Platform MCP required.

## Prerequisites

- Holistika Microsoft tenant with Power Apps / Power Automate licenses provisioned.
- Engagement scaffold signed.
- Composio Browser Tool active; operator available for consent dialogs.
- Anonymised referential ready (Excel or CSV seed).

## Procedure

### 1. Operator opens admin surfaces

- [Power Platform admin center](https://admin.powerplatform.microsoft.com/)
- Target environment selected (Holistika Phase 1 — not client tenant unless ratified)

AIC drives Browser Tool **under operator watch** for subsequent steps.

### 2. Create or open solution

- New solution named `<ENG>-<capability>-demo` (e.g. `SUEZ-F05-libelle-demo`).
- Add canvas app + cloud flow to solution for clean export later.

### 3. Build referential

Upload three-tab Excel (parc, suppliers, naming rules) per demo spec, or link SharePoint list.
Use **generic names only** in captured screenshots.

### 4. Build canvas app

Fields: parc picker, intervention code, supplier, devis/facture (maintenance path); CAPEX branch per spec.
Display composed libellé for one-click validation.

### 5. Build cloud flow

Trigger: email arrival → parse entities → lookup referential → apply category rule → output libellé.
Test with fixtures; screenshot each step for evidence folder.

### 6. Screenshot capture

Save to `00-internal/evidence/<date>-method-b/`:

- Referential structure (blurred if needed)
- Canvas app validation screen
- Flow run history (success)
- Sample output libellé

### 7. Registry before sign-off

Activate `BI-HOL-POWER-PLATFORM` and `power_platform` adapter if not already active.

```powershell
py scripts/bi_integration_readiness_check.py --report
```

## Combining with Method A

Typical pattern: **B** builds and captures evidence; **A** exports solution for repeatability and Phase 2 handoff (`pac solution export`).

## Escalation

| Blocker | Escalate to |
|:---|:---|
| Browser auth / MFA loop | Operator takes over keyboard |
| Connector policy blocked | System Owner + client DSI if client tenant |
| Screenshot contains PII | Reshoot with anonymised referential |
