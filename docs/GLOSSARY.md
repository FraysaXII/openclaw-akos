# Glossary (AKOS + HLK + ops)

One-line pointers; deep definitions live in linked docs. **SSOT** for verification commands: [config/verification-profiles.json](../config/verification-profiles.json) and [DEVELOPER_CHECKLIST](DEVELOPER_CHECKLIST.md).

| Term | Meaning / pointer |
|:-----|:------------------|
| **AKOS** | Agentic Knowledge Operating System — this repo’s control plane, prompts, and HLK alignment on top of [OpenClaw](https://github.com/openclaw/openclaw). See [ARCHITECTURE](ARCHITECTURE.md). |
| **AkosState** | Persisted session/agent state; includes routes like Madeira `madeiraInteractionMode`. See [ARCHITECTURE](ARCHITECTURE.md). |
| **Control plane** | FastAPI app (`akos/api.py`, `serve-api`) on port 8420 — agents, health, HLK HTTP API; distinct from the OpenClaw **gateway** UI port. |
| **Eval (agent eval)** | Offline or live checks over `tests/evals/suites/<id>/`; **rubric** mode scores golden text. See [tests/evals/README](../tests/evals/README.md). |
| **Governance rubric suites** | Eval suite directory names in `eval_rubric_governance_suites` in [verification-profiles.json](../config/verification-profiles.json); same set as `AKOS_EVAL_RUBRIC=1` in [release-gate](../scripts/release-gate.py) and `run-evals --governance-rubric`. |
| **HLK** | Holistika’s organisational/process **registry** and vault (roles, areas, `process_list.csv`, v3.0 markdown). See [ARCHITECTURE](ARCHITECTURE.md) HLK sections, [USER_GUIDE](USER_GUIDE.md). |
| **Initiative** | A numbered folder under [wip/planning](wip/planning/README.md) (`NN-…`) with roadmap, decision log, and reports. |
| **Madeira (agent)** | User-facing HLK lookup / escalation agent in the 5-agent stack. |
| **Mirror (compliance)** | DB or derived copy of a canonical CSV; writes follow operator approval and SOP. See [PRECEDENCE](references/hlk/compliance/PRECEDENCE.md). |
| **MCP** | Model Context Protocol server — tool surface for the gateway; AKOS lists several in [README](../README.md). |
| **OpenClaw** | Upstream gateway + channels product; AKOS customizes via repo config and bootstrap. |
| **PRECEDENCE** | [references/hlk/compliance/PRECEDENCE.md](references/hlk/compliance/PRECEDENCE.md) — which artefacts are canonical vs mirrored vs reference-only. |
| **pre_commit (profile)** | Named verification **profile** in [verification-profiles.json](../config/verification-profiles.json) — run via `py scripts/verify.py pre_commit`. |
| **Profile (verification)** | A named list of **steps** (each with `id` + `argv`) in the verification registry. |
| **Release gate** | [scripts/release-gate.py](../scripts/release-gate.py) — inventory, tests, drift, browser smoke, API smoke, HLK validators, optional rubric evals. |
| **ShadowGPU** | Shadow’s **cloud** GPU service (OpenStack tenant: API, Horizon, floating IP, vLLM on instances). The `gpu-shadow` profile targets this. Not the same as **ShadowPC** (local Windows machine). |
| **ShadowPC** | Shadow’s **local** Windows PC / streaming product for dev or gaming — not the OpenStack cloud. |
| **SSOT** | Single source of truth — one authoritative artefact; others link or generate from it. Contrast with planning mirrors under `docs/wip/`. |
| **SSOT (runtime)** | Repo config + `~/.openclaw` materialized state; see [ARCHITECTURE](ARCHITECTURE.md) responsibility matrix. |
| **UAT** | User acceptance testing — may include human browser / qualitative checks; **not** fully replaced by automated smoke. See planning rule `akos-planning-traceability.mdc`. |
| **FINOPS counterparty register** | Git CSV `FINOPS_COUNTERPARTY_REGISTER.csv` + mirror `compliance.finops_counterparty_register_mirror`; vendor/customer/partner metadata only (no amounts). See [PRECEDENCE](references/hlk/compliance/PRECEDENCE.md), Initiative 18 roadmap. |
| **Stripe FDW (`stripe_gtm`)** | Supabase Wrappers read projection of Stripe (e.g. schema `stripe_gtm`, server `stripe_gtm_server`); API authoritative; server-only access. See Initiative 18 runbook. |
| **Vault (HLK v3.0)** | Tree under [references/hlk/v3.0](references/hlk/v3.0/index.md) (SOPs, narratives). |
| **Verification registry** | [config/verification-profiles.json](../config/verification-profiles.json) + loader [akos/verification_profiles.py](../akos/verification_profiles.py). |
| **WIP** | Work in progress under [docs/wip](wip/README.md) — not treated as final release documentation. |

---

*Add a term when it appears in three or more first-class docs, or when onboarding feedback repeats the same question.*
