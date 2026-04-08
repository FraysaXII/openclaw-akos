# HLK KM plan — follow-up checklist (avoid duplicate work)

Use this after the initial Topic–Fact–Source / Output 1 rollout. **Do not** re-author the KM contract, templates, pilot bundle, or `validate_hlk_km_manifests.py` unless requirements change.

## Done in baseline rollout

- [x] `HLK_KM_TOPIC_FACT_SOURCE.md` + PRECEDENCE row + Drive vs repo notes  
- [x] `v3.0/index.md` KM section + `_assets/` convention  
- [x] Topic template + visual manifest example  
- [x] PMO `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` (reconciled to primary Trello JSON slice)  
- [x] Trello exports under `PMO/imports/` (primary / archive / full)  
- [x] `docs/wip/hlk-km/` syntheses + `docs/wip/README.md` + `planning/_proposals/` for loose `.plan.md`  
- [x] `scripts/validate_hlk_km_manifests.py` + DEVELOPER_CHECKLIST / CONTRIBUTING / README  
- [x] UAT Scenario 8 in `docs/uat/hlk_admin_smoke.md`  

## When to run again (incremental)

| Trigger | Actions |
|---------|---------|
| New Trello cards for research backlog | Update primary JSON in `imports/`, add registry row(s), link wip synthesis if `in_wip`. |
| New Output 1 assets | Add raster + `*.manifest.md` + stub; run `py scripts/validate_hlk_km_manifests.py`. |
| Promotion to v3.0 | Update registry `promoted_v3` + path; follow [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md). |
| Compliance CSV / taxonomy edit | `py scripts/validate_hlk.py` + operator approval gates per governance rules. |

## Verification (minimal)

```bash
py scripts/validate_hlk.py
py scripts/validate_hlk_km_manifests.py
```

Full matrix: [docs/DEVELOPER_CHECKLIST.md](../../../../DEVELOPER_CHECKLIST.md).
