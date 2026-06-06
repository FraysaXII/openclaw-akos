# Runbook — MS Demo Factory Method A (Azure CLI + pac)

> Paired with `SOP-DATA_MS_DEMO_FACTORY_001.md` · method `MS-DEMO-METHOD-A` ·
> registry `akos/hlk_ms_demo_methods.py`.

## When to use

- Repeatable solution export/import between Holistika environments.
- Operator wants git-tracked **manifest** (solution name, component list) while flows stay in tenant.
- CI or AIC-driven steps after operator completes `az login`.

## Prerequisites

- Holistika Microsoft tenant credentials via env / vault (never commit secrets).
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and
  [Power Platform CLI (`pac`)](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction).
- Engagement scaffold signed; `power_platform` adapter row exists (may activate in same tranche).

## Procedure

### 1. Authenticate (operator gate)

```powershell
az login
pac auth create --environment https://<org>.crm4.dynamics.com
pac org list
```

Operator confirms correct environment before AIC continues.

### 2. Baseline or export existing solution

```powershell
mkdir -p export/<engagement-slug>
pac solution export --name <SolutionUniqueName> --path export/<engagement-slug>/
```

Record solution unique name in engagement `00-internal/build-log.md`.

### 3. Build components in tenant

Per demo spec (e.g. SUEZ F-05):

| Component | pac / portal action |
|:---|:---|
| Excel referential | Upload to SharePoint; note site URL in build log (not secrets) |
| Canvas app | Create in maker portal or import from solution |
| Cloud flow | Email trigger → compose libellé logic → write output |
| Connection references | Refresh after import; operator approves connectors |

Git tracks **manifest only** — solution zip or component list under `00-internal/ms-manifest/`, not live flow definitions in AKOS root.

### 4. Validate with fixtures

Run ≥3 anonymised fixture emails through the flow; compare output to demo spec § worked examples.
Log pass/fail in build log.

### 5. Registry + readiness

```powershell
py scripts/bi_integration_readiness_check.py --report
py scripts/validate_bi_consumer_registry.py
py scripts/validate_adapter_registries.py
```

### 6. Evidence

Export screenshots to `00-internal/evidence/<date>-method-a/`. No prior-client imagery.

## AIC posture

AIC may run steps 2–5 after operator completes step 1. Operator must approve connector consent dialogs and environment selection.

## Escalation

| Blocker | Escalate to |
|:---|:---|
| pac auth / licensing | System Owner |
| Registry FK failure | Data Governance Office |
| Demo logic mismatch vs spec | RevOps Manager + engagement owner |
