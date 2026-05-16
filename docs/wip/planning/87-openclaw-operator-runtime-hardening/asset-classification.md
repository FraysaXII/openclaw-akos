---
initiative_id: I87
language: en
last_review: 2026-05-16
---

# I87 — Asset classification

Per [`PRECEDENCE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md).

## Canonical (edit-here-first; canonical-CSV gates apply)

| Asset | Phase | Gate | Notes |
|:---|:---|:---|:---|
| `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` | P5 | operator approval | New SOP minted under Tech/System Owner area + role |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv` (one row append: `env_tech_sop_openclaw_runtime_health_triage_001`) | P5 | operator approval (canonical CSV gate per `akos-governance-remediation.mdc`) | SOP-META order — CSV before SOP `status: active` flip |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` (one row append: `INIT-OPENCLAW_AKOS-87`) | P0 | operator approval | Promotes candidate to active |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` (three rows append: D-IH-87-A/B/C) | P0 | operator approval | Charter decisions |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv` (one row append: `OPS-87-1`) | P0 | operator approval | Open action: validator wiring follow-up |

## Mirrored / derived (auto-rendered from canonicals)

| Asset | Source | Renderer |
|:---|:---|:---|
| `docs/wip/planning/OPERATOR_INBOX.md` | `OPS_REGISTER.csv` | `scripts/render_operator_inbox.py` |
| `docs/wip/planning/WIP_DASHBOARD.md` | per-initiative `master-roadmap.md` frontmatter | `scripts/render_wip_dashboard.py` |
| Supabase `compliance.initiative_registry_mirror` / `compliance.decision_register_mirror` / `compliance.ops_register_mirror` | three canonical CSVs above | `scripts/sync_compliance_mirrors_from_csv.py` |

## Reference-only (no compliance gate)

| Asset | Notes |
|:---|:---|
| `docs/wip/intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md` | Evidence SSOT; WIP — not promoted to canonical |
| `~/.openclaw/openclaw.json` (operator-local) | Per-operator state; documented in P2 template; not git-canonical |
| `~/.openclaw/modelsConfig.yaml` (operator-local) | Per-operator state; documented in P3; not git-canonical |
| OpenClaw upstream code (any repo path under `openclaw/` from upstream) | Not Holistika-canonical; P4 may file upstream ticket but not modify |

## Scripts and tests (engineering surface; not compliance-canonical but governed by [`CONTRIBUTING.md`](../../../CONTRIBUTING.md))

| Asset | Phase | Compliance contract |
|:---|:---|:---|
| `scripts/validate_openclaw_plugin_pinning.py` | P2 | Pydantic model in `akos/openclaw_plugin_allow.py`; tests under `tests/test_validate_openclaw_plugin_pinning.py`; wired into `release-gate.py` as INFO |
| `scripts/openclaw_health_triage.py` (paired runbook for P5 SOP) | P5 | Pydantic model in `akos/openclaw_health_triage.py`; tests; wired into `process_list.csv` runbook column |
