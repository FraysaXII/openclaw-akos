# MADEIRA Lookup Hardening Report

**Source plan**: `C:\Users\Shadow\.cursor\plans\madeira_lookup_hardening_a13d1a4e.plan.md`
**Timeline**: 2026-04-03
**Outcome**: **GO WITH RESIDUAL** -- direct lookup and ranked-search flows are hardened and governed gates pass; live escalation wording still drifts into planning-style clarification on `qwen3:8b`
**Author**: MADEIRA (Lookup hardening execution)

---

## 1. Executive Summary

This remediation followed the gateway-alignment work and closed the next-layer lookup UX defects in Madeira. The HLK service now resolves normalized role/process queries deterministically, returns ranked search results with explicit `best_role` / `best_process` winners, narrows Madeira's runtime profile to a lookup-appropriate `minimal` surface, and exposes real agent-specific drift data through the API instead of a placeholder response.

The governed verification matrix is green. Live browser UAT now proves that direct lookup and explicit search-form wording both produce grounded canonical answers. One residual remains: a pure restructuring request still tends to drift into clarification/planning language instead of immediately escalating to Orchestrator in the live `qwen3:8b` session surface.

## 2. Delivery Scope Completed

| Area | Result |
|------|--------|
| HLK lookup semantics | `akos/hlk.py` now normalizes lookups, ranks search results, and returns `best_role` / `best_process` for deterministic resolution |
| Madeira runtime posture | `config/agent-capabilities.json` and `config/openclaw.json.example` now keep Madeira on a narrower `minimal` runtime surface with curated `read`, memory lookup, finance, and HLK tools |
| Madeira prompt contract | Lookup ladder, same-turn retry, search silence, role-answer field requirements, and internal-tool leakage suppression were tightened in `prompts/base/MADEIRA_BASE.md` and `prompts/MADEIRA_PROMPT.md` |
| Repo-wide parity fixes | `/agents/{id}/capability-drift` now returns live drift issues; base prompt startup wording now uses `read`; Verifier prompt labeling/tool wording is closer to runtime truth; Executor/Verifier browser exposure now matches their validation role |
| Docs and governance sync | Architecture, user guide, SOP, security policy, UAT guidance, roadmap mirror, runtime UX report, changelog, and governance/doc-sync rules now reflect the lookup-hardening contract |

## 3. Verification Matrix

| Check | Result | Evidence |
|-------|--------|----------|
| `py scripts/bootstrap.py --skip-ollama` | PASS | Rebuilt config and all 15 prompts; synced runtime profiles including Madeira `minimal` |
| `py scripts/doctor.py` | PASS | `46 PASS`, `0 FAIL`, `1 WARN`; Madeira profile aligned as `minimal`; plugin synced |
| `py scripts/legacy/verify_openclaw_inventory.py` | PASS | Strict inventory contract preserved |
| `py scripts/check-drift.py` | PASS | No drift detected |
| `py -m pytest tests/test_hlk.py -q` | PASS | `51 passed` |
| `py -m pytest tests/validate_prompts.py -q` | PASS | `33 passed` |
| `py -m pytest tests/test_api.py tests/validate_configs.py tests/test_bootstrap_full_inventory.py tests/validate_prompts.py -q` | PASS | `110 passed` |
| `py scripts/test.py all` | PASS | `394 passed`, `2 skipped`, `1 warning` |
| `py -m pytest tests/test_api.py -v` | PASS | `18 passed`, `1 warning` |
| `py scripts/validate_hlk.py` | PASS | `OVERALL: PASS`; `Org roles: 65`, `Process items: 317` |
| `py scripts/browser-smoke.py --playwright` | SKIP | Playwright worker crashes on this host (`3221225477`) -> all six scenarios SKIP, zero FAIL |
| `py scripts/release-gate.py` | PASS | Verdict `PASS` |

## 4. Live Browser UAT Evidence

### 4.1 Direct lookup (`live-uat-10`)

Prompt: `Who is the CTO?`

Observed result:
- Madeira called `hlk_role("CTO")`
- Returned direct grounded answer
- Included access level `5`
- Cited `baseline_organisation.csv`
- Did not leak `hlk_role`, `hlk_search`, `best_role`, or raw query strings in the final answer

### 4.2 Explicit search wording (`live-uat-13`)

Prompt: `Search HLK for CTO and return the closest canonical role.`

Observed result:
- Madeira resolved the closest canonical role to `Chief Technology Officer (CTO)`
- Included description, access level, reports-to chain, area, entity, and SOP link
- Cited `baseline_organisation.csv`
- Did not leak internal tool/source identifiers in the final answer

### 4.3 Escalation boundary (`live-uat-14`)

Prompt: `I need to restructure the Finance area.`

Observed result:
- Madeira remained read-only and did not mutate anything
- Madeira did **not** mention Orchestrator or explicitly escalate
- Instead it drifted into planning-style clarification and restructuring questions

Interpretation:
- The hard safety boundary held
- The operator-facing escalation UX still needs one more iteration for this specific request class on the live `qwen3:8b` model

## 5. Residual Risks

- **Live escalation wording drift**: restructuring/admin requests can still turn into clarification/planning questions instead of immediate escalation language.
- **Post-compaction audit friction**: follow-up turns in long-lived sessions may be interrupted by startup-file recency audits, especially around missing dated memory files. This did not block first-turn lookup validation but still affects operator smoothness.
- **OpenClaw plugin provenance warning**: `openclaw plugins list` still warns that `akos-runtime-tools` is a local global plugin without install/load-path provenance, even though AKOS config trusts it and doctor/drift pass.
- **Playwright worker instability on this host**: browser-smoke remains SKIP-only because local browser workers exit with `3221225477`.

## 6. Final Verdict

The Madeira Lookup Hardening program is implementation-complete for:

- deterministic direct lookup
- deterministic search-form resolution
- runtime/profile narrowing
- real drift visibility
- repo/doc parity hardening
- governed automated verification

The remaining open item is a live-model UX residual on the escalation branch, not a runtime bridge or inventory contract defect. Treat the program as **GO WITH RESIDUAL** and track one follow-up pass focused on read-only escalation wording plus post-compaction audit smoothness.
