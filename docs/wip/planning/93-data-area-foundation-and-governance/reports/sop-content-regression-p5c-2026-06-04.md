---
intellectual_kind: regression_report
initiative: I93
phase: P5c
authored: 2026-06-04
verdict: remediated_pre_commit
---

# P5c SOP content regression — pre-commit review

## Scope

Content-quality review (not mechanical validators) of I93 P5c integration SOP family:

| Artifact | Role |
|:---|:---|
| `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md` | Upstream gate |
| `SOP-DATA_MS_DEMO_FACTORY_001.md` + addendum | MS Phase 1 build |
| `SOP-DATA_PRODUCTION_READINESS_001.md` | Engagement-funded production |
| `SOP-DATA_SUEZ_STREAM_B_LIBELLE_001.md` | SUEZ F-05 scenario |
| Runbooks `ms-demo-cli-method-a.md`, `ms-demo-browser-method-b.md` | Method execution |

**Quality bar:** `SOP-DATA_LINEAGE_001.md`, `SOP-RESEARCH_ACTION_001.md` (Purpose → Scope → Inputs → Steps HUMAN/AUTOMATION → Failure modes → Outputs → Cross-refs).

## Findings (pre-remediation)

| ID | Severity | Finding |
|:---|:---|:---|
| SOP-CQ-01 | **Blocker** | Broken YAML frontmatter — blank line between every field on 4 SOPs (parser-fragile; unlike vault exemplars) |
| SOP-CQ-02 | **Blocker** | Body double-spacing — every paragraph separated by blank line pair; reads auto-generated |
| SOP-CQ-03 | **Major** | Missing **Inputs**, **Failure modes**, **Outputs** on all P5c SOPs |
| SOP-CQ-04 | **Major** | AC-HUMAN / AC-AUTOMATION not split into executable step lists with commands |
| SOP-CQ-05 | **Major** | MS demo factory workflow = 6 stub bullets; no roles, no fixture validation, no IP policy |
| SOP-CQ-06 | **Major** | Production readiness methods had no selection logic, hardening detail, or funding gate |
| SOP-CQ-07 | **Major** | SUEZ SOP filename implied Edge-primary; conflicted with D-IH-93-J Phase 1 MS binding |
| SOP-CQ-08 | **Major** | Three "stream" vocabularies conflated (DATA A/B/C, SUEZ commercial A/B, Phase 1/2) |
| SOP-CQ-09 | **Minor** | Runbooks = 5 generic bullets; no SUEZ F-05 component table, escalation, or combine A+B guidance |
| SOP-CQ-10 | **Minor** | Scaffold lacked failure modes and downstream routing to new SOPs |

## Remediation applied (2026-06-04)

- Rewrote all five SOP bodies + addendum to exemplar structure.
- Fixed frontmatter to compact YAML.
- Added stream disambiguation table (addendum + SUEZ purpose note).
- Grounded Holistika-tenant build in post-handshake source grounding §3.2, §5.
- Expanded runbooks with procedures, tables, escalation, Method A+B combination pattern.
- Updated scaffold `last_review_decision_id` to D-IH-93-J.

## Post-remediation verification

```powershell
py scripts/validate_hlk.py          # OVERALL PASS (run before commit)
py -m pytest tests/test_ms_demo_methods.py -v
```

## Residual follow-ups (not blockers for P5c commit)

| Item | Suggestion |
|:---|:---|
| Rename `SOP-DATA_SUEZ_STREAM_B_*` file to `SOP-DATA_SUEZ_LIBELLE_001` | ✅ Done — full ripple (process_list, pairing, PRECEDENCE, CANONICAL_REGISTRY) |
| `akos/hlk_production_readiness_methods.py` | Optional parity with MS demo method registry |
| KNOWLEDGE_PAIRING_REGISTRY rows for new SOP pairs | Index tranche with commit |

## Verdict

**Ready for operator review before commit** — content bar aligned with lineage/research-action SOPs; mechanical gates pass.
