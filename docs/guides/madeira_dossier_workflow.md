# MADEIRA dossier workflow

**Audience:** operators producing or reading a MADEIRA-focused UAT dossier.

Canonical verdict **what**: [SOP-MADEIRA_VERDICT_AND_CADENCE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_VERDICT_AND_CADENCE_001.md). Section inventory and renderer contracts: [`docs/wip/planning/48-operator-dossier/dossier-section-spec.md`](../wip/planning/48-operator-dossier/dossier-section-spec.md).

## Emitting a MADEIRA-flavored dossier

Saved profile flag (composer over persona × initiative × skill):

```bash
py scripts/render_uat_dossier.py --filter madeira --mode live --format all
```

Dry runs and narrower formats behave like the default dossier CLI; `--filter madeira` only changes the baked filter set and MADEIRA-specialized Section 1 (three-light executive verdict) plus Section 8 extensions when flavor is recorded.

Compliance mirror row for the run carries `flavor='madeira'` plus per-light status fields where implemented.

## How to read Section 1 (three lights)

| Light | Question it answers |
|:------|:--------------------|
| Conversational | Do eval rubric + judge signals meet Initiative 49 thresholds on the MADEIRA personas in filter scope? |
| Operator | Are HTTP scenario-0 and dated UAT reports green inside freshness windows (and Docker readiness when Tier-3 applies)? |
| Surface | Does control-plane UX evidence pack (critique artefact path, accessibility signal, localization signal) satisfy the Surface lane checklist? |

GO requires all three green; otherwise treat as NO-GO and route through [SOP-MADEIRA_INCIDENT_RESPONSE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_INCIDENT_RESPONSE_001.md) when regressions need containment.

Cadence thresholds (weekly cost envelopes, drift limits): Part H table in [`MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](../wip/planning/02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md).

## Acting on regressions by section

- **Sections 5–7 (quality / adversarial / drift):** rerun targeted [`scripts/eval.py`](../../scripts/eval.py) slices for the personas named in Section 1; compare with Langfuse slices using [`madeira_langfuse_dashboard.md`](madeira_langfuse_dashboard.md) (Initiative 49 P13 saved view).
- **Section 4 (calibration):** revisit `lifecycle_status`, `quarantined` table, `priority_score` ordering for hot spots.
- **Section 8 (operational health + MADEIRA Surface UX):** read linked critique markdown, axe summary, offline brand lint output; route UI fixes through `static/madeira_control.html` ownership and UX SOP quarterly window when not emergent.

## Evidence layout

Prefer Initiative 49 closure pattern: artifact directory under `artifacts/uat-dossier/` named with UTC stamp; link it from Initiative 49 `reports/uat-i49-madeira-management-YYYY-MM-DD.md` when filing closure evidence.
