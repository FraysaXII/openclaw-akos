---
language: en
status: closed
initiative: 58-cycle-2-multi-track-forward
phase: D.2
report_kind: closure
program_id: shared
plane: tech
authority: System Owner
last_review: 2026-05-05
---

# I58 D.2 — RunPod / Kalavai alias seam in `runpod_provider.py`

**Date**: 2026-05-05
**Phase**: I58 D.2 (engineering hygiene)
**Phase ref**: cycle_2_multi-track_forward_(i58)_769da1a3.plan.md → todo `d2_runpod_alias`
**Decision**: D-IH-58-G (alias seam, `VLLM_*` wins precedence)
**Verdict**: **GREEN — alias seam shipped + 8 new precedence tests + doc-sync complete**

---

## 1. Scope

I58 D.2 implements the alias seam decided under D-IH-58-G: external tools and the long-lived `~/.openclaw/.env` block (written under I58 P0) refer to GPU endpoints by alias names (`RUNPOD_ENDPOINT_URL`, `KALAVAI_ENDPOINT_URL`), while the AKOS runtime canonicalizes on `VLLM_*`. The seam ensures a single resolution path with **fixed precedence: canonical wins**, never the other way around.

Per the user's "design for invariance + SSOT + deduplication" preferences, this is implemented as a single helper `resolve_endpoint_url(kind)` in `akos/runpod_provider.py` rather than scattered `os.environ.get` calls.

## 2. Engineering deliverables (this commit)

### 2.1 Helper function — `akos/runpod_provider.py`

Added `resolve_endpoint_url(kind, *, env=None) -> str` and the module-private mapping `_ENDPOINT_URL_ALIASES`:

```python
_ENDPOINT_URL_ALIASES: dict[str, tuple[str, ...]] = {
    "runpod": ("VLLM_RUNPOD_URL", "RUNPOD_ENDPOINT_URL"),
    "shadow": ("VLLM_SHADOW_URL", "KALAVAI_ENDPOINT_URL"),
}
```

Behavior:

- Returns the first non-empty env var in the canonical → alias precedence chain.
- Empty alias values never shadow a populated canonical (precedence is by *value populated*, not by *key present*).
- Returns `""` when neither is set.
- Raises `ValueError` for unknown `kind`.
- Optional `env=` parameter for testability (defaults to `os.environ`).

### 2.2 Consumer migration — `akos/api.py`

The `/health` endpoint previously called `os.environ.get("VLLM_RUNPOD_URL", "")` directly. Replaced with `resolve_endpoint_url("runpod")` so the alias seam takes effect for the gateway health probe — operators who paste `RUNPOD_ENDPOINT_URL` into `~/.openclaw/.env` (per the I58 P0 long-lived block) get the same `/health` payload as those who set `VLLM_RUNPOD_URL`.

### 2.3 Tests — `tests/test_runpod_provider.py`

Added `TestEndpointUrlAliasSeam` class with 8 tests pinning precedence:

1. `test_runpod_canonical_wins_over_alias` — both set, canonical wins.
2. `test_runpod_alias_used_when_canonical_unset` — only alias set, alias wins.
3. `test_runpod_empty_canonical_falls_through_to_alias` — empty canonical falls through.
4. `test_runpod_returns_empty_when_neither_set` — both unset, empty string.
5. `test_shadow_canonical_wins_over_alias` — symmetric for Kalavai.
6. `test_shadow_alias_used_when_canonical_unset` — symmetric for Kalavai.
7. `test_unknown_kind_raises_value_error` — guard rail.
8. `test_default_env_uses_os_environ` — default arg semantics.

These tests lock in the precedence contract per R-58-8 ("Env-var alias seam inverts precedence and breaks gateway → +1 unit test asserting `VLLM_*` wins").

### 2.4 Doc-sync

Per `.cursor/rules/akos-docs-config-sync.mdc`, three docs received synchronized updates:

1. **`config/environments/dev-local.env.example`** — new commented "Endpoint URL alias seam (D-IH-58-G)" block under the inactive-provider section. Aliases are commented in dev-local because the canonical names are sufficient locally; the aliases live in `~/.openclaw/.env` for external-tool compatibility.

2. **`docs/ARCHITECTURE.md`** — new "Endpoint URL alias seam (D-IH-58-G)" subsection under "Environment Placeholder Hardening", with the canonical→alias table and pointer to the helper.

3. **`docs/USER_GUIDE.md`** — new §8.7.1 "Endpoint URL alias seam (D-IH-58-G)" with a code snippet showing the helper API and the precedence rule explained in operator-friendly terms.

## 3. Verification

```powershell
py -m pytest tests/test_runpod_provider.py tests/test_api.py -q
```

**Result**: `57 passed in 28.04s` — **PASS** (29 in `test_runpod_provider.py` including the 8 new precedence tests; 28 in `test_api.py` confirming the `/health` endpoint still passes after the consumer migration).

Linter: `ReadLints` reports **no errors** on the three modified Python files.

## 4. Governance

- **Asset classification** (per `akos-governance-remediation.mdc`):
  - Edited (engineering): `akos/runpod_provider.py`, `akos/api.py`, `tests/test_runpod_provider.py`.
  - Edited (config): `config/environments/dev-local.env.example`.
  - Edited (docs): `docs/ARCHITECTURE.md`, `docs/USER_GUIDE.md`.
  - Created: this report.
  - **No** edits to canonical CSVs → no operator-SQL gate triggered.
- **SSOT / DI / SOC / DX / UX** (per user rules + `akos-governance-remediation.mdc`):
  - **SSOT**: single helper `resolve_endpoint_url` is the only place env-var → URL resolution happens for these two endpoint families.
  - **DI (Design for Invariance)**: precedence is fixed by data structure (`_ENDPOINT_URL_ALIASES` ordered tuple); inverting the chain requires touching the constant and breaks the 8 precedence tests.
  - **SOC**: helper is module-private mapping + pure function; no globals mutated; no I/O.
  - **DX**: optional `env=` parameter for tests; `ValueError` for unknown kind catches typos at import time.
  - **UX**: single docs source (USER_GUIDE §8.7.1) explains the rule without leaking implementation jargon.
- **No duplication**: `os.environ.get("VLLM_RUNPOD_URL", "")` is no longer scattered in `api.py`; the only remaining direct reference is the placeholder dict in `akos/io.py` (deliberately, since that's the runtime placeholder contract, not URL resolution).
- **Commit discipline**: this commit covers D.2 only (helper + migration + tests + 3 docs + this report). E.0 ships separately. No mixed concerns.

## 5. Risk reduction (R-58-8 retired)

R-58-8 (env-var alias seam inverts precedence and breaks gateway) is **retired** by:

- The 8 precedence tests in `TestEndpointUrlAliasSeam`.
- Single-line revert path: replace the helper call in `api.py` back to `os.environ.get("VLLM_RUNPOD_URL", "")` — no other consumer migrated.
- Doc trail in ARCHITECTURE.md + USER_GUIDE §8.7.1 + dev-local.env.example explicitly state precedence.

## 6. Roll-up

- **I58 todo**: `d2_runpod_alias` → **completed**.
- **Cycle progress**: P0, A.0-A.5 (OPS-58-1), B.1-B.4, C.1, D.1, D.2 complete. Remaining: E.0 (closure UAT).
- **Next action**: proceed to E.0 (closure UAT, status flips, dashboard re-render, CHANGELOG roll-up).

---

**Author**: Agent (Cursor / I58 D.2 step)
**Reviewer**: Operator (implicit, via I58 plan approval)
**Status**: D-IH-58-G alias seam shipped; R-58-8 retired; doc-sync complete.
