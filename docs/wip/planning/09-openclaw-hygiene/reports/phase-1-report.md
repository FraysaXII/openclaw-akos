# Phase 1 report — OpenClaw hygiene (initiative 09)

**Date:** 2026-04-16

**Note:** Subsequent **initiative 10** work superseded the `tools.exec.host` / sandbox defaults and Path C tool stripping described here; see [`master-roadmap.md`](../master-roadmap.md) supersession paragraph.

## Delivered

- Planning mirror: `docs/wip/planning/09-openclaw-hygiene/` + README index row **09**.
- `config/openclaw.json.example`: removed `gateway.controlUi`; `tools.exec.host` set to `gateway`.
- `akos/models.py`: `GatewayConfig.controlUi` optional; `ExecConfig.host` default `gateway`.
- Docs: `USER_GUIDE` §3.3.1, §14.3 expansion; `SECURITY` audit summary; `CONTRIBUTING` CLI upgrade section; `ARCHITECTURE` gateway notes; `SOP` §9.11 exec bullet; `workspace-scaffold/README`; `README` pointer; `CHANGELOG` [Unreleased].
- Tests: `tests/test_akos_models.py` gateway defaults; `tests/validate_configs.py` exec host + no `controlUi`.

## Verification

Run governed matrix from repo root before merge (see `docs/DEVELOPER_CHECKLIST.md`).
