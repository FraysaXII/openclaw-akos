# Initiative 09 — OpenClaw hygiene (gateway SSOT, security audit, bootstrap, CLI updates)

**Source:** `.cursor/plans/openclaw_hygiene_triad_66fa92e1.plan.md`  
**Last synced:** 2026-04-16  
**Status:** execution mirror (non-canonical; canonical planning workflow remains in Cursor plan until this file is updated each phase).

**Supersession (2026-04):** Live gateway SSOT and Path B/C tool policy are tracked in **[initiative 10](../10-madeira-eval-hardening/master-roadmap.md)** (`sandbox.mode` + `tools.exec.host: sandbox`, no `web_search`/`web_fetch` on orch/arch). The **decision log below** retains the earlier hygiene triad record; treat **D1–D2** as historical unless reconciled in a future edit.

## Scope

- Align `config/openclaw.json.example` with OpenClaw **2026.4.x** schema (remove unsupported `gateway.controlUi.title`).
- Coherent **`tools.exec.host`** vs sandbox story for native Windows / dev-local (SSOT defaults).
- Document **`openclaw security audit`** CRITICAL/WARN interpretation (Path A/B/C) in USER_GUIDE / SECURITY.
- Document **SOUL.md / bootstrap file** operator path for all five agents.
- Document **`openclaw update`** maintenance checklist in CONTRIBUTING.
- Optional: `gateway.nodes.denyCommands` exact IDs; `trustedProxies` when behind reverse proxy.

## Asset classification

See [docs/references/hlk/compliance/PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md). This initiative does **not** change canonical HLK compliance CSVs or vault markdown.

## Decision log (execution record)

| ID | Decision |
|----|------------|
| D1 | **Path A (primary):** Document OpenClaw CRITICAL/WARN interpretation in USER_GUIDE §14.3 and SECURITY; retain curated read-only web tools in SSOT for Orchestrator/Architect on dev-local loopback. Paths B/C remain operator options per matrix. |
| D2 | **`tools.exec.host: "gateway"`** in `openclaw.json.example` (and `ExecConfig` default) to align with sandbox-off dev-local; avoids "sandbox exec host with sandbox.mode off" audit warning without claiming a missing sandbox runtime. |
| D3 | **`gateway.controlUi` removed** from SSOT JSON; `GatewayConfig.controlUi` optional in Pydantic (upstream rejected `title`). |
| D4 | **`gateway.nodes.denyCommands`:** no template rows in SSOT; document exact-ID requirement in SECURITY (defer live edits to operator). |

## Verification matrix

Per [docs/DEVELOPER_CHECKLIST.md](../../../DEVELOPER_CHECKLIST.md): inventory verify, check-drift, test.py all, browser-smoke, test_api, release-gate; HLK validators N/A unless scope expands.

## Reports

Place phase completion notes under [`reports/`](reports/).
